from text_to_speech import Config, TextToSpeechClient, SaveStream
from pdf_reader import PDFReader


if __name__ == "__main__":
    config = Config()

    pdf_reader = PDFReader("pdf_books/Book1.pdf")
    pdf_text = pdf_reader.extract_text(12)

    tts_client = TextToSpeechClient(config)
    
    voice_selection = tts_client.describe_voices()
    
    response = tts_client.synthesize_speech(pdf_text)
    
    audio_output = SaveStream("tts_output/", "output_file.mp3")
    
    audio_output.save_audio(response.get("AudioStream"))
