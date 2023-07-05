from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import NoSuchElementException
import time
import math
import wget
import pdfkit
import fitz
import sys
import os
import pathlib


def WordSplit(word):

    if "+" in word:
        index = word.find("+")
        word_real = word[0:index]+" "+word[index+1:]

    else:
        word_real = word

    return word_real


def CreateFolder(word, path):
    folderlist = os.listdir(path+"\\Çıktılar")
    count = 0
    wordfolder = word

    while wordfolder in folderlist:
        count += 1
        wordfolder = word+" - "+str(count)

    os.chdir(path+"\\Çıktılar\\")
    os.makedirs(wordfolder)
    os.chdir(path+"\\Çıktılar\\"+wordfolder)
    os.makedirs("PDF Dosyaları")

    return wordfolder


def Search(word):

    browser = webdriver.Firefox()
    browser.get("https://www.resmigazete.gov.tr/")

    time.sleep(1)
    browser.find_element("xpath", "/html/body/div[2]/div/div/div/div/div[1]/div/button").click()

    time.sleep(1)
    browser.find_element("xpath", "//*[@id='genelaranacakkelime']").send_keys(word)

    time.sleep(1)
    browser.find_element("xpath", "//*[@id='btnFilterSearch']").click()

    time.sleep(2)
    browser.find_element("xpath", "//*[@id='nav-Icerik-tab']").click()

    time.sleep(2)
    Select(browser.find_element("xpath", "//*[@id='filterTableIcerik_length']/label/select")).select_by_value("100")

    return browser


def PageNumber():

    time.sleep(1)
    record = browser.find_element("xpath", "//*[@id='filterTableIcerik_info']").text
    index1 = record.find(" ")
    record_output = record[0:index1]
    if "," in record_output:
        index2 = record.find(",")
        record_real = int(record_output[0:index2]+record_output[index2+1:])

    else:
        record_real = int(record_output)

    remainder = record_real % 100
    if remainder == 0:
        page_number = record_real/100
    else:

        if record_real > 0 and record_real <= 100:
            page_number = math.floor(record_real/100)
        page_number = math.ceil(record_real/100)

    return page_number, remainder, record_real


def LastPage(page_number):

    if page_number != 1:
        if page_number >= 7:
            browser.find_element("xpath", "//*[@id='filterTableIcerik_paginate']/ul/li[8]").click()
            
        elif page_number == 6:
            browser.find_element("xpath", "//*[@id='filterTableIcerik_paginate']/ul/li[7]").click()
        
        elif page_number == 5:
            browser.find_element("xpath", "//*[@id='filterTableIcerik_paginate']/ul/li[6]").click()
        
        elif page_number == 4:
            browser.find_element("xpath", "//*[@id='filterTableIcerik_paginate']/ul/li[5]").click()
        
        elif page_number == 3:
            browser.find_element("xpath", "//*[@id='filterTableIcerik_paginate']/ul/li[4]").click()
        
        elif page_number == 2:
            browser.find_element("xpath", "//*[@id='filterTableIcerik_paginate']/ul/li[3]").click()  

def Next():

    time.sleep(1)
    browser.find_element("xpath", "//*[@id='filterTableIcerik_next']").click()


def Previous():
    time.sleep(1)
    browser.find_element("xpath", "//*[@id='filterTableIcerik_previous']").click()


def GetLink(number):

    output_link = browser.find_element("xpath", "//*[@id='filterTableIcerik']/tbody/tr["+str(number)+"]/td/div/a").get_attribute('href')

    return output_link


def GetName(number):

    output_name = browser.find_element("xpath", "//*[@id='filterTableIcerik']/tbody/tr["+str(number)+"]/td/div/a").text

    return output_name


