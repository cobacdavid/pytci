__author__ = "david cobac"
__email__ = "david.cobac @ gmail.com"
__twitter__ = "https://twitter.com/david_cobac"
__github__ = "https://github.com/cobacdavid"
__copyright__ = "Copyright 2021, CC-BY-NC-SA"

# import YT
from pytube import YouTube
# récupération du rep. courant
import os
# pour effacer des répertoires non vides
import shutil
# traitement video avec
# opencv-python-headless
# la version opencv-python ne semble pas compatible
# avec matplotlib ou PIL ou ?
import cv2
# home
from pathlib import Path


class ytdown:

    """Class to handle a YT video download and extraction of images
    from this video.

    :param vid: YT video unique id
    :type vid: str
    :param step: step in seconds between two image extractions
    :type step: float


    **Attributes**
     - vid : str unique identifier of a YT video
     - step : float seconds between two image extractions

    **Methods**
     - down() : downloads the chosen YT video using its id as name
     - to_images() : extracts images from video every step seconds
                     and stores them into a pytci- directory

    """

    def __init__(self, vid, step=1):
        self._vid = vid
        self._url = f'http://youtube.com/watch?v={self.vid}'
        # chemin enregistrement
        self._path = Path.home()
        # _pas en millisecondes
        self._pas = step * 1_000
        self._qualite = None
        self._set_paths()
        self._init_yt()

    def _set_paths(self):
        self._vid_fullname = os.path.join(self._path, self._vid)
        self._img_dir = 'pytci-' + os.path.splitext(self._vid)[0]
        self._img_fulldir = os.path.join(self._path, self._img_dir)

    def _init_yt(self):
        self._yt = YouTube(self._url)

    @property
    def vid(self):
        return self._vid

    @vid.setter
    def vid(self, YT_vid_id):
        self._vid = YT_vid_id
        self._url = f'http://youtube.com/watch?v={self.vid}'
        self._set_paths()
        self._init_yt()

    @property
    def step(self):
        return self._pas / 1_000

    @step.setter
    def step(self, pas_en_s):
        self._pas = pas_en_s * 1_000

    def down(self):
        self._choix_qualite_min()
        self._down()

    def _choix_qualite_min(self):
        liste_qualite = self._yt.streams.filter(progressive="True")

        stream = None
        taille_min = float('inf')
        for s in liste_qualite:
            if s.type == 'video' and s.filesize < taille_min:
                taille_min = s.filesize
                stream = s

        self._qualite = stream.itag

    def _nb_chiffres_nb_photos(self):
        duree = self._yt.length
        # durée en s et pas en ms
        # nb_photos -> en faire un atrribut ?
        nb_photos = round(duree / (self._pas / 1_000))

        i = 0
        n = nb_photos
        while n > 1:
            i += 1
            n /= 10

        return i

    def _down(self):
        stream = self._yt.streams.get_by_itag(self._qualite)
        stream.download(output_path=self._path,
                        filename=self._vid)

    def to_images(self):
        repertoire = os.path.dirname(self._vid_fullname)
        #
        os.chdir(repertoire)
        #
        if os.path.isdir(self._img_dir):
            shutil.rmtree(self._img_dir)
        os.mkdir(self._img_dir)
        #
        capture_video = cv2.VideoCapture(self._vid)
        b, image = capture_video.read()
        compteur = 0
        N = self._nb_chiffres_nb_photos()
        while b:
            # position dans la video
            capture_video.set(cv2.CAP_PROP_POS_MSEC, compteur * self._pas)
            b, image = capture_video.read()
            if b:
                cv2.imwrite(
                    os.path.join(
                        self._img_dir,
                        "pytcimage-{:0{N}d}.jpg".format(compteur, N=N)
                    ),
                    image)
            else:
                break
            compteur += 1
