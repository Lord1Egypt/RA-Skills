# TWSE API - Corporate Governance <!-- 公司治理 -->

Company profiles, insider holdings, board/governance data, material announcements, dividends, and ESG disclosures. All endpoints: `GET https://openapi.twse.com.tw/v1<path>`, no parameters, JSON array response.

| Endpoint | Description |
|---|---|
| `/opendata/t187ap46_L_21` | ESG disclosure - occupational safety and health |
| `/opendata/t187ap45_L` | Dividend distribution of listed companies |
| `/opendata/t187ap46_L_20` | ESG disclosure - anti-competitive litigation |
| `/opendata/t187ap46_L_19` | ESG disclosure - risk management policy |
| `/opendata/t187ap46_L_18` | ESG disclosure - ownership and control |
| `/opendata/t187ap46_L_17` | ESG disclosure - financial inclusion |
| `/opendata/t187ap46_L_16` | ESG disclosure - information security |
| `/opendata/t187ap46_L_15` | ESG disclosure - community relations |
| `/opendata/t187ap46_L_14` | ESG disclosure - product quality and safety |
| `/opendata/t187ap46_L_13` | ESG disclosure - supply chain management |
| `/opendata/t187ap46_L_12` | ESG disclosure - food safety |
| `/opendata/t187ap46_L_11` | ESG disclosure - product lifecycle |
| `/opendata/t187ap46_L_10` | ESG disclosure - fuel management |
| `/opendata/t187ap46_L_9` | ESG disclosure - functional committees |
| `/opendata/t187ap46_L_8` | ESG disclosure - climate-related issues management |
| `/opendata/t187ap05_P` | Monthly operating revenue summary of public companies |
| `/opendata/t187ap46_L_7` | ESG disclosure - investor communication |
| `/opendata/t187ap46_L_6` | ESG disclosure - board of directors |
| `/opendata/t187ap46_L_5` | ESG disclosure - human capital development |
| `/opendata/t187ap46_L_4` | ESG disclosure - waste management |
| `/opendata/t187ap46_L_3` | ESG disclosure - water resource management |
| `/opendata/t187ap46_L_2` | ESG disclosure - energy management |
| `/opendata/t187ap46_L_1` | ESG disclosure - greenhouse gas emissions |
| `/company/applylistingForeign` | Foreign companies applying for TWSE primary listing |
| `/company/newlisting` | Recently listed companies |
| `/company/suspendListingCsvAndHtml` | Delisted (terminated listing) companies |
| `/company/applylistingLocal` | Domestic companies applying for listing |
| `/opendata/t187ap04_L` | Daily material information (major announcements) of listed companies |
| `/opendata/t187ap03_L` | Basic profile of listed companies |
| `/opendata/t187ap02_L` | Major shareholders holding over 10% of listed companies |
| `/opendata/t187ap14_L` | EPS statistics of listed companies by industry |
| `/opendata/t187ap08_L` | Directors/supervisors with shareholding below legal minimum |
| `/opendata/t187ap11_L` | Director/supervisor shareholding balance details (listed companies) |
| `/opendata/t187ap12_L` | Insider share-transfer pre-declarations - shares transferred (daily) |
| `/opendata/t187ap13_L` | Insider share-transfer pre-declarations - shares not yet transferred (daily) |
| `/opendata/t187ap22_L` | FSC Securities and Futures Bureau sanction cases against listed companies |
| `/opendata/t187ap30_L` | Concurrent positions held by independent directors/supervisors |
| `/opendata/t187ap29_A_L` | Director compensation of listed companies |
| `/opendata/t187ap29_B_L` | Supervisor compensation of listed companies |
| `/opendata/t187ap29_C_L` | Director compensation (consolidated financial statements) |
| `/opendata/t187ap29_D_L` | Supervisor compensation (consolidated financial statements) |
| `/opendata/t187ap23_L` | Listed companies violating information-filing / material-info / press-conference rules |
| `/opendata/t187ap03_P` | Basic profile of public (non-listed) companies |
| `/announcement/punish` | Disposition stocks announced (centralized market) |
| `/opendata/t187ap10_L` | Directors/supervisors below legal shareholding for 3+ consecutive months |
| `/opendata/t187ap38_L` | Shareholder meeting convening announcements (since 2006) |
| `/opendata/t187ap24_L` | Change-of-control listed companies |
| `/opendata/t187ap26_L` | Control change + major business-scope change - trading suspended |
| `/opendata/t187ap41_L` | Shareholder meeting date, venue and e-voting adoption |
| `/opendata/t187ap25_L` | Listed companies with major business-scope changes |
| `/opendata/t187ap27_L` | Control change + major business-scope change - placed under altered trading method |
| `/opendata/t187ap32_L` | Corporate governance rules and regulations adopted by listed companies |
| `/opendata/t187ap33_L` | Whether the chairman also serves as general manager (CEO duality) |
| `/opendata/t187ap09_L` | Pledged shares ratio of directors and supervisors |
| `/opendata/t187ap34_L` | Director/supervisor election methods (cumulative voting, nomination system) and results |
| `/opendata/t187ap35_L` | Shareholder proposal rights exercised at listed companies |

