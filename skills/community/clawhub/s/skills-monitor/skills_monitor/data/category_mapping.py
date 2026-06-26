"""
官方标签分类映射 v0.5.0
========================
将 ClawHub 官方分类标签对齐到本地分类体系。

使用方式：
    from skills_monitor.data.category_mapping import get_category, match_tags
    
    cat = get_category("finance")          # → {"name": "金融投资", "icon": "📈", ...}
    tags = match_tags(["stock", "trading"]) # → ["finance"]
"""

from typing import Dict, List, Optional, Set


# ──────── ClawHub 官方分类 → 本地标签映射 ────────

CLAWHUB_CATEGORIES: Dict[str, Dict] = {
    "finance": {
        "name": "金融投资",
        "name_en": "Finance & Investment",
        "icon": "📈",
        "keywords": {"stock", "trading", "finance", "invest", "market", "fund", "crypto", "forex"},
        "description": "股票、基金、加密货币、外汇等金融交易工具",
    },
    "data-analysis": {
        "name": "数据分析",
        "name_en": "Data Analysis",
        "icon": "📊",
        "keywords": {"data", "analysis", "analytics", "statistics", "visualization", "chart", "report"},
        "description": "数据处理、统计分析、数据可视化工具",
    },
    "web-scraping": {
        "name": "数据采集",
        "name_en": "Web Scraping",
        "icon": "🕸️",
        "keywords": {"scrape", "scraping", "crawl", "spider", "extract", "fetch"},
        "description": "网页抓取、数据提取、爬虫工具",
    },
    "automation": {
        "name": "自动化",
        "name_en": "Automation",
        "icon": "🤖",
        "keywords": {"automate", "automation", "workflow", "pipeline", "schedule", "cron", "task"},
        "description": "流程自动化、任务调度、工作流工具",
    },
    "communication": {
        "name": "通讯协作",
        "name_en": "Communication",
        "icon": "💬",
        "keywords": {"chat", "message", "email", "slack", "discord", "telegram", "wechat", "notification"},
        "description": "即时通讯、邮件、通知、协作工具",
    },
    "development": {
        "name": "开发工具",
        "name_en": "Development",
        "icon": "🛠️",
        "keywords": {"dev", "code", "coding", "git", "github", "debug", "test", "deploy", "ci", "cd"},
        "description": "代码开发、测试、部署、DevOps 工具",
    },
    "search": {
        "name": "搜索引擎",
        "name_en": "Search",
        "icon": "🔍",
        "keywords": {"search", "query", "find", "lookup", "google", "bing", "duckduckgo"},
        "description": "网络搜索、信息检索工具",
    },
    "media": {
        "name": "多媒体",
        "name_en": "Media",
        "icon": "🎨",
        "keywords": {"image", "video", "audio", "media", "photo", "music", "art", "design", "draw"},
        "description": "图片、视频、音频处理与生成工具",
    },
    "security": {
        "name": "安全审计",
        "name_en": "Security",
        "icon": "🔐",
        "keywords": {"security", "audit", "scan", "vulnerability", "password", "encrypt", "ssl"},
        "description": "安全扫描、漏洞检测、加密工具",
    },
    "education": {
        "name": "学习教育",
        "name_en": "Education",
        "icon": "📚",
        "keywords": {"learn", "education", "study", "course", "tutorial", "knowledge", "quiz"},
        "description": "在线学习、知识管理、教程工具",
    },
    "productivity": {
        "name": "效率工具",
        "name_en": "Productivity",
        "icon": "⚡",
        "keywords": {"productivity", "todo", "note", "calendar", "time", "organize", "manage"},
        "description": "任务管理、笔记、日历、时间管理工具",
    },
    "ai-model": {
        "name": "AI 模型",
        "name_en": "AI Model",
        "icon": "🧠",
        "keywords": {"ai", "ml", "model", "llm", "gpt", "claude", "deepseek", "gemini", "openai"},
        "description": "AI 模型调用、提示工程、模型管理工具",
    },
    "database": {
        "name": "数据库",
        "name_en": "Database",
        "icon": "🗄️",
        "keywords": {"database", "sql", "mysql", "postgres", "mongodb", "redis", "supabase", "firebase"},
        "description": "数据库操作、查询、管理工具",
    },
    "cloud": {
        "name": "云服务",
        "name_en": "Cloud",
        "icon": "☁️",
        "keywords": {"cloud", "aws", "azure", "gcp", "tencent", "aliyun", "docker", "kubernetes"},
        "description": "云平台操作、容器管理、服务部署工具",
    },
    "document": {
        "name": "文档处理",
        "name_en": "Document",
        "icon": "📄",
        "keywords": {"document", "pdf", "word", "excel", "markdown", "csv", "file", "convert"},
        "description": "文档读写、格式转换、文件处理工具",
    },
    "other": {
        "name": "其他",
        "name_en": "Other",
        "icon": "📦",
        "keywords": set(),
        "description": "未分类工具",
    },
}


# ──────── 公共 API ────────

def get_category(category_id: str) -> Optional[Dict]:
    """获取分类详情"""
    return CLAWHUB_CATEGORIES.get(category_id)


def get_all_categories() -> Dict[str, Dict]:
    """获取所有分类"""
    return dict(CLAWHUB_CATEGORIES)


def match_tags(tags: List[str]) -> List[str]:
    """
    根据标签列表匹配分类 ID
    
    Args:
        tags: ["stock", "trading", "analysis"]
    Returns:
        ["finance", "data-analysis"]
    """
    if not tags:
        return ["other"]

    tag_set = {t.lower().strip() for t in tags}
    matched = []

    for cat_id, cat_info in CLAWHUB_CATEGORIES.items():
        if cat_id == "other":
            continue
        keywords = cat_info.get("keywords", set())
        if tag_set & keywords:  # 交集非空
            matched.append(cat_id)

    return matched if matched else ["other"]


def infer_category_from_name(skill_name: str) -> str:
    """从 skill 名称推断分类"""
    name_lower = skill_name.lower().replace("-", " ").replace("_", " ")
    best_match = "other"
    best_score = 0

    for cat_id, cat_info in CLAWHUB_CATEGORIES.items():
        if cat_id == "other":
            continue
        score = sum(1 for kw in cat_info.get("keywords", set()) if kw in name_lower)
        if score > best_score:
            best_score = score
            best_match = cat_id

    return best_match


def get_category_display(category_id: str) -> str:
    """获取分类的显示文本（含 icon）"""
    cat = CLAWHUB_CATEGORIES.get(category_id, CLAWHUB_CATEGORIES["other"])
    return f"{cat['icon']} {cat['name']}"
