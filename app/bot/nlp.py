from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

FAQ = {
    "hola": "¡Hola! ¿En qué puedo ayudarte?",
    "qué servicios ofrecen?": "Ofrecemos cursos, asesorías y talleres académicos.",
    "¿cómo me inscribo?": "Puedes inscribirte en nuestra web o escribiéndonos por aquí.",
    "¿cuánto cuesta?": "Tenemos precios variados según el curso. Escríbenos para más detalles.",
    "gracias": "¡Con gusto! 😊",
    "adiós": "¡Hasta luego! 👋",
    "¿dónde están ubicados?": "Estamos en Cali, Colombia. También atendemos en línea.",
    "¿quiénes son?": "Somos una plataforma de apoyo académico.",
    "¿qué horarios manejan?": "De lunes a viernes, 8:00 a.m. a 6:00 p.m.",
    "¿puedo agendar una cita?": "¡Claro! Déjanos tus datos y te contactamos."
}

corpus = list(FAQ.keys())
vectorizer = TfidfVectorizer().fit(corpus)
X = vectorizer.transform(corpus)

def obtener_respuesta(mensaje_usuario, umbral=0.4):
    vector_usuario = vectorizer.transform([mensaje_usuario])
    similitudes = cosine_similarity(vector_usuario, X)[0]

    idx_max = similitudes.argmax()
    score_max = similitudes[idx_max]

    if score_max >= umbral:
        pregunta_similar = corpus[idx_max]
        return FAQ[pregunta_similar]
    return None
