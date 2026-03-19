import streamlit as st
import requests
import json
import pandas as pd
import time

st.set_page_config(page_title="MuleSoft", layout="wide")

st.title("🗣️ Protocolo de Fofocas")

url = "https://anypoint.mulesoft.com/mocking/api/v1/links/15a23c7c-fc30-4cb2-99f0-18868470d8bd/fofoca"

col_envio, col_monitor = st.columns([1, 1.5], gap="large")


with col_envio:
    st.header("📤 Enviar Nova Fofoca")
    # O segredo está aqui: tudo que compõe o formulário fica "dentro" do WITH
    with st.form("fofoca_form"):
        st.write("Preencha os dados da fofoca:")
        
        # Campos do formulário
        emissor = st.text_input("Quem contou?")
        categoria = st.selectbox("Setor", ["TI", "RH", "Diretoria"])
        conteudo = st.text_area("O Segredo")
        
        # ESTE BOTÃO PRECISA ESTAR AQUI DENTRO DO 'WITH'
        submitted = st.form_submit_button("Espalhar Fofoca! 🚀")

# A lógica de envio acontece DEPOIS que o botão é clicado
if submitted:
    if conteudo:
        payload = {
            "emissor": emissor,
            "categoria": categoria.lower(),
            "mensagem": conteudo
        }
        
        try:
            
            # O timeout de 2 segundos evita que o Streamlit trave se o Mule estiver offline
            response = requests.post(url, json=payload, timeout=2)
            
            if response.status_code in [200, 201]:
                st.success("✅ O Mule recebeu a fofoca!")                
            else:
                st.error(f"❌ Erro no Mule: {response.status_code}")
        except Exception as e:
            st.error(f"❌ Erro de conexão: Verifique se o Mule está rodando no 8081")
    else:
        st.warning("Escreva a fofoca antes de enviar!")


with col_monitor:

    # Função para consumir a API do Mule
    def fetch_fofocas_from_mule():
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                return response.json()
            else:
                st.error(f"Erro na API do Mule: {response.status_code}")
                return []
        except Exception as e:
            st.error(f"Não foi possível conectar à API: {e}")
            return []

# Espaço para os cards
    
placeholder = st.empty()

def get_notification_style(count):
    # Dicionário para transformar números normais em sobrescrito (¹ ² ³ ⁴...)
    superscripts = str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹")
    
    # Transforma o número, ex: 5 vira ⁵
    count_top = str(count).translate(superscripts)
    
    # Retorna o ícone + o número no alto em negrito
    return count_top

with placeholder.container():
    dados = fetch_fofocas_from_mule()
    if dados is None:
            st.warning("Não foi possível conectar à API de leitura do Mule.")
    elif not dados:
            st.info("Nenhuma fofoca processada ainda...")
    else:            
                        
            st.header("📥 Total de Fofocas " + get_notification_style(len(dados)))
            
            
            
            cols = st.columns(3)           
            for idx, item in enumerate(dados): 
                with cols[idx % 3]:
                    with st.container(border=True):
                        
                        categoria = item.get("categoria", "Geral").upper()
                        emissor = item.get("emissor", "Anônimo")
                        msg = item.get("mensagem", "...")
                        
                        st.markdown(f"### 📍 {categoria}")
                        st.caption(f"Enviado por: {emissor}")
                        st.write(msg)
                        

if st.button("🔄 Forçar Atualização"):
        st.rerun()

# Sidebar para controle
st.sidebar.header("Configurações")
auto_refresh = st.sidebar.checkbox("Atualização Automática (20s)", value=True)

# Lógica de atualização
if "last_update" not in st.session_state:
    st.session_state.last_update = time.time()

# Script de auto-refresh simples
if auto_refresh:
    time.sleep(20)
    st.rerun()