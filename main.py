from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
import sqlite3

base = sqlite3.connect('data.db')
c = base.cursor()

class MyApp(App):
    def build(self):
        #Створюємо головний макет
        layout = GridLayout(cols=2)
        # Створюємо елементи введення тексту
        self.name_input = TextInput()
        self.faculty_input = TextInput()
        self.group_input = TextInput()
        self.course_input = TextInput()
        self.section_input = TextInput()
        self.head_input = TextInput()
        self.title_input = TextInput()

        # Додаємо елементи введення тексту на макет
        layout.add_widget(Label(text='ПІБ студента:'))
        layout.add_widget(self.name_input)
        layout.add_widget(Label(text='Факультет студента:'))
        layout.add_widget(self.faculty_input)
        layout.add_widget(Label(text='Група студента:'))
        layout.add_widget(self.group_input)
        layout.add_widget(Label(text='Курс студента:'))
        layout.add_widget(self.course_input)
        layout.add_widget(Label(text='Назва наукової секції:'))
        layout.add_widget(self.section_input)
        layout.add_widget(Label(text='Керівник:'))
        layout.add_widget(self.head_input)
        layout.add_widget(Label(text='Назва доповіді:'))
        layout.add_widget(self.title_input)

        # Створюємо кнопки
        self.add_button = Button(text='Додати користувача')
        self.add_button.bind(on_press=self.add_users)

        self.print_button = Button(text='Вивести список користувачів')
        self.print_button.bind(on_press=self.print_users)

        self.delete_button = Button(text='Видалити користувача')
        self.delete_button.bind(on_press=self.delete_users)

        # Додаємо кнопки на макет
        layout.add_widget(self.add_button)
        layout.add_widget(self.print_button)
        layout.add_widget(self.delete_button)

        self.users_data = GridLayout(cols=1)

        self.users_popup = Popup(title='Список користувачів', content=self.users_data,
                                 size_hint=(None, None), size=(400, 400))

        return layout

    def print_users(self, instance):
        # Заповнюємо список користувачів
        c.execute("SELECT * FROM users")
        users = c.fetchall()

        if len(users) == 0:
            self.show_alert("Помилка", "У базі немає жодного користувача!")
        else:
            for user in users:
                user_label = Label(text=str(user))
                self.users_data.add_widget(user_label)

        self.users_popup.open()

    def show_alert(self, title, message):
        alert = Popup(title=title, content=Label(text=message), size_hint=(None, None), size=(200, 200))
        alert.open()

    def add_users(self, instance):
        # Додаємо користувача до бази даних
        name = self.name_input.text
        faculty = self.faculty_input.text
        group = self.group_input.text
        course = self.course_input.text
        section = self.section_input.text
        head = self.head_input.text
        title = self.title_input.text
        if name == '' or faculty == '' or group == '' or course == '' or section == '' or head == '' or title == '':
            self.show_alert("Помилка", "Будь ласка, заповніть усі поля!")
        else:
            c.execute(
                "INSERT INTO users (name, faculty, group_num, course, section_name, head, title) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (name, faculty, group, course, section, head, title))
            base.commit()
            self.show_alert("Успіх", "Користувача успішно додано до бази даних!")

    def print_users(self, instance):
        c.execute("SELECT * FROM users")
        users = c.fetchall()
        if len(users) == 0:
            self.show_alert("Помилка", "У базі немає жодного користувача!")
        else:
            for user in users:
                user_label = Label(text=str(user))
                self.users_data.add_widget(user_label)
            self.users_popup.open()

    def delete_users(self, instance):
        name = self.name_input.text
        if name == '':
            self.show_alert("Помилка", "Введіть ім'я користувача, якого бажаєте видалити!")
        else:
            c.execute("DELETE FROM users WHERE name=?", (name,))
            base.commit()
            self.show_alert("Успіх", "Користувача успішно видалено з бази даних!")


if __name__ == "__main__":
    MyApp().run()
