from __future__ import annotations

import os
import random
import threading
import time
from typing import Any, Optional

import httpx

from app.core.settings import settings
from app.core.errors import AppError, ErrorCodes
from app.utils.bilibili_subtitle_validate import (
    passes_duration_coverage,
    should_enforce_title_match,
    title_match_score,
)

_THROTTLE_LOCK = threading.Lock()
_LAST_REQUEST_AT = 0.0


def _norm_sub_lan(lan: str) -> str:
    return str(lan or "").strip().lower().replace("_", "-")


def is_ai_subtitle_lan(lan: str) -> bool:
    return _norm_sub_lan(lan).startswith("ai-")


def is_chinese_subtitle_lan(lan: str) -> bool:
    """B 站常见中文/华语字幕代码（含 AI 中文）。"""
    x = _norm_sub_lan(lan)
    if not x:
        return False
    if x == "ai-zh" or x.startswith("ai-zh-"):
        return True
    if x.startswith("zh"):
        return True
    if x in ("cmn", "yue", "wyw"):
        return True
    return False


def _chinese_lan_rank(lan: str) -> tuple[int, str]:
    """中文轨道内部优先级：简体/大陆 → 通用 zh → 繁体 → AI 中文。"""
    x = _norm_sub_lan(lan)
    if x in ("zh-cn", "zh-hans", "zh-sg"):
        return (0, x)
    if x in ("zh", "cmn"):
        return (1, x)
    if x.startswith("zh-hant") or x in ("zh-tw", "zh-hk", "zh-mo", "yue"):
        return (2, x)
    if x == "ai-zh":
        return (3, x)
    if x.startswith("ai-zh"):
        return (4, x)
    return (5, x)


