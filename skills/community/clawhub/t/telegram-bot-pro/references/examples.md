# Telegram Bot Examples

## Example 1: Simple Echo Bot

```python
# echo_bot.py
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Echo bot started!")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(update.message.text)

app = Application.builder().token("YOUR_TOKEN").build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT, echo))
app.run_polling()
```

## Example 2: Inline Keyboard Bot

```python
# keyboard_bot.py
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Option 1", callback_data="1")],
        [InlineKeyboardButton("Option 2", callback_data="2")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Choose:", reply_markup=reply_markup)

async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(f"You chose: {query.data}")

app = Application.builder().token("YOUR_TOKEN").build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button_click))
app.run_polling()
```

## Example 3: Admin Bot for Groups

```python
# admin_bot.py
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

ADMIN_IDS = [123456789]  # Your user ID

async def ban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.id not in ADMIN_IDS:
        await update.message.reply_text("Not authorized")
        return
    if update.message.reply_to_message:
        await context.bot.ban_chat_member(
            chat_id=update.message.chat_id,
            user_id=update.message.reply_to_message.from_user.id
        )
        await update.message.reply_text("User banned")

app = Application.builder().token("YOUR_TOKEN").build()
app.add_handler(CommandHandler("ban", ban))
app.run_polling()
```

## Example 4: Notification Bot

```python
# notify_bot.py
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Store user IDs
USER_IDS = set()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    USER_IDS.add(update.message.from_user.id)
    await update.message.reply_text(f"Registered! Your ID: {update.message.from_user.id}")

async def notify(context: ContextTypes.DEFAULT_TYPE, message: str):
    for user_id in USER_IDS:
        await context.bot.send_message(chat_id=user_id, text=message)

# Usage:
# await notify(context, "Something happened!")
```

## Running the Bot

```bash
# Polling mode (development)
python scripts/bot.py --token YOUR_TOKEN --poll

# Webhook mode (production)
python scripts/bot.py --token YOUR_TOKEN --webhook-url https://your-domain.com/webhook
```

## Getting Help

- Bot API: https://core.telegram.org/bots/api
- python-telegram-bot: https://python-telegram-bot.org