---

## `GET /opendata/t187ap46_L_21`
ESG disclosure - occupational safety and health  <!-- 上市公司企業ESG資訊揭露彙總資料-職業安全衛生 -->

Response item fields (exact JSON keys):
`出表日期`, `報告年度`, `公司代號`, `公司名稱`, `職業災害人數及比率-人數`, `職業災害人數及比率-比率`, `火災件數(件)`, `火災死傷人數(人)`, `火災死傷人數占員工總人數比率`

## `GET /opendata/t187ap45_L`
Dividend distribution of listed companies  <!-- 上市公司股利分派情形 -->

Response item fields (exact JSON keys):
`出表日期`, `公司代號`, `公司名稱`, `決議（擬議）進度`, `股利年度`, `股利所屬年(季)度`, `股利所屬期間`, `期別`, `董事會（擬議）股利分派日`, `股東會日期`, `期初未分配盈餘/待彌補虧損(元)`, `本期淨利(淨損)(元)`, `可分配盈餘(元)`, `分配後期末未分配盈餘(元)`, `股東配發-盈餘分配之現金股利(元/股)`, `股東配發-法定盈餘公積發放之現金(元/股)`, `股東配發-資本公積發放之現金(元/股)`, `股東配發-股東配發之現金(股利)總金額(元)`, `股東配發-盈餘轉增資配股(元/股)`, `股東配發-法定盈餘公積轉增資配股(元/股)`, `股東配發-資本公積轉增資配股(元/股)`, `股東配發-股東配股總股數(股)`, `摘錄公司章程-股利分派部分`, `備註`

## `GET /opendata/t187ap46_L_20`
ESG disclosure - anti-competitive litigation  <!-- 上市公司企業ESG資訊揭露彙總資料-反競爭行為法律訴訟 -->

Response item fields (exact JSON keys):
`出表日期`, `報告年度`, `公司代號`, `公司名稱`, `因與反競爭行為條例相關的法律訴訟而造成的金錢損失總額(仟元)`

## `GET /opendata/t187ap46_L_19`
ESG disclosure - risk management policy  <!-- 上市公司企業ESG資訊揭露彙總資料-風險管理政策 -->

Response item fields (exact JSON keys):
`出表日期`, `報告年度`, `公司代號`, `公司名稱`, `重大事件之風險管理政策`, `與使用關鍵材料相關的風險管理之描述`

## `GET /opendata/t187ap46_L_18`
ESG disclosure - ownership and control  <!-- 上市公司企業ESG資訊揭露彙總資料-持股及控制力 -->

Response item fields (exact JSON keys):
`出表日期`, `報告年度`, `公司代號`, `公司名稱`, `前10大股東持股情形`

## `GET /opendata/t187ap46_L_17`
ESG disclosure - financial inclusion  <!-- 上市公司企業ESG資訊揭露彙總資料-普惠金融 -->

Response item fields (exact JSON keys):
`出表日期`, `報告年度`, `公司代號`, `公司名稱`, `對促進小型企業及社區發展的貸放件數(件)`, `對促進小型企業及社區發展的貸放餘額(仟元)`, `對缺少銀行服務之弱勢族群提供金融教育之參與人數(人)`

## `GET /opendata/t187ap46_L_16`
ESG disclosure - information security  <!-- 上市公司企業ESG資訊揭露彙總資料-資訊安全 -->

Response item fields (exact JSON keys):
`出表日期`, `報告年度`, `公司代號`, `公司名稱`, `資訊外洩事件數量`, `與個資相關的資訊外洩事件占比`, `因資訊外洩事件而受影響的顧客數(人)`

## `GET /opendata/t187ap46_L_15`
ESG disclosure - community relations  <!-- 上市公司企業ESG資訊揭露彙總資料-社區關係 -->

