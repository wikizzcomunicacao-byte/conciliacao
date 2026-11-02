import streamlit as st
import pandas as pd
from ofxparse import OfxParser

# Configuração da página para o modo wide (aproveita melhor a largura da tela)
st.set_page_config(
    page_title="SaaS Contábil - Conciliação Bancária",
    page_icon="💼",
    layout="wide"
)

# Estilo visual limpo para o dashboard
st.title("💼 SaaS Contábil Inteligente")
st.markdown("### Módulo 2: Conciliação Bancária Automatizada (OFX + IA)")

# Barra lateral para navegação entre os módulos futuros
st.sidebar.header("Navegação do SaaS")
modulo = st.sidebar.selectbox(
    "Escolha o Módulo:",
    ["Conciliação Bancária (OFX)", "Ingestão de Documentos (OCR)", "Monitoramento SERPRO", "Gestão eSocial", "CRM de Cobrança"]
)

if modulo == "Conciliação Bancária (OFX)":
    st.info("Carregue o extrato bancário em formato `.ofx` fornecido pelo cliente para iniciar a conciliação automática.")

    # Área de Upload do Arquivo OFX
    uploaded_file = st.file_uploader("Arraste ou selecione o ficheiro .ofx", type=["ofx"])

    if uploaded_file is not None:
        try:
            # Processa o arquivo OFX
            ofx = OfxParser.parse(uploaded_file)
            conta = ofx.account
            extrato = conta.statement
            
            transacoes = []
            for t in extrato.transactions:
                valor = float(t.amount)
                # Regra universal: valor positivo é Crédito, negativo é Débito
                tipo_transacao = "Crédito" if valor > 0 else "Débito"
                
                transacoes.append({
                    "Data": t.date.strftime("%Y-%m-%d"),
                    "Valor (R$)": valor,
                    "Tipo": tipo_transacao,
                    "Histórico Bancário": t.memo,
                    "Status": "Pendente"
                })
                
            df = pd.DataFrame(transacoes)
            
            # Métricas rápidas no topo recalculadas corretamente
            total_transacoes = len(df)
            total_creditos = len(df[df["Tipo"] == "Crédito"])
            total_debitos = len(df[df["Tipo"] == "Débito"])
            
            col1, col2, col3 = st.columns(3)
            col1.metric("Total de Transações", total_transacoes)
            col2.metric("Créditos Encontrados", total_creditos)
            col3.metric("Débitos Encontrados", total_debitos)
            
            st.markdown("---")
            st.subheader("Extrato Importado")
            
            # Exibe a tabela interativa
            st.dataframe(df, use_container_width=True)
            
            # Botão para disparar o motor de conciliação
            if st.button("🚀 Executar Conciliação Inteligente (Match + IA)", type="primary"):
                with st.spinner("A cruzar dados com notas fiscais e a aplicar o motor de inteligência..."):
                    # Simulando o resultado da conciliação baseada em regras e IA
                    df["Status"] = "Conciliado (Match Exato)"
                    
                st.success("Conciliação concluída com sucesso! 95% dos lançamentos processados automaticamente.")
                
                # Exibe a tabela atualizada com os status resolvidos
                st.subheader("Resultado da Conciliação")
                st.dataframe(df, use_container_width=True)
                
        except Exception as e:
            st.error(f"Erro ao processar o arquivo OFX: {e}")

else:
    st.warning(f"O módulo '{modulo}' está configurado para as próximas etapas do desenvolvimento.")
