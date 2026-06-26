"""
utils.py — 常量定义 + 基础工具函数

包含所有全局常量（路径、关键词、推荐规则）和被多个模块复用的工具函数。
"""

import os
import re
import sys
import subprocess
from pathlib import Path
from collections import defaultdict


# ─── 路径常量 ───────────────────────────────────────────────────────────────

HOME = Path.home()


def _detect_bundled_path() -> Path:
    """自动探测 OpenClaw bundled skills 的安装路径"""
    candidates = [
        Path("/opt/homebrew/lib/node_modules/openclaw/skills"),  # Homebrew (macOS Apple Silicon)
        Path("/usr/local/lib/node_modules/openclaw/skills"),     # Homebrew (Intel) / npm global
        Path("/home/linuxbrew/.linuxbrew/lib/node_modules/openclaw/skills"),  # Linuxbrew
    ]
    # 尝试通过 `which openclaw` 推测
    try:
        result = subprocess.run(
            ["which", "openclaw"], capture_output=True, text=True, timeout=5
        )
        if result.returncode == 0:
            openclaw_bin = Path(result.stdout.strip()).resolve()
            # openclaw 通常在 lib/node_modules/openclaw/bin/
            node_modules = openclaw_bin.parent.parent
            if node_modules.name == "node_modules":
                candidate = node_modules / "openclaw" / "skills"
                if candidate.is_dir():
                    return candidate
    except Exception:
        pass
    for p in candidates:
        if p.is_dir():
            return p
    return candidates[0]  # fallback


SKILL_PATHS = {
    "bundled": _detect_bundled_path(),
    "workspace": HOME / ".openclaw/workspace/skills",
    "managed": HOME / ".openclaw/skills",
}

# 数据源路径（均为可选，缺失时优雅降级）
MEMORY_MD = HOME / ".openclaw/workspace/MEMORY.md"
HEARTBEAT_MD = HOME / ".openclaw/workspace/HEARTBEAT.md"
AGENTS_MD = HOME / ".openclaw/workspace/AGENTS.md"
MEMORY_DIR = HOME / ".openclaw/workspace/memory"
SESSIONS_DIR = HOME / ".openclaw/agents/main/sessions"


def detect_available_data_sources() -> list[dict]:
    """
    检测当前环境可用的数据源。
    返回 [{"name": str, "available": bool, "path": str, "description": str}, ...]
    """
    sources = [
        ("Session 日志", SESSIONS_DIR.is_dir(), str(SESSIONS_DIR), "用户对话记录"),
        ("每日记忆", MEMORY_DIR.is_dir(), str(MEMORY_DIR), "memory/*.md 日记文件"),
        ("MEMORY.md", MEMORY_MD.is_file(), str(MEMORY_MD), "核心配置与偏好"),
        ("HEARTBEAT.md", HEARTBEAT_MD.is_file(), str(HEARTBEAT_MD), "定期任务配置"),
        ("AGENTS.md", AGENTS_MD.is_file(), str(AGENTS_MD), "工作规则"),
    ]
    # Mem0: 检查脚本或数据文件
    mem0_script = HOME / ".openclaw/skills/mem0/list.py"
    mem0_data = HOME / ".openclaw/skills/mem0"
    mem0_ok = mem0_script.is_file() or any(
        f.is_file() and f.name not in ("package.json", "README.md")
        for f in mem0_data.glob("*") if mem0_data.is_dir()
    ) if mem0_data.is_dir() else False
    sources.insert(0, ("Mem0", mem0_ok, str(mem0_data), "向量记忆系统"))

    return [{"name": n, "available": a, "path": p, "description": d} for n, a, p, d in sources]


# ─── 关键词过滤 ─────────────────────────────────────────────────────────────

