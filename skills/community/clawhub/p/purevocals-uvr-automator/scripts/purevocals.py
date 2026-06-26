#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Skill Name: PureVocals-UVR-Automator
Author: 王岷瑞 / https://github.com/wangminrui2022
License: Apache License
Description: 使用 audio-separator 自动从音频文件中提取干净干声。
             智能检测 GPU：有 GPU 自动使用 [gpu] 版（CUDA 加速），无 GPU 使用 [cpu] 版。
             保持原文件夹结构，自动创建虚拟环境，日志仅保留最近 3 天。
"""

import os
import sys
import subprocess
import venv
import logging
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path
import argparse
from datetime import datetime
import shutil
import re
from logger_manager import LoggerManager
import env_manager
import ensure_package
from config import MODEL_DIR,SKILL_ROOT,VENV_DIR
ensure_package.pip("pydub", "pydub","AudioSegment")
ensure_package.pip("ffmpeg-downloader")
ensure_package.pip("audio-separator")
import ffmpeg_downloader as ffdl
import importlib
# 现在添加所有导入语句
from pydub import AudioSegment

# --- 日志系统初始化 ---
logger = LoggerManager.setup_logger(logger_name="purevocals-uvr-automator")

def ensure_ffmpeg():
    """自动检测 + 下载 ffmpeg（已彻底修复 --quiet 错误 + 更稳定）"""
    # 关键修复：判断 None + 移除 --quiet
    if ffdl.ffmpeg_path is None or not os.path.exists(ffdl.ffmpeg_path):
        logger.info("⚠️  未检测到 ffmpeg，正在自动下载便携版到本地（只需一次，约 100-200MB）...")
        logger.info("   下载来源：Windows=gyan.dev | Linux=johnvansickle | macOS=evermeet")
        
        # 🔥 关键：自动输入 Y（默认 yes），彻底无交互
        logger.info("   自动确认下载中...")
        subprocess.run(["ffdl", "install"], input="Y\n", text=True, check=True)
        
        # 下载完后刷新模块
        importlib.reload(ffdl)
        
        logger.info("✅ 下载 + 安装完成！") 
        #C:\Users\Administrator\AppData\Local\ffmpegio\ffmpeg-downloader\ffmpeg\bin

    # 添加到 PATH + 强制 pydub 使用
    ffdl.add_path()
    AudioSegment.converter = ffdl.ffmpeg_path

    logger.info(f"✅ ffmpeg 已就绪 → {ffdl.ffmpeg_path}")
    return True

def show_manual_download_guide(model_name: str):
    """下载失败时显示手动下载指南"""
    print("\n" + "="*80)
    print("❌ 模型自动下载失败（网络问题）")
    print("请按照以下步骤手动下载模型并放入 models 文件夹：")
    print("="*80)
    print(f"1. 创建文件夹（如果不存在）：")
    print(f"   {MODEL_DIR}")
    print("\n2. 下载对应模型并重命名为下方文件名，放到上面文件夹：")
    
    if model_name == "6_HP-Karaoke-UVR.pth":
        print(f"   • {model_name}")
        print("     下载地址: https://github.com/TRvlvr/model_repo/releases/download/all_public_uvr_models/6_HP-Karaoke-UVR.pth")
    elif model_name == "Kim_Vocal_2.onnx":
        print(f"   • {model_name}")
        print("     下载地址: https://github.com/TRvlvr/model_repo/releases/download/all_public_uvr_models/Kim_Vocal_2.onnx")
    elif model_name == "UVR_MDXNET_KARA_2.onnx":
        print(f"   • {model_name}")
        print("     下载地址: https://github.com/TRvlvr/model_repo/releases/download/all_public_uvr_models/UVR_MDXNET_KARA_2.onnx")
    else:
        print(f"   • {model_name}")
        print("     请访问 https://github.com/TRvlvr/model_repo/releases/tag/all_public_uvr_models 下载对应文件")
    
    print("\n3. 下载完成后重新运行命令即可自动使用。")
    print("   （以后再次失败仍会显示此提示）")
    print("="*80)
    logger.error("模型下载失败，已显示手动下载指南")

def extract_pure_vocals(input_path: str, output_dir: str, model: str, window_size: int, aggression: int, chunk_duration: int = None, sample_mode: bool = False):
    """核心提取逻辑"""
    src_path = Path(input_path).resolve()
    dest_path = Path(output_dir).resolve()
    MODEL_DIR.mkdir(exist_ok=True)          # 确保 models 目录存在
    
    logger.info(f"--- 开始干声提取任务 ---")
    logger.info(f"输入路径: {src_path}")
    logger.info(f"输出路径: {dest_path}")
    logger.info(f"模型目录: {MODEL_DIR}") 
    logger.info(f"模型: {model} | Window Size: {window_size} | Aggression: {aggression} | Sample Mode: {sample_mode}")

    # 新增：模型缓存到技能目录下的 models/ 文件夹（永久缓存，第二次秒开）
    model_dir = SKILL_ROOT / "models"
    model_dir.mkdir(parents=True, exist_ok=True)
    logger.info(f"模型缓存目录: {model_dir} ")#首次下载会显示 tqdm 进度条
    logger.info(f"模型: {args.model} | Window Size: {window_size} | Aggression: {aggression}")

    if not src_path.exists():
        logger.error(f"输入路径不存在: {src_path}")
        sys.exit(1)
    
    # 收集所有支持的音频文件
    audio_files = []
    if src_path.is_file():
        if src_path.suffix.lower() in {".mp3", ".wav", ".flac", ".ogg", ".m4a"}:
            audio_files = [src_path]
    else:
        for ext in ["*.mp3", "*.wav", "*.flac", "*.ogg", "*.m4a"]:
            audio_files.extend(src_path.rglob(ext))
    
    if not audio_files:
        logger.warning("未发现任何支持的音频文件。")
        sys.exit(0)
    
    logger.info(f"共发现 {len(audio_files)} 个音频文件，开始处理...")
    
    # CLI 路径（venv 内）
    if os.name == "nt":
        cli_path = str(VENV_DIR / "Scripts" / "audio-separator.exe")
    else:
        cli_path = str(VENV_DIR / "bin" / "audio-separator")
    
    success = 0
    fail = 0
    
    for audio_file in audio_files:
        rel_path = audio_file.relative_to(src_path) if src_path.is_dir() else Path(audio_file.name)
        out_subdir = dest_path / rel_path.parent
        out_subdir.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"正在处理: {rel_path}")
        # ─────────────── Sample Mode 处理 ───────────────
        process_file = audio_file
        is_temp = False
        if args.sample_mode:
            process_file = prepare_sample_file(
                original_file=audio_file,
                output_dir=out_subdir,
                sample_seconds=30
            )
            is_temp = (process_file != audio_file)        
        try:
            cmd = [
                cli_path,
                str(process_file),               # ← 这里使用处理后的文件（可能是临时文件）
                "--output_dir", str(out_subdir),
	            "--model_file_dir", str(MODEL_DIR),      # 指定模型下载路径
                "--model_filename", model,
                "--output_format", "WAV",
                "--single_stem", "Vocals",
                "--vr_window_size", str(window_size),
                "--vr_aggression", str(aggression),
                "--normalization", "0.9"
            ]
            
            if chunk_duration:
                cmd.extend(["--chunk_duration", str(chunk_duration)])
            if sample_mode:
                logger.info("Sample Mode 已启用（仅处理前 30s）")
                # 如需严格 30s 采样可在此处用 pydub 裁剪，此处保持全量 + 日志提示
            
            logger.info(f"🚀 开始处理: {audio_file.name} （模型下载/加载中...）")
            # 添加 --model_file_dir 参数，让模型下载到我们自己的 models/ 目录
            cmd.extend(["--model_file_dir", str(model_dir)])
            # 关键修改：不捕获输出，让 tqdm 进度条直接显示在控制台
            process = subprocess.run(
                cmd,
                check=True,          # 出错自动抛异常
                timeout=1200,        # 长音频给更长时间（20分钟）
                # capture_output=False 默认就是不捕获，进度条会实时显示
            )
            logger.info(f"✅ 处理完成: {audio_file.name}")

            if process.returncode == 0:
                # 重命名输出文件为干净名称 xxx_vocals.wav
                generated_files = list(out_subdir.glob(f"*{audio_file.stem}*Vocals*.wav"))
                if generated_files:
                    # 获取当前时间戳（格式：20260226_143055）
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    # 加上时间戳的文件名
                    final_file = out_subdir / f"{audio_file.stem}_{timestamp}.wav"
                    generated_files[0].rename(final_file)
                    logger.info(f"✅ 提取成功: {final_file.name}")
                    success += 1
                else:
                    logger.warning(f"输出文件未找到: {audio_file.name}")
                    fail += 1
            else:
                logger.error(f"audio-separator 报错 ({audio_file.name}): {process.stderr.strip()}")
                show_manual_download_guide(model)
                fail += 1
                
        except Exception as e:
            logger.error(f"处理异常 ({audio_file.name}): {str(e)}")
            show_manual_download_guide(model)
            fail += 1
        finally:
            # 清理临时文件
            if is_temp:
                cleanup_temp_file(process_file)    
    
    logger.info(f"--- 任务结束: 成功 {success} 个，失败 {fail} 个 ---")
    print(f"\n[结果反馈] 成功: {success} | 失败: {fail}")

def prepare_sample_file(
    original_file: Path,
    output_dir: Path,
    sample_seconds: int = 30
) -> Path:
    """
    如果启用了 Sample Mode，则将原始音频裁剪为前 N 秒的临时文件，并返回要处理的路径。
    
    参数:
        original_file: 原始音频文件路径 (Path 对象)
        output_dir: 输出目录（临时文件会放在这里）
        sample_seconds: 要裁剪的秒数，默认 30 秒
    
    返回:
        Path: 要实际处理的音频文件路径（可能是原文件，也可能是临时裁剪文件）
    """
    if not sample_seconds or sample_seconds <= 0:
        return original_file

    temp_file = None
    try:
        logger.info(f"Sample Mode 启用 → 裁剪前 {sample_seconds} 秒")

        audio = AudioSegment.from_file(str(original_file))
        duration_ms = len(audio)
        target_ms = sample_seconds * 1000

        if duration_ms <= target_ms:
            logger.info(f"文件时长 {duration_ms//1000}s ≤ {sample_seconds}s，直接使用原文件")
            return original_file

        # 裁剪前 N 秒
        clipped = audio[:target_ms]

        # 生成临时文件名，放在输出目录中，避免与原文件冲突
        stem = original_file.stem
        suffix = original_file.suffix
        temp_name = f"{stem}_sample_{sample_seconds}s{suffix}"
        temp_file = output_dir / temp_name

        # 导出临时文件（格式与原文件一致）
        clipped.export(str(temp_file), format=suffix.lstrip('.').lower())
        logger.info(f"已生成临时采样文件: {temp_file.name} ({sample_seconds}s)")

        return temp_file

    except Exception as e:
        logger.error(f"Sample Mode 裁剪失败: {str(e)}，将使用完整原文件")
        if temp_file and temp_file.exists():
            try:
                temp_file.unlink()
            except:
                pass
        return original_file

def cleanup_temp_file(temp_path: Path):
    """尝试清理临时采样文件"""
    if temp_path and temp_path.exists():
        try:
            temp_path.unlink()
            logger.info(f"已清理临时文件: {temp_path.name}")
        except Exception as e:
            logger.warning(f"清理临时文件失败: {str(e)}")

if __name__ == "__main__":
    env_manager.check_python_version()
    env_manager.setup_venv()# 必须最先执行（包含 GPU 自动检测）
    ensure_ffmpeg()

    parser = argparse.ArgumentParser(description="PureVocals_UVR_Automator - 干净干声提取")
    parser.add_argument("input", nargs="?", help="输入音频文件或目录")
    parser.add_argument("output_dir", nargs="?", help="输出目录")
    # ==================== 模型参数（已优化）====================
    parser.add_argument("--model", default="Kim_Vocal_2.onnx",
                       help="""模型文件名（默认: Kim_Vocal_2.onnx - 强烈推荐）
支持的内置模型：
  - Kim_Vocal_2.onnx            （速度最快 + 干声最干净，推荐默认）
  - UVR_MDXNET_KARA_2.onnx  （极致速度，适合批量）
  - 6_HP-Karaoke-UVR.pth        （你原来的高质量模型，需手动下载后使用）""")
    parser.add_argument("--window_size", type=int, default=320, help="VR Window Size")
    parser.add_argument("--aggression", type=int, default=10, help="VR Aggression")
    parser.add_argument("--chunk_duration", type=int, help="分块处理秒数（长音频推荐）")
    parser.add_argument("--sample_mode", action="store_true", help="启用 Sample Mode（30s）")
    
    args = parser.parse_args()
    
    if not args.input or not args.output_dir:
        logger.error("参数不足！用法示例: python purevocals.py <输入路径> <输出目录> [--model ...]")
        sys.exit(1)
    
    extract_pure_vocals(
        args.input,
        args.output_dir,
        args.model,
        args.window_size,
        args.aggression,
        args.chunk_duration,
        args.sample_mode
    )