#!/usr/bin/env python3
"""
音频转录脚本
支持多种ASR服务：OpenAI Whisper API、阿里云、讯飞等
"""

import json
import sys
import os

def transcribe_with_openai_whisper(audio_path, api_key=None):
    """使用 OpenAI Whisper API 转录"""
    try:
        import openai
    except ImportError:
        print("请先安装: pip install openai")
        return None
    
    client = openai.OpenAI(api_key=api_key or os.environ.get("OPENAI_API_KEY"))
    
    with open(audio_path, "rb") as audio_file:
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
            response_format="verbose_json",
            timestamp_granularities=["segment"]
        )
    
    # 转换为统一格式
    result = {
        "segments": [
            {"start": seg.start, "end": seg.end, "text": seg.text}
            for seg in transcript.segments
        ]
    }
    return result

def transcribe_with_alibaba(audio_path, appkey=None, token=None):
    """使用阿里云语音识别 API"""
    # TODO: 实现阿里云ASR
    print("阿里云ASR尚未实现，请选择其他方案")
    return None

def transcribe_with_xfyun(audio_path, appid=None, api_key=None, api_secret=None):
    """使用讯飞语音识别 API"""
    # TODO: 实现讯飞ASR
    print("讯飞ASR尚未实现，请选择其他方案")
    return None

def transcribe_with_local_whisper(audio_path, model="tiny"):
    """使用 faster-whisper 本地转录（更快更轻量）"""
    try:
        from faster_whisper import WhisperModel
    except ImportError:
        print("请先安装: pip install faster-whisper")
        return None
    
    # 设置 HuggingFace 镜像（国内加速）
    os.environ.setdefault("HF_ENDPOINT", "https://hf-mirror.com")
    
    print(f"加载 faster-whisper 模型: {model}...")
    # device="cpu", compute_type="int8" 适合无 GPU 环境
    whisper_model = WhisperModel(model, device="cpu", compute_type="int8")
    
    print("转录中...")
    segments, info = whisper_model.transcribe(audio_path, language="zh")
    
    # 转换为统一格式
    result_segments = [
        {"start": seg.start, "end": seg.end, "text": seg.text.strip()}
        for seg in segments
    ]
    print(f"转录完成，共 {len(result_segments)} 个片段")
    return {"segments": result_segments}

def transcribe(audio_path, method="local", **kwargs):
    """
    统一转录接口
    
    参数:
        audio_path: 音频文件路径
        method: 转录方法 (openai/local/alibaba/xfyun)
        **kwargs: 各方法所需的参数
    
    返回:
        {"segments": [{"start": float, "end": float, "text": str}, ...]}
    """
    if not os.path.exists(audio_path):
        print(f"错误: 音频文件不存在: {audio_path}")
        return None
    
    if method == "openai":
        return transcribe_with_openai_whisper(audio_path, kwargs.get("api_key"))
    elif method == "local":
        return transcribe_with_local_whisper(audio_path, kwargs.get("model", "base"))
    elif method == "alibaba":
        return transcribe_with_alibaba(audio_path, kwargs.get("appkey"), kwargs.get("token"))
    elif method == "xfyun":
        return transcribe_with_xfyun(audio_path, kwargs.get("appid"), kwargs.get("api_key"), kwargs.get("api_secret"))
    else:
        print(f"不支持的转录方法: {method}")
        return None

def main():
    if len(sys.argv) < 2:
        print("使用方法: python transcribe_audio.py <音频文件> [方法] [参数]")
        print("方法: local(默认), openai, alibaba, xfyun")
        print("")
        print("示例:")
        print("  python transcribe_audio.py audio.wav local")
        print("  python transcribe_audio.py audio.wav openai --api-key YOUR_KEY")
        print("  python transcribe_audio.py audio.wav local --model small")
        sys.exit(1)
    
    audio_path = sys.argv[1]
    method = sys.argv[2] if len(sys.argv) > 2 else "local"
    
    # 解析额外参数
    kwargs = {}
    args = sys.argv[3:]
    for i in range(0, len(args), 2):
        key = args[i].replace("--", "").replace("-", "_")
        value = args[i + 1] if i + 1 < len(args) else None
        if value:
            kwargs[key] = value
    
    print(f"音频文件: {audio_path}")
    print(f"转录方法: {method}")
    print("")
    
    result = transcribe(audio_path, method, **kwargs)
    
    if result:
        # 保存结果
        output_path = audio_path.replace(".wav", "_transcript.json")
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"\n转录完成，结果保存到: {output_path}")
        
        # 打印摘要
        print("\n=== 转录摘要 ===")
        for seg in result["segments"]:
            print(f"[{seg['start']:.1f}s - {seg['end']:.1f}s] {seg['text']}")
    else:
        print("转录失败")
        sys.exit(1)

if __name__ == "__main__":
    main()
