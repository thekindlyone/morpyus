import sys
from PySide.QtCore import *
from PySide.QtGui import *
from pyunpack import Archive
import os
from os.path import splitext,basename,expanduser,exists,dirname
import shutil
from functools import partial
from keys import keynames
class mainwindow(QWidget):
    
    def __init__(self,bookfile,screensize,currentpage=0):
        super(mainwindow, self).__init__()
        self.screen_w,self.screen_h=screensize
        self.bookfile=bookfile
        self.prime_bookshelf()
        self.load_book()
        self.currentpage=currentpage
        self.initUI()
        self.keymap={
        Qt.Key_Escape  : partial(sys.exit,0),
        Qt.Key_PageDown: self.next_page,
        Qt.Key_PageUp  : self.prev_page
        }
        
    def initUI(self):        
        self.setWindowTitle('PyCDisplay')
        self.load_current_page()
        self.showFullScreen()
    
    def show_page(self):
        self.load_current_page()
        self.showFullScreen()

    def get_bookshelf(self):
        shelfdir=dirname(self.bookfile)
        supported=['.cbr','.cbz']
        self.bookshelf=sorted([os.path.join(shelfdir,fn) for fn in os.listdir(shelfdir) if splitext(fn).lower() in supported])
        self.currentbook_no=self.bookshelf.index[self.bookfile]
        self.lastbook=len(self.bookshelf)-1
    
    def next_book(self):
        if self.currentbook_no!=self.lastbook:
            self.currentbook_no+=1
            self.bookfile=self.bookshelf[self.currentbook_no]
            self.load_book()
            self.load_current_page()
    
    def prev_book(self):
        if self.currentbook_no!=0:
            self.currentbook_no-=1
            self.bookfile=self.bookshelf[self.currentbook_no]
            self.load_book()
            self.load_current_page()

    def load_book(self):
        tempdir=os.path.join(expanduser('~/.morpyus/'),splitext(basename(self.bookfile))[0])
        if exists(tempdir):
            shutil.rmtree(tempdir)
        os.makedirs(tempdir)
        Archive(bookfile).extractall(tempdir)
        pages=self.fetch_pages(tempdir)
        self.pages=pages
        self.lastpage=len(pages)-1
        self.currentpage=0
    
    def load_current_page(self):
        pixmap = QPixmap(self.pages[self.currentpage]).scaledToHeight(self.screen_h)
        lbl = QLabel(self)
        lbl.setPixmap(pixmap)
        lbl.show()
         
    def next_page(self):
        if self.currentpage!=self.lastpage:
            self.currentpage+=1
            self.load_current_page()
    def prev_page(self):
        if self.currentpage!=0:
            self.currentpage-=1
            self.load_current_page()
    def fetch_pages(self,path):
        SUPPORTED = ['.png', '.jpg', '.jpeg', '.gif']
        pages=[]
        for root, dirs, files in os.walk(path):
            pages.extend([os.path.join(root, fname) for fname in sorted(files) if os.path.splitext(fname)[-1].lower() in SUPPORTED])
        return pages

    def keyPressEvent(self, event):
        if type(event) == QKeyEvent:
            action=self.keymap.get(event.key(),None)
            if action:
                action()
            # print event.key()
            # if event.key() == Qt.Key_Escape:
            #     sys.exit(0)
            # if event.key() == Qt.Key_PageDown:
            #     self.next_page()


    def mousePressEvent(self, QMouseEvent):
            #print mouse position
            button= QMouseEvent.button()
            if button==Qt.MouseButton.LeftButton:
                # print 'lb'
                self.next_page()

def main():
    bookfile=sys.argv[1]
    shelfdir=dirname(bookfile)
    supported=['.cbr','.cbz']
    bookshelf=[os.path.join(shelfdir,fn) for fn in os.listdir(shelfdir) if splitext(fn).lower() in supported]
    # tempdir=os.path.join(expanduser('~/.morpyus/'),splitext(basename(bookfile))[0])
    # if exists(tempdir):
    #     shutil.rmtree(tempdir)
    # os.makedirs(tempdir)
    # Archive(bookfile).extractall(tempdir)
    app = QApplication(sys.argv)
    screensize=app.desktop().availableGeometry().width(),app.desktop().availableGeometry().height()
    ex = mainwindow(bookfile,screensize)
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()



