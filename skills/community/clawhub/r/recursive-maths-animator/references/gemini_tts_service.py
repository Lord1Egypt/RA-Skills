"""
Gemini TTS Service for manim-voiceover

Requires: pip install google-genai
API Key: Set GEMINI_API_KEY environment variable

Usage:
    from gemini_tts_service import GeminiTTSService
    self.set_speech_service(GeminiTTSService(voice_name="Charon"))

Available voices: Charon, Aoede, Kore, Zephyr, Leda, Orus
"""

import os
import struct
import mimetypes
from pathlib import Path
from google import genai
from google.genai import types

from manim_voiceover.services.base import SpeechService


def parse_audio_mime_type(mime_type: str) -> dict[str, int | None]:
    """Parses bits per sample and rate from an audio MIME type string.

    Assumes bits per sample is encoded like "L16" and rate as "rate=xxxxx".

    Args:
        mime_type: The audio MIME type string (e.g., "audio/L16;rate=24000").

    Returns:
        A dictionary with "bits_per_sample" and "rate" keys.
    """
    bits_per_sample = 16
    rate = 24000

    # Extract rate from parameters
    parts = mime_type.split(";")
    for param in parts:
        param = param.strip()
        if param.lower().startswith("rate="):
            try:
                rate_str = param.split("=", 1)[1]
                rate = int(rate_str)
            except (ValueError, IndexError):
                pass
        elif param.startswith("audio/L"):
            try:
                bits_per_sample = int(param.split("L", 1)[1])
            except (ValueError, IndexError):
                pass

    return {"bits_per_sample": bits_per_sample, "rate": rate}


def convert_to_wav(audio_data: bytes, mime_type: str) -> bytes:
    """Convert audio data to WAV format.

    Handles Gemini TTS output which is PCM16 raw audio (audio/L16;codec=pcm;rate=24000).
    Adds a proper WAV header to the raw PCM data.

    Args:
        audio_data: The raw audio data as a bytes object.
        mime_type: Mime type of the audio data.

    Returns:
        A bytes object representing the complete WAV file.
    """
    # Parse mime type for parameters
    # Format: audio/L16;codec=pcm;rate=24000
    sample_rate = 24000  # Default
    bits_per_sample = 16  # Default for L16

    if "rate=" in mime_type:
        try:
            sample_rate = int(mime_type.split("rate=")[1].split(";")[0])
        except (ValueError, IndexError):
            pass

    if "L16" in mime_type:
        bits_per_sample = 16

    num_channels = 1
    data_size = len(audio_data)
    bytes_per_sample = bits_per_sample // 8
    block_align = num_channels * bytes_per_sample
    byte_rate = sample_rate * block_align
    chunk_size = 36 + data_size

    # Create WAV header
    header = struct.pack(
        "<4sI4s4sIHHIIHH4sI",
        b"RIFF",          # ChunkID
        chunk_size,       # ChunkSize (total file size - 8 bytes)
        b"WAVE",          # Format
        b"fmt ",          # Subchunk1ID
        16,               # Subchunk1Size (16 for PCM)
        1,                # AudioFormat (1 for PCM)
        num_channels,     # NumChannels
        sample_rate,      # SampleRate
        byte_rate,        # ByteRate
        block_align,      # BlockAlign
        bits_per_sample,  # BitsPerSample
        b"data",          # Subchunk2ID
        data_size         # Subchunk2Size (size of audio data)
    )

    return header + audio_data


