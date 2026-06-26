import argparse
import json
import subprocess
import os
import sys


def get_video_info(input_path):
    """Get video duration, resolution, and check for audio stream."""
    cmd = [
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration:stream=codec_type,width,height",
        "-of", "json", input_path
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception(f"ffprobe failed: {result.stderr}")

    data = json.loads(result.stdout)
    duration = float(data.get('format', {}).get('duration', 0))
    has_audio = any(s.get('codec_type') == 'audio' for s in data.get('streams', []))
    width = None
    height = None
    for s in data.get('streams', []):
        if s.get('codec_type') == 'video':
            width = s.get('width')
            height = s.get('height')
            break
    return duration, has_audio, width, height


def find_sfx_file(sfx_dir, sfx_type):
    """Find SFX file in directory with common extensions."""
    if not sfx_dir or not os.path.isdir(sfx_dir):
        return None
    extensions = ['.mp3', '.wav', '.m4a', '.ogg', '.flac']
    for ext in extensions:
        path = os.path.join(sfx_dir, f"{sfx_type}{ext}")
        if os.path.exists(path):
            return path
        path = os.path.join(sfx_dir, f"{sfx_type.lower()}{ext}")
        if os.path.exists(path):
            return path
    return None


def escape_ass_path(path):
    """Escape path for ffmpeg ass filter."""
    return path.replace("\\", "\\\\").replace("'", "\\'").replace(":", "\\:")


def main():
    parser = argparse.ArgumentParser(description="Render video with subtitles, BGM, and SFX")
    parser.add_argument("--input", required=True, help="Input video path")
    parser.add_argument("--subtitles", required=True, help="ASS subtitle file path")
    parser.add_argument("--plan", required=True, help="Production plan JSON path")
    parser.add_argument("--bgm", help="BGM audio file path")
    parser.add_argument("--sfx-dir", help="SFX directory")
    parser.add_argument("--output", required=True, help="Output video path")
    parser.add_argument("--resolution", default=None,
                        help="Output resolution WxH (e.g. 720x1280). If omitted, keep original.")
    parser.add_argument("--bgm-volume", type=float, default=-18.0, help="BGM volume in dB")
    parser.add_argument("--sfx-volume", type=float, default=-6.0, help="SFX volume in dB")

    args = parser.parse_args()

    for path, name in [(args.input, "Input video"), (args.subtitles, "Subtitle file"), (args.plan, "Production plan")]:
        if not os.path.exists(path):
            print(f"Error: {name} not found: {path}")
            sys.exit(1)

    print("--- Starting Render Process ---")
    print(f"Input: {args.input}")
    print(f"Output: {args.output}")

    # 1. Get Video Info
    try:
        duration, has_video_audio, orig_w, orig_h = get_video_info(args.input)
        print(f"Video: {orig_w}x{orig_h}, duration: {duration:.2f}s, audio: {'Yes' if has_video_audio else 'No'}")
    except Exception as e:
        print(f"Error getting video info: {e}")
        sys.exit(1)

    # 2. Load Production Plan
    with open(args.plan, 'r') as f:
        plan = json.load(f)

    sfx_list = plan.get('sfx', [])
    bgm_config = plan.get('bgm', {})
    bgm_vol = bgm_config.get('volume', args.bgm_volume)

    # Detect rotation from input video
    rotation = 0
    try:
        rot_cmd = [
            "ffprobe", "-v", "error",
            "-select_streams", "v:0",
            "-show_entries", "stream_side_data=rotation",
            "-of", "csv=p=0", args.input
        ]
        rot_result = subprocess.run(rot_cmd, capture_output=True, text=True)
        rot_str = rot_result.stdout.strip()
        if rot_str:
            rotation = int(float(rot_str))
            print(f"Detected rotation: {rotation}°")
    except Exception:
        pass

    # 3. Build FFmpeg Command
    ffmpeg_cmd = ["ffmpeg", "-y", "-hide_banner"]
    if rotation != 0:
        ffmpeg_cmd.append("-noautorotate")

    # Input 0: Video
    ffmpeg_cmd.extend(["-i", args.input])
    input_count = 1
    bgm_idx = -1
    sfx_inputs = []  # list of (input_index, delay_ms)

    # Input 1: BGM (optional)
    if args.bgm and os.path.exists(args.bgm):
        ffmpeg_cmd.extend(["-stream_loop", "-1", "-i", args.bgm])
        bgm_idx = input_count
        input_count += 1
        print(f"BGM: {args.bgm} (Vol: {bgm_vol}dB)")
    elif args.bgm:
        print(f"Warning: BGM file not found: {args.bgm}")

    # Inputs 2+: SFX — deduplicate files, reuse same input for same file
    sfx_file_to_idx = {}
    for sfx in sfx_list:
        sfx_path = find_sfx_file(args.sfx_dir, sfx['type'])
        if sfx_path:
            if sfx_path not in sfx_file_to_idx:
                ffmpeg_cmd.extend(["-i", sfx_path])
                sfx_file_to_idx[sfx_path] = input_count
                input_count += 1
            delay_ms = int(sfx['time'] * 1000)
            sfx_inputs.append((sfx_file_to_idx[sfx_path], delay_ms, sfx['type']))
            print(f"SFX: {sfx['type']} at {sfx['time']}s")
        else:
            print(f"Warning: SFX file not found for type '{sfx['type']}'")

    # 4. Build filter_complex
    filter_parts = []

    # Video filter: handle rotation + optional scale + ASS subtitles
    esc_sub = escape_ass_path(os.path.abspath(args.subtitles))

    # Build video filter chain
    vf_chain = []

    # Apply rotation manually if -noautorotate was used
    if rotation == -90 or rotation == 270:
        vf_chain.append("transpose=1")  # 90° clockwise
    elif rotation == 90 or rotation == -270:
        vf_chain.append("transpose=2")  # 90° counter-clockwise
    elif rotation == 180 or rotation == -180:
        vf_chain.append("transpose=1,transpose=1")  # 180°

    if args.resolution:
        res_w, res_h = args.resolution.split('x')
        vf_chain.append(f"scale={res_w}:{res_h}:force_original_aspect_ratio=increase,crop={res_w}:{res_h}")

    vf_chain.append(f"ass=filename='{esc_sub}'")

    v_filter = f"[0:v]{','.join(vf_chain)}[v_out]"
    filter_parts.append(v_filter)

    # Audio mixing
    audio_labels = []

    # Original audio
    if has_video_audio:
        filter_parts.append("[0:a]acopy[orig_a]")
        audio_labels.append("[orig_a]")
    else:
        filter_parts.append(f"anullsrc=channel_layout=stereo:sample_rate=44100,atrim=end={duration}[orig_a]")
        audio_labels.append("[orig_a]")

    # BGM
    if bgm_idx != -1:
        fade_out_start = max(0, duration - 3)
        bgm_filter = (f"[{bgm_idx}:a]atrim=end={duration},"
                      f"volume={bgm_vol}dB,"
                      f"afade=t=in:st=0:d=2,"
                      f"afade=t=out:st={fade_out_start:.2f}:d=3[bgm_out]")
        filter_parts.append(bgm_filter)
        audio_labels.append("[bgm_out]")

    # SFX — each gets its own delayed copy
    for i, (idx, delay_ms, sfx_type) in enumerate(sfx_inputs):
        label = f"sfx{i}"
        # Use adelay to position the SFX at the right time
        # Pad the SFX to full duration so amix works correctly
        sfx_filter = (f"[{idx}:a]volume={args.sfx_volume}dB,"
                      f"adelay={delay_ms}|{delay_ms},"
                      f"apad=whole_dur={duration}[{label}]")
        filter_parts.append(sfx_filter)
        audio_labels.append(f"[{label}]")

    # Mix all audio tracks
    n_audio = len(audio_labels)
    if n_audio == 1:
        # Only original audio, just pass through
        mix_filter = f"{audio_labels[0]}acopy[a_out]"
        filter_parts.append(mix_filter)
    else:
        # Use amix with normalize=0 to prevent automatic volume reduction
        # Then apply dynaudnorm to bring levels back to normal
        labels_str = "".join(audio_labels)
        # Weights: original voice=1, others based on their pre-set volume
        mix_filter = (f"{labels_str}amix=inputs={n_audio}:"
                      f"duration=first:dropout_transition=0:normalize=0,"
                      f"dynaudnorm=p=0.95:s=5[a_out]")
        filter_parts.append(mix_filter)

    ffmpeg_cmd.extend(["-filter_complex", ";".join(filter_parts)])

    # Output settings
    ffmpeg_cmd.extend([
        "-map", "[v_out]",
        "-map", "[a_out]",
        "-c:v", "libx264",
        "-preset", "medium",
        "-crf", "20",
        "-c:a", "aac",
        "-ar", "44100",
        "-ac", "2",
        "-shortest",
        "-metadata:s:v:0", "rotate=0",  # Clear rotation metadata
        args.output
    ])

    # Print full command for debugging
    cmd_str = " ".join(f'"{c}"' if " " in c else c for c in ffmpeg_cmd)
    print(f"\nFFmpeg command:\n{cmd_str}\n")

    print("Executing FFmpeg...")
    try:
        process = subprocess.Popen(
            ffmpeg_cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True
        )

        for line in process.stdout:
            if "frame=" in line or "time=" in line:
                print(f"\rProgress: {line.strip()}", end="")
            elif "Error" in line or "error" in line:
                print(f"\n{line.strip()}")

        process.wait()
        print("\nFFmpeg process finished.")

        if process.returncode != 0:
            print(f"Error: FFmpeg failed with return code {process.returncode}")
            sys.exit(process.returncode)

    except KeyboardInterrupt:
        process.kill()
        print("\nProcess interrupted.")
        sys.exit(1)
    except Exception as e:
        print(f"Error executing FFmpeg: {e}")
        sys.exit(1)

    # 5. Verify
    if os.path.exists(args.output):
        size = os.path.getsize(args.output)
        if size > 1000:
            print(f"Success! Output saved to: {args.output} ({size / 1024 / 1024:.2f} MB)")
        else:
            print(f"Warning: Output file seems too small ({size} bytes).")
    else:
        print("Error: Output file was not created.")
        sys.exit(1)


if __name__ == "__main__":
    main()
