"""
Podcast Generator - Agent 调用脚本

用法:
    python3 generate.py --topic "话题内容"
    python3 generate.py --topic "话题" --speed 1.2 --output /path/to/file.mp3
"""

import argparse
import json
import os
import sys
import requests
from pathlib import Path
from typing import Dict, Any
import subprocess

# 项目路径
PROJECT_DIR = Path("/home/wang/桌面/龙虾工作区/podcast-generator")
API_BASE = "http://localhost:5000"
OPENCLAW_CONFIG = Path.home() / ".openclaw" / "openclaw.json"

# IM 发送相关
OPENCLAW_GATEWAY = "http://localhost:18789"
OPENCLAW_TOKEN = None  # 从配置读取


def load_config() -> Dict[str, Any]:
    """从 openclaw.json 加载配置"""
    
    if not OPENCLAW_CONFIG.exists():
        return {"senseaudio_api_key": "", "gateway_token": ""}
    
    with open(OPENCLAW_CONFIG) as f:
        config = json.load(f)
    
    # 获取 gateway token
    gateway_token = config.get("gateway", {}).get("auth", {}).get("token", "")
    global OPENCLAW_TOKEN
    OPENCLAW_TOKEN = gateway_token
    
    return {
        "senseaudio_api_key": config.get("env", {}).get("SENSEAUDIO_API_KEY", ""),
        "gateway_token": gateway_token,
        "llm_provider": "bailian",
        "llm_model": "qwen3.5-plus",
    }


def upload_to_feishu_drive(audio_path: str, folder_token: str = None) -> Dict[str, Any]:
    """
    上传 MP3 到飞书云盘
    
    Args:
        audio_path: 音频文件路径
        folder_token: 云盘文件夹 token（从 URL 获取）
    
    Returns:
        {"success": bool, "file_token": str, "file_url": str, "error": str}
    """
    
    import os
    from requests_toolbelt import MultipartEncoder
    
    if not folder_token:
        # 使用默认文件夹
        folder_token = 'DtGffqCRTl0s3Rdv56DcAGghnyb'  # 测试云盘文件夹
    
    if not Path(audio_path).exists():
        return {"success": False, "error": "音频文件不存在"}
    
    # 从配置获取飞书 credentials
    with open(OPENCLAW_CONFIG) as f:
        config = json.load(f)
    
    feishu_config = config['channels']['feishu']['accounts']['new-channel']
    app_id = feishu_config['appId']
    app_secret = feishu_config['appSecret']
    
    # 获取 token
    token_response = requests.post(
        'https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal',
        json={'app_id': app_id, 'app_secret': app_secret}
    )
    token = token_response.json()['tenant_access_token']
    
    file_size = os.path.getsize(audio_path)
    file_name = Path(audio_path).name
    
    # 上传
    form = {
        'file_name': file_name,
        'parent_type': 'explorer',
        'parent_node': folder_token,
        'size': str(file_size),
        'file': (open(audio_path, 'rb'))
    }
    
    multi_form = MultipartEncoder(form)
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': multi_form.content_type
    }
    
    upload_response = requests.post(
        'https://open.feishu.cn/open-apis/drive/v1/files/upload_all',
        headers=headers,
        data=multi_form
    )
    
    result = upload_response.json()
    
    if result.get('code') == 0:
        file_token = result['data']['file_token']
        return {
            "success": True,
            "file_token": file_token,
            "file_url": f"https://my.feishu.cn/drive/file/{file_token}",
        }
    else:
        return {
            "success": False,
            "error": result.get('msg', '上传失败'),
        }

def detect_im_channel() -> str:
    """检测当前 IM 渠道"""
    
    # 从环境变量或 runtime context 检测
    channel = os.getenv("OPENCLAW_CHANNEL", "")
    
    if not channel:
        # 尝试从 runtime context 读取
        context_file = Path("/tmp/openclaw-runtime-context.json")
        if context_file.exists():
            try:
                with open(context_file) as f:
                    context = json.load(f)
                channel = context.get("channel", "")
            except:
                pass
    
    return channel

def convert_to_opus(mp3_path: str) -> str:
    """将 MP3 转换为飞书支持的 OPUS 格式"""
    
    import subprocess
    
    opus_path = mp3_path.replace('.mp3', '.opus')
    
    # FFmpeg 转换
    result = subprocess.run(
        [
            'ffmpeg', '-i', mp3_path,
            '-acodec', 'libopus', '-ac', '1', '-ar', '16000',
            opus_path, '-y'
        ],
        capture_output=True,
        text=True,
    )
    
    if result.returncode == 0 and Path(opus_path).exists():
        return opus_path
    else:
        return None

