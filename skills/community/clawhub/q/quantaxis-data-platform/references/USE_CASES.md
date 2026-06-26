# Known Use Cases (KUC)

Total: **8**

## `KUC-101`
**Source**: `examples/factoranalysis.py`

Computes and stores a 5-day moving average (MA5) factor for daily stock data, enabling technical indicator analysis across multiple stocks using ClickHouse database storage.

## `KUC-102`
**Source**: `examples/featureanalysis.ipynb`

Retrieves pre-computed MA5 factor data from ClickHouse and generates comprehensive tear sheets for factor performance analysis and visualization in research environments.

## `KUC-103`
**Source**: `examples/qadatabridge_example.py`

Demonstrates efficient zero-copy conversion between Pandas and Polars dataframes, and shared memory-based cross-process data transmission for high-performance data pipelines.

## `KUC-104`
**Source**: `examples/qarsbridge_example.py`

Provides a bridge interface to QARS2 Rust-powered backend components for high-performance account management, trading operations, and backtesting with 100x account and 10x backtest speed improvements.

## `KUC-105`
**Source**: `examples/qifiaccountexample.py`

Simulates trading account operations including order placement, trade execution, and daily settlement for backtesting trading strategies with persistent account state management.

## `KUC-106`
**Source**: `examples/resource_manager_example.py`

Provides unified context manager-based resource management for MongoDB, RabbitMQ, ClickHouse, and Redis connections with automatic connection handling and exception safety.

## `KUC-107`
**Source**: `examples/scheduleserver.py`

Implements a web-based task scheduler allowing users to add, query, and manage periodic or cron-based jobs through HTTP endpoints for automated trading task execution.

## `KUC-108`
**Source**: `examples/test_ckread_qifi.py`

Provides direct SQL query access to QIFI trading data stored in ClickHouse, enabling retrieval of account information, orders, trades, and positions for analysis.
