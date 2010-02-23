from PySide import QtGui
<<<<<<< HEAD:views/texteditor.py
=======
from controllers.texteditor import TextEditorController
>>>>>>> textflow/master:views/texteditor.py

class TextEditor(QtGui.QTextEdit):
    """
    Text editor view.
    """    
    
    def __init__(self, parent):
        super(TextEditor, self).__init__(parent)
        self.setAcceptDrops(True)
        
<<<<<<< HEAD:views/texteditor.py
    def dropEvent(self, event):
        print str(event.mimeData().urls()[0].toLocalFile())
=======
        self.controller = TextEditorController()
        
    def dropEvent(self, event):
        filepath = str(event.mimeData().urls()[0].toLocalFile())

        success, document = self.controller.open(filepath)
            
        if success:
            self.setPlainText(document.text)
        else:
            QtGui.QMessageBox.critical(self, "Error",
                                       "The file <b>%s</b> doesn't exists." % 
                                       filepath, QtGui.QMessageBox.Ok)
>>>>>>> textflow/master:views/texteditor.py
