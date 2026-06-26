# Known Use Cases (KUC)

Total: **38**

## `KUC-101`
**Source**: `examples/benchmarks/LightGBM/features_resample_N.py`

Resampling high-frequency 1-minute data to lower frequencies (e.g., daily) for downstream feature computation and model training.

## `KUC-102`
**Source**: `examples/benchmarks/LightGBM/features_sample.py`

Resampling 1-minute data to daily frequency by extracting a specific minute point from each day for feature generation.

## `KUC-103`
**Source**: `examples/benchmarks/LightGBM/multi_freq_handler.py`

Loading and processing data with both daily frequency features and 15-minute frequency features for models that leverage multiple time scales.

## `KUC-104`
**Source**: `examples/benchmarks/TFT/tft.py`

Training and evaluating a Temporal Fusion Transformer model using Alpha158 features for stock return prediction.

## `KUC-105`
**Source**: `examples/benchmarks/TFT/data_formatters/qlib_Alpha158.py`

Formatting Alpha158 dataset specifically for Temporal Fusion Transformer models with proper column definitions and transformations.

## `KUC-106`
**Source**: `examples/benchmarks/TFT/libs/hyperparam_opt.py`

Optimizing hyperparameters for Temporal Fusion Transformer models using random search, supporting both single-GPU and distributed training.

## `KUC-107`
**Source**: `examples/benchmarks/TRA/example.py`

Training a Temporal Routing Attention model for stock prediction using LSTM-based architecture with configurable seed for reproducibility.

## `KUC-108`
**Source**: `examples/benchmarks/TRA/src/dataset.py`

Creating time series slices for the TRA model, handling multi-index pandas data with instrument and datetime levels for sequential model training.

## `KUC-109`
**Source**: `examples/benchmarks/TRA/src/model.py`

Implementing the Temporal Routing Attention neural network model with configurable LSTM cells and loss functions for stock prediction.

## `KUC-110`
**Source**: `examples/benchmarks/TRA/Reports.ipynb`

Analyzing and reporting backtest results for TRA model including MSE, MAE, IC metrics and top-N ranking performance.

## `KUC-111`
**Source**: `examples/benchmarks_dynamic/DDG-DA/workflow.py`

Running domain adaptation workflow for dynamic trading strategies using DDG-DA method to adapt models across different market regimes.

## `KUC-112`
**Source**: `examples/benchmarks_dynamic/baseline/rolling_benchmark.py`

Running rolling window benchmarks for model evaluation using fixed configurations with Linear and LightGBM models on Alpha158 features.

## `KUC-113`
**Source**: `examples/data_demo/data_cache_demo.py`

Demonstrating how to serialize and cache processed data handlers to disk to avoid redundant data preprocessing operations.

## `KUC-114`
**Source**: `examples/data_demo/data_mem_resuse_demo.py`

Demonstrating how to reuse processed data in memory across multiple training iterations to improve efficiency.

## `KUC-115`
**Source**: `examples/highfreq/highfreq_handler.py`

Handling high-frequency 1-minute market data with specific feature configurations for short-term trading models.

## `KUC-116`
**Source**: `examples/highfreq/highfreq_ops.py`

Implementing operators for high-frequency data processing including DayLast (daily last value), forward/backward fill, date extraction, and null handling.

## `KUC-117`
**Source**: `examples/highfreq/highfreq_processor.py`

Normalizing high-frequency price and volume data using median-based scaling for consistent feature ranges across instruments.

## `KUC-118`
**Source**: `examples/highfreq/workflow.py`

Executing end-to-end high-frequency trading workflow from data loading through model training to signal generation for minute-level strategies.

## `KUC-119`
**Source**: `examples/hyperparameter/LightGBM/hyperparameter_158.py`

Optimizing LightGBM hyperparameters using Optuna for Alpha158 feature dataset to find best model configuration for stock prediction.

## `KUC-120`
**Source**: `examples/hyperparameter/LightGBM/hyperparameter_360.py`

Optimizing LightGBM hyperparameters using Optuna for Alpha360 (high-frequency) feature dataset for minute-level prediction models.

## `KUC-121`
**Source**: `examples/model_interpreter/feature.py`

Extracting and analyzing feature importance from trained GBDT models to understand which factors drive model predictions.

## `KUC-122`
**Source**: `examples/model_rolling/task_manager_rolling.py`

Managing rolling training tasks across multiple time periods with task generation, collection, and multiprocessing support.

## `KUC-123`
**Source**: `examples/nested_decision_execution/workflow.py`

Running backtests for nested decision trading strategies that execute at multiple frequencies (daily and 30-minute) with portfolio analysis.

## `KUC-124`
**Source**: `examples/online_srv/online_management_simulate.py`

Simulating online model management with rolling tasks, including model updates and signal generation for live trading scenarios.

## `KUC-125`
**Source**: `examples/online_srv/rolling_online_management.py`

Managing online models with rolling updates including first training, routine updates, strategy addition, and signal preparation for production.

## `KUC-126`
**Source**: `examples/online_srv/update_online_pred.py`

Updating online model predictions with first training and subsequent prediction refreshes for production deployment.

## `KUC-127`
**Source**: `examples/orderbook_data/create_dataset.py`

Importing raw orderbook data (ticks, orders, transactions) into Qlib's data storage using Arctic time-series database.

## `KUC-128`
**Source**: `examples/orderbook_data/example.py`

Demonstrating how to use imported orderbook data in Qlib with custom providers and non-aligned time series handling.

## `KUC-129`
**Source**: `examples/portfolio/prepare_riskdata.py`

Preparing portfolio risk model data using Structured Covariance Estimator for risk management and portfolio optimization.

## `KUC-130`
**Source**: `examples/rl/simple_example.ipynb`

Implementing a simple reinforcement learning simulator and state interpreter for RL-based trading agent development.

## `KUC-131`
**Source**: `examples/rl_order_execution/scripts/gen_pickle_data.py`

Generating pickle-format training data for reinforcement learning order execution from high-frequency backtest results.

## `KUC-132`
**Source**: `examples/rl_order_execution/scripts/gen_training_orders.py`

Generating synthetic training orders for RL order execution by sampling from historical volume distributions with train/valid/test splits.

## `KUC-133`
**Source**: `examples/rl_order_execution/scripts/merge_orders.py`

Merging multiple order files into consolidated train/valid/test datasets for RL order execution model training.

## `KUC-134`
**Source**: `examples/rolling_process_data/rolling_handler.py`

Creating a data handler specifically designed for rolling window data processing with configurable time ranges.

## `KUC-135`
**Source**: `examples/rolling_process_data/workflow.py`

Executing rolling window workflows for model training and evaluation with pre-processor caching to optimize repeated runs.

## `KUC-136`
**Source**: `examples/run_all_model.py`

Running comprehensive benchmarks across multiple models with standardized configurations for fair model comparison and evaluation.

## `KUC-137`
**Source**: `examples/tutorial/detailed_workflow.ipynb`

Learning Qlib's detailed workflow including data access, feature computation, model training, and portfolio analysis through interactive examples.

## `KUC-138`
**Source**: `examples/workflow_by_code.py`

Building Qlib workflows programmatically using Python code instead of YAML configuration for fine-grained control over the pipeline.
