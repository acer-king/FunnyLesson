import sys
from PyQt5.QtWidgets import (QMainWindow, QApplication, QPushButton, QWidget, 
QAction, QTabWidget,QVBoxLayout,QHBoxLayout,QGridLayout,QFrame,QLabel,QSlider,QScrollArea,QCheckBox,QSizePolicy,QFileDialog,QDockWidget, QDialog,\
    QListWidget)
from PyQt5.QtGui import QIcon,QFont,QCursor,QPixmap,QPaintDevice,QPainter,QPen
from PyQt5.QtCore import pyqtSlot, Qt, QSize,QEvent,QTimer
from Setting import Settings,loadData
from Mybutton import *
from Container import *
from ProjectMgr.LocalMgr import LocalProjectMgr
import os
from MyUtil import match_image
import logging

class StudentHeaderToolBar(MyFrame):

    sig_bt_resumeplay = pyqtSignal()
    sig_bt_carmin = pyqtSignal()
    
    sig_bt_signal = pyqtSignal()
    sig_bt_question = pyqtSignal()
    sig_bt_social = pyqtSignal()
    sig_bt_speaker = pyqtSignal()
    sig_bt_search = pyqtSignal()
    
    def __init__(self,parent):

        super(StudentHeaderToolBar,self).__init__(parent)
        self.setMaximumHeight(40)
        self.__initUI()
    
    def __initUI(self):
        
        hbox = MyHBoxLayout(self)

        self.bt_resumeplay = PlayResumeButton(self)
        self.bt_carmin = CarmineButton(self)
        
        self.bt_signal = SignalButton(self)
        self.bt_question = QuestionButton(self)
        self.bt_social = SocialButton(self)
        self.bt_speaker = SpeakerButton(self)
        self.bt_search = SearchButton(self)
        
        hbox.addWidget(self.bt_resumeplay)
        hbox.addWidget(self.bt_carmin)
        hbox.addStretch(1)
        hbox.addWidget(self.bt_signal)
        hbox.addWidget(self.bt_question)
        hbox.addWidget(self.bt_social)
        hbox.addWidget(self.bt_speaker)
        hbox.addWidget(self.bt_search)

        #bind event
        self.bt_signal.clicked.connect(self.sig_bt_signal)
        self.bt_resumeplay.clicked.connect(self.sig_bt_resumeplay)
        self.bt_carmin.clicked.connect(self.sig_bt_carmin)
        self.bt_question.clicked.connect(self.sig_bt_question)
        self.bt_social.clicked.connect(self.sig_bt_social)
        self.bt_speaker.clicked.connect(self.sig_bt_speaker)
        self.bt_search.clicked.connect(self.sig_bt_search)

class CommonLessonItem(MyFrame):
    sig_ItemHeaderIcon = pyqtSignal(str,int,int)
    def __init__(self,parent):

        super(CommonLessonItem,self).__init__(parent)
        self.lbl_title = CommonHeaderLabel(self)
        self.lbl_description = CommonDescriptionLabel(self)
        self.lbl_icon = CommonHeaderIcon(self)
        self.__initUI()
        self.isChild = False
        self.anchorPixmapUrl = None
        self.posx = None
        self.posy = None


    def __initUI(self):
        
        #set layout
        self.layout = MyGridLayout(self)
        self.layout.addWidget(self.lbl_title,0,0,1,19)
        self.layout.addWidget(self.lbl_icon,0,19,1,1)
        self.layout.addWidget(self.lbl_description,1,0,1,20)
        
        #initialize info
        self.setInfo("Title","Description",None)
        self.setLayout(self.layout)

        #event binding
        self.lbl_icon.mousePressEvent = self.processMatchEvent
    
    def processMatchEvent(self,event):
        self.sig_ItemHeaderIcon.emit(self.anchorPixmapUrl,self.posx,self.posy)
        

    def display(self,isminimized=False):

        if(isminimized):
            self.lbl_icon.hide()
            self.lbl_description.hide()
        else:
            self.lbl_icon.show()
            self.lbl_description.show()
    

    def setInfo(self,title,description,iconPath):
        self.lbl_title.setText(title)
        self.lbl_description.setText(description)
        if(iconPath is not None):
            self.lbl_icon.setPixmap(QPixmap(iconPath))

