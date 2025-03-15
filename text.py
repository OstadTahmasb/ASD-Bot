from enum import Enum

class Text(Enum):
    def __init__(self, text, parse_mode="Markdown"):
        self.text = text
        self.parse_mode = parse_mode

    # joined in channel and access granted to bot
    START = "سلام داپش"

    # not joined in channels
    JOIN_CHANNEL = "تو چنل جوین نیستی که کیری برو بعدا بیا دوباره استارت کن"

class Lists(Enum):
    CHANNELS = [
        "@AlirezaASDbeat",
    ]
    MAIN_MENU_BUTTONS = [
        {
            "text": "kir mikham",
            "callback_data": "kir",
        },
        {
            "text": "حمایت از آرتیست",
            "callback_data": "support",
        },
        {
            "text": "درباره آلبوم",
            "callback_data": "about",
        },
        {
            "text": "خرید آلبوم",
            "callback_data": "purchase",
        },
        {
            "text": "پروفایل",
            "callback_data": "profile",
        },
    ]