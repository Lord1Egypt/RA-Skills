"""
TTS Voice Generator Skill - 文本转语音生成工具

核心功能：
1. 浏览/搜索可用声音
2. 选择声音生成语音
3. 上传自定义参考音频
4. 查询任务状态
"""

from tts_service import TTSService
import os
import json


# ============= 配置区域 =============
BASE_URL = os.getenv("TTS_API_BASE_URL", "https://www.datamass.cn/ai-back")

def get_api_key() -> str:
    """从 ~/.openclaw/config.json 读取 API Key"""
    config_path = os.path.expanduser('~/.openclaw/config.json')
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        api_key = config.get('datamass_api_key')
        if not api_key:
            raise ValueError("缺少 datamass_api_key，请在 ~/.openclaw/config.json 中配置")
        return api_key
    except FileNotFoundError:
        raise ValueError(f"配置文件不存在：{config_path}")
    except json.JSONDecodeError:
        raise ValueError(f"配置文件格式错误：{config_path}")
# ===================================


def init_service() -> TTSService:
    """初始化 TTS 服务"""
    api_key = get_api_key()
    return TTSService(BASE_URL, api_key)


def list_voices(limit: int = 20) -> dict:
    """
    获取可用声音列表（带格式化输出）

    Args:
        limit: 最多返回多少个声音

    Returns:
        {
            "success": True,
            "voices": [
                {"index": 1, "id": "...", "name": "...", "type": "...", "preview": "..."},
                ...
            ],
            "count": 10
        }
    """
    try:
        service = init_service()
        voices = service.get_voice_list()

        formatted = []
        for i, voice in enumerate(voices[:limit], 1):
            style_type = voice.get('styleType', 0)
            type_map = {1: '本人声音', 2: '定制声音'}
            formatted.append({
                "index": i,
                "id": str(voice.get('id', '')),
                "name": voice.get('styleName', '未知'),
                "type": type_map.get(style_type, f'类型{style_type}'),
                "audio_text": voice.get('audioText', ''),
                "media_path": voice.get('savedPath', '')
            })

        return {"success": True, "voices": formatted, "count": len(formatted)}
    except Exception as e:
        return {"success": False, "error": str(e)}


def show_voice_list(limit: int = 10) -> str:
    """
    显示声音列表（用于直接展示给用户）

    Returns:
        格式化的声音列表字符串
    """
    result = list_voices(limit)
    if not result["success"]:
        return f"获取失败：{result.get('error', '')}"

    if result["count"] == 0:
        return "暂无可用声音"

    lines = ["可用声音列表：", ""]
    for v in result["voices"]:
        lines.append(f"  {v['index']}. {v['name']} ({v['type']})")
        if v.get('audio_text'):
            # 只显示前 30 个字符
            preview = v['audio_text'][:30] + "..." if len(v['audio_text']) > 30 else v['audio_text']
            lines.append(f"     试听文本：{preview}")

    lines.append("")
    lines.append("💡 使用方式：")
    lines.append("  • 选择声音：说'用第 X 个声音'或'用 [声音名称]'")
    lines.append("  • 上传自定义声音：说'上传我的声音'并提供音频文件和名称")
    lines.append("")
    lines.append(f"共 {result['count']} 个声音")

    return "\n".join(lines)


def select_voice(index: int) -> dict:
    """
    根据序号选择声音

    Args:
        index: 声音序号（从 1 开始）

    Returns:
        {
            "success": True,
            "voice": {"name": "...", "media_path": "..."}
        }
    """
    result = list_voices(100)
    if not result["success"]:
        return result

    if index < 1 or index > len(result["voices"]):
        return {"success": False, "error": f"序号超出范围 (1-{len(result['voices'])})"}

    voice = result["voices"][index - 1]
    return {"success": True, "voice": voice}


