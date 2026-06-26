#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Video Dubbing Skill - 通用版

使用VoxCPM进行中文配音，支持：
- 分组TTS（保持连贯）
- 智能音频匹配
- 硬字幕自动检测
- 断点续传

使用方法：
    python dubbing.py <视频路径> [--config config.json]
"""

import sys, os, subprocess, numpy as np, json, argparse
from pathlib import Path
import soundfile as sf
import scipy.signal

# 禁用torch编译（避免某些环境问题）
os.environ['TORCH_COMPILE_DISABLE'] = '1'
os.environ['TORCHDYNAMO_DISABLE'] = '1'

# 默认配置（所有路径和端点均可通过环境变量覆盖）
DEFAULT_CONFIG = {
    "work_dir": os.environ.get('WORK_DIR', './workspace'),
    "voxcpm_dir": os.environ.get('VOXCPM_DIR', './VoxCPM'),
    "ffmpeg_path": os.environ.get('FFMPEG_PATH', 'ffmpeg'),
    "translate": {
        "api_url": os.environ.get('TRANSLATE_API_URL', 'https://api.siliconflow.cn/v1/chat/completions'),
        "api_key": os.environ.get('TRANSLATE_API_KEY', ''),
        "model": os.environ.get('TRANSLATE_MODEL', 'tencent/Hunyuan-MT-7B')
    },
    "vision": {
        "api_url": os.environ.get('VISION_API_URL', 'https://api.siliconflow.cn/v1/chat/completions'),
        "model": os.environ.get('VISION_MODEL', 'Qwen/Qwen2.5-VL-72B-Instruct')
    },
    "whisper": {
        "model": os.environ.get('WHISPER_MODEL', 'medium'),
        "language": os.environ.get('WHISPER_LANGUAGE', 'en')
    },
    "tts": {
        "reference_audio": os.environ.get('REFERENCE_AUDIO', './reference_audio/speaker.wav'),
        "reference_text": os.environ.get('REFERENCE_TEXT', '参考音频对应的文本内容'),
        "max_group_duration": 15.0,
        "inference_timesteps": 10,
        "cfg_value": 2.0
    },
    "subtitle": {
        "fontsize": 16,
        "fontname": "SimHei",
        "outline": 2,
        "margin_v": 20,
        "alignment": 2
    },
    "output": {
        "default_name": "dubbed",
        "video_codec": "h264_nvenc",
        "audio_codec": "aac"
    }
}


def load_config(config_path=None):
    """加载配置文件（环境变量已在DEFAULT_CONFIG中处理）"""
    config = DEFAULT_CONFIG.copy()
    
    if config_path and os.path.exists(config_path):
        with open(config_path, 'r', encoding='utf-8') as f:
            user_config = json.load(f)
            # 深度合并
            for key, value in user_config.items():
                if isinstance(value, dict) and key in config:
                    config[key].update(value)
                else:
                    config[key] = value
    
    return config


def detect_hard_subtitle(video_path, config, translate_key):
    """自动检测视频是否有硬字幕（烧录字幕）"""
    import base64
    import requests
    import re
    
    print(f"\n[*] 检测硬字幕...")
    
    work_dir = Path(config['work_dir'])
    temp_dir = work_dir / "temp"
    temp_dir.mkdir(parents=True, exist_ok=True)
    
    # 提取一帧
    frame_path = str(temp_dir / "subtitle_check.jpg")
    ffmpeg = config['ffmpeg_path']
    cmd = [ffmpeg, "-y", "-ss", "30", "-i", video_path, "-vframes", "1", "-q:v", "2", frame_path]
    result = subprocess.run(cmd, capture_output=True)
    
    if not os.path.exists(frame_path):
        print("  [!] 无法提取视频帧，默认不覆盖")
        return {"has_subtitle": False}
    
    # 转base64
    with open(frame_path, 'rb') as f:
        image_data = base64.b64encode(f.read()).decode()
    
    # AI分析（使用配置中的vision API）
    prompt = """分析这张视频截图，判断是否存在硬字幕（烧录在画面中的字幕文字）。

请回答JSON格式：
{
    "has_subtitle": true/false,
    "subtitle_position": "bottom/center/top/none",
    "subtitle_height_percent": 0-20,
    "confidence": 0-100
}

