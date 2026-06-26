#!/usr/bin/env python3
"""
Generate timed captions from video audio using Whisper.

Creates SRT/VTT captions synced to video timeline.
Optionally burns captions into video.

Requirements:
    pip install openai-whisper

Usage:
    python caption-sync.py input.mp4 --output captions.srt
    python caption-sync.py input.mp4 --output captions.srt --burn
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path


def check_whisper():
    """Check if Whisper is installed."""
    try:
        import whisper
        return True
    except ImportError:
        return False


def transcribe_audio(video_path: str, model_size: str = "base", verbose: bool = False) -> dict:
    """Transcribe audio using Whisper."""
    if not check_whisper():
        print("Error: Whisper not installed. Run: pip install openai-whisper")
        return None
    
    import whisper
    
    if verbose:
        print(f"Loading Whisper model: {model_size}")
    
    model = whisper.load_model(model_size)
    
    if verbose:
        print(f"Transcribing: {video_path}")
    
    result = model.transcribe(video_path)
    
    return result


def format_timestamp(seconds: float) -> str:
    """Format seconds to SRT timestamp format."""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds - int(seconds)) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"


def format_vtt_timestamp(seconds: float) -> str:
    """Format seconds to VTT timestamp format."""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds - int(seconds)) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d}.{millis:03d}"


def generate_srt(segments: list, output_path: str) -> None:
    """Generate SRT file from transcription segments."""
    with open(output_path, 'w', encoding='utf-8') as f:
        for i, segment in enumerate(segments, 1):
            start = format_timestamp(segment['start'])
            end = format_timestamp(segment['end'])
            text = segment['text'].strip()
            
            if text:
                f.write(f"{i}\n")
                f.write(f"{start} --> {end}\n")
                f.write(f"{text}\n\n")


def generate_vtt(segments: list, output_path: str) -> None:
    """Generate VTT file from transcription segments."""
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("WEBVTT\n\n")
        
        for segment in segments:
            start = format_vtt_timestamp(segment['start'])
            end = format_vtt_timestamp(segment['end'])
            text = segment['text'].strip()
            
            if text:
                f.write(f"{start} --> {end}\n")
                f.write(f"{text}\n\n")


def burn_captions(video_path: str, srt_path: str, output_path: str, 
                  font_size: int = 24, font_color: str = "white",
                  position: str = "bottom", verbose: bool = False) -> bool:
    """Burn captions into video using FFmpeg."""
    
    # Calculate position
    y_position = "h-th-50" if position == "bottom" else "50"
    
    # Escape path for FFmpeg
    srt_escaped = srt_path.replace(':', '\\:')
    
    # Build filter
    vfilter = f"subtitles='{srt_escaped}':force_style='FontSize={font_size},PrimaryColour=&H{font_color}&,OutlineColour=&H000000&,Outline=2'"
    
    cmd = [
        "ffmpeg", "-y",
        "-i", video_path,
        "-vf", vfilter,
        "-c:v", "libx264",
        "-c:a", "copy",
        output_path
    ]
    
    if verbose:
        print(f"Running: {' '.join(cmd)}")
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"FFmpeg error: {result.stderr}")
        return False
    
    if verbose:
        print(f"Burned captions saved to: {output_path}")
    
    return True


def generate_captions(video_path: str, output_path: str,
                      format: str = "srt",
                      model_size: str = "base",
                      burn: bool = False,
                      output_video: str = None,
                      verbose: bool = False) -> bool:
    """Generate captions from video."""
    
    # Transcribe
    result = transcribe_audio(video_path, model_size, verbose)
    
    if not result:
        return False
    
    segments = result.get('segments', [])
    
    if not segments:
        print("Error: No speech detected in video")
        return False
    
    if verbose:
        print(f"Detected {len(segments)} caption segments")
    
    # Determine output format
    suffix = Path(output_path).suffix.lower()
    
    if format == "srt" or suffix == ".srt":
        generate_srt(segments, output_path)
        if verbose:
            print(f"SRT saved to: {output_path}")
    elif format == "vtt" or suffix == ".vtt":
        generate_vtt(segments, output_path)
        if verbose:
            print(f"VTT saved to: {output_path}")
    elif format == "json":
        with open(output_path, 'w') as f:
            json.dump(segments, f, indent=2)
        if verbose:
            print(f"JSON saved to: {output_path}")
    else:
        # Default to SRT
        generate_srt(segments, output_path)
    
    # Burn captions if requested
    if burn:
        video_out = output_video or str(Path(video_path).with_name(
            Path(video_path).stem + "_captioned.mp4"
        ))
        success = burn_captions(video_path, output_path, video_out, verbose=verbose)
        
        if success:
            if verbose:
                print(f"Burned video saved to: {video_out}")
            return True
        return False
    
    return True


def main():
    parser = argparse.ArgumentParser(description="Generate captions from Roblox video")
    parser.add_argument("input", help="Input video file")
    parser.add_argument("--output", "-o", default="captions.srt", help="Output caption file")
    parser.add_argument("--format", "-f", choices=["srt", "vtt", "json"], 
                        default="srt", help="Caption format")
    parser.add_argument("--model", "-m", default="base", 
                        choices=["tiny", "base", "small", "medium", "large"],
                        help="Whisper model size")
    parser.add_argument("--burn", "-b", action="store_true", 
                        help="Burn captions into video")
    parser.add_argument("--output-video", help="Output video with burned captions")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    
    args = parser.parse_args()
    
    if not Path(args.input).exists():
        print(f"Error: Input file not found: {args.input}")
        sys.exit(1)
    
    success = generate_captions(
        args.input, args.output,
        format=args.format,
        model_size=args.model,
        burn=args.burn,
        output_video=args.output_video,
        verbose=args.verbose
    )
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()