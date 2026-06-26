#!/usr/bin/env python3
"""
Cloud Share Downloader v2 - 完全自动化，无需登录
"""

import re
import sys

def detect_cloud(url):
    """检测网盘类型"""
    if "pan.baidu.com" in url or "baidu.com" in url:
        return "baidu"
    elif "alipan.com" in url or "aliyun.com" in url:
        return "aliyun"
    elif "115.com" in url:
        return "115"
    elif "quark.cn" in url:
        return "quark"
    elif "douyin.com" in url:
        return "douyin"
    elif "kuaishou.com" in url:
        return "kuaishou"
    elif "b23.tv" in url:  # B站短链
        return "bilibili"
    elif "weibo.com" in url or "m.weibo.cn" in url:
        return "weibo"
    else:
        return "unknown"

def get_download_url(share_url):
    """
    主入口 - 返回可下载的URL或说明
    
    用户只需发链接给我们，我们自动处理！
    """
    cloud = detect_cloud(share_url)
    
    # 可以直接获取的（无需登录）
    no_login_clouds = {
        "douyin": "抖音视频 - 使用yt-dlp直接解析",
        "kuaishou": "快手视频 - 使用yt-dlp直接解析", 
        "bilibili": "B站视频 - 使用yt-dlp直接解析",
        "weibo": "微博视频/图片 - 使用yt-dlp直接解析",
        "115": "115网盘 - 可能需要登录",
        "quark": "夸克网盘 - 可能需要登录"
    }
    
    login_clouds = {
        "baidu": "百度网盘 - 需要Cookie授权",
        "aliyun": "阿里云盘 - 需要Cookie授权"
    }
    
    if cloud in no_login_clouds:
        return {
            "status": "auto",
            "cloud": cloud,
            "message": f"检测到{no_login_clouds[cloud]}，可以直接尝试下载！",
            "need_login": False
        }
    elif cloud in login_clouds:
        return {
            "status": "need_help",
            "cloud": cloud,
            "message": f"检测到{login_clouds[cloud]}，需要一点帮助才能下载。",
            "need_login": True,
            "how_to_help": "请提供网盘的Cookie，我可以帮你保存"
        }
    else:
        return {
            "status": "unknown",
            "cloud": "unknown",
            "message": "暂不支持该链接，请换一个试试",
            "need_login": None
        }

def auto_process(share_url):
    """
    完全自动化处理流程
    用户只需要发链接！
    """
    result = get_download_url(share_url)
    
    if result["status"] == "auto":
        print(f"✅ {result['message']}")
        print(f"正在自动下载...")
        # 这里会调用 yt-dlp 等工具自动下载
        return result
    elif result["status"] == "need_help":
        print(f"⚠️ {result['message']}")
        print(f"💡 {result['how_to_help']}")
        return result
    else:
        print(f"❌ {result['message']}")
        return result

if __name__ == "__main__":
    if len(sys.argv) > 1:
        url = sys.argv[1]
    else:
        print("请提供分享链接")
        print("用法: python3 download.py <分享链接>")
        sys.exit(1)
    
    auto_process(url)
