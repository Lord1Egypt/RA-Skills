# TWSE API - Broker Data <!-- 券商資料 -->

Securities firm (broker) directories, personnel and financial statistics. All endpoints: `GET https://openapi.twse.com.tw/v1<path>`, no parameters, JSON array response.

| Endpoint | Description |
|---|---|
| `/ETFReport/ETFRank` | Regular savings plan account count - monthly ranking |
| `/brokerService/secRegData` | Brokers offering regular savings plan (dollar-cost averaging) services |
| `/brokerService/brokerList` | Securities firm head-office basic data |
| `/opendata/t187ap01` | Securities firm personnel count by business type |
| `/opendata/t187ap20` | Securities firm monthly statements |
| `/opendata/t187ap21` | Securities firm income and expense summary |
| `/opendata/t187ap18` | Securities firm basic data |
| `/opendata/OpenData_BRK01` | Securities firm sales agents count by gender |
| `/opendata/OpenData_BRK02` | Securities firm branch office basic data |

---

## `GET /ETFReport/ETFRank`
Regular savings plan account count - monthly ranking  <!-- 定期定額交易戶數統計排行月報表 -->

Response item fields (exact JSON keys):
`No`, `STOCKsSecurityCode`, `STOCKsName`, `STOCKsNumberofTradingAccounts`, `ETFsSecurityCode`, `ETFsName`, `ETFsNumberofTradingAccounts`

## `GET /brokerService/secRegData`
Brokers offering regular savings plan (dollar-cost averaging) services  <!-- 開辦定期定額業務證券商名單 -->

Response item fields (exact JSON keys):
`SecuritiesFirmCode`, `Name`, `BrokerageBusinessStartingDate`, `WealthManagementBusinessStartingDate`

## `GET /brokerService/brokerList`
Securities firm head-office basic data  <!-- 證券商總公司基本資料 -->

Response item fields (exact JSON keys):
`Code`, `Name`, `EstablishmentDate`, `Address`, `Telephone`

## `GET /opendata/t187ap01`
Securities firm personnel count by business type  <!-- 券商業務別人員數 -->

Response item fields (exact JSON keys):
`出表日期`, `職位`, `受託買賣`, `受託買賣（衍生性商品銷售）`, `內部稽核`, `融資融券`, `證券借貸`, `自行買賣`, `其他人員`, `結算交割`, `股務人員`, `承銷人員`, `法令遵循`, `風險管理-模型管理`, `驗證人員-模型管理`, `內部稽核-模型管理`, `共同行銷`, `合作推廣`, `開戶`, `徵信`, `營業櫃檯輸單`, `主辦會計`, `財富管理`, `風險管理-其他`, `公司治理人員`, `受託管理私募股權基金人員`, `基金買賣及互易`, `數位服務（數位體驗專區）`, `數位服務（客戶服務中心）`, `合計`

## `GET /opendata/t187ap20`
Securities firm monthly statements  <!-- 各券商每月月計表 -->

Response item fields (exact JSON keys):
`出表日期`, `券商代號`, `券商名稱`, `科目`, `會計科目名稱`, `本月借方總額`, `本月貸方總額`, `借方餘額`

## `GET /opendata/t187ap21`
Securities firm income and expense summary  <!-- 各券商收支概況表資料 -->

Response item fields (exact JSON keys):
`出表日期`, `券商代號`, `券商名稱`, `科目`, `會計科目名稱`, `本月金額`, `累進金額`

## `GET /opendata/t187ap18`
Securities firm basic data  <!-- 證券商基本資料 -->

Response item fields (exact JSON keys):
`出表日期`, `證券代號`, `券商(證券IB)簡稱`, `登記資本額（仟元）`, `實收資本額（仟元）`, `指撥營運金（仟元）`, `營利事業統一編號`, `變更日期`, `區域代碼`, `融資融券開辦日期`, `設立日期`, `開業日期`, `電話`, `傳真`, `交割金融機構`, `交割專戶帳號`, `違約專戶`, `錯帳專戶帳號`, `權證履約專戶帳號`, `代辦交割證券商(證券IB)代號`, `營業保證金保管銀行`, `發行狀況`, `業務種類`, `負責人`, `總經理`, `營業部經理`, `財務部經理`, `行政部門地址`, `營業處所－經`, `營業處所－經代表號`, `營業廳`, `營業處所－自`, `營業處所－自代表號`, `營業處所－承`, `營業處所－承代表號`, `股務代理商地址`, `備註`, `營業項目1`, `營業項目2`, `營業項目3`, `營業項目4`, `營業項目5`, `營業項目6`, `營業項目7`, `營業項目8`, `營業項目9`, `營業項目10`, `營業項目11`, `營業項目12`, `營業項目13`, `營業項目14`, `營業項目15`, `營業項目16`, `營業項目17`, `營業項目18`, `營業項目19`, `營業項目20`, `營業項目21`, `營業項目22`, `營業項目23`, `營業項目24`, `營業項目25`, `營業項目26`, `營業項目27`, `營業項目28`, `營業項目29`, `營業項目30`, `營業項目31`

## `GET /opendata/OpenData_BRK01`
Securities firm sales agents count by gender  <!-- 證券商營業員男女人數統計資料 -->

Response item fields (exact JSON keys):
`出表日期`, `證券商代號`, `男性員工人數`, `女性員工人數`, `總人數`

## `GET /opendata/OpenData_BRK02`
Securities firm branch office basic data  <!-- 證券商分公司基本資料 -->

Response item fields (exact JSON keys):
`出表日期`, `證券商代號`, `證券商名稱`, `開業日`, `地址`, `電話`
