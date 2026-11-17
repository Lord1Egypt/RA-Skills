# TWSE API - Warrants <!-- 權證 -->

Call/put warrant issuance and trading statistics. See also `/opendata/t187ap37_L` (warrant basic data) in securities-trading.md. All endpoints: `GET https://openapi.twse.com.tw/v1<path>`, no parameters, JSON array response.

| Endpoint | Description |
|---|---|
| `/opendata/t187ap36_L` | Annual call/put warrant issuance statistics |
| `/opendata/t187ap43_L` | Call/put warrant trader counts |
| `/opendata/t187ap42_L` | Daily call/put warrant trading data |

---

## `GET /opendata/t187ap36_L`
Annual call/put warrant issuance statistics  <!-- 上市認購(售)權證年度發行量概況統計表 -->

Response item fields (exact JSON keys):
`出表日期`, `發行人代號`, `發行人名稱`, `權證代號`, `名稱`, `標的代號`, `標的名稱`, `申請發行日期`

## `GET /opendata/t187ap43_L`
Call/put warrant trader counts  <!-- 上市認購(售)權證交易人數檔 -->

Response item fields (exact JSON keys):
`出表日期`, `日期`, `人數`

## `GET /opendata/t187ap42_L`
Daily call/put warrant trading data  <!-- 上市認購(售)權證每日成交資料檔 -->

Response item fields (exact JSON keys):
`出表日期`, `交易日期`, `權證代號`, `權證名稱`, `成交金額`, `成交張數`