Response item fields (exact JSON keys):
`出表日期`, `報告年度`, `公司代號`, `公司名稱`, `在人口密集地區的煉油廠數量(座)`

## `GET /opendata/t187ap46_L_14`
ESG disclosure - product quality and safety  <!-- 上市公司企業ESG資訊揭露彙總資料-產品品質與安全 -->

Response item fields (exact JSON keys):
`出表日期`, `報告年度`, `公司代號`, `公司名稱`, `售出產品重量(公噸(t))`, `生產設施場所數量(座)`, `依產品類別之產品產量`

## `GET /opendata/t187ap46_L_13`
ESG disclosure - supply chain management  <!-- 上市公司企業ESG資訊揭露彙總資料-供應鏈管理 -->

Response item fields (exact JSON keys):
`出表日期`, `報告年度`, `公司代號`, `公司名稱`, `採購符合國際認可之產品責任標準者占整體採購之百分比，並依標準區分`, `對供應商進行稽核之家數(家)`, `對供應商進行稽核之百分比`

## `GET /opendata/t187ap46_L_12`
ESG disclosure - food safety  <!-- 上市公司企業ESG資訊揭露彙總資料-食品安全 -->

Response item fields (exact JSON keys):
`出表日期`, `報告年度`, `公司代號`, `為改善食品衛生、安全與品質，而針對其從業人員、作業場所、設施衛生管理及其品保制度等方面進行之評估與改進及所影響之百分比`, `違反有關產品與服務之健康與安全法規及未遵循產品與服務之資訊與標示法規之事件類別與次數`, `違反有關產品與服務之健康與安全法規及未遵循產品與服務之資訊與標示法規之產品下架次數(次)`, `違反有關產品與服務之健康與安全法規及未遵循產品與服務之資訊與標示法規之下架產品總重量(公噸(t))`, `經獨立第三方驗證符合國際認證之食品安全管理系統標準之廠房所生產產品之百分比`, `依法規要求或自願進行產品追溯與追蹤管理之相關產品占所有產品之百分比`, `依法規要求或自願設置食品安全實驗室之相關支出(仟元)`, `依法規要求或自願設置食品安全實驗室之相關支出占營業收入淨額之百分比`

## `GET /opendata/t187ap46_L_11`
ESG disclosure - product lifecycle  <!-- 上市公司企業ESG資訊揭露彙總資料-產品生命週期 -->

Response item fields (exact JSON keys):
`出表日期`, `報告年度`, `公司代號`, `公司名稱`, `產品生命週期管理之揭露：報廢產品及電子廢棄物之重量(公噸(t))`, `產品生命週期管理之揭露：含報廢產品及電子廢棄物之再循環之百分比`

## `GET /opendata/t187ap46_L_10`
ESG disclosure - fuel management  <!-- 上市公司企業ESG資訊揭露彙總資料-燃料管理 -->

Response item fields (exact JSON keys):
`出表日期`, `報告年度`, `公司代號`, `公司名稱`, `消耗燃料總量(十億焦耳(GJ))`, `煤炭百分比`, `天然氣百分比`, `再生燃料百分比`

## `GET /opendata/t187ap46_L_9`
ESG disclosure - functional committees  <!-- 上市公司企業ESG資訊揭露彙總資料-功能性委員會 -->

Response item fields (exact JSON keys):
`出表日期`, `報告年度`, `公司代號`, `公司名稱`, `薪酬委員會席次`, `薪酬委員會獨立董事席次`, `薪酬委員會出席率`, `審計委員會席次`, `審計委員會出席率`

## `GET /opendata/t187ap46_L_8`
ESG disclosure - climate-related issues management  <!-- 上市公司企業ESG資訊揭露彙總資料-氣候相關議題管理 -->

Response item fields (exact JSON keys):
`出表日期`, `報告年度`, `公司代號`, `公司名稱`, `董事會與管理階層對於氣候相關風險與機會之監督及治理`, `辨識之氣候風險與機會如何影響企業之業務、策略及財務 (短期、中期、長期)`, `極端氣候事件及轉型行動對財務之影響`, `氣候風險之辨識、評估及管理流程如何整合於整體風險管理制度`, `若使用情境分析評估面對氣候變遷風險之韌性，應說明所使用之情境、參數、假設、分析因子及主要財務影響`, `若有因應管理氣候相關風險之轉型計畫，說明該計畫內容，及用於辨識及管理實體風險及轉型風險之指標與目標`, `使用內部碳定價作為規劃工具，應說明價格制定基礎,若有設定氣候相關目標，應說明所涵蓋之活動、溫室氣體排放範疇、規劃期程，每年達成進度等資訊；若使用碳抵換或再生能源憑證(RECs)以達成相關目標，應說明所抵換之減碳額度來源及數量或再生能源憑證(RECs)數量`

