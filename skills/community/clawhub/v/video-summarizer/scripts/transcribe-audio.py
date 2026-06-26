#!/usr/bin/env python3
"""
transcribe-audio.py - Plan B: 语音转录字幕
三层降级方案（云端优先，本地降级）：
1. Groq API (whisper-large-v3) - 如果配置且可用
2. Faster-Whisper (CPU/GPU 自适应) - Groq 不可用时本地方案
3. Whisper.cpp / OpenAI Whisper - 保底方案

用法：python3 transcribe-audio.py <音频文件> [输出字幕文件]

版本：v1.0.13
更新：移除硅基流动依赖，Groq API 为可选配置
"""

import sys
import os
import json
import subprocess
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path.home() / '.openclaw' / '.env')

# 配置
GROQ_API_KEY = os.getenv('GROQ_API_KEY')
WHISPER_MODEL = os.getenv('WHISPER_MODEL', 'base')  # faster-whisper 模型：tiny/base/small/medium/large
WHISPER_CPP_MODEL = os.getenv('WHISPER_CPP_MODEL', 'base')
FORCE_LOCAL = os.getenv('USE_LOCAL_WHISPER', 'false').lower() == 'true'


def check_gpu():
    """检测 GPU 可用性，返回 (可用，显存 GB, 设备名)"""
    try:
        result = subprocess.run(
            ['nvidia-smi', '--query-gpu=name,memory.total', '--format=csv,noheader,nounits'],
            capture_output=True, text=True, timeout=10
        )
        if result.returncode == 0:
            lines = result.stdout.strip().split('\n')
            if lines:
                parts = lines[0].split(', ')
                gpu_name = parts[0]
                vram_gb = int(parts[1]) / 1024  # MB → GB
                return True, vram_gb, gpu_name
    except:
        pass
    return False, 0, None


def select_faster_whisper_model(vram_gb: float):
    """根据显存选择 Faster-Whisper 模型"""
    if vram_gb >= 8:
        return 'large-v2', 'GPU'
    elif vram_gb >= 4:
        return 'medium', 'GPU'
    elif vram_gb >= 2:
        return 'small', 'GPU'
    elif vram_gb >= 1:
        return 'base', 'GPU'
    else:
        # CPU 模式
        return 'base', 'CPU'


def transcribe_with_faster_whisper(audio_file: str) -> dict:
    """使用 Faster-Whisper 转录（第二方案）"""
    try:
        from faster_whisper import WhisperModel
        
        # GPU 检测
        has_gpu, vram_gb, gpu_name = check_gpu()
        
        if has_gpu:
            model_size, device = select_faster_whisper_model(vram_gb)
            print(f"   🖥️ Faster-Whisper | 设备：{device} ({gpu_name}, {vram_gb:.1f}GB) | 模型：{model_size}")
        else:
            model_size, device = 'base', 'CPU'
            print(f"   🖥️ Faster-Whisper | 设备：CPU (无 GPU) | 模型：{model_size}")
        
        # 加载模型
        device_arg = "cuda" if has_gpu else "cpu"
        compute_type = "float16" if has_gpu else "int8"
        
        model = WhisperModel(model_size, device=device_arg, compute_type=compute_type)
        
        # 转录（添加标点参数）
        segments, info = model.transcribe(
            audio_file, 
            language='zh', 
            vad_filter=True,
            initial_prompt="请添加适当的标点符号，使文本更易读。"  # 提示添加标点
        )
        
        # 收集结果
        text_parts = []
        segs_list = []
        for seg in segments:
            text_parts.append(seg.text)
            segs_list.append({
                'start': seg.start,
                'end': seg.end,
                'text': seg.text.strip()
            })
        
        return {
            'success': True,
            'text': ''.join(text_parts),
            'segments': segs_list,
            'language': info.language,
            'model': f"faster-whisper/{model_size}"
        }
        
    except ImportError:
        return {
            'success': False,
            'error': "Faster-Whisper 未安装，运行：pip install faster-whisper"
        }
    except Exception as e:
        return {
            'success': False,
            'error': f"Faster-Whisper 失败：{str(e)}"
        }


def transcribe_with_groq(audio_file: str) -> dict:
    """使用 Groq API 转录（第一方案）"""
    import requests
    
    print("   🌐 使用 Groq API 转录...")
    
    url = "https://api.groq.com/openai/v1/audio/transcriptions"
    headers = {"Authorization": f"Bearer {GROQ_API_KEY}"}
    
    try:
        with open(audio_file, 'rb') as f:
            files = {"file": f}
            data = {"model": "whisper-large-v3", "response_format": "verbose_json"}
            response = requests.post(url, headers=headers, files=files, data=data, timeout=600)
    except requests.exceptions.Timeout:
        return {'success': False, 'error': 'Groq API 超时'}
    except requests.exceptions.ConnectionError as e:
        return {'success': False, 'error': f'Groq API 连接失败：{str(e)[:200]}'}
    except requests.exceptions.SSLError as e:
        return {'success': False, 'error': f'Groq API SSL 错误：{str(e)[:200]}'}
    except requests.exceptions.RequestException as e:
        return {'success': False, 'error': f'Groq API 请求异常：{str(e)[:200]}'}
    
    if response.status_code == 200:
        result = response.json()
        return {
            'success': True,
            'text': result.get('text', ''),
            'segments': result.get('segments', [])
        }
    else:
        return {
            'success': False,
            'error': f"Groq API 错误：{response.status_code} - {response.text[:200]}"
        }





