# Tushare Pro API Quick Reference (11000 Points)

This document provides a quick reference for all 185 Tushare Pro APIs (11000 points + `rt_k` permission).

## Common Parameters

- All date parameters use `YYYYMMDD` format unless specified otherwise.
- Stock codes use the format `XXXXXX.SH` (Shanghai), `XXXXXX.SZ` (Shenzhen), or `XXXXXX.BJ` (Beijing).
- Most APIs support `limit` and `offset` for pagination.

---

## 1. Stock Master Data (12 APIs)

| API Name | Description | Key Params |
|---|---|---|
| `stock_basic` | Get stock master data, including code, name, list date, and delist date | `is_hs`, `list_status`, `exchange` |
| `trade_cal` | Get exchange trading calendar data | `exchange`, `start_date`, `end_date` |
| `stock_st` | Get the daily historical list of ST stocks | `ts_code`, `trade_date` |
| `st` | Get the ST risk-warning board stock list | `ts_code`, `pub_date` |
| `stock_hsgt` | Get the Stock Connect eligible stock list | `trade_date`, `type` |
| `namechange` | Get stock historical name changes | `ts_code`, `start_date`, `end_date` |
| `stock_company` | Get listed company profile data | `exchange` |
| `stk_managers` | Get listed company management data | `ts_code`, `ann_date` |
| `stk_rewards` | Get management compensation and shareholding data | `ts_code`, `end_date` |
| `bse_mapping` | Get Beijing Stock Exchange old/new code mapping | `o_code`, `n_code` |
| `new_share` | Get IPO listing data | `start_date`, `end_date` |
| `bak_basic` | Get backup basic data, including valuation and financial indicators | `trade_date`, `ts_code` |

## 2. Market Data (Low Frequency: Daily / Weekly / Monthly) (11 APIs)

| API Name | Description | Key Params |
|---|---|---|
| `daily` | Get A-share historical daily bars | `ts_code`, `trade_date`, `start_date` |
| `pro_bar` | Get adjusted A-share price data (forward/backward adjusted) and minute data | `ts_code`, `adj`, `freq`, `start_date`, `end_date` |
| `weekly` | Get A-share weekly bars | `ts_code`, `trade_date`, `start_date` |
| `monthly` | Get A-share monthly bars | `ts_code`, `trade_date`, `start_date` |
| `stk_weekly_monthly` | Get daily-updated weekly/monthly bars | `ts_code`, `trade_date`, `freq` |
| `stk_week_month_adj` | Get daily-updated adjusted weekly/monthly bars | `ts_code`, `trade_date`, `freq`, `adj` |
| `adj_factor` | Get adjustment factors | `ts_code`, `trade_date` |
| `daily_basic` | Get key daily fundamentals, including PE, PB, shares, and market cap | `ts_code`, `trade_date` |
| `stk_limit` | Get daily limit-up / limit-down prices for stocks | `ts_code`, `trade_date` |
| `suspend_d` | Get daily trading suspension / resumption data | `ts_code`, `trade_date`, `suspend_type` |
| `bak_daily` | Get backup market data with selected technical indicators | `trade_date`, `ts_code` |

## 3. Market Data (Real-Time Daily K) (1 API)

| API Name | Description | Key Params |
|---|---|---|
| `rt_k` | Get real-time daily K-line data for Shanghai, Shenzhen, and Beijing markets, with wildcard batch support (up to 6000 rows per call) | `ts_code` (supports wildcards such as `6*.SH`, `3*.SZ`) |

## 4. Stock Connect Market Data (4 APIs)

| API Name | Description | Key Params |
|---|---|---|
| `ggt_daily` | Get daily Hong Kong Stock Connect turnover statistics | `trade_date` |
| `ggt_monthly` | Get monthly Hong Kong Stock Connect turnover statistics | `month` |
| `ggt_top10` | Get daily Hong Kong Stock Connect turnover details for Shanghai and Shenzhen channels | `trade_date`, `market_type` |
| `hsgt_top10` | Get top-10 daily turnover details for Shanghai Stock Connect and Shenzhen Stock Connect | `trade_date`, `market_type` |