class BilibiliSubtitleService:
    def __init__(self, timeout: float = 30.0) -> None:
        self.timeout = timeout
        self.max_retries = max(1, settings.bilibili_max_retries)
        self.base_backoff = max(0.1, settings.bilibili_backoff_base_seconds)
        self.min_interval = max(0.0, settings.bilibili_min_interval_seconds)

    def fetch_subtitle_payload(
        self,
        bvid: str,
        page: int = 1,
        prefer_lang: str = "zh-CN",
        only_lan: Optional[str] = None,
    ) -> Optional[dict[str, Any]]:
        """拉取字幕 JSON：遍历全部轨道，结合时长与标题相关性校验，多轮取最优。

        若严格阈值下无结果，再试放宽阈值（仍要求物理门限），避免误杀。
        设置 `bilibili_subtitle_validate=false` 时跳过校验与多轮采样，只取第一条非空轨道（更快）。
        `only_lan` 指定时只拉该语言码（用户在前端选的轨道），不做标题相关性过滤。
        """
        if only_lan and only_lan.strip():
            return self._fetch_payload_single_lan(bvid=bvid, page=page, lan=only_lan.strip())
        if not settings.bilibili_subtitle_validate:
            return self._fetch_first_payload_raw(bvid=bvid, page=page, prefer_lang=prefer_lang)

        rounds = max(1, settings.bilibili_subtitle_sample_rounds)
        gap = max(0.0, settings.bilibili_subtitle_sample_round_sleep_seconds)
        raw_thresholds = [
            settings.bilibili_subtitle_min_title_match_score,
            settings.bilibili_subtitle_relaxed_title_match_score,
        ]
        thresholds = sorted({t for t in raw_thresholds if t >= 0}, reverse=True)
        for min_title in thresholds:
            best_payload: Optional[dict[str, Any]] = None
            best_rank: tuple[float, int] = (-1.0, -1)
            for attempt in range(rounds):
                result = self._fetch_best_payload_one_round(
                    bvid=bvid, page=page, prefer_lang=prefer_lang, min_title_threshold=min_title
                )
                if result:
                    payload, score, body_len = result
                    if (score, body_len) > best_rank:
                        best_rank = (score, body_len)
                        best_payload = payload
                if attempt < rounds - 1 and gap > 0:
                    time.sleep(gap)
            if best_payload is not None:
                return best_payload
        return None

    def _best_payload_from_tracks(
        self,
        client: httpx.Client,
        track_list: list[dict[str, Any]],
        title_for_match: str,
        duration: float,
        min_title_threshold: float,
        enforce_title: bool,
    ) -> Optional[tuple[dict[str, Any], float, int]]:
        best_payload: Optional[dict[str, Any]] = None
        best_score = -1.0
        best_len = -1
        for track in track_list:
            url = track.get("subtitle_url")
            if not url:
                continue
            subtitle_url = self._normalize_subtitle_url(url)
            try:
                response = self._request_with_retry(client, subtitle_url)
                payload = response.json()
            except Exception:
                continue
            if not isinstance(payload, dict):
                continue
            body = payload.get("body")
            if not isinstance(body, list) or not body:
                continue
            if not passes_duration_coverage(
                body,
                duration,
                settings.bilibili_subtitle_min_duration_for_coverage_check_seconds,
                settings.bilibili_subtitle_min_coverage_ratio,
                settings.bilibili_subtitle_long_video_min_duration_seconds,
                settings.bilibili_subtitle_long_video_min_body_lines,
            ):
                continue
            plain = self.payload_to_text(payload)
            score = title_match_score(title_for_match, plain)
            eff_threshold = float(min_title_threshold)
            if is_ai_subtitle_lan(str(track.get("lan") or "")):
                eff_threshold = max(
                    eff_threshold, float(settings.bilibili_subtitle_ai_min_title_match)
                )
            if enforce_title and score < eff_threshold:
                continue
            blen = len(body)
            if score > best_score or (score == best_score and blen > best_len):
                best_score = score
                best_len = blen
                best_payload = payload
        if best_payload is None:
            return None
        return (best_payload, best_score, best_len)

    def _fetch_first_payload_raw(
        self, bvid: str, page: int, prefer_lang: str
    ) -> Optional[dict[str, Any]]:
        """无校验：view → player → 按轨道顺序取首条非空 body（player 空列表时最多重试 2 次）。"""

        def run_with_cookie(cookie_header: Optional[str]) -> Optional[dict[str, Any]]:
            headers = self._client_headers(cookie_header)
            with httpx.Client(timeout=self.timeout, headers=headers) as client:
                try:
                    view_data = self._fetch_view(client, bvid)
                    title = str(view_data.get("title") or "")
                    extra = str(view_data.get("tname") or "") + str(view_data.get("desc") or "")
                    title_for_match = f"{title} {extra}"[:800]
                    min_chars = settings.bilibili_subtitle_min_title_chars_for_match
                    enforce_ai_sanity = should_enforce_title_match(title_for_match, min_chars)
                    aid, cid = self._pick_aid_and_cid(view_data, page)
                    tracks: list[dict[str, Any]] = []
                    max_empty = max(1, min(2, settings.bilibili_player_subtitle_empty_retries))
                    empty_sleep = max(0.0, settings.bilibili_player_subtitle_empty_retry_sleep_seconds)
                    for attempt in range(max_empty):
                        tracks = self._fetch_player_subtitles(client, aid, cid, bvid)
                        if tracks:
                            break
                        if attempt < max_empty - 1 and empty_sleep > 0:
                            time.sleep(empty_sleep)
                    if not tracks:
                        return None
                    ordered = self._ordered_tracks(tracks, prefer_lang)
                    ai_min = float(settings.bilibili_subtitle_ai_min_title_match)
                    for track in ordered:
                        url = track.get("subtitle_url")
                        if not url:
                            continue
                        subtitle_url = self._normalize_subtitle_url(url)
                        try:
                            response = self._request_with_retry(client, subtitle_url)
                            payload = response.json()
                        except Exception:
                            continue
                        if not isinstance(payload, dict):
                            continue
                        body = payload.get("body")
                        if isinstance(body, list) and body:
                            if (
                                settings.bilibili_subtitle_ai_sanity_when_validate_off
                                and enforce_ai_sanity
                                and is_ai_subtitle_lan(str(track.get("lan") or ""))
                            ):
                                plain = self.payload_to_text(payload)
                                if (
                                    title_match_score(title_for_match, plain)
                                    < ai_min
                                ):
                                    continue
                            return payload
                    return None
                except Exception as exc:
                    raise AppError(ErrorCodes.SUBTITLE_FETCH_FAILED, f"B站字幕提取失败: {exc}", 400) from exc

        cookie_header = _build_sessdata_cookie()
        if cookie_header:
            got = run_with_cookie(cookie_header)
            if got:
                return got
        return run_with_cookie(None)

    def _fetch_best_payload_one_round(
        self, bvid: str, page: int, prefer_lang: str, min_title_threshold: float
    ) -> Optional[tuple[dict[str, Any], float, int]]:
        """单次：view → player 全部轨道 → 逐条下载并校验，取标题匹配度最高且通过时长门限的一条。"""

        def run_with_cookie(cookie_header: Optional[str]) -> Optional[tuple[dict[str, Any], float, int]]:
            headers = self._client_headers(cookie_header)
            with httpx.Client(timeout=self.timeout, headers=headers) as client:
                try:
                    view_data = self._fetch_view(client, bvid)
                    title = str(view_data.get("title") or "")
                    extra = str(view_data.get("tname") or "") + str(view_data.get("desc") or "")
                    title_for_match = f"{title} {extra}"[:800]
                    duration = float(view_data.get("duration") or 0)
                    aid, cid = self._pick_aid_and_cid(view_data, page)
                    tracks: list[dict[str, Any]] = []
                    empty_retries = max(1, settings.bilibili_player_subtitle_empty_retries)
                    empty_sleep = max(0.0, settings.bilibili_player_subtitle_empty_retry_sleep_seconds)
                    for attempt in range(empty_retries):
                        tracks = self._fetch_player_subtitles(client, aid, cid, bvid)
                        if tracks:
                            break
                        if attempt < empty_retries - 1 and empty_sleep > 0:
                            time.sleep(empty_sleep)
                    if not tracks:
                        return None
                    ordered = self._ordered_tracks(tracks, prefer_lang)
                    zh_list = [t for t in ordered if is_chinese_subtitle_lan(str(t.get("lan") or ""))]
                    other_list = [t for t in ordered if not is_chinese_subtitle_lan(str(t.get("lan") or ""))]
                    min_chars = settings.bilibili_subtitle_min_title_chars_for_match
                    enforce_title = should_enforce_title_match(title_for_match, min_chars)
                    picked = self._best_payload_from_tracks(
                        client,
                        zh_list,
                        title_for_match,
                        duration,
                        min_title_threshold,
                        enforce_title,
                    )
                    if picked is None:
                        picked = self._best_payload_from_tracks(
                            client,
                            other_list,
                            title_for_match,
                            duration,
                            min_title_threshold,
                            enforce_title,
                        )
                    if picked is None:
                        return None
                    best_payload, best_score, best_len = picked
                    return (best_payload, best_score if enforce_title else max(best_score, 0.0), best_len)
                except Exception as exc:
                    raise AppError(ErrorCodes.SUBTITLE_FETCH_FAILED, f"B站字幕提取失败: {exc}", 400) from exc

        cookie_header = _build_sessdata_cookie()
        if cookie_header:
            got = run_with_cookie(cookie_header)
            if got:
                return got
        return run_with_cookie(None)

    def _fetch_payload_single_lan(self, bvid: str, page: int, lan: str) -> Optional[dict[str, Any]]:
        """只拉取指定 lan 的字幕；用户显式选轨时不做标题命中率过滤。"""

        def run_with_cookie(cookie_header: Optional[str]) -> Optional[dict[str, Any]]:
            headers = self._client_headers(cookie_header)
            with httpx.Client(timeout=self.timeout, headers=headers) as client:
                try:
                    view_data = self._fetch_view(client, bvid)
                    duration = float(view_data.get("duration") or 0)
                    aid, cid = self._pick_aid_and_cid(view_data, page)
                    tracks = self._fetch_player_subtitles(client, aid, cid, bvid)
                    want = _norm_sub_lan(lan)
                    picked = None
                    for t in tracks:
                        if _norm_sub_lan(str(t.get("lan") or "")) == want:
                            picked = t
                            break
                    if not picked:
                        for t in tracks:
                            if str(t.get("lan") or "").strip() == lan.strip():
                                picked = t
                                break
                    if not picked:
                        return None
                    url = picked.get("subtitle_url")
                    if not url:
                        return None
                    subtitle_url = self._normalize_subtitle_url(url)
                    response = self._request_with_retry(client, subtitle_url)
                    payload = response.json()
                    if not isinstance(payload, dict):
                        return None
                    body = payload.get("body")
                    if not isinstance(body, list) or not body:
                        return None
                    if settings.bilibili_subtitle_validate:
                        if not passes_duration_coverage(
                            body,
                            duration,
                            settings.bilibili_subtitle_min_duration_for_coverage_check_seconds,
                            settings.bilibili_subtitle_min_coverage_ratio,
                            settings.bilibili_subtitle_long_video_min_duration_seconds,
                            settings.bilibili_subtitle_long_video_min_body_lines,
                        ):
                            return None
                    return payload
                except Exception as exc:
                    raise AppError(ErrorCodes.SUBTITLE_FETCH_FAILED, f"B站字幕提取失败: {exc}", 400) from exc

        cookie_header = _build_sessdata_cookie()
        if cookie_header:
            got = run_with_cookie(cookie_header)
            if got:
                return got
        return run_with_cookie(None)

    @staticmethod
    def _ordered_tracks(tracks: list[dict[str, Any]], prefer_lang: str) -> list[dict[str, Any]]:
        """中文类轨道整体优先于外语；同组内 exact prefer_lang → 中文内部排序 → 非中文按 lan。"""

        pref = _norm_sub_lan(prefer_lang)

        def sort_key(t: dict[str, Any]) -> tuple:
            lan_raw = str(t.get("lan") or "")
            x = _norm_sub_lan(lan_raw)
            is_zh = is_chinese_subtitle_lan(lan_raw)
            exact = 0 if x == pref else 1
            if is_zh:
                rank = _chinese_lan_rank(lan_raw)
                is_ai = x.startswith("ai-")
                non_ai = 0 if not is_ai else 1
                return (0, exact, non_ai, rank[0], rank[1], lan_raw)
            is_ai = x.startswith("ai-")
            non_ai = 0 if not is_ai else 1
            return (1, exact, non_ai, lan_raw)

        return sorted(tracks, key=sort_key)

    def fetch_subtitle_text(
        self,
        bvid: str,
        page: int = 1,
        prefer_lang: str = "zh-CN",
        only_lan: Optional[str] = None,
    ) -> Optional[str]:
        payload = self.fetch_subtitle_payload(bvid, page, prefer_lang, only_lan=only_lan)
        if not payload:
            return None
        return self.payload_to_text(payload)

    def list_subtitle_tracks(self, bvid: str, page: int = 1) -> list[dict[str, Any]]:
        """返回 player/wbi/v2 中的字幕轨道摘要（lan / lan_doc），便于与播放器里选项对照。"""
        tracks: list[dict[str, Any]] = []
        cookie_header = _build_sessdata_cookie()

        def collect(cookie: Optional[str]) -> list[dict[str, Any]]:
            headers = self._client_headers(cookie)
            with httpx.Client(timeout=self.timeout, headers=headers) as client:
                view_data = self._fetch_view(client, bvid)
                aid, cid = self._pick_aid_and_cid(view_data, page)
                return self._fetch_player_subtitles(client, aid, cid, bvid)

        if cookie_header:
            tracks = collect(cookie_header)
        else:
            tracks = []
        if not tracks:
            tracks = collect(None)
        tracks = self._ordered_tracks(tracks, "zh-CN")
        out: list[dict[str, Any]] = []
        for item in tracks:
            out.append(
                {
                    "lan": item.get("lan"),
                    "lan_doc": item.get("lan_doc"),
                    "subtitle_url": (item.get("subtitle_url") or "")[:120],
                }
            )
        return out

    def resolve_player_ids(self, bvid: str, page: int = 1) -> tuple[int, int]:
        """从 view 接口解析当前分 P 的 aid/cid，供嵌入播放器 player.html 使用（含 t 起播时常需）。"""
        cookie_header = _build_sessdata_cookie()

        def run(cookie: Optional[str]) -> Optional[tuple[int, int]]:
            try:
                headers = self._client_headers(cookie)
                with httpx.Client(timeout=self.timeout, headers=headers) as client:
                    view_data = self._fetch_view(client, bvid)
                aid, cid = self._pick_aid_and_cid(view_data, page)
                return (int(aid), int(cid))
            except Exception:
                return None

        if cookie_header:
            got = run(cookie_header)
            if got:
                return got
        got = run(None)
        if got:
            return got
        return (0, 0)

    def fetch_video_brief(self, bvid: str, page: int = 1) -> Optional[dict[str, Any]]:
        """从 view 接口获取标题、UP 主昵称、简介（与 list_subtitle_tracks 相同的 Cookie 策略）。"""
        cookie_header = _build_sessdata_cookie()

        def collect(cookie: Optional[str]) -> Optional[dict[str, Any]]:
            try:
                headers = self._client_headers(cookie)
                with httpx.Client(timeout=self.timeout, headers=headers) as client:
                    view_data = self._fetch_view(client, bvid)
            except Exception:
                return None
            owner = view_data.get("owner") or {}
            return {
                "title": str(view_data.get("title") or "").strip(),
                "author": str(owner.get("name") or "").strip(),
                "description": str(view_data.get("desc") or "").strip(),
                "duration": float(view_data.get("duration") or 0),
            }

        data: Optional[dict[str, Any]] = None
        if cookie_header:
            data = collect(cookie_header)
        if not data or not data.get("title"):
            alt = collect(None)
            if alt and (not data or not data.get("title")):
                data = alt
            elif not data:
                data = alt
        return data

    @staticmethod
    def payload_to_text(payload: dict[str, Any]) -> str:
        body = payload.get("body")
        if not isinstance(body, list):
            return ""
        lines = []
        for item in body:
            content = (item.get("content") or "").strip()
            if content:
                lines.append(content)
        return "\n".join(lines).strip()

    @staticmethod
    def payload_to_srt(payload: dict[str, Any]) -> str:
        body = payload.get("body")
        if not isinstance(body, list):
            return ""
        chunks = []
        idx = 0
        for item in body:
            content = (item.get("content") or "").strip()
            if not content:
                continue
            idx += 1
            start = float(item.get("from", 0))
            end = float(item.get("to", start))
            chunks.append(f"{idx}\n{_sec_to_srt(start)} --> {_sec_to_srt(end)}\n{content}\n")
        return "\n".join(chunks).strip()

    @staticmethod
    def payload_to_segments(payload: dict[str, Any]) -> list[dict[str, Any]]:
        body = payload.get("body")
        if not isinstance(body, list):
            return []
        out: list[dict[str, Any]] = []
        for item in body:
            content = (item.get("content") or "").strip()
            if not content:
                continue
            start = float(item.get("from", 0.0) or 0.0)
            end = float(item.get("to", start) or start)
            if end < start:
                end = start
            out.append({"start": start, "end": end, "text": content})
        return out

    def _client_headers(self, cookie_header: Optional[str]) -> dict[str, str]:
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            ),
            "Referer": "https://www.bilibili.com/",
            "Accept": "application/json",
        }
        if cookie_header:
            headers["Cookie"] = cookie_header
        return headers

    def _fetch_view(self, client: httpx.Client, bvid: str) -> dict[str, Any]:
        resp = self._request_with_retry(client, "https://api.bilibili.com/x/web-interface/view", params={"bvid": bvid})
        data = resp.json()
        if data.get("code") != 0:
            raise RuntimeError(f"view API code={data.get('code')} message={data.get('message')}")
        return data.get("data") or {}

    @staticmethod
    def _pick_aid_and_cid(view_data: dict[str, Any], page: int) -> tuple[int, int]:
        aid = view_data.get("aid")
        pages = view_data.get("pages") or []
        if not aid or not pages:
            raise RuntimeError("view 数据缺少 aid 或 pages")
        picked = None
        for page_item in pages:
            if int(page_item.get("page") or 0) == page:
                picked = page_item
                break
        if not picked:
            picked = pages[0]
        cid = picked.get("cid")
        if not cid:
            raise RuntimeError("分 P 缺少 cid")
        return int(aid), int(cid)

    def _fetch_player_subtitles(self, client: httpx.Client, aid: int, cid: int, bvid: str) -> list[dict[str, Any]]:
        # 与 yt-dlp 一致：需登录可见的字幕在 wbi/v2 中返回；旧版 /x/player/v2 常为空
        resp = self._request_with_retry(
            client,
            "https://api.bilibili.com/x/player/wbi/v2",
            params={"aid": aid, "cid": cid, "bvid": bvid},
        )
        data = resp.json()
        if data.get("code") != 0:
            raise RuntimeError(f"player/v2 code={data.get('code')} message={data.get('message')}")
        subtitle = (data.get("data") or {}).get("subtitle") or {}
        out = list(subtitle.get("subtitles") or [])
        if out:
            return out
        # 部分稿件 wbi/v2 字幕列表为空，但 x/player/v2 仍返回轨道（例如仅 AI 字幕）
        resp2 = self._request_with_retry(
            client,
            "https://api.bilibili.com/x/player/v2",
            params={"aid": aid, "cid": cid, "bvid": bvid},
        )
        data2 = resp2.json()
        if data2.get("code") != 0:
            return []
        subtitle2 = (data2.get("data") or {}).get("subtitle") or {}
        return list(subtitle2.get("subtitles") or [])

    def _request_with_retry(self, client: httpx.Client, url: str, params: Optional[dict[str, Any]] = None) -> httpx.Response:
        last_error: Optional[Exception] = None
        for attempt in range(1, self.max_retries + 1):
            try:
                self._throttle()
                response = client.get(url, params=params)
                if response.status_code in {412, 429, 500, 502, 503, 504}:
                    raise RuntimeError(f"HTTP {response.status_code}")
                response.raise_for_status()
                return response
            except Exception as exc:
                last_error = exc
                if attempt >= self.max_retries:
                    break
                delay = self.base_backoff * (2 ** (attempt - 1)) + random.uniform(0.0, 0.3)
                time.sleep(delay)
        raise RuntimeError(f"request failed after retries: {last_error}")

    def _throttle(self) -> None:
        global _LAST_REQUEST_AT
        if self.min_interval <= 0:
            return
        with _THROTTLE_LOCK:
            now = time.monotonic()
            wait = self.min_interval - (now - _LAST_REQUEST_AT)
            if wait > 0:
                time.sleep(wait)
            _LAST_REQUEST_AT = time.monotonic()

    @staticmethod
    def _normalize_subtitle_url(url: str) -> str:
        if url.startswith("//"):
            return "https:" + url
        return url