## `GET /opendata/t187ap05_P`
Monthly operating revenue summary of public companies  <!-- 公開發行公司每月營業收入彙總表 -->

Response item fields (exact JSON keys):
`出表日期`, `資料年月`, `公司代號`, `公司名稱`, `產業別`, `營業收入-當月營收`, `營業收入-上月營收`, `營業收入-去年當月營收`, `營業收入-上月比較增減(%)`, `營業收入-去年同月增減(%)`, `累計營業收入-當月累計營收`, `累計營業收入-去年累計營收`, `累計營業收入-前期比較增減(%)`, `備註`

## `GET /opendata/t187ap46_L_7`
ESG disclosure - investor communication  <!-- 上市公司企業ESG資訊揭露彙總資料-投資人溝通 -->

Response item fields (exact JSON keys):
`出表日期`, `報告年度`, `公司代號`, `公司名稱`, `公司年度召開法說會次數(次)`

## `GET /opendata/t187ap46_L_6`
ESG disclosure - board of directors  <!-- 上市公司企業ESG資訊揭露彙總資料-董事會 -->

Response item fields (exact JSON keys):
`出表日期`, `報告年度`, `公司代號`, `公司名稱`, `董事席次(含獨立董事)(席)`, `獨立董事席次(席)`, `女性董事席次及比率-席`, `女性董事席次及比率-比率`, `董事出席董事會出席率`, `董監事進修時數符合進修要點比率`

## `GET /opendata/t187ap46_L_5`
ESG disclosure - human capital development  <!-- 上市公司企業ESG資訊揭露彙總資料-人力發展 -->

Response item fields (exact JSON keys):
`出表日期`, `報告年度`, `公司代號`, `公司名稱`, `員工福利平均數(仟元/人)`, `員工薪資平均數(仟元/人) `, `非擔任主管職務之全時員工薪資平均數(仟元/人) `, `非擔任主管職務之全時員工薪資平均數變動百分比`, `非擔任主管之全時員工薪資中位數(仟元/人) `, `非擔任主管職務之全時員工薪資中位數變動百分比`, `管理職女性主管佔比`, `新進員工年齡分布`, `離職員工年齡分布`, `高齡員工晉用政策及培訓計畫`

## `GET /opendata/t187ap46_L_4`
ESG disclosure - waste management  <!-- 上市公司企業ESG資訊揭露彙總資料-廢棄物管理 -->

Response item fields (exact JSON keys):
`出表日期`, `報告年度`, `公司代號`, `公司名稱`, `有害廢棄物量-數據(公噸) `, `有害廢棄物量-資料範圍`, `非有害廢棄物量-數據(公噸)`, `非有害廢棄物量-資料範圍`, `總重量(有害+非有害)-數據(公噸)`, `總重量(有害+非有害)-資料範圍`, `廢棄物密集度-密集度(公噸/單位) `, `廢棄物密集度-單位`, `取得驗證`

## `GET /opendata/t187ap46_L_3`
ESG disclosure - water resource management  <!-- 上市公司企業ESG資訊揭露彙總資料-水資源管理 -->

Response item fields (exact JSON keys):
`出表日期`, `報告年度`, `公司代號`, `公司名稱`, `用水量(公噸)`, `資料範圍`, `用水密集度-密集度(公噸/單位) `, `用水密集度-單位`, `取得驗證`

## `GET /opendata/t187ap46_L_2`
ESG disclosure - energy management  <!-- 上市公司企業ESG資訊揭露彙總資料-能源管理 -->

Response item fields (exact JSON keys):
`出表日期`, `報告年度`, `公司代號`, `公司名稱`, `使用率(再生能源/總能源)`, `資料範圍`, `取得驗證`

## `GET /opendata/t187ap46_L_1`
ESG disclosure - greenhouse gas emissions  <!-- 上市公司企業ESG資訊揭露彙總資料-溫室氣體排放 -->

