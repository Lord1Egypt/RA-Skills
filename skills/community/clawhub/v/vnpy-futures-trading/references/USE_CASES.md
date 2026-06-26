# Known Use Cases (KUC)

Total: **21**

## `KUC-101`
**Source**: `examples/alpha_research/download_data_rq.ipynb`

Download historical CSI300 index constituent stock data from RQData data service for use in alpha factor research and backtesting.

## `KUC-102`
**Source**: `examples/alpha_research/download_data_xt.ipynb`

Download historical CSI300 index constituent stock data from XTQuant data service for use in alpha factor research.

## `KUC-103`
**Source**: `examples/alpha_research/research_workflow_alpha101.ipynb`

Conduct alpha factor research using the Alpha101 factor library to discover predictive signals in CSI300 constituent stocks.

## `KUC-104`
**Source**: `examples/alpha_research/research_workflow_lasso.ipynb`

Develop and test alpha factors using Lasso regression with Alpha158 dataset for feature selection and regularization in stock prediction.

## `KUC-105`
**Source**: `examples/alpha_research/research_workflow_lgb.ipynb`

Build and evaluate alpha factors using LightGBM gradient boosting with Alpha158 dataset for stock return prediction.

## `KUC-106`
**Source**: `examples/alpha_research/research_workflow_mlp.ipynb`

Develop and test alpha factors using multi-layer perceptron neural network with Alpha158 dataset for non-linear pattern recognition in stock data.

## `KUC-107`
**Source**: `examples/candle_chart/run.py`

Visualize historical price data with candlestick charts and volume bars for market analysis and strategy review.

## `KUC-108`
**Source**: `examples/client_server/run_client.py`

Set up a VeighNa client instance connected to an RPC server for distributed CTA strategy execution.

## `KUC-109`
**Source**: `examples/client_server/run_server.py`

Configure a VeighNa server with CTP gateway and RPC service for handling trading requests from remote clients.

## `KUC-110`
**Source**: `examples/cta_backtesting/backtesting_demo.ipynb`

Backtest ATR RSI trading strategy on futures contracts to evaluate performance metrics and optimize parameters.

## `KUC-111`
**Source**: `examples/cta_backtesting/portfolio_backtesting.ipynb`

Backtest multiple CTA strategies simultaneously to evaluate portfolio-level performance and diversification benefits.

## `KUC-112`
**Source**: `examples/data_recorder/data_recorder.py`

Connect to futures exchanges via CTP interface and automatically record real-time market data to database.

## `KUC-113`
**Source**: `examples/download_bars/download_bars.ipynb`

Download historical bar data for futures contracts from data service providers for backtesting and analysis.

## `KUC-114`
**Source**: `examples/no_ui/run.py`

Run CTA strategy execution without graphical UI, connecting directly to CTP for automated futures trading.

## `KUC-115`
**Source**: `examples/notebook_trading/demo_notebook.ipynb`

Execute trading operations interactively from Jupyter notebook using script trader for quick strategy testing and manual trading.

## `KUC-116`
**Source**: `examples/portfolio_backtesting/backtesting_demo.ipynb`

Backtest portfolio strategies like pair trading on multiple futures contracts to evaluate spread-based trading opportunities.

## `KUC-117`
**Source**: `examples/simple_rpc/test_client.py`

Test and demonstrate RPC client functionality for distributed system communication and remote procedure calls.

## `KUC-118`
**Source**: `examples/simple_rpc/test_server.py`

Test and demonstrate RPC server functionality for handling remote client requests and publishing data updates.

## `KUC-119`
**Source**: `examples/spread_backtesting/backtesting.ipynb`

Backtest statistical arbitrage strategies trading spreads between related futures contracts to identify mean reversion opportunities.

## `KUC-120`
**Source**: `examples/veighna_trader/demo_script.py`

Execute custom trading scripts for basket orders, hedging strategies, cross-exchange arbitrage, and market monitoring.

## `KUC-121`
**Source**: `examples/veighna_trader/run.py`

Launch VeighNa Trader desktop application with CTP gateway for futures trading and data management capabilities.
