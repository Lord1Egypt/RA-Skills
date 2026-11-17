"""XHS 短链 / 长链 / 口令 → note_id 解析。

XHS note_id = 24 位十六进制字符串，例如 665ea88c0000000003031383。

短链（xhslink.com/o/xxx）需要跟随重定向 — HEAD 请求会被 404，必须 GET。
"""

from __future__ import annotations
import re
import urllib.error
import urllib.request


_NOTE_ID_RE = re.compile(r"[a-f0-9]{24}")
_XHS_URL_RE = re.compile(r"https?://(?:xhslink\.com|www\.xiaohongshu\.com)/[A-Za-z0-9/_.?=&-]+")
_NOTE_PATH_RE = re.compile(r"(?:explore|discovery/item)/([a-f0-9]{24})")

# 真实浏览器 UA — xhslink 拒绝 bot UA
_BROWSER_UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)


def resolve_xhs_link(input_text: str, timeout: int = 15) -> tuple[str, str]:
    """把任意 XHS 输入解析成 (note_id, final_url)。

    支持的输入形式：
    - 24 位 hex 字符串（裸 note_id）
    - 长链 https://www.xiaohongshu.com/explore/{id}?...
    - 长链 https://www.xiaohongshu.com/discovery/item/{id}?...
    - 短链 https://xhslink.com/o/xxx
    - 任何含上述链接的分享口令文本

    Raises:
        ValueError: 完全无法识别。
    """
    text = input_text.strip()

    # 1. 裸 note_id
    if re.fullmatch(_NOTE_ID_RE, text):
        return text, f"https://www.xiaohongshu.com/explore/{text}"

    # 2. 提取文本里的第一个 XHS URL
    m = _XHS_URL_RE.search(text)
    if not m:
        raise ValueError(
            f"No XHS link or 24-char note_id found in input: {text[:80]!r}"
        )
    url = m.group(0)

    # 3. 长链直接 regex 提取
    if note_match := _NOTE_PATH_RE.search(url):
        return note_match.group(1), url

    # 4. 短链 — 跟随重定向
    final_url = _follow_redirects(url, timeout=timeout)
    if note_match := _NOTE_PATH_RE.search(final_url):
        return note_match.group(1), final_url

    raise ValueError(f"Could not extract note_id from final URL: {final_url}")


def _follow_redirects(url: str, timeout: int = 15) -> str:
    """GET + 跟随重定向，返回最终 URL。失败返回原 URL。"""
    req = urllib.request.Request(url, headers={"User-Agent": _BROWSER_UA})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.geturl()
    except urllib.error.HTTPError as e:
        # 即使 HTTP 错误，url 可能已重定向
        return getattr(e, "url", url) or url
    except urllib.error.URLError:
        return url