## 5. Financial Data (9 APIs)

| API Name | Description | Key Params |
|---|---|---|
| `income` | Get listed company income statements | `ts_code`, `period`, `report_type` |
| `balancesheet` | Get listed company balance sheets | `ts_code`, `period`, `report_type` |
| `cashflow` | Get listed company cash flow statements | `ts_code`, `period`, `report_type` |
| `forecast` | Get earnings forecasts | `ts_code`, `ann_date`, `period` |
| `express` | Get earnings express reports | `ts_code`, `end_date`, `ann_date` |
| `fina_indicator` | Get listed company financial indicators | `ts_code`, `period` |
| `fina_audit` | Get financial audit opinions | `ts_code`, `ann_date`, `period` |
| `fina_mainbz` | Get listed company main business composition | `ts_code`, `period`, `type` |
| `disclosure_date` | Get financial report disclosure dates | `pre_date`, `end_date` |

## 6. Reference Data (Shareholders / Pledges / Unlocks) (11 APIs)

| API Name | Description | Key Params |
|---|---|---|
| `top10_holders` | Get top 10 shareholders | `ts_code`, `period` |
| `top10_floatholders` | Get top 10 floating shareholders | `ts_code`, `period` |
| `pledge_stat` | Get equity pledge statistics | `ts_code`, `end_date` |
| `pledge_detail` | Get equity pledge details | `ts_code` |
| `repurchase` | Get listed company share repurchase data | `ann_date`, `start_date`, `end_date` |
| `share_float` | Get restricted-share unlock data | `ts_code`, `ann_date` |
| `block_trade` | Get block trade data | `ts_code`, `trade_date` |
| `stk_account` | Get A-share account opening counts (CSDC) | `date`, `start_date`, `end_date` |
| `stk_account_old` | Get A-share account opening counts, legacy version (pre-2019) | `date` |
| `stk_holdernumber` | Get listed company shareholder counts | `ts_code`, `enddate` |
| `stk_holdertrade` | Get insider and executive shareholding changes | `ts_code`, `ann_date` |

## 7. Dragon Tiger List Data (6 APIs)

| API Name | Description | Key Params |
|---|---|---|
| `top_list` | Get daily Dragon Tiger list details | `trade_date` |
| `top_inst` | Get institutional trading details from the Dragon Tiger list | `trade_date` |
| `limit_list_ths` | Get daily limit-up / limit-down statistics from Tonghuashun | `trade_date`, `limit_type` |
| `limit_list_d` | Get daily limit-up, limit-down, and failed board-break statistics | `trade_date`, `limit_type` |
| `limit_step` | Get consecutive limit-up ladder statistics | `trade_date`, `start_date`, `end_date` |
| `limit_cpt_list` | Get the strongest limit-up concepts / industries | `trade_date` |

## 8. Margin Trading & Securities Lending Data (7 APIs)

| API Name | Description | Key Params |
|---|---|---|
| `margin` | Get margin trading and securities lending summary data | `trade_date`, `exchange_id` |
| `margin_detail` | Get margin trading and securities lending detail data | `trade_date`, `ts_code` |
| `margin_secs` | Get eligible margin trading and securities lending securities | `ts_code` |
| `slb_len` | Get securities borrowing data under the refinancing program | `trade_date`, `ts_code` |
| `slb_sec` | Get refinancing program eligible securities | `ts_code` |
| `slb_sec_detail` | Get refinancing program security details | `trade_date`, `ts_code` |
| `slb_len_mm` | Get monthly securities borrowing data under the refinancing program | `month`, `ts_code` |

## 9. Money Flow Data (8 APIs)

