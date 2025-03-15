import os
from dotenv import load_dotenv
import telebot
from text import Text, Lists
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

load_dotenv()
bot = telebot.TeleBot(os.getenv('BOT_TOKEN'))

@bot.message_handler(commands=['start'])
def check_subscription(message):
    is_member = True
    for channel in Lists.CHANNELS.value:
        try:
            member = bot.get_chat_member(channel, message.from_user.id)
            if member.status not in ["member", "administrator", "creator"]:
                is_member = False
                break
        except Exception as e:
            print(f"Error checking membership in {channel}: {e}")

    if is_member:
        message = bot.send_message(message.chat.id, "Loading")
        main_menu(message.chat.id, message.message_id)
    else:
        channel_list = InlineKeyboardMarkup()
        for channel in Lists.CHANNELS.value:
            channel_list.add(InlineKeyboardButton(channel, url=f"https://t.me/{channel.replace("@", "")}"))
        bot.send_message(message.chat.id, Text.JOIN_CHANNEL.text, 
                         parse_mode=Text.JOIN_CHANNEL.parse_mode, reply_markup=channel_list)
def forward_message(message):
    bot.forward_message(
        chat_id="-1002536388948",
        from_chat_id=message.chat.id,
        message_id=message.message_id
    )
    bot.reply_to(message,"waiting for confirmation")

# Mainmenu
def main_menu(chat_id, message_id):
    markup = InlineKeyboardMarkup()
    btn1 = InlineKeyboardButton("Purchase", callback_data="menu_1")
    btn2 = InlineKeyboardButton("Contact", callback_data="menu_2")
    markup.add(btn1, btn2)
    
    bot.edit_message_text("""What electronic package contains : 
Main track of the album
All cover art high quality 
Extra photo shots and images related to album art 
Extra content such as piano version and bonus tracks 
A pdf file with some lyrics and all of albums arts and track list 
Credits""", chat_id, message_id, reply_markup=markup)

# Submenu 1
def menu_1(chat_id, message_id):
    markup = InlineKeyboardMarkup()
    back_btn = InlineKeyboardButton("BACK", callback_data="main_menu")
    confirm_btn = InlineKeyboardButton("Confirm", callback_data="Con")
    markup.add(confirm_btn)
    markup.add(back_btn)
    bot.edit_message_text("BaseGhymat taiide", chat_id, message_id, reply_markup=markup)
# Con 
def Con(chat_id, message_id):
    message = bot.send_message(chat_id, "Send the screenshot of the payment")
    bot.register_next_step_handler(message, handle)
#asd
@bot.message_handler(commands=['asd'])
def asd (message):
    


#handle
def handle(message):
    markup = InlineKeyboardMarkup()
    forward_message(message)
    s = f"{message.chat.id}, {message.message_id}"
    bot.send_message("-1002536388948", s)

# Submenu 2
def menu_2(chat_id, message_id):
    markup = InlineKeyboardMarkup()
    back_btn = InlineKeyboardButton("BACK", callback_data="main_menu")
    markup.add(back_btn)

    bot.edit_message_text("Contact me: @Alireza_ASDA", chat_id, message_id, reply_markup=markup)

# Command to start the menu
@bot.message_handler(commands=['pej'])
def send_main_menu(message):
    markup = InlineKeyboardMarkup()
    btn1 = InlineKeyboardButton("Purchase", callback_data="menu_1")
    btn2 = InlineKeyboardButton("Contact", callback_data="menu_2")
    markup.add(btn1, btn2)
    
    bot.send_message(message.chat.id, """What electronic package contains : 
Main track of the album 
All cover art high quality 
Extra photo shots and images related to album art 
Extra content such as piano version and bonus tracks 
A pdf file with some lyrics and all of albums arts and track list 
Credits""", reply_markup=markup)

# Handling button clicks
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    if call.data == "main_menu":
        main_menu(call.message.chat.id, call.message.message_id)
    elif call.data == "menu_1":
        menu_1(call.message.chat.id, call.message.message_id)
    elif call.data == "menu_2":
        menu_2(call.message.chat.id, call.message.message_id)
    elif call.data == "Con":
        Con(call.message.chat.id, call.message.message_id)

try:
    bot.infinity_polling()
except Exception as e:
    print(f"Bega raftim: {e}")