# 过于泛化的关键词，单独匹配时忽略（避免误判）
# 这些词只有在与更具体的词组合时才有意义
GENERIC_KEYWORDS = {
    # English common words
    "code", "coding", "tool", "tools", "agent", "agents", "skill", "skills",
    "app", "apps", "use", "using", "used", "make", "create", "build",
    "run", "get", "set", "check", "test", "help", "work", "data",
    "file", "files", "open", "new", "update", "add", "delete", "remove",
    "list", "search", "find", "read", "write", "edit", "show",
    "the", "for", "and", "with", "this", "that", "from", "into",
    "can", "you", "your", "will", "all", "not", "are", "was",
    "via", "cli", "api", "when", "how", "also", "more", "has",
    "based", "enable", "allows", "provides", "support", "supports",
    "control", "manage", "monitor", "track", "view", "access",
    "install", "setup", "config", "configure", "integration",
    "best", "practices", "including", "such", "each", "other",
    "need", "needs", "should", "must", "may", "might",
    "just", "only", "both", "most", "well", "very",
    "local", "remote", "host", "cloud", "web", "online",
    "send", "receive", "download", "upload", "fetch", "parse",
    "format", "output", "input", "process", "convert", "extract",
    "text", "json", "markdown", "html", "pdf", "image", "audio",
    "video", "photo", "media", "content", "document", "documents",
    "cli", "tui", "gui", "interface", "dashboard", "panel",
    # Extra generic short words (2-3 chars)
    "the", "and", "for", "are", "but", "not", "you", "all",
    "can", "has", "had", "was", "its", "our", "out", "how",
    "who", "why", "way", "may", "one", "two", "new", "now",
    "use", "get", "set", "put", "see", "say", "try", "own",
    "any", "few", "let", "via", "api", "url", "app", "end",
    "run", "add", "log", "key", "tag", "due", "day", "top",
    "pr", "ci", "cd", "gh", "db", "st", "qr", "ai",
    "via", "per", "pro", "non", "pre", "sub", "dis", "mis",
    "all", "and", "but", "for", "nor", "yet", "out", "off",
    "com", "org", "net", "www", "tcp", "udp", "dns", "ssh",
    "mac", "ios", "rpc", "sql", "xml", "csv", "tmp", "low",
    "zh", "en", "de", "fr", "jp", "cn", "us", "uk",
    # More generic tech terms
    "user", "admin", "auth", "token", "basic", "advanced", "simple", "custom",
    "default", "global", "local", "public", "private", "internal", "external",
    "first", "last", "next", "previous", "current", "latest", "recent",
    "single", "multiple", "batch", "single",
    "query", "request", "response", "result", "results",
    "status", "state", "event", "action", "trigger", "handler",
    "before", "after", "during", "between", "without", "within",
    "include", "includes", "exclude", "requires", "supports",
    "option", "options", "feature", "features", "setting", "settings",
    "service", "services", "system", "systems", "platform", "plugin", "plugins",
    "project", "projects", "module", "modules", "package", "packages",
    "version", "release", "deploy", "deploy", "server", "client",
    # Chinese common words
    "支持", "使用", "功能", "配置", "管理", "设置", "操作", "任务",
    "工具", "文件", "信息", "内容", "生成", "创建", "处理", "执行",
    "分析", "查看", "获取", "检查", "更新", "安装", "运行",
    "通过", "包括", "可以", "需要", "提供", "支持", "实现",
    "进行", "完成", "发送", "接收", "转换", "编辑", "读取",
    "写入", "搜索", "查找", "下载", "上传", "解析", "监控",
    "管理", "控制", "访问", "连接", "集成", "自动化", "定期",
    "智能", "基于", "优化", "改进", "增强", "简化", "扩展",
    "记录", "日志", "状态", "报告", "结果", "数据",
    # Extra generic tech terms that appear everywhere
    "openclaw", "clawdbot", "cream", "session", "message", "workspace",
}


# ─── 推荐规则 ───────────────────────────────────────────────────────────────

