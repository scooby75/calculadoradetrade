import streamlit as st

# Funções Auxiliares
def calcular_retornos_e_lucros(stakes, odds, stake_total):
    """Calcula retornos e lucros para cada mercado."""
    retornos = {mercado: stakes[mercado] * odds[mercado] for mercado in stakes}
    lucros = {mercado: retorno - stake_total for mercado, retorno in retornos.items()}
    return retornos, lucros

def calcular_stakes(stake_total, lucro_desejado, odds):
    """Calcula as stakes para garantir lucro positivo em todos os mercados."""
    stakes = {}

    # Calcular stake mínima necessária para garantir lucro em cada mercado
    for mercado, odd in odds.items():
        stakes[mercado] = (stake_total + lucro_desejado) / odd

    # Ajustar stakes proporcionalmente ao total disponível
    total_stakes = sum(stakes.values())
    if total_stakes > stake_total:
        ajuste = stake_total / total_stakes
        stakes = {mercado: stake * ajuste for mercado, stake in stakes.items()}

    # Calcular retornos e lucros
    retornos, lucros = calcular_retornos_e_lucros(stakes, odds, stake_total)

    # Verificar se o lucro é positivo em todos os mercados
    if min(lucros.values()) < lucro_desejado:
        st.warning("Não foi possível garantir lucro positivo para todos os mercados com as odds e stakes fornecidas.")
    
    return {"stakes": stakes, "retornos": retornos, "lucros": lucros}

# Interface do Streamlit
st.title("Calculadora de Dutching HT")

# Entradas do usuário
stake_total = st.number_input("Stake Total", min_value=0.0, value=10.0, step=0.1)
lucro_desejado = st.number_input("Lucro Desejado", min_value=0.0, value=2.0, step=0.1)

# Odds para cada mercado
odds = {
    "0x0": st.number_input("Odd para 0x0", min_value=1.01, value=30.0, step=0.1),
    "25HT": st.number_input("Odd para Over 2.5 HT", min_value=1.01, value=5.1, step=0.1),
    "05HT": st.number_input("Odd para Over 0.5 HT", min_value=1.01, value=1.6, step=0.1),
    "15HT": st.number_input("Odd para Over 1.5 HT", min_value=1.01, value=2.5, step=0.1),
}

# Botão para calcular
if st.button("Calcular"):
    # Validação de entradas
    if stake_total <= 0:
        st.error("Stake total deve ser maior que 0.")
    elif lucro_desejado < 0:
        st.error("Lucro desejado deve ser não-negativo.")
    elif any(odd <= 1.0 for odd in odds.values()):
        st.error("Todas as odds devem ser maiores que 1.0.")
    else:
        # Cálculo dos resultados
        resultado = calcular_stakes(stake_total, lucro_desejado, odds)
        
        # Exibir resultados
        st.subheader("Resultados")
        st.write("Stakes por mercado:")
        st.json(resultado["stakes"])

        st.write("Retornos por mercado:")
        st.json(resultado["retornos"])

        st.write("Lucros por mercado:")
        st.json(resultado["lucros"])
