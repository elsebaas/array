# encoding: utf-8
from __future__ import unicode_literals
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from datetime import datetime
import base64, string, os, shutil, time, sys, re
from os import path
from selenium.webdriver.common.keys import Keys

now = datetime.now()
log_path = "C:\\Python27\\array\\logs\\"
reload(sys)
sys.setdefaultencoding('utf-8')
sys.stdout = open(log_path + 'output - ' + now.strftime("%d%m%Y_%H%M") + '.txt', 'w')
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

# Proceso de ingreso de datos.
try:
    directory = 'C:\\Python27\\array\\docs_distribucion'
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            route_file = os.path.join(directory, filename)
            print(os.path.join(directory, filename))
            with open(route_file, 'r') as file:
                counter = 1
                # Ir a Oficina de Partes / Documentos entrantes
                try:
                    print("Ingresando a: Nuevo documento a distribuir\n")
                    time.sleep(2)
                    driver.get("https://demodoc.digital.gob.cl/")
                    driver.get("https://demodoc.digital.gob.cl/fed/inbox#/nueva/solicitud")
                    time.sleep(2)
                    driver.execute_script("$('#content > div > div.table-content > div:nth-child(2) > div > form > div:nth-child(11) > div > div > center > button').click()")
                except NoSuchElementException, e:
                    print "No fue posible acceder a la ruta: https://demodoc.digital.gob.cl/fed/inbox#/nueva/solicitud"
                    print e
                print("PDF: Asignando archivo")
                doc_pdf = filename.replace('.txt', '.pdf')
                driver.execute_script("$('#content > div > div.table-content > div:nth-child(2) > div > form > div:nth-child(5) > div:nth-child(1) > div > div:nth-child(1) > div > ul > li > div.file-actions.text-right > a.btn.btn-default.ng-scope > span').length&&$('#content > div > div.table-content > div:nth-child(2) > div > form > div:nth-child(5) > div:nth-child(1) > div > div:nth-child(1) > div > ul > li > div.file-actions.text-right > a.btn.btn-default.ng-scope').click();")
                time.sleep(2)
                driver.find_element_by_css_selector("input[name='file'][type='file']").send_keys("C:\\Python27\\array\\docs_distribucion\\" + doc_pdf)
                time.sleep(5)
                driver.execute_script("$( '#noSignatureInput' ).prop( 'checked', true )")
                for line in file:
                    id, value = line.split(':')
                    if counter == 1: #Tipo de documento
                        print("Paso 1: Tipo de documento")
                        driver.execute_script("$('#typeInput > div.ui-select-match > span').click()")
                        driver.find_element_by_xpath("""//*[@id="typeInput"]/input[1]""").send_keys(value, Keys.TAB)
                    if counter == 2: #Materia o tema del documento
                        print("Paso 2: Materia o tema del documento")
                        driver.find_element_by_xpath("""//*[@id="nameInput"]""").send_keys(value)
                    if counter == 3: #Descripción del documento
                        print("Paso 3: Descripción del documento")
                        driver.find_element_by_xpath("""//*[@id="descriptionInput"]""").send_keys(value)
                    if counter == 4: #Es un documento resuelto(SI/NO)
                        print("Paso 4: Es un documento resuelto(SI/NO)")
                        if value == "SI":
                            time.sleep(2)
                            driver.execute_script("$( '#noSignatureInput' ).prop( 'checked', true )")
                    if counter == 5: #Es un documento reservado(SI/NO)
                        print("Paso 5: Es un documento reservado(SI/NO)")
                        if value == "SI":
                            time.sleep(2)
                            driver.execute_script("$( '#reservedInput' ).prop( 'checked', true )")
                    if counter == 6: #Ministerio u organismo
                        print("Paso 6: Ministerio u organismo")
                        driver.execute_script("$('#content > div > div.table-content > div:nth-child(2) > div > form > div.row.no-margin.ng-scope > div > div:nth-child(2) > div:nth-child(1) > div > div > div.ui-select-container.ui-select-bootstrap.dropdown.ng-invalid.ng-invalid-required > div.ui-select-match > span').click()")
                        el = driver.find_element_by_xpath("""//*[@id="content"]/div/div[2]/div[2]/div/form/div[11]/div/div[2]/div[1]/div/div/div[2]/input[1]""")
                        text = value
                        for character in text:
                            el.send_keys(character)
                            time.sleep(0.5)
                    if counter == 7: #Institucion
                        print("Paso 7: Institucion, Jefe de servicio y enviar formulario")
                        driver.execute_script("$('#content > div > div.table-content > div:nth-child(2) > div > form > div.row.no-margin.ng-scope > div > div:nth-child(2) > div:nth-child(2) > div > div > div.ui-select-container.ui-select-bootstrap.dropdown.ng-invalid.ng-invalid-required > div.ui-select-match > span > span.ui-select-placeholder.text-muted.ng-binding').click()")
                        el = driver.find_element_by_xpath("""//*[@id="content"]/div/div[2]/div[2]/div/form/div[11]/div/div[2]/div[2]/div/div/div[2]/input[1]""")
                        text = value
                        for character in text:
                            el.send_keys(character)
                            time.sleep(0.2)
                        el.send_keys(Keys.RETURN)
                        time.sleep(1)
                        driver.execute_script("$('#findByPositionRadio').prop('checked', true).trigger('click')")
                        driver.execute_script("$('#content > div > div.table-content > div:nth-child(2) > div > form > div.row.no-margin.ng-scope > div > div:nth-child(3) > div.col-xs-12.col-lg-12 > div > div.input-group > div.ui-select-container.ui-select-multiple.ui-select-bootstrap.dropdown.form-control.ng-dirty.ng-invalid.ng-invalid-required > div > input').click()")
                        driver.find_element_by_xpath("""//*[@id="content"]/div/div[2]/div[2]/div/form/div[11]/div/div[3]/div[1]/div/div[2]/div[2]/div/input""").send_keys("jefe de")
                        time.sleep(3)
                        driver.find_element_by_xpath("""//*[@id="content"]/div/div[2]/div[2]/div/form/div[11]/div/div[3]/div[1]/div/div[2]/div[2]/div/input""").send_keys(Keys.RETURN)
                        time.sleep(1)
                    counter += 1
        else:
            continue
except NoSuchElementException, e:
    print "Existe un error, favor consulte con el administrador"
    print e

driver.quit()
