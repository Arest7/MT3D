from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp
from kivymd.uix.button import MDRaisedButton, MDRectangleFlatIconButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.screenmanager import Screen
from plyer import filechooser
from kivymd.toast import toast
import json
from kivy.core.window import Window

# Fayldan ma'lumotlarni o'qish funksiyasi
def read_data_from_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data
    except Exception as e:
        print(f"Fayldan o'qishda xatolik: {e}")
        return []

# Saralash funksiyalari
def direct_insertion_sort(data, key):
    for i in range(1, len(data)):
        current = data[i]
        j = i - 1
        while j >= 0 and data[j][key] > current[key]:
            data[j + 1] = data[j]
            j -= 1
        data[j + 1] = current
    return data

def direct_selection_sort(data, key):
    for i in range(len(data)):
        min_index = i
        for j in range(i + 1, len(data)):
            if data[j][key] < data[min_index][key]:
                min_index = j
        data[i], data[min_index] = data[min_index], data[i]
    return data

def direct_bubble_sort(data, key):
    for i in range(len(data) - 1):
        for j in range(len(data) - 1 - i):
            if data[j][key] > data[j + 1][key]:
                data[j], data[j + 1] = data[j + 1], data[j]
    return data

# KivyMD bilan dastur
class TarbiyalanuvchilarApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data = []  # Ma'lumotlar ro'yxati
        self.title = "Tarbiyalanuvchilar Saralash"
        self.theme_cls.theme_style = "Light"  # You can also use "Dark"
        self.theme_cls.primary_palette = "Cyan"

    def build(self):
        # Asosiy ekranni yaratish
        screen = Screen()
        layout = MDBoxLayout(orientation='vertical', spacing=20, padding=20)
        Window.size = (900, 700)
        
        # Fayl tanlash va saralash tugmalari
        sort_buttons = MDBoxLayout(orientation='horizontal', size_hint=(1, None), height=dp(50), spacing=10)
        sort_buttons.add_widget(MDRectangleFlatIconButton(
            text="Fayl tanlash", 
            icon="folder",
            on_release=self.file_manager_open,
            theme_text_color="Custom",
            text_color=self.theme_cls.primary_color,
        ))
        sort_buttons.add_widget(MDRectangleFlatIconButton(
            text="Qo'shish Usuli", 
            icon="sort",
            on_release=self.sort_by_direct_insertion,
            theme_text_color="Custom",
            text_color=self.theme_cls.primary_color,
        ))
        sort_buttons.add_widget(MDRectangleFlatIconButton(
            text="Tanlash Usuli", 
            icon="sort-variant",
            on_release=self.sort_by_direct_selection,
            theme_text_color="Custom",
            text_color=self.theme_cls.primary_color,
        ))
        sort_buttons.add_widget(MDRectangleFlatIconButton(
            text="Almashtirish Usuli", 
            icon="sort-ascending",
            on_release=self.sort_by_direct_bubble,
            theme_text_color="Custom",
            text_color=self.theme_cls.primary_color,
        ))

        layout.add_widget(sort_buttons)

        # DataTable uchun
        self.table = MDDataTable(
            size_hint=(1, 0.8),
            column_data=[
                ("Tarbiyalanuvchi", dp(30)),
                ("Bog'cha No.", dp(20)),
                ("Guruh", dp(15)),
                ("Yoshi", dp(20)),
            ],
            row_data=[],
        )

        # DataTable ni layoutga qo'shish
        layout.add_widget(self.table)
        screen.add_widget(layout)

        return screen

    # Faylni tanlash va o'qish
    def file_manager_open(self, *args):
        path = filechooser.open_file(title="Faylni tanlang", filters=["*.json"])
        if path:
            self.data = read_data_from_file(path[0])  # path[0] - tanlangan fayl
            if self.data:
                self.update_table()
                toast("Fayl muvaffaqiyatli yuklandi!")  # Toast orqali bildirishnoma
            else:
                toast("Faylni o'qishda xatolik yuz berdi.")

    # Ma'lumotlarni yangilash
    def update_table(self):
        self.table.row_data = [
            (d['fish'], str(d['bogcha_nomer']), d['guruh'], str(d['yoshi']))
            for d in self.data
        ]
    
    # Saralash usullari
    def sort_by_direct_insertion(self, instance):
        self.data = direct_insertion_sort(self.data, 'yoshi')
        self.update_table()
        toast("To'g'ridan-to'g'ri Qo'shish usuli bo'yicha saralandi")

    def sort_by_direct_selection(self, instance):
        self.data = direct_selection_sort(self.data, 'fish')
        self.update_table()
        toast("To'g'ridan-to'g'ri Tanlash usuli bo'yicha saralandi")

    def sort_by_direct_bubble(self, instance):
        self.data = direct_bubble_sort(self.data, 'bogcha_nomer')
        self.update_table()
        toast("To'g'ridan-to'g'ri Almashtirish usuli bo'yicha saralandi")

# Dastur ishlatilishi
if __name__ == '__main__':
    TarbiyalanuvchilarApp().run()