只返回JSON。"""
    
    # 从配置获取vision API信息
    vision_url = config.get('vision', {}).get('api_url', 'https://api.siliconflow.cn/v1/chat/completions')
    vision_model = config.get('vision', {}).get('model', 'Qwen/Qwen2.5-VL-72B-Instruct')
    
    try:
        resp = requests.post(
            vision_url,
            headers={"Authorization": f"Bearer {translate_key}", "Content-Type": "application/json"},
            json={
                "model": vision_model,
                "messages": [{"role": "user", "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_data}"}}
                ]}],
                "max_tokens": 200
            },
            timeout=30
        )
        
        content = resp.json()['choices'][0]['message']['content']
        json_match = re.search(r'\{[\s\S]*\}', content)
        if json_match:
            result = json.loads(json_match.group())
            
            if result.get('has_subtitle'):
                height_pct = result.get('subtitle_height_percent', 10)
                cover_height = int(2160 * height_pct / 100)
                cover_height = max(60, min(150, cover_height))
                
                print(f"  [!] 检测到硬字幕: 位置={result.get('subtitle_position')}, 高度={height_pct}%")
                return {
                    "has_subtitle": True,
                    "cover_height": cover_height,
                    "cover_opacity": 0.7
                }
    except Exception as e:
        print(f"  [!] 检测失败: {e}")
    
    print("  [OK] 无硬字幕")
    return {"has_subtitle": False}


def run_ffmpeg(cmd):
    result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='replace')
    return result.returncode == 0


def cut_video(video_path, duration, output_path, config):
    """切割视频"""
    print(f"[*] Cutting first {duration}s...")
    ffmpeg = config['ffmpeg_path']
    codec = config['output']['video_codec']
    cmd = [ffmpeg, "-y", "-i", video_path, "-t", str(duration),
           "-c:v", codec, "-preset", "default", "-c:a", "aac", output_path]
    return run_ffmpeg(cmd)


def extract_audio(video_path, output_path, sample_rate=16000, config=None):
    """提取音频"""
    ffmpeg = config['ffmpeg_path'] if config else "ffmpeg"
    cmd = [ffmpeg, "-y", "-i", video_path, "-vn", "-acodec", "pcm_s16le", 
           "-ar", str(sample_rate), "-ac", "1", output_path]
    run_ffmpeg(cmd)
    audio, sr = sf.read(output_path)
    return audio, sr


def transcribe_whisper(audio_path, config):
    """Whisper转写"""
    import torch
    import whisper
    
    model_name = config['whisper']['model']
    language = config['whisper']['language']
    
    print(f"\n[*] Whisper ({language}, {model_name} model)...")
    
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = whisper.load_model(model_name, device=device)
    result = model.transcribe(audio_path, language=language)
    
    segments = [{"start": seg['start'], "end": seg['end'], "text": seg['text'].strip()} for seg in result['segments']]
    print(f"[OK] {len(segments)} segments")
    
    del model
    torch.cuda.empty_cache()
    return segments


def translate_all(texts, config):
    """批量翻译 - 分隔符方案"""
    import time
    
    api_url = config['translate']['api_url']
    api_key = config['translate']['api_key']
    model = config['translate']['model']
    
    if not api_key:
        raise ValueError("请配置翻译API密钥（config.json中的translate.api_key或环境变量TRANSLATE_API_KEY）")
    
    print(f"\n[*] Batch translating {len(texts)} segments...")
    
    batch_size = 20
    batches = [texts[i:i+batch_size] for i in range(0, len(texts), batch_size)]
    print(f"    {len(texts)} texts -> {len(batches)} batches")
    
    SEPARATOR = "|||"
    all_translations = []
    max_retries = 5
    
    for batch_idx, batch in enumerate(batches):
        success = False
        translations = None
        
        for retry in range(max_retries):
            input_text = SEPARATOR.join(batch)
            
            prompt = f"""你是专业翻译。将以下英文完全翻译成中文。
规则：
1. 必须翻译所有内容，不要保留任何英文
2. 人名、品牌名音译成中文
3. 用 {SEPARATOR} 分隔各句翻译，保持相同数量
4. 直接返回翻译结果，不要加任何解释

