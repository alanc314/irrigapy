import streamlit as st
import math 
import pandas as pd

def infos_aba2():
    st.subheader("O App")
    st.markdown("O IrrigaPY é um app criado na linguagem Python com foco nos cálculos de dimensionamento de sistema de irrigação por aspersão convencional. O objetivo do app é facilitar o dimensionamento desse sistema de maneira acessível e prática. Criado por Alan C F Fernandes e João Guilherme S Pedreira (2024) para a disciplina Introdução a Programação de Computadores Aplicada a Ciências Biológicas (CEN0336).")  

def infos_aba3():
    st.subheader("Entrada dos Parâmetros")

   
    st.subheader("Área")
    largura = st.number_input("Qual a largura da área a ser irrigada em m?", min_value = 0.1)
    st.write("Considere a largura da área como o eixo de disposição das linhas laterais do sistema de irrigação.")
    
    comprimento = st.number_input("Qual o comprimento da área a ser irrigada em m?", min_value = 0.1)
    st.write("Considere o comprimento da área como o eixo de disposição da linha principal do sistema de irrigação.")
    area = comprimento * largura / 10000
    st.write(f'A área a ser irrigada é de {area:.4f} ha.')
    
    declividade_largura = st.number_input("Qual a declividade ao longo da largura da área em %?", min_value = 0.0)
    
    declividade_comprimento = st.number_input("Qual a declividade ao longo do comprimento da área em %?", min_value = 0.0)
    
    dist_moto_bomba = st.number_input("Qual a distância do início da linha principal a moto-bomba em m?", min_value = 0.1)
    
    declividade_moto_bomba = st.number_input("Qual a declividade entre a linha principal e a moto-bomba área em %?", min_value = 0.0)
    
    

    
    st.subheader("Solo")
    ucc = st.number_input("Qual a umidade na capacidade de campo do solo da área em %?", min_value = 0.1, max_value = 100.0)
    upmp = st.number_input("Qual a umidade no ponto de murcha permanente do solo da área em %?", min_value = 0.1, max_value = 100.0)
    ds = st.number_input("Qual a densidade do solo da área em g/cm³?", min_value = 0.1)
    vib = st.number_input("Qual a velocidade de infiltração básica (VIB) do solo da área em mm/h?", min_value = 0.1)

    st.subheader("Parâmetros da Cultura")
    culturas = {"soja": {"profundidade_raiz": 25, "fator": 0.35, "kc": 1.10},
    "milho": {"profundidade_raiz": 175, "fator": 0.40, "kc": 1.15},
    "arroz": {"profundidade_raiz": 75, "fator": 0.30, "kc": 1.15},
    "feijão": {"profundidade_raiz": 90, "fator": 0.35, "kc": 1.00},
    "trigo": {"profundidade_raiz": 125, "fator": 0.35, "kc": 0.95},
    "tomate": {"profundidade_raiz": 75, "fator": 0.35, "kc": 1.00},
    "alface": {"profundidade_raiz": 30, "fator": 0.25, "kc": 0.85},
    "cenoura": {"profundidade_raiz": 40, "fator": 0.30, "kc": 0.90},
    "batata": {"profundidade_raiz": 50, "fator": 0.30, "kc": 0.90},
    "cebola": {"profundidade_raiz": 40, "fator": 0.30, "kc": 0.85}}
    
    cultura = st.selectbox("Qual cultura será irrigada?", list(culturas.keys()) + ["Adicionar uma nova cultura"])

    
    if cultura == "Adicionar uma nova cultura":
        outra_cultura = st.text_input("Qual a nova cultura?")
        if outra_cultura:
            z_outra_cultura = st.number_input("Qual a profundidade da raiz dessa nova cultura em cm?", min_value = 0.1)
            f_outra_cultura = st.number_input("Qual o fator f dessa nova cultura?", min_value = 0.1)
            kc_outra_cultura = st.number_input("Qual o Kc dessa nova cultura?", min_value = 0.1)

            salvar = st.button("Salvar nova cultura")
            
            if salvar:  
                culturas[outra_cultura] = {
                    "profundidade_raiz": z_outra_cultura,
                    "fator": f_outra_cultura,
                    "kc": kc_outra_cultura
                }
                z = z_outra_cultura
                st.session_state.z = z
                
                f = f_outra_cultura
                st.session_state.f = f
                
                kc = kc_outra_cultura
                st.session_state.kc = kc
                
                st.success(f"A cultura {outra_cultura} foi adicionada com sucesso!")
                   

    else:
        z = culturas[cultura]["profundidade_raiz"]
        st.session_state.z = z
        
        f = culturas[cultura]["fator"]
        st.session_state.f = f
        
        kc = culturas[cultura]["kc"]
        st.session_state.kc = kc
                
    
    st.subheader("Clima")
    eto = st.number_input("Qual a ETo máx para sua região, considerando sua cultura em mm/d?", min_value = 0.1)

    st.subheader("Jornada de Trabalho")
    jornada_trab = st.number_input("Qual a jornada de trabalho em horas por dia?", min_value = 0.1, max_value = 24.0)

    st.subheader("Aspersor")
    nome_aspersor = st.text_input("Qual o nome do aspersor que irá utilizar?")
    dist_entre_aspersor = st.number_input("Qual a distância entre aspersores utilizada em m?", min_value = 0.1)
    dist_entre_linha = st.number_input("Qual a distância entre linhas de aspersores utilizada em m?", min_value = 0.1)
    pressao_servico = st.number_input("Qual a pressão de serviço do emissor utilizado em mca?", min_value = 0.1)
    altura_aspersor = st.number_input("Qual a altura do aspersor utilizado em m?", min_value = 0.1)
    vazao = st.number_input("Qual a vazão do aspersor utilizado em m³/h?", min_value = 0.1)
    int_aplicacao = (vazao * 1000) / (dist_entre_aspersor *  dist_entre_linha)

    if int_aplicacao and vib:
        if int_aplicacao > vib:
            st.write("O aspersor utilizado retorna uma intensidade de aplicação maior que a VIB do solo, o que pode acarretar no encharcamento da área. Considere escolher um aspersor de menor vazão.")
            vazao = (vib * dist_entre_aspersor * dist_entre_linha) / 1000
            st.write(f"Considere utilizar uma vazão de até {vazao:.2f} m³/h para o espaçamento utilizado.")             

    st.session_state.largura = largura
    st.session_state.comprimento = comprimento 
    st.session_state.area = area 
    st.session_state.declividade_largura = declividade_largura
    st.session_state.declividade_comprimento = declividade_comprimento
    st.session_state.dist_moto_bomba = dist_moto_bomba  
    st.session_state.declividade_moto_bomba = declividade_moto_bomba
    st.session_state.ucc = ucc
    st.session_state.upmp = upmp
    st.session_state.ds = ds
    st.session_state.vib = vib
    if cultura == "Adicionar uma nova cultura":
        st.session_state.cultura = outra_cultura
    else:
        st.session_state.cultura = cultura
    st.session_state.eto = eto
    st.session_state.jornada_trab = jornada_trab
    st.session_state.nome_aspersor = nome_aspersor
    st.session_state.dist_entre_aspersor = dist_entre_aspersor
    st.session_state.dist_entre_linha = dist_entre_linha
    st.session_state.pressao_servico = pressao_servico
    st.session_state.altura_aspersor = altura_aspersor
    st.session_state.vazao = vazao
    st.session_state.int_aplicacao = int_aplicacao

    if vazao > 0.1:
        st.write('Vá para a aba do Menu "Resultado do Dimensionamento".')
        