Response item fields (exact JSON keys):
`出表日期`, `報告年度`, `公司代號`, `公司名稱`, `範疇一排放量(噸CO2e)`, `範疇一資料邊界`, `範疇一取得驗證`, `範疇二排放量(噸CO2e)`, `範疇二資料邊界`, `範疇二取得驗證`, `範疇三排放量(噸CO2e)`, `範疇三資料邊界`, `範疇三取得驗證`, `溫室氣體排放密集度(噸CO2e/單位)`

## `GET /company/applylistingForeign`
Foreign companies applying for TWSE primary listing  <!-- 外國公司向證交所申請第一上市之公司 -->

Response item fields (exact JSON keys):
`No`, `Code`, `Company`, `ApplicationDate`, `Chairman`, `AmountofCapital `, `CommitteeDate`, `ApprovedDate`, `AgreementDate`, `ListingDate`, `Underwriter`, `UnderwritingPrice`, `Note`

## `GET /company/newlisting`
Recently listed companies  <!-- 最近上市公司 -->

Response item fields (exact JSON keys):
`Code`, `Company`, `ApplicationDate`, `Chairman`, `AmountofCapital `, `CommitteeDate`, `ApprovedDate`, `AgreementDate`, `ListingDate`, `ApprovedListingDate`, `Underwriter`, `UnderwritingPrice`, `Note`

## `GET /company/suspendListingCsvAndHtml`
Delisted (terminated listing) companies  <!-- 終止上市公司 -->

Response item fields (exact JSON keys):
`DelistingDate`, `Company`, `Code`

## `GET /company/applylistingLocal`
Domestic companies applying for listing  <!-- 申請上市之本國公司 -->

Response item fields (exact JSON keys):
`Code`, `Company`, `ApplicationDate`, `Chairman`, `AmountofCapital `, `CommitteeDate`, `ApprovedDate`, `AgreementDate`, `ListingDate`, `ApprovedListingDate`, `Underwriter`, `UnderwritingPrice`, `Note`

## `GET /opendata/t187ap04_L`
Daily material information (major announcements) of listed companies  <!-- 上市公司每日重大訊息 -->

Response item fields (exact JSON keys):
`出表日期`, `發言日期`, `發言時間`, `公司代號`, `公司名稱`, `主旨 `, `符合條款`, `事實發生日`, `說明`

## `GET /opendata/t187ap03_L`
Basic profile of listed companies  <!-- 上市公司基本資料 -->

Response item fields (exact JSON keys):
`出表日期`, `公司代號`, `公司名稱`, `公司簡稱`, `外國企業註冊地國`, `產業別`, `住址`, `營利事業統一編號`, `董事長`, `總經理`, `發言人`, `發言人職稱`, `代理發言人`, `總機電話`, `成立日期`, `上市日期`, `普通股每股面額`, `實收資本額`, `私募股數`, `特別股`, `編制財務報表類型`, `股票過戶機構`, `過戶電話`, `過戶地址`, `簽證會計師事務所`, `簽證會計師1`, `簽證會計師2`, `英文簡稱`, `英文通訊地址`, `傳真機號碼`, `電子郵件信箱`, `網址`, `已發行普通股數或TDR原股發行股數`

## `GET /opendata/t187ap02_L`
Major shareholders holding over 10% of listed companies  <!-- 上市公司持股逾 10% 大股東名單 -->

Response item fields (exact JSON keys):
`出表日期`, `公司代號`, `公司名稱`, `大股東名稱`

## `GET /opendata/t187ap14_L`
EPS statistics of listed companies by industry  <!-- 上市公司各產業EPS統計資訊 -->

Response item fields (exact JSON keys):
`出表日期`, `年度`, `季別`, `公司代號`, `公司名稱`, `產業別`, `基本每股盈餘(元)`, `普通股每股面額`, `營業收入`, `營業利益`, `營業外收入及支出`, `稅後淨利`

## `GET /opendata/t187ap08_L`
Directors/supervisors with shareholding below legal minimum  <!-- 上市公司董事、監察人持股不足法定成數彙總表 -->

Response item fields (exact JSON keys):
`出表日期`, `公司代號`, `公司名稱`, `已發行股份總額`, `全體董事應持有股數`, `全體董事本人實際持有股數`, `全體董事法人代表人分戶集保股數`, `全體董事保留運用決定權信託股數`, `全體董事不足股數`, `全體監察人應持有股數`, `全體監察人本人實際持有股數`, `全體監察人法人代表人分戶集保股數`, `全體監察人保留運用決定權信託股數`, `全體監察人不足股數`, `持股不足已通知其董監`

