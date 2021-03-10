# encoding: utf-8
from __future__ import unicode_literals
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from datetime import datetime
import base64, string, os, shutil, time, sys, re
from os import path


now = datetime.now()
log_path = "C:\\Python27\\array\\logs\\"
reload(sys)
sys.setdefaultencoding('utf-8')
#sys.stdout = open(log_path + 'output - ' + now.strftime("%d%m%Y_%H%M") + '.txt', 'w')
with open("ruta_descargas.txt", "r") as downloads:
    src = downloads.read()
with open("ruta_docs_entrantes.txt", "r") as doc_entrantes:
    src_entrantes = doc_entrantes.read()
print "\n###############################################\nRobot by array consulting group 2021\nExtraccion de datos y asignacion de documentos entrantes en oficina de partes SSFFAA\n###############################################\n"

# Inicio de Chrome Webdriver
options = Options()
options.add_argument('--hide-scrollbars')
options.add_argument('--disable-gpu')
options.add_argument("--log-level=3")
options.add_argument("--incognito")
driver = webdriver.Chrome(executable_path="C:/Python27/array/webdriver/chromedriver.exe", chrome_options=options)
driver.maximize_window()

# Ingreso a doc.digital
try:
    print("Ingresando a https://demodoc.digital.gob.cl\n")
    driver.get("https://demodoc.digital.gob.cl/")
except NoSuchElementException, e:
    print "No fue posible ingresar a la plataforma."
    print e

# Ingreso de clave unica
try:
    driver.execute_script("$('a#buttonCUnica').click();")
    print("Ingresando rut y clave unica\n")
    with open('credenciales.txt', 'r') as file:
        for line in file:
            user, password = line.split(':')
            driver.find_element_by_id("inputUsuario").send_keys(user)
            driver.find_element_by_id("inputPassword").send_keys(password)
    driver.execute_script("$('#formClaveUnica > form > fieldset > div.row > div > div.main > div:nth-child(3) > div > button').click();")
    time.sleep(2)
except NoSuchElementException, e:
    print "No fue posible autentificarse, revise sus credenciales."
    print e

# Ir a Oficina de Partes / Documentos entrantes
try:
    print("Ingresando a: Oficina de partes / Documentos entrantes\n")
    time.sleep(2)
    driver.get("https://demodoc.digital.gob.cl/fed/inbox#/oficinapartes/entrada/sin_asignar")
    time.sleep(2)
except NoSuchElementException, e:
    print "No fue posible acceder a la ruta: https://demodoc.digital.gob.cl/fed/inbox#/oficinapartes/entrada/sin_asignar"
    print e

