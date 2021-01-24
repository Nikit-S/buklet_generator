from weasyprint import HTML , CSS
import pdfkit
from bs4 import BeautifulSoup
import copy
from weasyprint.fonts import FontConfiguration

while True:
    font_config = FontConfiguration()
    css = CSS('templates\style.css', font_config=font_config)

    url = input("введите имя файла: ")
    doc = r"Buklet_html" + "\\" + url + '.html'
    HTML(doc).write_pdf(r'Buklet'+'\\' + url +'.pdf', stylesheets=[css], font_config=font_config)
