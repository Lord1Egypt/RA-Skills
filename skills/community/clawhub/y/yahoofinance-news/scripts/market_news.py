#!/usr/bin/env python3
"""
market_news.py

Fetch recent Yahoo Finance news for a symbol and print JSON.

Usage:
  python scripts/market_news.py AAPL
  python scripts/market_news.py TSLA --limit 15
  python scripts/market_news.py NVDA --no-cache
"""

from __future__ import annotations

import argparse
import json
import os
import re
import time
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

CACHE_DIR = os.path.join(".cache", "finance-news")
os.makedirs(CACHE_DIR, exist_ok=True)

DEFAULT_TTL_SECONDS = 300
MAX_LIMIT = 50


def _cache_path(key: str) -> str:
	safe = re.sub(r"[^A-Za-z0-9_.-]+", "_", key)
	return os.path.join(CACHE_DIR, f"{safe}.json")


def _cache_get(key: str, ttl_seconds: int) -> Optional[Dict[str, Any]]:
	path = _cache_path(key)
	if not os.path.exists(path):
		return None
	try:
		with open(path, "r", encoding="utf-8") as f:
			payload = json.load(f)
		cached_at = int(payload.get("_cached_at", 0))
		if int(time.time()) - cached_at <= ttl_seconds:
			return payload
	except Exception:
		return None
	return None


def _cache_set(key: str, payload: Dict[str, Any]) -> None:
	payload["_cached_at"] = int(time.time())
	with open(_cache_path(key), "w", encoding="utf-8") as f:
		json.dump(payload, f, ensure_ascii=False, indent=2)


def _to_unix_ts(value: Any) -> Optional[int]:
	if value is None:
		return None

	if isinstance(value, bool):
		return None

	if isinstance(value, int):
		if value > 10**12:
			return int(value / 1000)
		return value

	if isinstance(value, float):
		iv = int(value)
		if iv > 10**12:
			return int(iv / 1000)
		return iv

	if isinstance(value, str):
		s = value.strip()
		if not s:
			return None

		if s.isdigit():
			iv = int(s)
			if iv > 10**12:
				return int(iv / 1000)
			return iv

		try:
			# Accept trailing Z for UTC.
			if s.endswith("Z"):
				s = s[:-1] + "+00:00"
			dt = datetime.fromisoformat(s)
			if dt.tzinfo is None:
				dt = dt.replace(tzinfo=timezone.utc)
			return int(dt.timestamp())
		except ValueError:
			return None

	return None


def _to_utc_string(unix_ts: Optional[int]) -> Optional[str]:
	if unix_ts is None:
		return None
	return datetime.fromtimestamp(unix_ts, tz=timezone.utc).isoformat()


def _first_non_empty(*values: Any) -> Optional[str]:
	for v in values:
		if isinstance(v, str):
			vv = v.strip()
			if vv:
				return vv
	return None


def _extract_link(content: Dict[str, Any], top_level: Dict[str, Any]) -> Optional[str]:
	candidates: List[Any] = [
		content.get("link"),
		content.get("url"),
		top_level.get("link"),
		top_level.get("url"),
	]

	canonical = content.get("canonicalUrl")
	if isinstance(canonical, dict):
		candidates.append(canonical.get("url"))
	elif isinstance(canonical, str):
		candidates.append(canonical)

	click = content.get("clickThroughUrl")
	if isinstance(click, dict):
		candidates.append(click.get("url"))
	elif isinstance(click, str):
		candidates.append(click)

	for c in candidates:
		if isinstance(c, str) and c.strip():
			return c.strip()
	return None


