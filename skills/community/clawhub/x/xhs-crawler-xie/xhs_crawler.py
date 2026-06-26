#!/usr/bin/env python3
"""
小红书爬虫核心模块
- 根据关键词搜索笔记
- 获取笔记详情
- 返回结构化数据
"""

import random
import re
import time
import json
import logging
import sys
from pathlib import Path
from typing import List, Dict, Optional, Any

import requests

# 添加项目根目录到路径，以便导入 xhshow 和 xhs_sign（如果存在）
PROJECT_ROOT = Path(__file__).parent.parent
if (PROJECT_ROOT / "xhshow").exists():
    sys.path.insert(0, str(PROJECT_ROOT))
    from xhshow import Xhshow
    from xhs_sign import sign, get_search_id
else:
    # Skill 独立运行模式，这些模块不可用
    Xhshow = None
    sign = None
    get_search_id = None

from config import (
    BASE_HEADERS,
    XHS_SEARCH_URL,
    XHS_NOTE_DETAIL_URL,
    NOTE_TYPE_DICT,
    SORT_TYPE_DICT,
    DEFAULT_MAX_NOTES,
    REQUEST_DELAY_MIN,
    REQUEST_DELAY_MAX,
    LOG_FILE,
    LOG_LEVEL,
    LOG_FORMAT,
)
from cookie_manager import load_cookie_sync, get_cookie_sync

# 初始化日志
LOG_FILE.parent.mkdir(exist_ok=True)
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format=LOG_FORMAT,
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler(),
    ],
)
log = logging.getLogger(__name__)


