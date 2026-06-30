import os
import shutil
import zipfile
import customtkinter as ctk

from tkinter import filedialog


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class FileManager(ctk.CTk):

    def __init__(self):

        super().__init__()

        self.title("🚀 Smart File Manager PRO")
        self.geometry("1100x750")


        self.path=os.getcwd()

        self.selected_file=None



        ctk.CTkLabel(
            self,
            text="✨ Smart File Manager PRO",
            font=("Arial",30)
        ).pack(pady=15)



        panel=ctk.CTkFrame(self)
        panel.pack()



        buttons=[

            ("📂 Папка",self.open_folder),

            ("📊 Размер",self.sort_size),

            ("🧹 Очистка",self.smart_clean),

            ("📦 ZIP",self.make_zip)

        ]


        for i,(txt,cmd) in enumerate(buttons):

            ctk.CTkButton(
                panel,
                text=txt,
                command=cmd
            ).grid(
                row=0,
                column=i,
                padx=5
            )




        self.files=ctk.CTkScrollableFrame(
            self,
            width=500,
            height=450
        )

        self.files.pack(
            side="left",
            padx=20,
            pady=20
        )



        self.info=ctk.CTkTextbox(
            self,
            width=400,
            height=300
        )

        self.info.pack(
            side="right",
            padx=20
        )



        self.show()



    # загрузка файлов


    def show(self):

        for w in self.files.winfo_children():

            w.destroy()



        for file in os.listdir(self.path):


            btn=ctk.CTkButton(

                self.files,

                text="📄 "+file,

                anchor="w",

                command=lambda f=file:
                self.select_file(f)

            )

            btn.pack(
                fill="x",
                pady=3
            )





    # выделение файла


    def select_file(self,file):


        self.selected_file=file


        full=os.path.join(
            self.path,
            file
        )


        size=os.path.getsize(full)/1024/1024


        self.info.delete(
            "0.0",
            "end"
        )


        self.info.insert(
            "end",

f"""
Выбран файл:

📄 {file}


Размер:
{size:.2f} MB


Путь:

{full}

"""
        )




    # папка


    def open_folder(self):

        folder=filedialog.askdirectory()

        if folder:

            self.path=folder

            self.show()





    # сортировка по размеру


    def sort_size(self):


        files=[]


        for f in os.listdir(self.path):

            p=os.path.join(
                self.path,
                f
            )

            if os.path.isfile(p):

                files.append(
                    (
                        f,
                        os.path.getsize(p)
                    )
                )


        files.sort(
            key=lambda x:x[1],
            reverse=True
        )


        self.info.delete(
            "0.0",
            "end"
        )


        for f,s in files:


            self.info.insert(
                "end",
                f"{f} | {s/1024/1024:.1f} MB\n"
            )






    # умная очистка


    def smart_clean(self):


        found=[]


        for root,dirs,files in os.walk(
            self.path
        ):


            for file in files:


                full=os.path.join(
                    root,
                    file
                )


                size=os.path.getsize(full)


                # временные

                if file.endswith(
                    (".tmp",".log",".bak")
                ):

                    found.append(
                        full
                    )


                # большие файлы

                elif size>500*1024*1024:

                    found.append(
                        full
                    )



        self.info.delete(
            "0.0",
            "end"
        )


        self.info.insert(
            "end",
            "🧹 Найдено:\n\n"
        )


        if not found:

            self.info.insert(
                "end",
                "Мусора нет 👍"
            )

        else:

            for f in found:

                self.info.insert(
                    "end",
                    f+" \n"
                )




    # ZIP


    def make_zip(self):


        with zipfile.ZipFile(
            "Archive.zip",
            "w"
        ) as z:


            for f in os.listdir(self.path):


                if os.path.isfile(
                    os.path.join(
                        self.path,
                        f
                    )
                ):


                    z.write(
                        os.path.join(
                            self.path,
                            f
                        ),
                        f
                    )



        self.info.insert(
            "end",
            "\n\n📦 ZIP создан!"
        )






app=FileManager()

app.mainloop()
