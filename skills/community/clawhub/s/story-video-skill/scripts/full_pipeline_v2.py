#!/usr/bin/env python3
"""
full_pipeline_v2.py — MiniMax T2I→I2V 全自动流水线（支持 I2V 重试）
与 full_pipeline.py 的区别：I2V 失败时会自动用脱敏 prompt 重试一次。
用法：
    export MINIMAX_API_KEY="your_key"
    export MINIMAX_BASE_URL="https://api.minimaxi.com/v1"  # 可选
    python full_pipeline_v2.py -i shots.json [-o output.mp4]
"""
import os, sys, json, time, requests, subprocess
from pathlib import Path
from argparse import ArgumentParser

# ── Config ──────────────────────────────────────────────────────────────────
BASE = os.environ.get("MINIMAX_BASE_URL", "https://api.minimaxi.com/v1")
T2I_URL  = f"{BASE}/image_generation"
I2V_URL  = f"{BASE}/video_generation"
POLL_URL = f"{BASE}/query/video_generation"
RETRIEVE_URL = f"{BASE}/files/retrieve"


def get_api_key():
    key = os.environ.get("MINIMAX_API_KEY")
    if not key:
        sys.stderr.write("ERROR: MINIMAX_API_KEY environment variable not set\n")
        sys.exit(1)
    return key


def get_headers():
    return {"Authorization": f"Bearer {get_api_key()}", "Content-Type": "application/json"}


def get_output_dirs(script_dir):
    out = script_dir / "output"
    return out / "frames", out / "videos", out / "final_story.mp4"


def parse_args():
    p = ArgumentParser(description="MiniMax T2I→I2V 全自动流水线（支持 I2V 重试）")
    p.add_argument("-i", "--input", required=True, help="分镜 JSON 文件路径")
    p.add_argument("-o", "--output", default=None, help="最终输出 MP4 路径")
    p.add_argument("--crf", default="23", help="ffmpeg CRF（默认: 23）")
    return p.parse_args()


# ── API helpers ─────────────────────────────────────────────────────────────
def t2i_generate(visual_prompt):
    """调用 MiniMax T2I，返回 (img_url, error_msg)"""
    resp = requests.post(T2I_URL, headers=get_headers(), json={
        "model": "image-01",
        "prompt": visual_prompt,
        "aspect_ratio": "16:9"
    }, timeout=60)
    try:
        data = resp.json()
    except Exception:
        return None, f"non-JSON [{resp.status_code}]"
    base = data.get("base_resp", {})
    if base.get("status_code") != 0:
        return None, f"[{base.get('status_code')}]: {base.get('status_msg')}"
    img_data = data.get("data")
    if not img_data:
        return None, "data is null"
    img_url = img_data.get("image_urls", [None])[0]
    if not img_url:
        return None, "no image_urls"
    return img_url, None


def i2v_submit(img_url, prompt):
    """提交 I2V 任务，返回 (task_id, error_msg)"""
    try:
        resp = requests.post(I2V_URL, headers=get_headers(), json={
            "model": "MiniMax-Hailuo-2.3",
            "first_frame_image": img_url,
            "prompt": prompt[:200],
            "duration": 6,
            "resolution": "768P"
        }, timeout=60)
        resp.raise_for_status()
        task_id = resp.json().get("task_id")
        return task_id, None
    except Exception as e:
        return None, str(e)


def poll_task(task_id, timeout=600):
    """轮询视频任务状态，返回 file_id"""
    start = time.time()
    while time.time() - start < timeout:
        try:
            resp = requests.get(POLL_URL, headers=get_headers(),
                                params={"task_id": task_id}, timeout=30)
            resp.raise_for_status()
            result = resp.json()
        except Exception as e:
            print(f"  ⚠ poll error: {e}, retrying...")
            time.sleep(5)
            continue
        status = result.get("status", "")
        print(f"  [{status}]", end=" ", flush=True)
        if status == "Success":
            print(" ✅")
            return result.get("file_id")
        if status == "Fail":
            print(f" ❌ {result.get('base_resp', {}).get('status_msg')}")
            return None
        time.sleep(10)
    print(" ❌ timeout")
    return None


def get_download_url(file_id):
    try:
        resp = requests.get(RETRIEVE_URL, headers=get_headers(),
                           params={"file_id": file_id}, timeout=30)
        resp.raise_for_status()
        return resp.json().get("file", {}).get("download_url")
    except Exception:
        return None


