import streamlit as st

# Funções auxiliares
def calcular_retornos_e_lucros(stakes, odds, stake_total):
    """Calcula retornos e lucros para cada mercado."""
    retornos = {mercado: stake * odd for mercado, (stake, odd) in zip(stakes.keys(), odds.items())}
    lucros = {mercado: retorno - stake_total for mercado, retorno in retornos.items()}
    return retornos, lucros

def ajustar_stakes(stakes, stake_total):
    """Ajusta as stakes para caber no total permitido."""
    ajuste = stake_total / sum(stakes.values())
    return {mercado: stake * ajuste for mercado, stake in stakes.items()}

# Função principal
def calcular_stakes(stake_total, lucro_desejado, odds):
    stakes = {mercado: (stake_total + lucro_desejado) / odd for mercado, odd in odds.items()}
    stakes = ajustar_stakes(stakes, stake_total)
    retornos, lucros = calcular_retornos_e_lucros(stakes, odds, stake_total)

    # Ajustar stakes até atingir o lucro desejado
    while min(lucros.values()) < lucro_desejado:
        stakes = {mercado: stake * 1.01 for mercado, stake in stakes.items()}
        stakes = ajustar_stakes(stakes, stake_total)
        retornos, lucros = calcular_retornos_e_lucros(stakes, odds, stake_total)

    return {"stakes": stakes, "retornos": retornos, "lucros": lucros}

# Interface do Streamlit
st.title("Dutching HT")

# Entradas do usuário
stake_total = st.number_input("Stake Total", min_value=0.0, value=10.0, step=0.1)
lucro_desejado = st.number_input("Lucro Desejado", min_value=0.0, value=2.0, step=0.1)

# Odds para cada mercado
odds = {
    "0x0": st.number_input("Odd para 0x0", min_value=1.0, value=30.0, step=0.1),
    "25HT": st.number_input("Odd para Over 2.5 HT", min_value=1.0, value=5.1, step=0.1),
    "05HT": st.number_input("Odd para Over 0.5 HT", min_value=1.0, value=1.6, step=0.1),
    "15HT": st.number_input("Odd para Over 1.5 HT", min_value=1.0, value=2.5, step=0.1),
}

# Botão para calcular
if st.button("Calcular"):
    if any(odd <= 1.0 for odd in odds.values()):
        st.error("Todas as odds devem ser maiores que 1.0!")
    elif stake_total <= 0 or lucro_desejado < 0:
        st.error("Stake total deve ser maior que 0 e lucro desejado deve ser não-negativo.")
    else:
        resultado = calcular_stakes(stake_total, lucro_desejado, odds)
        
        # Exibir os resultados
        st.subheader("Resultados")
        st.write("Stakes por mercado:")
        st.json(resultado['stakes'])

        st.write("Retornos por mercado:")
        st.json(resultado['retornos'])

        st.write("Lucros por mercado:")
        st.json(resultado['lucros'])
