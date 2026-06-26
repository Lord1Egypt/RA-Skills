#!/usr/bin/env python3
"""
THUQX AutoOps for OpenClaw 0.5 — 根据主题生成四平台文案，输出 JSON 到 stdout（供 run_social_ops_v5.sh 解析）。
与 OpenClaw skill zeelin-social-autopublisher 内脚本保持一致。

通义千问：设置环境变量 DASHSCOPE_API_KEY 或 QWEN_API_KEY（阿里云 DashScope）。
可选：QWEN_API_BASE（默认 DashScope 兼容模式）、QWEN_MODEL（默认 qwen-turbo）。
未配置 Key 时回退为本地模板文案。
"""
from __future__ import annotations

import argparse
import json
import os
import re
import ssl
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

_SCRIPT_DIR = Path(__file__).resolve().parent
_HANDBOOK_NAME = "四大平台内容生产提示词手册.md"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate four-platform social copy and print JSON to stdout."
    )
    parser.add_argument("topic_positional", nargs="?", help="Topic, for backward compatibility")
    parser.add_argument("--topic", help="Topic to generate content for")
    parser.add_argument(
        "--output",
        help="Optional file path to store the final JSON payload",
    )
    parser.add_argument(
        "--pretty",
        action="store_true",
        help="Pretty-print JSON to stdout/output file",
    )
    parser.add_argument(
        "--materials-output",
        help="Optional file path to store fetched reference materials",
    )
    return parser.parse_args()


ARGS = parse_args()
topic = ARGS.topic or ARGS.topic_positional or "AI认知债务"
MAX_RETRIES = max(1, int(os.environ.get("THUQX_CONTENT_MAX_RETRIES", "3")))


def _load_prompt_handbook() -> str:
    """Load bundled 四大平台手册；与 generate_content.py 同目录。"""
    path = _SCRIPT_DIR / _HANDBOOK_NAME
    if not path.is_file():
        return ""
    try:
        return path.read_text(encoding="utf-8")
    except OSError:
        return ""

# 千问 / DashScope（兼容 OpenAI Chat Completions）
QWEN_API_BASE = os.environ.get(
    "QWEN_API_BASE", "https://dashscope.aliyuncs.com/compatible-mode/v1"
).rstrip("/")
QWEN_MODEL = os.environ.get("QWEN_MODEL", "qwen-turbo")
DASHSCOPE_API_KEY = (
    os.environ.get("DASHSCOPE_API_KEY") or os.environ.get("QWEN_API_KEY") or ""
).strip()
# 若系统 CA 不完整（如 macOS 自带 Python），设为 1 时在意图错误校验失败回退到不校验证书（仅建议本机调试）
QWEN_INSECURE_SSL = os.environ.get("QWEN_INSECURE_SSL", "").strip() in ("1", "true", "yes")


def _https_open(req: urllib.request.Request, timeout: int):
    def ctx_default():
        try:
            import certifi  # type: ignore

            return ssl.create_default_context(cafile=certifi.where())
        except Exception:
            return ssl.create_default_context()

    try:
        return urllib.request.urlopen(req, timeout=timeout, context=ctx_default())
    except urllib.error.URLError as e:
        reason = getattr(e, "reason", e)
        ssl_bad = isinstance(reason, ssl.SSLError) and (
            "CERTIFICATE_VERIFY_FAILED" in str(reason)
            or "certificate verify failed" in str(reason).lower()
        )
        if ssl_bad and QWEN_INSECURE_SSL:
            ctx = ssl._create_unverified_context()
            return urllib.request.urlopen(req, timeout=timeout, context=ctx)
        if ssl_bad and not QWEN_INSECURE_SSL:
            print(
                "[generate_content] SSL 证书校验失败，已回退模板。"
                "可安装 certifi、运行 Python「Install Certificates」"
                "或临时设置 QWEN_INSECURE_SSL=1。",
                file=sys.stderr,
            )
        raise


