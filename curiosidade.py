import google.generativeai as genai
import os
import textwrap
import sys 
# Importa a classe de exceção correta para erros de API
import google.api_core.exceptions
from keys import GEMINI_API_KEY
def buscar_curiosidades_furia():
    """
    Conecta na API do Gemini para buscar informações e curiosidades
    sobre o time da FURIA de CS.

    Retorna:
        str: Uma string contendo as informações e curiosidades obtidas
             da API, ou uma mensagem de erro detalhada.
    """
    # REGISTRANDO A CHAVE DA API DIRETAMENTE NO CÓDIGO
    # ATENÇÃO: Esta prática NÃO É SEGURA para chaves secretas.
    # É altamente recomendável usar variáveis de ambiente ou um arquivo de configuração.
    google_api_key = GEMINI_API_KEY # <-- SUBSTITUA PELA SUA CHAVE REAL

    # Verificar se a chave placeholder ainda está lá
    if google_api_key == "xxx":
         return "Erro: Por favor, substitua 'SUA_CHAVE_DA_API_AQUI' pela sua chave de API real no arquivo curiosidade.py."

    try:
        # Configura a chave da API
        genai.configure(api_key=google_api_key)


        # Use um modelo adequado para gerar texto
        model_name = "gemini-2.0-flash" 
        model = genai.GenerativeModel(model_name=model_name)


        # Define o prompt para o modelo
        prompt = "Através do site: https://www.hltv.org/team/8297/furia cite somente uma curiosidde sobre a FURIA de CS2. essa curiosidade precisa ser sobre algum dos jogadores da line atual:KSCERATO, yuurih, FalleN, molodoy, YEKINDAR "

        print(f"Buscando informações sobre a FURIA '{model_name}' com a API do Gemini...")
        # Realiza a chamada da API
        response = model.generate_content(prompt)

        # --- VERIFICAÇÃO E TRATAMENTO DA RESPOSTA ---

        # Verifica se a resposta contém texto
        if response and hasattr(response, 'text') and response.text:
            # Retorna o texto completo gerado pela API
            return response.text
        elif response and hasattr(response, 'candidates') and response.candidates:
             # Se não há texto mas há candidatos, pode ter sido bloqueado
             # Acessa o feedback para entender por que o conteúdo foi bloqueado, se for o caso
             feedback = response.prompt_feedback
             if feedback and hasattr(feedback, 'block_reason'):
                  block_reason = feedback.block_reason
                  # Em versões mais antigas da lib ou dependendo do cenário, finish_reason pode ser mais útil
                  if hasattr(response.candidates[0], 'finish_reason'):
                       finish_reason = response.candidates[0].finish_reason
                       return f"A API do Gemini bloqueou o conteúdo. Razão: {finish_reason} (Feedback: {block_reason})"
                  else:
                       return f"A API do Gemini bloqueou o conteúdo. Feedback: {block_reason}"
             else:
                if hasattr(response.candidates[0], 'finish_reason'):
                     finish_reason = response.candidates[0].finish_reason
                     return f"A API do Gemini não retornou texto e o candidato tem finish_reason: {finish_reason}. O conteúdo pode ter sido bloqueado ou incompleto."
                else:
                     return "A API do Gemini retornou uma resposta inesperada sem texto ou feedback claro."
        elif response and hasattr(response, 'prompt_feedback') and response.prompt_feedback:
             # Caso não haja texto nem candidatos, pode haver feedback no prompt
             feedback = response.prompt_feedback
             return f"A API do Gemini retornou feedback no prompt: {feedback}. O conteúdo pode ter sido problemático."
        else:
            # Resposta vazia ou inesperada
            return "A API do Gemini retornou uma resposta vazia ou inesperada."

    # CAPTURA DE ERROS ESPECÍFICOS DA API USANDO google.api_core.exceptions
    except google.api_core.exceptions.NotFound as e:
        # Erro específico para modelo não encontrado
        return f"Erro de API (NotFound): O modelo '{model_name}' não foi encontrado ou não está disponível. Mensagem: {e}. Descomente o bloco 'VERIFIQUE OS MODELOS DISPONÍVEIS' no código para listar os modelos válidos."
    except google.api_core.exceptions.InvalidArgument as e:
        # Erro específico para argumento inválido (como API key inválida)
        return f"Erro de API (InvalidArgument): {e}. Por favor, verifique sua chave de API no arquivo curiosidade.py."
    except google.api_core.exceptions.GoogleAPIError as e:
        # Captura outros erros gerais da API do Google Cloud
        return f"Ocorreu um erro da API do Google: {e}"
    except Exception as e:
        # Captura quaisquer outras exceções inesperadas
        return f"Ocorreu um erro inesperado ao usar a API do Gemini: {e}"

# Este bloco só será executado se você rodar o arquivo diretamente (python curiosidade.py)
# Não será executado se você importar a função em outro script.
if __name__ == "__main__":
    print("--- Executando curiosidade.py diretamente ---")
    informacoes_furia = buscar_curiosidades_furia()
    print(informacoes_furia)
    print("------------------------------------------")