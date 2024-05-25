import os
import random
import requests
import subprocess
import json

def download_tiktok(video_url, context, chat_id):
    try:
        # Envia uma mensagem de que o download está sendo feito
        context.bot.send_message(chat_id=chat_id, text="O download do vídeo do TikTok está sendo feito, aguarde por favor...")

        # Comando para obter a URL do vídeo
        cmd = [
            'python', '-m', 'tiktok_downloader',
            '--url', video_url,
            '--snaptik'
        ]

        # Executa o comando e captura a saída
        result = subprocess.run(cmd, capture_output=True, text=True)
        output = result.stdout.strip()

        if not output:
            raise ValueError("A resposta do comando tiktok_downloader está vazia.")

        # Converte a saída JSON em um objeto Python
        try:
            video_info = json.loads(output)
        except json.JSONDecodeError:
            raise ValueError("Falha ao decodificar a resposta JSON.")

        # Verifica se a URL de download está presente
        if not video_info or 'url' not in video_info[0]:
            raise ValueError("URL de download não encontrada na resposta.")

        # Obtém a URL de download do vídeo
        download_url = video_info[0]['url']

        # Gera 5 números aleatórios para o nome do arquivo
        random_nums = ''.join([str(random.randint(0, 9)) for _ in range(5)])
        video_filename = f"tiktok_video_{random_nums}.mp4"

        # Define o caminho para salvar o vídeo
        video_path = os.path.join(os.getcwd(), video_filename)

        # Faz o download do vídeo e salva no caminho especificado
        response = requests.get(download_url)
        with open(video_path, 'wb') as f:
            f.write(response.content)

        # Envia o vídeo para o usuário
        with open(video_path, "rb") as file:
            context.bot.send_document(chat_id=chat_id, document=file)

        # Apaga o vídeo baixado
        os.remove(video_path)
        
        context.bot.send_message(chat_id=chat_id, text="Download do vídeo do TikTok concluído!")
    except Exception as e:
        context.bot.send_message(chat_id=chat_id, text="Erro ao baixar vídeo do TikTok: " + str(e))
