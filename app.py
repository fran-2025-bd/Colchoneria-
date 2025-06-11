from flask import Flask, render_template
import os
import json
import gspread
from google.oauth2.service_account import Credentials

app = Flask(__name__)

# Leer el secreto como diccionario (Streamlit o entorno)
google_secret_raw = os.environ.get("GOOGLE_CREDENTIALS")

if google_secret_raw:
    # En entorno: GOOGLE_CREDENTIALS es un JSON en string
    google_credentials = json.loads(google_secret_raw)
else:
    # Alternativamente (ej: Streamlit-style secret), cargá desde archivo .toml o config
    from dotenv import dotenv_values
    secrets = dotenv_values(".env")  # Si tenés un archivo .env con TOML-like
    google_credentials = json.loads(secrets["google_service_account"])

# Autenticación con Google Sheets
scoped_creds = Credentials.from_service_account_info(
    google_credentials,
    scopes=["https://www.googleapis.com/auth/spreadsheets.readonly"]
)
client = gspread.authorize(scoped_creds)

# Acceder a la hoja
sheet = client.open("sigbd rivadavia").worksheet("stock")

@app.route('/')
def catalogo():
    data = sheet.get_all_records()
    return render_template('catalogo.html', productos=data)

if __name__ == '__main__':
    app.run(debug=True)
