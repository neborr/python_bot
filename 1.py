import telebot
import SimpleQIWI
import sql3Functions
import uuid

token = '8689d180b4c1314a97b7c0bb5fe202b5'
phone = '+79226793786'
wallet = SimpleQIWI.QApi(token=token, phone=phone)
bot = telebot.TeleBot('5496962451:AAE2zlW80MHwfrCTkqhx_R1kzDde-p_T-9I')

menuKeyboard = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
menuKeyboard.add(telebot.types.KeyboardButton('Ассортимент'),
                 telebot.types.KeyboardButton('Личные данные'),
                 telebot.types.KeyboardButton('Корзина покупок'),
                 telebot.types.KeyboardButton('Оплатить покупки'),
                 telebot.types.KeyboardButton('Воспользоватся кэшбеком'),
                 telebot.types.KeyboardButton('Заказы'),
                 telebot.types.KeyboardButton('Выполнить заказ'))

shoppingCartKeyboard = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
shoppingCartKeyboard.add(telebot.types.KeyboardButton('Очистить корзину'),
                 telebot.types.KeyboardButton('Оплатить покупки'),
                 telebot.types.KeyboardButton('Главное меню'))

paymentKeyboard = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
paymentKeyboard.add(telebot.types.KeyboardButton('Проверить оплату'),
                 telebot.types.KeyboardButton('Главное меню'))

delitKeyboard = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
delitKeyboard.add(telebot.types.KeyboardButton('Да'),
                 telebot.types.KeyboardButton('Нет'))


@bot.message_handler(commands=['start'])
def start_message(message):
    id = message.from_user.id
    name = message.from_user.first_name
    surname = message.from_user.last_name
    username = message.from_user.username
    language = message.from_user.language_code

    sql3Functions.create_table(r'neskam.db',
                               'orders',
                               userId='INT',
                               primogemsID='TEXT',
                               comment='TEXT')

    sql3Functions.create_table(r'neskam.db',
                               'shoppingCart',
                               userId='INT',
                               primogemsID='TEXT',
                               totalSum='INT',
                               comment='TEXT',
                               cashback='INT')

    sql3Functions.create_table(r'neskam.db',
                               'users',
                               id='INT',
                               name='TEXT',
                               surname='TEXT',
                               username='TEXT',
                               language='TEXT',
                               balance='REAL')
    if sql3Functions.get_from_table(r'neskam.db', 'users', id=id) == None:
        sql3Functions.insert_into_table(r'neskam.db',
                                        'users',
                                        id=id, name=name, surname=surname, username=username, language=language, balance=0)
    if sql3Functions.get_from_table(r'neskam.db', 'shoppingCart', userId=id) == None:
        sql3Functions.insert_into_table(r'neskam.db',
                                        'shoppingCart',
                                        userId=id, primogemsID=0, totalSum=0, comment=None)
    if sql3Functions.get_from_table(r'neskam.db', 'orders', userId=id) == None:
        sql3Functions.insert_into_table(r'neskam.db',
                                        'orders',
                                        userId=id, primogemsID=0, comment=None)
    bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEGxSdjlMD3o_il9oxlXnjUlzw5E4L42wACQSgAAoaIqEjlJcfqZurtvisE')
    bot.send_message(message.chat.id, 'Добро пожаловать в НЕскам магазин!')
    bot.send_message(message.chat.id, 'Выберите один из пунктов меню', reply_markup=menuKeyboard)

    bot.register_next_step_handler(message, get_answer)
    if id == 5018518202:
        pass
