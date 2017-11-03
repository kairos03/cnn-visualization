# Copyright kairos03. All Right Reserved.

import sys
import time
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from components import DataLoader, ImgLabel


class SignalingThread(QThread):
    def __init__(self):
        super().__init__()
        self.input_data_loader = DataLoader()

    def __del__(self):
        super().__init__()
        self.wait()

    def input_loaded(self, path):
        self.input_data_loader.inputLoaded(path)

    def run(self):
        time.sleep(5)
        self.input_loaded('./data/ex1/input.png')
        time.sleep(5)
        self.input_loaded('./data/white.png')


class App(QDialog):

    def __init__(self, input_data_loader):
        super(App, self).__init__()
        self.input_data_loader = input_data_loader

        self.init_ui()

    def init_ui(self):
        l_img = ImgLabel(None, 200, 200)
        l_img.make_connection(self.input_data_loader.inputLoaded)

        lay = QVBoxLayout()
        lay.addStretch()
        lay.addWidget(l_img)
        lay.addStretch()

        self.setLayout(lay)
        self.setWindowTitle('Signal Slot Test')
        self.setGeometry(200, 200, 100, 100)

        self.show()


if __name__ == '__main__':
    st = SignalingThread()

    app = QApplication(sys.argv)
    ex = App(st.input_data_loader)

    st.start()

    sys.exit(app.exec_())
