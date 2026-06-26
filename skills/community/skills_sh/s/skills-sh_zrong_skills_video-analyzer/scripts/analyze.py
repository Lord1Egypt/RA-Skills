#!/usr/bin/env python3
"""Video Analyzer — 使用视觉/视频大模型分析视频内容。

支持三种视频来源：
  - 本地文件路径
  - 直接视频 URL（.mp4, .mkv, .webm 等）
  - 视频站点 URL（YouTube, Bilibili 等，通过 yt-dlp 下载）

支持两种分析模式：
  - 抽帧分析：提取关键帧发给视觉模型
  - 直接视频分析：将视频发给支持原生视频输入的模型
"""

import argparse
import base64
import json
import os
import re
import subprocess
import sys
import tempfile
import tomllib
from pathlib import Path

import cv2
import httpx
from openai import OpenAI

SCRIPT_DIR = Path(__file__).parent
SKILL_DIR = SCRIPT_DIR.parent
MODELS_FILE = SCRIPT_DIR / "models.json"
CONFIG_SECTION = "video-analyzer"

VIDEO_EXTENSIONS = {
    ".mp4", ".mkv", ".webm", ".avi", ".mov", ".flv", ".wmv", ".m4v", ".ts", ".mpg", ".mpeg",
}


def _find_config() -> Path | None:
    """查找 agent_config.toml 配置文件（四位置发现策略）。

    优先级（从高到低）：
    1. 当前工作目录（CWD）/agent_config.toml
    2. Skill 目录（SKILL_DIR）/agent_config.toml
    3. 向上查找 .git 所在目录/agent_config.toml
    4. ~/.agents/agent_config.toml

    找不到时返回 None（fallback 到 models.json）。
    """
    candidates = [
        Path.cwd() / "agent_config.toml",
        SKILL_DIR / "agent_config.toml",
    ]
    for parent in Path.cwd().parents:
        if (parent / ".git").exists():
            candidates.append(parent / "agent_config.toml")
            break
    candidates.append(Path.home() / ".agents" / "agent_config.toml")

    for candidate in candidates:
        if candidate.exists():
            return candidate
    return None


def load_toml_config() -> dict | None:
    """从 agent_config.toml 加载 [video-analyzer] 配置。找不到时返回 None。"""
    config_path = _find_config()
    if not config_path:
        return None
    with open(config_path, "rb") as f:
        config = tomllib.load(f)
    return config.get(CONFIG_SECTION, {})


def load_models_config() -> dict:
    """加载模型配置。优先从 agent_config.toml 读取，fallback 到 models.json。"""
    toml_cfg = load_toml_config()
    if toml_cfg and "models" in toml_cfg:
        return toml_cfg

    # fallback: models.json
    if not MODELS_FILE.exists():
        print(
            f"错误: 未找到 agent_config.toml 中的 [{CONFIG_SECTION}] 配置，"
            f"且 models.json 不存在: {MODELS_FILE}\n"
            f"请复制 {SKILL_DIR / 'agent_config.example.toml'} 为 agent_config.toml 并填入实际值",
            file=sys.stderr,
        )
        sys.exit(1)
    with open(MODELS_FILE) as f:
        return json.load(f)


def resolve_model(config: dict, model_name: str | None) -> dict:
    """解析模型配置，返回完整的模型信息。"""
    name = model_name or config.get("default_model")
    if not name:
        print("错误: 未指定模型，且配置文件中没有 default_model", file=sys.stderr)
        sys.exit(1)
    model_cfg = config["models"].get(name)
    if not model_cfg:
        available = ", ".join(config["models"].keys())
        print(f"错误: 模型 '{name}' 不存在。可用模型: {available}", file=sys.stderr)
        sys.exit(1)
    return model_cfg


def is_url(path: str) -> bool:
    return path.startswith("http://") or path.startswith("https://")


