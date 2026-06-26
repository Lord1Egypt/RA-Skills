#!/usr/bin/env python3
"""
Video Remix Agent - OpenClaw Skill Script

This script is called by OpenClaw when the video-remix skill is triggered.
It processes YouTube videos through the full pipeline:
1. Download
2. Transcribe
3. Analyze
4. Generate script
5. TTS voiceover
6. Merge final video

Usage:
    python video_remix.py <youtube_url> [options]

The script reads configuration from environment variables and command-line arguments.
Results are printed to stdout for OpenClaw to capture and return to the user.
"""

import sys
import os
import asyncio
import argparse
from pathlib import Path
from typing import Optional, Dict, Any
import json

# Add the script's directory and modules to path for imports
SCRIPT_DIR = Path(__file__).parent
SKILL_DIR = SCRIPT_DIR.parent
MODULES_DIR = SKILL_DIR / "modules"
sys.path.insert(0, str(SKILL_DIR))
sys.path.insert(0, str(MODULES_DIR))

# Import modules
from modules.downloader import VideoDownloader, DownloadResult
from modules.transcriber import Transcriber, TranscriptionResult
from modules.analyzer import ContentAnalyzer, AnalysisResult
from modules.script_gen import ScriptGenerator, ScriptResult, ScriptStyle
from modules.tts import EdgeTTS, TTSResult
from modules.merger import VideoMerger, MergeResult, MergeSegment


