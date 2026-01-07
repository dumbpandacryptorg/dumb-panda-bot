#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🤖 DUMB PANDA TELEGRAM BOT - FULL VERSION
با تمام مراحل، بازی‌ها، رفرال و سیستم جدول امتیاز
"""

import os
import json
import re
import sys
import random

try:
    import telebot
    from telebot import types
except ImportError:
    print("❌ خطا: telebot نصب نیست!")
    sys.exit(1)

try:
    from flask import Flask, request
except ImportError:
    print("❌ خطا: Flask نصب نیست!")
    sys.exit(1)

# ========== تنظیمات ==========
BOT_TOKEN = os.getenv("BOT_TOKEN", "توکن_ربات_تو")
BOT_USERNAME = os.getenv("BOT_USERNAME", "DumbPandaBot")
DOMAIN = os.getenv("DOMAIN", "https://yourdomain.com")

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)
# ========== لینک‌ها ==========
CONTRACT_ADDRESS = "0xa6c916065c49672247908d1148506220fd28c065"
LIQUIDITY_POOL_ADDRESS = "0x66f9986ab66186740531781c1ba01229bec1a1fd"

BSC_SCAN_TOKEN_URL = f"https://bscscan.com/token/{CONTRACT_ADDRESS}"
BSC_SCAN_CONTRACT_URL = f"https://bscscan.com/address/{CONTRACT_ADDRESS}"
DEXTOOLS_TOKEN_URL = f"https://www.dextools.io/app/bnb/pair-explorer/{LIQUIDITY_POOL_ADDRESS}"
PANCAKESWAP_SWAP_URL = f"https://pancakeswap.finance/swap?outputCurrency={CONTRACT_ADDRESS}"
TELEGRAM_CHANNEL_URL = "https://t.me/dumbpandacryptochanel"
INSTAGRAM_URL = "https://www.instagram.com/dumb_panda_token"

# ========== تصاویر ==========
IMG_WELCOME = "https://i.ibb.co/zWpY5dfC/Chat-GPT-Image-Dec-22-2025-05-56-57-PM.png"
IMG_CONTRACT = "https://img.sanishtech.com/u/02231c9b23f59c47c20be45189898e90.png"
IMG_LIQUIDITY = "https://i.ibb.co/F43R2fsX/Chat-GPT-Image-Dec-22-2025-04-54-47-PM.png"
IMG_LISTING = "https://i.ibb.co/d0Gx8VGQ/global-listing-telegram-1365x2048.png"
IMG_AIRDROP = "https://i.ibb.co/N6QpVfgR/Chat-GPT-Image-Dec-22-2025-05-54-18-PM.png"
IMG_TASKS = "https://i.ibb.co/CCXRjD8/517a4540-c8a0-4ed3-aabe-cdaf67e2e627.png"
IMG_WALLET = "https://i.ibb.co/tTcqkPMW/wallet-telegram-1365x2048-1.png"
IMG_FINAL = "https://img.sanishtech.com/u/5c68e53ccef70816f1577d5b84c9380d.png"
IMG_GAME1 = "https://i.ibb.co/game1.jpg"  # عکس بازی 1
IMG_GAME2 = "https://i.ibb.co/game2.jpg"  # عکس بازی 2
# ========== ذخیره‌سازی کاربران ==========
class UserStorage:
    def __init__(self):
        self.data_dir = "data"
        os.makedirs(self.data_dir, exist_ok=True)
        self.users_file = os.path.join(self.data_dir, "users.json")
        self.users = self._load_users()
    
    def _load_users(self):
        if not os.path.exists(self.users_file):
            return {}
        try:
            with open(self.users_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}
    
    def _save_users(self):
        try:
            with open(self.users_file, 'w', encoding='utf-8') as f:
                json.dump(self.users, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"⚠️ خطا در ذخیره کاربران: {e}")
    
    def get_user(self, user_id):
        uid = str(user_id)
        if uid not in self.users:
            self.users[uid] = {
                "lang": "fa",
                "stage": 0,
                "wallet": None,
                "awaiting_wallet": False,
                "points": 0,
                "referrals": 0
            }
            self._save_users()
        return self.users[uid]
    
    def update_user(self, user_id, data):
        user = self.get_user(user_id)
        user.update(data)
        self._save_users()
        return user

storage = UserStorage()
# ========== مراحل و سیستم اصلی ==========
STAGES = [
    # مرحله ۰: انتخاب زبان
    {
        "key": "language",
        "img": IMG_WELCOME,
        "caption_fa": "🌍 لطفاً زبان خود را انتخاب کنید:",
        "caption_en": "🌍 Please select your language:"
    },
    # مرحله ۱: خوش‌آمدگویی
    {
        "key": "welcome",
        "img": IMG_WELCOME,
        "caption_fa": "🐼 سلام! من دامب پاندا هستم.\n\nهمین الان می‌تونی ثبت‌نام کنی و سهمت رو از ایردراپ‌های پیش‌رو تضمین کنی.\nتو پست های بعدی بیشتر با هم آشنا میشیم…\nو جایزه‌هامون هم گرم‌تر می‌شه! 🎁\n\nآماده‌ای؟\n→ ثبت نام کن!",
        "caption_en": "🐼 Hey! I'm Dumb Panda.\n\nRegister now to secure your spot for upcoming airdrops.\nIn the next messages, we'll get to know each other better…\nAnd trust me — rewards will only get hotter! 🔥\n\nReady?\n→ Sign up now!"
    },
    # مرحله ۲: قرارداد
    {
        "key": "contract",
        "img": IMG_CONTRACT,
        "caption_fa": "🐼 دامب پاندا (DMP) — توکنی که همه چیزش رو می‌بینی!\n\n✅ وریفای شده و استعلام — قرارداد هوشمند ما کاملاً روی بلاکچین قابل بررسی است و هر کسی می‌تونه مستقیماً بررسی کند.\n\n💰 اولین بار در دنیای کریپتو: با DMP می‌تونی تا ۳ برابر موجودیت وام بگیری — بدون ضامن، بدون سرور، فقط با کد!\n\n🎁 ۱۵٪ ایردراپ قفل شده است — فقط زمانی که شما شرایط را برآورده کنید، آزاد می‌شود.\n\n🔐 همه چیز در قرارداد نوشته شده — هیچ چیز پنهانی نیست.",
        "caption_en": "🐼 Dumb Panda (DMP) — a token where everything is visible!\n\n✅ Verified & auditable — our smart contract is fully on-chain and publicly inspectable by anyone.\n\n💰 First in crypto: with DMP, you can borrow up to 3x your wallet balance — no collateral, no servers, just code!\n\n🎁 15% airdrop is locked — released only when you meet conditions.\n\n🔐 Everything is written in code — no hidden clauses."
    },
    # مرحله ۳: نقدینگی
    {
        "key": "liquidity",
        "img": IMG_LIQUIDITY,
        "caption_fa": "🔐 دامب پاندا (DMP) — نقدینگی قفل‌شده، ارزش پایدار\n\n✅ این یک پروژه \"صفر شونده\" نیست.\nتوکن DMP با ساختاری هوشمند طراحی شده:\nهمه ارزش توکن در قرارداد قفل شده — نه برای فرار، بلکه برای پایداری و اعتماد.\n\n🎯 ما اینجا برای ماندگاری هستیم — نه برای یه پرش سریع و فرار.",
        "caption_en": "🔐 Dumb Panda (DMP) — locked liquidity, real value\n\n✅ This is not a \"rug-pull\" project.\nDMP is designed with long-term value:\nAll liquidity is locked — not to escape, but to ensure stability and trust.\n\n🎯 We're here for the long game — not a quick pump and dump."
    },
    # مرحله ۴: لیستینگ
    {
        "key": "listing",
        "img": IMG_LISTING,
        "caption_fa": "🌍 دامب پاندا (DMP) — پروژه جهانی با استانداردهای بالا\n\n✅ همه چیز با دقت صنعتی انجام شده است.\n📈 در حال حاضر در Binance، OKX، CoinMarketCap و دیگر شبکه‌ها لیست شده‌ایم.",
        "caption_en": "🌍 Dumb Panda (DMP) — a global project with professional standards\n\n✅ Every step executed with industry-grade precision.\n📈 Already listed on Binance, OKX, CoinMarketCap and more."
    },
    # مرحله ۵: ایردراپ
    {
        "key": "airdrop",
        "img": IMG_AIRDROP,
        "caption_fa": "💰 🐼 دامب پاندا: کیف پول رو آماده کن… جایزه‌ها شروع می‌شوند!\n\n🎁 اولین ایردراپت رو همین الان دریافت میکنی و می‌تونی برای دریافت وام ۳ برابر استفاده کنی.\n📈 مراحل بعدی = جایزه بیشتر = سود بیشتر!",
        "caption_en": "💰 🐼 Dumb Panda: Get your wallet ready — rewards are live!\n\n🎁 Claim your first airdrop now and use these tokens to borrow up to 3x your balance.\n📈 Next stages = bigger rewards = more profit!"
    },
    # مرحله ۶: تسک‌ها
    {
        "key": "tasks",
        "img": IMG_TASKS,
        "caption_fa": "🐼 دامب پاندا: کار + جایزه هست!\n\n✅ برای دریافت ایردراپ، چند کار ساده انجام بده:\n- فالو کردن تلگرام: [کانال](https://t.me/dumbpandacryptochanel)\n- فالو کردن اینستاگرام: [اینجا](https://www.instagram.com/dumb_panda_token)\n\n🎁 هر کاری = امتیاز بیشتر و ایردراپ بزرگ‌تر!",
        "caption_en": "🐼 Dumb Panda: Tasks + rewards!\n\n✅ Complete simple tasks to claim your airdrop:\n- Follow Telegram: [Channel](https://t.me/dumbpandacryptochanel)\n- Follow Instagram: [Here](https://www.instagram.com/dumb_panda_token)\n\n🎁 Each task = more points and bigger airdrop!"
    },
    # مرحله ۷: بازی‌ها و رفرال
    {
        "key": "games",
        "img": IMG_GAME1,
        "caption_fa": "🎮 بازی‌ها و دعوت دوستان\n\n✅ بازی اول: حدس عدد\n✅ بازی دوم: سنگ-کاغذ-قیچی\n\n🎯 دعوت هر ۳ نفر = ۳۰۰ امتیاز",
        "caption_en": "🎮 Games & referrals\n\n✅ Game 1: Guess the number\n✅ Game 2: Rock-paper-scissors\n\n🎯 Invite 3 friends = 300 points"
    },
    # مرحله ۸: کیف پول
    {
        "key": "wallet",
        "img": IMG_WALLET,
        "caption_fa": "🐼 دامب پاندا: آدرس والت رو بده… جایزه آماده‌ست!\n\n✅ با ارسال والت، DMP دریافت می‌کنی.",
        "caption_en": "🐼 Dumb Panda: Send your wallet address… reward is ready!\n\n✅ Send wallet to receive DMP."
    },
    # مرحله ۹: پایانی
    {
        "key": "final",
        "img": IMG_FINAL,
        "caption_fa": "🐼 دامب پاندا: ممنون که اومدی… جایزه‌ها به زودی می‌آید! 🌟",
        "caption_en": "🐼 Dumb Panda: Thank you for joining… rewards coming soon! 🌟"
    }
]
def get_keyboard(user_id, stage_idx):
    user = storage.get_user(user_id)
    lang = user["lang"]
    kb = types.InlineKeyboardMarkup()

    if stage_idx == 0:
        kb.row(
            types.InlineKeyboardButton("🇮🇷 فارسی", callback_data="setlang_fa"),
            types.InlineKeyboardButton("🇺🇸 English", callback_data="setlang_en")
        )
    elif stage_idx == 1:
        btn_text = "🔥 شروع" if lang == "fa" else "🔥 Start"
        kb.row(types.InlineKeyboardButton(btn_text, callback_data="stage_2"))
    elif stage_idx in [2,3,4,5,6,7]:
        back_text = "⬅️ قبلی" if lang=="fa" else "⬅️ Back"
        next_text = "➡️ بعدی" if lang=="fa" else "➡️ Next"
        kb.row(types.InlineKeyboardButton(back_text, callback_data=f"stage_{stage_idx-1}"),
               types.InlineKeyboardButton(next_text, callback_data=f"stage_{stage_idx+1}"))
        # لینک‌ها برای مراحل خاص
        if stage_idx==2:
            kb.row(types.InlineKeyboardButton("🧾 BscScan", url=BSC_SCAN_CONTRACT_URL))
        if stage_idx==3:
            kb.row(types.InlineKeyboardButton("🛒 PancakeSwap", url=PANCAKESWAP_SWAP_URL))
            kb.row(types.InlineKeyboardButton("📊 DEXTools", url=DEXTOOLS_TOKEN_URL))
        if stage_idx==6:
            kb.row(types.InlineKeyboardButton("📲 Telegram", url=TELEGRAM_CHANNEL_URL))
            kb.row(types.InlineKeyboardButton("📸 Instagram", url=INSTAGRAM_URL))
        if stage_idx==7:
            kb.row(types.InlineKeyboardButton("🎮 بازی اول", callback_data="game1"))
            kb.row(types.InlineKeyboardButton("🎮 بازی دوم", callback_data="game2"))
            kb.row(types.InlineKeyboardButton("📩 ارسال آدرس والت", callback_data="input_wallet"))
    elif stage_idx==8:
        back_text = "⬅️ قبلی" if lang=="fa" else "⬅️ Back"
        kb.row(types.InlineKeyboardButton(back_text, callback_data="stage_7"))
        kb.row(types.InlineKeyboardButton("📢 کانال را دنبال کنید", url=TELEGRAM_CHANNEL_URL))
    return kb

def send_stage(chat_id, user_id, stage_idx):
    if stage_idx<0: stage_idx=0
    if stage_idx>=len(STAGES): stage_idx=len(STAGES)-1

    user = storage.get_user(user_id)
    stage = STAGES[stage_idx]
    storage.update_user(user_id, {"stage": stage_idx})

    caption = stage["caption_fa"] if user["lang"]=="fa" else stage["caption_en"]
    reply_markup = get_keyboard(user_id, stage_idx)

    bot.send_photo(chat_id, stage["img"], caption=caption, reply_markup=reply_markup)
@bot.message_handler(commands=['start','help'])
def handle_start(message):
    user_id = message.from_user.id
    user = storage.get_user(user_id)
    if not user["lang"]:
        send_stage(message.chat.id, user_id, 0)
    else:
        send_stage(message.chat.id, user_id, 1)

@bot.callback_query_handler(func=lambda call: call.data.startswith("setlang_"))
def handle_language(call):
    lang = call.data.split("_")[1]
    storage.update_user(call.from_user.id, {"lang":lang})
    bot.answer_callback_query(call.id, "✅ زبان تغییر کرد" if lang=="fa" else "✅ Language changed")
    send_stage(call.message.chat.id, call.from_user.id, 1)

@bot.callback_query_handler(func=lambda call: call.data.startswith("stage_"))
def handle_stage(call):
    stage_num = int(call.data.split("_")[1])
    send_stage(call.message.chat.id, call.from_user.id, stage_num)
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda call: call.data=="input_wallet")
def handle_wallet(call):
    storage.update_user(call.from_user.id, {"awaiting_wallet": True})
    msg = "📌 لطفاً آدرس کیف پول خود را ارسال کنید:" if storage.get_user(call.from_user.id)["lang"]=="fa" else "📌 Please send your wallet address:"
    bot.send_message(call.message.chat.id, msg)
    bot.answer_callback_query(call.id)

@bot.message_handler(func=lambda m: storage.get_user(m.from_user.id).get("awaiting_wallet", False))
def handle_wallet_input(message):
    wallet = message.text.strip()
    user_id = message.from_user.id
    if re.match(r"^0x[a-fA-F0-9]{40}$", wallet):
        storage.update_user(user_id, {"wallet":wallet,"awaiting_wallet":False,"points":100})
        bot.send_message(message.chat.id,"✅ آدرس کیف پول ثبت شد!" if storage.get_user(user_id)["lang"]=="fa" else "✅ Wallet saved!")
        send_stage(message.chat.id, user_id, 8)
    else:
        bot.send_message(message.chat.id,"❌ آدرس نامعتبر است." if storage.get_user(user_id)["lang"]=="fa" else "❌ Invalid address.")
# بازی اول: حدس عدد
@bot.callback_query_handler(func=lambda call: call.data=="game1")
def game1(call):
    number = random.randint(1,5)
    storage.update_user(call.from_user.id, {"game1_number": number})
    bot.send_message(call.message.chat.id,"🎯 حدس بزن عدد بین 1 تا 5 چیه؟")
    bot.answer_callback_query(call.id)

@bot.message_handler(func=lambda m: storage.get_user(m.from_user.id).get("game1_number"))
def game1_guess(message):
    user_id = message.from_user.id
    number = storage.get_user(user_id).get("game1_number")
    try:
        guess = int(message.text)
        if guess==number:
            storage.update_user(user_id, {"points": storage.get_user(user_id)["points"]+50})
            bot.send_message(message.chat.id,"🎉 درست حدس زدی! +50 امتیاز")
        else:
            bot.send_message(message.chat.id,f"❌ اشتباه بود! عدد درست {number} بود.")
    except:
        bot.send_message(message.chat.id,"❌ لطفا عدد ارسال کن")
    storage.update_user(user_id, {"game1_number": None})

# بازی دوم: سنگ-کاغذ-قیچی
@bot.callback_query_handler(func=lambda call: call.data=="game2")
def game2(call):
    bot.send_message(call.message.chat.id,"🪨✂️📄 سنگ-کاغذ-قیچی! انتخاب کن: سنگ، کاغذ یا قیچی")
    storage.update_user(call.from_user.id, {"game2_active": True})
    bot.answer_callback_query(call.id)

@bot.message_handler(func=lambda m: storage.get_user(m.from_user.id).get("game2_active"))
def game2_play(message):
    choices = ["سنگ","کاغذ","قیچی"]
    user_choice = message.text.strip()
    bot_choice = random.choice(choices)
    user_id = message.from_user.id
    if user_choice==bot_choice:
        bot.send_message(message.chat.id,f"🔹 مساوی! هر دو {bot_choice}")
    elif (user_choice=="سنگ" and bot_choice=="قیچی") or (user_choice=="قیچی" and bot_choice=="کاغذ") or (user_choice=="کاغذ" and bot_choice=="سنگ"):
        storage.update_user(user_id, {"points": storage.get_user(user_id)["points"]+50})
        bot.send_message(message.chat.id,f"🎉 بردی! من {bot_choice} بودم +50 امتیاز")
    else:
        bot.send_message(message.chat.id,f"❌ باختی! من {bot_choice} بردم")
    storage.update_user(user_id, {"game2_active": False})
@app.route('/', methods=['POST','GET'])
def webhook():
    if request.method=='POST':
        update = telebot.types.Update.de_json(request.get_data().decode("utf-8"))
        bot.process_new_updates([update])
        return 'OK',200
    return 'DUMB PANDA BOT RUNNING 🐼'

@app.route('/health', methods=['GET'])
def health(): return '🤖 Bot is running 🐼',200

@app.route('/setup', methods=['GET'])
def setup():
    try:
        bot.remove_webhook()
        import time; time.sleep(1)
        bot.set_webhook(url=f'{DOMAIN}/')
        return f'✅ Webhook set! {DOMAIN}',200
    except Exception as e:
        return f'❌ Error: {e}',500

if __name__=='__main__':
    import time
    try:
        bot.remove_webhook(); time.sleep(1)
        bot.set_webhook(url=f'{DOMAIN}/')
    except: pass
    app.run(host="0.0.0.0", port=int(os.getenv("PORT",5000)), debug=False)

