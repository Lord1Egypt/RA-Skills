# Unified STT Engine Interface

class STTEngine:
    def __init__(self, engine_type):
        self.engine_type = engine_type

    def transcribe(self, audio_file):
        if self.engine_type == 'SenseVoice':
            return self.transcribe_with_sensevoice(audio_file)
        elif self.engine_type == 'Whisper':
            return self.transcribe_with_whisper(audio_file)
        elif self.engine_type == 'Vosk':
            return self.transcribe_with_vosk(audio_file)
        else:
            raise ValueError('Unsupported STT engine type')

    def transcribe_with_sensevoice(self, audio_file):
        # Implement SenseVoice transcription logic here
        return 'Transcribed text from SenseVoice'

    def transcribe_with_whisper(self, audio_file):
        # Implement Whisper transcription logic here
        return 'Transcribed text from Whisper'

    def transcribe_with_vosk(self, audio_file):
        # Implement Vosk transcription logic here
        return 'Transcribed text from Vosk'