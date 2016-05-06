from PyQt4 import QtCore, QtGui
import SDC_GUI as My_GUI
import sys

class Window(QtGui.QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        self.ui = My_GUI.Ui_MainWindow()
        self.ui.setupUi(self)
        self.SentPrev = 0
    def keyPressEvent(self, ev):
        if(self.ui.Driving_Mode > -1):
            if(ev.key() == 16777235 and self.SentPrev != 1):
                print 'Up'
                self.SentPrev = 1
                self.ui.SendSerial('W')
                if(self.ui.Driving_Mode == 2):
                    self.ui.Camera.Take(1)
            if(ev.key() == 16777237 and self.SentPrev != 2):
                print 'Down'
                self.SentPrev = 2
                self.ui.SendSerial('S')
                if(self.ui.Driving_Mode == 2):
                    self.ui.Camera.Take(2)
            if(ev.key() == 16777236 and self.SentPrev != 3):
                print 'Right'
                self.SentPrev = 3
                self.ui.SendSerial('D')
                if(self.ui.Driving_Mode == 2):
                    self.ui.Camera.Take(3)
            if(ev.key() == 16777234 and self.SentPrev != 4):
                print 'Left'
                self.SentPrev = 4
                self.ui.SendSerial('A')
                if(self.ui.Driving_Mode == 2):
                    self.ui.Camera.Take(4)
            if(ev.key() == 16777249 and self.SentPrev != 5):
                print 'Left'
                self.SentPrev = 5
                self.ui.SendSerial('S')
                if(self.ui.Driving_Mode == 2):
                    self.ui.Camera.Take(5)
            print ev.key()

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    MainWindow = Window()
    MainWindow.show()
    sys.exit(app.exec_())