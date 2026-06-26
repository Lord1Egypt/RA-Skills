#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Video Multi-Platform Publish - 一站式多平台视频发布工作流
从视频剪辑到多平台发布全流程自动化
"""

import os
import sys
import subprocess
import argparse
import json
from datetime import datetime
from pathlib import Path

# 平台规格
PLATFORMS = {
    "wechat": {
        "name": "微信公众号",
        "aspect_ratio": "16:9",
        "width": 1920,
        "height": 1080,
        "max_duration": 600,
        "bitrate": "5000k",
        "vertical": False,
        "title_max_length": 64,
        "tags_max_count": 3,
        "best_publish_time": "20:00-22:00"
    },
    "bilibili": {
        "name": "B 站",
        "aspect_ratio": "16:9",
        "width": 1920,
        "height": 1080,
        "max_duration": 900,
        "bitrate": "6000k",
        "vertical": False,
        "title_max_length": 80,
        "tags_max_count": 10,
        "best_publish_time": "18:00-20:00"
    },
    "xiaohongshu": {
        "name": "小红书",
        "aspect_ratio": "9:16",
        "width": 1080,
        "height": 1920,
        "max_duration": 180,
        "bitrate": "8000k",
        "vertical": True,
        "title_max_length": 20,
        "tags_max_count": 5,
        "best_publish_time": "19:00-21:00"
    },
    "douyin": {
        "name": "抖音",
        "aspect_ratio": "9:16",
        "width": 1080,
        "height": 1920,
        "max_duration": 300,
        "bitrate": "8000k",
        "vertical": True,
        "title_max_length": 55,
        "tags_max_count": 5,
        "best_publish_time": "19:00-21:00"
    },
    "youtube": {
        "name": "YouTube",
        "aspect_ratio": "16:9",
        "width": 1920,
        "height": 1080,
        "max_duration": 7200,
        "bitrate": "8000k",
        "vertical": False,
        "title_max_length": 100,
        "tags_max_count": 15,
        "best_publish_time": "14:00-16:00 (UTC)"
    },
    "tiktok": {
        "name": "TikTok",
        "aspect_ratio": "9:16",
        "width": 1080,
        "height": 1920,
        "max_duration": 180,
        "bitrate": "8000k",
        "vertical": True,
        "title_max_length": 150,
        "tags_max_count": 5,
        "best_publish_time": "18:00-20:00 (local)"
    }
}


def check_ffmpeg():
    """检查 ffmpeg 是否安装"""
    try:
        subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def get_video_info(input_file):
    """获取视频信息"""
    cmd = [
        'ffprobe', '-v', 'error',
        '-select_streams', 'v:0',
        '-show_entries', 'stream=duration,width,height,r_frame_rate',
        '-of', 'default=noprint_wrappers=1',
        input_file
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        info = {}
        for line in result.stdout.strip().split('\n'):
            if '=' in line:
                key, value = line.split('=')
                info[key] = value
        return info
    except Exception as e:
        print(f"❌ 获取视频信息失败：{e}")
        return None


def clip_video(input_file, output_file, platform, duration=None, start_time=0):
    """剪辑视频"""
    if platform not in PLATFORMS:
        print(f"❌ 不支持的平台：{platform}")
        return False
    
    platform_info = PLATFORMS[platform]
    
    # 构建 ffmpeg 命令
    cmd = ['ffmpeg', '-i', input_file]
    
    # 起始时间
    if start_time > 0:
        cmd.extend(['-ss', str(start_time)])
    
    # 时长限制
    if duration:
        cmd.extend(['-t', str(duration)])
    else:
        cmd.extend(['-t', str(platform_info['max_duration'])])
    
    # 视频编码
    cmd.extend([
        '-c:v', 'libx264',
        '-b:v', platform_info['bitrate'],
        '-preset', 'medium'
    ])
    
    # 画面处理
    if platform_info['vertical']:
        # 竖屏：裁剪 + 缩放
        cmd.extend([
            '-vf', f"crop=ih*(9/16):ih,scale={platform_info['width']}:{platform_info['height']}"
        ])
    else:
        # 横屏：缩放
        cmd.extend([
            '-vf', f"scale={platform_info['width']}:{platform_info['height']}"
        ])
    
    # 音频编码
    cmd.extend([
        '-c:a', 'aac',
        '-b:a', '128k'
    ])
    
    # 输出文件
    cmd.extend(['-y', output_file])
    
    # 执行
    print(f"  🎬 剪辑 {platform_info['name']} 版本...")
    try:
        subprocess.run(cmd, check=True, capture_output=True)
        print(f"  ✅ {platform_info['name']} 版本完成")
        return True
    except subprocess.CalledProcessError as e:
        print(f"  ❌ {platform_info['name']} 版本失败：{e}")
        return False


def optimize_title(title, platform):
    """优化标题"""
    if platform not in PLATFORMS:
        return title
    
    max_length = PLATFORMS[platform]['title_max_length']
    
    if len(title) <= max_length:
        return title
    
    # 截断标题
    return title[:max_length-3] + "..."


def generate_tags(title, platform):
    """生成标签"""
    if platform not in PLATFORMS:
        return []
    
    # 默认标签
    default_tags = {
        "wechat": ["视频号", "原创", "热门"],
        "bilibili": ["原创", "教程", "技能"],
        "xiaohongshu": ["#视频", "#技巧", "#干货"],
        "douyin": ["#热门", "#推荐", "#热门视频"],
        "youtube": ["Tutorial", "How to", "Tips"],
        "tiktok": ["#fyp", "#viral", "#trending"]
    }
    
    return default_tags.get(platform, [])


def publish_video(video_file, platform, title, description, tags=None):
    """发布视频到平台 (模拟)"""
    if platform not in PLATFORMS:
        print(f"❌ 不支持的平台：{platform}")
        return False
    
    platform_info = PLATFORMS[platform]
    
    # 优化标题
    optimized_title = optimize_title(title, platform)
    
    # 生成标签
    if not tags:
        tags = generate_tags(title, platform)
    
    # 模拟发布
    print(f"  📤 发布到 {platform_info['name']}...")
    print(f"     标题：{optimized_title}")
    print(f"     标签：{', '.join(tags)}")
    print(f"     最佳发布时间：{platform_info['best_publish_time']}")
    print(f"  ✅ {platform_info['name']} 发布成功 (模拟)")
    
    return True


def clip_all_platforms(input_file, output_dir, platforms=None):
    """为所有平台剪辑视频"""
    os.makedirs(output_dir, exist_ok=True)
    
    if not platforms:
        platforms = list(PLATFORMS.keys())
    
    results = {}
    for platform_key in platforms:
        platform_info = PLATFORMS[platform_key]
        output_file = os.path.join(output_dir, f"{Path(input_file).stem}_{platform_key}.mp4")
        
        success = clip_video(input_file, output_file, platform_key)
        results[platform_key] = {
            "success": success,
            "file": output_file if success else None
        }
    
    return results


def publish_all_platforms(video_dir, title, description, platforms=None):
    """发布到所有平台"""
    if not platforms:
        platforms = list(PLATFORMS.keys())
    
    results = {}
    for platform_key in platforms:
        video_file = os.path.join(video_dir, f"video_{platform_key}.mp4")
        
        if not os.path.exists(video_file):
            print(f"⚠️ {platform_key} 视频文件不存在")
            results[platform_key] = {"success": False, "reason": "文件不存在"}
            continue
        
        success = publish_video(video_file, platform_key, title, description)
        results[platform_key] = {"success": success}
    
    return results


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='一站式多平台视频发布工作流')
    parser.add_argument('-i', '--input', required=True, help='输入视频文件')
    parser.add_argument('-p', '--platforms', nargs='+', default=None, help='目标平台 (默认所有平台)')
    parser.add_argument('--title', required=True, help='视频标题')
    parser.add_argument('--desc', '--description', default='', help='视频描述')
    parser.add_argument('--tags', help='标签 (逗号分隔)')
    parser.add_argument('-o', '--output', default='output', help='输出目录')
    parser.add_argument('--clip-only', action='store_true', help='仅剪辑不发布')
    parser.add_argument('--publish-only', action='store_true', help='仅发布不剪辑')
    parser.add_argument('--schedule', help='定时发布时间 (YYYY-MM-DD HH:MM:SS)')
    
    args = parser.parse_args()
    
    # 检查 ffmpeg
    if not check_ffmpeg():
        print("❌ ffmpeg 未安装")
        print("\n请安装 ffmpeg:")
        print("Windows: winget install ffmpeg")
        print("macOS: brew install ffmpeg")
        print("Linux: sudo apt-get install ffmpeg")
        sys.exit(1)
    
    # 检查输入文件
    if not args.publish_only and not os.path.exists(args.input):
        print(f"❌ 输入文件不存在：{args.input}")
        sys.exit(1)
    
    # 解析标签
    tags = None
    if args.tags:
        tags = [tag.strip() for tag in args.tags.split(',')]
    
    print("="*60)
    print("一站式多平台视频发布工作流")
    print("="*60)
    print()
    
    # Stage 1: 视频分析
    if not args.publish_only:
        print("📊 Stage 1: 视频分析")
        video_info = get_video_info(args.input)
        if video_info:
            duration = float(video_info.get('duration', 0))
            width = int(video_info.get('width', 0))
            height = int(video_info.get('height', 0))
            print(f"   时长：{duration:.2f}秒 ({duration/60:.2f}分钟)")
            print(f"   分辨率：{width}x{height}")
        print()
    
    # Stage 2: 自动剪辑
    if not args.publish_only:
        print("🎬 Stage 2: 自动剪辑")
        platforms = args.platforms if args.platforms else list(PLATFORMS.keys())
        clip_results = clip_all_platforms(args.input, args.output, platforms)
        
        # 总结
        print("\n剪辑完成总结:")
        for platform_key, result in clip_results.items():
            platform_name = PLATFORMS[platform_key]['name']
            if result['success']:
                file_size = os.path.getsize(result['file']) / 1024 / 1024
                print(f"  ✅ {platform_name}: {result['file']} ({file_size:.2f} MB)")
            else:
                print(f"  ❌ {platform_name}: 失败")
        print()
    
    # Stage 3 & 4: 内容优化 & 平台发布
    if not args.clip_only:
        print("📤 Stage 3 & 4: 内容优化 & 平台发布")
        platforms = args.platforms if args.platforms else list(PLATFORMS.keys())
        publish_results = publish_all_platforms(args.output, args.title, args.desc, platforms)
        
        # 总结
        print("\n发布完成总结:")
        for platform_key, result in publish_results.items():
            platform_name = PLATFORMS[platform_key]['name']
            if result.get('success'):
                print(f"  ✅ {platform_name}: 发布成功")
            else:
                print(f"  ❌ {platform_name}: 发布失败 - {result.get('reason', '未知错误')}")
        print()
    
    print("="*60)
    print("工作流完成！")
    print("="*60)


if __name__ == "__main__":
    main()
