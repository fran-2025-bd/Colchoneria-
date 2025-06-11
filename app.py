import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
img_url = producto.get("ImagenURL", "").strip()
if img_url:
    img_url = f"https://drive.google.com/uc?export=view&id={img_url}"

# Configuración
st.set_page_config(page_title="Catálogo | Colchonería Rey", layout="wide")

# Autenticación Google Sheets con scopes adecuados
google_credentials = st.secrets["google_service_account"]
scopes = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]
scoped_creds = Credentials.from_service_account_info(
    google_credentials,
    scopes=scopes
)
client = gspread.authorize(scoped_creds)

# Intentar abrir el archivo y la hoja
try:
    sheet = client.open("sigbd rivadavia").worksheet("stock")
    data = sheet.get_all_records()
except Exception as e:
    st.error("❌ Error al acceder al Google Sheet.")
    st.exception(e)
    st.stop()

# Leer plantilla HTML
try:
    with open("template.html", "r", encoding="utf-8") as f:
        plantilla = f.read()
except FileNotFoundError:
    st.error("❌ No se encontró el archivo template.html en el directorio.")
    st.stop()

# Generar HTML para productos
productos_html = ""
for producto in data:
    raw_id = producto.get("ImagenURL", "").strip()
    img_url = f"https://drive.google.com/uc?export=view&id={raw_id}" if raw_id else ""
    nombre = producto.get('Nombre', 'Sin nombre')
    precio = producto.get('Precio', 'N/D')
    descripcion = producto.get('Descripcion', '')

    img_tag = f"<img src='{img_url}' alt='Imagen producto' style='max-width: 100%; height: auto;'>" if img_url else ""

    productos_html += f"""
    <div class="producto" style="border:1px solid #ccc; padding:10px; margin-bottom:15px; border-radius:8px;">
        <h3 style="margin-bottom:5px;">{nombre}</h3>
        <p style="font-weight:bold; color:#2a9d8f;">💸 ${precio}</p>
        <p>{descripcion}</p>
        {img_tag}
    </div>
    """
    """

# Insertar productos en la plantilla
html_final = plantilla.replace("<!-- PRODUCTOS_AQUI -->", productos_html)

# Mostrar HTML en Streamlit
st.markdown(html_final, unsafe_allow_html=True)
