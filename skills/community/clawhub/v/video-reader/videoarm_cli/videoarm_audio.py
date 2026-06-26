"""videoarm-audio: Extract and transcribe audio from frame ranges.

Accepts video URL or local path. Automatically downloads and resolves metadata.
"""

import argparse
import json
import os
import subprocess
import sys
import tempfile

from videoarm_lib.logger import ToolTracer
from videoarm_lib.resolve import resolve_video


def extract_and_transcribe(video_path, start_frame, end_frame, fps, tracer=None):
    """Extract audio from frame range and transcribe via Whisper API."""
    start_time = start_frame / fps
    duration = end_frame / fps - start_time

    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
        tmp = f.name

    try:
        subprocess.run(
            ["ffmpeg", "-y", "-i", str(video_path),
             "-ss", str(start_time), "-t", str(duration),
             "-vn", "-acodec", "pcm_s16le", "-ar", "16000", "-ac", "1", tmp],
            capture_output=True, text=True, check=True,
        )

        if tracer:
            file_size = os.path.getsize(tmp)
            tracer.log("audio_extracted", duration_sec=round(duration, 2), file_size_kb=round(file_size / 1024, 1))

        api_key = os.environ.get("WHISPER_API_KEY", "")
        base_url = os.environ.get("WHISPER_BASE_URL", "https://api.groq.com/openai/v1")
        model = os.environ.get("WHISPER_MODEL", "whisper-large-v3")
        if not api_key:
            return {"error": "WHISPER_API_KEY not set"}

        import requests
        proxy = os.environ.get("HTTPS_PROXY") or os.environ.get("https_proxy")
        # Don't proxy localhost requests
        is_local = "127.0.0.1" in base_url or "localhost" in base_url
        proxies = {"https": proxy, "http": proxy} if proxy and not is_local else None

        if tracer:
            tracer.log("api_call", model=model, base_url=base_url, proxy=bool(proxy))

        with open(tmp, "rb") as audio_file:
            resp = requests.post(
                f"{base_url}/audio/transcriptions",
                headers={"Authorization": f"Bearer {api_key}"},
                files={"file": ("audio.wav", audio_file, "audio/wav")},
                data={"model": model, "response_format": "verbose_json"},
                timeout=120,
                proxies=proxies,
            )
        resp.raise_for_status()
        data = resp.json()

        segments = []
        for seg in data.get("segments", []):
            seg_start = start_time + seg["start"]
            seg_end = start_time + seg["end"]
            segments.append({
                "text": seg["text"].strip(),
                "start_time": round(seg_start, 2),
                "end_time": round(seg_end, 2),
                "start_frame": int(seg_start * fps),
                "end_frame": int(seg_end * fps),
            })

        if tracer:
            tracer.log("api_response", segments=len(segments), transcript_len=len(data.get("text", "")))

        return {
            "transcript": data.get("text", ""),
            "segments": segments,
            "frame_range": [start_frame, end_frame],
        }
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)


def main():
    parser = argparse.ArgumentParser(description="Transcribe audio from video")
    parser.add_argument("video", help="Video file path or URL")
    parser.add_argument("--start", type=int, default=0)
    parser.add_argument("--end", type=int, default=None)
    args = parser.parse_args()

    from dotenv import load_dotenv
    load_dotenv()

    try:
        with ToolTracer("audio", video=args.video, start_frame=args.start, end_frame=args.end) as t:
            video_path, meta = resolve_video(args.video, tracer=t)

            if not meta["has_audio"]:
                json.dump({"status": "no_audio", "message": "No audio stream", "meta": meta}, sys.stdout)
                print()
                return

            fps = meta["fps"]
            end = args.end if args.end is not None else meta["total_frames"] - 1

            result = extract_and_transcribe(video_path, args.start, end, fps, tracer=t)
            result["video"] = str(video_path)
            result["meta"] = meta
            t.set_result(result)

        json.dump(result, sys.stdout, indent=2)
        print()
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