class GeminiTTSService(SpeechService):
    """
    Gemini TTS Service for manim-voiceover

    High-quality neural TTS from Google's Gemini API.
    Supports voice control via natural language prompts.

    Args:
        voice_name: Voice to use (Charon, Aoede, Kore, Zephyr, Leda, Orus)
        scene_description: Optional scene context for voice styling
        sample_context: Optional sample context for tone/pacing
        temperature: Creativity parameter (0.0 - 2.0, default 1.0)
        api_key: Gemini API key (or set GEMINI_API_KEY env var)
        transcription_model: Model for transcription (default: whisper-1)

    Example:
        service = GeminiTTSService(
            voice_name="Charon",
            scene_description="A professional business presentation",
            sample_context="Clear, authoritative tone with measured pace"
        )
    """

    AVAILABLE_VOICES = ["Charon", "Aoede", "Kore", "Zephyr", "Leda", "Orus"]

    def __init__(
        self,
        voice_name: str = "Charon",
        scene_description: str = "",
        sample_context: str = "",
        temperature: float = 1.0,
        api_key: str = None,
        transcription_model: str = "whisper-1",
        **kwargs
    ):
        self.voice_name = voice_name
        self.scene_description = scene_description
        self.sample_context = sample_context
        self.temperature = temperature
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY")
        self.transcription_model = transcription_model

        if not self.api_key:
            raise ValueError(
                "Gemini API key required. Set GEMINI_API_KEY environment variable "
                "or pass api_key parameter."
            )

        if self.voice_name not in self.AVAILABLE_VOICES:
            raise ValueError(
                f"Voice '{voice_name}' not available. "
                f"Choose from: {', '.join(self.AVAILABLE_VOICES)}"
            )

        self.client = genai.Client(api_key=self.api_key)
        self.model = "gemini-2.5-flash-preview-tts"

        super().__init__(**kwargs)

    def generate_from_text(self, text: str, path: str = None, cache_dir: str = None, **kwargs) -> dict:
        """
        Generate speech from text using Gemini TTS.

        Returns dict with:
            - audio_path: Path to generated audio file
            - word_boundaries: List of (word, start_time, end_time) tuples
        """
        # Handle cache_dir and path like other services (e.g., GTTSService)
        if cache_dir is None:
            cache_dir = self.cache_dir

        if path is None:
            audio_path = self.get_audio_basename(input_text=text) + ".wav"
        else:
            audio_path = path

        # Full output path includes cache_dir
        output_path = Path(cache_dir) / audio_path

        # Build prompt with scene context if provided
        prompt_parts = []
        if self.scene_description:
            prompt_parts.append(f"## Scene:\n{self.scene_description}")
        if self.sample_context:
            prompt_parts.append(f"## Sample Context:\n{self.sample_context}")
        prompt_parts.append(f"## Transcript:\n{text}")
        full_prompt = "\n\n".join(prompt_parts)

        contents = [
            types.Content(
                role="user",
                parts=[types.Part.from_text(text=full_prompt)],
            ),
        ]

        config = types.GenerateContentConfig(
            temperature=self.temperature,
            response_modalities=["audio"],
            speech_config=types.SpeechConfig(
                voice_config=types.VoiceConfig(
                    prebuilt_voice_config=types.PrebuiltVoiceConfig(
                        voice_name=self.voice_name
                    )
                )
            ),
        )

        # Collect audio chunks
        audio_chunks = []
        for chunk in self.client.models.generate_content_stream(
            model=self.model,
            contents=contents,
            config=config,
        ):
            if chunk.parts and chunk.parts[0].inline_data:
                inline_data = chunk.parts[0].inline_data
                if inline_data and inline_data.data:
                    audio_chunks.append((inline_data.data, inline_data.mime_type))

        if not audio_chunks:
            raise RuntimeError("No audio generated from Gemini TTS")

        # Combine chunks and convert to WAV
        combined_audio = b""
        for data, mime_type in audio_chunks:
            file_extension = mimetypes.guess_extension(mime_type)
            if file_extension is None or file_extension not in [".wav", ".mp3", ".ogg"]:
                # Convert to WAV if needed
                data = convert_to_wav(data, mime_type)
            combined_audio += data if not combined_audio else data

        # Save to file
        output_path = Path(output_path)

        # Ensure parent directory exists (handle both relative and absolute paths)
        if not output_path.parent.is_absolute():
            # If relative, ensure parent exists relative to current working directory
            output_path.parent.mkdir(parents=True, exist_ok=True)
        else:
            output_path.parent.mkdir(parents=True, exist_ok=True)

        print(f"[GeminiTTS] Saving audio to: {output_path.absolute()}")

        with open(output_path, "wb") as f:
            f.write(combined_audio)

        print(f"[GeminiTTS] Audio saved successfully: {output_path.exists()}")

        # Return format expected by manim-voiceover
        # original_audio should be relative to cache_dir (just the filename)
        return {
            "audio_path": audio_path,
            "original_audio": audio_path,
            "word_boundaries": [],  # Gemini doesn't provide word boundaries
            "input_text": text,  # Required by VoiceoverTracker
        }

    def get_audio_basename(self, input_text: str = None, **kwargs) -> str:
        """Generate unique basename for audio file."""
        import hashlib
        if input_text:
            hash_str = hashlib.md5(input_text.encode()).hexdigest()[:12]
            return f"gemini_tts_{self.voice_name.lower()}_{hash_str}"
        return f"gemini_tts_{self.voice_name.lower()}_{id(self)}"


if __name__ == "__main__":
    # Test the service
    import tempfile

    service = GeminiTTSService(voice_name="Charon")
    result = service.generate_from_text(
        "Hello, this is a test of the Gemini TTS service.",
        output_path="/tmp/test_gemini_tts.wav"
    )
    print(f"Audio saved to: {result['audio_path']}")