def generate_speech(
    text: str,
    voice_index: int = None,
    voice_name: str = None,
    media_path: str = None,
    wait: bool = False,
    timeout: int = 300
) -> dict:
    """
    生成语音（支持多种指定声音的方式）

    Args:
        text: 要转换的文本内容
        voice_index: 声音序号（从 list_voices 返回的序号）
        voice_name: 声音名称（模糊匹配）
        media_path: 直接指定声音路径（优先级最高）
        wait: 是否等待任务完成
        timeout: 等待超时时间（秒）

    Returns:
        {"success": True, "task_id": "..."} 或 {"success": True, "audio_url": "..."}
    """
    try:
        service = init_service()

        # 确定使用哪个声音
        final_media_path = media_path

        if not final_media_path and voice_index:
            # 按序号选择
            voice_result = select_voice(voice_index)
            if voice_result["success"]:
                final_media_path = voice_result["voice"]["media_path"]

        if not final_media_path and voice_name:
            # 按名称模糊匹配
            voices = service.get_voice_list()
            for voice in voices:
                if voice_name.lower() in voice.get('styleName', '').lower():
                    final_media_path = voice.get('savedPath', '')
                    break

        if not final_media_path:
            # 默认使用第一个声音
            voices = service.get_voice_list()
            if voices:
                final_media_path = voices[0].get('savedPath', '')

        if not final_media_path:
            return {"success": False, "error": "没有可用声音，请先上传参考音频"}

        # 提交任务
        result = service.generate_speech(
            text=text,
            media_path=final_media_path,
            workflow_id='76'
        )

        if not result['success']:
            return result

        if wait:
            wait_result = service.wait_for_task(
                result['task_id'],
                max_attempts=timeout // 5,
                interval=5
            )
            return wait_result

        return {"success": True, "task_id": result['task_id']}

    except Exception as e:
        return {"success": False, "error": str(e)}


def check_task_status(task_id: str) -> dict:
    """
    检查任务状态
    """
    try:
        service = init_service()
        result = service.check_task_status(task_id)
        return {"success": True, **result}
    except Exception as e:
        return {"success": False, "error": str(e)}


def upload_audio(file_path: str, style_name: str = "", audio_text: str = "") -> dict:
    """
    上传音频文件作为参考声音

    Args:
        file_path: 本地音频文件路径
        style_name: 声音名称
        audio_text: 音频对应的文本内容

    Returns:
        {"success": True, "audio_url": "..."}
    """
    try:
        service = init_service()
        result = service.upload_audio(file_path, style_name, audio_text)
        if result['success']:
            return {"success": True, "audio_url": result['audio_url']}
        return result
    except Exception as e:
        return {"success": False, "error": str(e)}


def add_custom_voice(audio_url: str, style_name: str, audio_text: str) -> dict:
    """
    添加定制声音（保存参考音频记录）

    Args:
        audio_url: 上传后返回的 OSS URL
        style_name: 声音名称
        audio_text: 音频中读的文本内容

    Returns:
        {"success": True, "message": "声音添加成功"}
    """
    try:
        service = init_service()
        result = service.add_custom_voice(
            audio_url=audio_url,
            style_name=style_name,
            audio_text=audio_text,
            style_type=2
        )
        if result['success']:
            return {"success": True, "message": "声音添加成功"}
        return result
    except Exception as e:
        return {"success": False, "error": str(e)}


def upload_and_add(file_path: str, style_name: str, audio_text: str) -> dict:
    """
    完整流程：上传音频并添加为定制声音

    Args:
        file_path: 本地音频文件路径
        style_name: 声音名称
        audio_text: 音频中读的文本内容

    Returns:
        {"success": True, "message": "...", "voice_index": N}
    """
    # 步骤 1：上传音频并保存到数据库（一步完成）
    upload_result = upload_audio(file_path, style_name, audio_text)
    if not upload_result["success"]:
        return upload_result

    # 步骤 2：获取新声音的序号
    list_result = list_voices(100)
    voice_index = None
    if list_result["success"]:
        for i, v in enumerate(list_result["voices"], 1):
            if v["name"] == style_name:
                voice_index = i
                break

    return {
        "success": True,
        "message": f"✅ 声音'{style_name}'已保存成功！现在可以说'用 {style_name} 生成：[文本]'来使用",
        "voice_index": voice_index
    }

