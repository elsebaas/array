from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from datetime import datetime
import base64, string, os, shutil, time, sys
from os import path

now = datetime.now()
log_path = "C:\\Python27\\array\\logs\\"
reload(sys)
sys.setdefaultencoding('utf-8')
sys.stdout = open(log_path + 'output - ' + now.strftime("%d%m%Y_%H%M") + '.txt', 'w')
src = "C:\\Users\\\salva\\Downloads\\"
print "\n###############################################\nRobot by array consulting group 2021\nExtraccion de datos y asignacion de documentos entrantes en oficina de partes SSFFA\n###############################################\n"

# Inicio de Chrome Webdriver
options = Options()
options.add_argument('--headless')
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
    driver.get("https://demodoc.digital.gob.cl/fed/inbox#/oficinapartes/entrada/sin_asignar")
    time.sleep(2)
except NoSuchElementException, e:
    print "No fue posible acceder a la ruta: https://demodoc.digital.gob.cl/fed/inbox#/oficinapartes/entrada/sin_asignar"
    print e

# Proceso de extraccion de datos.
try:
    print("Buscando si existen documentos en la tabla.\n")
    table_path = driver.find_element(By.XPATH, '//*[@id="content"]/div/div[2]/div/div/div[4]/div/table/tbody')
    rows = table_path.find_elements(By.TAG_NAME, "tr")
    counter = 1
    print("Existen " + str(len(rows)) + " documentos para extraccion de datos y asignacion.\n")
    for row in rows:
        time.sleep(2)
        viewdoc = driver.find_element_by_xpath("//*[@id='content']/div/div[2]/div/div/div[4]/div/table/tbody/tr[" + str(counter) + "]/td[10]/a")
        viewdoc.click()
        time.sleep(2)
        driver.execute_script("$('#content > div > div.table-content.container-fluid > div:nth-child(2) > div.col-xs-12.col-sm-7 > div:nth-child(3) > div > accordion > div > div:nth-child(1) > div.panel-collapse.in.collapse > div > table > tbody > tr:nth-child(1) > td strong, #content > div > div.table-content.container-fluid > div:nth-child(2) > div.col-xs-12.col-sm-7 > div:nth-child(3) > div > accordion > div > div:nth-child(1) > div.panel-collapse.in.collapse > div > table > tbody > tr:nth-child(7) > td > strong, #content > div > div.table-content.container-fluid > div:nth-child(2) > div.col-xs-12.col-sm-7 > div:nth-child(3) > div > accordion > div > div:nth-child(1) > div.panel-collapse.in.collapse > div > table > tbody > tr:nth-child(6) > td > strong, #content > div > div.table-content.container-fluid > div:nth-child(2) > div.col-xs-12.col-sm-7 > div:nth-child(3) > div > accordion > div > div:nth-child(1) > div.panel-collapse.in.collapse > div > table > tbody > tr:nth-child(5) > td > strong, #content > div > div.table-content.container-fluid > div:nth-child(2) > div.col-xs-12.col-sm-7 > div:nth-child(3) > div > accordion > div > div:nth-child(1) > div.panel-collapse.in.collapse > div > table > tbody > tr:nth-child(9) > td > strong').remove('strong');")
        download = driver.find_element_by_xpath("""//*[@id="content"]/div/div[2]/div[2]/div[3]/div[1]/div/a""")
        nm = driver.find_element_by_xpath("""//*[@id="content"]/div/div[2]/div[2]/div[3]/div[2]/div/accordion/div/div[1]/div[2]/div/table/tbody/tr[1]/td""")
        io = driver.find_element_by_xpath("""//*[@id="content"]/div/div[2]/div[2]/div[3]/div[2]/div/accordion/div/div[1]/div[2]/div/table/tbody/tr[7]/td""")
        ae = driver.find_element_by_xpath("""//*[@id="content"]/div/div[2]/div[2]/div[3]/div[2]/div/accordion/div/div[1]/div[2]/div/table/tbody/tr[6]/td""")
        uo = driver.find_element_by_xpath("""//*[@id="content"]/div/div[2]/div[2]/div[3]/div[2]/div/accordion/div/div[1]/div[2]/div/table/tbody/tr[5]/td""")
        td = driver.find_element_by_xpath("""//*[@id="content"]/div/div[2]/div[2]/div[3]/div[2]/div/accordion/div/div[1]/div[2]/div/table/tbody/tr[9]/td""")
        print('Extrayendo datos del documento "' + str(nm.text) + '" para generar archivo .txt\n')
        dst = "C:\\Python27\\array\\doc_entrantes"
        route_file = dst + "\\" + str(nm.text) + " - " + now.strftime("%d%m%Y_%H%M") + ".txt"
        txtfile = open(route_file, 'w')
        txtfile.write("IO:" + io.text + "\r")
        txtfile.write("AS:" + ae.text + "\r")
        txtfile.write("UO:" + uo.text + "\r")
        txtfile.write("TD:" + td.text)
        txtfile.close()
        time.sleep(2)
        print("Descargando documento PDF\n")
        download.click()
        time.sleep(2)
        filename = str(nm.text) + ".pdf"
        files = [i for i in os.listdir(src) if i.startswith(filename) and path.isfile(path.join(src, i))]
        for f in files:
            shutil.move(path.join(src, f), dst)
        time.sleep(2)
        new_filename = nm.text + " - " + now.strftime("%d%m%Y_%H%M") + ".pdf"
        os.chdir('C:\\Python27\\array\\doc_entrantes')
        os.rename(filename, new_filename)
        print('Extraccion de datos para el documento "' + str(nm.text) + '" realizado con exito. Pasando al siguiente documento...\n-----------------------------------------\n')
        time.sleep(2)
        counter += 1
        driver.get("https://demodoc.digital.gob.cl/fed/inbox#/oficinapartes/entrada/sin_asignar")
    print "\n\nNo hay mas documentos. Proceso de extraccion de datos finalizado con exito."
except NoSuchElementException, e:
    print "No existen documentos para procesar en la tabla. Intentelo mas tarde"
    print e
driver.quit()