import os
import shutil
import customtkinter as ctk
from tkinter import filedialog
from datetime import datetime


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class FileManager(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Smart File Manager")
        self.geometry("1000x650")

        self.current_path = os.getcwd()
        self.history = []

        # Заголовок
        self.title_label = ctk.CTkLabel(
            self,
            text="Smart File Manager",
            font=("Arial", 30)
        )
        self.title_label.pack(pady=15)


        # Поиск
        self.search = ctk.CTkEntry(
            self,
            placeholder_text="🔍 Поиск файла..."
        )
        self.search.pack(fill="x", padx=30)

        self.search.bind("<KeyRelease>", lambda e:self.show_files())


        # Панель кнопок

        panel = ctk.CTkFrame(self)
        panel.pack(pady=15)


        ctk.CTkButton(
            panel,
            text="Открыть папку",
            command=self.open_folder
        ).grid(row=0,column=0,padx=10)


        ctk.CTkButton(
            panel,
            text="Найти мусор",
            command=self.clean
        ).grid(row=0,column=1,padx=10)


        ctk.CTkButton(
            panel,
            text="Сортировать",
            command=self.organize
        ).grid(row=0,column=2,padx=10)



        # Список файлов

        self.listbox = ctk.CTkTextbox(
            self,
            width=900,
            height=350,
            font=("Consolas",15)
        )

        self.listbox.pack(pady=20)


        self.info = ctk.CTkLabel(
            self,
            text=""
        )

        self.info.pack()


        self.show_files()



    # показать файлы

    def show_files(self):

        self.listbox.delete("0.0","end")

        text=self.search.get().lower()


        size=0

        for file in os.listdir(self.current_path):

            if text in file.lower():

                path=os.path.join(
                    self.current_path,
                    file
                )

                icon="" if os.path.isdir(path) else ""

                if os.path.isfile(path):
                    size+=os.path.getsize(path)

                self.listbox.insert(
                    "end",
                    f"{icon} {file}\n"
                )


        self.info.configure(
            text=f" {self.current_path} | Размер: {size//1024} KB"
        )



    # открыть папку

    def open_folder(self):

        folder=filedialog.askdirectory()

        if folder:

            self.history.append(
                self.current_path
            )

            self.current_path=folder

            self.show_files()



    # очистка временных файлов

    def clean(self):

        deleted=0

        for root,dirs,files in os.walk(
            self.current_path
        ):

            for f in files:

                if f.endswith(
                    (".tmp",".log",".bak")
                ):

                    try:

                        os.remove(
                            os.path.join(root,f)
                        )

                        deleted+=1

                    except:
                        pass


        self.listbox.insert(
            "end",
            f"\n Удалено файлов: {deleted}\n"
        )



    # сортировка файлов

    def organize(self):

        categories={

            "Фото":
            [".png",".jpg",".jpeg"],

            "Видео":
            [".mp4",".avi"],

            "Документы":
            [".pdf",".docx",".txt"],

            "Музыка":
            [".mp3",".wav"]

        }


        for folder,extensions in categories.items():

            folder_path=os.path.join(
                self.current_path,
                folder
            )

            os.makedirs(
                folder_path,
                exist_ok=True
            )


            for file in os.listdir(
                self.current_path
            ):

                for ext in extensions:

                    if file.endswith(ext):

                        shutil.move(
                            file,
                            folder_path
                        )



        self.show_files()

        self.listbox.insert(
            "end",
            "\n Файлы отсортированы!\n"
        )




app=FileManager()

app.mainloop()