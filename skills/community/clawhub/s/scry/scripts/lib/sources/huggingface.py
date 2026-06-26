"""Hugging Face source for SCRY skill."""

from ..source_base import Source, SourceMeta
from .. import http, query, dates
from typing import Any, Dict, List
from urllib.parse import quote_plus


class HuggingFaceSource(Source):
    def meta(self) -> SourceMeta:
        return SourceMeta(
            id="huggingface",
            display_name="Hugging Face",
            tier=2,
            emoji="\U0001f917",
            id_prefix="HF",
            has_engagement=True,
            requires_keys=[],
            requires_bins=[],
            domains=["tech", "science"],
        )

    def is_available(self, config):
        return True

    def search(self, topic, from_date, to_date, depth, config):
        dc = self.depth_config(depth)
        core = query.extract_core_subject(topic)

        items = []

        # Search models
        models_url = (
            f"https://huggingface.co/api/models"
            f"?search={quote_plus(core)}"
            f"&sort=downloads"
            f"&direction=-1"
            f"&limit={min(dc['max_results'], 20)}"
        )

        try:
            models = http.get(models_url, timeout=dc["timeout"])
        except http.HTTPError:
            models = []

        if isinstance(models, list):
            for model in models:
                model_id = model.get("modelId", "") or model.get("id", "")
                if not model_id:
                    continue

                item_url = f"https://huggingface.co/{model_id}"
                pipeline_tag = model.get("pipeline_tag", "")
                tags = model.get("tags", [])

                # Parse date from lastModified
                item_date = None
                last_modified = model.get("lastModified", "")
                if last_modified:
                    dt = dates.parse_date(last_modified)
                    if dt:
                        item_date = dt.date().isoformat()

                title = model_id
                description = pipeline_tag or " ".join(tags[:5])
                relevance = query.compute_relevance(topic, f"{model_id} {description}")

                items.append({
                    "title": f"[Model] {title}",
                    "url": item_url,
                    "date": item_date,
                    "relevance": relevance,
                    "engagement": {
                        "downloads": model.get("downloads", 0),
                        "likes": model.get("likes", 0),
                        "stars": model.get("likes", 0),
                    },
                    "author": model_id.split("/")[0] if "/" in model_id else "",
                    "snippet": description[:300],
                    "source_id": model_id,
                    "tags": tags[:10],
                })

        # Search spaces
        spaces_limit = min(dc["max_results"] // 2, 10)
        spaces_url = (
            f"https://huggingface.co/api/spaces"
            f"?search={quote_plus(core)}"
            f"&sort=likes"
            f"&direction=-1"
            f"&limit={spaces_limit}"
        )

        try:
            spaces = http.get(spaces_url, timeout=dc["timeout"])
        except http.HTTPError:
            spaces = []

        if isinstance(spaces, list):
            for space in spaces:
                space_id = space.get("id", "")
                if not space_id:
                    continue

                item_url = f"https://huggingface.co/spaces/{space_id}"
                tags = space.get("tags", [])
                sdk = space.get("sdk", "")

                # Parse date
                item_date = None
                last_modified = space.get("lastModified", "")
                if last_modified:
                    dt = dates.parse_date(last_modified)
                    if dt:
                        item_date = dt.date().isoformat()

                description = sdk or " ".join(tags[:5])
                relevance = query.compute_relevance(topic, f"{space_id} {description}")

                items.append({
                    "title": f"[Space] {space_id}",
                    "url": item_url,
                    "date": item_date,
                    "relevance": relevance,
                    "engagement": {
                        "downloads": 0,
                        "likes": space.get("likes", 0),
                        "stars": space.get("likes", 0),
                    },
                    "author": space_id.split("/")[0] if "/" in space_id else "",
                    "snippet": description[:300],
                    "source_id": space_id,
                    "tags": tags[:10],
                })

        # Sort combined results by relevance
        items.sort(key=lambda x: x["relevance"], reverse=True)
        return items[:dc["max_results"]]


def get_source():
    return HuggingFaceSource()