# Proceso de extraccion de datos.
try:
    print("Ordenando la tabla por resposanble...")
    order_responsible = driver.find_element_by_xpath("//*[@id='content']/div/div[2]/div/div/div[4]/div/table/thead/tr/th[9]/a")
    time.sleep(2)
    order_responsible.click()
    time.sleep(2)
    order_responsible.click()
    print("Buscando si existen documentos en la tabla.\n")
    driver.execute_script('$("#content > div > div:nth-child(2) > div > div > div:nth-child(2) > div.col-xs-2.col-sm-8.options-table > div:nth-child(1) > button").click()')
    time.sleep(1)
    driver.execute_script('$("#content > div > div:nth-child(2) > div > div > div:nth-child(2) > div.col-xs-2.col-sm-8.options-table > div.btn-group.hidden-xs.open > ul > li:nth-child(4)").click()')
    time.sleep(1)
    table_path = driver.find_element(By.XPATH, '//*[@id="content"]/div/div[2]/div/div/div[4]/div/table/tbody')
    rows = table_path.find_elements(By.TAG_NAME, "tr")
    counter = 1
    print("Existen " + str(len(rows)) + " documentos para extraccion de datos y asignacion.\n")
    for row in rows:
        check_responsible = driver.find_element_by_xpath("//*[@id='content']/div/div[2]/div/div/div[4]/div/table/tbody/tr[" + str(counter) + "]/td[9]")
        check_docname = driver.find_element_by_xpath("//*[@id='content']/div/div[2]/div/div/div[4]/div/table/tbody/tr[" + str(counter) + "]/td[3]/div[2]")
        #print(check_responsible.text)
        if check_responsible.text == "---":
            time.sleep(2)
            viewdoc = driver.find_element_by_xpath("//*[@id='content']/div/div[2]/div/div/div[4]/div/table/tbody/tr[" + str(counter) + "]/td[10]/a")
            time.sleep(2)
            viewdoc.click()
            time.sleep(6)
            #driver.execute_script('var txt=$("#content > div > div.table-content.container-fluid > div:nth-child(2) > div.col-xs-12.col-sm-7 > div:nth-child(1) > div > a").attr("href"),ret=txt.replace("oficiometro/document/","");console.log(ret);')
            # Getting current URL
            #get_url = driver.current_url
            get_href = driver.find_element_by_xpath("//*[@id='content']/div/div[2]/div[2]/div[3]/div[1]/div/a").get_attribute("href")
            doc_id = get_href[-5:]
            try:
                download = driver.find_element_by_xpath("""//*[@id="content"]/div/div[2]/div[2]/div[3]/div[1]/div/a""")
            except NoSuchElementException, e:
                print 'No fue posible encontrar el botón "Descargar"'
                print e

            driver.execute_script("$('#content > div > div.table-content.container-fluid > div:nth-child(2) > div.col-xs-12.col-sm-7 > div:nth-child(3) > div > accordion > div > div:nth-child(1) > div.panel-collapse.in.collapse > div > table > tbody > tr > td strong').remove('strong');")
            nd = driver.find_element_by_xpath("""//*[@id="content"]/div/div[2]/div[2]/div[3]/div[2]/div/accordion/div/div[1]/div[2]/div/table/tbody/tr[1]/td""")  # Nombre del documento
            print("Creando carpeta\n")
            folder_path = os.path.join(src_entrantes, datetime.now().strftime("%d%m%Y_%H%M") + "_" + str(counter))
            os.mkdir(folder_path)
            file_name = nd.text.encode('utf-8') + ' - ' + datetime.now().strftime("%d%m%Y_%H%M")
            file_folder_name = datetime.now().strftime("%d%m%Y_%H%M") + "_" + str(counter)
            new_path = src_entrantes + file_folder_name
            print('Carpeta "' + new_path + '" creada.\n')
            print("Descargando documento PDF\n")
            time.sleep(3)
            download.click()
            time.sleep(2)
            filename = str(nd.text.encode('utf8')) + ".pdf"
            #source = 'C:\\Users\\\salva\\Downloads\\'
            files = [filename]
            for f in files:
                shutil.move(src + f, new_path)
            new_filename = file_name + ".pdf"
            os.chdir(new_path)
            os.rename(filename, new_filename)
            io = driver.find_element_by_xpath("""//*[@id="content"]/div/div[2]/div[2]/div[3]/div[2]/div/accordion/div/div[1]/div[2]/div/table/tbody/tr[7]/td""") #Oficina de partes saliente
            ae = driver.find_element_by_xpath("""//*[@id="content"]/div/div[2]/div[2]/div[3]/div[2]/div/accordion/div/div[1]/div[2]/div/table/tbody/tr[6]/td""") #Descripcion / Nombre del doc
            uo = driver.find_element_by_xpath("""//*[@id="content"]/div/div[2]/div[2]/div[3]/div[2]/div/accordion/div/div[1]/div[2]/div/table/tbody/tr[5]/td""") #Creado por
            td = driver.find_element_by_xpath("""//*[@id="content"]/div/div[2]/div[2]/div[3]/div[2]/div/accordion/div/div[1]/div[2]/div/table/tbody/tr[9]/td""") #Tipo
            fo = driver.find_element_by_xpath("""//*[@id="content"]/div/div[2]/div[2]/div[3]/div[2]/div/accordion/div/div[1]/div[2]/div/table/tbody/tr[2]/td""") #Folio
            ff = driver.find_element_by_xpath("""//*[@id="content"]/div/div[2]/div[2]/div[3]/div[2]/div/accordion/div/div[1]/div[2]/div/table/tbody/tr[3]/td""") #Fecha folio
            gs = driver.find_element_by_xpath("""//*[@id="content"]/div/div[2]/div[2]/div[3]/div[2]/div/accordion/div/div[1]/div[2]/div/table/tbody/tr[8]/td""") #Reservado
            ff_transform = ff.text
            res = str(ff_transform).replace('/', '-').replace(' a las', '').replace(' horas', ':30')
            print('Extrayendo datos del documento "' + str(nd.text) + '" para generar archivo .txt\n')
            route_file = src_entrantes + file_folder_name + "\\" + file_name + ".txt"
            txtfile = open(route_file, 'w')
            txtfile.write("IO:" + io.text + "\n")
            txtfile.write("AS:" + ae.text + "\n")
            txtfile.write("UO:" + uo.text + "\n")
            txtfile.write("FO:" + fo.text + "\n")
            if td.text == 'Memorando':
                txtfile.write("TD:Memorándum\n")
                txtfile.write("ND:Memorándum + " + fo.text + "\n")
            if td.text == 'Resoluciones':
                txtfile.write("TD:Resolución\n")
                txtfile.write("ND:Resolución + " + fo.text + "\n")
            if td.text == 'Carta':
                txtfile.write("TD:Carta\n")
                txtfile.write("ND:Carta + " + fo.text + "\n")
            if td.text == 'Oficio':
                txtfile.write("TD:Oficio\n")
                txtfile.write("ND:Oficio + " + fo.text + "\n")
            if td.text == 'Circular':
                txtfile.write("TD:Circular\n")
                txtfile.write("ND:Circular + " + fo.text + "\n")
            if td.text == 'Convenios':
                txtfile.write("TD:Convenio\n")
                txtfile.write("ND:Convenio + " + fo.text + "\n")
            #if not any(('Memorando', 'Resoluciones', 'Carta', 'Oficio', 'Circular')):
                #txtfile.write("TD:Otros\n")
                #txtfile.write("ND:Otros + " + fo.text + "\n")
            txtfile.write("FF:" + res + "\n")
            if gs.text == 'Si':
                txtfile.write("GS:Reservado\n")
            else:
                txtfile.write("GS:Público\n")
            txtfile.write("MA:" + nd.text)
            txtfile.close()
            print('Extraccion de datos para el documento "' + str(nd.text) + '" realizado con exito. Pasando al siguiente documento...\n-----------------------------------------\n')
            time.sleep(2)
            driver.get("https://demodoc.digital.gob.cl/fed/inbox#/oficinapartes/entrada/sin_asignar")
            try:
                print("Asignando el documento: " + ae.text + "\n")
                time.sleep(2)
                assign_doc = driver.find_element_by_xpath("//*[@id='content']/div/div[2]/div/div/div[4]/div/table/tbody/tr[" + str(counter) + "]/td[1]/div/input")
                time.sleep(2)
                assign_doc.click()
                time.sleep(1)
                driver.execute_script('$("#content > div > div:nth-child(2) > div > div > div:nth-child(2) > div.col-xs-12.col-sm-4 > button").click()')
                time.sleep(1)
                driver.execute_script('$("body > div.modal.fade.ng-isolate-scope.in > div > div > form > div.modal-footer > button.btn.btn-primary.ng-binding").click()')
                time.sleep(3)
                driver.get("https://demodoc.digital.gob.cl/fed/inbox#/detalle/oficina/" + doc_id + "?page=15")
                time.sleep(6)
                driver.execute_script('$("#content > div > div.table-content.container-fluid > div:nth-child(2) > div.col-xs-12.col-sm-7 > div:nth-child(1) > div > span > button.btn.btn-primary.ng-scope").click()')
                time.sleep(1)
                driver.execute_script('$("body > div.modal.fade.ng-isolate-scope.in > div > div > form > div.modal-footer > button.btn.btn-primary.ng-binding").click()')
                time.sleep(6)
                print("Documento asignado con exito\n")
            except NoSuchElementException, e:
                print "No fue asignar el documento."
                print e
            counter += 1
            driver.get("https://demodoc.digital.gob.cl/fed/inbox#/oficinapartes/entrada/sin_asignar")
            time.sleep(1)
        else:
            print("El documento N°" + str(counter) + " correspondiente a: " + check_docname.text + " ya se encuentra asignado, pasando al siguiente documento.")
            counter += 1
    print "\n\nNo hay mas documentos. Proceso de extraccion de datos finalizado con exito."
except NoSuchElementException, e:
    print "No existen documentos para procesar en la tabla. Intentelo mas tarde"
    print e
driver.quit()
