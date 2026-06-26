from typing import Optional
import logging
import re

import httpx
from yt_dlp import YoutubeDL

from app.core.errors import AppError, ErrorCodes
from app.extractors.base import BaseExtractor, ParseContext
from app.services.bilibili_subtitle import BilibiliSubtitleService, get_bilibili_sessdata_cookie_header
from app.utils.url_tools import parse_bilibili_identity

logger = logging.getLogger(__name__)

class BilibiliExtractor(BaseExtractor):
    def __init__(self) -> None:
        self.subtitle_service = BilibiliSubtitleService()

    def can_handle(self, url: str) -> bool:
        return "bilibili.com" in url or "b23.tv" in url

    def extract(self, url: str, subtitle_lan: Optional[str] = None) -> ParseContext:
        identity = parse_bilibili_identity(url)
        bvid, page = identity["bvid"], identity["page"]
        normalized_url = f"https://www.bilibili.com/video/{bvid}?p={page}"
        logger.info("Bilibili extract start bvid=%s page=%s", bvid, page)
        player_aid, player_cid = self.subtitle_service.resolve_player_ids(bvid, page)

        brief = self.subtitle_service.fetch_video_brief(bvid, page)
        info: Optional[dict] = None

        def ensure_info() -> dict:
            nonlocal info
            if info is None:
                info = self._extract_info(normalized_url)
            return info

        duration_seconds = 0.0
        if brief:
            title = (brief.get("title") or "").strip() or bvid
            author = (brief.get("author") or "").strip()
            description = (brief.get("description") or "").strip()
            duration_seconds = float(brief.get("duration") or 0)
        else:
            data = ensure_info()
            title = (data.get("title") or "").strip() or bvid
            author = (data.get("uploader") or data.get("channel") or "") or ""
            description = (data.get("description") or "") or ""

        fixed_title = self._fetch_title_from_webpage(normalized_url)
        if fixed_title and not self._is_captcha_title(fixed_title) and not self._looks_mojibake(fixed_title):
            title = fixed_title
        elif self._looks_mojibake(title):
            data = ensure_info()
            title = (data.get("title") or "").strip() or bvid
            if self._looks_mojibake(title):
                title = bvid
            if not brief:
                author = author or (data.get("uploader") or data.get("channel") or "") or ""
                description = description or (data.get("description") or "") or ""

        raw_tracks = self.subtitle_service.list_subtitle_tracks(bvid=bvid, page=page)
        subtitle_tracks = [{"lan": t.get("lan"), "lan_doc": t.get("lan_doc")} for t in raw_tracks]

        subtitle_text: Optional[str] = None
        subtitle_segments: list[dict] = []
        only_lan = (subtitle_lan or "").strip() or None
        if raw_tracks:
            payload = self._load_subtitle_payload(bvid, page, only_lan=only_lan)
            if payload:
                subtitle_text = self.subtitle_service.payload_to_text(payload)
                subtitle_segments = self.subtitle_service.payload_to_segments(payload)
            if subtitle_text:
                logger.info("Official subtitle found")
            else:
                logger.info("Subtitle tracks present but no usable text after fetch/validate")

        subtitle_lan_used = ""
        if subtitle_text and raw_tracks:
            subtitle_lan_used = only_lan or (raw_tracks[0].get("lan") or "")

        if duration_seconds <= 0:
            try:
                meta = ensure_info()
                duration_seconds = float(meta.get("duration") or 0)
            except Exception:
                pass

        return ParseContext(
            platform="bilibili",
            title=title,
            subtitle_text=subtitle_text,
            audio_url=None,
            author=author,
            description=description,
            subtitle_track_count=len(raw_tracks),
            subtitle_tracks=subtitle_tracks,
            subtitle_lan_used=str(subtitle_lan_used) if subtitle_lan_used else "",
            normalized_bilibili_url=normalized_url,
            duration_seconds=duration_seconds,
            subtitle_segments=subtitle_segments,
            subtitle_payload=payload if raw_tracks else None,
            player_aid=player_aid,
            player_cid=player_cid,
        )

    def _yt_dlp_opts(self, extra: Optional[dict] = None) -> dict:
        opts: dict = {"quiet": True, "skip_download": True, "encoding": "utf-8"}
        if extra:
            opts.update(extra)
        cookie = get_bilibili_sessdata_cookie_header()
        if cookie:
            opts["http_headers"] = {
                "Cookie": cookie,
                "Referer": "https://www.bilibili.com/",
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                    "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
                ),
            }
        return opts

    def _extract_info(self, url: str) -> dict:
        opts = self._yt_dlp_opts()
        try:
            with YoutubeDL(opts) as ydl:
                return ydl.extract_info(url, download=False)
        except Exception as exc:
            logger.warning("Bilibili info extract failed: %s", exc)
            raise AppError(ErrorCodes.VIDEO_NOT_ACCESSIBLE, f"B站信息提取失败: {exc}", 400) from exc

    def extract_audio_url(self, page_url: str) -> str:
        """供 ASR 使用：解析页 URL → yt-dlp 最佳音频直链（与字幕共用 Cookie）。"""
        return self._extract_audio_url(page_url)

    def _extract_audio_url(self, url: str) -> str:
        opts = self._yt_dlp_opts({"format": "bestaudio/best"})
        try:
            with YoutubeDL(opts) as ydl:
                info = ydl.extract_info(url, download=False)
            audio_url = info.get("url")
            if not audio_url:
                raise AppError(ErrorCodes.AUDIO_EXTRACT_FAILED, "未获取到音频流地址", 400)
            logger.info("Audio url extracted")
            return audio_url
        except AppError:
            raise
        except Exception as exc:
            logger.warning("Audio extraction failed: %s", exc)
            raise AppError(ErrorCodes.AUDIO_EXTRACT_FAILED, f"音频提取失败: {exc}", 400) from exc

    def _load_subtitle_payload(self, bvid: str, page: int, only_lan: Optional[str] = None) -> Optional[dict]:
        try:
            return self.subtitle_service.fetch_subtitle_payload(
                bvid=bvid, page=page, prefer_lang="zh-CN", only_lan=only_lan
            )
        except AppError as exc:
            logger.warning("Subtitle fetch failed via subtitle service: %s", exc.message)
            return None

    def _looks_mojibake(self, text: Optional[str]) -> bool:
        if not text:
            return True
        # 包含替换字符，几乎可判定为乱码
        if "�" in text:
            return True
        # 过多不可见/异常符号也认为是乱码
        weird = re.findall(r"[^\w\u4e00-\u9fff\s\-\.,!?;:，。！？；：·《》“”‘’()（）【】]", text)
        return len(weird) > max(3, len(text) // 3)

    def _fetch_title_from_webpage(self, normalized_url: str) -> Optional[str]:
        headers = {
            "User-Agent": "Mozilla/5.0",
            "Referer": "https://www.bilibili.com/",
            "Accept-Language": "zh-CN,zh;q=0.9",
        }
        cookie = get_bilibili_sessdata_cookie_header()
        if cookie:
            headers["Cookie"] = cookie
        try:
            with httpx.Client(timeout=20, headers=headers) as client:
                response = client.get(normalized_url)
                response.raise_for_status()
                html = response.text
            # 优先取 og:title
            og_match = re.search(
                r'<meta\s+property=["\']og:title["\']\s+content=["\'](.*?)["\']',
                html,
                re.IGNORECASE,
            )
            if og_match:
                return self._clean_web_title(og_match.group(1))
            # 兜底取 <title>
            title_match = re.search(r"<title>(.*?)</title>", html, re.IGNORECASE | re.DOTALL)
            if title_match:
                return self._clean_web_title(title_match.group(1))
            return None
        except Exception as exc:
            logger.warning("Fetch webpage title failed: %s", exc)
            return None

    def _clean_web_title(self, raw_title: str) -> str:
        title = raw_title.strip()
        title = re.sub(r"_哔哩哔哩_bilibili$", "", title).strip()
        return title

    def _is_captcha_title(self, title: str) -> bool:
        return "验证码" in title or "安全验证" in title
