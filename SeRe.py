import tkinter as tk
import os, os.path

import re

# Globals

NOMBRE_LOG = "./SeRe.log"

SEP_TEMP = "S"
SEP_CAPI = "E"


REGEX_MODEL = "(.*)[S|T](\d\d)E(\d\d)(.*)\.(\w\w\w)"

# Inicializamos variables necesarias

nserie="Simpsons"   #esto es temporal, habra que poner entrada para elegir


# flags:

flag_log = False
flag_serie = True

capis = set([])



# nuestra bonita clase capitulos

# file tiene que ser un string con una estructura de archivo de serie, con una
#temporada y un capitulo

#Siempre hay que verificar el campo true que es el que nos dice si tiene una
# estructura valida de archivo
class Capitulo:

    def __init__(self,file):

        self.filename = file


        expre = re.compile(REGEX_MODEL)
        
        blocks = expre.match(file)

        if blocks == None:
            self.valid = False
            print("hay un archivo que no vale",file)

        else:
            self.valid = True

            self.show = blocks.groups()[0]
            self.temp = blocks.groups()[1]
            self.capi = blocks.groups()[2]
            self.vers = blocks.groups()[3]
            self.ext  = blocks.groups()[4]

        




        # Vamos con las extensiones


###       Este bloque mola un huevo, pero habra que reescribirlo con expresiones regulares 
##
##        bloque = list(file)
##
##        ext =[]
##
##        a = bloque.pop()
##
##        while not (a == "."):
##            ext.append(a)
##            a = bloque.pop()
##
##        ext.reverse()
##
##
##        #esto mola un huevo para unir, pero pos
##        self.ext = "".join(str(x) for x in ext)
##                








# helper function to get two functions en un boton

def combine_funcs(*funcs):
    def combined_func(*args, **kwargs):
        for f in funcs:
            f(*args, **kwargs)
    return combined_func



# funcion auxiliar que saca un menu para pedir el directorio y lo cambia
def getdir():
    direc=tk.filedialog.askdirectory()
    os.chdir(direc)
    


# mete en el set capis un Capitulo por cada archivo
def procdir():

    global log

    if not flag_log : return()

    base = os.listdir()

    for arch in base:

#   Ignoramos los archivos ocultos, por que hay un huevo por tanto mac
#   Tambien ignoro las cosas que no tienen un punto (y que no van a ser archivos interesantes, y ademas nos clava la cosa)
        if (not(arch[0] == ".") and ("." in arch)):
            capis.add(Capitulo(arch))
        



    for capi in list(capis):
        if capi.valid:

            newname = nserie + SEP_TEMP + capi.temp + SEP_CAPI + capi.capi + "." + capi.ext           

# compruebo que no este ya en el formato
            if newname == capi.filename:
                log.write("old  "+capi.filename+ "ya estaba en el formato"+"\n")


# compruebo que el archivo destino no existe (para no pisarlo)
            elif os.path.isfile(newname):
                log.write("rep  "+ capi.filename+" el archivo objetivo ya existia"+"\n")
            
            else:
                os.rename(capi.filename,newname)
                log.write("mv   " +capi.filename + " -> " + newname +"\n")
        
# si no es valido lo logamos tambien
        else:
            log.write("not  " + capi.filename + "no me parece un capitulo"+"\n")
# una vez hemos acabado con el lo sacamos del set por si queremos hacer varios directorios seguidos

        capis.discard(capi)

        

# esta se usa a veces de placeholder    
def test():
    print("test")
    

def openlog():

    global log
    global flag_log

# compruebo si ya esta abierto, y si lo esta lo cierro
    try:
      log
    except NameError: 
      pass
    else:        
      log.close()


#   Abro el que haria falta para este directorio
    
#    os.path.isfile("/etc/passwd")
    log = open(NOMBRE_LOG,"w")
    flag_log=True
# TODO:  aqui hay que gestionar el si es viejo, para encender el undo




def salir():
    #compruebo si hay log abierto y si lo hay lo cierro 
    global log
    global root
    try:
      log
    except NameError: 
      pass
    else:        
      log.close()

    root.destroy()



# Y aqui empezamos el meollo del asunto
root = tk.Tk()
root.title("SeRe")



#creamos los botones


eledir = tk.Button(root, text='Elegir directorio', width=50,
                   command=combine_funcs(getdir,openlog))
eledir.pack()

procdir = tk.Button(root, text='Procesar directorio', width=50,
                   command=combine_funcs(test,procdir))

procdir.pack()

bquit = tk.Button(root, text = 'Quit', width = 50, command = salir)
bquit.pack()

root.mainloop()
