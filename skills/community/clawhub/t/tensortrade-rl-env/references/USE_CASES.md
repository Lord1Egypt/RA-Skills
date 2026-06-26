# Known Use Cases (KUC)

Total: **19**

## `KUC-101`
**Source**: `docs/source/conf.py`

Infrastructure configuration for building TensorTrade documentation using Sphinx. Not a trading or ML use case.

## `KUC-102`
**Source**: `examples/ledger_example.ipynb`

Demonstrates how to set up a portfolio with wallets across multiple exchanges (Bitfinex, Bitstamp) and different trading pairs for simulated trading.

## `KUC-103`
**Source**: `examples/renderers_and_plotly_chart.ipynb`

Visualizes historical price data with technical analysis indicators on interactive Plotly charts for trading analysis and reporting.

## `KUC-104`
**Source**: `examples/setup_environment_tutorial.ipynb`

Tutorial demonstrating how to set up TensorTrade environment including data feeds, exchanges, and wallets for cryptocurrency trading research.

## `KUC-105`
**Source**: `examples/train_and_evaluate.ipynb`

End-to-end workflow for training reinforcement learning agents to trade cryptocurrency and evaluating their performance on test data.

## `KUC-106`
**Source**: `examples/training/run_ray_simulation.py`

Runs Ray RLlib PPO training simulations for cryptocurrency trading using custom RSI and MACD indicators as features.

## `KUC-107`
**Source**: `examples/training/train_advanced.py`

Trains trading agents using AdvancedPBR reward combining position-based returns, trading penalties, and hold bonuses to generate actual profits.

## `KUC-108`
**Source**: `examples/training/train_best.py`

Uses the best-performing configuration combining PBR reward and Optuna-optimized hyperparameters with zero commission for maximum agent skill isolation.

## `KUC-109`
**Source**: `examples/training/train_historical.py`

Trains RL agents on each available historical BTC data with technical indicators, then evaluates on recent market prices to assess generalization.

## `KUC-110`
**Source**: `examples/training/train_optuna.py`

Runs hyperparameter optimization trials using Optuna + Ray RLlib to find the best trading agent configuration based on validation performance.

## `KUC-111`
**Source**: `examples/training/train_profit.py`

Profit-focused strategy that trains on bear market data with simple trend-following features and risk-adjusted returns (Sharpe ratio) optimization.

## `KUC-112`
**Source**: `examples/training/train_ray_long.py`

Long-running (5-10 min) Ray RLlib training with custom callbacks that track wallet/portfolio net worth at episode boundaries for performance monitoring.

## `KUC-113`
**Source**: `examples/training/train_robust.py`

Robust training approach using normalized/scale-invariant features, higher exploration entropy, early stopping, noise injection, and simpler networks to prevent overfitting.

## `KUC-114`
**Source**: `examples/training/train_simple.py`

Simple demonstration showing how to train a trading agent with actual wallet balances and trade execution visibility for educational purposes.

## `KUC-115`
**Source**: `examples/training/train_trend.py`

Simple trend-following strategy using only 5 trend indicators and a tiny (32x32) neural network to learn basic market entry/exit signals, avoiding complex overfitting.

## `KUC-116`
**Source**: `examples/training/train_walkforward.py`

Walk-forward training that uses rolling windows across multiple market regimes (bull, bear, sideways) with incremental learning and checkpointing for robust strategy development.

## `KUC-117`
**Source**: `examples/use_attentionnet_rllib.ipynb`

Uses attention mechanisms in LSTM networks for RLlib-based cryptocurrency trading, allowing the model to focus on relevant historical price patterns.

## `KUC-118`
**Source**: `examples/use_lstm_rllib.ipynb`

LSTM recurrent neural network for cryptocurrency trading using custom RSI and MACD technical indicators as features with Ray RLlib.

## `KUC-119`
**Source**: `examples/use_stochastic_data.ipynb`

Generates synthetic financial data using stochastic processes (GBM, Heston, FBM, Cox) for testing trading strategies without requiring real market data.
