# ===== app.py =====
import streamlit as st
import pandas as pd
import altair as alt
from resultados import generar_base_completa

# Configuración general
st.set_page_config(page_title="Panel Redes Sociales Eva", layout="wide")

# Fondo con gradiente y estilo visual
st.markdown("""
    <style>
        body {
            background: linear-gradient(180deg, #F4F7FB 0%, #E9EFF6 100%);
            color: #1E1E1E;
            font-family: 'Segoe UI', sans-serif;
        }
        .stApp {
            background: linear-gradient(180deg, #F4F7FB 0%, #E9EFF6 100%);
        }
        .main-card {
            background-color: white;
            border-radius: 15px;
            padding: 25px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.05);
        }
        .refresh-btn {
            display: flex;
            justify-content: right;
            margin-top: -50px;
        }
    </style>
""", unsafe_allow_html=True)

# ---- Botón superior ----
col_refresh, col_title = st.columns([1, 5])
with col_refresh:
    if st.button("🔄 Refrescar Datos"):
        with st.spinner("Actualizando datos..."):
            df = generar_base_completa()
            df.to_excel("redes_sociales_eva.xlsx", index=False)
            st.success("✅ Datos actualizados correctamente")
            st.rerun()

with col_title:
    st.markdown("""
        <div style='text-align:center'>
            <h1 style='color:#2F4F4F;'>📊 Panel de Seguimiento Redes Sociales - Eva Daferu</h1>
            <p style='color:gray;'>Análisis integral de desempeño digital desde el 08/08/2025</p>
        </div>
    """, unsafe_allow_html=True)

# ---- Datos base ----
df = generar_base_completa()
dias_transcurridos = df["Días Transcurridos"].iloc[0]
max_videos = df["Videos Publicados"].max()

col1, col2, col3 = st.columns(3)
col1.metric("Total Seguidores", f"{df['Seguidores'].sum():,}")
col2.metric("Días desde inicio de publicaciones", f"{dias_transcurridos}")
col3.metric("Videos publicados", f"{max_videos}")

# ---- Tabla general ----
st.markdown("<div class='main-card'>", unsafe_allow_html=True)
st.markdown("### 🗂️ Datos Generales")
df_display = df.drop(columns=["Días Transcurridos"])
st.dataframe(df_display, use_container_width=True)

# ---- Gráfica de seguidores ----
st.markdown("### 📊 Gráfica Comparativa de Seguidores")
chart1 = alt.Chart(df).mark_bar(color='#3B82F6').encode(
    x='Canal',
    y='Seguidores',
    tooltip=['Canal', 'Seguidores']
)
st.altair_chart(chart1, use_container_width=True)

# ---- Distribución ----
st.markdown("### 🥧 Distribución de Seguidores por Canal")
chart2 = alt.Chart(df).mark_arc(innerRadius=60).encode(
    theta=alt.Theta(field='Seguidores', type='quantitative'),
    color=alt.Color(field='Canal', type='nominal'),
    tooltip=['Canal', 'Seguidores']
)
st.altair_chart(chart2, use_container_width=True)

# ---- Promedio diario ----
st.markdown("### 📈 Promedio de Seguidores Diarios")
chart3 = alt.Chart(df).mark_line(point=True, color='#2F855A').encode(
    x='Canal',
    y='Promedio Seguidores Diarios',
    tooltip=['Canal', 'Promedio Seguidores Diarios']
).properties(height=400)
st.altair_chart(chart3, use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)
