#!/usr/bin/env python3
"""
QQ Bot 语音消息处理脚本
自动解码 QQ Silk V3 格式语音，使用 Whisper 转文字

用法：
    python3 process_qq_voice.py voice.amr
    python3 process_qq_voice.py voice.amr --output /tmp/output
    python3 process_qq_voice.py --batch /path/to/voices/
"""

import subprocess
import os
import sys
import argparse
from pathlib import Path

# 配置
DECODER_PATH = os.getenv("SILK_DECODER_PATH", "/tmp/silk-v3-decoder")
WHISPER_MODEL = os.getenv("WHISPER_MODEL", "medium")  # v2.0: 默认 medium 模型，准确率 ~95%+
WHISPER_LANGUAGE = os.getenv("WHISPER_LANGUAGE", "zh")


def check_dependencies():
    """检查依赖是否已安装"""
    missing = []
    
    # 检查 silk-v3-decoder
    if not os.path.exists(DECODER_PATH):
        missing.append(f"silk-v3-decoder (路径：{DECODER_PATH})")
    
    # 检查 whisper
    try:
        subprocess.run(["whisper", "--version"], capture_output=True, check=False)
    except FileNotFoundError:
        missing.append("whisper (pip3 install openai-whisper)")
    
    # 检查 ffmpeg
    try:
        subprocess.run(["ffmpeg", "-version"], capture_output=True, check=False)
    except FileNotFoundError:
        missing.append("ffmpeg (apt install ffmpeg)")
    
    if missing:
        print("❌ 缺少依赖：")
        for dep in missing:
            print(f"   - {dep}")
        print("\n请先安装依赖后再运行。")
        return False
    
    return True


def decode_qq_voice(amr_path, output_dir=None):
    """
    解码 QQ 语音文件
    
    参数:
        amr_path: .amr 文件路径
        output_dir: 输出目录（可选）
    
    返回:
        (mp3_path, transcript) 或 (None, None)
    """
    amr_path = Path(amr_path)
    
    if not amr_path.exists():
        print(f"❌ 文件不存在：{amr_path}")
        return None, None
    
    if output_dir is None:
        output_dir = amr_path.parent
    else:
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
    
    try:
        # 1. 去掉第一个字节 (0x02)
        fixed_path = amr_path.with_suffix(amr_path.suffix + ".fixed")
        with open(amr_path, 'rb') as f:
            data = f.read()
        with open(fixed_path, 'wb') as f:
            f.write(data[1:])  # 跳过 0x02
        
        print(f"✅ 已去掉文件头：{fixed_path}")
        
        # 2. 使用 silk-v3-decoder 转换
        output_mp3 = output_dir / f"{amr_path.stem}.mp3"
        
        print(f"🎵 正在解码...")
        result = subprocess.run(
            ["bash", f"{DECODER_PATH}/converter.sh", str(fixed_path), "mp3"],
            capture_output=True,
            text=True,
            timeout=120
        )
        
        if result.returncode != 0:
            print(f"❌ 解码失败：{result.stderr}")
            return None, None
        
        # 移动输出文件
        decoded_mp3 = Path(fixed_path.with_suffix(".mp3"))
        if decoded_mp3.exists():
            decoded_mp3.rename(output_mp3)
        
        print(f"✅ 解码完成：{output_mp3}")
        
        # 3. Whisper 识别文字
        print(f"🎤 正在识别...")
        result = subprocess.run(
            ["whisper", "--model", WHISPER_MODEL, "--language", WHISPER_LANGUAGE,
             str(output_mp3), "--output_dir", str(output_dir),
             "--verbose", "False"],
            capture_output=True,
            text=True,
            timeout=300
        )
        
        # 读取转录文本
        txt_path = output_mp3.with_suffix(".txt")
        if txt_path.exists():
            with open(txt_path, 'r', encoding='utf-8') as f:
                transcript = f.read().strip()
        else:
            transcript = ""
        
        print(f"✅ 识别完成")
        
        # 4. 清理临时文件
        if fixed_path.exists():
            fixed_path.unlink()
        if decoded_mp3.exists():
            decoded_mp3.unlink()
        
        return str(output_mp3), transcript
        
    except subprocess.TimeoutExpired:
        print("❌ 处理超时")
        return None, None
    except Exception as e:
        print(f"❌ 处理失败：{e}")
        return None, None


def batch_process(input_dir, output_dir=None):
    """批量处理目录下的所有 .amr 文件"""
    input_dir = Path(input_dir)
    
    if not input_dir.exists():
        print(f"❌ 目录不存在：{input_dir}")
        return
    
    amr_files = list(input_dir.glob("*.amr"))
    
    if not amr_files:
        print(f"❌ 未找到 .amr 文件：{input_dir}")
        return
    
    print(f"📂 找到 {len(amr_files)} 个语音文件")
    
    results = []
    for i, amr_file in enumerate(amr_files, 1):
        print(f"\n[{i}/{len(amr_files)}] 处理：{amr_file.name}")
        mp3, text = decode_qq_voice(amr_file, output_dir)
        
        if mp3:
            results.append({
                "file": amr_file.name,
                "mp3": mp3,
                "transcript": text
            })
            print(f"📝 文字：{text[:50]}...")
        else:
            print(f"❌ 处理失败")
    
    # 输出汇总
    print("\n" + "="*50)
    print("📊 处理结果汇总")
    print("="*50)
    
    for r in results:
        print(f"\n📁 {r['file']}")
        print(f"   🎵 MP3: {r['mp3']}")
        print(f"   📝 文字：{r['transcript']}")
    
    return results


def main():
    parser = argparse.ArgumentParser(
        description="QQ Bot 语音转文字工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python3 process_qq_voice.py voice.amr
  python3 process_qq_voice.py voice.amr --output /tmp/output
  python3 process_qq_voice.py --batch /path/to/voices/
        """
    )
    
    parser.add_argument("input", nargs="?", help="输入的 .amr 文件或目录")
    parser.add_argument("--output", "-o", help="输出目录")
    parser.add_argument("--batch", "-b", action="store_true", help="批量处理目录")
    parser.add_argument("--model", "-m", default=WHISPER_MODEL, help=f"Whisper 模型 (默认：{WHISPER_MODEL})")
    parser.add_argument("--language", "-l", default=WHISPER_LANGUAGE, help=f"语言 (默认：{WHISPER_LANGUAGE})")
    parser.add_argument("--check", "-c", action="store_true", help="检查依赖")
    
    args = parser.parse_args()
    
    # 检查依赖
    if args.check or not check_dependencies():
        sys.exit(0 if args.check else 1)
    
    # 设置模型
    global WHISPER_MODEL, WHISPER_LANGUAGE
    WHISPER_MODEL = args.model
    WHISPER_LANGUAGE = args.language
    
    # 处理
    if args.batch:
        if not args.input:
            print("❌ 批量处理需要指定目录")
            sys.exit(1)
        batch_process(args.input, args.output)
    else:
        if not args.input:
            print("❌ 需要指定输入文件")
            print("用法：python3 process_qq_voice.py voice.amr")
            sys.exit(1)
        
        mp3, text = decode_qq_voice(args.input, args.output)
        
        if mp3:
            print(f"\n✅ 处理完成！")
            print(f"🎵 MP3: {mp3}")
            print(f"📝 文字：{text}")
        else:
            print(f"\n❌ 处理失败")
            sys.exit(1)


if __name__ == "__main__":
    main()
