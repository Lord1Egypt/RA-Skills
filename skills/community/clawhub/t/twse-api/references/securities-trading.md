# TWSE API - Securities Trading <!-- 證券交易 -->

Daily quotes, market summaries, valuation ratios (P/E, yield, P/B), margin balances, block trades, day trading, attention/disposition stocks, and the market calendar. All endpoints: `GET https://openapi.twse.com.tw/v1<path>`, no parameters, JSON array response.

| Endpoint | Description |
|---|---|
| `/exchangeReport/BWIBBU_ALL` | P/E ratio, dividend yield and P/B ratio of all listed stocks (latest, by code) |
| `/exchangeReport/STOCK_DAY_AVG_ALL` | Daily closing price and monthly average price for all listed stocks |
| `/exchangeReport/STOCK_DAY_ALL` | Daily OHLC trading data for all listed stocks |
| `/exchangeReport/FMSRFK_ALL` | Monthly trading summary per listed stock |
| `/exchangeReport/FMNPTK_ALL` | Yearly trading summary per listed stock |
| `/exchangeReport/MI_INDEX` | Daily closing quotes - market index summary |
| `/fund/MI_QFIIS_cat` | Foreign & mainland-China investor shareholding ratio by sector |
| `/fund/MI_QFIIS_sort_20` | Top 20 stocks by foreign & mainland-China investor shareholding |
| `/exchangeReport/TWT88U` | New listings within first 5 days (no price limit) |
| `/Announcement/BFZFZU_T` | Stocks abnormally promoted by investment TV/media programs |
| `/exchangeReport/TWTB4U` | Day-trading eligible stocks and daily statistics |
| `/exchangeReport/TWTBAU1` | Advance notice: suspension of sell-first day trading |
| `/exchangeReport/TWTBAU2` | History: suspension of sell-first day trading |
| `/exchangeReport/MI_5MINS` | Order/trade statistics every 5 seconds |
| `/exchangeReport/FMTQIK` | Daily whole-market trading summary (volume, value, TAIEX) |
| `/exchangeReport/MI_INDEX20` | Top 20 securities by daily trading volume |
| `/exchangeReport/TWT53U` | Odd-lot trading quotes |
| `/exchangeReport/TWTAWU` | Suspended-trading securities |
| `/exchangeReport/BFT41U` | After-hours fixed-price trading |
| `/exchangeReport/BFI84U` | Advance notice of margin-trading (financing / short-sale) suspension |
| `/exchangeReport/MI_MARGN` | Margin trading (financing and short-sale) balances |
| `/block/BFIAUU_d` | Block trading volume/value statistics (daily) |
| `/block/BFIAUU_m` | Block trading volume/value statistics (monthly) |
| `/block/BFIAUU_y` | Block trading volume/value statistics (yearly) |
| `/exchangeReport/STOCK_FIRST` | Daily trading of primary-listed foreign stocks |
| `/exchangeReport/TWT85U` | Securities placed under altered trading method |
| `/holidaySchedule/holidaySchedule` | Market open/holiday schedule |
| `/exchangeReport/BWIBBU_d` | P/E ratio, dividend yield and P/B ratio (by date) |
| `/SBL/TWT96U` | Shares available today for SBL short sale (TWSE and TPEx) |
| `/exchangeReport/TWT84U` | Daily price fluctuation limits per stock |
| `/opendata/twtazu_od` | Advance/decline statistics (number of rising/falling securities) |
| `/opendata/t187ap19` | Electronic trading statistics |
| `/opendata/t187ap37_L` | Listed warrant basic data summary |
| `/announcement/notetrans` | Attention-stock cumulative count of abnormal criteria |
| `/announcement/notice` | Today's announced attention stocks |
| `/exchangeReport/TWT48U_ALL` | Ex-dividend / ex-rights advance notice |

---

## `GET /exchangeReport/BWIBBU_ALL`
P/E ratio, dividend yield and P/B ratio of all listed stocks (latest, by code)  <!-- 上市個股日本益比、殖利率及股價淨值比（依代碼查詢） -->

Response item fields (exact JSON keys):
`Date`, `Code`, `Name`, `PEratio`, `DividendYield`, `PBratio`

## `GET /exchangeReport/STOCK_DAY_AVG_ALL`
Daily closing price and monthly average price for all listed stocks  <!-- 上市個股日收盤價及月平均價 -->

