"""
core/models.py - Data Models for Wechat Article Reader
"""

from dataclasses import dataclass, field
from typing import Optional, List, Dict

# Re-use parse_count from utils to avoid duplication
from core.utils import parse_count


@dataclass
class ArticleMetrics:
    """Article interaction metrics"""
    like_count: int = 0
    comment_count: int = 0
    share_count: int = 0
    clicks_count: int = 0
    interactive_count: int = 0

    @property
    def total_interaction(self) -> int:
        return self.like_count + self.comment_count + self.share_count + self.interactive_count

    @classmethod
    def from_dict(cls, data: dict) -> 'ArticleMetrics':
        return cls(
            like_count=parse_count(data.get('likeCount', 0)),
            comment_count=parse_count(data.get('commentCount', 0) or data.get('useCommentCount', 0)),
            share_count=parse_count(data.get('shareCount', 0)),
            clicks_count=parse_count(data.get('clicksCount', 0)),
            interactive_count=parse_count(data.get('interactiveCount', 0)),
        )


@dataclass
class TrendingArticle:
    """A trending article from the API"""
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
    content: str = ''  # Full article content from API

    @property
    def article_url(self) -> str:
        # 优先使用原始长链接，添加 chksm 参数使其可被 fetch_wechat_article.py 抓取
        if self.ori_url and self.ori_url.startswith('http'):
            url = self.ori_url
            # 如果没有 chksm 参数，添加一个（微信验证需要）
            if 'chksm=' not in url:
                url = url.replace('#rd', '&chksm=placeholder#rd')
            return url
        # 无有效链接时返回空字符串（photoId 不是有效链接）
        return ''

    @classmethod
    def from_api_dict(cls, data: dict, cat_key: str = '') -> 'TrendingArticle':
        fans_raw = data.get('fans', 0)
        return cls(
            photo_id=data.get('photoId', ''),
            title=data.get('title', '') or data.get('summary', '')[:50],
            summary=data.get('summary', ''),
            account_id=data.get('accountId', ''),
            account_name=data.get('userName', '') or data.get('accountId', '未知账号'),
            fans=parse_count(fans_raw),
            public_time=data.get('publicTime', ''),
            ori_url=data.get('oriUrl', ''),
            cover_url=data.get('coverUrl', ''),
            category_key=cat_key,
            metrics=ArticleMetrics.from_dict(data),
            content=data.get('content', ''),
        )


@dataclass
class ScoredArticle:
    """A scored article with ranking info"""
    article: TrendingArticle
    data_score: float = 0.0
    relevance_score: float = 0.0
    title_quality: int = 100
    matched_keyword_count: int = 0  # 多关键词模式下记录匹配了多少个关键词

    @property
    def final_score(self) -> float:
        return self.data_score + self.relevance_score


class Category:
    """Article category enum"""
    # Class-level singleton instances (initialized below)
    LOW_FAN_EXPLOSIVE: 'Category'
    TEN_W_READING: 'Category'
    ORIGINAL_RANK: 'Category'
    ONE_W_READING: 'Category'

    def __init__(self, key: str, display: str):
        self.key = key
        self.display = display

    def __repr__(self):
        return f"Category('{self.key}', '{self.display}')"

    def __eq__(self, other):
        if isinstance(other, Category):
            return self.key == other.key
        return False

    @classmethod
    def all(cls) -> List['Category']:
        return [
            cls.LOW_FAN_EXPLOSIVE,
            cls.TEN_W_READING,
            cls.ORIGINAL_RANK,
            cls.ONE_W_READING,
        ]

    @classmethod
    def from_key(cls, key: str) -> Optional['Category']:
        for cat in cls.all():
            if cat.key == key:
                return cat
        return None


# Initialize class-level singletons
Category.LOW_FAN_EXPLOSIVE = Category('low_fan_explosive', '低粉高阅读')
Category.TEN_W_READING = Category('ten_w_reading', '10万+阅读')
Category.ORIGINAL_RANK = Category('original_rank', '原创排行')
Category.ONE_W_READING = Category('one_w_reading', '万阅读')


@dataclass
class TrendingResult:
    """Result of trending articles query"""
    keyword: str
    raw_categories: Dict[str, List]
    scored_articles: List[ScoredArticle] = field(default_factory=list)

    @property
    def total_raw(self) -> int:
        return sum(len(v) for v in self.raw_categories.values())

    @property
    def categories_covered(self) -> int:
        return len(set(a.article.category_key for a in self.scored_articles if a.article.category_key))