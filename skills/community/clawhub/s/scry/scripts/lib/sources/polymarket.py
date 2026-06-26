"""Polymarket source for SCRY skill."""

from ..source_base import Source, SourceMeta
from .. import http, query, dates
from typing import Any, Dict, List
from urllib.parse import quote_plus


class PolymarketSource(Source):
    def meta(self) -> SourceMeta:
        return SourceMeta(
            id="polymarket",
            display_name="Polymarket",
            tier=1,
            emoji="\U0001f4ca",
            id_prefix="PM",
            has_engagement=True,
            requires_keys=[],
            requires_bins=[],
            domains=["finance", "politics", "news"],
        )

    def is_available(self, config):
        return True

    def search(self, topic, from_date, to_date, depth, config):
        dc = self.depth_config(depth)
        core = query.extract_core_subject(topic)

        limit = min(dc["max_results"], 50)
        url = (
            f"https://gamma-api.polymarket.com/public-search"
            f"?query={quote_plus(core)}"
            f"&limit={limit}"
        )

        try:
            data = http.get(url, timeout=dc["timeout"])
        except http.HTTPError:
            return []

        # Response may be a list of events or have an "events" key
        if isinstance(data, list):
            events = data
        else:
            events = data.get("events", data.get("data", []))

        items = []
        for event in events:
            title = event.get("title", "")
            if not title:
                continue

            slug = event.get("slug", "")
            event_id = event.get("id", "")
            item_url = f"https://polymarket.com/event/{slug}" if slug else ""

            # Parse dates
            start_date = event.get("startDate", "")
            end_date_str = event.get("endDate", "")
            item_date = None
            if start_date:
                dt = dates.parse_date(start_date)
                if dt:
                    item_date = dt.date().isoformat()

            # Aggregate market data
            markets = event.get("markets", [])
            total_volume = 0
            total_liquidity = 0
            outcome_parts = []
            first_question = ""

            for market in markets:
                # Sum volumes
                try:
                    vol = float(market.get("volume", 0) or 0)
                    total_volume += vol
                except (ValueError, TypeError):
                    pass

                try:
                    liq = float(market.get("liquidity", 0) or 0)
                    total_liquidity += liq
                except (ValueError, TypeError):
                    pass

                # Capture first market question
                if not first_question:
                    first_question = market.get("question", "")

                # Format outcome prices
                outcome_prices = market.get("outcomePrices", "")
                outcomes = market.get("outcomes", [])
                if outcome_prices and outcomes:
                    try:
                        if isinstance(outcome_prices, str):
                            import json
                            prices = json.loads(outcome_prices)
                        else:
                            prices = outcome_prices
                        for i, outcome in enumerate(outcomes):
                            if i < len(prices):
                                try:
                                    pct = float(prices[i]) * 100
                                    outcome_parts.append(f"{outcome}: {pct:.0f}%")
                                except (ValueError, TypeError):
                                    pass
                    except (json.JSONDecodeError, TypeError):
                        pass

            items.append({
                "title": title,
                "url": item_url,
                "date": item_date,
                "relevance": query.compute_relevance(topic, title),
                "engagement": {
                    "volume": total_volume,
                    "liquidity": total_liquidity,
                },
                "snippet": first_question or title,
                "source_id": str(event_id),
                "extras": {
                    "outcome_prices": "; ".join(outcome_parts) if outcome_parts else "",
                    "question": first_question,
                },
            })

        return items


def get_source():
    return PolymarketSource()
