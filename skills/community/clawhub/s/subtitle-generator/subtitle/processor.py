"""SubtitleProcessor - orchestrates the full subtitle generation pipeline."""
import sys
from pathlib import Path
from typing import Dict, Optional, Union

# Add whisper venv to sys.path
WHISPER_VENV_SITE = Path.home() / ".whisper-venv" / "lib" / "python3.12" / "site-packages"
if WHISPER_VENV_SITE.exists() and str(WHISPER_VENV_SITE) not in sys.path:
    sys.path.insert(0, str(WHISPER_VENV_SITE))


class SubtitleProcessor:
    """Orchestrates audio extraction, ASR, and subtitle generation."""

    DEFAULT_AUDIO_SAMPLE_RATE = 16000
    DEFAULT_AUDIO_CHANNELS = 1

    def __init__(self) -> None:
        self.engine = None
        self.last_segment_count = 0

    def _extract_audio(self, video_path: Union[str, Path], output_audio: str = "audio.wav") -> Path:
        """Extract audio from video using ffmpeg."""
        import ffmpeg

        print(f"正在提取音频: {Path(video_path).name}")
        (
            ffmpeg
            .input(str(video_path))
            .output(
                output_audio,
                acodec='pcm_s16le',
                ac=self.DEFAULT_AUDIO_CHANNELS,
                ar=str(self.DEFAULT_AUDIO_SAMPLE_RATE),
            )
            .overwrite_output()
            .run(capture_stdout=True, capture_stderr=True)
        )
        return Path(output_audio)

    def process(
        self,
        video_path: Union[str, Path],
        output_format: str = "srt",
        language: Optional[str] = None,
        max_duration: float = 10.0,
    ) -> Path:
        """Full subtitle generation pipeline.

        Returns:
            Path to the generated subtitle file.
        """
        from engines import create_engine
        from subtitle.timing import TimingAligner
        from subtitle.converter import SubtitleConverter

        video_path = Path(video_path)
        if not video_path.exists():
            raise FileNotFoundError(f"文件不存在: {video_path}")

        print(f"正在处理: {video_path.name}")
        print(f"引擎: auto-detect | 格式: {output_format.upper()}")

        # Step 1: Extract audio
        audio_path = self._extract_audio(video_path)

        try:
            # Step 2: ASR
            engine = create_engine()
            result = engine.transcribe(str(audio_path), language=language)
            segments = result["segments"]
            detected_lang = result.get("language", "unknown")

            print(f"识别语言: {detected_lang}")
            print(f"识别段数: {len(segments)}")

            # Step 3: Timing alignment
            print("正在优化时间轴...")
            aligner = TimingAligner()
            aligned_segments = aligner.align_segments(segments, max_duration=max_duration)
            self.last_segment_count = len(aligned_segments)

            # Step 4: Generate subtitle file
            output_path = video_path.with_suffix(f".{output_format}")
            converter = SubtitleConverter()

            if output_format.lower() == "srt":
                converter.to_srt(aligned_segments, str(output_path))
            elif output_format.lower() == "vtt":
                converter.to_vtt(aligned_segments, str(output_path))
            else:
                raise ValueError(f"不支持的格式: {output_format}")

            print(f"✓ 字幕已生成: {output_path.name}")
            print(f"✓ 共 {len(aligned_segments)} 条字幕")

            return output_path

        finally:
            # Cleanup temp audio
            audio_path.unlink(missing_ok=True)
