"""CoinGecko source for SCRY skill."""

from ..source_base import Source, SourceMeta
from .. import http, query, dates
from typing import Any, Dict, List
from urllib.parse import quote_plus


class CoinGeckoSource(Source):
    def meta(self) -> SourceMeta:
        return SourceMeta(
            id="coingecko",
            display_name="CoinGecko",
            tier=1,
            emoji="\U0001fa99",
            id_prefix="CG",
            has_engagement=True,
            requires_keys=[],
            requires_bins=[],
            domains=["crypto", "finance"],
        )

    def is_available(self, config):
        return True

    def search(self, topic, from_date, to_date, depth, config):
        dc = self.depth_config(depth)
        core = query.extract_core_subject(topic)

        # Step 1: Search for coins
        search_url = f"https://api.coingecko.com/api/v3/search?query={quote_plus(core)}"

        try:
            search_data = http.get(search_url, timeout=dc["timeout"])
        except http.HTTPError:
            return []

        coins = search_data.get("coins", [])
        if not coins:
            return []

        # Limit to top results based on depth
        max_detail = min(dc["max_results"], len(coins), 10)
        top_coins = coins[:max_detail]

        items = []
        for coin in top_coins:
            coin_id = coin.get("id", "")
            name = coin.get("name", "")
            symbol = coin.get("symbol", "")

            if not coin_id or not name:
                continue

            title = f"{name} ({symbol.upper()})" if symbol else name
            item_url = f"https://www.coingecko.com/en/coins/{coin_id}"

            # Step 2: Fetch detail for each coin
            detail_url = (
                f"https://api.coingecko.com/api/v3/coins/{coin_id}"
                f"?localization=false"
                f"&tickers=false"
                f"&community_data=false"
                f"&developer_data=false"
            )

            try:
                detail = http.get(detail_url, timeout=dc["timeout"])
            except http.HTTPError:
                # Still add the coin with basic info from search
                items.append({
                    "title": title,
                    "url": item_url,
                    "date": None,
                    "relevance": query.compute_relevance(topic, title),
                    "engagement": None,
                    "snippet": f"Cryptocurrency: {title}",
                    "source_id": coin_id,
                })
                continue

            market_data = detail.get("market_data", {})

            # Extract engagement metrics
            total_volume_usd = 0
            total_volume = market_data.get("total_volume", {})
            if isinstance(total_volume, dict):
                total_volume_usd = total_volume.get("usd", 0) or 0

            market_cap_rank = detail.get("market_cap_rank") or 9999
            # Invert rank: lower rank = higher score (max 10000)
            inverted_score = max(0, 10000 - market_cap_rank)

            # Price changes
            price_change_24h = market_data.get("price_change_percentage_24h") or 0
            price_change_7d = market_data.get("price_change_percentage_7d") or 0

            market_cap_usd = 0
            market_cap = market_data.get("market_cap", {})
            if isinstance(market_cap, dict):
                market_cap_usd = market_cap.get("usd", 0) or 0

            # Last updated as date
            last_updated = detail.get("last_updated", "")
            item_date = None
            if last_updated:
                dt = dates.parse_date(last_updated)
                if dt:
                    item_date = dt.date().isoformat()

            description_text = ""
            desc = detail.get("description", {})
            if isinstance(desc, dict):
                description_text = desc.get("en", "")
            if description_text:
                import re
                description_text = re.sub(r"<[^>]+>", "", description_text).strip()[:500]

            items.append({
                "title": title,
                "url": item_url,
                "date": item_date,
                "relevance": query.compute_relevance(topic, title),
                "engagement": {
                    "volume": total_volume_usd,
                    "score": inverted_score,
                },
                "snippet": description_text or f"Cryptocurrency: {title}",
                "source_id": coin_id,
                "extras": {
                    "price_change_24h": price_change_24h,
                    "price_change_7d": price_change_7d,
                    "market_cap": market_cap_usd,
                },
            })

        return items


def get_source():
    return CoinGeckoSource()
