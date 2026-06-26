"""SubtitleConverter - generates SRT and VTT subtitle files."""
from typing import List


class SubtitleConverter:
    """Converts subtitle segments to SRT and VTT formats."""

    def to_srt(self, segments: List[dict], output_path: str) -> None:
        """Generate SRT format subtitle file."""
        with open(output_path, 'w', encoding='utf-8') as f:
            for i, seg in enumerate(segments, 1):
                start_time = self._format_srt_time(seg["start"])
                end_time = self._format_srt_time(seg["end"])

                f.write(f"{i}\n")
                f.write(f"{start_time} --> {end_time}\n")
                f.write(f"{seg['text'].strip()}\n\n")

    def to_vtt(self, segments: List[dict], output_path: str) -> None:
        """Generate WebVTT format subtitle file."""
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("WEBVTT\n\n")

            for i, seg in enumerate(segments, 1):
                start_time = self._format_vtt_time(seg["start"])
                end_time = self._format_vtt_time(seg["end"])

                f.write(f"{i}\n")
                f.write(f"{start_time} --> {end_time}\n")
                f.write(f"{seg['text'].strip()}\n\n")

    def _parse_time_components(self, seconds: float) -> tuple:
        """Parse time into hours, minutes, seconds, milliseconds."""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        millis = int((seconds % 1) * 1000)
        return hours, minutes, secs, millis

    def _format_srt_time(self, seconds: float) -> str:
        """Format time for SRT: HH:MM:SS,mmm."""
        hours, minutes, secs, millis = self._parse_time_components(seconds)
        return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"

    def _format_vtt_time(self, seconds: float) -> str:
        """Format time for WebVTT: HH:MM:SS.mmm."""
        hours, minutes, secs, millis = self._parse_time_components(seconds)
        return f"{hours:02d}:{minutes:02d}:{secs:02d}.{millis:03d}"
