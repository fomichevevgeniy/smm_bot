import schedule
from telebot import TeleBot
from telebot.types import Message, CallbackQuery
from telebot.types import ReplyKeyboardRemove
import time
from telebot.apihelper import ApiTelegramException
from datetime import datetime

from configs import *
from keyboards import *
from queries import *

# -------------------------------------------------------------------------------------------

bot = TeleBot(TOKEN, parse_mode='HTML')


@bot.message_handler(commands=['start'])
def command_start(message: Message):
    user_id = message.from_user.id
    users = get_all_users_ids()
    if user_id == ADMIN_ID:
        admin()
    elif user_id in users:
        bot.send_message(user_id, f"Hurmatli foydalanuvchi siz ushbu botdan ro`yxatdan o`tgansiz"
                                  f"BEPUL SMM VEBINARINI ushbu havola orqali ko`ra olasiz !")
        send_url_webinar(message)
    else:
        bot.send_message(user_id,
                         '<b>📲 Assalomu Alaykum. BEPUL SMM VEBINARINI ko`rish uchun ro`yxatdan o`ting !</b>')
        ask_full_name(message)


# --------------------------------------------------------------------------------------------
# Registration

def ask_full_name(message: Message):
    user_id = message.from_user.id
    msg = bot.send_message(user_id, '<b>Ism, Familyangiz:</b>')
    bot.register_next_step_handler(msg, ask_age)


def ask_age(message: Message):
    user_id = message.from_user.id
    full_name = message.text
    msg = bot.send_message(user_id, '<b>Yoshingiz:</b>')
    bot.register_next_step_handler(msg, ask_contact, full_name)


def ask_contact(message: Message, full_name):
    user_id = message.from_user.id
    age = message.text
    msg = bot.send_message(user_id,
                           '📲 <b>Siz bilan bog`lanish uchun telefon raqamingiz:</b>',
                           reply_markup=generate_ask_contact())
    bot.register_next_step_handler(msg, ask_address, full_name, age)


def ask_address(message: Message, full_name, age):
    user_id = message.from_user.id
    if message.content_type == 'contact':
        contact = message.contact.phone_number
    elif message.content_type == 'text':
        contact = message.text
    msg = bot.send_message(user_id, f"""📍 <b>Yashash manzilingiz:
Masalan: Toshkent, Chilonzor.</b>""",
                           reply_markup=ReplyKeyboardRemove())
    bot.register_next_step_handler(msg, ask_reason_smm, full_name, age, contact)


def ask_reason_smm(message: Message, full_name, age, contact):
    user_id = message.from_user.id
    address = message.text
    msg = bot.send_message(user_id, '<b>Nima maqsadda SMM ni o`rganmoqchisiz ?</b>')
    bot.register_next_step_handler(msg, show_data, full_name, age, contact, address)


def show_data(message: Message, full_name, age, contact, address):
    user_id = message.from_user.id
    reason = message.text
    bot.send_message(user_id, '<b>Ma`lumotlaringizni tasdiqlang !</b>')
    msg = bot.send_message(user_id, f"""<b>Ism, Familya:</b> <i>{full_name}</i>
<b>Yoshingiz:</b> <i>{age}</i>
<b>Telefon raqamingiz:</b> <i>{contact}</i>
<b>Yashash manzilingiz:</b> <i>{address}</i>
<b>SMM ni o`rganishdan maqsadingiz:</b> <i>{reason}</i>""",
                           reply_markup=generate_yes_not())
    bot.register_next_step_handler(msg, submitting_user_data, full_name, age, contact, address, reason)


def submitting_user_data(message: Message, full_name, age, contact, address, reason):
    user_id = message.from_user.id
    if message.text == 'Ha ✅':
        insert_user(telegram_id=user_id,
                    full_name=full_name,
                    age=age,
                    contact=contact,
                    address=address,
                    reason=reason)
        bot.send_message(REGISTER_CHANNEL_ID, f"""<b>Ism, Familya:</b> <i>{full_name}</i>
<b>Yoshingiz:</b> <i>{age}</i>
<b>Telefon raqamingiz:</b> <i>{contact}</i>
<b>Yashash manzilingiz:</b> <i>{address}</i>
<b>SMM ni o`rganishdan maqsadingiz:</b> <i>{reason}</i>""")
        bot.send_message(REGISTER_CHANNEL_ID, f"Ro`yxatga olindi ✅✅✅")
        bot.send_message(user_id, f"<b>{full_name} tabriklaymiz, Siz muvofaqqiyatli ro`yxatdan o`tdingiz </b>🥳",
                         reply_markup=ReplyKeyboardRemove())
        send_url_webinar(message)

    elif message.text == 'Yo`q ❌':
        command_start(message)


