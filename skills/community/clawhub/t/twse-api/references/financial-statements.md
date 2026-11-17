# TWSE API - Financial Statements <!-- 財務報表 -->

Monthly revenue, income statements and balance sheets (split by industry accounting format), and profitability summaries. Income statement (`t187ap06_*`) and balance sheet (`t187ap07_*`) endpoints are split by industry suffix: `_ci` general industry (一般業), `_basi` banking (金融業), `_fh` financial holding (金控業), `_ins` insurance (保險業), `_bd` securities & futures (證券期貨業), `_mim` mixed/other (異業). `_L_` = listed companies (上市), `_X_` = public non-listed companies (公發). Most stocks (e.g. TSMC 2330) are in `_ci`. All endpoints: `GET https://openapi.twse.com.tw/v1<path>`, no parameters, JSON array response.

| Endpoint | Description |
|---|---|
| `/opendata/t187ap07_X_ci` | Balance sheets of public companies - general industry |
| `/opendata/t187ap07_X_mim` | Balance sheets of public companies - mixed/other industry |
| `/opendata/t187ap06_X_basi` | Income statements of public companies - banking industry |
| `/opendata/t187ap06_X_bd` | Income statements of public companies - securities & futures industry |
| `/opendata/t187ap06_X_ci` | Income statements of public companies - general industry |
| `/opendata/t187ap06_X_fh` | Income statements of public companies - financial holding industry |
| `/opendata/t187ap06_X_ins` | Income statements of public companies - insurance industry |
| `/opendata/t187ap06_X_mim` | Income statements of public companies - mixed/other industry |
| `/opendata/t187ap05_L` | Monthly operating revenue summary of listed companies |
| `/opendata/t187ap15_L` | Quarterly financial forecast achievement status (condensed) |
| `/opendata/t187ap16_L` | Audited results deviating from forecasts by 10%+/20%+ (condensed) |
| `/opendata/t187ap17_L` | Profitability analysis summary of all listed companies |
| `/opendata/t187ap31_L` | Financial reports recognized by supervisors |
| `/opendata/t187ap06_L_bd` | Income statements of listed companies - securities & futures industry |
| `/opendata/t187ap06_L_ci` | Income statements of listed companies - general industry |
| `/opendata/t187ap06_L_fh` | Income statements of listed companies - financial holding industry |
| `/opendata/t187ap06_L_ins` | Income statements of listed companies - insurance industry |
| `/opendata/t187ap06_L_mim` | Income statements of listed companies - mixed/other industry |
| `/opendata/t187ap07_L_bd` | Balance sheets of listed companies - securities & futures industry |
| `/opendata/t187ap07_L_ci` | Balance sheets of listed companies - general industry |
| `/opendata/t187ap07_L_fh` | Balance sheets of listed companies - financial holding industry |
| `/opendata/t187ap07_L_ins` | Balance sheets of listed companies - insurance industry |
| `/opendata/t187ap07_L_mim` | Balance sheets of listed companies - mixed/other industry |
| `/opendata/t187ap07_X_basi` | Balance sheets of public companies - banking industry |
| `/opendata/t187ap07_X_bd` | Balance sheets of public companies - securities & futures industry |
| `/opendata/t187ap07_X_fh` | Balance sheets of public companies - financial holding industry |
| `/opendata/t187ap07_X_ins` | Balance sheets of public companies - insurance industry |
| `/opendata/t187ap11_P` | Director/supervisor shareholding balance details (public companies) |
| `/opendata/t187ap06_L_basi` | Income statements of listed companies - banking industry |
| `/opendata/t187ap07_L_basi` | Balance sheets of listed companies - banking industry |

---

## `GET /opendata/t187ap07_X_ci`
Balance sheets of public companies - general industry  <!-- 公發公司資產負債表-一般業 -->

Response item fields (exact JSON keys):
`出表日期`, `年度`, `季別`, `公司代號`, `公司名稱`, `流動資產`, `非流動資產`, `資產總計`, `流動負債`, `非流動負債`, `負債總計`, `股本`, `權益─具證券性質之虛擬通貨`, `資本公積`, `保留盈餘`, `其他權益`, `庫藏股票`, `歸屬於母公司業主之權益合計`, `共同控制下前手權益`, `合併前非屬共同控制股權`, `非控制權益`, `權益總計`, `待註銷股本股數（單位：股）`, `預收股款（權益項下）之約當發行股數（單位：股）`, `母公司暨子公司所持有之母公司庫藏股股數（單位：股）`, `每股參考淨值`

