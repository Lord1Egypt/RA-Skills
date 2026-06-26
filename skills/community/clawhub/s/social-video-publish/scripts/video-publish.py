#!/usr/bin/env python3
"""
多平台视频图文发布助手 - 主脚本
支持抖音、快手、B站、小红书、微信视频号五大平台

⚠️ 安全声明：
- 本脚本仅在用户明确授权时操作
- 所有操作都在用户本地浏览器中进行
- 不会自动登录或存储任何账户凭证
"""

import os
import sys
import json
import argparse
from pathlib import Path

# 尝试导入平台助手
try:
    from platform_helper import PLATFORM_CONFIGS, get_publish_url, validate_video
except ImportError:
    print("❌ 错误：找不到 platform_helper.py，请确保在同一目录下")
    sys.exit(1)


def parse_args():
    parser = argparse.ArgumentParser(description='多平台视频图文发布助手')
    parser.add_argument('--platform', '-p', nargs='+', 
                        choices=['douyin', 'kuaishou', 'bilibili', 'xiaohongshu', 'video'],
                        help='目标平台列表')
    parser.add_argument('--video', '-v', type=str, required=True,
                        help='视频文件路径')
    parser.add_argument('--title', '-t', type=str, default='',
                        help='视频标题')
    parser.add_argument('--desc', '-d', type=str, default='',
                        help='视频描述')
    parser.add_argument('--tags', '-g', nargs='*', default=[],
                        help='标签列表')
    parser.add_argument('--auto', '-a', action='store_true',
                        help='自动模式（需要浏览器已登录）')
    return parser.parse_args()


def check_video_file(video_path: str) -> tuple[bool, str]:
    """检查视频文件"""
    path = Path(video_path)
    
    if not path.exists():
        return False, f"视频文件不存在: {video_path}"
    
    if not path.is_file():
        return False, f"路径不是文件: {video_path}"
    
    # 检查文件大小
    size_mb = path.stat().st_size / (1024 * 1024)
    if size_mb < 0.1:
        return False, f"视频文件太小: {size_mb:.2f}MB"
    
    # 检查扩展名
    valid_exts = ['.mp4', '.mov', '.avi', '.mkv', '.flv', '.wmv']
    if path.suffix.lower() not in valid_exts:
        return False, f"不支持的视频格式: {path.suffix}，支持: {', '.join(valid_exts)}"
    
    return True, f"视频文件正常，大小: {size_mb:.2f}MB"


def print_platform_guide(platform: str):
    """打印平台发布指导"""
    config = PLATFORM_CONFIGS.get(platform, {})
    publish_url = config.get('publish_url', '')
    
    print(f"\n📤 发布到 {config.get('name', platform)}")
    print(f"   说明: {config.get('desc', '')}")
    if publish_url:
        print(f"   发布地址: {publish_url}")
    print(f"   标签: {', '.join(config.get('tags', []))}")


def generate_browser_commands(platform: str, video_path: str, title: str, desc: str, tags: list):
    """生成浏览器自动化命令（用于 xbrowser skill）"""
    config = PLATFORM_CONFIGS.get(platform, {})
    publish_url = config.get('publish_url', '')
    
    commands = []
    
    if publish_url:
        commands.append(f'open {publish_url}')
        commands.append('wait --load networkidle')
        commands.append('snapshot -i')
    
    # 生成说明文本
    guide = f"""
【{config.get('name', platform)} 发布步骤】
1. 点击"上传视频"按钮
2. 选择视频文件: {video_path}
3. 填写标题: {title}
4. 填写描述: {desc}
5. 添加标签: {', '.join(tags) if tags else '无'}
6. 设置封面（可选）
7. 检查平台特有选项
8. 点击发布
"""
    return commands, guide


def main():
    args = parse_args()
    
    print("🎬 多平台视频图文发布助手 v2.0.0")
    print("=" * 50)
    
    # 检查视频文件
    valid, msg = check_video_file(args.video)
    if not valid:
        print(f"❌ {msg}")
        sys.exit(1)
    print(f"✅ {msg}")
    
    # 确定目标平台
    platforms = args.platform or ['douyin']
    
    print(f"\n📋 目标平台: {', '.join(p for p in platforms)}")
    print(f"📝 标题: {args.title or '（未设置）'}")
    print(f"📖 描述: {args.desc or '（未设置）'}")
    print(f"🏷️  标签: {', '.join(args.tags) if args.tags else '（未设置）'}")
    
    # 生成各平台发布指导
    for platform in platforms:
        print_platform_guide(platform)
        
        if args.auto:
            cmds, guide = generate_browser_commands(platform, args.video, args.title, args.desc, args.tags)
            print(f"   浏览器命令: {cmds}")
            print(guide)
    
    print("\n" + "=" * 50)
    print("💡 提示：")
    print("   1. 请确保已在浏览器中登录目标平台账号")
    print("   2. 使用 --auto 参数可启用自动化模式")
    print("   3. 查看 --help 获取更多选项")
    print("\n⚠️  安全提示：所有操作都在本地浏览器完成，不会上传您的凭证")


if __name__ == '__main__':
    main()