"""
TikTok-style text overlay for videos.

Reuses the image overlay engine from tiktok_overlay.py and applies it
frame-by-frame using moviepy.

Usage:
    from tiktok_video_overlay import overlay_video_text, overlay_video_texts
    from tiktok_overlay import TextOverlay, TikTokStyle

    # Simple — static text on entire video
    overlay_video_text("input.mp4", "Hello TikTok!", "output.mp4",
        style=TikTokStyle.CLASSIC, font_size=52, stroke_width=5)

    # Multiple texts, each with optional time range
    from tiktok_video_overlay import VideoTextOverlay
    overlay_video_texts("input.mp4", [
        VideoTextOverlay("First text", t_start=0, t_end=3,
            style=TikTokStyle.CLASSIC, position="top", font_size=48, stroke_width=4),
        VideoTextOverlay("Second text", t_start=2, t_end=5,
            style=TikTokStyle.STRONG, position="center", font_size=56,
            text_color="#FF6B6B", stroke_width=5),
        VideoTextOverlay("Always visible", t_start=None, t_end=None,
            style=TikTokStyle.CLASSIC, position="bottom", font_size=40,
            bg_style="highlight"),
    ], "output.mp4")

    # With fade in/out
    overlay_video_texts("input.mp4", [
        VideoTextOverlay("Fade me", t_start=1, t_end=4,
            fade_in=0.5, fade_out=0.5,
            style=TikTokStyle.CLASSIC, font_size=48, stroke_width=4),
    ], "output.mp4")
"""

from dataclasses import dataclass
from typing import Optional, Union
from PIL import Image
import numpy as np

from tiktok_overlay import (
    TikTokStyle, TextOverlay, _draw_text_block,
)


@dataclass
class VideoTextOverlay:
    """A text overlay with optional time range for video."""
    text: str
    t_start: Optional[float] = None   # seconds, None = from beginning
    t_end: Optional[float] = None     # seconds, None = until end
    fade_in: float = 0.0              # fade in duration (seconds)
    fade_out: float = 0.0             # fade out duration (seconds)
    # All the same styling options as TextOverlay
    style: TikTokStyle = TikTokStyle.CLASSIC
    font_size: int = 48
    text_color: str = "#FFFFFF"
    bg_style: str = "highlight"
    bg_color: str = "#000000"
    bg_opacity: float = 0.6
    position: Union[str, tuple] = "center"
    alignment: str = "center"
    stroke_width: int = 0
    stroke_color: str = "#000000"
    padding: int = 8
    line_spacing: int = 6
    max_width_ratio: float = 0.85

    def to_text_overlay(self) -> TextOverlay:
        return TextOverlay(
            text=self.text, style=self.style, font_size=self.font_size,
            text_color=self.text_color, bg_style=self.bg_style,
            bg_color=self.bg_color, bg_opacity=self.bg_opacity,
            position=self.position, alignment=self.alignment,
            stroke_width=self.stroke_width, stroke_color=self.stroke_color,
            padding=self.padding, line_spacing=self.line_spacing,
            max_width_ratio=self.max_width_ratio,
        )

    def is_visible(self, t: float, duration: float) -> bool:
        start = self.t_start if self.t_start is not None else 0
        end = self.t_end if self.t_end is not None else duration
        return start <= t <= end

    def get_opacity(self, t: float, duration: float) -> float:
        """Returns 0.0-1.0 opacity considering fade in/out."""
        start = self.t_start if self.t_start is not None else 0
        end = self.t_end if self.t_end is not None else duration

        if t < start or t > end:
            return 0.0

        opacity = 1.0
        # Fade in
        if self.fade_in > 0 and t < start + self.fade_in:
            opacity = (t - start) / self.fade_in
        # Fade out
        if self.fade_out > 0 and t > end - self.fade_out:
            opacity = min(opacity, (end - t) / self.fade_out)

        return max(0.0, min(1.0, opacity))


def _render_frame(frame: np.ndarray, overlays: list[VideoTextOverlay],
                  t: float, duration: float) -> np.ndarray:
    """Apply visible text overlays to a single video frame."""
    img = Image.fromarray(frame)

    for vto in overlays:
        if not vto.is_visible(t, duration):
            continue

        opacity = vto.get_opacity(t, duration)
        text_overlay = vto.to_text_overlay()

        if opacity >= 1.0:
            # Full opacity — render directly
            img = _draw_text_block(img, text_overlay)
        else:
            # Partial opacity — render text layer separately and blend
            base = img.convert("RGBA")
            text_img = _draw_text_block(
                Image.new("RGBA", img.size, (0, 0, 0, 0)),
                text_overlay,
            )
            # Scale alpha channel by opacity
            r, g, b, a = text_img.split()
            a = a.point(lambda x: int(x * opacity))
            text_img = Image.merge("RGBA", (r, g, b, a))
            img = Image.alpha_composite(base, text_img)

    return np.array(img.convert("RGB"))


def overlay_video_text(
    input_path: str,
    text: str,
    output_path: str,
    style: TikTokStyle = TikTokStyle.CLASSIC,
    font_size: int = 48,
    text_color: str = "#FFFFFF",
    bg_style: str = "highlight",
    bg_color: str = "#000000",
    bg_opacity: float = 0.6,
    position: Union[str, tuple] = "center",
    alignment: str = "center",
    stroke_width: int = 0,
    stroke_color: str = "#000000",
    padding: int = 8,
    t_start: Optional[float] = None,
    t_end: Optional[float] = None,
    fade_in: float = 0.0,
    fade_out: float = 0.0,
    codec: str = "libx264",
    audio: bool = True,
) -> str:
    """Add a single TikTok-style text overlay to a video."""
    vto = VideoTextOverlay(
        text=text, t_start=t_start, t_end=t_end,
        fade_in=fade_in, fade_out=fade_out,
        style=style, font_size=font_size, text_color=text_color,
        bg_style=bg_style, bg_color=bg_color, bg_opacity=bg_opacity,
        position=position, alignment=alignment, stroke_width=stroke_width,
        stroke_color=stroke_color, padding=padding,
    )
    return overlay_video_texts(input_path, [vto], output_path,
                                codec=codec, audio=audio)


def overlay_video_texts(
    input_path: str,
    overlays: list[VideoTextOverlay],
    output_path: str,
    codec: str = "libx264",
    audio: bool = True,
) -> str:
    """Add multiple timed TikTok-style text overlays to a video."""
    from moviepy import VideoFileClip

    clip = VideoFileClip(input_path)
    duration = clip.duration

    def process_frame(get_frame, t):
        frame = get_frame(t)
        return _render_frame(frame, overlays, t, duration)

    result = clip.transform(process_frame)

    result.write_videofile(
        output_path,
        codec=codec,
        audio=audio,
        logger="bar",
    )

    clip.close()
    result.close()
    return output_path


# --- CLI usage ---
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 4:
        print("Usage: python tiktok_video_overlay.py <input_video> <text> <output_video> [style]")
        print(f"Styles: {', '.join(s.value for s in TikTokStyle)}")
        print("\nExamples:")
        print('  python tiktok_video_overlay.py input.mp4 "Hello!" output.mp4')
        print('  python tiktok_video_overlay.py input.mp4 "Bold!" output.mp4 strong')
        sys.exit(1)

    input_path = sys.argv[1]
    text = sys.argv[2]
    output_path = sys.argv[3]
    style = TikTokStyle(sys.argv[4]) if len(sys.argv) > 4 else TikTokStyle.CLASSIC

    overlay_video_text(input_path, text, output_path,
                        style=style, stroke_width=4, font_size=52)
    print(f"Saved to {output_path}")