class CommonLessonOverview(CommonLessonItem):
    
    def __init__(self,parent):

        super(CommonLessonOverview,self).__init__(parent)
        self.isMinimized = False
        self.__initUI()
    
    def __initUI(self):
        self.layout.removeWidget(self.lbl_icon)
        self.layout.addWidget(self.lbl_icon,0,19,2,1)
        self.lbl_icon.setPixmap(QPixmap('icons/lookstep.png'))
    
    def mousePressEvent(self,event):
        if(self.isMinimized):
            self.lbl_icon.hide()
            self.lbl_description.hide()
        else:
            self.lbl_icon.show()
            self.lbl_description.show()
        self.isMinimized = not self.isMinimized

class CommonLessonLookStepItem(CommonLessonItem):
    
    def __init__(self,parent):

        super(CommonLessonLookStepItem,self).__init__(parent)
        self.__initUI()
    
    def __initUI(self):

        self.lbl_icon.setPixmap(QPixmap('icons/lookstep.png'))    

class CommonLessonClickStepItem(CommonLessonItem):
    
    def __init__(self,parent):
        super(CommonLessonClickStepItem,self).__init__(parent)
        self.__initUI()    
        
    
    def __initUI(self):
        self.lbl_icon.setPixmap(QPixmap('icons/clickstep.png'))

class CommonLessonMatchStepItem(CommonLessonItem):
    
    def __init__(self,parent):
        super(CommonLessonMatchStepItem,self).__init__(parent)
        self.__initUI()
        self.lbl_icon.setPixmap(QPixmap('icons/matchstep.png'))
        
    def __initUI(self):
        
        self.lbl_uploadImg = MyDropableLable(self)
        self.layout.addWidget(self.lbl_uploadImg,2,0,1,20)

class CommonLessonMouseStepItem(CommonLessonItem):
    
    def __init__(self,parent):
    
        super(CommonLessonMouseStepItem,self).__init__(parent)
        
        self.__initUI()
        self.lbl_icon.setPixmap(QPixmap('icons/mousestep.png'))
        
    def __initUI(self):
        self.lbl_uploadImg = MyDropableLable(self)
        self.lbl_uploadImg.setAlignment(Qt.AlignCenter)
        self.lbl_uploadImg.setWindowFlags(Qt.FramelessWindowHint|Qt.Window)
        self.lbl_uploadImg.setAttribute(Qt.WA_TranslucentBackground)
        self.lbl_uploadImg.setScaledContents(True)
        self.lbl_uploadImg.move(400,400)
        
    def setInfo(self,title,description,iconPath):
        super(CommonLessonMouseStepItem,self).setInfo(title,description,iconPath)
        self.setMouseStepImage()
        pass
    def setMouseStepImage(self,isCurrentItem=False):
        if(self.lbl_title.text() == Settings.scrollDown):
            #set image as scroll down
            self.lbl_uploadImg.setPixmap(QPixmap('icons/scrolldown.png'))
        elif(self.lbl_title.text() == Settings.scrollUp):
            #set image as scroll up
            self.lbl_uploadImg.setPixmap(QPixmap('icons/scrollup.png'))
        else:
            pass
    
    def hideEvent(self,event):
        self.lbl_uploadImg.hide()
        super(CommonLessonMouseStepItem,self).hide()
    def showEvent(self,event):
        # self.lbl_uploadImg.show()
        super(CommonLessonMouseStepItem,self).show()
    
class CommonLessonAttachStepItem(CommonLessonItem):
    def __init__(self,parent):

        super(CommonLessonAttachStepItem,self).__init__(parent)
        self.__initUI()

    def __initUI(self):
        self.lbl_webview = MyWebView(self)
        # self.lbl_webview.setFixedSize(200,200)
        self.lbl_icon.setPixmap(QPixmap('icons/attachstep.png'))
        self.layout.addWidget(self.lbl_webview,2,0,1,20)

class CommonLessonPiskelStepItem(CommonLessonItem):

    def __init__(self,parent):
    
        super(CommonLessonPiskelStepItem,self).__init__(parent)
        self.lbl_referUrl = CommonDescriptionLabel('wwww.piskelapp.com')
        self.__initUI()
        self.lbl_icon.setPixmap(QPixmap('icons/lookstep.png'))

    
    def __initUI(self):

        pass
    