## `GET /opendata/t187ap07_X_mim`
Balance sheets of public companies - mixed/other industry  <!-- 公發公司資產負債表-異業 -->

Response item fields (exact JSON keys):
`出表日期`, `年度`, `季別`, `公司代號`, `公司名稱`, `流動資產`, `非流動資產`, `資產總計`, `流動負債`, `非流動負債`, `負債總計`, `股本`, `權益－具證券性質之虛擬通貨`, `資本公積`, `保留盈餘`, `其他權益`, `庫藏股票`, `歸屬於母公司業主之權益合計`, `共同控制下前手權益`, `非控制權益`, `權益總額`, `待註銷股本股數（單位：股）`, `預收股款（權益項下）之約當發行股數（單位：股）`, `母公司暨子公司所持有之母公司庫藏股股數（單位：股）`, `每股參考淨值`

## `GET /opendata/t187ap06_X_basi`
Income statements of public companies - banking industry  <!-- 公發公司綜合損益表-金融業 -->

Response item fields (exact JSON keys):
`出表日期`, `年度`, `季別`, `公司代號`, `公司名稱`, `利息淨收益`, `利息以外淨損益`, `呆帳費用、承諾及保證責任準備提存`, `營業費用`, `繼續營業單位稅前淨利（淨損）`, `所得稅費用（利益）`, `繼續營業單位本期稅後淨利（淨損）`, `停業單位損益`, `合併前非屬共同控制股權損益`, `本期稅後淨利（淨損）`, `其他綜合損益（稅後）`, `合併前非屬共同控制股權綜合損益淨額`, `本期綜合損益總額（稅後）`, `淨利（損）歸屬於母公司業主`, `淨利（損）歸屬於共同控制下前手權益`, `淨利（損）歸屬於非控制權益`, `綜合損益總額歸屬於母公司業主`, `綜合損益總額歸屬於共同控制下前手權益`, `綜合損益總額歸屬於非控制權益`, `基本每股盈餘（元）`

## `GET /opendata/t187ap06_X_bd`
Income statements of public companies - securities & futures industry  <!-- 公發公司綜合損益表-證券期貨業 -->

Response item fields (exact JSON keys):
`出表日期`, `年度`, `季別`, `公司代號`, `公司名稱`, `收益`, `支出及費用`, `營業利益`, `營業外損益`, `稅前淨利（淨損）`, `所得稅費用（利益）`, `繼續營業單位本期淨利（淨損）`, `停業單位損益`, `合併前非屬共同控制股權損益`, `本期淨利（淨損）`, `本期其他綜合損益（稅後淨額）`, `合併前非屬共同控制股權綜合損益淨額`, `本期綜合損益總額`, `淨利（損）歸屬於母公司業主`, `淨利（淨損）歸屬於共同控制下前手權益`, `淨利（損）歸屬於非控制權益`, `綜合損益總額歸屬於母公司業主`, `綜合損益總額歸屬於共同控制下前手權益`, `綜合損益總額歸屬於非控制權益`, `基本每股盈餘（元）`

## `GET /opendata/t187ap06_X_ci`
Income statements of public companies - general industry  <!-- 公發公司綜合損益表-一般業 -->

Response item fields (exact JSON keys):
`出表日期`, `年度`, `季別`, `公司代號`, `公司名稱`, `營業收入`, `營業成本`, `原始認列生物資產及農產品之利益（損失）`, `生物資產當期公允價值減出售成本之變動利益（損失）`, `營業毛利（毛損）`, `未實現銷貨（損）益`, `已實現銷貨（損）益`, `營業毛利（毛損）淨額`, `營業費用`, `其他收益及費損淨額`, `營業利益（損失）`, `營業外收入及支出`, `稅前淨利（淨損）`, `所得稅費用（利益）`, `繼續營業單位本期淨利（淨損）`, `停業單位損益`, `合併前非屬共同控制股權損益`, `本期淨利（淨損）`, `其他綜合損益（淨額）`, `合併前非屬共同控制股權綜合損益淨額`, `本期綜合損益總額`, `淨利（淨損）歸屬於母公司業主`, `淨利（淨損）歸屬於共同控制下前手權益`, `淨利（淨損）歸屬於非控制權益`, `綜合損益總額歸屬於母公司業主`, `綜合損益總額歸屬於共同控制下前手權益`, `綜合損益總額歸屬於非控制權益`, `基本每股盈餘（元）`

## `GET /opendata/t187ap06_X_fh`
Income statements of public companies - financial holding industry  <!-- 公發公司綜合損益表-金控業 -->

