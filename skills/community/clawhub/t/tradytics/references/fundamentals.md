# Fundamentals

Every US filer's income statements, balance sheets and cash flow since 2009, built from its own filings the day they are filed, ratios at the price now or any close, and what analysts expect, report by report.

## Company profile

`GET /fundamentals/profile` (scope `research`)

The company, its size and its valuation at the price now.

| Param | In | Type | Description |
| --- | --- | --- | --- |
| `symbol` | query | string | Ticker symbol, e.g. `AAPL`. Required. |

| Field | Type | Description |
| --- | --- | --- |
| `symbol` | string | Ticker. |
| `name` | string | Short name, e.g. `Apple`. |
| `legal_name` | string | Registered name. |
| `description` | string | What the company does. |
| `sector, industry` | string | Sector and industry. |
| `exchange, country` | string | Listing exchange and country. |
| `employees` | integer | Full-time employees. |
| `website` | string | Company site. |
| `ipo_date` | string | First trading day, `YYYY-MM-DD`. |
| `is_etf` | boolean | Whether it is a fund. |
| `price` | number | Price now, as `/stocks/quotes` has it. |
| `price_date` | string | Session of the price. |
| `market_cap_usd, enterprise_value_usd` | number | Market cap (every share class) and enterprise value at that price. |
| `shares_outstanding, float_shares` | integer | Shares outstanding and free float. |
| `valuation` | object | `pe`, `forward_pe` (on the next fiscal year's average EPS estimate), `ps`, `pb`, `ev_to_ebitda`. |
| `margins` | object | `gross`, `operating`, `net` over the trailing twelve months, decimals. |
| `dividend_yield` | number | Trailing yield, decimal. |
| `beta` | number | Beta. |
| `year_high, year_low` | number | Highest and lowest price of the last 52 weeks. |

Request: `GET https://tradytics.com/api/public/v1/fundamentals/profile?symbol=AAPL&apiKey=YOUR_API_KEY`

## Income statement

`GET /fundamentals/income-statement` (scope `research`, cursor-paged)

Quarterly, annual or trailing-twelve-month income statements from the 10-Qs and 10-Ks, newest first, at the latest filed figures; a renamed ticker keeps its history (`META` includes its years as `FB`). Q4 is the year less nine months. A line the filing doesn't show, or shows as zero, is `null`.

| Param | In | Type | Description |
| --- | --- | --- | --- |
| `symbol` | query | string | Ticker symbol, e.g. `AAPL`. Required. |
| `period` | query | string | `quarter`, `annual` or `ttm` (trailing twelve months). Default `quarter`. |
| `limit` | query | integer | Periods, newest first, up to 200 (every filing since 2009). Default `12`. |
| `from` | query | string | Earliest period end, `YYYY-MM-DD`. |
| `to` | query | string | Latest period end, `YYYY-MM-DD`. |
| `cursor` | query | string | `next_cursor` from the previous page. |

| Field | Type | Description |
| --- | --- | --- |
| `symbol` | string | Ticker. |
| `fiscal_year` | integer | Fiscal year, as the company names it. |
| `fiscal_period` | string | `Q1` to `Q4` (for `ttm`, the quarter the twelve months end with) or `FY`. |
| `period_end` | string | Last day of the period, `YYYY-MM-DD`. |
| `filed_date` | string | Date of the latest filing behind these numbers (a later filing restates earlier periods). |
| `first_filed_date` | string | Date the period was first on file in full. |
| `accession` | string | SEC accession number of that latest filing. |
| `template` | string | `standard`, `bank`, `insurer` or `reit`: which industry lines apply. |
| `currency` | string | Reporting currency, `USD` (filers reporting in another currency, and 20-F and 40-F filers, are not covered). |
| `revenue_usd` | number | Revenue (banks: net interest income plus noninterest income; insurers and REITs: total revenues). |
| `cost_of_revenue_usd` | number | Cost of revenue (`null` for banks and insurers). |
| `gross_profit_usd` | number | Gross profit, or revenue less cost of revenue where the statement doesn't show it (`null` for banks and insurers). |
| `research_and_development_usd` | number | R&D. |
| `selling_general_and_administrative_usd` | number | SG&A. |
| `depreciation_and_amortization_usd` | number | Depreciation and amortization (the cash flow statement's where the income statement has none). |
| `other_operating_expenses_usd` | number | Other operating expenses. |
| `operating_expenses_usd` | number | Total operating expenses (banks: noninterest expense). |
| `operating_income_usd` | number | Operating income. |
| `interest_income_usd` | number | Interest income. |
| `interest_expense_usd` | number | Interest expense. |
| `other_income_expense_usd` | number | Other income or expense. |
| `total_other_income_expense_usd` | number | Total non-operating income or expense. |
| `income_before_tax_usd` | number | Pretax income. |
| `income_tax_expense_usd` | number | Income tax. |
| `discontinued_operations_usd` | number | Discontinued operations. |
| `equity_in_affiliates_usd` | number | Equity in affiliates. |
| `extraordinary_items_usd` | number | Extraordinary items. |
| `consolidated_net_income_usd` | number | Net income including minority interests. |
| `noncontrolling_interest_usd` | number | Minority interests' share. |
| `net_income_attributable_to_parent_usd` | number | Net income of the company's shareholders. |
| `preferred_dividends_usd` | number | Preferred dividends. |
| `net_income_usd` | number | Net income to common shareholders. |
| `ebitda_usd` | number | Operating income plus depreciation and amortization. |
| `eps, eps_diluted` | number | Basic and diluted EPS, $, adjusted for later splits. Q4: the earnings release's where it agrees with the filings, else Q4 net income over its shares. |
| `weighted_shares, weighted_shares_diluted` | number | Weighted average shares, basic and diluted, adjusted for later splits (integers). |
| `net_interest_income_usd, noninterest_income_usd` | number | Banks: net interest income and noninterest income. |
| `provision_for_credit_losses_usd` | number | Banks: provision for credit losses. |
| `noninterest_expense_usd` | number | Banks: noninterest expense. |
| `premiums_earned_usd, net_investment_income_usd` | number | Insurers: net premiums earned and net investment income. |
| `claims_usd` | number | Insurers: losses, claims and policy benefits. |
| `as_first_filed` | object | Lines a later filing changed, as first filed (`{"revenue_usd": …}`), or `null`. |

Request: `GET https://tradytics.com/api/public/v1/fundamentals/income-statement?symbol=AAPL&apiKey=YOUR_API_KEY`

## Balance sheet

`GET /fundamentals/balance-sheet` (scope `research`, cursor-paged)

Quarterly or annual balance sheets from the 10-Qs and 10-Ks, newest first, at the latest filed figures. A line the filing doesn't show, or shows as zero, is `null`.

| Param | In | Type | Description |
| --- | --- | --- | --- |
| `symbol` | query | string | Ticker symbol, e.g. `AAPL`. Required. |
| `period` | query | string | `quarter` or `annual`. Default `quarter`. |
| `limit` | query | integer | Periods, newest first, up to 200 (every filing since 2009). Default `12`. |
| `from` | query | string | Earliest period end, `YYYY-MM-DD`. |
| `to` | query | string | Latest period end, `YYYY-MM-DD`. |
| `cursor` | query | string | `next_cursor` from the previous page. |

| Field | Type | Description |
| --- | --- | --- |
| `symbol` | string | Ticker. |
| `fiscal_year` | integer | Fiscal year, as the company names it. |
| `fiscal_period` | string | `Q1` to `Q4` (for `ttm`, the quarter the twelve months end with) or `FY`. |
| `period_end` | string | Last day of the period, `YYYY-MM-DD`. |
| `filed_date` | string | Date of the latest filing behind these numbers (a later filing restates earlier periods). |
| `first_filed_date` | string | Date the period was first on file in full. |
| `accession` | string | SEC accession number of that latest filing. |
| `template` | string | `standard`, `bank`, `insurer` or `reit`: which industry lines apply. |
| `currency` | string | Reporting currency, `USD` (filers reporting in another currency, and 20-F and 40-F filers, are not covered). |
| `cash_and_equivalents_usd` | number | Cash and equivalents. |
| `short_term_investments_usd` | number | Short-term investments. |
| `receivables_usd` | number | Receivables. |
| `inventory_usd` | number | Inventory. |
| `other_current_assets_usd` | number | Other current assets. |
| `total_current_assets_usd` | number | Current assets. |
| `property_plant_equipment_usd` | number | Net PP&E. |
| `goodwill_usd` | number | Goodwill. |
| `intangible_assets_usd` | number | Net intangibles. |
| `other_assets_usd` | number | Other non-current assets. |
| `total_assets_usd` | number | Total assets. |
| `accounts_payable_usd` | number | Accounts payable. |
| `deferred_revenue_usd` | number | Current deferred revenue. |
| `short_term_debt_usd` | number | Debt due within a year. |
| `accrued_and_other_current_liabilities_usd` | number | Accrued and other current liabilities. |
| `total_current_liabilities_usd` | number | Current liabilities. |
| `long_term_debt_usd` | number | Long-term debt and capital leases. |
| `other_noncurrent_liabilities_usd` | number | Other non-current liabilities. |
| `total_liabilities_usd` | number | Total liabilities (liabilities and equity less equity where the balance sheet shows no total). |
| `commitments_and_contingencies_usd` | number | Commitments and contingencies. |
| `temporary_equity_usd` | number | Redeemable (temporary) equity. |
| `preferred_stock_usd` | number | Preferred stock. |
| `common_stock_usd` | number | Common stock. |
| `additional_paid_in_capital_usd` | number | Additional paid-in capital. |
| `treasury_stock_usd` | number | Treasury stock. |
| `accumulated_other_comprehensive_income_usd` | number | Accumulated other comprehensive income. |
| `retained_earnings_usd` | number | Retained earnings (deficit). |
| `other_equity_usd` | number | Other equity. |
| `stockholders_equity_usd` | number | Equity of the parent's shareholders. |
| `noncontrolling_interest_usd` | number | Minority interests. |
| `total_equity_usd` | number | Total equity. |
| `total_liabilities_and_equity_usd` | number | Liabilities and equity. |
| `total_debt_usd` | number | Short-term plus long-term debt. |
| `net_debt_usd` | number | Total debt less cash and equivalents. |
| `loans_usd, deposits_usd` | number | Banks: net loans and deposits. |
| `real_estate_investments_usd` | number | REITs: real estate, net. |
| `as_first_filed` | object | Lines a later filing changed, as first filed (`{"revenue_usd": …}`), or `null`. |

Request: `GET https://tradytics.com/api/public/v1/fundamentals/balance-sheet?symbol=AAPL&apiKey=YOUR_API_KEY`

## Cash flow statement

`GET /fundamentals/cash-flow` (scope `research`, cursor-paged)

Quarterly, annual or trailing-twelve-month cash flow statements, newest first: a quarter is the filing's year to date less the quarter before's. A line the filing doesn't show, or shows as zero, is `null`.

| Param | In | Type | Description |
| --- | --- | --- | --- |
| `symbol` | query | string | Ticker symbol, e.g. `AAPL`. Required. |
| `period` | query | string | `quarter`, `annual` or `ttm` (trailing twelve months). Default `quarter`. |
| `limit` | query | integer | Periods, newest first, up to 200 (every filing since 2009). Default `12`. |
| `from` | query | string | Earliest period end, `YYYY-MM-DD`. |
| `to` | query | string | Latest period end, `YYYY-MM-DD`. |
| `cursor` | query | string | `next_cursor` from the previous page. |

| Field | Type | Description |
| --- | --- | --- |
| `symbol` | string | Ticker. |
| `fiscal_year` | integer | Fiscal year, as the company names it. |
| `fiscal_period` | string | `Q1` to `Q4` (for `ttm`, the quarter the twelve months end with) or `FY`. |
| `period_end` | string | Last day of the period, `YYYY-MM-DD`. |
| `filed_date` | string | Date of the latest filing behind these numbers (a later filing restates earlier periods). |
| `first_filed_date` | string | Date the period was first on file in full. |
| `accession` | string | SEC accession number of that latest filing. |
| `template` | string | `standard`, `bank`, `insurer` or `reit`: which industry lines apply. |
| `currency` | string | Reporting currency, `USD` (filers reporting in another currency, and 20-F and 40-F filers, are not covered). |
| `net_income_usd` | number | Net income. |
| `depreciation_and_amortization_usd` | number | Depreciation and amortization. |
| `stock_based_compensation_usd` | number | Stock-based compensation. |
| `other_cash_adjustments_usd` | number | Other non-cash adjustments. |
| `change_in_working_capital_usd` | number | Change in operating assets and liabilities. |
| `other_operating_activities_usd` | number | Other operating activities. |
| `operating_cash_flow_continuing_usd, operating_cash_flow_discontinued_usd` | number | Operating cash flow of continuing and discontinued operations. |
| `operating_cash_flow_usd` | number | Operating cash flow. |
| `capital_expenditure_usd` | number | Capital expenditure (negative). |
| `sale_of_property_plant_equipment_usd` | number | PP&E sold. |
| `acquisitions_usd` | number | Businesses acquired, net of cash (negative). |
| `other_investing_activities_usd` | number | Other investing activities. |
| `investing_cash_flow_continuing_usd, investing_cash_flow_discontinued_usd` | number | Investing cash flow of continuing and discontinued operations. |
| `investing_cash_flow_usd` | number | Investing cash flow. |
| `net_short_term_debt_issued_usd, net_long_term_debt_issued_usd` | number | Debt issued less repaid, short and long term. |
| `dividends_paid_usd` | number | Dividends paid (negative). |
| `share_repurchases_usd` | number | Shares bought back (negative). |
| `noncontrolling_interests_usd` | number | Paid to minority interests (negative). |
| `other_financing_activities_usd` | number | Other financing. |
| `financing_cash_flow_continuing_usd, financing_cash_flow_discontinued_usd` | number | Financing cash flow of continuing and discontinued operations. |
| `financing_cash_flow_usd` | number | Financing cash flow. |
| `effect_of_exchange_rates_usd` | number | Currency effect on cash. |
| `discontinued_operations_income_usd` | number | Income from discontinued operations. |
| `change_in_cash_usd` | number | Change in cash. |
| `free_cash_flow_usd` | number | Operating cash flow plus capital expenditure. |
| `as_first_filed` | object | Lines a later filing changed, as first filed (`{"revenue_usd": …}`), or `null`. |

Request: `GET https://tradytics.com/api/public/v1/fundamentals/cash-flow?symbol=AAPL&apiKey=YOUR_API_KEY`

## Ratios

`GET /fundamentals/ratios` (scope `research`, cursor-paged)

Valuation, margin, return and balance sheet ratios on the trailing twelve months: at the price now, or at each close since 2009 with `from` and `to`, on the statements on file that day.

| Param | In | Type | Description |
| --- | --- | --- | --- |
| `symbol` | query | string | Ticker symbol, e.g. `AAPL`. Required. |
| `from` | query | string | First day, `YYYY-MM-DD`. |
| `to` | query | string | Last day, `YYYY-MM-DD`. |
| `limit` | query | integer | Rows per page, up to 1000. Default `100`. |
| `cursor` | query | string | `next_cursor` from the previous page. |

| Field | Type | Description |
| --- | --- | --- |
| `symbol` | string | Ticker. |
| `date` | string | Session, `YYYY-MM-DD`. |
| `price` | number | Price now, as `/stocks/quotes` has it, or the close. |
| `market_cap_usd` | number | Market cap across all share classes. Historical values use the close and filed shares, with the historical issuer market cap series for Berkshire Hathaway. |
| `enterprise_value_usd` | number | Market cap plus total debt less cash and equivalents. |
| `eps` | number | Trailing net income to common per share outstanding, $. |
| `pe, ps, pb` | number | Market cap over trailing net income to common, revenue and stockholders' equity (`null` for a loss). |
| `price_to_cash_flow, price_to_free_cash_flow` | number | Market cap over trailing operating and free cash flow. |
| `ev_to_sales, ev_to_ebitda` | number | Enterprise value over trailing revenue and EBITDA. |
| `gross_margin, operating_margin, net_margin` | number | Trailing gross profit, operating income and net income to common over revenue, decimals. |
| `dividend_yield` | number | Trailing dividends paid over market cap, decimal. |
| `return_on_assets, return_on_equity` | number | Trailing net income to common over the latest total assets and stockholders' equity, decimals. |
| `debt_to_equity` | number | Total debt over stockholders' equity. |
| `current_ratio, quick_ratio, cash_ratio` | number | Current assets; cash, short-term investments and receivables; and cash, over current liabilities. |
| `free_cash_flow_usd` | number | Trailing free cash flow. |
| `average_volume` | integer | Average daily volume of the 30 sessions to the date, shares (`null` at the price now). |

Request: `GET https://tradytics.com/api/public/v1/fundamentals/ratios?symbol=AAPL&apiKey=YOUR_API_KEY`

## Revenue segments

`GET /fundamentals/segments` (scope `research`)

Revenue by product line or by region as reported, newest period first, largest segment first.

| Param | In | Type | Description |
| --- | --- | --- | --- |
| `symbol` | query | string | Ticker symbol, e.g. `AAPL`. Required. |
| `by` | query | string | `product` or `region`. Default `product`. |
| `period` | query | string | `annual` or `quarter`. Default `annual`. |

| Field | Type | Description |
| --- | --- | --- |
| `symbol` | string | Ticker. |
| `period_end` | string | Last day of the period. |
| `fiscal_year` | integer | Fiscal year. |
| `fiscal_period` | string | `Q1` to `Q4` or `FY`. |
| `segment` | string | Segment as the company names it. |
| `revenue_usd` | number | Its revenue. |

Request: `GET https://tradytics.com/api/public/v1/fundamentals/segments?symbol=AAPL&by=product&apiKey=YOUR_API_KEY`

## Earnings

`GET /fundamentals/earnings` (scope `research`, cursor-paged)

Every report with EPS and revenue against the estimates, newest first. The next report comes first, its actuals `null`.

| Param | In | Type | Description |
| --- | --- | --- | --- |
| `symbol` | query | string | Ticker symbol, e.g. `AAPL`. Required. |
| `limit` | query | integer | Rows per page, up to 1000. Default `40`. |
| `cursor` | query | string | `next_cursor` from the previous page. |

| Field | Type | Description |
| --- | --- | --- |
| `symbol` | string | Ticker. |
| `date` | string | Report date. |
| `fiscal_year, fiscal_period, period_end` | mixed | The quarter reported (`period_end` `null` until filed, for 52/53-week years). |
| `eps_adjusted, eps_estimate` | number | EPS as analysts count it (adjusted, where the company reports adjusted EPS) and their consensus, $. |
| `eps_surprise_pct` | number | `eps_adjusted` against the consensus, %. |
| `eps_diluted` | number | GAAP diluted EPS of the quarter from the filings (the income statement's `eps_diluted`), `null` until filed, $. |
| `revenue_usd, revenue_estimate_usd` | number | Reported revenue and the consensus. |
| `revenue_surprise_pct` | number | Revenue against the consensus, %. |

Request: `GET https://tradytics.com/api/public/v1/fundamentals/earnings?symbol=AAPL&apiKey=YOUR_API_KEY`

## Analyst estimates

`GET /fundamentals/estimates` (scope `research`)

Consensus for each fiscal period not reported yet, nearest first.

| Param | In | Type | Description |
| --- | --- | --- | --- |
| `symbol` | query | string | Ticker symbol, e.g. `AAPL`. Required. |
| `period` | query | string | `annual` or `quarter`. Default `annual`. |

| Field | Type | Description |
| --- | --- | --- |
| `symbol` | string | Ticker. |
| `period_end` | string | Last day of the fiscal period. |
| `fiscal_year` | integer | Fiscal year. |
| `fiscal_period` | string | `Q1` to `Q4` or `FY`. |
| `revenue_low_usd, revenue_average_usd, revenue_high_usd` | number | Revenue: the lowest, average and highest estimate. |
| `eps_low, eps_average, eps_high` | number | EPS, $. |
| `ebitda_low_usd, ebitda_average_usd, ebitda_high_usd` | number | EBITDA. |
| `net_income_low_usd, net_income_average_usd, net_income_high_usd` | number | Net income. |
| `revenue_analysts, eps_analysts` | integer | Analysts behind the revenue and EPS estimates. |

Request: `GET https://tradytics.com/api/public/v1/fundamentals/estimates?symbol=AAPL&apiKey=YOUR_API_KEY`

## Analysts

`GET /fundamentals/analysts` (scope `research`)

Ratings consensus, price targets and the latest 50 calls by firm.

| Param | In | Type | Description |
| --- | --- | --- | --- |
| `symbol` | query | string | Ticker symbol, e.g. `AAPL`. Required. |

| Field | Type | Description |
| --- | --- | --- |
| `symbol` | string | Ticker. |
| `consensus` | object | `rating` (`strong_buy` to `strong_sell`, the firms' average) and the firms at each on their latest call of the last 12 months: `strong_buy`, `buy`, `hold`, `sell`, `strong_sell`. |
| `price_target` | object | `low`, `median`, `average`, `high`, $. |
| `grades[]` | array | `date`, `firm`, `action` (`upgrade`, `downgrade`, `maintain` …), `previous_grade`, `grade` in the firm's own words. |

Request: `GET https://tradytics.com/api/public/v1/fundamentals/analysts?symbol=AAPL&apiKey=YOUR_API_KEY`

## Call transcripts

`GET /fundamentals/transcripts` (scope `research`)

Earnings call transcripts: the latest, one quarter, or every quarter of a fiscal year.

| Param | In | Type | Description |
| --- | --- | --- | --- |
| `symbol` | query | string | Ticker symbol, e.g. `AAPL`. Required. |
| `year` | query | integer | Fiscal year. Alone, every quarter of it. |
| `quarter` | query | integer | Fiscal quarter, 1 to 4, with `year`. |

| Field | Type | Description |
| --- | --- | --- |
| `symbol` | string | Ticker. |
| `fiscal_year` | integer | Fiscal year. |
| `fiscal_period` | string | `Q1` to `Q4`. |
| `date` | string | Call date. |
| `content` | string | The whole call, one speaker per paragraph. |

Request: `GET https://tradytics.com/api/public/v1/fundamentals/transcripts?symbol=AAPL&apiKey=YOUR_API_KEY`

## ETF holdings

`GET /fundamentals/etf-holdings` (scope `research`, cursor-paged)

Everything a fund holds, largest weight first, as its issuer last published.

| Param | In | Type | Description |
| --- | --- | --- | --- |
| `symbol` | query | string | An ETF, e.g. `QQQ`. Required. |
| `limit` | query | integer | Rows per page, up to 1000. Default `100`. |
| `cursor` | query | string | `next_cursor` from the previous page. |

| Field | Type | Description |
| --- | --- | --- |
| `symbol` | string | The holding's ticker. |
| `name` | string | Its name. |
| `weight` | number | Share of the fund, decimal. |
| `shares` | integer | Shares held. |
| `market_value_usd` | number | Value of the position. |

Request: `GET https://tradytics.com/api/public/v1/fundamentals/etf-holdings?symbol=QQQ&apiKey=YOUR_API_KEY`
