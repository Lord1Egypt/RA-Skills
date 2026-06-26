#!/usr/bin/env python3
"""
visual.py — 抽帧 + 视觉观测（合并脚本）

从视频中抽取关键帧，然后对每帧做结构化视觉观测，输出 observations_visual.json。
长视频（>4分钟）自动分段，每段独立抽帧+观测，最后合并为单一 JSON。

用法：
  # 预处理模式（默认）—— 只抽帧，不调 API
  python3 visual.py --video input.mp4 --output-dir /tmp/out [--max-frames 20]

  # 完整模式 —— 使用外部视觉 LLM API 生成结构化观测
  python3 visual.py --video input.mp4 --output-dir /tmp/out \
    --vision-llm-key KEY --vision-llm-base URL --vision-llm-model MODEL

  # 保留帧图片（默认清理）
  python3 visual.py --video input.mp4 --output-dir /tmp/out --keep-frames
"""

import os
import sys
import json
import base64
import glob
import re
import argparse
import subprocess
import shutil
import tempfile
import urllib.request

# 公共工具
from common import http_request_with_retry, get_media_duration, parse_json_from_llm, extract_llm_content


# ── 分段抽帧 ──

SEGMENT_SECONDS = 240  # 4 分钟一段
MAX_FRAMES_PER_SEGMENT = 20


def plan_segments(duration: float, segment_seconds: float = SEGMENT_SECONDS,
                  max_frames_per_segment: int = MAX_FRAMES_PER_SEGMENT) -> list:
    """规划分段策略，返回 [(start, duration, interval, frame_count), ...]"""
    segments = []
    if duration <= segment_seconds:
        # 单段：自适应间隔
        interval = max(1, duration / max_frames_per_segment)
        frame_count = min(int(duration / interval), max_frames_per_segment)
        if frame_count < 1:
            frame_count = 1
        segments.append((0.0, duration, interval, frame_count))
    else:
        start = 0.0
        while start < duration:
            seg_end = min(start + segment_seconds, duration)
            seg_duration = seg_end - start
            if seg_duration < 1:
                break
            if seg_duration >= segment_seconds:
                # 满段：固定间隔
                interval = segment_seconds / max_frames_per_segment
            else:
                # 尾段（不满一段）：自适应
                interval = max(1, seg_duration / max_frames_per_segment)
            frame_count = min(int(seg_duration / interval), max_frames_per_segment)
            if frame_count < 1:
                frame_count = 1
            segments.append((start, seg_duration, interval, frame_count))
            start = seg_end
    return segments


