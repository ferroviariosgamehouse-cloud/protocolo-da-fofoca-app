import streamlit as st
import requests
import json
import pandas as pd
import time

st.title("🗣️ Protocolo de Fofocas")

url = "https://anypoint.mulesoft.com/mocking/api/v1/links/001ec433-4dda-4176-8c2b-105a425ce25a/fofoca"

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




# Configuração da Página
st.write("Monitor de Fofocas via API:")



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

# Sidebar para controle
st.sidebar.header("Configurações")
auto_refresh = st.sidebar.checkbox("Atualização Automática (5s)", value=True)

# Lógica de atualização
if "last_update" not in st.session_state:
    st.session_state.last_update = time.time()

# Busca os dados
dados = fetch_fofocas_from_mule()

if not dados:
    st.info("Aguardando novas fofocas serem processadas...")
else:
    # Mostra os dados em métricas no topo
    st.columns(3)[0].metric("Total de Fofocas:", len(dados))
    
    st.divider()

    # Exibição em Grid
    cols = st.columns(3)
    for idx, item in enumerate(dados):
        with cols[idx % 3]:
            with st.container(border=True):
                # Ajuste os campos abaixo conforme o JSON que seu Mule retorna
                categoria = item.get("categoria", "Geral").upper()
                emissor = item.get("emissor", "Anônimo")
                msg = item.get("mensagem", "...")
                
                st.markdown(f"### 📍 {categoria}")
                st.caption(f"Enviado por: {emissor}")
                st.write(msg)

# Script de auto-refresh simples
if auto_refresh:
    time.sleep(5)
    st.rerun()