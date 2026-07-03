"""
trends/scoring.py - Article scoring algorithms
"""

import math
from datetime import datetime
from core.models import TrendingArticle, ScoredArticle, ArticleMetrics
from core import parse_count


def calculate_title_quality(title: str) -> int:
    """
    Calculate title quality score (0-100).
    - Deductions for clickbait keywords (5 points each)
    - Deductions for length issues (<10 or >40 chars)
    """
    if not title:
        return 100

    score = 100
    title = str(title)

    # Clickbait keywords
    clickbait_words = ["震惊", "必看", "绝了", "突发", "紧急", "刚刚", "终于", "沸腾",
                       "惊人", "笑喷", "内幕", "爆料", "曝光", "服了", "哭", "笑死"]
    for word in clickbait_words:
        if word in title:
            score -= 5

    # Title length check
    title_len = len(title)
    if title_len < 10:
        score -= 3
    elif title_len > 40:
        score -= 3

    return max(0, score)


def calculate_relevance_score(article: TrendingArticle, keyword: str) -> tuple:
    """
    Calculate content relevance score (0-15).
    Based on keyword matching with title/summary/content.

    Scoring:
    - Title match: +6 points
    - Summary match: +3 points
    - Content match: +1 points
    - Multiple keywords bonus: +2 each (max +6)

    Returns: (score, matched_keyword_count)
    """
    if not keyword:
        return 0.0, 0

    keywords = [k.strip() for k in keyword.split(',') if k.strip()]
    if not keywords:
        return 0.0, 0

    title_lower = article.title.lower()
    summary_lower = article.summary[:200].lower() if article.summary else ''
    content_lower = ''
    if hasattr(article, 'content') and article.content:
        content_lower = article.content[:500].lower()

    score = 0.0
    matched_keywords = 0

    for kw in keywords:
        kw_lower = kw.lower()
        if kw_lower in title_lower:
            matched_keywords += 1
            score += 6
        elif kw_lower in summary_lower:
            matched_keywords += 1
            score += 3
        elif kw_lower in content_lower:
            matched_keywords += 1
            score += 1

    # Multi-keyword bonus (max +6)
    if matched_keywords > 1:
        score += min(6.0, (matched_keywords - 1) * 2)

    return min(15.0, score), matched_keywords


def calculate_data_score(article: TrendingArticle, cat_key: str, keyword: str = '') -> float:
    """
    Calculate data performance score (0-150).

    Dimensions:
    - Interaction rate (most valuable)
    - Time decay (newer articles weighted higher)
    - Title quality
    - Content relevance
    """
    m = article.metrics
    total_inter = m.like_count + m.comment_count + m.share_count + m.interactive_count

    if total_inter == 0:
        return 0.0

    # Base score
    base_score = (
        math.log10(m.like_count + 1) * 15 +
        math.log10(m.share_count + 1) * 20 +
        math.log10(m.comment_count + 1) * 18 +
        math.log10(m.interactive_count + 1) * 12
    )

    # Clicks bonus
    if m.clicks_count > 0:
        base_score += min(15, math.log10(m.clicks_count + 1) * 3)

    # 1. Interaction rate bonus (0-20)
    if m.clicks_count > 0:
        interaction_rate = total_inter / m.clicks_count
        if interaction_rate > 0.10:
            base_score += 20
        elif interaction_rate > 0.05:
            base_score += 10
        elif interaction_rate > 0.02:
            base_score += 5

    # 2. Time decay
    time_multiplier = 1.0
    pub_time = article.public_time
    if pub_time:
        try:
            article_date = datetime.strptime(pub_time, '%Y-%m-%d')
            days_ago = (datetime.now() - article_date).days
            if days_ago <= 7:
                time_multiplier = 1.2
            elif days_ago <= 15:
                time_multiplier = 1.0
            elif days_ago <= 30:
                time_multiplier = 0.8
            else:
                time_multiplier = 0.7
        except Exception:
            pass

    score = base_score * time_multiplier

    # 3. Title quality (0.9 coefficient)
    title_quality = calculate_title_quality(article.title or article.summary[:30])
    score = score * (title_quality / 100) * 1.0 + (title_quality / 100) * 20

    # 4. Content relevance
    relevance, _ = calculate_relevance_score(article, keyword)
    score += relevance

    # Category bonus
    if cat_key == 'low_fan_explosive':
        if 0 < article.fans < 10000:
            score += 8
        elif article.fans < 50000:
            score += 5

    if cat_key == 'ten_w_reading' and m.clicks_count >= 100000:
        score += 10

    return min(150.0, score)


def score_article(article: TrendingArticle, keyword: str, cat_key: str) -> ScoredArticle:
    """
    Score a single article and return ScoredArticle.
    """
    relevance_score, matched_count = calculate_relevance_score(article, keyword)
    return ScoredArticle(
        article=article,
        data_score=calculate_data_score(article, cat_key, keyword),
        relevance_score=relevance_score,
        title_quality=calculate_title_quality(article.title or ''),
        matched_keyword_count=matched_count
    )