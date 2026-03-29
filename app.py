import streamlit as st
import pandas as pd
import os
import textwrap

# 1. Configuración de la página
st.set_page_config(
    page_title="Agenda - Museo del Hambre 2026",
    page_icon="📅",
    layout="wide"
)

# 2. Estilo CSS (Diseño Limpio y Minimalista)
st.markdown("""
<style>
.main { background-color: #f8fafc; }
.event-card {
    background-color: #ffffff;
    padding: 30px;
    border-radius: 28px;
    border: 1px solid #e2e8f0;
    box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    margin-bottom: 25px;
    display: flex;
    flex-direction: column;
}
.date-badge {
    color: #1a73e8;
    font-weight: 800;
    font-size: 14px;
    text-transform: uppercase;
    margin-bottom: 8px;
}
.event-title {
    color: #1e293b;
    font-size: 26px;
    font-weight: 700;
    margin-bottom: 6px;
}
.location {
    color: #64748b;
    font-size: 17px;
    font-weight: 500;
    margin-bottom: 20px;
}
.description {
    color: #334155;
    font-size: 16px;
    line-height: 1.7;
}
</style>
""", unsafe_allow_html=True)

# 3. Carga de datos desde tu Google Sheet
@st.cache_data(ttl=60)
def load_data():
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQVnI-dbe62M3I0uv9mzw43pEZuwHAJMb-SpfFyXRu66uHZnNrRyy_xW-lRX4sooN28T357B5JLONxa/pub?gid=1828847868&single=true&output=csv"
    try:
        df = pd.read_csv(url)
        df.columns = df.columns.str.strip()
        
        # Mapeo solo de lo necesario
        mapping = {
            'Nombre del evento': 'Nombre',
            'Descripción': 'Desc'
        }
        df = df.rename(columns={k: v for k, v in mapping.items() if k in df.columns})
        
        # Aseguramos solo las 5 columnas pedidas
        for c in ['Fecha', 'Hora', 'Nombre', 'Desc', 'Lugar']:
            if c not in df.columns: df[c] = ""
            df[c] = df[c].fillna("").astype(str).str.strip()
        return df
    except: return None

df = load_data()

if df is not None:
    # Logo del Centro Cultural
    if os.path.exists("logo.png"):
        st.image("logo.png", width=140)
    
    st.title("📅 Propuestas - Museo del Hambre 2026")
    
    # Buscador y Filtro por Lugar
    st.markdown("### 🔍 Buscar en la Agenda")
    c1, c2 = st.columns(2)
    with c1:
        lugares = sorted([x for x in df['Lugar'].unique() if x != ""])
        lugar_sel = st.multiselect("Filtrar por Lugar", lugares)
    with c2:
        search = st.text_input("Buscar por nombre del evento...", placeholder="Escribe aquí...")

    # Filtrado
    f_df = df.copy()
    if lugar_sel: f_df = f_df[f_df['Lugar'].isin(lugar_sel)]
    if search: f_df = f_df[f_df['Nombre'].str.contains(search, case=False)]

    if f_df.empty:
        st.info("No hay eventos que coincidan con la búsqueda.")
    else:
        st.write(f"Mostrando **{len(f_df)}** eventos")
        
        for i, row in f_df.iterrows():
            # Construcción del HTML en una sola línea para evitar el error de "bloque de código"
            card = f"""<div class="event-card"><div class="date-badge">🗓️ {row['Fecha']} — 🕒 {row['Hora']}</div><div class="event-title">{row['Nombre']}</div><div class="location">📍 {row['Lugar']}</div><div class="description">{row['Desc']}</div></div>"""
            st.markdown(card, unsafe_allow_html=True)

st.markdown("---")
st.caption("Plataforma de Eventos - Museo del Hambre 2026")
