from deepgram import Deepgram
import asyncio
import os
from dotenv import load_dotenv
from tqdm import tqdm

load_dotenv()
DEEPGRAM_API_KEY = os.getenv('DEEPGRAM_API_KEY')
SAVE_PATH = os.getenv('SAVE_PATH')
AUDIO_PATH_INIT = os.getenv('AUDIO_PATH_INIT')
AUDIO_PATH_FIN = os.getenv('AUDIO_PATH_FIN')

async def main():
    deepgram = Deepgram(DEEPGRAM_API_KEY)

    for file in tqdm(os.listdir(AUDIO_PATH_INIT)):
        file_path = os.path.join(AUDIO_PATH_INIT, file)
        with open (file_path, "rb") as audio:
            source = { 'buffer': audio, 'mimetype': 'audio/mp3' }
            transcription_options = { 'punctuate': True, 'diarize': True, 'paragraphs': True }
            response = await deepgram.transcription.prerecorded(source, transcription_options)
            transcript = response['results']['channels'][0]['alternatives'][0]['paragraphs']['transcript']
            completeName = os.path.join(SAVE_PATH, file+".txt")
           
            with open(completeName, 'w') as f:
                f.write(transcript)

        os.rename(file_path, os.path.join(AUDIO_PATH_FIN, file))

if __name__ == '__main__':
    asyncio.run(main())