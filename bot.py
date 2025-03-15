import os
from dotenv import load_dotenv
import telebot
from text import Text, Lists
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

load_dotenv()
bot = telebot.TeleBot(os.getenv('BOT_TOKEN'))

@bot.message_handler(commands=['start'])
def check_subscription(message):
    is_member = False
    for channel in Lists.CHANNELS.value:
        try:
            member = bot.get_chat_member(channel, message.from_user.id)
            if member.status not in ["member", "administrator", "creator"]:
                is_member = False
                break
        except Exception as e:
            print(f"Error checking membership in {channel}: {e}")

    if is_member:
        main_menu(message)
    else:
        channel_list = InlineKeyboardMarkup()
        for channel in Lists.CHANNELS.value:
            channel_list.add(InlineKeyboardButton(channel, url=f"https://t.me/{channel.replace("@", "")}"))
        bot.send_message(message.chat.id, Text.JOIN_CHANNEL.text, 
                         parse_mode=Text.JOIN_CHANNEL.parse_mode, reply_markup=channel_list)

# Main menu function
def main_menu(chat_id, message_id):
    markup = InlineKeyboardMarkup()
    btn1 = InlineKeyboardButton("Go to Menu 1", callback_data="menu_1")
    btn2 = InlineKeyboardButton("Go to Menu 2", callback_data="menu_2")
    markup.add(btn1, btn2)
    
    bot.edit_message_text("🏠 Main Menu:\nChoose an option:", chat_id, message_id, reply_markup=markup)

# Submenu 1
def menu_1(chat_id, message_id):
    markup = InlineKeyboardMarkup()
    back_btn = InlineKeyboardButton("🔙 Back to Main Menu", callback_data="main_menu")
    markup.add(back_btn)

    bot.edit_message_text("📜 This is Menu 1.\nClick below to go back.", chat_id, message_id, reply_markup=markup)

# Submenu 2
def menu_2(chat_id, message_id):
    markup = InlineKeyboardMarkup()
    back_btn = InlineKeyboardButton("🔙 Back to Main Menu", callback_data="main_menu")
    markup.add(back_btn)

    bot.edit_message_text("📜 This is Menu 2.\nClick below to go back.", chat_id, message_id, reply_markup=markup)

# Command to start the menu
@bot.message_handler(commands=['pej'])
def send_main_menu(message):
    markup = InlineKeyboardMarkup()
    btn1 = InlineKeyboardButton("Go to Menu 1", callback_data="menu_1")
    btn2 = InlineKeyboardButton("Go to Menu 2", callback_data="menu_2")
    markup.add(btn1, btn2)
    
    bot.send_message(message.chat.id, "🏠 Main Menu:\nChoose an option:", reply_markup=markup)

# Handling button clicks
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    if call.data == "main_menu":
        main_menu(call.message.chat.id, call.message.message_id)
    elif call.data == "menu_1":
        menu_1(call.message.chat.id, call.message.message_id)
    elif call.data == "menu_2":
        menu_2(call.message.chat.id, call.message.message_id)


try:
    bot.infinity_polling()
except Exception as e:
    print(f"Bega raftim: {e}")
