# Known Use Cases (KUC)

Total: **12**

## `KUC-101`
**Source**: `tests/test_utils.py`

Ensures date/timezone parsing and validation utilities work correctly for handling mixed timezone data from financial APIs.

## `KUC-102`
**Source**: `tests/test_screener.py`

Tests the ability to filter and screen stocks based on financial criteria like price thresholds and predefined strategies.

## `KUC-103`
**Source**: `tests/test_search.py`

Allows users to find ticker symbols by searching company names or partial queries, including fuzzy matching for misspellings.

## `KUC-104`
**Source**: `tests/test_calendars.py`

Retrieves upcoming earnings dates and IPO information calendars to help investors track corporate events.

## `KUC-105`
**Source**: `tests/test_prices.py`

Fetches historical price and volume data for securities across multiple intervals (daily, weekly, monthly) and time periods.

## `KUC-106`
**Source**: `tests/test_ticker.py`

Retrieves comprehensive metadata for a ticker including holder information, splits, recommendations, and fundamental data.

## `KUC-107`
**Source**: `tests/test_price_repair.py`

Corrects corrupted or misaligned price data and resamples data between different time intervals while maintaining data integrity.

## `KUC-108`
**Source**: `tests/test_live.py`

Provides real-time cryptocurrency price streaming via WebSocket for trading applications and live market monitoring.

## `KUC-109`
**Source**: `tests/test_cache_noperms.py`

Handles cache storage gracefully when running in restricted environments without write permissions to the filesystem.

## `KUC-110`
**Source**: `tests/test_multi.py`

Downloads price data for multiple tickers concurrently with thread safety, ensuring results don't get mixed between tickers.

## `KUC-111`
**Source**: `tests/test_lookup.py`

Looks up ticker symbols filtered by asset type (stocks, ETFs, mutual funds, indices) to find specific securities.

## `KUC-112`
**Source**: `tests/test_cache.py`

Caches timezone data for securities to reduce API calls and improve performance when fetching data for frequently-used tickers.
