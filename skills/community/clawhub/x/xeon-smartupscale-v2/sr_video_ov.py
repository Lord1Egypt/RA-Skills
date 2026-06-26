#!/usr/bin/env python3

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time

import cv2
import numpy as np
import openvino as ov

try:
    import cpuinfo
except Exception:
    cpuinfo = None


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
FFMPEG_BIN = os.path.join(SCRIPT_DIR, "bin", "ffmpeg")
FFPROBE_BIN = os.path.join(SCRIPT_DIR, "bin", "ffprobe")


def resolve_infer_precision_hint():
    amx_bf16 = False
    amx_f16 = False
    brand_raw = ""
    flags = set()
    sources = []

    if cpuinfo is not None:
        try:
            info = cpuinfo.get_cpu_info() or {}
            brand_raw = str(info.get("brand_raw", ""))
            flags.update(info.get("flags", []))
            sources.append("py-cpuinfo")
        except Exception:
            pass

    try:
        with open("/proc/cpuinfo", "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                l = line.lower()
                if l.startswith("flags") and ":" in line:
                    flags.update(line.split(":", 1)[1].strip().split())
                elif not brand_raw and l.startswith("model name") and ":" in line:
                    brand_raw = line.split(":", 1)[1].strip()
        sources.append("/proc/cpuinfo")
    except Exception:
        pass

    try:
        out = subprocess.check_output(["lscpu"], text=True, stderr=subprocess.DEVNULL)
        for line in out.splitlines():
            if line.startswith("Flags:") and ":" in line:
                flags.update(line.split(":", 1)[1].strip().split())
            elif not brand_raw and line.startswith("Model name:") and ":" in line:
                brand_raw = line.split(":", 1)[1].strip()
        sources.append("lscpu")
    except Exception:
        pass

    amx_bf16 = "amx_bf16" in flags
    amx_f16 = "amx_fp16" in flags or "amx_f16" in flags

    if not (amx_bf16 or amx_f16):
        try:
            core = ov.Core()
            caps = core.get_property("CPU", "OPTIMIZATION_CAPABILITIES")
            caps_l = {str(c).lower() for c in caps}
            if "amx" in caps_l or "amx_bf16" in caps_l:
                amx_bf16 = True
                sources.append("openvino-caps")
        except Exception:
            pass

    force_mode = int(os.environ.get("INTEL_FORCE_AMX", "0"))
    if force_mode == 1:
        amx_bf16 = True
    elif force_mode == 2:
        amx_bf16 = False
        amx_f16 = False

    infer_type = "bf16" if (amx_bf16 or amx_f16) else "f32"
    detect_msg = (
        f"CPU detect: brand='{brand_raw or 'unknown'}' "
        f"amx_bf16={'yes' if amx_bf16 else 'no'} "
        f"amx_f16={'yes' if amx_f16 else 'no'} "
        f"sources={','.join(sources) if sources else 'none'} "
        f"INTEL_FORCE_AMX={force_mode}"
    )
    return infer_type, detect_msg


def get_video_info(video_path):
    cmd = [
        FFPROBE_BIN,
        "-v",
        "quiet",
        "-print_format",
        "json",
        "-show_streams",
        "-show_format",
        video_path,
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"ffprobe failed: {result.stderr}")

    info = json.loads(result.stdout)
    video_stream = next((stream for stream in info["streams"] if stream["codec_type"] == "video"), None)
    if video_stream is None:
        raise RuntimeError("No video stream found")

    width = int(video_stream["width"])
    height = int(video_stream["height"])
    r_frame_rate = video_stream.get("r_frame_rate", "30/1")
    num, den = map(int, r_frame_rate.split("/"))
    fps = num / den
    has_audio = any(stream["codec_type"] == "audio" for stream in info["streams"])
    return width, height, fps, has_audio


def main():
    parser = argparse.ArgumentParser(description="Real-ESRGAN general-x4v3 video super-resolution (OpenVINO)")
    parser.add_argument("input", help="Input video path")
    parser.add_argument("-o", "--output", help="Output video path")
    parser.add_argument(
        "--model",
        default=os.path.join(SCRIPT_DIR, "model", "realesr-general-x4v3_480x270.xml"),
        help="OpenVINO IR model path (.xml)",
    )
    parser.add_argument("--scale", type=int, default=4, help="Scale factor (default: 4)")
    parser.add_argument("--device", default="CPU", help="OpenVINO device (default: CPU)")
    parser.add_argument("--nthreads", type=int, default=0, help="Number of inference threads (0=auto)")
    parser.add_argument("--prescale-width", type=int, help="Optional in-memory Lanczos width before inference")
    parser.add_argument("--prescale-height", type=int, help="Optional in-memory Lanczos height before inference")
    args = parser.parse_args()

    input_video = args.input
    if not os.path.isfile(input_video):
        print(f"Error: input video not found: {input_video}")
        sys.exit(1)

    output_video = args.output or f"{os.path.splitext(input_video)[0]}_sr{args.scale}x_ov.mp4"

    if not os.path.isfile(FFMPEG_BIN) or not os.path.isfile(FFPROBE_BIN):
        print("Error: ffmpeg/ffprobe not found in repo bin/. Run install.sh first.")
        sys.exit(1)

    print(f"Analyzing input: {input_video}")
    width, height, fps, has_audio = get_video_info(input_video)
    infer_w = args.prescale_width or width
    infer_h = args.prescale_height or height
    out_w, out_h = infer_w * args.scale, infer_h * args.scale
    print(f"Source: {width}x{height}, {fps:.2f} fps, audio: {'yes' if has_audio else 'no'}")
    if infer_w != width or infer_h != height:
        print(f"Pre-scale: in-memory lanczos -> {infer_w}x{infer_h}")
    else:
        print(f"Pre-scale: skipped, model input stays at {infer_w}x{infer_h}")
    print(f"Input:  {infer_w}x{infer_h}")
    print(f"Output: {out_w}x{out_h}")
    print(f"Loading OpenVINO model: {args.model}")

    core = ov.Core()
    if args.nthreads > 0:
        core.set_property("CPU", {"INFERENCE_NUM_THREADS": args.nthreads})

    infer_type, detect_msg = resolve_infer_precision_hint()

    compile_config = {
        "PERFORMANCE_HINT": os.environ.get("OV_REALX4_PERFORMANCE_HINT", "LATENCY"),
        "INFERENCE_PRECISION_HINT": os.environ.get("OV_REALX4_PRECISION_HINT", infer_type),
    }

    model = core.read_model(args.model)
    model.reshape({0: [1, 3, infer_h, infer_w]})
    compiled = core.compile_model(model, args.device, compile_config)
    infer_request = compiled.create_infer_request()
    input_port = compiled.input(0)
    print(detect_msg)
    print(f"Model loaded on {args.device}")
    print(
        "OpenVINO config: "
        f"precision={compile_config['INFERENCE_PRECISION_HINT']} "
        f"performance={compile_config['PERFORMANCE_HINT']}"
    )

    dummy = np.zeros((1, 3, infer_h, infer_w), dtype=np.float32)
    infer_request.infer({input_port: dummy})
    print("Warmup done")

    tmp_dir = tempfile.mkdtemp()
    tmp_video = os.path.join(tmp_dir, "sr_video_noaudio.mp4")

    try:
        cap = cv2.VideoCapture(input_video)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        print(f"Total frames: {total_frames}")

        encode_preset = os.environ.get("OV_REALX4_PRESET", "medium")
        encode_crf = os.environ.get("OV_REALX4_CRF", "15")
        print(f"Encoder: libx264 preset={encode_preset} crf={encode_crf}")

        ffmpeg_cmd = [
            FFMPEG_BIN,
            "-y",
            "-f",
            "rawvideo",
            "-vcodec",
            "rawvideo",
            "-s",
            f"{out_w}x{out_h}",
            "-pix_fmt",
            "bgr24",
            "-r",
            str(fps),
            "-i",
            "-",
            "-c:v",
            "libx264",
            "-preset",
            encode_preset,
            "-crf",
            encode_crf,
            "-pix_fmt",
            "yuv420p",
            tmp_video,
        ]
        pipe = subprocess.Popen(ffmpeg_cmd, stdin=subprocess.PIPE, stderr=subprocess.DEVNULL)

        frame_idx = 0
        total_infer_time = 0.0
        start_time = time.time()

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            if frame.shape[1] != infer_w or frame.shape[0] != infer_h:
                frame = cv2.resize(frame, (infer_w, infer_h), interpolation=cv2.INTER_LANCZOS4)

            img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB).astype(np.float32) / 255.0
            img_tensor = np.transpose(img, (2, 0, 1))[np.newaxis, ...]

            t0 = time.time()
            infer_request.infer({input_port: img_tensor})
            result = infer_request.get_output_tensor(0).data.copy()
            t1 = time.time()
            total_infer_time += t1 - t0

            output = result.squeeze(0).transpose(1, 2, 0)
            output = np.clip(output, 0, 1) * 255.0
            output = output.astype(np.uint8)
            output = cv2.cvtColor(output, cv2.COLOR_RGB2BGR)

            pipe.stdin.write(output.tobytes())
            frame_idx += 1

            if frame_idx % 10 == 0 or frame_idx == total_frames:
                elapsed = time.time() - start_time
                fps_proc = frame_idx / elapsed if elapsed > 0 else 0.0
                infer_fps = frame_idx / total_infer_time if total_infer_time > 0 else 0.0
                print(
                    f"\rProgress: {frame_idx}/{total_frames} "
                    f"({frame_idx * 100 / max(total_frames, 1):.1f}%) "
                    f"total: {fps_proc:.2f} fps, infer: {infer_fps:.2f} fps",
                    end="",
                    flush=True,
                )

        if pipe.stdin is not None:
            pipe.stdin.close()
        pipe.wait()
        cap.release()
        print()

        total_time = time.time() - start_time
        print(f"Done! {frame_idx} frames in {total_time:.2f}s")
        if frame_idx > 0:
            print(f"  Total pipeline: {frame_idx / total_time:.2f} fps")
            print(f"  Pure inference: {frame_idx / total_infer_time:.2f} fps ({total_infer_time:.2f}s)")
            print(f"  Avg infer/frame: {total_infer_time / frame_idx * 1000:.1f} ms")

        if has_audio:
            print("Merging audio...")
            merge_cmd = [
                FFMPEG_BIN,
                "-y",
                "-i",
                tmp_video,
                "-i",
                input_video,
                "-c:v",
                "copy",
                "-c:a",
                "copy",
                "-map",
                "0:v:0",
                "-map",
                "1:a:0?",
                "-shortest",
                output_video,
            ]
            result = subprocess.run(merge_cmd, capture_output=True, text=True)
            if result.returncode != 0:
                print(f"Audio merge warning: {result.stderr}")
                shutil.copy2(tmp_video, output_video)
        else:
            shutil.copy2(tmp_video, output_video)

        print(f"Saved: {output_video}")

    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)


if __name__ == "__main__":
    main()