def get_answer(message):
    id = message.from_user.id
    if message.text == 'Ассортимент':
        assortment_data = sql3Functions.get_all_from_table(r'neskam.db', 'primogems')

        for primogems in assortment_data:
            primogems_info = f'ID: {primogems[0]}\n' + f'Название: {primogems[1]}\n' + f'Цена: {primogems[2]} рублей'
            k = sql3Functions.get_from_table(r'neskam.db', 'primogems', id=primogems[0])
            bot.send_sticker(message.chat.id, k[3])

            bot.send_message(message.chat.id, primogems_info)

        else:
            bot.send_message(message.chat.id, 'Выберите ID гемов')

            bot.register_next_step_handler(message, primogems_id)

    elif message.text == 'Заказы' and id == 803721716:
        bot.send_message(message.chat.id, 'Отправте чек заказа')
        bot.register_next_step_handler(message, Orders)

    elif message.text == 'Выполнить заказ' and id == 803721716:
        bot.send_message(message.chat.id, 'Отправте чек заказа')
        bot.register_next_step_handler(message, Execute_an_order)

    elif message.text == 'Личные данные':
        personal_data = sql3Functions.get_from_table(r'neskam.db', 'users', username=message.from_user.username)
        id = personal_data[0]
        name = personal_data[1]
        surname = personal_data[2]
        username = personal_data[3]
        language = personal_data[4]
        balance = personal_data[5]

        bot.send_message(message.chat.id,
                         f'ID: {id}\n' +
                         f'Имя: {name}\n' +
                         f'Фамилия: {surname}\n' +
                         f'Имя пользователя: @{username}\n' +
                         f'Язык: {language}\n' +
                         f'Баланс: {balance} руб',
                         reply_markup=menuKeyboard)

        bot.register_next_step_handler(message, get_answer)

    elif message.text == 'Корзина покупок':
        userId = message.from_user.id
        shoppingCart = sql3Functions.get_from_table(r'neskam.db', 'shoppingCart', userId=userId)

        if shoppingCart == None or shoppingCart[1] == '0':
            bot.send_message(message.chat.id, 'Корзина пуста', reply_markup=menuKeyboard)

            bot.register_next_step_handler(message, get_answer)

        else:
            prim_kup = (shoppingCart[1]).strip().split(' ')

            for pokypki in prim_kup:
                if pokypki == '0':
                    continue
                l = sql3Functions.get_from_table(r'neskam.db', 'primogems', id=pokypki)
                kup_gem = f'ID: {l[0]}\n' + f'Название: {l[1]}\n' + f'Цена: {l[2]} рублей'
                bot.send_sticker(message.chat.id, l[3])
                bot.send_message(message.chat.id, kup_gem)
            else:
                bot.send_message(message.chat.id, f'Общяя сумма: {shoppingCart[2]} руб')
                bot.send_message(message.chat.id, 'Вы хотите очистить корзину?', reply_markup=delitKeyboard)
                bot.register_next_step_handler(message, delit)


    elif message.text == 'Оплатить покупки':
        userData = sql3Functions.get_from_table('neskam.db', 'shoppingCart', userId=message.from_user.id)
        sum = userData[2]
        comment = str(uuid.uuid4())

        sql3Functions.update_table('neskam.db', 'shoppingCart', 'comment', comment, userId=message.from_user.id)
        bot.send_message(message.chat.id,
                         f'Переведите {sum} рублей с Вашего QIWI Кошелька на QIWI Счет {phone} с комментарием {comment}',
                         reply_markup=paymentKeyboard)

        bot.register_next_step_handler(message, check_payment)

    else:
        bot.send_message(message.chat.id, 'Выберите один из пунктов меню', reply_markup=menuKeyboard)

        bot.register_next_step_handler(message, get_answer)

def primogems_id(message):
    try:

        userId = message.from_user.id
        idd = int(message.text)
        primogems_data = sql3Functions.get_from_table(r'neskam.db', 'primogems', id=idd)

        if primogems_data == None:
            bot.send_message(message.chat.id, 'Выбранные Вами примогемы отсутствует в продаже',
                             reply_markup=menuKeyboard)
            bot.register_next_step_handler(message, get_answer)

        else:
            d = sql3Functions.get_from_table(r'neskam.db', 'shoppingCart', userId=userId)
            dd = d[1]
            b = d[2]
            bot.send_sticker(message.chat.id, primogems_data[3])
            bot.send_message(message.chat.id, f'{primogems_data[2]} руб')
            ddd = f'{dd} {primogems_data[0]}'
            bb = f'{int(b) + int(primogems_data[2])}'
            sql3Functions.update_table(r'neskam.db', 'shoppingCart', 'primogemsID', f"{ddd}", userId=userId)
            sql3Functions.update_table(r'neskam.db', 'shoppingCart', 'totalSum', f"{bb}", userId=userId)
            bot.send_message(message.chat.id, 'Вы успешно добавили товар в корзину', reply_markup=menuKeyboard)
            bot.register_next_step_handler(message, get_answer)

    except:
        bot.send_message(message.chat.id, 'Выбранные Вами примогемы отсутствует в продаже', reply_markup=menuKeyboard)
        bot.register_next_step_handler(message, get_answer)

def delit(message):
    userId = message.from_user.id
    if message.text == 'Нет':
        bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEGxQtjlLzl9ZpuMTFX1aT82FOEoH0EjgACNxAAAiySYEjN86Q4WRMitSsE', reply_markup=menuKeyboard)
        bot.register_next_step_handler(message, get_answer)
    elif message.text == 'Да':
        sql3Functions.update_table(r'neskam.db', 'shoppingCart', 'primogemsID', "0", userId=userId)
        sql3Functions.update_table(r'neskam.db', 'shoppingCart', 'totalSum', "0", userId=userId)
        bot.send_message(message.chat.id, 'Вы успешно очистили корзину!', reply_markup=menuKeyboard)
        bot.register_next_step_handler(message, get_answer)
    else:
        bot.send_message(message.chat.id, 'Выберите один из пунктов меню', reply_markup=menuKeyboard)

        bot.register_next_step_handler(message, get_answer)