# --------------------------------------------------------------------------------------------------------
def send_url_webinar(message: Message):
    user_id = message.from_user.id
    bot.send_message(user_id, "<b>BEPUL VEBINARNI ushbu havola orqali ko'rishingiz mumkin 😊</b>")
    bot.send_message(user_id, 'https://youtu.be/iMU-at_CUec', protect_content=True)
    time.sleep(1800)
    ask_for_seeing_webinar(message)


def ask_for_seeing_webinar(message: Message):
    user_id = message.from_user.id
    bot.send_message(user_id, "<b>VEBINARNI ko`rdingizmi ? </b>🤔")
    msg = bot.send_message(user_id, f"""<b>Agar ko`rgan bo`lsangiz, o`z fikringizni jo`nating.
VEBINAR sizga yoqtimi ?</b>""",
                           reply_markup=webinar_reactions())
    bot.register_next_step_handler(msg, thanks_for_reactions)


def thanks_for_reactions(message: Message):
    user_id = message.from_user.id
    user = get_user_data(user_id)
    reaction = message.text

    bot.send_message(FEEDBACK_CHANNEL_ID, f"""
<b>Ushbu o`quvchi fikrini bildirdi 😁😁😁</b>
<b>Ism, Familya:</b> <i>{user[2]}</i>
<b>Telefon raqami:</b> <i>{user[4]}</i>
<b>REACTION:</b> <i>{reaction}</i>""")

    msg = bot.send_message(user_id, "<b>Fikringiz uchun raxmat 😍</b>",
                           reply_markup=generate_vaucher())
    bot.register_next_step_handler(msg, send_sale)


def send_sale(message: Message):
    user_id = message.from_user.id
    user = get_user_data(user_id)
    bot.send_message(user_id, f"""<b>Hurmatli <i>{user[2]}</i> !
Tabriklaymiz siz 1 000 000 so`mlik vaucherga ega bo`ldingiz 🎉🎉🎉</b>""",
                     reply_markup=ReplyKeyboardRemove())
    bot.send_photo(user_id, VAUCHER_ID, protect_content=True)

    bot.send_message(SALE_CHANNEL_ID, f"""<b>Ism, Familya:</b> <i>{user[2]}</i>
<b>Telefon raqami:</b> <i>{user[4]}</i>
<b>VAUCHERGA ega bo'ldi ✅✅✅</b>""")

    time.sleep(10)

    ask_students_results(message)


def ask_students_results(message: Message):
    user_id = message.from_user.id
    msg = bot.send_message(user_id,
                           "<b>Bizning o'quvchilarimiz qanday natijalarga erishishyabti Sizga qiziqmi</b> ⁉️💰",
                           reply_markup=student_results_reactions())
    bot.register_next_step_handler(msg, send_students_results)


def send_students_results(message: Message):
    user_id = message.from_user.id

    bot.send_video(user_id, FEEDBACK_1, reply_markup=ReplyKeyboardRemove())

    bot.send_video(user_id, FEEDBACK_2)

    bot.send_message(user_id, "Vaqtingizni ayamasdan videolarni albatta ko`rishingizni maslaxat beramiz ☺")


# -------------------------------------------------------------------------------------------
def admin():
    bot.send_message(ADMIN_ID, 'RASSILKA turini tanlang !',
                     reply_markup=generate_rassilka())


@bot.message_handler(func=lambda message: message.text == "Text 📜" and message.from_user.id == ADMIN_ID)
def ask_text_rassilka(message: Message):
    user_id = message.from_user.id
    msg = bot.send_message(user_id, "'Text 📜' rassilka uchun 'TEXT' yozib jo'nating !")
    bot.register_next_step_handler(msg, send_text_rassilka)


def send_text_rassilka(message: Message):
    users = get_all_users_ids()
    text = message.text
    for user_id in users:
        try:
            bot.send_message(user_id, text)
        except ApiTelegramException:
            continue
    bot.send_message(ADMIN_ID, "SMS habarnomalar barchaga jo`natildi ✅✅✅")
    admin()


