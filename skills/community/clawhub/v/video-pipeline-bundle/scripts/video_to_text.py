#!/usr/bin/env python3
"""
视频转文字稿脚本
1. 用 Faster Whisper 识别语音生成 SRT
2. 用 LLM 词级别纠错
自动检查依赖，支持多种 LLM
"""

import os
import sys
import argparse
import subprocess
import requests

# 配置
os.environ.setdefault("HF_ENDPOINT", "https://hf-mirror.com")

# 支持的 LLM 提供商
LLM_PROVIDERS = {
    "minimax": {
        "name": "MiniMax",
        "url": "https://api.minimaxi.com/anthropic",
        "env_key": "MINIMAX_API_KEY",
        "model": "MiniMax-M2.5"
    },
    "openai": {
        "name": "OpenAI",
        "url": "https://api.openai.com/v1",
        "env_key": "OPENAI_API_KEY",
        "model": "gpt-3.5-turbo"
    },
    "anthropic": {
        "name": "Anthropic Claude",
        "url": "https://api.anthropic.com/v1",
        "env_key": "ANTHROPIC_API_KEY",
        "model": "claude-3-haiku-20240307"
    }
}

TARGET = None

def check_dependencies():
    """检查并安装依赖"""
    print("🔍 检查依赖...")
    
    deps = ["faster-whisper", "requests"]
    for dep in deps:
        try:
            __import__(dep.replace("-", "_"))
            print(f"  ✅ {dep} 已安装")
        except ImportError:
            print(f"  📦 正在安装 {dep}...")
            try:
                subprocess.run([sys.executable, "-m", "pip", "install", dep, "--break-system-packages"], 
                           capture_output=True)
                print(f"  ✅ {dep} 安装完成")
            except Exception as e:
                print(f"  ❌ {dep} 安装失败: {e}")
                return False
    return True

def get_llm_config(provider):
    """获取 LLM 配置"""
    if provider not in LLM_PROVIDERS:
        print(f"❌ 不支持的 LLM 提供商: {provider}")
        print(f"支持的提供商: {', '.join(LLM_PROVIDERS.keys())}")
        return None
    
    config = LLM_PROVIDERS[provider]
    api_key = os.environ.get(config["env_key"])
    
    if not api_key:
        print(f"⚠️ 未设置 {config['env_key']} 环境变量")
        print(f"💡 请设置: export {config['env_key']}='你的APIKey'")
        return None
    
    return config

def send_message(msg):
    if not TARGET:
        print(msg)
        return
    subprocess.run([
        "openclaw", "message", "send",
        "--channel", "feishu",
        "--target", TARGET,
        "--message", msg
    ], capture_output=True)

def get_video_files(directory, exclude_pattern="已转写"):
    video_extensions = ['.mp4', '.mov', '.avi', '.mkv', '.flv', '.wmv']
    files = []
    if not os.path.exists(directory):
        return files
    for root, dirs, filenames in os.walk(directory):
        dirs[:] = [d for d in dirs if exclude_pattern not in d]
        for f in filenames:
            if exclude_pattern in f:
                continue
            ext = os.path.splitext(f)[1].lower()
            if ext in video_extensions:
                full_path = os.path.join(root, f)
                rel_path = os.path.relpath(full_path, directory)
                files.append({
                    "full_path": full_path,
                    "rel_path": rel_path,
                    "filename": f,
                    "subdir": os.path.dirname(rel_path)
                })
    return sorted(files, key=lambda x: x["rel_path"])

def ensure_dir(path):
    os.makedirs(path, exist_ok=True)

