# 微信文章读取器模块化重构计划

## 项目信息
- **项目路径**: `/home/morav/.openclaw/agents/xingchen/workspace/skills/wechat-article-reader/scripts/`
- **目标**: 将 `fetch_gzh_trends.py` (1117行) 拆分为独立模块
- **原则**: TDD, 向后兼容, 可测试

---

## 目标架构

```
wechat-article-reader/scripts/
├── gzh_article.py              # 主入口 (CLI不变)
├── wechat_article.py           # 公众号文章列表
├── fetch_wechat_article.py     # 单篇正文抓取
│
├── core/                       # 核心共享模块
│   ├── __init__.py             # 统一导出
│   ├── models.py               # 数据模型
│   ├── security.py             # 安全工具
│   ├── http_client.py          # HTTP客户端
│   └── utils.py                # 工具函数
│
└── trends/                     # 爆款数据模块
    ├── __init__.py
    ├── api.py                  # API调用
    ├── scoring.py              # 评分算法
    ├── sorting.py              # 排序逻辑
    └── formatters/             # 格式化器
        ├── __init__.py
        ├── base.py
        ├── text.py
        ├── json.py
        └── html.py
```

---

## 数据模型 (core/models.py)

```python
# 关键 dataclass

@dataclass
class ArticleMetrics:
    like_count: int = 0
    comment_count: int = 0
    share_count: int = 0
    clicks_count: int = 0
    interactive_count: int = 0

@dataclass
class TrendingArticle:
    photo_id: str
    title: str
    summary: str
    account_id: str
    account_name: str
    fans: int
    public_time: str
    metrics: ArticleMetrics
    ori_url: str = ''
    cover_url: str = ''
    category_key: str = ''
    category_name: str = ''

@dataclass
class ScoredArticle:
    article: TrendingArticle
    data_score: float = 0.0
    relevance_score: float = 0.0
    title_quality: int = 100

@dataclass
class TrendingResult:
    keyword: str
    raw_categories: Dict[str, List]
    scored_articles: List[ScoredArticle] = field(default_factory=list)
```

---

## 阶段1任务分配

| Agent | 文件 | 职责 | 输入 |
|-------|------|------|------|
| Agent-1 | core/models.py | 数据模型 dataclass | 已有 core/__init__.py |
| Agent-2 | core/security.py | 安全函数 (sanitize_*, safe_*) | fetch_gzh_trends.py:20-65 |
| Agent-3 | core/http_client.py | NoSNIClient 类 | fetch_gzh_trends.py:89-186 |
| Agent-4 | core/utils.py | parse_count, format_number | core/__init__.py |
| Agent-5 | core/__init__.py | 统一导出, __all__ | 协调其他模块 |

---

## 阶段2任务分配

| Agent | 文件 | 职责 | 依赖 |
|-------|------|------|------|
| Agent-6 | trends/api.py | fetch_trending_data() | core/* |
| Agent-7 | trends/scoring.py | calculate_*_score() | core/models.py |
| Agent-8 | trends/sorting.py | merge_and_sort(), ensure_diversity() | core/models.py |
| Agent-9 | trends/formatters/ | Text/Json/HtmlFormatter | core/* |
| Agent-10 | trends/__init__.py + cli.py | 统一导出, CLI入口 | trends/* |

---

## 关键函数签名

### core/security.py
```python
def sanitize_http_url(url) -> str
def safe_href_url(url) -> str
def safe_wechat_account_id(account_id) -> str
def safe_filename_from_keyword(keyword: str, max_len: int = 120) -> str
```

### core/http_client.py
```python
class NoSNIClient:
    def fetch_json(self, url: str, params: dict, headers: dict) -> dict
    def fetch_text(self, url: str, params: dict, headers: dict) -> str
```

### trends/api.py
```python
def fetch_trending_data(
    keyword: str,
    start_date: Optional[str] = None,
    client: Optional[NoSNIClient] = None,
    debug: bool = False
) -> TrendingResult
```

### trends/scoring.py
```python
def calculate_title_quality(title: str) -> int  # 0-100
def calculate_relevance_score(article: TrendingArticle, keyword: str) -> float  # 0-15
def calculate_data_score(article: TrendingArticle, cat_key: str, keyword: str = '') -> float  # 0-150
def score_article(article: TrendingArticle, keyword: str, cat_key: str) -> ScoredArticle
```

### trends/sorting.py
```python
def merge_and_sort(
    articles: List[TrendingArticle],
    keyword: str = '',
    max_items: int = 10
) -> List[ScoredArticle]

def ensure_category_diversity(
    scored: List[ScoredArticle],
    max_items: int = 10,
    min_categories: int = 3
) -> List[ScoredArticle]
```

---

## 测试要求

每个模块必须有自己的测试文件：
- `test_core_models.py`
- `test_core_security.py`
- `test_core_http_client.py`
- `test_core_utils.py`
- `test_trends_api.py`
- `test_trends_scoring.py`
- `test_trends_sorting.py`
- `test_trends_formatters.py`

---

## 向后兼容

~~`fetch_gzh_trends.py` 保留为兼容层~~ - **已删除旧代码**

新模块直接使用：
```bash
# 新的调用方式
from trends.api import fetch_trending_data
from trends.formatters import get_formatter
```

或通过 CLI：
```bash
python3 trends/cli.py --keyword AI --max-items 5
```

---

## 验证方法

```bash
# 阶段1完成后
python3 -c "from core import *"

# 阶段2完成后
python3 trends/cli.py --keyword AI --max-items 5

# 整体验证
python3 gzh_article.py trends AI --max-items 5
# 输出应与重构前一致
```

---

## 更新日志

- 2026-05-23: 创建计划文档
- 2026-05-23: 阶段1完成 - 5个Agent创建core模块 (88 tests passed)
- 2026-05-23: 启动阶段2 - 4个Agent并行创建trends模块
  - trends/api.py - API调用
  - trends/scoring.py - 评分算法
  - trends/sorting.py - 排序逻辑
  - trends/formatters/ - 格式化器