def web_search_materials(q: str, max_items: int = 5) -> list[dict]:
    """
    Basic web search step for reference materials (no key required).
    Tries DuckDuckGo HTML endpoint and extracts top result titles/urls.
    Returns [] on failure.
    """
    try:
        url = "https://duckduckgo.com/html/?" + urllib.parse.urlencode({"q": q})
        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/122.0 Safari/537.36"
            },
        )
        with urllib.request.urlopen(req, timeout=8) as r:
            html = r.read().decode("utf-8", errors="ignore")

        items: list[dict] = []
        for m in re.finditer(r'class="result__a"[^>]*href="([^"]+)"[^>]*>(.*?)</a>', html):
            href = m.group(1)
            title = re.sub(r"<.*?>", "", m.group(2)).strip()
            if not title:
                continue
            items.append({"title": title[:140], "url": href[:300]})
            if len(items) >= max_items:
                break
        return items
    except Exception:
        return []


materials = web_search_materials(topic)
extra = web_search_materials(f"{topic} 选手 赛果", max_items=3)
seen = {m["url"] for m in materials}
for it in extra:
    if it["url"] not in seen:
        materials.append(it)
        seen.add(it["url"])
    if len(materials) >= 8:
        break

materials_text = ""
if materials:
    bullets = [f"- {it['title']} ({it['url']})" for it in materials]
    materials_text = "参考素材（公开网页摘要，写作时请核对；与主题冲突则以可验证事实为准）：\n" + "\n".join(
        bullets
    )

REQUIRED_KEYS = (
    "twitter",
    "weibo",
    "xhs_title",
    "xhs_body",
    "wechat_title",
    "wechat_body",
)

_ALLOW_TEMPLATE = os.environ.get("THUQX_ALLOW_TEMPLATE_FALLBACK", "").strip() in (
    "1",
    "true",
    "yes",
)

_BAD_PHRASE = re.compile(
    r"Auto\s*Ops|自动发布|本推文由|本文由|本条由",
    re.IGNORECASE,
)

# 核心约束（与《四大平台内容生产提示词手册》叠加；手册在同名 .md 文件中）
_QWEN_SYSTEM_CORE = """你是资深全媒体主编，也是懂增长的中文自媒体操盘手。只输出一个 JSON 对象，不要 Markdown、不要代码围栏、不要解释性文字。
JSON 必须包含且仅包含这六个字符串键：twitter, weibo, xhs_title, xhs_body, wechat_title, wechat_body。
每个键对应一条「最终可发布」的定稿（不是多组 A/B/C，从中各选一个最佳写法即可）。

【总目标】
- 你的输出不是“通顺介绍”，而是“可传播、可讨论、可收藏、可转发”的成稿。
- 所有平台都必须围绕同一个母判断展开：先讲现象，再给判断，再给用户启发。
- 不要写行业汇报腔、公告腔、模板腔；要写成能让用户停下来、看下去、愿意互动的内容。

【事实与人称】
- 紧扣用户「主题」与「参考素材」。素材充足时写清事件、产品、趋势节点；不足时保守表述，不捏造数字、机构表态、发布时间、奖项与结论。
- 主题涉及真实人物：以参考素材为准判断性别与身份；素材未明示时禁止凭名字猜「她/他」，优先「姓名+身份」或中性称呼。

【统一爆款写法标准】
- 开头 1-2 句必须有钩子：反常识、冲突、对比、代价、提问、数字、情绪张力，至少占一种。
- 正文不能只“描述趋势”，必须明确表达判断：为什么重要、为什么现在、谁会受影响、用户该怎么看。
- 至少出现 2 个具体信号（产品变化、行业动向、用户场景、技术走向、竞争格局），不要空泛谈“未来会改变世界”。
- 尽量写出一句适合截图传播的金句，要求有对比、结论感或警告感。
- 每个平台都要避免“正确的废话”“宏大空话”“通用 AI 口水稿”。

【强禁止】
- 所有字段严禁：「Auto Ops」「自动发布」「本推文由」「本文由」等脚注。
- 严禁空洞套话：如“随着技术不断发展”“正在重塑行业”“未来已来”“值得关注的是”“让我们拭目以待”“这将如何改变未来”。
- 严禁“我觉得”“我相信”“我们可以看到”等弱观点开头。
- 严禁 emoji、口号式鸡汤、过度书面化政企宣传腔。
- 严禁把内容写成“新闻摘要复述”；必须有观点提炼与结构化表达。

【按手册落实 — 与各字段对应关系】
- twitter：全英文。必须是可直接发的单条，不要 thread。严格用手册「推特」节的钩子公式（反认知/提问/数字极限/对比对立/损失厌恶至少一种），结构为“钩子判断 + 2-3 个具体信号 + 前瞻结论”。总长尽量控制在 180-270 字符；禁止中文；除非必要，不强塞 hashtag。
- weibo：全中文。必须像自媒体观点微博，不像新闻播报。用手册「微博」开篇钩子 +「模式A｜热搜体短微博」取向，350-800 字；多短段；至少 1 句传播型金句；结尾有互动（反问、站队、评论区召唤）；2-3 个 #话题#（双井号格式）。
- xhs_title + xhs_body：全中文。标题必须是小红书点击型标题，优先短、狠、准，避免空泛，长度尽量不超过 20 个汉字；正文 500-1000 字，用手册「干货清单型」或「知识科普型」取向之一，结构必须清晰（痛点/判断/拆解/行动建议）；结尾带 5-10 个搜索向 #标签#（空格或换行分隔均可）。
- wechat_title + wechat_body：全中文。标题要有公众号打开率意识，避免太虚；正文 1500-3000 字，按「观点型深度」或「故事型深度」取向写：开篇场景化、主体分段递进、至少 2 句可截图传播的金句、结尾有自然转发/在看引导。不能只堆信息，必须有清晰主线与节奏。"""


