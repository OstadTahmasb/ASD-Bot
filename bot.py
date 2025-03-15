import os
from dotenv import load_dotenv
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

load_dotenv()
bot = telebot.TeleBot(os.getenv('BOT_TOKEN'))

lala_channel = "-1002536388948"
join_channel_list = ["@AlirezaASDbeat"]

@bot.message_handler(commands=['start'])
def check_subscription(message):
    is_member = True
    for channel in join_channel_list:
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
        for channel in join_channel_list:
            channel_list.add(InlineKeyboardButton(channel, url=f"https://t.me/{channel.replace("@", "")}"))
        bot.send_message(message.chat.id, "برای حمایت از آلبوم لطفا در چنل عضو شوید.\nبعد از جوین شدن مجددا بات را استارت کنید.", reply_markup=channel_list)

def forward_message(message):
    bot.forward_message(
        chat_id="-1002536388948",
        from_chat_id=message.chat.id,
        message_id=message.message_id
    )

# Mainmenu
def main_menu(chat_id, message_id):
    markup = InlineKeyboardMarkup()
    btn1 = InlineKeyboardButton("حمایت", callback_data="menu_1")
    btn2 = InlineKeyboardButton("Contact", callback_data="menu_2")
    markup.add(btn1)
    markup.add(btn2)
    
    bot.edit_message_text("""سلام و درود
 با خرید این آلبوم از آرتیست حمایت کردید و جهت تشکر از شما پکیج الکترونیک با محتوایی اضافه بر آنچه در چنل تلگرام یا ساندکلاد موجود هست دریافت میکنید که در ادامه لیست این محتوا نوشته شده. پرداخت به شکل کارت به کارت و ارسال فیش بانک صورت میگیره و بعد از تایید ساعاتی قبل از پخش برای شما ایمیل میشه. حداقل مبلغ 100 هزار تومن در نظر گرفته شده اما اگر به حمایت بیشتر تمایل داشتین میتونین بیشتر پرداخت کنین. 

پکیج الکترونیک آلبوم شامل موارد زیر است:
فایل ترک های اصلی آلبوم 
فایل با کیفیت تمام کاور آرت های آلبوم 
16 فوتو شات اضافه هماهنگ با فضا و تم ترک ها
یک دفترچه(pdf) شامل ترک لیست و کاور آرت ها و متن ها و تصاویر هماهنگ با فضای هر ترک و کل آلبوم(جهت درک عمیق تر فضای هنری ترک ها)
محتوای اضافه از جمله یک ترک اضافه + یسری سوپرایز :)
کردیت ها

برای حمایت گزینه پرداخت رو بزنید 
اگر هرگونه سوال یا ایراد وجود داشت گزینه contact رو بزنید""", chat_id, message_id, reply_markup=markup)

# Submenu 1
def menu_1(chat_id, message_id):
    markup = InlineKeyboardMarkup()
    back_btn = InlineKeyboardButton("بازگشت", callback_data="main_menu")
    confirm_btn = InlineKeyboardButton("تایید و ارسال تصویر رسید", callback_data="Con")
    markup.add(confirm_btn)
    markup.add(back_btn)
    bot.edit_message_text("""حداقل مبلغ پرداختی: 100 هزار تومن
`6274121207587106`
علیرضا بیاتی
حتما اسکرین شات یا تصویر رسید پرداخت رو سیو کنید""", chat_id, message_id, reply_markup=markup, parse_mode="Markdown")

#asd
@bot.message_handler(commands=['asd'])
def asd (message):
    if message.from_user.id == 395256157:
        msg = bot.send_message(message.chat.id, "Chat Id:")
        bot.register_next_step_handler(msg, asd_chat_id)

def asd_chat_id(message):
    chat_id = message.text
    msg = bot.send_message(message.chat.id, "Send custom confirmation:")
    bot.register_next_step_handler(msg, asd_confirm, chat_id)

def asd_confirm(message, chat_id):
    bot.send_message(chat_id, "با تشکر از حمایت شما\nپیام زیر توسط آرتیست برای قدردانی از شما نوشته شده است:\n" + message.text)

# Con 
def Con(chat_id, message_id):
    message = bot.send_message(chat_id, "لطفا تصویر رسید خود را ارسال کنید:")
    bot.register_next_step_handler(message, get_payment)

#handle
def get_payment(message):
    forward_message(message)
    s = f"`{message.chat.id}`\n@{message.from_user.username}"
    bot.send_message("-1002536388948", s, parse_mode="Markdown")
    bot.send_message(message.chat.id, "ایمیل خود را ارسال کنید")
    bot.register_next_step_handler(message, get_email)

def get_email(message):
    forward_message(message)
    bot.send_message(message.chat.id, "اطلاعات شما دریافت شد.\nدر انتظار تایید پرداخت\nپس از تایید از طریق همین بات به شما اطلاع داده خواهد شد.")

# Submenu 2
def menu_2(chat_id, message_id):
    markup = InlineKeyboardMarkup()
    back_btn = InlineKeyboardButton("بازگشت", callback_data="main_menu")
    markup.add(back_btn)

    bot.edit_message_text("Contact me: @Alireza_ASDA", chat_id, message_id, reply_markup=markup)

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
