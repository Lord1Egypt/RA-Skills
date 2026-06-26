# Known Use Cases (KUC)

Total: **29**

## `KUC-101`
**Source**: `docs/LLM_ADAPTER_TEMPLATE.py`

Users need a template to create custom LLM adapters for OpenAI-compatible API providers to integrate with TradingAgents framework.

## `KUC-102`
**Source**: `examples/batch_analysis.py`

Investors need to analyze multiple stocks simultaneously and generate comparison reports for portfolio selection and sector analysis.

## `KUC-103`
**Source**: `examples/cli_demo.py`

Chinese-speaking users need to see how TradingAgents CLI tools support Chinese language output and commands.

## `KUC-104`
**Source**: `examples/config_management_demo.py`

Users need to manage multiple LLM model configurations, track token usage, and monitor API costs across different providers.

## `KUC-105`
**Source**: `examples/crawlers/internal_message_crawler.py`

System needs to crawl internal messages from corporate sources and store them in the message database for analysis.

## `KUC-106`
**Source**: `examples/crawlers/message_crawler_scheduler.py`

System needs to coordinate and schedule crawling tasks for both social media and internal messages in a unified pipeline.

## `KUC-107`
**Source**: `examples/crawlers/social_media_crawler.py`

System needs to crawl social media platforms for stock-related discussions and sentiment data.

## `KUC-108`
**Source**: `examples/custom_analysis_demo.py`

Investors need customized stock analysis with selectable focus areas like technical, fundamental, risk assessment, or sector comparison.

## `KUC-109`
**Source**: `examples/dashscope_examples/demo_dashscope.py`

Users need to run TradingAgents framework using Alibaba's BaiLian (通义千问) large language model for stock analysis.

## `KUC-110`
**Source**: `examples/dashscope_examples/demo_dashscope_chinese.py`

Chinese-speaking users need stock analysis powered by BaiLian with complete Chinese language output and localized analysis.

## `KUC-111`
**Source**: `examples/dashscope_examples/demo_dashscope_no_memory.py`

Users need stateless stock analysis using BaiLian model without conversation history memory for independent analysis sessions.

## `KUC-112`
**Source**: `examples/dashscope_examples/demo_dashscope_simple.py`

Users need a simple test to verify BaiLian API connectivity and basic LLM functionality before running full analysis.

## `KUC-113`
**Source**: `examples/data_dir_config_demo.py`

Users need to configure and manage data storage directories for TradingAgents including cache, logs, and output paths.

## `KUC-114`
**Source**: `examples/demo_deepseek_analysis.py`

Users need to perform stock investment analysis using DeepSeek V3 large language model as an alternative to other providers.

## `KUC-115`
**Source**: `examples/demo_deepseek_simple.py`

Users need a minimal, dependency-light demonstration of DeepSeek API integration without complex TradingAgents imports.

## `KUC-116`
**Source**: `examples/demo_news_filtering.py`

Investors need to filter and clean news data to remove irrelevant or low-quality content before sentiment analysis.

## `KUC-117`
**Source**: `examples/enhanced_history_demo.py`

Users need to view, load, and review historical stock analysis results for tracking investment decisions over time.

## `KUC-118`
**Source**: `examples/my_stock_analysis.py`

Individual investors need a personalized script to analyze stocks of their choice with custom focus areas.

## `KUC-119`
**Source**: `examples/run_message_crawlers.py`

Users need to execute message crawling tasks for social media and internal communications through a unified runner script.

## `KUC-120`
**Source**: `examples/simple_analysis_demo.py`

New users need a quick, simple demonstration of TradingAgents-CN capabilities for rapid stock analysis.

## `KUC-121`
**Source**: `examples/stock_data_model_usage.py`

Users need to access extended stock data models with comprehensive company information for Chinese A-share markets.

## `KUC-122`
**Source**: `examples/stock_list_example.py`

Users need to fetch comprehensive stock lists with server failover capability from configuration files for robust data access.

## `KUC-123`
**Source**: `examples/stock_query_examples.py`

Users need to query stock data through a robust API that falls back to traditional methods when primary services fail.

## `KUC-124`
**Source**: `examples/test_enhanced_data_integration.py`

Users need to test the MongoDB app cache integration for faster data access when TA_USE_APP_CACHE is enabled.

## `KUC-125`
**Source**: `examples/test_installation.py`

Users need to verify that TradingAgents-CN is correctly installed with each dependencies and proper environment configuration.

## `KUC-126`
**Source**: `examples/test_news_timeout.py`

Users need to test news retrieval timeout handling, especially for Google News which may timeout, with polling retry mechanism.

## `KUC-127`
**Source**: `examples/token_tracking_demo.py`

Users need to track LLM token consumption, calculate API costs, and monitor usage statistics across different models.

## `KUC-128`
**Source**: `examples/tushare_demo.py`

Users need to access Chinese A-share market data (stocks, indices, fundamentals) through Tushare professional data API.

## `KUC-129`
**Source**: `examples/tushare_unified_demo.py`

Users need to use the unified TushareProvider and TushareSyncService for consistent access to Chinese market data with async support.
