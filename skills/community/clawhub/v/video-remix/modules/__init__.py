"""
Video Remix Agent - Modules

This package provides modules for video processing:
- downloader: YouTube video download
- transcriber: Speech-to-text transcription
- analyzer: Content analysis and segment identification
- script_gen: LLM-based script generation
- tts: Text-to-speech using Edge-TTS
- merger: Video/audio merging with FFmpeg
"""

from .downloader import VideoDownloader, DownloadResult
from .transcriber import Transcriber, TranscriptionResult, TranscriptionSegment
from .analyzer import ContentAnalyzer, AnalysisResult, VideoSegment, SegmentType
from .script_gen import ScriptGenerator, ScriptResult, ScriptSegment, ScriptStyle
from .tts import EdgeTTS, TTSResult
from .merger import VideoMerger, MergeResult, MergeSegment

__all__ = [
    "VideoDownloader",
    "DownloadResult",
    "Transcriber",
    "TranscriptionResult",
    "TranscriptionSegment",
    "ContentAnalyzer",
    "AnalysisResult",
    "VideoSegment",
    "SegmentType",
    "ScriptGenerator",
    "ScriptResult",
    "ScriptSegment",
    "ScriptStyle",
    "EdgeTTS",
    "TTSResult",
    "VideoMerger",
    "MergeResult",
    "MergeSegment",
]