def _build_system_prompt() -> str:
    hb = _load_prompt_handbook()
    # 完整手册约 1.2 万+ 字，部分网络/SSL 下过长请求易断连；默认截断保留前部公式与规则。
    # 不截断：export THUQX_PROMPT_HANDBOOK_MAX_CHARS=0
    _mc = os.environ.get("THUQX_PROMPT_HANDBOOK_MAX_CHARS", "12000").strip()
    max_chars = 0 if _mc in ("0", "") else int(_mc)
    if max_chars > 0 and len(hb) > max_chars:
        hb = hb[:max_chars] + "\n\n…（手册已截断，可提高 THUQX_PROMPT_HANDBOOK_MAX_CHARS 或去掉截断）"
    if hb.strip():
        return (
            _QWEN_SYSTEM_CORE
            + "\n\n【《四大平台内容生产提示词手册》全文 — 你必须遵守其中公式、结构、禁忌，除上文「每条一键出稿」约束外不另生成多组模式】\n\n"
            + hb.strip()
        )
    return (
        _QWEN_SYSTEM_CORE
        + "\n\n（未找到同目录 "
        + _HANDBOOK_NAME
        + "，请将该文件放在 scripts 目录以获得完整爆款公式。）"
    )


def _parse_llm_json_block(text: str):
    text = (text or "").strip()
    fence = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", text)
    if fence:
        text = fence.group(1).strip()
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        return None
    if not isinstance(data, dict):
        return None
    out = {}
    for k in REQUIRED_KEYS:
        if k not in data or not str(data[k]).strip():
            return None
        out[k] = str(data[k]).strip()
    return out


def _sanitize_platform_text(s: str) -> str:
    s = _BAD_PHRASE.sub("", s or "")
    return re.sub(r"\n{3,}", "\n\n", s).strip()


