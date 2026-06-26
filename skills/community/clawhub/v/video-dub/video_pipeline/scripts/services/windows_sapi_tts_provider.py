import re
import subprocess
import wave
from pathlib import Path

from services.tts_base import TTSProvider


class WindowsSapiTTSProvider(TTSProvider):
    POWERSHELL_EXE = r"C:\WINDOWS\System32\WindowsPowerShell\v1.0\powershell.exe"

    def __init__(self, voice: str = "Microsoft Huihui Desktop", rate: int = 0) -> None:
        self.voice = voice
        self.rate = rate

    def synthesize(self, text: str, output_path: Path, context_text: str = "") -> tuple[str, float]:
        output_path = output_path.with_suffix(".wav")
        output_path.parent.mkdir(parents=True, exist_ok=True)

        if not output_path.exists():
            self._save_tts(text.strip() or " ", output_path)

        duration = self._get_media_duration(output_path)
        return str(output_path), float(duration)

    def _save_tts(self, text: str, output_path: Path) -> None:
        safe_voice = self.voice.replace("'", "''")
        safe_output_path = str(output_path).replace("'", "''")
        text_file_path = output_path.with_name(f"{output_path.stem}_input.txt")
        script_file_path = output_path.with_name(f"{output_path.stem}_tts.ps1")
        text_file_path.write_text(text, encoding="utf-8-sig")

        safe_text_file_path = str(text_file_path).replace("'", "''")
        script = (
            "$ErrorActionPreference = 'Stop'\n"
            "Add-Type -AssemblyName System.Speech\n"
            "$synth = New-Object System.Speech.Synthesis.SpeechSynthesizer\n"
            f"$synth.SelectVoice('{safe_voice}')\n"
            f"$synth.Rate = {self.rate}\n"
            f"$synth.SetOutputToWaveFile('{safe_output_path}')\n"
            f"$text = Get-Content -Raw -Encoding UTF8 '{safe_text_file_path}'\n"
            "$synth.Speak($text)\n"
            "$synth.SetOutputToNull()\n"
            "$synth.Dispose()\n"
        )
        script_file_path.write_text(script, encoding="utf-8-sig")
        result = subprocess.run(
            [self.POWERSHELL_EXE, "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(script_file_path)],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
            text=True,
        )
        try:
            text_file_path.unlink(missing_ok=True)
        except Exception:
            pass
        try:
            script_file_path.unlink(missing_ok=True)
        except Exception:
            pass
        if result.returncode != 0:
            raise RuntimeError(result.stderr.strip() or "Windows SAPI TTS generation failed")

    @staticmethod
    def _get_media_duration(path: Path) -> float:
        if path.suffix.lower() == ".wav":
            with wave.open(str(path), "rb") as wav_file:
                frames = wav_file.getnframes()
                frame_rate = wav_file.getframerate()
                if frame_rate > 0:
                    return frames / float(frame_rate)

        result = subprocess.run(["ffmpeg", "-i", str(path)], capture_output=True, text=True)
        duration_match = re.search(r"Duration:\s*(\d+):(\d+):(\d+(?:\.\d+)?)", result.stderr)
        if duration_match:
            hours = int(duration_match.group(1))
            minutes = int(duration_match.group(2))
            seconds = float(duration_match.group(3))
            return hours * 3600 + minutes * 60 + seconds
        raise RuntimeError(f"Unable to determine media duration for {path}")
