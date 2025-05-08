from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from process_video import process_video
import os

TOKEN = os.environ.get("7966937455:AAGrawnkd5eJiia9TyRPch2fmPsxZCmhCh8")

if not os.path.exists("videos"):
    os.makedirs("videos")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user.first_name
    welcome_text = f"سلام {user} عزیز! به ربات ترجمه و زیرنویس خوش اومدی."
    menu = [["ارسال فیلم برای ترجمه"]]
    reply_markup = ReplyKeyboardMarkup(menu, resize_keyboard=True)
    await update.message.reply_text(welcome_text, reply_markup=reply_markup)

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "ارسال فیلم برای ترجمه":
        await update.message.reply_text("لطفاً فایل ویدیویی‌ت رو بفرست.")

async def handle_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    video = update.message.video or update.message.document
    if not video:
        await update.message.reply_text("ویدیویی دریافت نشد. لطفاً دوباره تلاش کن.")
        return

    await update.message.reply_text("در حال دریافت و ذخیره‌سازی ویدیو...")

    file = await context.bot.get_file(video.file_id)
    video_path = f"videos/{video.file_name or 'video.mp4'}"
    await file.download_to_drive(video_path)

    await update.message.reply_text("در حال پردازش و ساخت زیرنویس...")

    try:
        subtitle_path = process_video(video_path)
        await update.message.reply_document(document=open(subtitle_path, "rb"), filename="subtitle.srt")
    except Exception as e:
        await update.message.reply_text(f"خطا در پردازش ویدیو: {str(e)}")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
app.add_handler(MessageHandler(filters.VIDEO | filters.Document.VIDEO, handle_video))

print("ربات فعال شد...")
app.run_polling()
