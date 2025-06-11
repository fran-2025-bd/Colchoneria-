import streamlit as st
import gspread
from google.oauth2.service_account import Credentials

st.set_page_config(page_title="Catálogo | Colchonería Rey", layout="wide")

# Leer credencial directamente desde secrets (ya es un dict)
google_credentials = st.secrets["google_service_account"]

# Autenticación
scoped_creds = Credentials.from_service_account_info(
    google_credentials,
    scopes=["https://www.googleapis.com/auth/spreadsheets.readonly"]
)
client = gspread.authorize(scoped_creds)

# Acceder a la hoja
sheet = client.open("sigbd rivadavia").worksheet("stock")
data = sheet.get_all_records()

# Título de la tienda
st.markdown("# 🛏️ Catálogo de Colchonería Rey")
st.markdown("Catálogo actualizado automáticamente desde Google Sheets.")

# Mostrar productos en columnas
cols = st.columns(3)

for i, producto in enumerate(data):
    with cols[i % 3]:
        st.markdown("----")
        st.subheader(producto.get("Nombre", "Sin nombre"))
        st.write(f"💸 **Precio:** ${producto.get('Precio', 'N/D')}")
        if "Imagen" in producto and producto["Imagen"]:
            st.image(producto["Imagen"], use_column_width=True)
