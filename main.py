import sys

from pdf_reader import PDFReader
from text_to_speech import Config, SaveStream, TextToSpeechClient

if __name__ == "__main__":
    config = Config()

    pdf_reader = PDFReader(sys.argv[1])
    pdf_text = pdf_reader.extract_text(0)

    tts_client = TextToSpeechClient(config)

    voice_selection = tts_client.describe_voices()

    response = tts_client.synthesize_speech(pdf_text)

    audio_output = SaveStream("tts_output/", "output_file.mp3")

    audio_output.save_audio(response.get("AudioStream"))
