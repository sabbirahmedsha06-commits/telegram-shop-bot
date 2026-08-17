import os
import asyncio
from datetime import datetime, timedelta, timezone

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

# =========================
# SETTINGS
# =========================

BOT_TOKEN = os.getenv("BOT_TOKEN")

# তোমার Telegram numeric ID এখানে বসাবে
ADMIN_ID = int(os.getenv("ADMIN_ID", "8752830051"))

SUPPORT_USERNAME = "@sabbirahmed187"

BKASH = "01755196906"
NAGAD = "01706965471"


# =========================
# PRODUCTS
# =========================

PRODUCTS = {
    "sabbir": {
        "name": "🔥 SABBIR MODE PRO APK",
        "type": "key",
        "prices": {
            "7": 40,
            "15": 80,
            "30": 120,
        },
    },

    "pest": {
        "name": "🩵 PEST TOURNAMENT LOCATION",
        "type": "file",
        "price": 150,
        "duration": 90,
    },

    "pink": {
        "name": "💜 PINK TOURNAMENT LOCATION",
        "type": "file",
        "price": 150,
        "duration": 90,
    },

    "yellow": {
        "name": "💛 YELLOW TOURNAMENT LOCATION",
        "type": "file",
        "price": 150,
        "duration": 90,
    },

    "blue": {
        "name": "💙 BLUE TOURNAMENT LOCATION",
        "type": "file",
        "price": 150,
        "duration": 90,
    },

    "green": {
        "name": "💚 GREEN TOURNAMENT LOCATION",
        "type": "file",
        "price": 150,
        "duration": 90,
    },

    "brcs": {
        "name": "🔥 BR CS + TOURNAMENT LOCATION",
        "type": "file",
        "price": 200,
        "duration": 90,
    },
}


# =========================
# TEMPORARY ORDERS
# =========================

orders = {}


