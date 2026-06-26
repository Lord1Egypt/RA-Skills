"""
TTS 语音生成器 - ClawHub Skill 入口脚本

使用方法:
    python tts_generator.py list_voices     # 获取声音列表
    python tts_generator.py generate "文本" # 生成语音
    python tts_generator.py upload file.wav # 上传音频
    python tts_generator.py status taskId   # 查询状态
"""

import sys
import os
import json

# 添加父目录到路径，便于导入 tts_service
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tts_service import TTSService


def get_config():
    """获取配置"""
    config_path = os.path.expanduser('~/.openclaw/config.json')
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        return config.get('datamass_api_key'), config.get('download_tool_base_url', 'https://www.datamass.cn/ai-back')
    except Exception as e:
        print(f"读取配置失败：{e}")
        return None, None


def list_voices():
    """获取声音列表"""
    api_key, base_url = get_config()
    if not api_key:
        print("错误：请配置 API Key")
        return
    
    service = TTSService(base_url, api_key)
    voices = service.get_voice_list()
    
    print(f"\n共 {len(voices)} 个声音:\n")
    for i, voice in enumerate(voices[:20], 1):  # 只显示前 20 个
        style_name = voice.get('styleName', 'N/A')
        style_type = voice.get('styleType', 'N/A')
        type_map = {1: '本人声音', 2: '定制声音'}
        print(f"  {i}. {style_name} (类型：{type_map.get(style_type, style_type)})")
    
    if len(voices) > 20:
        print(f"  ... 还有 {len(voices) - 20} 个声音")


def generate_speech(text):
    """生成语音"""
    api_key, base_url = get_config()
    if not api_key:
        print("错误：请配置 API Key")
        return
    
    service = TTSService(base_url, api_key)
    
    # 获取第一个可用声音
    voices = service.get_voice_list()
    if not voices:
        print("错误：没有可用声音")
        return
    
    voice = voices[0]
    media_path = voice.get('savedPath', '')
    
    print(f"使用声音：{voice.get('styleName', 'N/A')}")
    print(f"文本：{text}")
    
    result = service.generate_speech(
        text=text,
        media_path=media_path,
        workflow_id='73'
    )
    
    if result.get('success'):
        task_id = result.get('result', '')
        print(f"\n任务已提交，Task ID: {task_id}")
        print("使用 'python tts_generator.py status {task_id}' 查询状态")
    else:
        print(f"失败：{result.get('error', '未知错误')}")


def upload_audio(file_path):
    """上传音频"""
    api_key, base_url = get_config()
    if not api_key:
        print("错误：请配置 API Key")
        return
    
    if not os.path.exists(file_path):
        print(f"错误：文件不存在：{file_path}")
        return
    
    service = TTSService(base_url, api_key)
    result = service.upload_audio(file_path, "uploaded_audio")
    
    if result.get('success'):
        print(f"上传成功：{result.get('audio_url', '')}")
    else:
        print(f"失败：{result.get('error', '未知错误')}")


def check_status(task_id):
    """查询任务状态"""
    api_key, base_url = get_config()
    if not api_key:
        print("错误：请配置 API Key")
        return
    
    service = TTSService(base_url, api_key)
    result = service.check_task_status(task_id)
    
    print(f"任务 {task_id} 状态:")
    print(f"  状态：{result.get('status', 'unknown')}")
    if result.get('status') == 'completed':
        print(f"  音频 URL: {result.get('audio_url', '')}")
    elif result.get('message'):
        print(f"  消息：{result.get('message', '')}")


def print_usage():
    """打印使用说明"""
    print(__doc__)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print_usage()
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "list_voices":
        list_voices()
    elif command == "generate" and len(sys.argv) >= 3:
        text = " ".join(sys.argv[2:])
        generate_speech(text)
    elif command == "upload" and len(sys.argv) >= 3:
        file_path = sys.argv[2]
        upload_audio(file_path)
    elif command == "status" and len(sys.argv) >= 3:
        task_id = sys.argv[2]
        check_status(task_id)
    else:
        print_usage()
        sys.exit(1)
