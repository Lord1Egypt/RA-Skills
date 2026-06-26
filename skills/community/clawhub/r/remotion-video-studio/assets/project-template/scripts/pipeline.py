#!/usr/bin/env python3
"""
Pipeline script — end-to-end: TTS generation → render props → Remotion render.

Features:
  - Config validation at startup
  - Optional audio post-processing (loudness normalization)
  - Intro/outro slide type support
  - Render progress logging

Usage:
    python scripts/pipeline.py                       # Use default TTS engine from config
    python scripts/pipeline.py --tts edge            # Force Edge TTS
    python scripts/pipeline.py --tts qwen            # Force Qwen TTS
    python scripts/pipeline.py --skip-tts            # Skip TTS, use existing audio
    python scripts/pipeline.py --skip-render         # Only generate TTS + props, no render
"""

import json
import os
import subprocess
import sys
import argparse

from tts_utils import resolve_project_root, load_config_and_content


# ---------------------------------------------------------------------------
# Config Validation
# ---------------------------------------------------------------------------

def validate_config(config: dict) -> list[str]:
    """
    Validate project configuration and return a list of error messages.
    Returns empty list if config is valid.
    """
    errors = []

    # Video config
    video = config.get("video", {})
    if video.get("width", 0) <= 0 or video.get("height", 0) <= 0:
        errors.append(f"video.width/height must be positive, got {video.get('width')}×{video.get('height')}")
    if video.get("fps", 0) <= 0 or video.get("fps", 0) > 120:
        errors.append(f"video.fps must be 1-120, got {video.get('fps')}")
    if video.get("crf", -1) < 0 or video.get("crf", 100) > 63:
        errors.append(f"video.crf must be 0-63, got {video.get('crf')}")

    # TTS config
    tts = config.get("tts", {})
    if tts.get("engine") not in ("edge", "qwen"):
        errors.append(f"tts.engine must be 'edge' or 'qwen', got '{tts.get('engine')}'")
    speed_rate = tts.get("speedRate", 1.0)
    if speed_rate <= 0 or speed_rate > 3.0:
        errors.append(f"tts.speedRate must be 0.1-3.0, got {speed_rate}")

    # Animation config
    anim = config.get("animation", {})
    if anim.get("transition") not in ("fade", "slide", "wipe", "none"):
        errors.append(f"animation.transition must be fade/slide/wipe/none, got '{anim.get('transition')}'")
    if anim.get("paddingFrames", 0) < 0:
        errors.append(f"animation.paddingFrames must be >= 0, got {anim.get('paddingFrames')}")

    # Subtitle config
    sub = config.get("subtitle", {})
    if sub.get("style") not in ("tiktok", "bottom", "center"):
        errors.append(f"subtitle.style must be tiktok/bottom/center, got '{sub.get('style')}'")
    if sub.get("displayMode") not in ("sentence", "full"):
        errors.append(f"subtitle.displayMode must be sentence/full, got '{sub.get('displayMode')}'")

    return errors


def validate_content(content: dict) -> list[str]:
    """Validate content script and return a list of error messages."""
    errors = []
    slides = content.get("slides", [])
    if not slides:
        errors.append("No slides found in content file")
        return errors

    seen_ids = set()
    for i, slide in enumerate(slides):
        sid = slide.get("id", "")
        if not sid:
            errors.append(f"Slide {i+1}: missing 'id' field")
        elif sid in seen_ids:
            errors.append(f"Slide {i+1}: duplicate id '{sid}'")
        seen_ids.add(sid)

        if not slide.get("text", "").strip():
            errors.append(f"Slide '{sid}': empty 'text' field")

    return errors


# ---------------------------------------------------------------------------
# Audio Post-Processing
# ---------------------------------------------------------------------------

def normalize_audio(file_path: str) -> None:
    """
    Normalize audio loudness using ffmpeg (EBU R128).
    Overwrites the original file.
    """
    tmp_path = file_path + ".tmp.mp3"
    try:
        subprocess.run(
            [
                "ffmpeg", "-y", "-i", file_path,
                "-filter:a", "loudnorm=I=-16:TP=-1.5:LRA=11",
                "-ar", "44100",
                tmp_path,
            ],
            capture_output=True, text=True, check=True,
        )
        os.replace(tmp_path, file_path)
    except (subprocess.CalledProcessError, FileNotFoundError):
        # Silently skip if ffmpeg fails — normalization is optional
        if os.path.exists(tmp_path):
            os.remove(tmp_path)


