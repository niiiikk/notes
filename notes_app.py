from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QWidget, QHBoxLayout, QVBoxLayout,  QPushButton, QLabel, QTextEdit, QListWidget, QLineEdit, QInputDialog)
import json

app = QApplication([])
window = QWidget()

window.resize(900, 600)

window.setWindowTitle('Умные Заметки')

text = QTextEdit()
text.setPlaceholderText('Напиши здесь свою заметку')
add_note_btn = QPushButton('Создать Заметку')
delete_note_btn = QPushButton('Удалить Заметку')
save_note_btn = QPushButton('Сохранить Заметку')
add_teg_btn = QPushButton('Добавить к заметке')
minus_note_btn = QPushButton('Открепить от заметки')
search_note_btn = QPushButton('Искать заметки по тегу')
list_notes = QListWidget()
list_teg = QListWidget()
print_teg = QLineEdit()
print_teg.setPlaceholderText('Напиши здесь тег')
Label_spisok = QLabel('Список заметок')
Label_teg = QLabel('Список тегов')

layout_H = QHBoxLayout()
layout_V = QVBoxLayout()
layout_Button = QHBoxLayout()
layout_Button2 = QHBoxLayout()

layout_H.addWidget(text, stretch = 2)

layout_H.addLayout(layout_V, stretch = 1)

layout_V.addWidget(Label_spisok)
layout_V.addWidget(list_notes)

layout_V.addLayout(layout_Button)

layout_V.addWidget(save_note_btn)
layout_V.addWidget(Label_teg)
layout_V.addWidget(list_teg)
layout_V.addWidget(print_teg)

layout_V.addLayout(layout_Button2)

layout_V.addWidget(search_note_btn)

layout_Button.addWidget(add_note_btn)
layout_Button.addWidget(delete_note_btn)

layout_Button2.addWidget(add_teg_btn)
layout_Button2.addWidget(minus_note_btn)


window.setLayout(layout_H)

#Функции 

def show_note():
    key = list_notes.selectedItems()[0].text()
    text.setText(notes[key]['текст'])
    list_teg.clear()
    list_teg.addItems(notes[key]['теги'])




def add_note():
    name_note, ok = QInputDialog.getText(window, 'Добаить заметку', 'название заметки')
    if ok and name_note != '':
        notes[name_note] = {'текст' : '', 'теги' : []}
        list_notes.addItem(name_note)
        list_teg.addItems(notes[name_note]['теги'])
        



def save_note():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        notes[key]["текст"] = text.toPlainText()
        with open("notes_data.json", "w", encoding='utf-8') as file:
            json.dump(notes, file, sort_keys=True, ensure_ascii=False)
    else:
        print("Заметка для сохранения не выбрана!")

def delete_note():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        del notes[key]
        list_notes.clear()
        list_teg.clear()
        text.clear()
        list_notes.addItems(notes)
        with open("notes_data.json", "w", encoding='utf-8') as file:
            json.dump(notes, file, sort_keys=True, ensure_ascii=False)
        print(notes)
    else:
        print("Заметка для удаления не выбрана!")

def add_teg():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        tag = print_teg.text()
        if not tag in notes[key]["теги"]:
            notes[key]["теги"].append(tag)
            list_teg.addItem(tag)
            print_teg.clear()
        with open("notes_data.json", "w", encoding='utf-8') as file:
            json.dump(notes, file, sort_keys=True, ensure_ascii=False)
        print(notes)
    else:
        print("Заметка для добавления тега не выбрана!")

def delete_teg():
    if list_teg.selectedItems():
        key = list_notes.selectedItems()[0].text()
        tag = list_teg.selectedItems()[0].text()
        notes[key]["теги"].remove(tag)
        list_teg.clear()
        list_teg.addItems(notes[key]["теги"])
        with open("notes_data.json", "w", encoding='utf-8') as file:
            json.dump(notes, file, sort_keys=True, ensure_ascii=False)
    else:
        print("Тег для удаления не выбран!")

    

def search_teg():
    print(search_note_btn.text())
    tag = print_teg.text()
    if search_note_btn.text() == "Искать заметки по тегу" and tag:
        print(tag)
        notes_filtered = {} #тут будут заметки с выделенным тегом
        for note in notes:
            if tag in notes[note]["теги"]: 
                notes_filtered[note]=notes[note]
        search_note_btn.setText("Сбросить поиск")
        list_notes.clear()
        list_teg.clear()
        list_notes.addItems(notes_filtered)
        print(search_note_btn.text())
    elif search_note_btn.text() == "Сбросить поиск":
        print_teg.clear()
        list_notes.clear()
        list_teg.clear()
        list_notes.addItems(notes)
        search_note_btn.setText("Искать заметки по тегу")
        print(search_note_btn.text())
    else:
        pass

list_notes.itemClicked.connect(show_note)
add_note_btn.clicked.connect(add_note)
save_note_btn.clicked.connect(save_note)
delete_note_btn.clicked.connect(delete_note)
add_teg_btn.clicked.connect(add_teg)
minus_note_btn.clicked.connect(delete_teg)
search_note_btn.clicked.connect(search_teg)



with open('notes_data.json', 'r',encoding= 'utf-8') as file:
    notes = json.load(file)
    list_notes.addItems(notes)



window.show()
app.exec_()