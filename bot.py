from MakerWorldScrapper import obtain_data
from CalcPrice import calculate_final_price
import json
import os
import re
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

with open('var.json', 'r', encoding="utf-8") as file:
    config = json.load(file)

url_pattern = re.compile(r"https?://(www\.)?makerworld\.com/\S+")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hola! por favor digite el link del modelo de MakerWorld que desea calcular el precio de impresión. Asegúrese de que sea un enlace válido de MakerWorld."
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text or ""
    match = url_pattern.search(text)

    if not match:
        await update.message.reply_text("Por favor, envíame un link válido de MakerWorld.")
        return

    url = match.group(0)
    await update.message.reply_text("Buscando datos del modelo, por favor espere...")

    try:
        weight, time_sec, title, time_str = obtain_data(url)
    except Exception as e:
        logger.exception("Error scraping MakerWorld")
        await update.message.reply_text("Ocurrió un error al consultar MakerWorld. Intenta de nuevo más tarde.")
        return

    if weight is None:
        await update.message.reply_text("No pude obtener los datos de ese modelo. ¿El link es correcto?")
        return

    time_hr = time_sec / 3600
    final_price = calculate_final_price(config, weight, time_hr, prep_time_min=0)

    reply = (
        f"Modelo: {title}\n"
        f"Tiempo estimado: {time_str}\n"
        f"Peso: {weight} g\n"
        f"Precio sugerido: ${final_price:,.0f} COP"
    )
    await update.message.reply_text(reply)

def main():
    token = os.getenv("tele_token")
    if not token:
        raise ValueError("El token del bot no está configurado en las variables de entorno.")
    app = Application.builder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    logger.info("Bot iniciado. Esperando mensajes...")
    app.run_polling()

if __name__ == "__main__":
    main()