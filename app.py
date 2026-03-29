import streamlit as st
import pandas as pd
import os
import textwrap

# 1. Configuración de la página
st.set_page_config(
    page_title="Propuestas - Museo del Hambre 2026",
    page_icon="📅",
    layout="wide"
)

# 2. Estilo CSS (Diseño Google - Corregido para evitar errores visuales)
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
    margin-bottom: 10px;
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
    margin-bottom: 20px;
}
.description {
    color: #334155;
    font-size: 16px;
    line-height: 1.7;
    margin-bottom: 25px;
}
.contact-box {
    background-color: #f1f5f9;
    padding: 20px;
    border-radius: 20px;
}
.label { 
    font-size: 11px; 
    font-weight: 800; 
    color: #64748b; 
    text-transform: uppercase; 
    margin-bottom: 4px;
}
.value-big { 
    font-size: 22px; 
    font-weight: 700; 
    color: #0f172a; 
    margin-bottom: 15px;
}
.value-small { font-size: 15px; color: #334155; margin-bottom: 12px; }
.ref-container { display: flex; gap: 12px; margin-top: 15px; margin-bottom: 15px; flex-wrap: wrap; }
.ref-btn {
    padding: 10px 18px;
    border-radius: 12px;
    font-size: 13px;
    font-weight: 700;
    text-decoration: none !important;
}
.ref-on { background-color: #e8f0fe; color: #1967d2 !important; border: 1px solid #1967d2; }
.ref-off { background-color: #1a1a1a; color: #ffffff !important; opacity: 0.8; }
</style>
""", unsafe_allow_html=True)

# 3. Carga de datos desde tu link de Google Sheets
@st.cache_data(ttl=60)
def load_data():
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQVnI-dbe62M3I0uv9mzw43pEZuwHAJMb-SpfFyXRu66uHZnNrRyy_xW-lRX4sooN28T357B5JLONxa/pub?gid=1828847868&single=true&output=csv"
    try:
        df = pd.read_csv(url)
        df.columns = df.columns.str.strip()
        # Mapeo de columnas
        mapping = {
            'Nombre del evento': 'Nombre',
            'Descripción': 'Desc',
            'Contacto (mail)': 'Mail',
            'Contacto (whatsapp)': 'WhatsApp',
            'Nombre del contacto principal': 'Responsable'
        }
        df = df.rename(columns={k: v for k, v in mapping.items() if k in df.columns})
        # Aseguramos columnas
        for c in ['Fecha', 'Hora', 'Nombre', 'Lugar', 'Desc', 'Referencia 1', 'Referencia 2', 'Referencia 3', 'Mail', 'WhatsApp', 'Responsable']:
            if c not in df.columns: df[c] = ""
            df[c] = df[c].fillna("").astype(str).str.strip()
        return df
    except: return None

df = load_data()

if df is not None:
    if os.path.exists("logo.png"):
        st.image("logo.png", width=140)
    
    st.title("📅 Propuestas - Museo del Hambre 2026")
    
    st.markdown("### 🔍 Filtrar Agenda")
    c1, c2 = st.columns(2)
    with c1:
        lugar_sel = st.multiselect("Filtrar por Lugar", sorted([x for x in df['Lugar'].unique() if x != ""]))
    with c2:
        search = st.text_input("Buscar por nombre...", placeholder="Escribe aquí...")

    f_df = df.copy()
    if lugar_sel: f_df = f_df[f_df['Lugar'].isin(lugar_sel)]
    if search: f_df = f_df[f_df['Nombre'].str.contains(search, case=False)]

    if f_df.empty:
        st.info("No hay eventos que coincidan.")
    else:
        for i, row in f_df.iterrows():
            # Construir referencias
            refs = ""
            for n in ["1", "2", "3"]:
                link = row[f'Referencia {n}']
                if link and len(link) > 5:
                    refs += f'<a href="{link}" target="_blank" class="ref-btn ref-on">Ref {n} 🔗</a>'
                else:
                    refs += f'<span class="ref-btn ref-off">Ref {n} 🚫</span>'

            # El HTML final sin ningún espacio al principio de las líneas (CRUCIAL)
            card = f"""<div class="event-card"><div class="date-badge">🗓️ {row['Fecha']} — 🕒 {row['Hora']}</div><div class="event-title">{row['Nombre']}</div><div class="location">📍 {row['Lugar']}</div><div class="description">{row['Desc']}</div><div class="label">📂 Referencias:</div><div class="ref-container">{refs}</div><div class="contact-box"><div class="label">👤 Responsable</div><div class="value-small">{row['Responsable']}</div><div class="label">📧 Correo</div><div class="value-big">{row['Mail']}</div><div class="label">📱 WhatsApp</div><div class="value-big">{row['WhatsApp']}</div></div></div>"""
            st.markdown(card, unsafe_allow_html=True)

st.markdown("---")
st.caption("Museo del Hambre - 2026")
