import os
import json
import tempfile
import wave
from typing import Optional, Dict, List
from pathlib import Path

class VoiceTranscriber:
    """Voice-to-Text Transcription Toolkit - 语音转文字工具包"""

    SUPPORTED_FORMATS = ['.wav', '.mp3', '.m4a', '.flac', '.ogg', '.webm']

    def __init__(self, engine: str = "whisper", model_size: str = "base"):
        self.engine = engine
        self.model_size = model_size
        self._model = None
        self._load_model()

    def _load_model(self):
        """加载语音识别模型"""
        if self.engine == "whisper":
            try:
                import whisper
                self._model = whisper.load_model(self.model_size)
            except ImportError:
                print("Warning: whisper not installed. Install with: pip install openai-whisper")
                self._model = None
        elif self.engine == "vosk":
            try:
                from vosk import Model
                self._model = Model(lang="en")
            except ImportError:
                print("Warning: vosk not installed. Install with: pip install vosk")
                self._model = None

    def transcribe(self, audio_path: str, language: Optional[str] = None,
                   output_format: str = "text") -> Dict:
        """
        转录音频文件为文字

        Args:
            audio_path: 音频文件路径
            language: 语言代码 (如 'en', 'zh', 'ja')，None表示自动检测
            output_format: 输出格式 ('text', 'json', 'srt', 'vtt')

        Returns:
            Dict 包含 text, segments, language 等信息
        """
        ext = Path(audio_path).suffix.lower()
        if ext not in self.SUPPORTED_FORMATS:
            raise ValueError(f"Unsupported format: {ext}. Supported: {self.SUPPORTED_FORMATS}")

        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"Audio file not found: {audio_path}")

        if self._model is None:
            # Fallback: 返回模拟结果（当模型未安装时用于演示）
            return self._mock_transcribe(audio_path, language)

        if self.engine == "whisper":
            return self._transcribe_whisper(audio_path, language, output_format)
        elif self.engine == "vosk":
            return self._transcribe_vosk(audio_path, language)
        else:
            raise ValueError(f"Unknown engine: {self.engine}")

    def _transcribe_whisper(self, audio_path: str, language: Optional[str],
                            output_format: str) -> Dict:
        import whisper

        options = {}
        if language:
            options["language"] = language

        result = self._model.transcribe(audio_path, **options)

        segments = []
        for seg in result.get("segments", []):
            segments.append({
                "id": seg.get("id", 0),
                "start": seg.get("start", 0.0),
                "end": seg.get("end", 0.0),
                "text": seg.get("text", "").strip(),
            })

        return {
            "text": result["text"].strip(),
            "language": result.get("language", "unknown"),
            "segments": segments,
            "duration": segments[-1]["end"] if segments else 0,
            "engine": self.engine,
            "model": self.model_size,
        }

    def _transcribe_vosk(self, audio_path: str, language: Optional[str]) -> Dict:
        from vosk import KaldiRecognizer
        import wave

        wf = wave.open(audio_path, "rb")
        rec = KaldiRecognizer(self._model, wf.getframerate())

        text_parts = []
        while True:
            data = wf.readframes(4000)
            if len(data) == 0:
                break
            if rec.AcceptWaveform(data):
                part = json.loads(rec.Result())
                if part.get("text"):
                    text_parts.append(part["text"])

        final = json.loads(rec.FinalResult())
        if final.get("text"):
            text_parts.append(final["text"])

        full_text = " ".join(text_parts)

        return {
            "text": full_text,
            "language": language or "unknown",
            "segments": [],
            "duration": wf.getnframes() / wf.getframerate(),
            "engine": self.engine,
            "model": "vosk",
        }

    def _mock_transcribe(self, audio_path: str, language: Optional[str]) -> Dict:
        """模拟转录（用于无模型环境演示）"""
        import random
        sample_texts = {
            "en": "This is a sample transcription. The quick brown fox jumps over the lazy dog.",
            "zh": "这是一个示例转录。今天天气很好，适合出去散步。",
            "ja": "これはサンプルの文字起こしです。今日は良い天気です。",
            "es": "Esta es una transcripción de muestra. El clima está muy bueno hoy.",
        }
        lang = language or random.choice(list(sample_texts.keys()))
        text = sample_texts.get(lang, sample_texts["en"])

        return {
            "text": text,
            "language": lang,
            "segments": [
                {"id": 0, "start": 0.0, "end": 2.5, "text": text[:30]},
                {"id": 1, "start": 2.5, "end": 5.0, "text": text[30:]},
            ],
            "duration": 5.0,
            "engine": self.engine,
            "model": f"{self.model_size} (mock)",
            "note": "Mock result - install whisper/vosk for real transcription",
        }

    def transcribe_batch(self, audio_paths: List[str], language: Optional[str] = None) -> List[Dict]:
        """批量转录多个音频文件"""
        results = []
        for path in audio_paths:
            try:
                result = self.transcribe(path, language)
                result["file"] = path
                result["success"] = True
            except Exception as e:
                result = {
                    "file": path,
                    "success": False,
                    "error": str(e),
                }
            results.append(result)
        return results

    def export_subtitles(self, transcription: Dict, format_type: str = "srt") -> str:
        """将转录结果导出为字幕格式"""
        segments = transcription.get("segments", [])

        if format_type == "srt":
            lines = []
            for seg in segments:
                start = self._seconds_to_srt_time(seg["start"])
                end = self._seconds_to_srt_time(seg["end"])
                lines.append(f"{seg['id'] + 1}")
                lines.append(f"{start} --> {end}")
                lines.append(seg["text"])
                lines.append("")
            return "\n".join(lines)

        elif format_type == "vtt":
            lines = ["WEBVTT", ""]
            for seg in segments:
                start = self._seconds_to_vtt_time(seg["start"])
                end = self._seconds_to_vtt_time(seg["end"])
                lines.append(f"{start} --> {end}")
                lines.append(seg["text"])
                lines.append("")
            return "\n".join(lines)

        else:
            raise ValueError(f"Unsupported subtitle format: {format_type}")

    def _seconds_to_srt_time(self, seconds: float) -> str:
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        millis = int((seconds % 1) * 1000)
        return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"

    def _seconds_to_vtt_time(self, seconds: float) -> str:
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        millis = int((seconds % 1) * 1000)
        return f"{hours:02d}:{minutes:02d}:{secs:02d}.{millis:03d}"