Response item fields (exact JSON keys):
`出表日期`, `年度`, `季別`, `公司代號`, `公司名稱`, `利息淨收益`, `利息以外淨收益`, `淨收益`, `呆帳費用、承諾及保證責任準備提存`, `保險負債準備淨變動`, `營業費用`, `繼續營業單位稅前損益`, `所得稅（費用）利益`, `繼續營業單位本期淨利（淨損）`, `停業單位損益`, `本期稅後淨利（淨損）`, `本期其他綜合損益（稅後淨額）`, `本期綜合損益總額`, `淨利（淨損）歸屬於母公司業主`, `淨利（淨損）歸屬於共同控制下前手權益`, `淨利（淨損）歸屬於非控制權益`, `綜合損益總額歸屬於母公司業主`, `綜合損益總額歸屬於共同控制下前手權益`, `綜合損益總額歸屬於非控制權益`, `基本每股盈餘（元）`

## `GET /opendata/t187ap06_X_ins`
Income statements of public companies - insurance industry  <!-- 公發公司綜合損益表-保險業 -->

Response item fields (exact JSON keys):
`出表日期`, `年度`, `季別`, `公司代號`, `公司名稱`, `營業收入`, `營業成本`, `營業費用`, `營業利益（損失）`, `營業外收入及支出`, `繼續營業單位稅前純益（純損）`, `所得稅費用（利益）`, `繼續營業單位本期純益（純損）`, `停業單位損益`, `合併前非屬共同控制股權損益`, `本期淨利（淨損）`, `其他綜合損益（稅後淨額）`, `合併前非屬共同控制股權綜合損益淨額`, `本期綜合損益總額`, `淨利（淨損）歸屬於母公司業主`, `淨利（淨損）歸屬於共同控制下前手權益`, `淨利（淨損）歸屬於非控制權益`, `綜合損益總額歸屬於母公司業主`, `綜合損益總額歸屬於共同控制下前手權益`, `綜合損益總額歸屬於非控制權益`, `基本每股盈餘（元）`

## `GET /opendata/t187ap06_X_mim`
Income statements of public companies - mixed/other industry  <!-- 公發公司綜合損益表-異業 -->

Response item fields (exact JSON keys):
`出表日期`, `年度`, `季別`, `公司代號`, `公司名稱`, `收入`, `支出`, `繼續營業單位稅前淨利（淨損）`, `所得稅費用（利益）`, `繼續營業單位本期淨利（淨損）`, `停業單位損益`, `本期淨利（淨損）`, `其他綜合損益`, `本期綜合損益總額`, `淨利（淨損）歸屬於母公司業主`, `淨利（淨損）歸屬於共同控制下前手權益`, `淨利（淨損）歸屬於非控制權益`, `綜合損益總額歸屬於母公司業主`, `綜合損益總額歸屬於共同控制下前手權益`, `綜合損益總額歸屬於非控制權益`, `基本每股盈餘（元）`

## `GET /opendata/t187ap05_L`
Monthly operating revenue summary of listed companies  <!-- 上市公司每月營業收入彙總表 -->

Response item fields (exact JSON keys):
`出表日期`, `資料年月`, `公司代號`, `公司名稱`, `產業別`, `營業收入-當月營收`, `營業收入-上月營收`, `營業收入-去年當月營收`, `營業收入-上月比較增減(%)`, `營業收入-去年同月增減(%)`, `累計營業收入-當月累計營收`, `累計營業收入-去年累計營收`, `累計營業收入-前期比較增減(%)`, `備註`

## `GET /opendata/t187ap15_L`
Quarterly financial forecast achievement status (condensed)  <!-- 上市公司截至各季綜合損益財測達成情形(簡式) -->

Response item fields (exact JSON keys):
`出表日期`, `年度`, `季別`, `公司代號`, `公司名稱`, `財測序號`, `涵蓋期間`, `截至該季經會計師查核或核閱數`, `截至該季綜合損益預測數`

## `GET /opendata/t187ap16_L`
Audited results deviating from forecasts by 10%+/20%+ (condensed)  <!-- 上市公司當季綜合損益經會計師查核(核閱)數與當季預測數差異達百分之十以上者，或截至當季累計差異達百分之二十以上者(簡式) -->

Response item fields (exact JSON keys):
`出表日期`, `年度`, `季別`, `公司代號`, `公司名稱`, `財測序號`, `涵蓋期間`, `當季經會計師查核或核閱數`, `截至當季經會計師查核或核閱數`, `當季稅前(綜合)損益預測數`, `截至當季稅前(綜合)損益預測數`

