import streamlit as st
import whisper
from googletrans import Translator
import tempfile
import os

# Load Whisper model
@st.cache_resource
def load_model():
    return whisper.load_model("base")

model = load_model()
translator = Translator()

st.title("🎙️ Language Learning Tool")
st.write("Upload an audio file, get the transcription, and translate it into another language.")

# File uploader
uploaded_file = st.file_uploader("Upload an audio file (MP3, WAV, etc.)", type=["mp3", "wav", "m4a"]) 

if uploaded_file is not None:
    # Save uploaded file to a temporary location
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as temp_audio:
        temp_audio.write(uploaded_file.read())
        temp_audio_path = temp_audio.name
    
    st.audio(uploaded_file, format="audio/mp3")
    
    # Transcription
    st.write("🔄 Transcribing...")
    result = model.transcribe(temp_audio_path)
    transcript = result["text"]
    
    st.subheader("📝 Transcription (Original Text)")
    st.text_area("", transcript, height=150)
    
    # Select target language
    language_options = {"French": "fr", "Spanish": "es", "German": "de", "Urdu": "ur", "Chinese": "zh-cn"}
    target_lang = st.selectbox("Select translation language", list(language_options.keys()))
    
    if st.button("Translate"):
        translated_text = translator.translate(transcript, dest=language_options[target_lang]).text
        
        st.subheader("🌍 Translated Text")
        st.text_area("", translated_text, height=150)
    
    # Cleanup temporary file
    os.remove(temp_audio_path)