class XhsCrawler:
    """小红书爬虫类"""

    def __init__(self, cookie: Optional[str] = None):
        """
        初始化爬虫
        
        Args:
            cookie: Cookie 字符串，为 None 则自动从文件加载
        """
        self.client = Xhshow()
        self.cookie = cookie or load_cookie_sync()
        self.headers = BASE_HEADERS.copy()

        if self.cookie:
            self.headers["cookie"] = self.cookie
            log.info("✅ Cookie 已加载")
        else:
            log.warning("⚠️ 未提供 Cookie，请先登录")

    def _get_a1_from_cookie(self) -> Optional[str]:
        """从 Cookie 中提取 a1 值"""
        if not self.cookie:
            return None
        match = re.search(r'a1=([^;]+)', self.cookie)
        return match.group(1) if match else None

    def _make_request(self, url: str, uri: str, data: dict) -> dict:
        """
        发送带签名的 POST 请求
        
        Args:
            url: 完整 URL
            uri: URI 路径（用于签名）
            data: 请求数据
            
        Returns:
            dict: 响应结果 {"success": bool, "data": ...}
        """
        a1 = self._get_a1_from_cookie()
        if not a1:
            log.error("无法从 Cookie 中提取 a1 值")
            return {"success": False, "error": "无效的 Cookie"}

        # 生成签名
        signature = self.client.sign_xs_post(
            uri=uri,
            a1_value=a1,
            payload=data
        )

        signs = sign(
            a1=a1,
            b1="",
            x_s=signature,
            x_t=str(int(time.time())),
        )

        # 构建请求头
        sign_header = {
            "X-S": signs["x-s"],
            "X-T": signs["x-t"],
            "x-S-Common": signs["x-s-common"],
            "X-B3-Traceid": signs["x-b3-traceid"],
        }

        headers = {**self.headers, **sign_header}
        payload = json.dumps(data, separators=(',', ':'), ensure_ascii=False)

        try:
            response = requests.post(
                url,
                headers=headers,
                data=payload.encode('utf-8'),
                timeout=30
            )
            result = response.json()

            if result.get('success') is False:
                log.error("请求失败，Cookie 可能已失效")
                return {"success": False, "error": "Cookie 失效"}

            return {"success": True, "data": result.get("data")}

        except Exception as e:
            log.error(f"请求异常: {e}")
            return {"success": False, "error": str(e)}

    def _parse_note_data(self, note_data: dict, note_id: str, xsec_token: str) -> dict:
        """
        解析笔记数据
        
        Args:
            note_data: 原始笔记数据
            note_id: 笔记 ID
            xsec_token: xsec_token
            
        Returns:
            dict: 解析后的笔记数据
        """
        note_card = note_data.get('note_card', {})

        # 提取图片列表
        image_list = note_card.get('image_list', [])
        images = [img.get('url', '') for img in image_list]

        # 提取视频链接
        video = note_card.get('video', None)
        video_url = None
        if video:
            streams = (
                video.get('media', {}).get('stream', {}).get('h265', []) or
                video.get('media', {}).get('stream', {}).get('h264', [])
            )
            if streams:
                video_url = streams[0].get('master_url', '')

        # 笔记类型
        note_type = note_card.get('type', '')

        # 构建笔记链接
        note_link = f"https://www.xiaohongshu.com/explore/{note_id}?xsec_token={xsec_token}&xsec_source=pc_feed"

        # 互动信息
        interact_info = note_card.get('interact_info', {})

        return {
            "笔记ID": note_id,
            "笔记类型": "图文" if note_type == 'normal' else "视频" if video_url else note_type,
            "笔记链接": note_link,
            "作者昵称": note_card.get('user', {}).get('nickname', '').strip(),
            "作者ID": note_card.get('user', {}).get('user_id', ''),
            "标题": note_card.get('title', '').strip() if note_card.get('title') else "",
            "内容": note_card.get('desc', '').replace("\n", " ").strip(),
            "点赞数": interact_info.get('liked_count', '0'),
            "收藏数": interact_info.get('collected_count', '0'),
            "评论数": interact_info.get('comment_count', '0'),
            "分享数": interact_info.get('share_count', '0'),
            "图片数量": len(images),
            "图片链接": images,
            "视频链接": video_url if video_url else None,
            "发布时间": self._format_time(note_card.get('time', 0)),
        }

    def _format_time(self, timestamp: int) -> str:
        """格式化时间戳"""
        if not timestamp:
            return ""
        try:
            time_array = time.localtime(int(timestamp / 1000))
            return time.strftime("%Y-%m-%d %H:%M:%S", time_array)
        except:
            return ""

    def get_note_detail(self, note_id: str, xsec_token: str) -> Optional[dict]:
        """
        获取笔记详情
        
        Args:
            note_id: 笔记 ID
            xsec_token: xsec_token
            
        Returns:
            dict: 笔记详情，失败返回 None
        """
        data = {
            "source_note_id": note_id,
            "image_scenes": ["jpg", "webp", "avif"],
            "extra": {"need_body_topic": "1"},
            "xsec_token": xsec_token,
            "xsec_source": "pc_search"
        }

        response = self._make_request(
            XHS_NOTE_DETAIL_URL,
            uri='/api/sns/web/v1/feed',
            data=data
        )

        if not response.get('success'):
            log.error(f"获取笔记详情失败: {note_id}")
            return None

        try:
            note_data = response['data']['items'][0]
            return self._parse_note_data(note_data, note_id, xsec_token)
        except (KeyError, IndexError) as e:
            log.error(f"解析笔记数据失败: {e}")
            return None

    def search_notes(
        self,
        keyword: str,
        note_type: str = "全部",
        sort_type: str = "最多点赞",
        filter_time: str = "不限",
        max_notes: int = DEFAULT_MAX_NOTES
    ) -> List[dict]:
        """
        搜索笔记
        
        Args:
            keyword: 搜索关键词
            note_type: 笔记类型（全部/图文/视频）
            sort_type: 排序方式（综合/最新/最多点赞/最多评论/最多收藏）
            filter_time: 时间筛选（不限/一天内/一周内/半年内）
            max_notes: 最多爬取笔记数
            
        Returns:
            list: 笔记数据列表
        """
        if not self.cookie:
            log.error("未设置 Cookie，无法搜索")
            return []

        log.info(f"开始搜索: {keyword}, 类型: {note_type}, 排序: {sort_type}")

        results = []
        page = 1
        search_id = get_search_id()
        collected_count = 0

        while collected_count < max_notes:
            # 构建筛选条件
            filters = [
                {"tags": [SORT_TYPE_DICT.get(sort_type, "general")], "type": "sort_type"},
                {"tags": ["不限"], "type": "filter_note_type"},
                {"tags": filter_time, "type": "filter_note_time"},
                {"tags": ["不限"], "type": "filter_note_range"},
                {"tags": ["不限"], "type": "filter_pos_distance"}
            ]

            data = {
                "ext_flags": ["query", "note"],  # 启用模糊搜索
                "filters": filters,
                "geo": "",
                "image_formats": ["jpg", "webp", "avif"],
                "keyword": keyword,
                "note_type": NOTE_TYPE_DICT.get(note_type, 0),
                "page": page,
                "page_size": 20,
                "search_id": search_id,
                "sort": "general"
            }

            response = self._make_request(
                XHS_SEARCH_URL,
                uri='/api/sns/web/v1/search/notes',
                data=data
            )

            if not response.get('success'):
                log.error(f"搜索失败: {keyword}, 第 {page} 页")
                break

            json_data = response.get('data', {})
            notes = json_data.get('items', [])

            if not notes:
                log.info(f"没有更多数据，共 {collected_count} 条")
                break

            log.info(f"第 {page} 页找到 {len(notes)} 条结果")

            # 处理每条笔记
            for note in notes:
                if collected_count >= max_notes:
                    break

                # 只处理笔记类型
                if note.get('model_type') != "note":
                    continue

                note_id = note.get('id')
                xsec_token = note.get('xsec_token')

                if not note_id or not xsec_token:
                    continue

                # 添加随机延迟
                time.sleep(random.uniform(REQUEST_DELAY_MIN, REQUEST_DELAY_MAX))

                # 获取笔记详情
                detail = self.get_note_detail(note_id, xsec_token)
                if detail:
                    results.append(detail)
                    collected_count += 1
                    log.info(f"✅ 已采集 {collected_count}/{max_notes}: {detail['标题'][:30]}...")

            # 检查是否还有更多
            if not json_data.get('has_more', False):
                log.info("没有更多页面")
                break

            page += 1

        log.info(f"搜索完成: 共采集 {len(results)} 条笔记")
        return results


