#!/usr/bin/env python3
"""
环境检查脚本 - 检查 video-batch-transcript 的依赖
"""

import sys
import subprocess
from pathlib import Path

def check_python_version():
    """检查 Python 版本"""
    version = sys.version_info
    print(f"Python 版本：{version.major}.{version.minor}.{version.micro}")
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("⚠️  警告：建议使用 Python 3.8+")
        return False
    return True

def check_package(package_name, import_name=None):
    """检查 Python 包是否安装"""
    if import_name is None:
        import_name = package_name
    
    try:
        __import__(import_name)
        print(f"✓ {package_name}: 已安装")
        return True
    except ImportError:
        print(f"✗ {package_name}: 未安装")
        return False

def check_command(cmd):
    """检查命令行工具是否可用"""
    try:
        result = subprocess.run(
            [cmd, '--version'],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            version_line = result.stdout.split('\n')[0]
            print(f"✓ {cmd}: 已安装 ({version_line})")
            return True
        else:
            print(f"✗ {cmd}: 未找到")
            return False
    except (FileNotFoundError, subprocess.TimeoutExpired):
        print(f"✗ {cmd}: 未找到")
        return False

def check_cuda():
    """检查 CUDA 是否可用"""
    try:
        import torch
        if torch.cuda.is_available():
            gpu_name = torch.cuda.get_device_name(0)
            gpu_memory = torch.cuda.get_device_properties(0).total_memory / 1024**3
            print(f"✓ CUDA: 可用")
            print(f"  GPU: {gpu_name}")
            print(f"  显存：{gpu_memory:.1f} GB")
            
            # 推荐模型
            if gpu_memory < 4:
                print(f"  推荐模型：tiny 或 base")
            elif gpu_memory < 8:
                print(f"  推荐模型：small 或 medium")
            else:
                print(f"  推荐模型：medium 或 large")
            return True
        else:
            print("○ CUDA: 不可用 (将使用 CPU)")
            return False
    except ImportError:
        print("○ torch: 未安装")
        return False
    except Exception as e:
        print(f"○ CUDA 检查失败：{e}")
        return False

def main():
    print("=" * 60)
    print("Video Batch Transcript - 环境检查")
    print("=" * 60)
    print()
    
    # Python 版本
    print("【Python 环境】")
    check_python_version()
    print()
    
    # Python 包
    print("【Python 依赖】")
    packages = [
        ('yt-dlp', 'yt_dlp'),
        ('faster-whisper', 'faster_whisper'),
        ('pandas', 'pandas'),
        ('torch', 'torch'),
    ]
    
    for pkg, imp in packages:
        check_package(pkg, imp)
    print()
    
    # 命令行工具
    print("【系统工具】")
    check_command('ffmpeg')
    check_command('yt-dlp')
    print()
    
    # CUDA
    print("【GPU 加速】")
    check_cuda()
    print()
    
    # 支持的网站
    print("【支持的网站】")
    print("  国内：哔哩哔哩、抖音、快手、西瓜视频、腾讯视频等")
    print("  国际：YouTube, Vimeo, Dailymotion, Twitch, Twitter/X, Instagram, TikTok 等")
    print("  流媒体：Netflix, Hulu, HBO, Disney+ (需登录)")
    print("  音频：SoundCloud, Bandcamp, Spotify (需登录)")
    print("  教育：Coursera, edX, Udemy, Khan Academy, TED")
    print("  完整列表：https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md")
    print()
    
    # 安装建议
    print("【安装命令】")
    print("pip install yt-dlp faster-whisper pandas python-docx")
    print()
    print("如需 GPU 加速，请确保已安装:")
    print("  - NVIDIA 驱动")
    print("  - CUDA Toolkit")
    print("  - PyTorch (CUDA 版本)")
    print("  pip install torch --index-url https://download.pytorch.org/whl/cu118")
    print()
    print("=" * 60)

if __name__ == '__main__':
    main()