def is_direct_video_url(url: str) -> bool:
    """判断 URL 是否直接指向视频文件。"""
    # 去掉 query string 后检查扩展名
    path_part = url.split("?")[0].split("#")[0]
    return Path(path_part).suffix.lower() in VIDEO_EXTENSIONS


def download_direct_url(url: str, dest: Path) -> None:
    """使用 httpx 下载直接视频 URL。"""
    print(f"正在下载视频: {url}")
    with httpx.stream("GET", url, follow_redirects=True, timeout=300) as resp:
        resp.raise_for_status()
        total = int(resp.headers.get("content-length", 0))
        downloaded = 0
        with open(dest, "wb") as f:
            for chunk in resp.iter_bytes(chunk_size=1024 * 1024):
                f.write(chunk)
                downloaded += len(chunk)
                if total:
                    pct = downloaded * 100 // total
                    print(f"\r  下载进度: {pct}% ({downloaded // 1024 // 1024}MB)", end="", flush=True)
    print()


def download_with_ytdlp(url: str, dest: Path) -> None:
    """使用 yt-dlp 下载视频站点的视频。"""
    print(f"正在通过 yt-dlp 下载视频: {url}")
    cmd = [
        sys.executable, "-m", "yt_dlp",
        "-f", "best[ext=mp4]/best",
        "-o", str(dest),
        "--no-playlist",
        "--quiet",
        "--progress",
        url,
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"yt-dlp 下载失败:\n{result.stderr}", file=sys.stderr)
        sys.exit(1)
    print(f"  下载完成: {dest}")


def prepare_video(source: str, tmp_dir: str) -> Path:
    """准备视频文件，返回本地文件路径。"""
    if not is_url(source):
        path = Path(source).expanduser().resolve()
        if not path.exists():
            print(f"错误: 视频文件不存在: {path}", file=sys.stderr)
            sys.exit(1)
        return path

    # 确定下载目标路径
    if is_direct_video_url(source):
        suffix = Path(source.split("?")[0]).suffix or ".mp4"
        dest = Path(tmp_dir) / f"video{suffix}"
        download_direct_url(source, dest)
    else:
        dest = Path(tmp_dir) / "video.mp4"
        download_with_ytdlp(source, dest)

    return dest


def extract_frames(video_path: Path, num_frames: int, max_size: int) -> list[str]:
    """从视频中均匀提取帧，返回 base64 编码的 JPEG 列表。"""
    cap = cv2.VideoCapture(str(video_path))
    if not cap.isOpened():
        print(f"错误: 无法打开视频文件: {video_path}", file=sys.stderr)
        sys.exit(1)

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    duration = total_frames / fps if fps > 0 else 0
    print(f"视频信息: {total_frames} 帧, {fps:.1f} FPS, {duration:.1f} 秒")

    # 计算采样间隔
    if num_frames >= total_frames:
        indices = list(range(total_frames))
    else:
        indices = [int(i * total_frames / num_frames) for i in range(num_frames)]

    frames_b64 = []
    for idx in indices:
        cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
        ret, frame = cap.read()
        if not ret:
            continue

        # 缩放
        h, w = frame.shape[:2]
        if max(h, w) > max_size:
            scale = max_size / max(h, w)
            frame = cv2.resize(frame, (int(w * scale), int(h * scale)))

        # 编码为 JPEG
        _, buf = cv2.imencode(".jpg", frame, [cv2.IMWRITE_JPEG_QUALITY, 85])
        b64 = base64.b64encode(buf.tobytes()).decode("utf-8")
        frames_b64.append(b64)

        timestamp = idx / fps if fps > 0 else 0
        print(f"  提取帧 {len(frames_b64)}/{num_frames}: {timestamp:.1f}s")

    cap.release()
    print(f"共提取 {len(frames_b64)} 帧")
    return frames_b64