def Download(href, name, word, path, wordfolder):

    pdfname = name+".pdf"

    if ".htm" in href:

        config = pdfkit.configuration(
            wkhtmltopdf=path+"\\env\\Lib\\site-packages\\wkhtmltopdf\\bin\\wkhtmltopdf.exe")
        options = {"no-images": ""}
        pdfkit.from_url(href, path+"\\Çıktılar\\"+wordfolder+"\\PDF Dosyaları\\"+pdfname, configuration=config, options=options)

    else:

        wget.download(href, out=path+"\\Çıktılar\\"+wordfolder+"\\PDF Dosyaları\\"+pdfname)

    return pdfname


def PdfToString(pdfname, word, path, wordfolder):

    pdfOpen = fitz.open(path+"\\Çıktılar\\"+wordfolder+"\\PDF Dosyaları\\"+pdfname)

    text = ""
    for i in pdfOpen:
        text += i.get_text()

    return text


def Result(text, word_real):

    if "I" in text:
        text = text.replace("I", "ı")
    if "İ" in text:
        text = text.replace("İ", "i")
    if "Ğ" in text:
        text = text.replace("Ğ", "ğ")
    if "Ü" in text:
        text = text.replace("Ü", "ü")
    if "Ö" in text:
        text = text.replace("Ö", "ö")
    if "U" in text:
        text = text.replace("U", "u")
    if "O" in text:
        text = text.replace("O", "o")
    if "Ç" in text:
        text = text.replace("Ç", "ç")
    if "Ş" in text:
        text = text.replace("Ş", "ş")

    if "I" in word_real:
        word_real = word_real.replace("I", "ı")
    if "İ" in word_real:
        word_real = word_real.replace("İ", "i")
    if "Ğ" in word_real:
        word_real = word_real.replace("Ğ", "ğ")
    if "Ü" in word_real:
        word_real = word_real.replace("Ü", "ü")
    if "Ö" in word_real:
        word_real = word_real.replace("Ö", "ö")
    if "U" in word_real:
        word_real = word_real.replace("U", "u")
    if "O" in word_real:
        word_real = word_real.replace("O", "o")
    if "Ç" in text:
        word_real = word_real.replace("Ç", "ç")
    if "Ş" in word_real:
        word_real = word_real.replace("Ş", "ş")

    text_little = text.lower()
    word = word_real.lower()
    index = text_little.find(word)
    print(index)

    if index < 601 and index != -1:
        result = text_little[0:index+600]
        print("Aranan kelime bu çıktıda bulundu.")
    elif index > 601 and index != -1:
        result = text_little[index-600:index+600]
        print("Aranan kelime bu çıktıda bulundu.")
    else:
        result = ""
        print("Aranan kelime bu çıktıda bulunamadı.")

    return result


def Write(result, name, word, path, count, wordfolder):
    txt = open(path+"\\Çıktılar\\"+wordfolder+"\\" +word+".doc", "a", encoding="utf-8")
    txt.writelines(name+"\t\t\t\t\t"+str(count)+". Çıktı\n\n")
    txt.writelines(result+"\n\n")
    txt.writelines("************************************************************************* \n\n")
    txt.close()
    os.remove(path+"\\Çıktılar\\"+wordfolder+"\\PDF Dosyaları\\"+pdfname)


word = input("Lütfen aranacak kelimeyi giriniz: ")
sort = input("Aramaya baştan mı yoksa sondan mı başlansın? ([b]aştan, [s]ondan): ")
path = str(pathlib.Path(__file__).parent.resolve())
wordfolder = CreateFolder(word, path)
word_real = WordSplit(word)
browser = Search(word)
page_variable = PageNumber()