def check_payment(message):
    if message.text == 'Главное меню':
            bot.send_message(message.chat.id, 'Выберите один из пунктов меню', reply_markup=menuKeyboard)
            bot.register_next_step_handler(message, get_answer)


    elif message.text == 'Проверить оплату':
        userData = sql3Functions.get_from_table('neskam.db', 'shoppingCart', userId=message.from_user.id)
        payments = wallet.payments
        sum = userData[2]
        comment = userData[3]

        for payment in payments['data']:
            paymentSum = payment['sum']['amount']
            paymentComment = payment['comment']

            if paymentSum == sum and paymentComment == comment:
                d = sql3Functions.get_from_table(r'neskam.db', 'shoppingCart', userId=message.from_user.id)
                c = sql3Functions.get_from_table(r'neskam.db', 'orders', userId=message.from_user.id)
                cc = c[1]
                dd = d[1]
                ddd = d[3]
                h = f'{cc} {dd}'
                bot.send_message(message.chat.id, 'Товар оплачен')
                bot.send_message(message.chat.id, f'напишите @Nebor и отправте чек- {comment}  чтобы получить товар')
                sql3Functions.update_table('neskam.db', 'orders', 'primogemsID', h, userId=message.from_user.id)
                sql3Functions.update_table('neskam.db', 'orders', 'comment', ddd, userId=message.from_user.id)
                sql3Functions.update_table(r'neskam.db', 'shoppingCart', 'primogemsID', "0", userId=message.from_user.id)
                sql3Functions.update_table('neskam.db', 'shoppingCart', 'totalSum', 0, userId=message.from_user.id)
                sql3Functions.update_table('neskam.db', 'shoppingCart', 'comment', None, userId=message.from_user.id)
                bot.send_message(message.chat.id, 'Выберите один из пунктов меню', reply_markup=menuKeyboard)
                bot.register_next_step_handler(message, get_answer)
                break



        else:
            d = sql3Functions.get_from_table(r'neskam.db', 'shoppingCart', userId=message.from_user.id)
            c = sql3Functions.get_from_table(r'neskam.db', 'orders', userId=message.from_user.id)
            cc = c[1]
            dd = d[1]
            ddd = d[3]
            h = f'{cc} {dd}'
            bot.send_message(message.chat.id, 'Товар оплачен')
            bot.send_message(message.chat.id, f'напишите @Nebor и отправте чек- {comment}  чтобы получить товар')
            sql3Functions.update_table('neskam.db', 'orders', 'primogemsID', h, userId=message.from_user.id)
            sql3Functions.update_table('neskam.db', 'orders', 'comment', ddd, userId=message.from_user.id)
            sql3Functions.update_table(r'neskam.db', 'shoppingCart', 'primogemsID', "0", userId=message.from_user.id)
            sql3Functions.update_table('neskam.db', 'shoppingCart', 'totalSum', 0, userId=message.from_user.id)
            sql3Functions.update_table('neskam.db', 'shoppingCart', 'comment', None, userId=message.from_user.id)
            bot.send_message(message.chat.id, 'Выберите один из пунктов меню', reply_markup=menuKeyboard)
            bot.register_next_step_handler(message, get_answer)
            bot.send_message(message.chat.id, 'Товар не оплачен', reply_markup=paymentKeyboard)
            bot.register_next_step_handler(message, check_payment)
    else:
        bot.send_message(message.chat.id, 'Выберите один из пунктов меню', reply_markup=menuKeyboard)

        bot.register_next_step_handler(message, get_answer)
def Orders(message):
    try:
        if message.text == "0" or message.text == "None":
            bot.send_message(message.chat.id, 'Попробуйте ещё раз', reply_markup=menuKeyboard)
            bot.register_next_step_handler(message, get_answer)
        else:
            chek = sql3Functions.get_from_table(r'neskam.db', 'orders', comment=message.text)
            if chek[1] == 0:
                bot.send_message(message.chat.id, "Нет такого заказа", reply_markup=menuKeyboard)
                bot.register_next_step_handler(message, get_answer)
            else:
                 bot.send_message(message.chat.id, f'Покупка пользователя с ID- {chek[0]} товары({chek[1]})', reply_markup=menuKeyboard)
                 bot.register_next_step_handler(message, get_answer)
    except:
        bot.send_message(message.chat.id, 'Заказа не существует', reply_markup=menuKeyboard)
        bot.register_next_step_handler(message, get_answer)

def Execute_an_order(message):
    try:
        if message.text == "0" or message.text == "None":
            bot.send_message(message.chat.id, 'Попробуйте ещё раз', reply_markup=menuKeyboard)
            bot.register_next_step_handler(message, get_answer)
        else:
            chek = sql3Functions.get_from_table(r'neskam.db', 'orders', comment=message.text)
            if chek[1] == 0 or chek[2] == 0:
                bot.send_message(message.chat.id, "Нет такого заказа", reply_markup=menuKeyboard)
                bot.register_next_step_handler(message, get_answer)
            else:
                sql3Functions.update_table(r'neskam.db', 'orders', 'primogemsID', 0, comment=message.text)
                sql3Functions.update_table('neskam.db', 'orders', 'comment', None, comment=message.text)
                bot.send_message(message.chat.id, 'Вы успешно выполнили заказ', reply_markup=menuKeyboard)
                bot.register_next_step_handler(message, get_answer)
    except:
        bot.send_message(message.chat.id, 'Заказа не существует', reply_markup=menuKeyboard)
        bot.register_next_step_handler(message, get_answer)

bot.polling(non_stop=True, interval=0)