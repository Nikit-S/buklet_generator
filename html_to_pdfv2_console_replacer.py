#!/usr/bin/python
# -*- coding: utf-8 -*-
import difflib
import requests
import re
from requests import get
from bs4 import BeautifulSoup
from lxml import html
import codecs
import copy
import pdfkit
from weasyprint import HTML , CSS
import mysql.connector
import mysql.connector
import requests
import json
import copy
import base64
from tkinter import *
from tkinter import filedialog
import PyPDF2
from weasyprint.fonts import FontConfiguration

font_config = FontConfiguration()


def replacer(text, dic):
  text = dic



def html_to_pdf():
    global T_choose_amount
    global soup
    global set
    global bottles
    global bottle
    global url_name
    global set_id
    global URL
    global SET

    USERNAME='nsh@invisible.ru'
    PASSWORD='IlovevIne4101'


    url_l= re.compile('/product/([a-zA-Z0-9-_].*/+)')

    url_name = url_l.findall(input('?: '))[0][:-1]
    SET_GQL = '''
    {
      products(url: \"''' + url_name + '''\") {
        edges {
          node {
            id
            title
            description
            descriptionFromSet
            smallDescription
            photoSet {
              edges {
                node {
                  image
                  active
                }
              }
            }
            bottlesInSet
            bottles {
              edges {
                node {
                  bottle {
                    year
                    title
                    placeOfProduction
                    country {
                      name
                    }
                    type
                    naVkus
                    sChem
                    vinograd
                    krepkost
                    description
                  }
                }
              }
            }
          }
        }
      }
    }'''


    access_token, refresh_token = get_token(USERNAME, PASSWORD)
    SET = query(access_token, SET_GQL)

    for i in SET['products']['edges'][0]['node']:
        exec('set.' + str(i) + ' = SET[\'products\'][\'edges\'][0][\'node\'][i]')
        if i == 'bottles':
            for f in SET['products']['edges'][0]['node']['bottles']['edges']:
                for s in f['node']['bottle']:
                    exec('bottle.' + str(s) + ' = f[\'node\'][\'bottle\'][s]')
                bottles.append(copy.copy(bottle))

    for i in [0,1]:
        if set.photoSet['edges'][i]['node']['active'] == False:
            del set.photoSet['edges'][i]
            set.photoSet = 'https://www.invisible.ru/media/' + str(set.photoSet['edges'][0]['node']['image'])
            break

    URL = 'https://www.invisible.ru/product/'+ url_name +'/?token='
    set_id = set.id
    page = requests.get(URL)
    soup = BeautifulSoup(page.text, 'html.parser')

    Template()
    Buklet()
    SavingPDF()


def Template():
    global template
    global template_rout
    global wine_color_dic
    global set
    global soup

    if len(bottles) == 1:
        template_rout = r"templates\html_pdf_yashik.html"
        if set.bottlesInSet//len(bottles) == 2 or set.bottlesInSet//len(bottles) == 3:
            template_rout = 'templates\html_pdf_one.html'

    if len(bottles) == 2:
        template_rout = r"templates\html_pdf_two.html"

    if len(bottles) == 3:
        template_rout = r"templates\html_pdf_three.html"

    if len(bottles) == 4:
        template_rout = r"templates\html_pdf_four.html"

    if len(bottles) == 5:
        template_rout = r"templates\html_pdf_five.html"

    if len(bottles) == 6:
        template_rout = r"templates\html_pdf_six.html"

    if len(bottles) == 7:
        template_rout = r"templates\html_pdf_seven.html"

    if len(bottles) == 10:
        template_rout = r"templates\html_pdf_ten.html"

    with codecs.open(template_rout, "r", encoding='utf_8') as f:
        template=f.read()


def Buklet():

    global URL
    global set_name
    global set_img
    global set_long_dis
    global Bottle
    global bottles
    global template_rout
    global wine_color_dic
    global template
    global color_photo


    with codecs.open(template_rout, "r", encoding='utf_8') as f:
        template=f.read()

    template = template.replace('%set.title%', set.title)
    template = template.replace('%set.descriptionFromSet%', set.descriptionFromSet)
    template =  template.replace('%set.description%', set.description)
    print(set.photoSet)
    template =  template.replace('%set.photoSet%', set.photoSet)



    di = ['description','naVkus','sChem','vinograd','krepkost','name']


    li_c = []
    split = set.bottlesInSet//len(bottles)
    print(split)

    for i in range(len(bottles)):
        for g in range(split):
            li_c.append(bottles[i].color())


    for c in range(len(li_c)):
        try:
            template = template.replace('%type' + str(c+1) + '%', wine_color_dic[li_c[c]])
        except:
            template = template.replace('%type' + str(c+1) + '%', "black;")

    for i in range(len(bottles)):

        try:
            template = template.replace('%bottle_color' + str(i+1) + '%', bottles[i].color())
        except:
            template = template.replace('%bottle_color' + str(i+1) + '%', "black;")

        for l in range(len(di)):
            try:
                exec('template = template.replace(\'%' + di[l] + str(i+1) + '%\', bottles['+ str(i)+'].' + di[l] + ')', globals())
            except TypeError as e:
                exec('template = template.replace(\'%' + di[l] + str(i+1) + '%\', bottles['+ str(i)+'].' + di[l] + '())', globals())




