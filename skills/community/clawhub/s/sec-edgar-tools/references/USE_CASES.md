# Known Use Cases (KUC)

Total: **55**

## `KUC-101`
**Source**: `docs/Usage.ipynb`

Discovering and retrieving SEC filings for companies to understand their regulatory submissions, corporate actions, and financial disclosures.

## `KUC-102`
**Source**: `docs/doctest.py`

Extracting financial data from SEC filings to analyze company performance, including income statements, balance sheets, and cash flows.

## `KUC-103`
**Source**: `docs/examples/insider_transactions.py`

Tracking insider buying and selling activities by processing Form 4 filings to identify significant insider transactions and ownership changes.

## `KUC-104`
**Source**: `notebooks/13f-institutional-holdings-python.ipynb`

Analyzing institutional investment holdings from 13F filings to understand portfolio composition, top holdings, and changes in positions over time.

## `KUC-105`
**Source**: `docs/examples/crowdfunding.py`

Tracking Regulation CF crowdfunding campaigns through their complete lifecycle including initial filings, amendments, updates, and termination.

## `KUC-106`
**Source**: `notebooks/Reading-Data-From-XBRL.ipynb`

Extracting structured financial data from XBRL-tagged filings including income statements, balance sheets, and cash flow statements with period history.

## `KUC-107`
**Source**: `notebooks/10k-business-description-python.ipynb`

Extracting and analyzing sections from 10-K annual reports including business descriptions, risk factors, and MD&A for fundamental analysis.

## `KUC-108`
**Source**: `notebooks/8k-earnings-release-python.ipynb`

Finding and extracting earnings information from 8-K current reports including press releases, financial tables, and earnings-related disclosures.

## `KUC-109`
**Source**: `notebooks/etf-fund-holdings-python.ipynb`

Analyzing ETF portfolio holdings from NPORT-P filings to understand fund composition, top positions, and allocation by sector or country.

## `KUC-110`
**Source**: `notebooks/executive-compensation-sec-python.ipynb`

Analyzing executive compensation from DEF 14A proxy statements including CEO pay, pay-vs-performance metrics, and compensation trends.

## `KUC-111`
**Source**: `notebooks/10q-quarterly-earnings-python.ipynb`

Comparing quarterly financial results across companies or tracking a single company's quarterly performance over multiple periods.

## `KUC-112`
**Source**: `notebooks/compare-company-financials-python.ipynb`

Comparing financial metrics across multiple companies to benchmark performance, profitability, and growth metrics.

## `KUC-113`
**Source**: `notebooks/monitor-sec-filings-python.ipynb`

Monitoring today's SEC filings to track earnings announcements, insider trading, and other corporate events as they happen.

## `KUC-114`
**Source**: `notebooks/download-sec-filings-bulk-python.ipynb`

Downloading large batches of SEC filings for archival, analysis, or processing with support for multiple output formats (text, markdown, HTML).

## `KUC-115`
**Source**: `notebooks/sec-filing-text-nlp-python.ipynb`

Applying NLP techniques to SEC filings including text extraction, search, section identification, and document chunking for analysis.

## `KUC-116`
**Source**: `notebooks/sec-industry-sic-code-python.ipynb`

Filtering companies and filings by SIC codes and industry classifications to focus research on specific sectors like semiconductors, software, or banking.

## `KUC-117`
**Source**: `notebooks/beneficial-ownership-sec-python.ipynb`

Tracking beneficial ownership changes through Schedule 13D and 13G filings to identify significant shareholders and ownership stakes.

## `KUC-118`
**Source**: `notebooks/money-market-fund-nmfp-python.ipynb`

Analyzing money market fund portfolios from N-MFP filings including holdings, maturity schedules, yield history, and fund composition.

## `KUC-119`
**Source**: `notebooks/mutual-fund-holdings-nport-python.ipynb`

Extracting mutual fund portfolio holdings from NPORT-P filings to analyze fund composition, country allocation, and sector exposure.

## `KUC-120`
**Source**: `notebooks/bdc-business-development-company-python.ipynb`

Researching BDCs including portfolio companies, investment strategies, and financial performance for alternative investment analysis.

## `KUC-121`
**Source**: `notebooks/XBRL2-StitchingStatements.ipynb`

Combining XBRL financial statements across multiple filings or periods to create unified views of financial performance over time.

## `KUC-122`
**Source**: `notebooks/financial-statements-to-dataframe.ipynb`

Exporting financial statements to pandas DataFrames for further analysis, visualization, or integration with other data tools.

## `KUC-123`
**Source**: `notebooks/extract-revenue-earnings-python.ipynb`

Extracting specific financial metrics like revenue, net income, and free cash flow for time series analysis and growth tracking.

## `KUC-124`
**Source**: `notebooks/XBRL2-FactQueries.ipynb`

Querying XBRL facts using semantic search to find specific financial data points, concepts, and dimensional breakdowns.

## `KUC-125`
**Source**: `notebooks/sec-filing-exhibits-python.ipynb`

Accessing and extracting exhibits attached to SEC filings including press releases, supporting documents, and supplemental information.

## `KUC-126`
**Source**: `docs/examples/fund_examples.py`

Navigating fund entities including fund companies, series, and share classes to find and analyze fund information by ticker, CIK, or Series ID.