class StudentBodyWidget(MyContainer):
    resetEvent = pyqtSignal(str)
    def __init__(self,parent):
    
        super(StudentBodyWidget,self).__init__(parent)
        self.prevItem = PrevArrowWidget(self)
        self.itemHeader = None
        self.currentItem = None
        self.layout = None
        self.itemList = None
        self.nextItem = None
        self.nestedItems = []
        self.currentAnchorPixmapUrl = None
        self.anchorDlg = QAnchorDialog(self)

        #set timer
        self.timer = QTimer(self)
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.processAnchorAnimation)
        self.timer.start()
        self.step = 0

        #event binding
        self.window().moveEvent = self.processMoveEvent
        # self.initializeObject(path)

    def processMatchByAnchor(self,anchorUrl,posx=None,posy=None):
        if(anchorUrl is not None):
            self.currentAnchorPixmapUrl = (anchorUrl)
        else:
            return 
        if(self.currentAnchorPixmapUrl is not None):
            found = 0
            try:
                (found,X,Y,W,H,R) = match_image(self.currentAnchorPixmapUrl)
            except:
                logging.exception("cv template matching issue")

            if(found == 0):
                print("not found")
                return
            else:
                # print(X,Y,W,H)
                pass

            if posx is not None and posy is not None:
                self.anchorDlg.ClickPointable = True
                self.anchorDlg.posyToEmit = posy
                self.anchorDlg.posxToEmit = posx
            self.anchorDlg.resize(H,W)
            self.anchorDlg.move(X,Y)
            self.anchorDlg.setStyleSheet('background-color:lightgreen')
            
            self.step = 1
            pass
        else:
            pass

    def processAnchorAnimation(self):
        if(self.step>7 or self.step ==0):
            self.anchorDlg.hide()
            return
        if(self.step%2):
            self.anchorDlg.show()
        else:
            self.anchorDlg.hide()
        self.step = self.step + 1
        pass

    def currentProjectChanged(self,name):
        self.projectPath = os.path.join(os.getcwd(),Settings.projectStudentPath)
        self.projectPath = os.path.join(self.projectPath,name)
        self.initializeObject(self.projectPath)
        pass

    def initializeObject(self,projectPath):
        self.prevItem.hide()
        self.resetEvent.emit("")
        if(projectPath is None):
            return
        self.currentItem = None
        self.nextItem = None
        self.nestedItems = []
        self.clearLayout()
        projectfilePath = os.path.join(projectPath,Settings.projectFileName)
        self.loadData(projectfilePath)
        if(self.data is None):
            return
        self.__initUI()
        pass

    def clearLayout(self):
        print("checkmehereclearlayout")
        if self.layout is not None:
            while self.layout.count():
                child = self.layout.takeAt(0)
                if child.widget():
                    child.widget().deleteLater()

    def loadData(self,projectfilePath):

        self.data = loadData(projectfilePath)

    def __initUI(self):
        
        self.imageBaseUrl = self.data.metaInfo.baseImgUrl
        
        #initializeHeader
        self.itemHeader = CommonLessonOverview(self)
        self.itemHeader.setInfo(self.data.header.title,self.data.header.description,os.path.join(self.projectPath, self.data.header.imageName))
        self.itemHeader.anchorPixmapUrl = os.path.join(self.projectPath,self.data.header.anchorImageName)
        self.itemHeader.sig_ItemHeaderIcon.connect(self.processMatchByAnchor)
        
        #adds listwidgets to layout
        if(self.layout is None):
            self.layout = MyVBoxLayout(self)
        self.layout.addWidget(self.itemHeader)
        self.prevItem.hide()

        self.itemList = []
        for idx in range(len(self.data.lessons)):
            if(self.data.lessons[idx].type == Settings.lookStep):
                curInfo = self.data.lessons[idx]
                item = CommonLessonLookStepItem(self)
                item.setInfo(curInfo.title,curInfo.description,None)
                item.anchorPixmapUrl = os.path.join(self.projectPath,curInfo.anchorPixmap)
                item.hide()
                self.layout.addWidget(item)
                self.itemList.append(item)
                item.installEventFilter(self)
                item.isChild = (curInfo.isChild == "true")
                item.sig_ItemHeaderIcon.connect(self.processMatchByAnchor)
                pass
            elif(self.data.lessons[idx].type == Settings.clickStep):
                curInfo = self.data.lessons[idx]
                item = CommonLessonClickStepItem(self)
                item.setInfo(curInfo.title,curInfo.description,None)
                item.anchorPixmapUrl = os.path.join(self.projectPath,curInfo.anchorPixmap)
                item.hide()
                self.layout.addWidget(item)
                self.itemList.append(item)
                item.installEventFilter(self)
                item.isChild = (curInfo.isChild == "true")
                try:
                    item.posx = curInfo.posx
                    item.posy = curInfo.posy
                except:
                    pass
                item.sig_ItemHeaderIcon.connect(self.processMatchByAnchor)
                pass
            elif(self.data.lessons[idx].type == Settings.matchStep):
                curInfo = self.data.lessons[idx]
                item = CommonLessonMatchStepItem(self)
                item.setInfo(curInfo.title,curInfo.description,None)
                item.lbl_uploadImg.setPixmap(QPixmap(os.path.join(self.projectPath,curInfo.anchorPixmap)))
                item.hide()
                self.layout.addWidget(item)
                self.itemList.append(item)
                item.installEventFilter(self)
                item.isChild = (curInfo.isChild == "true")
                item.sig_ItemHeaderIcon.connect(self.processMatchByAnchor)
                pass
            elif(self.data.lessons[idx].type == Settings.mouseStep):
                curInfo = self.data.lessons[idx]
                item = CommonLessonMouseStepItem(self)
                item.setInfo(curInfo.title,curInfo.description,None)
                item.anchorPixmapUrl = os.path.join(self.projectPath,curInfo.anchorPixmap)
                item.hide()
                self.layout.addWidget(item)
                self.itemList.append(item)
                item.installEventFilter(self)
                item.isChild = (curInfo.isChild == "true")
                item.sig_ItemHeaderIcon.connect(self.processMatchByAnchor)
                pass
            elif(self.data.lessons[idx].type == Settings.attachStep):
                curInfo = self.data.lessons[idx]
                item = CommonLessonAttachStepItem(self)
                item.lbl_webview.setUrl(curInfo.referUrl)
                item.hide()
                self.layout.addWidget(item)
                self.itemList.append(item)
                item.installEventFilter(self)
                item.isChild = (curInfo.isChild == "true")
                item.sig_ItemHeaderIcon.connect(self.processMatchByAnchor)
                pass
            elif(self.data.lessons[idx].type == Settings.piskelStep):
                curInfo = self.data.lessons[idx]
                item = CommonLessonPiskelStepItem(self)
                item.setInfo(title=curInfo.title,description=curInfo.description,iconPath=None)
                item.lbl_referUrl.setText(curInfo.referUrl)
                item.hide()
                self.layout.addWidget(item)
                self.itemList.append(item)
                item.installEventFilter(self)
                item.isChild = (curInfo.isChild == "true")
                item.sig_ItemHeaderIcon.connect(self.processMatchByAnchor)
                pass
            else:
                pass
        
        self.layout.addStretch(1)

        #event binding
        self.itemHeader.mousePressEvent = self.processMoveEvent
        self.prevItem.clicked.connect(self.gotoPrev)

    def hideAllNextAndNestedItems(self,isHide=True):
        
        if(isHide == True and self.nextItem is not None):
            self.nextItem.hide()
            if(self.nestedItems is not None):
                for item in self.nestedItems:
                    item.hide()
            pass
        elif(isHide == False and self.nextItem is not None):
            self.nextItem.show()
            if(self.nestedItems is not None):
                for item in self.nestedItems:
                    item.show()
            pass

    def eventFilter(self,source,event):
        
        if((event.type() == QEvent.Enter and source == self.currentItem and self.currentItem is not None) or (event.type() == QEvent.MouseButtonPress and source == self.currentItem and self.currentItem is not None)):
            #view prev and next
            self.setNextItemFloating(True)
            self.hideAllNextAndNestedItems(False)
            pass

        elif(event.type() == QEvent.MouseButtonPress and source == self.nextItem):
            #process press event in next item
            self.currentItem.hide()
            self.setNextItemFloating(False)
            self.currentItem = self.nextItem
            self.currentItemChanged()
            
        elif(event.type() == QEvent.MouseButtonPress and self.nestedItems is not None):
            #process press event in nested item
            if(source in self.nestedItems):
                source.display(False)
                pass
            else:
                pass
        else:
            pass
        return super(StudentBodyWidget,self).eventFilter(source,event)

    def movePrevItem(self):
        
        self.prevItem.setSize(self.prevItem.width(),self.currentItem.height()+2)
        self.prevItem.show()
        self.prevItem.move(self.currentItem.mapToGlobal(QPoint(0,0))-QPoint(self.prevItem.width(),4))

    def play(self,event):
        if(self.itemHeader is not None):
            self.itemHeader.display(isminimized=True)
        if(self.currentItem is not None):
            self.currentItem.hide()
        if(self.itemList is not None):
            if(len(self.itemList) > 0):
                self.currentItem = self.itemList[0]
                self.currentItemChanged()

        #event binding
    
    def hideEvent(self,event):
        self.hideAll()
    def hideAll(self):

        self.hideAllNextAndNestedItems(False)
        if(self.currentItem is not None):
            self.currentItem.hide()
        if(self.prevItem is not None):
            self.prevItem.hide()
        if(self.itemHeader is not None):
            self.itemHeader.hide()
        if(self.nextItem is not None):
            self.nextItem.hide()
        for item in self.nestedItems:
            item.hide()
        
    def currentItemChanged(self):
        
        #hide all nested items and next item
        self.hideAllNextAndNestedItems(True)
        self.currentItem.show()
        self.currentAnchorPixmapUrl = self.currentItem.anchorPixmapUrl
        self.movePrevItem()
        
        #change nested items and next item in itemList
        length = self.itemList.__len__()
        idx = self.itemList.index(self.currentItem)
        sign_next = False
        sign_nested = False

        for index in range(idx+1, length):
            if(self.itemList[index].isChild == True):
                sign_nested = True
                self.nestedItems.append(self.itemList[index])
            else:
                sign_next = True
                self.nextItem = self.itemList[index]
                break

        if(sign_next == False):
            self.nextItem = None
        if(sign_nested == False):
            self.nestedItems = []

        
        #if current item is mousestepitem, then show mouse image
        if type(self.currentItem).__name__ == "CommonLessonMouseStepItem":
            if(self.currentItem.lbl_title.text() == Settings.scrollUp or self.currentItem.lbl_title.text() == Settings.scrollDown):
                self.currentItem.lbl_uploadImg.show()
            else:
                self.currentItem.lbl_uploadImg.hide()
            pass

    def setNextItemFloating(self,isFloat=False):
        
        if(isFloat == True and self.nextItem is not None):
            self.nextItem.setWindowFlags(Qt.FramelessWindowHint|Qt.Window)
            self.nextItem.resize(self.currentItem.width(),self.nextItem.sizeHint().height())
            self.processMoveEvent(None)
            self.nextItem.show()
        else:
            if(self.nextItem is not None):
                self.nextItem.setWindowFlags(Qt.Widget)
                self.nextItem.show()

    def processMoveEvent(self,event):

        if(self.prevItem is not None and self.currentItem is not None):
            self.prevItem.move(self.currentItem.mapToGlobal(QPoint(0,0))-QPoint(self.prevItem.width(),4))
            if(self.nextItem is not None):
                ######################  float next item to next current item #####################
                self.nextItem.move(self.currentItem.mapToGlobal(QPoint(0,0))+QPoint(self.currentItem.width()+4,-4))
                #########################
        pass

    def gotoPrev(self,event):
        
        idx = self.itemList.index(self.currentItem)
        if(idx == 0):
            #go to main page.
            if(self.prevItem is not None):
                self.prevItem.hide()
            if(self.nextItem is not None):
                self.nextItem.hide()

            if(self.nestedItems is not None):
                for item in self.nestedItems:
                    item.hide()
            self.currentItem.hide()
            self.itemHeader.display(isminimized=False)
            # emit reset event.
            self.resetEvent.emit("")
        else:
            self.currentItem.hide()
            while(idx > 0):
                if(self.itemList[idx-1].isChild == True):
                    idx = idx -1
                    continue
                else:
                    self.currentItem = self.itemList[idx-1]
                    break
            self.currentItemChanged()
            pass
        

