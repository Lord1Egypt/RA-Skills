from __future__ import annotations

import hashlib
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from render import build_markdown_digest, build_xhs_post, now_labels, write_json, write_text
from scoring import score_comment, score_post
from xhs_client import XHSClient


@dataclass
class PipelineResult:
    digest_markdown_path: Path
    digest_json_path: Path
    post_draft_path: Path
    publish_result_path: Path | None
    ranked_posts: list[dict[str, Any]]
    post_payload: dict[str, str]


class DailyPipeline:
    def __init__(self, project_root: Path, topic_key: str, topic_config: dict[str, Any]) -> None:
        self.project_root = project_root
        self.topic_key = topic_key
        self.topic_config = topic_config
        self.client = XHSClient()

    def run(self, publish: bool = False) -> PipelineResult:
        date_folder, date_label = now_labels()
        base_dir = self.project_root / 'data' / self.topic_key / date_folder
        raw_dir = base_dir / 'raw'
        processed_dir = base_dir / 'processed'
        search_rows = self._collect_search_results(raw_dir)
        ranked_posts = self._rank_and_enrich(search_rows, processed_dir)
        digest_markdown_path = processed_dir / 'digest.md'
        write_text(digest_markdown_path, build_markdown_digest(self.topic_config['display_name'], date_label, ranked_posts))
        digest_json_path = processed_dir / 'digest.json'
        write_json(digest_json_path, ranked_posts)
        post_payload = build_xhs_post(self.topic_config['display_name'], self.topic_config, date_label, ranked_posts)
        post_draft_path = processed_dir / 'post_draft.json'
        write_json(post_draft_path, post_payload)
        publish_result_path = None
        if publish:
            publish_result = self.client.publish_content(post_payload['title'], post_payload['content'], [self.topic_config['default_cover_image']])
            publish_result_path = processed_dir / 'publish_result.txt'
            write_text(publish_result_path, publish_result)
        return PipelineResult(digest_markdown_path, digest_json_path, post_draft_path, publish_result_path, ranked_posts, post_payload)

    def _collect_search_results(self, raw_dir: Path) -> list[dict[str, Any]]:
        seen_ids: set[str] = set()
        collected: list[dict[str, Any]] = []
        for keyword in self.topic_config['keywords']:
            result = self.client.search_feeds(keyword)
            write_json(raw_dir / f"search-{self._slug(keyword)}.json", result)
            feeds = result.get('feeds', [])[: self.topic_config['max_search_results_per_keyword']]
            for feed in feeds:
                feed_id = str(feed.get('id') or '')
                if not feed_id or feed_id in seen_ids:
                    continue
                seen_ids.add(feed_id)
                collected.append(feed)
        return collected

    def _rank_and_enrich(self, posts: list[dict[str, Any]], processed_dir: Path) -> list[dict[str, Any]]:
        scored = [{'post': post, 'score': score_post(post)} for post in posts]
        scored.sort(key=lambda item: item['score'], reverse=True)
        ranked: list[dict[str, Any]] = []
        for index, item in enumerate(scored[: self.topic_config['max_posts_for_detail']]):
            post = item['post']
            feed_id = post.get('id')
            xsec = post.get('xsecToken')
            detail = {}
            if index == 0 and feed_id and xsec:
                try:
                    detail = self.client.get_feed_detail(str(feed_id), str(xsec), load_all_comments=False, limit=self.topic_config['max_comment_preview'])
                except Exception as exc:
                    detail = {'error': str(exc)}
            ranked.append({
                'score': item['score'],
                'post': post,
                'detail': detail,
                'summary': self._summarize_post(post, detail),
                'top_comments': self._select_comments(detail),
            })
        ranked.sort(key=lambda row: row['score'], reverse=True)
        ranked = ranked[: self.topic_config['max_digest_items']]
        write_json(processed_dir / 'ranked_posts_full.json', ranked)
        return ranked

    def _summarize_post(self, post: dict[str, Any], detail: dict[str, Any]) -> str:
        card = post.get('noteCard', {})
        detail_note = ((detail.get('data') or {}).get('note') or {}) if isinstance(detail.get('data'), dict) else {}
        title = detail_note.get('title') or card.get('displayTitle') or ''
        body = detail_note.get('desc') or detail.get('content') or detail.get('desc') or card.get('desc') or post.get('content') or ''
        text = ' '.join(f'{title} {body}'.strip().split())
        if not text:
            return '这条内容信息量有限，但在关键词搜索结果里有一定相关性。'
        cleaned = text.replace('#', ' ').replace('[话题]', ' ').replace('http://', ' ').replace('https://', ' ')
        return cleaned[:220] + ('…' if len(cleaned) > 220 else '')

    def _select_comments(self, detail: dict[str, Any]) -> list[str]:
        comment_candidates: list[tuple[float, str]] = []
        data = detail.get('data') if isinstance(detail.get('data'), dict) else {}
        sources = []
        if isinstance(detail.get('comments'), list):
            sources.append(detail.get('comments'))
        if isinstance(detail.get('commentList'), list):
            sources.append(detail.get('commentList'))
        if isinstance(data.get('comments'), list):
            sources.append(data.get('comments'))
        for rows in sources:
            for row in rows:
                if not isinstance(row, dict):
                    continue
                text = row.get('content') or row.get('comment') or row.get('text')
                if not text:
                    continue
                score = score_comment(row)
                if score > 0:
                    comment_candidates.append((score, str(text).strip()))
        comment_candidates.sort(key=lambda item: item[0], reverse=True)
        return [text for _, text in comment_candidates[:3]]

    @staticmethod
    def _slug(value: str) -> str:
        return hashlib.md5(value.encode('utf-8')).hexdigest()[:10]
