import qrcode
import os

# Datos de Twilio sandbox
numero_twilio = "14155238886"
codigo_sandbox = "join flat-got"

# URL completa para generar el QR
link_wa = f"https://wa.me/{numero_twilio}?text={codigo_sandbox.replace(' ', '%20')}"

# Generar QR
img = qrcode.make(link_wa)
img.save("qr_twilio.png")

# Abrir imagen (en Windows)
os.system("start qr_twilio.png")
