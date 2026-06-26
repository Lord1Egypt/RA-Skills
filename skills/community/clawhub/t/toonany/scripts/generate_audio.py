#!/usr/bin/env python3
"""Generate TTS audio and subtitles from script.

Features:
- Character-voice mapping from project.json
- Sentence-level subtitle generation (not word-level)
- Multi-provider TTS support
"""

import argparse
import json
import os
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from utils.api_client import TTSAPIClient
from utils.config_loader import ConfigLoader, ConfigError
from utils.logger import setup_logger


@dataclass
class Dialogue:
    character: str
    text: str
    emotion: Optional[str] = None


def parse_script(script_path: Path) -> dict[int, list[Dialogue]]:
    """Parse script and extract dialogues per segment.

    Returns:
        Dict mapping segment_num -> list of Dialogue.
    """
    content = script_path.read_text(encoding="utf-8")

    segment_pattern = r"## 片段(\d+)：(.*?)(?=\n## |\Z)"
    segments = re.findall(segment_pattern, content, re.DOTALL)

    dialogues_by_segment = {}

    for segment_num_str, segment_content in segments:
        segment_num = int(segment_num_str)
        dialogues = []

        lines = segment_content.split('\n')
        in_dialogue = False

        for line in lines:
            if '**【' in line and '】' in line:
                in_dialogue = '对白' in line or '台词' in line
                continue

            if '---' in line:
                in_dialogue = False
                continue

            if not in_dialogue:
                continue

            line = line.strip()
            if not line:
                continue

            if line.startswith('**') or line.startswith('###'):
                continue

            # Match: 角色名（表情）："台词"
            match = re.match(
                r"^\s*([^（\n\-]+?)[（(]([^)）]+)[)）][：:]\s*[\"\"''']?(.+?)[\"\"'']?\s*$",
                line
            )
            if match:
                character = match.group(1).strip()
                emotion = match.group(2).strip()
                text = match.group(3).strip()
                text = text.replace('"', '').replace("'", '')
                if text:
                    dialogues.append(Dialogue(character=character, text=text, emotion=emotion))
                continue

            # Match simpler: 角色："台词"
            match = re.match(r"^\s*([^【\n\-]+?)[：:]\s*[\"\"'']?(.+?)[\"\"'']?\s*$", line)
            if match:
                character = match.group(1).strip()
                text = match.group(2).strip()

                # Skip non-dialogue labels
                if character in ['场景描述', '动作', '旁白', '画面', '镜头', '场景']:
                    continue
                if not re.search(r'[一-鿿]', text):
                    continue
                if '场景' in character or '镜头' in character:
                    continue

                text = text.replace('"', '').replace("'", '')
                if text:
                    dialogues.append(Dialogue(character=character, text=text))

        dialogues_by_segment[segment_num] = dialogues

    return dialogues_by_segment


def load_voice_map(project_path: Path) -> dict[str, str]:
    """Load character-to-voice mapping from project.json.

    Returns:
        Dict mapping character_name -> voice_type.
    """
    project_json = project_path / "project.json"
    if not project_json.exists():
        return {}

    with open(project_json, "r", encoding="utf-8") as f:
        data = json.load(f)

    voice_map = {}
    for char in data.get("characters", []):
        name = char.get("name")
        voice = char.get("voiceType")
        if name and voice:
            voice_map[name] = voice

    # Default voice from audio model config
    audio_config = data.get("models", {}).get("audio", {})
    default_voice = audio_config.get("model", "zh_male_shaonianzixin_uranus_bigtts")
    voice_map["DEFAULT"] = default_voice

    return voice_map


def merge_word_timestamps(words: list[tuple[int, int, str]], gap_threshold: int = 500) -> list[tuple[int, int, str]]:
    """Merge word-level timestamps into sentence-level.

    Args:
        words: List of (start_ms, end_ms, word_text).
        gap_threshold: Gap in ms to trigger new sentence.

    Returns:
        List of (start_ms, end_ms, sentence_text).
    """
    if not words:
        return []

    sentences = []
    current_text = words[0][2]
    current_start = words[0][0]
    current_end = words[0][1]

    sentence_end_marks = "。！？.!?"

    for i in range(1, len(words)):
        start_ms, end_ms, word_text = words[i]

        # Start new sentence if long gap or sentence-ending punctuation
        gap = start_ms - current_end
        prev_char = current_text[-1] if current_text else ""

        if gap > gap_threshold or prev_char in sentence_end_marks:
            sentences.append((current_start, current_end, current_text))
            current_text = word_text
            current_start = start_ms
            current_end = end_ms
        else:
            current_text += word_text
            current_end = end_ms

    # Don't forget last sentence
    if current_text:
        sentences.append((current_start, current_end, current_text))

    return sentences


def create_srt_file(sentences: list[tuple[int, int, str]], output_path: Path) -> None:
    """Create SRT subtitle file from sentence timestamps."""
    with open(output_path, "w", encoding="utf-8") as f:
        for i, (start_ms, end_ms, text) in enumerate(sentences, 1):
            f.write(f"{i}\n")
            f.write(f"{ms_to_srt_time(start_ms)} --> {ms_to_srt_time(end_ms)}\n")
            f.write(f"{text}\n\n")


