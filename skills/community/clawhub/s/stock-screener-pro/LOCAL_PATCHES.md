# Local hardening patch

Based on ClawHub release `frontier-ai-vl/stock-screener-pro` version `3.1.1`.

Local version: `3.8.1`.

Changes:

- Fixed sell accounting in `backtest_strategy`: net sale proceeds are added to cash.
- Restricted DSA requests to loopback addresses only; the distributed skill never sends DSA credentials to a remote host.
- Added Tonghuashun iFinD HTTP QuantAPI support for realtime quotes and daily history.
- Fixed the QuantAPI host to `https://quantapi.51ifind.com` so credentials cannot be redirected by configuration.
- Moved Tencent public quote and K-line fallbacks to HTTPS.
- Integrated AI4Trade read APIs and explicitly-confirmed signal, follow, and one-shot heartbeat actions using a fixed API host and environment-only token handling.
- Added `auto`, `ths`, and `tencent` provider modes plus a credential-safe status tool.
- Added regression tests for backtest accounting, DSA URL policy, and Tonghuashun response parsing.
- Compacted the public MCP surface, removed the QLib backend, and retained TradingAgents as the optional multi-agent research backend.
- Updated TradingAgents for its 0.7 configuration API and added a short-lived loopback bridge to the current OpenClaw default model. The bridge passes no Gateway token or upstream provider key to TradingAgents.
- Added Tencent public qfq daily-bar factor research with local caching, explicit caller-supplied universes, one-day signal lag, training-only factor direction, out-of-sample metrics, and random cross-sectional controls; it does not require Tushare or Vibe-Trading.
- Added QuantaAlpha as an opt-in, commit-pinned isolated backend with explicit bootstrap/data setup, OpenClaw default-model bridging, research-only factor mining, and fixed-root custom-factor backtesting. No QuantaAlpha source or dataset is bundled in the Skill.
- Added `score_portfolio`, which maps six QuantaAlpha Alpha158_20 OHLCV factors onto Tencent qfq bars, validates factor direction on training history, reports out-of-sample evidence, and scores holdings only as peer-relative exposure.

Do not overwrite this folder with `openclaw skills update stock-screener-pro` unless the upstream release contains equivalent fixes.
