#!/usr/bin/env python3
"""
平台辅助工具
安全版本 - 提供下载链接解析功能，不直接下载

使用方式:
    python platform-helper.py --url <视频页面URL> --action parse
    
安全说明:
    - 本脚本仅解析页面信息，不执行下载
    - 所有下载操作由用户在浏览器中完成
    - 不绕过任何平台的安全机制
"""

import argparse
import json
import re
import urllib.parse


def parse_jimeng_url(page_url: str) -> dict:
    """
    解析即梦平台视频信息
    
    注意：此函数仅提供解析指导，不执行实际网络请求
    实际视频获取需要用户在浏览器中操作
    """
    
    result = {
        "platform": "jimeng",
        "input_url": page_url,
        "status": "info_required",
        "message": "安全解析模式：需要用户在浏览器中操作"
    }
    
    # 提供浏览器操作指导
    result["browser_steps"] = [
        "1. 在浏览器中打开视频页面",
        "2. 右键点击视频 → 在新标签页打开视频",
        "3. 或按 F12 打开开发者工具 → Network 标签",
        "4. 刷新页面，找到 .mp4 请求",
        "5. 右键 → Copy → Copy link address",
        "6. 使用浏览器下载管理器下载"
    ]
    
    result["security_note"] = (
        "安全提示:\n"
        "- 不要使用第三方下载工具\n"
        "- 确保下载来源可信\n"
        "- 检查文件大小是否合理\n"
        "- 扫描下载的文件"
    )
    
    return result


def parse_douyin_url(page_url: str) -> dict:
    """
    解析抖音视频信息
    
    注意：抖音视频有防盗链保护
    建议使用官方创作者平台下载自己的视频
    """
    
    result = {
        "platform": "douyin",
        "input_url": page_url,
        "status": "info_required",
        "message": "抖音视频有防盗链保护，建议使用官方渠道"
    }
    
    # 检查是否是分享链接
    if "v.douyin.com" in page_url:
        result["type"] = "share_link"
        result["browser_steps"] = [
            "1. 在浏览器中打开分享链接",
            "2. 等待重定向到完整 URL",
            "3. 复制地址栏中的完整 URL",
            "4. 使用创作者平台下载自己的视频"
        ]
    
    result["official_method"] = (
        "官方下载方式:\n"
        "1. 打开抖音 App\n"
        "2. 进入个人主页\n"
        "3. 选择要下载的视频\n"
        "4. 点击分享 → 保存本地"
    )
    
    return result


def generate_download_script(video_url: str, output_name: str = None) -> dict:
    """
    生成安全的下载指导
    
    注意：不执行下载，仅提供指导
    """
    
    if not output_name:
        output_name = "video_download"
    
    # 验证 URL 安全性
    parsed = urllib.parse.urlparse(video_url)
    
    if parsed.scheme not in ["http", "https"]:
        return {
            "status": "error",
            "message": "仅支持 HTTP/HTTPS 协议"
        }
    
    # 提供安全的下载方法
    result = {
        "status": "guide_generated",
        "video_url": video_url,
        "suggested_name": f"{output_name}.mp4",
        "methods": {
            "browser": {
                "description": "浏览器直接下载（推荐）",
                "steps": [
                    f"1. 在浏览器中打开: {video_url}",
                    "2. 按 Ctrl+S 或右键 → 另存为",
                    f"3. 保存为: {output_name}.mp4"
                ]
            },
            "curl": {
                "description": "使用 curl 下载（命令行）",
                "command": f'curl -L -o "{output_name}.mp4" "{video_url}"',
                "note": "在终端中运行此命令"
            },
            "wget": {
                "description": "使用 wget 下载（命令行）",
                "command": f'wget -O "{output_name}.mp4" "{video_url}"',
                "note": "需要安装 wget"
            }
        },
        "security_checklist": [
            "✓ URL 使用 HTTPS 协议" if parsed.scheme == "https" else "⚠ URL 使用 HTTP 协议（不安全）",
            "✓ 确认文件来源可信",
            "✓ 下载后扫描文件",
            "✓ 检查文件大小是否合理"
        ]
    }
    
    return result


def main():
    parser = argparse.ArgumentParser(description="平台辅助工具（安全版）")
    parser.add_argument("--url", "-u", help="视频页面 URL")
    parser.add_argument("--action", "-a", 
                        choices=["parse", "download-guide"], 
                        default="parse", 
                        help="操作类型")
    parser.add_argument("--output", "-o", help="输出文件名")
    
    args = parser.parse_args()
    
    if not args.url:
        print("使用说明:")
        print("  python platform-helper.py --url <URL> --action parse")
        print("  python platform-helper.py --url <视频URL> --action download-guide --output video_name")
        print("\n支持的平台:")
        print("  - jimeng (即梦)")
        print("  - douyin (抖音)")
        return
    
    # 根据平台选择解析方法
    if "jimeng" in args.url.lower():
        result = parse_jimeng_url(args.url)
    elif "douyin" in args.url.lower() or "v.douyin.com" in args.url:
        result = parse_douyin_url(args.url)
    elif args.action == "download-guide":
        result = generate_download_script(args.url, args.output)
    else:
        result = {
            "status": "unknown_platform",
            "url": args.url,
            "message": "未知平台，使用通用解析方法",
            "browser_steps": [
                "1. 在浏览器中打开 URL",
                "2. 使用开发者工具 (F12) 查找视频源",
                "3. 复制视频直链下载"
            ]
        }
    
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