| API Name | Description | Key Params |
|---|---|---|
| `moneyflow` | Get stock-level money flow data | `ts_code`, `trade_date` |
| `moneyflow_ths` | Get Tonghuashun stock-level money flow data | `ts_code`, `trade_date` |
| `moneyflow_dc` | Get Eastmoney stock-level money flow data | `ts_code`, `trade_date` |
| `moneyflow_cnt_ths` | Get Tonghuashun concept money flow data | `trade_date` |
| `moneyflow_ind_ths` | Get Tonghuashun industry money flow data | `trade_date` |
| `moneyflow_ind_dc` | Get Eastmoney industry money flow data | `trade_date` |
| `moneyflow_mkt_dc` | Get Eastmoney market-wide money flow data | `trade_date` |
| `moneyflow_hsgt` | Get Stock Connect money flow data | `trade_date`, `start_date`, `end_date` |

## 10. Concept / Sector Data (11 APIs)

| API Name | Description | Key Params |
|---|---|---|
| `ths_index` | Get Tonghuashun concept and industry indices | `exchange`, `type` |
| `ths_daily` | Get Tonghuashun concept and industry index market data | `ts_code`, `trade_date` |
| `ths_member` | Get Tonghuashun concept constituent stocks | `ts_code` |
| `dc_index` | Get Eastmoney concept indices | `exchange`, `type` |
| `dc_member` | Get Eastmoney concept constituent stocks | `ts_code` (must use the code returned by `dc_index`, such as `BK1644.DC`) |
| `dc_daily` | Get Eastmoney concept index market data | `ts_code`, `trade_date` |
| `tdx_index` | Get Tongdaxin sector indices | `exchange`, `type` |
| `tdx_member` | Get Tongdaxin sector constituents | `ts_code` |
| `tdx_daily` | Get Tongdaxin sector index market data | `ts_code`, `trade_date` |
| `kpl_list` | Get hot stocks, strong stocks, consecutive limit-up names, unusual movers, high-priced stocks, etc. | `list_type` |
| `kpl_concept_cons` | Get KPL concept constituents | `concept_id` |

## 11. Specialty Data (15 APIs)

| API Name | Description | Key Params |
|---|---|---|
| `report_rc` | Get broker morning meeting reports | `report_date`, `start_date`, `end_date` |
| `cyq_perf` | Get recent daily performance data for a stock | `ts_code`, `trade_date` |
| `cyq_chips` | Get chip distribution data | `ts_code`, `trade_date` |
| `stk_factor_pro` | Get professional factors, including momentum, volatility, valuation, and financial factors | `ts_code`, `trade_date` |
| `ccass_hold` | Get CCASS holding statistics | `ts_code`, `trade_date` |
| `ccass_hold_detail` | Get CCASS holding details | `trade_date`, `hk_code` |
| `hk_hold` | Get Stock Connect holdings for Hong Kong shares | `code`, `trade_date` |
| `stk_nineturn` | Get TD Sequential / nine-turn sequence data | `ts_code`, `trade_date` |
| `stk_ah_comparison` | Get A/H share price comparison data | `ts_code`, `trade_date` |
| `stk_surv` | Get listed company investor research / survey data | `ts_code`, `surv_date` |
| `broker_recommend` | Get broker stock ratings | `month` |
| `hm_list` | Get active trading desks / Dragon Tiger list seats | `list_type` |
| `hm_detail` | Get active trading desk appearance details | `trade_date`, `ribo_code` |
| `ths_hot` | Get Tonghuashun App hot ranking data | `type` |
| `dc_hot` | Get Eastmoney App hot ranking data | `type` |

## 12. ETF Data (5 APIs)

| API Name | Description | Key Params |
|---|---|---|
| `etf_basic` | Get ETF basic information | `market` |
| `etf_index` | Get the index tracked by an ETF | `ts_code` |
| `fund_daily` | Get exchange-traded fund daily bars | `ts_code`, `trade_date` |
| `fund_adj` | Get exchange-traded fund adjustment factors | `ts_code`, `trade_date` |
| `etf_share_size` | Get ETF shares outstanding and asset size | `trade_date`, `fund_type` |

## 13. Index Data (15 APIs)