## `GET /opendata/t187ap17_L`
Profitability analysis summary of all listed companies  <!-- 上市公司營益分析查詢彙總表(全體公司彙總報表) -->

Response item fields (exact JSON keys):
`出表日期`, `年度`, `季別`, `公司代號`, `公司名稱`, `營業收入(百萬元)`, `毛利率(%)(營業毛利)/(營業收入)`, `營業利益率(%)(營業利益)/(營業收入)`, `稅前純益率(%)(稅前純益)/(營業收入)`, `稅後純益率(%)(稅後純益)/(營業收入)`

## `GET /opendata/t187ap31_L`
Financial reports recognized by supervisors  <!-- 上市公司財務報告經監察人承認情形 -->

Response item fields (exact JSON keys):
`出表日期`, `公司代號`, `公司名稱`, `是否設置審計委員會`, `出具本次財務報告審查報告書之監察人姓名`, `監察人實際在任席次`

## `GET /opendata/t187ap06_L_bd`
Income statements of listed companies - securities & futures industry  <!-- 上市公司綜合損益表(證券期貨業) -->

Response item fields (exact JSON keys):
`出表日期`, `年度`, `季別`, `公司代號`, `公司名稱`, `收益`, `支出及費用`, `營業利益`, `營業外損益`, `稅前淨利（淨損）`, `所得稅費用（利益）`, `繼續營業單位本期淨利（淨損）`, `停業單位損益`, `合併前非屬共同控制股權損益`, `本期淨利（淨損）`, `本期其他綜合損益（稅後淨額）`, `合併前非屬共同控制股權綜合損益淨額`, `本期綜合損益總額`, `淨利（損）歸屬於母公司業主`, `淨利（淨損）歸屬於共同控制下前手權益`, `淨利（損）歸屬於非控制權益`, `綜合損益總額歸屬於母公司業主`, `綜合損益總額歸屬於共同控制下前手權益`, `綜合損益總額歸屬於非控制權益`, `基本每股盈餘（元）`

## `GET /opendata/t187ap06_L_ci`
Income statements of listed companies - general industry  <!-- 上市公司綜合損益表(一般業) -->

Response item fields (exact JSON keys):
`出表日期`, `年度`, `季別`, `公司代號`, `公司名稱`, `營業收入`, `營業成本`, `原始認列生物資產及農產品之利益（損失）`, `生物資產當期公允價值減出售成本之變動利益（損失）`, `營業毛利（毛損）`, `未實現銷貨（損）益`, `已實現銷貨（損）益`, `營業毛利（毛損）淨額`, `營業費用`, `其他收益及費損淨額`, `營業利益（損失）`, `營業外收入及支出`, `稅前淨利（淨損）`, `所得稅費用（利益）`, `繼續營業單位本期淨利（淨損）`, `停業單位損益`, `合併前非屬共同控制股權損益`, `本期淨利（淨損）`, `其他綜合損益（淨額）`, `合併前非屬共同控制股權綜合損益淨額`, `本期綜合損益總額`, `淨利（淨損）歸屬於母公司業主`, `淨利（淨損）歸屬於共同控制下前手權益`, `淨利（淨損）歸屬於非控制權益`, `綜合損益總額歸屬於母公司業主`, `綜合損益總額歸屬於共同控制下前手權益`, `綜合損益總額歸屬於非控制權益`, `基本每股盈餘（元）`

## `GET /opendata/t187ap06_L_fh`
Income statements of listed companies - financial holding industry  <!-- 上市公司綜合損益表(金控業) -->

Response item fields (exact JSON keys):
`出表日期`, `年度`, `季別`, `公司代號`, `公司名稱`, `利息淨收益`, `其他收益及費損淨額`, `利息以外淨收益`, `淨收益`, `呆帳費用、承諾及保證責任準備提存`, `保險負債準備淨變動`, `營業費用`, `繼續營業單位稅前損益`, `繼續營業單位本期淨利（淨損）`, `停業單位損益`, `本期稅後淨利（淨損）`, `本期其他綜合損益（稅後淨額）`, `本期綜合損益總額`, `淨利（淨損）歸屬於母公司業主`, `淨利（淨損）歸屬於共同控制下前手權益`, `淨利（淨損）歸屬於非控制權益`, `綜合損益總額歸屬於母公司業主`, `綜合損益總額歸屬於共同控制下前手權益`, `綜合損益總額歸屬於非控制權益`, `基本每股盈餘（元）`

