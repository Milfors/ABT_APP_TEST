# kivy
from kivy.lang import Builder
#from kivy.core.window import Window
from functools import partial

#kivymd
from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton

# импорт переменных для цены
from PriceOsnovi import files_nail
from DiskiPedikur import Pedicure_discs
from FilesTonkie import Removable_files_on_a_thin_basis
from Bafi import Bafi
from FilesPena import FilesPena
from FilesDiskiPena import DiskiPena
from Other import OtherPrice

# библеотека для отпраки заказов
import smtplib
from email.mime.text import MIMEText

# размер экрана
#Window.size = (340, 600)

# итоговая ценв(список)
finalPriceKV = []

# словарь для корзины пользователя
Basket = {}


class MainApp(MDApp):

    # для всплывающего окна с предупреждением
    dialog = None

    # Списки для хранение цены
    new_files_nail = files_nail
    new_Pedicure_discs = Pedicure_discs
    new_Removable_files_on_a_thin_basis = Removable_files_on_a_thin_basis
    new_Bafi = Bafi
    new_FilesPena = FilesPena
    new_DiskiPena = DiskiPena
    new_OtherPrice = OtherPrice

    # для того чтобы программа видела файл с раширением .kv
    def build(self):
        self.theme_cls.primary_palette = 'Blue'
        return Builder.load_file('kv.kv')

    # функция добавления товаров
    def add_item(self, name, price, counter):

        # прверка на корректность ввода от пользователя
        # разрешенные здачения 1 2 3 4 5 6 7 8 9 0
        # нельзя добавить уже добавленный товар
        if name not in Basket and counter.isdigit() == True:
            # добавление товара с количетсом в корзину (словарь)
            Basket[name] = counter

            #print('Содержание корзины: ')
            #print(Basket)

            #подсчет цены в зависимости от количества
            priceCounter = int(price) * int(counter)

            #priceCounter = int(price) * int(counter)

            # добавление буквы 'р' для цены
            # добавление 'Кол-во' для количесва
            priceDependsOnQuantity = str(priceCounter) + ' ₽'
            counterr = 'Кол-во: ' + str(counter)

            # подсчет цены для KV
            finalPriceKV.append(priceCounter)

            # создание экземпляра для MDGridLayout и MDRaisedButton
            box = MDGridLayout(adaptive_height=True, cols=2)
            item = MDLabel(text=name, adaptive_height=True, adaptive_width=True)
            theFinalPriceForTheProduct = MDLabel(text=priceDependsOnQuantity, adaptive_height=True, adaptive_width=True, width=60, size_hint_x=None)
            quantity = MDLabel(text=counterr, adaptive_height=True, adaptive_width=True, width=120, size_hint_x=None)
            mdRB = MDRaisedButton(text='—', md_bg_color=(1, 0, 0, 1))

            # передача переменных в функцию удаления
            # для удаления
            mdRB.bind(on_press=partial(self.delete_mdRB, box, priceCounter, item))

            # добавление всех нужных виджетов для корзины
            box.add_widget(
                item
            )
            box.add_widget(
                theFinalPriceForTheProduct
            )
            box.add_widget(
                quantity
            )
            box.add_widget(
                mdRB
            )
            box.add_widget(
                MDLabel(text='-----------------------------', adaptive_height=True, adaptive_width=True, width=120, size_hint_x=None)
            )
            box.add_widget(
                MDLabel(text='-----------------------------', adaptive_height=True, adaptive_width=True, width=120, size_hint_x=None)
            )
            self.root.ids.basketItems.add_widget(
                box
            )

            # запись итоговой цены во вкладке "отправить"
            self.root.ids.name_mdlabel.text = str(sum(finalPriceKV))

        else:
            # всплывающее окно с предупреждением
            if not self.dialog:
                self.dialog = MDDialog(
                    title='Предупреждение!',
                    text='1.Некоректный ввод данных.\n(Используйте ТОЛЬКО цифры)\n2.Или Вы добавли товар,\nкоторый уже существует\nв корзине.\n(Проверти корзину)',
                    buttons=[
                        MDFlatButton(
                            text="ОК", text_color=self.theme_cls.primary_color, on_release=self.close_dialog
                        )
                    ]
                )
            self.dialog.open()

    # функция для закрытия всплывающего окна с предупреждением
    def close_dialog(self, odj):
        self.dialog.dismiss()


    #функция удаления товаров
    def delete_mdRB(self, box, priceCounter, item, button):

        # удаление конкретного товара
        box.parent.remove_widget(box)
        # удаление из товара из корзины
        del Basket[item.text]

        #print('Содержание корзины: ')
        #print(Basket)

        # корректовка итоговой цены
        finalPriceKV.remove(priceCounter)

        #print('итогова цена: ')
        #print(sum(finalPriceKV))

        self.root.ids.name_mdlabel.text = str(sum(finalPriceKV))

    # Полная очистка корзины
    def clearBasket(self):

        # очистка всех виджетов содержимого вкладки 'Корзина'
        for child in [child for child in self.root.ids.basketItems.children]:
            self.root.ids.basketItems.remove_widget(child)

        # очистка словара для корзины
        Basket.clear()

        # очитска списка для цены
        finalPriceKV.clear()

        #очистка переменной для вывода на экран во вкладке "Отправить"
        self.root.ids.name_mdlabel.text = str(sum(finalPriceKV))

        # print('Содержание корзины: ')
        # print(Basket)
        #
        # print('итогова цена: ')
        # print(sum(finalPriceKV))

    # функция для отправки заказа через почту
    def send_email(self, FIO, nubmer_phone, number_contract):
        sender = 'qeklim@gmail.com'
        password = 'bcihsklwreimvlku'
        to = 'melfors.ll@gmail.com'

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()

        Basket['ФИО'] = FIO
        Basket['Номер телефона'] = nubmer_phone
        Basket['Номер договора'] = number_contract
        Order = ''

        for item in Basket:
            Order += item + ':' + Basket[item] + '\n'

        try:
            server.login(sender, password)
            msg = MIMEText(Order)
            msg['Subject'] = f'Заказ от {FIO}'
            server.sendmail(sender, to, msg.as_string())

            # после отправки заказа происходит очитска всех полей
            finalPriceKV.clear()
            self.root.ids.name_mdlabel.text = str(sum(finalPriceKV))
            Basket.clear()

            self.root.ids.FIO.text = ''
            self.root.ids.nubmer_phone.text = ''
            self.root.ids.number_contract.text = ''

            for child in [child for child in self.root.ids.basketItems.children]:
                self.root.ids.basketItems.remove_widget(child)

            return print(f'Заказ отправлен!')
        except Exception as _ex:
            return print(f'{_ex}/Проверьте введенные данные!')

if __name__ == '__main__':
    MainApp().run()