def generate_with_qwen(feedback: str = "") -> dict | None:
    if not DASHSCOPE_API_KEY:
        return None
    url = f"{QWEN_API_BASE}/chat/completions"
    user_block = f"""用户主题：{topic}

{materials_text if materials_text else "（当前无可用网页摘要：请仅根据主题做合理、克制的推断，避免捏造具体事实；人物性别不明时请用中性称呼。）"}

{feedback if feedback else ""}

请严格按 system 规则，为主题生成六个平台稿件，输出单个 JSON 对象（仅该对象，无其它字符）。"""
    payload = json.dumps(
        {
            "model": QWEN_MODEL,
            "messages": [
                {"role": "system", "content": _build_system_prompt()},
                {"role": "user", "content": user_block},
            ],
            "temperature": 0.65,
        },
        ensure_ascii=False,
    ).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=payload,
        headers={
            "Content-Type": "application/json; charset=utf-8",
            "Authorization": f"Bearer {DASHSCOPE_API_KEY}",
        },
        method="POST",
    )
    try:
        with _https_open(req, 180) as resp:
            raw = json.loads(resp.read().decode("utf-8", errors="ignore"))
        reply = raw["choices"][0]["message"]["content"]
        parsed = _parse_llm_json_block(reply)
        if parsed:
            for k in REQUIRED_KEYS:
                parsed[k] = _sanitize_platform_text(parsed[k])
            return parsed
        return None
    except Exception as e:
        if os.environ.get("THUQX_DEBUG_LLM", "").strip() in ("1", "true", "yes"):
            print(f"[generate_content] LLM error: {e}", file=sys.stderr)
        return None


def _trim_for_twitter(text: str, max_len: int = 280) -> str:
    text = (text or "").strip()
    if len(text) <= max_len:
        return text
    return text[: max_len - 1].rstrip() + "…"


def _count_cjk(text: str) -> int:
    return sum(1 for ch in text if "\u4e00" <= ch <= "\u9fff")


def _too_generic(text: str) -> bool:
    bad_phrases = [
        "随着技术不断发展",
        "正在重塑",
        "未来已来",
        "值得关注的是",
        "让我们拭目以待",
        "这将如何改变未来",
        "我们可以看到",
        "我觉得",
        "我相信",
    ]
    text = (text or "").strip()
    return any(p in text for p in bad_phrases)


def _has_hook(text: str) -> bool:
    text = (text or "").strip()
    if not text:
        return False
    head = "\n".join(text.splitlines()[:2])
    hook_markers = [
        "？",
        "?",
        "不是",
        "而是",
        "但",
        "却",
        "正在",
        "别再",
        "真相",
        "代价",
        "99%",
        "90%",
        "3个",
        "5个",
        "为什么",
    ]
    return any(marker in head for marker in hook_markers)


def _count_signals(text: str) -> int:
    text = (text or "").strip()
    signal_markers = [
        "因为",
        "比如",
        "例如",
        "一个信号",
        "第二个信号",
        "第三个信号",
        "信号",
        "变化",
        "数据",
        "产品",
        "用户",
        "成本",
        "价格",
        "发布",
        "增长",
        "下降",
        "instead",
        "because",
        "signal",
        "shift",
        "cost",
        "users",
        "launch",
    ]
    hits = sum(text.count(marker) for marker in signal_markers)
    return hits


def _has_judgment(text: str) -> bool:
    text = (text or "").strip().lower()
    markers = [
        "我判断",
        "判断是",
        "不是",
        "而是",
        "本质上",
        "真正的变化",
        "意味着",
        "接下来",
        "核心不是",
        "关键不在于",
        "the real shift",
        "this means",
        "the point is",
        "what matters is",
        "the moat is",
        "the race is",
    ]
    return any(marker in text for marker in markers)