def extract_segment_frames(video_path: str, output_dir: str,
                           start: float, seg_duration: float,
                           interval: float, max_frames: int) -> list:
    """用 ffmpeg 从视频指定时间段抽取关键帧"""
    os.makedirs(output_dir, exist_ok=True)

    result = subprocess.run(
        ["ffmpeg", "-y", "-ss", str(start), "-i", video_path,
         "-t", str(seg_duration),
         "-vf", f"fps=1/{interval:.1f}",
         "-frames:v", str(max_frames),
         "-q:v", "2",
         os.path.join(output_dir, "frame_%03d.jpg")],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        print(f"WARNING: ffmpeg exited with code {result.returncode}: {result.stderr}", file=sys.stderr)

    frames = sorted(glob.glob(os.path.join(output_dir, "frame_*.jpg")))
    return frames


def extract_all_frames(video_path: str, output_dir: str, duration: float,
                       max_frames_per_segment: int = MAX_FRAMES_PER_SEGMENT) -> list:
    """分段抽帧，返回 segment info 列表"""
    segments = plan_segments(duration, max_frames_per_segment=max_frames_per_segment)
    all_segments = []

    print(f"Video: {video_path}")
    print(f"Duration: {duration:.1f}s | Segments: {len(segments)}")

    for i, (start, seg_dur, interval, frame_count) in enumerate(segments):
        seg_dir = os.path.join(output_dir, f"seg_{i:03d}")
        print(f"  Segment {i+1}/{len(segments)}: {start:.0f}s-{start+seg_dur:.0f}s "
              f"(interval={interval:.1f}s, ~{frame_count} frames)")
        frames = extract_segment_frames(video_path, seg_dir, start, seg_dur, interval, frame_count)
        all_segments.append({
            "index": i,
            "start": start,
            "duration": seg_dur,
            "interval": interval,
            "frames": frames
        })
        print(f"    Extracted {len(frames)} frames")

    total = sum(len(s["frames"]) for s in all_segments)
    print(f"Total: {total} frames across {len(segments)} segments")
    return all_segments


# ── 帧编码 ──

def encode_image(path: str, max_size_kb: int = 200, max_width: int = 1280) -> str:
    """Encode image to base64 data URL. Auto-resize if file exceeds max_size_kb."""
    with open(path, "rb") as f:
        raw = f.read()
    ext = os.path.splitext(path)[1].lstrip(".")
    mime = {"jpg": "jpeg", "jpeg": "jpeg", "png": "png", "webp": "webp"}.get(ext, "jpeg")

    if len(raw) <= max_size_kb * 1024:
        # Small enough, use as-is
        data = base64.b64encode(raw).decode()
    else:
        # Resize to reduce payload
        try:
            from PIL import Image
            import io
            img = Image.open(path)
            if img.width > max_width:
                ratio = max_width / img.width
                img = img.resize((max_width, int(img.height * ratio)), Image.LANCZOS)
            buf = io.BytesIO()
            img.save(buf, format="JPEG", quality=85)
            data = base64.b64encode(buf.getvalue()).decode()
            mime = "jpeg"
        except ImportError:
            # Pillow not available, use ffmpeg to resize
            with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp:
                tmp_path = tmp.name
            proc = subprocess.run(["ffmpeg", "-y", "-i", path, "-vf", f"scale={max_width}:-1", "-q:v", "2", tmp_path],
                           capture_output=True)
            if proc.returncode != 0 or not os.path.exists(tmp_path) or os.path.getsize(tmp_path) == 0:
                # ffmpeg resize failed, fall back to raw file data
                print(f"WARNING: ffmpeg resize failed (rc={proc.returncode}), using original image")
                os.unlink(tmp_path) if os.path.exists(tmp_path) else None
                with open(path, "rb") as rf:
                    data = base64.b64encode(rf.read()).decode()
                return f"data:image/{mime};base64,{data}"
            with open(tmp_path, "rb") as tf:
                data = base64.b64encode(tf.read()).decode()
            os.unlink(tmp_path)
            mime = "jpeg"

    return f"data:image/{mime};base64,{data}"


# ── LLM 调用 ──

def call_llm(api_base: str, api_key: str, model: str, messages: list) -> str:
    """调用 OpenAI 兼容 API（带重试）"""
    payload = {"model": model, "messages": messages, "max_tokens": 6000, "temperature": 0.3}
    req_data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        f"{api_base.rstrip('/')}/chat/completions",
        data=req_data,
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"}
    )
    resp_data = http_request_with_retry(req, timeout=180, label=f"Vision LLM ({model})")
    content = extract_llm_content(resp_data, label=f"Vision LLM ({model})")
    return content


# ── Prompt 构建 ──

