#!/usr/bin/env python3
"""
小红书搜索核心脚本 (生产级)
集成所有测试功能,支持搜索、翻页、数据筛选和保存
"""
import http.client
import json
import os
from datetime import datetime
from urllib.parse import urlencode
from typing import Dict, List, Optional, Any
import re
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()


class XiaohongshuSearcher:
    """小红书搜索客户端"""

    def __init__(
        self,
        token: Optional[str] = None,
        host: str = "api.tikhub.io",
        path: str = "/api/v1/xiaohongshu/app/search_notes",
        timeout: int = 30
    ):
        """
        初始化搜索客户端

        Args:
            token: API Token (默认从环境变量TIKHUB_TOKEN读取)
            host: API主机地址
            path: API路径
            timeout: 请求超时时间(秒)
        """
        self.token = token or os.getenv("TIKHUB_TOKEN", "")
        self.host = host
        self.path = path
        self.timeout = timeout
        self.search_id = ""
        self.session_id = ""

    def search(
        self,
        keyword: str,
        page: int = 1,
        sort_type: str = "general",
        filter_note_type: str = "不限",
        filter_note_time: str = "不限",
        reset_session: bool = False
    ) -> Dict[str, Any]:
        """
        搜索小红书笔记

        Args:
            keyword: 搜索关键词
            page: 页码,从1开始
            sort_type: 排序方式 (general/time_descending/popularity_descending/comment_descending/collect_descending)
            filter_note_type: 笔记类型筛选 (不限/视频笔记/普通笔记)
            filter_note_time: 时间筛选 (不限/一天内/一周内/半年内)
            reset_session: 是否重置会话(新关键词时使用)

        Returns:
            dict: API响应数据
        """
        # 重置会话
        if reset_session:
            self.search_id = ""
            self.session_id = ""

        # 构建参数
        params = {
            "keyword": keyword,
            "page": page,
            "search_id": self.search_id,
            "session_id": self.session_id,
            "sort_type": sort_type,
            "filter_note_type": filter_note_type,
            "filter_note_time": filter_note_time,
        }

        # 发送请求
        query = urlencode(params, doseq=True)
        full_path = f"{self.path}?{query}" if query else self.path

        conn = http.client.HTTPSConnection(self.host, timeout=self.timeout)
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/json",
        }

        conn.request("GET", full_path, headers=headers)
        res = conn.getresponse()
        raw = res.read()
        conn.close()

        # 解析响应
        text = raw.decode("utf-8", errors="replace")
        try:
            data = json.loads(text)
        except json.JSONDecodeError:
            return {
                "success": False,
                "error": "JSON解析失败",
                "raw": text,
                "_http_status": res.status
            }

        # 保存翻页参数
        if data.get("code") == 200:
            inner_data = data.get("data", {})
            if isinstance(inner_data, str):
                try:
                    inner_data = json.loads(inner_data)
                except:
                    pass

            if isinstance(inner_data, dict):
                self.search_id = inner_data.get("searchId", "")
                self.session_id = inner_data.get("sessionId", "")

        data["_http_status"] = res.status
        return data

    def extract_items(self, result: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        从API响应中提取笔记列表

        Args:
            result: API响应数据

        Returns:
            list: 笔记列表
        """
        items = []
        data = result.get("data") if isinstance(result, dict) else None

        if isinstance(data, dict):
            inner = data.get("data")
            if isinstance(inner, dict):
                items = inner.get("items", [])
            else:
                items = data.get("items", [])
        elif isinstance(data, str):
            try:
                inner_data = json.loads(data)
                if isinstance(inner_data, dict):
                    items = inner_data.get("data", {}).get("items", [])
            except:
                pass

        return items

    def extract_core_info(self, result: Dict[str, Any], keyword: str = "") -> Dict[str, Any]:
        """
        提取核心信息

        Args:
            result: API响应数据
            keyword: 搜索关键词

        Returns:
            dict: 包含核心信息的字典
        """
        # 提取搜索信息
        search_info = {
            "keyword": keyword,
            "search_time": datetime.now().isoformat(),
            "search_id": self.search_id,
            "session_id": self.session_id,
        }

        # 提取笔记列表
        items = self.extract_items(result)
        notes = []

        for entry in items:
            if not isinstance(entry, dict):
                continue

            note = entry.get("note")
            if not isinstance(note, dict):
                continue

            # 提取基本信息
            title = (note.get("title") or "").strip()
            desc = (note.get("desc") or "").strip()

            # 提取标签
            tags = self._extract_tags(title, desc)

            # 提取作者信息
            user = note.get("user") or {}
            author = {
                "user_id": user.get("userid"),
                "red_id": user.get("red_id"),
                "nickname": user.get("nickname"),
                "avatar": user.get("images"),
            }

            # 提取互动数据
            interact_info = note.get("interact_info") or {}
            stats = {
                "liked_count": note.get("liked_count") or interact_info.get("liked_count", 0),
                "collected_count": note.get("collected_count") or interact_info.get("collected_count", 0),
                "comments_count": note.get("comments_count") or interact_info.get("comments_count", 0),
                "shared_count": note.get("shared_count") or interact_info.get("shared_count", 0),
            }

            # 提取媒体信息
            media = self._extract_media_info(note)

            # 笔记类型
            note_type = note.get("type", "unknown")
            if note_type == "normal":
                note_type_cn = "图文笔记"
            elif note_type == "video":
                note_type_cn = "视频笔记"
            else:
                note_type_cn = note_type

            note_info = {
                "note_id": note.get("id") or note.get("note_id"),
                "title": title,
                "desc": desc[:200] + "..." if len(desc) > 200 else desc,  # 限制描述长度
                "tags": tags,
                "note_type": note_type,
                "note_type_cn": note_type_cn,
                "author": author,
                "stats": stats,
                "media": media,
                "publish_time": note.get("timestamp"),
                "update_time": note.get("update_time"),
            }

            notes.append(note_info)

        return {
            "search_info": search_info,
            "total_count": len(notes),
            "notes": notes,
        }

    def _extract_tags(self, title: str, desc: str) -> List[str]:
        """提取标签"""
        tags = []

        # 从标题和描述中提取 #标签
        for text in [title, desc]:
            if not text:
                continue
            matches = re.findall(r"#([^#\\s]+)", text)
            tags.extend([f"#{match}" for match in matches])

        # 去重
        seen = set()
        unique_tags = []
        for tag in tags:
            if tag not in seen:
                seen.add(tag)
                unique_tags.append(tag)

        return unique_tags

    def _extract_media_info(self, note: Dict[str, Any]) -> Dict[str, Any]:
        """提取媒体信息"""
        media = {
            "type": note.get("type", "unknown"),
            "images": [],
            "videos": [],
        }

        # 提取图片
        images_list = note.get("images_list") or []
        for img in images_list[:9]:  # 最多9张图
            if isinstance(img, dict):
                image_info = {
                    "url": img.get("url"),
                    "url_large": img.get("url_size_large"),
                    "width": img.get("width"),
                    "height": img.get("height"),
                }
                media["images"].append(image_info)

        # 提取视频
        video_info = note.get("video_info_v2")
        if video_info:
            media_data = video_info.get("media", {})
            streams = media_data.get("stream", {})

            # H264
            h264_list = streams.get("h264", [])
            if h264_list:
                video_url = h264_list[0].get("master_url")
                media["videos"].append({
                    "type": "h264",
                    "url": video_url,
                    "quality": "HD",
                })

            # H265
            h265_list = streams.get("h265", [])
            for stream in h265_list[:2]:  # 最多2个质量
                quality_type = stream.get("quality_type", "unknown")
                media["videos"].append({
                    "type": "h265",
                    "url": stream.get("master_url"),
                    "quality": quality_type,
                })

        return media


def save_results(
    result: Dict[str, Any],
    core_info: Dict[str, Any],
    save_dir: str = "responses"
) -> tuple[str, str]:
    """
    保存结果到文件

    Args:
        result: 完整的API响应
        core_info: 提取的核心信息
        save_dir: 保存目录

    Returns:
        tuple: (完整响应文件路径, 核心信息文件路径)
    """
    os.makedirs(save_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    keyword = core_info.get("search_info", {}).get("keyword", "unknown")

    # 1. 保存完整响应
    full_filename = f"{timestamp}_xhs_search_{keyword}_full.json"
    full_path = os.path.join(save_dir, full_filename)
    with open(full_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    # 2. 保存核心信息
    core_filename = f"{timestamp}_xhs_search_{keyword}_core.json"
    core_path = os.path.join(save_dir, core_filename)
    with open(core_path, "w", encoding="utf-8") as f:
        json.dump(core_info, f, ensure_ascii=False, indent=2)

    return full_path, core_path


def main():
    """主函数 - 示例用法"""
    # 初始化搜索客户端
    searcher = XiaohongshuSearcher()

    # 搜索
    keyword = "猫粮"
    print(f"🔍 搜索关键词: {keyword}")

    result = searcher.search(
        keyword=keyword,
        page=1,
        sort_type="general",
        filter_note_type="不限",
        filter_note_time="不限",
        reset_session=True
    )

    # 检查响应
    if result.get("code") != 200:
        print(f"❌ 搜索失败: {result.get('message')}")
        return

    print(f"✅ 搜索成功,状态码: {result.get('code')}")

    # 提取核心信息
    core_info = searcher.extract_core_info(result, keyword)

    print(f"📊 搜索结果:")
    print(f"   - 返回数量: {core_info.get('total_count')}")
    print(f"   - Search ID: {core_info.get('search_info', {}).get('search_id')}")
    print(f"   - Session ID: {core_info.get('search_info', {}).get('session_id')}")

    # 显示前3条
    notes = core_info.get("notes", [])
    if notes:
        print(f"\n📝 前3条笔记:")
        for i, note in enumerate(notes[:3], 1):
            print(f"\n   {i}. {note.get('title')}")
            print(f"      类型: {note.get('note_type_cn')}")
            print(f"      作者: {note.get('author', {}).get('nickname')}")
            print(f"      点赞: {note.get('stats', {}).get('liked_count')}")
            print(f"      收藏: {note.get('stats', {}).get('collected_count')}")
            print(f"      评论: {note.get('stats', {}).get('comments_count')}")
            tags = note.get('tags', [])
            if tags:
                print(f"      标签: {', '.join(tags[:5])}")

    # 保存结果
    full_path, core_path = save_results(result, core_info)
    print(f"\n💾 结果已保存:")
    print(f"   - 完整响应: {full_path}")
    print(f"   - 核心信息: {core_path}")


if __name__ == "__main__":
    main()