def transcribe_with_whisper_cpp(audio_file: str) -> dict:
    """使用 Whisper.cpp 转录（保底方案）"""
    print("   🐌 使用 Whisper.cpp 转录 (保底，较慢)...")
    
    # 查找 whisper.cpp 的 main 程序
    whisper_cpp_paths = [
        '/usr/local/bin/whisper-cpp',
        '/usr/bin/whisper-cpp',
        os.path.expanduser('~/whisper.cpp/main'),
        os.path.expanduser('~/.local/bin/whisper-cpp')
    ]
    
    whisper_cpp = None
    for p in whisper_cpp_paths:
        if os.path.isfile(p) and os.access(p, os.X_OK):
            whisper_cpp = p
            break
    
    if not whisper_cpp:
        # 尝试查找 ggml 模型
        for model_name in ['base', 'small', 'medium']:
            model_path = os.path.expanduser(f'~/whisper.cpp/models/ggml-{model_name}.bin')
            if os.path.exists(model_path):
                whisper_cpp = os.path.expanduser('~/whisper.cpp/main')
                WHISPER_CPP_MODEL = model_name
                break
    
    if not whisper_cpp or not os.path.exists(whisper_cpp):
        return {
            'success': False,
            'error': "Whisper.cpp 未找到，请安装：git clone https://github.com/ggerganov/whisper.cpp"
        }
    
    # 使用 openai-whisper 作为 whisper.cpp 的替代保底
    try:
        import whisper
        print("   🐌 使用 OpenAI Whisper (本地保底)...")
        model = whisper.load_model('base')
        result = model.transcribe(audio_file, language='zh')
        return {
            'success': True,
            'text': result.get('text', ''),
            'segments': result.get('segments', [])
        }
    except:
        return {
            'success': False,
            'error': "Whisper.cpp 和 OpenAI Whisper 均不可用"
        }


def segments_to_vtt(segments: list, output_file: str):
    """将转录片段转换为 VTT 字幕格式"""
    def format_time(seconds: float) -> str:
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        millis = int((seconds % 1) * 1000)
        return f"{hours:02d}:{minutes:02d}:{secs:02d}.{millis:03d}"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("WEBVTT\n\n")
        for i, seg in enumerate(segments, 1):
            start = format_time(seg.get('start', 0))
            end = format_time(seg.get('end', 0))
            text = seg.get('text', '').strip()
            if text:
                f.write(f"{i}\n{start} --> {end}\n{text}\n\n")


def main():
    if len(sys.argv) < 2:
        print("用法：python3 transcribe-audio.py <音频文件> [输出字幕文件]")
        sys.exit(1)
    
    audio_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else audio_file.rsplit('.', 1)[0] + '.vtt'
    
    if not os.path.exists(audio_file):
        print(f"❌ 音频文件不存在：{audio_file}")
        sys.exit(1)
    
    print("=" * 60)
    print("🎤 语音转录 (Plan B) - 三层降级方案")
    print("=" * 60)
    print()
    
    # GPU 检测
    has_gpu, vram_gb, gpu_name = check_gpu()
    if has_gpu:
        print(f"📊 GPU: {gpu_name} ({vram_gb:.1f}GB)")
    else:
        print("📊 GPU: 未检测到 (使用 CPU)")
    print()
    
    # 三层降级逻辑：Groq API → Faster-Whisper → Whisper.cpp
    result = {'success': False, 'error': '未尝试'}
    
    # 方案 1: Groq API (如果配置了 Key)
    if GROQ_API_KEY and GROQ_API_KEY.strip():
        print("【方案 1/3】Groq API (whisper-large-v3)")
        result = transcribe_with_groq(audio_file)
        
        if result['success']:
            print("   ✅ 成功")
        else:
            print(f"   ❌ 失败：{result['error']}")
            print("   → 降级到本地 Faster-Whisper")
    else:
        print("⚠️  未配置 GROQ_API_KEY，跳过 Groq API")
    
    # 方案 2: Faster-Whisper (本地，Groq 不可用时使用)
    if not result['success']:
        print("\n【方案 2/3】Faster-Whisper (本地)")
        result = transcribe_with_faster_whisper(audio_file)
        
        if result['success']:
            print(f"   ✅ 成功 | 模型：{result.get('model', 'unknown')}")
        else:
            print(f"   ❌ 失败：{result['error']}")
            print("   → 降级到 Whisper.cpp 保底")
    
    # 方案 3: Whisper.cpp / OpenAI Whisper (保底)
    if not result['success']:
        print("\n【方案 3/3】Whisper 本地保底")
        result = transcribe_with_whisper_cpp(audio_file)
        
        if result['success']:
            print("   ✅ 成功")
        else:
            print(f"   ❌ 失败：{result['error']}")
    
    print()
    print("=" * 60)
    
    if result['success']:
        print(f"✅ 转录成功 | 文本长度：{len(result['text'])} 字符 | 片段数：{len(result['segments'])}")
        
        # 保存 VTT
        segments_to_vtt(result['segments'], output_file)
        print(f"📄 字幕已保存：{output_file}")
        
        # 同时保存纯文本
        txt_file = output_file.rsplit('.', 1)[0] + '.txt'
        with open(txt_file, 'w', encoding='utf-8') as f:
            f.write(result['text'])
        print(f"📄 文本已保存：{txt_file}")
    else:
        print(f"❌ 所有方案均失败：{result['error']}")
        sys.exit(1)
    
    print()


if __name__ == '__main__':
    main()