def post_process_audio(audio_dir: str, slides: list) -> None:
    """Run audio post-processing on all generated audio files."""
    print("\n🔊 Audio post-processing (loudness normalization)...\n")
    for slide in slides:
        slide_id = slide["id"]
        for ext in ("mp3", "wav"):
            audio_path = os.path.join(audio_dir, f"{slide_id}.{ext}")
            if os.path.exists(audio_path):
                print(f"  Normalizing {slide_id}.{ext}...")
                normalize_audio(audio_path)
                break
    print("  ✅ Audio post-processing complete")


# ---------------------------------------------------------------------------
# TypeScript Pre-Check
# ---------------------------------------------------------------------------

def typecheck(root: str) -> None:
    """
    Run TypeScript type check before rendering to catch errors early.
    This avoids wasting time on TTS + audio processing only to fail at render.
    """
    print("\n🔍 TypeScript pre-check...\n")
    try:
        result = subprocess.run(
            ["npx", "tsc", "--noEmit"],
            cwd=root,
            capture_output=True,
            text=True,
            timeout=120,
        )
        if result.returncode != 0:
            print("❌ TypeScript errors found:")
            # Show at most 30 lines of errors to avoid flooding
            lines = (result.stdout + result.stderr).strip().splitlines()
            for line in lines[:30]:
                print(f"   {line}")
            if len(lines) > 30:
                print(f"   ... and {len(lines) - 30} more lines")
            print()
            print("💡 Fix the TypeScript errors above before running the pipeline.")
            print("   Common issues:")
            print("   • Curly braces in JSX text: use {\"text with { braces }\"} instead")
            print("   • Missing imports or typos in component names")
            print("   • Wrong prop types passed to components")
            sys.exit(1)
        else:
            print("  ✅ TypeScript check passed")
    except FileNotFoundError:
        print("  ⚠️  npx/tsc not found, skipping type check")
    except subprocess.TimeoutExpired:
        print("  ⚠️  TypeScript check timed out (120s), skipping")


# ---------------------------------------------------------------------------
# Core Pipeline Functions
# ---------------------------------------------------------------------------

def get_audio_duration(file_path: str) -> float:
    """Get audio duration using ffprobe."""
    try:
        result = subprocess.run(
            [
                "ffprobe", "-v", "quiet",
                "-show_entries", "format=duration",
                "-of", "csv=p=0",
                file_path,
            ],
            capture_output=True, text=True, check=True,
        )
        return float(result.stdout.strip())
    except Exception as e:
        print(f"  ⚠️  ffprobe failed for {file_path}: {e}. Using default 3.0s")
        return 3.0


