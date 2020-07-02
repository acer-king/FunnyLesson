import sys

from PyQt5.QtCore import QPoint
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import pyqtSlot, Qt, QSize,QEvent,QRect
from Setting import Settings
from PyQt5.QtGui import QIcon,QFont,QCursor,QPixmap,QPainter,QPen
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QWidget, \
QAction, QTabWidget,QVBoxLayout,QHBoxLayout,QGridLayout,QFrame,QLabel,QSlider,QScrollArea,QCheckBox,QSizePolicy,QFileDialog,QDockWidget, QDialog
from Component import MyTableWidget
import webbrowser
from Container import MyBar
from Mybutton import CommonButton
import logging


class MainWindow(QWidget):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.layout  = QGridLayout()
        titlebar = MyBar(self)
        titlebar.setStyleSheet('border: 1px solid')
        self.layout.addWidget(titlebar,0,0,1,100)
        body = MyTableWidget(self)
        self.layout.addWidget(body,1,0,100,100)

        #profile and setting button
        bt_profile = CommonButton(self,"Profile")
        bt_profile.setIcon(QIcon('icons/profile.png'))
        bt_profile.setStyleSheet('border:None')
        setting_profile = CommonButton(self,"Setting")
        setting_profile.setIcon(QIcon('icons/setting.png'))

        self.layout.addWidget(bt_profile,1,88,1,5)
        self.layout.addWidget(setting_profile,1,94,1,5)
        

        self.setLayout(self.layout)
        self.layout.setContentsMargins(0,0,0,0)
        self.setMinimumSize(450,850)
        self.setWindowFlags(Qt.FramelessWindowHint|Qt.WindowStaysOnTopHint)
        self.pressing = False
        

        #init style sheet
        
        # self.__initStyleSheet()

    def __initStyleSheet(self):
        self.styleSheet = """
        MyRichTextDockWidget{
            margin:0px;
            padding:0px;
        }
        #AnchorDlg{
            border:3px solid black;
            border-style: dashed
        }
        QWidget{
            margin:0px;
            padding:0px;
        }
        QLabel{
            
        }
        QTextEdit{
            margin:0px;
            padding:0px;
        }
        QVBoxLayout{
            margin:0px;
            padding:0px;
        }
        QHBoxLayout{
            margin:0px;
            padding:0px;
            border:1px solid
        }
        QGridLayout{
            margin:0px;
            padding:0px;
        }
        QTextEdit#objectName{
            margin:0px;
            padding:0px;
        }
        MainWindow{
            margin:0px;
            padding:0px;
        }
        """
        self.setStyleSheet(self.styleSheet)
        # self.setStyleSheet("border:3px dashed solid")
        
    def paintEvent(self,event):

        painter = QPainter(self)
        pen = QPen(Qt.black)
        pen.setWidth(2)
        painter.setPen(pen)
        painter.drawRect(QRect(2,2,self.width()-5,self.height()-5))
        

if __name__ == "__main__":

    logging.basicConfig(filename='log.txt', filemode='w', format='%(message)s')
    app = QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec_())