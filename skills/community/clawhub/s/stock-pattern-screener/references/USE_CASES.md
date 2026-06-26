# Known Use Cases (KUC)

Total: **30**

## `KUC-001`
**Source**: `backend/app/main.py`

Provides the main FastAPI application entry point with CORS middleware, dependency injection wiring, and runtime service initialization for the Hermes Market Copilot backend.

## `KUC-002`
**Source**: `xui-reader/src/xui_reader/cli.py`

Provides a Typer-based CLI for authenticating with X (Twitter), managing browser sessions, and collecting social media data for theme discovery and sentiment analysis.

## `KUC-003`
**Source**: `backend/scripts/run_legacy_runtime_migrations.py`

Runs pre-Alembic schema reconciliation steps exactly once to migrate legacy runtime data structures to the current schema.

## `KUC-004`
**Source**: `backend/app/use_cases/scanning/run_bulk_scan.py`

Orchestrates the full bulk scan execution lifecycle including checkpoint-based resume support, chunk processing, progress reporting, and cancellation handling.

## `KUC-005`
**Source**: `backend/app/services/server_auth.py`

Provides single-user server authentication helpers including token encoding, decoding, expiration checking, and HMAC signature validation for securing API endpoints.

## `KUC-006`
**Source**: `backend/app/interfaces/mcp/server.py`

Provides a minimal stdio MCP (Model Context Protocol) server for integrating the Hermes Market Copilot with external AI agents via JSON-RPC messaging.

## `KUC-007`
**Source**: `backend/tests/unit/test_universe_resolver_asia_indices.py`

Resolves index-based universes (HSI, NIKKEI225, TAIEX) to constituent symbols for targeted Asian market scanning.

## `KUC-008`
**Source**: `backend/tests/unit/test_watchlist_import_service.py`

Parses and deduplicates symbols from text, CSV, or tab-delimited watchlist imports for stock screening.

## `KUC-009`
**Source**: `backend/tests/unit/test_market_hours.py`

Provides utilities for detecting trading days, checking market open/close times, and managing NYSE calendar integration across US and Asian markets.

## `KUC-010`
**Source**: `backend/tests/unit/test_minervini_scanner.py`

Implements the Minervini trend template screening strategy for identifying growth stocks in strong uptrends with market cap, price, and volume criteria.

## `KUC-011`
**Source**: `backend/tests/unit/test_canslim_scanner.py`

Implements the CANSLIM screening strategy combining current earnings, annual earnings, new products/management, supply/demand, market direction, and leader/laggard analysis.

## `KUC-012`
**Source**: `backend/tests/unit/test_ipo_scanner.py`

Screens for stocks with recent IPO dates that meet Minervini/CANSLIM criteria, identifying early-stage companies with growth potential.

## `KUC-013`
**Source**: `backend/tests/unit/test_custom_scanner.py`

Provides a configurable stock screener with custom filters for price, volume, RS rating, market cap, debt, sector, EPS/sales growth, and technical criteria.

## `KUC-014`
**Source**: `backend/tests/unit/test_setup_engine_screener.py`

Detects chart patterns (VCP, Cup-with-Handle, NR7, etc.) using normalized scoring and cross-detector calibration for trade setup quality assessment.

## `KUC-015`
**Source**: `backend/tests/unit/test_breadth_calculator.py`

Calculates market breadth metrics including the percentage of stocks above their moving averages to assess overall market health and participation.

## `KUC-016`
**Source**: `backend/tests/unit/test_scan_result_query_builder.py`

Builds and executes filtered, sorted, paginated queries on scan results with support for JSON field extraction and complex filter conditions.

## `KUC-017`
**Source**: `backend/tests/unit/test_quality_policy_scoring.py`

Applies quality-aware fallback policy to stock ratings based on data completeness, excluding low-quality signals and downgrading partial data.

## `KUC-018`
**Source**: `backend/tests/unit/test_validation_service.py`

Validates scan predictions against actual price outcomes, tracking win rates and accuracy across different time horizons (20, 50, 100 days).

## `KUC-019`
**Source**: `backend/tests/unit/test_stock_universe_service_index_membership.py`

Manages stock universe membership including active/inactive status, index constituents (SP500, HSI, NIKKEI225, TAIEX), and market/exchange categorization.

## `KUC-020`
**Source**: `backend/tests/unit/test_assistant_gateway_service.py`

Bridges Hermes AI assistant requests to backend services, handling conversation management, tool routing, and MCP watchlist writes.

## `KUC-021`
**Source**: `backend/tests/unit/test_theme_discovery_ingestion_tasks.py`

Ingests content from various sources (Twitter, Substack, news) for theme discovery, tracking content items and error states during extraction.

## `KUC-022`
**Source**: `backend/tests/unit/test_setup_engine_feature_flag.py`

Controls setup engine inclusion in scan orchestrator via feature flag, allowing silent filtering when disabled without breaking existing workflows.

## `KUC-023`
**Source**: `backend/tests/unit/test_hybrid_fundamentals_service.py`

Fetches fundamentals from multiple providers (yfinance, finviz) with market-aware routing policy, caching, and FX normalization for international stocks.

## `KUC-024`
**Source**: `backend/tests/unit/test_breadth_tasks.py`

Orchestrates daily breadth calculation tasks with warmup checks, refusing to publish when price cache warmup is incomplete.

## `KUC-025`
**Source**: `backend/tests/unit/test_pattern_calibration.py`

Normalizes scores across multiple pattern detectors using cross-detector calibration to ensure consistent quality and readiness scoring.

## `KUC-026`
**Source**: `backend/tests/unit/test_multilingual_qa_harness.py`

Validates multilingual text extraction pipeline (CJK alias resolution, language detection, ticker normalization) against golden corpora with precision/recall gates.

## `KUC-027`
**Source**: `backend/tests/unit/test_mcp_market_copilot.py`

Provides MCP tools for stock snapshots, scan results, breadth data, and watchlist management accessible to external AI agents via JSON-RPC.

## `KUC-028`
**Source**: `backend/tests/unit/test_custom_scanner_mixed_market.py`

Applies market-aware filtering policies for multi-market scans, using USD-normalized criteria when scanning across US, HK, JP, and TW markets.

## `KUC-029`
**Source**: `backend/tests/unit/test_universe_compat_adapter.py`

Adapts legacy universe request formats to typed UniverseDefinition with deprecation headers for gradual migration from old API style.

## `KUC-030`
**Source**: `backend/tests/unit/test_theme_content_recovery_logic.py`

Detects and recovers from theme content corruption by resetting storage and recreating data immediately after schema rewind.
