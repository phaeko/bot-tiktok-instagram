import os
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from tiktok_download import download_tiktok
from instagram_download import download_instagram
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Obtém o token do bot do ambiente
TOKEN = os.getenv("TOKEN")

# Cria uma instância do bot do Telegram
bot = telegram.Bot(token=TOKEN)

# Define a função de callback para o comando /start
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Olá! Envie o link do vídeo do TikTok ou do Instagram que deseja baixar.")

# Define a função de callback para o comando /help
def help(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Envie o link do vídeo do TikTok ou do Instagram que deseja baixar.")

# Define a função de callback para receber mensagens
def receive_message(update, context):
    # Obtém a mensagem enviada pelo usuário
    message = update.message.text
    
    # Verifica se a mensagem é uma URL do TikTok
    if "tiktok.com" in message:
        download_tiktok(message, context, update.effective_chat.id)
    # Verifica se a mensagem é uma URL do Instagram
    elif "instagram.com" in message:
        download_instagram(message, context, update.effective_chat.id)
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Por favor, envie uma URL válida do TikTok ou do Instagram.")
    
# Cria uma instância do Updater
updater = Updater(token=TOKEN, use_context=True)

# Obtém o objeto de despacho de comandos do Updater
dispatcher = updater.dispatcher

# Adiciona o tratador de comandos /start
dispatcher.add_handler(CommandHandler("start", start))

# Adiciona o tratador de comandos /help
dispatcher.add_handler(CommandHandler("help", help))

# Adiciona o tratador de mensagens
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, receive_message))

# Inicia o bot
updater.start_polling()

# Espera o bot ser encerrado
updater.idle()
