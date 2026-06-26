"""
YouTube video downloader using yt-dlp
"""
import os
import subprocess
import sys
from pathlib import Path
from typing import Optional, Dict, Any
from dataclasses import dataclass


@dataclass
class DownloadResult:
    """Result of a download operation"""
    success: bool
    video_path: Optional[Path] = None
    audio_path: Optional[Path] = None
    title: Optional[str] = None
    duration: Optional[int] = None  # Duration in seconds
    error: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class VideoDownloader:
    """Download videos from YouTube and other platforms"""
    
    def __init__(self, output_dir: Path, quality: str = "best", proxy: Optional[str] = None):
        self.output_dir = output_dir
        self.quality = quality
        self.proxy = proxy or os.getenv("HTTP_PROXY") or os.getenv("HTTPS_PROXY")
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def download(self, url: str, download_audio: bool = True) -> DownloadResult:
        """
        Download a video from URL
        
        Args:
            url: Video URL
            download_audio: Also download separate audio track
        
        Returns:
            DownloadResult with paths and metadata
        """
        try:
            # First, get video info
            info = self._get_info(url)
            
            if not info:
                return DownloadResult(
                    success=False,
                    error="Failed to get video information"
                )
            
            video_id = info.get("id", "unknown")
            title = self._sanitize_filename(info.get("title", "video"))
            
            # Download video
            video_path = self.output_dir / f"{video_id}.mp4"
            
            cmd = [
                "yt-dlp",
                "-f", self._get_format(),
                "-o", str(self.output_dir / f"{video_id}.%(ext)s"),
                "--no-playlist",
                "--write-info-json",
            ]
            if self.proxy:
                cmd.extend(["--proxy", self.proxy])
            cmd.append(url)
            
            print(f"📥 Downloading video: {title}")
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=600  # 10 minute timeout
            )
            
            if result.returncode != 0:
                return DownloadResult(
                    success=False,
                    error=f"Download failed: {result.stderr}"
                )
            
            # Find the downloaded file
            video_path = self._find_downloaded_file(video_id)
            
            if not video_path:
                return DownloadResult(
                    success=False,
                    error="Video file not found after download"
                )
            
            # Download audio separately if requested
            audio_path = None
            if download_audio:
                audio_path = self._download_audio(url, video_id)
            
            print(f"✅ Download complete: {video_path}")
            
            return DownloadResult(
                success=True,
                video_path=video_path,
                audio_path=audio_path,
                title=title,
                duration=info.get("duration"),
                metadata=info
            )
            
        except subprocess.TimeoutExpired:
            return DownloadResult(
                success=False,
                error="Download timed out"
            )
        except Exception as e:
            return DownloadResult(
                success=False,
                error=str(e)
            )
    
    def _get_info(self, url: str) -> Optional[Dict[str, Any]]:
        """Get video information without downloading"""
        try:
            cmd = [
                "yt-dlp",
                "-J",  # Dump JSON
                "--no-playlist",
            ]
            if self.proxy:
                cmd.extend(["--proxy", self.proxy])
            cmd.append(url)
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                import json
                return json.loads(result.stdout)
            
            return None
            
        except Exception as e:
            print(f"Error getting video info: {e}")
            return None
    
    def _get_format(self) -> str:
        """Get format string for yt-dlp"""
        quality_map = {
            "best": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
            "worst": "worstvideo[ext=mp4]+worstaudio[ext=m4a]/worst[ext=mp4]/worst",
            "1080p": "bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/best[height<=1080][ext=mp4]/best",
            "720p": "bestvideo[height<=720][ext=mp4]+bestaudio[ext=m4a]/best[height<=720][ext=mp4]/best",
            "480p": "bestvideo[height<=480][ext=mp4]+bestaudio[ext=m4a]/best[height<=480][ext=mp4]/best",
        }
        return quality_map.get(self.quality, quality_map["best"])
    
    def _download_audio(self, url: str, video_id: str) -> Optional[Path]:
        """Download audio track separately"""
        try:
            audio_path = self.output_dir / f"{video_id}.m4a"
            
            cmd = [
                "yt-dlp",
                "-x",  # Extract audio
                "--audio-format", "m4a",
                "-o", str(self.output_dir / f"{video_id}.%(ext)s"),
                "--no-playlist",
            ]
            if self.proxy:
                cmd.extend(["--proxy", self.proxy])
            cmd.append(url)
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300
            )
            
            if result.returncode == 0 and audio_path.exists():
                return audio_path
            
            return None
            
        except Exception as e:
            print(f"Error downloading audio: {e}")
            return None
    
    def _find_downloaded_file(self, video_id: str) -> Optional[Path]:
        """Find the downloaded video file"""
        extensions = [".mp4", ".mkv", ".webm", ".flv"]
        
        for ext in extensions:
            path = self.output_dir / f"{video_id}{ext}"
            if path.exists():
                return path
        
        # Try to find any video file with this ID
        for file in self.output_dir.glob(f"{video_id}.*"):
            if file.suffix.lower() in extensions:
                return file
        
        return None
    
    def _sanitize_filename(self, filename: str) -> str:
        """Remove invalid characters from filename"""
        import re
        # Remove or replace invalid characters
        filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
        # Remove control characters
        filename = re.sub(r'[\0-\31]', '', filename)
        # Limit length
        return filename[:200]
    
    def cleanup(self, keep_video: bool = False):
        """Clean up temporary files"""
        if not keep_video:
            for file in self.output_dir.glob("*.mp4"):
                file.unlink()
            for file in self.output_dir.glob("*.m4a"):
                file.unlink()
            for file in self.output_dir.glob("*.info.json"):
                file.unlink()


if __name__ == "__main__":
    # Test download
    import sys
    if len(sys.argv) > 1:
        downloader = VideoDownloader(Path("./test_downloads"))
        result = downloader.download(sys.argv[1])
        print(f"Success: {result.success}")
        if result.success:
            print(f"Video: {result.video_path}")
            print(f"Audio: {result.audio_path}")
            print(f"Title: {result.title}")
            print(f"Duration: {result.duration}s")
        else:
            print(f"Error: {result.error}")
