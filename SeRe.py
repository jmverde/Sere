#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tkinter as tk
import os, os.path

import codecs  #evitar problemas escribiendo el log

import re

# Globals

NOMBRE_LOG = "./SeRe.log"

SEP_TEMP = "S"
SEP_CAPI = "E"


modelos = set([])

#REGEX_MODEL = "(.*)[S|T](\d\d)E(\d\d)(.*)\.(\w\w\w)"

modelos.add("(.*)[S|T](\d\d)E(\d\d)(.*)\.(\w\w\w)")

#para las que tienen el formato con una x delante

#REGEX_MODEL = "(.*)([\d|\d\d])x(\d\d)(.*)\.(\w\w\w)"

modelos.add("(.*)([\d|\d\d])x(\d\d)(.*)\.(\w\w\w)")


expres=set([])

for mod in modelos:

    expres.add(re.compile(mod))



# Inicializamos variables necesarias

nserie=""   #esto es temporal, habra que poner entrada para elegir


# flags:

flag_log = False
flag_serie = False

capis = set([])



# nuestra bonita clase capitulos

# file tiene que ser un string con una estructura de archivo de serie, con una
#temporada y un capitulo

#Siempre hay que verificar el campo true que es el que nos dice si tiene una
# estructura valida de archivo
class Capitulo:

    def __init__(self,file,expres):

        self.filename = file

        for expre in expres:
        
        
            blocks = expre.match(file)

# chequea si cumple el regex y si no lo marca como no valido 

            if blocks == None:
                self.valid = False

            else:
                self.valid = True

                self.show = blocks.groups()[0]

                temp = blocks.groups()[1]
                if len(temp) == 1:
                     temp="0"+temp                       
                self.temp = temp
            
                self.capi = blocks.groups()[2]            
                self.vers = blocks.groups()[3]
                self.ext  = blocks.groups()[4]
                break

        




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


#    Cojo el nombre base, y si esta en blanco paso de seguir

    nserie = cuadro_nom.get()

    if nserie =="":
        return()

    openlog()

    base = os.listdir()

    for arch in base:

#   Ignoramos los archivos ocultos, por que hay un huevo por tanto mac
#   Tambien ignoro las cosas que no tienen un punto (y que no van a ser archivos interesantes, y ademas nos clava la cosa)
        if (not(arch[0] == ".") and ("." in arch)):
            capis.add(Capitulo(arch,expres))
        



    for capi in list(capis):
        if capi.valid:

            newname = nserie + SEP_TEMP + capi.temp + SEP_CAPI + capi.capi + "." + capi.ext           

# compruebo que no este ya en el formato
            if newname == capi.filename:
                log.write("old  "+capi.filename+ " ya estaba en el formato"+"\n")
                salida_text("old  "+capi.filename+ " ya estaba en el formato"+"\n")



# compruebo que el archivo destino no existe (para no pisarlo)
            elif os.path.isfile(newname):
                log.write("rep  "+ capi.filename+" el archivo objetivo ya existia"+"\n")
                salida_text("rep  "+ capi.filename+" el archivo objetivo ya existia"+"\n")
            else:
                os.rename(capi.filename,newname)
                log.write("mv   " +capi.filename + " -> " + newname +"\n")
                salida_text("mv   " +capi.filename + " -> " + newname +"\n") 
        
# si no es valido lo logamos tambien
        else:
            log.write("not  " + capi.filename + " no me parece un capitulo"+"\n")
            salida_text("not  " + capi.filename + " no me parece un capitulo"+"\n")
# una vez hemos acabado con el lo sacamos del set por si queremos hacer varios directorios seguidos

        capis.discard(capi)

    closelog()

        

# esta se usa a veces de placeholder    
def test():
    print("test")
    

def openlog():

    global log
    global flag_log

    
    if flag_log:
        closelog()

### Esto funcionaba bien, pero es mas comodo usarlo con un flag
### compruebo si ya esta abierto, y si lo esta lo cierro
##    try:
##      log
##    except NameError: 
##      pass
##    else:        
##      log.close()


#   Abro el que haria falta para este directorio
    
#    log = open(NOMBRE_LOG,"a")
# a ver si evitamos problema con los nombres de archivo

    log=codecs.open(NOMBRE_LOG, "a", "utf-8-sig")

    flag_log=True
# TODO:  aqui hay que gestionar el si es viejo, para encender el undo


def closelog():
    
    global log
    global flag_log

    if flag_log:
        log.close()

    flag_log = False    

### esto era chulo pero creo que no hace falta ta
### compruebo si ya esta abierto, y si lo esta lo cierro
##    try:
##      log
##    except NameError: 
##      pass
##    else:        
##      log.close()


# ESTO SOBRA YA
##def aceptar():
##
##    global nserie, label_nombre,flag_serie
##
##    nserie = cuadro_nom.get()
##    label_nombre.config(text=("Nombre base: "+nserie))
##    flag_serie = True


def salida_text(mensaje):
    global mensajes
    mensajes.insert(tk.END,mensaje)


def update_labeldir():

    label_dir.config(text=(os.getcwd()))




def salir():
    #compruebo si hay log abierto y si lo hay lo cierro 
    global log
    global root

    if flag_log:
        log.close()
    
    root.destroy()



# Y aqui empezamos el meollo del asunto
root = tk.Tk()
root.title("SeRe")



#creamos los botones
#en algun momento hay que dejarlo con grid

eledir = tk.Button(root, text='Elegir directorio', 
                   command=combine_funcs(getdir,update_labeldir))
#eledir.pack()

label_dirt= tk.Label(root,text="Directorio Actual:")
label_dir = tk.Label(root,text=os.getcwd())

#label_dir.pack()
#width = 50

procdir = tk.Button(root, text='Procesar directorio', 
                   command=combine_funcs(test,procdir))

#procdir.pack()

cuadro_nom = tk.Entry(root)

#cuadro_nom.pack()

##acept=tk.Button(root, text='Aceptar',
##                   command=aceptar)

#acept.pack()

label_nombre =tk.Label(root,text="Nombre base:")
#label_nombre.pack() 

bquit = tk.Button(root, text = 'Quit', command = salir)
#bquit.pack()

mensajes = tk.Text(root, height=3, width=90)
# El disabled hace que no se pueda escribir en el desde el teclado,state="disabled"




eledir.grid(row=0,column=2)
label_dir.grid(row=0,column=1)
label_dirt.grid(row=0,column=0)

label_nombre.grid(row=2,column=0)
cuadro_nom.grid(row=2,column=1)
##acept.grid(row=2,column=1)

#label_nombre.grid(row=1,columnspan=2)

procdir.grid(row=2,column=2)

mensajes.grid(row=3,columnspan=3)


bquit.grid(row=4,columnspan=3)


root.mainloop()