def build_observe_prompt(frame_count: int, duration: float, interval: float,
                         seg_start: float = 0.0, total_segments: int = 1, seg_index: int = 0) -> str:
    time_label = f"{seg_start:.0f}s - {seg_start+duration:.0f}s" if total_segments > 1 else f"0 - {duration:.1f}s"
    seg_info = f"（这是视频的第 {seg_index+1}/{total_segments} 段，时间范围 {time_label}）" if total_segments > 1 else ""

    return f"""## 任务
你是一个专业的视频帧观察助手。下面是从一段视频中抽取的 {frame_count} 个关键帧截图（每 {interval:.1f} 秒一帧，覆盖 {duration:.1f} 秒）。{seg_info}

请仔细观察每一帧，按顺序输出一个 JSON 数组，每个元素包含以下字段：

| 字段 | 类型 | 说明 |
|------|------|------|
| frame | string | 文件名（如 frame_001.jpg） |
| objects | string[] | 画面中出现的关键对象、人物、UI 元素（这是实体的唯一来源，必须先完成识别） |
| desc | string | ~100 字描述段落，用六要素（Who/What/When/Where/Why/How）描述画面核心内容。使用视频内容的主要语言输出（中文视频用中文，英文视频用英文，以此类推）。⚠️ **desc 中的 Who 必须使用 objects 字段中识别出的实体名称，不得凭空编造。** |
| texts | string | 画面中可读的所有明显文字，用逗号分隔。无文字则为空字符串 |
| actions | string[] | 画面中正在发生的动作或事件（如：展示信息、切换画面、标注步骤） |
| style | string | 画面风格标签（科技感/教程/日常/娱乐/卡通/纪录片等） |
| cover_candidate | boolean | 该帧是否适合作为视频封面（画面信息密度高、文字清晰、有视觉冲击力时为 true） |

## 观察要点
- **先识别 objects，再写 desc**：objects 是实体注册表，desc 中的 Who 必须从中取用
- **六要素精简**：desc 约100字，覆盖核心要素即可，不需要面面俱到
- **文字识别**：标题、副标题、按钮文字、状态栏、标签、编号等所有可读文字
- **UI 元素**：卡片、列表、流程图、进度条、弹窗、状态面板等
- **逻辑关系**：帧与帧之间是否有递进（如步骤1→2→3）、对比、因果等关系
- **风格判断**：配色方案（深色/浅色）、字体风格、整体氛围
- **封面评估**：信息密度、文字可读性、视觉焦点是否明确

## 输出格式
严格输出 JSON 数组，不要包含任何其他文字、解释或 markdown 标记。
数组长度必须等于 {frame_count}（每帧一个对象，顺序对应截图顺序）。

示例（2帧）：
[{{"frame":"frame_001.jpg","objects":["研究员","实验设备","蓝色显示屏"],"desc":"深色科技界面中，研究员正在调试大型实验设备，蓝色显示屏显示实时数据流，实验室环境，2026年5月。","texts":"实验参数,2026-05","actions":["调试设备参数"],"style":"科技感/深色系","cover_candidate":true}},{{"frame":"frame_002.jpg","objects":["AI助手角色","数据图表"],"desc":"AI助手角色在虚拟办公室中讲解折线图数据，展示Q3上升趋势的阶段性成果。","texts":"Q3 Results,趋势图","actions":["讲解数据"],"style":"教程/科技感","cover_candidate":false}}]"""


def parse_observations(content: str) -> list:
    """从 LLM 输出解析观测 JSON 数组"""
    result = parse_json_from_llm(content, expect_array=True)
    if isinstance(result, list):
        return result
    if result is not None:
        print(f"WARNING: LLM output parsed but was not an array (got {type(result).__name__})")
    return []


# ── 观测单段 ──

