import moviepy.editor as mp
import whisper
from deep_translator import GoogleTranslator
import os

def extract_audio(video_path, audio_path="audio.wav"):
    clip = mp.VideoFileClip(video_path)
    clip.audio.write_audiofile(audio_path)
    return audio_path

def transcribe_audio(audio_path):
    model = whisper.load_model("base")
    result = model.transcribe(audio_path)
    return result['text']

def translate_text(text, target_lang="fa"):
    return GoogleTranslator(source='auto', target=target_lang).translate(text)

def make_srt(translated_text, output_path="subtitles.srt"):
    lines = translated_text.split(".")
    with open(output_path, "w", encoding="utf-8") as f:
        for i, line in enumerate(lines):
            if not line.strip():
                continue
            f.write(f"{i+1}
")
            f.write(f"00:00:{i*5:02d},000 --> 00:00:{(i+1)*5:02d},000
")
            f.write(line.strip() + ".

")
    return output_path

def process_video(video_path):
    audio_path = extract_audio(video_path)
    text = transcribe_audio(audio_path)
    translated = translate_text(text)
    subtitle_path = make_srt(translated)
    return subtitle_path
