"""
配置模块 - Skills Trending 配置
"""
import os

# ============================================================================
# Skills.sh 配置
# ============================================================================
SKILLS_BASE_URL = os.getenv("SKILLS_BASE_URL", "https://skills.sh")
SKILLS_TRENDING_URL = f"{SKILLS_BASE_URL}/trending"

# ============================================================================
# 抓取配置
# ============================================================================
TOP_N_DETAILS = 20  # 抓取详情的数量
FETCH_REQUEST_DELAY = 2  # 抓取详情时的请求间隔（秒）

# ============================================================================
# 技能分类定义
# ============================================================================
CATEGORIES = {
    "frontend": {
        "name": "前端",
        "name_en": "Frontend",
        "icon": "🌐",
        "description": "React, Vue, CSS 等前端技术"
    },
    "backend": {
        "name": "后端",
        "name_en": "Backend",
        "icon": "⚙️",
        "description": "Node, Python, APIs 等后端技术"
    },
    "mobile": {
        "name": "移动",
        "name_en": "Mobile",
        "icon": "📱",
        "description": "iOS, Android, React Native"
    },
    "devops": {
        "name": "运维",
        "name_en": "DevOps",
        "icon": "🔧",
        "description": "CI/CD, Docker, Kubernetes"
    },
    "video": {
        "name": "视频",
        "name_en": "Video",
        "icon": "🎬",
        "description": "视频生成、编辑"
    },
    "animation": {
        "name": "动画",
        "name_en": "Animation",
        "icon": "✨",
        "description": "动画、动效设计"
    },
    "data": {
        "name": "数据",
        "name_en": "Data",
        "icon": "📊",
        "description": "数据分析、BI 工具"
    },
    "ai-ml": {
        "name": "AI/ML",
        "name_en": "AI/ML",
        "icon": "🤖",
        "description": "机器学习、人工智能"
    },
    "testing": {
        "name": "测试",
        "name_en": "Testing",
        "icon": "🧪",
        "description": "QA, E2E 测试"
    },
    "marketing": {
        "name": "营销",
        "name_en": "Marketing",
        "icon": "📢",
        "description": "SEO, 内容营销"
    },
    "docs": {
        "name": "文档",
        "name_en": "Docs",
        "icon": "📚",
        "description": "教程、文档"
    },
    "design": {
        "name": "设计",
        "name_en": "Design",
        "icon": "🎨",
        "description": "UI/UX 设计"
    },
    "database": {
        "name": "数据库",
        "name_en": "Database",
        "icon": "🗄️",
        "description": "SQL, NoSQL"
    },
    "security": {
        "name": "安全",
        "name_en": "Security",
        "icon": "🔒",
        "description": "安全工具"
    },
    "other": {
        "name": "其他",
        "name_en": "Other",
        "icon": "📁",
        "description": "未分类"
    }
}


def get_category_info(category_key: str) -> dict:
    """获取分类信息"""
    return CATEGORIES.get(category_key, CATEGORIES["other"])