## `GET /opendata/t187ap11_L`
Director/supervisor shareholding balance details (listed companies)  <!-- 上市公司董監事持股餘額明細資料 -->

Response item fields (exact JSON keys):
`出表日期`, `資料年月`, `公司代號`, `公司名稱`, `職稱`, `姓名`, `選任時持股 `, `目前持股`, `設質股數`, `設質股數佔持股比例`, `內部人關係人目前持股合計`, `內部人關係人設質股數`, `內部人關係人設質比例`

## `GET /opendata/t187ap12_L`
Insider share-transfer pre-declarations - shares transferred (daily)  <!-- 上市公司每日內部人持股轉讓事前申報表-持股轉讓日報表 -->

Response item fields (exact JSON keys):
`出表日期`, `公司代號`, `公司名稱`, `申報人身分`, `姓名`, `預定轉讓方式及股數-轉讓方式`, `預定轉讓方式及股數-轉讓股數`, `每日於盤中交易最大得轉讓股數`, `受讓人`, `目前持有股數-自有持股`, `目前持有股數-保留運用決定權信託股數`, `預定轉讓總股數-自有持股`, `預定轉讓總股數-保留運用決定權信託股數`, `預定轉讓後持股-自有持股`, `預定轉讓後持股-保留運用決定權信託股數`, `有效轉讓期間`

## `GET /opendata/t187ap13_L`
Insider share-transfer pre-declarations - shares not yet transferred (daily)  <!-- 上市公司每日內部人持股轉讓事前申報表-持股未轉讓日報表 -->

Response item fields (exact JSON keys):
`出表日期`, `公司代號`, `公司名稱`, `申報人身分`, `姓名`, `未轉讓股數-自有持股`, `未轉讓股數-保留運用決定權信託股數`, `目前持股-自有持股`, `目前持股-保留運用決定權信託股數`, `原申報預定轉讓股數-自有持股`, `原申報預定轉讓股數-保留運用決定權信託股數`, `未轉讓理由`

## `GET /opendata/t187ap22_L`
FSC Securities and Futures Bureau sanction cases against listed companies  <!-- 上市公司金管會證券期貨局裁罰案件專區 -->

Response item fields (exact JSON keys):
`出表日期`, `發函日期`, `股票代號`, `公司名稱`, `違規事由`, `違反法規`, `裁處情形`

## `GET /opendata/t187ap30_L`
Concurrent positions held by independent directors/supervisors  <!-- 上市公司獨立董監事兼任情形彙總表 -->

Response item fields (exact JSON keys):
`出表日期`, `序號`, `公司代號`, `公司名稱`, `職稱`, `姓名`, `就任日期`, `主要現職`, `主要經歷`, `目前兼任其他公司名稱`, `其他公司職稱`, `備註`

## `GET /opendata/t187ap29_A_L`
Director compensation of listed companies  <!-- 上市公司董事酬金相關資訊 -->

Response item fields (exact JSON keys):
`出表日期`, `產業類別`, `公司代號`, `公司名稱`, `董事酬金-前年支付`, `董事酬金-今年支付`, `董事酬金-合計`, `董事酬金加計兼任員工酬金-前年支付`, `董事酬金加計兼任員工酬金-今年支付`, `加計兼任員工酬金-合計`, `酬金總額占稅後損益百分比(%)-董事酬金`, `酬金總額占稅後損益百分比(%)-加計兼任員工酬金`, `平均每位董事酬金-董事酬金`, `平均每位董事酬金-加計兼任員工酬金`, `領取來自子公司以外轉投資事業或母公司酬金`, `稅後純益`, `每股盈餘`, `股東權益報酬率(%)`, `實收資本額(仟元)`, `稅後損益與董監酬金變動之關聯性與合理性說明`

## `GET /opendata/t187ap29_B_L`
Supervisor compensation of listed companies  <!-- 上市公司監察人酬金相關資訊 -->

Response item fields (exact JSON keys):
`出表日期`, `產業類別`, `公司代號`, `公司名稱`, `監察人酬金-前年支付`, `監察人酬金-今年支付`, `監察人酬金-合計`, `酬金總額占稅後損益百分比(%)`, `平均每位監察人酬金`, `領取來自子公司以外轉投資事業或母公司酬金`, `稅後純益`, `每股盈餘`, `股東權益報酬率(%)`, `實收資本額(仟元)`, `稅後損益與董監酬金變動之關聯性與合理性說明`

