#!/usr/bin/env python3
"""
TTS Script for Video Podcast Maker (Azure / Doubao / CosyVoice / Edge / ElevenLabs / OpenAI / Google TTS)
Generates audio from podcast.txt and creates SRT subtitles + timing.json for Remotion sync
"""
import os
import sys
import re
import argparse
import subprocess

from tts.phonemes import load_phoneme_dicts, extract_inline_phonemes
from tts.sections import parse_sections, validate_sections, print_validation_report, match_section_times
from tts.srt import write_srt, write_timing


def build_parser():
    parser = argparse.ArgumentParser(
        description='Generate TTS audio from podcast script',
        epilog='Backends: edge (default, free), azure, doubao, cosyvoice, elevenlabs, openai, google. '
               'Env: TTS_BACKEND, AZURE_SPEECH_KEY, VOLCENGINE_APPID, VOLCENGINE_ACCESS_TOKEN, '
               'DASHSCOPE_API_KEY, EDGE_TTS_VOICE, ELEVENLABS_API_KEY, OPENAI_API_KEY, GOOGLE_TTS_API_KEY, TTS_RATE'
    )
    parser.add_argument('--input', '-i', default='podcast.txt', help='Input script file (default: podcast.txt)')
    parser.add_argument('--output-dir', '-o', default='.', help='Output directory (default: current dir)')
    parser.add_argument('--phonemes', '-p', default=None, help='Phoneme dictionary JSON file')
    parser.add_argument('--backend', '-b', default=None,
        help='TTS backend: edge, azure, doubao, cosyvoice, elevenlabs, openai, or google')
    parser.add_argument('--resume', action='store_true', help='Resume from last breakpoint')
    parser.add_argument('--dry-run', action='store_true', help='Estimate duration without calling TTS API')
    parser.add_argument('--validate', action='store_true', help='Validate podcast.txt format without calling TTS API')
    return parser


def chunk_text(clean_text, max_chars):
    """Split text into chunks for TTS synthesis.

    Handles both Chinese (。；) and English (. ; ? !) sentence boundaries.
    """
    # Normalize semicolons to periods for splitting
    normalized = clean_text.replace("；", "。")
    # Split on Chinese period, English sentence-ending punctuation, or newlines
    sentences = re.split(r'(?<=[。.!?])\s*', normalized)
    chunks = []
    current_chunk = ""
    for s in sentences:
        s = s.strip()
        if not s:
            continue
        if len(current_chunk) + len(s) + 1 < max_chars:
            current_chunk += s if s.endswith(("。", ".", "!", "?")) else s + "。"
        else:
            if current_chunk:
                chunks.append(current_chunk)
            current_chunk = s if s.endswith(("。", ".", "!", "?")) else s + "。"
    if current_chunk:
        chunks.append(current_chunk)
    return chunks


