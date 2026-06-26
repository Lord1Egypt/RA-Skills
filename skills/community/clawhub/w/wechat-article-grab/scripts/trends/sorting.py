"""
trends/sorting.py - Article sorting and diversity logic
"""

from typing import List
from core.models import TrendingArticle, ScoredArticle


def merge_and_sort(
    articles: List[TrendingArticle],
    keyword: str = '',
    max_items: int = 10
) -> List[ScoredArticle]:
    """
    Merge articles from all categories, deduplicate, score and sort.

    Steps:
    1. Merge all category articles into candidate pool
    2. Deduplicate by photoId
    3. Score each article
    4. Global sort by score (relevance articles first)
    5. Ensure category diversity
    """
    from trends.scoring import score_article

    # Deduplicate by photoId
    seen = set()
    deduped = []
    for article in articles:
        photo_id = article.photo_id
        if photo_id and photo_id not in seen:
            seen.add(photo_id)
            deduped.append(article)

    # Score each article
    scored = []
    for article in deduped:
        s = score_article(article, keyword, article.category_key)
        scored.append(s)

    # Sort: relevance > score (descending)
    scored.sort(key=lambda x: (
        1 if x.relevance_score > 0 else 0,
        x.final_score
    ), reverse=True)

    # Ensure diversity
    return ensure_category_diversity(scored, max_items)


def ensure_category_diversity(
    scored: List[ScoredArticle],
    max_items: int = 10,
    min_categories: int = 3
) -> List[ScoredArticle]:
    """
    Ensure category diversity in results.

    Rules:
    - Must cover >= min_categories categories
    - If only 1 category, supplement from others
    - Prioritize higher scored content
    """
    if not scored:
        return []

    # Count categories
    cat_counts = {}
    for s in scored:
        cat_key = s.article.category_key
        if cat_key:
            cat_counts[cat_key] = cat_counts.get(cat_key, 0) + 1

    # If only 1 category and no others, return as-is
    if len(cat_counts) == 1:
        only_cat = list(cat_counts.keys())[0]
        other_cat_items = [s for s in scored if s.article.category_key != only_cat]
        if not other_cat_items:
            return scored[:max_items]

    # Group by category
    cat_items = {}
    for s in scored:
        cat_key = s.article.category_key
        if cat_key not in cat_items:
            cat_items[cat_key] = []
        cat_items[cat_key].append(s)

    # Round-robin selection
    result = []
    used_indices = {cat_key: 0 for cat_key in cat_items}

    # Sort categories by their top score
    sorted_cats = sorted(
        cat_items.keys(),
        key=lambda k: cat_items[k][0].final_score if cat_items[k] else 0,
        reverse=True
    )

    while len(result) < max_items:
        added = False
        for cat_key in sorted_cats:
            if used_indices[cat_key] < len(cat_items[cat_key]):
                result.append(cat_items[cat_key][used_indices[cat_key]])
                used_indices[cat_key] += 1
                added = True
                if len(result) >= max_items:
                    break
        if not added:
            break

    # Re-sort by final score
    result.sort(key=lambda x: x.final_score, reverse=True)

    return result