def observe_segment(seg: dict, total_segs: int, api_key: str, api_base: str, model: str) -> list:
    """对单段进行视觉 LLM 观测，返回观测列表"""
    frames = seg["frames"]
    if not frames:
        return []

    seg_idx = seg["index"]
    seg_label = f"Segment {seg_idx+1}/{total_segs}"
    print(f"\n--- {seg_label}: {len(frames)} frames ({seg['start']:.0f}s-{seg['start']+seg['duration']:.0f}s) ---")

    frame_data = []
    for i, fp in enumerate(frames):
        b64 = encode_image(fp)
        frame_data.append({"type": "image_url", "image_url": {"url": b64}})
        print(f"  Encoded frame {i+1}/{len(frames)}: {os.path.basename(fp)}")

    prompt = build_observe_prompt(
        len(frames), seg["duration"], seg["interval"],
        seg_start=seg["start"], total_segments=total_segs, seg_index=seg_idx
    )
    messages_base = [{"role": "user", "content": [{"type": "text", "text": prompt}, *frame_data]}]
    try:
        content = call_llm(api_base, api_key, model, messages_base)
    except Exception as e:
        print(f"WARNING: Vision LLM call failed for {seg_label}: {e}")
        content = ""

    # 多轮 JSON 解析重试
    obs = []
    if content is None:
        content = ""
    if content:
        obs = parse_observations(content)
    if not obs:
        for retry_i in range(2):
            print(f"  Visual parse retry {retry_i+1}/2 for {seg_label}...")
            retry_msg = f"你的上一次输出不是合法的 JSON 数组。请重新输出，严格只输出 JSON 数组，不要包含任何其他文字、解释或 markdown 标记。"
            retry_messages = [
                *messages_base,
                {"role": "assistant", "content": content},
                {"role": "user", "content": retry_msg}
            ]
            try:
                content = call_llm(api_base, api_key, model, retry_messages)
                if content is None:
                    content = ""
                obs = parse_observations(content)
                if obs:
                    print(f"  Visual parse retry {retry_i+1} succeeded")
                    break
            except Exception as e:
                print(f"  Visual retry {retry_i+1} failed: {e}")
                # 继续重试，不让单次失败中断整个段
                continue

    if not obs:
        # 退化：用帧文件名 + 原始 LLM 文本构造基础观测
        print(f"WARNING: No observations parsed for {seg_label} after retries. Generating placeholder entries.")
        for i, fp in enumerate(frames):
            excerpt = (content or "")[:200]
            obs.append({
                "frame": os.path.basename(fp),
                "objects": [],
                "desc": f"(LLM output unparseable) {excerpt}",
                "texts": "",
                "actions": [],
                "style": "",
                "cover_candidate": False,
                "segment": seg_idx,
                "segment_start": seg["start"],
                "parse_failed": True
            })
    else:
        for o in obs:
            o.setdefault("segment", seg_idx)
            o.setdefault("segment_start", seg["start"]) 
    print(f"  {seg_label}: {len(obs)} observations")
    return obs


def observe_segment_placeholder(seg: dict) -> list:
    """预处理模式：生成占位观测"""
    obs = []
    for fp in seg["frames"]:
        obs.append({
            "frame": os.path.basename(fp),
            "segment": seg["index"],
            "segment_start": seg["start"],
            "desc": "",
            "texts": "",
            "objects": [],
            "actions": [],
            "style": "",
            "cover_candidate": False
        })
    return obs


# ── 主流程 ──