## `GET /opendata/t187ap06_L_ins`
Income statements of listed companies - insurance industry  <!-- 上市公司綜合損益表(保險業) -->

Response item fields (exact JSON keys):
`出表日期`, `年度`, `季別`, `公司代號`, `公司名稱`, `營業收入`, `營業成本`, `營業費用`, `營業利益（損失）`, `營業外收入及支出`, `繼續營業單位稅前純益（純損）`, `所得稅費用（利益）`, `繼續營業單位本期純益（純損）`, `停業單位損益`, `合併前非屬共同控制股權損益`, `本期淨利（淨損）`, `其他綜合損益（淨額）`, `合併前非屬共同控制股權綜合損益淨額`, `本期綜合損益總額`, `淨利（淨損）歸屬於母公司業主`, `淨利（淨損）歸屬於共同控制下前手權益`, `淨利（淨損）歸屬於非控制權益`, `綜合損益總額歸屬於母公司業主`, `綜合損益總額歸屬於共同控制下前手權益`, `綜合損益總額歸屬於非控制權益`, `基本每股盈餘（元）`

## `GET /opendata/t187ap06_L_mim`
Income statements of listed companies - mixed/other industry  <!-- 上市公司綜合損益表(異業) -->

Response item fields (exact JSON keys):
`出表日期`, `年度`, `季別`, `公司代號`, `公司名稱`, `收入`, `支出`, `繼續營業單位稅前淨利（淨損）`, `所得稅費用（利益）`, `繼續營業單位本期淨利（淨損）`, `停業單位損益`, `本期淨利（淨損）`, `其他綜合損益`, `本期綜合損益總額`, `淨利（淨損）歸屬於母公司業主`, `淨利（淨損）歸屬於共同控制下前手權益`, `淨利（淨損）歸屬於非控制權益`, `綜合損益總額歸屬於母公司業主`, `綜合損益總額歸屬於共同控制下前手權益`, `綜合損益總額歸屬於非控制權益`, `基本每股盈餘（元）`

## `GET /opendata/t187ap07_L_bd`
Balance sheets of listed companies - securities & futures industry  <!-- 上市公司資產負債表(證券期貨業) -->

Response item fields (exact JSON keys):
`出表日期`, `年度`, `季別`, `公司代號`, `公司名稱`, `流動資產`, `非流動資產`, `資產總額`, `流動負債`, `非流動負債`, `負債總額`, `股本`, `權益－具證券性質之虛擬通貨`, `資本公積`, `保留盈餘`, `其他權益`, `庫藏股票`, `歸屬於母公司業主之權益合計`, `共同控制下前手權益`, `合併前非屬共同控制股權`, `非控制權益`, `權益總額`, `預收股款（權益項下）之約當發行股數`, `待註銷股本股數`, `母公司暨子公司所持有之母公司庫藏股股數`, `每股參考淨值`

## `GET /opendata/t187ap07_L_ci`
Balance sheets of listed companies - general industry  <!-- 上市公司資產負債表(一般業) -->

Response item fields (exact JSON keys):
`出表日期`, `年度`, `季別`, `公司代號`, `公司名稱`, `流動資產`, `非流動資產`, `資產總額`, `流動負債`, `非流動負債`, `負債總額`, `股本`, `權益─具證券性質之虛擬通貨`, `資本公積`, `保留盈餘`, `其他權益`, `庫藏股票`, `歸屬於母公司業主之權益合計`, `共同控制下前手權益`, `合併前非屬共同控制股權`, `非控制權益`, `權益總額`, `預收股款（權益項下）之約當發行股數`, `待註銷股本股數`, `母公司暨子公司所持有之母公司庫藏股股數`, `每股參考淨值`

## `GET /opendata/t187ap07_L_fh`
Balance sheets of listed companies - financial holding industry  <!-- 上市公司資產負債表(金控業) -->

