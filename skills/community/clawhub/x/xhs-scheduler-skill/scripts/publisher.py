#!/usr/bin/env python3
"""
小红书发布器 - 使用 REST API
"""

import argparse
import json
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
import requests


class XiaohongshuPublisher:
    """小红书发布器 - REST API 版本"""
    
    def __init__(self, base_url: str = "http://localhost:18060"):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })
    
    def _api_get(self, endpoint: str, timeout: int = 30) -> Dict:
        """发送 GET 请求"""
        url = f"{self.base_url}{endpoint}"
        try:
            response = self.session.get(url, timeout=timeout)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"success": False, "error": str(e)}
    
    def _api_post(self, endpoint: str, data: Dict, timeout: int = 60) -> Dict:
        """发送 POST 请求"""
        url = f"{self.base_url}{endpoint}"
        try:
            response = self.session.post(url, json=data, timeout=timeout)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"success": False, "error": str(e)}
    
    def check_login_status(self) -> Dict:
        """检查登录状态"""
        result = self._api_get("/api/v1/login/status")
        if result.get("success"):
            data = result.get("data", {})
            return {
                "logged_in": data.get("is_logged_in", False),
                "username": data.get("username", ""),
                "message": result.get("message", "")
            }
        return {
            "logged_in": False,
            "error": result.get("error", result.get("message", "未知错误"))
        }
    
    def _resolve_image_paths(self, images: List[str]) -> List[str]:
        """将相对路径转换为绝对路径"""
        resolved = []
        for img_path in images:
            path = Path(img_path)
            if not path.is_absolute():
                # 相对于当前工作目录解析
                path = Path.cwd() / path
            resolved.append(str(path.resolve()))
        return resolved
    
    def publish_note(self, title: str, content: str, images: List[str] = None,
                     tags: List[str] = None) -> Dict:
        """
        发布图文笔记
        
        Args:
            title: 笔记标题
            content: 笔记内容
            images: 图片路径列表
            tags: 标签列表
        """
        # 处理图片路径
        images = images or []
        images = self._resolve_image_paths(images)
        
        # 准备发布数据（使用大写字段名匹配 Go 结构体）
        publish_data = {
            "Title": title,
            "Content": content,
            "Images": images,
            "Tags": tags or []
        }
        
        # 小红书要求至少一张图片
        if not publish_data["Images"]:
            return {
                "success": False,
                "error": "小红书发布需要至少一张图片，请提供图片路径"
            }
        
        result = self._api_post("/api/v1/publish", publish_data, timeout=300)
        
        if result.get("success"):
            data = result.get("data", {})
            return {
                "success": True,
                "note_id": data.get("note_id", ""),
                "url": data.get("url", ""),
                "message": result.get("message", "发布成功")
            }
        return {
            "success": False,
            "error": result.get("error", result.get("message", "发布失败"))
        }
    
    def publish_video(self, title: str, content: str, video_path: str,
                      cover_path: str = None, tags: List[str] = None) -> Dict:
        """
        发布视频笔记
        
        Args:
            title: 视频标题
            content: 视频描述
            video_path: 视频文件路径
            cover_path: 封面图片路径
            tags: 标签列表
        """
        publish_data = {
            "Title": title,
            "Content": content,
            "VideoPath": video_path,
            "CoverPath": cover_path or "",
            "Tags": tags or []
        }
        
        result = self._api_post("/api/v1/publish/video", publish_data, timeout=300)
        
        if result.get("success"):
            data = result.get("data", {})
            return {
                "success": True,
                "note_id": data.get("note_id", ""),
                "url": data.get("url", ""),
                "message": result.get("message", "发布成功")
            }
        return {
            "success": False,
            "error": result.get("error", result.get("message", "发布失败"))
        }


def main():
    parser = argparse.ArgumentParser(description="小红书发布器")
    parser.add_argument("--base-url", default="http://localhost:18060",
                       help="MCP服务基础URL")
    
    subparsers = parser.add_subparsers(dest="command", help="可用命令")
    
    # check-login 命令
    subparsers.add_parser("check-login", help="检查登录状态")
    
    # publish 命令
    publish_parser = subparsers.add_parser("publish", help="发布图文笔记")
    publish_parser.add_argument("--title", required=True, help="笔记标题")
    publish_parser.add_argument("--content", required=True, help="笔记内容")
    publish_parser.add_argument("--images", help="图片路径，逗号分隔")
    publish_parser.add_argument("--tags", help="标签，逗号分隔")
    
    # publish-video 命令
    video_parser = subparsers.add_parser("publish-video", help="发布视频笔记")
    video_parser.add_argument("--title", required=True, help="视频标题")
    video_parser.add_argument("--content", required=True, help="视频描述")
    video_parser.add_argument("--video", required=True, help="视频文件路径")
    video_parser.add_argument("--cover", help="封面图片路径")
    video_parser.add_argument("--tags", help="标签，逗号分隔")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    publisher = XiaohongshuPublisher(base_url=args.base_url)
    
    if args.command == "check-login":
        result = publisher.check_login_status()
        if result.get("logged_in"):
            print(f"[OK] 已登录")
            print(f"   用户名: {result.get('username', 'N/A')}")
        else:
            print(f"[FAIL] 未登录")
            print(f"   错误: {result.get('error', '未知错误')}")
            print(f"   请使用小红书APP扫描二维码登录")
    
    elif args.command == "publish":
        images = args.images.split(",") if args.images else []
        tags = args.tags.split(",") if args.tags else []
        
        print(f"正在发布图文笔记...")
        print(f"   标题: {args.title}")
        
        result = publisher.publish_note(args.title, args.content, images, tags)
        
        if result.get("success"):
            print(f"[OK] 发布成功")
            print(f"   笔记ID: {result.get('note_id')}")
            print(f"   链接: {result.get('url')}")
        else:
            print(f"[FAIL] 发布失败")
            print(f"   错误: {result.get('error')}")
    
    elif args.command == "publish-video":
        tags = args.tags.split(",") if args.tags else []
        
        print(f"正在发布视频笔记...")
        print(f"   标题: {args.title}")
        print(f"   视频: {args.video}")
        
        result = publisher.publish_video(
            args.title, args.content, args.video, args.cover, tags
        )
        
        if result.get("success"):
            print(f"[OK] 发布成功")
            print(f"   笔记ID: {result.get('note_id')}")
            print(f"   链接: {result.get('url')}")
        else:
            print(f"[FAIL] 发布失败")
            print(f"   错误: {result.get('error')}")


if __name__ == "__main__":
    main()
