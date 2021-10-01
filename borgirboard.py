import sys

import numpy as np
from PyQt5 import QtWidgets as qw
import PyQt5.QtCore as qc
import PyQt5.QtMultimedia as qm


def build_sounds():
    return {
        "clap"              : qm.QSound("sounds/clap.wav"),
        "laughing"          : qm.QSound("sounds/laughing.wav"),

        "Snail Eating"      : qm.QSound("sounds/snail_eating.wav"),
        "borgir"            : qm.QSound("sounds/borgir.wav"),
        "Grot"              : qm.QSound("sounds/grot_trim.wav"),

        "Goulet"            : qm.QSound("sounds/goulet.wav"),
        "Papa"              : qm.QSound("sounds/papa.wav"),
        "energy"            : qm.QSound("sounds/kamen_energy_trim.wav"),

        "gumball"           : qm.QSound("sounds/lpc_gumball.wav"),
        "gumball_timer"     : qm.QSound("sounds/lpc_gumball.wav"),
    }

class SoundButton(qw.QWidget):
    def __init__(self, name, soundfile):
        super(SoundButton,self).__init__()

        self.name = name
        self.button = qw.QPushButton(self)
        self.button.setGeometry(0,0,100,100)
        self.button.setText(name)
        self.button.clicked.connect(self.play_sound)

        self.soundfile = soundfile
        self.is_playing = False

    def play_sound(self):
        if self.soundfile.isFinished():
            self.is_playing = False

        if self.is_playing:
            self.soundfile.stop()
            self.is_playing = False
        else:
            self.soundfile.play()
            self.is_playing = True

class TimedSoundButton(SoundButton):
    def __init__(self, name, soundfile, seconds):
        super(TimedSoundButton,self).__init__(name, soundfile)

        self.timer = qc.QTimer()
        self.timer.timeout.connect(self.show_time)
        self.timer.start(1000 # 1 second)
        self.count = 0
        self.seconds = seconds + 1 # first second is skipped.

    def show_time(self):
        if self.count == 1:
            super().play_sound()
        if self.count > 0:
            self.count -= 1
        self.draw_pretty_time()

    def play_sound(self):
        self.count = self.seconds

    def draw_pretty_time(self):
        mins = self.count // 60
        secs = self.count % 60
        self.button.setText(f"{self.name}\n\n{mins}:{secs}")


def run():
    app = qw.QApplication(sys.argv)
    windows = qw.QWidget()

    windows.resize(500,500)
    windows.move(300,300)
    windows.setWindowTitle("SmorgasborgirBoard")

    layout = qw.QGridLayout()

    SOUND_FILES = build_sounds()

    NUM_COLS = 3
    GUMBALL_TIME = 15*60

    for i,(s_name,s_file) in enumerate(SOUND_FILES.items()):
        if s_name == "gumball_timer":
            btn = TimedSoundButton(s_name, soundfile=s_file, seconds=GUMBALL_TIME)
        else:
            btn = SoundButton(s_name, soundfile=s_file)
        layout.addWidget(btn, i // NUM_COLS, i % NUM_COLS, 1, 1)

    windows.setLayout(layout)

    windows.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    run()