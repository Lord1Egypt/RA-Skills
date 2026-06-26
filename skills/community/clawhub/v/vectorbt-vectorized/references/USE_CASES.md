# Known Use Cases (KUC)

Total: **23**

## `KUC-101`
**Source**: `docs/generate_api.py`

Automatically generate API documentation in Markdown format from Python source code to maintain consistent and up-to-date documentation.

## `KUC-102`
**Source**: `docs/update_api_nav.py`

Automatically update the navigation structure in mkdocs.yml based on the actual API documentation files present in the docs directory.

## `KUC-103`
**Source**: `examples/BitcoinDMAC.ipynb`

Execute a daily MACD (Moving Average Convergence Divergence) crossover strategy on Bitcoin to identify buy and sell signals based on momentum.

## `KUC-104`
**Source**: `examples/MACDVolume.ipynb`

Test multiple MACD parameter combinations (fast/slow windows, signal periods) using 3D volume visualization to find optimal momentum indicator settings.

## `KUC-105`
**Source**: `examples/PairsTrading.ipynb`

Implement statistical arbitrage using pairs trading between correlated assets (PEP/KO) based on cointegration and mean reversion principles.

## `KUC-106`
**Source**: `examples/PortfolioOptimization.ipynb`

Optimize portfolio allocation across multiple assets using Modern Portfolio Theory and the Efficient Frontier to maximize risk-adjusted returns.

## `KUC-107`
**Source**: `examples/PortingBTStrategy.ipynb`

Migrate an existing Backtrader trading strategy (RSI-based with moving averages) to vectorbt for faster backtesting and vectorized operations.

## `KUC-108`
**Source**: `examples/StopSignals.ipynb`

Analyze and compare different exit strategies including stop-loss (SL), trailing stop (TS), take-profit (TP), and random exits across multiple crypto assets.

## `KUC-109`
**Source**: `examples/TelegramSignals.ipynb`

Monitor real-time cryptocurrency prices using Bollinger Bands and send trading signals via Telegram when price crosses indicator bands.

## `KUC-110`
**Source**: `examples/TradingSessions.ipynb`

Filter and segment price data by trading sessions (e.g., market hours) to analyze intraday patterns and run strategies on session-specific data.

## `KUC-111`
**Source**: `examples/WalkForwardOptimization.ipynb`

Perform walk-forward analysis to validate trading strategy robustness by testing parameter optimization on rolling in-sample windows against out-of-sample performance.

## `KUC-112`
**Source**: `tests/notebooks/base.ipynb`

Test and validate base data structure operations including column grouping, array wrapping, indexing, reshaping, and combining functions.

## `KUC-113`
**Source**: `tests/notebooks/generic.ipynb`

Test generic data operations like fillna, frequency handling, and time series utilities across various data shapes and configurations.

## `KUC-114`
**Source**: `tests/notebooks/indicators.ipynb`

Test technical indicator implementations including MACD, Bollinger Bands, RSI, and other TA-Lib/ta-based indicators for correctness and performance.

## `KUC-115`
**Source**: `tests/notebooks/labels.ipynb`

Test labeling functions like FMEAN, FSTD, FMIN, FMAX for computing rolling/floating window statistics on financial time series.

## `KUC-116`
**Source**: `tests/notebooks/ohlcv.ipynb`

Test OHLCV (Open-High-Low-Close-Volume) data handling including column naming conventions and plotting functionality for candlestick data.

## `KUC-117`
**Source**: `tests/notebooks/plotting.ipynb`

Test visualization components including gauges, bar plots, scatter plots, and interactive figure updates for financial data visualization.

## `KUC-118`
**Source**: `tests/notebooks/portfolio.ipynb`

Test portfolio simulation functionality including order processing, position sizing, cash management, and performance metrics calculation.

## `KUC-119`
**Source**: `tests/notebooks/records.ipynb`

Test records data structure for storing and manipulating array-based records with custom field types and grouping capabilities.

## `KUC-120`
**Source**: `tests/notebooks/returns.ipynb`

Test returns calculation functionality including percentage changes, annualization, and integration with empyrical for performance metrics.

## `KUC-121`
**Source**: `tests/notebooks/shortcash.ipynb`

Test short selling mechanics and cash value tracking in portfolio simulation including leverage and margin calculations.

## `KUC-122`
**Source**: `tests/notebooks/signals.ipynb`

Test signal generation and manipulation functions including entries, exits, and boolean signal operations for trading strategies.

## `KUC-123`
**Source**: `tests/notebooks/utils.ipynb`

Test utility functions for configuration, checks, decorators, and attributes used throughout the vectorbt framework.