Response item fields (exact JSON keys):
`出表日期`, `年度`, `季別`, `公司代號`, `公司名稱`, `現金及約當現金`, `存放央行及拆借金融同業`, `透過損益按公允價值衡量之金融資產`, `透過其他綜合損益按公允價值衡量之金融資產`, `按攤銷後成本衡量之債務工具投資`, `避險之金融資產`, `附賣回票券及債券投資`, `應收款項－淨額`, `本期所得稅資產`, `待出售資產－淨額`, `待分配予業主之資產－淨額`, `貼現及放款－淨額`, `再保險合約資產－淨額`, `採用權益法之投資－淨額`, `受限制資產－淨額`, `其他金融資產－淨額`, `投資性不動產－淨額`, `不動產及設備－淨額`, `使用權資產－淨額`, `無形資產－淨額`, `遞延所得稅資產`, `其他資產－淨額`, `資產總計`, `央行及金融同業存款`, `央行及同業融資`, `透過損益按公允價值衡量之金融負債`, `避險之金融負債`, `附買回票券及債券負債`, `應付商業本票－淨額`, `應付款項`, `本期所得稅負債`, `與待出售資產直接相關之負債`, `存款及匯款`, `應付債券`, `其他借款`, `特別股負債`, `負債準備`, `其他金融負債`, `租賃負債`, `遞延所得稅負債`, `其他負債`, `負債總計`, `股本`, `資本公積`, `保留盈餘`, `其他權益`, `庫藏股票`, `共同控制下前手權益`, `歸屬於母公司業主之權益`, `非控制權益`, `權益總計`, `待註銷股本股數（單位：股）`, `預收股款（權益項下）之約當發行股數（單位：股）`, `母公司暨子公司所持有之母公司庫藏股股數（單位：股）`, `每股參考淨值`

## `GET /opendata/t187ap07_L_ins`
Balance sheets of listed companies - insurance industry  <!-- 上市公司資產負債表(保險業) -->

Response item fields (exact JSON keys):
`出表日期`, `年度`, `季別`, `公司代號`, `公司名稱`, `現金及約當現金`, `應收款項`, `本期所得稅資產`, `待出售資產`, `待分配予業主之資產（或處分群組）`, `投資`, `再保險合約資產`, `不動產及設備`, `使用權資產`, `無形資產`, `遞延所得稅資產`, `其他資產`, `分離帳戶保險商品資產`, `資產總計`, `短期債務`, `應付款項`, `本期所得稅負債`, `與待出售資產直接相關之負債`, `透過損益按公允價值衡量之金融負債`, `避險之金融負債`, `應付債券`, `特別股負債`, `其他金融負債`, `租賃負債`, `保險負債`, `具金融商品性質之保險契約準備`, `外匯價格變動準備`, `負債準備`, `遞延所得稅負債`, `其他負債`, `分離帳戶保險商品負債`, `負債總計`, `股本`, `權益─具證券性質之虛擬通貨`, `資本公積`, `保留盈餘`, `其他權益`, `庫藏股票`, `歸屬於母公司業主之權益合計`, `共同控制下前手權益`, `合併前非屬共同控制股權`, `非控制權益`, `權益總計`, `負債及權益總計`, `待註銷股本股數（單位：股）`, `母公司暨子公司所持有之母公司庫藏股股數（單位：股）`, `預收股款（權益項下）之約當發行股數（單位：股）`, `每股參考淨值`

## `GET /opendata/t187ap07_L_mim`
Balance sheets of listed companies - mixed/other industry  <!-- 上市公司資產負債表(異業) -->

Response item fields (exact JSON keys):
`出表日期`, `年度`, `季別`, `公司代號`, `公司名稱`, `流動資產`, `非流動資產`, `資產總額`, `流動負債`, `非流動負債`, `負債總額`, `股本`, `權益－具證券性質之虛擬通貨`, `資本公積`, `保留盈餘`, `其他權益`, `庫藏股票`, `歸屬於母公司業主之權益合計`, `共同控制下前手權益`, `非控制權益`, `權益總額`, `待註銷股本股數（單位：股）`, `預收股款（權益項下）之約當發行股數（單位：股）`, `母公司暨子公司所持有之母公司庫藏股股數（單位：股）`, `每股參考淨值`

## `GET /opendata/t187ap07_X_basi`
Balance sheets of public companies - banking industry  <!-- 公發公司資產負債表-金融業 -->

