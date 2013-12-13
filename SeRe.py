import tkinter as tk
import os

import re

# Globals



# Inicializamos variables necesarias

capis = set([])



# nuestra bonita clase capitulos

# file tiene que ser un string con una estructura de archivo de serie, con una
#temporada y un capitulo

#Siempre hay que verificar el campo true que es el que nos dice si tiene una
# estructura valida de archivo
class Capitulo:

    def __init__(self,file):

        self.filename = file


        expre = re.compile("(.*)[S|T](\d\d)E(\d\d)(.*)\.(\w\w\w)")
        
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
    
    base = os.listdir()

    for arch in base:

#   Ignoramos los archivos ocultos, por que hay un huevo por tanto mac
#   Tambien ignoro las cosas que no tienen un punto (y que no van a ser archivos interesantes, y ademas nos clava la cosa)
        if (not(arch[0] == ".") and ("." in arch)):
            print(arch)
            capis.add(Capitulo(arch))
        

    prueba()

def prueba():
    for capi in capis:
        if capi.valid:
            print (capi.filename, capi.ext)



# esta se usa a veces de placeholder    
def test():
    print("test")
    



#acordarse de dropear los archivos ocultos (esos que empiezan por .

# Y aqui empezamos el meollo del asunto
root = tk.Tk()
root.title("SeRe")



#creamos los botones


eledir = tk.Button(root, text='Elegir directorio', width=50,
                   command=combine_funcs(getdir,procdir))
eledir.pack()

bquit = tk.Button(root, text = 'Quit', width = 50, command = root.destroy)
bquit.pack()

root.mainloop()