def _build_bilibili_cookie() -> Optional[str]:
    """组装完整的 B 站登录 Cookie（SESSDATA + bili_jct + DedeUserID + DedeUserID__ckMd5）。

    仅 SESSDATA 时仍可回退；但 player API 对 need_login_subtitle=True 的视频
    需要完整登录态才会返回字幕轨道列表。
    """
    import logging
    _log = logging.getLogger(__name__)

    raw_sess = (
        os.environ.get("BILIBILI_SESSION_TOKEN")
        or os.environ.get("SESSDATA")
        or (settings.bilibili_session_token or "").strip()
        or (settings.sessdata or "").strip()
    )
    if not raw_sess:
        return None
    sess_list = [v.strip() for v in raw_sess.split(",") if v.strip()]
    if not sess_list:
        return None
    sessdata = sess_list[0]

    parts = [f"SESSDATA={sessdata}"]
    bili_jct = (os.environ.get("BILI_JCT") or (settings.bili_jct or "").strip())
    dede_uid = (os.environ.get("DEDEUSERID") or os.environ.get("DedeUserID") or (settings.dede_user_id or "").strip())
    dede_ckmd5 = (os.environ.get("DEDEUSERID__CKMD5") or os.environ.get("DedeUserID__ckMd5") or (settings.dede_user_id_ckmd5 or "").strip())
    if bili_jct:
        parts.append(f"bili_jct={bili_jct}")
    if dede_uid:
        parts.append(f"DedeUserID={dede_uid}")
    if dede_ckmd5:
        parts.append(f"DedeUserID__ckMd5={dede_ckmd5}")

    cookie_str = "; ".join(parts)
    if len(parts) < 4:
        _log.debug(
            "B 站 Cookie 不完整（仅 %d/4），need_login_subtitle 视频可能无法获取字幕",
            len(parts),
        )
    return cookie_str


def _build_sessdata_cookie() -> Optional[str]:
    """向后兼容：返回完整 Cookie（如已配全）或仅 SESSDATA。"""
    return _build_bilibili_cookie()


def get_bilibili_sessdata_cookie_header() -> Optional[str]:
    """供 yt-dlp / 网页抓取等复用：返回完整 B 站登录 Cookie。"""
    return _build_bilibili_cookie()


def _sec_to_srt(value: float) -> str:
    sec = float(value)
    hour = int(sec // 3600)
    minute = int((sec % 3600) // 60)
    second = int(sec % 60)
    ms = int(round((sec - int(sec)) * 1000))
    if ms >= 1000:
        ms = 999
    return f"{hour:02d}:{minute:02d}:{second:02d},{ms:03d}"
