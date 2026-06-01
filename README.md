AI News Reel Generator
Automated pipeline that turns any topic into a ready-to-post video reel (TikTok/Instagram).

How it works
Searches latest news via Google (Serper API)

Writes 1-min script with Gemini AI

Downloads background image from Pollinations
4 Creates video with Spanish voiceover

Quick start
bash
# Install dependencies
pip install crewai crewai-tools requests gtts moviepy python-dotenv google-generativeai

# Add your keys to .env
GEMINI_API_KEY=your_key
SERPER_API_KEY=your_key

# Change topic (optional)
TEMA_NOTICIA = "Your topic here"

# Run
python script.py
Output
Creates folder: {Topic}_{YYYY-MM-DD}/ with:

guion.txt - the script

reel_final.mp4 - final video

Files
guion.txt - written script

imagen_fondo.jpg - background image

locucion.mp3 - audio narration

reel_final.mp4 - finished video

Requirements
Python 3.8+

API keys from Gemini and Serper

Notes
Scripts are ~130 words (~1 minute in Spanish)

Video is vertical format (1080x1920)

Each task retries 5 times on failure

Common issues
No search results - check Serper API quota
Video won't render - reinstall moviepy: pip install --upgrade moviepy

That's it. Run it and you get a video.