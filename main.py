from tkinter import * 
from tkinter import simpledialog
from tkinter import ttk, messagebox
import sqlite3
import webbrowser


class Window(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master

        F1 = Frame(self.master)
        F1.pack(pady=15, padx=25)

        self.F_listele = Frame(self.master)
        self.F_ekle = Frame(self.master)

    
        B3 = Button(F1, text="Üye Ol", command=self.uye_ol, font="Verdana 10 bold", cursor="hand2", fg="black", width=13, height=3)
        B3.grid(row=0, column=2)
        B4 = Button(F1, text="Giriş Yap", command=self.giris_yap, font="Verdana 10 bold", cursor="hand2", fg="black", width=13, height=3)
        B4.grid(row=0, column=3)
        self.baglanti = sqlite3.connect("baglan.sql", check_same_thread=True)
        self.im = self.baglanti.cursor()

    def ekle(self):
        if self.F_listele:
            self.F_listele.destroy()
        if self.F_ekle:
            self.F_ekle.destroy()
        self.F_ekle = Frame(self.master)
        self.F_ekle.place(x=250,y=150)
        Label(self.F_ekle,text="Makale_Baslıgı: ").grid(row=0,column=0,pady=5,sticky=W)
        self.E1 = Entry(self.F_ekle, width=35)
        self.E1.grid(row=0,column=1,pady=5)

        Label(self.F_ekle,text="Yazar: ").grid(row=1,column=0,pady=5,sticky=W)
        self.E2 = Entry(self.F_ekle, width=35)
        self.E2.grid(row=1,column=1,pady=5)

        Label(self.F_ekle,text="Eposta: ").grid(row=2,column=0,pady=5,sticky=W)
        self.E3 = Entry(self.F_ekle, width=35)
        self.E3.grid(row=2,column=1,pady=5)

        Label(self.F_ekle,text="Kurum: ").grid(row=3,column=0,pady=5,sticky=W)
        self.E4 = Entry(self.F_ekle, width=35)
        self.E4.grid(row=3,column=1,pady=5)

        Label(self.F_ekle,text="Tarih: ").grid(row=4,column=0,pady=5,sticky=W)
        self.BasimYil = Spinbox(self.F_ekle, from_=0, to = 2021, width=35)
        self.BasimYil.grid(row=4,column=1,pady=5)

        B3 = Button(self.F_ekle, text="Kayıt ET",command=self.kayit_et,fg="red", cursor="hand2", width=15)
        B3.grid(row=5,column=1,pady=8,sticky=NE)

    def uye_ol(self):
        if self.F_listele:
            self.F_listele.destroy()
        if self.F_ekle:
            self.F_ekle.destroy()

        self.F_ekle = Frame(self.master)
        self.F_ekle.place(x=250, y=150)

        Label(self.F_ekle, text="Kullanıcı Adı: ").grid(row=0, column=0, pady=5, sticky=W)
        self.kullanici_adi_entry = Entry(self.F_ekle, width=35)
        self.kullanici_adi_entry.grid(row=0, column=1, pady=5)

        Label(self.F_ekle, text="Şifre: ").grid(row=1, column=0, pady=5, sticky=W)
        self.sifre_entry = Entry(self.F_ekle, width=35, show="*")
        self.sifre_entry.grid(row=1, column=1, pady=5)

        Label(self.F_ekle, text="Rol: ").grid(row=2, column=0, pady=5, sticky=W)
        self.rol_entry = ttk.Combobox(self.F_ekle, values=["Yazar", "Editör", "Hakem"])
        self.rol_entry.grid(row=2, column=1, pady=5)

        B3 = Button(self.F_ekle, text="Kabul ET", command=self.kullanici_kayit_et, fg="red", cursor="hand2", width=15)
        B3.grid(row=3, column=1, pady=8, sticky=NE)

    def kullanici_kayit_et(self):
        kullanici_adi = self.kullanici_adi_entry.get()
        sifre = self.sifre_entry.get()
        rol = self.rol_entry.get()

        if kullanici_adi and sifre and rol:
            try:
                # Eğer tablo henüz oluşturulmadıysa, oluştur
                self.im.execute("CREATE TABLE IF NOT EXISTS kullanicilar (id INTEGER PRIMARY KEY, KullaniciAdi VARCHAR(45), Sifre VARCHAR(45), Rol VARCHAR(10))")
                self.im.execute("INSERT INTO kullanicilar (KullaniciAdi, Sifre, Rol) VALUES (?, ?, ?)", (kullanici_adi, sifre, rol))
                self.baglanti.commit()
                messagebox.showinfo("Başarılı", "Üye kaydı başarıyla tamamlandı.")
                self.F_ekle.destroy()
            except Exception as e:
                messagebox.showwarning("Hata", f"Hata oluştu: {str(e)}")
        else:
            messagebox.showwarning("Hata", "Lütfen tüm alanları doldurun.")


    def giris_yap(self):
        if self.F_ekle:
            self.F_ekle.destroy()
        if self.F_listele:
            self.F_listele.destroy()

        kullanici_adi = simpledialog.askstring("Giriş Yap", "Kullanıcı Adı:")
        sifre = simpledialog.askstring("Giriş Yap", "Şifre:")

        if kullanici_adi and sifre:
            query = "SELECT * FROM kullanicilar WHERE KullaniciAdi=? AND Sifre=?"
            self.im.execute(query, (kullanici_adi, sifre))
            kullanici = self.im.fetchone()

            if kullanici:
                messagebox.showinfo("Giriş Başarılı", f"{kullanici[1]} olarak giriş yaptınız.")
                self.devam_et(kullanici[3])  # Kullanıcının rolüne göre devam et
            else:
                messagebox.showwarning("Hata", "Kullanıcı adı veya şifre hatalı.")
        else:
            messagebox.showwarning("Hata", "Lütfen tüm alanları doldurun.")
            
    def devam_et(self, rol):
        if rol == "Yazar":
            self.ekle()
        elif rol == "Editör":
            self.listele()
        elif rol == "Hakem":
            self.listele()
           
            
    def kayit_et(self):
        try:
            self.im.execute("CREATE TABLE IF NOT EXISTS makale (id INTEGER PRIMARY KEY, Makale_Baslıgı VARCHAR(45), Yazar VARCHAR(45), Eposta VARCHAR(45), Kurum INT, Tarih)") # Tablo oluşturma
            self.im.execute("INSERT INTO makale VALUES (null,'"+self.E1.get()+"','"+self.E2.get()+"','"+self.E3.get()+"','"+self.E4.get()+"','"+self.BasimYil.get()+"')")  # Veri ekleme
            self.baglanti.commit()
            say = Label(self.F_ekle, text="Kayıt Başarılı.", font="bold", fg="green")
            say.grid(row=6,column=1,pady=8,sticky=W)
            say.after(2000, say.destroy)
        except:
            messagebox.showerror("Hata","Galiba Kayıt Edilemedi.")

    def listele(self):
        try:
            if self.F_ekle:
                self.F_ekle.destroy()
            if self.F_listele:
                self.F_listele.destroy()
            self.F_listele = Frame(self.master)
            self.F_listele.place(x=0,y=120)
            self.im.execute("SELECT * FROM makale")
            data = self.im.fetchall()
            def search():
                deget = self.ara.get()
                query = "SELECT id, Makale_Baslıgı, Yazar, Eposta, Kurum, Tarih FROM makale WHERE Makale_Baslıgı LIKE '%"+deget+"%' OR Yazar LIKE '%"+deget+"%' OR Eposta LIKE '%"+deget+"%'"
                self.im.execute(query)
                rows = self.im.fetchall()
                update(rows)
                bulunanVeri = len(rows)
                toplamverilbl["text"] = ""
                AraLBL["text"] = "Bulunan Veri: "+str(bulunanVeri)
                AraLBL.grid(row=3,column=0,sticky=W)

            self.ara = Entry(self.F_listele,width=35)
            self.ara.grid(row=0,column=0,sticky=W,pady=20,padx=10)
            self.araBTN = Button(self.F_listele, text="Ara",fg="blue",command=search,width=5)
            self.araBTN.grid(row=0,column=0,sticky=W,pady=20,padx=230)

            self.tv = ttk.Treeview(self.F_listele, columns=(1,2,3,4,5,6), show='headings', height=10)
            self.tv.grid()
            self.tv.bind("<Button-3>", self.popup)
            self.tv.heading(1, text='ID')
            self.tv.heading(2, text='Makale_Baslıgı')
            self.tv.heading(3, text='Yazar')
            self.tv.heading(4, text='Eposta')
            self.tv.heading(5, text='Kurum')
            self.tv.heading(6, text='Tarih')

            self.tv.column("1",minwidth=10,width=27)
            self.tv.column("2",minwidth=50,width=250)
            self.tv.column("3",minwidth=50,width=198)
            self.tv.column("4",minwidth=50,width=100)
            self.tv.column("5",minwidth=10,width=60)
            self.tv.column("6",minwidth=10,width=40)
           

            sb = Scrollbar(self.F_listele, orient=VERTICAL,command=self.tv.yview)
            sb.grid(row=1,column=1,sticky=NS)
            sb2 = Scrollbar(self.F_listele, orient=HORIZONTAL, command=self.tv.xview)
            sb2.grid(row=2,column=0,sticky=EW)
            
            toplamVeri = f"{len(data)} Veri Bulundu."
            toplamverilbl = Label(self.F_listele,text=toplamVeri)
            toplamverilbl.grid(row=3,column=0,sticky=W) #.place(x=0, y=380)
            Button(self.F_listele, text="Tabloyu Yenile",fg="red", command=self.Yenile).grid(row=3,column=0,sticky=S)
            AraLBL = Label(self.F_listele)

            self.tv.config(yscrollcommand=sb2.set)
            self.tv.configure(yscrollcommand=sb.set, xscrollcommand=sb2.set)
            s = 1
            for i in data:
                self.tv.insert(parent='', index=s, iid=s, values=(i[0],i[1],i[2],i[3],i[4],i[5]))
                s += 1

            def update(rows):
                self.tv.delete(*self.tv.get_children())
                for i in rows:
                    self.tv.insert("","end",values=i)
        except:
            messagebox.showwarning("Hata", "Veri Tabanı Bulunamadı")
    def Yenile(self):
        self.F_listele.destroy()
        self.listele()

    def popup(self, event):
        iid = self.tv.identify_row(event.y)
        if iid:
            m = Menu(root, tearoff=0)
            m.add_command(label="Düzenle", command=self.Duzenle)
            m.add_command(label="Degerlendirmede", command=self.Degerlendir)

            self.tv.selection_set(iid)
            self.at = self.tv.selection_set(iid)
            m.post(event.x_root, event.y_root)
        else:
            pass

    def Duzenle(self):
        focus = self.tv.focus()
        numara = self.tv.item(focus)["values"][0]
        yeniWin = Toplevel()
        yeniWin.wm_title("Düzenle")
        windowWidth = yeniWin.winfo_reqwidth()
        windowHeight = yeniWin.winfo_reqheight()
        positionRight = int(yeniWin.winfo_screenwidth()/2 - windowWidth/1)
        positionDown = int(yeniWin.winfo_screenheight()/3 - windowHeight/3)
        yeniWin.geometry(f"300x320+{positionRight}+{positionDown}")
        yeniWin.resizable(width=False, height=False)

        def veriKayit():
            # Veri Tabanını oluştur
            self.im.execute("CREATE TABLE IF NOT EXISTS makale (Makale Baslıgı VARCHAR(45), Yazar VARCHAR(45), Eposta VARCHAR(45), Kurum VARCHAR(45), Tarih )") # Tablo oluşturma

            self.im.execute("UPDATE makale SET Makale_Baslıgı = ?, Yazar = ?, Eposta = ?, Kurum = ?, Tarih = ? WHERE id = ?", (self.E1.get(),self.E2.get(),self.E3.get(),self.E4.get(),self.BasimYil.get(),numara))
            self.baglanti.commit()
            say = Label(yeniWin,text="Kabul Edildi.", font="bold", fg="green")
            say.pack(side=BOTTOM)
            say.after(2000, say.destroy)
        def veriDuzenle():
            self.E1.config(state="normal")
            self.E2.config(state="normal")
            self.E3.config(state="normal")
            self.E4.config(state="normal")
            self.BasimYil.config(state="normal")
            B3.config(state="normal",cursor="hand2")
        def veriSil():
            evet = messagebox.askyesno("RED","Veri Tabanından reddetmek istiyormusunuz?")
            if evet:
                self.im.execute("DELETE FROM makale WHERE id = ?",[numara])
                self.baglanti.commit()
                yeniWin.destroy()
        F_ekle = Frame(yeniWin)
        F_ekle.pack()
        kopya = self.tv.focus()
        Label(F_ekle,text="Makale Adı: ").grid(row=0,column=0,pady=5,sticky=W)
        
        self.E1 = Entry(F_ekle, width=35)
        self.E1.insert(0, self.tv.item(kopya)["values"][1])
        # print(self.tv.item(kopya)["values"][3])
        self.E1.config(state="disable")
        self.E1.grid(row=0,column=1,pady=5)
        Label(F_ekle,text="Yazar: ").grid(row=1,column=0,pady=5,sticky=W)
        self.E2 = Entry(F_ekle, width=35)
        self.E2.insert(0, self.tv.item(kopya)["values"][2])
        self.E2.config(state="disable")
        self.E2.grid(row=1,column=1,pady=5)
        Label(F_ekle,text="Eposta: ").grid(row=2,column=0,pady=5,sticky=W)
        self.E3 = Entry(F_ekle, width=35)
        self.E3.insert(0, self.tv.item(kopya)["values"][3])
        self.E3.config(state="disable")
        self.E3.grid(row=2,column=1,pady=5)
        Label(F_ekle,text="Kurum: ").grid(row=3,column=0,pady=5,sticky=W)
        self.E4 = Entry(F_ekle, width=5)
        self.E4.insert(0, self.tv.item(kopya)["values"][4])
        self.E4.config(state="disable")
        self.E4.grid(row=3,column=1,pady=5,sticky=W)
        Label(F_ekle,text="Tarih: ").grid(row=5,column=0,pady=5,sticky=W)
        self.BasimYil = Spinbox(F_ekle, width=5)
        self.BasimYil.insert(0, self.tv.item(kopya)["values"][5])
        self.BasimYil.config(state="disable")
        self.BasimYil.grid(row=5,column=1,sticky=W)
        B3 = Button(F_ekle, text="Kabul ET",command=veriKayit,fg="green", width=15)
        B3.config(state="disable")
        B3.grid(row=5,column=1,pady=8,sticky=NE)
        
        B4 = Button(F_ekle,text="Düzenle",command=veriDuzenle,fg="blue", cursor="hand2", width=15)
        B4.grid(row=6,column=1,pady=8,sticky=NE)

        B5 = Button(F_ekle,text="Ret",command=veriSil,fg="red", cursor="hand2", width=15)
        B5.grid(row=8,column=1,pady=8,sticky=NE)
    
    def Degerlendir(self):
        kopya = self.tv.focus()
        self.master.clipboard_clear()
        self.master.clipboard_append(self.tv.item(kopya)["values"])
        say = Label(self.master,text="Degerlendirmede", font="bold", fg="red")
        say.pack(side=BOTTOM)
        say.after(2000, say.destroy)

    def exitProgram(self):
        exit()
root = Tk()
app = Window(root)
root.wm_title("Makale Kayıt Sistemi")

windowWidth = root.winfo_reqwidth()
windowHeight = root.winfo_reqheight()
positionRight = int(root.winfo_screenwidth()/3 - windowWidth/2)
positionDown = int(root.winfo_screenheight()/3 - windowHeight/2)
root.geometry(f"755x520+{positionRight}+{positionDown}")
root.resizable(width=False, height=False)

def callback(url):
    webbrowser.open_new(url)
me = Label(root, text="Developer: sude | selin", fg="black",cursor="hand2",font="Verdana 10 bold")
me.pack(side=BOTTOM)


root.mainloop()