def format_time(seconds):
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    ms = int((seconds % 1) * 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"

def transcribe(video_path, output_srt, model):
    from faster_whisper import WhisperModel
    print(f"🔧 加载模型: {model}")
    whisper_model = WhisperModel(model, device="cpu", compute_type="int8")
    print(f"🎤 转写中: {video_path}")
    segments, info = whisper_model.transcribe(video_path)
    print(f"📝 语言: {info.language}")
    
    with open(output_srt, "w", encoding="utf-8") as f:
        for i, seg in enumerate(segments, 1):
            start = format_time(seg.start)
            end = format_time(seg.end)
            text = seg.text.strip()
            f.write(f"{i}\n{start} --> {end}\n{text}\n\n")
    
    # 纯文本
    segments, _ = whisper_model.transcribe(video_path)
    text = " ".join([s.text.strip() for s in segments])
    return text

def correct_text(text, api_key, provider="minimax"):
    if not api_key:
        return text
    print("🤖 LLM 纠错...")
    
    config = LLM_PROVIDERS.get(provider)
    if not config:
        return text
    
    url = f"{config['url']}/messages"
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    
    prompt = "请只修正以下演讲稿中的错别字和明显的识别错误（词级别），不修改句子结构，只返回修正后的文字："
    
    if provider == "anthropic":
        headers["anthropic-version"] = "2023-06-01"
        payload = {"model": config["model"], "max_tokens": 4096, 
                  "messages": [{"role": "user", "content": prompt + text}]}
    else:
        payload = {"model": config["model"], "max_tokens": 4096, 
                  "messages": [{"role": "user", "content": prompt + text}]}
    
    try:
        resp = requests.post(url, headers=headers, json=payload, timeout=120)
        result = resp.json()
        if "content" in result:
            for c in result["content"]:
                if c.get("type") == "text":
                    return c.get("text", text)
    except Exception as e:
        print(f"❌ API错误: {e}")
    return text

def correct_srt(srt_path, corrected_text):
    pass  # SRT 保持原始

def process_video(video_info, output_root, model, api_key, provider):
    input_path = video_info["full_path"]
    rel_path = video_info["rel_path"]
    filename = video_info["filename"]
    subdir = video_info["subdir"]
    
    name_without_ext = os.path.splitext(filename)[0]
    ext = os.path.splitext(filename)[1]
    
    if subdir and subdir != ".":
        output_subdir = os.path.join(output_root, subdir)
    else:
        output_subdir = output_root
    ensure_dir(output_subdir)
    
    output_name = f"{name_without_ext}.srt"
    output_path = os.path.join(output_subdir, output_name)
    temp_srt = output_path.replace(".srt", "_temp.srt")
    
    print(f"\n📹 处理: {rel_path}")
    send_message(f"▶️ 开始转写: {filename}")
    
    # 转写
    text = transcribe(input_path, temp_srt, model)
    if not text:
        send_message(f"❌ 转写失败: {filename}")
        return None
    
    # 纠错
    corrected = correct_text(text, api_key, provider)
    
    # 保存校正后SRT
    corrected_srt = correct_srt(temp_srt, corrected)
    with open(output_path, "w", encoding="utf-8") as f:
        # 直接复制原始 SRT（有时间线）
        if os.path.exists(temp_srt):
            with open(temp_srt, "r") as f_orig:
                f.write(f_orig.read())
    
    # 保存纯文本
    txt_path = output_path.replace(".srt", ".txt")
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(corrected)
    
    if os.path.exists(temp_srt):
        os.remove(temp_srt)
    
    send_message(f"✅ 完成: {filename}\n字数: {len(text)} → {len(corrected)}")
    return True

def main():
    global TARGET
    
    # 检查依赖
    if not check_dependencies():
        print("❌ 依赖检查失败，请手动安装")
        sys.exit(1)
    
    parser = argparse.ArgumentParser(description="视频转文字稿")
    parser.add_argument("--input", "-i", required=True)
    parser.add_argument("--output", "-o", default=None)
    parser.add_argument("--model", "-m", default="small", help="Whisper 模型: tiny, small, base, medium")
    parser.add_argument("--target", "-T", default=None)
    parser.add_argument("--api-key", "-k", default=None, help="LLM API Key")
    parser.add_argument("--provider", "-p", default="minimax", 
                       choices=["minimax", "openai", "anthropic"],
                       help="LLM 提供商")
    args = parser.parse_args()
    
    if args.output is None:
        args.output = args.input
    
    TARGET = args.target
    
    # 获取 API Key
    config = LLM_PROVIDERS[args.provider]
    api_key = args.api_key or os.environ.get(config["env_key"])
    
    if not api_key:
        print(f"\n⚠️ 需要设置 {args.provider} 的 API Key")
        print(f"💡 方式1: --api-key '你的Key'")
        print(f"💡 方式2: export {config['env_key']}='你的Key'")
        print(f"\n支持的 LLM 提供商:")
        for k, v in LLM_PROVIDERS.items():
            print(f"  • {k}: {v['name']} (env: {v['env_key']})")
        sys.exit(1)
    
    video_files = get_video_files(args.input)
    if not video_files:
        print("没有找到视频")
        return
    
    print(f"🎬 找到 {len(video_files)} 个视频")
    send_message(f"🎬 开始转写！共 {len(video_files)} 个视频\nLLM: {config['name']}")
    
    for i, f in enumerate(video_files, 1):
        process_video(f, args.output, args.model, api_key, args.provider)
    
    send_message(f"🎉 全部完成！共处理 {len(video_files)} 个视频")

if __name__ == "__main__":
    TARGET = None
    main()
