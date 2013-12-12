import tkinter as tk
import os


# Globals


class Capitulo:
    pass



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
    print("s")
    
def test():
    print("test")
    



#acordarse de dropear los archivos ocultos (esos que empiezan por .

# Y aqui empezamos el meollo del asunto
root = tk.Tk()
root.title("SeRe")


#creamos los botones

eledir = tk.Button(root, text='Elegir directorio', width=50,
                   command=combine_funcs(getdir,test))
eledir.pack()

bquit = tk.Button(root, text = 'Quit', width = 50, command = root.destroy)
bquit.pack()

root.mainloop()
