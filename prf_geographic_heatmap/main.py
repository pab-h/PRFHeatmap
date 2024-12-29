import folium
import pandas as pd
import streamlit as st

from folium.plugins import HeatMap 
from streamlit_folium import st_folium

def preprocessDatafranDf(datatran):
    datatran["latitude"] = datatran["latitude"].str.replace(",", ".") 
    datatran["longitude"] = datatran["longitude"].str.replace(",", ".") 

    datatran["latitude"] = pd.to_numeric(datatran["latitude"])
    datatran["longitude"] = pd.to_numeric(datatran["longitude"]) 

    return datatran

st.set_page_config(
    page_title = "Heatmap de acidentes"
)

st.header("Faça o upload dos dados")
st.write("Os dados podem ser achados [aqui](https://www.gov.br/prf/pt-br/acesso-a-informacao/dados-abertos/dados-abertos-da-prf). Selecione um ano posterior a 2017")

inputFile = st.file_uploader("Faça o upload aqui!")

if inputFile:
    datatran = pd.read_csv(
        filepath_or_buffer = inputFile,
        encoding = "latin1",
        sep = ";"
    )

    datatran = preprocessDatafranDf(datatran)

    mapCenter = datatran[[
        "latitude", 
        "longitude"
    ]].mean().tolist()

    accidentMap = folium.Map(
        location = mapCenter
    ) 

    HeatMap(
        data = datatran[["latitude", "longitude"]].values.tolist(),
    ).add_to(accidentMap)

    st.title("Mapa de calor gerado com os dados da PRF")

    st_folium(accidentMap, width = 800, height = 500)

    st.header("O que é um mapa de calor?")
    st.write("Um mapa de calor é uma técnica de visualização de dados que mostra a magnitude de um fenômeno por meio de cor em duas dimensões. A variação de cor pode ser por matiz ou intensidade, dando pistas visuais óbvias ao leitor sobre como o fenômeno está agrupado ou varia no espaço.")

    st.header("Sobre o dataset")
    st.write("O dicionário dos dados pode ser encontrado [aqui](https://drive.google.com/file/d/11pXLw_0D0hHVS8fiC8cv2dPX39vpuOH1/view)")
    st.write("Aqui está uma pequena amostra do dataset")
    st.write(datatran.sample(10))