RECOMMENDATION_RULES = [
    {
        "scene": "💰 金融/理财/基金/股票",
        "keywords": ["基金", "股票", "理财", "投资", "汇率", "黄金", "加密", "比特币",
                     "BTC", "ETF", "定投", "净值", "A股", "港股", "美股", "财经",
                     "fund", "stock", "crypto", "forex", "finance"],
        "search_query": "finance",
    },
    {
        "scene": "🌐 翻译/多语言",
        "keywords": ["翻译", "英文", "日文", "韩文", "translate", "translation",
                     "中翻英", "英翻中", "多语言", "localization", "i18n"],
        "search_query": "translate",
    },
    {
        "scene": "📅 日历/日程/提醒",
        "keywords": ["日程", "会议", "日历", "提醒", "日程表", "calendar", "schedule",
                     "meeting", "reminder", "提醒我", "几点"],
        "search_query": "calendar",
    },
    {
        "scene": "📊 数据分析/可视化",
        "keywords": ["数据分析", "图表", "可视化", "统计", "报表", "data analysis",
                     "visualization", "chart", "dashboard", "数据透视", "CSV分析"],
        "search_query": "data analysis",
    },
    {
        "scene": "🔐 密码/凭证管理",
        "keywords": ["密码", "密码管理", "凭证", "credential", "password", "API key",
                     "密钥", "token管理"],
        "search_query": "password",
    },
    {
        "scene": "📝 任务管理/待办",
        "keywords": ["待办", "TODO", "todo list", "任务列表",
                     "提醒我做什么", "清单", "checklist"],
        "search_query": "todo task",
    },
    {
        "scene": "🔗 API/接口测试",
        "keywords": ["API测试", "接口测试", "curl", "HTTP请求", "接口调试",
                     "API debug", "postman", "rest api", "endpoint"],
        "search_query": "api test",
    },
    {
        "scene": "📁 文件管理/整理",
        "keywords": ["文件整理", "文件管理", "重命名", "批量", "归类", "文件分类",
                     "organize", "file management", "批量处理"],
        "search_query": "file organize",
    },
    {
        "scene": "🤖 AI提示词优化",
        "keywords": ["提示词", "prompt", "提示工程", "提示优化", "system prompt",
                     "prompt engineering", "提示词模板"],
        "search_query": "prompt engineering",
    },
    {
        "scene": "📰 RSS/信息订阅",
        "keywords": ["RSS", "订阅", "信息源", "feed", "博客更新", "newsletter"],
        "search_query": "rss",
    },
    {
        "scene": "🖼️ 截图/录屏",
        "keywords": ["截图", "录屏", "屏幕录制", "screenshot", "screen recording",
                     "屏幕截图", "屏幕抓取"],
        "search_query": "screenshot",
    },
    {
        "scene": "🧹 系统/环境清理",
        "keywords": ["清理", "磁盘", "缓存", "垃圾文件", "内存", "系统优化",
                     "cleanup", "disk", "cache", "storage"],
        "search_query": "system cleanup",
    },
]


# ─── 工具函数 ───────────────────────────────────────────────────────────────

def run_cmd(cmd: str, timeout: int = 30) -> str:
    """运行 shell 命令，返回 stdout"""
    try:
        result = subprocess.run(
            ["/bin/sh", "-c", cmd],
            capture_output=True, text=True, timeout=timeout
        )
        return result.stdout.strip()
    except subprocess.TimeoutExpired:
        return ""
    except Exception:
        return ""


def find_skill_dirs() -> list[tuple[str, Path]]:
    """发现所有 Skill 目录，返回 [(source, path), ...]"""
    dirs = []
    for source, base in SKILL_PATHS.items():
        if not base.is_dir():
            continue
        for entry in sorted(base.iterdir()):
            skill_md = entry / "SKILL.md"
            if skill_md.is_file():
                dirs.append((source, entry))
    return dirs


def parse_skill_md(path: Path) -> dict:
    """解析 SKILL.md，提取 name、description 等元信息"""
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return {}

    info = {"name": path.parent.name, "description": "", "path": str(path)}

    # 解析 YAML frontmatter
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            frontmatter = parts[1].strip()
            m = re.search(r'^name:\s*(.+)$', frontmatter, re.MULTILINE)
            if m:
                info["name"] = m.group(1).strip().strip('"\'')
            m = re.search(r'^description:\s*(.+)$', frontmatter, re.MULTILINE)
            if m:
                info["description"] = m.group(1).strip().strip('"\'')

    # 如果 frontmatter 没有提取到 description，从第一段非空内容取
    if not info["description"]:
        for line in text.split("\n"):
            line = line.strip()
            if line and not line.startswith("#") and not line.startswith("---"):
                info["description"] = line[:200]
                break

    return info


def tokenize(text: str) -> set[str]:
    """文本分词，返回小写词集合"""
    text = text.lower()
    words = re.split(r'[\s\-_/|,.:;!?()\[\]{}]+', text)
    return {w for w in words if len(w) >= 2}


