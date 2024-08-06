import json
from Header.OptionManager import _LOG
from openal import *

class MusicManager:
    def __init__(self):
        oalInit()
        config = self.InitConfig()
        self._VOLUME = _LOG._CONFIG['volume']
        self._MUSIC_DICTIONARY = {
            'MUSIC_BG_1' : oalOpen(config['music']['aria_math']),
            'MUSIC_BG_2' : oalOpen(config['music']['calm']),
            'MUSIC_BG_3' : oalOpen(config['music']['living_mice']),
            'MUSIC_BG_4' : oalOpen(config['music']['moog_city']),
            'MUSIC_BG_5' : oalOpen(config['music']['stal']),
            'MUSIC_BG_6' : oalOpen(config['music']['subwoofer_lullaby']),
            'MUSIC_BG_7' : oalOpen(config['music']['sweden']),
            'MUSIC_BG_8' : oalOpen(config['music']['wet_hands'])
        }


    def InitConfig(self):
        with open("./Music/Musics.json", 'r') as File:
            return json.load(File)

    def PlayMusic(self, bg_name : str):
        self._MUSIC_DICTIONARY[bg_name].set_looping(True)
        self._MUSIC_DICTIONARY[bg_name].play()

    def StopMusic(self, bg_name : str):
        self._MUSIC_DICTIONARY[bg_name].stop()

    def Update(self):
        self._VOLUME = _LOG._CONFIG['volume']
        for audio in self._MUSIC_DICTIONARY:
            self._MUSIC_DICTIONARY[audio].set_gain(self._VOLUME)

    def Quit(self):
        for audio in self._MUSIC_DICTIONARY:
            self._MUSIC_DICTIONARY[audio].stop()
        oalQuit()


class SoundManager:
    def __init__(self):
        oalInit()
        config = self.InitConfig()
        self._VOLUME = _LOG._CONFIG['sound_volume']
        self._SOUND_DICTIONARY = {
            'SOUND_RESET_WARNING' : oalOpen(config['sounds']['ResetWarning']),
            'SOUND_RESET' : oalOpen(config['sounds']['Reset']),
            'SOUND_CLICK' : oalOpen(config['sounds']['Click']),
            'SOUND_ROCK' : oalOpen(config['sounds']['Rock']),
            'SOUND_PAPER' : oalOpen(config['sounds']['Paper']),
            'SOUND_SCISSORS' : oalOpen(config['sounds']['Scissors']),
            'SOUND_DRAW_1' : oalOpen(config['sounds']['Draw']),
            'SOUND_LOSE' : oalOpen(config['sounds']['Lose']),
            'SOUND_WIN' : oalOpen(config['sounds']['Win']),
        }

    def InitConfig(self):
        with open("./Sounds/Sounds.json", 'r') as File:
            return json.load(File)

    def PlaySound(self, sound_name : str):
        self._SOUND_DICTIONARY[sound_name].play()

    def StopSound(self, sound_name : str):
        self._SOUND_DICTIONARY[sound_name].stop()

    def Update(self):
        self._VOLUME = _LOG._CONFIG['sound_volume']
        for audio in self._SOUND_DICTIONARY:
            self._SOUND_DICTIONARY[audio].set_gain(self._VOLUME)

    def Quit(self):
        for audio in self._SOUND_DICTIONARY:
            self._SOUND_DICTIONARY[audio].stop()
        oalQuit()


# SoundManager Class
_SOUND_MANAGER = SoundManager()
_MUSIC_MANAGER = MusicManager()

# Update Managers
def SoundManagerUpdate():
    _SOUND_MANAGER.Update()
    _MUSIC_MANAGER.Update()

