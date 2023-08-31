from telebot.types import ReplyKeyboardMarkup, KeyboardButton


def generate_ask_contact():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    btn_ask_contact = KeyboardButton(text='Telefon raqamni jo`natish 📲', request_contact=True)
    markup.add(btn_ask_contact)
    return markup


def generate_yes_not():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn_submit = KeyboardButton(text='Ha ✅')
    btn_unsubmit = KeyboardButton(text='Yo`q ❌')
    markup.add(btn_submit, btn_unsubmit)
    return markup


def generate_rassilka():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    btn_text = KeyboardButton(text='Text 📜')
    btn_image = KeyboardButton(text='Rasm 🖼')
    btn_video = KeyboardButton(text='Video 🎞')
    btn_image_text = KeyboardButton(text='Rasm 🖼 + Text 📜')
    btn_video_text = KeyboardButton(text='Video 🎞 + Text 📜')
    markup.row(btn_image_text)
    markup.row(btn_video_text)
    markup.row(btn_text, btn_image, btn_video)
    return markup


def webinar_reactions():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    btn_yes = KeyboardButton(text="Xa, albatta 🚀")
    btn_no = KeyboardButton(text="Hali ko'rishga ulgurmadim 😕")
    btn_negative = KeyboardButton(text="Unchalik emas 🤏")
    markup.row(btn_yes)
    markup.row(btn_no, btn_negative)
    return markup


def student_results_reactions():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    btn_yes = KeyboardButton(text="Albatta qiziq 💰🚀")
    btn_no = KeyboardButton(text="Xa 🔥")
    btn_negative = KeyboardButton(text="Unchalik emas 🤏")
    markup.row(btn_yes)
    markup.row(btn_no, btn_negative)
    return markup


def generate_sale():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    btn_sale = KeyboardButton(text="Chegirma narxida harid qilish 😎")
    markup.row(btn_sale)
    return markup


def generate_vaucher():
    markup = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    vaucher_btn = KeyboardButton(text="VAUCHERGA ega bo`lish 💵")
    markup.add(vaucher_btn)
    return markup