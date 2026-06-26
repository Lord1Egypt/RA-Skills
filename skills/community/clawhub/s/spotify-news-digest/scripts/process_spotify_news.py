#!/usr/bin/env python3
"""
Spotify News Processor
去重、评分、分类，并生成一句话中文总结
"""

import sys
import json
from typing import List, Dict
from difflib import SequenceMatcher
from datetime import datetime, timezone


# ─── 分类标签映射 ───────────────────────────────────────────────
CATEGORY_LABELS = {
    'official': '🎵 官方动态',
    'research': '🔬 技术研究',
    'design': '🎨 产品设计',
    'media': '📰 媒体报道',
    'community': '💬 社区讨论',
    'industry': '🏭 行业资讯',
}

# ─── 一句话中文总结模板（按分类） ──────────────────────────────
# 这些 prompt 提示词用于指引 LLM 生成一句话总结
SUMMARY_HINT = {
    'official': '这是 Spotify 官方发布的内容，请用一句话总结核心信息（产品/功能/公告）',
    'research': '这是 Spotify 工程或研究团队的技术博客，请用一句话总结技术方向或算法亮点',
    'design': '这是 Spotify 设计团队的文章，请用一句话总结设计理念或交互改进点',
    'media': '这是媒体对 Spotify 的报道，请用一句话总结新闻事件',
    'community': '这是 Hacker News 等社区对 Spotify 的讨论，请用一句话总结讨论焦点',
    'industry': '这是音乐行业对 Spotify 的报道，请用一句话总结商业动态',
}


class SpotifyNewsProcessor:
    def __init__(self, similarity_threshold: float = 0.65):
        self.similarity_threshold = similarity_threshold

    def process(self, news_list: List[Dict], max_output: int = 20) -> Dict:
        """去重 → 评分 → 分类"""
        unique = self._deduplicate(news_list)
        print(f"去重后: {len(unique)} 条", file=sys.stderr)

        scored = self._score(unique)
        sorted_news = sorted(scored, key=lambda x: x['final_score'], reverse=True)

        # 按分类归组
        result: Dict[str, List] = {}
        for news in sorted_news[:max_output]:
            cat = news.get('category', 'media')
            result.setdefault(cat, []).append(news)

        return result

    def _deduplicate(self, news_list: List[Dict]) -> List[Dict]:
        unique = []
        for item in news_list:
            dup = False
            for existing in unique:
                sim = SequenceMatcher(
                    None,
                    item['title'].lower(),
                    existing['title'].lower()
                ).ratio()
                if sim > self.similarity_threshold:
                    # 保留分数更高的
                    if item.get('score', 0) > existing.get('score', 0):
                        unique.remove(existing)
                        unique.append(item)
                    dup = True
                    break
            if not dup:
                unique.append(item)
        return unique

    def _score(self, news_list: List[Dict]) -> List[Dict]:
        now = datetime.now(timezone.utc)

        # 来源权重
        source_weight = {
            'Spotify Engineering Blog': 90,
            'Spotify Research': 85,
            'Spotify Newsroom': 80,
            'Spotify Design': 75,
            'TechCrunch Spotify': 60,
            'The Verge Spotify': 55,
            'Hacker News Spotify': 50,
            'Music Business Worldwide': 40,
            'Billboard Music Tech': 35,
        }

        for item in news_list:
            score = 0.0

            # 来源权威性（0–90分）
            score += source_weight.get(item['source'], 30) * 0.4

            # 新鲜度（距截止时间越近越高）
            pub = item.get('published')
            if isinstance(pub, str):
                try:
                    from dateutil import parser as dp
                    pub = dp.parse(pub)
                    if pub.tzinfo is None:
                        pub = pub.replace(tzinfo=timezone.utc)
                except Exception:
                    pub = now
            elif pub is None:
                pub = now

            hours_ago = max(0, (now - pub).total_seconds() / 3600)
            freshness = max(0.0, 100.0 - hours_ago * 4)  # 24h 内满分
            score += freshness * 0.4

            # HN 热度分
            score += min(item.get('score', 0), 100) * 0.2

            item['final_score'] = round(score, 2)

        return news_list


def format_digest(result: Dict, date_str: str = None) -> str:
    """
    将处理结果格式化为企业微信可读的 Markdown 文本。
    每条新闻输出：
      分类标题
      · [一句话中文总结]（source）
        🔗 原文链接
    """
    if date_str is None:
        date_str = datetime.now().strftime('%Y-%m-%d')

    total = sum(len(v) for v in result.values())
    lines = [
        f"🎵 **Spotify 新闻日报 · {date_str}**",
        f"共 {total} 条（去重后）",
        "─────────────────────────────",
    ]

    # 固定分类显示顺序
    display_order = ['official', 'research', 'design', 'media', 'community', 'industry']
    for cat in display_order:
        items = result.get(cat, [])
        if not items:
            continue
        label = CATEGORY_LABELS.get(cat, cat)
        lines.append(f"\n{label}（{len(items)} 条）")
        for item in items:
            # 一句话总结：优先用 summary，否则用标题
            zh_summary = item.get('zh_summary', '')
            if not zh_summary:
                # 直接用英文标题，调用方（LLM）应在渲染时生成中文总结
                # 这里先用 [待翻译] 标记，SKILL.md 说明由 LLM 处理
                zh_summary = f"[{item['title']}]"
            source = item.get('source', '')
            url = item.get('url', '')
            lines.append(f"· {zh_summary}（{source}）")
            if url:
                lines.append(f"  🔗 {url}")

    lines.append("\n─────────────────────────────")
    lines.append("🤖 由 OpenClaw · spotify-news-digest 自动生成")
    return "\n".join(lines)


if __name__ == '__main__':
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument('--input', required=True)
    p.add_argument('--output', default=None)
    p.add_argument('--max', type=int, default=20)
    args = p.parse_args()

    with open(args.input, 'r', encoding='utf-8') as f:
        raw = json.load(f)

    processor = SpotifyNewsProcessor()
    result = processor.process(raw, max_output=args.max)

    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2, default=str)
        print(f"已保存到 {args.output}")
    else:
        for cat, items in result.items():
            print(f"\n== {cat} ({len(items)}) ==")
            for a in items:
                print(f"  [{a['source']}] {a['title']}")
                print(f"  分数: {a['final_score']}  🔗 {a['url']}")