class MyProjectListWidget(QListWidget):
    def __init__(self,parent):
        super(MyProjectListWidget,self).__init__(parent)
        self.__initUI()    
        self.setFont(QFont('Arial',14))
    def __initUI(self):
        pass

class StudentProjectList(MyContainer):
    sig_CurrentProjectChanged = pyqtSignal(str)
    def __init__(self,parent):
        super(StudentProjectList,self).__init__(parent)
        self.currentProjectName = None
        self.__initUI()
        pass               
    def __initUI(self):
        self.projectList = MyProjectListWidget(self)
        self.vbox = MyVBoxLayout(self)
        self.vbox.addWidget(self.projectList)
        
        #event binding
        self.projectList.currentItemChanged.connect(self.currentItemChanged)
        #set style sheet
        self.setContentsMargins(10,0,10,0)
        
        pass
    def currentItemChanged(self,cur,prev):
        if(cur is not None):
            self.sig_CurrentProjectChanged.emit(cur.text())
        else:
            return None

    def display(self,projectNameList):
        self.projectList.clear()
        for idx,item in enumerate(projectNameList):
            self.projectList.insertItem(idx,item)
        self.projectList.setCurrentRow(0)
        
    def getSelectedItemName(self):
        if len(self.projectList.selectedItems()) == 0:
            return None
        return self.projectList.selectedItems()[0].text()

