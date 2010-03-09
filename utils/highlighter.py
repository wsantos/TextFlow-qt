#
# hex2QColor and QFormatter and Highlighter are based in code of WikiParser (http://thewikiblog.appspot.com/).
#

from PyQt4 import QtGui, QtCore

from pygments.formatter import Formatter
from pygments import highlight

import pygments.lexers as pyglexers

import os

def hex2QColor(c):
    r=int(c[0:2],16)
    g=int(c[2:4],16)
    b=int(c[4:6],16)
    return QtGui.QColor(r,g,b)
    

class QFormatter(Formatter):
    
    def __init__(self):
        Formatter.__init__(self)
        self.data=[]
        
        # Create a dictionary of text styles, indexed
        # by pygments token names, containing QTextCharFormat
        # instances according to pygments' description
        # of each style
        
        self.styles={}
        for token, style in self.style:
            qtf=QtGui.QTextCharFormat()

            if style['color']:
                qtf.setForeground(hex2QColor(style['color'])) 
            if style['bgcolor']:
                qtf.setBackground(hex2QColor(style['bgcolor'])) 
            if style['bold']:
                qtf.setFontWeight(QtGui.QFont.Bold)
            if style['italic']:
                qtf.setFontItalic(True)
            if style['underline']:
                qtf.setFontUnderline(True)
            self.styles[str(token)]=qtf
    
    def format(self, tokensource, outfile):
        global styles
        # We ignore outfile, keep output in a buffer
        self.data=[]
        
        # Just store a list of styles, one for each character
        # in the input. Obviously a smarter thing with
        # offsets and lengths is a good idea!
        
        for ttype, value in tokensource:
            l=len(value)
            t=str(ttype)                
            self.data.extend([self.styles[t],]*l)

class Highlighter(QtGui.QSyntaxHighlighter):
 
    def __init__(self, *args):
        QtGui.QSyntaxHighlighter.__init__(self, *args)

        self.formatter=QFormatter()
        self.lexer=pyglexers.get_lexer_by_name("boo") #Default lexer
            
    def setFileSyntax(self, filename):
        
        try:
            self.lexer=pyglexers.get_lexer_for_filename(os.path.basename(str(filename)))
        except:
            self.lexer=pyglexers.get_lexer_by_name("boo")


    def highlightBlock(self, text):
        """Takes a block, applies format to the document. 
        according to what's in it.
        """
        # I need to know where in the document we are,
        # because our formatting info is global to
        # the document
        cb = self.currentBlock()
        p = cb.position()

        # The \n is not really needed, but sometimes  
        # you are in an empty last block, so your position is
        # **after** the end of the document.
        text=unicode(self.document().toPlainText())+'\n'
        
        # Yes, re-highlight the whole document.
        # There **must** be some optimizacion possibilities
        # but it seems fast enough.
        highlight(text,self.lexer,self.formatter)
        
        # Just apply the formatting to this block.
        # For titles, it may be necessary to backtrack
        # and format a couple of blocks **earlier**.
        for i in range(len(unicode(text))):
            try:
                self.setFormat(i,1,self.formatter.data[p+i])
            except IndexError:
                pass



