import PyPDF2
from textsummarizer import compressor


def pdfsum(txt):
    myfile = open(txt, 'rb')
    pdfr = PyPDF2.PdfFileReader(myfile)
    origlen = 0
    sumlen = 0
    summd = []
    orig = []
    for p in range(pdfr.numPages):
        title = '<br> PAGE '+str(p+1)+' : <br>'
        strng = pdfr.getPage(p).extractText()
        orig.append(title)
        orig.append(strng)
        reslt, len1, len2 = compressor(strng, 5)
        origlen += len1
        sumlen += len2
        summd.append(title)
        summd.append(reslt)
    return ' '.join(orig), ' '.join(summd), origlen, sumlen
