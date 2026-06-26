# Video processing module - adapted from public source
import os
from typing import List, Tuple, Optional
import ffmpeg
import numpy as np
from dataclasses import dataclass

@dataclass
class VideoInfo:
    width: int
    height: int
    duration_seconds: float
    total_frames: int
    fps: float
    codec: str

@dataclass
class ExtractedFrame:
    frame_number: int
    timestamp_seconds: float
    width: int
    height: int
    image_bytes: bytes = None
    file_path: str = None

class VideoProcessor:
    def __init__(self, temp_dir: str = "/tmp/video_frames"):
        self.temp_dir = temp_dir
        os.makedirs(temp_dir, exist_ok=True)
    
    def get_video_info(self, video_path: str) -> VideoInfo:
        try:
            probe = ffmpeg.probe(video_path)
            video_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
            
            if not video_stream:
                raise ValueError("No video stream found in the file")
            
            fps_num, fps_den = map(int, video_stream['r_frame_rate'].split('/'))
            fps = fps_num / fps_den if fps_den != 0 else 0
            
            return VideoInfo(
                width=int(video_stream['width']),
                height=int(video_stream['height']),
                duration_seconds=float(video_stream['duration']),
                total_frames=int(video_stream['nb_frames']),
                fps=fps,
                codec=video_stream['codec_name']
            )
        except ffmpeg.Error as e:
            raise RuntimeError(f"Failed to probe video: {e.stderr.decode()}") from e
    
    def extract_keyframes(self, video_path: str, interval_seconds: int = 10) -> List[ExtractedFrame]:
        """Extract keyframes at specified intervals"""
        video_info = self.get_video_info(video_path)
        frames = []
        
        # Calculate timestamps
        timestamps = []
        current_time = 0
        while current_time < video_info.duration_seconds:
            timestamps.append(current_time)
            current_time += interval_seconds
        
        for ts in timestamps:
            frame_bytes = self._extract_frame_at_time(video_path, ts)
            frame_number = int(ts * video_info.fps)
            
            frames.append(ExtractedFrame(
                frame_number=frame_number,
                timestamp_seconds=ts,
                width=video_info.width,
                height=video_info.height,
                image_bytes=frame_bytes
            ))
        
        return frames
    
    def _extract_frame_at_time(self, video_path: str, time_seconds: float, quality: int = 2) -> bytes:
        try:
            out, _ = (
                ffmpeg
                .input(video_path, ss=time_seconds)
                .output('pipe:', vframes=1, format='image2', vcodec='mjpeg', qv=quality)
                .run(capture_stdout=True, capture_stderr=True)
            )
            return out
        except ffmpeg.Error as e:
            raise RuntimeError(f"Failed to extract frame: {e.stderr.decode()}") from e
    
    def save_frame(self, frame: ExtractedFrame, output_path: str) -> None:
        """Save frame to file"""
        with open(output_path, 'wb') as f:
            f.write(frame.image_bytes)
        frame.file_path = output_path