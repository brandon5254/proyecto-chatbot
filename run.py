import os
import qrcode
from flask import Flask, request
from dotenv import load_dotenv
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse

from app.bot.core import (
    cargar_contactos,
    guardar_contactos,
    guardar_pregunta_no_reconocida,
    generar_reporte
)
from app.bot.nlp import obtener_respuesta

#  CONFIGURACION INICIAL
load_dotenv()
app = Flask(__name__)

# Mostrar código QR del sandbox
numero_twilio = "14155238886"
codigo_sandbox = "join flat-got"
link_wa = f"https://wa.me/{numero_twilio}?text={codigo_sandbox.replace(' ', '%20')}"
img = qrcode.make(link_wa)
img.save("qr_twilio.png")
os.system("start qr_twilio.png")  # Solo en Windows

# WHATSAPP BOT 
usuarios_saludados = cargar_contactos()

@app.route("/webhook", methods=["POST"])
def whatsapp_bot():
    incoming_msg = request.values.get("Body", "").lower().strip()
    numero_usuario = request.values.get("From")

    # Saludo automático si es nuevo contacto
    if numero_usuario not in usuarios_saludados:
        usuarios_saludados.add(numero_usuario)
        guardar_contactos(usuarios_saludados)
        mensaje_bienvenida = "👋 ¡Hola! Bienvenido al asistente académico. Pregúntame lo que necesites."
    else:
        mensaje_bienvenida = ""

    # Buscar respuesta con similitud semántica
    respuesta = obtener_respuesta(incoming_msg)

    if not respuesta:
        respuesta = "Lo siento, no entendí tu pregunta."
        guardar_pregunta_no_reconocida(numero_usuario, incoming_msg)

    # Unir saludo + respuesta
    mensaje_final = f"{mensaje_bienvenida}\n\n{respuesta}" if mensaje_bienvenida else respuesta

    # Enviar respuesta
    resp = MessagingResponse()
    resp.message(mensaje_final)
    return str(resp)

# ENVÍO DE MENSAJE DE BIENVENIDA
def enviar_mensaje_bienvenida():
    account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")
    from_whatsapp_number = os.getenv("TWILIO_PHONE_NUMBER")

    client = Client(account_sid, auth_token)

    destinatarios = [
        "whatsapp:+573045874931",
        "whatsapp:+573001111222"
    ]

    for numero in destinatarios:
        client.messages.create(
            from_=from_whatsapp_number,
            body="👋 ¡Hola! Bienvenido al asistente académico. Pregúntame lo que necesites.",
            to=numero
        )

#       EJECUCIÓN 
if __name__ == "__main__":
    # enviar_mensaje_bienvenida()  # Descomenta si estás dentro del límite diario de Twilio
    generar_reporte()              # Muestra las estadísticas por consola
    app.run(port=5000, debug=True)