## `GET /opendata/t187ap29_C_L`
Director compensation (consolidated financial statements)  <!-- 上市公司合併報表董事酬金相關資訊 -->

Response item fields (exact JSON keys):
`出表日期`, `產業類別`, `公司代號`, `公司名稱`, `董事酬金-前年支付`, `董事酬金-今年支付`, `董事酬金-合計`, `董事酬金加計兼任員工酬金-前年支付`, `董事酬金加計兼任員工酬金-今年支付`, `加計兼任員工酬金-合計`, `酬金總額占稅後損益百分比(%)-董事酬金`, `酬金總額占稅後損益百分比(%)-加計兼任員工酬金`, `平均每位董事酬金-董事酬金`, `平均每位董事酬金-加計兼任員工酬金`, `領取來自子公司以外轉投資事業或母公司酬金`, `稅後純益`, `每股盈餘`, `股東權益報酬率(%)`, `實收資本額(仟元)`, `稅後損益與董監酬金變動之關聯性與合理性說明`

## `GET /opendata/t187ap29_D_L`
Supervisor compensation (consolidated financial statements)  <!-- 上市公司合併報表監察人酬金相關資訊 -->

Response item fields (exact JSON keys):
`出表日期`, `產業類別`, `公司代號`, `公司名稱`, `監察人酬金-前年支付`, `監察人酬金-今年支付`, `監察人酬金-合計`, `酬金總額占稅後損益百分比(%)`, `平均每位監察人酬金`, `領取來自子公司以外轉投資事業或母公司酬金`, `稅後純益`, `每股盈餘`, `股東權益報酬率(%)`, `實收資本額(仟元)`, `稅後損益與董監酬金變動之關聯性與合理性說明`

## `GET /opendata/t187ap23_L`
Listed companies violating information-filing / material-info / press-conference rules  <!-- 上市公司違反資訊申報、重大訊息及說明記者會規定專區 -->

Response item fields (exact JSON keys):
`出表日期`, `發函日期`, `股票代號`, `公司名稱`, `違規事由`, `違反資訊申報作業辦法條款`, `違反重大訊息之查證暨公開處理程序條款`, `裁罰金額(萬)`

## `GET /opendata/t187ap03_P`
Basic profile of public (non-listed) companies  <!-- 公開發行公司基本資料 -->

Response item fields (exact JSON keys):
`出表日期`, `公司代號`, `公司名稱`, `公司簡稱`, `外國企業註冊地國`, `產業別`, `住址`, `營利事業統一編號`, `董事長`, `總經理`, `發言人`, `發言人職稱`, `代理發言人`, `總機電話`, `成立日期`, `上市日期`, `普通股每股面額`, `實收資本額`, `私募股數`, `特別股`, `編制財務報表類型`, `股票過戶機構`, `過戶電話`, `過戶地址`, `簽證會計師事務所`, `簽證會計師1`, `簽證會計師2`, `英文簡稱`, `英文通訊地址`, `傳真機號碼`, `電子郵件信箱`, `網址`, `已發行普通股數或TDR原股發行股數`

## `GET /announcement/punish`
Disposition stocks announced (centralized market)  <!-- 集中市場公布處置股票 -->

Response item fields (exact JSON keys):
`Number`, `Date`, `Code`, `Name`, `NumberOfAnnouncement`, `ReasonsOfDisposition`, `DispositionPeriod`, `DispositionMeasures`, `Detail`, `LinkInformation`

## `GET /opendata/t187ap10_L`
Directors/supervisors below legal shareholding for 3+ consecutive months  <!-- 上市公司董事、監察人持股不足法定成數連續達3個月以上彙總表 -->

Response item fields (exact JSON keys):
`出表日期`, `連續不足達3個月`, `連續不足達4個月`, `連續不足達5個月`, `連續不足達6個月`, `連續不足達7個月`, `連續不足達8個月`, `連續不足達9個月`, `連續不足達10個月`, `連續不足達11個月`, `連續不足達12個月`, `連續不足逾1年以上`

## `GET /opendata/t187ap38_L`
Shareholder meeting convening announcements (since 2006)  <!-- 上市公司股東會公告-召集股東常(臨時)會公告資料彙總表(95年度起適用) -->

