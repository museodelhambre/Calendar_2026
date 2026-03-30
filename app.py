import streamlit as st
import pandas as pd
import os
import textwrap

# 1. Configuración de la página
st.set_page_config(
    page_title="Agenda de actividades - Museo del Hambre 2026",
    page_icon="📅",
    layout="wide"
)

# 2. Estilo CSS (Paleta Cálida y Diseño de Cuadrícula)
st.markdown("""
<style>
    /* Fondo cálido tipo papel/crema */
    .main { background-color: #fdfcf0; }
    
    .event-card {
        background-color: #ffffff;
        padding: 25px;
        border-radius: 24px;
        border: 1px solid #eaddca;
        box-shadow: 0 6px 15px rgba(139, 69, 19, 0.05);
        margin-bottom: 25px;
        display: flex;
        flex-direction: column;
        min-height: 420px;
        transition: transform 0.2s ease;
    }
    .event-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 20px rgba(139, 69, 19, 0.1);
    }
    
    /* Fecha y Hora Destacadas */
    .date-time-container {
        background-color: #fef5e7;
        padding: 15px;
        border-radius: 18px;
        border-left: 5px solid #d35400;
        margin-bottom: 15px;
    }
    .date-text {
        color: #d35400;
        font-weight: 800;
        font-size: 20px; /* Tamaño grande */
        display: block;
        line-height: 1.1;
    }
    .time-text {
        color: #a04000;
        font-weight: 600;
        font-size: 16px;
        display: block;
        margin-top: 5px;
    }
    
    .event-title {
        color: #2c3e50;
        font-size: 22px;
        font-weight: 700;
        margin-bottom: 10px;
        line-height: 1.2;
    }
    
    .location {
        color: #7f8c8d;
        font-size: 15px;
        font-weight: 500;
        margin-bottom: 15px;
        font-style: italic;
    }
    
    .description {
        color: #5d6d7e;
        font-size: 15px;
        line-height: 1.6;
        overflow: hidden;
        display: -webkit-box;
        -webkit-line-clamp: 5;
        -webkit-box-orient: vertical;
    }
</style>
""", unsafe_allow_html=True)

# 3. Carga de datos
@st.cache_data(ttl=60)
def load_data():
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQVnI-dbe62M3I0uv9mzw43pEZuwHAJMb-SpfFyXRu66uHZnNrRyy_xW-lRX4sooN28T357B5JLONxa/pub?gid=1828847868&single=true&output=csv"
    try:
        df = pd.read_csv(url)
        df.columns = df.columns.str.strip()
        mapping = {'Nombre del evento': 'Nombre', 'Descripción': 'Desc'}
        df = df.rename(columns={k: v for k, v in mapping.items() if k in df.columns})
        for c in ['Fecha', 'Hora', 'Nombre', 'Desc', 'Lugar']:
            if c not in df.columns: df[c] = ""
            df[c] = df[c].fillna("").astype(str).str.strip()
        return df
    except: return None

df = load_data()

if df is not None:
    # Encabezado
    if os.path.exists("logo.png"):
        st.image("logo.png", width=150)
    
    st.title("📅 Agenda de actividades - Museo del Hambre 2026")
    
    # Buscador (Filtro por lugar eliminado)
    search = st.text_input("🔍 Buscar actividad por nombre...", placeholder="Escribe aquí el evento que buscas...")

    # Filtrado
    f_df = df.copy()
    if search:
        f_df = f_df[f_df['Nombre'].str.contains(search, case=False)]

    if f_df.empty:
        st.info("No hay actividades que coincidan con la búsqueda.")
    else:
        st.write(f"Mostrando **{len(f_df)}** actividades")
        
        # --- DISEÑO DE 3 COLUMNAS ---
        cols = st.columns(3)
        
        for i, row in f_df.reset_index().iterrows():
            with cols[i % 3]:
                # Construcción del HTML (sin espacios iniciales para evitar errores)
                card_html = f"""<div class="event-card"><div class="date-time-container"><span class="date-text">🗓️ {row['Fecha']}</span><span class="time-text">🕒 {row['Hora']} hs</span></div><div class="event-title">{row['Nombre']}</div><div class="location">📍 {row['Lugar']}</div><div class="description">{row['Desc']}</div></div>"""
                st.markdown(card_html, unsafe_allow_html=True)

st.markdown("---")
st.caption("Agenda Cultural - Museo del Hambre 2026")
