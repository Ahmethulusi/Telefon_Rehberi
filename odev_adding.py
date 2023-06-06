import sqlite3
from tkinter import *



adding_root =Tk()
adding_root.title("Adding")
adding_root.geometry("300x200+500+100")
     
isim_ve_soyisimvalues = StringVar()
telvalues = StringVar()
                 
   

isim_ve_soyisim_lbl =Label(adding_root, text="fullname", font=("Helvetica", 10), bg='#708090', fg='white')
isim_ve_soyisim_lbl.place(x=10, y=10)
isim_ve_soyisim_Entry =Entry(adding_root, textvariable=isim_ve_soyisimvalues,bd=2,font="arial 12")
isim_ve_soyisim_Entry.place(x=80, y=10)

isim_ve_soyisim_lbl =Label(adding_root, text="tel.", font=("Helvetica", 10), bg='#708090', fg='white')
isim_ve_soyisim_lbl.place(x=10, y=50)
tel_Entry =Entry(adding_root, textvariable=telvalues,bd=2,font="arial 12")
tel_Entry.place(x=80, y=50)
    
def adding():

    name_and_surname = isim_ve_soyisimvalues.get()
    tel_number = telvalues.get()
    print("Eklenecek veriler: ",name_and_surname,tel_number)
    if (name_and_surname and tel_number) !="":
        conn = sqlite3.connect("rehber.db")
        cursor = conn.cursor()
        comment =  """INSERT INTO KULLANICI_1  VALUES (?,?) """
        cursor.execute(comment,(name_and_surname,tel_number))        
        conn.commit()
    adding_root.destroy()
    

button_ekle = Button(adding_root, text="Add", font=("Helvetica", 12), bg='#708090', fg='white',height=1,command=adding)
button_ekle.place(x=120, y=100)

adding_root.mainloop()