def ms_to_srt_time(ms: int) -> str:
    """Convert milliseconds to SRT time format."""
    seconds = ms // 1000
    milliseconds = ms % 1000
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    return f"{hours:02d}:{minutes:02d}:{seconds:02d},{milliseconds:03d}"


def get_audio_duration(audio_path: Path) -> float:
    """Get audio duration in milliseconds using ffprobe."""
    try:
        result = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "csv=p=0", str(audio_path)],
            capture_output=True, text=True, check=True
        )
        return float(result.stdout.strip()) * 1000
    except Exception:
        # Fallback: rough estimate from file size
        return audio_path.stat().st_size / 8.0


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate TTS audio and subtitles")
    parser.add_argument("--project", "-p", type=str, required=True, help="Project directory")
    parser.add_argument("--script", "-s", type=str, default="script/script-01.md", help="Script path")
    parser.add_argument("--episode", type=int, default=1, help="Episode number")
    parser.add_argument("--verbose", "-v", action="store_true")
    args = parser.parse_args()

    project_path = Path(args.project)
    script_path = project_path / args.script
    logger = setup_logger("audio_generator", verbose=args.verbose)

    if not script_path.exists():
        logger.error(f"Script not found: {script_path}")
        return 1

    try:
        loader = ConfigLoader(project_path)
        config = loader.load()
    except ConfigError as e:
        logger.error(str(e))
        return 1

    missing = loader.check_required_models("audio")
    if missing:
        print(loader.format_missing_guide(missing))
        return 1

    if not config.audio_model or not config.audio_model.api_key:
        logger.error("Audio API Key not configured")
        return 1

    # Load voice mapping
    voice_map = load_voice_map(project_path)
    default_voice = voice_map.get("DEFAULT", "zh_male_shaonianzixin_uranus_bigtts")

    # Parse script
    logger.info(f"Parsing script: {script_path}")
    dialogues_by_segment = parse_script(script_path)

    if not dialogues_by_segment:
        logger.error("No dialogues found")
        return 1

    # Setup output dirs
    audio_dir = project_path / "audio" / f"ep{args.episode:02d}"
    subtitle_dir = project_path / "subtitle"
    audio_dir.mkdir(parents=True, exist_ok=True)
    subtitle_dir.mkdir(parents=True, exist_ok=True)

    # Initialize TTS client
    tts = TTSAPIClient(
        api_key=config.audio_model.api_key,
        base_url=config.audio_model.base_url or "https://openspeech.bytedance.com/api/v3/tts",
        model=config.audio_model.model,
        logger=logger,
    )

    all_sentences = []
    sum_dur = 0  # Cumulative duration offset

    total_dialogues = sum(len(d) for d in dialogues_by_segment.values())
    processed = 0

    for segment_num, dialogues in sorted(dialogues_by_segment.items()):
        logger.info(f"Processing segment {segment_num}: {len(dialogues)} dialogues")
        segment_audio_files = []
        segment_words = []

        for dialogue in dialogues:
            processed += 1
            voice_type = voice_map.get(dialogue.character, default_voice)

            logger.info(f"  [{processed}/{total_dialogues}] {dialogue.character}: {dialogue.text[:30]}...")

            audio_bytes, timestamps = tts.synthesize(
                text=dialogue.text,
                voice_type=voice_type,
                emotion=dialogue.emotion,
            )

            if audio_bytes:
                safe_name = re.sub(r'[<>:"/\\|?*]', '_', dialogue.character)
                audio_path = audio_dir / f"seg{segment_num:02d}_{safe_name}_{processed:03d}.mp3"
                audio_path.write_bytes(audio_bytes)
                segment_audio_files.append(audio_path)

                if timestamps:
                    # Get actual duration
                    duration_ms = get_audio_duration(audio_path)

                    # Apply offset
                    for start_ms, end_ms, text in timestamps:
                        segment_words.append((start_ms + sum_dur, end_ms + sum_dur, text))

                    sum_dur += duration_ms

                    logger.info(f"    Audio saved: {audio_path.name}")
            else:
                logger.warning(f"    Failed: {dialogue.text[:50]}")

        # Create subtitles for segment
        if segment_words:
            sentences = merge_word_timestamps(segment_words)
            srt_path = subtitle_dir / f"episode{args.episode:02d}_segment{segment_num:02d}.srt"
            create_srt_file(sentences, srt_path)
            logger.info(f"  Subtitle saved: {srt_path.name}")
            all_sentences.extend(sentences)

    # Create combined subtitle file
    if all_sentences:
        combined_srt = subtitle_dir / f"episode{args.episode:02d}.srt"
        create_srt_file(all_sentences, combined_srt)
        logger.info(f"Combined subtitle saved: {combined_srt.name}")

    logger.info("\n" + "=" * 50)
    logger.info("TTS generation complete!")
    logger.info(f"Audio: {audio_dir}")
    logger.info(f"Subtitles: {subtitle_dir}")
    logger.info("=" * 50)

    return 0


if __name__ == "__main__":
    sys.exit(main())
