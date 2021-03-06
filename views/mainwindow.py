from PyQt4 import QtGui, QtCore
from ui.mainwindow import Ui_MainWindow
from controllers.mainwindow import MainWindowController
from views.texteditor import TFEditor

class MainWindowView(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindowView, self).__init__()
        self.setupUi(self)
        
        self.editor = TFEditor(self.centralwidget)
        self.editor.setObjectName("text_editor")
        self.horizontalLayout.addWidget(self.editor)
        
        self.controller = MainWindowController()
        
        self.__connect_signals()
        
    def __connect_signals(self):
        QtCore.QObject.connect(self.actionOpen, QtCore.SIGNAL("triggered()"), self.open_menu_clicked)
        QtCore.QObject.connect(self.actionSave, QtCore.SIGNAL("triggered()"), self.save_menu_clicked)
        QtCore.QObject.connect(self.actionSave_As, QtCore.SIGNAL("triggered()"), self.save_as_menu_clicked)
        
    def open_menu_clicked(self):
        filepath = QtGui.QFileDialog.getOpenFileName()
        
        if filepath:
            success, document = self.editor.controller.open(filepath)
            self.editor.text_area.highlighter.setFileSyntax(filepath)
            
            if success:
                self.editor.set_text(document.text)
            else:
                QtGui.QMessageBox.critical(self, "Error",
                                           "The file <b>%s</b> doesn't exists." % 
                                           filepath, QtGui.QMessageBox.Ok)
                                       
    def save_menu_clicked(self):
        success = self.editor.controller.save(self.editor.get_text())
        
        if not success:
            filepath = QtGui.QFileDialog.getSaveFileName()
            
            if filepath:
                self.editor.controller.save(self.editor.get_text(), filepath)
            
    def save_as_menu_clicked(self):
        filepath = QtGui.QFileDialog.getSaveFileName()
        
        if filepath:
            self.editor.controller.save(self.editor.get_text(), filepath)
            
