from flask import Flask, render_template
import os
import json
import gspread
from google.oauth2.service_account import Credentials

app = Flask(__name__)

# Leer las credenciales directamente desde variable de entorno
google_credentials = json.loads(os.environ["GOOGLE_CREDENTIALS"])

# Autenticación
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
