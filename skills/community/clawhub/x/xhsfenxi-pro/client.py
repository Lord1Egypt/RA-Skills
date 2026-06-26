"""
XhsClient — 小红书数据抓取 + 分析客户端
基于 SeleniumBase UC Mode + XHR 拦截，无需逆向签名算法
整合 xhsfenxi 三型博主分类体系 + 五层账号模型

用法:
    from xhscosmoskill import XhsClient

    with XhsClient() as xhs:
        notes = xhs.search("咖啡", limit=30)
        user_notes = xhs.get_user_notes("USER_ID_HEX_HERE")
        report = xhs.analyze_account(user_notes, creator_name="博主名")
        detail = xhs.get_note_detail("https://www.xiaohongshu.com/explore/xxx")
"""
import json
import time
import os
from typing import List, Optional

from .browser import BrowserSession
from .models import Note, UserProfile
from .parser import (
    parse_search_response,
    parse_user_notes_response,
    parse_note_detail_response,
    parse_comment_page_response,
    parse_dom_notes,
)
from .analyzer import analyze_account as _analyze_account

DEFAULT_COOKIES = os.path.join(os.path.dirname(__file__), "..", "xhs_cookies.json")


class XhsClient:
    """
    小红书数据抓取客户端

    参数:
        cookies_file: cookie 文件路径（运行 xhs_login.py 生成）
        headless: 是否无头模式（默认 False，首次建议 False 观察行为）
        scroll_times: 每次操作滚动次数（影响加载数量）

    支持 context manager（with 语句）或手动 open()/close()
    """

    def __init__(
        self,
        cookies_file: str = DEFAULT_COOKIES,
        headless: bool = True,
        scroll_times: int = 5,
    ):
        self.cookies_file = os.path.abspath(cookies_file)
        self.headless = headless
        self.scroll_times = scroll_times
        self._session: Optional[BrowserSession] = None

    def open(self):
        self._session = BrowserSession(self.cookies_file, self.headless)
        self._session.__enter__()
        return self

    def close(self):
        if self._session:
            self._session.__exit__(None, None, None)
            self._session = None

    def __enter__(self):
        return self.open()

    def __exit__(self, *args):
        self.close()

    # ─── 公开接口 ──────────────────────────────────────────────

    def search(self, keyword: str, limit: int = 20, scroll_times: int = None) -> List[Note]:
        """
        搜索笔记

        参数:
            keyword: 搜索关键词
            limit: 最大返回数量
            scroll_times: 滚动次数（越多加载越多，默认用初始化值）

        返回: List[Note]
        """
        self._ensure_session()
        url = f"https://www.xiaohongshu.com/search_result?keyword={keyword}&source=web_explore_feed"
        self._session.clear_cache()
        self._session.navigate(url, wait=3)
        self._session.scroll_and_collect(scroll_times or self.scroll_times)

        cache = self._session.get_api_cache()
        notes = parse_search_response(cache)

        # API 拦截失败时 fallback 到 DOM
        if not notes:
            notes = parse_dom_notes(self._session)

        return notes[:limit]

    def get_user_notes(self, user_id: str, limit: int = 50, scroll_times: int = None) -> List[Note]:
        """
        获取用户主页所有笔记

        参数:
            user_id: 小红书用户 ID（URL 中的那串 hex）
            limit: 最大返回数量
            scroll_times: 滚动次数

        返回: List[Note]
        """
        self._ensure_session()
        url = f"https://www.xiaohongshu.com/user/profile/{user_id}"
        self._session.clear_cache()
        self._session.navigate(url, wait=4)

        seen_ids = set()
        notes = []
        n_scroll = scroll_times or self.scroll_times

        for _ in range(n_scroll):
            self._session.execute_script("window.scrollBy(0, 1500)")
            time.sleep(2)
            cache = self._session.get_api_cache()
            batch = parse_user_notes_response(cache)

            # DOM fallback if API empty
            if not batch:
                batch = parse_dom_notes(self._session)

            for n in batch:
                key = n.id or n.url or n.title
                if key and key not in seen_ids:
                    seen_ids.add(key)
                    notes.append(n)

            if len(notes) >= limit:
                break

        return notes[:limit]

    def get_note_detail(self, note_url: str) -> Optional[Note]:
        """
        获取单篇笔记详情（正文、评论、互动数据）

        参数:
            note_url: 笔记完整 URL

        返回: Note 或 None
        """
        self._ensure_session()
        self._session.clear_cache()
        self._session.navigate(note_url, wait=4)

        cache = self._session.get_api_cache()
        note = parse_note_detail_response(cache)

        # API 失败时从 DOM 提取正文和标题
        if not note:
            note = Note()
            note.url = note_url
            for sel in ["#detail-desc", "span#detail-desc", ".desc.expand", "[class*='desc']"]:
                try:
                    el = self._session.find_elements(sel)
                    if el and el[0].text.strip():
                        note.content = el[0].text.strip()
                        break
                except Exception:
                    pass
            for sel in ["#detail-title", ".note-content .title", "h1", "[class*='title']"]:
                try:
                    el = self._session.find_elements(sel)
                    if el and el[0].text.strip():
                        note.title = el[0].text.strip()
                        break
                except Exception:
                    pass

        # 无论 API 是否成功，都尝试从 comment/page 补充评论
        if not note.comments:
            note.comments = parse_comment_page_response(cache)

        return note if (note and (note.content or note.title)) else None

    def post_comment(self, note_url: str, text: str) -> bool:
        """
        在笔记下发表评论

        参数:
            note_url: 笔记完整 URL
            text: 评论内容

        返回: True 成功 / False 失败
        """
        self._ensure_session()
        self._session.navigate(note_url, wait=4)

        try:
            from selenium.webdriver.common.action_chains import ActionChains
            from selenium.webdriver.common.keys import Keys

            driver = self._session.driver

            # 1. JS 点击评论区占位符，激活输入框
            activate_selectors = [
                ".comment-input-inner-container",
                "[class*='comment-input']",
                ".input-inner-container",
                "[class*='commentInput']",
                "[class*='input-box']",
            ]
            activated = False
            for sel in activate_selectors:
                els = self._session.find_elements(sel)
                if els:
                    driver.execute_script("arguments[0].scrollIntoView({block:'center'})", els[0])
                    time.sleep(0.5)
                    driver.execute_script("arguments[0].click()", els[0])
                    activated = True
                    time.sleep(1)
                    break

            if not activated:
                print("  ✗ 找不到评论输入框")
                return False

            # 2. 找激活后的 contenteditable 或 textarea
            editable_selectors = [
                "[contenteditable='true']",
                "textarea",
                "[class*='ql-editor']",
                "[class*='editor']",
            ]
            editable = None
            for sel in editable_selectors:
                els = self._session.find_elements(sel)
                if els:
                    editable = els[0]
                    break

            if editable:
                ActionChains(driver).move_to_element(editable).click().send_keys(text).perform()
            else:
                # fallback: 直接用 active element
                ActionChains(driver).send_keys(text).perform()

            time.sleep(1)

            # 3. 点击发送按钮
            submit_selectors = [
                "[class*='submit']",
                "[class*='send']",
                "button.submit",
                "[class*='confirm']",
            ]
            submitted = False
            for sel in submit_selectors:
                els = self._session.find_elements(sel)
                # 过滤不可见元素
                for el in els:
                    try:
                        if el.is_displayed() and el.is_enabled():
                            driver.execute_script("arguments[0].click()", el)
                            submitted = True
                            break
                    except Exception:
                        continue
                if submitted:
                    break

            if not submitted:
                # 最后 fallback: Enter
                ActionChains(driver).send_keys(Keys.ENTER).perform()

            time.sleep(2)
            print(f"  ✓ 评论已发送: {text[:30]}")
            return True

        except Exception as e:
            print(f"  ✗ 评论失败: {e}")
            return False

    def get_note_comments(self, note_url: str, limit: int = 20) -> List[dict]:
        """
        单独获取笔记评论

        参数:
            note_url: 笔记 URL
            limit: 最大评论数

        返回: List[dict] 含 user/text/likes 字段
        """
        note = self.get_note_detail(note_url)
        if note:
            return [c.__dict__ for c in note.comments[:limit]]
        return []

    def batch_get_details(self, notes: List[Note], delay: float = 1.5) -> List[Note]:
        """
        批量获取笔记详情（在已有列表基础上补充正文和评论）

        参数:
            notes: search() 或 get_user_notes() 返回的列表
            delay: 每篇请求间隔秒数（建议 1.5~3）

        返回: 补充了 content/comments 的 Notes 列表
        """
        enriched = []
        for i, note in enumerate(notes):
            if not note.url:
                enriched.append(note)
                continue
            print(f"  [{i+1}/{len(notes)}] {note.title[:30] or note.url[:40]}")
            detail = self.get_note_detail(note.url)
            if detail:
                detail.title = detail.title or note.title
                detail.likes = detail.likes or note.likes
                detail.type = detail.type or note.type
                enriched.append(detail)
            else:
                enriched.append(note)
            time.sleep(delay)
        return enriched

    # ─── 工具方法 ───────────────────────────────────────────────

    def save(self, notes: List[Note], filepath: str):
        """保存结果到 JSON 文件"""
        data = [n.to_dict() for n in notes]
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"已保存 {len(data)} 条到 {filepath}")

    def analyze_account(
        self,
        notes: List[Note],
        creator_name: str = "未知博主",
        mode: str = "full",
        save_to: str = None,
    ) -> str:
        """
        对已采集的笔记列表做完整分析，返回 Markdown 报告。

        参数:
            notes        — get_user_notes() 的返回值
            creator_name — 博主昵称（用于报告标题）
            mode         — 'full' 完整报告 | 'formula' 选题公式 | 'snapshot' 快速摘要
            save_to      — 可选，保存报告到文件路径（.md）

        返回: Markdown 字符串
        """
        report = _analyze_account(notes, creator_name=creator_name, mode=mode)
        if save_to:
            with open(save_to, "w", encoding="utf-8") as f:
                f.write(report)
            print(f"报告已保存到 {save_to}")
        return report

    def _ensure_session(self):
        if not self._session:
            raise RuntimeError("请先调用 open() 或使用 with 语句")