| API Name | Description | Key Params |
|---|---|---|
| `index_basic` | Get index basic information | `market`, `publisher`, `category` |
| `index_daily` | Get index daily bars | `ts_code`, `trade_date` |
| `index_weekly` | Get index weekly bars | `ts_code`, `trade_date` |
| `index_monthly` | Get index monthly bars | `ts_code`, `trade_date` |
| `index_weight` | Get index constituents and weights | `index_code`, `trade_date` |
| `index_dailybasic` | Get daily fundamental indicators for broad market indices | `trade_date` |
| `index_classify` | Get index classifications | `index_code`, `level` |
| `index_member_all` | Get all index constituents | `index_code` |
| `sw_daily` | Get Shenwan industry index market data | `ts_code`, `trade_date` |
| `ci_index_member` | Get CNI industry index constituents | `index_code` |
| `ci_daily` | Get CNI industry index market data | `ts_code`, `trade_date` |
| `index_global` | Get major global indices | `ts_code`, `trade_date` |
| `idx_factor_pro` | Get professional index factors | `ts_code`, `trade_date` |
| `daily_info` | Get Shanghai Stock Exchange daily statistics | `trade_date` |
| `sz_daily_info` | Get Shenzhen Stock Exchange daily statistics | `trade_date` |

## 14. Mutual Fund Data (10 APIs)

| API Name | Description | Key Params |
|---|---|---|
| `fund_basic` | Get mutual fund list data | `market`, `status` |
| `fund_company` | Get mutual fund company list data | `name` |
| `fund_manager` | Get mutual fund manager data | `ts_code`, `name` |
| `fund_share` | Get mutual fund share data | `ts_code`, `trade_date` |
| `fund_nav` | Get mutual fund NAV data | `ts_code`, `nav_date` |
| `fund_div` | Get mutual fund dividend data | `ann_date`, `ex_date` |
| `fund_portfolio` | Get mutual fund holdings data | `ts_code`, `end_date` |
| `fund_factor_pro` | Get professional mutual fund factors | `ts_code`, `trade_date` |
| `fund_sales_ratio` | Get mutual fund sales institutions | `fund_code` |
| `fund_sales_vol` | Get mutual fund sales scale data | `fund_code`, `start_date` |

## 15. Futures Data (12 APIs)

| API Name | Description | Key Params |
|---|---|---|
| `fut_basic` | Get futures contract basic information | `exchange`, `fut_type` |
| `trade_cal` | Get futures trading calendar data | `exchange` |
| `fut_daily` | Get futures daily bars | `trade_date`, `ts_code` |
| `fut_weekly_monthly` | Get futures weekly/monthly bars | `trade_date`, `ts_code`, `freq` |
| `ft_mins` | Get futures historical minute bars | `ts_code`, `freq` |
| `fut_wsr` | Get warehouse receipt daily reports | `trade_date`, `exchange` |
| `fut_settle` | Get futures settlement parameters | `trade_date`, `exchange` |
| `fut_holding` | Get futures open interest data | `trade_date`, `symbol` |
| `index_daily` | Get Nanhua commodity index market data | `ts_code`, `trade_date` |
| `fut_mapping` | Get mapping between main futures contracts and continuous contracts | `trade_date`, `ts_code` |
| `fut_weekly_detail` | Get weekly futures position details | `week`, `exchange` |
| `ft_limit` | Get futures daily price limits | `trade_date`, `exchange` |

## 16. Spot Data (Shanghai Gold Exchange) (2 APIs)

| API Name | Description | Key Params |
|---|---|---|
| `sge_basic` | Get Shanghai Gold Exchange contract list | `classify` |
| `sge_daily` | Get Shanghai Gold Exchange daily bars | `ts_code`, `trade_date` |

## 17. Options Data (3 APIs)

| API Name | Description | Key Params |
|---|---|---|
| `opt_basic` | Get option contract information | `exchange`, `ts_code` |
| `opt_daily` | Get option daily bars | `trade_date`, `ts_code` |
| `opt_mins` | Get option minute bars | `ts_code`, `freq` |

## 18. Bond Data (13 APIs)