def infos_aba4():
    st.subheader("Resultado do Dimensionamento")
    chaves = ["largura", "comprimento", "area", "declividade_largura", "declividade_comprimento", "dist_moto_bomba", "declividade_moto_bomba", "ucc", "upmp", "ds", "vib", "cultura", "eto", "jornada_trab", "nome_aspersor", "dist_entre_aspersor", "dist_entre_linha", 
        "pressao_servico", "altura_aspersor", "vazao", "int_aplicacao", "z", "kc", "f"]
    
    if all(chave in st.session_state for chave in chaves):
        largura = st.session_state.largura
        comprimento = st.session_state.comprimento
        area = st.session_state.area
        declividade_largura = st.session_state.declividade_largura
        declividade_comprimento = st.session_state.declividade_comprimento
        dist_moto_bomba = st.session_state.dist_moto_bomba
        declividade_moto_bomba = st.session_state.declividade_moto_bomba
        ucc = st.session_state.ucc
        upmp = st.session_state.upmp
        ds = st.session_state.ds
        vib = st.session_state.vib
        cultura = st.session_state.cultura
        eto = st.session_state.eto
        jornada_trab = st.session_state.jornada_trab
        nome_aspersor = st.session_state.nome_aspersor
        dist_entre_aspersor = st.session_state.dist_entre_aspersor
        dist_entre_linha = st.session_state.dist_entre_linha
        pressao_servico = st.session_state.pressao_servico
        altura_aspersor = st.session_state.altura_aspersor
        vazao = st.session_state.vazao
        int_aplicacao = st.session_state.int_aplicacao
        z = st.session_state.z
        f = st.session_state.f
        kc = st.session_state.kc 
        
        
        dra = ((ucc - upmp) * ds * z * f) / 10
        turno_rega = (dra) / (eto * kc) # quando tempo eu demoro para voltar a irrigar a área ou a parcela da área
        lam_liq_de_irrigacao = eto * kc * turno_rega
        lam_bruta_de_irrigacao = lam_liq_de_irrigacao / 0.8 # eficiência do sistema de irrigação
        
        tempo_irrigacao = lam_bruta_de_irrigacao / int_aplicacao     
        
        num_posicoes_irrigados_area_total = 2 * ((comprimento / dist_entre_linha))
       
        num_linhas_irrigadas_simultaneas = 2 
        
        num_aspersores_por_linha_lateral = ((largura / 2) / dist_entre_aspersor)
        
        vazao_por_linha_lateral = num_aspersores_por_linha_lateral * vazao
        vazao_linha_principal = vazao_por_linha_lateral * num_linhas_irrigadas_simultaneas
        
        comprimento_linha_lateral = (dist_entre_aspersor / 2) + (num_aspersores_por_linha_lateral - 1) * dist_entre_aspersor
        
        perda_de_carga_linha_lateral = 0.2 * pressao_servico # Critério de projeto
         
        pressao_inicio_linha_lateral = pressao_servico + 0.75 * perda_de_carga_linha_lateral + altura_aspersor 
    
        dist_centro_fim = num_posicoes_irrigados_area_total * dist_entre_linha
        dist_inicio_centro = dist_centro_fim
        dist_moto_bomba_inicio = dist_moto_bomba
    
        dist_moto_bomba_centro = dist_moto_bomba + dist_centro_fim
    
        
        vazao_total_simultanea_em_mm_por_seg = (num_linhas_irrigadas_simultaneas * (vazao_por_linha_lateral / 3600))
                                                
        diam_tubo_moto_bomba_centro = (1.030 * math.sqrt(vazao_total_simultanea_em_mm_por_seg)) * 100
        
        hf_moto_bomba_centro = (10.641 * (vazao_total_simultanea_em_mm_por_seg ** 1.852) * dist_moto_bomba_centro) / ((140 ** 1.852) * (diam_tubo_moto_bomba_centro ** 4.871))

        hf_centro_fim = ((10.641 * ((vazao_por_linha_lateral / 3600) ** 1.852)) * dist_centro_fim) / ((140 ** 1.852) * (diam_tubo_moto_bomba_centro ** 4.871))
       

        hf_total = hf_moto_bomba_centro + hf_centro_fim + pressao_inicio_linha_lateral + declividade_comprimento * comprimento + declividade_moto_bomba * dist_moto_bomba 
                          
        potencia_moto_bomba = ((num_linhas_irrigadas_simultaneas * (vazao_por_linha_lateral / 3600) * 100) * hf_total) / (75 * 0.7)
    
    
        cv_por_ha = potencia_moto_bomba / area
    
        

        dados = {
    "Parâmetros": [
        "Largura", "Comprimento", "Área", "Declividade da largura", "Declividade do comprimento",
        "Distância da motobomba a linha principal", "Declividade da motobomba", "Umidade do solo na capacidade de campo", 
        "Umidade do solo no ponto de murcha permanente", "Densidade do solo", "VIB", 
        "Cultura", "ETo", "Jornada de trabalho", "Nome do aspersor", "Distância entre aspersores", 
        "Distância entre as linhas laterais", "Pressão de serviço do aspersor", "Altura do aspersor", "Vazão do aspersor", 
        "Intensidade de aplicação", "Profundidade do sistema radicular", "Fator f", "Kc", 
        "Disponibilidade real de água no solo para a cultura", "Turno de rega", "Lâmina líquida de irrigação", 
        "Lâmina bruta de irrigação", "Tempo de irrigação", 
        "Número de posições irrigadas na área total",  
        "Número de linhas irrigadas simultâneas", "Número de aspersores por linha lateral", 
        "Vazão por linha lateral", "Vazão por linha principal", "Comprimento da linha lateral", 
        "Perda de carga na linha lateral", 
        "Pressão no início na linha lateral", "Diâmetro da tubo da motobomba", 
        "Potência da Motobomba", "Relação potência - área irrigada"
    ],
    "Valor": [
        st.session_state.largura, st.session_state.comprimento, st.session_state.area, 
        st.session_state.declividade_largura, st.session_state.declividade_comprimento, 
        st.session_state.dist_moto_bomba, st.session_state.declividade_moto_bomba, 
        st.session_state.ucc, st.session_state.upmp, st.session_state.ds, st.session_state.vib, 
        st.session_state.cultura, st.session_state.eto, st.session_state.jornada_trab, 
        st.session_state.nome_aspersor, st.session_state.dist_entre_aspersor, 
        st.session_state.dist_entre_linha, st.session_state.pressao_servico, 
        st.session_state.altura_aspersor, st.session_state.vazao, round(st.session_state.int_aplicacao, 2), 
        st.session_state.z, st.session_state.f, st.session_state.kc, 
        round(dra, 2), math.floor(turno_rega), round(lam_liq_de_irrigacao, 2), round(lam_bruta_de_irrigacao, 2), math.ceil(tempo_irrigacao), math.ceil(num_posicoes_irrigados_area_total), math.ceil(num_linhas_irrigadas_simultaneas), 
        math.ceil(num_aspersores_por_linha_lateral), round(vazao_por_linha_lateral, 2), round(vazao_linha_principal, 2), 
        round(comprimento_linha_lateral, 2), round(perda_de_carga_linha_lateral, 2),
        round(pressao_inicio_linha_lateral, 2), round(diam_tubo_moto_bomba_centro, 2), round(potencia_moto_bomba, 2), round(cv_por_ha, 2)
    ],
    "Unidade": [
        "m", "m", "ha", "%", "%",
        "m", "%", "%", "%", "g/cm³", "mm/h",
        "-", "mm", "h", "-", "m", 
        "m", "mca", "m", "mm/h", 
        "mm/h", "cm", "-", "-", 
        "mm", "d", "mm", 
        "mm", "h", "-", 
        "-", "-", "mm/h", "mm/h", "m", 
        "mca",
        "mca", "cm", "cv", "cv/ha"
    ]
}

        
        df = pd.DataFrame(dados)
        
        
        st.dataframe(df, width = 1200, height= 600)  
        
        csv = df.to_csv(index=False, sep=";")
        st.download_button(label = "Baixar tabela em CSV",
            data = csv,
            file_name = "dados_irrigaPy.csv",
            mime = "text/csv")

    else: 
        st.write("Por favor, insira todos os parâmetros necessários na aba 'Entrada dos Parâmetros' do Menu.")
        
        
def main():
    st.image("logo_irrigapy.png", width = 300)
    aba = st.sidebar.selectbox("Menu", ["", "O App", "Entrada dos Parâmetros", "Resultado do Dimensionamento"])
    
    if aba == "":
        st.subheader("Acesse o Menu")
    
    elif aba == "O App":
        infos_aba2()
    
    elif aba == "Entrada dos Parâmetros":
        infos_aba3()
        
    elif aba == "Resultado do Dimensionamento":
        infos_aba4()

if __name__ == "__main__":
    main()