def crawl_notes(
    keyword: str,
    cookie: Optional[str] = None,
    note_type: str = "全部",
    sort_type: str = "最新",
    filter_time: str = "不限",
    max_notes: int = DEFAULT_MAX_NOTES
) -> List[dict]:
    """
    便捷的爬虫函数（供 OpenClaw 调用）
    
    Args:
        keyword: 搜索关键词
        cookie: Cookie 字符串，为 None 则自动加载
        note_type: 笔记类型
        sort_type: 排序方式
        filter_time: 时间筛选
        max_notes: 最多爬取数量
        
    Returns:
        list: 笔记数据列表
        
    Example:
        >>> results = crawl_notes("新燕宝", max_notes=5)
        >>> print(results[0]['标题'])
        
    默认排序: 最新
    """
    # 如果没有提供 cookie，尝试获取有效 cookie
    if not cookie:
        cookie = get_cookie_sync()
        if not cookie:
            log.error("无法获取有效 Cookie，请先运行 login.py 登录")
            return []

    crawler = XhsCrawler(cookie=cookie)
    return crawler.search_notes(
        keyword=keyword,
        note_type=note_type,
        sort_type=sort_type,
        filter_time=filter_time,
        max_notes=max_notes
    )


if __name__ == "__main__":
    # 测试
    results = crawl_notes("中间带新燕宝", max_notes=2)
    print(f"\n共获取 {len(results)} 条笔记")
    for i, note in enumerate(results, 1):
        print(f"\n[{i}] {note['标题']}")
        print(f"    作者: {note['作者昵称']}")
        print(f"    点赞: {note['点赞数']}")
        print(f"    链接: {note['笔记链接']}")
