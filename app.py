import streamlit as st
import pandas as pd
import os
from datetime import datetime

# Intentar importar auto-refresh para mantener la sesión activa en el navegador
try:
    from streamlit_autorefresh import st_autorefresh
except ImportError:
    st_autorefresh = None

# 1. Configuración de la página
st.set_page_config(
    page_title="Agenda de actividades - Museo del Hambre 2026",
    page_icon="📅",
    layout="wide"
)

# --- KEEP ALIVE Y AUTO-REFRESH ---
# Refresca la app cada 15 minutos para evitar que la pestaña muera
if st_autorefresh:
    st_autorefresh(interval=15 * 60 * 1000, key="keepalive")

# --- FUNCIONES DE FORMATEO ---
def formatear_fecha_larga(fecha_str):
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
    try:
        if ":" in str(hora_str):
            partes = str(hora_str).split(":")
            hh = partes[0].zfill(2)
            mm = partes[1].zfill(2)
            return f"{hh}:{mm}"[:5]
        return hora_str
    except:
        return hora_str

# 2. Estilo CSS (Diseño Cálido y Tarjetas)
st.markdown("""
<style>
    .main { background-color: #fdfcf0; }
    .event-card {
        background-color: #ffffff;
        padding: 25px;
        border-radius: 28px;
        border: 1px solid #eaddca;
        box-shadow: 0 4px 12px rgba(75, 46, 42, 0.05);
        margin-bottom: 20px;
        display: flex;
        flex-direction: column;
        align-items: center;
        text-align: center;
        min-height: 440px;
    }
    .date-time-box {
        background-color: #f5ebd7;
        padding: 15px;
        border-radius: 20px;
        width: 85%;
        margin-bottom: 15px;
    }
    .date-text { color: #4b2e2a; font-weight: 800; font-size: 18px; }
    .time-text { color: #6d4c41; font-weight: 700; font-size: 15px; display: block; margin-top: 5px; }
    .event-title { color: #4b2e2a; font-size: 22px; font-weight: 700; margin-bottom: 10px; min-height: 55px; }
    .location { color: #8d6e63; font-size: 15px; font-style: italic; margin-bottom: 12px; }
    .description { color: #5d4037; font-size: 14px; line-height: 1.5; }
</style>
""", unsafe_allow_html=True)

# 3. Carga de datos
@st.cache_data(ttl=300)
def load_data():
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQVnI-dbe62M3I0uv9mzw43pEZuwHAJMb-SpfFyXRu66uHZnNrRyy_xW-lRX4sooN28T357B5JLONxa/pub?gid=1828847868&single=true&output=csv"
    try:
        df = pd.read_csv(url)
        df.columns = df.columns.str.strip()
        mapping = {'Nombre del evento': 'Nombre', 'Descripción': 'Desc'}
        df = df.rename(columns={k: v for k, v in mapping.items() if k in df.columns})
        
        # Asegurar orden cronológico convirtiendo la fecha temporalmente
        if 'Fecha' in df.columns:
            df['fecha_dt'] = pd.to_datetime(df['Fecha'], dayfirst=True, errors='coerce')
            df = df.sort_values(by='fecha_dt').drop(columns=['fecha_dt'])
            
        for c in ['Fecha', 'Hora', 'Nombre', 'Desc', 'Lugar']:
            if c not in df.columns: df[c] = ""
            df[c] = df[c].fillna("").astype(str).str.strip()
        return df
    except:
        return None

df = load_data()

if df is not None:
    if os.path.exists("logo.png"):
        st.image("logo.png", width=120)
    
    st.title("📅 Agenda Museo del Hambre 2026")
    search = st.text_input("🔍 Buscar actividad...", placeholder="Escriba aquí...")

    f_df = df.copy()
    if search:
        f_df = f_df[f_df['Nombre'].str.contains(search, case=False)]

    if f_df.empty:
        st.info("No hay actividades que coincidan.")
    else:
        # --- NUEVA LÓGICA DE FILAS PARA ORDEN CRONOLÓGICO ---
        # Dividimos los datos en grupos de 3 (para PC)
        num_columnas = 3
        for i in range(0, len(f_df), num_columnas):
            cols = st.columns(num_columnas)
            # Tomamos un bloque de hasta 3 eventos
            fila_eventos = f_df.iloc[i : i + num_columnas]
            
            for index, (idx_original, row) in enumerate(fila_eventos.iterrows()):
                with cols[index]:
                    fecha_larga = formatear_fecha_larga(row['Fecha'])
                    hora_limpia = formatear_hora_corta(row['Hora'])
                    
                    st.markdown(f"""
                    <div class="event-card">
                        <div class="date-time-box">
                            <span class="date-text">{fecha_larga}</span>
                            <span class="time-text">🕒 {hora_limpia} hs</span>
                        </div>
                        <div class="event-title">{row['Nombre']}</div>
                        <div class="location">📍 {row['Lugar']}</div>
                        <div class="description">{row['Desc']}</div>
                    </div>
                    """, unsafe_allow_html=True)

st.markdown("---")
st.caption(f"Última actualización automática: {datetime.now().strftime('%H:%M')} hs")
