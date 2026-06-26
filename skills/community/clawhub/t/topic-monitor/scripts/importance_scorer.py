#!/usr/bin/env python3
"""
AI-powered importance scoring for research findings.

Scores findings as:
- HIGH: Immediate alert
- MEDIUM: Include in digest
- LOW: Ignore

Also returns a coarse sentiment label for alert rendering and shift tracking.
"""

import re
from typing import Dict, Tuple
from datetime import datetime, timedelta


class ImportanceScorer:
    """Score research findings for importance."""

    SENTIMENT_LABELS = ("positive", "negative", "neutral", "mixed")

    def __init__(self, topic: Dict, settings: Dict):
        self.topic = topic
        self.settings = settings
        self.learning_enabled = settings.get("learning_enabled", False)

    def score(self, result: Dict) -> Tuple[str, float, str, str]:
        """
        Score a result.

        Returns:
            (priority, score, reason, sentiment)
        """
        title = result.get("title", "")
        snippet = result.get("snippet", "")
        url = result.get("url", "")
        published = result.get("published_date", "")
        content = f"{title} {snippet}".lower()

        signals = []
        total_score = 0.0

        keyword_score, keyword_reason = self._score_keywords(content)
        signals.append(("keyword_match", keyword_score, keyword_reason))
        total_score += keyword_score

        freshness_score, freshness_reason = self._score_freshness(published)
        signals.append(("freshness", freshness_score, freshness_reason))
        total_score += freshness_score

        source_score, source_reason = self._score_source(url)
        signals.append(("source_quality", source_score, source_reason))
        total_score += source_score

        condition_score, condition_reason = self._score_conditions(content, title)
        signals.append(("alert_conditions", condition_score, condition_reason))
        total_score += condition_score

        # Clamp into a sane range after penalties.
        total_score = max(0.0, min(1.0, total_score))

        threshold = self.topic.get("importance_threshold", "medium")
        if threshold == "high":
            if total_score >= 0.8:
                priority = "high"
            elif total_score >= 0.5:
                priority = "medium"
            else:
                priority = "low"
        elif threshold == "medium":
            if total_score >= 0.6:
                priority = "high"
            elif total_score >= 0.3:
                priority = "medium"
            else:
                priority = "low"
        else:
            if total_score >= 0.4:
                priority = "high"
            elif total_score >= 0.1:
                priority = "medium"
            else:
                priority = "low"

        top_signals = sorted(signals, key=lambda x: x[1], reverse=True)[:2]
        reason_parts = [s[2] for s in top_signals if s[2]]
        reason = " + ".join(reason_parts) if reason_parts else "low_relevance"
        sentiment = self._score_sentiment(title, snippet)

        return priority, total_score, reason, sentiment

    def _score_keywords(self, content: str) -> Tuple[float, str]:
        keywords = self.topic.get("keywords", [])
        if not keywords:
            return 0.0, ""

        matches = 0
        exact_matches = 0

        for keyword in keywords:
            keyword_lower = keyword.lower().strip()
            if not keyword_lower:
                continue

            if keyword_lower.startswith("-"):
                negative_keyword = keyword_lower[1:]
                if negative_keyword and negative_keyword in content:
                    return 0.0, f"contains_excluded_{negative_keyword}"
                continue

            if re.search(r'\b' + re.escape(keyword_lower) + r'\b', content):
                exact_matches += 1
                matches += 1
            elif keyword_lower in content:
                matches += 1

        if exact_matches >= 2:
            return 0.3, f"exact_match_{exact_matches}_keywords"
        if exact_matches == 1:
            return 0.2, "exact_match_1_keyword"
        if matches >= 2:
            return 0.15, f"partial_match_{matches}_keywords"
        if matches == 1:
            return 0.1, "partial_match_1_keyword"
        return 0.0, "no_keyword_match"

    def _score_freshness(self, published: str) -> Tuple[float, str]:
        if not published:
            return 0.0, ""

        try:
            if "T" in published:
                pub_date = datetime.fromisoformat(published.replace("Z", "+00:00"))
            else:
                pub_date = datetime.strptime(published, "%Y-%m-%d")

            age = datetime.now() - pub_date.replace(tzinfo=None)
            if age < timedelta(hours=6):
                return 0.2, "very_fresh_<6h"
            if age < timedelta(days=1):
                return 0.15, "fresh_<24h"
            if age < timedelta(days=3):
                return 0.1, "recent_<3d"
            return 0.05, "older_>3d"
        except Exception:
            return 0.0, ""

    def _score_source(self, url: str) -> Tuple[float, str]:
        boost_sources = self.topic.get("boost_sources", [])
        for source in boost_sources:
            if source and source in url:
                return 0.2, f"boosted_source_{source}"

        ignore_sources = self.topic.get("ignore_sources", [])
        for source in ignore_sources:
            if source and source in url:
                return -1.0, f"ignored_source_{source}"

        trusted = [
            "github.com",
            "arxiv.org",
            "news.ycombinator.com",
            "techcrunch.com",
            "theverge.com",
            "arstechnica.com",
        ]
        for source in trusted:
            if source in url:
                return 0.15, f"trusted_source_{source}"

        return 0.05, "standard_source"

    def _score_conditions(self, content: str, title: str) -> Tuple[float, str]:
        alert_on = self.topic.get("alert_on", [])

        for condition in alert_on:
            if condition == "price_change_10pct":
                if self._detect_price_change(content, threshold=0.10):
                    return 0.3, "price_change_>10%"
            elif condition == "keyword_exact_match":
                for kw in self.topic.get("keywords", []):
                    if kw and re.search(r'\b' + re.escape(kw.lower()) + r'\b', content):
                        return 0.2, "exact_keyword_in_condition"
            elif condition == "major_paper":
                if "arxiv" in content or "paper" in title.lower():
                    return 0.25, "academic_paper_detected"
            elif condition == "model_release":
                if re.search(r'(release|launch|announce).*\b(model|gpt|llm)\b', content, re.I):
                    return 0.3, "model_release_detected"
            elif condition == "patch_release":
                if re.search(r'(patch|update|version|release).*\d+\.\d+', content, re.I):
                    return 0.25, "patch_release_detected"
            elif condition == "major_bug_fix":
                if re.search(r'(fix|patch|solve).*(critical|major|bug)', content, re.I):
                    return 0.2, "major_bug_fix_detected"
            elif condition == "github_release":
                if "/releases/tag/" in content or "release" in title.lower():
                    return 0.25, "github_release_detected"

        return 0.0, ""

    def _detect_price_change(self, content: str, threshold: float = 0.10) -> bool:
        matches = re.findall(r'(\d+(?:\.\d+)?)\s*%', content)
        for match in matches:
            if float(match) >= threshold * 100:
                return True

        for keyword in ["surge", "plunge", "jump", "drop", "spike", "crash"]:
            if keyword in content:
                return True
        return False

    def _score_sentiment(self, title: str, snippet: str) -> str:
        text = f"{title} {snippet}".lower()
        positive_terms = [
            "launch", "released", "release", "improved", "improvement", "wins",
            "record", "growth", "surge", "upgrade", "success", "stable",
            "available", "general availability", "fast", "faster", "secure",
        ]
        negative_terms = [
            "breach", "incident", "critical", "severe", "failure", "fails",
            "outage", "downtime", "vulnerability", "cve", "warning", "recall",
            "delay", "delayed", "lawsuit", "drop", "crash", "exploit", "bug",
        ]

        pos = sum(1 for term in positive_terms if term in text)
        neg = sum(1 for term in negative_terms if term in text)

        if pos and neg:
            return "mixed"
        if neg > 0:
            return "negative"
        if pos > 0:
            return "positive"
        return "neutral"


def score_result(result: Dict, topic: Dict, settings: Dict) -> Tuple[str, float, str, str]:
    """Convenience function for scoring without creating scorer instance."""
    scorer = ImportanceScorer(topic, settings)
    return scorer.score(result)