Response item fields (exact JSON keys):
`Date`, `Code`, `Name`, `ClosingPrice`, `MonthlyAveragePrice`

## `GET /exchangeReport/STOCK_DAY_ALL`
Daily OHLC trading data for all listed stocks  <!-- 上市個股日成交資訊 -->

Response item fields (exact JSON keys):
`Date`, `Code`, `Name`, `TradeVolume`, `TradeValue`, `OpeningPrice`, `HighestPrice`, `LowestPrice`, `ClosingPrice`, `Change`, `Transaction`

## `GET /exchangeReport/FMSRFK_ALL`
Monthly trading summary per listed stock  <!-- 上市個股月成交資訊 -->

Response item fields (exact JSON keys):
`Month`, `Code`, `Name`, `HighestPrice`, `LowestPrice`, `WeightedAvgPriceAB`, `Transaction`, `TradeValueA`, `TradeVolumeB`, `TurnoverRatio`

## `GET /exchangeReport/FMNPTK_ALL`
Yearly trading summary per listed stock  <!-- 上市個股年成交資訊 -->

Response item fields (exact JSON keys):
`Year`, `Code`, `Name`, `TradeVolume`, `TradeValue`, `Transaction`, `HighestPrice`, `HDate`, `LowestPrice`, `LDate`, `AvgClosingPrice`

## `GET /exchangeReport/MI_INDEX`
Daily closing quotes - market index summary  <!-- 每日收盤行情-大盤統計資訊 -->

Response item fields (exact JSON keys):
`日期`, `指數`, `收盤指數`, `漲跌`, `漲跌點數`, `漲跌百分比`, `特殊處理註記`

## `GET /fund/MI_QFIIS_cat`
Foreign & mainland-China investor shareholding ratio by sector  <!-- 集中市場外資及陸資投資類股持股比率表 -->

Response item fields (exact JSON keys):
`IndustryCat`, `Numbers`, `ShareNumber`, `ForeignMainlandAreaShare`, `Percentage`

## `GET /fund/MI_QFIIS_sort_20`
Top 20 stocks by foreign & mainland-China investor shareholding  <!-- 集中市場外資及陸資持股前 20 名彙總表 -->

Response item fields (exact JSON keys):
`Rank`, `Code`, `Name`, `ShareNumber`, `AvailableShare`, `SharesHeld`, `AvailableInvestPer`, `SharesHeldPer`, `Upperlimit`

## `GET /exchangeReport/TWT88U`
New listings within first 5 days (no price limit)  <!-- 上市個股首五日無漲跌幅 -->

Response item fields (exact JSON keys):
`SecurCode`, `SecurName`, `1stTradingDate`, `5thTradingDate`, `PriceUnderwritten`, `OverAllotmentShares`, `Code`, `Name`, `BuySell`, `TradingPrice`, `TradingVolume`, `AccTradingVolume`

## `GET /Announcement/BFZFZU_T`
Stocks abnormally promoted by investment TV/media programs  <!-- 投資理財節目異常推介個股 -->

Response item fields (exact JSON keys):
`Number`, `Code`, `Name`, `Date`

## `GET /exchangeReport/TWTB4U`
Day-trading eligible stocks and daily statistics  <!-- 上市股票每日當日沖銷交易標的及統計 -->

Response item fields (exact JSON keys):
`Date`, `Code`, `Name`, `Suspension`

## `GET /exchangeReport/TWTBAU1`
Advance notice: suspension of sell-first day trading  <!-- 集中市場暫停先賣後買當日沖銷交易標的預告表 -->

Response item fields (exact JSON keys):
`Code`, `Name`, `StartDate`, `EndDate`, `Reason`

## `GET /exchangeReport/TWTBAU2`
History: suspension of sell-first day trading  <!-- 集中市場暫停先賣後買當日沖銷交易歷史查詢 -->

Response item fields (exact JSON keys):
`Code`, `Name`, `StartDate`, `EndDate`, `Reason`

## `GET /exchangeReport/MI_5MINS`
Order/trade statistics every 5 seconds  <!-- 每 5 秒委託成交統計 -->

Response item fields (exact JSON keys):
`Time`, `AccBidOrders`, `AccBidVolume`, `AccAskOrders`, `AccAskVolume`, `AccTransaction`, `AccTradeVolume`, `AccTradeValue`

