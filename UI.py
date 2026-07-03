import tkinter
from tkinter import ttk
import sv_ttk # https://github.com/rdbende/Sun-Valley-ttk-theme
import os
from helper import create_csv_string

def refresh_list():
    input_pdf_list = os.listdir("input")
    dictionary_list = os.listdir("dictionaries")

    input_pdf_menu['menu'].delete(0, 'end')
    for choice in input_pdf_list:
        input_pdf_menu['menu'].add_command(label=choice, command=tkinter._setit(input_pdf, choice))

    dictionary_menu['menu'].delete(0, 'end')
    for choice in dictionary_list:
        dictionary_menu['menu'].add_command(label=choice, command=tkinter._setit(dictionary, choice))

def create_csv():
    csv_ = create_csv_string(dictionary.get(),input_pdf.get())
    with open("output/"+input_pdf.get().split(".")[0]+".csv", "w", encoding="utf-8") as file:
        file.write(csv_)

root = tkinter.Tk()
root.geometry("400x400")
root.title("PDF to CSV")

for folder in ["input", "output", "dictionary"]:
    if not os.path.isdir(folder):
        os.makedirs(folder)

input_pdf_list = os.listdir("input")
dictionary_list = os.listdir("dictionaries")

if input_pdf_list == []:
    raise(IndexError("No pdf file in input/ directory"))

if dictionary_list == []:
    raise(IndexError("No dictionary file in dictionaries/ directory"))

input_pdf = tkinter.StringVar(root)
dictionary = tkinter.StringVar(root)

input_pdf.set("Choose input pdf")
dictionary.set("Choose Kaikki dictionary file")

refresh_button = ttk.Button(root, text="Refresh lists", command=refresh_list)
input_pdf_menu = tkinter.OptionMenu(root, input_pdf, *input_pdf_list)
dictionary_menu = tkinter.OptionMenu(root, dictionary, *dictionary_list)
create_button = ttk.Button(root, text="Create .csv", command=create_csv)


refresh_button.grid(row=0,column=0, rowspan=2, pady=10)
input_pdf_menu.grid(row=1,column=1, pady=10)
dictionary_menu.grid(row=2,column=1, pady=10)
create_button.grid(row=3,column=1, pady=10)

sv_ttk.set_theme("dark")
root.mainloop()