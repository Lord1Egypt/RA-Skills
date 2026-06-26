#!/usr/bin/env python3
"""
RealSense D435i Capture Script
Supports: depth photo, point cloud, IMU data, RGBD video

默认输出到 data/ 目录（相对于脚本所在目录）。
可通过 --output 指定其他路径。

Usage:
  python3 scripts/realsense_capture.py --mode depth
  python3 scripts/realsense_capture.py --mode pointcloud
  python3 scripts/realsense_capture.py --mode imu --duration 5
  python3 scripts/realsense_capture.py --mode rgbd --duration 5 --fps 30
"""

import argparse, csv, os, subprocess, sys, time
from datetime import datetime
import cv2, numpy as np, pyrealsense2 as rs

# ── 默认路径：data/ 在脚本同目录下 ─────────────────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_OUTPUT = os.path.join(SCRIPT_DIR, "data")

def parse_args():
    p = argparse.ArgumentParser(description="RealSense D435i Capture")
    p.add_argument("--mode", required=True,
                   choices=["depth", "pointcloud", "imu", "rgbd"])
    p.add_argument("--output", default=DEFAULT_OUTPUT,
                   help=f"Output directory (default: {DEFAULT_OUTPUT})")
    p.add_argument("--duration", type=int, default=5,
                   help="Recording duration in seconds (default: 5)")
    p.add_argument("--fps", type=int, default=30,
                   help="Frame rate (default: 30)")
    return p.parse_args()

def today(): return datetime.now().strftime("%Y-%m-%d")

def out_path(prefix, ext, subdir):
    """Build output path: output/type/YYYY-MM-DD/prefix_timestamp.ext"""
    base = os.path.join(args.output, subdir, today())
    os.makedirs(base, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    return os.path.join(base, f"{prefix}_{ts}.{ext}")

# ── Depth photo ──────────────────────────────────────────────────────────────
def capture_depth(args):
    """Depth + aligned RGB at 640x480 (USB 2.1 safe)."""
    print("[Depth] Starting pipeline...")
    pipe = rs.pipeline()
    cfg = rs.config()
    cfg.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
    cfg.enable_stream(rs.stream.color, 640, 480, rs.format.rgb8, 30)
    pipe.start()
    align = rs.align(rs.stream.color)

    time.sleep(2)
    print("[Depth] Capturing...")
    frames = pipe.wait_for_frames(15000)
    af = align.process(frames)
    df, cf = af.get_depth_frame(), af.get_color_frame()
    if not df or not cf:
        print("[Depth] ERROR: no frames"); pipe.stop(); return

    colorizer = rs.colorizer()
    dc = np.asanyarray(colorizer.colorize(df).get_data())
    rgb = np.asanyarray(cf.get_data())

    cv2.imwrite(out_path("rgb", "jpg", "photos/rgb"),
                cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR))
    cv2.imwrite(out_path("depth_colorized", "jpg", "photos/depth"),
                cv2.cvtColor(dc, cv2.COLOR_RGB2BGR))
    cv2.imwrite(out_path("depth_raw", "png", "photos/depth"),
                np.asanyarray(df.get_data()))
    pipe.stop()
    print("[Depth] Done.")

