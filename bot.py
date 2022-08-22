import time
from config import *
import telebot
from telebot import types
import sqlite3
import random

conn = sqlite3.connect('database.db', check_same_thread=False)
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS users_db
            (user_id TEXT,\
            user_username TEXT,\
            admin TEXT,\
            money INT,\
            link  TEXT,\
            banned TEXT)''')
		
conn.commit()


bot = telebot.TeleBot(settings['tokken'])

chats_link = types.InlineKeyboardMarkup()
worker_chat = types.InlineKeyboardButton(text="Чат воркеров🧑‍💻", url="https://t.me/+Mhp4Hg5Q-GQ2Nzdi")
chats_link.add(worker_chat)

main_menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
profile = types.KeyboardButton("Профиль👨‍💼")
setting = types.KeyboardButton("Настройки⚙️")
link = types.KeyboardButton("Ссылка📎")
chat = types.KeyboardButton("Заказать выплату💰")
main_menu.add(link, profile)
main_menu.add(setting, chat)

setting_menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
chats = types.KeyboardButton("Наши чаты💌")
back = types.KeyboardButton("Назад⬅️")
setting_menu.add(chats)
setting_menu.add(back)

admin = types.ReplyKeyboardMarkup(resize_keyboard=True)
spam = types.KeyboardButton("Рассылка🔥")
add_admin = types.KeyboardButton("Добавить админа👨🏻‍🔧")
del_admin = types.KeyboardButton("Удалить админа💀")
ban = types.KeyboardButton("Забанить пользователя💩")
give_money = types.KeyboardButton("Дать денег💸")
money_minus = types.KeyboardButton("Забрать денег🪦")
admin.add(spam)
admin.add(add_admin,del_admin,ban)
admin.add(give_money,money_minus)
admin.add(back)


spam_settings = types.ReplyKeyboardMarkup(resize_keyboard=True)
spam_text = types.KeyboardButton("Текст📜")
spam_photo = types.KeyboardButton("Картинка+Текст🖼")
spam_photo_no_text = types.KeyboardButton("Картинку🖼")
spam_settings.add(spam_text,spam_photo,spam_photo_no_text)

workspace = types.ReplyKeyboardMarkup(resize_keyboard=True)
CRYPTOLIR = types.KeyboardButton("CRYPTOLIR")
workspace.add(CRYPTOLIR)
workspace.add(back)

def multiple_replace(target_str, replace_values):
    for i, j in replace_values.items():
        target_str = target_str.replace(i, j)
    return target_str

@bot.message_handler(commands=['start'])
def send_welcome(message):
    try:
        bot.delete_message(message.chat.id, message.message_id)
        bot.delete_message(message.chat.id, message.message_id - 1)
    except:
        pass
    info = c.execute(f'SELECT * FROM users_db WHERE user_id="{message.chat.id}"')
    if info.fetchone() is None:
        msg = bot.send_message(message.chat.id, texts['start'].replace('$', message.chat.username), parse_mode='HTML')
        bot.register_next_step_handler(msg, second)
    else:
        bot.send_message(message.chat.id, 'Welcome back!', reply_markup=main_menu, parse_mode='HTML')

def kartinka(message):
    try:
        bot.delete_message(message.chat.id, message.message_id)
        bot.delete_message(message.chat.id, message.message_id - 1)
    except:
        pass
    tx = message.caption
    spam_mesag = message.photo[len(message.photo)-1].file_id

    c.execute("SELECT user_id FROM users_db where banned = '0'")
    a = c.fetchall()
    
    for id_spam in a:
        if str(message.chat.id) != id_spam[0]:
            bot.send_photo(id_spam[0], spam_mesag, caption=tx)
        else:
            pass
    bot.send_message(message.chat.id, 'Готово✅', reply_markup=admin)

def textovik(message):
    try:
        bot.delete_message(message.chat.id, message.message_id)
        bot.delete_message(message.chat.id, message.message_id - 1)
    except:
        pass
    spam_mesag = message.text
    c.execute("SELECT user_id FROM users_db where banned = '0'")
    a = c.fetchall()
    for id_spam in a:
        if str(message.chat.id) != id_spam[0]:
            bot.send_message(id_spam[0], spam_mesag)
        else:
            pass
    bot.send_message(message.chat.id, 'Готово✅', reply_markup=admin)

def kartinka_no_text(message):
    try:
        bot.delete_message(message.chat.id, message.message_id)
        bot.delete_message(message.chat.id, message.message_id - 1)
    except:
        pass
    spam_mesag = message.photo[len(message.photo)-1].file_id

    c.execute("SELECT user_id FROM users_db where banned = '0'")
    a = c.fetchall()
    
    for id_spam in a:
        if str(message.chat.id) != id_spam[0]:
            bot.send_photo(id_spam[0], spam_mesag)
        else:
            pass
    bot.send_message(message.chat.id, 'Готово✅', reply_markup=admin)

def second(message):
    try:
        bot.delete_message(message.chat.id, message.message_id)
        bot.delete_message(message.chat.id, message.message_id - 1)
    except:
        pass
    if message.text == '/start':
        msg = bot.send_message(message.chat.id, texts['anser_bitch'], parse_mode='HTML')
        bot.register_next_step_handler(msg, second)
    else:
        msg = bot.send_message(message.chat.id, texts['second'], parse_mode='HTML')
        bot.register_next_step_handler(msg, last)


def last(message):
    try:
        bot.delete_message(message.chat.id, message.message_id)
        bot.delete_message(message.chat.id, message.message_id - 1)
    except:
        pass
    if message.text == '/start':
        bot.send_message(message.chat.id, texts['anser_bitch'], parse_mode='HTML')
    else:
        bot.send_message(message.chat.id, texts['wait'], parse_mode='HTML')
        time.sleep(5)
        sqlite_insert_query = f"""INSERT INTO users_db
                            (user_id, user_username, admin, money, link, banned)
                            VALUES
                            ('{message.chat.id}', '{message.chat.username}', '0', 0, 'У вас нет ссылки', '0');"""
        count = c.execute(sqlite_insert_query)
        conn.commit()
        bot.delete_message(message.chat.id, message.message_id + 1)
        bot.send_message(message.chat.id, texts['welcome'].replace('$', message.chat.username), parse_mode='HTML', reply_markup=main_menu)


def add_adm_func(message):
    adminlist = c.execute(f'SELECT user_id FROM users_db WHERE admin="1"')
    admlist = adminlist.fetchall()
    ms_bd = []
    for a in admlist:
        ms_bd.append(a[0])
    if str(message.chat.id) in ms_bd:
        name = message.text
        user_name_find = c.execute(f"SELECT user_id FROM users_db WHERE user_username='{name}'")
        user_name_check = user_name_find.fetchall()
        c.execute(f"""UPDATE users_db SET admin = '1' WHERE user_id = '{user_name_check[0][0]}' """)
        conn.commit()
        bot.send_message(user_name_check[0][0], f'Тебя добавили в число админов!\n\nНапиши /admin')
        for admin_news in ms_bd:
            bot.send_message(admin_news, f'У нас еще 1 админ!\n\n@{name}')



def add_money_func(message):
    adminlist = c.execute(f'SELECT user_id FROM users_db WHERE admin="1"')
    admlist = adminlist.fetchall()
    ms_bd = []
    for a in admlist:
        ms_bd.append(a[0])
    if str(message.chat.id) in ms_bd:
        name_and_money = message.text.split(' ')
        name, money_donat = name_and_money
        user_name_find = c.execute(f"SELECT user_id FROM users_db WHERE user_username='{name}'")
        user_name_check = user_name_find.fetchall()
        c.execute(f"""UPDATE users_db SET money = money + '{money_donat}' WHERE user_id = '{user_name_check[0][0]}' """)
        conn.commit()
        bot.send_message(user_name_check[0][0], f'Тебе добавили {money_donat} рублей')
        for admin_news in ms_bd:
            bot.send_message(admin_news, f'Один из Админов кинул воркеру деньги\n\nВоркер: @{name}\n\nСумма донната: {money_donat}')

        bot.send_message(message.chat.id, f'Готово!✅', reply_markup=admin)


def del_money_func(message):
    adminlist = c.execute(f'SELECT user_id FROM users_db WHERE admin="1"')
    admlist = adminlist.fetchall()
    ms_bd = []
    for a in admlist:
        ms_bd.append(a[0])
    if str(message.chat.id) in ms_bd:
        name_and_money = message.text.split(' ')
        name, money_donat = name_and_money
        user_name_find = c.execute(f"SELECT user_id FROM users_db WHERE user_username='{name}'")
        user_name_check = user_name_find.fetchall()
        c.execute(f"""UPDATE users_db SET money = money - '{money_donat}' WHERE user_id = '{user_name_check[0][0]}' """)
        conn.commit()
        bot.send_message(user_name_check[0][0], f'У тебе забрали {money_donat} рублей')
        for admin_news in ms_bd:
            bot.send_message(admin_news, f'Один из Админов спиздил у воркера деньги\n\nВоркер: @{name}\n\nСумма списания: {money_donat}')


        bot.send_message(message.chat.id, f'Готово!✅', reply_markup=admin)
def del_adm_func(message):
    adminlist = c.execute(f'SELECT user_id FROM users_db WHERE admin="1"')
    admlist = adminlist.fetchall()
    ms_bd = []
    for a in admlist:
        ms_bd.append(a[0])
    if str(message.chat.id) in ms_bd:
        name = message.text
        user_name_find = c.execute(f"SELECT user_id FROM users_db WHERE user_username='{name}'")
        user_name_check = user_name_find.fetchall()
        c.execute(f"""UPDATE users_db SET admin = '0' WHERE user_id = '{user_name_check[0][0]}' """)
        conn.commit()
        bot.send_message(user_name_check[0][0], f'Ты больше не админ!')
        ms_bd.remove(user_name_check[0][0])
        for admin_news in ms_bd:
            bot.send_message(admin_news, f'У нас - 1 админ!\n\n@{name}')


def ban_func(message):
    adminlist = c.execute(f'SELECT user_id FROM users_db WHERE admin="1"')
    admlist = adminlist.fetchall()
    ms_bd = []
    for a in admlist:
        ms_bd.append(a[0])
    if str(message.chat.id) in ms_bd:
        name = message.text
        user_name_find = c.execute(f"SELECT user_id FROM users_db WHERE user_username='{name}'")
        user_name_check = user_name_find.fetchall()
        c.execute(f"""UPDATE users_db SET banned = '1' WHERE user_id = '{user_name_check[0][0]}' """)
        conn.commit()
        bot.send_message(user_name_check[0][0], f'Тебя забанили!')
        bot.send_message(message.chat.id, f'Готово!✅')

def viplata(message):
    name = message.text
    user_name_find = c.execute(f"SELECT user_id FROM users_db WHERE admin='1'")
    user_name_check = user_name_find.fetchall()
    adm = []
    for a in user_name_check:
        adm.append(a[0])
    rpm_adm = random.choice(adm)
    bot.send_message(rpm_adm, f'Новый заказ на выплату!\n\nВоркер: @{message.chat.username}\n\nСумма: {name}')
    bot.send_message(message.chat.id, f'Админы получили ваш заказ на выплату, в скором времени вам отпишут!\n\nСумма: {name}')

@bot.message_handler(commands=['admin'])
def send_admin(message):
    try:
        bot.delete_message(message.chat.id, message.message_id)
        bot.delete_message(message.chat.id, message.message_id - 1)
    except:
        pass

    adminlist = c.execute(f'SELECT user_id FROM users_db WHERE admin="1"')
    admlist = adminlist.fetchall()
    ms_bd = []
    for a in admlist:
        ms_bd.append(a[0])
    if str(message.chat.id) in ms_bd:
        bot.send_message(message.chat.id, texts['admin'], reply_markup=admin)

@bot.message_handler(content_types=['text'])
def texthandler(message):
    try:
        bot.delete_message(message.chat.id, message.message_id)
        bot.delete_message(message.chat.id, message.message_id - 1)
    except:
        pass
    info = c.execute(f'SELECT banned FROM users_db WHERE user_id="{message.chat.id}"')
    if info.fetchone()[0][0] == '0':
        mci = message.chat.id
        if message.text == 'Профиль👨‍💼':
            data_db = c.execute(f'SELECT money,link FROM users_db WHERE user_id="{message.chat.id}"')
            info_db = data_db.fetchall()[0]
            rps =  multiple_replace(texts['profile'], {"0": str(info_db[0]), "None": info_db[1], "$": str(message.chat.id)})
            bot.send_message(mci, rps, parse_mode='MarkDown', reply_markup=main_menu)
        elif message.text == 'Ссылка📎':
            bot.send_message(mci, texts['link'],parse_mode='HTML', reply_markup=workspace)
        elif message.text == 'Наши чаты💌':
            bot.send_message(mci, texts['chat'],parse_mode='HTML', reply_markup=chats_link)
            bot.send_message(mci, 'Ждем тебя в чатах!',parse_mode='HTML', reply_markup=main_menu)
        elif message.text == 'Настройки⚙️':
            bot.send_message(mci, texts['settings'],parse_mode='HTML', reply_markup=setting_menu)
        elif message.text == 'Назад⬅️':
            bot.send_message(mci, 'Вы в главном меню💸', reply_markup=main_menu)
        elif message.text == 'Чат с мамонтами🦣':
            bot.send_message(mci, 'У вас 0 активных чатов🔴', reply_markup=main_menu)
        elif message.text == 'Добавить домен🔐':
            bot.send_message(mci, 'тут мне уже нужно сделать сайт сначала', reply_markup=main_menu)
        elif message.text == 'Рассылка🔥':
            bot.send_message(mci, 'Выберите режим рассылки', reply_markup=spam_settings)
        elif message.text == 'Текст📜':
            msg = bot.send_message(mci, 'Отправь мне текст для рассылки')
            bot.register_next_step_handler(msg, textovik)
        elif message.text == 'Картинка+Текст🖼':
            msg = bot.send_message(mci, 'Отправь мне картинку с текстом для рассылки')
            bot.register_next_step_handler(msg, kartinka)
        elif message.text == 'Картинку🖼':
            msg = bot.send_message(mci, 'Отправь мне картинку для рассылки')
            bot.register_next_step_handler(msg, kartinka_no_text)

        elif message.text == 'Добавить админа👨🏻‍🔧':
            msg = bot.send_message(mci, 'Отправь мне юзернейм пользователя без @')
            bot.register_next_step_handler(msg, add_adm_func)
        
            msg = bot.send_message(mci, 'Отправь мне юзернейм пользователя без @')
        elif message.text == 'Удалить админа💀':
            bot.register_next_step_handler(msg, del_adm_func)

        elif message.text == 'Забанить пользователя💩':
            msg = bot.send_message(mci, 'Отправь мне юзернейм пользователя без @')
            bot.register_next_step_handler(msg, ban_func)
        
        elif message.text == 'CRYPTOLIR':
            bot.send_message(mci, f'Ваша ссылка:\n\n`https://CRYPTOLIR?rel={message.chat.id}`', reply_markup=main_menu, parse_mode='MarkDown')
            c.execute(f"""UPDATE users_db SET link = 'https://CRYPTOLIR?rel={message.chat.id}' WHERE user_id = '{message.chat.id}' """)
            conn.commit()

        elif message.text == 'Дать денег💸':
            msg = bot.send_message(mci, 'Отправь мне юзернейм пользователя без @ и сумму в рублях \n\n(grimeca 100)')
            bot.register_next_step_handler(msg, add_money_func)

        elif message.text == 'Забрать денег🪦':
            msg = bot.send_message(mci, 'Отправь мне юзернейм пользователя без @ и сумму в рублях \n\n(grimeca 100)')
            bot.register_next_step_handler(msg, del_money_func)
        
        elif message.text == 'Заказать выплату💰':
            user_money_find = c.execute(f"SELECT money FROM users_db WHERE user_id='{message.chat.id}'")
            user_money_check = user_money_find.fetchall()[0][0]
            if int(user_money_check) != 0:
                msg = bot.send_message(mci, f'У вас {user_money_check} рублей, сколько вы хотите снять?')
                bot.register_next_step_handler(msg, viplata)
            else:
                bot.send_message(mci, 'У вас 0 рублей вы не можете заказать выплату')
    else:
        pass

bot.infinity_polling()
conn.close()