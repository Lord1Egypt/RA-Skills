"""
Video merger using FFmpeg - combines video clips with new audio
"""
import subprocess
import tempfile
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass


@dataclass
class MergeSegment:
    """A segment to merge"""
    video_path: Path
    start_time: float
    end_time: float
    audio_path: Optional[Path] = None


@dataclass
class MergeResult:
    """Result of merge operation"""
    success: bool
    output_path: Optional[Path] = None
    duration: float = 0.0
    error: Optional[str] = None


class VideoMerger:
    """Merge video segments with new audio using FFmpeg"""
    
    def __init__(
        self,
        video_codec: str = "libx264",
        audio_codec: str = "aac",
        audio_bitrate: str = "192k",
        preset: str = "medium",
        crf: int = 23
    ):
        """
        Initialize video merger
        
        Args:
            video_codec: Video codec (libx264, libx265, etc.)
            audio_codec: Audio codec (aac, mp3, etc.)
            audio_bitrate: Audio bitrate
            preset: Encoding preset (ultrafast to veryslow)
            crf: Quality (0-51, lower is better)
        """
        self.video_codec = video_codec
        self.audio_codec = audio_codec
        self.audio_bitrate = audio_bitrate
        self.preset = preset
        self.crf = crf
    
    def merge(
        self,
        video_path: Path,
        audio_path: Path,
        output_path: Path,
        start_time: float = 0,
        end_time: Optional[float] = None
    ) -> MergeResult:
        """
        Merge video with new audio track
        
        Args:
            video_path: Source video file
            audio_path: New audio file
            output_path: Output file path
            start_time: Start time in video
            end_time: End time in video (optional)
        
        Returns:
            MergeResult with output path
        """
        try:
            print(f"🎬 Merging video and audio...")
            
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Build FFmpeg command
            cmd = [
                "ffmpeg",
                "-y",  # Overwrite output
                "-ss", str(start_time),  # Start time
                "-i", str(video_path),   # Input video
                "-i", str(audio_path),   # Input audio
            ]
            
            # Add end time if specified
            if end_time:
                duration = end_time - start_time
                cmd.extend(["-t", str(duration)])
            
            # Output settings
            cmd.extend([
                "-c:v", self.video_codec,
                "-c:a", self.audio_codec,
                "-b:a", self.audio_bitrate,
                "-preset", self.preset,
                "-crf", str(self.crf),
                "-map", "0:v",  # Video from first input
                "-map", "1:a",  # Audio from second input
                "-shortest",    # End when shortest stream ends
                str(output_path)
            ])
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=600
            )
            
            if result.returncode != 0:
                return MergeResult(
                    success=False,
                    error=f"FFmpeg failed: {result.stderr}"
                )
            
            if not output_path.exists():
                return MergeResult(
                    success=False,
                    error="Output file not created"
                )
            
            duration = self._get_duration(output_path)
            
            print(f"✅ Merge complete: {output_path.name} ({duration:.1f}s)")
            
            return MergeResult(
                success=True,
                output_path=output_path,
                duration=duration
            )
            
        except subprocess.TimeoutExpired:
            return MergeResult(
                success=False,
                error="Merge operation timed out"
            )
        except Exception as e:
            return MergeResult(
                success=False,
                error=str(e)
            )
    
    def merge_segments(
        self,
        video_path: Path,
        segments: List[MergeSegment],
        output_path: Path
    ) -> MergeResult:
        """
        Merge multiple segments from video with corresponding audio
        
        Args:
            video_path: Source video file
            segments: List of segments with timing and audio
            output_path: Output file path
        
        Returns:
            MergeResult
        """
        try:
            print(f"🎬 Merging {len(segments)} segments...")
            
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            with tempfile.TemporaryDirectory() as temp_dir:
                temp_path = Path(temp_dir)
                
                # Step 1: Extract and process each segment
                processed_segments = []
                
                for i, seg in enumerate(segments):
                    seg_output = temp_path / f"seg_{i:03d}.mp4"
                    
                    result = self.merge(
                        video_path=video_path,
                        audio_path=seg.audio_path,
                        output_path=seg_output,
                        start_time=seg.start_time,
                        end_time=seg.end_time
                    )
                    
                    if not result.success:
                        return MergeResult(
                            success=False,
                            error=f"Segment {i} failed: {result.error}"
                        )
                    
                    processed_segments.append(seg_output)
                
                # Step 2: Concatenate all segments
                return self.concatenate(processed_segments, output_path)
            
        except Exception as e:
            return MergeResult(
                success=False,
                error=str(e)
            )
    
    def concatenate(
        self,
        video_files: List[Path],
        output_path: Path
    ) -> MergeResult:
        """
        Concatenate multiple video files
        
        Args:
            video_files: List of video file paths
            output_path: Output file path
        
        Returns:
            MergeResult
        """
        try:
            print(f"🔗 Concatenating {len(video_files)} videos...")
            
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Create concat list file
            list_file = output_path.parent / "concat_list.txt"
            
            with open(list_file, "w", encoding="utf-8") as f:
                for video_file in video_files:
                    f.write(f"file '{video_file.absolute()}'\n")
            
            # Concatenate using FFmpeg
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
                timeout=300
            )
            
            # Clean up
            list_file.unlink(missing_ok=True)
            
            if result.returncode != 0:
                return MergeResult(
                    success=False,
                    error=f"FFmpeg concat failed: {result.stderr}"
                )
            
            if not output_path.exists():
                return MergeResult(
                    success=False,
                    error="Output file not created"
                )
            
            duration = self._get_duration(output_path)
            
            print(f"✅ Concatenation complete: {output_path.name} ({duration:.1f}s)")
            
            return MergeResult(
                success=True,
                output_path=output_path,
                duration=duration
            )
            
        except Exception as e:
            return MergeResult(
                success=False,
                error=str(e)
            )
    
    def add_audio_to_video(
        self,
        video_path: Path,
        audio_path: Path,
        output_path: Path,
        volume: float = 1.0
    ) -> MergeResult:
        """
        Add/replace audio track in video
        
        Args:
            video_path: Input video
            audio_path: New audio
            output_path: Output video
            volume: Audio volume multiplier
        
        Returns:
            MergeResult
        """
        try:
            print(f"🎵 Adding audio to video...")
            
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            cmd = [
                "ffmpeg",
                "-y",
                "-i", str(video_path),
                "-i", str(audio_path),
                "-c:v", "copy",
                "-c:a", self.audio_codec,
                "-b:a", self.audio_bitrate,
                "-map", "0:v",
                "-map", "1:a",
                "-af", f"volume={volume}",
                "-shortest",
                str(output_path)
            ]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=600
            )
            
            if result.returncode != 0:
                return MergeResult(
                    success=False,
                    error=f"FFmpeg failed: {result.stderr}"
                )
            
            duration = self._get_duration(output_path)
            
            return MergeResult(
                success=True,
                output_path=output_path,
                duration=duration
            )
            
        except Exception as e:
            return MergeResult(
                success=False,
                error=str(e)
            )
    
    def _get_duration(self, video_path: Path) -> float:
        """Get video duration using ffprobe"""
        try:
            cmd = [
                "ffprobe",
                "-v", "quiet",
                "-show_entries", "format=duration",
                "-of", "default=noprint_wrappers=1:nokey=1",
                str(video_path)
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
    
    def extract_audio(
        self,
        video_path: Path,
        output_path: Path
    ) -> MergeResult:
        """Extract audio from video"""
        try:
            print(f"🎵 Extracting audio...")
            
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            cmd = [
                "ffmpeg",
                "-y",
                "-i", str(video_path),
                "-vn",  # No video
                "-acodec", self.audio_codec,
                "-b:a", self.audio_bitrate,
                str(output_path)
            ]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300
            )
            
            if result.returncode != 0:
                return MergeResult(
                    success=False,
                    error=f"FFmpeg failed: {result.stderr}"
                )
            
            duration = self._get_duration(output_path)
            
            return MergeResult(
                success=True,
                output_path=output_path,
                duration=duration
            )
            
        except Exception as e:
            return MergeResult(
                success=False,
                error=str(e)
            )


if __name__ == "__main__":
    import sys
    
    # Test merge
    if len(sys.argv) >= 4:
        merger = VideoMerger()
        result = merger.merge(
            video_path=Path(sys.argv[1]),
            audio_path=Path(sys.argv[2]),
            output_path=Path(sys.argv[3])
        )
        print(f"Success: {result.success}")
        if result.success:
            print(f"Output: {result.output_path}")
            print(f"Duration: {result.duration:.1f}s")
        else:
            print(f"Error: {result.error}")
