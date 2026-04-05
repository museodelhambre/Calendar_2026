import streamlit as st
import pandas as pd
import os
from datetime import datetime
# Importamos la librería para el auto-refresco
try:
    from streamlit_autorefresh import st_autorefresh
except ImportError:
    st_autorefresh = None

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="Agenda de actividades - Museo del Hambre 2026",
    page_icon="📅",
    layout="wide"
)

# --- FUNCIÓN KEEP ALIVE (CÓDIGO) ---
# Si la librería está instalada, refresca la app cada 15 minutos en el navegador
if st_autorefresh:
    st_autorefresh(interval=15 * 60 * 1000, key="keepalive")

# --- FUNCIONES DE FORMATEO ---
def formatear_fecha_larga(fecha_str):
    """Convierte fechas a formato '4 de abril de 2026'"""
    try:
        fecha_obj = pd.to_datetime(fecha_str, dayfirst=True)
        meses = {
            1: "enero", 2: "febrero", 3: "marzo", 4: "abril",
            5: "mayo", 6: "junio", 7: "julio", 8: "agosto",
            9: "septiembre", 10: "octubre", 11: "noviembre", 12: "diciembre"
        }
        return f"{fecha_obj.day} de {meses[fecha_obj.month]} de {fecha_obj.year}"
    except:
        return fecha_str

def formatear_hora_corta(hora_str):
    """Asegura formato HH:MM (ej: 10:00)"""
    try:
        if ":" in str(hora_str):
            partes = str(hora_str).split(":")
            hh = partes[0].zfill(2)
            mm = partes[1].zfill(2)
            return f"{hh}:{mm}"[:5]
        return hora_str
    except:
        return hora_str

# --- ESTILO CSS ---
st.markdown("""
<style>
    .main { background-color: #fdfcf0; }
    .event-card {
        background-color: #ffffff;
        padding: 30px;
        border-radius: 28px;
        border: 1px solid #eaddca;
        box-shadow: 0 4px 12px rgba(75, 46, 42, 0.05);
        margin-bottom: 25px;
        display: flex;
        flex-direction: column;
        align-items: center;
        text-align: center;
        min-height: 460px;
        transition: transform 0.2s ease;
    }
    .event-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 20px rgba(75, 46, 42, 0.1);
    }
    .date-time-box {
        background-color: #f5ebd7;
        padding: 18px;
        border-radius: 22px;
        width: 80%;
        margin: 0 auto 20px auto;
        display: flex;
        flex-direction: column;
        align-items: center;
    }
    .date-text {
        color: #4b2e2a;
        font-weight: 800;
        font-size: 19px;
        line-height: 1.2;
    }
    .time-text {
        color: #6d4c41;
        font-weight: 700;
        font-size: 16px;
        margin-top: 6px;
    }
    .event-title {
        color: #4b2e2a;
        font-size: 24px;
        font-weight: 700;
        margin-bottom: 12px;
    }
    .location {
        color: #8d6e63;
        font-size: 16px;
        font-weight: 500;
        margin-bottom: 15px;
        font-style: italic;
    }
    .description {
        color: #5d4037;
        font-size: 15px;
        line-height: 1.7;
    }
</style>
""", unsafe_allow_html=True)

# --- CARGA DE DATOS ---
@st.cache_data(ttl=300)
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
    except:
        return None

# --- RENDERIZADO DE LA APP ---
df = load_data()

if df is not None:
    # Logo opcional
    if os.path.exists("logo.png"):
        st.image("logo.png", width=140)
    
    st.title("📅 Agenda de actividades - Museo del Hambre 2026")
    
    search = st.text_input("🔍 Buscar actividad...", placeholder="Escribe el nombre del evento...")

    f_df = df.copy()
    if search:
        f_df = f_df[f_df['Nombre'].str.contains(search, case=False)]

    if f_df.empty:
        st.info("No hay actividades programadas que coincidan.")
    else:
        cols = st.columns(3)
        for i, row in f_df.reset_index().iterrows():
            fecha_larga = formatear_fecha_larga(row['Fecha'])
            hora_limpia = formatear_hora_corta(row['Hora'])
            
            with cols[i % 3]:
                card_html = f"""
                <div class="event-card">
                    <div class="date-time-box">
                        <span class="date-text">{fecha_larga}</span>
                        <span class="time-text">🕒 {hora_limpia} hs</span>
                    </div>
                    <div class="event-title">{row['Nombre']}</div>
                    <div class="location">📍 {row['Lugar']}</div>
                    <div class="description">{row['Desc']}</div>
                </div>
                """
                st.markdown(card_html, unsafe_allow_html=True)

st.markdown("---")
st.caption(f"Agenda actualizada: {datetime.now().strftime('%d/%m/%Y %H:%M')} - Museo del Hambre")