## `KUC-127`
**Source**: `examples/scripts/ai/ai_context.py`

Generating token-efficient context from SEC filings for consumption by large language models (LLMs) with support for progressive disclosure.

## `KUC-128`
**Source**: `examples/scripts/advanced/ranking_search_examples.py`

Performing relevance-ranked search within SEC filings using BM25 or hybrid algorithms for semantic content discovery.

## `KUC-129`
**Source**: `examples/scripts/advanced/enterprise_config.py`

Configuring EdgarTools for enterprise use cases including custom SEC mirrors, rate limiting, and environment-based configuration profiles.

## `KUC-130`
**Source**: `notebooks/proxy-statement-def14a-python.ipynb`

Analyzing proxy statements (DEF 14A) for governance information including executive compensation, shareholder proposals, and board composition.

## `KUC-131`
**Source**: `docs/examples/formtype_demo_examples.py`

Using FormType enum for IDE autocomplete and type-safe form specification when querying SEC filings.

## `KUC-132`
**Source**: `docs/examples/periodtype_demo_examples.py`

Using PeriodType enum for period specification including annual, quarterly, TTM, and YTD with enhanced validation.

## `KUC-133`
**Source**: `docs/examples/feat004_demo_enhanced_validation.py`

Demonstrating enhanced parameter validation with helpful error messages for invalid form types, periods, and other inputs.

## `KUC-134`
**Source**: `docs/examples/plot_revenue.py`

Creating financial visualizations showing revenue, gross profit, and net income trends over time with professional formatting.

## `KUC-135`
**Source**: `examples/scripts/advanced/section_detection_demo.py`

Automatically detecting and identifying sections within SEC filings using hybrid detection with confidence scoring.

## `KUC-136`
**Source**: `notebooks/revenue-segment-hierarchy-python.ipynb`

Analyzing revenue segmentation and product/service hierarchies within financial statements to understand business composition.

## `KUC-137`
**Source**: `notebooks/fund-census-ncen-python.ipynb`

Analyzing fund census data from N-CEN filings including fund series, service providers, and classification information.

## `KUC-138`
**Source**: `notebooks/sec-comment-letters-python.ipynb`

Accessing and analyzing SEC staff comment letters to understand regulatory review topics and compliance issues.

## `KUC-139`
**Source**: `examples/scripts/basic/entity_facts_dataframe.py`

Exporting company financial facts to pandas DataFrames for custom analysis with filtering by period type and concept.

## `KUC-140`
**Source**: `examples/table_width_example.py`

Controlling table column widths when extracting text from SEC filings for AI/LLM processing to prevent truncation.

## `KUC-141`
**Source**: `notebooks/Beginners-Guide.ipynb`

Getting started with EdgarTools to perform basic SEC filing operations including company lookup, filing retrieval, and financial data access.

## `KUC-142`
**Source**: `notebooks/XBRL2-PeriodViews.ipynb`

Rendering XBRL statements with different period views including quarterly comparisons, annual comparisons, and YTD breakdowns.

## `KUC-143`
**Source**: `docs/examples/feat005_demo_statement_types.py`

Using StatementType enum for organized categorization of financial statements including primary, comprehensive, analytical, and specialized statements.

## `KUC-144`
**Source**: `docs/examples/investment_fund_research.py`

Researching investment fund performance and comparing with competitors using fund entity data and filings.

## `KUC-145`
**Source**: `notebooks/XBRL2-StandardizedStatements.ipynb`

Accessing standardized financial statements (income, balance, cash flow) from XBRL data with consistent formatting.

## `KUC-146`
**Source**: `docs/examples/offering_lifecycle_ai_discovery.py`

Demonstrating AI agent workflow for discovering crowdfunding campaign lifecycle data using context hints without manual API knowledge.

## `KUC-147`
**Source**: `notebooks/XBRL2-NonFinancialStatements.ipynb`

Accessing non-standard XBRL statements such as segment information, revenue by market, and other supplemental disclosures.

## `KUC-148`
**Source**: `notebooks/sec-reference-data-python.ipynb`

Accessing SEC reference data including company tickers, exchange listings, and company metadata for identification and lookup.

## `KUC-149`
**Source**: `tests/demo_to_markdown.ipynb`

Converting SEC filing content to markdown format with proper table formatting for documentation and sharing.

## `KUC-150`
**Source**: `notebooks/Initial-Insider-Transactions.ipynb`

Tracking initial insider filings (Form 3) and subsequent transactions (Form 4) for executive and director ownership reporting.

## `KUC-151`
**Source**: `notebooks/Paging-Through-Filings.ipynb`

Navigating through large sets of SEC filings using pagination methods to access results across multiple pages.

## `KUC-152`
**Source**: `notebooks/XBRL2-CustomTags.ipynb`

Analyzing custom XBRL tags and taxonomy extensions used by companies beyond standard US-GAAP tags.

## `KUC-153`
**Source**: `examples/scripts/ai/skills_usage.py`

Using AI Skills system for specialized SEC analysis workflows with helper functions and documentation.

## `KUC-154`
**Source**: `examples/scripts/ai/basic_docs.py`

Accessing interactive documentation directly within Python for learning the EdgarTools API without external resources.

## `KUC-155`
**Source**: `examples/scripts/advanced/start_page_number_example.py`

Controlling starting page numbers when converting documents to markdown with page break markers.
