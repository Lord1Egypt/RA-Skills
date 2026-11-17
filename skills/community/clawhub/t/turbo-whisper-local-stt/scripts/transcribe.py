#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Skill Name: Turbo-Whisper-Local-STT
Author: 王岷瑞 / https://github.com/wangminrui2022
License: Apache License
Description: 高性能、完全离线、支持批量处理的中文语音转录神器。
基于 Faster-Whisper（CTranslate2）实现，支持自动下载模型、GPU 加速、VAD 长音频智能分段。
单文件/整个文件夹一键转录，按原目录结构保存 `.txt` 或 `.json` 文件（JSON 严格为 `{ "success": true, "text": "..." }`）。
专为 OpenClaw Skill 设计，也可独立使用。
"""

import argparse
import json
from pathlib import Path
import gc
import sys
import env_manager
import ensure_package
from config import MODEL_DIR, SKILL_ROOT, VENV_DIR
import os  # 用于跨平台换行符）
from logger_manager import LoggerManager

# ==================== 自动安装依赖 ====================
ensure_package.pip("faster_whisper", "faster_whisper", "WhisperModel")
ensure_package.pip("torch")
ensure_package.pip("huggingface_hub")      # ← 简化，只传包名
ensure_package.pip("tqdm")

import torch
from huggingface_hub import snapshot_download
from tqdm import tqdm
from pydub import AudioSegment
from faster_whisper import WhisperModel

logger = LoggerManager.setup_logger(logger_name="turbo-whisper-local-stt")
# ==================== 模型名称映射表（已加入你的专属模型） ====================
MODEL_MAPPING = {
    "large-v3-ct2": "wangminrui2022/faster-whisper-large-v3-ct2",   # ← 模型（推荐别名）
    "faster-whisper-large-v3-ct2": "wangminrui2022/faster-whisper-large-v3-ct2",  # 完整仓库名也支持
    "large-v3-turbo-ct2": "wangminrui2022/faster-whisper-large-v3-turbo-ct2",
    "faster-whisper-large-v3-turbo-ct2": "wangminrui2022/faster-whisper-large-v3-turbo-ct2",
    "whisper-base-ct2": "wangminrui2022/faster-whisper-base-ct2",
    "faster-whisper-base-ct2": "wangminrui2022/faster-whisper-base-ct2",
}

def download_model(model_name: str, models_dir: Path) -> str:
    """自动下载模型（失败时控制台美观格式化显示）"""
    if model_name in MODEL_MAPPING:
        repo_id = MODEL_MAPPING[model_name]
        local_dir = models_dir / model_name.replace("/", "_")
    elif "/" in model_name:
        repo_id = model_name
        local_dir = models_dir / model_name.split("/")[-1].replace(":", "_")
    else:
        repo_id = model_name
        local_dir = models_dir / model_name.replace("/", "_")

    if local_dir.exists() and any(local_dir.iterdir()):
        logger.info(f"✅ 模型已存在: {local_dir}")
        return str(local_dir)

    logger.info(f"🔽 正在从 Hugging Face 下载模型: {model_name} → {repo_id}")
    logger.info(f"   保存路径: {local_dir}（当前models目录）")

    local_dir.mkdir(parents=True, exist_ok=True)

    try:
        snapshot_download(
            repo_id=repo_id,
            local_dir=str(local_dir),
            allow_patterns=["*"]
        )
        logger.info(f"✅ 下载完成！模型路径: {local_dir}")
        return str(local_dir)
    except Exception as e:
        download_url = f"https://huggingface.co/{repo_id}/tree/main"
        
        # ==================== 美观格式化输出（控制台友好） ====================
        print("\n" + "="*60)
        print("❌ 模型下载失败")
        print("="*60)
        print(f"错误原因: {str(e)}")
        print("\n💡 手动下载方案（推荐，3步搞定）：")
        print("   1. 打开下面链接（直接复制到浏览器）：")
        print(f"      👉 {download_url}")
        print("   2. 点击页面右上角 **Download** 按钮（或逐个文件下载）")
        print("      需要下载全部文件：config.json、model.bin、tokenizer.json、vocabulary.json 等")
        print(f"   3. 把所有文件放到以下目录：")
        print(f"      📁 {local_dir}")
        print("   4. 重新运行命令即可（自动识别已存在模型）")
        print("\n📋 你的专属模型下载地址（已为你生成）：")
        print(f"   {download_url}")
        print("="*60 + "\n")

        # ==================== 同时输出 JSON（供 Agent 使用） ====================
        #error_msg = f"模型下载失败: {str(e)}\n手动下载地址: {download_url}\n保存目录: {local_dir}"
        #plogger.inforint(json.dumps({"success": False, "error": error_msg}, ensure_ascii=False, indent=2))
        sys.exit(1)


# ==================== 支持的音频格式 ====================
AUDIO_EXTENSIONS = {'.wav', '.mp3', '.m4a', '.flac', '.ogg', '.opus'}

def transcribe_file(model, audio_path: Path) -> str:
    """单文件转录，返回完整文本"""
    logger.info(f"正在转录: {audio_path.name}")
    segments, info = model.transcribe(
        str(audio_path),
        language=args.language,          # 使用全局 args（批量模式复用）
        beam_size=args.beam_size,
        vad_filter=True,
        vad_parameters=dict(min_silence_duration_ms=500),
        word_timestamps=False
    )
    # 【修复重点】：检查字面量 "\\n" (命令行传入时的原样)
    if args.separator == "\\n" or args.separator == "\n":
        # 直接使用真正的换行符，后续写入文件时 open(..., 'w') 会自动跨平台处理
        args.separator = "\n"  
    logger.info(f"当前使用的分隔符: {repr(args.separator)}") # 使用 repr 打印，可以看到真实的字符表示
    logger.info(f"跨平台换行符: {args.separator}")
    # 【关键修复】：将字面量 "\n" 转换为真正的换行符
    # 如果用户传入的是字符串 "\n"，这个操作会把它变成真正的换行控制符
    try:
        actual_separator = args.separator.encode().decode('unicode_escape')
    except Exception:
        actual_separator = args.separator
    logger.info(f"当前使用的真实分隔符 (repr): {repr(actual_separator)}")
    # 拼接文本
    full_text = args.separator.join(segment.text.strip() for segment in segments)
    return full_text.strip()

def transcribe_and_split(model, audio_path: Path, out_dir: Path):
    logger.info(f"转录 + 按模型导出分段音频与文本: {out_dir}")
    """Export Segmented Audio and Text by Model"""
    out_dir.mkdir(parents=True, exist_ok=True)
    segments, info = model.transcribe(
        str(audio_path),
        language=args.language,
        beam_size=args.beam_size,
        vad_filter=True,
        vad_parameters=dict(min_silence_duration_ms=500),
        word_timestamps=False
    )
    # 读取完整音频
    audio = AudioSegment.from_file(audio_path)
    results = []
    for i, seg in enumerate(segments):
        text = seg.text.strip()
        # ❌ 过滤太短文本
        if len(text) < 2:
            continue
        start_ms = int(seg.start * 1000)
        end_ms = int(seg.end * 1000)
        # ✅ 加 overlap（避免截断）
        overlap = 200  # ms
        start_ms = max(0, start_ms - overlap)
        end_ms = min(len(audio), end_ms + overlap)
        chunk = audio[start_ms:end_ms]
        # 文件名
        base_name = f"{audio_path.stem}_{i:04d}"
        wav_path = out_dir / f"{base_name}.wav"
        txt_path = out_dir / f"{base_name}.txt"
        # 导出音频
        chunk.export(wav_path, format="wav")
        # 导出文本
        with open(txt_path, "w", encoding="utf-8") as f:
            f.write(text)
        results.append((wav_path, text))
    return results

def save_metadata(results, out_dir: Path):
    """
    将结果保存为 metadata.list，格式：
    wav_filename|文件夹名称|ZH|clean_text
    """
    # 自动创建输出文件夹
    out_dir.mkdir(exist_ok=True)
    # 输出文件路径改为 .list
    meta_path = out_dir / "metadata.list"
    with open(meta_path, "w", encoding="utf-8", newline="") as f:
        for wav_path, text in results:
            # 清理文本
            clean_text = text.strip()
            if not clean_text:          # 如果清理后为空，则跳过或使用占位符
                clean_text = "空文本"
            if args.speaker:
                speaker = args.speaker.strip()
            else:
                # 未传入 speaker 时，提取第一级子目录名
                speaker = wav_path.parent.name
            # 写入指定格式
            language=args.lang
            line = f"{wav_path.name}|{speaker}|{language}|{clean_text}\n"
            f.write(line)
    logger.info(f"✅ metadata.list 已保存至: {meta_path}")
    logger.info(f"   共写入 {len(results)} 条记录")

# def save_metadata(results, out_dir: Path):
#     # 自动创建输出文件夹（不存在就新建，避免报错）
#     out_dir.mkdir(exist_ok=True)
#     # 拼接文件路径
#     meta_path = out_dir / "metadata.csv"
#     # 写入文件（utf-8 保证中文不乱码）
#     with open(meta_path, "w", encoding="utf-8", newline="") as f:
#         for wav_path, text in results:
#             # 安全写入：自动处理空文本、去除多余空格
#             clean_text = text.strip()
#             f.write(f"{wav_path.name}|{clean_text}\n")

def save_result(full_text: str, save_path: Path, output_format: str):
    """指定的格式保存文件"""
    save_path.parent.mkdir(parents=True, exist_ok=True)
    logger.info(f"指定的格式保存文件: {output_format}")
    if output_format == "text":
        save_path = save_path.with_suffix('.txt')
        save_path.write_text(full_text, encoding="utf-8")
        logger.info(f"✅ 已保存 TXT: {save_path}")
    else:  # json
        save_path = save_path.with_suffix('.json')
        minimal_json = {
            "success": True,
            "text": full_text
        }
        save_path.write_text(json.dumps(minimal_json, ensure_ascii=False, indent=2), encoding="utf-8")
        logger.info(f"✅ 已保存 JSON: {save_path}")

def json_default(obj):
    if isinstance(obj, Path):
        return str(obj)
    raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")

def main():
    global args  # 批量模式需要访问

    input_path = Path(args.audio_path)
    if not input_path.exists():
        print(json.dumps({"success": False, "error": f"路径不存在: {input_path}"}, ensure_ascii=False))
        sys.exit(1)

    # ==================== 确定输出目录 ====================
    if input_path.is_file():
        # 单文件模式
        output_dir = Path(args.output_dir) if args.output_dir else input_path.parent
        output_dir.mkdir(parents=True, exist_ok=True)
        txt_path = output_dir / f"{input_path.stem}.txt"
        is_batch = False
    else:
        # 批量目录模式
        if args.output_dir:
            output_dir = Path(args.output_dir)
        else:
            output_dir = input_path.parent / f"{input_path.name}_transcripts"
        output_dir.mkdir(parents=True, exist_ok=True)
        is_batch = True

    # ==================== 确定模型路径 ====================
    models_dir = Path(SKILL_ROOT) / "models"
    models_dir.mkdir(parents=True, exist_ok=True)

    final_model_path = args.model_path
    if args.model is not None:
        final_model_path = download_model(args.model, models_dir)

    # 如果还是空，强制使用 large-v3-ct2 模型
    if final_model_path is None:
        final_model_path = download_model("large-v3-ct2", models_dir)

    logger.info(f"🚀 加载模型: {final_model_path} ...")
    model = WhisperModel(
        final_model_path,
        device="cuda" if torch.cuda.is_available() else "cpu",
        compute_type="int8_float16",
        local_files_only=True
    )

    # ==================== 处理逻辑 ====================
    if not is_batch:
        save_path = output_dir / input_path.stem
        if args.split:
            # 按模型切分导出音频和文本
            full_text=transcribe_and_split(model,input_path,save_path)
            if args.metadata:
                save_metadata(full_text,save_path)
            # 控制台输出（方便查看）
            #print("\n" + "="*50)
            #print(json.dumps(full_text, ensure_ascii=False, indent=2, default=json_default))
        else:    
            # 单文件模式
            full_text = transcribe_file(model, input_path)
            save_result(full_text, save_path, args.output)
    else:
        # 批量模式
        audio_files = []
        for ext in AUDIO_EXTENSIONS:
            audio_files.extend(input_path.rglob(f"*{ext}"))
            audio_files.extend(input_path.rglob(f"*{ext.upper()}"))

        logger.info(f"找到 {len(audio_files)} 个音频文件，开始批量转录...")

        success_count = 0
        for audio_file in tqdm(audio_files, desc="批量转录"):
            try:
                relative = audio_file.relative_to(input_path)
                txt_path = output_dir / relative.with_suffix('.txt')
                save_path = output_dir / relative.with_suffix('')
                # full_text = transcribe_file(model, audio_file)
                # save_result(full_text, save_path, args.output)
                if args.split:
                    # 按模型切分导出音频和文本
                    full_text=transcribe_and_split(model,audio_file,save_path)
                    if args.metadata:
                        save_metadata(full_text,save_path)
                    # 控制台输出（方便查看）
                    #print("\n" + "="*50)
                    #print(json.dumps(full_text, ensure_ascii=False, indent=2, default=json_default))
                else:    
                    # 单文件模式
                    full_text = transcribe_file(model, audio_file)
                    save_result(full_text, save_path, args.output)                
                success_count += 1
                logger.info(f"   ✅ {relative} → {txt_path.name}")
            except Exception as e:
                logger.info(f"   ❌ {audio_file.name} 失败: {e}")

        # 批量完成总结
        summary = {
            "success": True,
            "mode": "batch",
            "input_dir": str(input_path),
            "output_dir": str(output_dir),
            "total_files": len(audio_files),
            "success_count": success_count,
            "success_rate": round(success_count / len(audio_files) * 100, 2) if audio_files else 0
        }
        logger.info("\n" + "="*50)
        print(json.dumps(summary, ensure_ascii=False, indent=2))

    # ==================== 清理显存 ====================
    del model
    gc.collect()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
        torch.cuda.reset_peak_memory_stats()
    print("✅ 显存已释放", file=sys.stderr)


if __name__ == "__main__":
    env_manager.check_python_version()
    env_manager.setup_venv()

    parser = argparse.ArgumentParser(description="Faster Whisper 本地音频转文本（OpenClaw Skill）")
    parser.add_argument("--audio_path", type=str, required=True, help="音频文件绝对路径")
    parser.add_argument("--output_dir", type=str, default=None, help="输出目录（批量模式推荐指定，单文件默认同目录）")
    parser.add_argument("--language", type=str, default=None, help="语言提示 (zh/en 等)")
    parser.add_argument("--model_path", type=str, default=None, help="手动指定本地模型路径（优先级最高）")
    parser.add_argument("--model", type=str, default=None, help="模型别名（large-v3-ct2 / faster-whisper-large-v3-ct2 等，自动下载）")
    parser.add_argument("--beam_size", type=int, default=5)
    parser.add_argument("--output", choices=["json", "text"], default="text")
    parser.add_argument("--separator",type=str,default=chr(32),help="可指定拼接分隔符，默认一个空格（不传参时自动使用空格）") # 默认一个空格（用 chr(32) 写法，代码里一目了然）chr(32)==" "
    parser.add_argument("--split", action="store_true",help="启用分段导出，按模型切分导出音频和文本")
    parser.add_argument("--metadata", action="store_true",help="当用户需要为 **MeloTTS** 训练或微调生成 metadata.list 文件时自动触发，路径|speaker|lang|text（无空格）")
    parser.add_argument("--speaker", type=str, default=None, help="说话人名字。如果不传，则自动使用第一级子目录名作为 speaker（多音色模式）")
    parser.add_argument("--lang", type=str, default="ZH", choices=["ZH", "EN"], help="语言代码")
    
    args = parser.parse_args()

    main()