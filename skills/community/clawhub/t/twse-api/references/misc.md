# TWSE API - Miscellaneous <!-- 其他 -->

TWSE news, events, bond data, funds. All endpoints: `GET https://openapi.twse.com.tw/v1<path>`, no parameters, JSON array response.

| Endpoint | Description |
|---|---|
| `/opendata/t187ap47_L` | Fund basic data summary |
| `/news/eventList` | TWSE event announcements |
| `/news/newsList` | TWSE news |
| `/exchangeReport/BFI61U` | Central government bond interest compensation table |

---

## `GET /opendata/t187ap47_L`
Fund basic data summary  <!-- 基金基本資料彙總表 -->

Response item fields (exact JSON keys):
`出表日期`, `基金代號`, `基金簡稱`, `基金類型`, `基金中文名稱`, `基金英文名稱`, `標的指數/追蹤指數名稱`, `標的指數是否為客製化或需揭露相關資訊之指數`, `股票及債券投資比例說明`, `是否設有績效指標`, `績效指標中文名稱`, `績效指標英文名稱`, `是否包含國外成分股`, `基金統一編號`, `成立日期`, `上市日期`, `基金經理人`, `經理公司總機`, `經理公司地址`, `經理公司董事長`, `經理公司發言人`, `經理公司總經理`, `經理公司代理發言人`, `總代理人`, `發行單位數/轉換數`, `保管機構`, `保管機構電話`, `保管機構地址`, `備註`

## `GET /news/eventList`
TWSE event announcements  <!-- 證交所活動訊息 -->

Response item fields (exact JSON keys):
`No`, `Title`, `Details`

## `GET /news/newsList`
TWSE news  <!-- 證交所新聞 -->

Response item fields (exact JSON keys):
`Title`, `Url`, `Date`

## `GET /exchangeReport/BFI61U`
Central government bond interest compensation table  <!-- 中央登錄公債補息資料表 -->

Response item fields (exact JSON keys):
`Code`, `Name`, `IssuedDate`, `StartingDate`, `CouponRate`, `DailyAccInterest`
