#!/usr/bin/env python3
"""
Text-to-Speech using edge-tts (Microsoft Neural TTS).
Converts to OGG/Opus for Feishu compatibility.
"""
import argparse
import os
import sys
import time
import shutil

IS_WINDOWS = sys.platform == "win32" or sys.platform == "cygwin"
IS_LINUX = sys.platform.startswith("linux")
IS_MACOS = sys.platform == "darwin"


def get_default_output_dir():
    workspace = os.environ.get("OPENCLAW_WORKSPACE",
                              os.path.join(os.path.expanduser("~"), ".openclaw", "workspace"))
    return os.path.join(workspace, "projects", "tts-synthesizer", "output")


def get_skill_dir():
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def ensure_opus_available():
    """Check if PyAV is available for conversion."""
    try:
        import av
        return True
    except ImportError:
        return False


def convert_to_ogg_opus(input_path, output_path=None):
    """Convert audio to OGG/Opus format using PyAV."""
    import av
    from av.audio.resampler import AudioResampler

    if output_path is None:
        output_path = input_path.rsplit('.', 1)[0] + '.ogg'

    # Open input
    in_container = av.open(input_path)
    in_stream = in_container.streams.audio[0]

    # Resampler: convert any input to mono 16kHz s16
    resampler = AudioResampler(format='s16', layout='mono', rate=16000)

    # Create output OGG/Opus
    out_container = av.open(output_path, 'w')
    out_stream = out_container.add_stream('libopus', rate=16000, layout='mono')

    # Convert
    for frame in in_container.decode(in_stream):
        resampled = resampler.resample(frame)
        if resampled is not None:
            if not isinstance(resampled, list):
                resampled = [resampled]
            for r in resampled:
                for p in out_stream.encode(r):
                    out_container.mux(p)

    # Flush resampler
    resampled = resampler.resample(None)
    if resampled is not None:
        if not isinstance(resampled, list):
            resampled = [resampled]
        for r in resampled:
            for p in out_stream.encode(r):
                out_container.mux(p)

    # Flush encoder
    for p in out_stream.encode(None):
        out_container.mux(p)

    out_container.close()
    in_container.close()
    return output_path


def tts_with_edge(text, output_path, voice="zh-CN-XiaoxiaoNeural", rate="+0%", pitch="+0Hz"):
    """Generate speech using edge-tts and convert to OGG/Opus."""
    import asyncio
    import edge_tts

    async def _generate():
        communicate = edge_tts.Communicate(
            text,
            voice,
            rate=rate,
            pitch=pitch
        )
        # Save as webm first (edge-tts default)
        webm_path = output_path + '.webm'
        await communicate.save(webm_path)
        return webm_path

    webm_path = asyncio.run(_generate())

    # Convert to OGG/Opus for Feishu compatibility
    if os.path.exists(output_path):
        os.remove(output_path)
    convert_to_ogg_opus(webm_path, output_path)
    os.remove(webm_path)


def tts_with_api(text, output_path, api_url, api_key, model="tts-1", voice="alloy"):
    """Generate speech using OpenAI-compatible API."""
    from openai import OpenAI

    client = OpenAI(api_key=api_key, base_url=api_url)
    response = client.audio.speech.create(
        model=model,
        voice=voice,
        input=text,
        response_format="mp3"
    )
    with open(output_path, 'wb') as f:
        f.write(response.content)

    # Convert to OGG/Opus
    ogg_path = output_path.rsplit('.', 1)[0] + '.ogg'
    convert_to_ogg_opus(output_path, ogg_path)
    os.remove(output_path)
    return ogg_path


def main():
    parser = argparse.ArgumentParser(description="Text-to-Speech using edge-tts (Microsoft Neural TTS).")
    parser.add_argument("input", help="Text to speak, or path to .txt file")
    parser.add_argument("--output", "-o", default=None, help="Output audio file (.ogg for voice, .mp3 for API)")
    parser.add_argument("--engine", "-e", default="edge", choices=["edge", "api"],
                        help="TTS engine (default: edge)")
    parser.add_argument("--voice", "-v", default="zh-CN-XiaoxiaoNeural",
                        help="Voice (default: zh-CN-XiaoxiaoNeural)")
    parser.add_argument("--rate", "-r", default="+0%",
                        help="Speech rate, e.g. '+10%%' or '-5%%' (edge-tts only)")
    parser.add_argument("--pitch", "-p", default="+0Hz",
                        help="Pitch adjustment, e.g. '+5Hz' (edge-tts only)")
    parser.add_argument("--api-url", default=os.environ.get("TTS_API_URL", ""),
                        help="OpenAI-compatible API URL")
    parser.add_argument("--api-key", default=os.environ.get("TTS_API_KEY", ""),
                        help="API key")
    parser.add_argument("--api-model", default="tts-1",
                        help="API model (default: tts-1)")
    parser.add_argument("--output-dir", default=None,
                        help="Output directory")
    parser.add_argument("--keep-mp3", action="store_true",
                        help="Keep original MP3 (don't convert to OGG)")
    args = parser.parse_args()

    # Read text from file or use as-is
    if os.path.isfile(args.input):
        with open(args.input, 'r', encoding='utf-8') as f:
            text = f.read().strip()
    else:
        text = args.input

    if not text:
        print("ERROR: Empty text", file=sys.stderr)
        sys.exit(1)

    # Setup output path
    if args.output:
        output_path = args.output
    else:
        output_dir = args.output_dir or get_default_output_dir()
        os.makedirs(output_dir, exist_ok=True)
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        output_path = os.path.join(output_dir, f"tts_{timestamp}.ogg")

    print(f"[TTS] Starting...")
    print(f"  Text:      {text[:80]}{'...' if len(text) > 80 else ''}")
    print(f"  Engine:    {args.engine}")
    print(f"  Voice:     {args.voice}")
    print(f"  Output:    {output_path}")
    print()

    try:
        if args.engine == "edge":
            tts_with_edge(text, output_path, voice=args.voice, rate=args.rate, pitch=args.pitch)
        elif args.engine == "api":
            if not args.api_url or not args.api_key:
                print("ERROR: --api-url and --api-key required for API mode", file=sys.stderr)
                sys.exit(1)
            output_path = tts_with_api(text, output_path, args.api_url, args.api_key,
                                      model=args.api_model, voice=args.voice)

        size = os.path.getsize(output_path)
        print()
        print(f"Done! Output: {output_path}")
        print(f"  Size: {size / 1024:.1f} KB")
        print(output_path)

    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