Response item fields (exact JSON keys):
`出表日期`, `年度`, `季別`, `公司代號`, `公司名稱`, `現金及約當現金`, `存放央行及拆借銀行同業`, `透過損益按公允價值衡量之金融資產`, `透過其他綜合損益按公允價值衡量之金融資產`, `按攤銷後成本衡量之債務工具投資`, `避險之衍生金融資產淨額`, `附賣回票券及債券投資淨額`, `應收款項－淨額`, `當期所得稅資產`, `待出售資產－淨額`, `待分配予業主之資產－淨額`, `貼現及放款－淨額`, `採用權益法之投資－淨額`, `受限制資產－淨額`, `其他金融資產－淨額`, `不動產及設備－淨額`, `使用權資產－淨額`, `投資性不動產投資－淨額`, `無形資產－淨額`, `遞延所得稅資產`, `其他資產－淨額`, `資產總額`, `央行及銀行同業存款`, `央行及同業融資`, `透過損益按公允價值衡量之金融負債`, `避險之衍生金融負債－淨額`, `附買回票券及債券負債`, `應付款項`, `當期所得稅負債`, `與待出售資產直接相關之負債`, `存款及匯款`, `應付金融債券`, `應付公司債`, `特別股負債`, `其他金融負債`, `負債準備`, `租賃負債`, `遞延所得稅負債`, `其他負債`, `負債總額`, `股本`, `權益─具證券性質之虛擬通貨`, `資本公積`, `保留盈餘`, `其他權益`, `庫藏股票`, `歸屬於母公司業主之權益合計`, `共同控制下前手權益`, `合併前非屬共同控制股權`, `非控制權益`, `權益總額`, `待註銷股本股數（單位：股）`, `母公司暨子公司所持有之母公司庫藏股股數（單位：股）`, `預收股款（權益項下）之約當發行股數（單位：股）`, `每股參考淨值`

## `GET /opendata/t187ap07_X_bd`
Balance sheets of public companies - securities & futures industry  <!-- 公發公司資產負債表-證券期貨業 -->

Response item fields (exact JSON keys):
`出表日期`, `年度`, `季別`, `公司代號`, `公司名稱`, `流動資產`, `非流動資產`, `資產總計`, `流動負債`, `非流動負債`, `負債總計`, `股本`, `權益－具證券性質之虛擬通貨`, `資本公積`, `保留盈餘（或累積虧損）`, `其他權益`, `庫藏股票`, `歸屬於母公司業主權益合計`, `共同控制下前手權益`, `合併前非屬共同控制股權`, `非控制權益`, `權益總計`, `待註銷股本股數（單位：股）`, `預收股款（權益項下）之約當發行股數（單位：股）`, `母公司暨子公司持有之母公司庫藏股股數（單位：股）`, `每股參考淨值`

## `GET /opendata/t187ap07_X_fh`
Balance sheets of public companies - financial holding industry  <!-- 公發公司資產負債表-金控業 -->

Response item fields (exact JSON keys):
`出表日期`, `年度`, `季別`, `公司代號`, `公司名稱`, `現金及約當現金`, `存放央行及拆借金融同業`, `透過損益按公允價值衡量之金融資產`, `透過其他綜合損益按公允價值衡量之金融資產`, `按攤銷後成本衡量之債務工具投資`, `避險之衍生金融資產`, `附賣回票券及債券投資`, `應收款項－淨額`, `當期所得稅資產`, `待出售資產－淨額`, `空格`, `貼現及放款－淨額`, `再保險合約資產－淨額`, `採用權益法之投資－淨額`, `受限制資產－淨額`, `其他金融資產－淨額`, `投資性不動產－淨額`, `不動產及設備－淨額`, `使用權資產－淨額`, `無形資產－淨額`, `遞延所得稅資產`, `其他資產－淨額`, `資產總額`, `央行及金融同業存款`, `央行及同業融資`, `透過損益按公允價值衡量之金融負債`, `避險之衍生金融負債`, `附買回票券及債券負債`, `應付商業本票－淨額`, `應付款項`, `當期所得稅負債`, `與待出售資產直接相關之負債`, `存款及匯款`, `應付債券`, `其他借款`, `特別股負債`, `負債準備`, `其他金融負債`, `租賃負債`, `遞延所得稅負債`, `其他負債`, `負債總額`, `股本`, `資本公積`, `保留盈餘`, `其他權益`, `庫藏股票`, `共同控制下前手權益`, `歸屬於母公司業主之權益`, `非控制權益`, `權益總額`, `待註銷股本股數（單位：股）`, `預收股款（權益項下）之約當發行股數（單位：股）`, `母公司暨子公司所持有之母公司庫藏股股數（單位：股）`, `每股參考淨值`

## `GET /opendata/t187ap07_X_ins`
Balance sheets of public companies - insurance industry  <!-- 公發公司資產負債表-保險業 -->

