"""配置加载 — 仅 Cloudflare Pages 部署模式"""

import re
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
DIST_DIR = BASE_DIR / "dist"

# ── TOOLS.md 配置读取 ──
_TOOLS_PATHS = [
    Path.home() / ".openclaw/workspace/TOOLS.md",
    BASE_DIR.parent.parent / "TOOLS.md",  # workspace TOOLS.md
]

_tools_text = ""
for p in _TOOLS_PATHS:
    if p.exists():
        try:
            _tools_text += p.read_text("utf-8") + "\n"
        except (UnicodeDecodeError, PermissionError):
            pass


def _get(key):
    """Read a config value from TOOLS.md by key=value pattern.

    Handles formats like:
      - `KEY=value`  # comment
      - KEY=value
      - `KEY=value`
    """
    m = re.search(rf'(?:^|\s)`?{re.escape(key)}=(.+?)(?:`|$)', _tools_text, re.MULTILINE)
    if not m:
        return None
    v = m.group(1).strip()
    # Step 1: Remove surrounding quotes (single or double)
    if (v.startswith('"') and v.endswith('"') and len(v) > 1) or \
       (v.startswith("'") and v.endswith("'") and len(v) > 1):
        v = v[1:-1]
    # Step 2: Strip inline comment (respect # inside quotes)
    # Simple approach: split on # not inside quotes
    in_sq = in_dq = False
    cut = len(v)
    for idx, ch in enumerate(v):
        if ch == '"' and not in_sq:
            in_dq = not in_dq
        elif ch == "'" and not in_dq:
            in_sq = not in_sq
        elif ch == '#' and not in_sq and not in_dq:
            cut = idx
            break
    v = v[:cut].rstrip()
    # Step 3: Remove trailing/leading backticks (from `key=value` markdown format)
    if v.startswith('`') and v.endswith('`') and len(v) > 2:
        v = v[1:-1]
    elif v.startswith('`'):
        v = v[1:]
    elif v.endswith('`'):
        v = v[:-1]
    v = v.strip()
    return v or None


# ── 必需配置 ──
CLOUDFLARE_API_TOKEN = _get("CLOUDFLARE_API_TOKEN")
REPORT_CF_PROJECT = _get("REPORT_CF_PROJECT")  # Cloudflare Pages 项目名（空间名）

# ── 必需配置（站点信息） ──
REPORT_SITE_NAME = _get("REPORT_SITE_NAME") or "传琪"

# ── 可选配置 ──
REPORT_CUSTOM_DOMAIN = _get("REPORT_CUSTOM_DOMAIN")  # 自定义域名，如 xue.mei.pub

# ── 派生常量 ──
# 站点 URL：有自定义域名用自定义域名，否则用 CF Pages 默认域名
if REPORT_CUSTOM_DOMAIN:
    SITE_URL = f"https://{REPORT_CUSTOM_DOMAIN}"
else:
    SITE_URL = f"https://{REPORT_CF_PROJECT}.pages.dev" if REPORT_CF_PROJECT else ""

SITE_NAME = REPORT_SITE_NAME
INDEX_FILE = DIST_DIR / "index.json"

# ── 分类常量（全局唯一） ──
CATEGORIES = {
    "research": "深度研究",
    "analysis": "数据分析",
    "summary": "内容摘要",
    "comparison": "对比评测",
    "tutorial": "教程指南",
    "project": "项目作品",
    "other": "其他",
}


def load_index():
    if INDEX_FILE.exists():
        import json
        try:
            with open(INDEX_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
        except (json.JSONDecodeError, UnicodeDecodeError):
            print(f"⚠️ index.json 解析失败，将使用空索引")
            data = {}
        # Ensure required structure — config values are always authoritative
        data["site"] = {"name": SITE_NAME, "baseUrl": SITE_URL}
        # Legacy format: if "reports" key exists instead of "pages", migrate FIRST
        if "reports" in data and "pages" not in data:
            data["pages"] = data.pop("reports")
        if "reports" in data:
            # Clean up stale "reports" key if both exist
            del data["reports"]
        if "pages" not in data:
            data["pages"] = []
        return data
    return {"site": {"name": SITE_NAME, "baseUrl": SITE_URL}, "pages": []}


def save_index(data):
    import json, tempfile
    INDEX_FILE.parent.mkdir(parents=True, exist_ok=True)
    # Atomic write: write to temp file then rename
    tmp = INDEX_FILE.with_suffix('.tmp')
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    tmp.replace(INDEX_FILE)


def strip_emoji(text):
    import unicodedata
    return re.sub(
        r'[\U0001f300-\U0001f9ff\U00002702-\U000027b0\U00002600-\U000026ff'
        r'\U0001fa00-\U0001fa6f\U0001fa70-\U0001faff\u200d\ufe0f]', '', text
    )


def add_ids(html):
    counter = {}
    def repl(m):
        tag = m.group(1).lower()
        attrs = m.group(2) or ''
        text = re.sub(r'<[^>]+>', '', m.group(3)).strip()
        slug = re.sub(r'[^\w\u4e00-\u9fff]+', '-', text).strip('-').lower()
        if not slug:
            slug = 'section'
        counter[slug] = counter.get(slug, 0) + 1
        uid = slug if counter[slug] == 1 else f"{slug}-{counter[slug]}"
        # If id already exists in attrs, skip injection
        if 'id=' in attrs:
            return f'<{tag}{attrs}>{m.group(3)}</{tag}>'
        # Inject id before other attributes
        if attrs.strip():
            return f'<{tag} id="{uid}" {attrs.strip()}>{m.group(3)}</{tag}>'
        else:
            return f'<{tag} id="{uid}">{m.group(3)}</{tag}>'
    return re.sub(r'<(h[23])(\s[^>]*)?>(.*?)</\1>', repl, html, flags=re.DOTALL)


def check_config():
    """验证必需配置是否齐全，缺失则报错退出"""
    import sys, shutil
    errors = []
    if not CLOUDFLARE_API_TOKEN:
        errors.append("CLOUDFLARE_API_TOKEN — Cloudflare API Token（必需）")
    if not REPORT_CF_PROJECT:
        errors.append("REPORT_CF_PROJECT — Cloudflare Pages 项目名/空间名（必需）")
    if not shutil.which("npx"):
        errors.append("npx — Node.js CLI（必需，请安装 Node.js）")
    if errors:
        print("❌ 配置缺失，请在 TOOLS.md 中添加以下配置项或安装依赖：")
        for e in errors:
            print(f"   {e}")
        print()
        print("示例配置（添加到 TOOLS.md）：")
        print()
        print("### Report Expert 技能配置")
        print("- `CLOUDFLARE_API_TOKEN=<your-token>`")
        print("- `REPORT_CF_PROJECT=xuedi`")
        print("- `REPORT_SITE_NAME=雪地`")
        print("- `REPORT_CUSTOM_DOMAIN=xue.mei.pub`  # 可选：自定义域名")
        sys.exit(1)