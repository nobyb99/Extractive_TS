from flask import Flask, render_template, request
from textsummarizer import compressor
from webscraper import spider
from pdfsum import pdfsum

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('homepage.html')


@app.route('/summarizer', methods=['POST'])
def summarize():
    if request.method == 'POST':
        content = request.form['plaintext']
        num = request.form['num']
        if num is not None:
            summarized, lenorig, lensum = compressor(content, int(num))
        else:
            summarized, lenorig, lensum = compressor(content, 5)

        return render_template('summarized.html', orig=content, summed=summarized, lensum=lensum, lenorig=lenorig)


@app.route('/scraper', methods=['POST'])
def scrape():
    if request.method == 'POST':
        link = request.form['urllink']
        content, title = spider(link)
        compressed, lenorig, lensum = compressor(content, 5)

        return render_template('summarized.html', orig=content, title=title, summed=compressed, lensum=lensum, lenorig=lenorig)


@app.route('/pdfsum', methods=['POST'])
def pdf():
    if request.method == 'POST':
        content = request.form['contentpdf']
        summarized, lenorig, lensum = compressor(content, 5)

        return render_template('summarized.html', orig=content, summed=summarized, lensum=lensum, lenorig=lenorig)


if __name__ == "__main__":
    app.run(debug=True)