def SavingPDF():

    global URL
    global set_name
    global set_img
    global set_long_dis
    global Bottle
    global template
    global url_name
    global font_config
    def checking_name(a):
        try:
            with open('Buklet_html'+'\\' + a + '.html') as f:
                if a.count('.') == 1:
                    a = a + '.1'
                    return checking_name(a)

                if a.count('.') == 2:
                    add = str(int(a[-1])+1)
                    print(a[-1], adds)
                    del a[-1]
                    a = a + add
                    return checking_name(a)

        except:
            return a

    save_rout = 'Buklet_html'+'\\' + url_name + '.html'

    Html_file= codecs.open(save_rout,"w", 'utf_8_sig')

    Html_file.write(template)
    Html_file.close()


    css = CSS(r'templates\style.css',font_config=font_config)
    pdf_rout ='Buklet' +'\\'+ url_name + '.pdf'
    HTML(save_rout).write_pdf(pdf_rout, stylesheets=[css], font_config=font_config)

    pdfFileObj = open(pdf_rout, 'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)

    if pdfReader.numPages == 3:

        print('3 pages!!!, im deleting logo')
        template = template.replace('<div class=\'logo\'><img src="https://www.invisible.ru/media/2019/11/15/invisible_pdf_logo.png" alt="second logo"></div>', '')
        Html_file= codecs.open(save_rout,"w", 'utf_8_sig')
        Html_file.write(template)
        Html_file.close()

        HTML(save_rout).write_pdf(pdf_rout, stylesheets=[css], font_config=font_config)

    if pdfReader.numPages == 3:

        print('БЛИН, ВСЕ ЕЩЕ 3!!!, СЖИМАЮ ДО СОСТОЯНИЯ АЛМАЗА')
        template = template.replace('style=\'%%%\'', 'style=\'margin-top:-0.3cm;\'')
        template = template.replace('margin-top:-0.5cm','margin-top:-0.7cm')
        Html_file= codecs.open(save_rout,"w", 'utf_8_sig')
        Html_file.write(template)
        Html_file.close()
        HTML(save_rout).write_pdf(pdf_rout, stylesheets=[css], font_config=font_config)


    if pdfReader.numPages == 3:

        print('ЭТО УЖЕ НЕ СМЕШНО!!!, уменьшаю заголовки')
        template = template.replace('<style>', '''<style>
        .wine_dis_name{
       font-size: 12.5pt;
       line-height: 13pt;
      }''')

        Html_file= codecs.open(save_rout,"w", 'utf_8_sig')
        Html_file.write(template)
        Html_file.close()
        HTML(save_rout).write_pdf(pdf_rout, stylesheets=[css], font_config=font_config)

    if pdfReader.numPages == 3:

        print('-03 to -04!!!')
        template = template.replace('-0.3cm', '-0.4cm')

        Html_file= codecs.open(save_rout,"w", 'utf_8_sig')
        Html_file.write(template)
        Html_file.close()
        HTML(save_rout).write_pdf(pdf_rout, stylesheets=[css], font_config=font_config)




while True:
    #root = Tk()
    #root_file=""
    wine_color_dic = {'#a22554':'https://www.invisible.ru/media/2019/11/08/red_wine_logo4x.png','#cad52d':'https://www.invisible.ru/media/2019/11/08/white_wine_logo4x.png','#e36a66':'https://www.invisible.ru/media/2019/11/08/roz_wine_logo4x.png'}
    TYPE_OF_VINE = (
        (0, u'белое сухое'),
        (1, u'красное сухое'),
        (2, u'розовое сухое'),
        (3, u'игристое белое брют'),
        (4, u'игристое белое сухое'),  # в оригинале было - игристое белое сухое
        (5, u'игристое розовое брют'),
        (6, u'игристое розовое сухое'),
        (7, u'игристое белое полусладкое'),
        (8, u'игристое красное'),

        (9, u'белое полусухое'),
        (10, u'белое полусладкое'),
        (11, u'белое сладкое'),
        (12, u'красное полусухое'),
        (13, u'розовое полусухое'),
        (14, u'игристое белое полусухое'),
        (15, u'игристое белое полусладкое'),
        (16, u'игристое розовое полусухое'),
        (17, u'игристое белое сладкое'),
        (18, u'красное крепленое'),
        (19, u'белое крепленое'),
        (20, u'коньяк'),
        (21, u'арманьяк'),
        (22, u'кальвадос'),
        (23, u'виски'),
        (24, u'бурбон'),
        (25, u'ром'),
        (26, u'текила'),
        (27, u'джин'),
        (28, u'граппа'),
        (29, u'ликер'),

        (30, u'красное сладкое'),
        (31, u'пиво'),

        (32, u'игристое'),
        (33, u'розовое полусладкое'),
        (34, u'сидр'),
        (35, u'белое полусладкое безалкогольное'),
        (36, u'розовое крепленое'),
        (37, u'напиток винный ароматизированный игристый сладкий'),
        (38, u'жемчужное белое экстрабрют'),
        (39, u'аперитив'),
        (40, u'1'),
        (41, u'2'),
        (42, u'3'),
        (43, u'4'),
        (44, u'5'),
        (45, u'сидр игристый, сладкий'),
        (46, u'сидр игристый, полусухой'),
        (47, u'8'),
        (48, u'сидр игристый, брют'),
        (49, u'10'),
        (50, u'11'),
        (51, u'12'),
        (52, u'13'),
        (53, u'14'),
        (54, u'15'),
        (55, u'16'),
        (56, u'17'),
        (57, u'18'),
        (58, u'пуаре игристый, брют')
    )

    class SET:
        def __init__(
            self,
            id,
            title,
            description,
            descriptionFromSet,
            smallDescription,
            bottles,
            photoSet,
            bottlesInSet):
                self.id = id
                self.title = title
                self.description = description
                self.descriptionFromSet = descriptionFromSet
                self.smallDescription =  smallDescription
                self.bottles = bottles
                self.photoSet = photoSet
                self.bottlesInSet = bottlesInSet
        def dic(self):
            dic = {
                "title": self.title,
                "description": self.description ,
                "descriptionFromSet": self.descriptionFromSet,
                "smallDescription": self.smallDescription,
                "bottles": self.bottles,
                "photoSet": self.photoSet,
                "bottlesInSet": self.bottlesInSet
            }
            return dic

    class Bottle:
        def __init__(
            self,
            year,
            title,
            placeOfProduction,
            country,
            type,
            description,
            naVkus,
            sChem,
            vinograd,
            krepkost):
                self.year = year
                self.title = title
                self.placeOfProduction = placeOfProduction
                self.country = country
                self.type = type
                self.description = description
                self.naVkus = naVkus
                self.sChem = sChem
                self.vinograd = vinograd
                self.krepkost = krepkost

        def name(self):
            print(self.type)
            name = self.year +' ' + self.title +' '+ self.placeOfProduction +', '+ self.country['name'] +', '+ TYPE_OF_VINE[int(self.type[self.type.find('_')+1:])][1]
            return name

        def color(self):
            if self.name().find('красное') != -1:
                return '#a22554'

            if self.name().find('розовое') != -1:
                return '#e36a66'

            if self.name().find('белое') != -1:
                return '#cad52d'

    set= SET('','','','','','','','')
    bottles = []
    bottle = Bottle('','','','','','','','','','')
    url_name = ''
    URL = ''
    SET =''


    def get_token(username, password):
        r = requests.post('https://www.invisible.ru/account/login/', data={'username': username, 'password': password})
        r.raise_for_status()
        data = r.json()
        # print('get_token: {}'.format(data))
        return data['access_token'], data['refresh_token']

    def query(access_token, gql):
        r = requests.get('http://www.invisible.ru/api/graphql/?query={}'.format(gql), headers={'Authorization': 'bearer {}'.format(access_token)})
        r.raise_for_status()
        data = r.json()
        return data['data']

    '''mydb = mysql.connector.connect(
      host="88.212.254.18",
      user="nikita",
      passwd="iph7Aen8aediM4rahjaiSuoH",
      database="invisible2"
    )

    global T_choose_amount
    T_choose_amount = Text(root, height=1, font="Arial, 8")
    T_choose_amount.pack()
    start_button = Button(root, text="Выполнить", command = html_to_pdf)
    start_button.pack(side=RIGHT)
    root.mainloop()
'''
    html_to_pdf()
    print("Yup!")