@bot.message_handler(func=lambda message: message.text == "Rasm 🖼" and message.from_user.id == ADMIN_ID)
def ask_image_rassilka(message: Message):
    user_id = message.from_user.id
    msg = bot.send_message(user_id, "'Rasm 🖼' rassilka uchun 'RASM' jo'nating !")
    bot.register_next_step_handler(msg, send_image_rassilka)


def send_image_rassilka(message: Message):
    users = get_all_users_ids()
    image_id = message.photo[-1].file_id
    for user_id in users:
        try:
            bot.send_photo(user_id, image_id)
        except ApiTelegramException:
            continue
    bot.send_message(ADMIN_ID, "RASM habarnomalar barchaga jo`natildi ✅✅✅")
    admin()


@bot.message_handler(func=lambda message: message.text == "Video 🎞" and message.from_user.id == ADMIN_ID)
def ask_video_rassilka(message: Message):
    user_id = message.from_user.id
    msg = bot.send_message(user_id, "'Video 🎞' rassilka uchun 'VIDEO' jo'nating ! "
                                    "VIDEO hajmi 50mb dan oshmasin !")
    bot.register_next_step_handler(msg, send_video_rassilka)


def send_video_rassilka(message: Message):
    users = get_all_users_ids()

    video_id = message.video.file_id
    for user_id in users:
        try:
            bot.send_video(user_id, video_id)
        except ApiTelegramException:
            continue
    bot.send_message(ADMIN_ID, "RASM habarnomalar barchaga jo`natildi ✅✅✅")
    admin()


@bot.message_handler(func=lambda message: message.text == "Rasm 🖼 + Text 📜" and message.from_user.id == ADMIN_ID)
def ask_image_text_rassilka(message: Message):
    msg = bot.send_message(ADMIN_ID, "'RASM 🖼 + TEXT 📜' rassilka uchun 'RASM' jo'nating !",
                           reply_markup=ReplyKeyboardRemove())
    bot.register_next_step_handler(msg, ask_text_image_rassilka)


def ask_text_image_rassilka(message: Message):
    user_id = message.from_user.id
    image_id = message.photo[-1].file_id
    msg = bot.send_message(user_id, "'RASM 🖼 + TEXT 📜' rassilka uchun 'TEXT' jo'nating !")
    bot.register_next_step_handler(msg, send_image_text_rassilka, image_id)


def send_image_text_rassilka(message: Message, image_id):
    users = get_all_users_ids()
    text = message.text
    try:
        for user_id in users:
            try:
                bot.send_photo(user_id, image_id, caption=text)
            except ApiTelegramException:
                continue
        bot.send_message(ADMIN_ID, "RASM habarnomalar barchaga jo`natildi ✅✅✅")
        admin()
    except:
        bot.send_message(ADMIN_ID, "Nimadir hatolik ketti qaytadan urinib ko`ring 😢")


@bot.message_handler(func=lambda message: message.text == "Video 🎞 + Text 📜" and message.from_user.id == ADMIN_ID)
def ask_video_text_rassilka(message: Message):
    user_id = message.from_user.id
    msg = bot.send_message(user_id, "'Video 🎞 + Text 📜' rassilka uchun 'VIDEO' jo'nating !",
                           reply_markup=ReplyKeyboardRemove())
    bot.register_next_step_handler(msg, ask_text_video_rassilka)


def ask_text_video_rassilka(message: Message):
    user_id = message.from_user.id
    video_id = message.video.file_id
    msg = bot.send_message(user_id, "'Video 🎞 + Text 📜' rassilka uchun 'TEXT' yozib jo'nating !")
    bot.register_next_step_handler(msg, send_video_text_rassilka, video_id)


def send_video_text_rassilka(message: Message, video_id):
    users = get_all_users_ids()
    text = message.text
    try:
        for user_id in users:
            try:
                bot.send_video(user_id, video_id, caption=text)
            except ApiTelegramException:
                continue
        bot.send_message(ADMIN_ID, "RASM habarnomalar barchaga jo`natildi ✅✅✅")
        admin()
    except:
        bot.send_message(ADMIN_ID, "Nimadir hatolik ketti qaytadan urinib ko`ring 😢")


bot.infinity_polling()