# ── Point cloud ──────────────────────────────────────────────────────────────
def capture_pointcloud(args):
    """PLY point cloud (xyz only, no texture)."""
    print("[PointCloud] Trying rs-pointcloud utility...")
    ply_path = out_path("pointcloud", "ply", "pointcloud")
    try:
        r = subprocess.run(["rs-pointcloud", "--output", ply_path,
                            "--format", "ply"],
                           capture_output=True, text=True, timeout=5)
        if r.returncode == 0:
            print(f"[PointCloud] Saved (rs-pointcloud): {ply_path}")
            return
    except FileNotFoundError:
        print("[PointCloud] rs-pointcloud not found")
    except subprocess.TimeoutExpired:
        print("[PointCloud] rs-pointcloud timed out")

    print("[PointCloud] Using SDK fallback (depth-only)...")
    try:
        pipe = rs.pipeline()
        cfg = rs.config()
        cfg.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
        pipe.start()
        time.sleep(2)
        frames = pipe.wait_for_frames(15000)
        df = frames.get_depth_frame()
        pc = rs.pointcloud()
        pts = pc.calculate(df)
        flat = np.frombuffer(pts.get_vertices(), dtype=np.float32)
        xyz = flat.reshape(len(flat) // 3, 3).astype(np.float64)
        xyz = xyz[xyz[:, 2] > 0]
        pipe.stop()

        with open(ply_path, "w") as f:
            f.write("ply\nformat ascii 1.0\n")
            f.write(f"element vertex {len(xyz)}\n")
            f.write("property float x\nproperty float y\nproperty float z\n")
            f.write("end_header\n")
            for pt in xyz:
                f.write(f"{pt[0]:.6f} {pt[1]:.6f} {pt[2]:.6f}\n")
        print(f"[PointCloud] Saved: {ply_path} ({len(xyz)} pts)")
    except Exception as e:
        print(f"[PointCloud] SDK fallback failed: {e}")
        return
    print("[PointCloud] Done. Open with MeshLab / CloudCompare.")

# ── IMU ──────────────────────────────────────────────────────────────────────
def capture_imu(args):
    """Accel + Gyro data to CSV."""
    print(f"[IMU] Recording {args.duration}s @ accel 200Hz + gyro 200Hz...")
    pipe = rs.pipeline()
    cfg = rs.config()
    cfg.enable_stream(rs.stream.accel, rs.format.motion_xyz32f, 200)
    cfg.enable_stream(rs.stream.gyro,  rs.format.motion_xyz32f, 200)
    pipe.start()

    accel, gyro = [], []
    t0 = time.time()
    while time.time() - t0 < args.duration:
        try:
            frames = pipe.wait_for_frames(500)
            for f in frames:
                if not f.is_motion_frame(): continue
                d = np.asanyarray(f.as_motion_frame().get_motion_data())
                row = [f.get_timestamp()] + d.tolist()
                sn = f.profile.stream_name()
                (accel if "Accel" in sn else gyro).append(row + [sn.split()[0]])
        except Exception: pass

    csv_path = out_path("imu", "csv", "imu")
    with open(csv_path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["timestamp", "x", "y", "z", "type"])
        w.writerows(accel); w.writerows(gyro)
    pipe.stop()
    print(f"[IMU] Saved: {csv_path}")
    print(f"[IMU] Accel: {len(accel)} samples, Gyro: {len(gyro)} samples")

# ── RGBD video ────────────────────────────────────────────────────────────────
def capture_rgbd(args):
    """Synchronized RGB + Depth video at 640x480.
    Uses ffmpeg for reliable encoding.
    """
    print(f"[RGBD] Recording {args.duration}s @ {args.fps}fps...")
    pipe = rs.pipeline()
    cfg = rs.config()
    cfg.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, args.fps)
    cfg.enable_stream(rs.stream.color, 640, 480, rs.format.rgb8,  args.fps)
    pipe.start()
    align = rs.align(rs.stream.color)
    colorizer = rs.colorizer()

    rgb_dir = out_path("rgb", "mp4", "videos/rgb").rsplit("/", 1)[0]
    depth_dir = out_path("depth", "mp4", "videos/depth").rsplit("/", 1)[0]
    os.makedirs(rgb_dir, exist_ok=True)
    os.makedirs(depth_dir, exist_ok=True)

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    rgb_list = f"{rgb_dir}/rgb_frames_{ts}.txt"
    depth_list = f"{depth_dir}/depth_frames_{ts}.txt"
    rgb_frames, depth_frames = [], []

    t0 = time.time()
    while time.time() - t0 < args.duration:
        frames = pipe.wait_for_frames(1000)
        if not frames: continue
        af = align.process(frames)
        df, cf = af.get_depth_frame(), af.get_color_frame()
        if not df or not cf: continue

        c = np.asanyarray(cf.get_data())
        rgb_fp = f"{rgb_dir}/rgb_{ts}_{len(rgb_frames):04d}.jpg"
        cv2.imwrite(rgb_fp, cv2.cvtColor(c, cv2.COLOR_RGB2BGR))
        rgb_frames.append(rgb_fp)

        d = np.asanyarray(colorizer.colorize(df).get_data())
        d = np.clip(d, 0, 255).astype(np.uint8)
        depth_fp = f"{depth_dir}/depth_{ts}_{len(depth_frames):04d}.jpg"
        cv2.imwrite(depth_fp, cv2.cvtColor(d, cv2.COLOR_RGB2BGR))
        depth_frames.append(depth_fp)

    pipe.stop()

    rgb_out = f"{rgb_dir}/rgb_{ts}.mp4"
    depth_out = f"{depth_dir}/depth_{ts}.mp4"

    with open(rgb_list, "w") as f:
        for fp in rgb_frames: f.write(f"file '{fp}'\n")
    subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", rgb_list,
                   "-c:v", "libx264", "-preset", "ultrafast", "-crf", "23", rgb_out],
                  capture_output=True)

    with open(depth_list, "w") as f:
        for fp in depth_frames: f.write(f"file '{fp}'\n")
    subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", depth_list,
                   "-c:v", "libx264", "-preset", "ultrafast", "-crf", "23", depth_out],
                  capture_output=True)

    for fp in rgb_frames + depth_frames + [rgb_list, depth_list]:
        os.remove(fp)

    print(f"[RGBD] {len(rgb_frames)} frames → {rgb_out}")
    print(f"[RGBD] {len(depth_frames)} frames → {depth_out}")

# ── main ─────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    args = parse_args()
    print(f"[RealSense D435i] Output: {args.output}")
    modes = dict(depth=capture_depth, pointcloud=capture_pointcloud,
                 imu=capture_imu, rgbd=capture_rgbd)
    try:
        modes[args.mode](args)
    except KeyboardInterrupt:
        print("\nInterrupted."); sys.exit(1)
    except Exception as e:
        import traceback; traceback.print_exc(); sys.exit(1)