def _normalize_item(raw: Dict[str, Any]) -> Optional[Dict[str, Any]]:
	content = raw.get("content") if isinstance(raw.get("content"), dict) else raw

	title = _first_non_empty(content.get("title"), raw.get("title"))
	if not title:
		return None

	publisher = None
	provider = content.get("provider")
	if isinstance(provider, dict):
		publisher = _first_non_empty(provider.get("displayName"), provider.get("name"))
	if not publisher:
		publisher = _first_non_empty(content.get("publisher"), raw.get("publisher"))

	ts = _to_unix_ts(
		content.get("pubDate")
		or content.get("publishedAt")
		or content.get("providerPublishTime")
		or raw.get("providerPublishTime")
		or raw.get("publishedAt")
	)

	news_url = _extract_link(content, raw)

	item = {
		"id": _first_non_empty(
			str(content.get("id")) if content.get("id") is not None else None,
			str(raw.get("id")) if raw.get("id") is not None else None,
			str(raw.get("uuid")) if raw.get("uuid") is not None else None,
		),
		"title": title,
		"publisher": publisher,
		"published_at_unix": ts,
		"published_at_utc": _to_utc_string(ts),
		# Keep both keys for compatibility; `url` is the canonical field.
		"url": news_url,
		"link": news_url,
		"summary": _first_non_empty(content.get("summary"), content.get("description"), raw.get("summary")),
	}
	return item


def _fetch_news(symbol: str, limit: int) -> List[Dict[str, Any]]:
	import yfinance as yf

	ticker = yf.Ticker(symbol)

	raw_news: List[Dict[str, Any]] = []

	try:
		news_attr = getattr(ticker, "news", None)
		if isinstance(news_attr, list):
			raw_news = news_attr
	except Exception:
		raw_news = []

	if not raw_news:
		get_news = getattr(ticker, "get_news", None)
		if callable(get_news):
			try:
				data = get_news(count=limit, tab="news")
				if isinstance(data, list):
					raw_news = data
			except Exception:
				pass

	# Additional fallback for recent yfinance versions with Search API.
	if not raw_news:
		try:
			search = yf.Search(query=symbol, news_count=limit)
			data = getattr(search, "news", None)
			if isinstance(data, list):
				raw_news = data
		except Exception:
			pass

	normalized: List[Dict[str, Any]] = []
	seen = set()
	for item in raw_news:
		if not isinstance(item, dict):
			continue
		n = _normalize_item(item)
		if not n:
			continue
		dedupe_key = (n.get("id"), n.get("title"), n.get("url") or n.get("link"))
		if dedupe_key in seen:
			continue
		seen.add(dedupe_key)
		normalized.append(n)

	normalized.sort(key=lambda x: x.get("published_at_unix") or 0, reverse=True)
	return normalized[:limit]


def main() -> None:
	parser = argparse.ArgumentParser()
	parser.add_argument("symbol", help="Yahoo Finance symbol, e.g. AAPL, TSLA, ^GSPC")
	parser.add_argument("--limit", type=int, default=10, help=f"Max articles to return (1-{MAX_LIMIT})")
	parser.add_argument("--ttl", type=int, default=DEFAULT_TTL_SECONDS, help="Cache TTL in seconds")
	parser.add_argument("--no-cache", action="store_true", help="Bypass cache for this request")
	args = parser.parse_args()

	symbol = args.symbol.strip().upper()
	limit = max(1, min(MAX_LIMIT, args.limit))
	ttl = max(0, args.ttl)

	cache_key = f"news_{symbol}_{limit}"
	if not args.no_cache and ttl > 0:
		cached = _cache_get(cache_key, ttl)
		if cached:
			cached.pop("_cached_at", None)
			print(json.dumps(cached, ensure_ascii=False, indent=2))
			return

	items = _fetch_news(symbol, limit)

	payload: Dict[str, Any] = {
		"symbol": symbol,
		"source": "Yahoo Finance via yfinance (unofficial; best-effort)",
		"fetched_at_unix": int(time.time()),
		"fetched_at_utc": datetime.now(tz=timezone.utc).isoformat(),
		"count": len(items),
		"items": items,
		"note": "News coverage may be incomplete and can vary by symbol/region.",
	}

	if ttl > 0 and not args.no_cache:
		_cache_set(cache_key, dict(payload))

	print(json.dumps(payload, ensure_ascii=False, indent=2))


if __name__ == "__main__":
	main()
