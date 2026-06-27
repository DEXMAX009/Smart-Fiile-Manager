import os
import shutil
import hashlib
import customtkinter as ctk
from tkinter import filedialog


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class FileManager(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("🚀 Smart File Manager PRO")
        self.geometry("1000x700")

        self.current_path = os.getcwd()


        title = ctk.CTkLabel(
            self,
            text="✨ Smart File Manager PRO",
            font=("Arial",30)
        )

        title.pack(pady=15)



        self.path_label = ctk.CTkLabel(
            self,
            text=self.current_path
        )

        self.path_label.pack()



        buttons = ctk.CTkFrame(self)
        buttons.pack(pady=15)



        ctk.CTkButton(
            buttons,
            text="📂 Папка",
            command=self.open_folder
        ).grid(row=0,column=0,padx=5)


        ctk.CTkButton(
            buttons,
            text="📦 Сортировать",
            command=self.organize
        ).grid(row=0,column=1,padx=5)


        ctk.CTkButton(
            buttons,
            text="🔎 Дубликаты",
            command=self.find_duplicates
        ).grid(row=0,column=2,padx=5)


        ctk.CTkButton(
            buttons,
            text="📊 Анализ",
            command=self.analyze
        ).grid(row=0,column=3,padx=5)



        self.output = ctk.CTkTextbox(
            self,
            width=900,
            height=400
        )

        self.output.pack()



    # выбор папки

    def open_folder(self):

        folder=filedialog.askdirectory()

        if folder:

            self.current_path=folder

            self.path_label.configure(
                text=folder
            )

            self.show()



    # показать файлы

    def show(self):

        self.output.delete(
            "0.0",
            "end"
        )


        for f in os.listdir(
            self.current_path
        ):

            self.output.insert(
                "end",
                "📄 "+f+"\n"
            )



    # НОВАЯ правильная сортировка


    def organize(self):

        folders={

            "Фото":[
                ".png",".jpg",".jpeg",".webp"
            ],

            "Видео":[
                ".mp4",".avi",".mkv"
            ],

            "Музыка":[
                ".mp3",".wav"
            ],

            "Документы":[
                ".txt",".pdf",".docx"
            ]

        }


        moved=0


        for file in os.listdir(
            self.current_path
        ):

            full=os.path.join(
                self.current_path,
                file
            )


            if not os.path.isfile(full):
                continue



            ext=os.path.splitext(
                file
            )[1].lower()



            for folder,extensions in folders.items():

                if ext in extensions:


                    target_folder=os.path.join(
                        self.current_path,
                        folder
                    )


                    # создаём только если нужен

                    os.makedirs(
                        target_folder,
                        exist_ok=True
                    )


                    shutil.move(
                        full,
                        os.path.join(
                            target_folder,
                            file
                        )
                    )


                    moved+=1
                    break



        self.output.insert(
            "end",
            f"\n✅ Перемещено файлов: {moved}\n"
        )


        self.show()



    # поиск дубликатов


    def find_duplicates(self):

        hashes={}

        duplicates=[]


        for root,dirs,files in os.walk(
            self.current_path
        ):


            for file in files:


                path=os.path.join(
                    root,
                    file
                )


                try:

                    h=hashlib.md5(
                        open(path,"rb").read()
                    ).hexdigest()


                    if h in hashes:

                        duplicates.append(
                            path
                        )

                    else:

                        hashes[h]=path


                except:

                    pass



        self.output.insert(
            "end",
            "\n🔁 Дубликаты:\n"
        )


        for d in duplicates:

            self.output.insert(
                "end",
                d+"\n"
            )



    # анализ папки


    def analyze(self):

        count=0
        size=0


        for root,dirs,files in os.walk(
            self.current_path
        ):


            for f in files:

                try:

                    path=os.path.join(
                        root,f
                    )

                    size+=os.path.getsize(path)

                    count+=1


                except:
                    pass



        mb=size/1024/1024


        self.output.insert(
            "end",
            f"""

📊 Анализ папки:

Файлов: {count}

Размер:
{mb:.2f} MB

"""
        )





app=FileManager()

app.mainloop()
