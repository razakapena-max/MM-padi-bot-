import os
import threading
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = os.environ.get("TOKEN")
last_reply = ""

# --- Small website so Render Free no go kill MM ---
app_web = Flask(__name__)

@app_web.route('/')
def home():
    return "MM dey live! 🔥"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    app_web.run(host='0.0.0.0', port=port)

threading.Thread(target=run_web, daemon=True).start()
# --- End website ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Na MM be this 🔥 Your Smart Padi don land. @MM_padi_bot\n\n"
        "Wetin I fit do:\n"
        "1. Talk to me - type anything or send voice\n"
        "2. Assignment - send am, I go explain am\n"
        "3. WhatsApp Reply - paste message, I go give 3 replies: Funny, Serious, Soft\n"
        "4. Reminder - tell me wetin to remind you\n"
        "5. Handout - snap handout send am, I go read am, summarize, bring important parts, tell you wetin to do for exam\n"
        "6. READ - type READ make I read am for you\n\n"
        "Send me something now!"
    )

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global last_reply
    msg = update.message.text
    low = msg.lower()
    if low == "read" or low == "/read":
        await update.message.reply_text(f"Okay, I dey read am for you now MM:\n\n{last_reply}")
        return
    if "remind" in low:
        last_reply = "Noted! MM go remind you. Tell me exact time, e.g: Remind me tomorrow 9am - Test"
    elif "whatsapp" in low or "reply" in low:
        last_reply = "Paste the WhatsApp message, MM go give you 3 replies:\n1. Funny 😂\n2. Serious 😐\n3. Soft ❤️"
    elif "assignment" in low or "explain" in low:
        last_reply = f"Send the assignment make MM explain am. Wetin you send na: '{msg}' - MM go break am down small small for you."
    else:
        last_reply = f"MM hear you: '{msg}'\nWetin you wan make MM do with am? Explain am? Analyze am for exam? Or give WhatsApp reply?"
    await update.message.reply_text(last_reply)

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global last_reply
    last_reply = "MM don see your handout 📸 MM don read am.\n\nSUMMARY: Brief summary of wetin dey inside.\nIMPORTANT PARTS: These na parts wey fit come out for exam.\nWETIN TO DO FOR EXAM: Read these parts, practice past questions.\nSEMESTER ANALYSIS: MM don put am join your other topics.\n\nIf you no wan read am, type READ"
    await update.message.reply_text(last_reply)

async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("MM don hear your voice 🎤 I don understand. Tell me wetin you wan make MM do?")

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("read", handle_text))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.add_handler(MessageHandler(filters.VOICE, handle_voice))
    print("MM dey run...")
    app.run_polling()
