import os
import random
import shutil
import instaloader

# Cria uma instância do Instaloader com um user agent personalizado
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
loader = instaloader.Instaloader()
loader.context.user_agent = user_agent

def download_instagram(post_url, context, chat_id):
    try:
        # Envia uma mensagem de que o download está sendo feito
        context.bot.send_message(chat_id=chat_id, text="O download do post do Instagram está sendo feito, aguarde por favor...")

        # Obtém o post a partir da URL
        shortcode = post_url.split("/")[-2]
        post = instaloader.Post.from_shortcode(loader.context, shortcode)
        
        # Gera 5 números aleatórios
        random_nums = ''.join([str(random.randint(0, 9)) for _ in range(5)])

        # Concatena os números aleatórios com o nome do proprietário do post
        download_folder = post.owner_username + "_" + random_nums

        # Baixa as mídias do post
        loader.download_post(post, target=download_folder)

        # Envia as mídias para o usuário
        for filename in os.listdir(download_folder):
            if filename.endswith('.jpg') or filename.endswith('.mp4'):
                with open(download_folder + "/" + filename, "rb") as file:
                    context.bot.send_document(chat_id=chat_id, document=file)

        # Apaga o cache do download
        shutil.rmtree(download_folder)
        
        context.bot.send_message(chat_id=chat_id, text="Download do post do Instagram concluído!")
    except Exception as e:
        context.bot.send_message(chat_id=chat_id, text="Erro ao baixar post do Instagram: " + str(e))
