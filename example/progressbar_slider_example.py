# Copyright kairos03. All Right Reserved.

import sys

import time
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class ProgressBarDialog(QDialog):
    def __init__(self):
        super(ProgressBarDialog, self).__init__()
        self.init_ui()

    def init_ui(self):
        # Creating a label
        self.progressLabel = QLabel('Progress Bar:', self)

        # Creating a progress bar and setting the value limits
        self.progressBar = QProgressBar(self)
        self.progressBar.setMaximum(100)
        self.progressBar.setMinimum(0)

        # Creating a Horizontal Layout to add all the widgets
        self.hboxLayout = QHBoxLayout(self)

        # Adding the widgets
        self.hboxLayout.addWidget(self.progressLabel)
        self.hboxLayout.addWidget(self.progressBar)

        # Setting the hBoxLayout as the main layout
        self.setLayout(self.hboxLayout)
        self.setWindowTitle('Dialog with Progressbar')

        self.show()

    @pyqtSlot(int)
    def get_slider_value(self, val):
        self.progressBar.setValue(val)

    def make_connection(self, slider_object):
        slider_object.changedValue.connect(self.get_slider_value)


class SliderDialog(QDialog):

    changedValue = pyqtSignal(int)

    def __init__(self):
        super(SliderDialog, self).__init__()
        self.init_ui()

    def init_ui(self):
        # Creating a label
        self.sliderLabel = QLabel('Slider:', self)

        # Creating a slider and setting its maximum and minimum value
        self.slider = QSlider(self)
        self.slider.setMinimum(0)
        self.slider.setMaximum(100)
        self.slider.setOrientation(Qt.Horizontal)

        self.slider.valueChanged.connect(self.on_changed_value)

        # Creating a horizontalBoxLayout
        self.hboxLayout = QHBoxLayout(self)

        # Adding the widgets
        self.hboxLayout.addWidget(self.sliderLabel)
        self.hboxLayout.addWidget(self.slider)

        # Setting main layout
        self.setLayout(self.hboxLayout)

        self.setWindowTitle("Dialog with a Slider")
        self.show()

    def on_changed_value(self, value):
        self.changedValue.emit(value)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    sd = SliderDialog()
    pb = ProgressBarDialog()
    pb.make_connection(sd)
    sys.exit(app.exec_())


