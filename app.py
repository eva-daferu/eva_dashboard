# ===== app.py =====
import streamlit as st
import pandas as pd
import altair as alt
from resultados import generar_base_completa

st.set_page_config(page_title="Panel Redes Sociales Eva", layout="wide")

st.markdown("""
    <h1 style='text-align: center; color: #2F4F4F;'>📊 Panel de Seguimiento Redes Sociales - Eva Daferu</h1>
    <p style='text-align: center; color: gray;'>Análisis integral de desempeño digital desde el 08/08/2025</p>
""", unsafe_allow_html=True)

df = generar_base_completa()
dias_transcurridos = df["Dias Transcurridos"].iloc[0]
max_videos = df["Videos Publicados"].max()

col1, col2, col3 = st.columns(3)
col1.metric("Total Seguidores", f"{df['Seguidores'].sum():,}")
col2.metric("Días desde inicio de publicaciones", f"{dias_transcurridos}")
col3.metric("Videos publicados", f"{max_videos}")

st.markdown("### 📋 Datos Generales")
df_display = df.drop(columns=["Dias Transcurridos"])
st.dataframe(df_display, use_container_width=True)

st.markdown("### 📈 Gráfica Comparativa de Seguidores")
chart1 = alt.Chart(df).mark_bar(color='#38a169').encode(
    x=alt.X('Canal', sort='-y'),
    y='Seguidores',
    tooltip=['Canal', 'Seguidores']
).properties(height=400)
st.altair_chart(chart1, use_container_width=True)

st.markdown("### 🥧 Distribución de Seguidores por Canal")
chart2 = alt.Chart(df).mark_arc(innerRadius=60).encode(
    theta=alt.Theta(field="Seguidores", type="quantitative"),
    color=alt.Color(field="Canal", type="nominal"),
    tooltip=['Canal', 'Seguidores']
)
st.altair_chart(chart2, use_container_width=True)

st.markdown("### 📊 Promedio de Seguidores Diarios")
chart3 = alt.Chart(df).mark_line(point=True, color='#2F855A').encode(
    x='Canal',
    y='Promedio Seguidores Diarios',
    tooltip=['Canal', 'Promedio Seguidores Diarios']
).properties(height=400)
st.altair_chart(chart3, use_container_width=True)

if st.button("🔄 Refrescar Datos"):
    with st.spinner("Actualizando datos..."):
        df = generar_base_completa()
        df.to_excel("redes_sociales_eva.xlsx", index=False)
        st.success("✅ Datos actualizados correctamente")
        st.experimental_rerun()

st.markdown("""
    <hr>
    <p style='text-align: center; color: gray;'>
    Desarrollado por Eva EcoD 🌿 | Panel público compartido en Streamlit Cloud
    </p>
""", unsafe_allow_html=True)