def send_audio_to_im(audio_path: str, channel: str = None) -> Dict[str, Any]:
    """
    通过 OpenClaw Gateway 发送音频到 IM
    
    Args:
        audio_path: 音频文件路径
        channel: IM 渠道（feishu, telegram等），None表示自动检测
    
    Returns:
        {"success": bool, "error": str (if failed)}
    """
    
    # 检查文件是否存在
    if not Path(audio_path).exists():
        return {"success": False, "error": "音频文件不存在"}
    
    # 检查 gateway token
    if not OPENCLAW_TOKEN:
        return {"success": False, "error": "未配置 Gateway Token"}
    
    # 读取音频文件为 base64
    import base64
    with open(audio_path, "rb") as f:
        audio_data = f.read()
    audio_base64 = base64.b64encode(audio_data).decode()
    
    # 通过 OpenClaw message API 发送
    # 使用 subprocess 调用 openclaw CLI（更可靠）
    try:
        # 构建消息内容
        message_content = f"🎙️ 播客已生成！\n时长: {len(audio_data) / 32000 / 2:.1f} 秒\n\n[音频附件]"
        
        # 方案 A: 使用 subprocess 调用 openclaw
        # 注意：这里需要知道当前对话的 chat_id，通常从环境变量或 runtime context 获取
        # 在 OpenClaw agent 环境中，会有 OPENCLAW_CHAT_ID 环境变量
        
        chat_id = os.getenv("OPENCLAW_CHAT_ID", "")
        if not chat_id:
            # 尝试从 runtime context 读取
            context_file = Path("/tmp/openclaw-runtime-context.json")
            if context_file.exists():
                try:
                    with open(context_file) as f:
                        context = json.load(f)
                    chat_id = context.get("chat_id", "")
                except:
                    pass
        
        if not chat_id:
            return {"success": False, "error": "未检测到 IM 渠道（本地调用）"}
        
        # 发送音频文件
        # 使用 message 工具 API
        result = subprocess.run(
            [
                "openclaw", "message", "send",
                "--channel", channel or "feishu",
                "--chatId", chat_id,
                "--message", message_content,
                "--file", audio_path,
            ],
            capture_output=True,
            text=True,
            timeout=30,
        )
        
        if result.returncode == 0:
            return {"success": True, "message": "音频已发送"}
        else:
            # 尝试备用方案：直接用 Gateway API
            return {"success": False, "error": f"发送失败: {result.stderr}"}
            
    except subprocess.TimeoutExpired:
        return {"success": False, "error": "发送超时"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def check_server() -> bool:
    """检查服务是否运行"""
    
    try:
        response = requests.get(f"{API_BASE}/api/config", timeout=3)
        return response.status_code == 200
    except:
        return False


def start_server() -> bool:
    """启动服务"""
    
    import subprocess
    import time
    
    # 检查是否已运行
    if check_server():
        return True
    
    # 启动 Flask
    process = subprocess.Popen(
        ["python3", str(PROJECT_DIR / "backend" / "app.py")],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    
    # 等待启动
    for _ in range(10):
        time.sleep(1)
        if check_server():
            return True
    
    return False


def generate_podcast(
    topic: str,
    api_key: str,
    speed: float = 1.0,
    pitch_male: int = 0,
    pitch_female: int = 2,
    male_voice: str = "male_0004_a",
    female_voice: str = "female_0001_a",
    use_llm: bool = True,
    output: str = None,
    send_to_im: bool = True,  # 是否发送到 IM
    im_channel: str = None,   # IM 渠道（自动检测）
) -> Dict[str, Any]:
    """
    调用 API 生成播客
    
    Args:
        topic: 话题内容
        api_key: SenseAudio API Key
        speed: 语速 0.5-2.0
        pitch_male: 男声语调 -12~12
        pitch_female: 女声语调 -12~12
        male_voice: 男声音色 ID
        female_voice: 女声音色 ID
        use_llm: 是否用 LLM 生成脚本
        output: 输出文件路径（可选）
    
    Returns:
        {
            "success": bool,
            "audio_path": str,
            "duration_seconds": float,
            "segments": list,
            "error": str (if failed)
        }
    """
    
    # 确保服务运行
    if not check_server():
        if not start_server():
            return {
                "success": False,
                "error": "无法启动播客生成器服务",
            }
    
    # 构建请求
    request_data = {
        "topic": topic,
        "speed": speed,
        "pitch_male": pitch_male,
        "pitch_female": pitch_female,
        "male_voice": male_voice,
        "female_voice": female_voice,
        "use_llm": use_llm,
    }
    
    try:
        # 调用 API
        response = requests.post(
            f"{API_BASE}/api/generate",
            headers={
                "Content-Type": "application/json",
                "X-API-Key": api_key,
            },
            json=request_data,
            timeout=180,
        )
        
        data = response.json()
        
        if not data.get("success"):
            return {
                "success": False,
                "error": data.get("error", "生成失败"),
            }
        
        # 下载音频文件
        download_url = f"{API_BASE}{data['download_url']}"
        audio_response = requests.get(download_url, timeout=30)
        
        if audio_response.status_code != 200:
            return {
                "success": False,
                "error": "下载音频失败",
            }
        
        # 保存音频
        if output:
            audio_path = Path(output)
        else:
            # 使用项目输出目录
            output_dir = PROJECT_DIR / "output"
            audio_path = output_dir / data["output_file"]
        
        audio_path.parent.mkdir(parents=True, exist_ok=True)
        with open(audio_path, "wb") as f:
            f.write(audio_response.content)
        
        result = {
            "success": True,
            "audio_path": str(audio_path),
            "duration_seconds": data.get("duration_seconds", 0),
            "segments": data.get("segments", []),
            "output_file": data["output_file"],
        }
        
        # IM 发送处理
        if send_to_im:
            # 检测渠道
            im_channel = detect_im_channel()
            
            # 飞书需要上传到云盘
            if im_channel == "feishu":
                drive_result = upload_to_feishu_drive(str(audio_path))
                if drive_result.get("success"):
                    result["drive_file_token"] = drive_result["file_token"]
                    result["drive_file_url"] = drive_result["file_url"]
                    result["im_message"] = f"已上传到云盘: {drive_result['file_url']}"
                else:
                    result["im_message"] = drive_result.get("error", "云盘上传失败")
            else:
                # 其他渠道直接用 mp3
                result["im_format"] = "mp3"
                result["im_message"] = f"已为 {im_channel or '本地'} 准备音频"
        
        return result
        
    except requests.exceptions.Timeout:
        return {
            "success": False,
            "error": "请求超时（生成播客可能需要较长时间）",
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
        }


def main():
    """命令行入口"""
    
    parser = argparse.ArgumentParser(
        description="播客生成器 - Agent 调用脚本",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
    python3 generate.py --topic "人工智能的未来"
    python3 generate.py --topic "话题" --speed 1.2 --pitch-male 2
    python3 generate.py --topic "话题" --output ~/podcast.mp3
        """
    )
    
    parser.add_argument(
        "--topic", "-t",
        required=True,
        help="话题内容（建议 50-200 字）",
    )
    
    parser.add_argument(
        "--speed", "-s",
        type=float,
        default=1.0,
        help="语速（0.5-2.0，默认 1.0）",
    )
    
    parser.add_argument(
        "--pitch-male", "-pm",
        type=int,
        default=0,
        help="男声语调（-12~12，默认 0）",
    )
    
    parser.add_argument(
        "--pitch-female", "-pf",
        type=int,
        default=2,
        help="女声语调（-12~12，默认 2）",
    )
    
    parser.add_argument(
        "--male-voice", "-mv",
        default="male_0004_a",
        help="男声音色 ID（默认 male_0004_a）",
    )
    
    parser.add_argument(
        "--female-voice", "-fv",
        default="female_0001_a",
        help="女声音色 ID（默认 female_0001_a）",
    )
    
    parser.add_argument(
        "--output", "-o",
        help="输出文件路径（默认自动生成）",
    )
    
    parser.add_argument(
        "--send-im",
        action="store_true",
        default=True,
        help="发送音频到 IM（默认开启，IM环境自动检测）",
    )
    
    parser.add_argument(
        "--no-send-im",
        action="store_true",
        help="不发送音频到 IM（仅保存到本地）",
    )
    
    parser.add_argument(
        "--api-key",
        help="SenseAudio API Key（默认从 openclaw.json 读取）",
    )
    
    args = parser.parse_args()
    
    # 加载配置
    config = load_config()
    api_key = args.api_key or config["senseaudio_api_key"]
    
    if not api_key:
        result = {
            "success": False,
            "error": "缺少 API Key。请在 openclaw.json 中配置 SENSEAUDIO_API_KEY",
        }
        print(json.dumps(result, ensure_ascii=False))
        sys.exit(1)
    
    # 生成播客（API 只支持 LLM 模式）
    send_to_im = not args.no_send_im
    result = generate_podcast(
        topic=args.topic,
        api_key=api_key,
        speed=args.speed,
        pitch_male=args.pitch_male,
        pitch_female=args.pitch_female,
        male_voice=args.male_voice,
        female_voice=args.female_voice,
        use_llm=True,  # API 只支持 LLM 模式
        output=args.output,
        send_to_im=send_to_im,
    )
    
    # 输出结果
    print(json.dumps(result, ensure_ascii=False))
    
    if result["success"]:
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()