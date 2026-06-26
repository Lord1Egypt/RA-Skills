#!/usr/bin/env python3
"""
视频发布辅助工具
安全版本 - 不执行任何网络请求，仅提供操作指导

使用方式:
    python video-publish.py --platform <平台名> --action <操作>

示例:
    python video-publish.py --platform douyin --action guide
"""

import argparse
import sys
import json
from pathlib import Path


# 平台配置信息（仅用于指导，不存储凭证）
PLATFORM_CONFIG = {
    "douyin": {
        "name": "抖音",
        "url": "https://creator.douyin.com",
        "max_size_mb": 4096,
        "formats": ["mp4", "mov", "webm"],
        "max_duration_min": 60,
        "note": "需要在创作者平台登录"
    },
    "kuaishou": {
        "name": "快手",
        "url": "https://cp.kuaishou.com",
        "max_size_mb": 2048,
        "formats": ["mp4", "mov"],
        "max_duration_min": 30,
        "note": "支持批量上传"
    },
    "bilibili": {
        "name": "B站",
        "url": "https://member.bilibili.com",
        "max_size_mb": 8192,
        "formats": ["mp4", "flv", "mov"],
        "max_duration_min": 0,  # 无限制
        "note": "支持高清和4K"
    },
    "xiaohongshu": {
        "name": "小红书",
        "url": "https://creator.xiaohongshu.com",
        "max_size_mb": 1024,
        "formats": ["mp4", "mov"],
        "max_duration_min": 15,
        "note": "竖版视频效果更佳"
    }
}


def get_platform_guide(platform: str) -> str:
    """获取平台发布指南"""
    platform = platform.lower()
    if platform not in PLATFORM_CONFIG:
        return f"未知平台: {platform}\n支持的平台: {', '.join(PLATFORM_CONFIG.keys())}"

    config = PLATFORM_CONFIG[platform]
    
    guide = f"""
{'=' * 50}
{config['name']} ({platform}) 发布指南
{'=' * 50}

📍 创作者平台: {config['url']}

📋 视频要求:
   - 最大文件大小: {config['max_size_mb']} MB
   - 支持格式: {', '.join(config['formats'])}
   - 最大时长: {config['max_duration_min']} 分钟{'(无限制)' if config['max_duration_min'] == 0 else ''}
   - 备注: {config['note']}

🔐 安全提示:
   - 请确保已在浏览器中手动登录
   - 不要分享验证码或登录凭证
   - 定期检查账号活动记录

💡 发布步骤:
   1. 在浏览器中打开创作者平台
   2. 点击"上传视频"按钮
   3. 选择本地视频文件
   4. 填写标题、描述、标签
   5. 设置发布时间（可选）
   6. 确认发布

{'=' * 50}
"""
    return guide


def validate_video_file(file_path: str, platform: str) -> dict:
    """验证视频文件是否符合平台要求（仅本地检查，不上传）"""
    path = Path(file_path)
    
    if not path.exists():
        return {"valid": False, "error": f"文件不存在: {file_path}"}
    
    if platform.lower() not in PLATFORM_CONFIG:
        return {"valid": False, "error": f"未知平台: {platform}"}
    
    config = PLATFORM_CONFIG[platform.lower()]
    
    # 检查文件大小
    file_size_mb = path.stat().st_size / (1024 * 1024)
    if file_size_mb > config['max_size_mb']:
        return {
            "valid": False, 
            "error": f"文件过大: {file_size_mb:.1f}MB，平台限制: {config['max_size_mb']}MB"
        }
    
    # 检查文件格式
    suffix = path.suffix.lstrip('.').lower()
    if suffix not in config['formats']:
        return {
            "valid": False,
            "error": f"不支持格式: .{suffix}，支持: {', '.join(config['formats'])}"
        }
    
    return {
        "valid": True,
        "file_name": path.name,
        "file_size_mb": round(file_size_mb, 1),
        "platform": config['name']
    }


def main():
    parser = argparse.ArgumentParser(description="视频发布辅助工具（安全版）")
    parser.add_argument("--platform", "-p", help="目标平台 (douyin/kuaishou/bilibili/xiaohongshu)")
    parser.add_argument("--action", "-a", choices=["guide", "validate"], default="guide", help="操作类型")
    parser.add_argument("--file", "-f", help="视频文件路径（用于验证）")
    
    args = parser.parse_args()
    
    if args.action == "guide" and args.platform:
        print(get_platform_guide(args.platform))
    elif args.action == "validate" and args.file and args.platform:
        result = validate_video_file(args.file, args.platform)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif args.action == "guide" and not args.platform:
        print("支持的平台:")
        for key, config in PLATFORM_CONFIG.items():
            print(f"  - {key}: {config['name']} ({config['url']})")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
