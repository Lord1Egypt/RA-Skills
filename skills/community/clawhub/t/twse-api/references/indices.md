# TWSE API - Indices <!-- 指數 -->

TAIEX and other index historical data. All endpoints: `GET https://openapi.twse.com.tw/v1<path>`, no parameters, JSON array response.

| Endpoint | Description |
|---|---|
| `/exchangeReport/MI_INDEX4` | Daily TWSE/TPEx cross-market trading information |
| `/indicesReport/FRMSA` | Formosa Index historical data |
| `/indicesReport/TAI50I` | Taiwan 50 Index historical data |
| `/indicesReport/MI_5MINS_HIST` | TAIEX (weighted index) historical daily OHLC |
| `/indicesReport/MFI94U` | TAIEX Total Return Index |

---

## `GET /exchangeReport/MI_INDEX4`
Daily TWSE/TPEx cross-market trading information  <!-- 每日上市上櫃跨市場成交資訊 -->

Response item fields (exact JSON keys):
`Date`, `TradeValue`, `FormosaIndex`, `Change`

## `GET /indicesReport/FRMSA`
Formosa Index historical data  <!-- 寶島股價指數歷史資料 -->

Response item fields (exact JSON keys):
`Date`, `FormosaIndex`, `FormosaTotalReturnIndex`

## `GET /indicesReport/TAI50I`
Taiwan 50 Index historical data  <!-- 臺灣 50 指數歷史資料 -->

Response item fields (exact JSON keys):
`Date`, `Taiwan50Index`, `Taiwan50TotalReturnIndex`

## `GET /indicesReport/MI_5MINS_HIST`
TAIEX (weighted index) historical daily OHLC  <!-- 發行量加權股價指數歷史資料 -->

Response item fields (exact JSON keys):
`Date`, `OpeningIndex`, `HighestIndex`, `LowestIndex`, `ClosingIndex`

## `GET /indicesReport/MFI94U`
TAIEX Total Return Index  <!-- 發行量加權股價報酬指數 -->

Response item fields (exact JSON keys):
`Date`, `TAIEXTotalReturnIndex`
