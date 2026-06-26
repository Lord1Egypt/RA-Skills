#!/usr/bin/env python3
"""
xia-zhuan-audio 转录功能 - 基于 faster-whisper
自动下载 Whisper 模型，首次运行会下载约几十MB
"""
import sys
import os

os.environ.setdefault("HF_ENDPOINT", "https://huggingface.co")
os.environ["PYTHONIOENCODING"] = "utf-8"

import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
import argparse
import json

def format_timestamp(seconds, fmt="vtt"):
    """将秒数转换为指定格式的时间戳"""
    if seconds is None:
        return "00:00:00,000" if fmt == "srt" else "00:00:00.000"
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    ms = int((seconds % 1) * 1000)
    if fmt == "srt":
        return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"
    return f"{h:02d}:{m:02d}:{s:02d}.{ms:03d}"

def format_duration(seconds):
    """将秒数转换为中文时长描述"""
    if seconds is None:
        return "N/A"
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    if h > 0:
        return f"{h}小时{m}分{s}秒"
    if m > 0:
        return f"{m}分{s}秒"
    return f"{s}秒"

def detect_audio_video(input_path):
    """检查输入是音频还是视频文件"""
    video_exts = {".mp4", ".mkv", ".avi", ".mov", ".flv", ".wmv", ".webm", ".m4v"}
    ext = os.path.splitext(input_path)[1].lower()
    return ext in video_exts

def extract_audio(input_path, keep_audio=False):
    """从视频提取音频（临时文件）或原样返回"""
    import subprocess
    audio_exts = {".mp3", ".wav", ".flac", ".ogg", ".m4a", ".aac", ".wma", ".aiff"}
    ext = os.path.splitext(input_path)[1].lower()
    if ext in audio_exts:
        return input_path, None  # 本身就是音频，无需处理

    # 需要从视频提取音频
    temp_audio = os.path.splitext(input_path)[0] + "_temp_audio.mp3"
    cmd = [
        "ffmpeg", "-y", "-i", input_path,
        "-vn", "-acodec", "libmp3lame", "-q:a", "2",
        temp_audio
    ]
    print(f"  从视频提取音频...")
    try:
        subprocess.run(cmd, capture_output=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"[错误] 提取音频失败: {e.stderr.decode('utf-8', errors='replace')}")
        sys.exit(1)
    return temp_audio, temp_audio if not keep_audio else None