| API Name | Description | Key Params |
|---|---|---|
| `cb_basic` | Get convertible bond basic information | `ts_code` |
| `cb_issue` | Get convertible bond issuance data | `ann_date` |
| `cb_call` | Get convertible bond conversion / put / redemption data | `ts_code` |
| `cb_rate` | Get convertible bond coupon rate data | `ts_code` |
| `cb_daily` | Get convertible bond daily bars | `ts_code`, `trade_date` |
| `cb_factor_pro` | Get professional convertible bond factors | `ts_code`, `trade_date` |
| `cb_share` | Get convertible bond conversion results | `ts_code` |
| `repo_daily` | Get bond repo daily bars | `ts_code`, `trade_date` |
| `bc_otcqt` | Get Beijing Financial Assets Exchange bond quotes | `trade_date` |
| `bc_bestotcqt` | Get best bond quotes from the Beijing Financial Assets Exchange | `trade_date` |
| `bond_blk` | Get bond market block trade data | `trade_date` |
| `bond_blk_detail` | Get bond market block trade details | `trade_date` |
| `eco_cal` | Get economic calendar data | `date` |

## 19. FX Data (2 APIs)

| API Name | Description | Key Params |
|---|---|---|
| `fx_obasic` | Get FX basic information | `classify` |
| `fx_daily` | Get FX daily bars | `ts_code`, `trade_date` |

## 20. Hong Kong Stock Data (4 APIs)

| API Name | Description | Key Params |
|---|---|---|
| `hk_basic` | Get Hong Kong stock list data | `list_status` |
| `hk_tradecal` | Get Hong Kong stock trading calendar data | `start_date`, `end_date` |
| `hk_daily_adj` | Get adjusted Hong Kong stock market data | `ts_code`, `trade_date`, `adj` |
| `hk_mins` | Get Hong Kong stock minute bars | `ts_code`, `freq` |

## 21. U.S. Stock Data (3 APIs)

| API Name | Description | Key Params |
|---|---|---|
| `us_basic` | Get U.S. stock list data | `name` |
| `us_tradecal` | Get U.S. stock trading calendar data | `start_date`, `end_date` |
| `us_daily` | Get U.S. stock daily bars | `ts_code`, `trade_date` |

## 22. Industry & TMT Economics (3 APIs)

| API Name | Description | Key Params |
|---|---|---|
| `tmt_twincome` | Get monthly revenue data for Taiwan's electronics industry | `date`, `item` |
| `tmt_twincomedetail` | Get detailed monthly revenue data for Taiwan's electronics industry (parameter format to be confirmed) | `date`, `item` |
| `teleplay_record` | Get TV drama filing / registration data | `ann_date` |

## 23. Macroeconomic Data (18 APIs)

| API Name | Description | Key Params |
|---|---|---|
| `shibor` | Get Shibor rates | `date` |
| `shibor_quote` | Get Shibor quote data | `date` |
| `shibor_lpr` | Get LPR loan prime rates | `date` |
| `libor` | Get Libor rates | `date` |
| `hibor` | Get Hibor rates | `date` |
| `wz_index` | Get Wenzhou private lending rates | `month` |
| `gz_index` | Get Guangzhou private lending rates | `month` |
| `cn_gdp` | Get China GDP data | `quarter` |
| `cn_cpi` | Get China CPI data | `month` |
| `cn_ppi` | Get China PPI data | `month` |
| `cn_m` | Get China money supply data | `month` |
| `sf_month` | Get China total social financing data | `month` |
| `cn_pmi` | Get China PMI data | `month` |
| `us_tycr` | Get U.S. Treasury yield curve data | `date` |
| `us_trycr` | Get U.S. Treasury yield curve data for more maturities | `date` |
| `us_tbr` | Get U.S. Treasury short-term rates | `date` |
| `us_tltr` | Get U.S. Treasury long-term rates | `date` |
| `us_trltr` | Get U.S. Treasury real long-term rates | `date` |

## 24. Interactive Q&A Data (2 APIs)

| API Name | Description | Key Params |
|---|---|---|
| `irm_qa_sh` | Get Q&A data from the Shanghai Stock Exchange interactive platform | `ts_code`, `start_date` |
| `irm_qa_sz` | Get Q&A data from the Shenzhen Stock Exchange interactive platform | `ts_code`, `start_date` |