def _quality_notes(content: dict) -> list[str]:
    notes: list[str] = []
    if not _has_hook(content.get("twitter", "")):
        notes.append("twitter 开头缺少明显钩子")
    if not _has_judgment(content.get("twitter", "")):
        notes.append("twitter 缺少明确判断")
    if _count_signals(content.get("twitter", "")) < 2:
        notes.append("twitter 具体信号不足")
    if not _has_hook(content.get("weibo", "")):
        notes.append("weibo 开头不够抓人")
    if not _has_judgment(content.get("weibo", "")):
        notes.append("weibo 缺少明确观点")
    if _count_signals(content.get("weibo", "")) < 3:
        notes.append("weibo 具体信号不足")
    if not _has_hook(content.get("xhs_body", "")):
        notes.append("小红书正文开头缺少痛点/冲突钩子")
    if not _has_judgment(content.get("xhs_body", "")):
        notes.append("小红书正文缺少清晰判断")
    if not _has_hook(content.get("wechat_body", "")):
        notes.append("公众号开头场景感或冲突感不足")
    if _count_signals(content.get("wechat_body", "")) < 4:
        notes.append("公众号正文具体信号不足")
    return notes


def _paragraphs(text: str) -> list[str]:
    return [p.strip() for p in re.split(r"\n\s*\n", (text or "").strip()) if p.strip()]


def _validate_content(content: dict) -> tuple[bool, str]:
    tw = (content.get("twitter") or "").strip()
    wb = (content.get("weibo") or "").strip()
    xt = (content.get("xhs_title") or "").strip()
    xb = (content.get("xhs_body") or "").strip()
    wt = (content.get("wechat_title") or "").strip()
    wbody = (content.get("wechat_body") or "").strip()

    if not (180 <= len(tw) <= 280):
        return False, f"twitter length out of range: {len(tw)}"
    if _too_generic(tw):
        return False, "twitter too generic"
    if _count_cjk(tw) > 0:
        return False, "twitter contains Chinese"
    if not _has_hook(tw):
        return False, "twitter lacks a strong hook"
    if not _has_judgment(tw):
        return False, "twitter lacks explicit judgment"
    if _count_signals(tw) < 2:
        return False, "twitter lacks enough concrete signals"
    if not any(sig in tw.lower() for sig in ["but", "while", "instead", "shift", "race", "moat", "because"]):
        return False, "twitter lacks tension/judgment markers"

    if not (350 <= len(wb) <= 900):
        return False, f"weibo length out of range: {len(wb)}"
    if _too_generic(wb):
        return False, "weibo too generic"
    if len(_paragraphs(wb)) < 3:
        return False, "weibo lacks paragraph rhythm"
    if not _has_hook(wb):
        return False, "weibo lacks a strong hook"
    if not _has_judgment(wb):
        return False, "weibo lacks explicit judgment"
    if _count_signals(wb) < 3:
        return False, "weibo lacks enough concrete signals"
    if wb.count("#") < 4:
        return False, "weibo lacks topic tags"

    if not xt or len(xt) > 20:
        return False, f"xhs_title length invalid: {len(xt)}"
    if _too_generic(xt):
        return False, "xhs_title too generic"
    if not (500 <= len(xb) <= 1200):
        return False, f"xhs_body length out of range: {len(xb)}"
    if _too_generic(xb):
        return False, "xhs_body too generic"
    if not _has_hook(xb):
        return False, "xhs_body lacks a strong hook"
    if not _has_judgment(xb):
        return False, "xhs_body lacks explicit judgment"
    if xb.count("#") < 5:
        return False, "xhs_body lacks enough searchable tags"

    if not wt or len(wt) > 32:
        return False, f"wechat_title length invalid: {len(wt)}"
    if _too_generic(wt):
        return False, "wechat_title too generic"
    if len(wbody) < 1200:
        return False, f"wechat_body too short: {len(wbody)}"
    if _too_generic(wbody):
        return False, "wechat_body too generic"
    if len(_paragraphs(wbody)) < 6:
        return False, "wechat_body lacks enough sections"
    if not _has_hook(wbody):
        return False, "wechat_body lacks a strong opening hook"
    if not _has_judgment(wbody):
        return False, "wechat_body lacks explicit judgment"
    if _count_signals(wbody) < 4:
        return False, "wechat_body lacks enough concrete signals"

    return True, "ok"


