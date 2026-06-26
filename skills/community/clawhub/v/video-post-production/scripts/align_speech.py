#!/usr/bin/env python3
import argparse
import json
import os
import subprocess
import sys
import tempfile
import time

def print_err(*args, **kwargs):
    """Print to stderr for progress tracking."""
    print(*args, file=sys.stderr, **kwargs)

def get_video_duration(video_path):
    """Get video duration using ffprobe."""
    try:
        cmd = [
            "ffprobe", "-v", "error", "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1", video_path
        ]
        output = subprocess.check_output(cmd, stderr=subprocess.PIPE).decode("utf-8").strip()
        return float(output)
    except Exception as e:
        print_err(f"Warning: Could not get video duration via ffprobe: {e}")
        return 0.0

def extract_audio(video_path, audio_path):
    """Extract audio from video using ffmpeg."""
    try:
        # Extract to 16kHz mono PCM wav (optimal for Whisper)
        cmd = [
            "ffmpeg", "-i", video_path, "-vn", "-acodec", "pcm_s16le",
            "-ar", "16000", "-ac", "1", "-y", audio_path
        ]
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode != 0:
            print_err(f"Error: ffmpeg extraction failed with exit code {result.returncode}")
            print_err(result.stderr.decode())
            return False
        return True
    except FileNotFoundError:
        print_err("Error: 'ffmpeg' not found. Please install ffmpeg.")
        return False

def check_dependencies():
    """Check if ffmpeg and ffprobe are available."""
    for cmd in ["ffmpeg", "ffprobe"]:
        try:
            subprocess.run([cmd, "-version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except FileNotFoundError:
            print_err(f"Error: '{cmd}' is not installed or not in PATH.")
            return False
    return True

def main():
    parser = argparse.ArgumentParser(description="Align speech in video using faster-whisper.")
    parser.add_argument("--video", required=True, help="Input video path")
    parser.add_argument("--output", required=True, help="Output JSON path")
    parser.add_argument("--model", default="medium", help="Whisper model size (default: medium)")
    parser.add_argument("--language", default="zh", help="Language code (default: zh)")
    
    args = parser.parse_args()

    # 0. Check dependencies
    if not check_dependencies():
        sys.exit(1)

    if not os.path.exists(args.video):
        print_err(f"Error: Video file not found: {args.video}")
        sys.exit(1)

    # Load faster-whisper
    try:
        from faster_whisper import WhisperModel
    except ImportError:
        print_err("Error: 'faster-whisper' package not found. Run 'pip install faster-whisper'.")
        sys.exit(1)

    start_time = time.time()
    
    # 1. Get duration
    print_err(f"--> Processing: {os.path.basename(args.video)}")
    duration = get_video_duration(args.video)
    
    # 2. Extract audio
    fd, tmp_audio_path = tempfile.mkstemp(suffix=".wav")
    os.close(fd) # Close file descriptor so ffmpeg can write to it
    
    try:
        print_err("--> Extracting audio...")
        if not extract_audio(args.video, tmp_audio_path):
            sys.exit(1)

        # 3. Transcribe
        print_err(f"--> Initializing Whisper model '{args.model}'...")
        # device="auto" handles CUDA vs CPU automatically
        model = WhisperModel(args.model, device="auto", compute_type="default")

        print_err(f"--> Transcribing (language: {args.language})...")
        segments_iterator, info = model.transcribe(
            tmp_audio_path,
            language=args.language,
            word_timestamps=True,
            beam_size=5
        )

        segments_data = []
        for segment in segments_iterator:
            words_data = []
            if segment.words:
                for w in segment.words:
                    words_data.append({
                        "word": w.word.strip(),
                        "start": round(w.start, 3),
                        "end": round(w.end, 3)
                    })
            
            segments_data.append({
                "start": round(segment.start, 3),
                "end": round(segment.end, 3),
                "text": segment.text.strip(),
                "words": words_data
            })

        output_json = {
            "segments": segments_data,
            "duration": duration
        }

        # 4. Save result
        print_err(f"--> Saving alignment to {args.output}...")
        output_dir = os.path.dirname(os.path.abspath(args.output))
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
            
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(output_json, f, ensure_ascii=False, indent=2)

        elapsed = time.time() - start_time
        print_err(f"--> Successfully completed in {elapsed:.1f}s.")

    except Exception as e:
        print_err(f"Error during execution: {e}")
        sys.exit(1)
    finally:
        if os.path.exists(tmp_audio_path):
            try:
                os.remove(tmp_audio_path)
            except Exception as e:
                print_err(f"Warning: Failed to cleanup temp file {tmp_audio_path}: {e}")

if __name__ == "__main__":
    main()
