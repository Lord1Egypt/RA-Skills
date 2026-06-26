import argparse
import sys
import os
import math
import requests
from typing import Dict


def load_env_file() -> Dict[str, str]:
    """
    轻量读取 .env（仅在系统环境变量未定义时回填），避免直接运行 tts_client.py 时丢失配置。
    """
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    env_path = os.getenv("TTS_CONFIG_FILE", os.path.join(repo_root, ".env"))
    loaded = {}

    if not os.path.isfile(env_path):
        return loaded

    with open(env_path, "r", encoding="utf-8") as f:
        for line in f:
            raw = line.strip()
            if not raw or raw.startswith("#") or "=" not in raw:
                continue
            key, value = raw.split("=", 1)
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            if key and key not in os.environ:
                os.environ[key] = value
                loaded[key] = value

    return loaded


def env_float(name: str, default: float) -> float:
    try:
        return float(os.getenv(name, str(default)))
    except Exception:
        return default


def env_int(name: str, default: int) -> int:
    try:
        return int(os.getenv(name, str(default)))
    except Exception:
        return default


def get_request_timeout_seconds(text: str) -> float:
    """
    长文本按长度动态放大超时，防止 300s 固定上限导致请求中断。
    """
    base_timeout = env_float("TTS_REQUEST_TIMEOUT", 300.0)
    per_char = env_float("TTS_REQUEST_TIMEOUT_PER_CHAR", 0.8)
    per_chunk = env_float("TTS_REQUEST_TIMEOUT_PER_CHUNK", 90.0)
    max_timeout = env_float("TTS_REQUEST_TIMEOUT_MAX", 7200.0)
    chunk_chars = max(20, env_int("TTS_MAX_CHUNK_CHARS", 50))
    estimated_chunks = max(1, math.ceil(len(text) / chunk_chars))
    dynamic_timeout = (
        base_timeout
        + max(0, len(text) - 120) * per_char
        + estimated_chunks * per_chunk
    )
    return max(30.0, min(dynamic_timeout, max_timeout))

def main():
    load_env_file()

    parser = argparse.ArgumentParser(description="OpenClaw Voice Clone TTS Client")
    parser.add_argument("--text", type=str, required=True, help="需要被语音克隆引擎读出来的文字内容")
    parser.add_argument("--ref_audio", type=str, default="", help="用户指定的参考录音本地绝对路径")
    parser.add_argument("--speed", type=float, default=1.0, help="可选：调节生成的语速倍率，默认 1.0")
    parser.add_argument("--output_dir", type=str, default="", help="可选：指定生成的音频存放目录，默认为后端的 generated_audio/")
    
    args = parser.parse_args()
    
    if not args.text.strip():
        print("Error: 文本为空！无法生成音频。", file=sys.stderr)
        sys.exit(1)

    # 发送请求至本地常驻推理微服务（地址由 .env / 环境变量统一配置）
    tts_host = os.getenv("TTS_SERVER_HOST", "127.0.0.1")
    tts_port = env_int("TTS_SERVER_PORT", 8000)
    target_url = f"http://{tts_host}:{tts_port}/clone"
    timeout_sec = get_request_timeout_seconds(args.text)

    payload = {
        "text": args.text,
        "ref_audio_path": args.ref_audio if args.ref_audio else None,
        "speed": args.speed,
        "output_dir": args.output_dir if args.output_dir else None
    }
    
    try:
        resp = requests.post(target_url, json=payload, timeout=timeout_sec)
        
        resp.raise_for_status()
        data = resp.json()
        
        output_file = data.get("output_audio_path")
        if output_file and os.path.exists(output_file):
            print(f"DEBUG: 成功收到模型发还的音频地址: {output_file}", file=sys.stderr)
            # SKILL.md 要求：脚本标准输出只有一行即生成的音频绝对路径
            print(output_file)
            sys.exit(0)
        else:
            print(f"Error: 成功走完了接口，但返回的本地文件 {output_file} 无效或丢失。", file=sys.stderr)
            sys.exit(1)
            
    except Exception as e:
        print(
            f"Error: 请求守护端崩溃或不可达 ({tts_host}:{tts_port}, timeout={timeout_sec:.1f}s)。"
            f"你刚才是不是忘了启动 server/app.py？原因：{e}",
            file=sys.stderr
        )
        sys.exit(1)

if __name__ == "__main__":
    main()
