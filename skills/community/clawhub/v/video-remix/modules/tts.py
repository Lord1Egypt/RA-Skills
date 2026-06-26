"""
Text-to-Speech using Edge-TTS (free, no API key required)
"""
import asyncio
import subprocess
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass


@dataclass
class TTSResult:
    """Result of TTS generation"""
    success: bool
    audio_path: Optional[Path] = None
    duration: float = 0.0
    error: Optional[str] = None


class EdgeTTS:
    """Generate speech using Edge-TTS"""
    
    # Common Chinese voices
    CHINESE_VOICES = {
        "xiaoxiao": "zh-CN-XiaoxiaoNeural",      # Female, warm (default)
        "yunxi": "zh-CN-YunxiNeural",            # Male, calm
        "yunjian": "zh-CN-YunjianNeural",        # Male, energetic
        "xiaoyi": "zh-CN-XiaoyiNeural",          # Female, lively
        "yunyang": "zh-CN-YunyangNeural",        # Male, professional
        "xiaochen": "zh-CN-XiaochenNeural",      # Female, gentle
        "xiaohan": "zh-CN-XiaohanNeural",        # Female, serious
        "xiaomeng": "zh-CN-XiaomengNeural",      # Female, cute
        "xiaomo": "zh-CN-XiaomoNeural",          # Female, varied
        "xiaoqiu": "zh-CN-XiaoqiuNeural",        # Female, mature
        "xiaorui": "zh-CN-XiaoruiNeural",        # Female, calm
        "xiaoshuang": "zh-CN-XiaoshuangNeural",  # Female, childlike
        "xiaoyan": "zh-CN-XiaoyanNeural",        # Female, gentle
        "xiaoyou": "zh-CN-XiaoyouNeural",        # Female, young
        "xiaozhen": "zh-CN-XiaozhenNeural",      # Female, warm
        "yunfeng": "zh-CN-YunfengNeural",        # Male, serious
        "yunhao": "zh-CN-YunhaoNeural",          # Male, advertising
        "yunxia": "zh-CN-YunxiaNeural",          # Male, passionate
        "yunye": "zh-CN-YunyeNeural",            # Male, professional
    }
    
    def __init__(
        self,
        voice: str = "zh-CN-XiaoxiaoNeural",
        rate: str = "+0%",
        volume: str = "+0%",
        pitch: str = "+0Hz"
    ):
        """
        Initialize Edge-TTS
        
        Args:
            voice: Voice name (e.g., "zh-CN-XiaoxiaoNeural")
            rate: Speech rate (+/- percentage, e.g., "+10%", "-20%")
            volume: Volume (+/- percentage)
            pitch: Pitch (+/- Hz)
        """
        self.voice = voice
        self.rate = rate
        self.volume = volume
        self.pitch = pitch
    
    @classmethod
    def list_voices(cls, language: str = "zh") -> Dict[str, str]:
        """List available voices for a language"""
        if language == "zh":
            return cls.CHINESE_VOICES
        return {}
    
    @classmethod
    async def fetch_voices(cls) -> List[Dict]:
        """Fetch all available voices from Edge-TTS"""
        try:
            import edge_tts
            
            voices = await edge_tts.list_voices()
            return voices
            
        except Exception as e:
            print(f"Error fetching voices: {e}")
            return []
    
    def generate(
        self,
        text: str,
        output_path: Path
    ) -> TTSResult:
        """
        Generate speech from text
        
        Args:
            text: Text to convert to speech
            output_path: Output audio file path
        
        Returns:
            TTSResult with audio path and duration
        """
        try:
            print(f"🔊 Generating speech: {text[:30]}...")
            
            # Ensure output directory exists
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Use edge-tts CLI
            cmd = [
                "edge-tts",
                "--voice", self.voice,
                "--text", text,
                "--write-media", str(output_path),
                "--rate", self.rate,
                "--volume", self.volume,
                "--pitch", self.pitch
            ]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=120
            )
            
            if result.returncode != 0:
                return TTSResult(
                    success=False,
                    error=f"edge-tts failed: {result.stderr}"
                )
            
            if not output_path.exists():
                return TTSResult(
                    success=False,
                    error="Audio file not created"
                )
            
            # Get duration
            duration = self._get_audio_duration(output_path)
            
            print(f"✅ Speech generated: {output_path.name} ({duration:.1f}s)")
            
            return TTSResult(
                success=True,
                audio_path=output_path,
                duration=duration
            )
            
        except subprocess.TimeoutExpired:
            return TTSResult(
                success=False,
                error="TTS generation timed out"
            )
        except Exception as e:
            return TTSResult(
                success=False,
                error=str(e)
            )
    
    async def generate_async(
        self,
        text: str,
        output_path: Path
    ) -> TTSResult:
        """Async version of generate"""
        try:
            import edge_tts
            
            print(f"🔊 Generating speech (async): {text[:30]}...")
            
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            communicate = edge_tts.Communicate(
                text,
                self.voice,
                rate=self.rate,
                volume=self.volume,
                pitch=self.pitch
            )
            
            await communicate.save(str(output_path))
            
            if not output_path.exists():
                return TTSResult(
                    success=False,
                    error="Audio file not created"
                )
            
            duration = self._get_audio_duration(output_path)
            
            print(f"✅ Speech generated: {output_path.name} ({duration:.1f}s)")
            
            return TTSResult(
                success=True,
                audio_path=output_path,
                duration=duration
            )
            
        except Exception as e:
            return TTSResult(
                success=False,
                error=str(e)
            )
    
    def generate_batch(
        self,
        texts: List[str],
        output_dir: Path,
        prefix: str = "segment"
    ) -> List[TTSResult]:
        """
        Generate speech for multiple text segments
        
        Args:
            texts: List of texts to convert
            output_dir: Output directory
            prefix: Filename prefix
        
        Returns:
            List of TTSResult
        """
        results = []
        output_dir.mkdir(parents=True, exist_ok=True)
        
        for i, text in enumerate(texts):
            output_path = output_dir / f"{prefix}_{i:03d}.mp3"
            result = self.generate(text, output_path)
            results.append(result)
            
            if not result.success:
                print(f"⚠️  Failed at segment {i}: {result.error}")
        
        return results
    
    async def generate_batch_async(
        self,
        texts: List[str],
        output_dir: Path,
        prefix: str = "segment"
    ) -> List[TTSResult]:
        """Async batch generation"""
        output_dir.mkdir(parents=True, exist_ok=True)
        
        tasks = [
            self.generate_async(
                text,
                output_dir / f"{prefix}_{i:03d}.mp3"
            )
            for i, text in enumerate(texts)
        ]
        
        results = await asyncio.gather(*tasks)
        return list(results)
    
    def _get_audio_duration(self, audio_path: Path) -> float:
        """Get audio duration using ffprobe"""
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
            
            return 0.0
            
        except Exception:
            return 0.0
    
    def concatenate(
        self,
        audio_files: List[Path],
        output_path: Path
    ) -> TTSResult:
        """
        Concatenate multiple audio files
        
        Args:
            audio_files: List of audio file paths
            output_path: Output file path
        
        Returns:
            TTSResult with concatenated audio
        """
        try:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Create file list for ffmpeg
            list_file = output_path.parent / "concat_list.txt"
            
            with open(list_file, "w", encoding="utf-8") as f:
                for audio_file in audio_files:
                    f.write(f"file '{audio_file.absolute()}'\n")
            
            # Concatenate using ffmpeg
            cmd = [
                "ffmpeg",
                "-y",
                "-f", "concat",
                "-safe", "0",
                "-i", str(list_file),
                "-c", "copy",
                str(output_path)
            ]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=120
            )
            
            # Clean up list file
            list_file.unlink(missing_ok=True)
            
            if result.returncode != 0:
                return TTSResult(
                    success=False,
                    error=f"ffmpeg concat failed: {result.stderr}"
                )
            
            duration = self._get_audio_duration(output_path)
            
            return TTSResult(
                success=True,
                audio_path=output_path,
                duration=duration
            )
            
        except Exception as e:
            return TTSResult(
                success=False,
                error=str(e)
            )


async def main():
    """Test Edge-TTS"""
    tts = EdgeTTS(voice="zh-CN-XiaoxiaoNeural")
    
    # Test single generation
    result = tts.generate(
        "你好，这是一个测试。视频处理助手正在工作。",
        Path("./test_output.mp3")
    )
    
    print(f"Success: {result.success}")
    if result.success:
        print(f"Duration: {result.duration:.1f}s")
        print(f"Output: {result.audio_path}")


if __name__ == "__main__":
    asyncio.run(main())
