import json
import pandas as pd
import requests
import streamlit as st

# ============ CONFIGURAÇÃO ============
OLLAMA_URL = "http://localhost:11434/api/generate"
MODELO = "qwen2.5"

# ============ CARREGAR DADOS ============
acervo = pd.read_csv("./data/acervo_moedas.csv")
denominacoes = json.load(open("./data/denominacoes.json", encoding="utf-8"))
perfil = json.load(open("./data/perfil_colecionador.json", encoding="utf-8"))

# ============ MONTAR CONTEXTO ============
contexto = f"""
CLIENTE: {perfil['nome_colecionador']}, {perfil['perfil']}, perfil {perfil['nivel_conhecimento']}
OBJETIVO: {perfil['objetivo_do_acervo']}
PAÍSES FOCO: {perfil['paises_foco']}

DENOMINAÇÕES DISPONÍVEIS:
{json.dumps(denominacoes, indent=2, ensure_ascii=False)}
"""

# ============ SYSTEM PROMPT ============
SYSTEM_PROMPT = """Você é o Numo, um curador e educador numismático amigável e didático.

OBJETIVO:
Ajudar o colecionador a entender o acervo e a história por trás das moedas,
usando os dados catalogados como exemplos concretos.

FONTE DA VERDADE (não negociável):
- Os dados de cada moeda vêm da CAMADA 1 (acervo catalogado).
- O contexto histórico da denominação vem da CAMADA 2 (base de denominações).
- Use APENAS o que estiver no contexto fornecido a cada pergunta. 

REGRAS:
- NUNCA avalie preço nem faça precificação. Você educa e contextualiza,
  não diz quanto uma moeda vale;
- NUNCA recomende comprar, vender ou guardar como investimento;
- NUNCA invente dados (ano, metal, tiragem, casa da moeda). Se a informação
  não estiver no contexto, diga com naturalidade que não tem aquele dado;
- EVITE superlativos históricos ("a primeira", "a única", "a mais rara")
  a menos que estejam explícitos na base;
- Se o contexto trouxer um campo CUIDADO para a denominação, RESPEITE-O;
- JAMAIS responda a perguntas fora do tema numismática / história monetária.
  Quando ocorrer, lembre com gentileza o seu papel;
- Use linguagem simples e acolhedora, como quem conversa com um colecionador
  experiente, sem jargão desnecessário;
- Termine quase sempre com um convite para aprofundar;
- Responda de forma sucinta e direta.
"""
# ============ CHAMAR OLLAMA ============
def perguntar(msg):
    prompt = f"""
    {SYSTEM_PROMPT}

    CONTEXTO DO CLIENTE:
    {contexto}

    Pergunta: {msg}"""

    r = requests.post(OLLAMA_URL, json={"model": MODELO, "prompt": prompt, "stream": False})
    return r.json()['response']


# ============ INTERFACE ============
st.title("Numo, o Agente Numismata Inteligente")

if pergunta := st.chat_input("Sua dúvida sobre seu acervo..."):
    st.chat_message("user").write(pergunta)
    with st.spinner("..."):
        st.chat_message("assistant").write(perguntar(pergunta))