class StudentTabWidget(MyContainer):

    sig_bt_resumeplay = pyqtSignal()
    sig_bt_carmin = pyqtSignal()
    
    sig_bt_signal = pyqtSignal()
    sig_bt_question = pyqtSignal()
    sig_bt_social = pyqtSignal()
    sig_bt_speaker = pyqtSignal()
    sig_bt_search = pyqtSignal()

    def __init__(self,parent):
        super(StudentTabWidget,self).__init__(parent)
        self.__initUI()

    def __initUI(self):
        vbox = MyVBoxLayout(self)
        self.studentToolBar = StudentHeaderToolBar(self)
        self.studentBody  =  StudentBodyWidget(self)
        self.studentList = StudentProjectList(self)
        vbox.addWidget(self.studentToolBar)
        vbox.addWidget(self.studentBody)
        vbox.addWidget(self.studentList)
        vbox.addStretch(1)


        # hide some items at start.
        self.studentList.hide()
        #bind event.
        self.studentList.sig_CurrentProjectChanged.connect(self.studentBody.currentProjectChanged)
        self.sig_bt_resumeplay.connect(self.showSelectedLesson)


        self.studentToolBar.bt_resumeplay.clicked.connect(self.processPlayResume)
        self.studentBody.resetEvent.connect(self.processResetEvent)
        self.studentToolBar.sig_bt_signal.connect(self.sig_bt_signal)
        self.studentToolBar.sig_bt_resumeplay.connect(self.sig_bt_resumeplay)
        self.studentToolBar.sig_bt_carmin.connect(self.sig_bt_carmin)
        self.studentToolBar.sig_bt_question.connect(self.sig_bt_question)
        self.studentToolBar.sig_bt_social.connect(self.sig_bt_social)
        self.studentToolBar.sig_bt_speaker.connect(self.sig_bt_speaker)
        self.studentToolBar.sig_bt_search.connect(self.sig_bt_search)
        pass
    def setupProjectList(self,projectNameList):
        self.studentList.display(projectNameList)
        self.showProjectList()
    def showSelectedLesson(self):
        self.studentBody.show()
        self.studentList.hide()

    def getNameSelectedProject(self):
        self.studentList.getSelectedItemName()

    def showProjectList(self):
        self.studentList.show()
        self.studentBody.hide()

    def processPlayResume(self):
        if self.studentToolBar.bt_resumeplay.isPlaying == True:
            self.studentBody.play(None)
        else:
            if(self.studentBody.currentItem is not None):
                self.studentBody.currentItem.hide()
            if(self.studentBody.prevItem is not None):
                self.studentBody.prevItem.hide()
            self.studentBody.hideAllNextAndNestedItems()

    def processResetEvent(self):
        self.studentToolBar.bt_resumeplay.reset()
        # self.studentToolBar.bt_resumeplay.changeState()

    def hideEvent(self,event):
        self.studentList.hide()
        self.studentBody.hide()
        