if sort == "s":
    LastPage(page_variable[0])
    count = page_variable[2]
    
    if page_variable[2] <= 100:
        for number in range(page_variable[1], 0, -1):
            print(str(count)+". Çıktı.")
            href = GetLink(number)
            name = GetName(number)
            pdfname = Download(href, name, word, path, wordfolder)
            text = PdfToString(pdfname, word, path, wordfolder)
            result = Result(text, word_real)
            Write(result, name, word, path, count, wordfolder)
            count -= 1
            if number == 1:
                browser.close()
                print("\nİstenilen kelimeler arandı ve sonuçlar yazdırıldı.")
                sys.exit()
                
            
    else:
    
        for page in range(page_variable[0], 0, -1):
            
            if page == page_variable[0]:
                
                if page_variable[1] == 0:
                    for number in range(100, 0, -1):
                        print(str(count)+". Çıktı.")
                        href = GetLink(number)
                        name = GetName(number)
                        pdfname = Download(href, name, word, path, wordfolder)
                        text = PdfToString(pdfname, word, path, wordfolder)
                        result = Result(text, word_real)
                        Write(result, name, word, path, count, wordfolder)
                        count -= 1
                
                else:
                    for number in range(page_variable[1], 0, -1):
                        print(str(count)+". Çıktı.")
                        href = GetLink(number)
                        name = GetName(number)
                        pdfname = Download(href, name, word, path, wordfolder)
                        text = PdfToString(pdfname, word, path, wordfolder)
                        result = Result(text, word_real)
                        Write(result, name, word, path, count, wordfolder)
                        count -= 1
                    
                Previous()
                time.sleep(2)
            
            else:
                for number in range(100,0,-1):
                    print(str(count)+". Çıktı.")
                    href = GetLink(number)
                    name = GetName(number)
                    pdfname = Download(href, name, word, path, wordfolder)
                    text = PdfToString(pdfname, word, path, wordfolder)
                    result = Result(text, word_real)
                    Write(result, name, word, path, count, wordfolder)
                    count -= 1
                
                if page == 1:
                    browser.close()
                    print("\nİstenilen kelimeler arandı ve sonuçlar yazdırıldı.")
                    sys.exit()
                
                Previous()
                time.sleep(2)   
                    
            
else:
    count = 0
    
    if page_variable[2] <= 100:
        for number in range(1, page_variable[1]+1):
            count += 1
            print(str(count)+". Çıktı.")
            href = GetLink(number)
            name = GetName(number)
            pdfname = Download(href, name, word, path, wordfolder)
            text = PdfToString(pdfname, word, path, wordfolder)
            result = Result(text, word_real)
            Write(result, name, word, path, count, wordfolder)
            if number == page_variable[1]:
                browser.close()
                print("\nİstenilen kelimeler arandı ve sonuçlar yazdırıldı.")
                sys.exit()
    else:
    
        for page in range(1, page_variable[0]+1):
    
            if page_variable[1] == 0:
    
                for number in range(1, 101):
                    count += 1
                    print(str(count)+". Çıktı.")
                    href = GetLink(number)
                    name = GetName(number)
                    pdfname = Download(href, name, word, path, wordfolder)
                    text = PdfToString(pdfname, word, path, wordfolder)
                    result = Result(text, word_real)
                    Write(result, name, word, path, count, wordfolder)
                    if number == 100:
                        browser.close()
                        print("\nİstenilen kelimeler arandı ve sonuçlar yazdırıldı.")
                        sys.exit()
    
            else:
    
                if page == page_variable[0]:
    
                    for number in range(1, page_variable[1]+1):
                        count += 1
                        print(str(count)+". Çıktı.")
                        href = GetLink(number)
                        name = GetName(number)
                        pdfname = Download(href, name, word, path, wordfolder)
                        text = PdfToString(pdfname, word, path, wordfolder)
                        result = Result(text, word_real)
                        Write(result, name, word, path, count, wordfolder)
                        if number == page_variable[1]:
                            browser.close()
                            print("\nİstenilen kelimeler arandı ve sonuçlar yazdırıldı.")
                            sys.exit()
                else:
                    for number in range(1, 101):
                        count += 1
                        print(str(count)+". Çıktı.")
                        href = GetLink(number)
                        name = GetName(number)
                        pdfname = Download(href, name, word, path, wordfolder)
                        text = PdfToString(pdfname, word, path, wordfolder)
                        result = Result(text, word_real)
                        Write(result, name, word, path, count, wordfolder)
            Next()
            time.sleep(2)