def main():
    parser = argparse.ArgumentParser(
        description="xia-zhuan-audio 转录 - 音视频转文字（基于 Whisper AI）",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("input", help="输入音频或视频文件路径")
    parser.add_argument("--output", "-o", help="输出文件路径，默认同目录同名")
    parser.add_argument("--model", "-m", default="small",
                        choices=["tiny", "base", "small", "medium", "large"],
                        help="Whisper 模型: tiny/base/small/medium/large，默认 small")
    parser.add_argument("--language", "-l", default="auto",
                        help="语言代码，如 zh/en/ja/fr/de 等，默认 auto 自动检测")
    parser.add_argument("--format", "-f", default="txt",
                        choices=["txt", "srt", "vtt", "json"],
                        help="输出格式: txt(纯文本) srt(字幕) vtt(网页字幕) json(完整数据)，默认 txt")
    parser.add_argument("--task", "-t", default="transcribe",
                        choices=["transcribe", "translate"],
                        help="transcribe(转录) 或 translate(翻译为英文)，默认 transcribe")
    parser.add_argument("--device", "-d", default="auto",
                        choices=["auto", "cpu", "cuda"],
                        help="计算设备: auto/cpu/cuda，默认 auto")
    parser.add_argument("--keep-audio", "-k", action="store_true",
                        help="保留从视频提取的临时音频文件")

    args = parser.parse_args()

    if not os.path.exists(args.input):
        print(f"[错误] 文件不存在: {args.input}")
        sys.exit(1)

    # 确定输出路径
    if args.output:
        output_path = args.output
    else:
        ext_map = {"txt": ".txt", "srt": ".srt", "vtt": ".vtt", "json": ".json"}
        base = os.path.splitext(args.input)[0]
        output_path = base + ext_map[args.format]

    # 如果输入是视频，先提取音频
    temp_audio, temp_to_delete = extract_audio(args.input, args.keep_audio)
    actual_input = temp_audio

    print(f"\n🎤 音视频转文字")
    print(f"  输入文件: {args.input}")
    print(f"  输出文件: {output_path}")
    print(f"  模型: {args.model} | 语言: {args.language} | 格式: {args.format}")

    # 模型本地缓存目录
    model_dir = os.environ.get("XZA_MODELDIR") or os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "whisper_models"
    )
    os.makedirs(model_dir, exist_ok=True)

    try:
        from faster_whisper import WhisperModel
    except ImportError:
        print("\n[错误] 未安装 faster-whisper，请运行:")
        print("  pip install faster-whisper")
        sys.exit(1)

    # 选择计算设备
    if args.device == "cuda":
        try:
            import torch
            if torch.cuda.is_available():
                device = "cuda"
                compute_type = "float16"
            else:
                print("  [警告] 未检测到 CUDA，切换为 CPU")
                device = "cpu"
                compute_type = "int8"
        except ImportError:
            print("  [警告] 未安装 PyTorch CUDA 版本，切换为 CPU")
            device = "cpu"
            compute_type = "int8"
    elif args.device == "cpu":
        device = "cpu"
        compute_type = "int8"
    else:
        # auto 模式
        try:
            import torch
            if torch.cuda.is_available():
                device = "cuda"
                compute_type = "float16"
            else:
                device = "cpu"
                compute_type = "int8"
        except ImportError:
            device = "cpu"
            compute_type = "int8"

    device_label = "GPU (CUDA)" if device == "cuda" else "CPU"
    print(f"  设备: {device_label}")

    print(f"\n  首次使用将自动下载 Whisper {args.model} 模型...")
    print(f"  模型保存位置: {model_dir}")

    try:
        model = WhisperModel(
            args.model,
            device=device,
            compute_type=compute_type,
            download_root=model_dir,
        )

        language = None if args.language == "auto" else args.language

        print(f"\n  开始转录，请稍候...\n")

        segments_gen, info = model.transcribe(
            actual_input,
            language=language,
            task=args.task,
            beam_size=5,
            vad_filter=True,
        )

        if language is None:
            print(f"  检测语言: {info.language} | 时长: {format_duration(info.duration)}")
        else:
            if info.language != language:
                print(f"  [注意] 检测到语言: {info.language}，与指定语言 {language} 不一致\n")
            print(f"  时长: {format_duration(info.duration)}")

        # 将生成器转为列表（可迭代多次）
        segments_list = list(segments_gen)
        total = len(segments_list)
        duration = info.duration or 0

        if args.format == "txt":
            lines = []
            for i, seg in enumerate(segments_list, 1):
                text = seg.text.strip()
                lines.append(text)
                print(f"\r  进度: {i}/{total} 片段", end="", flush=True)
            with open(output_path, "w", encoding="utf-8") as f:
                f.write("\n".join(lines) + "\n")

        elif args.format == "srt":
            with open(output_path, "w", encoding="utf-8") as f:
                for i, seg in enumerate(segments_list, 1):
                    start = format_timestamp(seg.start, "srt")
                    end = format_timestamp(seg.end, "srt")
                    text = seg.text.strip()
                    f.write(f"{i}\n{start} --> {end}\n{text}\n\n")
                    print(f"\r  进度: {i}/{total} 片段", end="", flush=True)
            print("")

        elif args.format == "vtt":
            with open(output_path, "w", encoding="utf-8") as f:
                f.write("WEBVTT\n\n")
                for seg in segments_list:
                    start = format_timestamp(seg.start, "vtt")
                    end = format_timestamp(seg.end, "vtt")
                    text = seg.text.strip()
                    f.write(f"{start} --> {end}\n{text}\n\n")
                    print(f"\r  进度: {segments_list.index(seg)+1}/{total} 片段", end="", flush=True)
            print("")

        elif args.format == "json":
            output_data = {
                "model": args.model,
                "language": info.language,
                "duration": duration,
                "device": device_label,
                "task": args.task,
                "segments_count": total,
                "segments": []
            }
            for seg in segments_list:
                output_data["segments"].append({
                    "id": len(output_data["segments"]),
                    "start": round(seg.start, 3),
                    "end": round(seg.end, 3),
                    "text": seg.text.strip(),
                    "words": [
                        {
                            "word": w.word,
                            "start": round(w.start, 3),
                            "end": round(w.end, 3),
                            "probability": round(w.probability, 3)
                        } for w in (seg.words or [])
                    ]
                })
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(output_data, f, ensure_ascii=False, indent=2)
            print(f"  已保存 {total} 个片段的完整数据")

        print(f"\n\n  ✅ 转录完成!")
        print(f"  已保存到: {output_path}")

        # 统计信息
        with open(output_path, "r", encoding="utf-8") as f:
            content = f.read()
        if args.format != "json":
            char_count = len(content.replace("\n", "").replace(" ", ""))
            word_count = len(content.split())
            line_count = len(content.splitlines())
            print(f"  字符数: {char_count} | 词数: {word_count} | 片段数: {total}")
        else:
            print(f"  片段数: {total}")

    except Exception as e:
        print(f"\n[错误] 转录失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    finally:
        # 清理临时音频文件
        if temp_to_delete and os.path.exists(temp_to_delete):
            try:
                os.remove(temp_to_delete)
            except:
                pass

if __name__ == "__main__":
    main()
