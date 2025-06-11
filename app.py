import streamlit as st
import gspread
from google.oauth2.service_account import Credentials

# Configuración
st.set_page_config(page_title="Catálogo | Colchonería Rey", layout="wide")

# Autenticación Google Sheets
google_credentials = st.secrets["google_service_account"]
scoped_creds = Credentials.from_service_account_info(
    google_credentials,
    scopes=["https://www.googleapis.com/auth/spreadsheets.readonly"]
)
client = gspread.authorize(scoped_creds)

# Abrir hoja
try:
    sheet = client.open("sigbd rivadavia").worksheet("stock")
    data = sheet.get_all_records()
except Exception as e:
    st.error("❌ Error al acceder al Google Sheet.")
    st.exception(e)
    st.stop()

# Leer plantilla
with open("template.html", "r", encoding="utf-8") as f:
    plantilla = f.read()

# Generar HTML para productos
productos_html = ""
for producto in data:
    img_url = producto.get("ImagenURL", "")
    productos_html += f"""
    <div class="producto">
        <div class="nombre">{producto.get('Nombre', 'Sin nombre')}</div>
        <div class="precio">💸 ${producto.get('Precio', 'N/D')}</div>
        <div class="descripcion">{producto.get('Descripcion', '')}</div>
        {"<img src='" + img_url + "' alt='Imagen producto'>" if img_url else ""}
    </div>
    """

# Insertar productos en la plantilla
html_final = plantilla.replace("<!-- PRODUCTOS_AQUI -->", productos_html)

# Mostrar en Streamlit con permiso para HTML
st.markdown(html_final, unsafe_allow_html=True)
