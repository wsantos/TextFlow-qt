from PyQt4.Qt import QSyntaxHighlighter

class Highlighter(QSyntaxHighlighter):
 
    def __init__(self, *args):
        QSyntaxHighlighter.__init__(self, *args)