Response item fields (exact JSON keys):
`出表日期`, `年度`, `季別`, `公司代號`, `公司名稱`, `現金及約當現金`, `應收款項`, `本期所得稅資產`, `待出售資產`, `待分配予業主之資產（或處分群組）`, `投資`, `再保險合約資產`, `不動產及設備`, `使用權資產`, `無形資產`, `遞延所得稅資產`, `其他資產`, `分離帳戶保險商品資產`, `資產總計`, `短期債務`, `應付款項`, `本期所得稅負債`, `與待出售資產直接相關之負債`, `透過損益按公允價值衡量之金融負債`, `避險之衍生金融負債`, `應付債券`, `特別股負債`, `其他金融負債`, `租賃負債`, `保險負債`, `具金融商品性質之保險契約準備`, `外匯價格變動準備`, `負債準備`, `遞延所得稅負債`, `其他負債`, `分離帳戶保險商品負債`, `負債總計`, `股本`, `權益─具證券性質之虛擬通貨`, `資本公積`, `保留盈餘`, `其他權益`, `庫藏股票`, `歸屬於母公司業主之權益合計`, `共同控制下前手權益`, `合併前非屬共同控制股權`, `非控制權益`, `權益總計`, `負債及權益總計`, `待註銷股本股數（單位：股）`, `母公司暨子公司所持有之母公司庫藏股股數（單位：股）`, `預收股款（權益項下）之約當發行股數（單位：股）`, `每股參考淨值`

## `GET /opendata/t187ap11_P`
Director/supervisor shareholding balance details (public companies)  <!-- 公發公司董監事持股餘額明細 -->

Response item fields (exact JSON keys):
`出表日期`, `資料年月`, `公司代號`, `公司名稱`, `職稱`, `姓名`, `選任時持股`, `目前持股`, `設質股數`, `設質股數佔持股比例`, `內部人關係人目前持股合計`, `內部人關係人設質股數`, `內部人關係人設質比例`

## `GET /opendata/t187ap06_L_basi`
Income statements of listed companies - banking industry  <!-- 上市公司綜合損益表(金融業) -->

Response item fields (exact JSON keys):
`出表日期`, `年度`, `季別`, `公司代號`, `公司名稱`, `利息淨收益`, `利息以外淨損益`, `呆帳費用、承諾及保證責任準備提存`, `營業費用`, `繼續營業單位稅前淨利（淨損）`, `所得稅費用（利益）`, `繼續營業單位本期淨利（淨損）`, `停業單位損益`, `合併前非屬共同控制股權損益`, `本期淨利（淨損）`, `其他綜合損益（稅後）`, `合併前非屬共同控制股權綜合損益淨額`, `本期綜合損益總額（稅後）`, `淨利（損）歸屬於母公司業主`, `淨利（損）歸屬於共同控制下前手權益`, `淨利（損）歸屬於非控制權益`, `綜合損益總額歸屬於母公司業主`, `綜合損益總額歸屬於共同控制下前手權益`, `綜合損益總額歸屬於非控制權益`, `基本每股盈餘（元）`

## `GET /opendata/t187ap07_L_basi`
Balance sheets of listed companies - banking industry  <!-- 上市公司資產負債表(金融業) -->

Response item fields (exact JSON keys):
`出表日期`, `年度`, `季別`, `公司代號`, `公司名稱`, `現金及約當現金`, `存放央行及拆借銀行同業`, `透過損益按公允價值衡量之金融資產`, `透過其他綜合損益按公允價值衡量之金融資產`, `按攤銷後成本衡量之債務工具投資`, `避險之金融資產`, `附賣回票券及債券投資淨額`, `應收款項－淨額`, `本期所得稅資產`, `待出售資產－淨額`, `待分配予業主之資產－淨額`, `貼現及放款－淨額`, `採用權益法之投資－淨額`, `受限制資產－淨額`, `其他金融資產－淨額`, `不動產及設備－淨額`, `使用權資產－淨額`, `投資性不動產－淨額`, `無形資產－淨額`, `遞延所得稅資產`, `其他資產－淨額`, `資產總計`, `央行及銀行同業存款`, `央行及同業融資`, `透過損益按公允價值衡量之金融負債`, `避險之金融負債`, `附買回票券及債券負債`, `應付款項`, `本期所得稅負債`, `與待出售資產直接相關之負債`, `存款及匯款`, `應付金融債券`, `應付公司債`, `特別股負債`, `其他金融負債`, `負債準備`, `租賃負債`, `遞延所得稅負債`, `其他負債`, `負債總計`, `股本`, `權益─具證券性質之虛擬通貨`, `資本公積`, `保留盈餘`, `其他權益`, `庫藏股票`, `歸屬於母公司業主之權益合計`, `共同控制下前手權益`, `合併前非屬共同控制股權`, `非控制權益`, `權益總計`, `待註銷股本股數（單位：股）`, `母公司暨子公司所持有之母公司庫藏股股數（單位：股）`, `預收股款（權益項下）之約當發行股數（單位：股）`, `每股參考淨值`
