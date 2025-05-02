# 🤖 FURIANDO  — Chatbot da FURIA no Telegram

Este projeto é um chatbot desenvolvido em **Python** para fãs do time de CS:GO **FURIA**. Integrado ao Telegram, ele oferece informações atualizadas sobre o time, curiosidades, elenco atual, canais oficiais e ainda permite sugestões de fãs que são armazenadas em um banco de dados SQL.

## ⚙️ Funcionalidades

- **🔍 Último Jogo**: Utiliza *web scraping* com a função `buscar_ultimo_jogo_furia()` (módulo `draft5_scraper`) para extrair dados do último jogo da FURIA diretamente do site [Draft5.gg](https://draft5.gg).

- **🧠 Curiosidades**: Integração com a API **Gemini** via `buscar_curiosidades_furia()` para trazer curiosidades divertidas e informativas sobre a equipe.

- **📥 Sugestões**: Coleta o nome do usuário e sua sugestão por meio do botão "Furyback" e armazena no banco de dados SQLite via `salvar_sugestao_no_banco()`.

- **🧑‍💻 Elenco Atual**: Lista atualizada do elenco com nomes como **KSCERATO, yuurih, FalleN, molodoy, YEKINDAR**.

- **🌐 Canais Oficiais da FURIA**: Acesso rápido para as principais redes da organização:
  - [Twitch](https://www.twitch.tv/furiatv)
  - [Twitter/X](https://x.com/FURIA)
  - [Instagram](https://www.instagram.com/furiagg)
  - [Site Oficial](https://www.furia.gg/)
  - [Facebook](https://web.facebook.com/furiagg)

## 📦 Tecnologias Utilizadas

- **Python**
- **Telegram Bot API** (via `python-telegram-bot`)
- **SQLite** para armazenamento das sugestões
- **Web Scraping** com `requests` e `BeautifulSoup` para extrair dados de partidas no **Draft5.gg**
- **Gemini API** para geração de curiosidades

## 🚀 Executando o Bot

1. Clone este repositório
2. Configure suas chaves no arquivo `keys.py`
3. Execute o arquivo principal:

```bash
python furiando.py