## `GET /exchangeReport/FMTQIK`
Daily whole-market trading summary (volume, value, TAIEX)  <!-- 集中市場每日市場成交資訊 -->

Response item fields (exact JSON keys):
`Date`, `TradeVolume`, `TradeValue`, `Transaction`, `TAIEX`, `Change`

## `GET /exchangeReport/MI_INDEX20`
Top 20 securities by daily trading volume  <!-- 集中市場每日成交量前二十名證券 -->

Response item fields (exact JSON keys):
`Date`, `Rank`, `Code`, `Name`, `TradeVolume`, `Transaction`, `OpeningPrice`, `HighestPrice`, `LowestPrice`, `ClosingPrice`, `Dir`, `Change`, `LastBestBidPrice`, `LastBestAskPrice`

## `GET /exchangeReport/TWT53U`
Odd-lot trading quotes  <!-- 集中市場零股交易行情單 -->

Response item fields (exact JSON keys):
`Code`, `Name`, `TradeVolume`, `Transaction`, `TradeValue`, `TradePrice`, `BestBidPrice`, `BestBidVolume`, `BestAskPrice`, `BestAskVolume`

## `GET /exchangeReport/TWTAWU`
Suspended-trading securities  <!-- 集中市場暫停交易證券 -->

Response item fields (exact JSON keys):
`Number`, `Code`, `Name`, `TradingHaltDate`, `TradingHaltTime`, `TradingResumptionDate`, `TradingResumptionTime`

## `GET /exchangeReport/BFT41U`
After-hours fixed-price trading  <!-- 集中市場盤後定價交易 -->

Response item fields (exact JSON keys):
`Code`, `Name`, `TradeVolume`, `Transaction`, `TradeValue`, `TradePrice`, `BidVolume`, `AskVolume`

## `GET /exchangeReport/BFI84U`
Advance notice of margin-trading (financing / short-sale) suspension  <!-- 集中市場停資停券預告表 -->

Response item fields (exact JSON keys):
`Code`, `Name`, `StartDate`, `EndDate`, `Reason`

## `GET /exchangeReport/MI_MARGN`
Margin trading (financing and short-sale) balances  <!-- 集中市場融資融券餘額 -->

Response item fields (exact JSON keys):
`股票代號`, `股票名稱`, `融資買進`, `融資賣出`, `融資現金償還`, `融資前日餘額`, `融資今日餘額`, `融資限額`, `融券買進`, `融券賣出`, `融券現券償還`, `融券前日餘額`, `融券今日餘額`, `融券限額`, `資券互抵`, `註記`

## `GET /block/BFIAUU_d`
Block trading volume/value statistics (daily)  <!-- 集中市場鉅額交易日成交量值統計 -->

Response item fields (exact JSON keys):
`Date`, `Class`, `Type`, `TradeVolume`, `MarketSharePer`, `TradeValue`

## `GET /block/BFIAUU_m`
Block trading volume/value statistics (monthly)  <!-- 集中市場鉅額交易月成交量值統計 -->

Response item fields (exact JSON keys):
`Month`, `Class`, `TradeVolume`, `MarketSharePer`, `TradeValue`

## `GET /block/BFIAUU_y`
Block trading volume/value statistics (yearly)  <!-- 集中市場鉅額交易年成交量值統計 -->

Response item fields (exact JSON keys):
`Month`, `TradeVolume`, `MarketSharePer`, `TradeValue`

## `GET /exchangeReport/STOCK_FIRST`
Daily trading of primary-listed foreign stocks  <!-- 每日第一上市外國股票成交量值 -->

Response item fields (exact JSON keys):
`Code`, `Name`, `TradeVolume`, `Transaction`, `TradeValue`, `OpeningPrice`, `HighestPrice`, `LowestPrice`, `ClosingPrice`, `Dir`, `Change`, `LastBestBidPrice`, `LastBestBidVolume`, `LastBestAskPrice`, `LastBestAskVolume`, `PriceEarningRatio`

## `GET /exchangeReport/TWT85U`
Securities placed under altered trading method  <!-- 集中市場證券變更交易 -->

Response item fields (exact JSON keys):
`Code`, `Name`, `PeriodicCallAuctionTrading`

