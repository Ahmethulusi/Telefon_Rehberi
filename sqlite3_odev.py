import sqlite3
import subprocess
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

root = Tk()
root.title("Rehber")
root.geometry("400x420+500+100")
root.config(bg='#708090')
#root.resizable(0,0)


#Create a table
conn = sqlite3.connect("rehber.db")
cursor = conn.cursor()
cursor.execute(""" CREATE TABLE IF NOT EXISTS KULLANICI_1 (isim_soyisim TEXT ,tel TEXT )""")

## burda kaldım en son aşağıdaki arama kodu hatalıydı 
def search():
    search_text = arama_entry.get(1.0, "end-1c").capitalize() ####  ____.get(1.0, "end-1c")  text widgetten doğru veriyi almak için önemli bir yapı
    sorgu = "SELECT * FROM KULLANICI_1 WHERE isim_soyisim LIKE ? OR tel LIKE ?"
    conn = sqlite3.connect("rehber.db")
    cursor = conn.cursor()
    # isim_soyisim  veya tel sütununda arama metnini içeren satırları seç
    cursor.execute(sorgu, ("%"+search_text+"%", "%"+search_text+"%",)) ## Çok önemli bir Yapı
    rows = cursor.fetchall()    
    # eşleşen satırları yazdır
    if rows:
        table.delete(*table.get_children())
        for row in rows:
            table.insert("", "end", values=row)
    else:
        messagebox.showinfo("Sonuç", "Sonuç bulunamadı")

# Tablo görüntüsünü oluştur
table_frame = Frame(root)
table_frame.pack(expand=True, fill="both")


table = ttk.Treeview(table_frame, columns=("isim_soyisim", "tel"), show="headings")
table.heading("isim_soyisim", text="İsim Soyisim",anchor="center")
table.heading("tel", text="Telefon",anchor="center")
table.pack(expand=True, fill="both")

def load_data():
    # Tabloyu sorgula ve verileri al
    conn = sqlite3.connect("rehber.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM KULLANICI_1")
    rows = cursor.fetchall()

    for row in rows:
        table.insert("", "end", values=row)
    conn.close()
# Verileri tabloya ekle
load_data()
# Veritabanı bağlantısını kapat


def Güncelle():
    # Tabloyu temizle
    table.delete(*table.get_children())

    # Verileri sorgula ve ekle
    conn = sqlite3.connect("rehber.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM KULLANICI_1")
    rows = cursor.fetchall()

    for row in rows:
        table.insert("", "end", values=row)

    conn.close()
def satır_sec(event):
    selected_row = table.focus()
    print(selected_row)

def düzenle():
    if table.focus():
        global edit_window
        selected_row = table.focus()
        values = table.item(selected_row, "values")

        edit_window = Toplevel(root)
        edit_window.title("Düzenle")
        edit_window.geometry("300x250+550+140")
        edit_window.config(bg='#708090')
        edit_window.resizable(0, 0)

        # İsim düzenlemesi
        isim_label = Label(edit_window, text="İsim:",width=10,bg='#708090')
        isim_label.place(x=100, y=30)
        isim_entry = Entry(edit_window, width=30)
        isim_entry.insert(0, values[0])
        isim_entry.place(x=60, y=50)

        # Telefon düzenlemesi
        tel_label = Label(edit_window, text="Telefon:",width=10,bg='#708090')
        tel_label.place(x=100, y=70)
        tel_entry = Entry(edit_window, width=30)
        tel_entry.insert(0, values[1])
        tel_entry.place(x=60, y=90)

        # Kaydet butonu ve işlevi
        def kaydet():
            yeni_isim = isim_entry.get()
            yeni_tel = tel_entry.get()
            # Burada veritabanında güncelleme işlemleri yapılabilir
            update_comment = "UPDATE KULLANICI_1 SET isim_soyisim=?, tel=? WHERE isim_soyisim=? AND tel=?"
            cursor.execute(update_comment,(yeni_isim, yeni_tel, values[0], values[1]))
            conn.commit()
            edit_window.destroy()
        kaydet_button = Button(edit_window, text="Kaydet",width=12, command=kaydet)
        kaydet_button.place(x=100, y=110)

        edit_window.mainloop()
    edit_window

def satır_sil():
    selected_row = table.focus()
    if selected_row:
        #seçili satırın kimlik değerini al
        name_surname_set = table.set(selected_row, "#1")
        tel_set = table.set(selected_row,"#2")
        # veritabanından silme işlemi
        cursor.execute("DELETE FROM KULLANICI_1 WHERE isim_soyisim=? AND tel = ?""", (name_surname_set, tel_set))
        conn.commit()
        # seçili satırı silme işlemi
        table.delete(selected_row)
# tabloya tıklama olayını bağlama
table.bind("<ButtonRelease-1>", satır_sec)

#Sağ tıklama menüsü oluşturma
stıkMenu =Menu(root,tearoff=0)
stıkMenu.add_command(label="Sil",command=satır_sil)
stıkMenu.add_command(label="Güncelle",command=Güncelle)
stıkMenu.add_command(label="Düzenle",command=düzenle)

def show_stık_menu(event):
    stıkMenu.post(event.x_root,event.y_root)

# Sağ tıklama olayını bağlama
table.bind("<Button-3>", show_stık_menu)
table.bind("<Button-4>", show_stık_menu)
table.bind("<Button-5>", show_stık_menu)



## Yukarıdaki kodda, table.delete(*table.get_children()) satırıyla önce tabloyu temizliyoruz.
## Ardından SELECT sorgusuyla tablodaki tüm verileri alıyoruz ve her bir veriyi table nesnesine ekliyoruz.
## Bu şekilde, her güncelleme yapıldığında ekrandaki tablo temizlenir ve güncellenmiş veriler eklenir.
## Böylece aynı verilerin tekrar eklenmesi engellenir.
def adding():
   
    subprocess.run(["python", "odev_adding.py"])  # Çalıştırılacak olan Python dosyasını burada belirtin


text_frame = Frame(root)
text_frame.config(bg='#708090')
text_frame.pack(fill=BOTH,expand=1)
# Create a label and entry widget and button
arama_lbl =Label(text_frame, text="Search:", font=("Helvetica", 12), bg='#708090', fg='black')
arama_lbl.place(x=10, y=10)
arama_entry=Text(text_frame ,font=("Helvetica", 15),bg="lightgray",fg="black",width=27,height=1.5)        
arama_entry.place(x=80, y=10)
ara_btn = Button(text_frame, text="Search", font=("Helvetica", 12), bg='#708090', fg='white',width=10,command=search).place(x=150, y=60)

#button_ekle = Button(root, text="Add", font=("Helvetica", 12), bg='#708090', fg='white',height=1,command=deneme_ekle).place(x=120, y=130)

# Create a menu bar
menubar =Menu(root)
root.config(menu=menubar)
dosya_menu = Menu(menubar, tearoff=0)
dosya_menu.add_command(label="+ New",command=adding)
dosya_menu.add_command(label="Delete",command=satır_sil)
dosya_menu.add_command(label="Update",command=Güncelle)
menubar.add_cascade(label="File", menu=dosya_menu)
dosya_menu.add_separator()        
        
        
root.mainloop()