def main():
    parser = argparse.ArgumentParser(description="Visual: extract frames + observe")
    parser.add_argument("--video", required=True, help="Input video file")
    parser.add_argument("--output-dir", required=True, help="Output directory")
    parser.add_argument("--max-frames", type=int, default=15,
                        help="Max frames per 4-minute segment (default: 15)")
    parser.add_argument("--keep-frames", action="store_true", help="Keep frame images (default: clean up)")
    parser.add_argument("--vision-llm-key", default=None, help="Vision LLM API key")
    parser.add_argument("--vision-llm-base", default=None, help="Vision LLM API base URL")
    parser.add_argument("--vision-llm-model", default=None, help="Vision LLM model (must support image input)")
    args = parser.parse_args()

    if not os.path.exists(args.video):
        print(f"ERROR: Video not found: {args.video}", file=sys.stderr)
        sys.exit(1)

    os.makedirs(args.output_dir, exist_ok=True)
    frames_dir = os.path.join(args.output_dir, "frames")
    os.makedirs(frames_dir, exist_ok=True)

    duration = get_media_duration(args.video)
    is_long = duration > SEGMENT_SECONDS

    # Step 1: 分段抽帧
    print("=== Visual: Extracting frames ===")
    segments = extract_all_frames(args.video, frames_dir, duration, args.max_frames)
    print()

    # Step 2: 视觉观测
    print("=== Visual: Observing frames ===")
    has_api = args.vision_llm_key and args.vision_llm_base and args.vision_llm_model
    if has_api:
        print("⚠️  PRIVACY: Vision frames will be sent to external LLM endpoint:", args.vision_llm_base)
    final_output = os.path.join(args.output_dir, "observations_visual.json")

    if is_long:
        # ── 长视频：按段并行观测，最后合并 ──
        obs_dir = os.path.join(args.output_dir, "observations_visual")
        os.makedirs(obs_dir, exist_ok=True)
        all_observations = []
        total_segs = len(segments)

        def _observe_one(seg):
            """观测单个 segment 并返回 (seg_index, obs_list)"""
            try:
                if has_api:
                    obs = observe_segment(seg, total_segs, args.vision_llm_key,
                                          args.vision_llm_base, args.vision_llm_model)
                else:
                    print(f"Preprocess-only: Segment {seg['index']+1}/{total_segs}")
                    obs = observe_segment_placeholder(seg)
            except Exception as e:
                # 无论何种错误，都要保证写出占位文件，不让单段异常影响其它段
                print(f"ERROR: Exception while observing segment {seg['index']}: {e}")
                obs = observe_segment_placeholder(seg)
                for o in obs:
                    o["parse_failed"] = True
                    o["error"] = str(e)

            # 每段写入独立文件
            seg_path = os.path.join(obs_dir, f"segment_{seg['index']:03d}.json")
            try:
                with open(seg_path, "w", encoding="utf-8") as f:
                    json.dump(obs, f, ensure_ascii=False, indent=2)
                print(f"  Saved → {seg_path}")
            except Exception as e:
                print(f"ERROR: Failed to write segment file {seg_path}: {e}")
            return (seg["index"], obs)

        from concurrent.futures import ThreadPoolExecutor, as_completed
        with ThreadPoolExecutor(max_workers=min(total_segs, 4)) as pool:
            futures = {pool.submit(_observe_one, seg): seg for seg in segments}
            for future in as_completed(futures):
                seg_idx, obs = future.result()
                all_observations.extend(obs)

        def _sort_key(o):
            """按 segment + frame 编号排序"""
            seg = o.get("segment", 0)
            fname = os.path.basename(o.get("frame", "frame_999.jpg"))
            # 从 frame_XXX.jpg 提取编号
            m = re.search(r'(\d+)', fname)
            frame_num = int(m.group(1)) if m else 999
            return (seg, frame_num)

        all_observations.sort(key=_sort_key)

        # 合并为单一文件
        with open(final_output, "w", encoding="utf-8") as f:
            json.dump(all_observations, f, ensure_ascii=False, indent=2)
        print(f"\nMerged {len(all_observations)} observations from {total_segs} segments → {final_output}")

        # 清理分段文件（合并后不再需要）
        shutil.rmtree(obs_dir, ignore_errors=True)
        print(f"Cleaned up per-segment files in {obs_dir}")

    else:
        # ── 短视频：直接输出 observations_visual.json ──
        seg = segments[0]

        if has_api:
            obs = observe_segment(seg, 1, args.vision_llm_key,
                                  args.vision_llm_base, args.vision_llm_model)
        else:
            print("Preprocess-only mode (single segment)")
            obs = observe_segment_placeholder(seg)

        with open(final_output, "w", encoding="utf-8") as f:
            json.dump(obs, f, ensure_ascii=False, indent=2)
        print(f"\nObservations saved → {final_output} ({len(obs)} frames)")

    # 清理帧图片
    if not args.keep_frames:
        frame_count = sum(len(s["frames"]) for s in segments)
        shutil.rmtree(frames_dir, ignore_errors=True)
        print(f"Cleaned up {frame_count} frames")
    else:
        total = sum(len(s["frames"]) for s in segments)
        print(f"Kept {total} frames in {frames_dir}")


if __name__ == "__main__":
    main()