# =========================
# START
# =========================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [
        [InlineKeyboardButton("🛒 Shop", callback_data="shop")],
        [InlineKeyboardButton("🎥 Tutorial", callback_data="tutorial")],
        [InlineKeyboardButton("🎁 Lucky Spin", callback_data="spin")],
        [InlineKeyboardButton("🆘 Support", callback_data="support")],
    ]

    text = (
        "🛍️ <b>WELCOME TO OUR SHOP</b>\n\n"
        "🔥 Premium Products Available\n"
        "⚡ Fast Delivery\n"
        "🔐 Secure Service\n\n"
        "👇 নিচের Menu থেকে একটি অপশন নির্বাচন করুন।"
    )

    await update.message.reply_text(
        text,
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


# =========================
# SHOP
# =========================

async def shop(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    keyboard = [
        [InlineKeyboardButton("🔥 SABBIR MODE PRO APK", callback_data="product_sabbir")],
        [InlineKeyboardButton("🩵 PEST LOCATION", callback_data="product_pest")],
        [InlineKeyboardButton("💜 PINK LOCATION", callback_data="product_pink")],
        [InlineKeyboardButton("💛 YELLOW LOCATION", callback_data="product_yellow")],
        [InlineKeyboardButton("💙 BLUE LOCATION", callback_data="product_blue")],
        [InlineKeyboardButton("💚 GREEN LOCATION", callback_data="product_green")],
        [InlineKeyboardButton("🔥 BR CS + TOURNAMENT", callback_data="product_brcs")],
        [InlineKeyboardButton("🆘 Support", callback_data="support")],
    ]

    await query.edit_message_text(
        "🛒 <b>SHOP MENU</b>\n\n"
        "আপনার পছন্দের Product নির্বাচন করুন 👇",
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


# =========================
# PRODUCT
# =========================

async def product(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    product_id = query.data.replace("product_", "")
    product_data = PRODUCTS[product_id]

    if product_id == "sabbir":

        keyboard = [
            [InlineKeyboardButton("7 Days — 40৳", callback_data="buy_sabbir_7")],
            [InlineKeyboardButton("15 Days — 80৳", callback_data="buy_sabbir_15")],
            [InlineKeyboardButton("30 Days — 120৳", callback_data="buy_sabbir_30")],
            [InlineKeyboardButton("⬅️ Back", callback_data="shop")],
        ]

        text = (
            f"{product_data['name']}\n\n"
            "⏳ Choose Duration:\n\n"
            "7 Day — 40 Tk\n"
            "15 Day — 80 Tk\n"
            "30 Day — 120 Tk"
        )

    else:

        keyboard = [
            [
                InlineKeyboardButton(
                    f"💳 Buy — {product_data['price']}৳",
                    callback_data=f"buy_{product_id}"
                )
            ],
            [InlineKeyboardButton("⬅️ Back", callback_data="shop")],
        ]

        text = (
            f"<b>{product_data['name']}</b>\n\n"
            f"💰 Price: {product_data['price']} Tk\n"
            f"⏳ Validity: 3 Months\n\n"
            "নিচের Buy Button চাপুন।"
        )

    await query.edit_message_text(
        text,
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


# =========================
# BUY
# =========================

async def buy(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    data = query.data.replace("buy_", "")
    parts = data.split("_")

    product_id = parts[0]
    duration = parts[1] if len(parts) > 1 else None

    product_data = PRODUCTS[product_id]

    if product_id == "sabbir":
        price = product_data["prices"][duration]
        duration_text = f"{duration} Days"
    else:
        price = product_data["price"]
        duration_text = "3 Months"

    order_id = f"{query.from_user.id}_{int(datetime.now().timestamp())}"

    orders[order_id] = {
        "user_id": query.from_user.id,
        "username": query.from_user.username,
        "product": product_id,
        "duration": duration,
        "price": price,
    }

    keyboard = [
        [
            InlineKeyboardButton(
                "📤 I Have Paid",
                callback_data=f"paid_{order_id}"
            )
        ],
        [InlineKeyboardButton("⬅️ Back", callback_data="shop")],
    ]

    text = (
        "💳 <b>PAYMENT INFORMATION</b>\n\n"
        f"📦 Product: {product_data['name']}\n"
        f"⏳ Duration: {duration_text}\n"
        f"💰 Amount: {price} Tk\n\n"
        f"🟢 bKash: <code>{BKASH}</code>\n"
        f"🟠 Nagad: <code>{NAGAD}</code>\n\n"
        "Payment করার পর নিচের\n"
        "<b>📤 I Have Paid</b> Button চাপুন।"
    )

    await query.edit_message_text(
        text,
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


# =========================
# PAID
# =========================

async def paid(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    order_id = query.data.replace("paid_", "")

    if order_id not in orders:
        await query.edit_message_text("❌ Order পাওয়া যায়নি।")
        return

    order = orders[order_id]

    keyboard = [
        [
            InlineKeyboardButton(
                "✅ Approve",
                callback_data=f"approve_{order_id}"
            ),
            InlineKeyboardButton(
                "❌ Reject",
                callback_data=f"reject_{order_id}"
            ),
        ]
    ]

    admin_text = (
        "🔔 <b>NEW PAYMENT REQUEST</b>\n\n"
        f"🆔 Order: <code>{order_id}</code>\n"
        f"👤 User ID: <code>{order['user_id']}</code>\n"
        f"📦 Product: {order['product']}\n"
        f"⏳ Duration: {order['duration']}\n"
        f"💰 Amount: {order['price']} Tk\n"
        f"👤 Username: @{order['username'] or 'No Username'}"
    )

    await context.bot.send_message(
        ADMIN_ID,
        admin_text,
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )

    await query.edit_message_text(
        "✅ আপনার Payment Request Admin-এর কাছে পাঠানো হয়েছে।\n\n"
        "⏳ Payment verify হওয়ার পর আপনার Product দেওয়া হবে।"
    )


# =========================
# APPROVE
# =========================

async def approve(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    order_id = query.data.replace("approve_", "")

    if order_id not in orders:
        await query.edit_message_text("❌ Order পাওয়া যায়নি।")
        return

    order = orders[order_id]

    # SABBIR MODE
    if order["product"] == "sabbir":

        keyboard = [
            [
                InlineKeyboardButton(
                    "🔐 Send Username & Password",
                    callback_data=f"credential_{order_id}"
                )
            ]
        ]

        await query.edit_message_text(
            "✅ Payment Approved!\n\n"
            "এখন User-এর জন্য Username + Password তৈরি/পাঠান।",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )

    else:

        await query.edit_message_text(
            "✅ Payment Approved!\n\n"
            "📁 এখন Product-এর File User-কে পাঠাতে হবে।"
        )

        await context.bot.send_message(
            order["user_id"],
            "✅ <b>Payment Approved!</b>\n\n"
            "📁 আপনার Product প্রস্তুত করা হচ্ছে।",
            parse_mode="HTML",
        )


# =========================
# REJECT
# =========================

async def reject(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    order_id = query.data.replace("reject_", "")

    if order_id not in orders:
        return

    order = orders[order_id]

    await context.bot.send_message(
        order["user_id"],
        "❌ আপনার Payment Request Reject করা হয়েছে।\n\n"
        "প্রয়োজনে Support-এ যোগাযোগ করুন।"
    )

    await query.edit_message_text(
        f"❌ Order Rejected\n\nOrder: {order_id}"
    )


# =========================
# SUPPORT
# =========================

async def support(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    keyboard = [
        [
            InlineKeyboardButton(
                "💬 Contact Support",
                url="https://t.me/sabbirahmed187"
            )
        ],
        [InlineKeyboardButton("⬅️ Back to Menu", callback_data="shop")],
    ]

    await query.edit_message_text(
        "🆘 <b>SUPPORT</b>\n\n"
        "কোনো সমস্যা হলে আমাদের Support-এ যোগাযোগ করুন।\n\n"
        f"👤 Support: {SUPPORT_USERNAME}",
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


# =========================
# TUTORIAL
# =========================

async def tutorial(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    keyboard = [
        [
            InlineKeyboardButton(
                "📺 How To Purchase",
                callback_data="purchase_help"
            )
        ],
        [InlineKeyboardButton("⬅️ Back to Menu", callback_data="shop")],
    ]

    await query.edit_message_text(
        "📺 <b>VIDEO TUTORIALS</b>\n\n"
        "🎬 Learn How To Use Our Products\n\n"
        "📱 Step-by-step guides\n"
        "🎮 Game setup tutorials\n"
        "⚙️ Installation help\n"
        "💡 Tips & Tricks\n\n"
        "👇 Tutorial নির্বাচন করুন:",
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


# =========================
# PURCHASE HELP
# =========================

async def purchase_help(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    await query.edit_message_text(
        "🛒 <b>HOW TO PURCHASE</b>\n\n"
        "1️⃣ Shop Menu ওপেন করুন\n"
        "2️⃣ আপনার Product নির্বাচন করুন\n"
        "3️⃣ Duration নির্বাচন করুন\n"
        "4️⃣ bKash/Nagad-এ Payment করুন\n"
        "5️⃣ I Have Paid Button চাপুন\n"
        "6️⃣ Admin Payment Verify করবে\n"
        "7️⃣ Verify হওয়ার পর Product পাবেন\n\n"
        "🆘 সমস্যা হলে Support-এ যোগাযোগ করুন।",
        parse_mode="HTML",
    )


# =========================
# LUCKY SPIN
# =========================

async def spin(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    await query.edit_message_text(
        "🎰 <b>LUCKY SPIN</b>\n\n"
        "🎁 Lucky Spin System শীঘ্রই চালু হবে!\n\n"
        "⏰ Please come back later.",
        parse_mode="HTML",
    )


# =========================
# CALLBACK ROUTER
# =========================

async def callback_router(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query

    if query.data == "shop":
        await shop(update, context)

    elif query.data.startswith("product_"):
        await product(update, context)

    elif query.data.startswith("buy_"):
        await buy(update, context)

    elif query.data.startswith("paid_"):
        await paid(update, context)

    elif query.data.startswith("approve_"):
        await approve(update, context)

    elif query.data.startswith("reject_"):
        await reject(update, context)

    elif query.data == "support":
        await support(update, context)

    elif query.data == "tutorial":
        await tutorial(update, context)

    elif query.data == "purchase_help":
        await purchase_help(update, context)

    elif query.data == "spin":
        await spin(update, context)


# =========================
# MAIN
# =========================

def main():

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(callback_router))

    print("BOT IS RUNNING...")

    app.run_polling()


if __name__ == "__main__":
    main()
