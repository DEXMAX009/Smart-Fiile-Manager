import os
import shutil
import zipfile
import customtkinter as ctk

from tkinter import filedialog
from PIL import Image, ImageTk



ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")



class FileManager(ctk.CTk):

    def __init__(self):

        super().__init__()


        self.title("Smart File Manager PRO")
        self.geometry("1100x750")


        self.path=os.getcwd()



        ctk.CTkLabel(
            self,
            text="🚀 Smart File Manager PRO",
            font=("Arial",30)
        ).pack(pady=15)



        buttons=ctk.CTkFrame(self)
        buttons.pack()



        ctk.CTkButton(
            buttons,
            text="📂 Папка",
            command=self.open_folder
        ).grid(row=0,column=0,padx=5)


        ctk.CTkButton(
            buttons,
            text="📊 Размер",
            command=self.sort_size
        ).grid(row=0,column=1,padx=5)


        ctk.CTkButton(
            buttons,
            text="📦 Создать ZIP",
            command=self.make_zip
        ).grid(row=0,column=2,padx=5)


        ctk.CTkButton(
            buttons,
            text="🖼 Превью",
            command=self.preview
        ).grid(row=0,column=3,padx=5)



        self.list=ctk.CTkTextbox(
            self,
            width=700,
            height=400
        )

        self.list.pack(side="left",padx=20,pady=20)



        self.image_label=ctk.CTkLabel(
            self,
            text="Нет изображения"
        )

        self.image_label.pack(
            side="right",
            padx=30
        )



    # выбор папки

    def open_folder(self):

        folder=filedialog.askdirectory()

        if folder:

            self.path=folder

            self.show()



    # обычный список

    def show(self):

        self.list.delete(
            "0.0",
            "end"
        )


        for f in os.listdir(self.path):

            self.list.insert(
                "end",
                f+" \n"
            )



    # СОРТИРОВКА ПО РАЗМЕРУ


    def sort_size(self):


        files=[]


        for f in os.listdir(self.path):


            full=os.path.join(
                self.path,
                f
            )


            if os.path.isfile(full):

                size=os.path.getsize(full)

                files.append(
                    (f,size)
                )



        files.sort(
            key=lambda x:x[1],
            reverse=True
        )


        self.list.delete(
            "0.0",
            "end"
        )



        for name,size in files:


            mb=size/1024/1024


            self.list.insert(
                "end",
                f"📄 {name}  |  {mb:.2f} MB\n"
            )





    # СОЗДАНИЕ ZIP


    def make_zip(self):


        zip_name="Archive.zip"



        with zipfile.ZipFile(
            zip_name,
            "w"
        ) as zipf:


            for file in os.listdir(self.path):


                full=os.path.join(
                    self.path,
                    file
                )


                if os.path.isfile(full):

                    zipf.write(
                        full,
                        file
                    )



        self.list.insert(
            "end",
            "\n📦 ZIP создан!\n"
        )




    # ПРЕВЬЮ КАРТИНОК


    def preview(self):


        files=os.listdir(self.path)



        for file in files:


            if file.lower().endswith(
                (".png",".jpg",".jpeg",".webp")
            ):


                img=Image.open(
                    os.path.join(
                        self.path,
                        file
                    )
                )


                img.thumbnail(
                    (300,300)
                )


                photo=ImageTk.PhotoImage(
                    img
                )


                self.image_label.configure(
                    image=photo,
                    text=file
                )


                self.image_label.image=photo


                break





app=FileManager()

app.mainloop()
