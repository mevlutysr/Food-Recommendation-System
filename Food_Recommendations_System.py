from tkinter import *
from tkinter import filedialog
from tkinter.ttk import Combobox
from os import getcwd
from xlrd import open_workbook
from recommendations import *
import dbm
import pickle


class Editor(Frame):

    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.root = parent
        self.initUI()
        self.dbReading()
        self.refreshlisListbox()

    def initUI(self):
        self.pack()

        # Colors
        self.fgColor = "#008b00"
        self.bgColor = "#ffcc99"

        self.foods = ['Dort Peynirli Bavetta', 'Soya Soslu Tavuk', 'Sosisli', 'Islak Hamburger', 'Karisik Et Tabagi',
                      'citir Tavuk Durum',
                      'Sebzeli Tavuklu Bavetta', 'Penne Arabbiata', 'Tavuk Burger', 'Patlicanli Kofteli Kebap',
                      'Sahanda Kavurmali Yumurta',
                      'Tavuklu Kebap', 'cift Kasarli Tost', 'Akdeniz Salata', 'Kasarli Gozleme Tabagi',
                      'Yumurtali Ekmek', 'sis Kofte Salata',
                      'Kofte Durum', 'Bahcivan Omlet', 'Menemen Beyaz Peynirli', 'Menemen', 'Kavurmali Omlet',
                      'Sahanda Sucuklu Yumurta', 'Pilic Nugget',
                      'Kasarli Omlet', 'Kaplamali Tavuk', 'Patates Tava', 'Acili Tavuk', 'Taze Baharatli Izgara Tavuk',
                      'Su Boregi', 'Beyaz Peynirli Omlet',
                      'Pesto Soslu Tavuk', 'Bonfile Salata', 'Sade Omlet', 'Izgara Kofte', 'Pilic Sote',
                      'Izgara Tavuk Sandwic', 'Cheese Burger', 'citir Tavuk Salata',
                      'Beyaz Peynirli Tost', 'Sahanda Yumurta', 'Barbeku Soslu Tavuk', 'Kori Soslu Tavuk',
                      'cokertme Kebabi', 'Sucuk Durum', 'Karisik Tost', 'Ege Tost (Ciabata Ekmegi)',
                      'citir Tavuk Sepeti', 'Patso', 'Hamburger', 'Sucuklu Bazlama Tost', 'Gorali',
                      'Penne Con Melenzane', 'Bonfileli Penne', 'Menemen Kasarli', 'Kucuk Kahvalti Tabagi',
                      'Manti', 'Kahvalti Tabagi', 'Kavurmali Tost', 'Karisik Gozleme Tabagi', 'Ton Balikli Salata',
                      'Patatesli Kol Boregi', 'Beyaz Peynirli Gozleme Tabagi', 'Karisik Omlet',
                      'Kaplamali Tavuk Sandwic', 'Kasarli Tost', 'Tavuklu Sezar']

        self.frame1 = Frame(width = 20, height = 20)
        self.frame1.place(x = 476, y = 150)
        self.frame2 = Frame(width = 20, height = 20)
        self.frame2.place(x = 120, y = 470)
        self.frame3 = Frame(width = 20, height = 20)
        self.frame3.place(x = 490, y = 470)

        # Scrollbar
        self.scrollbar1 = Scrollbar(self.frame1)
        self.scrollbar1.pack(side = RIGHT, fill = Y)
        self.scrollbar2 = Scrollbar(self.frame2)
        self.scrollbar2.pack(side = RIGHT, fill = Y)
        self.scrollbar3 = Scrollbar(self.frame3)
        self.scrollbar3.pack(side = RIGHT, fill = Y)

        # Label
        self.lab = Label(text = "İSTİNYE KAFETERYA ÖNERİ SİSTEMİ", font = "Times 17 bold", bg = self.bgColor,
                         fg = self.fgColor)
        self.lab.pack()
        self.lab1 = Label(text = "Müşteri önerilerini yükle ", font = "Times 14 bold", bg = self.bgColor,
                          fg = self.fgColor)
        self.lab1.place(x = 240, y = 50)
        self.lab2 = Label(text = "KENDİ DEĞERLENDİRMELERİM ", font = "Times 15 bold", bg = self.bgColor,
                          fg = self.fgColor)
        self.lab2.place(x = 235, y = 100)
        self.lab3 = Label(text = "Kendi değerim (0.0-10.0)", font = "Times 14 bold ", bg = self.bgColor,
                          fg = self.fgColor)
        self.lab3.place(x = 155, y = 150)
        self.lab4 = Label(text = "AYARLAR", font = "Times 16 bold", bg = self.bgColor, fg = self.fgColor)
        self.lab4.place(x = 350, y = 280)
        self.lab5 = Label(text = "Toplam öneri adedi", font = "Times 15 bold", bg = self.bgColor, fg = self.fgColor)
        self.lab5.place(x = 10, y = 330)
        self.lab6 = Label(text = "Öneri Modeli", font = "Times 15 bold", bg = self.bgColor, fg = self.fgColor)
        self.lab6.place(x = 250, y = 330)
        self.lab7 = Label(text = "Benzerlik ölçütü", font = "Times 15 bold", bg = self.bgColor, fg = self.fgColor)
        self.lab7.place(x = 530, y = 330)

        # Entry
        self.pointEntry = Entry(font = "Times 14 bold", textvariable = StringVar(value = "0"), fg = self.fgColor)
        self.pointEntry.place(x = 285, y = 153, relx = 0.1, width = 30)

        self.recommendationsEntry = Entry(font = "Times 14 bold", textvariable = StringVar(value = "5"),
                                          fg = self.fgColor)
        self.recommendationsEntry.place(x = 110, y = 332, relx = 0.1, width = 30)

        # Listbox
        self.userSelectionsListBox = Listbox(self.frame1, font = "Times 11 bold", fg = self.fgColor, height = 7,
                                             width = 28, yscrollcommand = self.scrollbar1.set)
        self.userSelectionsListBox.pack()
        self.scrollbar1.config(command = self.userSelectionsListBox.yview)

        self.similarListBox = Listbox(self.frame2, font = "Times 11 bold", fg = self.fgColor, height = 7, width = 28,
                                      yscrollcommand = self.scrollbar2.set)
        self.similarListBox.pack()
        self.scrollbar2.config(command = self.similarListBox.yview)

        self.recommendationsListBox = Listbox(self.frame3, font = "Times 11 bold", fg = self.fgColor, height = 7,
                                              width = 28, yscrollcommand = self.scrollbar3.set)
        self.recommendationsListBox.pack()
        self.scrollbar3.config(command = self.recommendationsListBox.yview)

        # Radio Buttons
        self.var1 = StringVar()
        self.var2 = StringVar()
        self.var1.set(0)
        self.var2.set(0)

        # Öneri Modeli seçim butonları
        self.radioButton1 = Radiobutton(text = "Kullanıcı bazlı", font = "Times 12 bold", bg = self.bgColor,
                                        fg = self.fgColor, variable = self.var1, value = 0,
                                        command = self.getmethodTypes)
        self.radioButton1.place(x = 370, y = 330)
        self.radioButton2 = Radiobutton(text = "Ürün bazlı", font = "Times 12 bold", bg = self.bgColor,
                                        fg = self.fgColor, variable = self.var1, value = 1,
                                        command = self.getmethodTypes)
        self.radioButton2.place(x = 370, y = 355)

        # Benzerlik ölçütü seçim butonları
        self.radioButton3 = Radiobutton(text = "Öklid", font = "Times 12 bold", bg = self.bgColor, fg = self.fgColor,
                                        variable = self.var2, value = 0, command = self.getmethodTypes)
        self.radioButton3.place(x = 675, y = 330)
        self.radioButton4 = Radiobutton(text = "Pearson", font = "Times 12 bold", bg = self.bgColor, fg = self.fgColor,
                                        variable = self.var2, value = 1, command = self.getmethodTypes)
        self.radioButton4.place(x = 675, y = 355)
        self.radioButton5 = Radiobutton(text = "Jaccard", font = "Times 12 bold", bg = self.bgColor, fg = self.fgColor,
                                        variable = self.var2, value = 2, command = self.getmethodTypes)
        self.radioButton5.place(x = 675, y = 380)
        self.methods = {"0": "0", "1": "0"}

        # Butons
        self.loadButton = Button(text = "Yükle", font = "Times 13 bold", fg = self.fgColor, bg = self.bgColor,
                                 command = self.load, width = 6).place(x = 380, y = 48,
                                                                       relx = 0.1)  # Excel dosyasını seçmemizi sağlayan buton.
        self.appendButton = Button(text = "Ekle", font = "Times 13 bold", fg = self.fgColor, bg = self.bgColor,
                                   command = self.append, width = 6).place(x = 402, y = 150)

        self.deleteButton = Button(text = "Seçileni\nKaldır", font = "Times 13 bold", fg = self.fgColor,
                                   bg = self.bgColor,
                                   command = self.delete, width = 6).place(x = 725, y = 150)
        self.recommendationButton = Button(text = "Öneri Al", font = "times 12 bold", fg = self.fgColor,
                                           bg = self.bgColor,
                                           command = self.recommendations, width = 10).place(x = 184, y = 431)
        self.findSimilarButton = Button(text = "Benzer müşterileri listele", font = "times 12 bold", fg = self.fgColor,
                                        bg = self.bgColor,
                                        command = self.findSimilar, width = 19).place(x = 515, y = 430)
        # ComboBox
        self.selectedFood = StringVar()
        self.chooseFood = Combobox(values = self.foods, textvariable = self.selectedFood).place(x = 5, y = 154)

    def load(self):
        """
        Excel dosyasının kullanıcı tarafından seçilmesini ve
        bu dosyadaki müşteri değerlendirmelerinin alınmasını sağlar.
        """
        try:
            self.ratingsList = open_workbook(filedialog.askopenfilename(initialdir = getcwd(), title = "Dosya Seç",
                                                                        filetypes = [
                                                                            ("Excel files", "*.xlsx")])).sheet_by_index(
                0)
        except:
            return

        self.ratings = dict()
        for row in range(1, self.ratingsList.nrows):
            self.ratings.setdefault(self.ratingsList.cell(row, 0).value, {})
            self.ratings[self.ratingsList.cell(row, 0).value][self.ratingsList.cell(row, 1).value] = float(
                self.ratingsList.cell(row, 2).value)

    def dbReading(self):
        """
        DataBase'ten verileri okur ve değişkene atar.
        """
        self.db = dbm.open("kendi_degerlendirmelerim", "c")
        self.userSelections = list()
        try:
            self.userSelections = pickle.loads(self.db["user"])
        except:
            return

    def dbWriting(self):
        """
        DataBase'e verileri yazar.
        """
        self.db["user"] = pickle.dumps(self.userSelections)

    def makeUserRatings(self):
        """
        Kullanıcı değerlendirmelerini sözlük formatına dönüştürür.
        """
        self.userRatings = dict()
        for i in self.userSelections:
            self.userRatings[i[0]] = float(i[1])

    def recommendations(self):
        """
        Kullanıcıya yemek önerisi yapar.
        """
        self.makeUserRatings()
        self.ratings.update({"user": self.userRatings})
        self.similarListBox.delete(0, END)
        if self.methods["1"] == "0":
            for i in getRecommendations(self.ratings, "user", similarity = sim_distance)[0:5]:
                self.similarListBox.insert(END, "{}->{}".format(i[1], str(i[0])[0:4]))
        elif self.methods["1"] == "1":
            for i in getRecommendations(self.ratings, "user", similarity = sim_pearson)[0:5]:
                self.similarListBox.insert(END, "{}->{}".format(i[1], str(i[0])[0:4]))
        elif self.methods["1"] == "2":
            for i in getRecommendations(self.ratings, "user", similarity = sim_jaccard)[0:5]:
                self.similarListBox.insert(END, "{}->{}".format(i[1], str(i[0])[0:4]))

    def findSimilar(self):
        """
        Kullanıcı ile benzer yemek zevkleri bulunan müşterileri gösterir.
        """
        self.makeUserRatings()
        self.ratings.update({"user": self.userRatings})
        self.recommendationsListBox.delete(0, END)
        if self.methods["0"] == "0":
            for i in topMatches(self.ratings, "user", n = int(self.recommendationsEntry.get()),
                                similarity = sim_distance):
                self.recommendationsListBox.insert(END, "{}->{}".format(i[1], str(i[0])[0:4]))
        elif self.methods["0"] == "1":
            for i in topMatches(self.ratings, "user", n = int(self.recommendationsEntry.get()),
                                similarity = sim_pearson):
                self.recommendationsListBox.insert(END, "{}->{}".format(i[1], str(i[0])[0:4]))
        elif self.methods["0"] == "2":
            for i in topMatches(self.ratings, "user", n = int(self.recommendationsEntry.get()),
                                similarity = sim_jaccard):
                self.recommendationsListBox.insert(END, "{}->{}".format(i[1], str(i[0])[0:4]))


    def append(self):
        """
        Kullanıcının belirlediği değerlendirmeyi değerlendirmeleri arasına ekler.
        """
        self.userSelections.append((self.selectedFood.get(), self.pointEntry.get()))
        self.refreshlisListbox()


    def refreshlisListbox(self):
        """
        Kullanıcı değerlendirmelerinin olduğu Listbox widget'ını günceller.
        """
        self.userSelectionsListBox.delete(0, END)
        for i in self.userSelections:
            self.userSelectionsListBox.insert(END, "{}->{}\n".format(i[0], i[1]))
        self.dbWriting()

    def delete(self):
        """
        Kullanıcı'nın seçtiği değerlendirmeyi kaldırır.
        """
        self.userSelections.pop(self.userSelectionsListBox.index(ANCHOR))
        self.refreshlisListbox()

    def getmethodTypes(self):
        """
        Öneri metodlarını günceller.
        """
        self.methods[self.var1.get()] = self.var2.get()


def main():
    root = Tk()
    root.title("İstinye kafeterya öneri programı")
    root.resizable(0, 0)
    root.geometry("800x650")
    app = Editor(root)
    root.configure(bg = app.bgColor)
    root.mainloop()


if __name__ == '__main__':
    main()
