"""Threads source for SCRY skill (stub)."""

from ..source_base import Source, SourceMeta
from .. import http, query, dates
from typing import Any, Dict, List


class ThreadsSource(Source):
    def meta(self) -> SourceMeta:
        return SourceMeta(
            id="threads",
            display_name="Threads",
            tier=2,
            emoji="\U0001f9f5",
            id_prefix="TH",
            has_engagement=True,
            requires_keys=["THREADS_ACCESS_TOKEN"],
            requires_bins=[],
            domains=["general"],
        )

    def is_available(self, config):
        return bool(config.get("THREADS_ACCESS_TOKEN"))

    def search(self, topic, from_date, to_date, depth, config):
        # Stub: Threads API integration pending.
        # When Meta's Threads API supports public search, implement here.
        dc = self.depth_config(depth)
        core = query.extract_core_subject(topic)
        items = []
        return items


def get_source():
    return ThreadsSource()
