import os
from contextlib import closing

import boto3 as aws
from dotenv import load_dotenv
from pypdf import PdfReader


class Config:
    """Handles loading and storing of config from environment variables file"""

    def __init__(self) -> None:
        load_dotenv()
        self.aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
        self.aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
        self.aws_region = os.getenv("AWS_DEFAULT_REGION")


class PDFReader:
    """Opens and handles data from a PDF, extracting text from specific pages."""

    def __init__(self, pdf_file_path: str) -> None:
        self.file_path = pdf_file_path
        self.reader = PdfReader(self.file_path)

    def extract_text(self, page_number):
        page = self.reader.pages[page_number]
        return page.extract_text()


class TextToSpeechClient:
    def __init__(self, config) -> None:
        self.client = aws.client(
            "polly",
            aws_access_key_id=config.aws_access_key,
            aws_secret_access_key=config.aws_secret_key,
            region_name=config.aws_region,
        )

    def describe_voices(self) -> dict:
        return self.client.describe_voices(
            Engine="standard",
            LanguageCode="en-GB",
            IncludeAdditionalLanguageCodes=False,
        )

    def synthesize_speech(self, text: str) -> dict:
        return self.client.synthesize_speech(
            Engine="standard",
            LanguageCode="en-GB",
            OutputFormat="mp3",
            Text=text,
            VoiceId="Amy",
        )

class SaveStream:
    """Saves the audio stream from TTS client to a file."""
    def __init__(self, dir_path, file_name) -> None:
        self.dir_path = dir_path
        self.file_name = file_name
        self.save_location = os.path.join(self.dir_path, self.file_name)
        
        
    def save_audio(self, audio_stream):
        with closing(audio_stream) as stream:
            with open(self.save_location, "wb") as file:
                file.write(stream.read())
                

if __name__ == "__main__":
    config = Config()
    
    pdf_reader = PDFReader("pdf_books/Book1.pdf")
    pdf_text = pdf_reader.extract_text(12)
    
    tts_client = TextToSpeechClient(config)
    
    voice_selection = tts_client.describe_voices()
    
    response = tts_client.synthesize_speech(pdf_text)
    
    audio_output = SaveStream("tts_output/", "output_file.mp3")
    
    audio_output.save_audio(response.get("AudioStream"))