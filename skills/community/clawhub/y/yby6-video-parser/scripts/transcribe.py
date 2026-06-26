"""
视频转录模块
提供从视频中提取音频并转录为文本的功能
"""
import os
import subprocess
import requests
import uuid
import re
import sys
from pathlib import Path
from urllib.parse import quote
from datetime import datetime

# 默认配置
DEFAULT_API_BASE_URL = "https://api.siliconflow.cn/v1/audio/transcriptions"
DEFAULT_MODEL = "FunAudioLLM/SenseVoiceSmall"
USER_AGENT = "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) EdgiOS/121.0.2277.107 Version/17.0 Mobile/15E148 Safari/604.1"


def parse_video_url_local(share_url):
    """
    使用本地解析器解析视频 URL
    
    Args:
        share_url: 视频分享链接
        
    Returns:
        解析结果字典，格式与外部 API 一致
    """
    try:
        # 动态导入避免循环依赖
        import skill
        parse_result = skill.parse_video_by_url_sync(share_url)
        
        # 转换为与外部 API 一致的格式
        return {
            "code": 200,
            "msg": "success",
            "data": parse_result
        }
    except Exception as e:
        return {
            "code": 500,
            "msg": f"解析视频分享链接失败: {str(e)}",
            "data": None
        }


def load_env(env_path):
    """
    手动读取 .env 文件
    """
    env_vars = {}
    if os.path.exists(env_path):
        with open(env_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    key, value = line.split('=', 1)
                    env_vars[key.strip()] = value.strip()
    return env_vars


def create_tmp_dir(title):
    """
    创建临时目录，命名为 tmp/视频标题
    """
    # 清理文件名中的非法字符，包括换行符
    safe_title = re.sub(r'[\\/:*?"<>|\n\r\t]', '_', title)[:50]  # 限制长度
    tmp_dir = Path("tmp") / safe_title
    tmp_dir.mkdir(parents=True, exist_ok=True)
    return tmp_dir


def save_to_markdown(result, original_url, output_dir=None):
    """
    将处理结果保存为 Markdown 文件
    """
    # 如果未指定目录，使用 demos 目录
    if output_dir is None:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        output_dir = os.path.join(os.path.dirname(script_dir), "demos")

    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)

    parse_data = result.get("parse_info", {})
    if not parse_data or parse_data.get("code") != 200:
        return None

    data = parse_data.get("data", {})
    title = data.get("title", "未命名视频")
    author = data.get("author", {}).get("name", "未知作者")
    cover_url = data.get("cover_url", "")
    transcription = result.get("transcription", "无转录内容")

    # 清理文件名中的非法字符，包括换行符
    safe_title = re.sub(r'[\\/:*?"<>|\n\r\t]', '_', title)
    filename = f"{safe_title}.md"
    file_path = os.path.join(output_dir, filename)

    md_content = f"""# {title}

## 基本信息
- **作者**: {author}
- **原始链接**: [{original_url}]({original_url})
- **封面**: 
![封面图]({cover_url})

## 临时视频文件存放路径
- **视频文件**: yby6-video-parser\tmp\{safe_title}\video.mp4
- **音频文件**: yby6-video-parser\tmp\{safe_title}\audio.mp3


## 🎙️ 语音转录内容
{transcription}

## 🔍 原始解析信息
```json
{parse_data}
```

---
*生成时间: {datetime.fromtimestamp(Path(file_path).stat().st_mtime).strftime('%Y-%m-%d %H:%M:%S') if os.path.exists(file_path) else datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(md_content)

    return file_path


def download_video(video_url, output_path):
    """
    下载视频文件到本地
    """
    print(f"正在下载视频: {video_url} -> {output_path}")
    headers = {"User-Agent": USER_AGENT}
    try:
        response = requests.get(video_url, headers=headers, stream=True, timeout=300)
        response.raise_for_status()
        with open(output_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        print("视频下载完成")
        return True
    except Exception as e:
        print(f"下载视频失败: {e}")
        return False


def extract_audio(video_path, audio_path):
    """
    使用 ffmpeg 从视频中提取音频 (mp3)
    """
    print(f"正在提取音频: {video_path} -> {audio_path}")
    try:
        # ffmpeg 参数: -i 输入文件 -vn 不处理视频 -acodec libmp3lame 音频编码 -ar 16000 采样率 -ac 1 声道 -y 覆盖输出
        cmd = [
            "ffmpeg", "-i", str(video_path),
            "-vn", "-acodec", "libmp3lame",
            "-ar", "16000", "-ac", "1",
            "-y", str(audio_path)
        ]
        # 运行 ffmpeg 命令
        result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='ignore')
        if result.returncode != 0:
            print(f"ffmpeg 提取音频失败: {result.stderr}")
            return False
        print("音频提取完成")
        return True
    except Exception as e:
        print(f"提取音频异常: {e}")
        return False


def transcribe_audio(audio_path, api_key, model=DEFAULT_MODEL):
    """
    调用 SiliconFlow API 转录音频为文本
    """
    print(f"正在调用语音识别 API 提取文本 (模型: {model})...")
    try:
        headers = {
            "Authorization": f"Bearer {api_key}"
        }
        files = {
            "file": (os.path.basename(audio_path), open(audio_path, "rb"), "audio/mpeg")
        }
        data = {
            "model": model
        }
        response = requests.post(DEFAULT_API_BASE_URL, headers=headers, files=files, data=data, timeout=600)
        response.raise_for_status()

        result = response.json()
        if "text" in result:
            print("文本提取成功")
            return result["text"]
        else:
            print(f"API 响应中没有找到 text 字段: {result}")
            return str(result)
    except Exception as e:
        print(f"语音转录失败: {e}")
        return None


def process_video_transcription(video_url_to_parse, api_key, model=DEFAULT_MODEL, parse_result=None, auto_cleanup=None, use_local_parser=None):
    """
    核心流程: 解析URL -> 下载视频 -> 提取音频 -> 转录文本

    Args:
        video_url_to_parse: 视频分享链接
        api_key: SiliconFlow API 密钥
        model: 语音识别模型（默认: FunAudioLLM/SenseVoiceSmall）
        parse_result: 已有的解析结果（可选，如果已解析过可跳过第一步）
        auto_cleanup: 是否自动清理临时文件（None: 从 .env 读取, True: 清理, False: 保留）
        use_local_parser: 是否使用本地解析器（None: 从 .env 读取, True: 本地解析, False: 外部 API）

    Returns:
        包含解析信息和转录文本的字典
    """
    # 读取环境配置
    script_dir = os.path.dirname(os.path.abspath(__file__))
    env_path = os.path.join(os.path.dirname(script_dir), ".env")
    env_vars = load_env(env_path)

    # 确定是否自动清理临时文件
    if auto_cleanup is None:
        auto_cleanup = env_vars.get("auto_cleanup_temp_files", "false").lower() == "true"

    # 确定是否使用本地解析器
    if use_local_parser is None:
        # 优先使用本地解析器，除非明确配置了外部 API
        use_local_parser = not env_vars.get("parse_api_url", "").strip()

    # 如果没有提供解析结果，先解析视频
    if parse_result is None:
        print(f"正在解析视频 URL: {video_url_to_parse}")
        if use_local_parser:
            # 使用本地解析器
            parse_result = parse_video_url_local(video_url_to_parse)
            if parse_result.get("code") != 200:
                print(f"解析失败: {parse_result.get('msg')}")
                return {"error": parse_result.get('msg')}
        else:
            # 使用外部 API
            parse_api_url = env_vars.get("parse_api_url", "")
            full_parse_url = f"{parse_api_url}{quote(video_url_to_parse)}"
            try:
                response = requests.get(full_parse_url, timeout=30)
                response.raise_for_status()
                parse_result = response.json()

                if parse_result.get("code") != 200:
                    print(f"解析失败: {parse_result.get('msg')}")
                    return {"error": parse_result.get('msg')}
            except Exception as e:
                print(f"解析视频失败: {e}")
                return {"error": str(e)}

    # 获取视频标题用于创建临时目录
    data = parse_result.get("data", {})
    title = data.get("title", "未命名视频")
    tmp_dir = create_tmp_dir(title)

    # 结果字典
    final_result = {
        "parse_info": parse_result,
        "transcription": None
    }

    # 检查是否有视频 URL
    video_url = data.get("video_url")

    # 如果存在视频 URL, 则进行转录
    if video_url:
        # 创建临时文件
        temp_id = uuid.uuid4().hex

        video_file = tmp_dir / f"video_{temp_id}.mp4"
        audio_file = tmp_dir / f"audio_{temp_id}.mp3"

        try:
            # 下载
            if download_video(video_url, video_file):
                # 提取音频
                if extract_audio(video_file, audio_file):
                    # 转录
                    text = transcribe_audio(audio_file, api_key, model)
                    final_result["transcription"] = text
        finally:
            # 根据 auto_cleanup 配置决定是否删除临时文件
            if auto_cleanup:
                # 自动清理临时文件
                if video_file.exists():
                    video_file.unlink()
                    print(f"已删除临时视频文件: {video_file}")
                if audio_file.exists():
                    audio_file.unlink()
                    print(f"已删除临时音频文件: {audio_file}")
                # 如果临时目录为空，则删除目录
                try:
                    if not any(tmp_dir.iterdir()):
                        tmp_dir.rmdir()
                        print(f"已删除空的临时目录: {tmp_dir}")
                except:
                    pass
            else:
                # 保留临时文件在 tmp/视频标题 目录中
                print(f"临时文件已保存到: {tmp_dir}")
    else:
        print("未找到 video_url，跳过转录流程 (可能是图文笔记)")

    return final_result


# 命令行入口
import argparse
import json


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="解析视频链接并转录音频。")
    parser.add_argument("--url", required=True, help="要解析的视频分享链接。")
    parser.add_argument("--api_key", help="SiliconFlow API 密钥。如果未提供，将从 .env 文件中读取。")
    parser.add_argument("--model", help="要使用的语音识别模型。")
    parser.add_argument("--parse_result", help="已解析的结果 JSON 字符串（可选，如果已解析过可跳过解析步骤）。")
    parser.add_argument("--auto_cleanup", help="是否自动清理临时文件（true/false），默认从 .env 读取。")
    parser.add_argument("--use_local_parser", help="是否使用本地解析器（true/false），默认从 .env 读取。")

    args = parser.parse_args()

    # 尝试从 .env 加载配置
    script_dir = os.path.dirname(os.path.abspath(__file__))
    env_file = os.path.join(os.path.dirname(script_dir), ".env")
    env_config = load_env(env_file)

    # 优先级：命令行参数 > .env 文件 > 默认值
    video_url = args.url
    api_key = args.api_key or env_config.get("api_key")
    model = args.model or env_config.get("model", DEFAULT_MODEL)

    # 解析 auto_cleanup 参数
    if args.auto_cleanup:
        auto_cleanup = args.auto_cleanup.lower() == "true"
    else:
        auto_cleanup = env_config.get("auto_cleanup_temp_files", "false").lower() == "true"

    # 解析 use_local_parser 参数
    if args.use_local_parser:
        use_local_parser = args.use_local_parser.lower() == "true"
    else:
        use_local_parser = not env_config.get("parse_api_url", "").strip()

    # 解析 parse_result 参数（如果有）
    parse_result = None
    if args.parse_result:
        try:
            parse_result = json.loads(args.parse_result)
        except json.JSONDecodeError as e:
            print(f"解析 parse_result 参数失败: {e}")
            sys.exit(1)

    if not api_key:
        print("错误: 未提供 api_key。请通过命令行参数传递或在 .env 文件中设置。")
        sys.exit(1)
    
    
    url_reg = re.compile(r"http[s]?:\/\/[\w.-]+[\w\/-]*[\w.-]*\??[\w=&:\-\+\%]*[/]*")  # pyright: ignore[reportUnreachable]
    share_url = url_reg.search(args.url).group()
    
    result = process_video_transcription(
        video_url_to_parse=share_url,
        api_key=api_key,
        model=model,
        parse_result=parse_result,
        auto_cleanup=auto_cleanup,
        use_local_parser=use_local_parser
    )

    print("\n--- 处理结果 ---")
    print(json.dumps(result, ensure_ascii=False, indent=2))

    # 自动保存为 Markdown
    md_file = save_to_markdown(result, share_url)
    if md_file:
        print(f"\n✅ 已生成 Markdown 文档: {os.path.abspath(md_file)}")

