import streamlit as st

# Função para calcular stakes
def calcular_stakes(stake_total, lucro_desejado, odd_0x0, odd_25ht, odd_05ht, odd_15ht):
    stakes = {}
    
    # Calcular stake para cada mercado
    stakes['0x0'] = (stake_total + lucro_desejado) / odd_0x0
    stakes['25HT'] = (stake_total + lucro_desejado) / odd_25ht
    stakes['05HT'] = (stake_total + lucro_desejado) / odd_05ht
    stakes['15HT'] = (stake_total + lucro_desejado) / odd_15ht

    # Ajustar stakes para caber no stake total
    ajuste = stake_total / sum(stakes.values())
    stakes = {mercado: stake * ajuste for mercado, stake in stakes.items()}

    # Calcular retornos
    retornos = {
        mercado: stake * odd for mercado, (stake, odd) in zip(
            stakes.keys(), 
            [(stakes['0x0'], odd_0x0), 
             (stakes['25HT'], odd_25ht), 
             (stakes['05HT'], odd_05ht), 
             (stakes['15HT'], odd_15ht)]
        )
    }

    # Calcular lucros (retorno - stake total)
    lucros = {mercado: retorno - stake_total for mercado, retorno in retornos.items()}

    # Verificar e ajustar lucro mínimo para todos os mercados
    while min(lucros.values()) < lucro_desejado:
        stakes = {mercado: stake * 1.01 for mercado, stake in stakes.items()}  # Incremento pequeno para ajustar
        ajuste = stake_total / sum(stakes.values())
        stakes = {mercado: stake * ajuste for mercado, stake in stakes.items()}
        retornos = {
            mercado: stake * odd for mercado, (stake, odd) in zip(
                stakes.keys(), 
                [(stakes['0x0'], odd_0x0), 
                 (stakes['25HT'], odd_25ht), 
                 (stakes['05HT'], odd_05ht), 
                 (stakes['15HT'], odd_15ht)]
            )
        }
        lucros = {mercado: retorno - stake_total for mercado, retorno in retornos.items()}

    # Resultado final
    resultado = {
        "stakes": stakes,
        "retornos": retornos,
        "lucros": lucros
    }
    return resultado

# Interface do Streamlit
st.title("Dutching HT")

# Entradas do usuário
stake_total = st.number_input("Stake Total", min_value=0.0, value=10.0, step=0.1)
lucro_desejado = st.number_input("Lucro Desejado", min_value=0.0, value=2.0, step=0.1)
odd_0x0 = st.number_input("Odd para 0x0", min_value=1.0, value=30.0, step=0.1)
odd_25ht = st.number_input("Odd para Over 2.5 HT", min_value=1.0, value=5.1, step=0.1)
odd_05ht = st.number_input("Odd para Over 0.5 HT", min_value=1.0, value=1.6, step=0.1)
odd_15ht = st.number_input("Odd para Over 1.5 HT", min_value=1.0, value=2.5, step=0.1)

# Botão para calcular
if st.button("Calcular"):
    resultado = calcular_stakes(stake_total, lucro_desejado, odd_0x0, odd_25ht, odd_05ht, odd_15ht)
    
    # Exibir os resultados
    st.subheader("Resultados")
    st.write("Stakes por mercado:")
    st.json(resultado['stakes'])

    st.write("Retornos por mercado:")
    st.json(resultado['retornos'])

    st.write("Lucros por mercado:")
    st.json(resultado['lucros'])