## `GET /holidaySchedule/holidaySchedule`
Market open/holiday schedule  <!-- 有價證券集中交易市場開（休）市日期 -->

Response item fields (exact JSON keys):
`Name`, `Date`, `Weekday`, `Description`

## `GET /exchangeReport/BWIBBU_d`
P/E ratio, dividend yield and P/B ratio (by date)  <!-- 上市個股日本益比、殖利率及股價淨值比（依日期查詢） -->

Response item fields (exact JSON keys):
`Date`, `Code`, `Name`, `ClosePrice`, `DividendYield`, `DividendYear`, `PEratio`, `PBratio`, `FiscalYearQuarter`

## `GET /SBL/TWT96U`
Shares available today for SBL short sale (TWSE and TPEx)  <!-- 上市上櫃股票當日可借券賣出股數 -->

Response item fields (exact JSON keys):
`TWSECode`, `TWSEAvailableVolume`, `GRETAICode`, `GRETAIAvailableVolume`

## `GET /exchangeReport/TWT84U`
Daily price fluctuation limits per stock  <!-- 上市個股股價升降幅度 -->

Response item fields (exact JSON keys):
`Code`, `Name`, `TodayLimitUp`, `TodayOpeningRefPrice`, `TodayLimitDown`, `PreviousDayOpeningRefPrice`, `PreviousDayPrice`, `PreviousDayLimitUp`, `PreviousDayLimitDown`, `LastTradingDay`, `AllowOddLotTrade`

## `GET /opendata/twtazu_od`
Advance/decline statistics (number of rising/falling securities)  <!-- 集中市場漲跌證券數統計表 -->

Response item fields (exact JSON keys):
`出表日期`, `類型`, `上漲`, `漲停`, `下跌`, `跌停`, `持平`, `未成交`, `無比價`

## `GET /opendata/t187ap19`
Electronic trading statistics  <!-- 電子式交易統計資訊 -->

Response item fields (exact JSON keys):
`出表日期`, `成交月份`, `本月新增戶數`, `本月註銷戶數`, `累計開戶數`, `本月交易戶數`, `本月交易人數`, `委託筆數`, `委託金額`, `成交筆數`, `成交金額`, `平均每筆成交金額`, `公司總成交筆數`, `公司總成交金額`, `占公司成交比率(筆數)`, `占公司成交比率(金額)`, `市場成交總筆數(買賣合計)`, `市場成交總金額(買賣合計)`, `占市場成交比率(筆數)`, `占市場成交比率(金額)`

## `GET /opendata/t187ap37_L`
Listed warrant basic data summary  <!-- 上市權證基本資料彙總表 -->

Response item fields (exact JSON keys):
`出表日期`, `權證代號`, `權證簡稱`, `權證類型`, `類別`, `流動量提供者報價方式`, `履約開始日`, `最後交易日`, `履約截止日`, `發行單位數量(仟單位)`, `結算方式(詳附註編號說明)`, `標的證券/指數`, `最新標的履約配發數量(每仟單位權證)`, `原始履約價格(元)/履約指數`, `原始上限價格(元)/上限指數`, `原始下限價格(元)/下限指數`, `最新履約價格(元)/履約指數`, `最新上限價格(元)/上限指數`, `最新下限價格(元)/下限指數`, `備註`

## `GET /announcement/notetrans`
Attention-stock cumulative count of abnormal criteria  <!-- 集中市場公布注意累計次數異常資訊 -->

Response item fields (exact JSON keys):
`Code`, `Name`, `RecentlyMetAttentionSecuritiesCriteria`

## `GET /announcement/notice`
Today's announced attention stocks  <!-- 集中市場當日公布注意股票 -->

Response item fields (exact JSON keys):
`Number`, `Code`, `Name`, `NumberOfAnnouncement`, `TradingInfoForAttention`, `Date`, `ClosingPrice`, `PE`

## `GET /exchangeReport/TWT48U_ALL`
Ex-dividend / ex-rights advance notice  <!-- 上市股票除權除息預告表 -->

Response item fields (exact JSON keys):
`Date`, `Code`, `Name`, `Exdividend`, `StockDividendRatio`, `SubscriptionRatio`, `SubscriptionPricePerShare`, `CashDividend`, `SharesOffered`, `SharesEmpOwner`, `SharesholderOwner`, `StockHoldingRatio`
