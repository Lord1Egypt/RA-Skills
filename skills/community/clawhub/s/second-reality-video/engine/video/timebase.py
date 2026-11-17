"""Timebase: tick ↔ frame mapping with HLC authority."""

from typing import Dict, Optional


class Timebase:
    """Manages the mapping between world ticks and video frames.
    
    World runs at TPS (ticks per second), video at FPS (frames per second).
    frames_per_tick = FPS / TPS
    
    For default config: TPS=10, FPS=30 → frames_per_tick=3
    90 seconds = 900 ticks = 2700 frames
    """
    
    def __init__(self, tps: int = 10, fps: int = 30):
        self.tps = tps
        self.fps = fps
        self.frames_per_tick = fps // tps
        
        if fps % tps != 0:
            raise ValueError(
                f"FPS ({fps}) must be evenly divisible by TPS ({tps})"
            )
    
    def tick_to_frame(self, tick: int, sub: int = 0) -> int:
        """Convert tick number to frame index.
        
        Args:
            tick: World tick number
            sub: Sub-frame within tick [0, frames_per_tick)
            
        Returns:
            Frame index
        """
        if sub < 0 or sub >= self.frames_per_tick:
            raise ValueError(f"sub must be in [0, {self.frames_per_tick})")
        return tick * self.frames_per_tick + sub
    
    def frame_to_tick(self, frame: int) -> tuple:
        """Convert frame index to (tick, sub).
        
        Args:
            frame: Frame index
            
        Returns:
            Tuple of (tick, sub)
        """
        tick = frame // self.frames_per_tick
        sub = frame % self.frames_per_tick
        return tick, sub
    
    def total_frames(self, duration_seconds: float) -> int:
        """Calculate total frames for a given duration.
        
        Args:
            duration_seconds: Duration in seconds
            
        Returns:
            Total frame count
        """
        return int(duration_seconds * self.fps)
    
    def total_ticks(self, duration_seconds: float) -> int:
        """Calculate total ticks for a given duration.
        
        Args:
            duration_seconds: Duration in seconds
            
        Returns:
            Total tick count
        """
        return int(duration_seconds * self.tps)
    
    def to_dict(self) -> Dict:
        """Serialize timebase config."""
        return {
            "tps": self.tps,
            "fps": self.fps,
            "frames_per_tick": self.frames_per_tick,
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> "Timebase":
        """Deserialize timebase config."""
        return cls(tps=data["tps"], fps=data["fps"])
