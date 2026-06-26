"""SEC EDGAR source for SCRY skill."""

from ..source_base import Source, SourceMeta
from .. import http, query, dates
from typing import Any, Dict, List
from urllib.parse import quote_plus


class SECEdgarSource(Source):
    def meta(self) -> SourceMeta:
        return SourceMeta(
            id="sec_edgar",
            display_name="SEC EDGAR",
            tier=1,
            emoji="\U0001f3db\ufe0f",
            id_prefix="SC",
            has_engagement=False,
            requires_keys=[],
            requires_bins=[],
            domains=["finance"],
        )

    def is_available(self, config):
        return True

    def search(self, topic, from_date, to_date, depth, config):
        dc = self.depth_config(depth)
        core = query.extract_core_subject(topic)

        url = (
            f"https://efts.sec.gov/LATEST/search-index"
            f"?q={quote_plus(core)}"
            f"&dateRange=custom"
            f"&startdt={from_date}"
            f"&enddt={to_date}"
            f"&forms=10-K,10-Q,8-K"
        )

        headers = {
            "User-Agent": "scry-skill contact@example.com",
        }

        try:
            data = http.get(url, headers=headers, timeout=dc["timeout"])
        except http.HTTPError:
            return []

        hits = data.get("hits", data.get("filings", []))
        if isinstance(hits, dict):
            hits = hits.get("hits", [])

        items = []
        for hit in hits:
            # Handle nested _source structure or flat structure
            source = hit.get("_source", hit)

            display_names = source.get("display_names", source.get("entity_name", ""))
            if isinstance(display_names, list):
                display_names = ", ".join(display_names)

            form_type = source.get("form_type", "")
            file_date = source.get("file_date", source.get("period_of_report", ""))
            file_num = source.get("file_num", "")

            title = f"{display_names} - {form_type}" if display_names else form_type
            if not title.strip(" -"):
                continue

            # Parse date
            item_date = None
            if file_date:
                dt = dates.parse_date(file_date)
                if dt:
                    item_date = dt.date().isoformat()

            # Construct URL from accession number
            accession = source.get("accession_no", source.get("accession_number", ""))
            if accession:
                # Format: 0000000000-00-000000 -> remove dashes for URL path
                accession_clean = accession.replace("-", "")
                item_url = f"https://www.sec.gov/Archives/edgar/data/{accession_clean[:10]}/{accession_clean}/{accession_clean}.txt"
            else:
                item_url = f"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&company={quote_plus(core)}&type=&dateb=&owner=include&count=10"

            items.append({
                "title": title,
                "url": item_url,
                "date": item_date,
                "relevance": query.compute_relevance(topic, title),
                "engagement": None,
                "snippet": f"Form {form_type} filed by {display_names}" if display_names else f"Form {form_type}",
                "source_id": accession or file_num,
                "extras": {
                    "form_type": form_type,
                    "file_num": file_num,
                    "entity_name": display_names,
                },
            })

            if len(items) >= dc["max_results"]:
                break

        return items


def get_source():
    return SECEdgarSource()