def build_skill_keywords(skill_info: dict) -> list[str]:
    """
    为单个 Skill 构建搜索关键词列表。

    优先级：精确 name > name 分词 > description 关键词
    """
    keywords = []
    name = skill_info.get("name", "").lower()
    desc = skill_info.get("description", "").lower()

    # 1. 精确 name（最高优先级）
    if name:
        keywords.append(name)

    # 2. name 的各部分（按 - _ 分割）
    name_parts = re.split(r'[-_]+', name)
    for part in name_parts:
        if len(part) >= 2 and part not in GENERIC_KEYWORDS:
            keywords.append(part)

    # 3. 从 description 提取关键词
    # 移除标点，分词
    desc_words = re.split(r'[\s\-_/|,.:;!?()\[\]{}·、，。；：！？（）【】]+', desc)
    for w in desc_words:
        w = w.strip().lower()
        # 过滤：至少3个字符，不在通用词列表中，不是纯数字
        if len(w) >= 3 and w not in GENERIC_KEYWORDS and not w.isdigit():
            keywords.append(w)

    # 4. 中文变体 / 常见别名（手动映射部分高频 Skill）
    name_aliases = {
        "tavily-search": ["tavily", "tavily search"],
        "baidu-search": ["百度", "百度搜索", "baidu"],
        "edge-tts": ["edge-tts", "edge tts", "微软tts"],
        "feishu-edge-tts-voice": ["语音消息", "语音回复", "语音发送", "晓晓", "云希", "飞书语音"],
        "feishu-voice": ["语音消息", "语音回复", "飞书语音"],
        "openai-whisper": ["whisper", "语音识别", "stt", "语音转文字"],
        "apple-notes": ["apple notes", "苹果笔记", "备忘录"],
        "feishu-doc": ["飞书文档", "飞书doc"],
        "feishu-wiki": ["飞书知识库", "知识库"],
        "feishu-drive": ["飞书云空间", "云空间", "飞盘"],
        "nano-pdf": ["pdf编辑", "编辑pdf"],
        "qwen-image": ["通义万相", "图片生成", "qwen image"],
        "alicloud-ai-image-qwen-image-edit": ["图片编辑", "图像编辑", "inpaint"],
        "weather": ["天气", "weather"],
        "summarize": ["总结", "摘要", "summarize", "总结工具"],
        "video-frames": ["视频帧", "视频截图", "ffmpeg"],
        "image-text-editor": ["图片文字", "修复错别字", "图片修字"],
        "markdown-converter": ["markitdown", "格式转换", "文档转换"],
        "find-skills": ["查找skill", "发现skill", "skill搜索"],
        "clawhub": ["clawhub", "skill安装", "skill管理"],
        "coding-agent": ["codex", "claude code", "编程代理"],
        "gh-issues": ["github issue", "issue处理"],
        "session-logs": ["会话日志", "session日志"],
        "tmux": ["tmux", "终端管理"],
        "humanize-ai-text": ["降ai率", "人性化", "ai检测"],
        "ai-news-zh": ["ai日报", "ai新闻", "科技日报"],
        "proactive-agent-lite": ["主动代理", "proactive"],
        "mem0": ["mem0", "记忆系统", "向量记忆"],
        "healthcheck": ["健康检查", "安全审计"],
        "node-connect": ["节点连接", "设备配对", "node连接"],
        "auto-updater": ["自动更新", "skill更新"],
        "agentic-coding": ["agentic coding", "代理编程"],
        "gog": ["google workspace", "g suite", "gmail cli"],
        "skill-creator": ["skill创建", "skill开发", "创建skill"],
        "code-review": ["代码审查", "code review", "pr审查"],
    }

    if name in name_aliases:
        for alias in name_aliases[name]:
            if alias not in keywords:
                keywords.append(alias)

    # 去重但保持顺序（靠前的优先级更高）
    seen = set()
    result = []
    for kw in keywords:
        if kw not in seen:
            seen.add(kw)
            result.append(kw)

    return result


def read_file_safe(path: Path) -> str:
    """安全读取文件内容"""
    try:
        if path.is_file():
            return path.read_text(encoding="utf-8", errors="replace")
    except Exception:
        pass
    return ""


def count_keyword_hits(text: str, keywords: list[str]) -> dict:
    """
    在文本中统计关键词命中次数。

    keywords[0] 是 skill name（精确匹配），其余是 description 关键词。
    返回 {"name_hits": int, "keyword_hits": int, "name_details": [...], "keyword_details": [...]}
    """
    text_lower = text.lower()
    name_hits = 0
    keyword_hits = 0
    name_details = []
    keyword_details = []

    for i, kw in enumerate(keywords):
        kw_lower = kw.lower()
        if not kw_lower or len(kw_lower) < 2:
            continue
        count = text_lower.count(kw_lower)
        if count > 0:
            if i == 0:
                # 精确 name 匹配
                name_hits += count
                name_details.append((kw, count))
            else:
                # description 关键词匹配
                keyword_hits += count
                keyword_details.append((kw, count))

    return {
        "name_hits": name_hits,
        "keyword_hits": keyword_hits,
        "total": name_hits + keyword_hits,
        "name_details": name_details,
        "keyword_details": keyword_details,
    }
