import sys
from contextlib import contextmanager

#from PySide.QtCore import QApplication
from PySide.QtCore import QObject, Slot, Signal
from PySide.QtGui import QApplication, QMainWindow
from PySide.QtWebKit import QWebView, QWebSettings, QWebInspector, QWebPage


from router import WKNetworkAccessManager

@contextmanager
def RunMe():
    """
        Shortcut to launch a QApplication and kick start the QT rendering library.

        Was surprised this "works".  I am assuming the other QT objects
        survive because they've self-registered to QT.

        Otherwise the intention is to expose as little of QT as possible in preparation for
        pywk V2 which may or may not happen.  If it does, the less Python knows about QT the to pull the mess off.

    """
    app = QApplication(sys.argv)
    yield app
    sys.exit(app.exec_())



class WebPage(QWebPage):
    def javaScriptConsoleMessage(self, msg, line, source):
        line = '%s line %d: %s' % (source.split("www")[-1], line, msg)
        print line


class HTMLApplication(object):

    def __init__(self, index_file, bridge = None,  parent = None):
        self.index_file = index_file
        self.bridge = bridge
        self.mainWindow = QMainWindow(parent)
        self.mainWindow.setWindowTitle("My hub")
        self.mainWindow.setFixedSize(290,550);

        #This is basically a browser instance
        self.web = QWebView()
        self.mainWindow.setCentralWidget(self.web);

    def show(self):
        #It is IMPERATIVE that all forward slashes are scrubbed out, otherwise QTWebKit seems to be
        # easily confused



        #Asyncronously loads the website, in the interim you could throw up a splash screen
        # but this is relatively quick so it might not be worth it.
        self.web.loadFinished.connect(self.onLoad)
        self.web.setPage(WebPage())
        self.web.load(self.index_file)



        self.mainWindow.show()
        #self.web.show()

    def onLoad(self):

        self.myPage = self.web.page()
        self.myPage.settings().setAttribute(QWebSettings.DeveloperExtrasEnabled, True)

        self.myPage.setNetworkAccessManager(WKNetworkAccessManager())

        self.myFrame = self.myPage.mainFrame()
        for name, obj in self.bridge.items():
            self.myFrame.addToJavaScriptWindowObject(name, obj)

        self.myFrame.evaluateJavaScript("ApplicationIsReady();")

    def onReload(self):
        print "reloaded"