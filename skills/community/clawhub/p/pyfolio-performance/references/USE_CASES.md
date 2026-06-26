# Known Use Cases (KUC)

Total: **7**

## `KUC-101`
**Source**: `docs/deploy.py`

Automates the build and deployment of Sphinx-generated documentation for the pyfolio library, ensuring consistent documentation deployment across environments.

## `KUC-102`
**Source**: `docs/source/conf.py`

Configures Sphinx documentation build settings including theme, extensions, and project metadata for generating pyfolio library documentation.

## `KUC-103`
**Source**: `src/pyfolio/examples/round_trip_tear_sheet_example.ipynb`

Analyzes individual round trip trades (entry/exit) in a portfolio, computing profitability metrics by trade and sector to understand trading efficiency.

## `KUC-104`
**Source**: `src/pyfolio/examples/sector_mappings_example.ipynb`

Generates position and round trip tear sheets with sector-based profitability analysis, allowing comparison of trading performance across industry sectors.

## `KUC-105`
**Source**: `src/pyfolio/examples/single_stock_example.ipynb`

Downloads historical price data for a single stock and generates a returns tear sheet with in-sample/out-of-sample comparison to evaluate stock performance.

## `KUC-106`
**Source**: `src/pyfolio/examples/slippage_example.ipynb`

Evaluates the impact of transaction slippage on portfolio performance by generating a full tear sheet with slippage modeling, helping understand trading cost implications.

## `KUC-107`
**Source**: `src/pyfolio/examples/zipline_algo_example.ipynb`

Implements and backtests the On-Line Portfolio Moving Average Reversion (OLMAR) algorithm using Zipline, demonstrating mean-reversion portfolio management across multiple stocks.