def encode_video_b64(video_path: Path) -> str:
    """将视频文件编码为 base64。"""
    with open(video_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def build_responses_input(frames_b64: list[str], prompt: str) -> list[dict]:
    """构建 Responses API 格式的输入（抽帧模式）。"""
    content = []
    for i, b64 in enumerate(frames_b64):
        content.append({
            "type": "input_image",
            "image_url": f"data:image/jpeg;base64,{b64}",
        })
    content.append({
        "type": "input_text",
        "text": prompt,
    })
    return [{"role": "user", "content": content}]


def build_responses_video_input(video_b64: str, prompt: str, ext: str = "mp4") -> list[dict]:
    """构建 Responses API 格式的输入（直接视频模式）。"""
    mime = f"video/{ext}"
    content = [
        {
            "type": "input_video",
            "video_url": f"data:{mime};base64,{video_b64}",
        },
        {
            "type": "input_text",
            "text": prompt,
        },
    ]
    return [{"role": "user", "content": content}]


def build_chat_input(frames_b64: list[str], prompt: str) -> list[dict]:
    """构建 Chat Completions API 格式的输入（抽帧模式）。"""
    content = []
    for b64 in frames_b64:
        content.append({
            "type": "image_url",
            "image_url": {"url": f"data:image/jpeg;base64,{b64}"},
        })
    content.append({
        "type": "text",
        "text": prompt,
    })
    return [{"role": "user", "content": content}]


def build_chat_video_input(video_b64: str, prompt: str, ext: str = "mp4") -> list[dict]:
    """构建 Chat Completions API 格式的输入（直接视频模式）。"""
    mime = f"video/{ext}"
    content = [
        {
            "type": "video_url",
            "video_url": {"url": f"data:{mime};base64,{video_b64}"},
        },
        {
            "type": "text",
            "text": prompt,
        },
    ]
    return [{"role": "user", "content": content}]


def _resolve_api_key(model_cfg: dict, api_key_override: str | None = None) -> str:
    """解析 API Key。优先级：CLI 参数 > 配置文件 api_key > 环境变量 api_key_env。"""
    if api_key_override:
        return api_key_override

    # 优先读配置文件中的 api_key
    api_key = model_cfg.get("api_key", "")
    if api_key:
        return api_key

    # fallback: 从环境变量读取
    env_var = model_cfg.get("api_key_env", "")
    if env_var:
        api_key = os.getenv(env_var, "")
        if api_key:
            return api_key
        print(f"错误: 配置中无 api_key，且环境变量 {env_var} 未设置", file=sys.stderr)
    else:
        print("错误: 配置中无 api_key，且未指定 api_key_env", file=sys.stderr)
    sys.exit(1)


def call_api(model_cfg: dict, messages: list[dict], api_key_override: str | None = None) -> str:
    """调用 API 并返回模型的文本响应。"""
    api_key = _resolve_api_key(model_cfg, api_key_override)

    client = OpenAI(base_url=model_cfg["base_url"], api_key=api_key)
    api_type = model_cfg.get("api_type", "responses")

    print(f"正在调用模型: {model_cfg['model']} (API: {api_type})")

    if api_type == "responses":
        response = client.responses.create(
            model=model_cfg["model"],
            input=messages,
        )
        # Responses API 返回格式
        if hasattr(response, "output_text"):
            return response.output_text
        if hasattr(response, "output"):
            for item in response.output:
                if hasattr(item, "content"):
                    for block in item.content:
                        if hasattr(block, "text"):
                            return block.text
        return str(response)
    else:
        response = client.chat.completions.create(
            model=model_cfg["model"],
            messages=messages,
        )
        return response.choices[0].message.content


def extract_json(text: str) -> dict | None:
    """从模型输出中提取 JSON 对象，兼容 ```json 代码块包裹。

    贪婪匹配最大的 {...} 块后用 json.loads 解析，失败返回 None。
    """
    match = re.search(r"\{[\s\S]*\}", text)
    if not match:
        return None
    try:
        return json.loads(match.group())
    except json.JSONDecodeError:
        return None


def main():
    parser = argparse.ArgumentParser(
        description="使用视觉/视频大模型分析视频内容",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s --video video.mp4 --prompt "描述视频内容"
  %(prog)s --video https://example.com/video.mp4 --prompt "分析"
  %(prog)s --video https://www.youtube.com/watch?v=xxx --prompt "总结"
  %(prog)s --video video.mp4 --model gpt-4o --frames 20 --prompt "分析"
        """,
    )
    parser.add_argument("--video", required=True, help="视频文件路径或 URL")
    parser.add_argument("--prompt", required=True, help="分析提示词")
    parser.add_argument("--model", default=None, help="模型名称（对应 models.json 中的 key）")
    parser.add_argument("--frames", type=int, default=10, help="抽帧数量（默认 10）")
    parser.add_argument("--max-size", type=int, default=720, help="帧最大边长像素（默认 720）")
    parser.add_argument("--json", action="store_true",
                        help="要求模型返回 JSON 并解析输出（自动附加视频帧数/帧率/时长到 prompt，便于返回帧序号）")

    # 直接指定模型参数（不依赖 models.json）
    parser.add_argument("--base-url", default=None, help="API base URL（直接指定模式）")
    parser.add_argument("--api-key", default=None, help="API Key（直接指定模式）")
    parser.add_argument("--model-id", default=None, help="模型 ID（直接指定模式）")
    parser.add_argument("--api-type", default="responses", choices=["responses", "chat_completions"],
                        help="API 类型（直接指定模式，默认 responses）")
    parser.add_argument("--supports-video", action="store_true", help="模型支持原生视频输入")

    args = parser.parse_args()

    # 构建模型配置
    if args.base_url and args.model_id:
        model_cfg = {
            "base_url": args.base_url,
            "api_key_env": "",
            "model": args.model_id,
            "api_type": args.api_type,
            "supports_video": args.supports_video,
        }
        api_key_override = args.api_key
    else:
        config = load_models_config()
        model_cfg = resolve_model(config, args.model)
        api_key_override = None

    with tempfile.TemporaryDirectory(prefix="video-analyzer-") as tmp_dir:
        # 准备视频
        video_path = prepare_video(args.video, tmp_dir)

        # 构建 prompt（--json 模式附加视频元数据 + JSON 输出要求）
        prompt = args.prompt
        if args.json:
            cap = cv2.VideoCapture(str(video_path))
            total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            fps = cap.get(cv2.CAP_PROP_FPS)
            cap.release()
            duration = total / fps if fps > 0 else 0
            prompt = (
                f"（视频共 {total} 帧，{fps:.1f} FPS，{duration:.1f} 秒）\n\n"
                + args.prompt
                + "\n\n请只返回一个合法 JSON 对象，不要任何其他文字或 markdown 代码块。"
            )

        # 根据模型能力选择分析模式
        if model_cfg.get("supports_video"):
            print("模式: 直接视频分析")
            video_b64 = encode_video_b64(video_path)
            ext = video_path.suffix.lstrip(".") or "mp4"
            if model_cfg.get("api_type") == "chat_completions":
                messages = build_chat_video_input(video_b64, prompt, ext)
            else:
                messages = build_responses_video_input(video_b64, prompt, ext)
        else:
            print("模式: 抽帧分析")
            frames = extract_frames(video_path, args.frames, args.max_size)
            if not frames:
                print("错误: 未能提取到任何帧", file=sys.stderr)
                sys.exit(1)
            if model_cfg.get("api_type") == "chat_completions":
                messages = build_chat_input(frames, prompt)
            else:
                messages = build_responses_input(frames, prompt)

        # 调用 API
        result = call_api(model_cfg, messages, api_key_override)

        # --json 模式：解析并输出 JSON；否则打印自然语言结果
        if args.json:
            parsed = extract_json(result)
            if parsed is not None:
                print(json.dumps(parsed, indent=2, ensure_ascii=False))
            else:
                print("⚠ 未解析到 JSON，原始输出如下：")
                print(result)
        else:
            print("\n" + "=" * 60)
            print("分析结果:")
            print("=" * 60)
            print(result)


if __name__ == "__main__":
    main()
