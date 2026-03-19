import streamlit as st
import requests
import json

st.title("🗣️ Protocolo de Fofoca")

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
            url = "http://localhost:8081/fofoca"
            # O timeout de 2 segundos evita que o Streamlit trave se o Mule estiver offline
            response = requests.post(url, json=payload, timeout=2)
            
            if response.status_code in [200, 201]:
                st.success("✅ O Mule recebeu a fofoca!")
                st.json(payload)
            else:
                st.error(f"❌ Erro no Mule: {response.status_code}")
        except Exception as e:
            st.error(f"❌ Erro de conexão: Verifique se o Mule está rodando no 8081")
    else:
        st.warning("Escreva a fofoca antes de enviar!")