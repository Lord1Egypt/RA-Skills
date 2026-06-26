"""
Speech-to-text transcription using Whisper
"""
import subprocess
import json
from pathlib import Path
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, asdict


@dataclass
class TranscriptionSegment:
    """A segment of transcribed text with timing"""
    start: float  # Start time in seconds
    end: float    # End time in seconds
    text: str     # Transcribed text
    confidence: float = 1.0  # Confidence score


@dataclass
class TranscriptionResult:
    """Complete transcription result"""
    success: bool
    segments: List[TranscriptionSegment]
    full_text: str
    language: str
    duration: float
    error: Optional[str] = None


class Transcriber:
    """Transcribe audio/video to text using Whisper"""
    
    def __init__(self, model: str = "base", language: str = "zh"):
        """
        Initialize transcriber
        
        Args:
            model: Whisper model (tiny, base, small, medium, large)
            language: Language code (zh for Chinese, en for English)
        """
        self.model = model
        self.language = language
    
    def transcribe(self, audio_path: Path, output_dir: Optional[Path] = None) -> TranscriptionResult:
        """
        Transcribe audio/video file
        
        Args:
            audio_path: Path to audio or video file
            output_dir: Directory for output files (optional)
        
        Returns:
            TranscriptionResult with segments and text
        """
        if not audio_path.exists():
            return TranscriptionResult(
                success=False,
                segments=[],
                full_text="",
                language=self.language,
                duration=0,
                error=f"Audio file not found: {audio_path}"
            )
        
        try:
            print(f"🎤 Transcribing: {audio_path.name}")
            print(f"   Model: {self.model}, Language: {self.language}")
            
            # Use whisper-cli or faster-whisper if available
            result = self._transcribe_with_whisper(audio_path, output_dir)
            
            if result:
                print(f"✅ Transcription complete: {len(result.segments)} segments")
                return result
            
            # Fallback to alternative methods
            return self._transcribe_fallback(audio_path, output_dir)
            
        except Exception as e:
            return TranscriptionResult(
                success=False,
                segments=[],
                full_text="",
                language=self.language,
                duration=0,
                error=str(e)
            )
    
    def _transcribe_with_whisper(self, audio_path: Path, output_dir: Optional[Path]) -> Optional[TranscriptionResult]:
        """Transcribe using whisper-cli"""
        try:
            # Check if whisper is available
            result = subprocess.run(
                ["whisper", "--version"],
                capture_output=True,
                text=True
            )
            
            if result.returncode != 0:
                return None
            
            # Run whisper
            temp_dir = output_dir or audio_path.parent
            output_path = temp_dir / f"{audio_path.stem}.json"
            
            cmd = [
                "whisper",
                str(audio_path),
                "--model", self.model,
                "--language", self.language,
                "--output_format", "json",
                "--output_dir", str(temp_dir),
                "--word_timestamps", "True"
            ]
            
            process = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=3600  # 1 hour timeout for long videos
            )
            
            if process.returncode != 0:
                print(f"Whisper error: {process.stderr}")
                return None
            
            # Parse output JSON
            json_path = temp_dir / f"{audio_path.stem}.json"
            if not json_path.exists():
                return None
            
            return self._parse_whisper_output(json_path, audio_path)
            
        except FileNotFoundError:
            return None
        except subprocess.TimeoutExpired:
            print("⚠️  Transcription timed out")
            return None
        except Exception as e:
            print(f"Whisper error: {e}")
            return None
    
    def _transcribe_fallback(self, audio_path: Path, output_dir: Optional[Path]) -> TranscriptionResult:
        """Fallback transcription using faster-whisper Python library"""
        try:
            from faster_whisper import WhisperModel
            
            print("🔄 Using faster-whisper library...")
            
            # Load model
            model_size = self.model
            device = "cpu"  # Can be "cuda" if available
            model = WhisperModel(model_size, device=device)
            
            # Transcribe
            segments, info = model.transcribe(
                str(audio_path),
                language=self.language if self.language != "auto" else None,
                word_timestamps=True
            )
            
            transcription_segments = []
            full_text = []
            
            for segment in segments:
                trans_segment = TranscriptionSegment(
                    start=segment.start,
                    end=segment.end,
                    text=segment.text.strip(),
                    confidence=segment.avg_logprob
                )
                transcription_segments.append(trans_segment)
                full_text.append(segment.text.strip())
            
            # Get duration from audio file
            duration = self._get_audio_duration(audio_path)
            
            return TranscriptionResult(
                success=True,
                segments=transcription_segments,
                full_text="".join(full_text),
                language=info.language,
                duration=duration
            )
            
        except ImportError:
            print("⚠️  faster-whisper not installed. Install with: pip install faster-whisper")
            return TranscriptionResult(
                success=False,
                segments=[],
                full_text="",
                language=self.language,
                duration=0,
                error="Whisper not available. Install whisper-cli or faster-whisper"
            )
        except Exception as e:
            return TranscriptionResult(
                success=False,
                segments=[],
                full_text="",
                language=self.language,
                duration=0,
                error=str(e)
            )
    
    def _parse_whisper_output(self, json_path: Path, audio_path: Path) -> TranscriptionResult:
        """Parse Whisper JSON output"""
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        segments = []
        full_text = []
        
        # Handle different Whisper output formats
        if "segments" in data:
            for seg in data["segments"]:
                text = seg.get("text", "").strip()
                if text:
                    segment = TranscriptionSegment(
                        start=seg.get("start", 0),
                        end=seg.get("end", 0),
                        text=text,
                        confidence=seg.get("avg_logprob", 1.0)
                    )
                    segments.append(segment)
                    full_text.append(text)
        
        # Get duration
        duration = self._get_audio_duration(audio_path)
        
        # Clean up JSON file
        json_path.unlink(missing_ok=True)
        
        return TranscriptionResult(
            success=True,
            segments=segments,
            full_text=" ".join(full_text),
            language=data.get("language", self.language),
            duration=duration
        )
    
    def _get_audio_duration(self, audio_path: Path) -> float:
        """Get audio duration in seconds using ffprobe"""
        try:
            cmd = [
                "ffprobe",
                "-v", "quiet",
                "-show_entries", "format=duration",
                "-of", "default=noprint_wrappers=1:nokey=1",
                str(audio_path)
            ]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                return float(result.stdout.strip())
            
            return 0
            
        except Exception:
            return 0
    
    def save_transcription(self, result: TranscriptionResult, output_path: Path):
        """Save transcription to file"""
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        data = {
            "success": result.success,
            "language": result.language,
            "duration": result.duration,
            "full_text": result.full_text,
            "segments": [asdict(seg) for seg in result.segments]
        }
        
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        # Also save plain text
        txt_path = output_path.with_suffix(".txt")
        with open(txt_path, "w", encoding="utf-8") as f:
            f.write(result.full_text)
        
        print(f"💾 Saved transcription: {output_path}")
    
    def load_transcription(self, json_path: Path) -> Optional[TranscriptionResult]:
        """Load transcription from JSON file"""
        if not json_path.exists():
            return None
        
        try:
            with open(json_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            segments = [
                TranscriptionSegment(**seg)
                for seg in data.get("segments", [])
            ]
            
            return TranscriptionResult(
                success=data.get("success", False),
                segments=segments,
                full_text=data.get("full_text", ""),
                language=data.get("language", "zh"),
                duration=data.get("duration", 0)
            )
            
        except Exception as e:
            print(f"Error loading transcription: {e}")
            return None


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        transcriber = Transcriber(model="base", language="zh")
        result = transcriber.transcribe(Path(sys.argv[1]))
        print(f"Success: {result.success}")
        print(f"Segments: {len(result.segments)}")
        print(f"Duration: {result.duration}s")
        print(f"Text preview: {result.full_text[:200]}...")
