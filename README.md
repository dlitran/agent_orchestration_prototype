# 🎬 AI News Reel Generator

An automated pipeline using **CrewAI** and **Gemini** to research, script, and generate 1-minute vertical videos.

## 📦 Setup & Installation

1. **Install dependencies:**
   `pip install crewai crewai_tools python-dotenv requests gTTS moviepy`

2. **Configure environment variables** in a `.env` file:
   `GEMINI_API_KEY=your_gemini_key`
   `SERPER_API_KEY=your_serper_key`

## 🚀 Usage

1. Change the `TEMA_NOTICIA` variable in the script to your desired news topic.
2. Run the script: 
   `python main.py`
3. The AI agents will process the task and create a timestamped folder containing:
   * `guion.txt` (The generated script)
   * `imagen_fondo.jpg` (The AI background)
   * `locucion.mp3` (The TTS voiceover)
   * `reel_final.mp4` (The final rendered video)