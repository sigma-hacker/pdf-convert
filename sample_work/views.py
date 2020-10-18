from django.shortcuts import render,redirect
from django.http import HttpResponse
from PyPDF2 import PdfFileWriter, PdfFileReader
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from googletrans import Translator
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os
import reportlab
# pdfmetrics.registerFont(TTFont('Hindi1', 'gargi.ttf'))
# Create your views here.
def index(request):
    # reportlab_directory = os.path.dirname(reportlab.__file__)
    # print(reportlab_directory)
    return render(request,'index.html')
def translatesave(request):
    if request.method == "POST":
        # getting user feilds
        word = request.POST['word']
        username = request.POST['user']
        language = request.POST['lang']
        #translating word
        translator = Translator()
        translated = translator.translate(word,language)
        text = str(translated.text)
        # writing to pdf
        pouch = io.BytesIO()
        can = canvas.Canvas(pouch, pagesize=letter)
        can.drawString(80, 715,username)
        can.drawString(305, 715, text)
        can.save()
        pouch.seek(0)
        new_pdf = PdfFileReader(pouch)
        existing_pdf = PdfFileReader(open("original.pdf", "rb"))
        output = PdfFileWriter()
        page = existing_pdf.getPage(0)
        page.mergePage(new_pdf.getPage(0))
        output.addPage(page)
        outputStream = open(f"{username}.pdf", "wb")
        output.write(outputStream)
        outputStream.close()
    return redirect("/")