def download_video(download_url, output_path):
    resp = requests.get(download_url, timeout=300, stream=True)
    resp.raise_for_status()
    with open(output_path, "wb") as f:
        for chunk in resp.iter_content(chunk_size=8192):
            f.write(chunk)


def merge_videos(video_paths, output_path, crf="23"):
    """ffmpeg 合并多个视频"""
    list_file = Path("/tmp/story_video_list.txt")
    with open(list_file, "w") as f:
        for p in video_paths:
            if p and Path(p).exists():
                f.write(f"file '{p}'\n")
    existing = [p for p in video_paths if p and Path(p).exists()]
    if not existing:
        print("❌ No videos to merge!")
        sys.exit(1)
    if len(existing) == 1:
        import shutil
        shutil.copy(existing[0], output_path)
        print(f"✅ Single video copied → {output_path}")
        return
    cmd = ["ffmpeg", "-y", "-f", "concat", "-safe", "0",
           "-i", str(list_file),
           "-c:v", "libx264", "-crf", crf,
           "-preset", "fast", "-c:a", "aac", str(output_path)]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"❌ ffmpeg: {result.stderr[-300:]}")
    else:
        print(f"✅ Merged → {output_path}")


# ── Main ────────────────────────────────────────────────────────────────────
def main():
    args = parse_args()
    script_dir = Path(__file__).parent.resolve()
    frame_dir, video_dir, default_final = get_output_dirs(script_dir)

    if args.output:
        final_video = Path(args.output)
    else:
        final_video = default_final

    frame_dir.mkdir(parents=True, exist_ok=True)
    video_dir.mkdir(parents=True, exist_ok=True)

    with open(args.input) as f:
        shots = json.load(f)

    results = {}
    for shot in shots:
        num = shot["shot_number"]
        idx = str(num).zfill(3)
        video_path = video_dir / f"shot_{idx}.mp4"

        # 跳过已有视频
        if video_path.exists() and video_path.stat().st_size > 10000:
            print(f"⏭  Skip {idx}: already exists ({video_path.stat().st_size // 1024}KB)")
            results[num] = video_path
            continue

        desc = shot.get("description", "")[:200]
        visual = shot.get("visual_description", desc)[:300]
        # 脱敏备用 prompt（I2V 失败重试时使用）
        safe_prompt = shot.get("safe_prompt", desc[:200])

        print(f"\n{'=' * 60}")
        print(f"Shot {idx}: {desc[:60]}")
        print(f"{'=' * 60}")

        # T2I
        print(f"  [T2I] Generating...", end=" ", flush=True)
        img_url, err = t2i_generate(visual)
        if not img_url:
            print(f"❌ {err}")
            continue
        print(f"✅")

        # I2V — 最多 2 次重试
        i2v_ok = False
        for attempt in range(2):
            p = desc[:200] if attempt == 0 else safe_prompt
            retry_label = "(retry)" if attempt == 1 else ""
            print(f"  [I2V{retry_label}] Submitting...", end=" ", flush=True)
            task_id, err = i2v_submit(img_url, p)
            if not task_id:
                print(f"❌ {err}")
                if attempt == 0:
                    print(f"  ⚠ I2V failed, retrying with safe prompt...")
                    time.sleep(2)
                continue

            file_id = poll_task(task_id)
            if not file_id:
                if attempt == 0:
                    print(f"  ⚠ Retrying with safe prompt...")
                    time.sleep(2)
                continue

            print(f"  [DOWN] Downloading...", end=" ", flush=True)
            dl_url = get_download_url(file_id)
            if not dl_url:
                print(f"❌ get_download_url failed")
                if attempt == 0:
                    time.sleep(2)
                continue
            try:
                download_video(dl_url, video_path)
                print(f"✅ {video_path.stat().st_size // 1024}KB")
                results[num] = video_path
                i2v_ok = True
            except Exception as e:
                print(f"❌ {e}")
            break

        if not i2v_ok:
            print(f"  ❌ Shot {idx} failed after retries")

        time.sleep(1)

    # Merge
    print(f"\n{'=' * 60}")
    print(f"Merging {len(results)}/{len(shots)} videos...")
    videos = [results.get(s["shot_number"]) for s in shots]
    merge_videos(videos, final_video, crf=args.crf)
    if final_video.exists():
        sz = final_video.stat().st_size
        print(f"\n🎉 DONE! {final_video} ({sz / 1024 / 1024:.1f}MB)")


if __name__ == "__main__":
    main()
