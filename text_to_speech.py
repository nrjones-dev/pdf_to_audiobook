import os
from contextlib import closing

import boto3 as aws
from botocore.response import StreamingBody
from dotenv import load_dotenv


class Config:
    """Handles loading and storing of config from environment variables file"""

    def __init__(self) -> None:
        load_dotenv()
        self.aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
        self.aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
        self.aws_region = os.getenv("AWS_DEFAULT_REGION")


class TextToSpeechClient:
    def __init__(self, config: Config) -> None:
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

    def __init__(self, dir_path: str, file_name: str) -> None:
        self.dir_path = dir_path
        self.file_name = file_name
        self.save_location = os.path.join(self.dir_path, self.file_name)

    def save_audio(self, audio_stream: StreamingBody) -> None:
        with closing(audio_stream) as stream:
            with open(self.save_location, "wb") as file:
                file.write(stream.read())
