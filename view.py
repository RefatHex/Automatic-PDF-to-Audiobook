import base64
from edge_tts import VoicesManager
import edge_tts
from moviepy.editor import AudioFileClip, concatenate_audioclips
import streamlit as st
import os
import asyncio
from uuid import uuid4
import tika
from tika import parser
tika.initVM()
output_placeholder = st.empty()


def main():
    st.title("Audiobook Generator")

    uploaded_file = st.file_uploader("Upload PDF", type="pdf")

    if uploaded_file is not None:
        progress_bar = st.progress(0)

        final_audio_path = process_pdf(uploaded_file, progress_bar)

        if final_audio_path:
            print("Final audio path:", final_audio_path)

            st.audio(final_audio_path, format='audio/mp3', start_time=0)

            st.markdown(get_binary_file_downloader_html(
                final_audio_path), unsafe_allow_html=True)


def process_pdf(uploaded_file, progress_bar):
    filename = uploaded_file.name
    base_name, extension = os.path.splitext(filename)
    output_dir = os.path.join("output", base_name)
    os.makedirs(output_dir, exist_ok=True)
    pdf_path = os.path.join(output_dir, filename)
    with open(pdf_path, "wb") as f:
        f.write(uploaded_file.getvalue())
    final_audio_path = asyncio.run(read_book(pdf_path, progress_bar))

    return final_audio_path


async def read_book(path: str, progress_bar, chunk_size=500) -> str:
    raw = parser.from_file(path)
    text = raw["content"]

    chunks = [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]
    output_dir = path.replace(" ", "_").replace(".", "_")
    os.makedirs(output_dir, exist_ok=True)

    for i, chunk in enumerate(chunks):
        tts = TextToSpeech(chunk, ["en-US-GuyNeural"], output_dir=output_dir)
        await tts.generate_audio()
        progress_bar.progress((i + 1) / len(chunks))

    audio_clips = [AudioFileClip(audio_file)
                   for audio_file in TextToSpeech.audio_files]
    final_audio = concatenate_audioclips(audio_clips)

    final_audio_path = f"{output_dir}.mp3"
    final_audio.write_audiofile(final_audio_path)

    for audio_file in TextToSpeech.audio_files:
        os.remove(audio_file)

    return final_audio_path


class TextToSpeech:
    audio_files = []

    def __init__(self, text, voices, output_dir='output'):
        self.text = text
        self.voices = voices
        self.output_dir = output_dir

    async def generate_audio(self):
        os.makedirs(self.output_dir, exist_ok=True)

        for voice in self.voices:
            communicate = edge_tts.Communicate(self.text, voice)
            output_file = os.path.join(self.output_dir, f"{uuid4()}.mp3")
            await communicate.save(output_file)
            TextToSpeech.audio_files.append(output_file)


def get_binary_file_downloader_html(bin_file, file_label='File'):
    with open(bin_file, 'rb') as f:
        data = f.read()
    bin_str = base64.b64encode(data).decode()
    href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{os.path.basename(bin_file)}">Click here to download {file_label}</a>'
    return href


if __name__ == "__main__":
    main()
