from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
import os

# Nome do arquivo de cache
CACHE_FILE = "draft5.json"
CACHE_DURATION = 300  # Duração do cache em segundos (5 minutos)

# Função para carregar o cache do arquivo
def carregar_cache():
    try:
        with open(CACHE_FILE, "r") as f:
            cache = json.load(f)
            # Verifica se o cache ainda é válido
            if time.time() - cache["timestamp"] < CACHE_DURATION:
                return cache["dados"]
    except (FileNotFoundError, json.JSONDecodeError):
        pass
    return None

# Função para salvar os dados no cache
def salvar_cache(dados):
    with open(CACHE_FILE, "w") as f:
        json.dump({"dados": dados, "timestamp": time.time()}, f)

def buscar_ultimo_jogo_furia():
    """
    Esta função busca o último jogo da FURIA.
    """
    # Tenta carregar os dados do cache
    cache = carregar_cache()
    if cache:
        print("Usando cache...")
        return cache

    try:
        # Caminho para o EdgeDriver (ajuste conforme necessário)
        edgedriver_path = os.getenv("EDGEDRIVER_PATH", r"E:\Downloads\edgedriver_win64\msedgedriver.exe")
        service = Service(edgedriver_path)
        driver = webdriver.Edge(service=service)

        # URL da página de resultados da FURIA
        url = "https://draft5.gg/equipe/330-FURIA/resultados"
        driver.get(url)

        # Espera explícita para garantir que o elemento esteja presente
        wait = WebDriverWait(driver, 10)  # Tempo máximo de espera: 10 segundos

        # Localize o resultado do último jogo
        seletor_resultado = "#AppContainer > div > div > div > div.sc-dkPtRN.id__BaseCol-sc-1x9brse-0.TYdVh.edCxBh > div.id__ContentContainer-sc-1x9brse-2.hlMjcl > a:nth-child(3)"
        resultado_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, seletor_resultado)))
        resultado = resultado_element.text

        # Localize o adversário ou outras informações necessárias
        seletor_adversario = ".MatchCardSimple__TeamNameAndLogo-sc-wcmxha-40 span"
        adversario_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, seletor_adversario)))
        adversario = adversario_element.text

        # Fechar o navegador
        driver.quit()

        # Formatar o resultado
        ultimo_jogo = f"Último jogo: FURIA {resultado} contra {adversario}"

        # Salva os dados no cache
        salvar_cache(ultimo_jogo)

        return ultimo_jogo

    except Exception as e:
        print(f"Ocorreu um erro: {e}")
        return "Ocorreu um erro ao buscar o resultado do último jogo."

    finally:
        # Garante que o navegador será fechado
        try:
            driver.quit()
        except:
            pass