from PyQt5 import QtWidgets, uic
# from PyQt5.QtCore import pyqtSignal

class Ui_calibration_tab(QtWidgets.QWidget):

    # new_plot_param_signal = pyqtSignal()

    def __init__(self, parent=None):
        super(Ui_calibration_tab, self).__init__(parent)
        uic.loadUi("./ui_calibration_tab.ui", self)
        self.show()

        # appearance menu
        # self.cmap_list = ['jet', 'inferno', 'gray']
        # self.scale_list = ['linear', 'log']

        # useful params inside this widget
        self.japc = None
        self.current_cam_name = None

        # data to pass when emitting signals
        # self.plot_parameters = { 'cmap': self.cmap_list[0], 'cauto':True, 'cmin':0, 'cmax':4096, 'scale': self.scale_list[0] }

        self.hw_bin_h.setText('56')
        self.hw_bin_h.setText('45')

    def setup_calibration_tab(self, japc):
        ## japc
        self.japc = japc

    def camera_start(self, cam_name):
        self.current_cam_name = cam_name

        self.japc.subscribeParam(self.current_cam_name+'/AcquisitionStatus', onValueReceived=self.acqStatusCallback, getHeader=True, unixtime=True)
        self.japc.subscribeParam(self.current_cam_name+'/AcquiredParameters', onValueReceived=self.acqParamCallback, getHeader=True, unixtime=True)
        self.japc.subscribeParam(self.current_cam_name+'/ExpertSetting', onValueReceived=self.expSettingCallback, getHeader=True, unixtime=True)
        self.japc.startSubscriptions()

    def acqStatusCallback(self, paramName, value, headerInfo):
        # self.imageData = value
        # self.new_img_signal.emit()
        print('New AcqStatus')

    def acqParamCallback(self, paramName, value, headerInfo):
        # self.imageData = value
        # self.new_img_signal.emit()
        print('New AcqParam')

    def expSettingCallback(self, paramName, value, headerInfo):
        # self.imageData = value
        # self.new_img_signal.emit()
        print('New expSetting')
