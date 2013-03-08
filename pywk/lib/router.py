from PySide.QtNetwork import QNetworkAccessManager


"""
    TODO this is a perfect spot to intercept HTTP requests and do almost anything you could ever want to.

    Idea's include using a templating language, on demand SASS/Less, or that JS re-interpreter who's
    name I've forgotten.
"""

class WKNetworkAccessManager(QNetworkAccessManager):

    def createRequest(self, op, request, outgoingData = None):
        try:
            line = op.name, str(request.url().toEncoded()).split("www")[-1], outgoingData
            print line
        except Exception as e:
            print "Error out on createRequest spy", e
        return super(WKNetworkAccessManager, self).createRequest(op, request, outgoingData)