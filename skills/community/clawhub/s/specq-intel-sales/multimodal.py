"""
multimodal.py — SpecQ v2.0 多模态输入模块
图片 OCR / 语音转录 / 视频关键帧提取
"""
import os
import warnings


async def process_image(image_path: str) -> str:
    """OCR 提取图片文字，返回文本。"""
    if not os.path.exists(image_path):
        return ""
    try:
        from PIL import Image
        import pytesseract
        img = Image.open(image_path)
        text = pytesseract.image_to_string(img, lang="chi_sim+eng")
        return text.strip() or f"[图片无文字: {os.path.basename(image_path)}]"
    except ImportError:
        return f"[图片: {os.path.basename(image_path)}]（pytesseract 未安装，跳过 OCR）"
    except Exception as e:
        return f"[图片 OCR 失败: {os.path.basename(image_path)} - {e}]"


async def process_audio(audio_path: str) -> str:
    """语音转文字，返回文本。"""
    if not os.path.exists(audio_path):
        return ""
    try:
        api_key = os.getenv("LLM_API_KEY") or os.getenv("DEEPSEEK_API_KEY", "")
        if not api_key:
            return f"[音频: {os.path.basename(audio_path)}]（API Key 未配置，跳过转录）"
        import openai
        client = openai.OpenAI(api_key=api_key, base_url=os.getenv("LLM_BASE_URL", "https://api.deepseek.com"))
        with open(audio_path, "rb") as f:
            resp = client.audio.transcriptions.create(model="whisper-1", file=f)
        return resp.text[:2000]
    except ImportError:
        return f"[音频: {os.path.basename(audio_path)}]（openai 未安装，跳过转录）"
    except Exception as e:
        return f"[音频转录失败: {os.path.basename(audio_path)} - {e}]"


async def process_video(video_path: str) -> str:
    """提取视频关键帧 + 语音转录，返回文本摘要。"""
    warnings.warn("视频关键帧提取暂未实现，当前仅返回元数据", FutureWarning, stacklevel=2)
    if not os.path.exists(video_path):
        return ""
    fname = os.path.basename(video_path)
    try:
        import cv2
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            return f"[视频: {fname}]（无法打开）"

        fps = cap.get(cv2.CAP_PROP_FPS) or 1
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        cap.release()

        # 每 30 秒一帧的关键帧窗口
        return f"[视频: {fname}] {total_frames} 帧, {fps:.1f} fps（需 GPU 做关键帧 OCR+ASR 完整分析）"
    except ImportError:
        return f"[视频: {fname}]（cv2 未安装，跳过视频分析）"
    except Exception as e:
        return f"[视频分析失败: {fname} - {e}]"