class OpenClawVideoRemix:
    """Video Remix Agent for OpenClaw"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the agent
        
        Args:
            config: Configuration dictionary from OpenClaw
        """
        self.config = config or {}
        
        # Load configuration from environment
        self.output_dir = Path(os.getenv("VR_OUTPUT_DIR", "./output"))
        self.temp_dir = Path(os.getenv("VR_TEMP_DIR", "./temp"))
        self.video_quality = os.getenv("VR_VIDEO_QUALITY", "best")
        self.whisper_model = os.getenv("VR_WHISPER_MODEL", "base")
        self.whisper_language = os.getenv("VR_WHISPER_LANGUAGE", "zh")
        self.tts_voice = os.getenv("VR_TTS_VOICE", "xiaoxiao")
        self.llm_model = os.getenv("VR_LLM_MODEL", "gpt-4o-mini")
        self.llm_api_key = os.getenv("OPENAI_API_KEY")
        self.llm_base_url = os.getenv("VR_LLM_BASE_URL")
        
        # Create directories
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.temp_dir.mkdir(parents=True, exist_ok=True)
        
        # State
        self._video_path: Optional[Path] = None
        self._transcription: Optional[TranscriptionResult] = None
        self._analysis: Optional[AnalysisResult] = None
        self._script: Optional[ScriptResult] = None
        self._tts_results: list = []
        self._final_output: Optional[Path] = None
    
    async def process(
        self,
        input_source: str,
        output_path: Optional[Path] = None,
        voice: Optional[str] = None,
        style: str = "professional",
        keep_intermediate: bool = False,
        step: str = "all"
    ) -> Dict[str, Any]:
        """
        Process a video through the pipeline
        
        Args:
            input_source: YouTube URL or video file path
            output_path: Output file path
            voice: TTS voice name
            style: Script style
            keep_intermediate: Keep intermediate files
            step: Pipeline step to execute
        
        Returns:
            Dictionary with results and status
        """
        voice = voice or self.tts_voice
        output_path = output_path or (self.output_dir / "final.mp4")
        
        result = {
            "success": False,
            "steps_completed": [],
            "output_file": None,
            "transcription": None,
            "analysis": None,
            "script": None,
            "error": None
        }
        
        try:
            # Step 1: Download
            if step in ["download", "all"]:
                print(f"\n📥 Step 1: Downloading from {input_source}...")
                
                if input_source.startswith(("http://", "https://")):
                    download_result = await self._download(input_source)
                    
                    if not download_result or not download_result.get("success"):
                        result["error"] = "Download failed"
                        return result
                    
                    self._video_path = Path(download_result["video_path"])
                    result["steps_completed"].append("download")
                    result["video_info"] = {
                        "title": download_result.get("title"),
                        "duration": download_result.get("duration"),
                        "path": str(self._video_path)
                    }
                else:
                    self._video_path = Path(input_source)
                    result["steps_completed"].append("download")
            
            # Step 2: Transcribe
            if step in ["transcribe", "all"]:
                print(f"\n🎤 Step 2: Transcribing...")
                transcription = await self._transcribe(self._video_path)
                
                if not transcription or not transcription.get("success"):
                    result["error"] = "Transcription failed"
                    return result
                
                self._transcription = transcription
                result["steps_completed"].append("transcribe")
                result["transcription"] = {
                    "full_text": transcription.get("full_text"),
                    "segments_count": len(transcription.get("segments", [])),
                    "language": transcription.get("language"),
                    "duration": transcription.get("duration")
                }
            
            # Step 3: Analyze
            if step in ["analyze", "all"]:
                print(f"\n🔍 Step 3: Analyzing content...")
                analysis = await self._analyze()
                
                if not analysis or not analysis.get("success"):
                    result["error"] = "Analysis failed"
                    return result
                
                self._analysis = analysis
                result["steps_completed"].append("analyze")
                result["analysis"] = {
                    "segments_count": len(analysis.get("segments", [])),
                    "topics": analysis.get("topics"),
                    "segments": analysis.get("segments")[:5]  # Top 5 segments
                }
            
            # Step 4: Generate Script
            if step in ["script", "all"]:
                print(f"\n✍️  Step 4: Generating script with style '{style}'...")
                script = await self._generate_script(style=style)
                
                if not script or not script.get("success"):
                    result["error"] = "Script generation failed"
                    return result
                
                self._script = script
                result["steps_completed"].append("script")
                result["script"] = {
                    "segments_count": len(script.get("segments", [])),
                    "total_duration": script.get("total_duration"),
                    "full_script": script.get("full_script")
                }
            
            # Step 5: TTS
            if step in ["tts", "all"]:
                print(f"\n🔊 Step 5: Generating voiceover with voice '{voice}'...")
                tts_results = await self._generate_tts(voice=voice)
                
                if not tts_results:
                    result["error"] = "TTS generation failed"
                    return result
                
                self._tts_results = tts_results
                result["steps_completed"].append("tts")
                result["tts"] = {
                    "segments_count": len(tts_results),
                    "audio_files": [str(r["audio_path"]) for r in tts_results if r.get("success")]
                }
            
            # Step 6: Merge
            if step in ["merge", "all"]:
                print(f"\n🎬 Step 6: Merging final video...")
                final_output = await self._merge(output_path)
                
                if not final_output or not final_output.get("success"):
                    result["error"] = "Merge failed"
                    return result
                
                self._final_output = Path(final_output["output_path"])
                result["steps_completed"].append("merge")
                result["output_file"] = str(self._final_output)
                result["duration"] = final_output.get("duration")
            
            result["success"] = True
            
            # Cleanup
            if not keep_intermediate and step == "all":
                self._cleanup()
            
            return result
            
        except Exception as e:
            result["error"] = str(e)
            import traceback
            result["traceback"] = traceback.format_exc()
            return result
    
    async def _download(self, url: str) -> Optional[Dict[str, Any]]:
        """Download video from URL"""
        try:
            # Get proxy from env or args
            proxy = os.getenv("HTTP_PROXY") or os.getenv("HTTPS_PROXY")
            downloader = VideoDownloader(
                output_dir=self.temp_dir,
                quality=self.video_quality,
                proxy=proxy
            )
            
            # Run in executor to avoid blocking
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(
                None,
                lambda: downloader.download(url)
            )
            
            if result.success:
                return {
                    "success": True,
                    "video_path": str(result.video_path),
                    "title": result.title,
                    "duration": result.duration,
                    "metadata": result.metadata
                }
            
            return {"success": False, "error": result.error}
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def _transcribe(self, audio_path: Path) -> Optional[Dict[str, Any]]:
        """Transcribe audio/video"""
        try:
            transcriber = Transcriber(
                model=self.whisper_model,
                language=self.whisper_language
            )
            
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(
                None,
                lambda: transcriber.transcribe(audio_path, self.temp_dir)
            )
            
            if result.success:
                # Save transcription
                trans_path = self.temp_dir / "transcription.json"
                transcriber.save_transcription(result, trans_path)
                
                return {
                    "success": True,
                    "segments": [
                        {
                            "start": seg.start,
                            "end": seg.end,
                            "text": seg.text,
                            "confidence": seg.confidence
                        }
                        for seg in result.segments
                    ],
                    "full_text": result.full_text,
                    "language": result.language,
                    "duration": result.duration
                }
            
            return {"success": False, "error": result.error}
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def _analyze(self) -> Optional[Dict[str, Any]]:
        """Analyze transcribed content"""
        try:
            analyzer = ContentAnalyzer(
                min_length=5,
                max_length=60
            )
            
            trans_path = self.temp_dir / "transcription.json"
            
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(
                None,
                lambda: analyzer.analyze(trans_path)
            )
            
            if result.success:
                # Filter to top segments
                filtered = analyzer.filter_segments(
                    result.segments,
                    min_importance=0.5,
                    max_segments=10
                )
                result.segments = filtered
                
                # Save analysis
                analysis_path = self.temp_dir / "analysis.json"
                analyzer.save_analysis(result, analysis_path)
                
                return {
                    "success": True,
                    "segments": [
                        {
                            "start": seg.start,
                            "end": seg.end,
                            "text": seg.text,
                            "segment_type": seg.segment_type.value,
                            "importance": seg.importance,
                            "keywords": seg.keywords,
                            "summary": seg.summary
                        }
                        for seg in result.segments
                    ],
                    "topics": result.topics,
                    "total_duration": result.total_duration
                }
            
            return {"success": False, "error": result.error}
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def _generate_script(self, style: str = "professional") -> Optional[Dict[str, Any]]:
        """Generate voiceover script"""
        try:
            style_map = {
                "professional": ScriptStyle.PROFESSIONAL,
                "casual": ScriptStyle.CASUAL,
                "enthusiastic": ScriptStyle.ENTHUSIASTIC,
                "calm": ScriptStyle.CALM,
                "humorous": ScriptStyle.HUMOROUS,
            }
            
            generator = ScriptGenerator(
                provider="openai",
                model=self.llm_model,
                api_key=self.llm_api_key,
                base_url=self.llm_base_url,
                style=style_map.get(style, ScriptStyle.PROFESSIONAL)
            )
            
            analysis_path = self.temp_dir / "analysis.json"
            
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(
                None,
                lambda: generator.generate(analysis_path)
            )
            
            if result.success:
                # Save script
                script_path = self.temp_dir / "script.txt"
                generator.save_script(result, script_path)
                
                return {
                    "success": True,
                    "segments": [
                        {
                            "original_start": seg.original_start,
                            "original_end": seg.original_end,
                            "original_text": seg.original_text,
                            "script_text": seg.script_text,
                            "estimated_duration": seg.estimated_duration
                        }
                        for seg in result.segments
                    ],
                    "full_script": result.full_script,
                    "total_duration": result.total_duration
                }
            
            return {"success": False, "error": result.error}
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def _generate_tts(self, voice: str = "xiaoxiao") -> list:
        """Generate TTS for all script segments"""
        if not self._script:
            return []
        
        # Map voice name
        voice_map = EdgeTTS.list_voices("zh")
        voice_id = voice_map.get(voice, f"zh-CN-{voice.capitalize()}Neural")
        
        tts = EdgeTTS(
            voice=voice_id,
            rate="+0%",
            volume="+0%",
            pitch="+0Hz"
        )
        
        tts_dir = self.temp_dir / "tts"
        tts_dir.mkdir(parents=True, exist_ok=True)
        
        results = []
        loop = asyncio.get_event_loop()
        
        for i, segment in enumerate(self._script.get("segments", [])):
            output_path = tts_dir / f"segment_{i:03d}.mp3"
            
            result = await loop.run_in_executor(
                None,
                lambda s=segment, p=output_path: tts.generate(s["script_text"], p)
            )
            
            if result.success:
                results.append({
                    "success": True,
                    "audio_path": result.audio_path,
                    "duration": result.duration
                })
        
        return results
    
    async def _merge(self, output_path: Path) -> Optional[Dict[str, Any]]:
        """Merge video segments with TTS audio"""
        if not self._video_path or not self._script:
            return None
        
        merger = VideoMerger(
            video_codec="libx264",
            audio_codec="aac",
            audio_bitrate="192k",
            preset="medium"
        )
        
        merge_segments = []
        for i, segment in enumerate(self._script.get("segments", [])):
            if i < len(self._tts_results):
                merge_segments.append(MergeSegment(
                    video_path=self._video_path,
                    start_time=segment["original_start"],
                    end_time=segment["original_end"],
                    audio_path=self._tts_results[i]["audio_path"]
                ))
        
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(
            None,
            lambda: merger.merge_segments(
                self._video_path,
                merge_segments,
                output_path
            )
        )
        
        if result.success:
            return {
                "success": True,
                "output_path": str(result.output_path),
                "duration": result.duration
            }
        
        return {"success": False, "error": result.error}
    
    def _cleanup(self):
        """Clean up intermediate files"""
        import shutil
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)
            print("🧹 Cleaned up temporary files")