Response item fields (exact JSON keys):
`出表日期`, `公司代號`, `公司名稱`, `股東常(臨時)會日期-常或臨時`, `股東常(臨時)會日期-日期`, `停止過戶起訖日期-起`, `停止過戶起訖日期-訖`, `預擬配發現金(股利)(元/股)-盈餘`, `預擬配發現金(股利)(元/股)-法定盈餘公積、資本公積`, `預擬配股(元/股)-盈餘`, `預擬配股(元/股)-法定盈餘公積、資本公積`, `擬現金增資金額(元)`, `現金增資認購率(%)`, `員工紅利-現金紅利(元)`, `員工紅利-股票紅利(股)`, `特別股股利(元/股)`, `董監酬勞(元)`, `公告日期`, `公告時間`, `種類`

## `GET /opendata/t187ap24_L`
Change-of-control listed companies  <!-- 上市公司經營權及營業範圍異(變)動專區-經營權異動公司 -->

Response item fields (exact JSON keys):
`出表日期`, `公司代號`, `公司名稱`, `經營權異動日期`, `經營權異動說明`

## `GET /opendata/t187ap26_L`
Control change + major business-scope change - trading suspended  <!-- 上市公司經營權及營業範圍異(變)動專區-經營權異動且營業範圍重大變更停止買賣公司 -->

Response item fields (exact JSON keys):
`出表日期`, `公司代號`, `公司名稱`, `停止買賣開始日`

## `GET /opendata/t187ap41_L`
Shareholder meeting date, venue and e-voting adoption  <!-- 上市公司召開股東常 (臨時) 會日期、地點及採用電子投票情形等資料彙總表 -->

Response item fields (exact JSON keys):
`出表日期`, `公司代號`, `公司名稱`, `公司地址`, `股東常(臨時)會`, `開會日期`, `開會地點`, `是否改選董監`, `聯絡電話`, `股務單位`, `股務單位電話`, `是否採電子投票`

## `GET /opendata/t187ap25_L`
Listed companies with major business-scope changes  <!-- 上市公司經營權及營業範圍異(變)動專區-營業範圍重大變更公司 -->

Response item fields (exact JSON keys):
`出表日期`, `序號`, `年度`, `季別`, `公司代號`, `公司名稱`, `營業範圍重大變更說明`

## `GET /opendata/t187ap27_L`
Control change + major business-scope change - placed under altered trading method  <!-- 上市公司經營權及營業範圍異(變)動專區-經營權異動且營業範圍重大變更列為變更交易公司 -->

Response item fields (exact JSON keys):
`出表日期`, `公司代號`, `公司名稱`, `變更交易開始日`

## `GET /opendata/t187ap32_L`
Corporate governance rules and regulations adopted by listed companies  <!-- 上市公司公司治理之相關規程規則 -->

Response item fields (exact JSON keys):
`出表日期`, `公司代號`, `公司名稱`, `公司治理之相關規程規則`

## `GET /opendata/t187ap33_L`
Whether the chairman also serves as general manager (CEO duality)  <!-- 上市公司董事長是否兼任總經理 -->

Response item fields (exact JSON keys):
`出表日期`, `公司代號`, `公司名稱`, `董事長`, `總經理`, `董事長是否兼任總經理`

## `GET /opendata/t187ap09_L`
Pledged shares ratio of directors and supervisors  <!-- 上市公司董事、監察人質權設定占董事及監察人實際持有股數彙總表 -->

Response item fields (exact JSON keys):
`出表日期`, `百分比`, `公司名稱`

## `GET /opendata/t187ap34_L`
Director/supervisor election methods (cumulative voting, nomination system) and results  <!-- 上市公司採累積投票制、全額連記法、候選人提名制選任董監事及當選資料彙總表 -->

Response item fields (exact JSON keys):
`出表日期`, `公司代號`, `公司名稱`, `股東常(臨時)會日期-常或臨時`, `股東常(臨時)會日期-日期`, `是否選任董監事`, `董監事選任方式`, `是否採候選人提名制選任董監事`, `採候選人提名制選任董監事相關公告-提名受理期間`, `提名受理處所`, `候選人類別`, `候選人姓名`, `是否當選`

## `GET /opendata/t187ap35_L`
Shareholder proposal rights exercised at listed companies  <!-- 上市公司股東行使提案權情形彙總表 -->

Response item fields (exact JSON keys):
`出表日期`, `公司代號`, `公司名稱`, `召開股東會日期`, `股東依公司法第172條之1行使提案權-提案受理期間`, `提案受理處所`, `提案內容`