def main():
    parser = build_parser()
    args = parser.parse_args()

    # --- Backend init (skip for validate-only) ---
    if not args.validate:
        BACKEND = args.backend or os.environ.get("TTS_BACKEND", "edge")
        print(f"TTS backend: {BACKEND}")

        from tts.backends import init_backend, get_synthesize_func, get_max_chars
        config = init_backend(BACKEND)
        MAX_CHARS = get_max_chars(BACKEND)
    else:
        BACKEND = "edge"
        MAX_CHARS = 400

    SPEECH_RATE = os.environ.get("TTS_RATE", "+5%")

    # --- Read input ---
    os.makedirs(args.output_dir, exist_ok=True)

    if not os.path.exists(args.input):
        print(f"Error: Input file not found: {args.input}", file=sys.stderr)
        sys.exit(1)

    with open(args.input, "r", encoding="utf-8") as f:
        text = f.read().strip()

    # --- Parse sections ---
    sections, matches, clean_text = parse_sections(text)

    # --- Validate mode ---
    if args.validate:
        errors, warnings = validate_sections(text, sections, matches)
        print_validation_report(args.input, sections, clean_text, errors, warnings)
        return  # print_validation_report calls sys.exit, but guard against refactoring

    # --- Phonemes ---
    clean_text, inline_phonemes = extract_inline_phonemes(clean_text)
    if inline_phonemes:
        print(f"Extracted inline phoneme annotations: {len(inline_phonemes)} entries")
        for word, pinyin in inline_phonemes.items():
            print(f"    {word} -> {pinyin}")

    file_phonemes = load_phoneme_dicts(args.input, args.phonemes)
    phoneme_dict = {**file_phonemes, **inline_phonemes}
    print(f"Phoneme dictionary: {len(phoneme_dict)} entries (file: {len(file_phonemes)} + inline: {len(inline_phonemes)})")

    if BACKEND == "doubao" and phoneme_dict:
        print("Warning: Doubao TTS does not support the phoneme system. "
              "Inline markers and phonemes.json will be ignored. "
              "Consider using Azure or CosyVoice for phoneme support.", file=sys.stderr)
    if BACKEND in ("elevenlabs", "openai", "google") and phoneme_dict:
        print("Warning: ElevenLabs/OpenAI/Google TTS do not support the phoneme system. "
              "Inline markers and phonemes.json will be ignored. "
              "Consider using Azure or CosyVoice for phoneme support.", file=sys.stderr)

    # --- Default section ---
    if not sections:
        sections = [{'name': 'main', 'first_text': '', 'start_time': 0, 'end_time': None}]
        print("Note: No [SECTION:name] markers detected, generating single section")
    else:
        print(f"Detected {len(sections)} sections: {[s['name'] for s in sections]}")
        for s in sections:
            status = " (silent)" if s.get('is_silent') else ""
            print(f"  {s['name']}: \"{s['first_text'][:20]}...\"{status}")

    # --- Text cleanup ---
    clean_text = re.sub(r'([A-Za-z0-9\-]+)，读作["""]([\u4e00-\u9fff]+)["""]', r"\2", clean_text)
    print(f"Text length: {len(clean_text)} characters")

    # --- Dry run ---
    if args.dry_run:
        cn_chars = len(re.findall(r'[\u4e00-\u9fff]', clean_text))
        en_words = len(re.findall(r'[A-Za-z]+', clean_text))
        est_duration = cn_chars / 4.0 + en_words / 3.0
        rate_match = re.match(r'([+-]?\d+)%', SPEECH_RATE)
        if rate_match:
            est_duration /= 1.0 + int(rate_match.group(1)) / 100.0
        est_frames = int(est_duration * 30)
        print(f"\n--- Dry Run ---")
        print(f"Chinese chars: {cn_chars}, English words: {en_words}")
        print(f"Estimated duration: {est_duration:.0f}s ({est_duration/60:.1f}min)")
        print(f"Estimated frames: {est_frames} @ 30fps")
        print(f"Speech rate: {SPEECH_RATE}")
        print(f"Backend: {BACKEND} (not called)")
        non_silent = [s for s in sections if not s.get('is_silent')]
        if len(non_silent) > 1:
            avg = est_duration / len(non_silent)
            print(f"Average section: ~{avg:.0f}s ({len(non_silent)} sections with content)")
        sys.exit(0)

    # --- Chunk text ---
    chunks = chunk_text(clean_text, MAX_CHARS)
    print(f"Split into {len(chunks)} chunks")

    # --- Synthesize ---
    config['speech_rate'] = SPEECH_RATE
    config['phoneme_dict'] = phoneme_dict
    synthesize = get_synthesize_func(BACKEND)
    part_files, word_boundaries, total_duration = synthesize(chunks, config, args.output_dir, resume=args.resume)
    print(f"\nCollected {len(word_boundaries)} word boundaries")
    print(f"Total duration: {total_duration:.1f}s")

    # --- Match section times ---
    sections = match_section_times(sections, word_boundaries, total_duration)

    # --- Generate SRT + timing.json (before concat, so they're saved even if concat fails) ---
    print("\nGenerating subtitles...")
    output_srt = os.path.join(args.output_dir, "podcast_audio.srt")
    write_srt(word_boundaries, output_srt)

    output_timing = os.path.join(args.output_dir, "timing.json")
    write_timing(sections, total_duration, SPEECH_RATE, output_timing)

    # --- Concat audio ---
    print("\nConcatenating audio...")
    concat_list = os.path.join(args.output_dir, "concat_list.txt")
    output_wav = os.path.join(args.output_dir, "podcast_audio.wav")
    with open(concat_list, "w", encoding="utf-8") as f:
        for pf in part_files:
            f.write(f"file '{os.path.basename(pf)}'\n")

    concat_result = subprocess.run(
        ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", concat_list, "-c", "copy", output_wav],
        capture_output=True, text=True, cwd=args.output_dir)
    if concat_result.returncode != 0:
        print(f"Error: FFmpeg concat failed:\n{concat_result.stderr}", file=sys.stderr)
        print("Note: timing.json and podcast_audio.srt were saved successfully.", file=sys.stderr)
        sys.exit(1)
    print(f"Done: {output_wav}")
    print(f"  Temp files kept: {len(part_files)} part_*.wav (manual cleanup: Step 14)")


if __name__ == "__main__":
    main()