{input_text}"""
            
            headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
            data = {
                "model": model,
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 4000
            }
            
            try:
                resp = requests.post(api_url, headers=headers, json=data, timeout=60)
                result = resp.json()
                
                if 'choices' in result:
                    content = result['choices'][0]['message']['content'].strip()
                    translations = content.split(SEPARATOR)
                    translations = [t.strip() for t in translations if t.strip()]
                    
                    if len(translations) == len(batch):
                        all_valid = all(any('\u4e00' <= c <= '\u9fff' for c in t) for t in translations)
                        if all_valid:
                            success = True
                            print(f"    Batch {batch_idx+1}/{len(batches)}: OK")
                            break
                
                print(f"    [RETRY {retry+1}/{max_retries}] Batch {batch_idx+1}")
            except Exception as e:
                print(f"    [RETRY {retry+1}/{max_retries}] Batch {batch_idx+1}: {e}")
            
            time.sleep(1)
        
        if not success:
            # 逐句翻译兜底
            print(f"    [!] Batch {batch_idx+1} 批量失败，逐句翻译")
            translations = []
            for text in batch:
                for _ in range(3):
                    try:
                        resp = requests.post(
                            api_url,
                            headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
                            json={
                                "model": model,
                                "messages": [{"role": "user", "content": f"将以下英文完全翻译成中文：{text}"}],
                                "max_tokens": 500
                            },
                            timeout=30
                        )
                        trans = resp.json()['choices'][0]['message']['content'].strip()
                        if any('\u4e00' <= c <= '\u9fff' for c in trans):
                            translations.append(trans)
                            break
                    except:
                        pass
                else:
                    translations.append(f"[翻译失败]")
        
        all_translations.extend(translations if translations else batch)
    
    return all_translations


def group_segments_by_duration(segments, max_duration):
    """按时长分组"""
    print(f"\n[*] Grouping segments (max {max_duration}s per group)...")
    
    groups = []
    current_group = []
    current_duration = 0.0
    
    for seg in segments:
        seg_duration = seg['end'] - seg['start']
        
        if current_duration + seg_duration <= max_duration or not current_group:
            current_group.append(seg)
            current_duration += seg_duration
        else:
            groups.append(current_group)
            current_group = [seg]
            current_duration = seg_duration
    
    if current_group:
        groups.append(current_group)
    
    print(f"    {len(segments)} segments -> {len(groups)} groups")
    return groups


def generate_tts_for_group(texts, output_path, model, config):
    """为一组文本生成TTS"""
    import torch
    torch._dynamo.config.suppress_errors = True
    
    ref_wav = config['tts']['reference_audio']
    ref_text = config['tts']['reference_text']
    cfg_value = config['tts']['cfg_value']
    timesteps = config['tts']['inference_timesteps']
    
    combined_text = "\n".join(texts)
    
    wav = model.generate(
        text=combined_text,
        prompt_wav_path=ref_wav,
        prompt_text=ref_text,
        cfg_value=cfg_value,
        inference_timesteps=timesteps,
    )
    
    sf.write(output_path, wav, model.tts_model.sample_rate)
    print(f"    Generated {len(wav)/model.tts_model.sample_rate:.2f}s")
    
    return wav, model.tts_model.sample_rate


def generate_all_tts_by_groups(groups, output_dir, config):
    """按组生成TTS"""
    import torch
    torch._dynamo.config.suppress_errors = True
    
    voxcpm_dir = Path(config['voxcpm_dir'])
    sys.path.insert(0, str(voxcpm_dir))
    
    print(f"\n[*] Loading VoxCPM...")
    from voxcpm import VoxCPM
    
    model = VoxCPM.from_pretrained(str(voxcpm_dir / "1.5"))
    
    all_wavs = []
    all_srs = []
    
    for i, group in enumerate(groups):
        texts = [seg.get('text_zh', seg['text']) for seg in group]
        output_path = output_dir / f"group_{i:03d}.wav"
        
        # 断点续传
        if output_path.exists():
            print(f"  [{i+1}/{len(groups)}] 已存在，跳过")
            wav, sr = sf.read(str(output_path))
            all_wavs.append(wav)
            all_srs.append(sr)
            continue
        
        print(f"  [{i+1}/{len(groups)}] Group {i+1}: {len(texts)} sentences")
        wav, sr = generate_tts_for_group(texts, str(output_path), model, config)
        all_wavs.append(wav)
        all_srs.append(sr)
    
    del model
    torch.cuda.empty_cache()
    
    return all_wavs, all_srs[0] if all_srs else 24000


def stretch_audio_high_quality(wav, sr, target_duration):
    """高质量音频拉伸"""
    import librosa
    
    wav_duration = len(wav) / sr
    ratio = wav_duration / target_duration
    
    if ratio < 0.85:
        silence_samples = int((target_duration - wav_duration) * sr)
        silence = np.zeros(silence_samples, dtype=np.float32)
        result = np.concatenate([wav, silence])
        method = "pad silence"
    elif ratio > 1.15:
        speed = ratio
        result = librosa.effects.time_stretch(wav, rate=speed)
        method = f"librosa {speed:.2f}x"
    else:
        target_samples = int(target_duration * sr)
        if abs(len(wav) - target_samples) > 100:
            result = scipy.signal.resample(wav, target_samples)
            method = "resample"
        else:
            result = wav
            method = "direct"
    
    return result, method


def create_final_audio_grouped(groups, group_wavs, sr, orig_sr, output_path):
    """创建最终音频"""
    print(f"\n[*] Creating final audio...")
    
    total_duration = groups[-1][-1]['end']
    total_samples = int(total_duration * orig_sr)
    final_audio = np.zeros(total_samples, dtype=np.float32)
    
    for i, (group, wav) in enumerate(zip(groups, group_wavs)):
        group_start = group[0]['start']
        group_end = group[-1]['end']
        group_duration = group_end - group_start
        wav_duration = len(wav) / sr
        
        ratio = wav_duration / group_duration
        stretched, method = stretch_audio_high_quality(wav, sr, group_duration)
        
        if sr != orig_sr:
            new_len = int(len(stretched) * orig_sr / sr)
            stretched = scipy.signal.resample(stretched, new_len)
        
        start_sample = int(group_start * orig_sr)
        end_sample = min(start_sample + len(stretched), total_samples)
        actual_len = end_sample - start_sample
        
        if actual_len > 0 and len(stretched) >= actual_len:
            final_audio[start_sample:end_sample] = stretched[:actual_len]
        
        status = "OK" if ratio < 1.15 else "!"
        print(f"    Group {i+1}: ratio {ratio:.2f} [{method}] {status}")
    
    max_val = np.max(np.abs(final_audio))
    if max_val > 0:
        final_audio = final_audio / max_val * 0.9
    
    sf.write(output_path, final_audio, orig_sr)
    print(f"[OK] {output_path} ({total_duration:.2f}s)")
    
    return final_audio, orig_sr


def generate_srt(groups, output_path):
    """生成SRT字幕"""
    def fmt_time(s):
        h, m, s, ms = int(s//3600), int((s%3600)//60), int(s%60), int((s%1)*1000)
        return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"
    
    with open(output_path, 'w', encoding='utf-8') as f:
        idx = 1
        for group in groups:
            for seg in group:
                text = seg.get('text_zh', seg['text'])
                f.write(f"{idx}\n{fmt_time(seg['start'])} --> {fmt_time(seg['end'])}\n{text}\n\n")
                idx += 1
    
    print(f"[OK] SRT: {output_path}")


def merge_video_audio_srt(video_path, audio_path, srt_path, output_path, config, subtitle_config=None):
    """合并视频、音频、字幕"""
    print(f"\n[*] Merging...")
    
    ffmpeg = config['ffmpeg_path']
    subtitle_style = config['subtitle']
    
    style_str = ','.join([
        f"Fontsize={subtitle_style['fontsize']}",
        f"Fontname={subtitle_style['fontname']}",
        f"Outline={subtitle_style['outline']}",
        f"MarginV={subtitle_style['margin_v']}",
        f"Alignment={subtitle_style['alignment']}"
    ])
    srt_escaped = srt_path.replace('\\', '\\\\').replace(':', '\\:')
    
    vf_filters = []
    
    if subtitle_config and subtitle_config.get('has_subtitle'):
        cover_h = subtitle_config.get('cover_height', 80)
        cover_opacity = subtitle_config.get('cover_opacity', 0.7)
        vf_filters.append(f"drawbox=y=ih-{cover_h}:w=iw:h={cover_h}:color=black@{cover_opacity}:t=fill")
        print(f"  添加覆盖条: 高度={cover_h}px")
    
    vf_filters.append(f"subtitles='{srt_escaped}':force_style='{style_str}'")
    vf = ','.join(vf_filters)
    
    codec = config['output']['video_codec']
    cmd = [ffmpeg, "-y", "-i", video_path, "-i", audio_path,
           "-vf", vf, "-map", "0:v", "-map", "1:a",
           "-c:v", codec, "-preset", "default", "-c:a", "aac", output_path]
    
    result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='replace')
    if result.returncode == 0:
        print(f"[OK] {output_path}")
        return True
    
    # Fallback
    cmd_simple = [ffmpeg, "-y", "-i", video_path, "-i", audio_path,
                  "-vf", f"subtitles='{srt_escaped}':force_style='{style_str}'",
                  "-map", "0:v", "-map", "1:a",
                  "-c:v", codec, "-preset", "default", "-c:a", "aac", output_path]
    result2 = subprocess.run(cmd_simple, capture_output=True, text=True, encoding='utf-8', errors='replace')
    return result2.returncode == 0


def main():
    parser = argparse.ArgumentParser(description='Video Dubbing - VoxCPM中文配音')
    parser.add_argument('video', help='输入视频路径')
    parser.add_argument('--config', '-c', help='配置文件路径', default='config.json')
    parser.add_argument('--output', '-o', help='输出文件名（不含扩展名）')
    parser.add_argument('--test', '-t', type=int, help='测试模式：只处理前N秒')
    args = parser.parse_args()
    
    # 加载配置
    config = load_config(args.config)
    
    video_path = args.video
    output_name = args.output or Path(video_path).stem
    
    # 设置工作目录
    work_dir = Path(config['work_dir'])
    temp_dir = work_dir / "temp"
    output_dir = work_dir / "output"
    temp_dir.mkdir(parents=True, exist_ok=True)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print("="*60)
    print("[*] Video Dubbing - VoxCPM中文配音")
    print("    - 分组TTS（保持连贯）")
    print("    - 智能音频匹配")
    print("    - 硬字幕自动检测")
    print("    - 断点续传")
    print("="*60)
    
    # 1. 测试模式切割
    if args.test:
        test_video = str(temp_dir / f"{output_name}_{args.test}s.mp4")
        cut_video(video_path, args.test, test_video, config)
        print(f"[*] 测试模式：前{args.test}秒")
        video_path = test_video
    
    # 2. 检测硬字幕
    subtitle_config = detect_hard_subtitle(video_path, config, config['translate']['api_key'])
    
    # 3. 提取音频
    audio_path = str(temp_dir / "audio.wav")
    orig_audio, orig_sr = extract_audio(video_path, audio_path, config=config)
    print(f"[OK] 原音频: {len(orig_audio)/orig_sr:.2f}s")
    
    # 4. Whisper转写
    orig_segments = transcribe_whisper(audio_path, config)
    
    # 5. 翻译
    texts = [seg['text'] for seg in orig_segments]
    translations = translate_all(texts, config)
    for i, seg in enumerate(orig_segments):
        seg['text_zh'] = translations[i]
    
    # 6. 分组
    max_duration = config['tts']['max_group_duration']
    groups = group_segments_by_duration(orig_segments, max_duration)
    
    # 7. TTS
    tts_dir = temp_dir / "tts_groups"
    tts_dir.mkdir(parents=True, exist_ok=True)
    group_wavs, wav_sr = generate_all_tts_by_groups(groups, tts_dir, config)
    
    # 8. 创建最终音频
    final_path = str(output_dir / f"{output_name}_dubbed.wav")
    create_final_audio_grouped(groups, group_wavs, wav_sr, orig_sr, final_path)
    
    # 9. 生成SRT
    srt_path = str(output_dir / f"{output_name}.srt")
    generate_srt(groups, srt_path)
    
    # 10. 合并
    output_video = str(output_dir / f"{output_name}_dubbed.mp4")
    merge_video_audio_srt(video_path, final_path, srt_path, output_video, config, subtitle_config)
    
    print("\n" + "="*60)
    print("[OK] DONE!")
    print(f"    Video: {output_video}")
    print("="*60)


if __name__ == '__main__':
    main()