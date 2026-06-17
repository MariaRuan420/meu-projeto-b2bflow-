import os
import sys
import logging
import requests
from dotenv import load_dotenv
from supabase import create_client, Client

# 1. Configuração de Logs para monitoramento do fluxo
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# 2. Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
ZAPI_INSTANCE_ID = os.getenv("ZAPI_INSTANCE_ID")
ZAPI_TOKEN = os.getenv("ZAPI_TOKEN")
ZAPI_CLIENT_TOKEN = os.getenv("ZAPI_CLIENT_TOKEN")

# Validação das credenciais obrigatórias
if not all([SUPABASE_URL, SUPABASE_KEY, ZAPI_INSTANCE_ID, ZAPI_TOKEN]):
    logging.error("Erro: Variáveis de ambiente faltando no arquivo .env!")
    sys.exit(1)


def buscar_contatos_supabase() -> list:
    """Conecta ao Supabase e busca os primeiros 3 contatos da tabela."""
    try:
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
        
        # Busca apenas as colunas necessárias e limita a 3 registros
        resposta = supabase.table("contatos").select("nome, telefone").limit(3).execute()
        
        contatos = resposta.data
        logging.info(f"Sucesso: {len(contatos)} contatos recuperados do Supabase.")
        return contatos
    except Exception as e:
        logging.error(f"Erro ao conectar ou buscar dados no Supabase: {e}")
        return []


def enviar_mensagem_zapi(nome: str, telefone: str) -> bool:
    """Envia a mensagem padronizada para um contato via API da Z-API."""
    # Garante a formatação do número limpo apenas com dígitos
    numero_formatado = "".join(filter(str.isdigit, str(telefone)))
    if not numero_formatado.startswith("55"):
        numero_formatado = f"55{numero_formatado}"

    url = f"https://api.z-api.io/instances/{ZAPI_INSTANCE_ID}/token/{ZAPI_TOKEN}/send-text"
    
    # Cabeçalhos completos para evitar o bloqueio do servidor da Z-API
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    # Se você tiver o Client-Token no painel da Z-API, certifique-se de colocá-lo no .env
    if ZAPI_CLIENT_TOKEN:
        headers["Client-Token"] = ZAPI_CLIENT_TOKEN
    
    payload = {
        "phone": numero_formatado,
        "message": f"Olá, {nome} tudo bem com você?"
    }

    try:
        # Enviamos a requisição
        resposta = requests.post(url, json=payload, headers=headers, timeout=15)
        
        # A Z-API costuma retornar status 200 ou 201 para sucesso
        if resposta.status_code in [200, 201]:
            logging.info(f"Mensagem enviada com sucesso para {nome} ({numero_formatado}).")
            return True
        else:
            logging.error(f"Falha ao enviar para {nome}. Status: {resposta.status_code} - Resposta: {resposta.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        logging.error(f"Erro de rede ao comunicar com a Z-API para o contato {nome}: {e}")
        return False


def main():
    logging.info("Iniciando o processo de automação de mensagens...")
    
    # Executa o passo 1: Busca os dados
    lista_contatos = buscar_contatos_supabase()
    
    if not lista_contatos:
        logging.warning("Nenhum contato encontrado ou erro na busca. Processo encerrado.")
        return

    # Executa o passo 2: Itera e envia as mensagens (limitado a 3 pela busca)
    for contato in lista_contatos:
        nome_contato = contato.get("nome")
        telefone_contato = contato.get("telefone")
        
        if nome_contato and telefone_contato:
            enviar_mensagem_zapi(nome_contato, telefone_contato)
        else:
            logging.warning(f"Contato com dados incompletos ignorado: {contato}")

    logging.info("Processo de envio finalizado.")


if __name__ == "__main__":
    main()