def create_parser() -> argparse.ArgumentParser:
    """Create argument parser"""
    parser = argparse.ArgumentParser(
        prog="video_remix",
        description="🎬 Video Remix Agent - Process YouTube videos with AI voiceover",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument("input", nargs="?", help="YouTube URL or video file path")
    parser.add_argument("-o", "--output", type=str, default="./output/final.mp4", help="Output file path")
    parser.add_argument("--voice", type=str, default=None, help="TTS voice name")
    parser.add_argument("--style", type=str, default="professional", 
                       choices=["professional", "casual", "enthusiastic", "calm", "humorous"],
                       help="Voiceover style")
    parser.add_argument("-q", "--quality", type=str, default="best",
                       choices=["best", "worst", "1080p", "720p", "480p"],
                       help="Video quality")
    parser.add_argument("--whisper-model", type=str, default="base",
                       choices=["tiny", "base", "small", "medium", "large"],
                       help="Whisper model")
    parser.add_argument("--step", type=str, default="all",
                       choices=["download", "transcribe", "analyze", "script", "tts", "merge", "all"],
                       help="Pipeline step to execute")
    parser.add_argument("--keep-intermediate", action="store_true", help="Keep intermediate files")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")
    parser.add_argument("--list-voices", action="store_true", help="List available voices")
    parser.add_argument("--proxy", type=str, help="HTTP/HTTPS proxy (e.g., http://127.0.0.1:10808)")
    
    return parser


def list_voices():
    """List available TTS voices"""
    print("\n🎤 Available Chinese TTS Voices:")
    print("=" * 50)
    
    voices = EdgeTTS.list_voices("zh")
    for name, voice_id in voices.items():
        print(f"  {name:15} → {voice_id}")
    
    print("\nUse with: --voice <name>")
    print("Example: --voice yunxi")


async def main_async(args):
    """Main async entry point"""
    # Set environment variables from args
    if args.quality:
        os.environ["VR_VIDEO_QUALITY"] = args.quality
    if args.whisper_model:
        os.environ["VR_WHISPER_MODEL"] = args.whisper_model
    if args.proxy:
        os.environ["HTTP_PROXY"] = args.proxy
        os.environ["HTTPS_PROXY"] = args.proxy
    
    # Create agent
    agent = OpenClawVideoRemix()
    
    # Process video
    result = await agent.process(
        input_source=args.input,
        output_path=Path(args.output),
        voice=args.voice,
        style=args.style,
        keep_intermediate=args.keep_intermediate,
        step=args.step
    )
    
    # Output result as JSON for OpenClaw
    print("\n" + "=" * 50)
    print("📊 RESULT:")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    
    return 0 if result["success"] else 1


def main():
    """Main entry point"""
    parser = create_parser()
    args = parser.parse_args()
    
    # Handle list-voices
    if args.list_voices:
        list_voices()
        return 0
    
    # Run async
    return asyncio.run(main_async(args))


if __name__ == "__main__":
    sys.exit(main())