class AudioConverter:
    """音频格式转换工具"""

    SUPPORTED_INPUT = ['.mp3', '.m4a', '.flac', '.ogg', '.webm', '.aac']

    def __init__(self):
        self.ffmpeg_available = self._check_ffmpeg()

    def _check_ffmpeg(self) -> bool:
        import subprocess
        try:
            subprocess.run(["ffmpeg", "-version"], capture_output=True, check=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False

    def convert_to_wav(self, input_path: str, output_path: Optional[str] = None,
                       sample_rate: int = 16000) -> str:
        """
        将任意格式音频转换为WAV (Whisper/Vosk 推荐格式)
        """
        if not self.ffmpeg_available:
            raise RuntimeError("ffmpeg not found. Install with: apt install ffmpeg or brew install ffmpeg")

        import subprocess

        if output_path is None:
            base = Path(input_path).stem
            output_path = f"{base}_converted.wav"

        cmd = [
            "ffmpeg", "-i", input_path,
            "-ar", str(sample_rate),
            "-ac", "1",
            "-c:a", "pcm_s16le",
            "-y", output_path
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            raise RuntimeError(f"ffmpeg conversion failed: {result.stderr}")

        return output_path

    def get_audio_info(self, audio_path: str) -> Dict:
        """获取音频文件信息"""
        import subprocess

        cmd = [
            "ffprobe", "-v", "quiet", "-print_format", "json",
            "-show_format", "-show_streams", audio_path
        ]

        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            data = json.loads(result.stdout)

            format_info = data.get("format", {})
            stream = data.get("streams", [{}])[0]

            return {
                "duration": float(format_info.get("duration", 0)),
                "bitrate": int(format_info.get("bit_rate", 0)),
                "format": format_info.get("format_name", "unknown"),
                "sample_rate": int(stream.get("sample_rate", 0)),
                "channels": int(stream.get("channels", 0)),
                "codec": stream.get("codec_name", "unknown"),
            }
        except Exception as e:
            return {"error": str(e)}


if __name__ == "__main__":
    # 演示
    transcriber = VoiceTranscriber()

    # 创建一个模拟WAV文件用于演示
    demo_path = "demo_audio.wav"
    with wave.open(demo_path, 'w') as f:
        f.setnchannels(1)
        f.setsampwidth(2)
        f.setframerate(16000)
        f.writeframes(b'\x00' * 16000 * 2 * 3)  # 3 seconds of silence

    result = transcriber.transcribe(demo_path, language="en")
    print(json.dumps(result, indent=2, ensure_ascii=False))

    # 导出字幕
    srt = transcriber.export_subtitles(result, "srt")
    print(f"\nSRT:\n{srt}")

    os.remove(demo_path)