content = None
last_reason = ""
if DASHSCOPE_API_KEY:
    feedback = ""
    for attempt in range(1, MAX_RETRIES + 1):
        candidate = generate_with_qwen(feedback=feedback)
        if candidate is None:
            last_reason = "llm returned empty or unparsable content"
        else:
            ok, reason = _validate_content(candidate)
            if ok:
                content = candidate
                break
            last_reason = reason
            feedback = (
                "上一版内容未通过质检，请整体重写，不要只做微调。\n"
                f"失败原因：{reason}\n"
                "请重点修正：开头钩子、明确判断、具体信号数量、平台风格、标题长度。"
            )
        if os.environ.get("THUQX_DEBUG_LLM", "").strip() in ("1", "true", "yes"):
            print(f"[generate_content] retry {attempt}/{MAX_RETRIES} failed: {last_reason}", file=sys.stderr)
else:
    content = None

if not content and DASHSCOPE_API_KEY and not _ALLOW_TEMPLATE:
    print(
        "[generate_content] 通义千问生成失败或解析失败。请检查 API Key、网络与 QWEN_INSECURE_SSL；"
        f"最后失败原因：{last_reason or 'unknown'}；"
        "或临时设置 THUQX_ALLOW_TEMPLATE_FALLBACK=1 使用本地模板。",
        file=sys.stderr,
    )
    sys.exit(1)

if not content and not DASHSCOPE_API_KEY and not _ALLOW_TEMPLATE:
    print(
        "[generate_content] 未配置 DASHSCOPE_API_KEY / QWEN_API_KEY。"
        "请配置 ~/.openclaw/zeelin-qwen.env 或导出变量；"
        "调试可设 THUQX_ALLOW_TEMPLATE_FALLBACK=1。",
        file=sys.stderr,
    )
    sys.exit(1)

if content is None:
    content = {}

if not content:
    # 仅当 THUQX_ALLOW_TEMPLATE_FALLBACK=1 且千问不可用时启用；与主题弱相关占位，生产环境请用千问
    mt = (materials_text or "").strip()
    content["twitter"] = _trim_for_twitter(
        f"Quick note on «{topic}»: context matters—tell me what stood out to you. "
        f"(Template fallback — enable Qwen for real copy.) #News #Discussion"
    )
    content["weibo"] = _sanitize_platform_text(
        f"【{topic}】一条模板备用帖：请开启通义千问生成正式微博稿。摘要参考：\n{mt}"[:800]
    )
    content["xhs_title"] = f"{topic}｜模板占位（请用千问）"
    content["xhs_body"] = _sanitize_platform_text(
        f"这是「{topic}」的小红书模板占位正文，用于在无 API 时的兜底；请配置 DashScope 后重试以获得笔记风长文。\n\n{mt}"[
            :1200
        ]
    )
    content["wechat_title"] = f"{topic}：模板占位（建议启用内容生成）"
    content["wechat_body"] = _sanitize_platform_text(
        f"本文为系统模板占位，主题为「{topic}」。正式群发前请使用千问生成长文。\n\n{mt}"[:2500]
    )

if content.get("twitter"):
    content["twitter"] = _trim_for_twitter(_sanitize_platform_text(content["twitter"]))
for _k in ("weibo", "xhs_title", "xhs_body", "wechat_title", "wechat_body"):
    if content.get(_k):
        content[_k] = _sanitize_platform_text(content[_k])

ok, reason = _validate_content(content)
if not ok:
    print(f"[generate_content] 内容质检未通过：{reason}", file=sys.stderr)
    sys.exit(1)

json_text = json.dumps(content, ensure_ascii=False, indent=2 if ARGS.pretty else None)

if ARGS.output:
    Path(ARGS.output).expanduser().write_text(json_text + "\n", encoding="utf-8")

if ARGS.materials_output:
    Path(ARGS.materials_output).expanduser().write_text(
        json.dumps(materials, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

print(json_text)
