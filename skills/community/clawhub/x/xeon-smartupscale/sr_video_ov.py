import openvino as ov
import cv2
import numpy as np
import os
import sys
import time
import subprocess
import argparse
import tempfile
import shutil

# ---------------------------
# 项目内置 ffmpeg 路径
# ---------------------------
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
FFMPEG_BIN = os.path.join(SCRIPT_DIR, 'bin', 'ffmpeg')
FFPROBE_BIN = os.path.join(SCRIPT_DIR, 'bin', 'ffprobe')



def get_video_info(video_path):
    """用 ffprobe 获取视频信息"""
    import json
    cmd = [
        FFPROBE_BIN, '-v', 'quiet',
        '-print_format', 'json',
        '-show_streams', '-show_format',
        video_path
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"ffprobe failed: {result.stderr}")

    info = json.loads(result.stdout)
    video_stream = None
    for stream in info['streams']:
        if stream['codec_type'] == 'video':
            video_stream = stream
            break
    if video_stream is None:
        raise RuntimeError("No video stream found")

    width = int(video_stream['width'])
    height = int(video_stream['height'])
    r_frame_rate = video_stream.get('r_frame_rate', '30/1')
    num, den = map(int, r_frame_rate.split('/'))
    fps = num / den
    has_audio = any(s['codec_type'] == 'audio' for s in info['streams'])
    return width, height, fps, has_audio


def main():
    parser = argparse.ArgumentParser(description='ETDS Video 2x Super-Resolution (OpenVINO)')
    parser.add_argument('input', help='Input video path')
    parser.add_argument('-o', '--output', help='Output video path (default: input_sr2x_ov.mp4)')
    parser.add_argument('--model', default=os.path.join(SCRIPT_DIR, 'model', 'ETDS_M7C48_x2.xml'),
                        help='OpenVINO IR model path (.xml)')
    parser.add_argument('--scale', type=int, default=2, help='Scale factor (default: 2)')
    parser.add_argument('--device', default='CPU', help='OpenVINO device (default: CPU)')
    parser.add_argument('--nthreads', type=int, default=0, help='Number of inference threads (0=auto)')
    args = parser.parse_args()

    input_video = args.input
    if not os.path.isfile(input_video):
        print(f"Error: input video not found: {input_video}")
        sys.exit(1)

    if args.output:
        output_video = args.output
    else:
        base, ext = os.path.splitext(input_video)
        output_video = f"{base}_sr{args.scale}x_ov.mp4"

    if not os.path.isfile(FFMPEG_BIN):
        print(f"Error: ffmpeg not found: {FFMPEG_BIN}")
        sys.exit(1)

    # 获取视频信息
    print(f"Analyzing input: {input_video}")
    width, height, fps, has_audio = get_video_info(input_video)
    out_w, out_h = width * args.scale, height * args.scale
    print(f"Input:  {width}x{height}, {fps:.2f} fps, audio: {'yes' if has_audio else 'no'}")
    print(f"Output: {out_w}x{out_h}")

    # 加载 OpenVINO 模型
    print(f"Loading OpenVINO model: {args.model}")
    core = ov.Core()
    if args.nthreads > 0:
        core.set_property("CPU", {"INFERENCE_NUM_THREADS": args.nthreads})

    model = core.read_model(args.model)
    # 使用固定输入shape以获得最佳性能
    model.reshape({0: [1, 3, height, width]})
    compiled = core.compile_model(model, args.device)
    infer_request = compiled.create_infer_request()
    print(f"Model loaded on {args.device}")

    # Warmup
    dummy = np.random.rand(1, 3, height, width).astype(np.float32)
    infer_request.infer({0: dummy})
    print("Warmup done")

    tmp_dir = tempfile.mkdtemp()
    tmp_video = os.path.join(tmp_dir, 'sr_video_noaudio.mp4')

    try:
        cap = cv2.VideoCapture(input_video)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        print(f"Total frames: {total_frames}")

        ffmpeg_cmd = [
            FFMPEG_BIN, '-y',
            '-f', 'rawvideo', '-vcodec', 'rawvideo',
            '-s', f'{out_w}x{out_h}',
            '-pix_fmt', 'bgr24', '-r', str(fps),
            '-i', '-',
            '-c:v', 'libx264', '-preset', 'medium',
            '-crf', '18', '-pix_fmt', 'yuv420p',
            tmp_video
        ]
        pipe = subprocess.Popen(ffmpeg_cmd, stdin=subprocess.PIPE, stderr=subprocess.PIPE)

        frame_idx = 0
        total_infer_time = 0
        start_time = time.time()

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # 预处理: BGR -> RGB -> float32 -> NCHW
            img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB).astype(np.float32) / 255.0
            img_tensor = np.transpose(img, (2, 0, 1))[np.newaxis, ...]

            # OpenVINO 推理
            t0 = time.time()
            infer_request.infer({0: img_tensor})
            result = infer_request.get_output_tensor(0).data.copy()
            t1 = time.time()
            total_infer_time += (t1 - t0)

            # 后处理: NCHW -> HWC -> uint8 -> RGB -> BGR
            output = result.squeeze(0).transpose(1, 2, 0)
            output = np.clip(output, 0, 1) * 255.0
            output = output.astype(np.uint8)
            output = cv2.cvtColor(output, cv2.COLOR_RGB2BGR)

            pipe.stdin.write(output.tobytes())
            frame_idx += 1

            if frame_idx % 10 == 0 or frame_idx == total_frames:
                elapsed = time.time() - start_time
                fps_proc = frame_idx / elapsed if elapsed > 0 else 0
                infer_fps = frame_idx / total_infer_time if total_infer_time > 0 else 0
                print(f"\rProgress: {frame_idx}/{total_frames} "
                      f"({frame_idx * 100 / max(total_frames, 1):.1f}%) "
                      f"total: {fps_proc:.2f} fps, infer: {infer_fps:.2f} fps", end='', flush=True)

        pipe.stdin.close()
        pipe.wait()
        cap.release()
        print()

        total_time = time.time() - start_time
        print(f"Done! {frame_idx} frames in {total_time:.2f}s")
        print(f"  Total pipeline: {frame_idx / total_time:.2f} fps")
        print(f"  Pure inference: {frame_idx / total_infer_time:.2f} fps ({total_infer_time:.2f}s)")
        print(f"  Avg infer/frame: {total_infer_time / frame_idx * 1000:.1f} ms")

        if has_audio:
            print("Merging audio...")
            merge_cmd = [
                FFMPEG_BIN, '-y',
                '-i', tmp_video, '-i', input_video,
                '-c:v', 'copy', '-c:a', 'aac',
                '-map', '0:v:0', '-map', '1:a:0',
                '-shortest', output_video
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


if __name__ == '__main__':
    main()