def run_tts(
    tts_engine: str,
    config: dict,
    root: str,
    config_path: str,
    content_path: str,
) -> None:
    """Run the TTS generation step."""
    print("\n📢 Step 1: Generating TTS audio...\n")

    tts_script_map = {
        "edge": "scripts/tts_edge.py",
        "qwen": "scripts/tts_qwen.py",
    }

    tts_script = tts_script_map.get(tts_engine)
    if not tts_script:
        print(f"❌ Unknown TTS engine: {tts_engine}")
        print(f"   Available: {', '.join(tts_script_map.keys())}")
        sys.exit(1)

    tts_script_path = os.path.join(root, tts_script)

    # Determine how to invoke the TTS script.
    python_env = config["tts"].get("pythonEnv", {})
    env_type = python_env.get("type", "conda")
    use_env = tts_engine in ("qwen",)

    if use_env:
        if env_type == "venv":
            venv_path = python_env.get("venv", {}).get("path", ".venv")
            if not os.path.isabs(venv_path):
                venv_path = os.path.join(root, venv_path)
            activate_script = os.path.join(venv_path, "bin", "activate")
            if os.path.exists(activate_script):
                shell_cmd = (
                    f"source {activate_script} && "
                    f"python {tts_script_path} "
                    f"--config {config_path} --content {content_path}"
                )
                print(f"  [venv] {venv_path}")
                print(f"  Running: {shell_cmd}\n")
                try:
                    subprocess.run(
                        ["bash", "-c", shell_cmd],
                        check=True, cwd=root,
                    )
                except subprocess.CalledProcessError as e:
                    print(f"\n❌ TTS generation failed (exit code {e.returncode})")
                    sys.exit(1)
            else:
                print(f"⚠️  venv activate not found: {activate_script}")
                print(f"   Falling back to system python.\n")
                use_env = False

        elif env_type == "conda":
            conda_name = python_env.get("conda", {}).get("name", "base")
            shell_cmd = (
                f'eval "$(conda shell.bash hook 2>/dev/null)" && '
                f"conda activate {conda_name} && "
                f"python {tts_script_path} "
                f"--config {config_path} --content {content_path}"
            )
            print(f"  [conda] env={conda_name}")
            print(f"  Running: {shell_cmd}\n")
            try:
                subprocess.run(
                    ["bash", "-c", shell_cmd],
                    check=True, cwd=root,
                )
            except subprocess.CalledProcessError as e:
                print(f"\n❌ TTS generation failed (exit code {e.returncode})")
                sys.exit(1)
        else:
            print(f"⚠️  Unknown pythonEnv.type: {env_type}, falling back to system python.")
            use_env = False

    if not use_env:
        cmd = [
            sys.executable, tts_script_path,
            "--config", config_path,
            "--content", content_path,
        ]
        print(f"  Running: {' '.join(cmd)}\n")
        try:
            subprocess.run(cmd, check=True, cwd=root)
        except subprocess.CalledProcessError as e:
            print(f"\n❌ TTS generation failed (exit code {e.returncode})")
            sys.exit(1)


def generate_render_props(
    config: dict,
    content: dict,
    root: str,
    audio_dir: str,
    props_path: str,
) -> int:
    """
    Probe audio durations and generate render-props.json.

    Returns:
        Total frame count for the video.
    """
    print("📐 Step 2: Generating render props...\n")

    fps = config["video"]["fps"]
    padding_frames = config["animation"]["paddingFrames"]
    slides = []

    for slide in content.get("slides", []):
        slide_id = slide["id"]
        slide_type = slide.get("type", "content")
        audio_file = ""
        audio_duration = 3.0

        mp3_path = os.path.join(audio_dir, f"{slide_id}.mp3")
        wav_path = os.path.join(audio_dir, f"{slide_id}.wav")

        if os.path.exists(mp3_path):
            audio_file = f"audio/{slide_id}.mp3"
            audio_duration = get_audio_duration(mp3_path)
        elif os.path.exists(wav_path):
            audio_file = f"audio/{slide_id}.wav"
            audio_duration = get_audio_duration(wav_path)
        else:
            print(f"  ⚠️  No audio found for {slide_id}, using default duration")

        duration_in_frames = int(audio_duration * fps + 0.999) + padding_frames * 2

        slide_data = {
            "id": slide_id,
            "title": slide.get("title", ""),
            "text": slide["text"],
            "audioFile": audio_file,
            "audioDurationInSeconds": audio_duration,
            "durationInFrames": duration_in_frames,
        }

        # Include slide type if not default
        if slide_type in ("intro", "outro"):
            slide_data["type"] = slide_type

        slides.append(slide_data)

        type_tag = f" [{slide_type}]" if slide_type != "content" else ""
        suffix = f" ({audio_file})" if audio_file else " (no audio)"
        print(f"  {slide_id}{type_tag}: {audio_duration:.1f}s → {duration_in_frames} frames{suffix}")

    # Calculate total duration accounting for transitions
    transition_config = config["animation"]
    transition_frames = (
        transition_config.get("transitionDurationFrames", 0)
        if transition_config.get("transition", "none") != "none"
        else 0
    )
    total_frames = sum(s["durationInFrames"] for s in slides) - transition_frames * max(0, len(slides) - 1)

    render_props = {
        "slides": slides,
        "config": config,
    }

    os.makedirs(os.path.dirname(props_path), exist_ok=True)
    with open(props_path, "w", encoding="utf-8") as f:
        json.dump(render_props, f, indent=2, ensure_ascii=False)

    print(f"\n  ✅ Render props saved to: {props_path}")
    print(f"  📊 Total duration: {total_frames} frames ({total_frames / fps:.1f}s)")

    return total_frames


