"""TimingAligner - intelligent sentence splitting and timing alignment."""
import re
from typing import List


class TimingAligner:
    """Time axis aligner for subtitle segments."""

    PUNCTUATION_PATTERN = r'([。！？，.!?,,、])'

    def align_segments(
        self,
        segments: List[dict],
        max_duration: float = 10.0,
    ) -> List[dict]:
        """Intelligently split long sentences."""
        aligned = []

        for seg in segments:
            duration = seg["end"] - seg["start"]

            if duration <= max_duration:
                aligned.append(seg)
            else:
                sub_segments = self._split_long_segment(seg, max_duration)
                aligned.extend(sub_segments)

        return aligned

    def _split_long_segment(
        self,
        segment: dict,
        max_duration: float,
    ) -> List[dict]:
        """Split a long subtitle segment considering punctuation and speaking rate."""
        text = segment["text"]
        start = segment["start"]
        duration = segment["end"] - segment["start"]

        # Try splitting by punctuation first
        parts = self._split_by_punctuation(text)

        if len(parts) <= 1:
            # No punctuation found, split by character count
            parts = self._split_by_chars(text, 20)

        # Distribute time proportionally by character count
        segments = []
        total_chars = sum(len(p) for p in parts)

        current_time = start
        for part in parts:
            if total_chars == 0:
                part_duration = duration
            else:
                part_duration = (len(part) / total_chars) * duration

            segments.append({
                "start": current_time,
                "end": current_time + part_duration,
                "text": part.strip(),
            })
            current_time += part_duration

        return segments

    def _split_by_punctuation(self, text: str) -> List[str]:
        """Split text by punctuation marks."""
        parts = re.split(self.PUNCTUATION_PATTERN, text)

        result = []
        for i in range(0, len(parts) - 1, 2):
            if parts[i].strip():
                tail = parts[i + 1] if i + 1 < len(parts) else ""
                result.append(parts[i] + tail)

        if not result:
            result = [text]

        return [p.strip() for p in result if p.strip()]

    def _split_by_chars(self, text: str, max_chars: int) -> List[str]:
        """Split text by character count."""
        return [text[i:i + max_chars] for i in range(0, len(text), max_chars)]
