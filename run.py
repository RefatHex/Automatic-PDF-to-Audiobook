import os
import asyncio
from uuid import uuid4
import edge_tts
from edge_tts import VoicesManager
from tika import parser
from moviepy.editor import AudioFileClip, concatenate_audioclips

audio_files = [] 


class TextToSpeech:
    def __init__(self, text, voices, output_dir='output'):
        self.text = text
        self.voices = voices
        self.output_dir = output_dir

    async def generate_audio(self):
        os.makedirs(self.output_dir, exist_ok=True)

        for voice in self.voices:
            communicate = edge_tts.Communicate(self.text, voice)
            output_file = f"{uuid4()}.mp3"

            output_path = os.path.join(self.output_dir, output_file)
            await communicate.save(output_path)

            audio_files.append(output_path)

    def set_text(self, text):
        self.text = text

    def set_voices(self, voices):
        self.voices = voices

    def set_output_dir(self, output_dir):
        self.output_dir = output_dir

##This Error handled the file path exists and is a PDF before proceeding


async def main():
 
    pdf_path = input("Enter the path of the PDF: ").strip()

    
    if not os.path.exists(pdf_path) or not pdf_path.lower().endswith('.pdf'):
        print("Error: PDF file not found or invalid file type.")
        return

    try:
        final_audio_file = await read_book(pdf_path)
        print(f"Audio file generated: {final_audio_file}")
    except Exception as e:
        print(f"Failed to generate audio book: {e}")



async def read_book(path: str, chunk_size=500) -> str:
    raw = parser.from_file(path)
    text = raw["content"]

    print(f"Reading book from '{path}'")

    chunks = [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]
    output_dir = path.replace(" ", "_").replace(".", "_")

    for chunk in chunks:
        tts = TextToSpeech(chunk, ["en-US-GuyNeural"], output_dir=output_dir)
        await tts.generate_audio()

    audio_clips = [AudioFileClip(audio_file) for audio_file in audio_files]
    final_audio = concatenate_audioclips(audio_clips)

    final_audio_file = f"final-{output_dir}.mp3"
    final_audio.write_audiofile(final_audio_file)

    return final_audio_file


if __name__ == "__main__":
    loop = asyncio.get_event_loop_policy().get_event_loop()
    try:
        loop.run_until_complete(main())
    finally:
        loop.close()