def run_remotion_render(
    config: dict,
    root: str,
    props_path: str,
    output_video: str,
) -> None:
    """Run the Remotion video render step."""
    print("\n🎬 Step 3: Rendering video with Remotion...\n")

    render_cmd = [
        "npx", "remotion", "render",
        "src/index.ts",
        "MainVideo",
        output_video,
        "--props", props_path,
        "--concurrency", str(config["video"].get("concurrency", 4)),
        "--log", "verbose",
    ]

    try:
        subprocess.run(render_cmd, check=True, cwd=root)
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Remotion render failed (exit code {e.returncode})")
        sys.exit(1)

    print(f"\n✅ Video rendered: {output_video}")

    # Print file size
    if os.path.exists(output_video):
        size_mb = os.path.getsize(output_video) / (1024 * 1024)
        print(f"   File size: {size_mb:.1f} MB")


def main():
    parser = argparse.ArgumentParser(
        description="Remotion Video Studio — Pipeline"
    )
    parser.add_argument(
        "--config", default="config/project.json",
        help="Path to project config JSON"
    )
    parser.add_argument(
        "--content", default="content/subtitles.json",
        help="Path to subtitles JSON file"
    )
    parser.add_argument(
        "--tts", default=None,
        help="TTS engine override: edge | qwen"
    )
    parser.add_argument(
        "--skip-tts", action="store_true",
        help="Skip TTS generation, use existing audio"
    )
    parser.add_argument(
        "--skip-render", action="store_true",
        help="Only generate TTS + props, no Remotion render"
    )
    parser.add_argument(
        "--no-normalize", action="store_true",
        help="Skip audio loudness normalization"
    )
    args = parser.parse_args()

    # Resolve paths relative to project root
    root = resolve_project_root()
    config, content, config_path, content_path = load_config_and_content(args, root)

    # --- Config & Content Validation ---
    print("\n🔍 Validating configuration...\n")
    config_errors = validate_config(config)
    content_errors = validate_content(content)
    all_errors = config_errors + content_errors

    if all_errors:
        print("❌ Validation failed:")
        for err in all_errors:
            print(f"   • {err}")
        sys.exit(1)
    else:
        print("  ✅ Configuration valid")

    # Resolve directory paths from config
    paths_config = config.get("paths", {})
    build_dir = os.path.join(root, paths_config.get("buildDir", "build"))
    props_path = os.path.join(build_dir, "render-props.json")
    output_video = os.path.join(build_dir, "video.mp4")
    audio_dir = os.path.join(root, paths_config.get("audioDir", "public/audio"))

    os.makedirs(build_dir, exist_ok=True)

    tts_engine = args.tts or config["tts"]["engine"]

    slides = content.get("slides", [])
    slide_types = {}
    for s in slides:
        t = s.get("type", "content")
        slide_types[t] = slide_types.get(t, 0) + 1

    print()
    print("=" * 60)
    print("  Remotion Video Studio — Pipeline")
    print("=" * 60)
    print(f"  TTS Engine : {'(skipped)' if args.skip_tts else tts_engine}")
    print(f"  Slides     : {len(slides)} ({', '.join(f'{v} {k}' for k, v in slide_types.items())})")
    print(f"  Resolution : {config['video']['width']}×{config['video']['height']}")
    print(f"  FPS        : {config['video']['fps']}")
    print(f"  BGM        : {'enabled' if config.get('bgm', {}).get('enabled') else 'disabled'}")
    print("=" * 60)

    # Step 0: TypeScript pre-check (catch compile errors before expensive TTS)
    if not args.skip_render:
        typecheck(root)

    # Step 1: TTS Generation
    if not args.skip_tts:
        run_tts(tts_engine, config, root, config_path, content_path)

        # Audio post-processing (optional)
        if not args.no_normalize:
            post_process_audio(audio_dir, slides)
    else:
        print("\n⏭️  Step 1: Skipping TTS generation (--skip-tts)\n")

    # Step 2: Generate render props
    generate_render_props(config, content, root, audio_dir, props_path)

    # Step 3: Remotion Render
    if not args.skip_render:
        run_remotion_render(config, root, props_path, output_video)
    else:
        print("\n⏭️  Step 3: Skipping render (--skip-render)")
        print(f"   To render manually: npm run render:props")

    print()
    print("=" * 60)
    print("  Pipeline complete! 🎉")
    print("=" * 60)
    print()


if __name__ == "__main__":
    main()
