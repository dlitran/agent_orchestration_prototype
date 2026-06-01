import os
import requests
from datetime import datetime
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process
from crewai.tools import tool
from crewai_tools import SerperDevTool
from gtts import gTTS
from moviepy import ImageClip, AudioFileClip # <- Actualizado para MoviePy 2.x

# 1. Configuración inicial
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
SERPER_API_KEY = os.getenv("SERPER_API_KEY")
# Sustituye "TU_API_KEY" por la clave que generaste en Google AI Studio. 
# Lo ideal es que esté en tu archivo .env como GEMINI_API_KEY=AIzaSy...
os.environ["GEMINI_API_KEY"] = os.getenv("GEMINI_API_KEY", GEMINI_API_KEY)
os.environ["SERPER_API_KEY"] = SERPER_API_KEY

TEMA_NOTICIA = "Avances en Inteligencia Artificial"
FECHA_ACTUAL = datetime.now().strftime("%Y-%m-%d")

gemini_llm = 'gemini/gemini-2.5-flash'

# Carpeta base
DIRECTORIO_BASE = f"{TEMA_NOTICIA.replace(' ', '_')}_{FECHA_ACTUAL}"
os.makedirs(DIRECTORIO_BASE, exist_ok=True)

# 2. Definición de Herramientas (Tools)
buscador_web = SerperDevTool()

@tool("Descargador de Imagenes")
def descargar_imagen(query: str) -> str:
    """Busca y descarga una imagen de uso libre basada en la consulta (query)."""
    url = f"https://image.pollinations.ai/prompt/{query.replace(' ', '%20')}?width=1080&height=1920&nologo=true"
    ruta_imagen = os.path.join(DIRECTORIO_BASE, "imagen_fondo.jpg")
    
    try:
        response = requests.get(url)
        with open(ruta_imagen, 'wb') as f:
            f.write(response.content)
        return f"Imagen descargada exitosamente en: {ruta_imagen}"
    except Exception as e:
        return f"Error al descargar la imagen: {str(e)}"

@tool("Generador de Audio y Video")
def generar_video_final(guion: str) -> str:
    """Genera un archivo de audio a partir del guion y lo junta con la imagen para crear el reel de 1 minuto."""
    ruta_audio = os.path.join(DIRECTORIO_BASE, "locucion.mp3")
    ruta_imagen = os.path.join(DIRECTORIO_BASE, "imagen_fondo.jpg")
    ruta_video = os.path.join(DIRECTORIO_BASE, "reel_final.mp4")
    ruta_texto = os.path.join(DIRECTORIO_BASE, "guion.txt")
    
    # Guardar el guion en texto
    with open(ruta_texto, "w", encoding="utf-8") as f:
        f.write(guion)
        
    try:
        # 1. Texto a Voz (TTS)
        tts = gTTS(text=guion, lang='es', tld='com.mx') 
        tts.save(ruta_audio)
        
        # 2. Ensamblar Video (Sintaxis actualizada para MoviePy 2.x)
        audio_clip = AudioFileClip(ruta_audio)
        video_clip = ImageClip(ruta_imagen).with_duration(audio_clip.duration)
        video_clip = video_clip.with_audio(audio_clip)
        
        # Renderizar video (logger eliminado por compatibilidad)
        video_clip.write_videofile(ruta_video, fps=24, codec="libx264", audio_codec="aac")
        
        return f"¡Éxito! Video final generado en: {ruta_video}"
    except Exception as e:
        return f"Error al generar el video: {str(e)}"

# 3. Definición de Agentes
periodista = Agent(
    role='Periodista de Investigación',
    goal=f'Encontrar la noticia más relevante y actual sobre: {TEMA_NOTICIA}.',
    backstory='Eres un periodista galardonado experto en encontrar noticias de última hora en internet.',
    verbose=True,
    allow_delegation=False,
    tools=[buscador_web],
    llm=gemini_llm  # <- Asignamos Gemini
)

guionista = Agent(
    role='Guionista de Reels para TikTok/Instagram',
    goal='Escribir un guion dinámico de 1 minuto (aprox 130 palabras) resumiendo la noticia encontrada.',
    backstory='Eres un creador de contenido viral. Sabes cómo enganchar a la audiencia en los primeros 3 segundos y resumir información compleja de forma entretenida.',
    verbose=True,
    allow_delegation=False,
    llm=gemini_llm  # <- Asignamos Gemini
)

productor_audiovisual = Agent(
    role='Productor de Video IA',
    goal='Descargar una imagen relevante y generar el vídeo final usando el guion.',
    backstory='Eres un editor de video automatizado. Sabes exactamente qué herramientas usar para convertir texto en audio y ensamblar vídeos listos para publicarse.',
    verbose=True,
    allow_delegation=False,
    tools=[descargar_imagen, generar_video_final],
    llm=gemini_llm  # <- Asignamos Gemini
)

# 4. Definición de Tareas
tarea_investigar = Task(
    description=f'Busca en internet la noticia más impactante del día de hoy ({FECHA_ACTUAL}) sobre {TEMA_NOTICIA}. Extrae los hechos clave.',
    expected_output='Un resumen en viñetas de la noticia más importante.',
    agent=periodista,
    max_retries=5
)

tarea_escribir = Task(
    description='Basado en los hechos clave de la investigación, escribe un guion para un reel de 1 minuto. El tono debe ser informativo pero enérgico. NO incluyas acotaciones de cámara, solo el texto que se va a leer.',
    expected_output='Un guion de texto plano de aproximadamente 130-150 palabras.',
    agent=guionista,
    max_retries=5
)

tarea_producir = Task(
    description='''
    1. Piensa en un término de búsqueda corto en inglés para una imagen que represente el guion (ej. "robot working", "bitcoin chart").
    2. Usa la herramienta "Descargador de Imagenes" con ese término.
    3. Una vez tengas la imagen, usa la herramienta "Generador de Audio y Video" pasándole el guion exacto escrito por el guionista.
    ''',
    expected_output='El estado final de la generación del video, confirmando que todos los archivos se guardaron en la carpeta.',
    agent=productor_audiovisual,
    max_retries=5
)

# 5. Ejecución del Crew
equipo_noticias = Crew(
    agents=[periodista, guionista, productor_audiovisual],
    tasks=[tarea_investigar, tarea_escribir, tarea_producir],
    process=Process.sequential,
    max_rpm=4
)

# Iniciar proceso
print(f"🚀 Iniciando la generación de noticias para: {TEMA_NOTICIA}")
resultado = equipo_noticias.kickoff()

print("================================================")
print("🎬 PROCESO COMPLETADO 🎬")
print("================================================")
print(f"Tus archivos han sido guardados en la carpeta: {DIRECTORIO_BASE}/")