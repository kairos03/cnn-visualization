# Copyright kairos03. All Right Reserved.

import time

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class StyledLabel(QLabel):

    def __init__(self, text, id=None, font_size='20pt', color='black', background=None, highlight='green', border=None):
        super().__init__()

        self.text = text
        self.id = text if id is None else id
        self.font_size = font_size
        self.color = color
        self.background = background
        self.highlight = highlight
        self.border = border

        self.init_ui()

    def init_ui(self):
        self.setText(self.text)
        self.setMargin(10)
        self.setStyleSheet(self.styleSheet() + 'font-size: %s;' % (self.font_size))
        self.setStyleSheet(self.styleSheet() + 'color: %s;' % (self.color))
        self.setStyleSheet(self.styleSheet() + 'background-color: %s;' % (self.background))
        self.setStyleSheet(self.styleSheet() + 'border: %s;' % (self.border))

    @pyqtSlot(str)
    def change_background(self, state_code):
        if state_code == self.id:
            self.setStyleSheet(self.styleSheet() + 'background-color: %s;' % (self.background))
            print('dlog/change background, id: %s, text: %s' % (self.id, self.text))
        else:
            self.setStyleSheet(self.styleSheet() + 'background-color: None;')

    @pyqtSlot()
    def reset_background(self):
        self.setStyleSheet(self.styleSheet() + 'background-color: None;')

    def blink(self):
        for i in range(5):
            self.set_background(self.highlight)
            time.sleep(0.5)
            self.set_background(self.background)
            time.sleep(0.5)

    def make_connection(self, data_loader):
        data_loader.connect(self.change_background)

    def make_reset(self, signal):
        signal.connect(self.reset_background)


class ImgLabel(QLabel):

    def __init__(self, img_path=None, post_fix='', img_width=None, img_height=None):
        super().__init__()
        self.default_path = './data/white.png'
        self.post_fix = post_fix
        self.img_path = img_path + post_fix if img_path is not None else self.default_path
        self.img_width = img_width
        self.img_height = img_height

        self.init_ui()

    def init_ui(self):
        pixmap = self.make_pixmap()
        self.setPixmap(pixmap)
        self.setMaximumSize(self.img_width, self.img_height)

    def make_pixmap(self):
        pixmap = QPixmap(self.img_path)
        if self.img_width is not None and self.img_height is not None:
            pixmap = pixmap.scaled(self.img_width, self.img_height, Qt.KeepAspectRatio)
        else:
            self.img_width = pixmap.width()
            self.img_height = pixmap.height()
        return pixmap

    @pyqtSlot(str)
    def reload_image(self, img_path):
        path = img_path + self.post_fix
        print("dlog/reload image, path: %s" % (path))
        self.img_path = path
        pixmap = self.make_pixmap()
        self.setPixmap(pixmap)

    @pyqtSlot()
    def reset(self):
        path = './data/white.png'
        print("dlog/reload image, path: %s" % (path))
        self.img_path = path
        pixmap = self.make_pixmap()
        self.setPixmap(pixmap)

    def make_connection(self, data_loader):
        data_loader.connect(self.reload_image)

    def make_reset(self, signal):
        signal.connect(self.reset)


class DataLoader(QObject):
    def __init__(self):
        super().__init__()

    inputLoaded = pyqtSignal(str)
    convLoaded = pyqtSignal(str)
    outputLoaded = pyqtSignal(str)
    reset = pyqtSignal()

    def on_input_data_loaded(self, path):
        self.inputLoaded.emit(path)

    def on_conv_data_loaded(self, path):
        self.convLoaded.emit(path)

    def on_output_data_loaded(self, state_code):
        self.outputLoaded.emit(state_code)

    def on_reset(self):
        self.reset.emit()
