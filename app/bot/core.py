import os
import json
from datetime import datetime
from collections import Counter
import csv

DATA_DIR = "data"
CONTACTOS_FILE = os.path.join(DATA_DIR, "contactos_registrados.json")
NO_RECONOCIDAS_FILE = os.path.join(DATA_DIR, "no_reconocidas.json")
REPORTE_CSV = os.path.join(DATA_DIR, "reporte_no_reconocidas.csv")

# ========== CONTACTOS SALUDADOS ==========
def cargar_contactos():
    if os.path.exists(CONTACTOS_FILE) and os.path.getsize(CONTACTOS_FILE) > 0:
        with open(CONTACTOS_FILE, "r", encoding="utf-8") as f:
            return set(json.load(f))
    return set()

def guardar_contactos(contactos):
    with open(CONTACTOS_FILE, "w", encoding="utf-8") as f:
        json.dump(list(contactos), f, indent=2)

# ========== REGISTRO DE PREGUNTAS NO RECONOCIDAS ==========
def cargar_historial_no_reconocidas():
    if os.path.exists(NO_RECONOCIDAS_FILE) and os.path.getsize(NO_RECONOCIDAS_FILE) > 0:
        with open(NO_RECONOCIDAS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def guardar_pregunta_no_reconocida(numero, mensaje):
    historial = cargar_historial_no_reconocidas()
    historial.append({
        "numero": numero,
        "mensaje": mensaje,
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    with open(NO_RECONOCIDAS_FILE, "w", encoding="utf-8") as f:
        json.dump(historial, f, indent=2, ensure_ascii=False)

# ========== REPORTE ==========
def generar_reporte():
    historial = cargar_historial_no_reconocidas()
    if not historial:
        print(" No hay preguntas no reconocidas registradas todavía.")
        return

    preguntas = [entrada["mensaje"] for entrada in historial]
    frecuencia = Counter(preguntas)

    print("\n Preguntas no reconocidas (ordenadas por frecuencia):\n")
    for pregunta, cantidad in frecuencia.most_common():
        print(f" {pregunta} — {cantidad} veces")

    print(f"\n Total preguntas distintas: {len(frecuencia)}")
    print(f" Total registros: {len(historial)}")

    with open(REPORTE_CSV, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Pregunta", "Frecuencia"])
        for pregunta, cantidad in frecuencia.most_common():
            writer.writerow([pregunta, cantidad])

    print(f"\n Reporte guardado en: {REPORTE_CSV}")
