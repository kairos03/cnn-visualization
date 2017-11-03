# Copyright kairos03. All Right Reserved.
#
# CNN-Demo main
# images appear when input event emitted

import sys
import os

import time
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from components import *


class App(QWidget):
    """ Main Application
    """

    def __init__(self, data_loader):
        super().__init__()

        self.title = 'Smart Factory - Demo'
        self.left = 10
        self.top = 10
        self.width = 1200
        self.height = 800
        self.border = '1px solid black'

        # dataLoader
        self.data_loader = data_loader

        self.init_ui()

    def init_ui(self):

        # top widgets
        top_widgets = [StyledLabel('Data Convert', border=self.border, background='skyblue', id='./data/ex1/'),
                       StyledLabel('CNN Featuring', border=self.border, background='skyblue', id='./data/ex1/fmaps/'),
                       StyledLabel('Prediction', border=self.border, background='skyblue', id=None)]

        for w in top_widgets:
            w.reset_background()

        # connect event
        top_widgets[0].make_connection(self.data_loader.inputLoaded)
        top_widgets[1].make_connection(self.data_loader.convLoaded)
        top_widgets[2].make_connection(self.data_loader.outputLoaded)

        # top layout
        lay_top = QHBoxLayout()
        lay_top.addWidget(top_widgets[0])
        lay_top.addStretch()
        lay_top.addWidget(top_widgets[1])
        lay_top.addStretch()
        lay_top.addWidget(top_widgets[2])

        # center widgets
        # input
        input_image = ImgLabel(img_width=200, img_height=200, post_fix='input.png')
        input_image.make_connection(self.data_loader.inputLoaded)
        f_input = self.box_layout_frame_builder([input_image], 'Input Image')

        # conv widgets
        layer_image = []
        conv_widgets = []

        conv_widgets.append(StyledLabel('→'))
        layer_size = [10, 20, 40, 10]
        for i in range(len(layer_size)):
            imgs = []

            # make images
            for j in range(layer_size[i]):
                img = ImgLabel(img_width=50, img_height=50, post_fix='Conv%d-%02d.png' % (i+1, j+1))
                img.make_connection(self.data_loader.convLoaded)
                imgs.append(img)

            layer_image.append(imgs)
            conv_widgets.append(self.box_layout_frame_builder([self.grid_layout_frame_builder(imgs)],
                                                          'Feature Map %s' % (i+1)))
            conv_widgets.append(StyledLabel('→'))

        f_conv = self.box_layout_frame_builder(conv_widgets, layout=QHBoxLayout, no_stretch=True)

        # output
        output_label = [StyledLabel('Normal', id=0, border=self.border, background='green'),
                        StyledLabel('Stator', id=1, border=self.border, background='yellow'),
                        StyledLabel('Roter', id=2, border=self.border, background='orange'),
                        StyledLabel('Bearing', id=3, border=self.border, background='red')]
        for w in output_label:
            w.reset_background()
            w.make_connection(self.data_loader.outputLoaded)
        f_output = self.box_layout_frame_builder(output_label)

        # center layout
        lay_center = QHBoxLayout()
        lay_center.addWidget(f_input)
        lay_center.addWidget(f_conv)
        lay_center.addWidget(f_output)

        # main layout
        main_layout = QVBoxLayout()
        main_layout.addSpacing(10)
        main_layout.addLayout(lay_top)
        main_layout.addSpacing(10)
        main_layout.addLayout(lay_center)

        self.setLayout(main_layout)
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.show()

    @staticmethod
    def box_layout_frame_builder(widgets, text=None, layout=QVBoxLayout, no_stretch=False):
        """ vbox or hbox layout frame builder

        :param widgets:
        :param text:
        :param layout:
        :param no_stretch:
        :return:
        """
        lay = layout()
        if not no_stretch:
            lay.addStretch()
        for w in widgets:
            lay.addWidget(w)

        if text is not None:
            label = StyledLabel(text, font_size='10pt')
            lay.addWidget(label)

        if not no_stretch:
            lay.addStretch()
        lay.setAlignment(Qt.AlignCenter)

        frame = QFrame()
        frame.setLayout(lay)

        return frame

    @staticmethod
    def grid_layout_frame_builder(widgets, steps=10):
        """ grid layout frame builder

        :param widgets:
        :param steps:
        :return:
        """
        lay = QGridLayout()
        i = j = 0
        for w in widgets:
            lay.addWidget(w, i, j)
            i += 1
            if i >= steps:
                i = 0
                j += 1
        frame = QFrame()
        frame.setLayout(lay)
        return frame


class QDataThread(QThread):

    def __init__(self):
        super().__init__()

        self.data_loader = DataLoader()

    def run(self):
        for i in range(3):
            time.sleep(1)
            print(i)
        self.data_loader.on_input_data_loaded('./data/ex1/')
        for i in range(3):
            time.sleep(1)
            print(i)
        self.data_loader.on_conv_data_loaded('./data/ex1/fmaps/')
        for i in range(3):
            time.sleep(1)
            print(i)
        self.data_loader.on_output_data_loaded("0")


if __name__ == '__main__':
    qdt = QDataThread()

    app = QApplication(sys.argv)
    ex = App(qdt.data_loader)

    qdt.start()

    sys.exit(app.exec_())




