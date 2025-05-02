from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
    MessageHandler,
    )
import os

from dotenv import load_dotenv
from datetime import datetime
from draft5 import buscar_ultimo_jogo_furia  # Importando a função de scraping
from curiosidade import buscar_curiosidades_furia  # Importando a função de curiosidades
from database import salvar_sugestao_no_banco, inicializar_banco  # Importa a função do módulo de banco de dados
from keys import TELEGRAM_BOT# Importa a chave do bot do módulo keys


# Função para gerar o menu inicial
def gerar_menu():
    keyboard = [
        [InlineKeyboardButton("Último Jogo", callback_data='ultimojogo')],
        [InlineKeyboardButton("Elenco", callback_data='elenco')],
        [InlineKeyboardButton("Curiosidade", callback_data='curiosidade')],
        [InlineKeyboardButton("Canais ", callback_data='canais')],
        [InlineKeyboardButton("Furyback", callback_data='furyback')],
        [InlineKeyboardButton("Sair", callback_data='excluir_chat')]
    ]
    return InlineKeyboardMarkup(keyboard)

# Função para mostrar o menu principal após consultar alguma opção
async def voltar_ao_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.edit_message_text(
        "Escolha uma opção:",
        reply_markup=gerar_menu()
    )

# Handler do comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Adiciona esta linha para apagar a mensagem do comando /start
    if update.message:
        try:
            await update.message.delete()
        except Exception as e:
            # Trate possíveis erros caso o bot não tenha permissão para apagar mensagens
            print(f"Erro ao tentar apagar a mensagem /start: {e}")
    
    
    await context.bot.send_photo(
    chat_id=update.effective_chat.id, # O ID do chat para onde enviar a foto
    photo=open(r"\furiando.jpg", 'rb')) # Abre o arquivo da imagem)   
    await update.message.reply_text("Olá, FURIOSO! Bem-vindo ao FURIANDO!!!🖤𓃮")
    
    keyboard = [
        [InlineKeyboardButton("Último Jogo", callback_data='ultimojogo')],
        [InlineKeyboardButton("Elenco", callback_data='elenco')],
        [InlineKeyboardButton("Curiosidade", callback_data='curiosidade')],
        [InlineKeyboardButton("Canais ", callback_data='canais')],
        [InlineKeyboardButton("Furyback", callback_data='Furyback')],
        [InlineKeyboardButton("Sair", callback_data='excluir_chat')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Saiba mais:", reply_markup=reply_markup)

# Função para gerar o botão "Voltar ao Menu"
def botao_voltar_ao_menu():
    return [
        [InlineKeyboardButton("Voltar ao Menu", callback_data='voltar_menu')]
    ]

# Função para lidar com o botão "Excluir Chat"
async def excluir_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = "Chat excluído com sucesso!"
    await update.callback_query.edit_message_text(texto)
    
    # Apaga a mensagem do chat
    chat_id = update.callback_query.message.chat_id
    message_id = update.callback_query.message.message_id
    try:
        await context.bot.delete_message(chat_id=chat_id, message_id=message_id)
    except Exception as e:
        print(f"Erro ao excluir a mensagem: {e}")
    
    # Redireciona de volta ao menu principal
    await voltar_ao_menu(update, context)

# Função para lidar com o botão "Furyback"
async def furyback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Define que o bot está esperando o nome do usuário
    context.user_data["esperando_nome"] = True
    await update.callback_query.edit_message_text("Por favor, me diga o seu nome. 😊")

async def capturar_nome_ou_sugestao(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Caso o bot esteja esperando o nome do usuário
    if context.user_data.get("esperando_nome", False):
        nome = update.message.text
        context.user_data["nome"] = nome
        context.user_data["esperando_nome"] = False
        context.user_data["esperando_sugestao"] = True

        # Apagar a mensagem do usuário
        await context.bot.delete_message(chat_id=update.effective_chat.id, message_id=update.message.message_id)

        # Perguntar a sugestão
        mensagem_bot = await update.message.reply_text(f"Obrigado, {nome}! Agora, por favor, me diga sua sugestão. 😊")

        # Salvar o ID da mensagem do bot para apagá-la depois
        context.user_data["mensagem_bot_id"] = mensagem_bot.message_id

    # Caso o bot esteja esperando a sugestão do usuário
    elif context.user_data.get("esperando_sugestao", False):
        sugestao = update.message.text
        nome = context.user_data.get("nome")
        user = update.effective_user

        # Salvar a sugestão no banco de dados
        salvar_sugestao_no_banco(nome, user.username, user.id, sugestao)

        # Apagar as mensagens do usuário e do bot
        await context.bot.delete_message(chat_id=update.effective_chat.id, message_id=update.message.message_id)
        if "mensagem_bot_id" in context.user_data:
            await context.bot.delete_message(chat_id=update.effective_chat.id, message_id=context.user_data["mensagem_bot_id"])

        # Responder com uma mensagem final
        reply_markup = InlineKeyboardMarkup([
            [InlineKeyboardButton("Voltar ao Menu", callback_data='voltar_menu')]
        ])
        mensagem_final = await update.message.reply_text(
            "Obrigado pela sua sugestão! Ela foi registrada com sucesso.",
            reply_markup=reply_markup
        )

        # Salvar o ID da mensagem final do bot para apagar depois (opcional)
        context.user_data["mensagem_final_id"] = mensagem_final.message_id

        # Resetar os estados
        context.user_data["esperando_sugestao"] = False
        context.user_data["nome"] = None

    else:
        # Caso o bot não esteja esperando nenhuma informação
        await update.message.reply_text("Desculpe, não estou esperando nenhuma informação no momento. Use o menu para interagir comigo.")
        
        # Handler de cliques nos botões
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'curiosidade':
        texto = buscar_curiosidades_furia()
        reply_markup = InlineKeyboardMarkup(botao_voltar_ao_menu())
        await query.edit_message_text(texto, reply_markup=reply_markup)
    
    elif query.data == 'canais':
        texto = "🖤Canais oficiais da FURIA:🖤\n\n" \
                "Twitch: https://www.twitch.tv/furiatv\n" \
                "X/Twitter: https://x.com/FURIA\n" \
                "Instagram: https://www.instagram.com/furiagg\n" \
                "Site: https://www.furia.gg/\n" \
                "Facebook: https://web.facebook.com/furiagg\n"
        reply_markup = InlineKeyboardMarkup(botao_voltar_ao_menu())
        await query.edit_message_text(texto, reply_markup=reply_markup)
    
    

    elif query.data == 'ultimojogo':
        texto = buscar_ultimo_jogo_furia()  # Usando a função de scraping
        reply_markup = InlineKeyboardMarkup(botao_voltar_ao_menu())
        await query.edit_message_text(texto, reply_markup=reply_markup)
    
    elif query.data == 'furyback':
        # Chama a função para lidar com o botão "Furyback"
        await furyback_handler(update, context)

    elif query.data == 'elenco':
        texto = "Elenco atual: KSCERATO, yuurih, FalleN, molodoy, YEKINDAR."
        reply_markup = InlineKeyboardMarkup(botao_voltar_ao_menu())
        await query.edit_message_text(texto, reply_markup=reply_markup)

    elif query.data == 'voltar_menu':
        await voltar_ao_menu(update, context)  # Redireciona para o menu inicial

    elif query.data == 'excluir_chat':
        await excluir_chat(update, context)  # Lida com a exclusão do chat



# Inicialização do bot
app = ApplicationBuilder().token(TELEGRAM_BOT).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button_handler))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, capturar_nome_ou_sugestao))
app.run_polling()

