# mall-api

| Version | Update Time | Status | Author | Description |
|---------|-------------|--------|--------|-------------|
|v2026-06-14 21:32:08|2026-06-14 21:32:08|auto|@yu|Created by smart-doc|



## OpenAPI v1 —— 股东持仓 + 港股通 / 沪深港通 / CCASS 数据端点（stock.shareholder scope）。

&lt;p&gt;共 9 个端点：&lt;/p&gt;
&lt;p&gt;&lt;b&gt;① 股东持仓（3 个，阶段 11 从 site internal 迁入）：&lt;/b&gt;&lt;/p&gt;
&lt;ol&gt;
  &lt;li&gt;{@code holder/find-stocks} —— 通过股东名反查持仓股票（社保、汇金、明星基金经理 ...）&lt;/li&gt;
  &lt;li&gt;{@code holder/holdings} —— 某股东在指定报告期的全量持仓明细&lt;/li&gt;
  &lt;li&gt;{@code classify/list} —— 股东类别分组目录（社保 / 汇金 / 公募 / 私募 ...）&lt;/li&gt;
&lt;/ol&gt;

&lt;p&gt;&lt;b&gt;② 港股通 / 沪深港通 / CCASS（6 个，2026-05-22 新增）：&lt;/b&gt;&lt;/p&gt;
&lt;ol start=&quot;4&quot;&gt;
  &lt;li&gt;{@code ccass-hold} —— CCASS 持股统计（按股票汇总）&lt;/li&gt;
  &lt;li&gt;{@code ccass-detail} —— CCASS 机构维度持股明细&lt;/li&gt;
  &lt;li&gt;{@code hk-hold} —— 沪深港通持股明细（北向 / 南向）&lt;/li&gt;
  &lt;li&gt;{@code hsgt-list} —— 沪深港通可交易股票名单（4 通道：HK_SH/HK_SZ/SH_HK/SZ_HK）&lt;/li&gt;
  &lt;li&gt;{@code ggt-daily} —— 港股通每日成交统计（市场级，无 tsCode）&lt;/li&gt;
  &lt;li&gt;{@code ggt-monthly} —— 港股通每月成交统计（市场级，无 tsCode）&lt;/li&gt;
&lt;/ol&gt;

&lt;p&gt;套餐归属：Plus 及以上。
### 通过股东名反查持仓股票列表（支持多名联合查询）。
**URL:** /openapi/v1/stock/shareholder/holder/find-stocks

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 通过股东名反查持仓股票列表（支持多名联合查询）。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|holders|array|false|股东名列表（中文）。<b>必填</b>。<br/><br/><p><b>多名是交集</b>：返回"每个股东都持有"的票（不是并集）。<br/><b>LIKE 模糊匹配</b>：可写简称（如 {@code "中央汇金"} 可命中全称）。</p><br/><br/><p><b>示例</b>：</p><br/><pre><br/>["社保基金"]                  // 单名模糊：所有名字含"社保基金"的组合<br/>["社保基金", "中央汇金"]      // 交集：两类股东共同持有的票<br/></pre>|-|
|endDate|string|false|报告期<b>下界</b>，格式 {@code YYYYMMDD}（容错 {@code YYYY-MM-DD}）。<b>必填</b>。<br/><br/><p>语义是 {@code end_date >= endDate}（<b>不是</b>"截止日"）：查最新持仓传最近季末日<br/>（如 {@code "20260331"}）；想看更久历史传更早日期。缺失/格式错 → code=2 参数异常。</p>|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/stock/shareholder/holder/find-stocks?holders=,&endDate='
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─tsCode|string|股票代码（带交易所后缀），如 {@code "600519.SH"} / {@code "000001.SZ"} / {@code "832149.BJ"}。|-|
|└─symbol|string|纯数字股票代码（不带交易所后缀），如 {@code "600519"}。|-|
|└─name|string|股票中文简称，如 {@code "贵州茅台"} / {@code "中国平安"}。|-|
|└─area|string|注册地（省 / 直辖市），如 {@code "贵州"} / {@code "北京"} / {@code "广东"}。|-|
|└─industry|string|所属行业（口径同申万），如 {@code "白酒"} / {@code "保险"} / {@code "半导体"}。|-|
|└─cnSpell|string|公司名称拼音首字母，如贵州茅台 = {@code "GZMT"}。可用于按拼音搜索。|-|
|└─market|string|市场板块名：{@code "主板"} / {@code "创业板"} / {@code "科创板"} / {@code "北交所"}。|-|
|└─listDate|string|上市日期（Date 对象，JSON 序列化为时间戳）。|-|
|└─listDateStr|string|上市日期格式化字符串 {@code "YYYYMMDD"}（如 {@code "19990601"} = 1999 年 6 月 1 日）。<br/><p>给前端展示用，比 {@link #listDate} 更易读。</p>|-|
|└─actName|string|实际控制人姓名 / 机构名（如 {@code "国资委"} / {@code "马化腾"}）。可能为空。|-|
|└─actEntType|string|实控人类型：{@code "G"}（国企）/ {@code "P"}（私企）/ {@code "F"}（外资）等。可能为空。|-|
|└─exchange|string|交易所代码：{@code "SSE"}（上交所）/ {@code "SZSE"}（深交所）/ {@code "BSE"}（北交所）。|-|
|└─currType|string|计价币种：{@code "CNY"}（人民币）/ {@code "HKD"}（港币）/ {@code "USD"}（美元）等。|-|
|└─listStatus|string|上市状态：{@code "L"}（在市）/ {@code "D"}（已退市）/ {@code "P"}（暂停上市）。|-|
|└─delistDate|string|退市日期（Date 对象）。在市股票为 null。|-|
|└─delistDateStr|string|退市日期格式化字符串 {@code "YYYYMMDD"}。在市股票为 null。|-|
|└─isHs|string|是否沪深港通标的：{@code "H"}（沪股通）/ {@code "S"}（深股通）/ {@code "N"}（不是）。|-|
|└─enName|string|公司英文名（如有）。|-|
|└─fullName|string|公司中文全称，如 {@code "贵州茅台酒股份有限公司"}。|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "tsCode": "",
      "symbol": "",
      "name": "",
      "area": "",
      "industry": "",
      "cnSpell": "",
      "market": "",
      "listDate": "yyyy-MM-dd HH:mm:ss",
      "listDateStr": "",
      "actName": "",
      "actEntType": "",
      "exchange": "",
      "currType": "",
      "listStatus": "",
      "delistDate": "yyyy-MM-dd HH:mm:ss",
      "delistDateStr": "",
      "isHs": "",
      "enName": "",
      "fullName": ""
    }
  ],
  "traceId": ""
}
```

### 某股东在指定报告期的全量持仓明细（个股 + 持股数 + 比例）。<br>{@code calAvgPrice=1} 时附加均价计算。
**URL:** /openapi/v1/stock/shareholder/holder/holdings

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 某股东在指定报告期的全量持仓明细（个股 + 持股数 + 比例）。
{@code calAvgPrice=1} 时附加均价计算。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|holder|string|false|股东名（中文，<b>精确匹配全称</b>，与 find-stocks 的模糊匹配不同）。<b>必填</b>。<br/><p>支持英文逗号分隔多个（并集 IN 查询）。<br/>例如 {@code "中央汇金资产管理有限责任公司"} / {@code "社保基金一零一组合,社保基金一零八组合"}。<br/>全称可从 find-stocks 结果或 {@code classify/list} 字典获得。</p>|-|
|endDate|string|false|报告期<b>下界</b>，格式 {@code YYYYMMDD}（容错 {@code YYYY-MM-DD}）。<b>必填</b>。<br/><p>语义是 {@code end_date >= endDate}（<b>不是</b>"截止日"）。缺失/格式错 → code=2 参数异常。</p>|-|
|calAvgPrice|int32|false|是否计算均价。<br/><br/><ul><br/>  <li>{@code 0} —— 不计算均价（默认，速度快）</li><br/>  <li>{@code 1} —— 计算均价（基于报告期内 K 线，耗时增加）</li><br/></ul>|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/stock/shareholder/holder/holdings?calAvgPrice=0&holder=&endDate='
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─tsCode|string|股票代码（带交易所后缀），如 {@code "600519.SH"}。|-|
|└─tsCodeName|string|股票中文简称，如 {@code "贵州茅台"}。|-|
|└─annDate|string|公告日期。|-|
|└─endDate|string|报告期截止日（季末日）。|-|
|└─holderName|string|股东中文名（如 {@code "中央汇金资产管理有限责任公司"} / {@code "社保基金一零一组合"}）。|-|
|└─holdAmount|string|持股数量（万股，字符串以避免精度问题）。|-|
|└─holdRatio|string|占总股本比例（%）。{@code "5.00"} 表示 5%。|-|
|└─holdFloatRatio|string|占流通股本比例（%）。一般比 {@link #holdRatio} 更高。|-|
|└─holdChange|string|持股变动数量（万股）。<br/><ul><br/>  <li>正数 —— 增持</li><br/>  <li>负数 —— 减持</li><br/>  <li>{@code "0"} —— 持仓未变</li><br/>  <li>空 —— 新进 / 退出（与上一报告期对比）</li><br/></ul>|-|
|└─holderType|string|股东类型代码。<br/><ul><br/>  <li>{@code "G"} —— 国资</li><br/>  <li>{@code "P"} —— 个人</li><br/>  <li>{@code "C"} —— 公司</li><br/>  <li>{@code "F"} —— 境外</li><br/></ul>|-|
|└─holderCategory|string|股东类别（中文细分）。<br/><p>例如 {@code "社保"} / {@code "汇金"} / {@code "公募基金"} / {@code "私募基金"} / {@code "QFII"} / {@code "险资"} / {@code "信托"}。</p>|-|
|└─averagePrice|string|报告期内平均买入成本估算（元，字符串）。<br/><p>仅当请求 {@code calAvgPrice=1} 时才有值；基于该报告期内 K 线均价反推。</p>|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "tsCode": "",
      "tsCodeName": "",
      "annDate": "yyyy-MM-dd HH:mm:ss",
      "endDate": "yyyy-MM-dd HH:mm:ss",
      "holderName": "",
      "holdAmount": "",
      "holdRatio": "",
      "holdFloatRatio": "",
      "holdChange": "",
      "holderType": "",
      "holderCategory": "",
      "averagePrice": ""
    }
  ],
  "traceId": ""
}
```

### 股东类别分组目录（用于 holder filter 字典）。无入参。
**URL:** /openapi/v1/stock/shareholder/classify/list

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 股东类别分组目录（用于 holder filter 字典）。无入参。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/stock/shareholder/classify/list'
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─firstClassify|string|No comments found.|-|
|└─secondClassifyList|array|No comments found.|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "firstClassify": "",
      "secondClassifyList": [
        ""
      ]
    }
  ],
  "traceId": ""
}
```

### CCASS 持股统计（按股票汇总）。<br>对应 PG 表 {@code stock_ccass_hold}，反映港资 / 国际机构对单只港股的整体集中度。<br>tsCode 必填（带 .HK 后缀）。
**URL:** /openapi/v1/stock/shareholder/ccass-hold

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** CCASS 持股统计（按股票汇总）。
<p>对应 PG 表 {@code stock_ccass_hold}，反映港资 / 国际机构对单只港股的整体集中度。
<p>tsCode 必填（带 .HK 后缀）。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|page|int32|false|第几页，从 1 起。默认 1。0 / 负数会被当成 1。|-|
|size|int32|false|每页记录数。默认 50，硬上限 {@value #MAX_SIZE}。<br/><p>传入超过 {@value #MAX_SIZE} 时会被自动截断到 {@value #MAX_SIZE}（不报错）。</p>|-|
|tsCode|string|false|股票代码（带交易所后缀），如 {@code "600519.SH"} / {@code "00700.HK"}。<br/><p>ccass-hold / ccass-detail / hk-hold 必填；其他端点可空。</p>|-|
|startDate|string|false|起始日期，格式 {@code YYYYMMDD}。可空。|-|
|endDate|string|false|结束日期，格式 {@code YYYYMMDD}。可空。|-|
|type|string|false|类型过滤，仅 hsgt-list 端点使用：{@code HK_SZ}（深港通入港）/ {@code SZ_HK}（港通入深）/ {@code HK_SH} / {@code SH_HK}。可空。|-|
|exchange|string|false|交易所过滤，仅 hk-hold 端点使用：{@code SH} / {@code SZ} / {@code HK}。可空。|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/stock/shareholder/ccass-hold?page=0&size=0&type=&tsCode=&endDate=&startDate=&exchange='
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─tradeDate|string|交易日|-|
|└─tsCode|string|TS 代码（带 .HK 后缀）|-|
|└─name|string|股票名称|-|
|└─shareholding|number|CCASS 总持股量（股）|-|
|└─holdNums|int32|参与持股的 CCASS 机构数量|-|
|└─holdRatio|number|占已发行股份 / A+H 股百分比（%）|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "tradeDate": "yyyy-MM-dd HH:mm:ss",
      "tsCode": "",
      "name": "",
      "shareholding": 0,
      "holdNums": 0,
      "holdRatio": 0
    }
  ],
  "traceId": ""
}
```

### CCASS 持股明细（按机构维度展开）。<br>对应 PG 表 {@code stock_ccass_hold_detail}。同 (tradeDate, tsCode) 多行，每行一个机构。<br>tsCode 必填。
**URL:** /openapi/v1/stock/shareholder/ccass-detail

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** CCASS 持股明细（按机构维度展开）。
<p>对应 PG 表 {@code stock_ccass_hold_detail}。同 (tradeDate, tsCode) 多行，每行一个机构。
<p>tsCode 必填。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|page|int32|false|第几页，从 1 起。默认 1。0 / 负数会被当成 1。|-|
|size|int32|false|每页记录数。默认 50，硬上限 {@value #MAX_SIZE}。<br/><p>传入超过 {@value #MAX_SIZE} 时会被自动截断到 {@value #MAX_SIZE}（不报错）。</p>|-|
|tsCode|string|false|股票代码（带交易所后缀），如 {@code "600519.SH"} / {@code "00700.HK"}。<br/><p>ccass-hold / ccass-detail / hk-hold 必填；其他端点可空。</p>|-|
|startDate|string|false|起始日期，格式 {@code YYYYMMDD}。可空。|-|
|endDate|string|false|结束日期，格式 {@code YYYYMMDD}。可空。|-|
|type|string|false|类型过滤，仅 hsgt-list 端点使用：{@code HK_SZ}（深港通入港）/ {@code SZ_HK}（港通入深）/ {@code HK_SH} / {@code SH_HK}。可空。|-|
|exchange|string|false|交易所过滤，仅 hk-hold 端点使用：{@code SH} / {@code SZ} / {@code HK}。可空。|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/stock/shareholder/ccass-detail?page=0&size=0&exchange=&tsCode=&startDate=&type=&endDate='
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─tradeDate|string|交易日|-|
|└─tsCode|string|TS 代码|-|
|└─name|string|股票名称|-|
|└─colParticipantId|string|参与者编号（CCASS 内部唯一 ID）|-|
|└─colParticipantName|string|参与者名称（机构名，如 "HSBC NOMINEES (HONG KONG) LIMITED"）|-|
|└─colShareholding|number|该机构持股量（股）|-|
|└─colShareholdingPercent|number|该机构占已发行股份百分比（%）|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "tradeDate": "yyyy-MM-dd HH:mm:ss",
      "tsCode": "",
      "name": "",
      "colParticipantId": "",
      "colParticipantName": "",
      "colShareholding": 0,
      "colShareholdingPercent": 0
    }
  ],
  "traceId": ""
}
```

### 沪深港通持股明细（北向 / 南向资金对个股的持仓）。<br>对应 PG 表 {@code stock_hk_hold}。exchange = SH/SZ 时为北向持 A 股；exchange = HK 时为南向持港股。<br>tsCode 必填，可选 exchange 过滤。
**URL:** /openapi/v1/stock/shareholder/hk-hold

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 沪深港通持股明细（北向 / 南向资金对个股的持仓）。
<p>对应 PG 表 {@code stock_hk_hold}。exchange = SH/SZ 时为北向持 A 股；exchange = HK 时为南向持港股。
<p>tsCode 必填，可选 exchange 过滤。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|page|int32|false|第几页，从 1 起。默认 1。0 / 负数会被当成 1。|-|
|size|int32|false|每页记录数。默认 50，硬上限 {@value #MAX_SIZE}。<br/><p>传入超过 {@value #MAX_SIZE} 时会被自动截断到 {@value #MAX_SIZE}（不报错）。</p>|-|
|tsCode|string|false|股票代码（带交易所后缀），如 {@code "600519.SH"} / {@code "00700.HK"}。<br/><p>ccass-hold / ccass-detail / hk-hold 必填；其他端点可空。</p>|-|
|startDate|string|false|起始日期，格式 {@code YYYYMMDD}。可空。|-|
|endDate|string|false|结束日期，格式 {@code YYYYMMDD}。可空。|-|
|type|string|false|类型过滤，仅 hsgt-list 端点使用：{@code HK_SZ}（深港通入港）/ {@code SZ_HK}（港通入深）/ {@code HK_SH} / {@code SH_HK}。可空。|-|
|exchange|string|false|交易所过滤，仅 hk-hold 端点使用：{@code SH} / {@code SZ} / {@code HK}。可空。|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/stock/shareholder/hk-hold?page=0&size=0&startDate=&exchange=&endDate=&type=&tsCode='
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─tradeDate|string|交易日|-|
|└─tsCode|string|TS 代码|-|
|└─code|string|原始代码（无后缀）|-|
|└─name|string|股票名称|-|
|└─vol|number|持股数量（股）|-|
|└─ratio|number|持股占总股本比例（%）|-|
|└─exchange|string|交易所类型：{@code SH} / {@code SZ} / {@code HK}|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "tradeDate": "yyyy-MM-dd HH:mm:ss",
      "tsCode": "",
      "code": "",
      "name": "",
      "vol": 0,
      "ratio": 0,
      "exchange": ""
    }
  ],
  "traceId": ""
}
```

### 沪深港通可交易股票名单（4 通道：HK_SH/HK_SZ/SH_HK/SZ_HK）。<br>对应 PG 表 {@code stock_hsgt_list}。判断&amp;quot;该股是否被纳入沪股通 / 深股通 / 港股通&amp;quot;。<br>tsCode 可选；可选 type 过滤。
**URL:** /openapi/v1/stock/shareholder/hsgt-list

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 沪深港通可交易股票名单（4 通道：HK_SH/HK_SZ/SH_HK/SZ_HK）。
<p>对应 PG 表 {@code stock_hsgt_list}。判断"该股是否被纳入沪股通 / 深股通 / 港股通"。
<p>tsCode 可选；可选 type 过滤。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|page|int32|false|第几页，从 1 起。默认 1。0 / 负数会被当成 1。|-|
|size|int32|false|每页记录数。默认 50，硬上限 {@value #MAX_SIZE}。<br/><p>传入超过 {@value #MAX_SIZE} 时会被自动截断到 {@value #MAX_SIZE}（不报错）。</p>|-|
|tsCode|string|false|股票代码（带交易所后缀），如 {@code "600519.SH"} / {@code "00700.HK"}。<br/><p>ccass-hold / ccass-detail / hk-hold 必填；其他端点可空。</p>|-|
|startDate|string|false|起始日期，格式 {@code YYYYMMDD}。可空。|-|
|endDate|string|false|结束日期，格式 {@code YYYYMMDD}。可空。|-|
|type|string|false|类型过滤，仅 hsgt-list 端点使用：{@code HK_SZ}（深港通入港）/ {@code SZ_HK}（港通入深）/ {@code HK_SH} / {@code SH_HK}。可空。|-|
|exchange|string|false|交易所过滤，仅 hk-hold 端点使用：{@code SH} / {@code SZ} / {@code HK}。可空。|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/stock/shareholder/hsgt-list?page=0&size=0&tsCode=&exchange=&endDate=&type=&startDate='
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─tsCode|string|TS 代码|-|
|└─tradeDate|string|交易日（名单更新日期）|-|
|└─type|string|类型：HK_SZ / SZ_HK / HK_SH / SH_HK|-|
|└─name|string|股票名称|-|
|└─typeName|string|类型中文名（如"深股通"/"港股通"）|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "tsCode": "",
      "tradeDate": "yyyy-MM-dd HH:mm:ss",
      "type": "",
      "name": "",
      "typeName": ""
    }
  ],
  "traceId": ""
}
```

### 港股通每日成交统计（市场级，无 tsCode）。<br>对应 PG 表 {@code stock_ggt_daily}。{@code buyAmount - sellAmount} = 当日南向净流入。
**URL:** /openapi/v1/stock/shareholder/ggt-daily

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 港股通每日成交统计（市场级，无 tsCode）。
<p>对应 PG 表 {@code stock_ggt_daily}。{@code buyAmount - sellAmount} = 当日南向净流入。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|page|int32|false|第几页，从 1 起。默认 1。0 / 负数会被当成 1。|-|
|size|int32|false|每页记录数。默认 50，硬上限 {@value #MAX_SIZE}。<br/><p>传入超过 {@value #MAX_SIZE} 时会被自动截断到 {@value #MAX_SIZE}（不报错）。</p>|-|
|tsCode|string|false|股票代码（带交易所后缀），如 {@code "600519.SH"} / {@code "00700.HK"}。<br/><p>ccass-hold / ccass-detail / hk-hold 必填；其他端点可空。</p>|-|
|startDate|string|false|起始日期，格式 {@code YYYYMMDD}。可空。|-|
|endDate|string|false|结束日期，格式 {@code YYYYMMDD}。可空。|-|
|type|string|false|类型过滤，仅 hsgt-list 端点使用：{@code HK_SZ}（深港通入港）/ {@code SZ_HK}（港通入深）/ {@code HK_SH} / {@code SH_HK}。可空。|-|
|exchange|string|false|交易所过滤，仅 hk-hold 端点使用：{@code SH} / {@code SZ} / {@code HK}。可空。|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/stock/shareholder/ggt-daily?page=0&size=0&tsCode=&type=&endDate=&exchange=&startDate='
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─tradeDate|string|交易日|-|
|└─buyAmount|number|当日总买入成交金额（亿元）|-|
|└─buyVolume|number|当日总买入成交笔数|-|
|└─sellAmount|number|当日总卖出成交金额（亿元）|-|
|└─sellVolume|number|当日总卖出成交笔数|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "tradeDate": "yyyy-MM-dd HH:mm:ss",
      "buyAmount": 0,
      "buyVolume": 0,
      "sellAmount": 0,
      "sellVolume": 0
    }
  ],
  "traceId": ""
}
```

### 港股通每月成交统计（市场级，无 tsCode）。<br>对应 PG 表 {@code stock_ggt_monthly}。{@code startDate}/{@code endDate} 自动取前 6 位转 YYYYMM。
**URL:** /openapi/v1/stock/shareholder/ggt-monthly

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 港股通每月成交统计（市场级，无 tsCode）。
<p>对应 PG 表 {@code stock_ggt_monthly}。{@code startDate}/{@code endDate} 自动取前 6 位转 YYYYMM。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|page|int32|false|第几页，从 1 起。默认 1。0 / 负数会被当成 1。|-|
|size|int32|false|每页记录数。默认 50，硬上限 {@value #MAX_SIZE}。<br/><p>传入超过 {@value #MAX_SIZE} 时会被自动截断到 {@value #MAX_SIZE}（不报错）。</p>|-|
|tsCode|string|false|股票代码（带交易所后缀），如 {@code "600519.SH"} / {@code "00700.HK"}。<br/><p>ccass-hold / ccass-detail / hk-hold 必填；其他端点可空。</p>|-|
|startDate|string|false|起始日期，格式 {@code YYYYMMDD}。可空。|-|
|endDate|string|false|结束日期，格式 {@code YYYYMMDD}。可空。|-|
|type|string|false|类型过滤，仅 hsgt-list 端点使用：{@code HK_SZ}（深港通入港）/ {@code SZ_HK}（港通入深）/ {@code HK_SH} / {@code SH_HK}。可空。|-|
|exchange|string|false|交易所过滤，仅 hk-hold 端点使用：{@code SH} / {@code SZ} / {@code HK}。可空。|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/stock/shareholder/ggt-monthly?page=0&size=0&tsCode=&type=&startDate=&exchange=&endDate='
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─month|string|月份，{@code YYYYMM} 字符串|-|
|└─dayBuyAmt|number|当月日均买入成交金额|-|
|└─dayBuyVol|number|当月日均买入成交笔数|-|
|└─daySellAmt|number|当月日均卖出成交金额|-|
|└─daySellVol|number|当月日均卖出成交笔数|-|
|└─totalBuyAmt|number|当月总买入金额|-|
|└─totalBuyVol|number|当月总买入笔数|-|
|└─totalSellAmt|number|当月总卖出金额|-|
|└─totalSellVol|number|当月总卖出笔数|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "month": "",
      "dayBuyAmt": 0,
      "dayBuyVol": 0,
      "daySellAmt": 0,
      "daySellVol": 0,
      "totalBuyAmt": 0,
      "totalBuyVol": 0,
      "totalSellAmt": 0,
      "totalSellVol": 0
    }
  ],
  "traceId": ""
}
```

## OpenAPI v1 —— 股票基础端点（stock.basic scope）。

&lt;p&gt;对应套餐：免费档（散户引流）。5 个端点：
&lt;ol&gt;
  &lt;li&gt;{@code search} —— 按代码 / 简称 / 拼音模糊搜索&lt;/li&gt;
  &lt;li&gt;{@code list} —— 全市场股票（精简字段：tsCode/symbol/name）&lt;/li&gt;
  &lt;li&gt;{@code detail} —— 单只股票详情（公司简介级）&lt;/li&gt;
  &lt;li&gt;{@code classify} —— 行业 / 主题分类目录&lt;/li&gt;
  &lt;li&gt;{@code classify/list} —— 按分类拿成分股&lt;/li&gt;
&lt;/ol&gt;

&lt;p&gt;这些端点以前挂在 &lt;code&gt;/stock/api/stock/...&lt;/code&gt;（站内无鉴权裸奔）；
阶段 11 全部迁到 OpenAPI 路径并补 &lt;code&gt;@OpenApiScope(&quot;stock.basic&quot;)&lt;/code&gt;，关闭&quot;绕过套餐&quot;漏洞。
### 按代码 / 简称 / 拼音模糊搜索股票。返回 [{tsCode, symbol, name}]。
**URL:** /openapi/v1/stock/basic/search

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 按代码 / 简称 / 拼音模糊搜索股票。返回 [{tsCode, symbol, name}]。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|nameOrCode|string|false|股票代码 / 简称 / 中文名 / 拼音首字母（任选其一）。<br/><br/><p><b>示例</b>：</p><br/><ul><br/>  <li>{@code "600519"} —— 纯数字代码</li><br/>  <li>{@code "600519.SH"} —— 带交易所后缀的 ts_code</li><br/>  <li>{@code "茅台"} —— 中文简称</li><br/>  <li>{@code "贵州茅台"} —— 中文全称</li><br/>  <li>{@code "GZMT"} —— 拼音首字母</li><br/></ul><br/><br/><p>支持模糊匹配；多解时返回所有候选，由调用方自行二选一。</p>|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/stock/basic/search?nameOrCode='
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─tsCode|string|股票代码（带交易所后缀）。<br/><br/><p>格式：{@code <symbol>.<exchange>}，例如：</p><br/><ul><br/>  <li>{@code "600519.SH"} —— 上交所主板</li><br/>  <li>{@code "000001.SZ"} —— 深交所主板</li><br/>  <li>{@code "300750.SZ"} —— 深交所创业板</li><br/>  <li>{@code "688981.SH"} —— 上交所科创板</li><br/>  <li>{@code "832149.BJ"} —— 北交所</li><br/></ul><br/><br/><p><b>这是后续所有数据查询的主键</b>，几乎每个端点都需要它。</p>|-|
|└─symbol|string|纯数字股票代码（无交易所后缀），例如 {@code "600519"} / {@code "000001"}。<br/><p>主要用于显示；实际查询请用 {@link #tsCode}。</p>|-|
|└─name|string|股票中文名（一般是简称），例如 {@code "贵州茅台"} / {@code "中国平安"}。|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "tsCode": "",
      "symbol": "",
      "name": ""
    }
  ],
  "traceId": ""
}
```

### 全市场股票精简列表（通常 5000+ 条；MCP 端会截断到 200）。
**URL:** /openapi/v1/stock/basic/list

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 全市场股票精简列表（通常 5000+ 条；MCP 端会截断到 200）。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/stock/basic/list'
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─tsCode|string|股票代码（带交易所后缀）。<br/><br/><p>格式：{@code <symbol>.<exchange>}，例如：</p><br/><ul><br/>  <li>{@code "600519.SH"} —— 上交所主板</li><br/>  <li>{@code "000001.SZ"} —— 深交所主板</li><br/>  <li>{@code "300750.SZ"} —— 深交所创业板</li><br/>  <li>{@code "688981.SH"} —— 上交所科创板</li><br/>  <li>{@code "832149.BJ"} —— 北交所</li><br/></ul><br/><br/><p><b>这是后续所有数据查询的主键</b>，几乎每个端点都需要它。</p>|-|
|└─symbol|string|纯数字股票代码（无交易所后缀），例如 {@code "600519"} / {@code "000001"}。<br/><p>主要用于显示；实际查询请用 {@link #tsCode}。</p>|-|
|└─name|string|股票中文名（一般是简称），例如 {@code "贵州茅台"} / {@code "中国平安"}。|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "tsCode": "",
      "symbol": "",
      "name": ""
    }
  ],
  "traceId": ""
}
```

### 单只股票详情（公司简介级：名称、上市日、注册地、行业、交易所、currType）。
**URL:** /openapi/v1/stock/basic/detail

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 单只股票详情（公司简介级：名称、上市日、注册地、行业、交易所、currType）。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|tsCode|string|false|股票代码（带交易所后缀）。<br/><br/><p>格式：{@code <symbol>.<exchange>}，例如 {@code "600519.SH"} / {@code "000001.SZ"} / {@code "832149.BJ"}。</p><br/><br/><p>本端点要求<b>精确匹配</b>，不支持模糊查询。若只知道公司名，先调<br/>{@code /openapi/v1/stock/basic/search} 拿到 tsCode。</p>|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/stock/basic/detail?tsCode='
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|object|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─tsCode|string|股票代码（带交易所后缀），如 {@code "600519.SH"} / {@code "000001.SZ"} / {@code "832149.BJ"}。|-|
|└─symbol|string|纯数字股票代码（不带交易所后缀），如 {@code "600519"}。|-|
|└─name|string|股票中文简称，如 {@code "贵州茅台"} / {@code "中国平安"}。|-|
|└─area|string|注册地（省 / 直辖市），如 {@code "贵州"} / {@code "北京"} / {@code "广东"}。|-|
|└─industry|string|所属行业（口径同申万），如 {@code "白酒"} / {@code "保险"} / {@code "半导体"}。|-|
|└─cnSpell|string|公司名称拼音首字母，如贵州茅台 = {@code "GZMT"}。可用于按拼音搜索。|-|
|└─market|string|市场板块名：{@code "主板"} / {@code "创业板"} / {@code "科创板"} / {@code "北交所"}。|-|
|└─listDate|string|上市日期（Date 对象，JSON 序列化为时间戳）。|-|
|└─listDateStr|string|上市日期格式化字符串 {@code "YYYYMMDD"}（如 {@code "19990601"} = 1999 年 6 月 1 日）。<br/><p>给前端展示用，比 {@link #listDate} 更易读。</p>|-|
|└─actName|string|实际控制人姓名 / 机构名（如 {@code "国资委"} / {@code "马化腾"}）。可能为空。|-|
|└─actEntType|string|实控人类型：{@code "G"}（国企）/ {@code "P"}（私企）/ {@code "F"}（外资）等。可能为空。|-|
|└─exchange|string|交易所代码：{@code "SSE"}（上交所）/ {@code "SZSE"}（深交所）/ {@code "BSE"}（北交所）。|-|
|└─currType|string|计价币种：{@code "CNY"}（人民币）/ {@code "HKD"}（港币）/ {@code "USD"}（美元）等。|-|
|└─listStatus|string|上市状态：{@code "L"}（在市）/ {@code "D"}（已退市）/ {@code "P"}（暂停上市）。|-|
|└─delistDate|string|退市日期（Date 对象）。在市股票为 null。|-|
|└─delistDateStr|string|退市日期格式化字符串 {@code "YYYYMMDD"}。在市股票为 null。|-|
|└─isHs|string|是否沪深港通标的：{@code "H"}（沪股通）/ {@code "S"}（深股通）/ {@code "N"}（不是）。|-|
|└─enName|string|公司英文名（如有）。|-|
|└─fullName|string|公司中文全称，如 {@code "贵州茅台酒股份有限公司"}。|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": {
    "tsCode": "",
    "symbol": "",
    "name": "",
    "area": "",
    "industry": "",
    "cnSpell": "",
    "market": "",
    "listDate": "yyyy-MM-dd HH:mm:ss",
    "listDateStr": "",
    "actName": "",
    "actEntType": "",
    "exchange": "",
    "currType": "",
    "listStatus": "",
    "delistDate": "yyyy-MM-dd HH:mm:ss",
    "delistDateStr": "",
    "isHs": "",
    "enName": "",
    "fullName": ""
  },
  "traceId": ""
}
```

### 行业 / 主题分类目录（一级 / 二级）。
**URL:** /openapi/v1/stock/basic/classify

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 行业 / 主题分类目录（一级 / 二级）。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/stock/basic/classify'
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─id|int32|行业分类 ID（申万口径）。<br/><p>用作 {@code /classify/list} 端点的 {@code id} 入参。</p>|-|
|└─name|string|行业分类中文名，如 {@code "信息技术"} / {@code "白酒"} / {@code "半导体"}。|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "id": 0,
      "name": ""
    }
  ],
  "traceId": ""
}
```

### 按分类拿成分股（id + level）。
**URL:** /openapi/v1/stock/basic/classify/list

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 按分类拿成分股（id + level）。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|id|int32|false|父级分类 ID。<br/><br/><p>由 {@code /openapi/v1/stock/basic/classify} 端点返回的 {@code id} 字段提供。<br/>例如申万一级分类"信息技术"的 id 可能是 {@code 14}（实际数值随数据更新而变）。</p>|-|
|level|int32|false|申万行业级别：{@code 1} / {@code 2} / {@code 3}。<br/><br/><ul><br/>  <li>{@code 1} —— 一级行业（如"信息技术"，全市场约 31 个一级）</li><br/>  <li>{@code 2} —— 二级行业（如"半导体"，全市场约 134 个二级）</li><br/>  <li>{@code 3} —— 三级行业（如"集成电路制造"，全市场约 346 个三级）</li><br/></ul>|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/stock/basic/classify/list?id=0&level=0'
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─classifyName|string|分类中文名（如行业名 / 概念名 / 地域名），例如 {@code "白酒"} / {@code "新能源汽车"} / {@code "广东"}。|-|
|└─stockCount|int32|该分类下的股票数量（成分股数）。|-|
|└─swCode|string|申万行业分类代码（官方编码）。<br/><br/><p><b>示例</b>：</p><br/><ul><br/>  <li>{@code "801080"} —— 申万一级"电子"</li><br/>  <li>{@code "801081"} —— 申万二级"半导体"</li><br/>  <li>{@code "801120"} —— 申万一级"食品饮料"</li><br/></ul><br/><br/><p>用于跨数据源匹配申万体系的行情 / 估值数据（如 {@code /openapi/v1/stock/index/sw-industry-quo}）。</p>|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "classifyName": "",
      "stockCount": 0,
      "swCode": ""
    }
  ],
  "traceId": ""
}
```

### 北交所新旧代码对照（{@code bse_mapping}）。可按 keyword 模糊匹配 name / oCode / nCode。<br><br>用途：精选层（老三板）转板北交所时的代码映射，跨时间口径对齐成交 / 财务 / 公告数据。<br>例如：8 字头老代码 → 9 字头北交所新代码。 
**URL:** /openapi/v1/stock/basic/bse-mapping

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 北交所新旧代码对照（{@code bse_mapping}）。可按 keyword 模糊匹配 name / oCode / nCode。

<p>用途：精选层（老三板）转板北交所时的代码映射，跨时间口径对齐成交 / 财务 / 公告数据。
例如：8 字头老代码 → 9 字头北交所新代码。</p>

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|page|int32|false|第几页，从 1 起。默认 1。0 / 负数会被当成 1。|-|
|size|int32|false|每页记录数。默认 50，硬上限 {@value #MAX_SIZE}。<br/><p>传入超过 {@value #MAX_SIZE} 时会被自动截断到 {@value #MAX_SIZE}（不报错）。</p>|-|
|keyword|string|false|通用关键字（按表内最关键文本列模糊匹配，参类级注释）。|-|
|year|int32|false|年度（fund-sales-ratio / fund-sales-vol 用）。|-|
|startYear|int32|false|起始年度（fund-sales-ratio 区间）。|-|
|endYear|int32|false|结束年度（fund-sales-ratio 区间）。|-|
|quarter|string|false|季度（fund-sales-vol，如 "1"/"2"/"3"/"4" 或 "Q1"/...）。|-|
|startDate|string|false|起始日期 {@code YYYYMMDD}。|-|
|endDate|string|false|结束日期 {@code YYYYMMDD}。|-|
|country|string|false|国家代码（eco-cal）。|-|
|currency|string|false|货币代码（eco-cal，USD/EUR/CNY/...）。|-|
|ptype|string|false|政策类型（policy-npr）。|-|
|puborg|string|false|发布机构（policy-npr）。|-|
|exchange|string|false|交易所（futures-weekly-detail，DCE/CFFEX/CZCE/SHFE/INE）。|-|
|prd|string|false|期货品种代码（futures-weekly-detail，如 CU/RB/IF）。|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/stock/basic/bse-mapping?page=0&size=0&year=0&startYear=0&endYear=0&endDate=&currency=&country=&ptype=&prd=&startDate=&exchange=&keyword=&quarter=&puborg='
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─name|string|股票名称|-|
|└─oCode|string|原代码（精选层 / 老三板）|-|
|└─nCode|string|新代码（北交所）|-|
|└─listDate|string|北交所上市日期|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "name": "",
      "oCode": "",
      "nCode": "",
      "listDate": "yyyy-MM-dd HH:mm:ss"
    }
  ],
  "traceId": ""
}
```

## Agent 误探路径引导控制器。

&lt;p&gt;背景：部分 LLM agent（如把本服务误当 OpenAI/LLM 端点的 hermes agent）会按&quot;OpenAI 风格&quot;
探测 token 连通性，挨个试 {@code /v1/whoami}、{@code /v1/token/info}、{@code /auth/whoami}、
{@code /v1/models} 等——这些在本服务都不存在（本服务是股票数据 REST API，所有接口在
{@code /openapi/v1/**} 下），原本会返回裸 {@code NoHandlerFoundException} 404 堆栈，agent 拿不到任何线索。

&lt;p&gt;本控制器接住这些常见误探路径，返回一段**可读的引导 JSON**（明确正确端点 + base_url + 非 OpenAI 兼容），
让跑偏的 agent 读响应体即可自我纠正到 {@code POST /openapi/v1/whoami}。

&lt;p&gt;这些路径不在 {@code /openapi/**} 下，不经 token 拦截器，返回内容不含任何敏感数据，纯指引。
### 
**URL:** /v1/whoami;	/whoami;	/v1/token/info;	/token/info;	/auth/whoami;	/v1/auth/whoami;	/v1/models;	/models;	/v1/chat/completions

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/v1/whoami'
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|mapKey|object|A map key.|-|
|└─any object|object|any object.|-|

**Response-example:**
```json
{
  "mapKey": {
    "waring": "You may use java.util.Object for Map value; smart-doc can't be handle."
  }
}
```

## OpenAPI v1 —— 对外开放的股票数据子集（K 线 + 估值快照入口）。

所有 /openapi/** 路径由 OpenApiTokenInterceptor 统一鉴权：
 - Authorization: Bearer stk_live_xxxx  或  X-Api-Key: stk_live_xxxx
 - token 绑定的 IP 白名单必须命中当前来源 IP
 - 达到 @OpenApiScope 声明的权限
 - 未超过 per-minute 频率上限

Scope 体系（双层模型，详见 docs/openapi-token.md）：
 - 13 个数据维度 scope：stock.{basic,kline,minute,index,indicator,financial,
   market,shareholder,selection} + derivative + fund + market + bond
 - 5 档商业套餐：免费 / Pro / Max / Plus / Ultra

如需新增对外端点：
 1) 在 stock_mcp/skill/stock-insight/references/data-catalog.md 查清数据归属哪个 scope
 2) 新增一个 @PostMapping 方法（路径按 /openapi/v1/{category}/... 组织）
 3) 加 @OpenApiScope(&quot;stock.kline&quot;) 等 —— scope 名严格对照 docs/openapi-token.md
 4) 通过 OpenApiContext 拿 ownerName / tokenId 写审计（如需）
 5) 同步到 docs/openapi-token.md scope 表 + data-catalog.md + stock_mcp/ MCP 工具

⚠ 不要把 user-level 端点（/stock/user/**）直接映射到 /openapi/** —— 保持 OpenAPI
  只返回只读、非个人、可缓存的数据。个性化端点仍走 /stock/user/** + JWT。
### 日 / 周 / 月 K 线 —— 最常用的只读端点。<br>Scope: stock.kline（含 K 线、复权因子、多周期涨跌幅）。
**URL:** /openapi/v1/stock/kline/daily

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 日 / 周 / 月 K 线 —— 最常用的只读端点。
Scope: stock.kline（含 K 线、复权因子、多周期涨跌幅）。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|page|int32|false|第几页，从 1 起。默认 1。0 / 负数会被当成 1。|-|
|size|int32|false|每页记录数。默认 50，硬上限 {@value #MAX_SIZE}。<br/><p>传入超过 {@value #MAX_SIZE} 时会被自动截断到 {@value #MAX_SIZE}（不报错）。</p>|-|
|startDate|string|false|起始日期（含），格式 {@code YYYYMMDD}（如 {@code "20260101"}）。<br/><p>可空。不传时由 page/size 决定窗口（最近 N 个交易日往前）。</p>|-|
|endDate|string|false|结束日期（含），格式 {@code YYYYMMDD}（如 {@code "20260430"}）。<br/><p>可空。不传时取最新交易日。</p>|-|
|type|int32|false|K 线类型枚举值（来自 {@code com.common.enums.StockKLineType}）：<br/><ul><br/>  <li>{@code 11} —— 日 K（默认）</li><br/>  <li>{@code 12} —— 周 K</li><br/>  <li>{@code 13} —— 月 K</li><br/></ul><br/><br/><p>带默认值 {@code 11}（日 K）：调用方不传时按日 K 处理。<br/>历史缺陷：此前无默认值，不传 type 时反序列化为 0，服务层查表 miss 静默返回空列表<br/>且被 @Cacheable 缓存，调用方误判"无数据"。</p>|-|
|tsCode|string|false|股票代码（带交易所后缀），如 {@code "600519.SH"} / {@code "000001.SZ"}。<b>必填</b>。|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/stock/kline/daily?page=0&size=0&type=0&startDate=&tsCode=&endDate='
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─tsCode|string|股票代码（带交易所后缀），如 {@code "600519.SH"}。|-|
|└─tradeDate|string|交易日期，格式 {@code YYYYMMDD}（如 {@code "20260430"}）。|-|
|└─time|int64|Unix 毫秒时间戳（与 {@link #tradeDate} 表示同一天，给前端画图方便）。|-|
|└─open|number|开盘价（元）。|-|
|└─high|number|最高价（元）。|-|
|└─low|number|最低价（元）。|-|
|└─close|number|收盘价（元）。|-|
|└─preClose|number|前收盘价（昨日收盘价，元）。用于计算涨跌幅。|-|
|└─chg|number|涨跌额 = close - preClose（元）。|-|
|└─pctChg|number|涨跌幅 = (close - preClose) / preClose × 100（百分比，如 {@code 1.23} 表示 +1.23%）。|-|
|└─vol|number|成交量（手）。1 手 = 100 股。|-|
|└─amount|number|成交额（千元）。|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "tsCode": "",
      "tradeDate": "",
      "time": 0,
      "open": 0,
      "high": 0,
      "low": 0,
      "close": 0,
      "preClose": 0,
      "chg": 0,
      "pctChg": 0,
      "vol": 0,
      "amount": 0
    }
  ],
  "traceId": ""
}
```

### 批量获取最新估值指标快照（PE / PB / 换手 / 市值 / ROE 等）。<br>Scope: stock.indicator（技术指标 + 估值；详见 OpenApiV1StockIndicatorController 的历史时间序列端点）。
**URL:** /openapi/v1/stock/indicator/latest

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 批量获取最新估值指标快照（PE / PB / 换手 / 市值 / ROE 等）。
Scope: stock.indicator（技术指标 + 估值；详见 OpenApiV1StockIndicatorController 的历史时间序列端点）。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|tsCodes|array|false|股票代码列表（带交易所后缀）。<br/><br/><p><b>示例</b>：</p><br/><pre><br/>["600519.SH", "000858.SZ", "300750.SZ"]<br/></pre><br/><br/><p>建议单次 ≤ 50 个；超出可能被截断。同一只票多次出现会被去重。</p>|-|
|tradeDate|string|false|交易日期，格式 {@code YYYYMMDD}（如 {@code "20260430"}）。<br/><br/><p>可选；不传时取数据库里最新交易日。多数批量查询接口默认就是最新一日，<br/>只在用户明确说"看 X 月 Y 日"时才需要传。</p>|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/stock/indicator/latest?tsCodes=,&tradeDate='
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─tsCode|string|股票代码（带交易所后缀），如 {@code "600519.SH"}。|-|
|└─symbol|string|纯数字股票代码，如 {@code "600519"}。|-|
|└─name|string|股票中文简称，如 {@code "贵州茅台"}。|-|
|└─tradeDate|string|数据所属交易日。|-|
|└─close|number|当日收盘价（元）。|-|
|└─turnoverRate|number|换手率（%）= 当日成交量 / 流通股本 × 100。|-|
|└─turnoverRateF|number|自由流通换手率（%）= 当日成交量 / 自由流通股本 × 100。一般比 {@link #turnoverRate} 更高。|-|
|└─volumeRatio|number|量比 = 当日成交量 / 近 5 日平均成交量。{@code > 1} 表示放量，{@code > 2} 显著放量。|-|
|└─pe|number|静态市盈率：股价 / 上一年度 EPS。|-|
|└─peTtm|number|滚动市盈率：股价 / 最近 4 个季度 EPS（最常用）。|-|
|└─pb|number|市净率：股价 / 每股净资产。|-|
|└─ps|number|静态市销率：股价 / 上一年度 EPS_revenue。|-|
|└─psTtm|number|滚动市销率：股价 / 最近 4 个季度营收（更平滑）。|-|
|└─dvRatio|number|静态股息率（%）= 上一年度每股分红 / 股价 × 100。|-|
|└─dvTtm|number|滚动股息率（%）= 最近 4 个季度每股分红 / 股价 × 100。|-|
|└─totalShare|number|总股本（万股）。|-|
|└─floatShare|number|流通股本（万股）。|-|
|└─freeShare|number|自由流通股本（万股）。剔除限售 / 高管 / 国资等长期不流通部分。|-|
|└─totalMv|number|总市值（万元）= 总股本 × 当日收盘价。|-|
|└─circMv|number|流通市值（万元）= 流通股本 × 当日收盘价。|-|
|└─limitStatus|int8|涨跌停状态。<br/><ul><br/>  <li>{@code 0} —— 普通</li><br/>  <li>{@code 1} —— 涨停</li><br/>  <li>{@code 2} —— 跌停</li><br/>  <li>{@code 3} —— 一字涨停（开盘即涨停）</li><br/>  <li>{@code 4} —— 一字跌停</li><br/></ul><br/><p>具体编码以后端 {@code com.common.enums.LimitStatus} 为准。</p>|-|
|└─roe|number|净资产收益率（%，最近一期）。{@code > 15%} 普遍认为是优秀。|-|
|└─chg|number|涨跌额（元）= close - preClose。|-|
|└─pctChg|number|涨跌幅（%）。|-|
|└─roeDate|string|ROE 数据所属报告期日（季末日期，如 {@code 2026-03-31}）。|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{"code":0,"msg":"","data":[{"tsCode":"","symbol":"","name":"","tradeDate":"yyyy-MM-dd HH:mm:ss","close":0,"turnoverRate":0,"turnoverRateF":0,"volumeRatio":0,"pe":0,"peTtm":0,"pb":0,"ps":0,"psTtm":0,"dvRatio":0,"dvTtm":0,"totalShare":0,"floatShare":0,"freeShare":0,"totalMv":0,"circMv":0,"limitStatus":,"roe":0,"chg":0,"pctChg":0,"roeDate":"yyyy-MM-dd HH:mm:ss"}],"traceId":""}
```

## OpenAPI v1 —— 基金 / ETF 端点（fund scope）。

&lt;p&gt;覆盖 11 张 PG 表的 9 个端点（参见 IFundServices）。
全部 &lt;code&gt;@OpenApiScope(&quot;fund&quot;)&lt;/code&gt;，套餐归属 Max 及以上。

&lt;p&gt;路径规范：
&lt;ul&gt;
  &lt;li&gt;ETF 子域：&lt;code&gt;/openapi/v1/fund/etf/...&lt;/code&gt;&lt;/li&gt;
  &lt;li&gt;公募基金：&lt;code&gt;/openapi/v1/fund/...&lt;/code&gt;（不带 etf/ 前缀）&lt;/li&gt;
&lt;/ul&gt;

&lt;p&gt;对应 MCP 工具：见 stock_mcp/src/stock_mcp/tools/fund.py。
### ETF 列表筛选（按代码 / 名称 / 跟踪指数 / ETF 类型 / 上市状态 / 交易所）。<br>所有筛选项可选；返回 etf_basic_info 联表 etf_index 的全量元信息。
**URL:** /openapi/v1/fund/etf/list

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** ETF 列表筛选（按代码 / 名称 / 跟踪指数 / ETF 类型 / 上市状态 / 交易所）。
所有筛选项可选；返回 etf_basic_info 联表 etf_index 的全量元信息。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|page|int32|false|第几页，从 1 起。默认 1。0 / 负数会被当成 1。|-|
|size|int32|false|每页记录数。默认 50，硬上限 {@value #MAX_SIZE}。<br/><p>传入超过 {@value #MAX_SIZE} 时会被自动截断到 {@value #MAX_SIZE}（不报错）。</p>|-|
|tsCode|string|false|基金 / ETF 代码（精确匹配）。<br/><p>例如 {@code "510300.SH"}（ETF）/ {@code "110011.OF"}（公募场外）。</p>|-|
|nameKeyword|string|false|名称关键字（中文模糊匹配）。<br/><p>例如 {@code "蓝筹"} / {@code "纳指"} / {@code "黄金"}。</p>|-|
|fundType|string|false|基金类型：{@code "股票型"} / {@code "混合型"} / {@code "债券型"} / {@code "货币型"} / {@code "FOF"} / {@code "REITs"} 等。|-|
|status|string|false|上市状态。<br/><ul><br/>  <li>{@code "D"} —— 存续</li><br/>  <li>{@code "I"} —— 发行中</li><br/>  <li>{@code "L"} —— 已上市</li><br/>  <li>{@code "S"} —— 已终止</li><br/></ul>|-|
|market|string|false|市场归属：{@code "E"}（场内）/ {@code "O"}（场外）。空为全部。|-|
|exchange|string|false|交易所：{@code "SSE"} / {@code "SZSE"} / {@code "BSE"}。仅 ETF 适用。|-|
|indexCode|string|false|跟踪指数代码（仅 ETF 适用），如 {@code "000300.SH"} 找跟踪沪深 300 的全部 ETF。|-|
|managerName|string|false|基金经理姓名（仅 manager/list 端点用），如 {@code "张坤"} 查张坤管理的全部基金。|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/fund/etf/list?page=0&size=0&tsCode=&nameKeyword=&market=&managerName=&fundType=&indexCode=&exchange=&status='
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─tsCode|string|No comments found.|-|
|└─csName|string|ETF 中文名（cs_name）|-|
|└─extName|string|扩展名|-|
|└─cName|string|简称|-|
|└─indexCode|string|跟踪指数代码|-|
|└─indexName|string|跟踪指数名称|-|
|└─setupDate|string|成立日期 YYYYMMDD|-|
|└─listDate|string|上市日期 YYYYMMDD|-|
|└─listStatus|string|上市状态|-|
|└─exchange|string|交易所 SSE/SZSE/BSE|-|
|└─mgrName|string|基金管理人|-|
|└─custodName|string|托管机构|-|
|└─mgtFee|number|管理费率（%）|-|
|└─etfType|string|ETF 类型（如：股票指数 / 债券 / 商品 / 货币 / 跨境 / REITs）|-|
|└─baseDate|string|基期 YYYYMMDD|-|
|└─basePoint|number|基点|-|
|└─publisher|string|指数发布机构|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "tsCode": "",
      "csName": "",
      "extName": "",
      "cName": "",
      "indexCode": "",
      "indexName": "",
      "setupDate": "",
      "listDate": "",
      "listStatus": "",
      "exchange": "",
      "mgrName": "",
      "custodName": "",
      "mgtFee": 0,
      "etfType": "",
      "baseDate": "",
      "basePoint": 0,
      "publisher": ""
    }
  ],
  "traceId": ""
}
```

### ETF 日 K 线（含复权因子）。
**URL:** /openapi/v1/fund/etf/kline/daily

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** ETF 日 K 线（含复权因子）。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|page|int32|false|第几页，从 1 起。默认 1。0 / 负数会被当成 1。|-|
|size|int32|false|每页记录数。默认 50，硬上限 {@value #MAX_SIZE}。<br/><p>传入超过 {@value #MAX_SIZE} 时会被自动截断到 {@value #MAX_SIZE}（不报错）。</p>|-|
|tsCode|string|false|基金 / ETF 代码（带交易所或场外后缀）。<b>必填</b>。<br/><br/><p><b>示例</b>：</p><br/><ul><br/>  <li>ETF 场内：{@code "510300.SH"}（沪深 300ETF）/ {@code "159919.SZ"}</li><br/>  <li>公募场外：{@code "110011.OF"}（易方达蓝筹）</li><br/></ul>|-|
|startDate|string|false|起始日期，格式 {@code YYYYMMDD}。可空，不传时取最近 60 自然日窗口。|-|
|endDate|string|false|结束日期，格式 {@code YYYYMMDD}。可空，不传时取最新交易日。|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/fund/etf/kline/daily?page=0&size=0&endDate=&tsCode=&startDate='
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─tsCode|string|No comments found.|-|
|└─tradeDate|string|No comments found.|-|
|└─open|number|No comments found.|-|
|└─high|number|No comments found.|-|
|└─low|number|No comments found.|-|
|└─close|number|No comments found.|-|
|└─preClose|number|No comments found.|-|
|└─chg|number|No comments found.|-|
|└─pctChg|number|No comments found.|-|
|└─vol|number|成交量（手）|-|
|└─amount|number|成交额（元）|-|
|└─adjFactor|number|复权因子（来自 etf_adj_factor，可空）|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "tsCode": "",
      "tradeDate": "yyyy-MM-dd HH:mm:ss",
      "open": 0,
      "high": 0,
      "low": 0,
      "close": 0,
      "preClose": 0,
      "chg": 0,
      "pctChg": 0,
      "vol": 0,
      "amount": 0,
      "adjFactor": 0
    }
  ],
  "traceId": ""
}
```

### ETF 份额 / 规模历史（含当日 NAV 与收盘价，便于评估折溢价）。
**URL:** /openapi/v1/fund/etf/share-history

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** ETF 份额 / 规模历史（含当日 NAV 与收盘价，便于评估折溢价）。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|page|int32|false|第几页，从 1 起。默认 1。0 / 负数会被当成 1。|-|
|size|int32|false|每页记录数。默认 50，硬上限 {@value #MAX_SIZE}。<br/><p>传入超过 {@value #MAX_SIZE} 时会被自动截断到 {@value #MAX_SIZE}（不报错）。</p>|-|
|tsCode|string|false|基金 / ETF 代码（带交易所或场外后缀）。<b>必填</b>。<br/><br/><p><b>示例</b>：</p><br/><ul><br/>  <li>ETF 场内：{@code "510300.SH"}（沪深 300ETF）/ {@code "159919.SZ"}</li><br/>  <li>公募场外：{@code "110011.OF"}（易方达蓝筹）</li><br/></ul>|-|
|startDate|string|false|起始日期，格式 {@code YYYYMMDD}。可空，不传时取最近 60 自然日窗口。|-|
|endDate|string|false|结束日期，格式 {@code YYYYMMDD}。可空，不传时取最新交易日。|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/fund/etf/share-history?page=0&size=0&startDate=&tsCode=&endDate='
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─tsCode|string|No comments found.|-|
|└─tradeDate|string|No comments found.|-|
|└─etfName|string|ETF 名称|-|
|└─totalShare|number|总份额（份）|-|
|└─totalSize|number|总规模（元）|-|
|└─nav|number|净值|-|
|└─close|number|收盘价|-|
|└─exchange|string|交易所|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "tsCode": "",
      "tradeDate": "yyyy-MM-dd HH:mm:ss",
      "etfName": "",
      "totalShare": 0,
      "totalSize": 0,
      "nav": 0,
      "close": 0,
      "exchange": ""
    }
  ],
  "traceId": ""
}
```

### 公募基金列表筛选（按代码 / 名称 / 类型 / 状态 / 市场 / 管理人）。<br>注意：FundListForm.managerName 字段在此端点对应 fund_basic.management（基金公司）。
**URL:** /openapi/v1/fund/list

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 公募基金列表筛选（按代码 / 名称 / 类型 / 状态 / 市场 / 管理人）。
注意：FundListForm.managerName 字段在此端点对应 fund_basic.management（基金公司）。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|page|int32|false|第几页，从 1 起。默认 1。0 / 负数会被当成 1。|-|
|size|int32|false|每页记录数。默认 50，硬上限 {@value #MAX_SIZE}。<br/><p>传入超过 {@value #MAX_SIZE} 时会被自动截断到 {@value #MAX_SIZE}（不报错）。</p>|-|
|tsCode|string|false|基金 / ETF 代码（精确匹配）。<br/><p>例如 {@code "510300.SH"}（ETF）/ {@code "110011.OF"}（公募场外）。</p>|-|
|nameKeyword|string|false|名称关键字（中文模糊匹配）。<br/><p>例如 {@code "蓝筹"} / {@code "纳指"} / {@code "黄金"}。</p>|-|
|fundType|string|false|基金类型：{@code "股票型"} / {@code "混合型"} / {@code "债券型"} / {@code "货币型"} / {@code "FOF"} / {@code "REITs"} 等。|-|
|status|string|false|上市状态。<br/><ul><br/>  <li>{@code "D"} —— 存续</li><br/>  <li>{@code "I"} —— 发行中</li><br/>  <li>{@code "L"} —— 已上市</li><br/>  <li>{@code "S"} —— 已终止</li><br/></ul>|-|
|market|string|false|市场归属：{@code "E"}（场内）/ {@code "O"}（场外）。空为全部。|-|
|exchange|string|false|交易所：{@code "SSE"} / {@code "SZSE"} / {@code "BSE"}。仅 ETF 适用。|-|
|indexCode|string|false|跟踪指数代码（仅 ETF 适用），如 {@code "000300.SH"} 找跟踪沪深 300 的全部 ETF。|-|
|managerName|string|false|基金经理姓名（仅 manager/list 端点用），如 {@code "张坤"} 查张坤管理的全部基金。|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/fund/list?page=0&size=0&fundType=&market=&indexCode=&nameKeyword=&status=&exchange=&tsCode=&managerName='
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─tsCode|string|No comments found.|-|
|└─name|string|基金简称|-|
|└─management|string|管理人（基金公司）|-|
|└─custodian|string|托管人（银行）|-|
|└─fundType|string|投资类型（如 "股票型"、"混合型"、"债券型"、"货币型"、"FOF"、"REITs"）|-|
|└─foundDate|string|成立日期 YYYYMMDD|-|
|└─dueDate|string|到期日期 YYYYMMDD（封闭式适用）|-|
|└─listDate|string|上市时间 YYYYMMDD（场内基金）|-|
|└─issueDate|string|发行日期 YYYYMMDD|-|
|└─delistDate|string|退市日期 YYYYMMDD|-|
|└─issueAmount|number|发行份额（亿份）|-|
|└─mFee|number|管理费率（%）|-|
|└─cFee|number|托管费率（%）|-|
|└─durationYear|number|存续期（年）|-|
|└─pValue|number|面值|-|
|└─minAmount|number|起购金额（万元）|-|
|└─expReturn|number|预期收益率|-|
|└─benchmark|string|业绩比较基准|-|
|└─status|string|状态：D 存续 / I 发行 / L 上市 / S 终止|-|
|└─investType|string|投资风格|-|
|└─type|string|类型：开放式 / 封闭式|-|
|└─trustee|string|受托人|-|
|└─purcStartdate|string|申购起始日 YYYYMMDD|-|
|└─redmStartdate|string|赎回起始日 YYYYMMDD|-|
|└─market|string|市场：E 场内 / O 场外|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "tsCode": "",
      "name": "",
      "management": "",
      "custodian": "",
      "fundType": "",
      "foundDate": "",
      "dueDate": "",
      "listDate": "",
      "issueDate": "",
      "delistDate": "",
      "issueAmount": 0,
      "mFee": 0,
      "cFee": 0,
      "durationYear": 0,
      "pValue": 0,
      "minAmount": 0,
      "expReturn": 0,
      "benchmark": "",
      "status": "",
      "investType": "",
      "type": "",
      "trustee": "",
      "purcStartdate": "",
      "redmStartdate": "",
      "market": ""
    }
  ],
  "traceId": ""
}
```

### 基金净值历史（单位 / 累计 / 复权）。<br>适合算收益率、画净值曲线。
**URL:** /openapi/v1/fund/nav/history

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 基金净值历史（单位 / 累计 / 复权）。
适合算收益率、画净值曲线。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|page|int32|false|第几页，从 1 起。默认 1。0 / 负数会被当成 1。|-|
|size|int32|false|每页记录数。默认 50，硬上限 {@value #MAX_SIZE}。<br/><p>传入超过 {@value #MAX_SIZE} 时会被自动截断到 {@value #MAX_SIZE}（不报错）。</p>|-|
|tsCode|string|false|基金 / ETF 代码（带交易所或场外后缀）。<b>必填</b>。<br/><br/><p><b>示例</b>：</p><br/><ul><br/>  <li>ETF 场内：{@code "510300.SH"}（沪深 300ETF）/ {@code "159919.SZ"}</li><br/>  <li>公募场外：{@code "110011.OF"}（易方达蓝筹）</li><br/></ul>|-|
|startDate|string|false|起始日期，格式 {@code YYYYMMDD}。可空，不传时取最近 60 自然日窗口。|-|
|endDate|string|false|结束日期，格式 {@code YYYYMMDD}。可空，不传时取最新交易日。|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/fund/nav/history?page=0&size=0&startDate=&tsCode=&endDate='
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─tsCode|string|No comments found.|-|
|└─annDate|string|公告日期 YYYYMMDD|-|
|└─navDate|string|净值日期 YYYYMMDD|-|
|└─unitNav|number|单位净值|-|
|└─accumNav|number|累计净值|-|
|└─accumDiv|number|累计分红|-|
|└─netAsset|number|资产净值（元）|-|
|└─totalNetasset|number|合计资产净值（元，多份额合并）|-|
|└─adjNav|number|复权单位净值（适合算收益率）|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "tsCode": "",
      "annDate": "",
      "navDate": "",
      "unitNav": 0,
      "accumNav": 0,
      "accumDiv": 0,
      "netAsset": 0,
      "totalNetasset": 0,
      "adjNav": 0
    }
  ],
  "traceId": ""
}
```

### 基金分红记录（按公告日倒序）。<br>默认不限制日期窗口（分红条数本身少）。
**URL:** /openapi/v1/fund/dividend

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 基金分红记录（按公告日倒序）。
默认不限制日期窗口（分红条数本身少）。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|page|int32|false|第几页，从 1 起。默认 1。0 / 负数会被当成 1。|-|
|size|int32|false|每页记录数。默认 50，硬上限 {@value #MAX_SIZE}。<br/><p>传入超过 {@value #MAX_SIZE} 时会被自动截断到 {@value #MAX_SIZE}（不报错）。</p>|-|
|tsCode|string|false|基金 / ETF 代码（带交易所或场外后缀）。<b>必填</b>。<br/><br/><p><b>示例</b>：</p><br/><ul><br/>  <li>ETF 场内：{@code "510300.SH"}（沪深 300ETF）/ {@code "159919.SZ"}</li><br/>  <li>公募场外：{@code "110011.OF"}（易方达蓝筹）</li><br/></ul>|-|
|startDate|string|false|起始日期，格式 {@code YYYYMMDD}。可空，不传时取最近 60 自然日窗口。|-|
|endDate|string|false|结束日期，格式 {@code YYYYMMDD}。可空，不传时取最新交易日。|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/fund/dividend?page=0&size=0&tsCode=&startDate=&endDate='
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─tsCode|string|No comments found.|-|
|└─annDate|string|公告日期 YYYYMMDD|-|
|└─impAnndate|string|分红实施公告日 YYYYMMDD|-|
|└─baseDate|string|分红基准日 YYYYMMDD|-|
|└─divProc|string|分红进度（如 "实施"、"预案"）|-|
|└─recordDate|string|权益登记日 YYYYMMDD|-|
|└─exDate|string|除息日 YYYYMMDD|-|
|└─payDate|string|派息日 YYYYMMDD|-|
|└─earpayDate|string|收益支付日 YYYYMMDD|-|
|└─netExDate|string|净值除权日 YYYYMMDD|-|
|└─divCash|number|每份分红金额（元）|-|
|└─baseUnit|number|基准基金份额|-|
|└─earDistr|number|已分配收益（元）|-|
|└─earAmount|number|分红总额（元）|-|
|└─accountDate|string|入账日 YYYYMMDD|-|
|└─baseYear|string|分红年度（如 "2023" / "2024 上半年"）|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "tsCode": "",
      "annDate": "",
      "impAnndate": "",
      "baseDate": "",
      "divProc": "",
      "recordDate": "",
      "exDate": "",
      "payDate": "",
      "earpayDate": "",
      "netExDate": "",
      "divCash": 0,
      "baseUnit": 0,
      "earDistr": 0,
      "earAmount": 0,
      "accountDate": "",
      "baseYear": ""
    }
  ],
  "traceId": ""
}
```

### 基金持仓（前十大重仓股，按报告期）。<br>endDate 为空时自动取最新报告期。
**URL:** /openapi/v1/fund/portfolio

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 基金持仓（前十大重仓股，按报告期）。
endDate 为空时自动取最新报告期。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|page|int32|false|第几页，从 1 起。默认 1。0 / 负数会被当成 1。|-|
|size|int32|false|每页记录数。默认 50，硬上限 {@value #MAX_SIZE}。<br/><p>传入超过 {@value #MAX_SIZE} 时会被自动截断到 {@value #MAX_SIZE}（不报错）。</p>|-|
|tsCode|string|false|基金代码（带后缀）。<b>必填</b>。<br/><p>例如 {@code "110011.OF"}（易方达蓝筹）/ {@code "510300.SH"}（沪深 300ETF）。</p>|-|
|endDate|string|false|报告期截止日，格式 {@code YYYYMMDD}（季末日）。<br/><br/><ul><br/>  <li>{@code "20260331"} —— 一季报</li><br/>  <li>{@code "20260630"} —— 半年报</li><br/>  <li>{@code "20260930"} —— 三季报</li><br/>  <li>{@code "20261231"} —— 年报</li><br/></ul><br/><br/><p>可空。不传时取最新已披露的报告期。</p>|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/fund/portfolio?page=0&size=0&endDate=&tsCode='
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─tsCode|string|基金代码|-|
|└─annDate|string|公告日期 YYYYMMDD|-|
|└─endDate|string|报告期 YYYYMMDD（季末）|-|
|└─symbol|string|持仓股票代码（如 600519.SH）|-|
|└─mkv|number|持仓市值（元）|-|
|└─amount|number|持仓数量（股）|-|
|└─stkMkvRatio|number|占基金净值比例（%）|-|
|└─stkFloatRatio|number|占股票流通股比例（%）|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "tsCode": "",
      "annDate": "",
      "endDate": "",
      "symbol": "",
      "mkv": 0,
      "amount": 0,
      "stkMkvRatio": 0,
      "stkFloatRatio": 0
    }
  ],
  "traceId": ""
}
```

### 基金经理列表。tsCode 与 managerName 至少一个必填。<br>&lt;ul&gt;<br>  &lt;li&gt;仅传 tsCode → 该基金的所有经理（含历任）&lt;/li&gt;<br>  &lt;li&gt;仅传 managerName → 该经理管的所有基金&lt;/li&gt;<br>  &lt;li&gt;两者都传 → 精确组合&lt;/li&gt;<br>&lt;/ul&gt;
**URL:** /openapi/v1/fund/manager/list

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 基金经理列表。tsCode 与 managerName 至少一个必填。
<ul>
  <li>仅传 tsCode → 该基金的所有经理（含历任）</li>
  <li>仅传 managerName → 该经理管的所有基金</li>
  <li>两者都传 → 精确组合</li>
</ul>

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|page|int32|false|第几页，从 1 起。默认 1。0 / 负数会被当成 1。|-|
|size|int32|false|每页记录数。默认 50，硬上限 {@value #MAX_SIZE}。<br/><p>传入超过 {@value #MAX_SIZE} 时会被自动截断到 {@value #MAX_SIZE}（不报错）。</p>|-|
|tsCode|string|false|基金 / ETF 代码（精确匹配）。<br/><p>例如 {@code "510300.SH"}（ETF）/ {@code "110011.OF"}（公募场外）。</p>|-|
|nameKeyword|string|false|名称关键字（中文模糊匹配）。<br/><p>例如 {@code "蓝筹"} / {@code "纳指"} / {@code "黄金"}。</p>|-|
|fundType|string|false|基金类型：{@code "股票型"} / {@code "混合型"} / {@code "债券型"} / {@code "货币型"} / {@code "FOF"} / {@code "REITs"} 等。|-|
|status|string|false|上市状态。<br/><ul><br/>  <li>{@code "D"} —— 存续</li><br/>  <li>{@code "I"} —— 发行中</li><br/>  <li>{@code "L"} —— 已上市</li><br/>  <li>{@code "S"} —— 已终止</li><br/></ul>|-|
|market|string|false|市场归属：{@code "E"}（场内）/ {@code "O"}（场外）。空为全部。|-|
|exchange|string|false|交易所：{@code "SSE"} / {@code "SZSE"} / {@code "BSE"}。仅 ETF 适用。|-|
|indexCode|string|false|跟踪指数代码（仅 ETF 适用），如 {@code "000300.SH"} 找跟踪沪深 300 的全部 ETF。|-|
|managerName|string|false|基金经理姓名（仅 manager/list 端点用），如 {@code "张坤"} 查张坤管理的全部基金。|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/fund/manager/list?page=0&size=0&nameKeyword=&exchange=&indexCode=&managerName=&fundType=&status=&market=&tsCode='
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─tsCode|string|基金代码|-|
|└─annDate|string|公告日期 YYYYMMDD|-|
|└─name|string|经理姓名|-|
|└─gender|string|性别 M / F|-|
|└─birthYear|string|出生年份|-|
|└─edu|string|学历|-|
|└─nationality|string|国籍|-|
|└─beginDate|string|任职起始日 YYYYMMDD|-|
|└─endDate|string|任职截止日 YYYYMMDD（在任为空）|-|
|└─resume|string|简历摘要|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "tsCode": "",
      "annDate": "",
      "name": "",
      "gender": "",
      "birthYear": "",
      "edu": "",
      "nationality": "",
      "beginDate": "",
      "endDate": "",
      "resume": ""
    }
  ],
  "traceId": ""
}
```

### 基金规模份额历史（fund_share）。<br>与 ETF 的 share-history 区别：fund_share 只有总份额，没有 NAV / 收盘价。
**URL:** /openapi/v1/fund/share/history

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 基金规模份额历史（fund_share）。
与 ETF 的 share-history 区别：fund_share 只有总份额，没有 NAV / 收盘价。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|page|int32|false|第几页，从 1 起。默认 1。0 / 负数会被当成 1。|-|
|size|int32|false|每页记录数。默认 50，硬上限 {@value #MAX_SIZE}。<br/><p>传入超过 {@value #MAX_SIZE} 时会被自动截断到 {@value #MAX_SIZE}（不报错）。</p>|-|
|tsCode|string|false|基金 / ETF 代码（带交易所或场外后缀）。<b>必填</b>。<br/><br/><p><b>示例</b>：</p><br/><ul><br/>  <li>ETF 场内：{@code "510300.SH"}（沪深 300ETF）/ {@code "159919.SZ"}</li><br/>  <li>公募场外：{@code "110011.OF"}（易方达蓝筹）</li><br/></ul>|-|
|startDate|string|false|起始日期，格式 {@code YYYYMMDD}。可空，不传时取最近 60 自然日窗口。|-|
|endDate|string|false|结束日期，格式 {@code YYYYMMDD}。可空，不传时取最新交易日。|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/fund/share/history?page=0&size=0&endDate=&tsCode=&startDate='
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─tsCode|string|No comments found.|-|
|└─tradeDate|string|交易日 YYYYMMDD|-|
|└─fdShare|number|基金份额（亿份）|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "tsCode": "",
      "tradeDate": "",
      "fdShare": 0
    }
  ],
  "traceId": ""
}
```

### 各渠道公募基金销售保有规模占比（{@code fund_sales_ratio}，年度）。<br><br>可按 year 精确 / startYear-endYear 区间过滤。反映银行 / 券商 / 直销 / 第三方<br>等渠道在公募保有中的占比变化趋势。 
**URL:** /openapi/v1/fund/sales/ratio

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 各渠道公募基金销售保有规模占比（{@code fund_sales_ratio}，年度）。

<p>可按 year 精确 / startYear-endYear 区间过滤。反映银行 / 券商 / 直销 / 第三方
等渠道在公募保有中的占比变化趋势。</p>

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|page|int32|false|第几页，从 1 起。默认 1。0 / 负数会被当成 1。|-|
|size|int32|false|每页记录数。默认 50，硬上限 {@value #MAX_SIZE}。<br/><p>传入超过 {@value #MAX_SIZE} 时会被自动截断到 {@value #MAX_SIZE}（不报错）。</p>|-|
|keyword|string|false|通用关键字（按表内最关键文本列模糊匹配，参类级注释）。|-|
|year|int32|false|年度（fund-sales-ratio / fund-sales-vol 用）。|-|
|startYear|int32|false|起始年度（fund-sales-ratio 区间）。|-|
|endYear|int32|false|结束年度（fund-sales-ratio 区间）。|-|
|quarter|string|false|季度（fund-sales-vol，如 "1"/"2"/"3"/"4" 或 "Q1"/...）。|-|
|startDate|string|false|起始日期 {@code YYYYMMDD}。|-|
|endDate|string|false|结束日期 {@code YYYYMMDD}。|-|
|country|string|false|国家代码（eco-cal）。|-|
|currency|string|false|货币代码（eco-cal，USD/EUR/CNY/...）。|-|
|ptype|string|false|政策类型（policy-npr）。|-|
|puborg|string|false|发布机构（policy-npr）。|-|
|exchange|string|false|交易所（futures-weekly-detail，DCE/CFFEX/CZCE/SHFE/INE）。|-|
|prd|string|false|期货品种代码（futures-weekly-detail，如 CU/RB/IF）。|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/fund/sales/ratio?page=0&size=0&year=0&startYear=0&endYear=0&startDate=&country=&endDate=&ptype=&puborg=&quarter=&prd=&currency=&keyword=&exchange='
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─year|int32|年度|-|
|└─bank|number|银行系占比（%）|-|
|└─secComp|number|券商系占比（%）|-|
|└─fundComp|number|基金公司直销占比（%）|-|
|└─indepComp|number|独立销售机构占比（%）|-|
|└─rests|number|其他渠道占比（%）|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "year": 0,
      "bank": 0,
      "secComp": 0,
      "fundComp": 0,
      "indepComp": 0,
      "rests": 0
    }
  ],
  "traceId": ""
}
```

### 销售机构公募基金保有规模 + 排名（{@code fund_sales_vol}，季度）。<br><br>可按 year / quarter / keyword（按销售机构名模糊）过滤。<br>用于看头部代销机构每季度的规模变化与排名波动。 
**URL:** /openapi/v1/fund/sales/vol

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 销售机构公募基金保有规模 + 排名（{@code fund_sales_vol}，季度）。

<p>可按 year / quarter / keyword（按销售机构名模糊）过滤。
用于看头部代销机构每季度的规模变化与排名波动。</p>

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|page|int32|false|第几页，从 1 起。默认 1。0 / 负数会被当成 1。|-|
|size|int32|false|每页记录数。默认 50，硬上限 {@value #MAX_SIZE}。<br/><p>传入超过 {@value #MAX_SIZE} 时会被自动截断到 {@value #MAX_SIZE}（不报错）。</p>|-|
|keyword|string|false|通用关键字（按表内最关键文本列模糊匹配，参类级注释）。|-|
|year|int32|false|年度（fund-sales-ratio / fund-sales-vol 用）。|-|
|startYear|int32|false|起始年度（fund-sales-ratio 区间）。|-|
|endYear|int32|false|结束年度（fund-sales-ratio 区间）。|-|
|quarter|string|false|季度（fund-sales-vol，如 "1"/"2"/"3"/"4" 或 "Q1"/...）。|-|
|startDate|string|false|起始日期 {@code YYYYMMDD}。|-|
|endDate|string|false|结束日期 {@code YYYYMMDD}。|-|
|country|string|false|国家代码（eco-cal）。|-|
|currency|string|false|货币代码（eco-cal，USD/EUR/CNY/...）。|-|
|ptype|string|false|政策类型（policy-npr）。|-|
|puborg|string|false|发布机构（policy-npr）。|-|
|exchange|string|false|交易所（futures-weekly-detail，DCE/CFFEX/CZCE/SHFE/INE）。|-|
|prd|string|false|期货品种代码（futures-weekly-detail，如 CU/RB/IF）。|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/fund/sales/vol?page=0&size=0&year=0&startYear=0&endYear=0&keyword=&quarter=&endDate=&country=&puborg=&currency=&startDate=&ptype=&exchange=&prd='
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─year|int32|年度|-|
|└─quarter|string|季度|-|
|└─instName|string|销售机构名称|-|
|└─fundScale|number|公募基金保有规模（亿元）|-|
|└─scale|number|总保有规模（亿元）|-|
|└─rank|int32|排名|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "year": 0,
      "quarter": "",
      "instName": "",
      "fundScale": 0,
      "scale": 0,
      "rank": 0
    }
  ],
  "traceId": ""
}
```

## OpenAPI v1 —— 国际宏观全量端点（{@code intl-macro} scope，2026-06 起仅 ultra 内部、停止对外销售）。
&lt;p&gt;2026-06 重构：原 {@code stock.intl-macro} 重命名为 {@code intl-macro}（去掉 stock 前缀，修正 stock.* 通配符语义）；
存量持有旧名的 token 由 {@code TokenSnapshot} 当别名映射，不中断。

&lt;p&gt;覆盖 9 张 PG 表的 9 个端点（5 张美债收益率 + HK HIBOR + 国际 LIBOR + 中国民间利率 2 张）：
&lt;ul&gt;
  &lt;li&gt;{@code POST /openapi/v1/intl-macro/us-tycr}    — 美国国债收益率曲线（1M-30Y）&lt;/li&gt;
  &lt;li&gt;{@code POST /openapi/v1/intl-macro/us-trycr}   — 美国国债实际收益率曲线（5Y-30Y）&lt;/li&gt;
  &lt;li&gt;{@code POST /openapi/v1/intl-macro/us-tbr}     — 美国短期国债利率（4w-52w）&lt;/li&gt;
  &lt;li&gt;{@code POST /openapi/v1/intl-macro/us-tltr}    — 美国国债长期利率（LTC/CMT）&lt;/li&gt;
  &lt;li&gt;{@code POST /openapi/v1/intl-macro/us-trltr}   — 美国国债长期实际利率平均值&lt;/li&gt;
  &lt;li&gt;{@code POST /openapi/v1/intl-macro/hibor}      — 香港 HIBOR 同业拆借利率&lt;/li&gt;
  &lt;li&gt;{@code POST /openapi/v1/intl-macro/libor}      — 伦敦 LIBOR 同业拆借利率（多币种）&lt;/li&gt;
  &lt;li&gt;{@code POST /openapi/v1/intl-macro/gz-index}   — 广州民间借贷利率&lt;/li&gt;
  &lt;li&gt;{@code POST /openapi/v1/intl-macro/wz-index}   — 温州民间借贷利率&lt;/li&gt;
&lt;/ul&gt;

&lt;p&gt;注：全球财经事件日历（{@code macro_eco_cal}）和国家政策库（{@code macro_policy_npr}）已通过
{@code OpenApiV1StockBasicController}/{@code /openapi/v1/stock/basic/...} 暴露在 {@code stock.basic} scope 下，
此处不重复暴露。
### 美国国债收益率曲线（{@code macro_us_tycr}）。<br><br>1M / 2M / 3M / 4M / 6M / 1Y / 2Y / 3Y / 5Y / 7Y / 10Y / 20Y / 30Y 共 13 个期限。<br>用于判断曲线形态、计算期限利差（{@code y10 - m3}、{@code y10 - y2}）。
**URL:** /openapi/v1/intl-macro/us-tycr

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 美国国债收益率曲线（{@code macro_us_tycr}）。

<p>1M / 2M / 3M / 4M / 6M / 1Y / 2Y / 3Y / 5Y / 7Y / 10Y / 20Y / 30Y 共 13 个期限。
用于判断曲线形态、计算期限利差（{@code y10 - m3}、{@code y10 - y2}）。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|page|int32|false|第几页，从 1 起。默认 1。0 / 负数会被当成 1。|-|
|size|int32|false|每页记录数。默认 50，硬上限 {@value #MAX_SIZE}。<br/><p>传入超过 {@value #MAX_SIZE} 时会被自动截断到 {@value #MAX_SIZE}（不报错）。</p>|-|
|startDate|string|false|起始日期，格式 {@code YYYYMMDD}。可空。|-|
|endDate|string|false|结束日期，格式 {@code YYYYMMDD}。可空。|-|
|currType|string|false|币种（仅 libor 端点用）：{@code USD} / {@code EUR} / {@code JPY} / {@code GBP} / {@code CHF}。可空（默认 USD）。|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/intl-macro/us-tycr?page=0&size=0&endDate=&currType=&startDate='
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─date|string|日期|-|
|└─m1|number|1 月期收益率|-|
|└─m2|number|2 月期收益率|-|
|└─m3|number|3 月期收益率|-|
|└─m4|number|4 月期收益率|-|
|└─m6|number|6 月期收益率|-|
|└─y1|number|1 年期收益率|-|
|└─y2|number|2 年期收益率|-|
|└─y3|number|3 年期收益率|-|
|└─y5|number|5 年期收益率|-|
|└─y7|number|7 年期收益率|-|
|└─y10|number|10 年期收益率|-|
|└─y20|number|20 年期收益率|-|
|└─y30|number|30 年期收益率|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "date": "yyyy-MM-dd HH:mm:ss",
      "m1": 0,
      "m2": 0,
      "m3": 0,
      "m4": 0,
      "m6": 0,
      "y1": 0,
      "y2": 0,
      "y3": 0,
      "y5": 0,
      "y7": 0,
      "y10": 0,
      "y20": 0,
      "y30": 0
    }
  ],
  "traceId": ""
}
```

### 美国国债实际收益率曲线（{@code macro_us_trycr}）。<br><br>5Y / 7Y / 10Y / 20Y / 30Y，TIPS 通胀调整后收益率。<br>与 us-tycr 同期限相减可估算市场隐含通胀。
**URL:** /openapi/v1/intl-macro/us-trycr

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 美国国债实际收益率曲线（{@code macro_us_trycr}）。

<p>5Y / 7Y / 10Y / 20Y / 30Y，TIPS 通胀调整后收益率。
与 us-tycr 同期限相减可估算市场隐含通胀。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|page|int32|false|第几页，从 1 起。默认 1。0 / 负数会被当成 1。|-|
|size|int32|false|每页记录数。默认 50，硬上限 {@value #MAX_SIZE}。<br/><p>传入超过 {@value #MAX_SIZE} 时会被自动截断到 {@value #MAX_SIZE}（不报错）。</p>|-|
|startDate|string|false|起始日期，格式 {@code YYYYMMDD}。可空。|-|
|endDate|string|false|结束日期，格式 {@code YYYYMMDD}。可空。|-|
|currType|string|false|币种（仅 libor 端点用）：{@code USD} / {@code EUR} / {@code JPY} / {@code GBP} / {@code CHF}。可空（默认 USD）。|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/intl-macro/us-trycr?page=0&size=0&endDate=&currType=&startDate='
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─date|string|日期|-|
|└─y5|number|5 年期实际收益率|-|
|└─y7|number|7 年期实际收益率|-|
|└─y10|number|10 年期实际收益率|-|
|└─y20|number|20 年期实际收益率|-|
|└─y30|number|30 年期实际收益率|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "date": "yyyy-MM-dd HH:mm:ss",
      "y5": 0,
      "y7": 0,
      "y10": 0,
      "y20": 0,
      "y30": 0
    }
  ],
  "traceId": ""
}
```

### 美国短期国债利率（{@code macro_us_tbr}）。<br><br>4w / 8w / 13w / 17w / 26w / 52w 共 6 个期限，每期限两个口径：<br>Bd（银行贴现率）+ Ce（等价票面收益率）。
**URL:** /openapi/v1/intl-macro/us-tbr

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 美国短期国债利率（{@code macro_us_tbr}）。

<p>4w / 8w / 13w / 17w / 26w / 52w 共 6 个期限，每期限两个口径：
Bd（银行贴现率）+ Ce（等价票面收益率）。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|page|int32|false|第几页，从 1 起。默认 1。0 / 负数会被当成 1。|-|
|size|int32|false|每页记录数。默认 50，硬上限 {@value #MAX_SIZE}。<br/><p>传入超过 {@value #MAX_SIZE} 时会被自动截断到 {@value #MAX_SIZE}（不报错）。</p>|-|
|startDate|string|false|起始日期，格式 {@code YYYYMMDD}。可空。|-|
|endDate|string|false|结束日期，格式 {@code YYYYMMDD}。可空。|-|
|currType|string|false|币种（仅 libor 端点用）：{@code USD} / {@code EUR} / {@code JPY} / {@code GBP} / {@code CHF}。可空（默认 USD）。|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/intl-macro/us-tbr?page=0&size=0&startDate=&endDate=&currType='
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─date|string|日期|-|
|└─w4Bd|number|4 周 Bank Discount|-|
|└─w4Ce|number|4 周 Coupon Equivalent|-|
|└─w8Bd|number|8 周 Bank Discount|-|
|└─w8Ce|number|8 周 Coupon Equivalent|-|
|└─w13Bd|number|13 周 Bank Discount|-|
|└─w13Ce|number|13 周 Coupon Equivalent|-|
|└─w17Bd|number|17 周 Bank Discount|-|
|└─w17Ce|number|17 周 Coupon Equivalent|-|
|└─w26Bd|number|26 周 Bank Discount|-|
|└─w26Ce|number|26 周 Coupon Equivalent|-|
|└─w52Bd|number|52 周 Bank Discount|-|
|└─w52Ce|number|52 周 Coupon Equivalent|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "date": "yyyy-MM-dd HH:mm:ss",
      "w4Bd": 0,
      "w4Ce": 0,
      "w8Bd": 0,
      "w8Ce": 0,
      "w13Bd": 0,
      "w13Ce": 0,
      "w17Bd": 0,
      "w17Ce": 0,
      "w26Bd": 0,
      "w26Ce": 0,
      "w52Bd": 0,
      "w52Ce": 0
    }
  ],
  "traceId": ""
}
```

### 美国国债长期利率（{@code macro_us_tltr}）。<br><br>LTC（Long-Term Composite &amp;amp;gt;10Y）/ CMT（Constant Maturity Treasury）/<br>Extrapolation Factor。在 30Y 缺失时段美联储用 LTC 替代长端基准。
**URL:** /openapi/v1/intl-macro/us-tltr

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 美国国债长期利率（{@code macro_us_tltr}）。

<p>LTC（Long-Term Composite &gt;10Y）/ CMT（Constant Maturity Treasury）/
Extrapolation Factor。在 30Y 缺失时段美联储用 LTC 替代长端基准。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|page|int32|false|第几页，从 1 起。默认 1。0 / 负数会被当成 1。|-|
|size|int32|false|每页记录数。默认 50，硬上限 {@value #MAX_SIZE}。<br/><p>传入超过 {@value #MAX_SIZE} 时会被自动截断到 {@value #MAX_SIZE}（不报错）。</p>|-|
|startDate|string|false|起始日期，格式 {@code YYYYMMDD}。可空。|-|
|endDate|string|false|结束日期，格式 {@code YYYYMMDD}。可空。|-|
|currType|string|false|币种（仅 libor 端点用）：{@code USD} / {@code EUR} / {@code JPY} / {@code GBP} / {@code CHF}。可空（默认 USD）。|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/intl-macro/us-tltr?page=0&size=0&currType=&startDate=&endDate='
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─date|string|日期|-|
|└─ltc|number|Long-Term Composite (&gt;10Yrs)|-|
|└─cmt|number|Constant Maturity Treasury|-|
|└─eFactor|number|Extrapolation Factor|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "date": "yyyy-MM-dd HH:mm:ss",
      "ltc": 0,
      "cmt": 0,
      "eFactor": 0
    }
  ],
  "traceId": ""
}
```

### 美国国债长期实际利率平均值（{@code macro_us_trltr}）。<br><br>单一指标 Long-Term Real Rate Average，通胀调整后的长端平均实际利率。
**URL:** /openapi/v1/intl-macro/us-trltr

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 美国国债长期实际利率平均值（{@code macro_us_trltr}）。

<p>单一指标 Long-Term Real Rate Average，通胀调整后的长端平均实际利率。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|page|int32|false|第几页，从 1 起。默认 1。0 / 负数会被当成 1。|-|
|size|int32|false|每页记录数。默认 50，硬上限 {@value #MAX_SIZE}。<br/><p>传入超过 {@value #MAX_SIZE} 时会被自动截断到 {@value #MAX_SIZE}（不报错）。</p>|-|
|startDate|string|false|起始日期，格式 {@code YYYYMMDD}。可空。|-|
|endDate|string|false|结束日期，格式 {@code YYYYMMDD}。可空。|-|
|currType|string|false|币种（仅 libor 端点用）：{@code USD} / {@code EUR} / {@code JPY} / {@code GBP} / {@code CHF}。可空（默认 USD）。|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/intl-macro/us-trltr?page=0&size=0&startDate=&currType=&endDate='
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─date|string|日期|-|
|└─ltrAvg|number|Long-Term Real Rate Average|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "date": "yyyy-MM-dd HH:mm:ss",
      "ltrAvg": 0
    }
  ],
  "traceId": ""
}
```

### 香港银行间同业拆借利率（{@code macro_hibor}）。<br><br>ON / 1W / 2W / 1M / 2M / 3M / 6M / 12M 共 8 个期限的港元 HIBOR。<br>港元贷款与香港房贷的主流定价基准。
**URL:** /openapi/v1/intl-macro/hibor

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 香港银行间同业拆借利率（{@code macro_hibor}）。

<p>ON / 1W / 2W / 1M / 2M / 3M / 6M / 12M 共 8 个期限的港元 HIBOR。
港元贷款与香港房贷的主流定价基准。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|page|int32|false|第几页，从 1 起。默认 1。0 / 负数会被当成 1。|-|
|size|int32|false|每页记录数。默认 50，硬上限 {@value #MAX_SIZE}。<br/><p>传入超过 {@value #MAX_SIZE} 时会被自动截断到 {@value #MAX_SIZE}（不报错）。</p>|-|
|startDate|string|false|起始日期，格式 {@code YYYYMMDD}。可空。|-|
|endDate|string|false|结束日期，格式 {@code YYYYMMDD}。可空。|-|
|currType|string|false|币种（仅 libor 端点用）：{@code USD} / {@code EUR} / {@code JPY} / {@code GBP} / {@code CHF}。可空（默认 USD）。|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/intl-macro/hibor?page=0&size=0&currType=&startDate=&endDate='
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─date|string|日期|-|
|└─onRate|number|隔夜利率（API: on）|-|
|└─w1|number|1 周利率（API: 1w）|-|
|└─w2|number|2 周利率（API: 2w）|-|
|└─m1|number|1 月利率（API: 1m）|-|
|└─m2|number|2 月利率（API: 2m）|-|
|└─m3|number|3 月利率（API: 3m）|-|
|└─m6|number|6 月利率（API: 6m）|-|
|└─m12|number|12 月利率（API: 12m）|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "date": "yyyy-MM-dd HH:mm:ss",
      "onRate": 0,
      "w1": 0,
      "w2": 0,
      "m1": 0,
      "m2": 0,
      "m3": 0,
      "m6": 0,
      "m12": 0
    }
  ],
  "traceId": ""
}
```

### 伦敦银行间同业拆借利率（{@code macro_libor}）。<br><br>多币种支持（{@code currType} = USD/EUR/JPY/GBP/CHF，可选，默认全部），<br>7 个期限：ON / 1W / 1M / 2M / 3M / 6M / 12M。<br>&lt;b&gt;历史说明&lt;/b&gt;：LIBOR 2023-06 起多数币种 / 期限被 SOFR / ESTR / TONA / SONIA 替代退役。
**URL:** /openapi/v1/intl-macro/libor

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 伦敦银行间同业拆借利率（{@code macro_libor}）。

<p>多币种支持（{@code currType} = USD/EUR/JPY/GBP/CHF，可选，默认全部），
7 个期限：ON / 1W / 1M / 2M / 3M / 6M / 12M。
<p><b>历史说明</b>：LIBOR 2023-06 起多数币种 / 期限被 SOFR / ESTR / TONA / SONIA 替代退役。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|page|int32|false|第几页，从 1 起。默认 1。0 / 负数会被当成 1。|-|
|size|int32|false|每页记录数。默认 50，硬上限 {@value #MAX_SIZE}。<br/><p>传入超过 {@value #MAX_SIZE} 时会被自动截断到 {@value #MAX_SIZE}（不报错）。</p>|-|
|startDate|string|false|起始日期，格式 {@code YYYYMMDD}。可空。|-|
|endDate|string|false|结束日期，格式 {@code YYYYMMDD}。可空。|-|
|currType|string|false|币种（仅 libor 端点用）：{@code USD} / {@code EUR} / {@code JPY} / {@code GBP} / {@code CHF}。可空（默认 USD）。|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/intl-macro/libor?page=0&size=0&startDate=&endDate=&currType='
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─date|string|日期|-|
|└─currType|string|币种（USD/EUR/JPY/GBP/CHF）|-|
|└─onRate|number|隔夜利率（API: on）|-|
|└─w1|number|1 周利率（API: 1w）|-|
|└─m1|number|1 月利率（API: 1m）|-|
|└─m2|number|2 月利率（API: 2m）|-|
|└─m3|number|3 月利率（API: 3m）|-|
|└─m6|number|6 月利率（API: 6m）|-|
|└─m12|number|12 月利率（API: 12m）|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "date": "yyyy-MM-dd HH:mm:ss",
      "currType": "",
      "onRate": 0,
      "w1": 0,
      "m1": 0,
      "m2": 0,
      "m3": 0,
      "m6": 0,
      "m12": 0
    }
  ],
  "traceId": ""
}
```

### 广州民间借贷利率（{@code macro_gz_index}）。<br><br>10D / 1M / 3M / 6M / 12M / long 共 6 个期限。<br>反映珠三角民间资金成本，作为正规渠道外的影子利率参考。
**URL:** /openapi/v1/intl-macro/gz-index

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 广州民间借贷利率（{@code macro_gz_index}）。

<p>10D / 1M / 3M / 6M / 12M / long 共 6 个期限。
反映珠三角民间资金成本，作为正规渠道外的影子利率参考。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|page|int32|false|第几页，从 1 起。默认 1。0 / 负数会被当成 1。|-|
|size|int32|false|每页记录数。默认 50，硬上限 {@value #MAX_SIZE}。<br/><p>传入超过 {@value #MAX_SIZE} 时会被自动截断到 {@value #MAX_SIZE}（不报错）。</p>|-|
|startDate|string|false|起始日期，格式 {@code YYYYMMDD}。可空。|-|
|endDate|string|false|结束日期，格式 {@code YYYYMMDD}。可空。|-|
|currType|string|false|币种（仅 libor 端点用）：{@code USD} / {@code EUR} / {@code JPY} / {@code GBP} / {@code CHF}。可空（默认 USD）。|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/intl-macro/gz-index?page=0&size=0&startDate=&currType=&endDate='
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─date|string|日期|-|
|└─d10Rate|number|10 天期利率|-|
|└─m1Rate|number|1 月期利率|-|
|└─m3Rate|number|3 月期利率|-|
|└─m6Rate|number|6 月期利率|-|
|└─m12Rate|number|12 月期利率|-|
|└─longRate|number|长期利率|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "date": "yyyy-MM-dd HH:mm:ss",
      "d10Rate": 0,
      "m1Rate": 0,
      "m3Rate": 0,
      "m6Rate": 0,
      "m12Rate": 0,
      "longRate": 0
    }
  ],
  "traceId": ""
}
```

### 温州民间借贷利率指数（{@code macro_wz_index}）。<br><br>7 个市场主体口径（中心 / 微贷 / 资管 / 直接 / 农村互助 等）+ 4 个期限（1M/3M/6M/12M）<br>+ 长期 + 综合指数 {@code compRate}。
**URL:** /openapi/v1/intl-macro/wz-index

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 温州民间借贷利率指数（{@code macro_wz_index}）。

<p>7 个市场主体口径（中心 / 微贷 / 资管 / 直接 / 农村互助 等）+ 4 个期限（1M/3M/6M/12M）
+ 长期 + 综合指数 {@code compRate}。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|page|int32|false|第几页，从 1 起。默认 1。0 / 负数会被当成 1。|-|
|size|int32|false|每页记录数。默认 50，硬上限 {@value #MAX_SIZE}。<br/><p>传入超过 {@value #MAX_SIZE} 时会被自动截断到 {@value #MAX_SIZE}（不报错）。</p>|-|
|startDate|string|false|起始日期，格式 {@code YYYYMMDD}。可空。|-|
|endDate|string|false|结束日期，格式 {@code YYYYMMDD}。可空。|-|
|currType|string|false|币种（仅 libor 端点用）：{@code USD} / {@code EUR} / {@code JPY} / {@code GBP} / {@code CHF}。可空（默认 USD）。|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/intl-macro/wz-index?page=0&size=0&endDate=&startDate=&currType='
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─date|string|日期|-|
|└─compRate|number|温州民间融资综合利率指数|-|
|└─centerRate|number|民间借贷服务中心利率|-|
|└─microRate|number|小额贷款公司放款利率|-|
|└─cmRate|number|民间资本管理公司融资价格|-|
|└─sdbRate|number|社会直接借贷利率|-|
|└─omRate|number|其他市场主体利率|-|
|└─aaRate|number|农村互助会互助金费率|-|
|└─m1Rate|number|1 月期利率|-|
|└─m3Rate|number|3 月期利率|-|
|└─m6Rate|number|6 月期利率|-|
|└─m12Rate|number|12 月期利率|-|
|└─longRate|number|长期借贷利率|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "date": "yyyy-MM-dd HH:mm:ss",
      "compRate": 0,
      "centerRate": 0,
      "microRate": 0,
      "cmRate": 0,
      "sdbRate": 0,
      "omRate": 0,
      "aaRate": 0,
      "m1Rate": 0,
      "m3Rate": 0,
      "m6Rate": 0,
      "m12Rate": 0,
      "longRate": 0
    }
  ],
  "traceId": ""
}
```

## OpenAPI v1 —— 港股全量端点（{@code stock.hk} scope，Max 套餐及以上）。

&lt;p&gt;覆盖 10 张 PG 表的 10 个端点：
&lt;ul&gt;
  &lt;li&gt;{@code POST /openapi/v1/stock/hk/basic}        — 港股基础信息&lt;/li&gt;
  &lt;li&gt;{@code POST /openapi/v1/stock/hk/tradecal}     — 港股交易日历&lt;/li&gt;
  &lt;li&gt;{@code POST /openapi/v1/stock/hk/kline}        — 港股日 K 线（不复权）&lt;/li&gt;
  &lt;li&gt;{@code POST /openapi/v1/stock/hk/kline-adj}    — 港股日 K 线（复权 + 估值快照）&lt;/li&gt;
  &lt;li&gt;{@code POST /openapi/v1/stock/hk/adj-factor}   — 港股复权因子&lt;/li&gt;
  &lt;li&gt;{@code POST /openapi/v1/stock/hk/minute}       — 港股分钟 K 线&lt;/li&gt;
  &lt;li&gt;{@code POST /openapi/v1/stock/hk/income}       — 港股利润表（long format）&lt;/li&gt;
  &lt;li&gt;{@code POST /openapi/v1/stock/hk/balance-sheet}— 港股资产负债表（long format）&lt;/li&gt;
  &lt;li&gt;{@code POST /openapi/v1/stock/hk/cash-flow}    — 港股现金流量表（long format）&lt;/li&gt;
  &lt;li&gt;{@code POST /openapi/v1/stock/hk/fina-indicator}— 港股财务指标（精简 30 列）&lt;/li&gt;
&lt;/ul&gt;

&lt;p&gt;注：港股通持股（{@code stock_hk_hold}）已在 {@code OpenApiV1StockShareholderController} 下的
{@code /openapi/v1/stock/shareholder/hk-hold} 暴露（{@code stock.shareholder} scope），此处不再重复。
### 港股基础信息（{@code stock_hk_basic}）。<br><br>{@code tsCode} 可空（列全市场），可选 {@code listStatus} 过滤（{@code L} 上市 / {@code D} 退市）。
**URL:** /openapi/v1/stock/hk/basic

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 港股基础信息（{@code stock_hk_basic}）。

<p>{@code tsCode} 可空（列全市场），可选 {@code listStatus} 过滤（{@code L} 上市 / {@code D} 退市）。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|page|int32|false|第几页，从 1 起。默认 1。0 / 负数会被当成 1。|-|
|size|int32|false|每页记录数。默认 50，硬上限 {@value #MAX_SIZE}。<br/><p>传入超过 {@value #MAX_SIZE} 时会被自动截断到 {@value #MAX_SIZE}（不报错）。</p>|-|
|tsCode|string|false|港股 TS 代码，如 {@code "00700.HK"}。<br/><p>K 线 / 分钟 / 三大表 / 财务指标必填；basic / tradecal 可空。</p>|-|
|startDate|string|false|起始日期，格式 {@code YYYYMMDD}。可空。|-|
|endDate|string|false|结束日期，格式 {@code YYYYMMDD}。可空。|-|
|startTime|string|false|分钟级起始时间，格式 {@code YYYY-MM-DD HH:mm:ss}。仅 minute 端点用。|-|
|endTime|string|false|分钟级结束时间，格式 {@code YYYY-MM-DD HH:mm:ss}。仅 minute 端点用。|-|
|freq|string|false|分钟频率：{@code 1min} / {@code 5min} / {@code 15min} / {@code 30min} / {@code 60min}。<br/>仅 minute 端点用，默认 {@code 60min}。|-|
|reportType|string|false|报告期（仅 fina-indicator 端点用，精确等值匹配 report_type 列）。<b>值是带年份的完整报告期串</b>，<br/>如 {@code "2024年中报"} / {@code "2023年年报"}（港股只有年报 / 中报，无季报）。<br/><b>不要</b>传 {@code "中报"}/{@code "年报"} 这种不带年份的——匹配不到、返回空。<br/><b>不确定就别传</b>（返回全部报告期，自己再按年份/期别筛）。可空。|-|
|listStatus|string|false|上市状态（仅 basic 端点用）：{@code L} 上市 / {@code D} 退市 / {@code P} 暂停。可空。|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/stock/hk/basic?page=0&size=0&freq=&listStatus=&startTime=&endTime=&endDate=&reportType=&tsCode=&startDate='
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─tsCode|string|TS 代码（如 {@code 00700.HK}）|-|
|└─name|string|股票简称|-|
|└─fullname|string|公司全称|-|
|└─enname|string|英文名称|-|
|└─cnSpell|string|拼音简称|-|
|└─market|string|市场类别（主板 / 创业板）|-|
|└─listStatus|string|上市状态 {@code L} 上市 / {@code D} 退市 / {@code P} 暂停|-|
|└─listDate|string|上市日期|-|
|└─delistDate|string|退市日期|-|
|└─tradeUnit|number|交易单位（手）|-|
|└─isin|string|ISIN 代码|-|
|└─currType|string|货币代码（{@code HKD} / {@code USD} 等）|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "tsCode": "",
      "name": "",
      "fullname": "",
      "enname": "",
      "cnSpell": "",
      "market": "",
      "listStatus": "",
      "listDate": "yyyy-MM-dd HH:mm:ss",
      "delistDate": "yyyy-MM-dd HH:mm:ss",
      "tradeUnit": 0,
      "isin": "",
      "currType": ""
    }
  ],
  "traceId": ""
}
```

### 港股交易日历（{@code stock_hk_tradecal}）。<br><br>用途：判断港股是否交易日、计算上一/下一交易日。{@code startDate} / {@code endDate} 可空。
**URL:** /openapi/v1/stock/hk/tradecal

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 港股交易日历（{@code stock_hk_tradecal}）。

<p>用途：判断港股是否交易日、计算上一/下一交易日。{@code startDate} / {@code endDate} 可空。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|page|int32|false|第几页，从 1 起。默认 1。0 / 负数会被当成 1。|-|
|size|int32|false|每页记录数。默认 50，硬上限 {@value #MAX_SIZE}。<br/><p>传入超过 {@value #MAX_SIZE} 时会被自动截断到 {@value #MAX_SIZE}（不报错）。</p>|-|
|tsCode|string|false|港股 TS 代码，如 {@code "00700.HK"}。<br/><p>K 线 / 分钟 / 三大表 / 财务指标必填；basic / tradecal 可空。</p>|-|
|startDate|string|false|起始日期，格式 {@code YYYYMMDD}。可空。|-|
|endDate|string|false|结束日期，格式 {@code YYYYMMDD}。可空。|-|
|startTime|string|false|分钟级起始时间，格式 {@code YYYY-MM-DD HH:mm:ss}。仅 minute 端点用。|-|
|endTime|string|false|分钟级结束时间，格式 {@code YYYY-MM-DD HH:mm:ss}。仅 minute 端点用。|-|
|freq|string|false|分钟频率：{@code 1min} / {@code 5min} / {@code 15min} / {@code 30min} / {@code 60min}。<br/>仅 minute 端点用，默认 {@code 60min}。|-|
|reportType|string|false|报告期（仅 fina-indicator 端点用，精确等值匹配 report_type 列）。<b>值是带年份的完整报告期串</b>，<br/>如 {@code "2024年中报"} / {@code "2023年年报"}（港股只有年报 / 中报，无季报）。<br/><b>不要</b>传 {@code "中报"}/{@code "年报"} 这种不带年份的——匹配不到、返回空。<br/><b>不确定就别传</b>（返回全部报告期，自己再按年份/期别筛）。可空。|-|
|listStatus|string|false|上市状态（仅 basic 端点用）：{@code L} 上市 / {@code D} 退市 / {@code P} 暂停。可空。|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/stock/hk/tradecal?page=0&size=0&endDate=&endTime=&reportType=&listStatus=&freq=&tsCode=&startDate=&startTime='
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─calDate|string|日历日期|-|
|└─isOpen|int32|是否交易：0 休市 / 1 交易|-|
|└─pretradeDate|string|上一个交易日|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "calDate": "yyyy-MM-dd HH:mm:ss",
      "isOpen": 0,
      "pretradeDate": "yyyy-MM-dd HH:mm:ss"
    }
  ],
  "traceId": ""
}
```

### 港股日 K 线（不复权，{@code stock_hk_daily}）。{@code tsCode} 必填。<br><br>跨除权日比较股价时建议改用 {@code /kline-adj}（含复权）或配合 {@code /adj-factor} 自行换算。
**URL:** /openapi/v1/stock/hk/kline

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 港股日 K 线（不复权，{@code stock_hk_daily}）。{@code tsCode} 必填。

<p>跨除权日比较股价时建议改用 {@code /kline-adj}（含复权）或配合 {@code /adj-factor} 自行换算。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|page|int32|false|第几页，从 1 起。默认 1。0 / 负数会被当成 1。|-|
|size|int32|false|每页记录数。默认 50，硬上限 {@value #MAX_SIZE}。<br/><p>传入超过 {@value #MAX_SIZE} 时会被自动截断到 {@value #MAX_SIZE}（不报错）。</p>|-|
|tsCode|string|false|港股 TS 代码，如 {@code "00700.HK"}。<br/><p>K 线 / 分钟 / 三大表 / 财务指标必填；basic / tradecal 可空。</p>|-|
|startDate|string|false|起始日期，格式 {@code YYYYMMDD}。可空。|-|
|endDate|string|false|结束日期，格式 {@code YYYYMMDD}。可空。|-|
|startTime|string|false|分钟级起始时间，格式 {@code YYYY-MM-DD HH:mm:ss}。仅 minute 端点用。|-|
|endTime|string|false|分钟级结束时间，格式 {@code YYYY-MM-DD HH:mm:ss}。仅 minute 端点用。|-|
|freq|string|false|分钟频率：{@code 1min} / {@code 5min} / {@code 15min} / {@code 30min} / {@code 60min}。<br/>仅 minute 端点用，默认 {@code 60min}。|-|
|reportType|string|false|报告期（仅 fina-indicator 端点用，精确等值匹配 report_type 列）。<b>值是带年份的完整报告期串</b>，<br/>如 {@code "2024年中报"} / {@code "2023年年报"}（港股只有年报 / 中报，无季报）。<br/><b>不要</b>传 {@code "中报"}/{@code "年报"} 这种不带年份的——匹配不到、返回空。<br/><b>不确定就别传</b>（返回全部报告期，自己再按年份/期别筛）。可空。|-|
|listStatus|string|false|上市状态（仅 basic 端点用）：{@code L} 上市 / {@code D} 退市 / {@code P} 暂停。可空。|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/stock/hk/kline?page=0&size=0&endDate=&startTime=&tsCode=&startDate=&freq=&endTime=&reportType=&listStatus='
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─tsCode|string|TS 代码|-|
|└─tradeDate|string|交易日期|-|
|└─open|number|开盘价|-|
|└─high|number|最高价|-|
|└─low|number|最低价|-|
|└─close|number|收盘价|-|
|└─preClose|number|昨收价|-|
|└─change|number|涨跌额|-|
|└─pctChg|number|涨跌幅（%）|-|
|└─vol|number|成交量（股）|-|
|└─amount|number|成交额（港元）|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "tsCode": "",
      "tradeDate": "yyyy-MM-dd HH:mm:ss",
      "open": 0,
      "high": 0,
      "low": 0,
      "close": 0,
      "preClose": 0,
      "change": 0,
      "pctChg": 0,
      "vol": 0,
      "amount": 0
    }
  ],
  "traceId": ""
}
```

### 港股日 K 线（复权 + 估值快照，{@code stock_hk_daily_adj}）。{@code tsCode} 必填。<br><br>一站式港股数据：OHLCV + vwap + adj_factor + turnover_ratio + 流通/总股本 + 流通/总市值。
**URL:** /openapi/v1/stock/hk/kline-adj

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 港股日 K 线（复权 + 估值快照，{@code stock_hk_daily_adj}）。{@code tsCode} 必填。

<p>一站式港股数据：OHLCV + vwap + adj_factor + turnover_ratio + 流通/总股本 + 流通/总市值。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|page|int32|false|第几页，从 1 起。默认 1。0 / 负数会被当成 1。|-|
|size|int32|false|每页记录数。默认 50，硬上限 {@value #MAX_SIZE}。<br/><p>传入超过 {@value #MAX_SIZE} 时会被自动截断到 {@value #MAX_SIZE}（不报错）。</p>|-|
|tsCode|string|false|港股 TS 代码，如 {@code "00700.HK"}。<br/><p>K 线 / 分钟 / 三大表 / 财务指标必填；basic / tradecal 可空。</p>|-|
|startDate|string|false|起始日期，格式 {@code YYYYMMDD}。可空。|-|
|endDate|string|false|结束日期，格式 {@code YYYYMMDD}。可空。|-|
|startTime|string|false|分钟级起始时间，格式 {@code YYYY-MM-DD HH:mm:ss}。仅 minute 端点用。|-|
|endTime|string|false|分钟级结束时间，格式 {@code YYYY-MM-DD HH:mm:ss}。仅 minute 端点用。|-|
|freq|string|false|分钟频率：{@code 1min} / {@code 5min} / {@code 15min} / {@code 30min} / {@code 60min}。<br/>仅 minute 端点用，默认 {@code 60min}。|-|
|reportType|string|false|报告期（仅 fina-indicator 端点用，精确等值匹配 report_type 列）。<b>值是带年份的完整报告期串</b>，<br/>如 {@code "2024年中报"} / {@code "2023年年报"}（港股只有年报 / 中报，无季报）。<br/><b>不要</b>传 {@code "中报"}/{@code "年报"} 这种不带年份的——匹配不到、返回空。<br/><b>不确定就别传</b>（返回全部报告期，自己再按年份/期别筛）。可空。|-|
|listStatus|string|false|上市状态（仅 basic 端点用）：{@code L} 上市 / {@code D} 退市 / {@code P} 暂停。可空。|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/stock/hk/kline-adj?page=0&size=0&reportType=&startTime=&endDate=&tsCode=&listStatus=&endTime=&startDate=&freq='
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─tsCode|string|TS 代码|-|
|└─tradeDate|string|交易日期|-|
|└─close|number|收盘价|-|
|└─open|number|开盘价|-|
|└─high|number|最高价|-|
|└─low|number|最低价|-|
|└─preClose|number|昨收价|-|
|└─change|number|涨跌额|-|
|└─pctChange|number|涨跌幅（%）|-|
|└─vol|number|成交量（股）|-|
|└─amount|number|成交额（港元）|-|
|└─vwap|number|成交均价|-|
|└─adjFactor|number|复权因子|-|
|└─turnoverRatio|number|换手率（%）|-|
|└─freeShare|number|流通股本（股）|-|
|└─totalShare|number|总股本（股）|-|
|└─freeMv|number|流通市值|-|
|└─totalMv|number|总市值|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "tsCode": "",
      "tradeDate": "yyyy-MM-dd HH:mm:ss",
      "close": 0,
      "open": 0,
      "high": 0,
      "low": 0,
      "preClose": 0,
      "change": 0,
      "pctChange": 0,
      "vol": 0,
      "amount": 0,
      "vwap": 0,
      "adjFactor": 0,
      "turnoverRatio": 0,
      "freeShare": 0,
      "totalShare": 0,
      "freeMv": 0,
      "totalMv": 0
    }
  ],
  "traceId": ""
}
```

### 港股复权因子（{@code stock_hk_adjfactor}）。{@code tsCode} 必填。<br><br>用法：HFQ_price = BFQ_price × cum_adjfactor / 当日最新 cum_adjfactor。
**URL:** /openapi/v1/stock/hk/adj-factor

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 港股复权因子（{@code stock_hk_adjfactor}）。{@code tsCode} 必填。

<p>用法：HFQ_price = BFQ_price × cum_adjfactor / 当日最新 cum_adjfactor。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|page|int32|false|第几页，从 1 起。默认 1。0 / 负数会被当成 1。|-|
|size|int32|false|每页记录数。默认 50，硬上限 {@value #MAX_SIZE}。<br/><p>传入超过 {@value #MAX_SIZE} 时会被自动截断到 {@value #MAX_SIZE}（不报错）。</p>|-|
|tsCode|string|false|港股 TS 代码，如 {@code "00700.HK"}。<br/><p>K 线 / 分钟 / 三大表 / 财务指标必填；basic / tradecal 可空。</p>|-|
|startDate|string|false|起始日期，格式 {@code YYYYMMDD}。可空。|-|
|endDate|string|false|结束日期，格式 {@code YYYYMMDD}。可空。|-|
|startTime|string|false|分钟级起始时间，格式 {@code YYYY-MM-DD HH:mm:ss}。仅 minute 端点用。|-|
|endTime|string|false|分钟级结束时间，格式 {@code YYYY-MM-DD HH:mm:ss}。仅 minute 端点用。|-|
|freq|string|false|分钟频率：{@code 1min} / {@code 5min} / {@code 15min} / {@code 30min} / {@code 60min}。<br/>仅 minute 端点用，默认 {@code 60min}。|-|
|reportType|string|false|报告期（仅 fina-indicator 端点用，精确等值匹配 report_type 列）。<b>值是带年份的完整报告期串</b>，<br/>如 {@code "2024年中报"} / {@code "2023年年报"}（港股只有年报 / 中报，无季报）。<br/><b>不要</b>传 {@code "中报"}/{@code "年报"} 这种不带年份的——匹配不到、返回空。<br/><b>不确定就别传</b>（返回全部报告期，自己再按年份/期别筛）。可空。|-|
|listStatus|string|false|上市状态（仅 basic 端点用）：{@code L} 上市 / {@code D} 退市 / {@code P} 暂停。可空。|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/stock/hk/adj-factor?page=0&size=0&startDate=&endTime=&freq=&reportType=&tsCode=&endDate=&listStatus=&startTime='
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─tsCode|string|TS 代码|-|
|└─tradeDate|string|交易日期|-|
|└─cumAdjfactor|number|累计复权因子|-|
|└─closePrice|number|当日收盘价|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "tsCode": "",
      "tradeDate": "yyyy-MM-dd HH:mm:ss",
      "cumAdjfactor": 0,
      "closePrice": 0
    }
  ],
  "traceId": ""
}
```

### 港股分钟 K 线（{@code stock_hk_mins}）。{@code tsCode} 必填。<br><br>{@code freq} 默认 {@code 60min}（可选 {@code 1min} / {@code 5min} / {@code 15min} / {@code 30min}）。<br>时间范围用 {@code startTime} / {@code endTime}（{@code YYYY-MM-DD HH:mm:ss} 格式）。
**URL:** /openapi/v1/stock/hk/minute

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 港股分钟 K 线（{@code stock_hk_mins}）。{@code tsCode} 必填。

<p>{@code freq} 默认 {@code 60min}（可选 {@code 1min} / {@code 5min} / {@code 15min} / {@code 30min}）。
时间范围用 {@code startTime} / {@code endTime}（{@code YYYY-MM-DD HH:mm:ss} 格式）。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|page|int32|false|第几页，从 1 起。默认 1。0 / 负数会被当成 1。|-|
|size|int32|false|每页记录数。默认 50，硬上限 {@value #MAX_SIZE}。<br/><p>传入超过 {@value #MAX_SIZE} 时会被自动截断到 {@value #MAX_SIZE}（不报错）。</p>|-|
|tsCode|string|false|港股 TS 代码，如 {@code "00700.HK"}。<br/><p>K 线 / 分钟 / 三大表 / 财务指标必填；basic / tradecal 可空。</p>|-|
|startDate|string|false|起始日期，格式 {@code YYYYMMDD}。可空。|-|
|endDate|string|false|结束日期，格式 {@code YYYYMMDD}。可空。|-|
|startTime|string|false|分钟级起始时间，格式 {@code YYYY-MM-DD HH:mm:ss}。仅 minute 端点用。|-|
|endTime|string|false|分钟级结束时间，格式 {@code YYYY-MM-DD HH:mm:ss}。仅 minute 端点用。|-|
|freq|string|false|分钟频率：{@code 1min} / {@code 5min} / {@code 15min} / {@code 30min} / {@code 60min}。<br/>仅 minute 端点用，默认 {@code 60min}。|-|
|reportType|string|false|报告期（仅 fina-indicator 端点用，精确等值匹配 report_type 列）。<b>值是带年份的完整报告期串</b>，<br/>如 {@code "2024年中报"} / {@code "2023年年报"}（港股只有年报 / 中报，无季报）。<br/><b>不要</b>传 {@code "中报"}/{@code "年报"} 这种不带年份的——匹配不到、返回空。<br/><b>不确定就别传</b>（返回全部报告期，自己再按年份/期别筛）。可空。|-|
|listStatus|string|false|上市状态（仅 basic 端点用）：{@code L} 上市 / {@code D} 退市 / {@code P} 暂停。可空。|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/stock/hk/minute?page=0&size=0&tsCode=&startTime=&endTime=&freq=&listStatus=&endDate=&reportType=&startDate='
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─tsCode|string|TS 代码|-|
|└─tradeTime|string|分钟级时间戳|-|
|└─freq|string|频率（{@code 1min} / {@code 5min} / {@code 15min} / {@code 30min} / {@code 60min}）|-|
|└─open|number|开盘价|-|
|└─high|number|最高价|-|
|└─low|number|最低价|-|
|└─close|number|收盘价|-|
|└─vol|number|成交量|-|
|└─amount|number|成交额|-|
|└─preClose|number|昨收价|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "tsCode": "",
      "tradeTime": "yyyy-MM-dd HH:mm:ss",
      "freq": "",
      "open": 0,
      "high": 0,
      "low": 0,
      "close": 0,
      "vol": 0,
      "amount": 0,
      "preClose": 0
    }
  ],
  "traceId": ""
}
```

### 港股利润表（long format，{@code stock_hk_income}）。{@code tsCode} 必填。<br><br>每行一个 {@code indName} → {@code indValue} 键值对。需在客户端做透视成宽表。
**URL:** /openapi/v1/stock/hk/income

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 港股利润表（long format，{@code stock_hk_income}）。{@code tsCode} 必填。

<p>每行一个 {@code indName} → {@code indValue} 键值对。需在客户端做透视成宽表。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|page|int32|false|第几页，从 1 起。默认 1。0 / 负数会被当成 1。|-|
|size|int32|false|每页记录数。默认 50，硬上限 {@value #MAX_SIZE}。<br/><p>传入超过 {@value #MAX_SIZE} 时会被自动截断到 {@value #MAX_SIZE}（不报错）。</p>|-|
|tsCode|string|false|港股 TS 代码，如 {@code "00700.HK"}。<br/><p>K 线 / 分钟 / 三大表 / 财务指标必填；basic / tradecal 可空。</p>|-|
|startDate|string|false|起始日期，格式 {@code YYYYMMDD}。可空。|-|
|endDate|string|false|结束日期，格式 {@code YYYYMMDD}。可空。|-|
|startTime|string|false|分钟级起始时间，格式 {@code YYYY-MM-DD HH:mm:ss}。仅 minute 端点用。|-|
|endTime|string|false|分钟级结束时间，格式 {@code YYYY-MM-DD HH:mm:ss}。仅 minute 端点用。|-|
|freq|string|false|分钟频率：{@code 1min} / {@code 5min} / {@code 15min} / {@code 30min} / {@code 60min}。<br/>仅 minute 端点用，默认 {@code 60min}。|-|
|reportType|string|false|报告期（仅 fina-indicator 端点用，精确等值匹配 report_type 列）。<b>值是带年份的完整报告期串</b>，<br/>如 {@code "2024年中报"} / {@code "2023年年报"}（港股只有年报 / 中报，无季报）。<br/><b>不要</b>传 {@code "中报"}/{@code "年报"} 这种不带年份的——匹配不到、返回空。<br/><b>不确定就别传</b>（返回全部报告期，自己再按年份/期别筛）。可空。|-|
|listStatus|string|false|上市状态（仅 basic 端点用）：{@code L} 上市 / {@code D} 退市 / {@code P} 暂停。可空。|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/stock/hk/income?page=0&size=0&startDate=&endTime=&reportType=&listStatus=&endDate=&tsCode=&freq=&startTime='
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─tsCode|string|TS 代码|-|
|└─endDate|string|报告期|-|
|└─name|string|股票名称|-|
|└─indName|string|指标名称|-|
|└─indValue|number|指标值|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "tsCode": "",
      "endDate": "yyyy-MM-dd HH:mm:ss",
      "name": "",
      "indName": "",
      "indValue": 0
    }
  ],
  "traceId": ""
}
```

### 港股资产负债表（long format，{@code stock_hk_balancesheet}）。{@code tsCode} 必填。
**URL:** /openapi/v1/stock/hk/balance-sheet

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 港股资产负债表（long format，{@code stock_hk_balancesheet}）。{@code tsCode} 必填。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|page|int32|false|第几页，从 1 起。默认 1。0 / 负数会被当成 1。|-|
|size|int32|false|每页记录数。默认 50，硬上限 {@value #MAX_SIZE}。<br/><p>传入超过 {@value #MAX_SIZE} 时会被自动截断到 {@value #MAX_SIZE}（不报错）。</p>|-|
|tsCode|string|false|港股 TS 代码，如 {@code "00700.HK"}。<br/><p>K 线 / 分钟 / 三大表 / 财务指标必填；basic / tradecal 可空。</p>|-|
|startDate|string|false|起始日期，格式 {@code YYYYMMDD}。可空。|-|
|endDate|string|false|结束日期，格式 {@code YYYYMMDD}。可空。|-|
|startTime|string|false|分钟级起始时间，格式 {@code YYYY-MM-DD HH:mm:ss}。仅 minute 端点用。|-|
|endTime|string|false|分钟级结束时间，格式 {@code YYYY-MM-DD HH:mm:ss}。仅 minute 端点用。|-|
|freq|string|false|分钟频率：{@code 1min} / {@code 5min} / {@code 15min} / {@code 30min} / {@code 60min}。<br/>仅 minute 端点用，默认 {@code 60min}。|-|
|reportType|string|false|报告期（仅 fina-indicator 端点用，精确等值匹配 report_type 列）。<b>值是带年份的完整报告期串</b>，<br/>如 {@code "2024年中报"} / {@code "2023年年报"}（港股只有年报 / 中报，无季报）。<br/><b>不要</b>传 {@code "中报"}/{@code "年报"} 这种不带年份的——匹配不到、返回空。<br/><b>不确定就别传</b>（返回全部报告期，自己再按年份/期别筛）。可空。|-|
|listStatus|string|false|上市状态（仅 basic 端点用）：{@code L} 上市 / {@code D} 退市 / {@code P} 暂停。可空。|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/stock/hk/balance-sheet?page=0&size=0&endTime=&reportType=&freq=&startDate=&tsCode=&startTime=&listStatus=&endDate='
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─tsCode|string|TS 代码|-|
|└─endDate|string|报告期|-|
|└─name|string|股票名称|-|
|└─indName|string|指标名称|-|
|└─indValue|number|指标值|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "tsCode": "",
      "endDate": "yyyy-MM-dd HH:mm:ss",
      "name": "",
      "indName": "",
      "indValue": 0
    }
  ],
  "traceId": ""
}
```

### 港股现金流量表（long format，{@code stock_hk_cashflow}）。{@code tsCode} 必填。
**URL:** /openapi/v1/stock/hk/cash-flow

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 港股现金流量表（long format，{@code stock_hk_cashflow}）。{@code tsCode} 必填。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|page|int32|false|第几页，从 1 起。默认 1。0 / 负数会被当成 1。|-|
|size|int32|false|每页记录数。默认 50，硬上限 {@value #MAX_SIZE}。<br/><p>传入超过 {@value #MAX_SIZE} 时会被自动截断到 {@value #MAX_SIZE}（不报错）。</p>|-|
|tsCode|string|false|港股 TS 代码，如 {@code "00700.HK"}。<br/><p>K 线 / 分钟 / 三大表 / 财务指标必填；basic / tradecal 可空。</p>|-|
|startDate|string|false|起始日期，格式 {@code YYYYMMDD}。可空。|-|
|endDate|string|false|结束日期，格式 {@code YYYYMMDD}。可空。|-|
|startTime|string|false|分钟级起始时间，格式 {@code YYYY-MM-DD HH:mm:ss}。仅 minute 端点用。|-|
|endTime|string|false|分钟级结束时间，格式 {@code YYYY-MM-DD HH:mm:ss}。仅 minute 端点用。|-|
|freq|string|false|分钟频率：{@code 1min} / {@code 5min} / {@code 15min} / {@code 30min} / {@code 60min}。<br/>仅 minute 端点用，默认 {@code 60min}。|-|
|reportType|string|false|报告期（仅 fina-indicator 端点用，精确等值匹配 report_type 列）。<b>值是带年份的完整报告期串</b>，<br/>如 {@code "2024年中报"} / {@code "2023年年报"}（港股只有年报 / 中报，无季报）。<br/><b>不要</b>传 {@code "中报"}/{@code "年报"} 这种不带年份的——匹配不到、返回空。<br/><b>不确定就别传</b>（返回全部报告期，自己再按年份/期别筛）。可空。|-|
|listStatus|string|false|上市状态（仅 basic 端点用）：{@code L} 上市 / {@code D} 退市 / {@code P} 暂停。可空。|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/stock/hk/cash-flow?page=0&size=0&tsCode=&endDate=&listStatus=&reportType=&startDate=&startTime=&endTime=&freq='
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─tsCode|string|TS 代码|-|
|└─endDate|string|报告期|-|
|└─name|string|股票名称|-|
|└─indName|string|指标名称|-|
|└─indValue|number|指标值|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "tsCode": "",
      "endDate": "yyyy-MM-dd HH:mm:ss",
      "name": "",
      "indName": "",
      "indValue": 0
    }
  ],
  "traceId": ""
}
```

### 港股财务指标（精简 30 核心列，{@code stock_hk_fina_indicator}）。{@code tsCode} 必填。<br><br>每股 / 盈利能力 / 现金流 / 偿债 / 估值 / 增长。{@code reportType} 可选过滤（年报 / 中报 / 季报）。<br>表共 ~85 列，本端点只暴露 30 个高频字段；银行保险特有指标不在此暴露。
**URL:** /openapi/v1/stock/hk/fina-indicator

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 港股财务指标（精简 30 核心列，{@code stock_hk_fina_indicator}）。{@code tsCode} 必填。

<p>每股 / 盈利能力 / 现金流 / 偿债 / 估值 / 增长。{@code reportType} 可选过滤（年报 / 中报 / 季报）。
<p>表共 ~85 列，本端点只暴露 30 个高频字段；银行保险特有指标不在此暴露。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|page|int32|false|第几页，从 1 起。默认 1。0 / 负数会被当成 1。|-|
|size|int32|false|每页记录数。默认 50，硬上限 {@value #MAX_SIZE}。<br/><p>传入超过 {@value #MAX_SIZE} 时会被自动截断到 {@value #MAX_SIZE}（不报错）。</p>|-|
|tsCode|string|false|港股 TS 代码，如 {@code "00700.HK"}。<br/><p>K 线 / 分钟 / 三大表 / 财务指标必填；basic / tradecal 可空。</p>|-|
|startDate|string|false|起始日期，格式 {@code YYYYMMDD}。可空。|-|
|endDate|string|false|结束日期，格式 {@code YYYYMMDD}。可空。|-|
|startTime|string|false|分钟级起始时间，格式 {@code YYYY-MM-DD HH:mm:ss}。仅 minute 端点用。|-|
|endTime|string|false|分钟级结束时间，格式 {@code YYYY-MM-DD HH:mm:ss}。仅 minute 端点用。|-|
|freq|string|false|分钟频率：{@code 1min} / {@code 5min} / {@code 15min} / {@code 30min} / {@code 60min}。<br/>仅 minute 端点用，默认 {@code 60min}。|-|
|reportType|string|false|报告期（仅 fina-indicator 端点用，精确等值匹配 report_type 列）。<b>值是带年份的完整报告期串</b>，<br/>如 {@code "2024年中报"} / {@code "2023年年报"}（港股只有年报 / 中报，无季报）。<br/><b>不要</b>传 {@code "中报"}/{@code "年报"} 这种不带年份的——匹配不到、返回空。<br/><b>不确定就别传</b>（返回全部报告期，自己再按年份/期别筛）。可空。|-|
|listStatus|string|false|上市状态（仅 basic 端点用）：{@code L} 上市 / {@code D} 退市 / {@code P} 暂停。可空。|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/stock/hk/fina-indicator?page=0&size=0&endDate=&freq=&startTime=&startDate=&reportType=&listStatus=&tsCode=&endTime='
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─tsCode|string|TS 代码|-|
|└─name|string|股票名称|-|
|└─endDate|string|报告期|-|
|└─reportType|string|报告类型（年报 / 中报 / 季报）|-|
|└─orgType|string|行业分类|-|
|└─currency|string|货币|-|
|└─bps|number|每股净资产|-|
|└─basicEps|number|基本每股收益|-|
|└─dilutedEps|number|稀释每股收益|-|
|└─perOi|number|每股营业收入|-|
|└─perNetcashOperate|number|每股经营现金流|-|
|└─epsTtm|number|TTM 每股收益|-|
|└─operateIncome|number|营业收入|-|
|└─operateIncomeYoy|number|营业收入同比|-|
|└─grossProfit|number|毛利润|-|
|└─grossProfitRatio|number|毛利率|-|
|└─netProfitRatio|number|净利率|-|
|└─holderProfit|number|归母净利润|-|
|└─holderProfitYoy|number|归母净利润同比|-|
|└─roeAvg|number|平均 ROE|-|
|└─roeYearly|number|年化 ROE|-|
|└─roicYearly|number|年化 ROIC|-|
|└─roa|number|ROA|-|
|└─netcashOperate|number|经营活动现金流净额|-|
|└─netcashInvest|number|投资活动现金流净额|-|
|└─netcashFinance|number|筹资活动现金流净额|-|
|└─endCash|number|期末现金|-|
|└─totalAssets|number|总资产|-|
|└─totalLiabilities|number|总负债|-|
|└─debtAssetRatio|number|资产负债率|-|
|└─currentRatio|number|流动比率|-|
|└─diviRatio|number|派息比率|-|
|└─dividendRate|number|股息率|-|
|└─totalMarketCap|number|总市值|-|
|└─peTtm|number|市盈率 TTM|-|
|└─pbTtm|number|市净率 TTM|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "tsCode": "",
      "name": "",
      "endDate": "yyyy-MM-dd HH:mm:ss",
      "reportType": "",
      "orgType": "",
      "currency": "",
      "bps": 0,
      "basicEps": 0,
      "dilutedEps": 0,
      "perOi": 0,
      "perNetcashOperate": 0,
      "epsTtm": 0,
      "operateIncome": 0,
      "operateIncomeYoy": 0,
      "grossProfit": 0,
      "grossProfitRatio": 0,
      "netProfitRatio": 0,
      "holderProfit": 0,
      "holderProfitYoy": 0,
      "roeAvg": 0,
      "roeYearly": 0,
      "roicYearly": 0,
      "roa": 0,
      "netcashOperate": 0,
      "netcashInvest": 0,
      "netcashFinance": 0,
      "endCash": 0,
      "totalAssets": 0,
      "totalLiabilities": 0,
      "debtAssetRatio": 0,
      "currentRatio": 0,
      "diviRatio": 0,
      "dividendRate": 0,
      "totalMarketCap": 0,
      "peTtm": 0,
      "pbTtm": 0
    }
  ],
  "traceId": ""
}
```

## OpenAPI v1 —— TMT 媒体数据全量端点（{@code tmt} scope，Ultra 内部档——数据待补齐，暂不外卖）。

&lt;p&gt;覆盖 8 张 PG 表的 8 个端点：
&lt;ul&gt;
  &lt;li&gt;{@code POST /openapi/v1/tmt/bo-daily}            — 电影日票房（tmt_bo_daily）&lt;/li&gt;
  &lt;li&gt;{@code POST /openapi/v1/tmt/bo-weekly}           — 电影周票房（tmt_bo_weekly）&lt;/li&gt;
  &lt;li&gt;{@code POST /openapi/v1/tmt/bo-monthly}          — 电影月票房（tmt_bo_monthly）&lt;/li&gt;
  &lt;li&gt;{@code POST /openapi/v1/tmt/bo-cinema}           — 影院日票房（tmt_bo_cinema）&lt;/li&gt;
  &lt;li&gt;{@code POST /openapi/v1/tmt/film-record}         — 全国电影剧本备案（tmt_film_record）&lt;/li&gt;
  &lt;li&gt;{@code POST /openapi/v1/tmt/teleplay-record}     — 全国电视剧备案（tmt_teleplay_record）&lt;/li&gt;
  &lt;li&gt;{@code POST /openapi/v1/tmt/twincome}            — 台湾电子合计营收（tmt_twincome）&lt;/li&gt;
  &lt;li&gt;{@code POST /openapi/v1/tmt/twincome-detail}     — 台湾电子明细营收（tmt_twincome_detail）&lt;/li&gt;
&lt;/ul&gt;

&lt;p&gt;数据来源：Tushare {@code bo_daily} / {@code bo_weekly} / {@code bo_monthly} / {@code bo_cinema}
/ {@code film_record} / {@code teleplay_record} / {@code tmt_twincome} / {@code tmt_twincomedetail}。
### 电影日票房（{@code tmt_bo_daily}）。<br><br>单日电影维度票房榜（含 day_amount / total / list_day / wom_index / up_ratio / rank）。<br>过滤：{@code startDate} / {@code endDate}（YYYYMMDD）+ {@code name} 影片名模糊匹配。<br>排序：date DESC + rank ASC。
**URL:** /openapi/v1/tmt/bo-daily

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 电影日票房（{@code tmt_bo_daily}）。

<p>单日电影维度票房榜（含 day_amount / total / list_day / wom_index / up_ratio / rank）。
<p>过滤：{@code startDate} / {@code endDate}（YYYYMMDD）+ {@code name} 影片名模糊匹配。
<p>排序：date DESC + rank ASC。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|page|int32|false|第几页，从 1 起。默认 1。0 / 负数会被当成 1。|-|
|size|int32|false|每页记录数。默认 50，硬上限 {@value #MAX_SIZE}。<br/><p>传入超过 {@value #MAX_SIZE} 时会被自动截断到 {@value #MAX_SIZE}（不报错）。</p>|-|
|startDate|string|false|起始日期。可空。<br/><p>BO / film-record 用 {@code YYYYMMDD}；twincome / twincome-detail 用 {@code YYYYMM}。|-|
|endDate|string|false|结束日期。可空。同上。|-|
|name|string|false|影片 / 影院 / 剧目名称模糊匹配（BO 端点 + teleplay-record / film-record 用，可空）。|-|
|cName|string|false|影院名称模糊匹配（仅 bo-cinema 端点用，可空，与 name 互斥）。|-|
|recNo|string|false|备案号（仅 film-record 端点用，精确匹配，可空）。|-|
|licenseKey|string|false|许可证号（仅 teleplay-record 端点用，精确匹配，可空）。|-|
|item|string|false|台湾电子产品代码（仅 twincome / twincome-detail 端点用，可空），如 {@code 8001} 合计 / {@code 8002} 子分类。|-|
|symbol|string|false|台湾电子公司代码（仅 twincome-detail 端点用，可空）。|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/tmt/bo-daily?page=0&size=0&endDate=&item=&cName=&name=&symbol=&licenseKey=&startDate=&recNo='
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─date|string|日期|-|
|└─name|string|影片名称|-|
|└─avgPrice|number|平均票价|-|
|└─dayAmount|number|单日票房（万）|-|
|└─total|number|累计票房（万）|-|
|└─listDay|int32|上映天数|-|
|└─pPc|int32|场均人次|-|
|└─womIndex|number|口碑指数|-|
|└─upRatio|number|排片占比|-|
|└─rank|int32|排名|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "date": "yyyy-MM-dd HH:mm:ss",
      "name": "",
      "avgPrice": 0,
      "dayAmount": 0,
      "total": 0,
      "listDay": 0,
      "pPc": 0,
      "womIndex": 0,
      "upRatio": 0,
      "rank": 0
    }
  ],
  "traceId": ""
}
```

### 电影周票房（{@code tmt_bo_weekly}）。<br><br>单周电影维度票房榜（{@code date} = 周一日期），字段同 bo-daily（但 day_amount → week_amount）。
**URL:** /openapi/v1/tmt/bo-weekly

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 电影周票房（{@code tmt_bo_weekly}）。

<p>单周电影维度票房榜（{@code date} = 周一日期），字段同 bo-daily（但 day_amount → week_amount）。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|page|int32|false|第几页，从 1 起。默认 1。0 / 负数会被当成 1。|-|
|size|int32|false|每页记录数。默认 50，硬上限 {@value #MAX_SIZE}。<br/><p>传入超过 {@value #MAX_SIZE} 时会被自动截断到 {@value #MAX_SIZE}（不报错）。</p>|-|
|startDate|string|false|起始日期。可空。<br/><p>BO / film-record 用 {@code YYYYMMDD}；twincome / twincome-detail 用 {@code YYYYMM}。|-|
|endDate|string|false|结束日期。可空。同上。|-|
|name|string|false|影片 / 影院 / 剧目名称模糊匹配（BO 端点 + teleplay-record / film-record 用，可空）。|-|
|cName|string|false|影院名称模糊匹配（仅 bo-cinema 端点用，可空，与 name 互斥）。|-|
|recNo|string|false|备案号（仅 film-record 端点用，精确匹配，可空）。|-|
|licenseKey|string|false|许可证号（仅 teleplay-record 端点用，精确匹配，可空）。|-|
|item|string|false|台湾电子产品代码（仅 twincome / twincome-detail 端点用，可空），如 {@code 8001} 合计 / {@code 8002} 子分类。|-|
|symbol|string|false|台湾电子公司代码（仅 twincome-detail 端点用，可空）。|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/tmt/bo-weekly?page=0&size=0&name=&endDate=&cName=&licenseKey=&item=&startDate=&recNo=&symbol='
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─date|string|日期（周一日期）|-|
|└─name|string|影片名称|-|
|└─avgPrice|number|平均票价|-|
|└─weekAmount|number|周票房（万）|-|
|└─total|number|累计票房（万）|-|
|└─listDay|int32|上映天数|-|
|└─pPc|int32|场均人次|-|
|└─womIndex|number|口碑指数|-|
|└─upRatio|number|排片占比|-|
|└─rank|int32|排名|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "date": "yyyy-MM-dd HH:mm:ss",
      "name": "",
      "avgPrice": 0,
      "weekAmount": 0,
      "total": 0,
      "listDay": 0,
      "pPc": 0,
      "womIndex": 0,
      "upRatio": 0,
      "rank": 0
    }
  ],
  "traceId": ""
}
```

### 电影月票房（{@code tmt_bo_monthly}）。<br><br>单月电影维度票房榜（{@code date} = 月初日期）。<br>含 {@code listDate} 上映日期（原始字符串）和 {@code mRatio} 月度环比。
**URL:** /openapi/v1/tmt/bo-monthly

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 电影月票房（{@code tmt_bo_monthly}）。

<p>单月电影维度票房榜（{@code date} = 月初日期）。
含 {@code listDate} 上映日期（原始字符串）和 {@code mRatio} 月度环比。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|page|int32|false|第几页，从 1 起。默认 1。0 / 负数会被当成 1。|-|
|size|int32|false|每页记录数。默认 50，硬上限 {@value #MAX_SIZE}。<br/><p>传入超过 {@value #MAX_SIZE} 时会被自动截断到 {@value #MAX_SIZE}（不报错）。</p>|-|
|startDate|string|false|起始日期。可空。<br/><p>BO / film-record 用 {@code YYYYMMDD}；twincome / twincome-detail 用 {@code YYYYMM}。|-|
|endDate|string|false|结束日期。可空。同上。|-|
|name|string|false|影片 / 影院 / 剧目名称模糊匹配（BO 端点 + teleplay-record / film-record 用，可空）。|-|
|cName|string|false|影院名称模糊匹配（仅 bo-cinema 端点用，可空，与 name 互斥）。|-|
|recNo|string|false|备案号（仅 film-record 端点用，精确匹配，可空）。|-|
|licenseKey|string|false|许可证号（仅 teleplay-record 端点用，精确匹配，可空）。|-|
|item|string|false|台湾电子产品代码（仅 twincome / twincome-detail 端点用，可空），如 {@code 8001} 合计 / {@code 8002} 子分类。|-|
|symbol|string|false|台湾电子公司代码（仅 twincome-detail 端点用，可空）。|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/tmt/bo-monthly?page=0&size=0&cName=&item=&startDate=&endDate=&licenseKey=&name=&symbol=&recNo='
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─date|string|日期（月初 1 号）|-|
|└─name|string|影片名称|-|
|└─listDate|string|上映日期（原始字符串）|-|
|└─avgPrice|number|平均票价|-|
|└─monthAmount|number|月度票房（万）|-|
|└─listDay|int32|上映天数|-|
|└─pPc|int32|场均人次|-|
|└─womIndex|number|口碑指数|-|
|└─mRatio|number|月度环比|-|
|└─rank|int32|排名|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "date": "yyyy-MM-dd HH:mm:ss",
      "name": "",
      "listDate": "",
      "avgPrice": 0,
      "monthAmount": 0,
      "listDay": 0,
      "pPc": 0,
      "womIndex": 0,
      "mRatio": 0,
      "rank": 0
    }
  ],
  "traceId": ""
}
```

### 影院日票房（{@code tmt_bo_cinema}）。<br><br>单日影院维度票房榜（按影院汇总，含 aud_count 观影人次 / att_ratio 上座率 /<br>day_showcount 排片场次）。单位：元。<br>过滤：{@code startDate} / {@code endDate} + {@code cName} 影院名称模糊匹配。
**URL:** /openapi/v1/tmt/bo-cinema

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 影院日票房（{@code tmt_bo_cinema}）。

<p>单日影院维度票房榜（按影院汇总，含 aud_count 观影人次 / att_ratio 上座率 /
day_showcount 排片场次）。单位：元。
<p>过滤：{@code startDate} / {@code endDate} + {@code cName} 影院名称模糊匹配。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|page|int32|false|第几页，从 1 起。默认 1。0 / 负数会被当成 1。|-|
|size|int32|false|每页记录数。默认 50，硬上限 {@value #MAX_SIZE}。<br/><p>传入超过 {@value #MAX_SIZE} 时会被自动截断到 {@value #MAX_SIZE}（不报错）。</p>|-|
|startDate|string|false|起始日期。可空。<br/><p>BO / film-record 用 {@code YYYYMMDD}；twincome / twincome-detail 用 {@code YYYYMM}。|-|
|endDate|string|false|结束日期。可空。同上。|-|
|name|string|false|影片 / 影院 / 剧目名称模糊匹配（BO 端点 + teleplay-record / film-record 用，可空）。|-|
|cName|string|false|影院名称模糊匹配（仅 bo-cinema 端点用，可空，与 name 互斥）。|-|
|recNo|string|false|备案号（仅 film-record 端点用，精确匹配，可空）。|-|
|licenseKey|string|false|许可证号（仅 teleplay-record 端点用，精确匹配，可空）。|-|
|item|string|false|台湾电子产品代码（仅 twincome / twincome-detail 端点用，可空），如 {@code 8001} 合计 / {@code 8002} 子分类。|-|
|symbol|string|false|台湾电子公司代码（仅 twincome-detail 端点用，可空）。|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/tmt/bo-cinema?page=0&size=0&item=&cName=&name=&endDate=&startDate=&recNo=&symbol=&licenseKey='
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─date|string|日期|-|
|└─cName|string|影院名称|-|
|└─audCount|int32|观影人次|-|
|└─attRatio|number|上座率|-|
|└─dayAmount|number|票房（元）|-|
|└─dayShowcount|number|排片场次|-|
|└─avgPrice|number|平均票价|-|
|└─pPc|number|单场人次|-|
|└─rank|int32|排名|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "date": "yyyy-MM-dd HH:mm:ss",
      "cName": "",
      "audCount": 0,
      "attRatio": 0,
      "dayAmount": 0,
      "dayShowcount": 0,
      "avgPrice": 0,
      "pPc": 0,
      "rank": 0
    }
  ],
  "traceId": ""
}
```

### 全国电影剧本备案（{@code tmt_film_record}）。<br><br>电影年度备案制信息（备案号 / 影片名 / 备案单位 / 编剧 / 备案结果 / 备案地等）。<br>过滤：{@code startDate} / {@code endDate} 公示日期范围（YYYYMMDD）+ {@code recNo} 精确备案号 +<br>{@code name} 影片名模糊匹配。
**URL:** /openapi/v1/tmt/film-record

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 全国电影剧本备案（{@code tmt_film_record}）。

<p>电影年度备案制信息（备案号 / 影片名 / 备案单位 / 编剧 / 备案结果 / 备案地等）。
<p>过滤：{@code startDate} / {@code endDate} 公示日期范围（YYYYMMDD）+ {@code recNo} 精确备案号 +
{@code name} 影片名模糊匹配。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|page|int32|false|第几页，从 1 起。默认 1。0 / 负数会被当成 1。|-|
|size|int32|false|每页记录数。默认 50，硬上限 {@value #MAX_SIZE}。<br/><p>传入超过 {@value #MAX_SIZE} 时会被自动截断到 {@value #MAX_SIZE}（不报错）。</p>|-|
|startDate|string|false|起始日期。可空。<br/><p>BO / film-record 用 {@code YYYYMMDD}；twincome / twincome-detail 用 {@code YYYYMM}。|-|
|endDate|string|false|结束日期。可空。同上。|-|
|name|string|false|影片 / 影院 / 剧目名称模糊匹配（BO 端点 + teleplay-record / film-record 用，可空）。|-|
|cName|string|false|影院名称模糊匹配（仅 bo-cinema 端点用，可空，与 name 互斥）。|-|
|recNo|string|false|备案号（仅 film-record 端点用，精确匹配，可空）。|-|
|licenseKey|string|false|许可证号（仅 teleplay-record 端点用，精确匹配，可空）。|-|
|item|string|false|台湾电子产品代码（仅 twincome / twincome-detail 端点用，可空），如 {@code 8001} 合计 / {@code 8002} 子分类。|-|
|symbol|string|false|台湾电子公司代码（仅 twincome-detail 端点用，可空）。|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/tmt/film-record?page=0&size=0&cName=&licenseKey=&name=&recNo=&startDate=&endDate=&symbol=&item='
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─recNo|string|备案号|-|
|└─filmName|string|影片名|-|
|└─recOrg|string|备案单位|-|
|└─scriptWriter|string|编剧|-|
|└─recResult|string|备案结果|-|
|└─recArea|string|备案地（省）|-|
|└─classified|string|备案类型|-|
|└─dateRange|string|备案期间（原始字符串）|-|
|└─annDate|string|公示日期|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "recNo": "",
      "filmName": "",
      "recOrg": "",
      "scriptWriter": "",
      "recResult": "",
      "recArea": "",
      "classified": "",
      "dateRange": "",
      "annDate": "yyyy-MM-dd HH:mm:ss"
    }
  ],
  "traceId": ""
}
```

### 全国电视剧备案（{@code tmt_teleplay_record}）。<br><br>电视剧备案登记表（许可证号 / 剧目名称 / 题材分类 / 类型 / 制作机构 / 集数 / 拍摄日期等）。<br>所有业务字段为 TEXT，原样保存。<br>过滤：{@code licenseKey} 精确许可证号 + {@code name} 剧目名模糊匹配。
**URL:** /openapi/v1/tmt/teleplay-record

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 全国电视剧备案（{@code tmt_teleplay_record}）。

<p>电视剧备案登记表（许可证号 / 剧目名称 / 题材分类 / 类型 / 制作机构 / 集数 / 拍摄日期等）。
所有业务字段为 TEXT，原样保存。
<p>过滤：{@code licenseKey} 精确许可证号 + {@code name} 剧目名模糊匹配。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|page|int32|false|第几页，从 1 起。默认 1。0 / 负数会被当成 1。|-|
|size|int32|false|每页记录数。默认 50，硬上限 {@value #MAX_SIZE}。<br/><p>传入超过 {@value #MAX_SIZE} 时会被自动截断到 {@value #MAX_SIZE}（不报错）。</p>|-|
|startDate|string|false|起始日期。可空。<br/><p>BO / film-record 用 {@code YYYYMMDD}；twincome / twincome-detail 用 {@code YYYYMM}。|-|
|endDate|string|false|结束日期。可空。同上。|-|
|name|string|false|影片 / 影院 / 剧目名称模糊匹配（BO 端点 + teleplay-record / film-record 用，可空）。|-|
|cName|string|false|影院名称模糊匹配（仅 bo-cinema 端点用，可空，与 name 互斥）。|-|
|recNo|string|false|备案号（仅 film-record 端点用，精确匹配，可空）。|-|
|licenseKey|string|false|许可证号（仅 teleplay-record 端点用，精确匹配，可空）。|-|
|item|string|false|台湾电子产品代码（仅 twincome / twincome-detail 端点用，可空），如 {@code 8001} 合计 / {@code 8002} 子分类。|-|
|symbol|string|false|台湾电子公司代码（仅 twincome-detail 端点用，可空）。|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/tmt/teleplay-record?page=0&size=0&licenseKey=&startDate=&endDate=&name=&item=&cName=&symbol=&recNo='
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─licenseKey|string|许可证号（UK）|-|
|└─name|string|剧目名称|-|
|└─classify|string|题材分类|-|
|└─types|string|类型|-|
|└─org|string|制作机构|-|
|└─reportDate|string|备案月份（原始字符串）|-|
|└─episodes|string|集数|-|
|└─shootingDate|string|拍摄日期|-|
|└─prodCycle|string|制作周期|-|
|└─content|string|内容提要|-|
|└─proOpi|string|省局意见|-|
|└─deptOpi|string|总局意见|-|
|└─remarks|string|备注|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "licenseKey": "",
      "name": "",
      "classify": "",
      "types": "",
      "org": "",
      "reportDate": "",
      "episodes": "",
      "shootingDate": "",
      "prodCycle": "",
      "content": "",
      "proOpi": "",
      "deptOpi": "",
      "remarks": ""
    }
  ],
  "traceId": ""
}
```

### 台湾电子产品月营收合计（{@code tmt_twincome}）。<br><br>台湾电子产品分类营收月度数据，{@code date} 格式 {@code YYYYMM}（VARCHAR 字符串比较）。<br>{@code item} 为产品代码（{@code 8001} 合计 / {@code 8002} 子分类等）。
**URL:** /openapi/v1/tmt/twincome

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 台湾电子产品月营收合计（{@code tmt_twincome}）。

<p>台湾电子产品分类营收月度数据，{@code date} 格式 {@code YYYYMM}（VARCHAR 字符串比较）。
{@code item} 为产品代码（{@code 8001} 合计 / {@code 8002} 子分类等）。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|page|int32|false|第几页，从 1 起。默认 1。0 / 负数会被当成 1。|-|
|size|int32|false|每页记录数。默认 50，硬上限 {@value #MAX_SIZE}。<br/><p>传入超过 {@value #MAX_SIZE} 时会被自动截断到 {@value #MAX_SIZE}（不报错）。</p>|-|
|startDate|string|false|起始日期。可空。<br/><p>BO / film-record 用 {@code YYYYMMDD}；twincome / twincome-detail 用 {@code YYYYMM}。|-|
|endDate|string|false|结束日期。可空。同上。|-|
|name|string|false|影片 / 影院 / 剧目名称模糊匹配（BO 端点 + teleplay-record / film-record 用，可空）。|-|
|cName|string|false|影院名称模糊匹配（仅 bo-cinema 端点用，可空，与 name 互斥）。|-|
|recNo|string|false|备案号（仅 film-record 端点用，精确匹配，可空）。|-|
|licenseKey|string|false|许可证号（仅 teleplay-record 端点用，精确匹配，可空）。|-|
|item|string|false|台湾电子产品代码（仅 twincome / twincome-detail 端点用，可空），如 {@code 8001} 合计 / {@code 8002} 子分类。|-|
|symbol|string|false|台湾电子公司代码（仅 twincome-detail 端点用，可空）。|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/tmt/twincome?page=0&size=0&item=&name=&licenseKey=&endDate=&symbol=&startDate=&cName=&recNo='
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─date|string|报告期 YYYYMM|-|
|└─item|string|产品代码（8001/8002 等）|-|
|└─opIncome|string|营业收入|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "date": "",
      "item": "",
      "opIncome": ""
    }
  ],
  "traceId": ""
}
```

### 台湾电子月营收明细（{@code tmt_twincome_detail}）。<br><br>细化到公司代码 {@code symbol} 的月度营收 + 合并营业收入。<br>{@code date} 格式 {@code YYYYMM}。
**URL:** /openapi/v1/tmt/twincome-detail

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 台湾电子月营收明细（{@code tmt_twincome_detail}）。

<p>细化到公司代码 {@code symbol} 的月度营收 + 合并营业收入。
{@code date} 格式 {@code YYYYMM}。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|page|int32|false|第几页，从 1 起。默认 1。0 / 负数会被当成 1。|-|
|size|int32|false|每页记录数。默认 50，硬上限 {@value #MAX_SIZE}。<br/><p>传入超过 {@value #MAX_SIZE} 时会被自动截断到 {@value #MAX_SIZE}（不报错）。</p>|-|
|startDate|string|false|起始日期。可空。<br/><p>BO / film-record 用 {@code YYYYMMDD}；twincome / twincome-detail 用 {@code YYYYMM}。|-|
|endDate|string|false|结束日期。可空。同上。|-|
|name|string|false|影片 / 影院 / 剧目名称模糊匹配（BO 端点 + teleplay-record / film-record 用，可空）。|-|
|cName|string|false|影院名称模糊匹配（仅 bo-cinema 端点用，可空，与 name 互斥）。|-|
|recNo|string|false|备案号（仅 film-record 端点用，精确匹配，可空）。|-|
|licenseKey|string|false|许可证号（仅 teleplay-record 端点用，精确匹配，可空）。|-|
|item|string|false|台湾电子产品代码（仅 twincome / twincome-detail 端点用，可空），如 {@code 8001} 合计 / {@code 8002} 子分类。|-|
|symbol|string|false|台湾电子公司代码（仅 twincome-detail 端点用，可空）。|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/tmt/twincome-detail?page=0&size=0&symbol=&endDate=&name=&recNo=&startDate=&licenseKey=&cName=&item='
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─date|string|报告期 YYYYMM|-|
|└─item|string|产品代码|-|
|└─symbol|string|公司代码|-|
|└─opIncome|string|营业收入|-|
|└─consopIncome|string|合并营业收入|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "date": "",
      "item": "",
      "symbol": "",
      "opIncome": "",
      "consopIncome": ""
    }
  ],
  "traceId": ""
}
```

## OpenAPI v1 —— 财务报表深度端点（stock.financial scope）。

&lt;p&gt;覆盖 7 张 PG 表的 7 个端点，从三大报表到分业务/回购/质押。
全部 &lt;code&gt;@OpenApiScope(&quot;stock.financial&quot;)&lt;/code&gt;，套餐 Plus 及以上。

&lt;p&gt;与 &lt;code&gt;/stock/api/detail/coreFinancials&lt;/code&gt;（仅核心摘要 26 列）
和 &lt;code&gt;/stock/api/stock/stockRoeList&lt;/code&gt;（仅 ROE 历史）配套，
此 controller 暴露的是更深度的报表数据。
### 利润表（22 列）：基本/稀释 EPS + 收入 + 三项费用 + 研发 + 营业利润 + 净利润 + EBIT/EBITDA。<br>报告类型 reportType 可选：1 合并报表（默认推荐）/ 2 母公司 / 3 调整合并 / etc。
**URL:** /openapi/v1/stock/financial/income-statement

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 利润表（22 列）：基本/稀释 EPS + 收入 + 三项费用 + 研发 + 营业利润 + 净利润 + EBIT/EBITDA。
报告类型 reportType 可选：1 合并报表（默认推荐）/ 2 母公司 / 3 调整合并 / etc。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|page|int32|false|第几页，从 1 起。默认 1。0 / 负数会被当成 1。|-|
|size|int32|false|每页记录数。默认 50，硬上限 {@value #MAX_SIZE}。<br/><p>传入超过 {@value #MAX_SIZE} 时会被自动截断到 {@value #MAX_SIZE}（不报错）。</p>|-|
|tsCode|string|false|股票代码（带交易所后缀），如 {@code "600519.SH"}。<b>必填</b>。|-|
|startDate|string|false|起始报告期，格式 {@code YYYYMMDD}（季末日，如 {@code "20240331"}）。可空。<br/><p>不传时由 page/size 决定窗口（最近 N 期往前）。</p>|-|
|endDate|string|false|结束报告期，格式 {@code YYYYMMDD}。可空。不传时取最新报告期。|-|
|reportType|string|false|报告类型。<br/><br/><ul><br/>  <li>{@code "1"} —— 合并报表（默认 / 推荐，多数研究场景）</li><br/>  <li>{@code "2"} —— 母公司报表</li><br/>  <li>{@code "3"} —— 调整合并报表</li><br/>  <li>{@code "4"} —— 调整母公司报表</li><br/>  <li>...更多详见 Tushare 字典</li><br/></ul><br/><br/><p>可空 = 不限报表类型（同一报告期可能多行）。LLM 一般传 {@code "1"}。</p>|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/stock/financial/income-statement?page=0&size=0&tsCode=&startDate=&endDate=&reportType='
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─tsCode|string|No comments found.|-|
|└─annDate|string|公告日期|-|
|└─endDate|string|报告期（季末）|-|
|└─reportType|string|报告类型：1 合并 / 2 母公司 / etc.|-|
|└─basicEps|number|No comments found.|-|
|└─dilutedEps|number|No comments found.|-|
|└─totalRevenue|number|营业总收入|-|
|└─revenue|number|营业收入|-|
|└─totalCogs|number|营业总成本|-|
|└─operCost|number|营业成本|-|
|└─bizTaxSurchg|number|营业税金及附加|-|
|└─sellExp|number|销售费用|-|
|└─adminExp|number|管理费用|-|
|└─finExp|number|财务费用|-|
|└─rdExp|number|研发费用|-|
|└─operateProfit|number|营业利润|-|
|└─investIncome|number|投资收益|-|
|└─fvValueChgGain|number|公允价值变动收益|-|
|└─nonOperIncome|number|营业外收入|-|
|└─nonOperExp|number|营业外支出|-|
|└─totalProfit|number|利润总额|-|
|└─nIncome|number|净利润|-|
|└─nIncomeAttrP|number|归母净利润|-|
|└─ebit|number|EBIT|-|
|└─ebitda|number|EBITDA|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "tsCode": "",
      "annDate": "yyyy-MM-dd HH:mm:ss",
      "endDate": "yyyy-MM-dd HH:mm:ss",
      "reportType": "",
      "basicEps": 0,
      "dilutedEps": 0,
      "totalRevenue": 0,
      "revenue": 0,
      "totalCogs": 0,
      "operCost": 0,
      "bizTaxSurchg": 0,
      "sellExp": 0,
      "adminExp": 0,
      "finExp": 0,
      "rdExp": 0,
      "operateProfit": 0,
      "investIncome": 0,
      "fvValueChgGain": 0,
      "nonOperIncome": 0,
      "nonOperExp": 0,
      "totalProfit": 0,
      "nIncome": 0,
      "nIncomeAttrP": 0,
      "ebit": 0,
      "ebitda": 0
    }
  ],
  "traceId": ""
}
```

### 资产负债表（28 列）：流动资产 / 非流动资产 / 总资产 / 流动负债 / 非流动负债 / 总负债 /<br>股本 / 公积金 / 未分配利润 / 股东权益。
**URL:** /openapi/v1/stock/financial/balance-sheet

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 资产负债表（28 列）：流动资产 / 非流动资产 / 总资产 / 流动负债 / 非流动负债 / 总负债 /
股本 / 公积金 / 未分配利润 / 股东权益。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|page|int32|false|第几页，从 1 起。默认 1。0 / 负数会被当成 1。|-|
|size|int32|false|每页记录数。默认 50，硬上限 {@value #MAX_SIZE}。<br/><p>传入超过 {@value #MAX_SIZE} 时会被自动截断到 {@value #MAX_SIZE}（不报错）。</p>|-|
|tsCode|string|false|股票代码（带交易所后缀），如 {@code "600519.SH"}。<b>必填</b>。|-|
|startDate|string|false|起始报告期，格式 {@code YYYYMMDD}（季末日，如 {@code "20240331"}）。可空。<br/><p>不传时由 page/size 决定窗口（最近 N 期往前）。</p>|-|
|endDate|string|false|结束报告期，格式 {@code YYYYMMDD}。可空。不传时取最新报告期。|-|
|reportType|string|false|报告类型。<br/><br/><ul><br/>  <li>{@code "1"} —— 合并报表（默认 / 推荐，多数研究场景）</li><br/>  <li>{@code "2"} —— 母公司报表</li><br/>  <li>{@code "3"} —— 调整合并报表</li><br/>  <li>{@code "4"} —— 调整母公司报表</li><br/>  <li>...更多详见 Tushare 字典</li><br/></ul><br/><br/><p>可空 = 不限报表类型（同一报告期可能多行）。LLM 一般传 {@code "1"}。</p>|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/stock/financial/balance-sheet?page=0&size=0&endDate=&startDate=&reportType=&tsCode='
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─tsCode|string|No comments found.|-|
|└─annDate|string|No comments found.|-|
|└─endDate|string|No comments found.|-|
|└─reportType|string|No comments found.|-|
|└─moneyCap|number|货币资金|-|
|└─tradAsset|number|交易性金融资产|-|
|└─notesReceiv|number|应收票据|-|
|└─accountsReceiv|number|应收账款|-|
|└─inventories|number|存货|-|
|└─totalCurAssets|number|流动资产合计|-|
|└─fixAssets|number|固定资产|-|
|└─intanAssets|number|无形资产|-|
|└─goodwill|number|商誉|-|
|└─totalNca|number|非流动资产合计|-|
|└─totalAssets|number|资产总计|-|
|└─stBorr|number|短期借款|-|
|└─notesPayable|number|应付票据|-|
|└─acctPayable|number|应付账款|-|
|└─payrollPayable|number|应付职工薪酬|-|
|└─taxesPayable|number|应交税费|-|
|└─totalCurLiab|number|流动负债合计|-|
|└─ltBorr|number|长期借款|-|
|└─bondPayable|number|应付债券|-|
|└─totalLiab|number|负债合计|-|
|└─totalShare|number|股本|-|
|└─capRese|number|资本公积|-|
|└─surplusRese|number|盈余公积|-|
|└─undistrPorfit|number|未分配利润|-|
|└─totalHldrEqyExcMinInt|number|归母股东权益|-|
|└─totalHldrEqyIncMinInt|number|股东权益合计（含少数股东）|-|
|└─totalLiabHldrEqy|number|负债 + 所有者权益（验证表平衡）|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "tsCode": "",
      "annDate": "yyyy-MM-dd HH:mm:ss",
      "endDate": "yyyy-MM-dd HH:mm:ss",
      "reportType": "",
      "moneyCap": 0,
      "tradAsset": 0,
      "notesReceiv": 0,
      "accountsReceiv": 0,
      "inventories": 0,
      "totalCurAssets": 0,
      "fixAssets": 0,
      "intanAssets": 0,
      "goodwill": 0,
      "totalNca": 0,
      "totalAssets": 0,
      "stBorr": 0,
      "notesPayable": 0,
      "acctPayable": 0,
      "payrollPayable": 0,
      "taxesPayable": 0,
      "totalCurLiab": 0,
      "ltBorr": 0,
      "bondPayable": 0,
      "totalLiab": 0,
      "totalShare": 0,
      "capRese": 0,
      "surplusRese": 0,
      "undistrPorfit": 0,
      "totalHldrEqyExcMinInt": 0,
      "totalHldrEqyIncMinInt": 0,
      "totalLiabHldrEqy": 0
    }
  ],
  "traceId": ""
}
```

### 现金流量表（20 列）：经营 / 投资 / 筹资 三大活动现金流 + 期初 / 期末现金 + 自由现金流。
**URL:** /openapi/v1/stock/financial/cash-flow

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 现金流量表（20 列）：经营 / 投资 / 筹资 三大活动现金流 + 期初 / 期末现金 + 自由现金流。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|page|int32|false|第几页，从 1 起。默认 1。0 / 负数会被当成 1。|-|
|size|int32|false|每页记录数。默认 50，硬上限 {@value #MAX_SIZE}。<br/><p>传入超过 {@value #MAX_SIZE} 时会被自动截断到 {@value #MAX_SIZE}（不报错）。</p>|-|
|tsCode|string|false|股票代码（带交易所后缀），如 {@code "600519.SH"}。<b>必填</b>。|-|
|startDate|string|false|起始报告期，格式 {@code YYYYMMDD}（季末日，如 {@code "20240331"}）。可空。<br/><p>不传时由 page/size 决定窗口（最近 N 期往前）。</p>|-|
|endDate|string|false|结束报告期，格式 {@code YYYYMMDD}。可空。不传时取最新报告期。|-|
|reportType|string|false|报告类型。<br/><br/><ul><br/>  <li>{@code "1"} —— 合并报表（默认 / 推荐，多数研究场景）</li><br/>  <li>{@code "2"} —— 母公司报表</li><br/>  <li>{@code "3"} —— 调整合并报表</li><br/>  <li>{@code "4"} —— 调整母公司报表</li><br/>  <li>...更多详见 Tushare 字典</li><br/></ul><br/><br/><p>可空 = 不限报表类型（同一报告期可能多行）。LLM 一般传 {@code "1"}。</p>|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/stock/financial/cash-flow?page=0&size=0&startDate=&endDate=&reportType=&tsCode='
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─tsCode|string|股票代码（带交易所后缀），如 {@code "600519.SH"}。|-|
|└─annDate|string|公告日期。|-|
|└─endDate|string|报告期截止日（季末日，如 {@code 2026-03-31}）。|-|
|└─reportType|string|报告类型：{@code "1"} 合并 / {@code "2"} 母公司 / etc.（详见 {@code StockFinancialForm.reportType}）。|-|
|└─cFrSaleSg|number|销售商品、提供劳务收到的现金（元）。经营活动现金流入主项。|-|
|└─cPaidGoodsS|number|购买商品、接受劳务支付的现金（元）。经营活动现金流出主项。|-|
|└─cPaidToForEmpl|number|支付给职工以及为职工支付的现金（元）。|-|
|└─cPaidForTaxes|number|支付的各项税费（元）。|-|
|└─nCashflowAct|number|经营活动产生的现金流量净额（元）。<br/><p>{@code > 0} 主营造血能力强；{@code < 0} 经营性失血需警惕。</p>|-|
|└─cPayAcqConstFiolta|number|购建固定资产、无形资产和其他长期资产支付的现金（CapEx，元）。|-|
|└─cRecpReturnInvest|number|收回投资收到的现金（元）。|-|
|└─cPaidInvest|number|投资支付的现金（元）。|-|
|└─nCashflowInvAct|number|投资活动产生的现金流量净额（元）。<br/><p>成长期公司一般为负（持续投入扩张），成熟期可能转正。</p>|-|
|└─cRecpBorrow|number|取得借款收到的现金（元）。|-|
|└─cRecpCapContrib|number|吸收投资收到的现金（增发 / 配股，元）。|-|
|└─cPayDistDpcpIntExp|number|分配股利、利润或偿付利息支付的现金（元）。|-|
|└─nCashFlowsFncAct|number|筹资活动产生的现金流量净额（元）。<br/><p>融资型 vs 还债型 → 正负反映融资节奏。</p>|-|
|└─cCashEquBegPeriod|number|期初现金及现金等价物余额（元）。|-|
|└─cCashEquEndPeriod|number|期末现金及现金等价物余额（元）。三大活动净额之和反映在此。|-|
|└─freeCashflow|number|自由现金流（FCF，元）= 经营活动现金流净额 − CapEx。<br/><p>衡量公司分红 / 还债 / 再投资的真实弹性。FCF 持续为正且增长 = 高质量成长。</p>|-|
|└─provDeprAssets|number|固定资产折旧、油气资产折耗、生产性生物资产折旧（元）。会计上记账，无现金流出。|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "tsCode": "",
      "annDate": "yyyy-MM-dd HH:mm:ss",
      "endDate": "yyyy-MM-dd HH:mm:ss",
      "reportType": "",
      "cFrSaleSg": 0,
      "cPaidGoodsS": 0,
      "cPaidToForEmpl": 0,
      "cPaidForTaxes": 0,
      "nCashflowAct": 0,
      "cPayAcqConstFiolta": 0,
      "cRecpReturnInvest": 0,
      "cPaidInvest": 0,
      "nCashflowInvAct": 0,
      "cRecpBorrow": 0,
      "cRecpCapContrib": 0,
      "cPayDistDpcpIntExp": 0,
      "nCashFlowsFncAct": 0,
      "cCashEquBegPeriod": 0,
      "cCashEquEndPeriod": 0,
      "freeCashflow": 0,
      "provDeprAssets": 0
    }
  ],
  "traceId": ""
}
```

### 综合财务指标（26 列）：每股 / 盈利能力 / 现金流质量 / 增长 / 单季度。<br>与 stock.indicator 的&amp;quot;估值快照&amp;quot;区分（那个是 PE/PB/换手）。
**URL:** /openapi/v1/stock/financial/indicator

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 综合财务指标（26 列）：每股 / 盈利能力 / 现金流质量 / 增长 / 单季度。
与 stock.indicator 的"估值快照"区分（那个是 PE/PB/换手）。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|page|int32|false|第几页，从 1 起。默认 1。0 / 负数会被当成 1。|-|
|size|int32|false|每页记录数。默认 50，硬上限 {@value #MAX_SIZE}。<br/><p>传入超过 {@value #MAX_SIZE} 时会被自动截断到 {@value #MAX_SIZE}（不报错）。</p>|-|
|tsCode|string|false|股票代码（带交易所后缀），如 {@code "600519.SH"}。<b>必填</b>。|-|
|startDate|string|false|起始报告期，格式 {@code YYYYMMDD}（季末日，如 {@code "20240331"}）。可空。<br/><p>不传时由 page/size 决定窗口（最近 N 期往前）。</p>|-|
|endDate|string|false|结束报告期，格式 {@code YYYYMMDD}。可空。不传时取最新报告期。|-|
|reportType|string|false|报告类型。<br/><br/><ul><br/>  <li>{@code "1"} —— 合并报表（默认 / 推荐，多数研究场景）</li><br/>  <li>{@code "2"} —— 母公司报表</li><br/>  <li>{@code "3"} —— 调整合并报表</li><br/>  <li>{@code "4"} —— 调整母公司报表</li><br/>  <li>...更多详见 Tushare 字典</li><br/></ul><br/><br/><p>可空 = 不限报表类型（同一报告期可能多行）。LLM 一般传 {@code "1"}。</p>|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/stock/financial/indicator?page=0&size=0&tsCode=&endDate=&startDate=&reportType='
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─tsCode|string|No comments found.|-|
|└─annDate|string|No comments found.|-|
|└─endDate|string|No comments found.|-|
|└─eps|number|No comments found.|-|
|└─bps|number|No comments found.|-|
|└─ocfps|number|每股经营现金流|-|
|└─roe|number|No comments found.|-|
|└─roa|number|No comments found.|-|
|└─roic|number|No comments found.|-|
|└─grossprofitMargin|number|毛利率 %|-|
|└─netprofitMargin|number|净利率 %|-|
|└─ocfToOr|number|经营现金流 / 营业收入|-|
|└─ocfToProfit|number|经营现金流 / 净利润|-|
|└─ocfToDebt|number|经营现金流 / 总负债|-|
|└─ocfToShortdebt|number|经营现金流 / 流动负债|-|
|└─fcff|number|企业自由现金流|-|
|└─fcfe|number|股权自由现金流|-|
|└─basicEpsYoy|number|基本 EPS 同比增速 %|-|
|└─netprofitYoy|number|净利润同比 %|-|
|└─dtNetprofitYoy|number|扣非净利润同比 %|-|
|└─trYoy|number|营业总收入同比 %|-|
|└─orYoy|number|营业收入同比 %|-|
|└─qEps|number|单季度 EPS|-|
|└─qRoe|number|单季度 ROE|-|
|└─qNetprofitMargin|number|单季度净利率|-|
|└─qNetprofitYoy|number|单季度净利同比|-|
|└─qOcfToOr|number|单季度经营现金流 / 营业收入|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "tsCode": "",
      "annDate": "yyyy-MM-dd HH:mm:ss",
      "endDate": "yyyy-MM-dd HH:mm:ss",
      "eps": 0,
      "bps": 0,
      "ocfps": 0,
      "roe": 0,
      "roa": 0,
      "roic": 0,
      "grossprofitMargin": 0,
      "netprofitMargin": 0,
      "ocfToOr": 0,
      "ocfToProfit": 0,
      "ocfToDebt": 0,
      "ocfToShortdebt": 0,
      "fcff": 0,
      "fcfe": 0,
      "basicEpsYoy": 0,
      "netprofitYoy": 0,
      "dtNetprofitYoy": 0,
      "trYoy": 0,
      "orYoy": 0,
      "qEps": 0,
      "qRoe": 0,
      "qNetprofitMargin": 0,
      "qNetprofitYoy": 0,
      "qOcfToOr": 0
    }
  ],
  "traceId": ""
}
```

### 分业务营收（按报告期切片，每个业务一行）。<br>适合分析&amp;quot;主营业务集中度 / 多业务转型趋势&amp;quot;。
**URL:** /openapi/v1/stock/financial/business-segment

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 分业务营收（按报告期切片，每个业务一行）。
适合分析"主营业务集中度 / 多业务转型趋势"。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|page|int32|false|第几页，从 1 起。默认 1。0 / 负数会被当成 1。|-|
|size|int32|false|每页记录数。默认 50，硬上限 {@value #MAX_SIZE}。<br/><p>传入超过 {@value #MAX_SIZE} 时会被自动截断到 {@value #MAX_SIZE}（不报错）。</p>|-|
|tsCode|string|false|股票代码（带交易所后缀），如 {@code "600519.SH"}。<b>必填</b>。|-|
|startDate|string|false|起始报告期，格式 {@code YYYYMMDD}（季末日，如 {@code "20240331"}）。可空。<br/><p>不传时由 page/size 决定窗口（最近 N 期往前）。</p>|-|
|endDate|string|false|结束报告期，格式 {@code YYYYMMDD}。可空。不传时取最新报告期。|-|
|reportType|string|false|报告类型。<br/><br/><ul><br/>  <li>{@code "1"} —— 合并报表（默认 / 推荐，多数研究场景）</li><br/>  <li>{@code "2"} —— 母公司报表</li><br/>  <li>{@code "3"} —— 调整合并报表</li><br/>  <li>{@code "4"} —— 调整母公司报表</li><br/>  <li>...更多详见 Tushare 字典</li><br/></ul><br/><br/><p>可空 = 不限报表类型（同一报告期可能多行）。LLM 一般传 {@code "1"}。</p>|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/stock/financial/business-segment?page=0&size=0&reportType=&tsCode=&endDate=&startDate='
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─tsCode|string|No comments found.|-|
|└─endDate|string|报告期 YYYYMMDD|-|
|└─bzItem|string|业务名称|-|
|└─bzCode|string|业务代码|-|
|└─bzSales|number|业务收入|-|
|└─bzProfit|number|业务利润|-|
|└─bzCost|number|业务成本|-|
|└─currType|string|货币类型|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "tsCode": "",
      "endDate": "",
      "bzItem": "",
      "bzCode": "",
      "bzSales": 0,
      "bzProfit": 0,
      "bzCost": 0,
      "currType": ""
    }
  ],
  "traceId": ""
}
```

### 股票回购记录（按公告日倒序）。<br>字段含 vol / amount / high_limit / low_limit / proc 进度。
**URL:** /openapi/v1/stock/financial/repurchase

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 股票回购记录（按公告日倒序）。
字段含 vol / amount / high_limit / low_limit / proc 进度。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|page|int32|false|第几页，从 1 起。默认 1。0 / 负数会被当成 1。|-|
|size|int32|false|每页记录数。默认 50，硬上限 {@value #MAX_SIZE}。<br/><p>传入超过 {@value #MAX_SIZE} 时会被自动截断到 {@value #MAX_SIZE}（不报错）。</p>|-|
|tsCode|string|false|股票代码（带交易所后缀），如 {@code "600519.SH"}。<b>必填</b>。|-|
|startDate|string|false|起始报告期，格式 {@code YYYYMMDD}（季末日，如 {@code "20240331"}）。可空。<br/><p>不传时由 page/size 决定窗口（最近 N 期往前）。</p>|-|
|endDate|string|false|结束报告期，格式 {@code YYYYMMDD}。可空。不传时取最新报告期。|-|
|reportType|string|false|报告类型。<br/><br/><ul><br/>  <li>{@code "1"} —— 合并报表（默认 / 推荐，多数研究场景）</li><br/>  <li>{@code "2"} —— 母公司报表</li><br/>  <li>{@code "3"} —— 调整合并报表</li><br/>  <li>{@code "4"} —— 调整母公司报表</li><br/>  <li>...更多详见 Tushare 字典</li><br/></ul><br/><br/><p>可空 = 不限报表类型（同一报告期可能多行）。LLM 一般传 {@code "1"}。</p>|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/stock/financial/repurchase?page=0&size=0&startDate=&reportType=&endDate=&tsCode='
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─tsCode|string|No comments found.|-|
|└─annDate|string|公告日期|-|
|└─endDate|string|报告期|-|
|└─proc|string|进度（如 "实施"、"完成"、"预案"）|-|
|└─expDate|string|过期日期|-|
|└─vol|number|回购数量（股）|-|
|└─amount|number|回购金额（元）|-|
|└─highLimit|number|回购价格上限|-|
|└─lowLimit|number|回购价格下限|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "tsCode": "",
      "annDate": "yyyy-MM-dd HH:mm:ss",
      "endDate": "yyyy-MM-dd HH:mm:ss",
      "proc": "",
      "expDate": "yyyy-MM-dd HH:mm:ss",
      "vol": 0,
      "amount": 0,
      "highLimit": 0,
      "lowLimit": 0
    }
  ],
  "traceId": ""
}
```

### 股权质押统计（pledge_ratio 高 → 平仓风险，重要风控信号）。
**URL:** /openapi/v1/stock/financial/pledge

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 股权质押统计（pledge_ratio 高 → 平仓风险，重要风控信号）。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|page|int32|false|第几页，从 1 起。默认 1。0 / 负数会被当成 1。|-|
|size|int32|false|每页记录数。默认 50，硬上限 {@value #MAX_SIZE}。<br/><p>传入超过 {@value #MAX_SIZE} 时会被自动截断到 {@value #MAX_SIZE}（不报错）。</p>|-|
|tsCode|string|false|股票代码（带交易所后缀），如 {@code "600519.SH"}。<b>必填</b>。|-|
|startDate|string|false|起始报告期，格式 {@code YYYYMMDD}（季末日，如 {@code "20240331"}）。可空。<br/><p>不传时由 page/size 决定窗口（最近 N 期往前）。</p>|-|
|endDate|string|false|结束报告期，格式 {@code YYYYMMDD}。可空。不传时取最新报告期。|-|
|reportType|string|false|报告类型。<br/><br/><ul><br/>  <li>{@code "1"} —— 合并报表（默认 / 推荐，多数研究场景）</li><br/>  <li>{@code "2"} —— 母公司报表</li><br/>  <li>{@code "3"} —— 调整合并报表</li><br/>  <li>{@code "4"} —— 调整母公司报表</li><br/>  <li>...更多详见 Tushare 字典</li><br/></ul><br/><br/><p>可空 = 不限报表类型（同一报告期可能多行）。LLM 一般传 {@code "1"}。</p>|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/stock/financial/pledge?page=0&size=0&tsCode=&startDate=&reportType=&endDate='
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─tsCode|string|No comments found.|-|
|└─endDate|string|截止日期 YYYYMMDD|-|
|└─pledgeCount|int32|质押次数|-|
|└─unrestPledge|number|无限售股质押（万股）|-|
|└─restPledge|number|限售股质押（万股）|-|
|└─totalShare|number|总股本（万股）|-|
|└─pledgeRatio|number|质押比例（%）|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "tsCode": "",
      "endDate": "",
      "pledgeCount": 0,
      "unrestPledge": 0,
      "restPledge": 0,
      "totalShare": 0,
      "pledgeRatio": 0
    }
  ],
  "traceId": ""
}
```

### 核心财务数据精简版（最近 N 期，仅 26 列摘要：EPS/BPS/ROE/毛利/净利等核心指标）。<br>与 indicator 端点的全 341 列不同，这是给&amp;quot;快速概览&amp;quot;场景用的。<br><br>对应 site internal: &lt;code&gt;POST /stock/api/detail/coreFinancials&lt;/code&gt;。
**URL:** /openapi/v1/stock/financial/core

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 核心财务数据精简版（最近 N 期，仅 26 列摘要：EPS/BPS/ROE/毛利/净利等核心指标）。
与 indicator 端点的全 341 列不同，这是给"快速概览"场景用的。

<p>对应 site internal: <code>POST /stock/api/detail/coreFinancials</code>。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|page|int32|false|第几页，从 1 起。默认 1。0 / 负数会被当成 1。|-|
|size|int32|false|每页记录数。默认 50，硬上限 {@value #MAX_SIZE}。<br/><p>传入超过 {@value #MAX_SIZE} 时会被自动截断到 {@value #MAX_SIZE}（不报错）。</p>|-|
|tsCode|string|false|股票代码（带交易所后缀），如 {@code "600519.SH"}。<b>必填</b>。|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/stock/financial/core?page=0&size=0&tsCode='
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─tsCode|string|No comments found.|-|
|└─endDate|string|报告期 yyyyMMdd|-|
|└─eps|number|基本每股收益|-|
|└─dtEps|number|稀释每股收益|-|
|└─bps|number|每股净资产|-|
|└─ocfps|number|每股经营现金流|-|
|└─roe|number|ROE(%)|-|
|└─roeDt|number|扣非ROE(%)|-|
|└─roa|number|ROA(%)|-|
|└─grossprofitMargin|number|毛利率(%)|-|
|└─netprofitMargin|number|净利率(%)|-|
|└─revenueYoy|number|营收同比(%)|-|
|└─netprofitYoy|number|净利同比(%)|-|
|└─dtNetprofitYoy|number|扣非净利同比(%)|-|
|└─currentRatio|number|流动比率|-|
|└─quickRatio|number|速动比率|-|
|└─debtToAssets|number|资产负债率(%)|-|
|└─assetsTurn|number|总资产周转率|-|
|└─arTurn|number|应收账款周转率|-|
|└─ocfToOr|number|经营现金流/营收比|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "tsCode": "",
      "endDate": "",
      "eps": 0,
      "dtEps": 0,
      "bps": 0,
      "ocfps": 0,
      "roe": 0,
      "roeDt": 0,
      "roa": 0,
      "grossprofitMargin": 0,
      "netprofitMargin": 0,
      "revenueYoy": 0,
      "netprofitYoy": 0,
      "dtNetprofitYoy": 0,
      "currentRatio": 0,
      "quickRatio": 0,
      "debtToAssets": 0,
      "assetsTurn": 0,
      "arTurn": 0,
      "ocfToOr": 0
    }
  ],
  "traceId": ""
}
```

### 分红派息历史（送股 / 转股 / 现金分红 / 除权除息日 / 分红税）。<br><br>对应 site internal: &lt;code&gt;POST /stock/api/detail/dividendList&lt;/code&gt;。
**URL:** /openapi/v1/stock/financial/dividend

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 分红派息历史（送股 / 转股 / 现金分红 / 除权除息日 / 分红税）。

<p>对应 site internal: <code>POST /stock/api/detail/dividendList</code>。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|page|int32|false|第几页，从 1 起。默认 1。0 / 负数会被当成 1。|-|
|size|int32|false|每页记录数。默认 50，硬上限 {@value #MAX_SIZE}。<br/><p>传入超过 {@value #MAX_SIZE} 时会被自动截断到 {@value #MAX_SIZE}（不报错）。</p>|-|
|tsCode|string|false|股票代码（带交易所后缀），如 {@code "600519.SH"}。<b>必填</b>。|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/stock/financial/dividend?page=0&size=0&tsCode='
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─tsCode|string|No comments found.|-|
|└─endDate|string|分红年度 yyyyMMdd|-|
|└─annDate|string|公告日期|-|
|└─divProc|string|实施进度|-|
|└─stkDiv|number|每股送股(股)|-|
|└─stkBoRate|number|每股转增(股)|-|
|└─stkCoRate|number|每股配股(股)|-|
|└─cashDiv|number|每股分红(税前)(元)|-|
|└─cashDivTax|number|每股分红(税后)(元)|-|
|└─recordDate|string|股权登记日|-|
|└─exDate|string|除权除息日|-|
|└─payDate|string|派息日|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "tsCode": "",
      "endDate": "",
      "annDate": "",
      "divProc": "",
      "stkDiv": 0,
      "stkBoRate": 0,
      "stkCoRate": 0,
      "cashDiv": 0,
      "cashDivTax": 0,
      "recordDate": "",
      "exDate": "",
      "payDate": ""
    }
  ],
  "traceId": ""
}
```

### 业绩披露日历（stock_disclosure_date）—— 财报披露时间预判。<br><br>&lt;b&gt;用途&lt;/b&gt;：判断&amp;quot;本周/本月有哪些公司即将披露财报&amp;quot;，做事件驱动策略基础。<br>关键字段：preDate（预计披露日）、actualDate（实际披露日）、modifyDate（修改日）。<br>默认按 end_date DESC 返回最近的报告期。tsCode 必填。
**URL:** /openapi/v1/stock/financial/disclosure-date

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 业绩披露日历（stock_disclosure_date）—— 财报披露时间预判。

<p><b>用途</b>：判断"本周/本月有哪些公司即将披露财报"，做事件驱动策略基础。
<p>关键字段：preDate（预计披露日）、actualDate（实际披露日）、modifyDate（修改日）。
<p>默认按 end_date DESC 返回最近的报告期。tsCode 必填。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|page|int32|false|第几页，从 1 起。默认 1。0 / 负数会被当成 1。|-|
|size|int32|false|每页记录数。默认 50，硬上限 {@value #MAX_SIZE}。<br/><p>传入超过 {@value #MAX_SIZE} 时会被自动截断到 {@value #MAX_SIZE}（不报错）。</p>|-|
|tsCode|string|false|股票代码（带交易所后缀），如 {@code "600519.SH"}。<b>必填</b>。|-|
|startDate|string|false|起始报告期，格式 {@code YYYYMMDD}（季末日，如 {@code "20240331"}）。可空。<br/><p>不传时由 page/size 决定窗口（最近 N 期往前）。</p>|-|
|endDate|string|false|结束报告期，格式 {@code YYYYMMDD}。可空。不传时取最新报告期。|-|
|reportType|string|false|报告类型。<br/><br/><ul><br/>  <li>{@code "1"} —— 合并报表（默认 / 推荐，多数研究场景）</li><br/>  <li>{@code "2"} —— 母公司报表</li><br/>  <li>{@code "3"} —— 调整合并报表</li><br/>  <li>{@code "4"} —— 调整母公司报表</li><br/>  <li>...更多详见 Tushare 字典</li><br/></ul><br/><br/><p>可空 = 不限报表类型（同一报告期可能多行）。LLM 一般传 {@code "1"}。</p>|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/stock/financial/disclosure-date?page=0&size=0&reportType=&startDate=&tsCode=&endDate='
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─tsCode|string|股票代码（带交易所后缀，如 600519.SH）。|-|
|└─annDate|string|公告日期（最近一次公告日）。|-|
|└─endDate|string|报告期（如 2026-03-31 表示一季报，2026-06-30 表示半年报）。|-|
|└─preDate|string|预计披露日期。|-|
|└─actualDate|string|实际披露日期（披露后才填充）。|-|
|└─modifyDate|string|披露日期修改时间。|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "tsCode": "",
      "annDate": "yyyy-MM-dd HH:mm:ss",
      "endDate": "yyyy-MM-dd HH:mm:ss",
      "preDate": "yyyy-MM-dd HH:mm:ss",
      "actualDate": "yyyy-MM-dd HH:mm:ss",
      "modifyDate": "yyyy-MM-dd HH:mm:ss"
    }
  ],
  "traceId": ""
}
```

### 业绩快报（stock_express）—— 正式财报前的预披露数据。<br><br>&lt;b&gt;用途&lt;/b&gt;：超预期/不及预期早期信号源。含核心业绩 14 列：<br>revenue / operate_profit / total_profit / n_income / total_assets / total_hldr_eqy /<br>diluted_eps / diluted_roe / yoy_net_profit / bps / yoy_sales 等。<br>tsCode 必填。
**URL:** /openapi/v1/stock/financial/express

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 业绩快报（stock_express）—— 正式财报前的预披露数据。

<p><b>用途</b>：超预期/不及预期早期信号源。含核心业绩 14 列：
revenue / operate_profit / total_profit / n_income / total_assets / total_hldr_eqy /
diluted_eps / diluted_roe / yoy_net_profit / bps / yoy_sales 等。
<p>tsCode 必填。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|page|int32|false|第几页，从 1 起。默认 1。0 / 负数会被当成 1。|-|
|size|int32|false|每页记录数。默认 50，硬上限 {@value #MAX_SIZE}。<br/><p>传入超过 {@value #MAX_SIZE} 时会被自动截断到 {@value #MAX_SIZE}（不报错）。</p>|-|
|tsCode|string|false|股票代码（带交易所后缀），如 {@code "600519.SH"}。<b>必填</b>。|-|
|startDate|string|false|起始报告期，格式 {@code YYYYMMDD}（季末日，如 {@code "20240331"}）。可空。<br/><p>不传时由 page/size 决定窗口（最近 N 期往前）。</p>|-|
|endDate|string|false|结束报告期，格式 {@code YYYYMMDD}。可空。不传时取最新报告期。|-|
|reportType|string|false|报告类型。<br/><br/><ul><br/>  <li>{@code "1"} —— 合并报表（默认 / 推荐，多数研究场景）</li><br/>  <li>{@code "2"} —— 母公司报表</li><br/>  <li>{@code "3"} —— 调整合并报表</li><br/>  <li>{@code "4"} —— 调整母公司报表</li><br/>  <li>...更多详见 Tushare 字典</li><br/></ul><br/><br/><p>可空 = 不限报表类型（同一报告期可能多行）。LLM 一般传 {@code "1"}。</p>|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/stock/financial/express?page=0&size=0&startDate=&tsCode=&endDate=&reportType='
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─tsCode|string|股票代码。|-|
|└─annDate|string|公告日期。|-|
|└─endDate|string|报告期。|-|
|└─revenue|number|营业收入（元）。|-|
|└─operateProfit|number|营业利润（元）。|-|
|└─totalProfit|number|利润总额（元）。|-|
|└─nIncome|number|净利润（归母）。|-|
|└─totalAssets|number|总资产（期末）。|-|
|└─totalHldrEqyExcMinInt|number|股东权益（不含少数股东）。|-|
|└─dilutedEps|number|每股收益（稀释，元）。|-|
|└─dilutedRoe|number|净资产收益率（稀释，%）。|-|
|└─yoyNetProfit|number|净利润同比增长（%）。|-|
|└─bps|number|每股净资产（元）。|-|
|└─yoySales|number|营收同比增长（%）。|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "tsCode": "",
      "annDate": "yyyy-MM-dd HH:mm:ss",
      "endDate": "yyyy-MM-dd HH:mm:ss",
      "revenue": 0,
      "operateProfit": 0,
      "totalProfit": 0,
      "nIncome": 0,
      "totalAssets": 0,
      "totalHldrEqyExcMinInt": 0,
      "dilutedEps": 0,
      "dilutedRoe": 0,
      "yoyNetProfit": 0,
      "bps": 0,
      "yoySales": 0
    }
  ],
  "traceId": ""
}
```

### 业绩预告（stock_forecast）—— 未来 1 个报告期业绩预测。<br><br>&lt;b&gt;用途&lt;/b&gt;：事件驱动量化策略的高频信号源。关键字段 type（预增/略增/续盈/扭亏/预减/略减/续亏/首亏/不确定 9 类）+<br>pChangeMin/Max（净利润变动区间 %）+ 业绩变动原因摘要。<br>同一报告期可能多版本（首次 + 修正），返回时按 end_date DESC, ann_date DESC 排序。tsCode 必填。
**URL:** /openapi/v1/stock/financial/forecast

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 业绩预告（stock_forecast）—— 未来 1 个报告期业绩预测。

<p><b>用途</b>：事件驱动量化策略的高频信号源。关键字段 type（预增/略增/续盈/扭亏/预减/略减/续亏/首亏/不确定 9 类）+
pChangeMin/Max（净利润变动区间 %）+ 业绩变动原因摘要。
<p>同一报告期可能多版本（首次 + 修正），返回时按 end_date DESC, ann_date DESC 排序。tsCode 必填。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|page|int32|false|第几页，从 1 起。默认 1。0 / 负数会被当成 1。|-|
|size|int32|false|每页记录数。默认 50，硬上限 {@value #MAX_SIZE}。<br/><p>传入超过 {@value #MAX_SIZE} 时会被自动截断到 {@value #MAX_SIZE}（不报错）。</p>|-|
|tsCode|string|false|股票代码（带交易所后缀），如 {@code "600519.SH"}。<b>必填</b>。|-|
|startDate|string|false|起始报告期，格式 {@code YYYYMMDD}（季末日，如 {@code "20240331"}）。可空。<br/><p>不传时由 page/size 决定窗口（最近 N 期往前）。</p>|-|
|endDate|string|false|结束报告期，格式 {@code YYYYMMDD}。可空。不传时取最新报告期。|-|
|reportType|string|false|报告类型。<br/><br/><ul><br/>  <li>{@code "1"} —— 合并报表（默认 / 推荐，多数研究场景）</li><br/>  <li>{@code "2"} —— 母公司报表</li><br/>  <li>{@code "3"} —— 调整合并报表</li><br/>  <li>{@code "4"} —— 调整母公司报表</li><br/>  <li>...更多详见 Tushare 字典</li><br/></ul><br/><br/><p>可空 = 不限报表类型（同一报告期可能多行）。LLM 一般传 {@code "1"}。</p>|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/stock/financial/forecast?page=0&size=0&tsCode=&reportType=&endDate=&startDate='
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─tsCode|string|股票代码。|-|
|└─annDate|string|公告日期。|-|
|└─endDate|string|报告期。|-|
|└─type|string|业绩预告类型：<br/><ul><br/>  <li>"预增"、"略增"、"续盈"、"扭亏"</li><br/>  <li>"预减"、"略减"、"续亏"、"首亏"</li><br/>  <li>"不确定"</li><br/></ul>|-|
|└─pChangeMin|number|预告净利润变动幅度下限（%，可为负）。|-|
|└─pChangeMax|number|预告净利润变动幅度上限（%）。|-|
|└─netProfitMin|number|预告净利润下限（万元）。|-|
|└─netProfitMax|number|预告净利润上限（万元）。|-|
|└─lastParentNet|number|上年同期归母净利润（万元，对比基准）。|-|
|└─firstAnnDate|string|首次公告日（如本条是修正公告，原始公告日期）。|-|
|└─summary|string|业绩变动原因摘要（短句）。|-|
|└─changeReason|string|业绩变动原因（详细，可能为长文本）。|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "tsCode": "",
      "annDate": "yyyy-MM-dd HH:mm:ss",
      "endDate": "yyyy-MM-dd HH:mm:ss",
      "type": "",
      "pChangeMin": 0,
      "pChangeMax": 0,
      "netProfitMin": 0,
      "netProfitMax": 0,
      "lastParentNet": 0,
      "firstAnnDate": "yyyy-MM-dd HH:mm:ss",
      "summary": "",
      "changeReason": ""
    }
  ],
  "traceId": ""
}
```

## OpenAPI v1 —— 机器对机器（M2M）&lt;b&gt;元数据配置&lt;/b&gt;端点（scope / plan / 端点→scope 绑定 / 别名）。

&lt;p&gt;与 {@link OpenApiV1ProvisionController}（M2M token 管理）并列，供 claw-server 后台
（openclaw-app → claw-server → 本控制器）动态配置 stock 的 OpenAPI 元数据。
与人类管理员用的 {@code /stock/user/admin/openapi/meta/**}（JWT）功能一致、共用同一 Service，
只是鉴权换成 M2M：类级 {@link OpenApiScope}{@code (&quot;admin.provision&quot;)}（claw 服务令牌持有）。

&lt;p&gt;设计文档：{@code stock/docs/openapi-dynamic-config-design.md}。所有写操作经累进容纳校验 +
审计 + 缓存刷新 + Redis 广播。操作者取 {@code form.userId}（claw 转发管理员身份），否则记 claw-m2m。
### 
**URL:** /openapi/admin/meta/scopes

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/admin/meta/scopes'
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─name|string|scope 全名，如 "stock.kline" / "stock.minute"。|-|
|└─description|string|中文说明，如 "日/周/月 K 线、复权因子、多周期涨跌幅"。|-|
|└─minPlan|string|最低套餐档位（包含该 scope 的最低档）：free / pro / max / plus / ultra。|-|
|└─tableCount|int32|该 scope 覆盖的 PG 表数量（参考值）。|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "name": "",
      "description": "",
      "minPlan": "",
      "tableCount": 0
    }
  ],
  "traceId": ""
}
```

### 
**URL:** /openapi/admin/meta/plans

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/admin/meta/plans'
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─name|string|套餐名：free / pro / max / plus / ultra。|-|
|└─description|string|中文说明：例如 "免费版 · 仅基础行情" / "Pro · 加技术指标 + 财务报表"。|-|
|└─scopes|array|该套餐包含的 scope 列表（应用后整体覆盖 token.scopes）。|-|
|└─defaultRateLimitPerMin|int32|推荐默认每分钟频率上限。|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "name": "",
      "description": "",
      "scopes": [
        ""
      ],
      "defaultRateLimitPerMin": 0
    }
  ],
  "traceId": ""
}
```

### 
**URL:** /openapi/admin/meta/endpoints

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/admin/meta/endpoints'
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─id|int64|No comments found.|-|
|└─pathPattern|string|No comments found.|-|
|└─httpMethods|string|No comments found.|-|
|└─scopeName|string|No comments found.|-|
|└─category|string|No comments found.|-|
|└─title|string|No comments found.|-|
|└─description|string|No comments found.|-|
|└─tableMapping|string|No comments found.|-|
|└─onlineStatus|int32|No comments found.|-|
|└─enabled|int32|No comments found.|-|
|└─sortOrder|int32|No comments found.|-|
|└─createTime|string|No comments found.|-|
|└─updateTime|string|No comments found.|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "id": 0,
      "pathPattern": "",
      "httpMethods": "",
      "scopeName": "",
      "category": "",
      "title": "",
      "description": "",
      "tableMapping": "",
      "onlineStatus": 0,
      "enabled": 0,
      "sortOrder": 0,
      "createTime": "yyyy-MM-dd HH:mm:ss",
      "updateTime": "yyyy-MM-dd HH:mm:ss"
    }
  ],
  "traceId": ""
}
```

### 
**URL:** /openapi/admin/meta/scope/save

**Type:** POST


**Content-Type:** application/json

**Description:** 

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Body-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|userId|int64|false|No comments found.|-|
|d|int32|false|No comments found.|-|
|ip|string|false|No comments found.|-|
|market|string|false|No comments found.|-|
|vn|string|false|No comments found.|-|
|vc|int32|false|No comments found.|-|
|appsFlyerId|string|false|appsflyer 设备AF唯一ID|-|
|l|string|false|No comments found.|-|
|name|string|false|No comments found.|-|
|description|string|false|No comments found.|-|
|minPlan|string|false|No comments found.|-|
|tableCount|int32|false|No comments found.|-|
|sortOrder|int32|false|No comments found.|-|
|enabled|int32|false|No comments found.|-|

**Request-example:**
```bash
curl -X POST -H "Content-Type: application/json" -H "Authorization:Bearer {{token}}" -i '/openapi/admin/meta/scope/save' --data '{
  "userId": 0,
  "d": 0,
  "ip": "",
  "market": "",
  "vn": "",
  "vc": 0,
  "appsFlyerId": "",
  "l": "",
  "name": "",
  "description": "",
  "minPlan": "",
  "tableCount": 0,
  "sortOrder": 0,
  "enabled": 0
}'
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|object|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "traceId": ""
}
```

### 
**URL:** /openapi/admin/meta/scope/delete

**Type:** POST


**Content-Type:** application/json

**Description:** 

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Body-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|userId|int64|false|No comments found.|-|
|d|int32|false|No comments found.|-|
|ip|string|false|No comments found.|-|
|market|string|false|No comments found.|-|
|vn|string|false|No comments found.|-|
|vc|int32|false|No comments found.|-|
|appsFlyerId|string|false|appsflyer 设备AF唯一ID|-|
|l|string|false|No comments found.|-|
|key|string|false|No comments found.|-|

**Request-example:**
```bash
curl -X POST -H "Content-Type: application/json" -H "Authorization:Bearer {{token}}" -i '/openapi/admin/meta/scope/delete' --data '{
  "userId": 0,
  "d": 0,
  "ip": "",
  "market": "",
  "vn": "",
  "vc": 0,
  "appsFlyerId": "",
  "l": "",
  "key": ""
}'
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|object|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "traceId": ""
}
```

### 
**URL:** /openapi/admin/meta/plan/save

**Type:** POST


**Content-Type:** application/json

**Description:** 

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Body-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|userId|int64|false|No comments found.|-|
|d|int32|false|No comments found.|-|
|ip|string|false|No comments found.|-|
|market|string|false|No comments found.|-|
|vn|string|false|No comments found.|-|
|vc|int32|false|No comments found.|-|
|appsFlyerId|string|false|appsflyer 设备AF唯一ID|-|
|l|string|false|No comments found.|-|
|name|string|false|No comments found.|-|
|description|string|false|No comments found.|-|
|defaultRateLimitPerMin|int32|false|No comments found.|-|
|tierLevel|int32|false|No comments found.|-|
|sellable|int32|false|No comments found.|-|
|enabled|int32|false|No comments found.|-|

**Request-example:**
```bash
curl -X POST -H "Content-Type: application/json" -H "Authorization:Bearer {{token}}" -i '/openapi/admin/meta/plan/save' --data '{
  "userId": 0,
  "d": 0,
  "ip": "",
  "market": "",
  "vn": "",
  "vc": 0,
  "appsFlyerId": "",
  "l": "",
  "name": "",
  "description": "",
  "defaultRateLimitPerMin": 0,
  "tierLevel": 0,
  "sellable": 0,
  "enabled": 0
}'
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|object|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "traceId": ""
}
```

### 
**URL:** /openapi/admin/meta/plan/set-scopes

**Type:** POST


**Content-Type:** application/json

**Description:** 

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Body-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|userId|int64|false|No comments found.|-|
|d|int32|false|No comments found.|-|
|ip|string|false|No comments found.|-|
|market|string|false|No comments found.|-|
|vn|string|false|No comments found.|-|
|vc|int32|false|No comments found.|-|
|appsFlyerId|string|false|appsflyer 设备AF唯一ID|-|
|l|string|false|No comments found.|-|
|planName|string|false|No comments found.|-|
|scopes|array|false|No comments found.|-|

**Request-example:**
```bash
curl -X POST -H "Content-Type: application/json" -H "Authorization:Bearer {{token}}" -i '/openapi/admin/meta/plan/set-scopes' --data '{
  "userId": 0,
  "d": 0,
  "ip": "",
  "market": "",
  "vn": "",
  "vc": 0,
  "appsFlyerId": "",
  "l": "",
  "planName": "",
  "scopes": [
    ""
  ]
}'
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|object|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "traceId": ""
}
```

### 
**URL:** /openapi/admin/meta/endpoint/update

**Type:** POST


**Content-Type:** application/json

**Description:** 

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Body-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|userId|int64|false|No comments found.|-|
|d|int32|false|No comments found.|-|
|ip|string|false|No comments found.|-|
|market|string|false|No comments found.|-|
|vn|string|false|No comments found.|-|
|vc|int32|false|No comments found.|-|
|appsFlyerId|string|false|appsflyer 设备AF唯一ID|-|
|l|string|false|No comments found.|-|
|id|int64|false|No comments found.|-|
|scopeName|string|false|No comments found.|-|
|category|string|false|No comments found.|-|
|title|string|false|No comments found.|-|
|description|string|false|No comments found.|-|
|tableMapping|string|false|No comments found.|-|
|onlineStatus|int32|false|No comments found.|-|
|enabled|int32|false|No comments found.|-|
|sortOrder|int32|false|No comments found.|-|

**Request-example:**
```bash
curl -X POST -H "Content-Type: application/json" -H "Authorization:Bearer {{token}}" -i '/openapi/admin/meta/endpoint/update' --data '{
  "userId": 0,
  "d": 0,
  "ip": "",
  "market": "",
  "vn": "",
  "vc": 0,
  "appsFlyerId": "",
  "l": "",
  "id": 0,
  "scopeName": "",
  "category": "",
  "title": "",
  "description": "",
  "tableMapping": "",
  "onlineStatus": 0,
  "enabled": 0,
  "sortOrder": 0
}'
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|object|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "traceId": ""
}
```

### 
**URL:** /openapi/admin/meta/endpoint/toggle

**Type:** POST


**Content-Type:** application/json

**Description:** 

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Body-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|userId|int64|false|No comments found.|-|
|d|int32|false|No comments found.|-|
|ip|string|false|No comments found.|-|
|market|string|false|No comments found.|-|
|vn|string|false|No comments found.|-|
|vc|int32|false|No comments found.|-|
|appsFlyerId|string|false|appsflyer 设备AF唯一ID|-|
|l|string|false|No comments found.|-|
|id|int64|false|No comments found.|-|
|enabled|boolean|false|No comments found.|-|

**Request-example:**
```bash
curl -X POST -H "Content-Type: application/json" -H "Authorization:Bearer {{token}}" -i '/openapi/admin/meta/endpoint/toggle' --data '{
  "userId": 0,
  "d": 0,
  "ip": "",
  "market": "",
  "vn": "",
  "vc": 0,
  "appsFlyerId": "",
  "l": "",
  "id": 0,
  "enabled": true
}'
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|object|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "traceId": ""
}
```

### 
**URL:** /openapi/admin/meta/alias/save

**Type:** POST


**Content-Type:** application/json

**Description:** 

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Body-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|userId|int64|false|No comments found.|-|
|d|int32|false|No comments found.|-|
|ip|string|false|No comments found.|-|
|market|string|false|No comments found.|-|
|vn|string|false|No comments found.|-|
|vc|int32|false|No comments found.|-|
|appsFlyerId|string|false|appsflyer 设备AF唯一ID|-|
|l|string|false|No comments found.|-|
|alias|string|false|No comments found.|-|
|targetScopes|string|false|No comments found.|-|
|note|string|false|No comments found.|-|

**Request-example:**
```bash
curl -X POST -H "Content-Type: application/json" -H "Authorization:Bearer {{token}}" -i '/openapi/admin/meta/alias/save' --data '{
  "userId": 0,
  "d": 0,
  "ip": "",
  "market": "",
  "vn": "",
  "vc": 0,
  "appsFlyerId": "",
  "l": "",
  "alias": "",
  "targetScopes": "",
  "note": ""
}'
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|object|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "traceId": ""
}
```

### 
**URL:** /openapi/admin/meta/alias/delete

**Type:** POST


**Content-Type:** application/json

**Description:** 

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Body-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|userId|int64|false|No comments found.|-|
|d|int32|false|No comments found.|-|
|ip|string|false|No comments found.|-|
|market|string|false|No comments found.|-|
|vn|string|false|No comments found.|-|
|vc|int32|false|No comments found.|-|
|appsFlyerId|string|false|appsflyer 设备AF唯一ID|-|
|l|string|false|No comments found.|-|
|key|string|false|No comments found.|-|

**Request-example:**
```bash
curl -X POST -H "Content-Type: application/json" -H "Authorization:Bearer {{token}}" -i '/openapi/admin/meta/alias/delete' --data '{
  "userId": 0,
  "d": 0,
  "ip": "",
  "market": "",
  "vn": "",
  "vc": 0,
  "appsFlyerId": "",
  "l": "",
  "key": ""
}'
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|object|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "traceId": ""
}
```

### 
**URL:** /openapi/admin/meta/refresh

**Type:** POST


**Content-Type:** application/json

**Description:** 

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Body-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|userId|int64|false|No comments found.|-|
|d|int32|false|No comments found.|-|
|ip|string|false|No comments found.|-|
|market|string|false|No comments found.|-|
|vn|string|false|No comments found.|-|
|vc|int32|false|No comments found.|-|
|appsFlyerId|string|false|appsflyer 设备AF唯一ID|-|
|l|string|false|No comments found.|-|
|key|string|false|No comments found.|-|

**Request-example:**
```bash
curl -X POST -H "Content-Type: application/json" -H "Authorization:Bearer {{token}}" -i '/openapi/admin/meta/refresh' --data '{
  "userId": 0,
  "d": 0,
  "ip": "",
  "market": "",
  "vn": "",
  "vc": 0,
  "appsFlyerId": "",
  "l": "",
  "key": ""
}'
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|object|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "traceId": ""
}
```

### 
**URL:** /openapi/admin/meta/export/tiers-detail

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/admin/meta/export/tiers-detail'
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|string|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": "",
  "traceId": ""
}
```

### 
**URL:** /openapi/admin/meta/export/tier-table

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/admin/meta/export/tier-table'
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|string|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": "",
  "traceId": ""
}
```

## OpenAPI v1 —— K 线补完端点（stock.kline scope）。

&lt;p&gt;当前仅含 1 个端点：复权因子（adj-factor）。
&lt;p&gt;注意：股票周 / 月 K 线已通过 &lt;code&gt;/openapi/v1/stock/kline/daily&lt;/code&gt; 端点的 form.type 字段支持
（type=11 日 / 12 周 / 13 月），不重复造端点。
### 股票复权因子（adj_factor）。tsCode 必填。<br><br>用途：<br>&lt;ul&gt;<br>  &lt;li&gt;线性指标（MA / EMA / BOLL / KTN 等）：HFQ = BFQ × adj_factor&lt;/li&gt;<br>  &lt;li&gt;非线性指标（MACD / KDJ / RSI 等）必须用复权价独立计算，不能换算&lt;/li&gt;<br>  &lt;li&gt;跨除权日比较股价时必须用复权因子修正，否则跌幅会&amp;quot;虚假&amp;quot;&lt;/li&gt;<br>&lt;/ul&gt;
**URL:** /openapi/v1/stock/kline/adj-factor

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 股票复权因子（adj_factor）。tsCode 必填。

<p>用途：
<ul>
  <li>线性指标（MA / EMA / BOLL / KTN 等）：HFQ = BFQ × adj_factor</li>
  <li>非线性指标（MACD / KDJ / RSI 等）必须用复权价独立计算，不能换算</li>
  <li>跨除权日比较股价时必须用复权因子修正，否则跌幅会"虚假"</li>
</ul>

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|page|int32|false|第几页，从 1 起。默认 1。0 / 负数会被当成 1。|-|
|size|int32|false|每页记录数。默认 50，硬上限 {@value #MAX_SIZE}。<br/><p>传入超过 {@value #MAX_SIZE} 时会被自动截断到 {@value #MAX_SIZE}（不报错）。</p>|-|
|tsCode|string|false|代码（带交易所后缀）。<b>必填</b>。<br/><br/><p><b>示例</b>：</p><br/><ul><br/>  <li>股票：{@code "600519.SH"} / {@code "000001.SZ"}</li><br/>  <li>指数：{@code "000300.SH"}（沪深 300）/ {@code "000016.SH"}（上证 50）</li><br/>  <li>申万行业：{@code "801080"}（一级"电子"）/ {@code "801120"}（一级"食品饮料"）</li><br/></ul>|-|
|startDate|string|false|起始日期，格式 {@code YYYYMMDD}（如 {@code "20260101"}）。可空，不传时用默认窗口。|-|
|endDate|string|false|结束日期，格式 {@code YYYYMMDD}（如 {@code "20260430"}）。可空，不传时取最新交易日。|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/stock/kline/adj-factor?page=0&size=0&tsCode=&startDate=&endDate='
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─tsCode|string|No comments found.|-|
|└─tradeDate|string|交易日期 YYYYMMDD|-|
|└─adjFactor|number|复权因子（每股分红 / 拆股调整后的乘数）|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "tsCode": "",
      "tradeDate": "",
      "adjFactor": 0
    }
  ],
  "traceId": ""
}
```

### 股票每日涨跌停价（stock_limits）。tsCode 必填；缺日期默认最近 60 天。<br><br>覆盖 ST 加挂 5%、北交所 30%、创业 / 科创板 20% 等不同板规则。量化策略需要判断&amp;quot;是否触及涨跌停&amp;quot;用此端点。
**URL:** /openapi/v1/stock/kline/limits

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 股票每日涨跌停价（stock_limits）。tsCode 必填；缺日期默认最近 60 天。

<p>覆盖 ST 加挂 5%、北交所 30%、创业 / 科创板 20% 等不同板规则。量化策略需要判断"是否触及涨跌停"用此端点。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|page|int32|false|第几页，从 1 起。默认 1。0 / 负数会被当成 1。|-|
|size|int32|false|每页记录数。默认 50，硬上限 {@value #MAX_SIZE}。<br/><p>传入超过 {@value #MAX_SIZE} 时会被自动截断到 {@value #MAX_SIZE}（不报错）。</p>|-|
|tsCode|string|false|代码（带交易所后缀）。<b>必填</b>。<br/><br/><p><b>示例</b>：</p><br/><ul><br/>  <li>股票：{@code "600519.SH"} / {@code "000001.SZ"}</li><br/>  <li>指数：{@code "000300.SH"}（沪深 300）/ {@code "000016.SH"}（上证 50）</li><br/>  <li>申万行业：{@code "801080"}（一级"电子"）/ {@code "801120"}（一级"食品饮料"）</li><br/></ul>|-|
|startDate|string|false|起始日期，格式 {@code YYYYMMDD}（如 {@code "20260101"}）。可空，不传时用默认窗口。|-|
|endDate|string|false|结束日期，格式 {@code YYYYMMDD}（如 {@code "20260430"}）。可空，不传时取最新交易日。|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/stock/kline/limits?page=0&size=0&endDate=&startDate=&tsCode='
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─tradeDate|string|No comments found.|-|
|└─tsCode|string|No comments found.|-|
|└─preClose|number|前收|-|
|└─upLimit|number|当日涨停价|-|
|└─downLimit|number|当日跌停价|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "tradeDate": "",
      "tsCode": "",
      "preClose": 0,
      "upLimit": 0,
      "downLimit": 0
    }
  ],
  "traceId": ""
}
```

### 多周期涨跌幅（stock_percentage_change）。1d / 3d / 1w / 2w / 1m / 1q / 2q / 1y。<br><br>对应 site internal: &lt;code&gt;POST /stock/api/stock/stockPercentageChangeList&lt;/code&gt;。<br>阶段 11 迁到 OpenAPI；归 stock.kline scope（属价格层，不算指标）。
**URL:** /openapi/v1/stock/kline/percentage-change

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 多周期涨跌幅（stock_percentage_change）。1d / 3d / 1w / 2w / 1m / 1q / 2q / 1y。

<p>对应 site internal: <code>POST /stock/api/stock/stockPercentageChangeList</code>。
阶段 11 迁到 OpenAPI；归 stock.kline scope（属价格层，不算指标）。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|page|int32|false|第几页，从 1 起。默认 1。0 / 负数会被当成 1。|-|
|size|int32|false|每页记录数。默认 50，硬上限 {@value #MAX_SIZE}。<br/><p>传入超过 {@value #MAX_SIZE} 时会被自动截断到 {@value #MAX_SIZE}（不报错）。</p>|-|
|tsCode|string|false|股票代码（带交易所后缀），如 {@code "600519.SH"}。可空——空时配合 {@link #orderBy} 全市场排序。|-|
|orderBy|string|false|排序字段。可选值：<br/><ul><br/>  <li>{@code "pctChg"} —— 当日涨跌幅</li><br/>  <li>{@code "pctChg3d"} —— 近 3 日涨跌幅</li><br/>  <li>{@code "pctChg1w"} —— 近 1 周涨跌幅</li><br/>  <li>{@code "pctChg2w"} —— 近 2 周</li><br/>  <li>{@code "pctChg1m"} —— 近 1 个月</li><br/>  <li>{@code "pctChg1q"} —— 近 1 个季度</li><br/>  <li>{@code "pctChg2q"} —— 近 2 个季度</li><br/>  <li>{@code "pctChg1y"} —— 近 1 年</li><br/></ul>|-|
|direction|string|false|排序方向：{@code "asc"}（升序）/ {@code "desc"}（降序）。默认 {@code "desc"}。|-|
|exchange|string|false|交易所过滤：{@code "SH"}（上交所）/ {@code "SZ"}（深交所）/ {@code "BJ"}（北交所）。可空，空 = 全市场。|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/stock/kline/percentage-change?page=0&size=0&exchange=&orderBy=&tsCode=&direction='
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─tsCode|string|股票代码（带交易所后缀），如 {@code "600519.SH"}。|-|
|└─tradeDate|string|截止交易日（区间右端点）。|-|
|└─name|string|股票中文简称，如 {@code "贵州茅台"}。|-|
|└─pctChg|number|当日涨跌幅（%），即 (close - preClose) / preClose × 100。|-|
|└─close|number|当日收盘价（元）。|-|
|└─pctChg3d|number|近 3 个交易日涨跌幅（%）。|-|
|└─close3d|number|3 个交易日前的收盘价（元，用于反推区间起点）。|-|
|└─pctChg1w|number|近 1 周（5 个交易日）涨跌幅（%）。|-|
|└─close1w|number|1 周前的收盘价（元）。|-|
|└─pctChg2w|number|近 2 周（10 个交易日）涨跌幅（%）。|-|
|└─close2w|number|2 周前的收盘价（元）。|-|
|└─pctChg1m|number|近 1 个月（约 20 个交易日）涨跌幅（%）。|-|
|└─close1m|number|1 个月前的收盘价（元）。|-|
|└─pctChg1q|number|近 1 个季度（约 60 个交易日）涨跌幅（%）。|-|
|└─close1q|number|1 个季度前的收盘价（元）。|-|
|└─pctChg2q|number|近 2 个季度（约 120 个交易日）涨跌幅（%）。|-|
|└─close2q|number|2 个季度前的收盘价（元）。|-|
|└─pctChg1y|number|近 1 年（约 240 个交易日）涨跌幅（%）。|-|
|└─close1y|number|1 年前的收盘价（元）。|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "tsCode": "",
      "tradeDate": "yyyy-MM-dd HH:mm:ss",
      "name": "",
      "pctChg": 0,
      "close": 0,
      "pctChg3d": 0,
      "close3d": 0,
      "pctChg1w": 0,
      "close1w": 0,
      "pctChg2w": 0,
      "close2w": 0,
      "pctChg1m": 0,
      "close1m": 0,
      "pctChg1q": 0,
      "close1q": 0,
      "pctChg2q": 0,
      "close2q": 0,
      "pctChg1y": 0,
      "close1y": 0
    }
  ],
  "traceId": ""
}
```

### 涨停股票筛选（按近 N 个交易日内连板数）。<br><br>对应 site internal: &lt;code&gt;POST /stock/api/stock/candles/selectLimitUp&lt;/code&gt;。<br>注意：form 中字段名 {@code tadeDays}（拼写历史遗留，不要写成 tradeDays）。
**URL:** /openapi/v1/stock/kline/limit-up

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 涨停股票筛选（按近 N 个交易日内连板数）。

<p>对应 site internal: <code>POST /stock/api/stock/candles/selectLimitUp</code>。
注意：form 中字段名 {@code tadeDays}（拼写历史遗留，不要写成 tradeDays）。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|tadeDays|int32|false|回看 N 个交易日。例如 {@code 5} = 近 5 个交易日内的连板情况。<br/><p>⚠ 字段名拼写为 {@code tadeDays}（历史遗留，正确应为 {@code tradeDays}），保持兼容不改名。</p>|-|
|limitUpNum|int32|false|至少 M 个涨停板。例如 {@code limitUpNum=2} 表示"最少 2 板"，包括 2 / 3 / 4 / 5 板及以上。|-|
|type|int32|false|K 线形态枚举（来自 {@code com.common.enums.StockKLineGraphType}）。<br/><p>仅 {@code /graph-type} 端点使用。常见值：</p><br/><ul><br/>  <li>W 底 / M 顶</li><br/>  <li>头肩顶 / 头肩底</li><br/>  <li>箱体震荡</li><br/></ul><br/><p>具体枚举映射请参考后端 {@code StockKLineGraphType}。</p>|-|
|lineType|int32|false|K 线周期（来自 {@code com.common.enums.StockKLineType}）：{@code 11}=日 / {@code 12}=周 / {@code 13}=月。<br/><p>仅 {@code /graph-type} 端点使用。</p>|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/stock/kline/limit-up?tadeDays=0&limitUpNum=0&type=0&lineType=0'
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    "",
    ""
  ],
  "traceId": ""
}
```

### 按 K 线形态查找股票（箱体震荡 / 突破等）。<br><br>对应 site internal: &lt;code&gt;POST /stock/api/stock/candles/findStockKlineGraphType&lt;/code&gt;。
**URL:** /openapi/v1/stock/kline/graph-type

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 按 K 线形态查找股票（箱体震荡 / 突破等）。

<p>对应 site internal: <code>POST /stock/api/stock/candles/findStockKlineGraphType</code>。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|tadeDays|int32|false|回看 N 个交易日。例如 {@code 5} = 近 5 个交易日内的连板情况。<br/><p>⚠ 字段名拼写为 {@code tadeDays}（历史遗留，正确应为 {@code tradeDays}），保持兼容不改名。</p>|-|
|limitUpNum|int32|false|至少 M 个涨停板。例如 {@code limitUpNum=2} 表示"最少 2 板"，包括 2 / 3 / 4 / 5 板及以上。|-|
|type|int32|false|K 线形态枚举（来自 {@code com.common.enums.StockKLineGraphType}）。<br/><p>仅 {@code /graph-type} 端点使用。常见值：</p><br/><ul><br/>  <li>W 底 / M 顶</li><br/>  <li>头肩顶 / 头肩底</li><br/>  <li>箱体震荡</li><br/></ul><br/><p>具体枚举映射请参考后端 {@code StockKLineGraphType}。</p>|-|
|lineType|int32|false|K 线周期（来自 {@code com.common.enums.StockKLineType}）：{@code 11}=日 / {@code 12}=周 / {@code 13}=月。<br/><p>仅 {@code /graph-type} 端点使用。</p>|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/stock/kline/graph-type?tadeDays=0&limitUpNum=0&type=0&lineType=0'
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─tsCode|string|命中此形态的股票代码（带交易所后缀），如 {@code "600519.SH"}。|-|
|└─kLineType|int32|K 线周期（{@code com.common.enums.StockKLineType}）：{@code 11}=日 / {@code 12}=周 / {@code 13}=月。|-|
|└─data|array|形态特征点序列，每项是一个 key-value map，键随形态类型不同而异。<br/><br/><p>例如 W 底形态可能含：</p><br/><ul><br/>  <li>{@code "leftBottom"} —— 左底点（含 tradeDate / price）</li><br/>  <li>{@code "rightBottom"} —— 右底点</li><br/>  <li>{@code "neckline"} —— 颈线价</li><br/>  <li>{@code "confidence"} —— 置信度评分（0~1）</li><br/>  <li>{@code "breakout"} —— 突破点（如已突破颈线）</li><br/></ul><br/><br/><p>调用方按形态类型解析具体字段。</p>|-|
|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└─mapKey|object|A map key.|-|
|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└─any object|object|any object.|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "tsCode": "",
      "kLineType": 0,
      "data": [
        {
          "mapKey": {}
        }
      ]
    }
  ],
  "traceId": ""
}
```

### 分钟 K 线（1min / 5min / 15min / 30min / 60min）。<br><br>对应 site internal: &lt;code&gt;POST /stock/candles/stock/mins&lt;/code&gt;（Tushare 转发，不落库）。<br>阶段 11 迁到 OpenAPI；归 &lt;code&gt;stock.minute&lt;/code&gt; scope。<br><br>⚠ 走 Tushare 实时转发，会消耗 Tushare API 额度；窗口务必 ≤ 1 个月。
**URL:** /openapi/v1/stock/kline/minute

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 分钟 K 线（1min / 5min / 15min / 30min / 60min）。

<p>对应 site internal: <code>POST /stock/candles/stock/mins</code>（Tushare 转发，不落库）。
阶段 11 迁到 OpenAPI；归 <code>stock.minute</code> scope。

<p>⚠ 走 Tushare 实时转发，会消耗 Tushare API 额度；窗口务必 ≤ 1 个月。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|page|int32|false|第几页，从 1 起。默认 1。0 / 负数会被当成 1。|-|
|size|int32|false|每页记录数。默认 50，硬上限 {@value #MAX_SIZE}。<br/><p>传入超过 {@value #MAX_SIZE} 时会被自动截断到 {@value #MAX_SIZE}（不报错）。</p>|-|
|tsCode|string|false|股票代码（带交易所后缀），如 {@code "600519.SH"} / {@code "000001.SZ"}。<b>必填</b>。|-|
|freq|string|false|分钟级别。<b>必填</b>。<br/><br/><ul><br/>  <li>{@code "1min"} —— 1 分钟</li><br/>  <li>{@code "5min"} —— 5 分钟（最常用）</li><br/>  <li>{@code "15min"} —— 15 分钟</li><br/>  <li>{@code "30min"} —— 30 分钟</li><br/>  <li>{@code "60min"} —— 60 分钟</li><br/></ul>|-|
|startDate|string|false|起始时间，格式 {@code YYYYMMDD} 或 {@code YYYYMMDDHHmm}。可空。|-|
|endDate|string|false|结束时间，格式 {@code YYYYMMDD} 或 {@code YYYYMMDDHHmm}。可空，不传时取最新。|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/stock/kline/minute?page=0&size=0&freq=&tsCode=&endDate=&startDate='
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─id|int64|内部主键，调用方一般忽略。|-|
|└─tsCode|string|股票代码（带交易所后缀），如 {@code "600519.SH"}。|-|
|└─freq|string|分钟级别：{@code "1min"} / {@code "5min"} / {@code "15min"} / {@code "30min"} / {@code "60min"}。|-|
|└─tradeTime|string|K 线时间点（精确到分钟）。例如 {@code "2026-04-30 10:30:00"} 表示该 5min K 是 10:25-10:30 的结果。|-|
|└─open|number|开盘价（元）。|-|
|└─high|number|最高价（元）。|-|
|└─low|number|最低价（元）。|-|
|└─close|number|收盘价（元）。|-|
|└─vol|number|该 K 内成交量（手）。|-|
|└─amount|number|该 K 内成交额（千元）。|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "id": 0,
      "tsCode": "",
      "freq": "",
      "tradeTime": "yyyy-MM-dd HH:mm:ss",
      "open": 0,
      "high": 0,
      "low": 0,
      "close": 0,
      "vol": 0,
      "amount": 0
    }
  ],
  "traceId": ""
}
```

### 股票周/月线一体（{@code stk_weekly_monthly}）—— 不复权。tsCode 必填。<br><br>区别于站内 weekly / monthly 单独表：此表把周线和月线放在一张表里，按 {@code freq} 区分<br>（freq=week/month），适合一次性拉取做长周期对齐。不复权（BFQ）— 跨除权日比较需结合 adj-factor。 
**URL:** /openapi/v1/stock/kline/weekly-monthly

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 股票周/月线一体（{@code stk_weekly_monthly}）—— 不复权。tsCode 必填。

<p>区别于站内 weekly / monthly 单独表：此表把周线和月线放在一张表里，按 {@code freq} 区分
（freq=week/month），适合一次性拉取做长周期对齐。不复权（BFQ）— 跨除权日比较需结合 adj-factor。</p>

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|page|int32|false|第几页，从 1 起。默认 1。0 / 负数会被当成 1。|-|
|size|int32|false|每页记录数。默认 50，硬上限 {@value #MAX_SIZE}。<br/><p>传入超过 {@value #MAX_SIZE} 时会被自动截断到 {@value #MAX_SIZE}（不报错）。</p>|-|
|tsCode|string|false|TS 代码（指数 / 个股 / 权重端点的指数代码）。可空（必填时返回空）。|-|
|conCode|string|false|成分代码（仅 index_weight 端点用，可空 → 拉全部成分）。|-|
|tradeDate|string|false|单日交易日 {@code YYYYMMDD}。可空。|-|
|startDate|string|false|起始交易日 {@code YYYYMMDD}。可空。|-|
|endDate|string|false|结束交易日 {@code YYYYMMDD}。可空。|-|
|freq|string|false|频率：weekly_monthly / week_month_adj = {week,month}；idx_mins = {1min,5min,15min,30min,60min}。可空。|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/stock/kline/weekly-monthly?page=0&size=0&tradeDate=&startDate=&conCode=&freq=&tsCode=&endDate='
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─tradeDate|string|交易日（周线 = 周内最后一个交易日；月线 = 月内最后一个交易日）|-|
|└─tsCode|string|股票 TS 代码|-|
|└─endDate|string|周期末日期|-|
|└─freq|string|频率：week / month|-|
|└─open|number|开盘价|-|
|└─high|number|最高价|-|
|└─low|number|最低价|-|
|└─close|number|收盘价|-|
|└─preClose|number|前收盘价|-|
|└─vol|number|成交量（手）|-|
|└─amount|number|成交额（千元）|-|
|└─change|number|涨跌额|-|
|└─pctChg|number|涨跌幅（%）|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "tradeDate": "yyyy-MM-dd HH:mm:ss",
      "tsCode": "",
      "endDate": "yyyy-MM-dd HH:mm:ss",
      "freq": "",
      "open": 0,
      "high": 0,
      "low": 0,
      "close": 0,
      "preClose": 0,
      "vol": 0,
      "amount": 0,
      "change": 0,
      "pctChg": 0
    }
  ],
  "traceId": ""
}
```

### 股票周/月线复权一体（{@code stk_week_month_adj}）—— 同时含 BFQ / QFQ / HFQ 三套 OHLC。tsCode 必填。<br><br>这是替代 weekly-monthly + adj-factor 自行换算的&amp;quot;开箱即用&amp;quot;长周期复权 K，<br>适合直接画长周期复权 K 线、做中长期回测。freq=week/month。 
**URL:** /openapi/v1/stock/kline/week-month-adj

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 股票周/月线复权一体（{@code stk_week_month_adj}）—— 同时含 BFQ / QFQ / HFQ 三套 OHLC。tsCode 必填。

<p>这是替代 weekly-monthly + adj-factor 自行换算的"开箱即用"长周期复权 K，
适合直接画长周期复权 K 线、做中长期回测。freq=week/month。</p>

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|page|int32|false|第几页，从 1 起。默认 1。0 / 负数会被当成 1。|-|
|size|int32|false|每页记录数。默认 50，硬上限 {@value #MAX_SIZE}。<br/><p>传入超过 {@value #MAX_SIZE} 时会被自动截断到 {@value #MAX_SIZE}（不报错）。</p>|-|
|tsCode|string|false|TS 代码（指数 / 个股 / 权重端点的指数代码）。可空（必填时返回空）。|-|
|conCode|string|false|成分代码（仅 index_weight 端点用，可空 → 拉全部成分）。|-|
|tradeDate|string|false|单日交易日 {@code YYYYMMDD}。可空。|-|
|startDate|string|false|起始交易日 {@code YYYYMMDD}。可空。|-|
|endDate|string|false|结束交易日 {@code YYYYMMDD}。可空。|-|
|freq|string|false|频率：weekly_monthly / week_month_adj = {week,month}；idx_mins = {1min,5min,15min,30min,60min}。可空。|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/stock/kline/week-month-adj?page=0&size=0&tradeDate=&conCode=&freq=&tsCode=&startDate=&endDate='
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─tradeDate|string|交易日|-|
|└─tsCode|string|股票 TS 代码|-|
|└─endDate|string|周期末日期|-|
|└─freq|string|频率：week / month|-|
|└─open|number|No comments found.|-|
|└─high|number|No comments found.|-|
|└─low|number|No comments found.|-|
|└─close|number|No comments found.|-|
|└─preClose|number|前收盘价|-|
|└─openQfq|number|No comments found.|-|
|└─highQfq|number|No comments found.|-|
|└─lowQfq|number|No comments found.|-|
|└─closeQfq|number|No comments found.|-|
|└─openHfq|number|No comments found.|-|
|└─highHfq|number|No comments found.|-|
|└─lowHfq|number|No comments found.|-|
|└─closeHfq|number|No comments found.|-|
|└─vol|number|成交量（手）|-|
|└─amount|number|成交额（千元）|-|
|└─change|number|涨跌额|-|
|└─pctChg|number|涨跌幅（%）|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "tradeDate": "yyyy-MM-dd HH:mm:ss",
      "tsCode": "",
      "endDate": "yyyy-MM-dd HH:mm:ss",
      "freq": "",
      "open": 0,
      "high": 0,
      "low": 0,
      "close": 0,
      "preClose": 0,
      "openQfq": 0,
      "highQfq": 0,
      "lowQfq": 0,
      "closeQfq": 0,
      "openHfq": 0,
      "highHfq": 0,
      "lowHfq": 0,
      "closeHfq": 0,
      "vol": 0,
      "amount": 0,
      "change": 0,
      "pctChg": 0
    }
  ],
  "traceId": ""
}
```

### 指数历史分钟 K 线（{@code idx_mins}）—— 10 核心指数，2026-06-05 起逐日积累（更早历史暂缺）。tsCode 必填，freq 可选<br>（1min/5min/15min/30min/60min，默认全频率）。<br><br>与 {@code /openapi/v1/stock/kline/minute} 端点区别：那个走 Tushare 实时转发（消耗 Tushare 额度），<br>这个直接读 PG 库。如果想要更长历史窗口的指数分钟数据，走这个端点。 <br><br>归 stock.minute scope（与个股分钟同档）。 
**URL:** /openapi/v1/stock/kline/index-minute

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 指数历史分钟 K 线（{@code idx_mins}）—— 10 核心指数，2026-06-05 起逐日积累（更早历史暂缺）。tsCode 必填，freq 可选
（1min/5min/15min/30min/60min，默认全频率）。

<p>与 {@code /openapi/v1/stock/kline/minute} 端点区别：那个走 Tushare 实时转发（消耗 Tushare 额度），
这个直接读 PG 库。如果想要更长历史窗口的指数分钟数据，走这个端点。</p>

<p>归 stock.minute scope（与个股分钟同档）。</p>

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|page|int32|false|第几页，从 1 起。默认 1。0 / 负数会被当成 1。|-|
|size|int32|false|每页记录数。默认 50，硬上限 {@value #MAX_SIZE}。<br/><p>传入超过 {@value #MAX_SIZE} 时会被自动截断到 {@value #MAX_SIZE}（不报错）。</p>|-|
|tsCode|string|false|TS 代码（指数 / 个股 / 权重端点的指数代码）。可空（必填时返回空）。|-|
|conCode|string|false|成分代码（仅 index_weight 端点用，可空 → 拉全部成分）。|-|
|tradeDate|string|false|单日交易日 {@code YYYYMMDD}。可空。|-|
|startDate|string|false|起始交易日 {@code YYYYMMDD}。可空。|-|
|endDate|string|false|结束交易日 {@code YYYYMMDD}。可空。|-|
|freq|string|false|频率：weekly_monthly / week_month_adj = {week,month}；idx_mins = {1min,5min,15min,30min,60min}。可空。|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/stock/kline/index-minute?page=0&size=0&freq=&startDate=&tsCode=&tradeDate=&conCode=&endDate='
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─tsCode|string|指数 TS 代码|-|
|└─tradeTime|string|分钟级时间戳|-|
|└─freq|string|频率：1min / 5min / 15min / 30min / 60min|-|
|└─open|number|No comments found.|-|
|└─high|number|No comments found.|-|
|└─low|number|No comments found.|-|
|└─close|number|No comments found.|-|
|└─vol|number|No comments found.|-|
|└─amount|number|No comments found.|-|
|└─preClose|number|No comments found.|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "tsCode": "",
      "tradeTime": "yyyy-MM-dd HH:mm:ss",
      "freq": "",
      "open": 0,
      "high": 0,
      "low": 0,
      "close": 0,
      "vol": 0,
      "amount": 0,
      "preClose": 0
    }
  ],
  "traceId": ""
}
```

## OpenAPI v1 —— Token 自查端点。

&lt;p&gt;**不带 {@code @OpenApiScope} 注解**：interceptor 仍校验 token / IP / 频率，
但跳过 scope 校验。任何合法 token 都能调，用于：
&lt;ul&gt;
  &lt;li&gt;LLM Agent 启动时拿到&quot;我属于哪档套餐 / 拥有哪些 scope&quot;，避免越权调用导致 403&lt;/li&gt;
  &lt;li&gt;客户端集成时验证 token 是否就绪 + 套餐是否到位&lt;/li&gt;
  &lt;li&gt;排障：401/403 时第一步先调 whoami 看 token 状态&lt;/li&gt;
&lt;/ul&gt;
### 
**URL:** /openapi/v1/whoami;	/openapi/v1/token/info

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/whoami'
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|object|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─ownerName|string|调用方名称（签发时录入）|-|
|└─tokenPrefix|string|Token 前缀（脱敏，不含完整 token）|-|
|└─tier|string|套餐档位：FREE / PRO / MAX / ADMIN / CUSTOM（3 档对外，详见 docs/openapi-packages.md）|-|
|└─tierLabel|string|套餐中文名|-|
|└─scopes|array|拥有的 scope 列表（已展开通配符 stock.* → 全部 stock.xxx）|-|
|└─adminWildcard|boolean|是否含管理员通配（"*"）|-|
|└─rateLimitPerMin|int32|每分钟请求上限|-|
|└─allowedPaths|string|单接口级路径白/黑名单 CSV（方案 B）。null/空 = 不限路径（仅 scope 控制）；<br/>非空时即便 scope 覆盖某接口，仍仅放开 / 排除这些具体路径。普通项=允许、{@code !} 前缀=拒绝。|-|
|└─clientIp|string|当前请求来源 IP（确认 IP 校验已通过）|-|
|└─llmHint|string|给 LLM 的中文权限说明（直接拼到 system prompt 用）|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": {
    "ownerName": "",
    "tokenPrefix": "",
    "tier": "",
    "tierLabel": "",
    "scopes": [
      ""
    ],
    "adminWildcard": true,
    "rateLimitPerMin": 0,
    "allowedPaths": "",
    "clientIp": "",
    "llmHint": ""
  },
  "traceId": ""
}
```

## OpenAPI v1 —— 券商研报 / 卖方评级 / 月度金股端点（{@code stock.research} scope，Plus 套餐及以上）。

&lt;p&gt;覆盖 3 张 PG 表的 3 个端点：
&lt;ul&gt;
  &lt;li&gt;{@code POST /openapi/v1/stock/research/report} —— 券商研究报告（含行业级研报）&lt;/li&gt;
  &lt;li&gt;{@code POST /openapi/v1/stock/research/report-rc} —— 券商盈利预测 + 评级 + 目标价&lt;/li&gt;
  &lt;li&gt;{@code POST /openapi/v1/stock/research/broker-recommend} —— 券商月度金股推荐&lt;/li&gt;
&lt;/ul&gt;

&lt;p&gt;全部 {@code @OpenApiScope(&quot;stock.research&quot;)}，已加入 Pro / Max / Plus / Ultra 套餐。&lt;/p&gt;
### 券商研究报告（{@code stock_research_report}）。<br><br>&lt;b&gt;用途&lt;/b&gt;：跟踪机构覆盖情况、研报主题热度。{@code tsCode} 可空，<br>行业级 / 策略级研报的 {@code tsCode} 为空串（可按 {@code org}/日期范围检索）。<br>按 {@code trade_date DESC} 返回最新研报在前。
**URL:** /openapi/v1/stock/research/report

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 券商研究报告（{@code stock_research_report}）。

<p><b>用途</b>：跟踪机构覆盖情况、研报主题热度。{@code tsCode} 可空，
行业级 / 策略级研报的 {@code tsCode} 为空串（可按 {@code org}/日期范围检索）。
<p>按 {@code trade_date DESC} 返回最新研报在前。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|page|int32|false|第几页，从 1 起。默认 1。0 / 负数会被当成 1。|-|
|size|int32|false|每页记录数。默认 50，硬上限 {@value #MAX_SIZE}。<br/><p>传入超过 {@value #MAX_SIZE} 时会被自动截断到 {@value #MAX_SIZE}（不报错）。</p>|-|
|tsCode|string|false|股票代码（带交易所后缀），如 {@code "600519.SH"}。<br/><p>三端点均可空（不传则按日期范围 / 月度返回）。</p>|-|
|startDate|string|false|起始日期，格式 {@code YYYYMMDD}。可空。|-|
|endDate|string|false|结束日期，格式 {@code YYYYMMDD}。可空。|-|
|org|string|false|研究机构 / 券商名称过滤。可空。<br/><p>report-rc 对应 {@code org_name}，broker-recommend 对应 {@code broker}，research/report 对应 {@code inst_csname}。</p>|-|
|rating|string|false|评级过滤，仅 report-rc 端点使用：如 {@code "买入"} / {@code "增持"} / {@code "中性"}。可空。|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/stock/research/report?page=0&size=0&rating=&org=&endDate=&tsCode=&startDate='
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─tradeDate|string|报告日期|-|
|└─tsCode|string|股票代码（行业研报可能为空字符串）|-|
|└─title|string|报告标题|-|
|└─abstr|string|报告摘要|-|
|└─reportType|string|报告类型（如 公司研究 / 行业研究 / 策略报告）|-|
|└─author|string|作者|-|
|└─name|string|股票 / 行业名称|-|
|└─instCsname|string|研究机构中文名|-|
|└─indName|string|行业名称|-|
|└─url|string|报告 URL（可点击查看 PDF / 详情）|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "tradeDate": "yyyy-MM-dd HH:mm:ss",
      "tsCode": "",
      "title": "",
      "abstr": "",
      "reportType": "",
      "author": "",
      "name": "",
      "instCsname": "",
      "indName": "",
      "url": ""
    }
  ],
  "traceId": ""
}
```

### 券商盈利预测 + 评级 + 目标价（{@code stock_report_rc}）。<br><br>&lt;b&gt;用途&lt;/b&gt;：卖方一致预期跟踪，可做&amp;quot;卖方共识 vs 实际财报&amp;quot;对比、<br>&amp;quot;评级升降事件驱动策略&amp;quot;等。{@code rating} 可选过滤（如 {@code &amp;quot;买入&amp;quot;}）。<br>关键字段：{@code eps / pe / roe / maxPrice / minPrice / rating}。<br>按 {@code report_date DESC} 返回最近预测在前。
**URL:** /openapi/v1/stock/research/report-rc

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 券商盈利预测 + 评级 + 目标价（{@code stock_report_rc}）。

<p><b>用途</b>：卖方一致预期跟踪，可做"卖方共识 vs 实际财报"对比、
"评级升降事件驱动策略"等。{@code rating} 可选过滤（如 {@code "买入"}）。
<p>关键字段：{@code eps / pe / roe / maxPrice / minPrice / rating}。
<p>按 {@code report_date DESC} 返回最近预测在前。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|page|int32|false|第几页，从 1 起。默认 1。0 / 负数会被当成 1。|-|
|size|int32|false|每页记录数。默认 50，硬上限 {@value #MAX_SIZE}。<br/><p>传入超过 {@value #MAX_SIZE} 时会被自动截断到 {@value #MAX_SIZE}（不报错）。</p>|-|
|tsCode|string|false|股票代码（带交易所后缀），如 {@code "600519.SH"}。<br/><p>三端点均可空（不传则按日期范围 / 月度返回）。</p>|-|
|startDate|string|false|起始日期，格式 {@code YYYYMMDD}。可空。|-|
|endDate|string|false|结束日期，格式 {@code YYYYMMDD}。可空。|-|
|org|string|false|研究机构 / 券商名称过滤。可空。<br/><p>report-rc 对应 {@code org_name}，broker-recommend 对应 {@code broker}，research/report 对应 {@code inst_csname}。</p>|-|
|rating|string|false|评级过滤，仅 report-rc 端点使用：如 {@code "买入"} / {@code "增持"} / {@code "中性"}。可空。|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/stock/research/report-rc?page=0&size=0&rating=&endDate=&tsCode=&org=&startDate='
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─tsCode|string|TS 代码|-|
|└─reportDate|string|报告日期|-|
|└─name|string|股票名称|-|
|└─reportTitle|string|报告标题|-|
|└─reportType|string|报告类型|-|
|└─classify|string|分类|-|
|└─orgName|string|研究机构|-|
|└─authorName|string|作者|-|
|└─quarter|string|预测季度（如 {@code "2024Q4"}）|-|
|└─opRt|number|营业收入预测（亿元）|-|
|└─opPr|number|营业利润预测（亿元）|-|
|└─tp|number|利润总额预测（亿元）|-|
|└─np|number|净利润预测（亿元）|-|
|└─eps|number|每股收益预测（元）|-|
|└─pe|number|预测市盈率|-|
|└─rd|number|股息率预测（%）|-|
|└─roe|number|预测 ROE（%）|-|
|└─evEbitda|number|EV/EBITDA 估值倍数|-|
|└─rating|string|评级（买入 / 增持 / 中性 / 减持 / 卖出）|-|
|└─maxPrice|number|目标价上限|-|
|└─minPrice|number|目标价下限|-|
|└─impDg|string|重要程度（A / B / C）|-|
|└─createTime|string|发布时间字符串（Tushare 原样返回）|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "tsCode": "",
      "reportDate": "yyyy-MM-dd HH:mm:ss",
      "name": "",
      "reportTitle": "",
      "reportType": "",
      "classify": "",
      "orgName": "",
      "authorName": "",
      "quarter": "",
      "opRt": 0,
      "opPr": 0,
      "tp": 0,
      "np": 0,
      "eps": 0,
      "pe": 0,
      "rd": 0,
      "roe": 0,
      "evEbitda": 0,
      "rating": "",
      "maxPrice": 0,
      "minPrice": 0,
      "impDg": "",
      "createTime": ""
    }
  ],
  "traceId": ""
}
```

### 券商月度金股推荐（{@code stock_broker_recommend}）。<br><br>&lt;b&gt;用途&lt;/b&gt;：跟踪各大券商每月推荐的&amp;quot;金股&amp;quot;组合，做&amp;quot;金股共识度&amp;quot;分析<br>（同一月份多家券商共推的票）或回测&amp;quot;金股池&amp;quot;超额收益。<br>{@code startDate} / {@code endDate} 自动截取前 6 位转 YYYYMM 与 DB 的 {@code month} 列比对。<br>{@code org} 用于按券商名称过滤。按 {@code month DESC} 返回最近月份在前。
**URL:** /openapi/v1/stock/research/broker-recommend

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 券商月度金股推荐（{@code stock_broker_recommend}）。

<p><b>用途</b>：跟踪各大券商每月推荐的"金股"组合，做"金股共识度"分析
（同一月份多家券商共推的票）或回测"金股池"超额收益。
<p>{@code startDate} / {@code endDate} 自动截取前 6 位转 YYYYMM 与 DB 的 {@code month} 列比对。
<p>{@code org} 用于按券商名称过滤。按 {@code month DESC} 返回最近月份在前。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|page|int32|false|第几页，从 1 起。默认 1。0 / 负数会被当成 1。|-|
|size|int32|false|每页记录数。默认 50，硬上限 {@value #MAX_SIZE}。<br/><p>传入超过 {@value #MAX_SIZE} 时会被自动截断到 {@value #MAX_SIZE}（不报错）。</p>|-|
|tsCode|string|false|股票代码（带交易所后缀），如 {@code "600519.SH"}。<br/><p>三端点均可空（不传则按日期范围 / 月度返回）。</p>|-|
|startDate|string|false|起始日期，格式 {@code YYYYMMDD}。可空。|-|
|endDate|string|false|结束日期，格式 {@code YYYYMMDD}。可空。|-|
|org|string|false|研究机构 / 券商名称过滤。可空。<br/><p>report-rc 对应 {@code org_name}，broker-recommend 对应 {@code broker}，research/report 对应 {@code inst_csname}。</p>|-|
|rating|string|false|评级过滤，仅 report-rc 端点使用：如 {@code "买入"} / {@code "增持"} / {@code "中性"}。可空。|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/stock/research/broker-recommend?page=0&size=0&endDate=&org=&startDate=&tsCode=&rating='
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─month|string|推荐月度 YYYYMM|-|
|└─broker|string|推荐券商|-|
|└─tsCode|string|推荐股票代码（带交易所后缀）|-|
|└─name|string|股票名称|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "month": "",
      "broker": "",
      "tsCode": "",
      "name": ""
    }
  ],
  "traceId": ""
}
```

## OpenAPI v1 —— 选股模型结果端点（stock.selection scope）。

&lt;p&gt;从 site internal 阶段 11 迁移：
&lt;ol&gt;
  &lt;li&gt;ML 智能选股：{@code /ml/execute}（异步触发 Python 服务）+ {@code /ml/results}&lt;/li&gt;
  &lt;li&gt;动量博弈选股：{@code /momentum/execute} + {@code /momentum/results}&lt;/li&gt;
  &lt;li&gt;长期价值选股：{@code /value/execute} + {@code /value/results}&lt;/li&gt;
&lt;/ol&gt;

&lt;p&gt;套餐归属：Ultra（旗舰）。

&lt;p&gt;注意：
&lt;ul&gt;
  &lt;li&gt;execute 端点是触发型（{@code ApiResultModel&lt;Void&gt;}），异步在后端调度&lt;/li&gt;
  &lt;li&gt;results 端点是查询型，返回当前 / 历史日期的选股结果&lt;/li&gt;
&lt;/ul&gt;
### 触发 Python ML 服务执行选股（异步）。tradeDate 为 yyyyMMdd。
**URL:** /openapi/v1/stock/selection/ml/execute

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 触发 Python ML 服务执行选股（异步）。tradeDate 为 yyyyMMdd。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|page|int32|false|第几页，从 1 起。默认 1。0 / 负数会被当成 1。|-|
|size|int32|false|每页记录数。默认 50，硬上限 {@value #MAX_SIZE}。<br/><p>传入超过 {@value #MAX_SIZE} 时会被自动截断到 {@value #MAX_SIZE}（不报错）。</p>|-|
|tradeDate|string|false|选股交易日，格式 {@code YYYYMMDD}（如 {@code "20260430"}）。<br/><p>可空，不传时取最新模型运行日。</p>|-|
|minScore|number|false|最低 ML 得分阈值（{@code 0.0} ~ {@code 1.0}）。可选过滤。<br/><p>{@code 0.6} = 高质量门槛；{@code 0.8} = 强信号。分数越高代表上涨概率越大。</p>|-|
|signalType|string|false|信号类型过滤。<br/><br/><ul><br/>  <li>{@code "BUY"} —— 买入信号（最常用）</li><br/>  <li>{@code "HOLD"} —— 持有 / 观望</li><br/>  <li>{@code "WATCH"} —— 关注（边缘信号）</li><br/></ul><br/><br/><p>可空 = 不过滤，三种都返回。</p>|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/stock/selection/ml/execute?page=0&size=0&minScore=0&tradeDate=&signalType='
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|object|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "traceId": ""
}
```

### 拉取 ML 选股结果。可按日期 / 信号类型（BUY/HOLD/WATCH）/ 最低 ML 得分过滤。
**URL:** /openapi/v1/stock/selection/ml/results

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 拉取 ML 选股结果。可按日期 / 信号类型（BUY/HOLD/WATCH）/ 最低 ML 得分过滤。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|page|int32|false|第几页，从 1 起。默认 1。0 / 负数会被当成 1。|-|
|size|int32|false|每页记录数。默认 50，硬上限 {@value #MAX_SIZE}。<br/><p>传入超过 {@value #MAX_SIZE} 时会被自动截断到 {@value #MAX_SIZE}（不报错）。</p>|-|
|tradeDate|string|false|选股交易日，格式 {@code YYYYMMDD}（如 {@code "20260430"}）。<br/><p>可空，不传时取最新模型运行日。</p>|-|
|minScore|number|false|最低 ML 得分阈值（{@code 0.0} ~ {@code 1.0}）。可选过滤。<br/><p>{@code 0.6} = 高质量门槛；{@code 0.8} = 强信号。分数越高代表上涨概率越大。</p>|-|
|signalType|string|false|信号类型过滤。<br/><br/><ul><br/>  <li>{@code "BUY"} —— 买入信号（最常用）</li><br/>  <li>{@code "HOLD"} —— 持有 / 观望</li><br/>  <li>{@code "WATCH"} —— 关注（边缘信号）</li><br/></ul><br/><br/><p>可空 = 不过滤，三种都返回。</p>|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/stock/selection/ml/results?page=0&size=0&minScore=0&tradeDate=&signalType='
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─tradeDate|string|交易日期|-|
|└─tsCode|string|股票代码|-|
|└─name|string|股票名称|-|
|└─mlScore|number|ML综合得分 (0~1)|-|
|└─mlRank|int32|当日排名|-|
|└─signalType|string|信号类型: BUY/HOLD/WATCH|-|
|└─ma20Dev|number|MA20乖离率|-|
|└─rsi6|number|RSI(6)|-|
|└─macdHist|number|MACD柱状图|-|
|└─mainForceNetRatio|number|主力净流入比|-|
|└─momentum5d|number|5日动量|-|
|└─volatility20d|number|20日波动率|-|
|└─peTtm|number|滚动市盈率|-|
|└─pb|number|市净率|-|
|└─totalMv|number|总市值(万元)|-|
|└─turnoverRate|number|换手率(%)|-|
|└─modelVersion|string|模型版本|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "tradeDate": "",
      "tsCode": "",
      "name": "",
      "mlScore": 0,
      "mlRank": 0,
      "signalType": "",
      "ma20Dev": 0,
      "rsi6": 0,
      "macdHist": 0,
      "mainForceNetRatio": 0,
      "momentum5d": 0,
      "volatility20d": 0,
      "peTtm": 0,
      "pb": 0,
      "totalMv": 0,
      "turnoverRate": 0,
      "modelVersion": ""
    }
  ],
  "traceId": ""
}
```

### 触发动量博弈选股。
**URL:** /openapi/v1/stock/selection/momentum/execute

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 触发动量博弈选股。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|page|int32|false|第几页，从 1 起。默认 1。0 / 负数会被当成 1。|-|
|size|int32|false|每页记录数。默认 50，硬上限 {@value #MAX_SIZE}。<br/><p>传入超过 {@value #MAX_SIZE} 时会被自动截断到 {@value #MAX_SIZE}（不报错）。</p>|-|
|tradeDate|string|false|选股交易日，格式 {@code YYYYMMDD}。可空，不传时取最新一日。|-|
|minScore|number|false|最低综合得分阈值。可选过滤。{@code 0.6} 高质量门槛。|-|
|minConceptCount|int32|false|最少概念叠加数（可选过滤）。<br/><p>例如 {@code 3} 表示"至少叠加 3 个热门概念"——既有 AI 又有华为又有车的票更易爆炒。</p>|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/stock/selection/momentum/execute?page=0&size=0&minScore=0&minConceptCount=0&tradeDate='
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|object|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "traceId": ""
}
```

### 拉取动量选股结果。可按最低综合得分 / 最少概念叠加数过滤。
**URL:** /openapi/v1/stock/selection/momentum/results

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 拉取动量选股结果。可按最低综合得分 / 最少概念叠加数过滤。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|page|int32|false|第几页，从 1 起。默认 1。0 / 负数会被当成 1。|-|
|size|int32|false|每页记录数。默认 50，硬上限 {@value #MAX_SIZE}。<br/><p>传入超过 {@value #MAX_SIZE} 时会被自动截断到 {@value #MAX_SIZE}（不报错）。</p>|-|
|tradeDate|string|false|选股交易日，格式 {@code YYYYMMDD}。可空，不传时取最新一日。|-|
|minScore|number|false|最低综合得分阈值。可选过滤。{@code 0.6} 高质量门槛。|-|
|minConceptCount|int32|false|最少概念叠加数（可选过滤）。<br/><p>例如 {@code 3} 表示"至少叠加 3 个热门概念"——既有 AI 又有华为又有车的票更易爆炒。</p>|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/stock/selection/momentum/results?page=0&size=0&minScore=0&minConceptCount=0&tradeDate='
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─tsCode|string|No comments found.|-|
|└─name|string|No comments found.|-|
|└─tradeDate|string|No comments found.|-|
|└─topPlateCode|string|最强所属板块|-|
|└─topPlateName|string|No comments found.|-|
|└─plateNetAmount|number|No comments found.|-|
|└─platePctChange|number|No comments found.|-|
|└─conceptCount|int32|多概念叠加|-|
|└─conceptNames|string|No comments found.|-|
|└─macdSignal|string|技术面|-|
|└─priceVsMa20|number|No comments found.|-|
|└─stockPct5d|number|No comments found.|-|
|└─platePct5d|number|No comments found.|-|
|└─mainNetInflow|number|资金流|-|
|└─mainForceSignal|string|No comments found.|-|
|└─closePrice|number|行情|-|
|└─pctChange|number|No comments found.|-|
|└─turnoverRate|number|No comments found.|-|
|└─totalMv|number|No comments found.|-|
|└─totalScore|number|评分|-|
|└─scoreDetail|string|No comments found.|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "tsCode": "",
      "name": "",
      "tradeDate": "",
      "topPlateCode": "",
      "topPlateName": "",
      "plateNetAmount": 0,
      "platePctChange": 0,
      "conceptCount": 0,
      "conceptNames": "",
      "macdSignal": "",
      "priceVsMa20": 0,
      "stockPct5d": 0,
      "platePct5d": 0,
      "mainNetInflow": 0,
      "mainForceSignal": "",
      "closePrice": 0,
      "pctChange": 0,
      "turnoverRate": 0,
      "totalMv": 0,
      "totalScore": 0,
      "scoreDetail": ""
    }
  ],
  "traceId": ""
}
```

### 触发价值选股。
**URL:** /openapi/v1/stock/selection/value/execute

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 触发价值选股。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|page|int32|false|第几页，从 1 起。默认 1。0 / 负数会被当成 1。|-|
|size|int32|false|每页记录数。默认 50，硬上限 {@value #MAX_SIZE}。<br/><p>传入超过 {@value #MAX_SIZE} 时会被自动截断到 {@value #MAX_SIZE}（不报错）。</p>|-|
|tradeDate|string|false|选股交易日，格式 {@code YYYYMMDD}。可空，不传时取最新一日。|-|
|l1Code|string|false|申万一级行业代码（可选过滤）。<br/><br/><p><b>示例</b>：</p><br/><ul><br/>  <li>{@code "801080"} —— 电子</li><br/>  <li>{@code "801120"} —— 食品饮料</li><br/>  <li>{@code "801780"} —— 银行</li><br/></ul><br/><br/><p>用于"在 X 行业里找估值合理的票"。可空 = 全行业。</p>|-|
|minScore|number|false|最低综合得分阈值。可选过滤。|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/stock/selection/value/execute?page=0&size=0&minScore=0&l1Code=&tradeDate='
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|object|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "traceId": ""
}
```

### 拉取价值选股结果。可按行业 / 最低综合得分过滤。
**URL:** /openapi/v1/stock/selection/value/results

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 拉取价值选股结果。可按行业 / 最低综合得分过滤。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|page|int32|false|第几页，从 1 起。默认 1。0 / 负数会被当成 1。|-|
|size|int32|false|每页记录数。默认 50，硬上限 {@value #MAX_SIZE}。<br/><p>传入超过 {@value #MAX_SIZE} 时会被自动截断到 {@value #MAX_SIZE}（不报错）。</p>|-|
|tradeDate|string|false|选股交易日，格式 {@code YYYYMMDD}。可空，不传时取最新一日。|-|
|l1Code|string|false|申万一级行业代码（可选过滤）。<br/><br/><p><b>示例</b>：</p><br/><ul><br/>  <li>{@code "801080"} —— 电子</li><br/>  <li>{@code "801120"} —— 食品饮料</li><br/>  <li>{@code "801780"} —— 银行</li><br/></ul><br/><br/><p>用于"在 X 行业里找估值合理的票"。可空 = 全行业。</p>|-|
|minScore|number|false|最低综合得分阈值。可选过滤。|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/stock/selection/value/results?page=0&size=0&minScore=0&l1Code=&tradeDate='
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─tsCode|string|股票代码|-|
|└─name|string|股票名称|-|
|└─tradeDate|string|选股日期|-|
|└─l1Code|string|申万一级行业|-|
|└─l1Name|string|No comments found.|-|
|└─l2Code|string|申万二级行业|-|
|└─l2Name|string|No comments found.|-|
|└─l3Code|string|申万三级行业|-|
|└─l3Name|string|No comments found.|-|
|└─roeLatest|number|最新年报ROE(%)|-|
|└─roeAvg3y|number|近3年平均ROE(%)|-|
|└─debtToAssets|number|资产负债率(%)|-|
|└─debtIndustryRank|number|负债率行业分位(0~1)|-|
|└─ocfpsLatest|number|最新经营现金流/股|-|
|└─peTtm|number|当前PE_TTM|-|
|└─pePercentile|number|PE近3年历史分位(0~1)|-|
|└─dvTtm|number|股息率TTM(%)|-|
|└─totalMv|number|总市值(万元)|-|
|└─totalScore|number|综合得分(0~100)|-|
|└─scoreDetail|string|各维度得分JSON|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "tsCode": "",
      "name": "",
      "tradeDate": "",
      "l1Code": "",
      "l1Name": "",
      "l2Code": "",
      "l2Name": "",
      "l3Code": "",
      "l3Name": "",
      "roeLatest": 0,
      "roeAvg3y": 0,
      "debtToAssets": 0,
      "debtIndustryRank": 0,
      "ocfpsLatest": 0,
      "peTtm": 0,
      "pePercentile": 0,
      "dvTtm": 0,
      "totalMv": 0,
      "totalScore": 0,
      "scoreDetail": ""
    }
  ],
  "traceId": ""
}
```

## OpenAPI v1 —— 债券 / 可转债端点（bond scope）。

&lt;p&gt;覆盖 12 张 PG 表的 12 个端点。全部 &lt;code&gt;@OpenApiScope(&quot;bond&quot;)&lt;/code&gt;。

&lt;p&gt;路径分组：
&lt;ul&gt;
  &lt;li&gt;可转债：&lt;code&gt;/openapi/v1/bond/cb/...&lt;/code&gt;&lt;/li&gt;
  &lt;li&gt;回购：&lt;code&gt;/openapi/v1/bond/repo/daily&lt;/code&gt;&lt;/li&gt;
  &lt;li&gt;收益率曲线：&lt;code&gt;/openapi/v1/bond/yc&lt;/code&gt;&lt;/li&gt;
  &lt;li&gt;大宗交易：&lt;code&gt;/openapi/v1/bond/blk&lt;/code&gt; / &lt;code&gt;/blk-detail&lt;/code&gt;&lt;/li&gt;
&lt;/ul&gt;

&lt;p&gt;对应 MCP 工具：见 stock_mcp/src/stock_mcp/tools/bond.py。
### 可转债列表筛选（按代码 / 正股代码 / 简称关键字 / 评级）。所有字段可选。
**URL:** /openapi/v1/bond/cb/list

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 可转债列表筛选（按代码 / 正股代码 / 简称关键字 / 评级）。所有字段可选。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|page|int32|false|第几页，从 1 起。默认 1。0 / 负数会被当成 1。|-|
|size|int32|false|每页记录数。默认 50，硬上限 {@value #MAX_SIZE}。<br/><p>传入超过 {@value #MAX_SIZE} 时会被自动截断到 {@value #MAX_SIZE}（不报错）。</p>|-|
|tsCode|string|false|可转债代码（精确匹配）。<br/><p>例如 {@code "113008.SH"}（沪市）/ {@code "123100.SZ"} / {@code "127XXX.SH"}（深市）。</p>|-|
|stkCode|string|false|正股代码（精确匹配）。用于"找正股是茅台的转债" → {@code stkCode="600519.SH"}。|-|
|nameKeyword|string|false|简称关键字（中文模糊匹配，匹配可转债简称或正股简称）。<br/><p>例如 {@code "电气"} / {@code "茅台"}。</p>|-|
|issueRating|string|false|信用评级（精确匹配）。<br/><br/><ul><br/>  <li>{@code "AAA"} —— 最高级</li><br/>  <li>{@code "AA+"} / {@code "AA"} / {@code "AA-"}</li><br/>  <li>{@code "A+"} 及以下 —— 评级偏低，违约风险增加</li><br/></ul>|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/bond/cb/list?page=0&size=0&issueRating=&stkCode=&tsCode=&nameKeyword='
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─tsCode|string|转债代码（如 113008.SH / 123100.SZ）|-|
|└─bondFullName|string|转债全称|-|
|└─bondShortName|string|转债简称|-|
|└─stkCode|string|正股代码|-|
|└─stkShortName|string|正股简称|-|
|└─maturity|number|期限（年）|-|
|└─par|number|面值|-|
|└─issuePrice|number|发行价格|-|
|└─issueSize|number|发行规模（亿元）|-|
|└─listDate|string|上市日期 YYYYMMDD|-|
|└─delistDate|string|摘牌日期 YYYYMMDD|-|
|└─convPrice|number|当前转股价|-|
|└─maturityDate|string|到期日 YYYYMMDD|-|
|└─couponRate|number|票面利率（%；多档时取首档）|-|
|└─issueRating|string|信用评级（如 AAA / AA+）|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "tsCode": "",
      "bondFullName": "",
      "bondShortName": "",
      "stkCode": "",
      "stkShortName": "",
      "maturity": 0,
      "par": 0,
      "issuePrice": 0,
      "issueSize": 0,
      "listDate": "",
      "delistDate": "",
      "convPrice": 0,
      "maturityDate": "",
      "couponRate": 0,
      "issueRating": ""
    }
  ],
  "traceId": ""
}
```

### 可转债日 K 线（含纯债价值 / 转股价值 / 溢价率）。tsCode 必填，缺日期默认最近 60 天。
**URL:** /openapi/v1/bond/cb/daily

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 可转债日 K 线（含纯债价值 / 转股价值 / 溢价率）。tsCode 必填，缺日期默认最近 60 天。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|page|int32|false|第几页，从 1 起。默认 1。0 / 负数会被当成 1。|-|
|size|int32|false|每页记录数。默认 50，硬上限 {@value #MAX_SIZE}。<br/><p>传入超过 {@value #MAX_SIZE} 时会被自动截断到 {@value #MAX_SIZE}（不报错）。</p>|-|
|tsCode|string|false|债券代码（带交易所后缀）。<b>必填</b>。<br/><br/><p><b>示例</b>：</p><br/><ul><br/>  <li>可转债：{@code "113008.SH"}（沪市）/ {@code "123100.SZ"} / {@code "127XXX.SH"}（深市）</li><br/>  <li>国债逆回购：{@code "204001.SH"}（GC001）/ {@code "131810.SZ"}（R-001）</li><br/></ul>|-|
|startDate|string|false|起始日期，格式 {@code YYYYMMDD}。可空。|-|
|endDate|string|false|结束日期，格式 {@code YYYYMMDD}。可空。|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/bond/cb/daily?page=0&size=0&endDate=&startDate=&tsCode='
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─tsCode|string|可转债代码（带交易所后缀），如 {@code "113008.SH"} / {@code "123100.SZ"}。|-|
|└─tradeDate|string|交易日，格式 {@code YYYYMMDD}。|-|
|└─preClose|number|前收盘价（元）。|-|
|└─open|number|开盘价（元）。|-|
|└─high|number|最高价（元）。|-|
|└─low|number|最低价（元）。|-|
|└─close|number|收盘价（元）。|-|
|└─chg|number|涨跌额|-|
|└─pctChg|number|涨跌幅（%）|-|
|└─vol|number|成交量（手）|-|
|└─amount|number|成交额（千元）|-|
|└─bondValue|number|纯债价值|-|
|└─bondOverRate|number|纯债溢价率（%）|-|
|└─cbValue|number|转股价值|-|
|└─cbOverRate|number|转股溢价率（%）|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "tsCode": "",
      "tradeDate": "",
      "preClose": 0,
      "open": 0,
      "high": 0,
      "low": 0,
      "close": 0,
      "chg": 0,
      "pctChg": 0,
      "vol": 0,
      "amount": 0,
      "bondValue": 0,
      "bondOverRate": 0,
      "cbValue": 0,
      "cbOverRate": 0
    }
  ],
  "traceId": ""
}
```

### 可转债技术因子（cb_factor_pro，含 OHLCV 与 JSONB 动态因子）。tsCode 必填。
**URL:** /openapi/v1/bond/cb/factor

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 可转债技术因子（cb_factor_pro，含 OHLCV 与 JSONB 动态因子）。tsCode 必填。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|page|int32|false|第几页，从 1 起。默认 1。0 / 负数会被当成 1。|-|
|size|int32|false|每页记录数。默认 50，硬上限 {@value #MAX_SIZE}。<br/><p>传入超过 {@value #MAX_SIZE} 时会被自动截断到 {@value #MAX_SIZE}（不报错）。</p>|-|
|tsCode|string|false|债券代码（带交易所后缀）。<b>必填</b>。<br/><br/><p><b>示例</b>：</p><br/><ul><br/>  <li>可转债：{@code "113008.SH"}（沪市）/ {@code "123100.SZ"} / {@code "127XXX.SH"}（深市）</li><br/>  <li>国债逆回购：{@code "204001.SH"}（GC001）/ {@code "131810.SZ"}（R-001）</li><br/></ul>|-|
|startDate|string|false|起始日期，格式 {@code YYYYMMDD}。可空。|-|
|endDate|string|false|结束日期，格式 {@code YYYYMMDD}。可空。|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/bond/cb/factor?page=0&size=0&startDate=&tsCode=&endDate='
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─tsCode|string|可转债代码（带交易所后缀），如 {@code "113008.SH"} / {@code "123100.SZ"}。|-|
|└─tradeDate|string|交易日，格式 {@code YYYYMMDD}。|-|
|└─open|number|开盘价（元）。|-|
|└─close|number|收盘价（元）。|-|
|└─high|number|最高价（元）。|-|
|└─low|number|最低价（元）。|-|
|└─vol|number|成交量（手）。|-|
|└─amount|number|成交额（千元）。|-|
|└─pctChange|number|涨跌幅（%）。|-|
|└─factorData|string|PG JSONB 列原始文本，包含动态因子（如 {@code ma_bfq_5} / {@code macd} / {@code rsi_6} / {@code kdj_k}）。<br/><p>客户端按需自行解析。例如：</p><br/><pre>{"ma_bfq_5": 102.3, "macd": 0.45, "rsi_6": 55.2, "kdj_k": 70.1, ...}</pre>|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "tsCode": "",
      "tradeDate": "",
      "open": 0,
      "close": 0,
      "high": 0,
      "low": 0,
      "vol": 0,
      "amount": 0,
      "pctChange": 0,
      "factorData": ""
    }
  ],
  "traceId": ""
}
```

### 可转债发行（cb_issue）。tsCode 必填，按 ann_date 倒序，可选 startDate/endDate 切窗。
**URL:** /openapi/v1/bond/cb/issue

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 可转债发行（cb_issue）。tsCode 必填，按 ann_date 倒序，可选 startDate/endDate 切窗。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|page|int32|false|第几页，从 1 起。默认 1。0 / 负数会被当成 1。|-|
|size|int32|false|每页记录数。默认 50，硬上限 {@value #MAX_SIZE}。<br/><p>传入超过 {@value #MAX_SIZE} 时会被自动截断到 {@value #MAX_SIZE}（不报错）。</p>|-|
|tsCode|string|false|债券代码（带交易所后缀）。<b>必填</b>。<br/><br/><p><b>示例</b>：</p><br/><ul><br/>  <li>可转债：{@code "113008.SH"}（沪市）/ {@code "123100.SZ"} / {@code "127XXX.SH"}（深市）</li><br/>  <li>国债逆回购：{@code "204001.SH"}（GC001）/ {@code "131810.SZ"}（R-001）</li><br/></ul>|-|
|startDate|string|false|起始日期，格式 {@code YYYYMMDD}。可空。|-|
|endDate|string|false|结束日期，格式 {@code YYYYMMDD}。可空。|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/bond/cb/issue?page=0&size=0&startDate=&endDate=&tsCode='
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─tsCode|string|No comments found.|-|
|└─annDate|string|公告日 YYYYMMDD|-|
|└─resAnnDate|string|中签结果公告日 YYYYMMDD|-|
|└─planIssueSize|number|计划发行规模（亿元）|-|
|└─issueSize|number|实际发行规模（亿元）|-|
|└─issuePrice|number|发行价格|-|
|└─issueType|string|发行方式|-|
|└─issueCost|number|发行费用|-|
|└─onlWinningRate|number|网上中签率（%）|-|
|└─shdRationPrice|number|老股东配售价|-|
|└─offlDeposit|number|网下保证金比例|-|
|└─leadUnderwriter|string|主承销商|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "tsCode": "",
      "annDate": "",
      "resAnnDate": "",
      "planIssueSize": 0,
      "issueSize": 0,
      "issuePrice": 0,
      "issueType": "",
      "issueCost": 0,
      "onlWinningRate": 0,
      "shdRationPrice": 0,
      "offlDeposit": 0,
      "leadUnderwriter": ""
    }
  ],
  "traceId": ""
}
```

### 可转债赎回信息（cb_call）。覆盖到期 / 强赎 / 回售。tsCode 必填，按 ann_date 倒序。
**URL:** /openapi/v1/bond/cb/call

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 可转债赎回信息（cb_call）。覆盖到期 / 强赎 / 回售。tsCode 必填，按 ann_date 倒序。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|page|int32|false|第几页，从 1 起。默认 1。0 / 负数会被当成 1。|-|
|size|int32|false|每页记录数。默认 50，硬上限 {@value #MAX_SIZE}。<br/><p>传入超过 {@value #MAX_SIZE} 时会被自动截断到 {@value #MAX_SIZE}（不报错）。</p>|-|
|tsCode|string|false|债券代码（带交易所后缀）。<b>必填</b>。<br/><br/><p><b>示例</b>：</p><br/><ul><br/>  <li>可转债：{@code "113008.SH"}（沪市）/ {@code "123100.SZ"} / {@code "127XXX.SH"}（深市）</li><br/>  <li>国债逆回购：{@code "204001.SH"}（GC001）/ {@code "131810.SZ"}（R-001）</li><br/></ul>|-|
|startDate|string|false|起始日期，格式 {@code YYYYMMDD}。可空。|-|
|endDate|string|false|结束日期，格式 {@code YYYYMMDD}。可空。|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/bond/cb/call?page=0&size=0&startDate=&endDate=&tsCode='
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─tsCode|string|No comments found.|-|
|└─callType|string|赎回类型：到期赎回 / 强赎 / 回售 等|-|
|└─isCall|string|是否实际触发赎回 Y / N|-|
|└─annDate|string|公告日 YYYYMMDD|-|
|└─callDate|string|赎回日 YYYYMMDD|-|
|└─callPrice|number|赎回价（不含税）|-|
|└─callPriceTax|number|赎回价（含税）|-|
|└─callVol|number|赎回数量（万张）|-|
|└─callAmount|number|赎回金额（亿元）|-|
|└─paymentDate|string|兑付日 YYYYMMDD|-|
|└─callRegDate|string|赎回登记日 YYYYMMDD|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "tsCode": "",
      "callType": "",
      "isCall": "",
      "annDate": "",
      "callDate": "",
      "callPrice": 0,
      "callPriceTax": 0,
      "callVol": 0,
      "callAmount": 0,
      "paymentDate": "",
      "callRegDate": ""
    }
  ],
  "traceId": ""
}
```

### 可转债票面利率分档（cb_rate，每只转债 5–7 行）。tsCode 必填，不切日期。
**URL:** /openapi/v1/bond/cb/rate

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 可转债票面利率分档（cb_rate，每只转债 5–7 行）。tsCode 必填，不切日期。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|page|int32|false|第几页，从 1 起。默认 1。0 / 负数会被当成 1。|-|
|size|int32|false|每页记录数。默认 50，硬上限 {@value #MAX_SIZE}。<br/><p>传入超过 {@value #MAX_SIZE} 时会被自动截断到 {@value #MAX_SIZE}（不报错）。</p>|-|
|tsCode|string|false|债券代码（带交易所后缀）。<b>必填</b>。<br/><br/><p><b>示例</b>：</p><br/><ul><br/>  <li>可转债：{@code "113008.SH"}（沪市）/ {@code "123100.SZ"} / {@code "127XXX.SH"}（深市）</li><br/>  <li>国债逆回购：{@code "204001.SH"}（GC001）/ {@code "131810.SZ"}（R-001）</li><br/></ul>|-|
|startDate|string|false|起始日期，格式 {@code YYYYMMDD}。可空。|-|
|endDate|string|false|结束日期，格式 {@code YYYYMMDD}。可空。|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/bond/cb/rate?page=0&size=0&startDate=&tsCode=&endDate='
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─tsCode|string|No comments found.|-|
|└─rateFreq|int32|计息频率（次 / 年）|-|
|└─rateStartDate|string|计息起始日 YYYYMMDD|-|
|└─rateEndDate|string|计息截止日 YYYYMMDD|-|
|└─couponRate|number|票面利率（%）|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "tsCode": "",
      "rateFreq": 0,
      "rateStartDate": "",
      "rateEndDate": "",
      "couponRate": 0
    }
  ],
  "traceId": ""
}
```

### 可转债转股价变动（cb_price_chg）。tsCode 必填，按 change_date 倒序。
**URL:** /openapi/v1/bond/cb/price-chg

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 可转债转股价变动（cb_price_chg）。tsCode 必填，按 change_date 倒序。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|page|int32|false|第几页，从 1 起。默认 1。0 / 负数会被当成 1。|-|
|size|int32|false|每页记录数。默认 50，硬上限 {@value #MAX_SIZE}。<br/><p>传入超过 {@value #MAX_SIZE} 时会被自动截断到 {@value #MAX_SIZE}（不报错）。</p>|-|
|tsCode|string|false|债券代码（带交易所后缀）。<b>必填</b>。<br/><br/><p><b>示例</b>：</p><br/><ul><br/>  <li>可转债：{@code "113008.SH"}（沪市）/ {@code "123100.SZ"} / {@code "127XXX.SH"}（深市）</li><br/>  <li>国债逆回购：{@code "204001.SH"}（GC001）/ {@code "131810.SZ"}（R-001）</li><br/></ul>|-|
|startDate|string|false|起始日期，格式 {@code YYYYMMDD}。可空。|-|
|endDate|string|false|结束日期，格式 {@code YYYYMMDD}。可空。|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/bond/cb/price-chg?page=0&size=0&tsCode=&startDate=&endDate='
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─tsCode|string|No comments found.|-|
|└─bondShortName|string|简称（冗余）|-|
|└─publishDate|string|公告日 YYYYMMDD|-|
|└─changeDate|string|转股价生效日 YYYYMMDD|-|
|└─convertPriceInitial|number|初始转股价|-|
|└─convertpriceBef|number|调整前转股价|-|
|└─convertpriceAft|number|调整后转股价|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "tsCode": "",
      "bondShortName": "",
      "publishDate": "",
      "changeDate": "",
      "convertPriceInitial": 0,
      "convertpriceBef": 0,
      "convertpriceAft": 0
    }
  ],
  "traceId": ""
}
```

### 可转债转股结果（cb_share）。tsCode 必填，按 end_date 倒序。
**URL:** /openapi/v1/bond/cb/share

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 可转债转股结果（cb_share）。tsCode 必填，按 end_date 倒序。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|page|int32|false|第几页，从 1 起。默认 1。0 / 负数会被当成 1。|-|
|size|int32|false|每页记录数。默认 50，硬上限 {@value #MAX_SIZE}。<br/><p>传入超过 {@value #MAX_SIZE} 时会被自动截断到 {@value #MAX_SIZE}（不报错）。</p>|-|
|tsCode|string|false|债券代码（带交易所后缀）。<b>必填</b>。<br/><br/><p><b>示例</b>：</p><br/><ul><br/>  <li>可转债：{@code "113008.SH"}（沪市）/ {@code "123100.SZ"} / {@code "127XXX.SH"}（深市）</li><br/>  <li>国债逆回购：{@code "204001.SH"}（GC001）/ {@code "131810.SZ"}（R-001）</li><br/></ul>|-|
|startDate|string|false|起始日期，格式 {@code YYYYMMDD}。可空。|-|
|endDate|string|false|结束日期，格式 {@code YYYYMMDD}。可空。|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/bond/cb/share?page=0&size=0&tsCode=&endDate=&startDate='
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─tsCode|string|可转债代码（带交易所后缀），如 {@code "113008.SH"}。|-|
|└─bondShortName|string|可转债简称，如 {@code "电气转债"}。|-|
|└─publishDate|string|公告日 YYYYMMDD|-|
|└─endDate|string|截止日 YYYYMMDD（按 end_date 唯一）|-|
|└─issueSize|number|发行规模|-|
|└─convertPriceInitial|number|初始转股价|-|
|└─convertPrice|number|当前转股价|-|
|└─convertVal|number|转股金额（区间内）|-|
|└─convertVol|number|转股数量|-|
|└─convertRatio|number|转股比例（区间内）|-|
|└─accConvertVal|number|累计转股金额|-|
|└─accConvertVol|number|累计转股数量|-|
|└─accConvertRatio|number|累计转股比例|-|
|└─remainSize|number|剩余规模|-|
|└─totalShares|number|总股本（正股，万股）|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "tsCode": "",
      "bondShortName": "",
      "publishDate": "",
      "endDate": "",
      "issueSize": 0,
      "convertPriceInitial": 0,
      "convertPrice": 0,
      "convertVal": 0,
      "convertVol": 0,
      "convertRatio": 0,
      "accConvertVal": 0,
      "accConvertVol": 0,
      "accConvertRatio": 0,
      "remainSize": 0,
      "totalShares": 0
    }
  ],
  "traceId": ""
}
```

### 国债逆回购日行情（repo_daily）。tsCode 必填（如 204001.SH = GC001）。
**URL:** /openapi/v1/bond/repo/daily

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 国债逆回购日行情（repo_daily）。tsCode 必填（如 204001.SH = GC001）。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|page|int32|false|第几页，从 1 起。默认 1。0 / 负数会被当成 1。|-|
|size|int32|false|每页记录数。默认 50，硬上限 {@value #MAX_SIZE}。<br/><p>传入超过 {@value #MAX_SIZE} 时会被自动截断到 {@value #MAX_SIZE}（不报错）。</p>|-|
|tsCode|string|false|债券代码（带交易所后缀）。<b>必填</b>。<br/><br/><p><b>示例</b>：</p><br/><ul><br/>  <li>可转债：{@code "113008.SH"}（沪市）/ {@code "123100.SZ"} / {@code "127XXX.SH"}（深市）</li><br/>  <li>国债逆回购：{@code "204001.SH"}（GC001）/ {@code "131810.SZ"}（R-001）</li><br/></ul>|-|
|startDate|string|false|起始日期，格式 {@code YYYYMMDD}。可空。|-|
|endDate|string|false|结束日期，格式 {@code YYYYMMDD}。可空。|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/bond/repo/daily?page=0&size=0&startDate=&tsCode=&endDate='
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─tsCode|string|回购代码（带交易所后缀），如 {@code "204001.SH"}（GC001）/ {@code "131810.SZ"}（R-001）。|-|
|└─tradeDate|string|交易日，格式 {@code YYYYMMDD}。|-|
|└─repoMaturity|string|回购期限。<br/><ul><br/>  <li>{@code "GC001"} —— 1 天（最常用，反映短期资金面）</li><br/>  <li>{@code "GC007"} —— 7 天</li><br/>  <li>{@code "GC014"} —— 14 天</li><br/>  <li>{@code "GC028"} —— 28 天</li><br/>  <li>{@code "GC091"} —— 91 天</li><br/>  <li>{@code "GC182"} —— 182 天</li><br/></ul>|-|
|└─preClose|number|前收盘价。|-|
|└─open|number|开盘价。|-|
|└─high|number|最高价。|-|
|└─low|number|最低价。|-|
|└─close|number|收盘价。|-|
|└─weight|number|加权平均价|-|
|└─weightR|number|加权平均利率（%）|-|
|└─amount|number|成交额（千元）|-|
|└─num|int32|成交笔数|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "tsCode": "",
      "tradeDate": "",
      "repoMaturity": "",
      "preClose": 0,
      "open": 0,
      "high": 0,
      "low": 0,
      "close": 0,
      "weight": 0,
      "weightR": 0,
      "amount": 0,
      "num": 0
    }
  ],
  "traceId": ""
}
```

### 国债收益率曲线（yc_cb）。<br><br>建议用法：单日全期限做&amp;quot;利率曲线快照&amp;quot;，区间单期限做&amp;quot;利率走势&amp;quot;。<br>curveType（0 到期 / 1 即期）+ curveTerm（年）可选过滤。
**URL:** /openapi/v1/bond/yc

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 国债收益率曲线（yc_cb）。

<p>建议用法：单日全期限做"利率曲线快照"，区间单期限做"利率走势"。
curveType（0 到期 / 1 即期）+ curveTerm（年）可选过滤。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|page|int32|false|第几页，从 1 起。默认 1。0 / 负数会被当成 1。|-|
|size|int32|false|每页记录数。默认 50，硬上限 {@value #MAX_SIZE}。<br/><p>传入超过 {@value #MAX_SIZE} 时会被自动截断到 {@value #MAX_SIZE}（不报错）。</p>|-|
|tradeDate|string|false|单日，格式 {@code YYYYMMDD}。与 {@link #startDate} / {@link #endDate} 二选一。|-|
|startDate|string|false|起始日期，格式 {@code YYYYMMDD}。|-|
|endDate|string|false|结束日期，格式 {@code YYYYMMDD}。|-|
|tsCode|string|false|债券代码（精确匹配）。可选过滤单只。|-|
|curveType|string|false|收益率曲线类型（仅 {@code /bond/yc} 端点用）。<br/><br/><ul><br/>  <li>{@code "0"} —— 到期收益率（最常用）</li><br/>  <li>{@code "1"} —— 即期收益率</li><br/></ul>|-|
|curveTerm|string|false|收益率曲线期限（年，仅 {@code /bond/yc} 端点用）。<br/><br/><p><b>常用值</b>：</p><br/><ul><br/>  <li>{@code "0.25"} —— 3 个月</li><br/>  <li>{@code "1"} —— 1 年</li><br/>  <li>{@code "5"} —— 5 年</li><br/>  <li>{@code "10"} —— 10 年（最常关注的长端基准）</li><br/></ul><br/><br/><p>可空 = 返回全期限曲线（画图用）；指定 = 取该期限的时间序列。</p>|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/bond/yc?page=0&size=0&curveType=&curveTerm=&tsCode=&tradeDate=&endDate=&startDate='
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─tradeDate|string|交易日 YYYYMMDD|-|
|└─tsCode|string|曲线代码（如 1001=国债 / 1002=企业债 等）|-|
|└─curveName|string|曲线名称|-|
|└─curveType|string|0 到期 / 1 即期|-|
|└─curveTerm|number|期限（年），如 0.25 / 1 / 5 / 10|-|
|└─yieldRate|number|收益率（%）|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "tradeDate": "",
      "tsCode": "",
      "curveName": "",
      "curveType": "",
      "curveTerm": 0,
      "yieldRate": 0
    }
  ],
  "traceId": ""
}
```

### 债券大宗交易（bond_blk，按 trade_date+ts_code+price 唯一）。<br>至少传 tradeDate 或 startDate/endDate；tsCode 可选。
**URL:** /openapi/v1/bond/blk

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 债券大宗交易（bond_blk，按 trade_date+ts_code+price 唯一）。
至少传 tradeDate 或 startDate/endDate；tsCode 可选。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|page|int32|false|第几页，从 1 起。默认 1。0 / 负数会被当成 1。|-|
|size|int32|false|每页记录数。默认 50，硬上限 {@value #MAX_SIZE}。<br/><p>传入超过 {@value #MAX_SIZE} 时会被自动截断到 {@value #MAX_SIZE}（不报错）。</p>|-|
|tradeDate|string|false|单日，格式 {@code YYYYMMDD}。与 {@link #startDate} / {@link #endDate} 二选一。|-|
|startDate|string|false|起始日期，格式 {@code YYYYMMDD}。|-|
|endDate|string|false|结束日期，格式 {@code YYYYMMDD}。|-|
|tsCode|string|false|债券代码（精确匹配）。可选过滤单只。|-|
|curveType|string|false|收益率曲线类型（仅 {@code /bond/yc} 端点用）。<br/><br/><ul><br/>  <li>{@code "0"} —— 到期收益率（最常用）</li><br/>  <li>{@code "1"} —— 即期收益率</li><br/></ul>|-|
|curveTerm|string|false|收益率曲线期限（年，仅 {@code /bond/yc} 端点用）。<br/><br/><p><b>常用值</b>：</p><br/><ul><br/>  <li>{@code "0.25"} —— 3 个月</li><br/>  <li>{@code "1"} —— 1 年</li><br/>  <li>{@code "5"} —— 5 年</li><br/>  <li>{@code "10"} —— 10 年（最常关注的长端基准）</li><br/></ul><br/><br/><p>可空 = 返回全期限曲线（画图用）；指定 = 取该期限的时间序列。</p>|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/bond/blk?page=0&size=0&curveTerm=&tsCode=&tradeDate=&endDate=&curveType=&startDate='
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─tradeDate|string|交易日 YYYYMMDD|-|
|└─tsCode|string|No comments found.|-|
|└─name|string|简称|-|
|└─price|number|成交价|-|
|└─vol|number|成交量（手）|-|
|└─amount|number|成交额（千元）|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "tradeDate": "",
      "tsCode": "",
      "name": "",
      "price": 0,
      "vol": 0,
      "amount": 0
    }
  ],
  "traceId": ""
}
```

### 债券大宗交易明细（bond_blk_detail，含买卖营业部）。<br>至少传 tradeDate 或 startDate/endDate；tsCode 可选。
**URL:** /openapi/v1/bond/blk-detail

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 债券大宗交易明细（bond_blk_detail，含买卖营业部）。
至少传 tradeDate 或 startDate/endDate；tsCode 可选。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|page|int32|false|第几页，从 1 起。默认 1。0 / 负数会被当成 1。|-|
|size|int32|false|每页记录数。默认 50，硬上限 {@value #MAX_SIZE}。<br/><p>传入超过 {@value #MAX_SIZE} 时会被自动截断到 {@value #MAX_SIZE}（不报错）。</p>|-|
|tradeDate|string|false|单日，格式 {@code YYYYMMDD}。与 {@link #startDate} / {@link #endDate} 二选一。|-|
|startDate|string|false|起始日期，格式 {@code YYYYMMDD}。|-|
|endDate|string|false|结束日期，格式 {@code YYYYMMDD}。|-|
|tsCode|string|false|债券代码（精确匹配）。可选过滤单只。|-|
|curveType|string|false|收益率曲线类型（仅 {@code /bond/yc} 端点用）。<br/><br/><ul><br/>  <li>{@code "0"} —— 到期收益率（最常用）</li><br/>  <li>{@code "1"} —— 即期收益率</li><br/></ul>|-|
|curveTerm|string|false|收益率曲线期限（年，仅 {@code /bond/yc} 端点用）。<br/><br/><p><b>常用值</b>：</p><br/><ul><br/>  <li>{@code "0.25"} —— 3 个月</li><br/>  <li>{@code "1"} —— 1 年</li><br/>  <li>{@code "5"} —— 5 年</li><br/>  <li>{@code "10"} —— 10 年（最常关注的长端基准）</li><br/></ul><br/><br/><p>可空 = 返回全期限曲线（画图用）；指定 = 取该期限的时间序列。</p>|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/bond/blk-detail?page=0&size=0&endDate=&curveType=&curveTerm=&startDate=&tradeDate=&tsCode='
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─tradeDate|string|交易日，格式 {@code YYYYMMDD}。|-|
|└─tsCode|string|债券代码（带交易所后缀）。|-|
|└─name|string|债券中文简称。|-|
|└─price|number|大宗交易成交价（元）。|-|
|└─vol|number|成交量（手）。|-|
|└─amount|number|成交金额（千元）。|-|
|└─buyDp|string|买方营业部（如 {@code "中信证券股份有限公司北京呼家楼营业部"}）。|-|
|└─sellDp|string|卖方营业部。|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "tradeDate": "",
      "tsCode": "",
      "name": "",
      "price": 0,
      "vol": 0,
      "amount": 0,
      "buyDp": "",
      "sellDp": ""
    }
  ],
  "traceId": ""
}
```

## OpenAPI v1 —— 指数端点（stock.index scope）。

&lt;p&gt;4 个端点：
&lt;ul&gt;
  &lt;li&gt;指数列表（list）—— 按 market / 类型 / 发布机构筛选&lt;/li&gt;
  &lt;li&gt;指数日 K 线（kline/daily）&lt;/li&gt;
  &lt;li&gt;指数分钟 K 线（kline/minutes）&lt;/li&gt;
  &lt;li&gt;申万行业日 K（sw-industry-quo）—— 含行业整体 PE/PB/MV/权重&lt;/li&gt;
&lt;/ul&gt;

&lt;p&gt;与现有 &lt;code&gt;/stock/api/home/mainIndex&lt;/code&gt;（缓存型主要指数快照）互补：
此 controller 支持任意指数（中证 / 申万 / MSCI 等）按代码 + 时间范围查询。
### 指数列表筛选（按代码 / 名称 / 市场 / 类型 / 发布机构）。
**URL:** /openapi/v1/stock/index/list

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 指数列表筛选（按代码 / 名称 / 市场 / 类型 / 发布机构）。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|page|int32|false|第几页，从 1 起。默认 1。0 / 负数会被当成 1。|-|
|size|int32|false|每页记录数。默认 50，硬上限 {@value #MAX_SIZE}。<br/><p>传入超过 {@value #MAX_SIZE} 时会被自动截断到 {@value #MAX_SIZE}（不报错）。</p>|-|
|tsCode|string|false|精确指数代码（带交易所后缀），如 {@code "000300.SH"}（沪深 300）/ {@code "399006.SZ"}（创业板指）。<br/><p>传了就只返回该指数；用于"我知道代码，给我元信息"。</p>|-|
|nameKeyword|string|false|名称模糊匹配关键字（中文）。<br/><p><b>示例</b>：{@code "300"} 匹配沪深 300 / 中证 300 / 全指 300 等；{@code "新能源"} 匹配各种新能源指数。</p>|-|
|market|string|false|市场来源。<br/><br/><ul><br/>  <li>{@code "SSE"} —— 上交所</li><br/>  <li>{@code "SZSE"} —— 深交所</li><br/>  <li>{@code "CSI"} —— 中证</li><br/>  <li>{@code "SW"} —— 申万</li><br/>  <li>{@code "MSCI"} —— 摩根士丹利国际</li><br/>  <li>...更多见 Tushare 字典</li><br/></ul>|-|
|indexType|string|false|指数类型：{@code "综合"} / {@code "规模"} / {@code "行业"} / {@code "风格"} / {@code "主题"} / {@code "策略"}。|-|
|category|string|false|指数风格细分（在 indexType 之下进一步分类，如"价值" / "成长" / "高股息"）。|-|
|publisher|string|false|发布机构：{@code "中证"} / {@code "申万"} / {@code "国证"} / {@code "上证"} / {@code "深证"} 等。|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/stock/index/list?page=0&size=0&category=&indexType=&market=&nameKeyword=&publisher=&tsCode='
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─tsCode|string|No comments found.|-|
|└─name|string|指数简称|-|
|└─fullname|string|指数全称|-|
|└─market|string|市场（SSE / SZSE / CSI / SW 等）|-|
|└─publisher|string|发布机构|-|
|└─indexType|string|指数类型（综合 / 规模 / 行业 等）|-|
|└─category|string|风格|-|
|└─baseDate|string|基期 YYYYMMDD|-|
|└─basePoint|number|基点|-|
|└─listDate|string|上市日期|-|
|└─weightRule|string|加权方式（市值加权 / 等权 / 自由流通市值加权 等）|-|
|└─dsc|string|描述|-|
|└─expDate|string|终止日期|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "tsCode": "",
      "name": "",
      "fullname": "",
      "market": "",
      "publisher": "",
      "indexType": "",
      "category": "",
      "baseDate": "",
      "basePoint": 0,
      "listDate": "",
      "weightRule": "",
      "dsc": "",
      "expDate": ""
    }
  ],
  "traceId": ""
}
```

### 指数日 K 线。tsCode 必填（如 000300.SH 沪深 300、000905.SH 中证 500、399006.SZ 创业板指）。
**URL:** /openapi/v1/stock/index/kline/daily

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 指数日 K 线。tsCode 必填（如 000300.SH 沪深 300、000905.SH 中证 500、399006.SZ 创业板指）。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|page|int32|false|第几页，从 1 起。默认 1。0 / 负数会被当成 1。|-|
|size|int32|false|每页记录数。默认 50，硬上限 {@value #MAX_SIZE}。<br/><p>传入超过 {@value #MAX_SIZE} 时会被自动截断到 {@value #MAX_SIZE}（不报错）。</p>|-|
|tsCode|string|false|代码（带交易所后缀）。<b>必填</b>。<br/><br/><p><b>示例</b>：</p><br/><ul><br/>  <li>股票：{@code "600519.SH"} / {@code "000001.SZ"}</li><br/>  <li>指数：{@code "000300.SH"}（沪深 300）/ {@code "000016.SH"}（上证 50）</li><br/>  <li>申万行业：{@code "801080"}（一级"电子"）/ {@code "801120"}（一级"食品饮料"）</li><br/></ul>|-|
|startDate|string|false|起始日期，格式 {@code YYYYMMDD}（如 {@code "20260101"}）。可空，不传时用默认窗口。|-|
|endDate|string|false|结束日期，格式 {@code YYYYMMDD}（如 {@code "20260430"}）。可空，不传时取最新交易日。|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/stock/index/kline/daily?page=0&size=0&endDate=&tsCode=&startDate='
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─tsCode|string|指数代码（带交易所后缀），如 {@code "000300.SH"}（沪深 300）/ {@code "399006.SZ"}（创业板指）。|-|
|└─tradeDate|string|交易日期。|-|
|└─open|number|开盘点位。|-|
|└─high|number|最高点位。|-|
|└─low|number|最低点位。|-|
|└─close|number|收盘点位。|-|
|└─preClose|number|前收盘点位。|-|
|└─chg|number|涨跌点数 = close − preClose。|-|
|└─pctChg|number|涨跌幅（%）。|-|
|└─vol|number|成交量（手）。指数成交量 = 全部成分股成交量加权汇总。|-|
|└─amount|number|成交额（千元）。|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "tsCode": "",
      "tradeDate": "yyyy-MM-dd HH:mm:ss",
      "open": 0,
      "high": 0,
      "low": 0,
      "close": 0,
      "preClose": 0,
      "chg": 0,
      "pctChg": 0,
      "vol": 0,
      "amount": 0
    }
  ],
  "traceId": ""
}
```

### 指数分钟 K 线。
**URL:** /openapi/v1/stock/index/kline/minutes

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 指数分钟 K 线。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|page|int32|false|第几页，从 1 起。默认 1。0 / 负数会被当成 1。|-|
|size|int32|false|每页记录数。默认 50，硬上限 {@value #MAX_SIZE}。<br/><p>传入超过 {@value #MAX_SIZE} 时会被自动截断到 {@value #MAX_SIZE}（不报错）。</p>|-|
|tsCode|string|false|代码（带交易所后缀）。<b>必填</b>。<br/><br/><p><b>示例</b>：</p><br/><ul><br/>  <li>股票：{@code "600519.SH"} / {@code "000001.SZ"}</li><br/>  <li>指数：{@code "000300.SH"}（沪深 300）/ {@code "000016.SH"}（上证 50）</li><br/>  <li>申万行业：{@code "801080"}（一级"电子"）/ {@code "801120"}（一级"食品饮料"）</li><br/></ul>|-|
|startDate|string|false|起始日期，格式 {@code YYYYMMDD}（如 {@code "20260101"}）。可空，不传时用默认窗口。|-|
|endDate|string|false|结束日期，格式 {@code YYYYMMDD}（如 {@code "20260430"}）。可空，不传时取最新交易日。|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/stock/index/kline/minutes?page=0&size=0&tsCode=&endDate=&startDate='
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─tsCode|string|指数代码（带交易所后缀），如 {@code "000300.SH"}。|-|
|└─tradeTime|string|K 线时间点（精确到分钟）。|-|
|└─open|number|开盘点位。|-|
|└─high|number|最高点位。|-|
|└─low|number|最低点位。|-|
|└─close|number|收盘点位。|-|
|└─vol|number|该 K 内成交量（手）。|-|
|└─amount|number|该 K 内成交额（千元）。|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "tsCode": "",
      "tradeTime": "yyyy-MM-dd HH:mm:ss",
      "open": 0,
      "high": 0,
      "low": 0,
      "close": 0,
      "vol": 0,
      "amount": 0
    }
  ],
  "traceId": ""
}
```

### 申万行业日 K 线 + 估值（pe/pb/total_mv/float_mv/weight）。<br>tsCode 是申万行业代码（如 801010.SI 农林牧渔）。<br>适合做行业横向估值对比。
**URL:** /openapi/v1/stock/index/sw-industry-quo

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 申万行业日 K 线 + 估值（pe/pb/total_mv/float_mv/weight）。
tsCode 是申万行业代码（如 801010.SI 农林牧渔）。
适合做行业横向估值对比。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|page|int32|false|第几页，从 1 起。默认 1。0 / 负数会被当成 1。|-|
|size|int32|false|每页记录数。默认 50，硬上限 {@value #MAX_SIZE}。<br/><p>传入超过 {@value #MAX_SIZE} 时会被自动截断到 {@value #MAX_SIZE}（不报错）。</p>|-|
|tsCode|string|false|代码（带交易所后缀）。<b>必填</b>。<br/><br/><p><b>示例</b>：</p><br/><ul><br/>  <li>股票：{@code "600519.SH"} / {@code "000001.SZ"}</li><br/>  <li>指数：{@code "000300.SH"}（沪深 300）/ {@code "000016.SH"}（上证 50）</li><br/>  <li>申万行业：{@code "801080"}（一级"电子"）/ {@code "801120"}（一级"食品饮料"）</li><br/></ul>|-|
|startDate|string|false|起始日期，格式 {@code YYYYMMDD}（如 {@code "20260101"}）。可空，不传时用默认窗口。|-|
|endDate|string|false|结束日期，格式 {@code YYYYMMDD}（如 {@code "20260430"}）。可空，不传时取最新交易日。|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/stock/index/sw-industry-quo?page=0&size=0&startDate=&tsCode=&endDate='
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─tsCode|string|申万行业代码（如 801010.SI）|-|
|└─tradeDate|string|No comments found.|-|
|└─name|string|No comments found.|-|
|└─open|number|No comments found.|-|
|└─low|number|No comments found.|-|
|└─high|number|No comments found.|-|
|└─close|number|No comments found.|-|
|└─chg|number|No comments found.|-|
|└─pctChg|number|No comments found.|-|
|└─vol|number|No comments found.|-|
|└─amount|number|No comments found.|-|
|└─pe|number|No comments found.|-|
|└─pb|number|No comments found.|-|
|└─floatMv|number|No comments found.|-|
|└─totalMv|number|No comments found.|-|
|└─weight|number|No comments found.|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "tsCode": "",
      "tradeDate": "yyyy-MM-dd HH:mm:ss",
      "name": "",
      "open": 0,
      "low": 0,
      "high": 0,
      "close": 0,
      "chg": 0,
      "pctChg": 0,
      "vol": 0,
      "amount": 0,
      "pe": 0,
      "pb": 0,
      "floatMv": 0,
      "totalMv": 0,
      "weight": 0
    }
  ],
  "traceId": ""
}
```

### 主要指数最新行情快照（上证 / 深证 / 沪深 300 / 中证 500 / 创业板等约 8-10 个）。<br><br>对应 site internal: &lt;code&gt;POST /stock/api/home/mainIndex&lt;/code&gt;。<br>缓存型，几秒级刷新。
**URL:** /openapi/v1/stock/index/main/snapshot

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 主要指数最新行情快照（上证 / 深证 / 沪深 300 / 中证 500 / 创业板等约 8-10 个）。

<p>对应 site internal: <code>POST /stock/api/home/mainIndex</code>。
缓存型，几秒级刷新。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/stock/index/main/snapshot'
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─tsCode|string|指数代码|-|
|└─name|string|No comments found.|-|
|└─tradeDate|int64|交易日期|-|
|└─close|double|收盘价|-|
|└─open|double|开盘价|-|
|└─high|double|最高价|-|
|└─low|double|最低价|-|
|└─preClose|double|昨日收盘价|-|
|└─chg|float|涨跌额|-|
|└─pctChg|float|涨跌幅|-|
|└─vol|double|成交量（手）|-|
|└─amount|double|成交额（千元）|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "tsCode": "",
      "name": "",
      "tradeDate": 0,
      "close": 0.0,
      "open": 0.0,
      "high": 0.0,
      "low": 0.0,
      "preClose": 0.0,
      "chg": 0.0,
      "pctChg": 0.0,
      "vol": 0.0,
      "amount": 0.0
    }
  ],
  "traceId": ""
}
```

### 主要指数历史 K 线（外层 list 是不同指数，内层 list 是该指数的近期 K 线序列）。<br><br>对应 site internal: &lt;code&gt;POST /stock/api/home/mainIndex/quoList&lt;/code&gt;。
**URL:** /openapi/v1/stock/index/main/history

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 主要指数历史 K 线（外层 list 是不同指数，内层 list 是该指数的近期 K 线序列）。

<p>对应 site internal: <code>POST /stock/api/home/mainIndex/quoList</code>。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/stock/index/main/history'
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─tsCode|string|指数代码|-|
|└─name|string|No comments found.|-|
|└─tradeDate|int64|交易日期|-|
|└─close|double|收盘价|-|
|└─open|double|开盘价|-|
|└─high|double|最高价|-|
|└─low|double|最低价|-|
|└─preClose|double|昨日收盘价|-|
|└─chg|float|涨跌额|-|
|└─pctChg|float|涨跌幅|-|
|└─vol|double|成交量（手）|-|
|└─amount|double|成交额（千元）|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    [
      {
        "tsCode": "",
        "name": "",
        "tradeDate": 0,
        "close": 0.0,
        "open": 0.0,
        "high": 0.0,
        "low": 0.0,
        "preClose": 0.0,
        "chg": 0.0,
        "pctChg": 0.0,
        "vol": 0.0,
        "amount": 0.0
      }
    ]
  ],
  "traceId": ""
}
```

### 申万一级行业涨跌热力图（28 个一级行业，每个含名称 + 当日涨跌幅 + 资金净流入）。<br><br>对应 site internal: &lt;code&gt;POST /stock/api/home/sw/heatmap&lt;/code&gt;。
**URL:** /openapi/v1/stock/index/sw-heatmap

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 申万一级行业涨跌热力图（28 个一级行业，每个含名称 + 当日涨跌幅 + 资金净流入）。

<p>对应 site internal: <code>POST /stock/api/home/sw/heatmap</code>。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/stock/index/sw-heatmap'
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─swCode|string|申万行业代码|-|
|└─swName|string|申万行业名称|-|
|└─tradeDate|string|交易日期|-|
|└─close|number|收盘价|-|
|└─pctChg|number|涨跌幅百分比|-|
|└─totalMv|number|总市值|-|
|└─details|array|No comments found.|-|
|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└─tsCode|string|No comments found.|-|
|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└─name|string|No comments found.|-|
|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└─close|number|No comments found.|-|
|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└─pctChg|number|No comments found.|-|
|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└─totalMv|number|No comments found.|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "swCode": "",
      "swName": "",
      "tradeDate": "yyyy-MM-dd HH:mm:ss",
      "close": 0,
      "pctChg": 0,
      "totalMv": 0,
      "details": [
        {
          "tsCode": "",
          "name": "",
          "close": 0,
          "pctChg": 0,
          "totalMv": 0
        }
      ]
    }
  ],
  "traceId": ""
}
```

### 指数每日估值快照（{@code index_dailybasic}）。tsCode 必填。<br><br>含指数级 PE / PE-TTM / PB / 换手率 / 总市值 / 流通市值 / 总股本 / 流通股本 / 自由流通股本。<br>覆盖沪深主要宽基指数（沪深 300、中证 500、上证 50 等）与申万一级行业指数。 <br><br>典型用途：宽基估值百分位（&amp;quot;沪深 300 当前 PE-TTM 在历史 N 年的分位&amp;quot;）、<br>行业相对估值横向对比。 
**URL:** /openapi/v1/stock/index/dailybasic

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 指数每日估值快照（{@code index_dailybasic}）。tsCode 必填。

<p>含指数级 PE / PE-TTM / PB / 换手率 / 总市值 / 流通市值 / 总股本 / 流通股本 / 自由流通股本。
覆盖沪深主要宽基指数（沪深 300、中证 500、上证 50 等）与申万一级行业指数。</p>

<p>典型用途：宽基估值百分位（"沪深 300 当前 PE-TTM 在历史 N 年的分位"）、
行业相对估值横向对比。</p>

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|page|int32|false|第几页，从 1 起。默认 1。0 / 负数会被当成 1。|-|
|size|int32|false|每页记录数。默认 50，硬上限 {@value #MAX_SIZE}。<br/><p>传入超过 {@value #MAX_SIZE} 时会被自动截断到 {@value #MAX_SIZE}（不报错）。</p>|-|
|tsCode|string|false|TS 代码（指数 / 个股 / 权重端点的指数代码）。可空（必填时返回空）。|-|
|conCode|string|false|成分代码（仅 index_weight 端点用，可空 → 拉全部成分）。|-|
|tradeDate|string|false|单日交易日 {@code YYYYMMDD}。可空。|-|
|startDate|string|false|起始交易日 {@code YYYYMMDD}。可空。|-|
|endDate|string|false|结束交易日 {@code YYYYMMDD}。可空。|-|
|freq|string|false|频率：weekly_monthly / week_month_adj = {week,month}；idx_mins = {1min,5min,15min,30min,60min}。可空。|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/stock/index/dailybasic?page=0&size=0&tsCode=&endDate=&conCode=&tradeDate=&freq=&startDate='
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─tradeDate|string|交易日|-|
|└─tsCode|string|指数 TS 代码|-|
|└─totalMv|number|当日总市值（元）|-|
|└─floatMv|number|当日流通市值（元）|-|
|└─totalShare|number|当日总股本（股）|-|
|└─floatShare|number|当日流通股本（股）|-|
|└─freeShare|number|当日自由流通股本（股）|-|
|└─turnoverRate|number|换手率|-|
|└─turnoverRateF|number|换手率（基于自由流通股本）|-|
|└─pe|number|市盈率|-|
|└─peTtm|number|市盈率 TTM|-|
|└─pb|number|市净率|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "tradeDate": "yyyy-MM-dd HH:mm:ss",
      "tsCode": "",
      "totalMv": 0,
      "floatMv": 0,
      "totalShare": 0,
      "floatShare": 0,
      "freeShare": 0,
      "turnoverRate": 0,
      "turnoverRateF": 0,
      "pe": 0,
      "peTtm": 0,
      "pb": 0
    }
  ],
  "traceId": ""
}
```

### 指数周线行情（{@code index_weekly}）。tsCode 必填。
**URL:** /openapi/v1/stock/index/kline/weekly

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 指数周线行情（{@code index_weekly}）。tsCode 必填。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|page|int32|false|第几页，从 1 起。默认 1。0 / 负数会被当成 1。|-|
|size|int32|false|每页记录数。默认 50，硬上限 {@value #MAX_SIZE}。<br/><p>传入超过 {@value #MAX_SIZE} 时会被自动截断到 {@value #MAX_SIZE}（不报错）。</p>|-|
|tsCode|string|false|TS 代码（指数 / 个股 / 权重端点的指数代码）。可空（必填时返回空）。|-|
|conCode|string|false|成分代码（仅 index_weight 端点用，可空 → 拉全部成分）。|-|
|tradeDate|string|false|单日交易日 {@code YYYYMMDD}。可空。|-|
|startDate|string|false|起始交易日 {@code YYYYMMDD}。可空。|-|
|endDate|string|false|结束交易日 {@code YYYYMMDD}。可空。|-|
|freq|string|false|频率：weekly_monthly / week_month_adj = {week,month}；idx_mins = {1min,5min,15min,30min,60min}。可空。|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/stock/index/kline/weekly?page=0&size=0&freq=&conCode=&tsCode=&endDate=&startDate=&tradeDate='
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─tradeDate|string|交易日（周线对应的最后一个交易日）|-|
|└─tsCode|string|指数 TS 代码|-|
|└─open|number|No comments found.|-|
|└─high|number|No comments found.|-|
|└─low|number|No comments found.|-|
|└─close|number|No comments found.|-|
|└─preClose|number|No comments found.|-|
|└─change|number|No comments found.|-|
|└─pctChg|number|No comments found.|-|
|└─vol|number|成交量（手）|-|
|└─amount|number|成交额（千元）|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "tradeDate": "yyyy-MM-dd HH:mm:ss",
      "tsCode": "",
      "open": 0,
      "high": 0,
      "low": 0,
      "close": 0,
      "preClose": 0,
      "change": 0,
      "pctChg": 0,
      "vol": 0,
      "amount": 0
    }
  ],
  "traceId": ""
}
```

### 指数月线行情（{@code index_monthly}）。tsCode 必填。
**URL:** /openapi/v1/stock/index/kline/monthly

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 指数月线行情（{@code index_monthly}）。tsCode 必填。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|page|int32|false|第几页，从 1 起。默认 1。0 / 负数会被当成 1。|-|
|size|int32|false|每页记录数。默认 50，硬上限 {@value #MAX_SIZE}。<br/><p>传入超过 {@value #MAX_SIZE} 时会被自动截断到 {@value #MAX_SIZE}（不报错）。</p>|-|
|tsCode|string|false|TS 代码（指数 / 个股 / 权重端点的指数代码）。可空（必填时返回空）。|-|
|conCode|string|false|成分代码（仅 index_weight 端点用，可空 → 拉全部成分）。|-|
|tradeDate|string|false|单日交易日 {@code YYYYMMDD}。可空。|-|
|startDate|string|false|起始交易日 {@code YYYYMMDD}。可空。|-|
|endDate|string|false|结束交易日 {@code YYYYMMDD}。可空。|-|
|freq|string|false|频率：weekly_monthly / week_month_adj = {week,month}；idx_mins = {1min,5min,15min,30min,60min}。可空。|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/stock/index/kline/monthly?page=0&size=0&endDate=&startDate=&tsCode=&tradeDate=&conCode=&freq='
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─tradeDate|string|交易日（月线对应的最后一个交易日）|-|
|└─tsCode|string|指数 TS 代码|-|
|└─open|number|No comments found.|-|
|└─high|number|No comments found.|-|
|└─low|number|No comments found.|-|
|└─close|number|No comments found.|-|
|└─preClose|number|No comments found.|-|
|└─change|number|No comments found.|-|
|└─pctChg|number|No comments found.|-|
|└─vol|number|成交量（手）|-|
|└─amount|number|成交额（千元）|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "tradeDate": "yyyy-MM-dd HH:mm:ss",
      "tsCode": "",
      "open": 0,
      "high": 0,
      "low": 0,
      "close": 0,
      "preClose": 0,
      "change": 0,
      "pctChg": 0,
      "vol": 0,
      "amount": 0
    }
  ],
  "traceId": ""
}
```

### 指数成分股与权重（{@code index_weight}）。月度数据，tsCode 必填（指数代码）。<br><br>可加 conCode（成分股代码）精确过滤。默认按 (trade_date DESC, weight DESC) 排序，<br>拿最新一期权重前 N 用 size 控制。 
**URL:** /openapi/v1/stock/index/weight

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 指数成分股与权重（{@code index_weight}）。月度数据，tsCode 必填（指数代码）。

<p>可加 conCode（成分股代码）精确过滤。默认按 (trade_date DESC, weight DESC) 排序，
拿最新一期权重前 N 用 size 控制。</p>

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|page|int32|false|第几页，从 1 起。默认 1。0 / 负数会被当成 1。|-|
|size|int32|false|每页记录数。默认 50，硬上限 {@value #MAX_SIZE}。<br/><p>传入超过 {@value #MAX_SIZE} 时会被自动截断到 {@value #MAX_SIZE}（不报错）。</p>|-|
|tsCode|string|false|TS 代码（指数 / 个股 / 权重端点的指数代码）。可空（必填时返回空）。|-|
|conCode|string|false|成分代码（仅 index_weight 端点用，可空 → 拉全部成分）。|-|
|tradeDate|string|false|单日交易日 {@code YYYYMMDD}。可空。|-|
|startDate|string|false|起始交易日 {@code YYYYMMDD}。可空。|-|
|endDate|string|false|结束交易日 {@code YYYYMMDD}。可空。|-|
|freq|string|false|频率：weekly_monthly / week_month_adj = {week,month}；idx_mins = {1min,5min,15min,30min,60min}。可空。|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/stock/index/weight?page=0&size=0&conCode=&endDate=&tsCode=&startDate=&freq=&tradeDate='
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─tradeDate|string|交易日（月度发布日）|-|
|└─indexCode|string|指数代码|-|
|└─conCode|string|成分代码|-|
|└─weight|number|权重（%）|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "tradeDate": "yyyy-MM-dd HH:mm:ss",
      "indexCode": "",
      "conCode": "",
      "weight": 0
    }
  ],
  "traceId": ""
}
```

### 全球指数日 K 线（{@code index_global}）。tsCode 必填。<br><br>Tushare 国际主要指数（道琼斯 DJI / 纳斯达克 IXIC / 标普 SPX / 恒生 HSI /<br>日经 N225 / 富时 FTSE 等）日级行情。含振幅（swing）。 
**URL:** /openapi/v1/stock/index/global

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 全球指数日 K 线（{@code index_global}）。tsCode 必填。

<p>Tushare 国际主要指数（道琼斯 DJI / 纳斯达克 IXIC / 标普 SPX / 恒生 HSI /
日经 N225 / 富时 FTSE 等）日级行情。含振幅（swing）。</p>

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|page|int32|false|第几页，从 1 起。默认 1。0 / 负数会被当成 1。|-|
|size|int32|false|每页记录数。默认 50，硬上限 {@value #MAX_SIZE}。<br/><p>传入超过 {@value #MAX_SIZE} 时会被自动截断到 {@value #MAX_SIZE}（不报错）。</p>|-|
|tsCode|string|false|TS 代码（指数 / 个股 / 权重端点的指数代码）。可空（必填时返回空）。|-|
|conCode|string|false|成分代码（仅 index_weight 端点用，可空 → 拉全部成分）。|-|
|tradeDate|string|false|单日交易日 {@code YYYYMMDD}。可空。|-|
|startDate|string|false|起始交易日 {@code YYYYMMDD}。可空。|-|
|endDate|string|false|结束交易日 {@code YYYYMMDD}。可空。|-|
|freq|string|false|频率：weekly_monthly / week_month_adj = {week,month}；idx_mins = {1min,5min,15min,30min,60min}。可空。|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/stock/index/global?page=0&size=0&startDate=&tsCode=&endDate=&freq=&tradeDate=&conCode='
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─tradeDate|string|交易日|-|
|└─tsCode|string|TS 指数代码|-|
|└─open|number|No comments found.|-|
|└─close|number|No comments found.|-|
|└─high|number|No comments found.|-|
|└─low|number|No comments found.|-|
|└─preClose|number|No comments found.|-|
|└─change|number|No comments found.|-|
|└─pctChg|number|No comments found.|-|
|└─swing|number|振幅|-|
|└─vol|number|No comments found.|-|
|└─amount|number|No comments found.|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "tradeDate": "yyyy-MM-dd HH:mm:ss",
      "tsCode": "",
      "open": 0,
      "close": 0,
      "high": 0,
      "low": 0,
      "preClose": 0,
      "change": 0,
      "pctChg": 0,
      "swing": 0,
      "vol": 0,
      "amount": 0
    }
  ],
  "traceId": ""
}
```

## OpenAPI v1 —— 衍生品端点（derivative scope）。

&lt;p&gt;覆盖 12 张 PG 表的 12 个端点：
&lt;ul&gt;
  &lt;li&gt;期货（7）：list / kline-daily / kline-weekly-monthly / kline-minutes / holding / wsr / main-contract&lt;/li&gt;
  &lt;li&gt;期权（3）：contracts / kline-daily / kline-minutes&lt;/li&gt;
  &lt;li&gt;SGE（2）：list / kline-daily&lt;/li&gt;
&lt;/ul&gt;

&lt;p&gt;路径规范：&lt;code&gt;/openapi/v1/derivative/{futures, option, sge}/...&lt;/code&gt;
全部 &lt;code&gt;@OpenApiScope(&quot;derivative&quot;)&lt;/code&gt;，套餐 Max 及以上。
### 期货合约基础信息列表筛选（按代码 / 名称 / 交易所 / 品种）。<br>&lt;b&gt;scope&lt;/b&gt;: {@code derivative}（2026-06-02 套餐重排后期货并入 derivative，原 futures.basic 引流位已废）。
**URL:** /openapi/v1/derivative/futures/list

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 期货合约基础信息列表筛选（按代码 / 名称 / 交易所 / 品种）。
<p><b>scope</b>: {@code derivative}（2026-06-02 套餐重排后期货并入 derivative，原 futures.basic 引流位已废）。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|page|int32|false|第几页，从 1 起。默认 1。0 / 负数会被当成 1。|-|
|size|int32|false|每页记录数。默认 50，硬上限 {@value #MAX_SIZE}。<br/><p>传入超过 {@value #MAX_SIZE} 时会被自动截断到 {@value #MAX_SIZE}（不报错）。</p>|-|
|tsCode|string|false|精确合约代码（带交易所后缀），如 {@code "CU2412.SHF"} / {@code "Au9999.SGE"}。|-|
|nameKeyword|string|false|名称模糊匹配（中文）。例如 {@code "黄金"} 找出全部黄金期货。|-|
|exchange|string|false|交易所代码：<br/><ul><br/>  <li>{@code "CFFEX"} —— 中金所（股指期货 / 国债期货）</li><br/>  <li>{@code "SHFE"} —— 上期所（金属 / 能源化工）</li><br/>  <li>{@code "DCE"} —— 大商所（农产品 / 工业品）</li><br/>  <li>{@code "CZCE"} —— 郑商所（农产品 / 化工）</li><br/>  <li>{@code "INE"} —— 上海能源（原油等国际化品种）</li><br/>  <li>{@code "GFEX"} —— 广州期货（碳酸锂等新品种）</li><br/></ul>|-|
|futCode|string|false|期货品种代码（不带交易所后缀，仅期货 list 用）。<br/><p>例如 {@code "CU"}（铜）/ {@code "AU"}（黄金）/ {@code "RB"}（螺纹钢）。</p>|-|
|listStatus|string|false|上市状态：{@code "L"}（上市）/ {@code "D"}（退市）/ {@code "P"}（暂停）。|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/derivative/futures/list?page=0&size=0&nameKeyword=&exchange=&tsCode=&listStatus=&futCode='
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─tsCode|string|合约代码（带交易所后缀），如 {@code "CU2412.SHF"}（沪铜 2024 年 12 月）。|-|
|└─symbol|string|合约号（不带交易所后缀），如 {@code "CU2412"}。|-|
|└─exchange|string|交易所代码：{@code "CFFEX"} / {@code "SHFE"} / {@code "DCE"} / {@code "CZCE"} / {@code "INE"} / {@code "GFEX"}。|-|
|└─name|string|合约中文名，如 {@code "沪铜 2412"}。|-|
|└─futCode|string|期货品种代码（不带后缀），如 {@code "CU"}（铜）/ {@code "AU"}（黄金）/ {@code "RB"}（螺纹钢）。|-|
|└─multiplier|number|合约乘数（每点价值多少元）。例如沪铜 5 吨/手，铜价每涨 1 元 = 5 元盈亏。|-|
|└─tradeUnit|string|交易单位（中文描述），如 {@code "吨"} / {@code "千克"} / {@code "桶"}。|-|
|└─perUnit|number|每手数量（合约规模）。例如沪铜每手 5（吨）。|-|
|└─quoteUnit|string|报价单位代码。|-|
|└─quoteUnitDesc|string|报价单位描述（中文），如 {@code "元/吨"} / {@code "元/克"}。|-|
|└─dModeDesc|string|交割方式描述：{@code "实物交割"} / {@code "现金交割"}。|-|
|└─listDate|string|上市日期。|-|
|└─delistDate|string|退市日期（已退市合约）。|-|
|└─dMonth|string|交割月份，格式 {@code YYYYMM}（如 {@code "202412"}）。|-|
|└─lastDdate|string|最后交易日。该日后合约停止交易，进入交割流程。|-|
|└─tradeTimeDesc|string|交易时间描述（中文，如 {@code "9:00-11:30 / 13:30-15:00 / 21:00-02:30"}）。|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "tsCode": "",
      "symbol": "",
      "exchange": "",
      "name": "",
      "futCode": "",
      "multiplier": 0,
      "tradeUnit": "",
      "perUnit": 0,
      "quoteUnit": "",
      "quoteUnitDesc": "",
      "dModeDesc": "",
      "listDate": "yyyy-MM-dd HH:mm:ss",
      "delistDate": "yyyy-MM-dd HH:mm:ss",
      "dMonth": "",
      "lastDdate": "yyyy-MM-dd HH:mm:ss",
      "tradeTimeDesc": ""
    }
  ],
  "traceId": ""
}
```

### 期货日 K 线（含 settle / oi / oi_chg / 交割结算价）。<br> &lt;b&gt;scope&lt;/b&gt;: {@code derivative}（2026-06-02 重排，期货并入 derivative，原 futures.kline 已废）。
**URL:** /openapi/v1/derivative/futures/kline/daily

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 期货日 K 线（含 settle / oi / oi_chg / 交割结算价）。
 <p><b>scope</b>: {@code derivative}（2026-06-02 重排，期货并入 derivative，原 futures.kline 已废）。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|page|int32|false|第几页，从 1 起。默认 1。0 / 负数会被当成 1。|-|
|size|int32|false|每页记录数。默认 50，硬上限 {@value #MAX_SIZE}。<br/><p>传入超过 {@value #MAX_SIZE} 时会被自动截断到 {@value #MAX_SIZE}（不报错）。</p>|-|
|tsCode|string|false|合约代码（带交易所后缀）。K 线类端点用。<br/><br/><p><b>示例</b>：</p><br/><ul><br/>  <li>{@code "CU2412.SHF"} —— 上期所 2024 年 12 月铜期货合约</li><br/>  <li>{@code "RB2410.SHF"} —— 螺纹钢</li><br/>  <li>{@code "AU2412.SHF"} —— 黄金</li><br/>  <li>{@code "10006281.SH"} —— 50ETF 期权某合约</li><br/>  <li>{@code "Au9999.SGE"} —— 上金所黄金 T+D</li><br/>  <li>{@code "CU.SHF"} —— 主力连续（main-contract 端点用）</li><br/></ul>|-|
|symbol|string|false|期货品种代码（不带交易所后缀）。仅 {@code holding} / {@code wsr} 端点使用。<br/><p>例如 {@code "CU"}（铜）/ {@code "AU"}（黄金）/ {@code "RB"}（螺纹钢）。</p>|-|
|startDate|string|false|起始日期，格式 {@code YYYYMMDD}。可空。|-|
|endDate|string|false|结束日期，格式 {@code YYYYMMDD}。可空。|-|
|freq|string|false|周期：{@code "W"}（周）/ {@code "M"}（月）。仅 {@code weekly-monthly} 端点用。|-|
|exchange|string|false|交易所（可选过滤）。仅 {@code option/kline/daily-by-date}（期权全市场日 K）端点用，<br/>用于把单日全市场期权按交易所收窄：{@code "SSE"}/{@code "SZSE"}（ETF）·{@code "CFFEX"}（股指）·<br/>{@code "SHFE"}/{@code "DCE"}/{@code "CZCE"}/{@code "INE"}/{@code "GFEX"}（商品/能源）。可空（不传返全市场）。|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/derivative/futures/kline/daily?page=0&size=0&symbol=&startDate=&endDate=&freq=&tsCode=&exchange='
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─tsCode|string|期货合约代码，如 {@code "CU2412.SHF"}。|-|
|└─tradeDate|string|交易日期。|-|
|└─preClose|number|昨收盘价（元）。|-|
|└─preSettle|number|昨结算价（元）。期货次日开盘基准、保证金计算依据。|-|
|└─open|number|开盘价（元）。|-|
|└─high|number|最高价（元）。|-|
|└─low|number|最低价（元）。|-|
|└─close|number|收盘价（元）。|-|
|└─settle|number|结算价（元）。当日加权均价，用于次日保证金 / 涨跌停板基准。|-|
|└─change1|number|涨跌额 1（元）= close − preClose（基于收盘）。|-|
|└─change2|number|涨跌额 2（元）= settle − preSettle（基于结算，期货标准口径）。|-|
|└─vol|number|成交量（手）。|-|
|└─amount|number|成交额（万元）。|-|
|└─oi|number|持仓量（手）。多空双方未平仓合约总数 / 2。|-|
|└─oiChg|number|持仓量变化（手）= 当日 oi − 昨日 oi。<br/><p>{@code > 0} 资金流入（多空双开）；{@code < 0} 资金流出（多空双平）。</p>|-|
|└─delvSettle|number|交割结算价|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "tsCode": "",
      "tradeDate": "yyyy-MM-dd HH:mm:ss",
      "preClose": 0,
      "preSettle": 0,
      "open": 0,
      "high": 0,
      "low": 0,
      "close": 0,
      "settle": 0,
      "change1": 0,
      "change2": 0,
      "vol": 0,
      "amount": 0,
      "oi": 0,
      "oiChg": 0,
      "delvSettle": 0
    }
  ],
  "traceId": ""
}
```

### 期货周/月 K 线。freq = W 或 M（form.freq）。<br> &lt;b&gt;scope&lt;/b&gt;: {@code derivative}（2026-06-02 重排，期货并入 derivative，原 futures.kline 已废）。
**URL:** /openapi/v1/derivative/futures/kline/weekly-monthly

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 期货周/月 K 线。freq = W 或 M（form.freq）。
 <p><b>scope</b>: {@code derivative}（2026-06-02 重排，期货并入 derivative，原 futures.kline 已废）。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|page|int32|false|第几页，从 1 起。默认 1。0 / 负数会被当成 1。|-|
|size|int32|false|每页记录数。默认 50，硬上限 {@value #MAX_SIZE}。<br/><p>传入超过 {@value #MAX_SIZE} 时会被自动截断到 {@value #MAX_SIZE}（不报错）。</p>|-|
|tsCode|string|false|合约代码（带交易所后缀）。K 线类端点用。<br/><br/><p><b>示例</b>：</p><br/><ul><br/>  <li>{@code "CU2412.SHF"} —— 上期所 2024 年 12 月铜期货合约</li><br/>  <li>{@code "RB2410.SHF"} —— 螺纹钢</li><br/>  <li>{@code "AU2412.SHF"} —— 黄金</li><br/>  <li>{@code "10006281.SH"} —— 50ETF 期权某合约</li><br/>  <li>{@code "Au9999.SGE"} —— 上金所黄金 T+D</li><br/>  <li>{@code "CU.SHF"} —— 主力连续（main-contract 端点用）</li><br/></ul>|-|
|symbol|string|false|期货品种代码（不带交易所后缀）。仅 {@code holding} / {@code wsr} 端点使用。<br/><p>例如 {@code "CU"}（铜）/ {@code "AU"}（黄金）/ {@code "RB"}（螺纹钢）。</p>|-|
|startDate|string|false|起始日期，格式 {@code YYYYMMDD}。可空。|-|
|endDate|string|false|结束日期，格式 {@code YYYYMMDD}。可空。|-|
|freq|string|false|周期：{@code "W"}（周）/ {@code "M"}（月）。仅 {@code weekly-monthly} 端点用。|-|
|exchange|string|false|交易所（可选过滤）。仅 {@code option/kline/daily-by-date}（期权全市场日 K）端点用，<br/>用于把单日全市场期权按交易所收窄：{@code "SSE"}/{@code "SZSE"}（ETF）·{@code "CFFEX"}（股指）·<br/>{@code "SHFE"}/{@code "DCE"}/{@code "CZCE"}/{@code "INE"}/{@code "GFEX"}（商品/能源）。可空（不传返全市场）。|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/derivative/futures/kline/weekly-monthly?page=0&size=0&freq=&endDate=&tsCode=&symbol=&exchange=&startDate='
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─tsCode|string|No comments found.|-|
|└─tradeDate|string|No comments found.|-|
|└─endDate|string|周期结束日期|-|
|└─freq|string|周期 W / M|-|
|└─open|number|No comments found.|-|
|└─high|number|No comments found.|-|
|└─low|number|No comments found.|-|
|└─close|number|No comments found.|-|
|└─preClose|number|No comments found.|-|
|└─settle|number|No comments found.|-|
|└─preSettle|number|No comments found.|-|
|└─vol|number|No comments found.|-|
|└─amount|number|No comments found.|-|
|└─oi|number|No comments found.|-|
|└─oiChg|number|No comments found.|-|
|└─exchange|string|No comments found.|-|
|└─change1|number|No comments found.|-|
|└─change2|number|No comments found.|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "tsCode": "",
      "tradeDate": "yyyy-MM-dd HH:mm:ss",
      "endDate": "yyyy-MM-dd HH:mm:ss",
      "freq": "",
      "open": 0,
      "high": 0,
      "low": 0,
      "close": 0,
      "preClose": 0,
      "settle": 0,
      "preSettle": 0,
      "vol": 0,
      "amount": 0,
      "oi": 0,
      "oiChg": 0,
      "exchange": "",
      "change1": 0,
      "change2": 0
    }
  ],
  "traceId": ""
}
```

### 期货分钟 K 线。<br> &lt;b&gt;scope&lt;/b&gt;: {@code derivative}（2026-06-02 重排，期货并入 derivative，原 futures.kline 已废）。
**URL:** /openapi/v1/derivative/futures/kline/minutes

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 期货分钟 K 线。
 <p><b>scope</b>: {@code derivative}（2026-06-02 重排，期货并入 derivative，原 futures.kline 已废）。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|page|int32|false|第几页，从 1 起。默认 1。0 / 负数会被当成 1。|-|
|size|int32|false|每页记录数。默认 50，硬上限 {@value #MAX_SIZE}。<br/><p>传入超过 {@value #MAX_SIZE} 时会被自动截断到 {@value #MAX_SIZE}（不报错）。</p>|-|
|tsCode|string|false|合约代码（带交易所后缀）。K 线类端点用。<br/><br/><p><b>示例</b>：</p><br/><ul><br/>  <li>{@code "CU2412.SHF"} —— 上期所 2024 年 12 月铜期货合约</li><br/>  <li>{@code "RB2410.SHF"} —— 螺纹钢</li><br/>  <li>{@code "AU2412.SHF"} —— 黄金</li><br/>  <li>{@code "10006281.SH"} —— 50ETF 期权某合约</li><br/>  <li>{@code "Au9999.SGE"} —— 上金所黄金 T+D</li><br/>  <li>{@code "CU.SHF"} —— 主力连续（main-contract 端点用）</li><br/></ul>|-|
|symbol|string|false|期货品种代码（不带交易所后缀）。仅 {@code holding} / {@code wsr} 端点使用。<br/><p>例如 {@code "CU"}（铜）/ {@code "AU"}（黄金）/ {@code "RB"}（螺纹钢）。</p>|-|
|startDate|string|false|起始日期，格式 {@code YYYYMMDD}。可空。|-|
|endDate|string|false|结束日期，格式 {@code YYYYMMDD}。可空。|-|
|freq|string|false|周期：{@code "W"}（周）/ {@code "M"}（月）。仅 {@code weekly-monthly} 端点用。|-|
|exchange|string|false|交易所（可选过滤）。仅 {@code option/kline/daily-by-date}（期权全市场日 K）端点用，<br/>用于把单日全市场期权按交易所收窄：{@code "SSE"}/{@code "SZSE"}（ETF）·{@code "CFFEX"}（股指）·<br/>{@code "SHFE"}/{@code "DCE"}/{@code "CZCE"}/{@code "INE"}/{@code "GFEX"}（商品/能源）。可空（不传返全市场）。|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/derivative/futures/kline/minutes?page=0&size=0&exchange=&endDate=&symbol=&tsCode=&startDate=&freq='
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─tsCode|string|No comments found.|-|
|└─tradeTime|string|No comments found.|-|
|└─open|number|No comments found.|-|
|└─high|number|No comments found.|-|
|└─low|number|No comments found.|-|
|└─close|number|No comments found.|-|
|└─vol|number|No comments found.|-|
|└─amount|number|No comments found.|-|
|└─oi|number|No comments found.|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "tsCode": "",
      "tradeTime": "yyyy-MM-dd HH:mm:ss",
      "open": 0,
      "high": 0,
      "low": 0,
      "close": 0,
      "vol": 0,
      "amount": 0,
      "oi": 0
    }
  ],
  "traceId": ""
}
```

### 期货会员持仓排名（按品种 symbol，非合约 ts_code）。<br>symbol 必填（如 CU / RB / AU）。
**URL:** /openapi/v1/derivative/futures/holding

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 期货会员持仓排名（按品种 symbol，非合约 ts_code）。
symbol 必填（如 CU / RB / AU）。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|page|int32|false|第几页，从 1 起。默认 1。0 / 负数会被当成 1。|-|
|size|int32|false|每页记录数。默认 50，硬上限 {@value #MAX_SIZE}。<br/><p>传入超过 {@value #MAX_SIZE} 时会被自动截断到 {@value #MAX_SIZE}（不报错）。</p>|-|
|tsCode|string|false|合约代码（带交易所后缀）。K 线类端点用。<br/><br/><p><b>示例</b>：</p><br/><ul><br/>  <li>{@code "CU2412.SHF"} —— 上期所 2024 年 12 月铜期货合约</li><br/>  <li>{@code "RB2410.SHF"} —— 螺纹钢</li><br/>  <li>{@code "AU2412.SHF"} —— 黄金</li><br/>  <li>{@code "10006281.SH"} —— 50ETF 期权某合约</li><br/>  <li>{@code "Au9999.SGE"} —— 上金所黄金 T+D</li><br/>  <li>{@code "CU.SHF"} —— 主力连续（main-contract 端点用）</li><br/></ul>|-|
|symbol|string|false|期货品种代码（不带交易所后缀）。仅 {@code holding} / {@code wsr} 端点使用。<br/><p>例如 {@code "CU"}（铜）/ {@code "AU"}（黄金）/ {@code "RB"}（螺纹钢）。</p>|-|
|startDate|string|false|起始日期，格式 {@code YYYYMMDD}。可空。|-|
|endDate|string|false|结束日期，格式 {@code YYYYMMDD}。可空。|-|
|freq|string|false|周期：{@code "W"}（周）/ {@code "M"}（月）。仅 {@code weekly-monthly} 端点用。|-|
|exchange|string|false|交易所（可选过滤）。仅 {@code option/kline/daily-by-date}（期权全市场日 K）端点用，<br/>用于把单日全市场期权按交易所收窄：{@code "SSE"}/{@code "SZSE"}（ETF）·{@code "CFFEX"}（股指）·<br/>{@code "SHFE"}/{@code "DCE"}/{@code "CZCE"}/{@code "INE"}/{@code "GFEX"}（商品/能源）。可空（不传返全市场）。|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/derivative/futures/holding?page=0&size=0&exchange=&symbol=&freq=&tsCode=&endDate=&startDate='
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─tradeDate|string|No comments found.|-|
|└─symbol|string|品种代码（如 CU / RB）|-|
|└─broker|string|期货公司名称|-|
|└─vol|int32|成交量（手）|-|
|└─volChg|int32|成交量增减（手）|-|
|└─longHld|int32|多头持仓|-|
|└─longChg|int32|多头持仓变化|-|
|└─shortHld|int32|空头持仓|-|
|└─shortChg|int32|空头持仓变化|-|
|└─exchange|string|No comments found.|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "tradeDate": "yyyy-MM-dd HH:mm:ss",
      "symbol": "",
      "broker": "",
      "vol": 0,
      "volChg": 0,
      "longHld": 0,
      "longChg": 0,
      "shortHld": 0,
      "shortChg": 0,
      "exchange": ""
    }
  ],
  "traceId": ""
}
```

### 期货仓单日报（按品种 symbol）。
**URL:** /openapi/v1/derivative/futures/wsr

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 期货仓单日报（按品种 symbol）。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|page|int32|false|第几页，从 1 起。默认 1。0 / 负数会被当成 1。|-|
|size|int32|false|每页记录数。默认 50，硬上限 {@value #MAX_SIZE}。<br/><p>传入超过 {@value #MAX_SIZE} 时会被自动截断到 {@value #MAX_SIZE}（不报错）。</p>|-|
|tsCode|string|false|合约代码（带交易所后缀）。K 线类端点用。<br/><br/><p><b>示例</b>：</p><br/><ul><br/>  <li>{@code "CU2412.SHF"} —— 上期所 2024 年 12 月铜期货合约</li><br/>  <li>{@code "RB2410.SHF"} —— 螺纹钢</li><br/>  <li>{@code "AU2412.SHF"} —— 黄金</li><br/>  <li>{@code "10006281.SH"} —— 50ETF 期权某合约</li><br/>  <li>{@code "Au9999.SGE"} —— 上金所黄金 T+D</li><br/>  <li>{@code "CU.SHF"} —— 主力连续（main-contract 端点用）</li><br/></ul>|-|
|symbol|string|false|期货品种代码（不带交易所后缀）。仅 {@code holding} / {@code wsr} 端点使用。<br/><p>例如 {@code "CU"}（铜）/ {@code "AU"}（黄金）/ {@code "RB"}（螺纹钢）。</p>|-|
|startDate|string|false|起始日期，格式 {@code YYYYMMDD}。可空。|-|
|endDate|string|false|结束日期，格式 {@code YYYYMMDD}。可空。|-|
|freq|string|false|周期：{@code "W"}（周）/ {@code "M"}（月）。仅 {@code weekly-monthly} 端点用。|-|
|exchange|string|false|交易所（可选过滤）。仅 {@code option/kline/daily-by-date}（期权全市场日 K）端点用，<br/>用于把单日全市场期权按交易所收窄：{@code "SSE"}/{@code "SZSE"}（ETF）·{@code "CFFEX"}（股指）·<br/>{@code "SHFE"}/{@code "DCE"}/{@code "CZCE"}/{@code "INE"}/{@code "GFEX"}（商品/能源）。可空（不传返全市场）。|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/derivative/futures/wsr?page=0&size=0&freq=&tsCode=&startDate=&exchange=&endDate=&symbol='
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─tradeDate|string|No comments found.|-|
|└─symbol|string|品种代码|-|
|└─futName|string|品种名称|-|
|└─warehouse|string|仓库名称|-|
|└─whId|string|仓库 ID|-|
|└─preVol|int32|昨日仓单量|-|
|└─vol|int32|当日仓单量|-|
|└─volChg|int32|仓单变化|-|
|└─area|string|地区|-|
|└─year|string|年份|-|
|└─grade|string|等级|-|
|└─brand|string|品牌|-|
|└─place|string|产地|-|
|└─pd|int32|升贴水|-|
|└─isCt|string|是否完税|-|
|└─unit|string|单位|-|
|└─exchange|string|No comments found.|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "tradeDate": "yyyy-MM-dd HH:mm:ss",
      "symbol": "",
      "futName": "",
      "warehouse": "",
      "whId": "",
      "preVol": 0,
      "vol": 0,
      "volChg": 0,
      "area": "",
      "year": "",
      "grade": "",
      "brand": "",
      "place": "",
      "pd": 0,
      "isCt": "",
      "unit": "",
      "exchange": ""
    }
  ],
  "traceId": ""
}
```

### 期货主力连续合约映射（连续合约 ts_code → 当日真实合约 mapping_ts_code）。
**URL:** /openapi/v1/derivative/futures/main-contract

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 期货主力连续合约映射（连续合约 ts_code → 当日真实合约 mapping_ts_code）。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|page|int32|false|第几页，从 1 起。默认 1。0 / 负数会被当成 1。|-|
|size|int32|false|每页记录数。默认 50，硬上限 {@value #MAX_SIZE}。<br/><p>传入超过 {@value #MAX_SIZE} 时会被自动截断到 {@value #MAX_SIZE}（不报错）。</p>|-|
|tsCode|string|false|合约代码（带交易所后缀）。K 线类端点用。<br/><br/><p><b>示例</b>：</p><br/><ul><br/>  <li>{@code "CU2412.SHF"} —— 上期所 2024 年 12 月铜期货合约</li><br/>  <li>{@code "RB2410.SHF"} —— 螺纹钢</li><br/>  <li>{@code "AU2412.SHF"} —— 黄金</li><br/>  <li>{@code "10006281.SH"} —— 50ETF 期权某合约</li><br/>  <li>{@code "Au9999.SGE"} —— 上金所黄金 T+D</li><br/>  <li>{@code "CU.SHF"} —— 主力连续（main-contract 端点用）</li><br/></ul>|-|
|symbol|string|false|期货品种代码（不带交易所后缀）。仅 {@code holding} / {@code wsr} 端点使用。<br/><p>例如 {@code "CU"}（铜）/ {@code "AU"}（黄金）/ {@code "RB"}（螺纹钢）。</p>|-|
|startDate|string|false|起始日期，格式 {@code YYYYMMDD}。可空。|-|
|endDate|string|false|结束日期，格式 {@code YYYYMMDD}。可空。|-|
|freq|string|false|周期：{@code "W"}（周）/ {@code "M"}（月）。仅 {@code weekly-monthly} 端点用。|-|
|exchange|string|false|交易所（可选过滤）。仅 {@code option/kline/daily-by-date}（期权全市场日 K）端点用，<br/>用于把单日全市场期权按交易所收窄：{@code "SSE"}/{@code "SZSE"}（ETF）·{@code "CFFEX"}（股指）·<br/>{@code "SHFE"}/{@code "DCE"}/{@code "CZCE"}/{@code "INE"}/{@code "GFEX"}（商品/能源）。可空（不传返全市场）。|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/derivative/futures/main-contract?page=0&size=0&exchange=&symbol=&startDate=&endDate=&tsCode=&freq='
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─tsCode|string|No comments found.|-|
|└─tradeDate|string|No comments found.|-|
|└─mappingTsCode|string|No comments found.|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "tsCode": "",
      "tradeDate": "yyyy-MM-dd HH:mm:ss",
      "mappingTsCode": ""
    }
  ],
  "traceId": ""
}
```

### 期权合约列表筛选（含行权价 / 到期日 / call/put / 标的）。<br>复用站内 IOptionContractService 现有方法，避免双份维护。
**URL:** /openapi/v1/derivative/option/contracts

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 期权合约列表筛选（含行权价 / 到期日 / call/put / 标的）。
复用站内 IOptionContractService 现有方法，避免双份维护。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|page|int32|false|第几页，从 1 起。默认 1。0 / 负数会被当成 1。|-|
|size|int32|false|每页记录数。默认 50，硬上限 {@value #MAX_SIZE}。<br/><p>传入超过 {@value #MAX_SIZE} 时会被自动截断到 {@value #MAX_SIZE}（不报错）。</p>|-|
|tsCode|string|false|期权代码，<b>标的码或合约自身码均可</b>（服务端自动识别，对 agent 更直觉）：<br/><ul><br/>  <li><b>标的码</b>（如 {@code "510050.SH"} 50ETF）→ 返回该标的<b>全部</b>在挂期权合约。最常用。<br/>      （服务端按 {@code opt_code = "OP" + 标的码} 解析，本表 opt_code 恒为该形式）</li><br/>  <li><b>合约自身码</b>（如 {@code "10011254.SH"}）→ 精确返回该一张合约。</li><br/></ul><br/><p>底层等价于 {@code ts_code = 入参 OR opt_code = "OP" + 入参}。</p>|-|
|optCodes|array|false|期权<b>标的</b>代码列表（匹配 option_contracts.opt_code，<b>带 "OP" 前缀</b> = {@code "OP" + 标的ts_code}）。<br/><b>这是「列出某标的全部期权合约」的主入口。</b><br/><br/><p>映射规则：标的 {@code 510050.SH} → {@code "OP510050.SH"}；{@code 510300.SH} → {@code "OP510300.SH"}；<br/>{@code 159919.SZ} → {@code "OP159919.SZ"}。</p><br/><p><b>示例</b>：{@code ["OP510050.SH"]} = 上证 50ETF 全部在挂期权；{@code ["OP510300.SH"]} = 沪深 300ETF。</p>|-|
|exchanges|array|false|交易所列表。<br/><ul><br/>  <li>{@code "SSE"} —— 上交所</li><br/>  <li>{@code "SZSE"} —— 深交所</li><br/>  <li>{@code "CFFEX"} —— 中金所（股指期权）</li><br/></ul><br/><p>例如 {@code ["SSE", "SZSE"]}。</p>|-|
|exchange|string|false|交易所（单数便捷别名，与同域 {@code option/kline/daily-by-date} 端点的 {@code exchange} 字段保持一致）。<br/><p>与 {@link #exchanges} 等价，二者都传时取并集。<br/>历史缺陷：此前只认 {@code exchanges}（数组），agent 按邻近端点习惯传单数 {@code exchange}<br/>被静默忽略 → 全交易所合约整表返回（4MB+）。</p>|-|
|dates|array|false|到期<b>月份</b>列表（可选过滤，匹配 option_contracts.s_month）。格式 <b>{@code YYYYMM}</b>（<b>不是 YYYYMMDD</b>），<br/>如 {@code ["202606"]} = 2026 年 6 月到期。<b>不传时</b>服务端默认只返回「到期月 ≥ 当前月」的在挂合约。|-|
|optType|string|false|期权类型<br/>默认查询etf期权|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/derivative/option/contracts?page=0&size=0&optCodes=,&exchanges=,&dates=,&exchange=&tsCode=&optType='
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─tsCode|string|No comments found.|-|
|└─exchange|string|No comments found.|-|
|└─opName|string|No comments found.|-|
|└─perUnit|number|No comments found.|-|
|└─optCode|string|No comments found.|-|
|└─optType|string|No comments found.|-|
|└─callPut|string|No comments found.|-|
|└─exerciseType|string|No comments found.|-|
|└─exercisePrice|number|No comments found.|-|
|└─sMonthDate|string|No comments found.|-|
|└─maturityDate|string|No comments found.|-|
|└─listPrice|number|No comments found.|-|
|└─listDate|string|No comments found.|-|
|└─delistDate|string|No comments found.|-|
|└─lastEdate|string|No comments found.|-|
|└─lastDdate|string|No comments found.|-|
|└─quoteUnit|string|No comments found.|-|
|└─minPriceChg|string|No comments found.|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "tsCode": "",
      "exchange": "",
      "opName": "",
      "perUnit": 0,
      "optCode": "",
      "optType": "",
      "callPut": "",
      "exerciseType": "",
      "exercisePrice": 0,
      "sMonthDate": "yyyy-MM-dd HH:mm:ss",
      "maturityDate": "yyyy-MM-dd HH:mm:ss",
      "listPrice": 0,
      "listDate": "yyyy-MM-dd HH:mm:ss",
      "delistDate": "yyyy-MM-dd HH:mm:ss",
      "lastEdate": "yyyy-MM-dd HH:mm:ss",
      "lastDdate": "yyyy-MM-dd HH:mm:ss",
      "quoteUnit": "",
      "minPriceChg": ""
    }
  ],
  "traceId": ""
}
```

### 期权日 K 线（含 settle）。单合约：必传 {@code tsCode}（合约码）。
**URL:** /openapi/v1/derivative/option/kline/daily

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 期权日 K 线（含 settle）。单合约：必传 {@code tsCode}（合约码）。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|page|int32|false|第几页，从 1 起。默认 1。0 / 负数会被当成 1。|-|
|size|int32|false|每页记录数。默认 50，硬上限 {@value #MAX_SIZE}。<br/><p>传入超过 {@value #MAX_SIZE} 时会被自动截断到 {@value #MAX_SIZE}（不报错）。</p>|-|
|tsCode|string|false|合约代码（带交易所后缀）。K 线类端点用。<br/><br/><p><b>示例</b>：</p><br/><ul><br/>  <li>{@code "CU2412.SHF"} —— 上期所 2024 年 12 月铜期货合约</li><br/>  <li>{@code "RB2410.SHF"} —— 螺纹钢</li><br/>  <li>{@code "AU2412.SHF"} —— 黄金</li><br/>  <li>{@code "10006281.SH"} —— 50ETF 期权某合约</li><br/>  <li>{@code "Au9999.SGE"} —— 上金所黄金 T+D</li><br/>  <li>{@code "CU.SHF"} —— 主力连续（main-contract 端点用）</li><br/></ul>|-|
|symbol|string|false|期货品种代码（不带交易所后缀）。仅 {@code holding} / {@code wsr} 端点使用。<br/><p>例如 {@code "CU"}（铜）/ {@code "AU"}（黄金）/ {@code "RB"}（螺纹钢）。</p>|-|
|startDate|string|false|起始日期，格式 {@code YYYYMMDD}。可空。|-|
|endDate|string|false|结束日期，格式 {@code YYYYMMDD}。可空。|-|
|freq|string|false|周期：{@code "W"}（周）/ {@code "M"}（月）。仅 {@code weekly-monthly} 端点用。|-|
|exchange|string|false|交易所（可选过滤）。仅 {@code option/kline/daily-by-date}（期权全市场日 K）端点用，<br/>用于把单日全市场期权按交易所收窄：{@code "SSE"}/{@code "SZSE"}（ETF）·{@code "CFFEX"}（股指）·<br/>{@code "SHFE"}/{@code "DCE"}/{@code "CZCE"}/{@code "INE"}/{@code "GFEX"}（商品/能源）。可空（不传返全市场）。|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/derivative/option/kline/daily?page=0&size=0&startDate=&freq=&tsCode=&symbol=&exchange=&endDate='
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─tsCode|string|期权合约代码（带交易所后缀），如 {@code "10006281.SH"}。|-|
|└─tradeDate|string|交易日期。|-|
|└─exchange|string|交易所：{@code "SSE"} / {@code "SZSE"} / {@code "CFFEX"} 等。|-|
|└─preSettle|number|前结算价（元）。期权用结算价（不是收盘价）做次日基准。|-|
|└─preClose|number|前收盘价（元）。|-|
|└─open|number|开盘价（元）。|-|
|└─high|number|最高价（元）。|-|
|└─low|number|最低价（元）。|-|
|└─close|number|收盘价（元）。|-|
|└─settle|number|结算价（元）。期权交易日结算用此价计算保证金 / 盈亏。|-|
|└─vol|number|成交量（张）。|-|
|└─amount|number|成交额（元）。|-|
|└─oi|number|持仓量（张）。反映市场关注度——持仓激增 + 价格变动 = 主力真实意图。|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "tsCode": "",
      "tradeDate": "yyyy-MM-dd HH:mm:ss",
      "exchange": "",
      "preSettle": 0,
      "preClose": 0,
      "open": 0,
      "high": 0,
      "low": 0,
      "close": 0,
      "settle": 0,
      "vol": 0,
      "amount": 0,
      "oi": 0
    }
  ],
  "traceId": ""
}
```

### 期权&lt;b&gt;全市场&lt;/b&gt;日 K 线（按交易日，不限合约）。<br><br>给「某交易日全部期权一次拉下来做跨合约筛选 / 排序」用——避免逐合约调 {@code /option/kline/daily}<br>几万次。{@code startDate} &lt;b&gt;必填&lt;/b&gt;（单日传 {@code startDate=endDate}），可选 {@code exchange} 收窄；<br>分页（每页上限 500，配合 {@code page} 翻页）。典型用法：拉 6/2 + 6/3 两天快照，客户端按价格条件筛选排序。 
**URL:** /openapi/v1/derivative/option/kline/daily-by-date

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 期权<b>全市场</b>日 K 线（按交易日，不限合约）。

<p>给「某交易日全部期权一次拉下来做跨合约筛选 / 排序」用——避免逐合约调 {@code /option/kline/daily}
几万次。{@code startDate} <b>必填</b>（单日传 {@code startDate=endDate}），可选 {@code exchange} 收窄；
分页（每页上限 500，配合 {@code page} 翻页）。典型用法：拉 6/2 + 6/3 两天快照，客户端按价格条件筛选排序。</p>

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|page|int32|false|第几页，从 1 起。默认 1。0 / 负数会被当成 1。|-|
|size|int32|false|每页记录数。默认 50，硬上限 {@value #MAX_SIZE}。<br/><p>传入超过 {@value #MAX_SIZE} 时会被自动截断到 {@value #MAX_SIZE}（不报错）。</p>|-|
|tsCode|string|false|合约代码（带交易所后缀）。K 线类端点用。<br/><br/><p><b>示例</b>：</p><br/><ul><br/>  <li>{@code "CU2412.SHF"} —— 上期所 2024 年 12 月铜期货合约</li><br/>  <li>{@code "RB2410.SHF"} —— 螺纹钢</li><br/>  <li>{@code "AU2412.SHF"} —— 黄金</li><br/>  <li>{@code "10006281.SH"} —— 50ETF 期权某合约</li><br/>  <li>{@code "Au9999.SGE"} —— 上金所黄金 T+D</li><br/>  <li>{@code "CU.SHF"} —— 主力连续（main-contract 端点用）</li><br/></ul>|-|
|symbol|string|false|期货品种代码（不带交易所后缀）。仅 {@code holding} / {@code wsr} 端点使用。<br/><p>例如 {@code "CU"}（铜）/ {@code "AU"}（黄金）/ {@code "RB"}（螺纹钢）。</p>|-|
|startDate|string|false|起始日期，格式 {@code YYYYMMDD}。可空。|-|
|endDate|string|false|结束日期，格式 {@code YYYYMMDD}。可空。|-|
|freq|string|false|周期：{@code "W"}（周）/ {@code "M"}（月）。仅 {@code weekly-monthly} 端点用。|-|
|exchange|string|false|交易所（可选过滤）。仅 {@code option/kline/daily-by-date}（期权全市场日 K）端点用，<br/>用于把单日全市场期权按交易所收窄：{@code "SSE"}/{@code "SZSE"}（ETF）·{@code "CFFEX"}（股指）·<br/>{@code "SHFE"}/{@code "DCE"}/{@code "CZCE"}/{@code "INE"}/{@code "GFEX"}（商品/能源）。可空（不传返全市场）。|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/derivative/option/kline/daily-by-date?page=0&size=0&exchange=&symbol=&startDate=&freq=&endDate=&tsCode='
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─tsCode|string|期权合约代码（带交易所后缀），如 {@code "10006281.SH"}。|-|
|└─tradeDate|string|交易日期。|-|
|└─exchange|string|交易所：{@code "SSE"} / {@code "SZSE"} / {@code "CFFEX"} 等。|-|
|└─preSettle|number|前结算价（元）。期权用结算价（不是收盘价）做次日基准。|-|
|└─preClose|number|前收盘价（元）。|-|
|└─open|number|开盘价（元）。|-|
|└─high|number|最高价（元）。|-|
|└─low|number|最低价（元）。|-|
|└─close|number|收盘价（元）。|-|
|└─settle|number|结算价（元）。期权交易日结算用此价计算保证金 / 盈亏。|-|
|└─vol|number|成交量（张）。|-|
|└─amount|number|成交额（元）。|-|
|└─oi|number|持仓量（张）。反映市场关注度——持仓激增 + 价格变动 = 主力真实意图。|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "tsCode": "",
      "tradeDate": "yyyy-MM-dd HH:mm:ss",
      "exchange": "",
      "preSettle": 0,
      "preClose": 0,
      "open": 0,
      "high": 0,
      "low": 0,
      "close": 0,
      "settle": 0,
      "vol": 0,
      "amount": 0,
      "oi": 0
    }
  ],
  "traceId": ""
}
```

### 期权分钟 K 线。
**URL:** /openapi/v1/derivative/option/kline/minutes

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 期权分钟 K 线。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|page|int32|false|第几页，从 1 起。默认 1。0 / 负数会被当成 1。|-|
|size|int32|false|每页记录数。默认 50，硬上限 {@value #MAX_SIZE}。<br/><p>传入超过 {@value #MAX_SIZE} 时会被自动截断到 {@value #MAX_SIZE}（不报错）。</p>|-|
|tsCode|string|false|合约代码（带交易所后缀）。K 线类端点用。<br/><br/><p><b>示例</b>：</p><br/><ul><br/>  <li>{@code "CU2412.SHF"} —— 上期所 2024 年 12 月铜期货合约</li><br/>  <li>{@code "RB2410.SHF"} —— 螺纹钢</li><br/>  <li>{@code "AU2412.SHF"} —— 黄金</li><br/>  <li>{@code "10006281.SH"} —— 50ETF 期权某合约</li><br/>  <li>{@code "Au9999.SGE"} —— 上金所黄金 T+D</li><br/>  <li>{@code "CU.SHF"} —— 主力连续（main-contract 端点用）</li><br/></ul>|-|
|symbol|string|false|期货品种代码（不带交易所后缀）。仅 {@code holding} / {@code wsr} 端点使用。<br/><p>例如 {@code "CU"}（铜）/ {@code "AU"}（黄金）/ {@code "RB"}（螺纹钢）。</p>|-|
|startDate|string|false|起始日期，格式 {@code YYYYMMDD}。可空。|-|
|endDate|string|false|结束日期，格式 {@code YYYYMMDD}。可空。|-|
|freq|string|false|周期：{@code "W"}（周）/ {@code "M"}（月）。仅 {@code weekly-monthly} 端点用。|-|
|exchange|string|false|交易所（可选过滤）。仅 {@code option/kline/daily-by-date}（期权全市场日 K）端点用，<br/>用于把单日全市场期权按交易所收窄：{@code "SSE"}/{@code "SZSE"}（ETF）·{@code "CFFEX"}（股指）·<br/>{@code "SHFE"}/{@code "DCE"}/{@code "CZCE"}/{@code "INE"}/{@code "GFEX"}（商品/能源）。可空（不传返全市场）。|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/derivative/option/kline/minutes?page=0&size=0&endDate=&symbol=&startDate=&tsCode=&freq=&exchange='
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─tsCode|string|No comments found.|-|
|└─tradeTime|string|No comments found.|-|
|└─open|number|No comments found.|-|
|└─high|number|No comments found.|-|
|└─low|number|No comments found.|-|
|└─close|number|No comments found.|-|
|└─vol|number|No comments found.|-|
|└─amount|number|No comments found.|-|
|└─oi|number|No comments found.|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "tsCode": "",
      "tradeTime": "yyyy-MM-dd HH:mm:ss",
      "open": 0,
      "high": 0,
      "low": 0,
      "close": 0,
      "vol": 0,
      "amount": 0,
      "oi": 0
    }
  ],
  "traceId": ""
}
```

### SGE 现货合约列表（金 Au9999 / Au100g / iAu99.99 / mAu(T+D) / Pt9995 等）。
**URL:** /openapi/v1/derivative/sge/list

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** SGE 现货合约列表（金 Au9999 / Au100g / iAu99.99 / mAu(T+D) / Pt9995 等）。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|page|int32|false|第几页，从 1 起。默认 1。0 / 负数会被当成 1。|-|
|size|int32|false|每页记录数。默认 50，硬上限 {@value #MAX_SIZE}。<br/><p>传入超过 {@value #MAX_SIZE} 时会被自动截断到 {@value #MAX_SIZE}（不报错）。</p>|-|
|tsCode|string|false|精确合约代码（带交易所后缀），如 {@code "CU2412.SHF"} / {@code "Au9999.SGE"}。|-|
|nameKeyword|string|false|名称模糊匹配（中文）。例如 {@code "黄金"} 找出全部黄金期货。|-|
|exchange|string|false|交易所代码：<br/><ul><br/>  <li>{@code "CFFEX"} —— 中金所（股指期货 / 国债期货）</li><br/>  <li>{@code "SHFE"} —— 上期所（金属 / 能源化工）</li><br/>  <li>{@code "DCE"} —— 大商所（农产品 / 工业品）</li><br/>  <li>{@code "CZCE"} —— 郑商所（农产品 / 化工）</li><br/>  <li>{@code "INE"} —— 上海能源（原油等国际化品种）</li><br/>  <li>{@code "GFEX"} —— 广州期货（碳酸锂等新品种）</li><br/></ul>|-|
|futCode|string|false|期货品种代码（不带交易所后缀，仅期货 list 用）。<br/><p>例如 {@code "CU"}（铜）/ {@code "AU"}（黄金）/ {@code "RB"}（螺纹钢）。</p>|-|
|listStatus|string|false|上市状态：{@code "L"}（上市）/ {@code "D"}（退市）/ {@code "P"}（暂停）。|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/derivative/sge/list?page=0&size=0&listStatus=&exchange=&nameKeyword=&futCode=&tsCode='
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─tsCode|string|上金所产品代码，如 {@code "Au9999.SGE"}（黄金 9999）。|-|
|└─tsName|string|品种中文名，如 {@code "黄金 9999"} / {@code "白银（T+D）"}。|-|
|└─tradeType|string|交易类型：{@code "询价"} / {@code "集中竞价"} / {@code "T+D 延期交收"}。|-|
|└─tUnit|number|交易单位（每手数量），如黄金 1000 克。|-|
|└─pUnit|number|报价单位（每报价点对应数量），如 {@code 1}（克）。|-|
|└─minChange|number|最小变动价位（元）。报价跳动的最小步长。|-|
|└─priceLimit|number|涨跌停限制（%）。例如 {@code 10} 表示涨跌停 ±10%。|-|
|└─minVol|int32|最小开仓量（手）。|-|
|└─maxVol|int32|最大开仓量（手）。|-|
|└─tradeMode|string|交易方式：{@code "现货"} / {@code "延期"} 等。|-|
|└─marginRate|number|保证金比例（小数，{@code 0.10} = 10%）。|-|
|└─liqRate|number|强平比例（持仓亏损达此比例触发强平，小数）。|-|
|└─tradeTime|string|交易时间（中文描述），如 {@code "9:00-15:30 / 20:00-02:30"}。|-|
|└─listDate|string|上市日期，格式 {@code YYYYMMDD}。|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "tsCode": "",
      "tsName": "",
      "tradeType": "",
      "tUnit": 0,
      "pUnit": 0,
      "minChange": 0,
      "priceLimit": 0,
      "minVol": 0,
      "maxVol": 0,
      "tradeMode": "",
      "marginRate": 0,
      "liqRate": 0,
      "tradeTime": "",
      "listDate": ""
    }
  ],
  "traceId": ""
}
```

### SGE 上海黄金日行情。
**URL:** /openapi/v1/derivative/sge/kline/daily

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** SGE 上海黄金日行情。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|page|int32|false|第几页，从 1 起。默认 1。0 / 负数会被当成 1。|-|
|size|int32|false|每页记录数。默认 50，硬上限 {@value #MAX_SIZE}。<br/><p>传入超过 {@value #MAX_SIZE} 时会被自动截断到 {@value #MAX_SIZE}（不报错）。</p>|-|
|tsCode|string|false|合约代码（带交易所后缀）。K 线类端点用。<br/><br/><p><b>示例</b>：</p><br/><ul><br/>  <li>{@code "CU2412.SHF"} —— 上期所 2024 年 12 月铜期货合约</li><br/>  <li>{@code "RB2410.SHF"} —— 螺纹钢</li><br/>  <li>{@code "AU2412.SHF"} —— 黄金</li><br/>  <li>{@code "10006281.SH"} —— 50ETF 期权某合约</li><br/>  <li>{@code "Au9999.SGE"} —— 上金所黄金 T+D</li><br/>  <li>{@code "CU.SHF"} —— 主力连续（main-contract 端点用）</li><br/></ul>|-|
|symbol|string|false|期货品种代码（不带交易所后缀）。仅 {@code holding} / {@code wsr} 端点使用。<br/><p>例如 {@code "CU"}（铜）/ {@code "AU"}（黄金）/ {@code "RB"}（螺纹钢）。</p>|-|
|startDate|string|false|起始日期，格式 {@code YYYYMMDD}。可空。|-|
|endDate|string|false|结束日期，格式 {@code YYYYMMDD}。可空。|-|
|freq|string|false|周期：{@code "W"}（周）/ {@code "M"}（月）。仅 {@code weekly-monthly} 端点用。|-|
|exchange|string|false|交易所（可选过滤）。仅 {@code option/kline/daily-by-date}（期权全市场日 K）端点用，<br/>用于把单日全市场期权按交易所收窄：{@code "SSE"}/{@code "SZSE"}（ETF）·{@code "CFFEX"}（股指）·<br/>{@code "SHFE"}/{@code "DCE"}/{@code "CZCE"}/{@code "INE"}/{@code "GFEX"}（商品/能源）。可空（不传返全市场）。|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/derivative/sge/kline/daily?page=0&size=0&startDate=&freq=&tsCode=&endDate=&exchange=&symbol='
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─tsCode|string|上金所合约代码，如 {@code "Au9999.SGE"}（黄金 T+D）/ {@code "Ag(T+D).SGE"}（白银 T+D）。|-|
|└─tradeDate|string|交易日期。|-|
|└─close|number|收盘价（元/克）。|-|
|└─open|number|开盘价（元/克）。|-|
|└─high|number|最高价（元/克）。|-|
|└─low|number|最低价（元/克）。|-|
|└─priceAvg|number|加权平均价（元/克）。当日所有成交按金额加权。|-|
|└─chg|number|涨跌额（元/克）= close − preClose。|-|
|└─pctChange|number|涨跌幅（%）。|-|
|└─vol|number|成交量（千克）。|-|
|└─amount|number|成交额（元）。|-|
|└─oi|number|持仓量（千克）。T+D 持仓反映多空兴趣。|-|
|└─settleVol|number|当日延期补偿（递延费）成交量。|-|
|└─settleDire|string|延期补偿方向。<br/><ul><br/>  <li>{@code "B"} —— 多头补偿（多头给空头）</li><br/>  <li>{@code "S"} —— 空头补偿（空头给多头）</li><br/></ul>|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "tsCode": "",
      "tradeDate": "yyyy-MM-dd HH:mm:ss",
      "close": 0,
      "open": 0,
      "high": 0,
      "low": 0,
      "priceAvg": 0,
      "chg": 0,
      "pctChange": 0,
      "vol": 0,
      "amount": 0,
      "oi": 0,
      "settleVol": 0,
      "settleDire": ""
    }
  ],
  "traceId": ""
}
```

### 期货结算费用 + 保证金率（futures_settle）。tsCode 必填。<br>量化回测计算资金占用 / 真实手续费必用。
**URL:** /openapi/v1/derivative/futures/settle

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 期货结算费用 + 保证金率（futures_settle）。tsCode 必填。
量化回测计算资金占用 / 真实手续费必用。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|page|int32|false|第几页，从 1 起。默认 1。0 / 负数会被当成 1。|-|
|size|int32|false|每页记录数。默认 50，硬上限 {@value #MAX_SIZE}。<br/><p>传入超过 {@value #MAX_SIZE} 时会被自动截断到 {@value #MAX_SIZE}（不报错）。</p>|-|
|tsCode|string|false|合约代码（带交易所后缀）。K 线类端点用。<br/><br/><p><b>示例</b>：</p><br/><ul><br/>  <li>{@code "CU2412.SHF"} —— 上期所 2024 年 12 月铜期货合约</li><br/>  <li>{@code "RB2410.SHF"} —— 螺纹钢</li><br/>  <li>{@code "AU2412.SHF"} —— 黄金</li><br/>  <li>{@code "10006281.SH"} —— 50ETF 期权某合约</li><br/>  <li>{@code "Au9999.SGE"} —— 上金所黄金 T+D</li><br/>  <li>{@code "CU.SHF"} —— 主力连续（main-contract 端点用）</li><br/></ul>|-|
|symbol|string|false|期货品种代码（不带交易所后缀）。仅 {@code holding} / {@code wsr} 端点使用。<br/><p>例如 {@code "CU"}（铜）/ {@code "AU"}（黄金）/ {@code "RB"}（螺纹钢）。</p>|-|
|startDate|string|false|起始日期，格式 {@code YYYYMMDD}。可空。|-|
|endDate|string|false|结束日期，格式 {@code YYYYMMDD}。可空。|-|
|freq|string|false|周期：{@code "W"}（周）/ {@code "M"}（月）。仅 {@code weekly-monthly} 端点用。|-|
|exchange|string|false|交易所（可选过滤）。仅 {@code option/kline/daily-by-date}（期权全市场日 K）端点用，<br/>用于把单日全市场期权按交易所收窄：{@code "SSE"}/{@code "SZSE"}（ETF）·{@code "CFFEX"}（股指）·<br/>{@code "SHFE"}/{@code "DCE"}/{@code "CZCE"}/{@code "INE"}/{@code "GFEX"}（商品/能源）。可空（不传返全市场）。|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/derivative/futures/settle?page=0&size=0&exchange=&startDate=&symbol=&endDate=&freq=&tsCode='
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─tsCode|string|No comments found.|-|
|└─tradeDate|string|No comments found.|-|
|└─settle|number|结算价|-|
|└─tradingFeeRate|number|交易手续费率（万分比）|-|
|└─tradingFee|number|交易手续费（元 / 手）|-|
|└─deliveryFee|number|交割手续费（元 / 手）|-|
|└─bHedgingMarginRate|number|多头套保保证金率|-|
|└─sHedgingMarginRate|number|空头套保保证金率|-|
|└─longMarginRate|number|多头投机保证金率|-|
|└─shortMarginRate|number|空头投机保证金率|-|
|└─offsetTodayFee|number|平今手续费（元 / 手）|-|
|└─exchange|string|No comments found.|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "tsCode": "",
      "tradeDate": "",
      "settle": 0,
      "tradingFeeRate": 0,
      "tradingFee": 0,
      "deliveryFee": 0,
      "bHedgingMarginRate": 0,
      "sHedgingMarginRate": 0,
      "longMarginRate": 0,
      "shortMarginRate": 0,
      "offsetTodayFee": 0,
      "exchange": ""
    }
  ],
  "traceId": ""
}
```

### 期货合约每日涨跌停 + 保证金率（futures_limit）。tsCode 必填。
**URL:** /openapi/v1/derivative/futures/limit

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 期货合约每日涨跌停 + 保证金率（futures_limit）。tsCode 必填。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|page|int32|false|第几页，从 1 起。默认 1。0 / 负数会被当成 1。|-|
|size|int32|false|每页记录数。默认 50，硬上限 {@value #MAX_SIZE}。<br/><p>传入超过 {@value #MAX_SIZE} 时会被自动截断到 {@value #MAX_SIZE}（不报错）。</p>|-|
|tsCode|string|false|合约代码（带交易所后缀）。K 线类端点用。<br/><br/><p><b>示例</b>：</p><br/><ul><br/>  <li>{@code "CU2412.SHF"} —— 上期所 2024 年 12 月铜期货合约</li><br/>  <li>{@code "RB2410.SHF"} —— 螺纹钢</li><br/>  <li>{@code "AU2412.SHF"} —— 黄金</li><br/>  <li>{@code "10006281.SH"} —— 50ETF 期权某合约</li><br/>  <li>{@code "Au9999.SGE"} —— 上金所黄金 T+D</li><br/>  <li>{@code "CU.SHF"} —— 主力连续（main-contract 端点用）</li><br/></ul>|-|
|symbol|string|false|期货品种代码（不带交易所后缀）。仅 {@code holding} / {@code wsr} 端点使用。<br/><p>例如 {@code "CU"}（铜）/ {@code "AU"}（黄金）/ {@code "RB"}（螺纹钢）。</p>|-|
|startDate|string|false|起始日期，格式 {@code YYYYMMDD}。可空。|-|
|endDate|string|false|结束日期，格式 {@code YYYYMMDD}。可空。|-|
|freq|string|false|周期：{@code "W"}（周）/ {@code "M"}（月）。仅 {@code weekly-monthly} 端点用。|-|
|exchange|string|false|交易所（可选过滤）。仅 {@code option/kline/daily-by-date}（期权全市场日 K）端点用，<br/>用于把单日全市场期权按交易所收窄：{@code "SSE"}/{@code "SZSE"}（ETF）·{@code "CFFEX"}（股指）·<br/>{@code "SHFE"}/{@code "DCE"}/{@code "CZCE"}/{@code "INE"}/{@code "GFEX"}（商品/能源）。可空（不传返全市场）。|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/derivative/futures/limit?page=0&size=0&symbol=&exchange=&endDate=&freq=&startDate=&tsCode='
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─tsCode|string|No comments found.|-|
|└─tradeDate|string|No comments found.|-|
|└─preClose|number|前收（夜盘最后）|-|
|└─preSettle|number|前结算价|-|
|└─upLimit|number|当日涨停价|-|
|└─downLimit|number|当日跌停价|-|
|└─marginRate|number|保证金率|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "tsCode": "",
      "tradeDate": "",
      "preClose": 0,
      "preSettle": 0,
      "upLimit": 0,
      "downLimit": 0,
      "marginRate": 0
    }
  ],
  "traceId": ""
}
```

### 期货主要品种交易周报（{@code futures_weekly_detail}）。<br><br>可按 exchange（DCE/CFFEX/CZCE/SHFE/INE） / prd（品种代码如 CU/RB/IF）/ 周日期范围<br>（YYYYMMDD 按 week_date 过滤）过滤。含按品种聚合的成交量 / 成交额 / 持仓 / 主力收盘价 +<br>同比 / 环比，是看商品行业趋势的核心周度数据。 
**URL:** /openapi/v1/derivative/futures/weekly-detail

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 期货主要品种交易周报（{@code futures_weekly_detail}）。

<p>可按 exchange（DCE/CFFEX/CZCE/SHFE/INE） / prd（品种代码如 CU/RB/IF）/ 周日期范围
（YYYYMMDD 按 week_date 过滤）过滤。含按品种聚合的成交量 / 成交额 / 持仓 / 主力收盘价 +
同比 / 环比，是看商品行业趋势的核心周度数据。</p>

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|page|int32|false|第几页，从 1 起。默认 1。0 / 负数会被当成 1。|-|
|size|int32|false|每页记录数。默认 50，硬上限 {@value #MAX_SIZE}。<br/><p>传入超过 {@value #MAX_SIZE} 时会被自动截断到 {@value #MAX_SIZE}（不报错）。</p>|-|
|keyword|string|false|通用关键字（按表内最关键文本列模糊匹配，参类级注释）。|-|
|year|int32|false|年度（fund-sales-ratio / fund-sales-vol 用）。|-|
|startYear|int32|false|起始年度（fund-sales-ratio 区间）。|-|
|endYear|int32|false|结束年度（fund-sales-ratio 区间）。|-|
|quarter|string|false|季度（fund-sales-vol，如 "1"/"2"/"3"/"4" 或 "Q1"/...）。|-|
|startDate|string|false|起始日期 {@code YYYYMMDD}。|-|
|endDate|string|false|结束日期 {@code YYYYMMDD}。|-|
|country|string|false|国家代码（eco-cal）。|-|
|currency|string|false|货币代码（eco-cal，USD/EUR/CNY/...）。|-|
|ptype|string|false|政策类型（policy-npr）。|-|
|puborg|string|false|发布机构（policy-npr）。|-|
|exchange|string|false|交易所（futures-weekly-detail，DCE/CFFEX/CZCE/SHFE/INE）。|-|
|prd|string|false|期货品种代码（futures-weekly-detail，如 CU/RB/IF）。|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/derivative/futures/weekly-detail?page=0&size=0&year=0&startYear=0&endYear=0&quarter=&puborg=&prd=&ptype=&startDate=&currency=&keyword=&exchange=&country=&endDate='
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─exchange|string|交易所|-|
|└─prd|string|品种代码|-|
|└─name|string|品种名称|-|
|└─vol|number|成交量（手）|-|
|└─volYoy|number|成交量同比|-|
|└─amount|number|成交额|-|
|└─amoutYoy|number|成交额同比|-|
|└─cumvol|number|累计成交量|-|
|└─cumvolYoy|number|累计成交量同比|-|
|└─cumamt|number|累计成交额|-|
|└─cumamtYoy|number|累计成交额同比|-|
|└─openInterest|number|持仓量|-|
|└─interestWow|number|持仓量周环比|-|
|└─mcClose|number|主力合约收盘价|-|
|└─closeWow|number|主力收盘价周环比|-|
|└─week|string|周度（YYYYWW 等格式字符串）|-|
|└─weekDate|string|周日期|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "exchange": "",
      "prd": "",
      "name": "",
      "vol": 0,
      "volYoy": 0,
      "amount": 0,
      "amoutYoy": 0,
      "cumvol": 0,
      "cumvolYoy": 0,
      "cumamt": 0,
      "cumamtYoy": 0,
      "openInterest": 0,
      "interestWow": 0,
      "mcClose": 0,
      "closeWow": 0,
      "week": "",
      "weekDate": "yyyy-MM-dd HH:mm:ss"
    }
  ],
  "traceId": ""
}
```

## OpenAPI v1 —— 股票市场深度端点（A 股盘口资金面，套餐 Pro 及以上）。

&lt;p&gt;2026-06 重构：原单一 {@code stock.market} scope 已按数据维度拆为四个子 scope，端点逐个标注：
&lt;ul&gt;
  &lt;li&gt;&lt;b&gt;stock.plate&lt;/b&gt; —— 板块/概念/行业分类（东财/申万/同花顺/通达信/中信/开盘啦）+ 成分股 + 板块行情（15 端点）&lt;/li&gt;
  &lt;li&gt;&lt;b&gt;stock.lhb&lt;/b&gt; —— 龙虎榜 + 机构席位 + 券商营业部 + 游资名录/明细 + 开盘啦榜单（8 端点）&lt;/li&gt;
  &lt;li&gt;&lt;b&gt;stock.moneyflow&lt;/b&gt; —— 个股/板块资金流 + 板块连续净流入 + 北向沪深港通资金（7 端点）&lt;/li&gt;
  &lt;li&gt;&lt;b&gt;stock.sentiment&lt;/b&gt; —— 热度/股吧/情绪 + 筹码 + 涨跌停连板 + ST + 集合竞价 + 大宗 + 备用行情 + 放量突破（15 端点）&lt;/li&gt;
&lt;/ul&gt;
四个子 scope 同属 Pro 档。存量持有旧 {@code stock.market} 的 token 由 {@code TokenSnapshot} 自动展开为四子 scope，不中断。
### 东财热榜（dc_hot）。data_type 区分股票 / 板块 / 概念热榜。<br>tradeDate 或 tsCode 至少传一个。
**URL:** /openapi/v1/stock/market/hot-rank

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 东财热榜（dc_hot）。data_type 区分股票 / 板块 / 概念热榜。
tradeDate 或 tsCode 至少传一个。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|page|int32|false|第几页，从 1 起。默认 1。0 / 负数会被当成 1。|-|
|size|int32|false|每页记录数。默认 50，硬上限 {@value #MAX_SIZE}。<br/><p>传入超过 {@value #MAX_SIZE} 时会被自动截断到 {@value #MAX_SIZE}（不报错）。</p>|-|
|tsCode|string|false|股票代码（带交易所后缀），如 {@code "600519.SH"}。<br/><p>cyq-perf / block-trade / auction-open / auction-close / ths-concept / moneyflow-dc 等"针对单只票"的端点使用。</p>|-|
|tradeDate|string|false|交易日期，格式 {@code YYYYMMDD}（如 {@code "20260430"}）。可空。<br/><p>hot-rank / limit-analysis / hsgt-top10 / kpl-list / mainboard / guba-rank 等"按日切片"端点使用。<br/>不传时取最新交易日。</p>|-|
|startDate|string|false|起始日期，格式 {@code YYYYMMDD}。<br/><p>block-trade / hsgt-moneyflow / moneyflow-dc 等"按时间序列"端点使用。</p>|-|
|endDate|string|false|结束日期，格式 {@code YYYYMMDD}。<br/><p>同 {@link #startDate}，配套使用。</p>|-|
|nameKeyword|string|false|名称模糊匹配关键字（中文）。<br/><p>hm-list（游资名录搜索，如 {@code "宁波派"} / {@code "赵老哥"}）/ kpl-list（按概念名搜）使用。</p>|-|
|dataType|string|false|子分类标识（含义因端点而异）：<br/><br/><ul><br/>  <li><b>hot-rank（dc_hot）</b>：{@code "1"} 股票热榜 / {@code "2"} 板块热榜</li><br/>  <li><b>hsgt-top10</b>：{@code "1"} 沪股通 / {@code "2"} 深股通 / {@code "3"} 港股通</li><br/>  <li><b>cyq-perf</b>：{@code "D"} 日 / {@code "W"} 周 / {@code "M"} 月</li><br/></ul>|-|
|limitStat|string|false|涨跌停状态过滤（仅 limit-analysis 端点用）。<br/><br/><ul><br/>  <li>{@code "U"} —— 涨停</li><br/>  <li>{@code "D"} —— 跌停</li><br/>  <li>空 —— 不过滤</li><br/></ul>|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/stock/market/hot-rank?page=0&size=0&endDate=&nameKeyword=&limitStat=&dataType=&tsCode=&tradeDate=&startDate='
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─tradeDate|string|交易日期，格式 {@code YYYYMMDD}。|-|
|└─dataType|string|数据类型：{@code "1"} 股票热榜 / {@code "2"} 板块热榜 / {@code "3"} 概念热榜。|-|
|└─tsCode|string|标的代码（股票为 ts_code，板块 / 概念为各自代码）。|-|
|└─tsName|string|标的中文名（股票名 / 板块名 / 概念名）。|-|
|└─rankNum|int32|当日热榜排名，从 1 起（1 = 最热）。|-|
|└─pctChange|number|当日涨跌幅（%）。|-|
|└─currentPrice|number|当前价（股票为收盘价，板块 / 概念为指数）。|-|
|└─concept|string|概念标签（如热门 AI 个股可能标 {@code "ChatGPT,人工智能"}）。|-|
|└─rankReason|string|上榜原因（中文，如 {@code "连续涨停"} / {@code "成交活跃"}）。|-|
|└─hot|number|热度值（数值越大热度越高，是排名依据）。|-|
|└─rankTime|string|排名时间（精确到分钟，如 {@code "2026-04-30 14:30:00"}）。|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "tradeDate": "",
      "dataType": "",
      "tsCode": "",
      "tsName": "",
      "rankNum": 0,
      "pctChange": 0,
      "currentPrice": 0,
      "concept": "",
      "rankReason": "",
      "hot": 0,
      "rankTime": ""
    }
  ],
  "traceId": ""
}
```

### 涨跌停分析。limitStat（U 涨停 / D 跌停 / Z 炸板）+ limit_times（连板天数）+ open_times（开板次数）。<br>tradeDate 或 tsCode 至少传一个。
**URL:** /openapi/v1/stock/market/limit-analysis

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 涨跌停分析。limitStat（U 涨停 / D 跌停 / Z 炸板）+ limit_times（连板天数）+ open_times（开板次数）。
tradeDate 或 tsCode 至少传一个。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|page|int32|false|第几页，从 1 起。默认 1。0 / 负数会被当成 1。|-|
|size|int32|false|每页记录数。默认 50，硬上限 {@value #MAX_SIZE}。<br/><p>传入超过 {@value #MAX_SIZE} 时会被自动截断到 {@value #MAX_SIZE}（不报错）。</p>|-|
|tsCode|string|false|股票代码（带交易所后缀），如 {@code "600519.SH"}。<br/><p>cyq-perf / block-trade / auction-open / auction-close / ths-concept / moneyflow-dc 等"针对单只票"的端点使用。</p>|-|
|tradeDate|string|false|交易日期，格式 {@code YYYYMMDD}（如 {@code "20260430"}）。可空。<br/><p>hot-rank / limit-analysis / hsgt-top10 / kpl-list / mainboard / guba-rank 等"按日切片"端点使用。<br/>不传时取最新交易日。</p>|-|
|startDate|string|false|起始日期，格式 {@code YYYYMMDD}。<br/><p>block-trade / hsgt-moneyflow / moneyflow-dc 等"按时间序列"端点使用。</p>|-|
|endDate|string|false|结束日期，格式 {@code YYYYMMDD}。<br/><p>同 {@link #startDate}，配套使用。</p>|-|
|nameKeyword|string|false|名称模糊匹配关键字（中文）。<br/><p>hm-list（游资名录搜索，如 {@code "宁波派"} / {@code "赵老哥"}）/ kpl-list（按概念名搜）使用。</p>|-|
|dataType|string|false|子分类标识（含义因端点而异）：<br/><br/><ul><br/>  <li><b>hot-rank（dc_hot）</b>：{@code "1"} 股票热榜 / {@code "2"} 板块热榜</li><br/>  <li><b>hsgt-top10</b>：{@code "1"} 沪股通 / {@code "2"} 深股通 / {@code "3"} 港股通</li><br/>  <li><b>cyq-perf</b>：{@code "D"} 日 / {@code "W"} 周 / {@code "M"} 月</li><br/></ul>|-|
|limitStat|string|false|涨跌停状态过滤（仅 limit-analysis 端点用）。<br/><br/><ul><br/>  <li>{@code "U"} —— 涨停</li><br/>  <li>{@code "D"} —— 跌停</li><br/>  <li>空 —— 不过滤</li><br/></ul>|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/stock/market/limit-analysis?page=0&size=0&nameKeyword=&tradeDate=&dataType=&limitStat=&endDate=&startDate=&tsCode='
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─tradeDate|string|交易日期，格式 {@code YYYYMMDD}。|-|
|└─tsCode|string|股票代码（带交易所后缀），如 {@code "600519.SH"}。|-|
|└─name|string|股票中文简称。|-|
|└─industry|string|所属申万行业，如 {@code "白酒"} / {@code "半导体"}。|-|
|└─close|number|当日收盘价（元）。涨停时 close = preClose × (1 + 涨停幅度)。|-|
|└─pctChg|number|当日涨跌幅（%）。涨停一般为 +10% / +20%（创 / 科创板）/ +30%（北交所）。|-|
|└─swing|number|振幅（%）= (high − low) / preClose × 100。|-|
|└─amount|number|成交额|-|
|└─limitAmount|number|涨停成交额|-|
|└─floatMv|number|流通市值|-|
|└─totalMv|number|总市值|-|
|└─turnoverRatio|number|换手率|-|
|└─fdAmount|number|封单金额|-|
|└─firstTime|string|首次涨停时间|-|
|└─lastTime|string|最后涨停时间|-|
|└─openTimes|int32|开板次数|-|
|└─upStat|string|N天N板（如 "3天3板"）|-|
|└─limitTimes|int32|连板次数|-|
|└─limitStat|string|涨跌停状态：U / D / Z|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "tradeDate": "",
      "tsCode": "",
      "name": "",
      "industry": "",
      "close": 0,
      "pctChg": 0,
      "swing": 0,
      "amount": 0,
      "limitAmount": 0,
      "floatMv": 0,
      "totalMv": 0,
      "turnoverRatio": 0,
      "fdAmount": 0,
      "firstTime": "",
      "lastTime": "",
      "openTimes": 0,
      "upStat": "",
      "limitTimes": 0,
      "limitStat": ""
    }
  ],
  "traceId": ""
}
```

### 大宗交易（block trade）。tsCode 必填；按交易日范围过滤。
**URL:** /openapi/v1/stock/market/block-trade

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 大宗交易（block trade）。tsCode 必填；按交易日范围过滤。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|page|int32|false|第几页，从 1 起。默认 1。0 / 负数会被当成 1。|-|
|size|int32|false|每页记录数。默认 50，硬上限 {@value #MAX_SIZE}。<br/><p>传入超过 {@value #MAX_SIZE} 时会被自动截断到 {@value #MAX_SIZE}（不报错）。</p>|-|
|tsCode|string|false|股票代码（带交易所后缀），如 {@code "600519.SH"}。<br/><p>cyq-perf / block-trade / auction-open / auction-close / ths-concept / moneyflow-dc 等"针对单只票"的端点使用。</p>|-|
|tradeDate|string|false|交易日期，格式 {@code YYYYMMDD}（如 {@code "20260430"}）。可空。<br/><p>hot-rank / limit-analysis / hsgt-top10 / kpl-list / mainboard / guba-rank 等"按日切片"端点使用。<br/>不传时取最新交易日。</p>|-|
|startDate|string|false|起始日期，格式 {@code YYYYMMDD}。<br/><p>block-trade / hsgt-moneyflow / moneyflow-dc 等"按时间序列"端点使用。</p>|-|
|endDate|string|false|结束日期，格式 {@code YYYYMMDD}。<br/><p>同 {@link #startDate}，配套使用。</p>|-|
|nameKeyword|string|false|名称模糊匹配关键字（中文）。<br/><p>hm-list（游资名录搜索，如 {@code "宁波派"} / {@code "赵老哥"}）/ kpl-list（按概念名搜）使用。</p>|-|
|dataType|string|false|子分类标识（含义因端点而异）：<br/><br/><ul><br/>  <li><b>hot-rank（dc_hot）</b>：{@code "1"} 股票热榜 / {@code "2"} 板块热榜</li><br/>  <li><b>hsgt-top10</b>：{@code "1"} 沪股通 / {@code "2"} 深股通 / {@code "3"} 港股通</li><br/>  <li><b>cyq-perf</b>：{@code "D"} 日 / {@code "W"} 周 / {@code "M"} 月</li><br/></ul>|-|
|limitStat|string|false|涨跌停状态过滤（仅 limit-analysis 端点用）。<br/><br/><ul><br/>  <li>{@code "U"} —— 涨停</li><br/>  <li>{@code "D"} —— 跌停</li><br/>  <li>空 —— 不过滤</li><br/></ul>|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/stock/market/block-trade?page=0&size=0&limitStat=&startDate=&endDate=&tradeDate=&nameKeyword=&tsCode=&dataType='
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─tsCode|string|No comments found.|-|
|└─tradeDate|string|No comments found.|-|
|└─price|number|成交价格|-|
|└─vol|number|成交量（万股）|-|
|└─amount|number|成交金额（万元）|-|
|└─buyer|string|买方机构|-|
|└─seller|string|卖方机构|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "tsCode": "",
      "tradeDate": "",
      "price": 0,
      "vol": 0,
      "amount": 0,
      "buyer": "",
      "seller": ""
    }
  ],
  "traceId": ""
}
```

### 开盘集合竞价（盘前情绪）。tsCode / tradeDate / 日期范围至少一个。
**URL:** /openapi/v1/stock/market/auction-open

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 开盘集合竞价（盘前情绪）。tsCode / tradeDate / 日期范围至少一个。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|page|int32|false|第几页，从 1 起。默认 1。0 / 负数会被当成 1。|-|
|size|int32|false|每页记录数。默认 50，硬上限 {@value #MAX_SIZE}。<br/><p>传入超过 {@value #MAX_SIZE} 时会被自动截断到 {@value #MAX_SIZE}（不报错）。</p>|-|
|tsCode|string|false|股票代码（带交易所后缀），如 {@code "600519.SH"}。<br/><p>cyq-perf / block-trade / auction-open / auction-close / ths-concept / moneyflow-dc 等"针对单只票"的端点使用。</p>|-|
|tradeDate|string|false|交易日期，格式 {@code YYYYMMDD}（如 {@code "20260430"}）。可空。<br/><p>hot-rank / limit-analysis / hsgt-top10 / kpl-list / mainboard / guba-rank 等"按日切片"端点使用。<br/>不传时取最新交易日。</p>|-|
|startDate|string|false|起始日期，格式 {@code YYYYMMDD}。<br/><p>block-trade / hsgt-moneyflow / moneyflow-dc 等"按时间序列"端点使用。</p>|-|
|endDate|string|false|结束日期，格式 {@code YYYYMMDD}。<br/><p>同 {@link #startDate}，配套使用。</p>|-|
|nameKeyword|string|false|名称模糊匹配关键字（中文）。<br/><p>hm-list（游资名录搜索，如 {@code "宁波派"} / {@code "赵老哥"}）/ kpl-list（按概念名搜）使用。</p>|-|
|dataType|string|false|子分类标识（含义因端点而异）：<br/><br/><ul><br/>  <li><b>hot-rank（dc_hot）</b>：{@code "1"} 股票热榜 / {@code "2"} 板块热榜</li><br/>  <li><b>hsgt-top10</b>：{@code "1"} 沪股通 / {@code "2"} 深股通 / {@code "3"} 港股通</li><br/>  <li><b>cyq-perf</b>：{@code "D"} 日 / {@code "W"} 周 / {@code "M"} 月</li><br/></ul>|-|
|limitStat|string|false|涨跌停状态过滤（仅 limit-analysis 端点用）。<br/><br/><ul><br/>  <li>{@code "U"} —— 涨停</li><br/>  <li>{@code "D"} —— 跌停</li><br/>  <li>空 —— 不过滤</li><br/></ul>|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/stock/market/auction-open?page=0&size=0&tradeDate=&limitStat=&startDate=&dataType=&endDate=&tsCode=&nameKeyword='
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─tsCode|string|股票代码（带交易所后缀），如 {@code "600519.SH"}。|-|
|└─tradeDate|string|交易日期，格式 {@code YYYYMMDD}。|-|
|└─name|string|股票中文简称。|-|
|└─openPrice|number|开盘价（元，9:25 开盘集合竞价决定）。|-|
|└─preClose|number|昨收价|-|
|└─pctChange|number|较昨收涨跌幅 %|-|
|└─vol|number|开盘成交量|-|
|└─amount|number|开盘成交额|-|
|└─preVol|number|昨日成交量（用于对比量比）|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "tsCode": "",
      "tradeDate": "",
      "name": "",
      "openPrice": 0,
      "preClose": 0,
      "pctChange": 0,
      "vol": 0,
      "amount": 0,
      "preVol": 0
    }
  ],
  "traceId": ""
}
```

### 每日筹码胜率（cyq）。winner_rate / 5%~95% 分位成本 / 加权均价。<br>tsCode 必填。
**URL:** /openapi/v1/stock/market/cyq-perf

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 每日筹码胜率（cyq）。winner_rate / 5%~95% 分位成本 / 加权均价。
tsCode 必填。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|page|int32|false|第几页，从 1 起。默认 1。0 / 负数会被当成 1。|-|
|size|int32|false|每页记录数。默认 50，硬上限 {@value #MAX_SIZE}。<br/><p>传入超过 {@value #MAX_SIZE} 时会被自动截断到 {@value #MAX_SIZE}（不报错）。</p>|-|
|tsCode|string|false|股票代码（带交易所后缀），如 {@code "600519.SH"}。<br/><p>cyq-perf / block-trade / auction-open / auction-close / ths-concept / moneyflow-dc 等"针对单只票"的端点使用。</p>|-|
|tradeDate|string|false|交易日期，格式 {@code YYYYMMDD}（如 {@code "20260430"}）。可空。<br/><p>hot-rank / limit-analysis / hsgt-top10 / kpl-list / mainboard / guba-rank 等"按日切片"端点使用。<br/>不传时取最新交易日。</p>|-|
|startDate|string|false|起始日期，格式 {@code YYYYMMDD}。<br/><p>block-trade / hsgt-moneyflow / moneyflow-dc 等"按时间序列"端点使用。</p>|-|
|endDate|string|false|结束日期，格式 {@code YYYYMMDD}。<br/><p>同 {@link #startDate}，配套使用。</p>|-|
|nameKeyword|string|false|名称模糊匹配关键字（中文）。<br/><p>hm-list（游资名录搜索，如 {@code "宁波派"} / {@code "赵老哥"}）/ kpl-list（按概念名搜）使用。</p>|-|
|dataType|string|false|子分类标识（含义因端点而异）：<br/><br/><ul><br/>  <li><b>hot-rank（dc_hot）</b>：{@code "1"} 股票热榜 / {@code "2"} 板块热榜</li><br/>  <li><b>hsgt-top10</b>：{@code "1"} 沪股通 / {@code "2"} 深股通 / {@code "3"} 港股通</li><br/>  <li><b>cyq-perf</b>：{@code "D"} 日 / {@code "W"} 周 / {@code "M"} 月</li><br/></ul>|-|
|limitStat|string|false|涨跌停状态过滤（仅 limit-analysis 端点用）。<br/><br/><ul><br/>  <li>{@code "U"} —— 涨停</li><br/>  <li>{@code "D"} —— 跌停</li><br/>  <li>空 —— 不过滤</li><br/></ul>|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/stock/market/cyq-perf?page=0&size=0&tsCode=&endDate=&nameKeyword=&limitStat=&tradeDate=&dataType=&startDate='
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─tsCode|string|No comments found.|-|
|└─tradeDate|string|No comments found.|-|
|└─hisLow|number|历史最低价|-|
|└─hisHigh|number|历史最高价|-|
|└─cost5pct|number|5% 分位成本|-|
|└─cost15pct|number|15% 分位成本|-|
|└─cost50pct|number|50% 分位成本（中位数）|-|
|└─cost85pct|number|85% 分位成本|-|
|└─cost95pct|number|95% 分位成本|-|
|└─weightAvg|number|加权平均成本|-|
|└─winnerRate|number|胜率（盈利筹码占比 %）|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "tsCode": "",
      "tradeDate": "",
      "hisLow": 0,
      "hisHigh": 0,
      "cost5pct": 0,
      "cost15pct": 0,
      "cost50pct": 0,
      "cost85pct": 0,
      "cost95pct": 0,
      "weightAvg": 0,
      "winnerRate": 0
    }
  ],
  "traceId": ""
}
```

### 沪深股通十大成交股。dataType 字段承载 marketType（1 沪股通 / 3 深股通 / 2 港股通沪 / 4 港股通深）。<br>tradeDate 或 tsCode 至少传一个。
**URL:** /openapi/v1/stock/market/hsgt-top10

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 沪深股通十大成交股。dataType 字段承载 marketType（1 沪股通 / 3 深股通 / 2 港股通沪 / 4 港股通深）。
tradeDate 或 tsCode 至少传一个。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|page|int32|false|第几页，从 1 起。默认 1。0 / 负数会被当成 1。|-|
|size|int32|false|每页记录数。默认 50，硬上限 {@value #MAX_SIZE}。<br/><p>传入超过 {@value #MAX_SIZE} 时会被自动截断到 {@value #MAX_SIZE}（不报错）。</p>|-|
|tsCode|string|false|股票代码（带交易所后缀），如 {@code "600519.SH"}。<br/><p>cyq-perf / block-trade / auction-open / auction-close / ths-concept / moneyflow-dc 等"针对单只票"的端点使用。</p>|-|
|tradeDate|string|false|交易日期，格式 {@code YYYYMMDD}（如 {@code "20260430"}）。可空。<br/><p>hot-rank / limit-analysis / hsgt-top10 / kpl-list / mainboard / guba-rank 等"按日切片"端点使用。<br/>不传时取最新交易日。</p>|-|
|startDate|string|false|起始日期，格式 {@code YYYYMMDD}。<br/><p>block-trade / hsgt-moneyflow / moneyflow-dc 等"按时间序列"端点使用。</p>|-|
|endDate|string|false|结束日期，格式 {@code YYYYMMDD}。<br/><p>同 {@link #startDate}，配套使用。</p>|-|
|nameKeyword|string|false|名称模糊匹配关键字（中文）。<br/><p>hm-list（游资名录搜索，如 {@code "宁波派"} / {@code "赵老哥"}）/ kpl-list（按概念名搜）使用。</p>|-|
|dataType|string|false|子分类标识（含义因端点而异）：<br/><br/><ul><br/>  <li><b>hot-rank（dc_hot）</b>：{@code "1"} 股票热榜 / {@code "2"} 板块热榜</li><br/>  <li><b>hsgt-top10</b>：{@code "1"} 沪股通 / {@code "2"} 深股通 / {@code "3"} 港股通</li><br/>  <li><b>cyq-perf</b>：{@code "D"} 日 / {@code "W"} 周 / {@code "M"} 月</li><br/></ul>|-|
|limitStat|string|false|涨跌停状态过滤（仅 limit-analysis 端点用）。<br/><br/><ul><br/>  <li>{@code "U"} —— 涨停</li><br/>  <li>{@code "D"} —— 跌停</li><br/>  <li>空 —— 不过滤</li><br/></ul>|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/stock/market/hsgt-top10?page=0&size=0&tradeDate=&endDate=&nameKeyword=&dataType=&tsCode=&limitStat=&startDate='
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─tradeDate|string|交易日期，格式 {@code YYYYMMDD}。|-|
|└─tsCode|string|股票代码（带交易所后缀），如 {@code "600519.SH"}。|-|
|└─name|string|股票中文简称。|-|
|└─close|number|当日收盘价（元）。|-|
|└─chg|number|当日涨跌幅（%）。|-|
|└─rankNum|int32|当日 top10 中的排名，1~10。|-|
|└─marketType|string|市场类型：<br/><ul><br/>  <li>{@code "1"} —— 沪股通（北向，外资买 A 股沪市）</li><br/>  <li>{@code "3"} —— 深股通（北向，外资买 A 股深市）</li><br/>  <li>{@code "2"} —— 港股通（沪，南向，A 股资金买港股）</li><br/>  <li>{@code "4"} —— 港股通（深，南向）</li><br/></ul>|-|
|└─amount|number|当日通过通道的总成交额（元）= buy + sell。|-|
|└─netAmount|number|净流入额（元）= buy − sell。{@code > 0} 净买入（外资看好），{@code < 0} 净卖出。|-|
|└─buy|number|通过通道买入额（元）。|-|
|└─sell|number|通过通道卖出额（元）。|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "tradeDate": "",
      "tsCode": "",
      "name": "",
      "close": 0,
      "chg": 0,
      "rankNum": 0,
      "marketType": "",
      "amount": 0,
      "netAmount": 0,
      "buy": 0,
      "sell": 0
    }
  ],
  "traceId": ""
}
```

### 沪深港通资金流向汇总（北向 / 南向每日总额）。
**URL:** /openapi/v1/stock/market/hsgt-moneyflow

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 沪深港通资金流向汇总（北向 / 南向每日总额）。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|page|int32|false|第几页，从 1 起。默认 1。0 / 负数会被当成 1。|-|
|size|int32|false|每页记录数。默认 50，硬上限 {@value #MAX_SIZE}。<br/><p>传入超过 {@value #MAX_SIZE} 时会被自动截断到 {@value #MAX_SIZE}（不报错）。</p>|-|
|tsCode|string|false|股票代码（带交易所后缀），如 {@code "600519.SH"}。<br/><p>cyq-perf / block-trade / auction-open / auction-close / ths-concept / moneyflow-dc 等"针对单只票"的端点使用。</p>|-|
|tradeDate|string|false|交易日期，格式 {@code YYYYMMDD}（如 {@code "20260430"}）。可空。<br/><p>hot-rank / limit-analysis / hsgt-top10 / kpl-list / mainboard / guba-rank 等"按日切片"端点使用。<br/>不传时取最新交易日。</p>|-|
|startDate|string|false|起始日期，格式 {@code YYYYMMDD}。<br/><p>block-trade / hsgt-moneyflow / moneyflow-dc 等"按时间序列"端点使用。</p>|-|
|endDate|string|false|结束日期，格式 {@code YYYYMMDD}。<br/><p>同 {@link #startDate}，配套使用。</p>|-|
|nameKeyword|string|false|名称模糊匹配关键字（中文）。<br/><p>hm-list（游资名录搜索，如 {@code "宁波派"} / {@code "赵老哥"}）/ kpl-list（按概念名搜）使用。</p>|-|
|dataType|string|false|子分类标识（含义因端点而异）：<br/><br/><ul><br/>  <li><b>hot-rank（dc_hot）</b>：{@code "1"} 股票热榜 / {@code "2"} 板块热榜</li><br/>  <li><b>hsgt-top10</b>：{@code "1"} 沪股通 / {@code "2"} 深股通 / {@code "3"} 港股通</li><br/>  <li><b>cyq-perf</b>：{@code "D"} 日 / {@code "W"} 周 / {@code "M"} 月</li><br/></ul>|-|
|limitStat|string|false|涨跌停状态过滤（仅 limit-analysis 端点用）。<br/><br/><ul><br/>  <li>{@code "U"} —— 涨停</li><br/>  <li>{@code "D"} —— 跌停</li><br/>  <li>空 —— 不过滤</li><br/></ul>|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/stock/market/hsgt-moneyflow?page=0&size=0&startDate=&endDate=&dataType=&limitStat=&tradeDate=&nameKeyword=&tsCode='
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─tradeDate|string|No comments found.|-|
|└─ggtSs|number|港股通（沪）|-|
|└─ggtSz|number|港股通（深）|-|
|└─hgt|number|沪股通|-|
|└─sgt|number|深股通|-|
|└─northMoney|number|北向资金净流入|-|
|└─southMoney|number|南向资金净流入|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "tradeDate": "",
      "ggtSs": 0,
      "ggtSz": 0,
      "hgt": 0,
      "sgt": 0,
      "northMoney": 0,
      "southMoney": 0
    }
  ],
  "traceId": ""
}
```

### 游资名录（hm_list）。仅按 nameKeyword 模糊搜索。
**URL:** /openapi/v1/stock/market/hm-list

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 游资名录（hm_list）。仅按 nameKeyword 模糊搜索。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|page|int32|false|第几页，从 1 起。默认 1。0 / 负数会被当成 1。|-|
|size|int32|false|每页记录数。默认 50，硬上限 {@value #MAX_SIZE}。<br/><p>传入超过 {@value #MAX_SIZE} 时会被自动截断到 {@value #MAX_SIZE}（不报错）。</p>|-|
|tsCode|string|false|股票代码（带交易所后缀），如 {@code "600519.SH"}。<br/><p>cyq-perf / block-trade / auction-open / auction-close / ths-concept / moneyflow-dc 等"针对单只票"的端点使用。</p>|-|
|tradeDate|string|false|交易日期，格式 {@code YYYYMMDD}（如 {@code "20260430"}）。可空。<br/><p>hot-rank / limit-analysis / hsgt-top10 / kpl-list / mainboard / guba-rank 等"按日切片"端点使用。<br/>不传时取最新交易日。</p>|-|
|startDate|string|false|起始日期，格式 {@code YYYYMMDD}。<br/><p>block-trade / hsgt-moneyflow / moneyflow-dc 等"按时间序列"端点使用。</p>|-|
|endDate|string|false|结束日期，格式 {@code YYYYMMDD}。<br/><p>同 {@link #startDate}，配套使用。</p>|-|
|nameKeyword|string|false|名称模糊匹配关键字（中文）。<br/><p>hm-list（游资名录搜索，如 {@code "宁波派"} / {@code "赵老哥"}）/ kpl-list（按概念名搜）使用。</p>|-|
|dataType|string|false|子分类标识（含义因端点而异）：<br/><br/><ul><br/>  <li><b>hot-rank（dc_hot）</b>：{@code "1"} 股票热榜 / {@code "2"} 板块热榜</li><br/>  <li><b>hsgt-top10</b>：{@code "1"} 沪股通 / {@code "2"} 深股通 / {@code "3"} 港股通</li><br/>  <li><b>cyq-perf</b>：{@code "D"} 日 / {@code "W"} 周 / {@code "M"} 月</li><br/></ul>|-|
|limitStat|string|false|涨跌停状态过滤（仅 limit-analysis 端点用）。<br/><br/><ul><br/>  <li>{@code "U"} —— 涨停</li><br/>  <li>{@code "D"} —— 跌停</li><br/>  <li>空 —— 不过滤</li><br/></ul>|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/stock/market/hm-list?page=0&size=0&nameKeyword=&tsCode=&startDate=&limitStat=&endDate=&tradeDate=&dataType='
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─name|string|游资名称|-|
|└─description|string|描述|-|
|└─orgs|string|关联机构|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "name": "",
      "description": "",
      "orgs": ""
    }
  ],
  "traceId": ""
}
```

### 开盘啦榜单（kpl_list）。dataType 字段承载 tag（榜单类型）。<br>tradeDate 或 tsCode 至少传一个。
**URL:** /openapi/v1/stock/market/kpl-list

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 开盘啦榜单（kpl_list）。dataType 字段承载 tag（榜单类型）。
tradeDate 或 tsCode 至少传一个。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|page|int32|false|第几页，从 1 起。默认 1。0 / 负数会被当成 1。|-|
|size|int32|false|每页记录数。默认 50，硬上限 {@value #MAX_SIZE}。<br/><p>传入超过 {@value #MAX_SIZE} 时会被自动截断到 {@value #MAX_SIZE}（不报错）。</p>|-|
|tsCode|string|false|股票代码（带交易所后缀），如 {@code "600519.SH"}。<br/><p>cyq-perf / block-trade / auction-open / auction-close / ths-concept / moneyflow-dc 等"针对单只票"的端点使用。</p>|-|
|tradeDate|string|false|交易日期，格式 {@code YYYYMMDD}（如 {@code "20260430"}）。可空。<br/><p>hot-rank / limit-analysis / hsgt-top10 / kpl-list / mainboard / guba-rank 等"按日切片"端点使用。<br/>不传时取最新交易日。</p>|-|
|startDate|string|false|起始日期，格式 {@code YYYYMMDD}。<br/><p>block-trade / hsgt-moneyflow / moneyflow-dc 等"按时间序列"端点使用。</p>|-|
|endDate|string|false|结束日期，格式 {@code YYYYMMDD}。<br/><p>同 {@link #startDate}，配套使用。</p>|-|
|nameKeyword|string|false|名称模糊匹配关键字（中文）。<br/><p>hm-list（游资名录搜索，如 {@code "宁波派"} / {@code "赵老哥"}）/ kpl-list（按概念名搜）使用。</p>|-|
|dataType|string|false|子分类标识（含义因端点而异）：<br/><br/><ul><br/>  <li><b>hot-rank（dc_hot）</b>：{@code "1"} 股票热榜 / {@code "2"} 板块热榜</li><br/>  <li><b>hsgt-top10</b>：{@code "1"} 沪股通 / {@code "2"} 深股通 / {@code "3"} 港股通</li><br/>  <li><b>cyq-perf</b>：{@code "D"} 日 / {@code "W"} 周 / {@code "M"} 月</li><br/></ul>|-|
|limitStat|string|false|涨跌停状态过滤（仅 limit-analysis 端点用）。<br/><br/><ul><br/>  <li>{@code "U"} —— 涨停</li><br/>  <li>{@code "D"} —— 跌停</li><br/>  <li>空 —— 不过滤</li><br/></ul>|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/stock/market/kpl-list?page=0&size=0&startDate=&tradeDate=&tsCode=&dataType=&nameKeyword=&limitStat=&endDate='
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─tsCode|string|股票代码（带交易所后缀），如 {@code "600519.SH"}。|-|
|└─name|string|股票中文简称。|-|
|└─tradeDate|string|交易日期，格式 {@code YYYYMMDD}。|-|
|└─luTime|string|首次涨停时间，格式 {@code HH:mm:ss}（如 {@code "09:32:15"}）。|-|
|└─ldTime|string|跌停时间|-|
|└─openTime|string|开板时间|-|
|└─lastTime|string|最后封板时间|-|
|└─luDesc|string|涨停原因|-|
|└─tag|string|榜单类型（涨停 / 炸板 / 连板 等）|-|
|└─theme|string|题材|-|
|└─netChange|number|净额|-|
|└─bidAmount|number|封单金额|-|
|└─status|string|状态|-|
|└─upDays|int32|连板天数|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "tsCode": "",
      "name": "",
      "tradeDate": "",
      "luTime": "",
      "ldTime": "",
      "openTime": "",
      "lastTime": "",
      "luDesc": "",
      "tag": "",
      "theme": "",
      "netChange": 0,
      "bidAmount": 0,
      "status": "",
      "upDays": 0
    }
  ],
  "traceId": ""
}
```

### 同花顺概念成分股。tsCode 是概念代码（如 885589.TI），dataType 字段承载 code（成分股代码）。<br>两者至少传一个。
**URL:** /openapi/v1/stock/market/ths-concept

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 同花顺概念成分股。tsCode 是概念代码（如 885589.TI），dataType 字段承载 code（成分股代码）。
两者至少传一个。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|page|int32|false|第几页，从 1 起。默认 1。0 / 负数会被当成 1。|-|
|size|int32|false|每页记录数。默认 50，硬上限 {@value #MAX_SIZE}。<br/><p>传入超过 {@value #MAX_SIZE} 时会被自动截断到 {@value #MAX_SIZE}（不报错）。</p>|-|
|tsCode|string|false|股票代码（带交易所后缀），如 {@code "600519.SH"}。<br/><p>cyq-perf / block-trade / auction-open / auction-close / ths-concept / moneyflow-dc 等"针对单只票"的端点使用。</p>|-|
|tradeDate|string|false|交易日期，格式 {@code YYYYMMDD}（如 {@code "20260430"}）。可空。<br/><p>hot-rank / limit-analysis / hsgt-top10 / kpl-list / mainboard / guba-rank 等"按日切片"端点使用。<br/>不传时取最新交易日。</p>|-|
|startDate|string|false|起始日期，格式 {@code YYYYMMDD}。<br/><p>block-trade / hsgt-moneyflow / moneyflow-dc 等"按时间序列"端点使用。</p>|-|
|endDate|string|false|结束日期，格式 {@code YYYYMMDD}。<br/><p>同 {@link #startDate}，配套使用。</p>|-|
|nameKeyword|string|false|名称模糊匹配关键字（中文）。<br/><p>hm-list（游资名录搜索，如 {@code "宁波派"} / {@code "赵老哥"}）/ kpl-list（按概念名搜）使用。</p>|-|
|dataType|string|false|子分类标识（含义因端点而异）：<br/><br/><ul><br/>  <li><b>hot-rank（dc_hot）</b>：{@code "1"} 股票热榜 / {@code "2"} 板块热榜</li><br/>  <li><b>hsgt-top10</b>：{@code "1"} 沪股通 / {@code "2"} 深股通 / {@code "3"} 港股通</li><br/>  <li><b>cyq-perf</b>：{@code "D"} 日 / {@code "W"} 周 / {@code "M"} 月</li><br/></ul>|-|
|limitStat|string|false|涨跌停状态过滤（仅 limit-analysis 端点用）。<br/><br/><ul><br/>  <li>{@code "U"} —— 涨停</li><br/>  <li>{@code "D"} —— 跌停</li><br/>  <li>空 —— 不过滤</li><br/></ul>|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/stock/market/ths-concept?page=0&size=0&endDate=&limitStat=&startDate=&dataType=&tradeDate=&nameKeyword=&tsCode='
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─tsCode|string|概念代码|-|
|└─code|string|成分股代码|-|
|└─name|string|成分股名称|-|
|└─weight|number|权重 %|-|
|└─inDate|string|入选日期|-|
|└─outDate|string|退出日期（在板内为空）|-|
|└─isNew|string|是否新进 Y/N|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "tsCode": "",
      "code": "",
      "name": "",
      "weight": 0,
      "inDate": "",
      "outDate": "",
      "isNew": ""
    }
  ],
  "traceId": ""
}
```

### 个股资金流（东方财富口径）。tsCode 必填；按金额分超大单 / 大单 / 中单 / 小单。
**URL:** /openapi/v1/stock/market/moneyflow-dc

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 个股资金流（东方财富口径）。tsCode 必填；按金额分超大单 / 大单 / 中单 / 小单。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|page|int32|false|第几页，从 1 起。默认 1。0 / 负数会被当成 1。|-|
|size|int32|false|每页记录数。默认 50，硬上限 {@value #MAX_SIZE}。<br/><p>传入超过 {@value #MAX_SIZE} 时会被自动截断到 {@value #MAX_SIZE}（不报错）。</p>|-|
|tsCode|string|false|股票代码（带交易所后缀），如 {@code "600519.SH"}。<br/><p>cyq-perf / block-trade / auction-open / auction-close / ths-concept / moneyflow-dc 等"针对单只票"的端点使用。</p>|-|
|tradeDate|string|false|交易日期，格式 {@code YYYYMMDD}（如 {@code "20260430"}）。可空。<br/><p>hot-rank / limit-analysis / hsgt-top10 / kpl-list / mainboard / guba-rank 等"按日切片"端点使用。<br/>不传时取最新交易日。</p>|-|
|startDate|string|false|起始日期，格式 {@code YYYYMMDD}。<br/><p>block-trade / hsgt-moneyflow / moneyflow-dc 等"按时间序列"端点使用。</p>|-|
|endDate|string|false|结束日期，格式 {@code YYYYMMDD}。<br/><p>同 {@link #startDate}，配套使用。</p>|-|
|nameKeyword|string|false|名称模糊匹配关键字（中文）。<br/><p>hm-list（游资名录搜索，如 {@code "宁波派"} / {@code "赵老哥"}）/ kpl-list（按概念名搜）使用。</p>|-|
|dataType|string|false|子分类标识（含义因端点而异）：<br/><br/><ul><br/>  <li><b>hot-rank（dc_hot）</b>：{@code "1"} 股票热榜 / {@code "2"} 板块热榜</li><br/>  <li><b>hsgt-top10</b>：{@code "1"} 沪股通 / {@code "2"} 深股通 / {@code "3"} 港股通</li><br/>  <li><b>cyq-perf</b>：{@code "D"} 日 / {@code "W"} 周 / {@code "M"} 月</li><br/></ul>|-|
|limitStat|string|false|涨跌停状态过滤（仅 limit-analysis 端点用）。<br/><br/><ul><br/>  <li>{@code "U"} —— 涨停</li><br/>  <li>{@code "D"} —— 跌停</li><br/>  <li>空 —— 不过滤</li><br/></ul>|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/stock/market/moneyflow-dc?page=0&size=0&dataType=&startDate=&limitStat=&nameKeyword=&tsCode=&tradeDate=&endDate='
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─tsCode|string|股票代码（带交易所后缀），如 {@code "600519.SH"}。|-|
|└─tradeDate|string|交易日期，格式 {@code YYYYMMDD}。|-|
|└─name|string|股票中文简称。|-|
|└─pctChange|number|涨跌幅（%）。|-|
|└─close|number|当日收盘价（元）。|-|
|└─netAmount|number|主力净流入金额（万元）。{@code > 0} 主力净买入。|-|
|└─netAmountRate|number|主力净流入占当日总成交比例（%）。|-|
|└─buyElgAmount|number|超大单（订单 ≥ 100 万）净流入（万元）。|-|
|└─buyElgAmountRate|number|超大单净流入占比（%）。|-|
|└─buyLgAmount|number|大单（20~100 万）净流入（万元）。|-|
|└─buyLgAmountRate|number|大单净流入占比（%）。|-|
|└─buyMdAmount|number|中单（4~20 万）净流入（万元）。|-|
|└─buyMdAmountRate|number|中单净流入占比（%）。|-|
|└─buySmAmount|number|小单（< 4 万）净流入（万元）。|-|
|└─buySmAmountRate|number|小单净流入占比（%）。|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "tsCode": "",
      "tradeDate": "",
      "name": "",
      "pctChange": 0,
      "close": 0,
      "netAmount": 0,
      "netAmountRate": 0,
      "buyElgAmount": 0,
      "buyElgAmountRate": 0,
      "buyLgAmount": 0,
      "buyLgAmountRate": 0,
      "buyMdAmount": 0,
      "buyMdAmountRate": 0,
      "buySmAmount": 0,
      "buySmAmountRate": 0
    }
  ],
  "traceId": ""
}
```

### 大盘整体行情 + 资金流（沪深合并）。需 tradeDate 或 startDate/endDate 至少一个。
**URL:** /openapi/v1/stock/market/mainboard

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 大盘整体行情 + 资金流（沪深合并）。需 tradeDate 或 startDate/endDate 至少一个。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|page|int32|false|第几页，从 1 起。默认 1。0 / 负数会被当成 1。|-|
|size|int32|false|每页记录数。默认 50，硬上限 {@value #MAX_SIZE}。<br/><p>传入超过 {@value #MAX_SIZE} 时会被自动截断到 {@value #MAX_SIZE}（不报错）。</p>|-|
|tsCode|string|false|股票代码（带交易所后缀），如 {@code "600519.SH"}。<br/><p>cyq-perf / block-trade / auction-open / auction-close / ths-concept / moneyflow-dc 等"针对单只票"的端点使用。</p>|-|
|tradeDate|string|false|交易日期，格式 {@code YYYYMMDD}（如 {@code "20260430"}）。可空。<br/><p>hot-rank / limit-analysis / hsgt-top10 / kpl-list / mainboard / guba-rank 等"按日切片"端点使用。<br/>不传时取最新交易日。</p>|-|
|startDate|string|false|起始日期，格式 {@code YYYYMMDD}。<br/><p>block-trade / hsgt-moneyflow / moneyflow-dc 等"按时间序列"端点使用。</p>|-|
|endDate|string|false|结束日期，格式 {@code YYYYMMDD}。<br/><p>同 {@link #startDate}，配套使用。</p>|-|
|nameKeyword|string|false|名称模糊匹配关键字（中文）。<br/><p>hm-list（游资名录搜索，如 {@code "宁波派"} / {@code "赵老哥"}）/ kpl-list（按概念名搜）使用。</p>|-|
|dataType|string|false|子分类标识（含义因端点而异）：<br/><br/><ul><br/>  <li><b>hot-rank（dc_hot）</b>：{@code "1"} 股票热榜 / {@code "2"} 板块热榜</li><br/>  <li><b>hsgt-top10</b>：{@code "1"} 沪股通 / {@code "2"} 深股通 / {@code "3"} 港股通</li><br/>  <li><b>cyq-perf</b>：{@code "D"} 日 / {@code "W"} 周 / {@code "M"} 月</li><br/></ul>|-|
|limitStat|string|false|涨跌停状态过滤（仅 limit-analysis 端点用）。<br/><br/><ul><br/>  <li>{@code "U"} —— 涨停</li><br/>  <li>{@code "D"} —— 跌停</li><br/>  <li>空 —— 不过滤</li><br/></ul>|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/stock/market/mainboard?page=0&size=0&dataType=&tsCode=&nameKeyword=&endDate=&limitStat=&startDate=&tradeDate='
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─tradeDate|string|交易日期，格式 {@code YYYYMMDD}。|-|
|└─closeSh|number|上证综指收盘点位。|-|
|└─pctChangeSh|number|上证综指当日涨跌幅（%）。|-|
|└─closeSz|number|深证成指收盘点位。|-|
|└─pctChangeSz|number|深证成指当日涨跌幅（%）。|-|
|└─netAmount|number|全市场主力净流入（亿元）。{@code > 0} 主力净买入。|-|
|└─netAmountRate|number|主力净流入占当日总成交比例（%）。|-|
|└─buyElgAmount|number|超大单（订单 ≥ 100 万）净买入（亿元）。|-|
|└─buyElgAmountRate|number|超大单占比（%）。|-|
|└─buyLgAmount|number|大单（20~100 万）净买入（亿元）。|-|
|└─buyLgAmountRate|number|大单占比（%）。|-|
|└─buyMdAmount|number|中单（4~20 万）净买入（亿元）。|-|
|└─buyMdAmountRate|number|中单占比（%）。|-|
|└─buySmAmount|number|小单（< 4 万）净买入（亿元）。|-|
|└─buySmAmountRate|number|小单占比（%）。|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "tradeDate": "",
      "closeSh": 0,
      "pctChangeSh": 0,
      "closeSz": 0,
      "pctChangeSz": 0,
      "netAmount": 0,
      "netAmountRate": 0,
      "buyElgAmount": 0,
      "buyElgAmountRate": 0,
      "buyLgAmount": 0,
      "buyLgAmountRate": 0,
      "buyMdAmount": 0,
      "buyMdAmountRate": 0,
      "buySmAmount": 0,
      "buySmAmountRate": 0
    }
  ],
  "traceId": ""
}
```

### 收盘集合竞价（15:00）。tsCode 或 tradeDate 至少一个。
**URL:** /openapi/v1/stock/market/auction-close

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 收盘集合竞价（15:00）。tsCode 或 tradeDate 至少一个。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|page|int32|false|第几页，从 1 起。默认 1。0 / 负数会被当成 1。|-|
|size|int32|false|每页记录数。默认 50，硬上限 {@value #MAX_SIZE}。<br/><p>传入超过 {@value #MAX_SIZE} 时会被自动截断到 {@value #MAX_SIZE}（不报错）。</p>|-|
|tsCode|string|false|股票代码（带交易所后缀），如 {@code "600519.SH"}。<br/><p>cyq-perf / block-trade / auction-open / auction-close / ths-concept / moneyflow-dc 等"针对单只票"的端点使用。</p>|-|
|tradeDate|string|false|交易日期，格式 {@code YYYYMMDD}（如 {@code "20260430"}）。可空。<br/><p>hot-rank / limit-analysis / hsgt-top10 / kpl-list / mainboard / guba-rank 等"按日切片"端点使用。<br/>不传时取最新交易日。</p>|-|
|startDate|string|false|起始日期，格式 {@code YYYYMMDD}。<br/><p>block-trade / hsgt-moneyflow / moneyflow-dc 等"按时间序列"端点使用。</p>|-|
|endDate|string|false|结束日期，格式 {@code YYYYMMDD}。<br/><p>同 {@link #startDate}，配套使用。</p>|-|
|nameKeyword|string|false|名称模糊匹配关键字（中文）。<br/><p>hm-list（游资名录搜索，如 {@code "宁波派"} / {@code "赵老哥"}）/ kpl-list（按概念名搜）使用。</p>|-|
|dataType|string|false|子分类标识（含义因端点而异）：<br/><br/><ul><br/>  <li><b>hot-rank（dc_hot）</b>：{@code "1"} 股票热榜 / {@code "2"} 板块热榜</li><br/>  <li><b>hsgt-top10</b>：{@code "1"} 沪股通 / {@code "2"} 深股通 / {@code "3"} 港股通</li><br/>  <li><b>cyq-perf</b>：{@code "D"} 日 / {@code "W"} 周 / {@code "M"} 月</li><br/></ul>|-|
|limitStat|string|false|涨跌停状态过滤（仅 limit-analysis 端点用）。<br/><br/><ul><br/>  <li>{@code "U"} —— 涨停</li><br/>  <li>{@code "D"} —— 跌停</li><br/>  <li>空 —— 不过滤</li><br/></ul>|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/stock/market/auction-close?page=0&size=0&limitStat=&tradeDate=&startDate=&dataType=&tsCode=&nameKeyword=&endDate='
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─tsCode|string|股票代码（带交易所后缀），如 {@code "600519.SH"}。|-|
|└─tradeDate|string|交易日期，格式 {@code YYYYMMDD}。|-|
|└─name|string|股票中文简称。|-|
|└─closePrice|number|收盘竞价决定的收盘价（元）。|-|
|└─preClose|number|昨日收盘价（元）。|-|
|└─pctChange|number|较昨收涨跌幅（%）。|-|
|└─vol|number|集合竞价成交量（手）。|-|
|└─amount|number|集合竞价成交额（千元）。|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "tsCode": "",
      "tradeDate": "",
      "name": "",
      "closePrice": 0,
      "preClose": 0,
      "pctChange": 0,
      "vol": 0,
      "amount": 0
    }
  ],
  "traceId": ""
}
```

### 东财股吧排名（关注度榜单 / 个股历史）。tsCode 或 tradeDate 至少一个。
**URL:** /openapi/v1/stock/market/guba-rank

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 东财股吧排名（关注度榜单 / 个股历史）。tsCode 或 tradeDate 至少一个。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|page|int32|false|第几页，从 1 起。默认 1。0 / 负数会被当成 1。|-|
|size|int32|false|每页记录数。默认 50，硬上限 {@value #MAX_SIZE}。<br/><p>传入超过 {@value #MAX_SIZE} 时会被自动截断到 {@value #MAX_SIZE}（不报错）。</p>|-|
|tsCode|string|false|股票代码（带交易所后缀），如 {@code "600519.SH"}。<br/><p>cyq-perf / block-trade / auction-open / auction-close / ths-concept / moneyflow-dc 等"针对单只票"的端点使用。</p>|-|
|tradeDate|string|false|交易日期，格式 {@code YYYYMMDD}（如 {@code "20260430"}）。可空。<br/><p>hot-rank / limit-analysis / hsgt-top10 / kpl-list / mainboard / guba-rank 等"按日切片"端点使用。<br/>不传时取最新交易日。</p>|-|
|startDate|string|false|起始日期，格式 {@code YYYYMMDD}。<br/><p>block-trade / hsgt-moneyflow / moneyflow-dc 等"按时间序列"端点使用。</p>|-|
|endDate|string|false|结束日期，格式 {@code YYYYMMDD}。<br/><p>同 {@link #startDate}，配套使用。</p>|-|
|nameKeyword|string|false|名称模糊匹配关键字（中文）。<br/><p>hm-list（游资名录搜索，如 {@code "宁波派"} / {@code "赵老哥"}）/ kpl-list（按概念名搜）使用。</p>|-|
|dataType|string|false|子分类标识（含义因端点而异）：<br/><br/><ul><br/>  <li><b>hot-rank（dc_hot）</b>：{@code "1"} 股票热榜 / {@code "2"} 板块热榜</li><br/>  <li><b>hsgt-top10</b>：{@code "1"} 沪股通 / {@code "2"} 深股通 / {@code "3"} 港股通</li><br/>  <li><b>cyq-perf</b>：{@code "D"} 日 / {@code "W"} 周 / {@code "M"} 月</li><br/></ul>|-|
|limitStat|string|false|涨跌停状态过滤（仅 limit-analysis 端点用）。<br/><br/><ul><br/>  <li>{@code "U"} —— 涨停</li><br/>  <li>{@code "D"} —— 跌停</li><br/>  <li>空 —— 不过滤</li><br/></ul>|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/stock/market/guba-rank?page=0&size=0&nameKeyword=&dataType=&endDate=&limitStat=&tsCode=&startDate=&tradeDate='
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─tradeDate|string|No comments found.|-|
|└─tsCode|string|No comments found.|-|
|└─currentRank|int32|当日排名（数字越小越靠前）|-|
|└─rankChange|int32|排名变动（正值 = 上升）|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "tradeDate": "",
      "tsCode": "",
      "currentRank": 0,
      "rankChange": 0
    }
  ],
  "traceId": ""
}
```

### 新闻日度情绪聚合（全市场）。startDate/endDate 区间筛选。
**URL:** /openapi/v1/stock/market/news-sentiment

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 新闻日度情绪聚合（全市场）。startDate/endDate 区间筛选。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|page|int32|false|第几页，从 1 起。默认 1。0 / 负数会被当成 1。|-|
|size|int32|false|每页记录数。默认 50，硬上限 {@value #MAX_SIZE}。<br/><p>传入超过 {@value #MAX_SIZE} 时会被自动截断到 {@value #MAX_SIZE}（不报错）。</p>|-|
|tsCode|string|false|股票代码（带交易所后缀），如 {@code "600519.SH"}。<br/><p>cyq-perf / block-trade / auction-open / auction-close / ths-concept / moneyflow-dc 等"针对单只票"的端点使用。</p>|-|
|tradeDate|string|false|交易日期，格式 {@code YYYYMMDD}（如 {@code "20260430"}）。可空。<br/><p>hot-rank / limit-analysis / hsgt-top10 / kpl-list / mainboard / guba-rank 等"按日切片"端点使用。<br/>不传时取最新交易日。</p>|-|
|startDate|string|false|起始日期，格式 {@code YYYYMMDD}。<br/><p>block-trade / hsgt-moneyflow / moneyflow-dc 等"按时间序列"端点使用。</p>|-|
|endDate|string|false|结束日期，格式 {@code YYYYMMDD}。<br/><p>同 {@link #startDate}，配套使用。</p>|-|
|nameKeyword|string|false|名称模糊匹配关键字（中文）。<br/><p>hm-list（游资名录搜索，如 {@code "宁波派"} / {@code "赵老哥"}）/ kpl-list（按概念名搜）使用。</p>|-|
|dataType|string|false|子分类标识（含义因端点而异）：<br/><br/><ul><br/>  <li><b>hot-rank（dc_hot）</b>：{@code "1"} 股票热榜 / {@code "2"} 板块热榜</li><br/>  <li><b>hsgt-top10</b>：{@code "1"} 沪股通 / {@code "2"} 深股通 / {@code "3"} 港股通</li><br/>  <li><b>cyq-perf</b>：{@code "D"} 日 / {@code "W"} 周 / {@code "M"} 月</li><br/></ul>|-|
|limitStat|string|false|涨跌停状态过滤（仅 limit-analysis 端点用）。<br/><br/><ul><br/>  <li>{@code "U"} —— 涨停</li><br/>  <li>{@code "D"} —— 跌停</li><br/>  <li>空 —— 不过滤</li><br/></ul>|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/stock/market/news-sentiment?page=0&size=0&startDate=&tradeDate=&nameKeyword=&dataType=&limitStat=&endDate=&tsCode='
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─tradeDate|string|No comments found.|-|
|└─totalNewsCount|int32|当日新闻总数|-|
|└─positiveCount|int32|正面新闻数|-|
|└─negativeCount|int32|负面新闻数|-|
|└─avgSentimentScore|number|平均情绪分（-1 ~ 1）|-|
|└─newsVolumeMa5|number|5 日平均新闻量|-|
|└─newsSurgeRatio|number|新闻激增比（当日 / MA5）|-|
|└─srcDiversity|int32|来源多样性|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "tradeDate": "",
      "totalNewsCount": 0,
      "positiveCount": 0,
      "negativeCount": 0,
      "avgSentimentScore": 0,
      "newsVolumeMa5": 0,
      "newsSurgeRatio": 0,
      "srcDiversity": 0
    }
  ],
  "traceId": ""
}
```

### 龙虎榜机构席位明细（与 kpl/lhb 互补）。tsCode 或 tradeDate 至少一个。
**URL:** /openapi/v1/stock/market/institution-trading

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 龙虎榜机构席位明细（与 kpl/lhb 互补）。tsCode 或 tradeDate 至少一个。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|page|int32|false|第几页，从 1 起。默认 1。0 / 负数会被当成 1。|-|
|size|int32|false|每页记录数。默认 50，硬上限 {@value #MAX_SIZE}。<br/><p>传入超过 {@value #MAX_SIZE} 时会被自动截断到 {@value #MAX_SIZE}（不报错）。</p>|-|
|tsCode|string|false|股票代码（带交易所后缀），如 {@code "600519.SH"}。<br/><p>cyq-perf / block-trade / auction-open / auction-close / ths-concept / moneyflow-dc 等"针对单只票"的端点使用。</p>|-|
|tradeDate|string|false|交易日期，格式 {@code YYYYMMDD}（如 {@code "20260430"}）。可空。<br/><p>hot-rank / limit-analysis / hsgt-top10 / kpl-list / mainboard / guba-rank 等"按日切片"端点使用。<br/>不传时取最新交易日。</p>|-|
|startDate|string|false|起始日期，格式 {@code YYYYMMDD}。<br/><p>block-trade / hsgt-moneyflow / moneyflow-dc 等"按时间序列"端点使用。</p>|-|
|endDate|string|false|结束日期，格式 {@code YYYYMMDD}。<br/><p>同 {@link #startDate}，配套使用。</p>|-|
|nameKeyword|string|false|名称模糊匹配关键字（中文）。<br/><p>hm-list（游资名录搜索，如 {@code "宁波派"} / {@code "赵老哥"}）/ kpl-list（按概念名搜）使用。</p>|-|
|dataType|string|false|子分类标识（含义因端点而异）：<br/><br/><ul><br/>  <li><b>hot-rank（dc_hot）</b>：{@code "1"} 股票热榜 / {@code "2"} 板块热榜</li><br/>  <li><b>hsgt-top10</b>：{@code "1"} 沪股通 / {@code "2"} 深股通 / {@code "3"} 港股通</li><br/>  <li><b>cyq-perf</b>：{@code "D"} 日 / {@code "W"} 周 / {@code "M"} 月</li><br/></ul>|-|
|limitStat|string|false|涨跌停状态过滤（仅 limit-analysis 端点用）。<br/><br/><ul><br/>  <li>{@code "U"} —— 涨停</li><br/>  <li>{@code "D"} —— 跌停</li><br/>  <li>空 —— 不过滤</li><br/></ul>|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/stock/market/institution-trading?page=0&size=0&startDate=&dataType=&limitStat=&tradeDate=&tsCode=&nameKeyword=&endDate='
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─tradeDate|string|No comments found.|-|
|└─tsCode|string|No comments found.|-|
|└─buy|number|No comments found.|-|
|└─buyRate|number|买额占比（%）|-|
|└─sell|number|No comments found.|-|
|└─sellRate|number|No comments found.|-|
|└─netBuy|number|No comments found.|-|
|└─side|int32|1=买方机构 / 2=卖方机构|-|
|└─reason|string|上榜原因（如 "日涨幅偏离值达 7%"）|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "tradeDate": "",
      "tsCode": "",
      "buy": 0,
      "buyRate": 0,
      "sell": 0,
      "sellRate": 0,
      "netBuy": 0,
      "side": 0,
      "reason": ""
    }
  ],
  "traceId": ""
}
```

### 龙虎榜券商营业部明细。tsCode 或 tradeDate 至少一个；nameKeyword 用于按营业部模糊匹配。
**URL:** /openapi/v1/stock/market/broker-trade

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 龙虎榜券商营业部明细。tsCode 或 tradeDate 至少一个；nameKeyword 用于按营业部模糊匹配。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|page|int32|false|第几页，从 1 起。默认 1。0 / 负数会被当成 1。|-|
|size|int32|false|每页记录数。默认 50，硬上限 {@value #MAX_SIZE}。<br/><p>传入超过 {@value #MAX_SIZE} 时会被自动截断到 {@value #MAX_SIZE}（不报错）。</p>|-|
|tsCode|string|false|股票代码（带交易所后缀），如 {@code "600519.SH"}。<br/><p>cyq-perf / block-trade / auction-open / auction-close / ths-concept / moneyflow-dc 等"针对单只票"的端点使用。</p>|-|
|tradeDate|string|false|交易日期，格式 {@code YYYYMMDD}（如 {@code "20260430"}）。可空。<br/><p>hot-rank / limit-analysis / hsgt-top10 / kpl-list / mainboard / guba-rank 等"按日切片"端点使用。<br/>不传时取最新交易日。</p>|-|
|startDate|string|false|起始日期，格式 {@code YYYYMMDD}。<br/><p>block-trade / hsgt-moneyflow / moneyflow-dc 等"按时间序列"端点使用。</p>|-|
|endDate|string|false|结束日期，格式 {@code YYYYMMDD}。<br/><p>同 {@link #startDate}，配套使用。</p>|-|
|nameKeyword|string|false|名称模糊匹配关键字（中文）。<br/><p>hm-list（游资名录搜索，如 {@code "宁波派"} / {@code "赵老哥"}）/ kpl-list（按概念名搜）使用。</p>|-|
|dataType|string|false|子分类标识（含义因端点而异）：<br/><br/><ul><br/>  <li><b>hot-rank（dc_hot）</b>：{@code "1"} 股票热榜 / {@code "2"} 板块热榜</li><br/>  <li><b>hsgt-top10</b>：{@code "1"} 沪股通 / {@code "2"} 深股通 / {@code "3"} 港股通</li><br/>  <li><b>cyq-perf</b>：{@code "D"} 日 / {@code "W"} 周 / {@code "M"} 月</li><br/></ul>|-|
|limitStat|string|false|涨跌停状态过滤（仅 limit-analysis 端点用）。<br/><br/><ul><br/>  <li>{@code "U"} —— 涨停</li><br/>  <li>{@code "D"} —— 跌停</li><br/>  <li>空 —— 不过滤</li><br/></ul>|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/stock/market/broker-trade?page=0&size=0&dataType=&endDate=&tsCode=&nameKeyword=&tradeDate=&startDate=&limitStat='
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─tradeDate|string|No comments found.|-|
|└─tsCode|string|No comments found.|-|
|└─exalter|string|营业部名称|-|
|└─buy|number|No comments found.|-|
|└─buyRate|number|No comments found.|-|
|└─sell|number|No comments found.|-|
|└─sellRate|number|No comments found.|-|
|└─netBuy|number|No comments found.|-|
|└─side|int32|1=买方 / 2=卖方|-|
|└─reason|string|No comments found.|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "tradeDate": "",
      "tsCode": "",
      "exalter": "",
      "buy": 0,
      "buyRate": 0,
      "sell": 0,
      "sellRate": 0,
      "netBuy": 0,
      "side": 0,
      "reason": ""
    }
  ],
  "traceId": ""
}
```

### 板块列表（涨跌幅 / 资金净流入），从 site internal {@code /stock/api/dc/plate} 迁移。<br>不带筛选参数；返回当前活跃板块快照。
**URL:** /openapi/v1/stock/market/plate

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 板块列表（涨跌幅 / 资金净流入），从 site internal {@code /stock/api/dc/plate} 迁移。
不带筛选参数；返回当前活跃板块快照。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/stock/market/plate'
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─leadingName|string|领涨股票名称|-|
|└─leadingCode|string|领涨股票代码|-|
|└─leadingPct|number|领涨股涨跌幅|-|
|└─totalMv|number|板块总市值|-|
|└─turnoverRate|number|换手率|-|
|└─upNum|int32|上涨家数|-|
|└─downNum|int32|下跌家数|-|
|└─tradeDate|string|交易日期|-|
|└─contentType|string|内容类型|-|
|└─tsCode|string|股票代码|-|
|└─name|string|股票名称|-|
|└─pctChange|number|涨跌幅|-|
|└─close|number|收盘价|-|
|└─netAmount|number|净流入金额|-|
|└─netAmountRate|number|净流入比例|-|
|└─buyElgAmount|number|超大单买入金额|-|
|└─buyElgAmountRate|number|超大单买入比例|-|
|└─buyLgAmount|number|大单买入金额|-|
|└─buyLgAmountRate|number|大单买入比例|-|
|└─buyMdAmount|number|中单买入金额|-|
|└─buyMdAmountRate|number|中单买入比例|-|
|└─buySmAmount|number|小单买入金额|-|
|└─buySmAmountRate|number|小单买入比例|-|
|└─buySmAmountStock|string|小单买入股票|-|
|└─rankNum|int32|排名|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "leadingName": "",
      "leadingCode": "",
      "leadingPct": 0,
      "totalMv": 0,
      "turnoverRate": 0,
      "upNum": 0,
      "downNum": 0,
      "tradeDate": "yyyy-MM-dd HH:mm:ss",
      "contentType": "",
      "tsCode": "",
      "name": "",
      "pctChange": 0,
      "close": 0,
      "netAmount": 0,
      "netAmountRate": 0,
      "buyElgAmount": 0,
      "buyElgAmountRate": 0,
      "buyLgAmount": 0,
      "buyLgAmountRate": 0,
      "buyMdAmount": 0,
      "buyMdAmountRate": 0,
      "buySmAmount": 0,
      "buySmAmountRate": 0,
      "buySmAmountStock": "",
      "rankNum": 0
    }
  ],
  "traceId": ""
}
```

### 板块详情时间序列（按日期 + 类型）。site internal: {@code /stock/api/dc/plate/list}。
**URL:** /openapi/v1/stock/market/plate/list

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 板块详情时间序列（按日期 + 类型）。site internal: {@code /stock/api/dc/plate/list}。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|page|int32|false|第几页，从 1 起。默认 1。0 / 负数会被当成 1。|-|
|size|int32|false|每页记录数。默认 50，硬上限 {@value #MAX_SIZE}。<br/><p>传入超过 {@value #MAX_SIZE} 时会被自动截断到 {@value #MAX_SIZE}（不报错）。</p>|-|
|type|string|false|板块类型（东财分类）。<br/><br/><ul><br/>  <li>{@code "概念"} —— 概念板块（如新能源车 / AI）</li><br/>  <li>{@code "行业"} —— 行业板块（如半导体 / 银行）</li><br/>  <li>{@code "地域"} —— 地域板块（如广东 / 江苏）</li><br/></ul>|-|
|tradeDate|string|false|交易日期，格式 {@code YYYYMMDD}（如 {@code "20260430"}）。<br/><p>可空。不传时取最新交易日。</p>|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/stock/market/plate/list?page=0&size=0&tradeDate=&type='
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─totalMv|number|板块总市值（万元）。|-|
|└─turnoverRate|number|板块换手率（%）。|-|
|└─upNum|int32|板块成分股中当日上涨的家数。|-|
|└─downNum|int32|板块成分股中当日下跌的家数。|-|
|└─tradeDate|string|交易日期。|-|
|└─contentType|string|板块类型：{@code "概念"} / {@code "行业"} / {@code "地域"}。|-|
|└─tsCode|string|板块代码（东财口径），如 {@code "BK0475"}（半导体）。|-|
|└─name|string|板块中文名，如 {@code "半导体"} / {@code "新能源车"}。|-|
|└─pctChange|number|板块当日涨跌幅（%）。|-|
|└─close|number|板块当日收盘指数。|-|
|└─netAmount|number|板块当日资金净流入（万元）。{@code > 0} 净流入，{@code < 0} 净流出。<br/><p>口径 = 主力（大单 + 特大单）净流入。</p>|-|
|└─netAmountRate|number|板块净流入率（%）= netAmount / 板块总成交额 × 100。|-|
|└─rankNum|int32|当日板块排名（按 pctChange 降序，1 = 涨幅最大）。|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "totalMv": 0,
      "turnoverRate": 0,
      "upNum": 0,
      "downNum": 0,
      "tradeDate": "yyyy-MM-dd HH:mm:ss",
      "contentType": "",
      "tsCode": "",
      "name": "",
      "pctChange": 0,
      "close": 0,
      "netAmount": 0,
      "netAmountRate": 0,
      "rankNum": 0
    }
  ],
  "traceId": ""
}
```

### 板块成分股估值快照。site internal: {@code /stock/api/dc/stockIndicatorListLastByDcPlate}。
**URL:** /openapi/v1/stock/market/plate/stocks-indicator

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 板块成分股估值快照。site internal: {@code /stock/api/dc/stockIndicatorListLastByDcPlate}。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|code|string|false|板块代码（东财口径）。<br/><br/><p><b>示例</b>：</p><br/><ul><br/>  <li>{@code "BK0475"} —— 半导体板块</li><br/>  <li>{@code "BK0420"} —— 新能源车板块</li><br/></ul><br/><br/><p>由 {@code /openapi/v1/stock/market/plate/list} 返回的 {@code code} 字段提供。</p>|-|
|tradeDate|string|false|交易日期，格式 {@code YYYYMMDD}（如 {@code "20260430"}）。<br/><p>可空。不传时取最新交易日。</p>|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/stock/market/plate/stocks-indicator?code=&tradeDate='
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─tsCode|string|股票代码（带交易所后缀），如 {@code "600519.SH"}。|-|
|└─symbol|string|纯数字股票代码，如 {@code "600519"}。|-|
|└─name|string|股票中文简称，如 {@code "贵州茅台"}。|-|
|└─tradeDate|string|数据所属交易日。|-|
|└─close|number|当日收盘价（元）。|-|
|└─turnoverRate|number|换手率（%）= 当日成交量 / 流通股本 × 100。|-|
|└─turnoverRateF|number|自由流通换手率（%）= 当日成交量 / 自由流通股本 × 100。一般比 {@link #turnoverRate} 更高。|-|
|└─volumeRatio|number|量比 = 当日成交量 / 近 5 日平均成交量。{@code > 1} 表示放量，{@code > 2} 显著放量。|-|
|└─pe|number|静态市盈率：股价 / 上一年度 EPS。|-|
|└─peTtm|number|滚动市盈率：股价 / 最近 4 个季度 EPS（最常用）。|-|
|└─pb|number|市净率：股价 / 每股净资产。|-|
|└─ps|number|静态市销率：股价 / 上一年度 EPS_revenue。|-|
|└─psTtm|number|滚动市销率：股价 / 最近 4 个季度营收（更平滑）。|-|
|└─dvRatio|number|静态股息率（%）= 上一年度每股分红 / 股价 × 100。|-|
|└─dvTtm|number|滚动股息率（%）= 最近 4 个季度每股分红 / 股价 × 100。|-|
|└─totalShare|number|总股本（万股）。|-|
|└─floatShare|number|流通股本（万股）。|-|
|└─freeShare|number|自由流通股本（万股）。剔除限售 / 高管 / 国资等长期不流通部分。|-|
|└─totalMv|number|总市值（万元）= 总股本 × 当日收盘价。|-|
|└─circMv|number|流通市值（万元）= 流通股本 × 当日收盘价。|-|
|└─limitStatus|int8|涨跌停状态。<br/><ul><br/>  <li>{@code 0} —— 普通</li><br/>  <li>{@code 1} —— 涨停</li><br/>  <li>{@code 2} —— 跌停</li><br/>  <li>{@code 3} —— 一字涨停（开盘即涨停）</li><br/>  <li>{@code 4} —— 一字跌停</li><br/></ul><br/><p>具体编码以后端 {@code com.common.enums.LimitStatus} 为准。</p>|-|
|└─roe|number|净资产收益率（%，最近一期）。{@code > 15%} 普遍认为是优秀。|-|
|└─chg|number|涨跌额（元）= close - preClose。|-|
|└─pctChg|number|涨跌幅（%）。|-|
|└─roeDate|string|ROE 数据所属报告期日（季末日期，如 {@code 2026-03-31}）。|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{"code":0,"msg":"","data":[{"tsCode":"","symbol":"","name":"","tradeDate":"yyyy-MM-dd HH:mm:ss","close":0,"turnoverRate":0,"turnoverRateF":0,"volumeRatio":0,"pe":0,"peTtm":0,"pb":0,"ps":0,"psTtm":0,"dvRatio":0,"dvTtm":0,"totalShare":0,"floatShare":0,"freeShare":0,"totalMv":0,"circMv":0,"limitStatus":,"roe":0,"chg":0,"pctChg":0,"roeDate":"yyyy-MM-dd HH:mm:ss"}],"traceId":""}
```

### 个股所属板块反查（一只股票挂在哪些板块 / 概念下）。<br>site internal: {@code /stock/api/detail/platesByStock}。
**URL:** /openapi/v1/stock/market/plates-by-stock

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 个股所属板块反查（一只股票挂在哪些板块 / 概念下）。
site internal: {@code /stock/api/detail/platesByStock}。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|conCode|string|false|成分股代码（带交易所后缀），如 {@code "600519.SH"}。<b>必填</b>。<br/><br/><p>注意字段名是 {@code conCode}（constituent code，成分股代码）而不是 {@code tsCode}。</p>|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/stock/market/plates-by-stock?conCode='
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─plateCode|string|板块代码|-|
|└─plateName|string|板块名称|-|
|└─contentType|string|板块类型：行业/概念/地域|-|
|└─pctChange|number|板块涨跌幅(%)|-|
|└─close|number|板块收盘价|-|
|└─totalMv|number|板块总市值(万)|-|
|└─turnoverRate|number|板块换手率(%)|-|
|└─upNum|int32|板块上涨个股数|-|
|└─downNum|int32|板块下跌个股数|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "plateCode": "",
      "plateName": "",
      "contentType": "",
      "pctChange": 0,
      "close": 0,
      "totalMv": 0,
      "turnoverRate": 0,
      "upNum": 0,
      "downNum": 0
    }
  ],
  "traceId": ""
}
```

### 龙虎榜最新可用日期列表。site internal: {@code /stock/api/stock/dc/lhb/getLatestLhbDates}。
**URL:** /openapi/v1/stock/market/lhb/latest-dates

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 龙虎榜最新可用日期列表。site internal: {@code /stock/api/stock/dc/lhb/getLatestLhbDates}。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/stock/market/lhb/latest-dates'
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    "",
    ""
  ],
  "traceId": ""
}
```

### 按日期拉龙虎榜上榜股票清单。site internal: {@code /stock/api/stock/dc/lhb/getLhbStockListByDate}。
**URL:** /openapi/v1/stock/market/lhb/list

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 按日期拉龙虎榜上榜股票清单。site internal: {@code /stock/api/stock/dc/lhb/getLhbStockListByDate}。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|tradeDate|string|false|龙虎榜交易日，格式 {@code YYYYMMDD}（如 {@code "20260430"}）。<b>必填</b>。<br/><p>用 {@code /openapi/v1/stock/market/lhb/latest-dates} 获取近期 LHB 日期列表（不一定每天都有 LHB）。</p>|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/stock/market/lhb/list?tradeDate='
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─tsCode|string|股票代码|-|
|└─name|string|股票名称|-|
|└─pctChange|number|涨跌幅|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "tsCode": "",
      "name": "",
      "pctChange": 0
    }
  ],
  "traceId": ""
}
```

### 实时放量上涨突破信号（从 site internal {@code GET /stock/monitor/volume-breakout} 迁移）。<br>注意是 GET 端点（无 body）。
**URL:** /openapi/v1/stock/market/volume-breakout

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 实时放量上涨突破信号（从 site internal {@code GET /stock/monitor/volume-breakout} 迁移）。
注意是 GET 端点（无 body）。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/stock/market/volume-breakout'
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─tsCode|string|股票代码 (tsCode格式，如600000.SH)|-|
|└─name|string|股票名称|-|
|└─price|number|最新价|-|
|└─pctChange|number|涨跌幅(%)|-|
|└─deltaVol|number|本分钟增量成交量(股)|-|
|└─avgVol|double|历史同期平均成交量(股)|-|
|└─deltaAmount|number|本分钟增量成交额(元)|-|
|└─avgAmount|double|历史同期平均成交额(元)|-|
|└─volumeRatio|double|量比 (deltaVol / avgVol)|-|
|└─time|string|信号时间|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "tsCode": "",
      "name": "",
      "price": 0,
      "pctChange": 0,
      "deltaVol": 0,
      "avgVol": 0.0,
      "deltaAmount": 0,
      "avgAmount": 0.0,
      "volumeRatio": 0.0,
      "time": ""
    }
  ],
  "traceId": ""
}
```

### 个股资金流向（近 N 天，按金额分大单 / 中单 / 小单）。<br>对应 site internal: {@code /stock/api/detail/moneyFlow}。
**URL:** /openapi/v1/stock/market/moneyflow

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 个股资金流向（近 N 天，按金额分大单 / 中单 / 小单）。
对应 site internal: {@code /stock/api/detail/moneyFlow}。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|page|int32|false|第几页，从 1 起。默认 1。0 / 负数会被当成 1。|-|
|size|int32|false|每页记录数。默认 50，硬上限 {@value #MAX_SIZE}。<br/><p>传入超过 {@value #MAX_SIZE} 时会被自动截断到 {@value #MAX_SIZE}（不报错）。</p>|-|
|tsCode|string|false|股票代码（带交易所后缀），如 {@code "600519.SH"}。<b>必填</b>。|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/stock/market/moneyflow?page=0&size=0&tsCode='
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─tsCode|string|No comments found.|-|
|└─tradeDate|string|交易日期 yyyyMMdd|-|
|└─buySmAmount|number|小单买入金额(万)|-|
|└─sellSmAmount|number|小单卖出金额(万)|-|
|└─buyMdAmount|number|中单买入金额(万)|-|
|└─sellMdAmount|number|中单卖出金额(万)|-|
|└─buyLgAmount|number|大单买入金额(万)|-|
|└─sellLgAmount|number|大单卖出金额(万)|-|
|└─buyElgAmount|number|超大单买入金额(万)|-|
|└─sellElgAmount|number|超大单卖出金额(万)|-|
|└─netMfAmount|number|净流入金额(万)|-|
|└─tradeCount|int64|成交笔数|-|
|└─mainForceNetInflow|number|主力净流入(大单+超大单)(万)|-|
|└─retailNetInflow|number|散户净流入(小单+中单)(万)|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "tsCode": "",
      "tradeDate": "",
      "buySmAmount": 0,
      "sellSmAmount": 0,
      "buyMdAmount": 0,
      "sellMdAmount": 0,
      "buyLgAmount": 0,
      "sellLgAmount": 0,
      "buyElgAmount": 0,
      "sellElgAmount": 0,
      "netMfAmount": 0,
      "tradeCount": 0,
      "mainForceNetInflow": 0,
      "retailNetInflow": 0
    }
  ],
  "traceId": ""
}
```

### 板块资金流（按内容类型 + 排序）。<br>对应 site internal: {@code /stock/api/dc/stockDcPlateMarketCashFlowList}。
**URL:** /openapi/v1/stock/market/plate/cash-flow

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 板块资金流（按内容类型 + 排序）。
对应 site internal: {@code /stock/api/dc/stockDcPlateMarketCashFlowList}。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|page|int32|false|第几页，从 1 起。默认 1。0 / 负数会被当成 1。|-|
|size|int32|false|每页记录数。默认 50，硬上限 {@value #MAX_SIZE}。<br/><p>传入超过 {@value #MAX_SIZE} 时会被自动截断到 {@value #MAX_SIZE}（不报错）。</p>|-|
|tsCode|string|false|板块代码（可选）。传了就只返回这个板块当日资金流；不传则按 {@code contentType} 全榜。<br/><p><b>示例</b>：{@code "BK0475"}（半导体）。由 {@code /openapi/v1/stock/market/plate/list} 返回的 code 字段提供。</p>|-|
|tradeDate|string|false|交易日期，格式 {@code YYYYMMDD}（如 {@code "20260430"}）。可空，不传时取最新交易日。|-|
|contentType|string|false|内容类型：{@code "概念"} / {@code "行业"} / {@code "地域"}。<br/><p>不传时默认 {@code "概念"}。</p>|-|
|netInflowAndPctChangeGtZero|boolean|false|是否仅返回"净流入 且 涨跌幅 > 0"的板块（量价齐升的强势板块）。<br/><p>{@code true} = 过滤；{@code false} 或 null = 不过滤，返回全部。</p>|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/stock/market/plate/cash-flow?page=0&size=0&netInflowAndPctChangeGtZero=true&tsCode=&contentType=&tradeDate='
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─id|int64|内部主键，调用方一般忽略。|-|
|└─tradeDate|string|交易日期。|-|
|└─contentType|string|板块类型：{@code "概念"} / {@code "行业"} / {@code "地域"}。|-|
|└─tsCode|string|板块代码（东财口径），如 {@code "BK0475"}。|-|
|└─name|string|板块中文名，如 {@code "半导体"}。|-|
|└─pctChange|number|板块当日涨跌幅（%）。|-|
|└─close|number|板块当日收盘指数。|-|
|└─netAmount|number|净流入金额（万元）= 主力买入 − 主力卖出。|-|
|└─netAmountRate|number|净流入占比（%）= netAmount / 当日总成交额 × 100。|-|
|└─buyElgAmount|number|特大单买入额（万元）。订单金额 ≥ 100 万。|-|
|└─buyElgAmountRate|number|特大单买入占比（%）。|-|
|└─buyLgAmount|number|大单买入额（万元）。订单金额 20 万 ~ 100 万。|-|
|└─buyLgAmountRate|number|大单买入占比（%）。|-|
|└─buyMdAmount|number|中单买入额（万元）。订单金额 4 万 ~ 20 万。|-|
|└─buyMdAmountRate|number|中单买入占比（%）。|-|
|└─buySmAmount|number|小单买入额（万元）。订单金额 < 4 万。|-|
|└─buySmAmountRate|number|小单买入占比（%）。|-|
|└─buySmAmountStock|string|板块龙头股代码（小单跟风最热的成分股，可能为 ts_code 或简称）。|-|
|└─rankNum|int32|当日板块排名（1 = 净流入最大）。|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "id": 0,
      "tradeDate": "yyyy-MM-dd HH:mm:ss",
      "contentType": "",
      "tsCode": "",
      "name": "",
      "pctChange": 0,
      "close": 0,
      "netAmount": 0,
      "netAmountRate": 0,
      "buyElgAmount": 0,
      "buyElgAmountRate": 0,
      "buyLgAmount": 0,
      "buyLgAmountRate": 0,
      "buyMdAmount": 0,
      "buyMdAmountRate": 0,
      "buySmAmount": 0,
      "buySmAmountRate": 0,
      "buySmAmountStock": "",
      "rankNum": 0
    }
  ],
  "traceId": ""
}
```

### 板块连续净流入榜（lastDate 持续天数 + 累计净流入 + 日均流入）。<br>对应 site internal: {@code /stock/api/dc/stockDcPlateContinueNetAmountList}。
**URL:** /openapi/v1/stock/market/plate/continue-net

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 板块连续净流入榜（lastDate 持续天数 + 累计净流入 + 日均流入）。
对应 site internal: {@code /stock/api/dc/stockDcPlateContinueNetAmountList}。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|continueNum|int32|false|连续天数。例如 {@code 5} = 找近 5 个交易日**每日都净流入**的板块。<br/><p>常用 {@code 3} / {@code 5} / {@code 10}。</p>|-|
|type|string|false|板块类型：{@code "概念"} / {@code "行业"} / {@code "地域"}。|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/stock/market/plate/continue-net?continueNum=0&type='
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─tsCode|string|板块代码（东财口径），如 {@code "BK0475"}。|-|
|└─name|string|板块中文名，如 {@code "半导体"} / {@code "新能源车"}。|-|
|└─lastDate|string|最新一个净流入日（连续段的右端点）。|-|
|└─amount|number|连续 N 日累计净流入总额（万元）。|-|
|└─avgAmount|number|连续 N 日的日均净流入额（万元）= amount / N。|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "tsCode": "",
      "name": "",
      "lastDate": "yyyy-MM-dd HH:mm:ss",
      "amount": 0,
      "avgAmount": 0
    }
  ],
  "traceId": ""
}
```

### 龙虎榜单股详情（按日期 + 股票代码）。<br>对应 site internal: {@code /stock/api/stock/dc/lhb/getLhbDetailsByDateAndCode}。
**URL:** /openapi/v1/stock/market/lhb/details

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 龙虎榜单股详情（按日期 + 股票代码）。
对应 site internal: {@code /stock/api/stock/dc/lhb/getLhbDetailsByDateAndCode}。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|tradeDate|string|false|龙虎榜交易日，格式 {@code YYYYMMDD}（如 {@code "20260430"}）。<b>必填</b>。<br/><p>用 {@code /openapi/v1/stock/market/lhb/latest-dates} 获取近期 LHB 日期列表。</p>|-|
|tsCode|string|false|股票代码（带交易所后缀），如 {@code "600519.SH"}。<b>必填</b>。|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/stock/market/lhb/details?tradeDate=&tsCode='
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─id|int64|内部主键，调用方一般忽略。|-|
|└─tradeDate|string|龙虎榜交易日期。|-|
|└─tsCode|string|股票代码（带交易所后缀），如 {@code "600519.SH"}。|-|
|└─exalter|string|席位名称。<br/><br/><p><b>常见类型</b>：</p><br/><ul><br/>  <li>机构：{@code "机构专用"}</li><br/>  <li>游资营业部：{@code "中信证券股份有限公司北京呼家楼营业部"}（赵老哥常用）/ {@code "国泰君安证券股份有限公司上海江苏路营业部"}（章建平常用）</li><br/>  <li>沪深港通：{@code "深股通专用"} / {@code "沪股通专用"}</li><br/></ul><br/><br/><p>可与 {@code /openapi/v1/stock/market/hm-list} 的游资名录交叉匹配识别游资身份。</p>|-|
|└─buy|number|买入金额（元）。|-|
|└─buyRate|number|买入金额占当日成交额比例（%）。|-|
|└─sell|number|卖出金额（元）。|-|
|└─sellRate|number|卖出金额占当日成交额比例（%）。|-|
|└─netBuy|number|净买入额（元）= buy − sell。<br/><p>{@code > 0} 净买入，{@code < 0} 净卖出。绝对值越大主力意图越明确。</p>|-|
|└─side|string|买卖方向：{@code "B"}（买方）/ {@code "S"}（卖方）。<br/><p>表示该席位主要在买还是在卖（虽然 buy/sell 都可能 > 0）。</p>|-|
|└─reason|string|上榜原因（中文，由交易所披露）。<br/><br/><p><b>常见原因</b>：</p><br/><ul><br/>  <li>{@code "日涨幅偏离值达7%的证券"} —— 涨幅触发</li><br/>  <li>{@code "日跌幅偏离值达-7%的证券"} —— 跌幅触发</li><br/>  <li>{@code "日换手率达20%的证券"} —— 换手率触发</li><br/>  <li>{@code "连续三个交易日内，涨幅偏离值累计达20%的证券"} —— 连板触发</li><br/></ul>|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "id": 0,
      "tradeDate": "yyyy-MM-dd HH:mm:ss",
      "tsCode": "",
      "exalter": "",
      "buy": 0,
      "buyRate": 0,
      "sell": 0,
      "sellRate": 0,
      "netBuy": 0,
      "side": "",
      "reason": ""
    }
  ],
  "traceId": ""
}
```

### 同花顺行业 / 概念板块列表（{@code stock_ths_index}）。无 trade_date 字段，可按 type / nameKeyword 过滤。<br>类型枚举：N=概念 / I=行业 / R=地域 / S=同花顺特色 / ST=风格 / TH=主题 / BB=宽基。
**URL:** /openapi/v1/stock/market/ths-index

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 同花顺行业 / 概念板块列表（{@code stock_ths_index}）。无 trade_date 字段，可按 type / nameKeyword 过滤。
类型枚举：N=概念 / I=行业 / R=地域 / S=同花顺特色 / ST=风格 / TH=主题 / BB=宽基。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|page|int32|false|第几页，从 1 起。默认 1。0 / 负数会被当成 1。|-|
|size|int32|false|每页记录数。默认 50，硬上限 {@value #MAX_SIZE}。<br/><p>传入超过 {@value #MAX_SIZE} 时会被自动截断到 {@value #MAX_SIZE}（不报错）。</p>|-|
|tsCode|string|false|股票 / 板块 / 概念代码，如 {@code "600519.SH"} / {@code "885589.TI"}。可空。|-|
|tradeDate|string|false|单日交易日，{@code YYYYMMDD}。可空（与 startDate/endDate 互斥优先）。|-|
|startDate|string|false|起始交易日，{@code YYYYMMDD}。可空。|-|
|endDate|string|false|结束交易日，{@code YYYYMMDD}。可空。|-|
|dataType|string|false|数据类型 / 板块类型（如 ths-hot 的 data_type、tdx-index 的 idx_type、st-daily 的 type、bak-basic 的 industry）。可空。|-|
|nameKeyword|string|false|名称模糊关键字（如 hm-name 游资名、ths-index/tdx-index name 模糊匹配、ci 一级行业名 l1Name 等）。可空。|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/stock/market/ths-index?page=0&size=0&startDate=&nameKeyword=&endDate=&dataType=&tradeDate=&tsCode='
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─tsCode|string|板块代码（如 885589.TI）|-|
|└─name|string|板块名称|-|
|└─count|int32|成分股数量|-|
|└─exchange|string|交易所（A=A股 / HK=港股 / US=美股）|-|
|└─listDate|string|上市日期|-|
|└─type|string|类型（N=概念 / I=行业 / R=地域 / S=同花顺特色 / ST=风格 / TH=主题 / BB=宽基）|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "tsCode": "",
      "name": "",
      "count": 0,
      "exchange": "",
      "listDate": "yyyy-MM-dd HH:mm:ss",
      "type": ""
    }
  ],
  "traceId": ""
}
```

### 同花顺板块日行情（{@code stock_ths_daily}）。可按 tsCode（板块代码）+ 日期范围过滤。
**URL:** /openapi/v1/stock/market/ths-daily

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 同花顺板块日行情（{@code stock_ths_daily}）。可按 tsCode（板块代码）+ 日期范围过滤。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|page|int32|false|第几页，从 1 起。默认 1。0 / 负数会被当成 1。|-|
|size|int32|false|每页记录数。默认 50，硬上限 {@value #MAX_SIZE}。<br/><p>传入超过 {@value #MAX_SIZE} 时会被自动截断到 {@value #MAX_SIZE}（不报错）。</p>|-|
|tsCode|string|false|股票 / 板块 / 概念代码，如 {@code "600519.SH"} / {@code "885589.TI"}。可空。|-|
|tradeDate|string|false|单日交易日，{@code YYYYMMDD}。可空（与 startDate/endDate 互斥优先）。|-|
|startDate|string|false|起始交易日，{@code YYYYMMDD}。可空。|-|
|endDate|string|false|结束交易日，{@code YYYYMMDD}。可空。|-|
|dataType|string|false|数据类型 / 板块类型（如 ths-hot 的 data_type、tdx-index 的 idx_type、st-daily 的 type、bak-basic 的 industry）。可空。|-|
|nameKeyword|string|false|名称模糊关键字（如 hm-name 游资名、ths-index/tdx-index name 模糊匹配、ci 一级行业名 l1Name 等）。可空。|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/stock/market/ths-daily?page=0&size=0&tsCode=&tradeDate=&startDate=&dataType=&endDate=&nameKeyword='
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─tradeDate|string|交易日|-|
|└─tsCode|string|板块代码|-|
|└─open|number|开盘价|-|
|└─high|number|最高价|-|
|└─low|number|最低价|-|
|└─close|number|收盘价|-|
|└─preClose|number|昨收价|-|
|└─avgPrice|number|平均价|-|
|└─change|number|涨跌额|-|
|└─pctChange|number|涨跌幅(%)|-|
|└─vol|number|成交量|-|
|└─turnoverRate|number|换手率(%)|-|
|└─totalMv|number|总市值（万元）|-|
|└─floatMv|number|流通市值（万元）|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "tradeDate": "yyyy-MM-dd HH:mm:ss",
      "tsCode": "",
      "open": 0,
      "high": 0,
      "low": 0,
      "close": 0,
      "preClose": 0,
      "avgPrice": 0,
      "change": 0,
      "pctChange": 0,
      "vol": 0,
      "turnoverRate": 0,
      "totalMv": 0,
      "floatMv": 0
    }
  ],
  "traceId": ""
}
```

### 同花顺 App 热榜（{@code stock_ths_hot}）。dataType 区分热股 / 概念 / 热基。
**URL:** /openapi/v1/stock/market/ths-hot

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 同花顺 App 热榜（{@code stock_ths_hot}）。dataType 区分热股 / 概念 / 热基。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|page|int32|false|第几页，从 1 起。默认 1。0 / 负数会被当成 1。|-|
|size|int32|false|每页记录数。默认 50，硬上限 {@value #MAX_SIZE}。<br/><p>传入超过 {@value #MAX_SIZE} 时会被自动截断到 {@value #MAX_SIZE}（不报错）。</p>|-|
|tsCode|string|false|股票 / 板块 / 概念代码，如 {@code "600519.SH"} / {@code "885589.TI"}。可空。|-|
|tradeDate|string|false|单日交易日，{@code YYYYMMDD}。可空（与 startDate/endDate 互斥优先）。|-|
|startDate|string|false|起始交易日，{@code YYYYMMDD}。可空。|-|
|endDate|string|false|结束交易日，{@code YYYYMMDD}。可空。|-|
|dataType|string|false|数据类型 / 板块类型（如 ths-hot 的 data_type、tdx-index 的 idx_type、st-daily 的 type、bak-basic 的 industry）。可空。|-|
|nameKeyword|string|false|名称模糊关键字（如 hm-name 游资名、ths-index/tdx-index name 模糊匹配、ci 一级行业名 l1Name 等）。可空。|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/stock/market/ths-hot?page=0&size=0&tsCode=&startDate=&tradeDate=&dataType=&endDate=&nameKeyword='
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─tradeDate|string|交易日|-|
|└─dataType|string|数据类型（热股 / 概念 / 热基 ...）|-|
|└─tsCode|string|股票 / 概念代码|-|
|└─tsName|string|股票 / 概念名称|-|
|└─rank|int32|排名|-|
|└─pctChange|number|涨跌幅(%)|-|
|└─currentPrice|number|最新价格|-|
|└─concept|string|关联概念|-|
|└─rankReason|string|上榜解读|-|
|└─hot|number|热度值|-|
|└─rankTime|string|排行榜时间|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "tradeDate": "yyyy-MM-dd HH:mm:ss",
      "dataType": "",
      "tsCode": "",
      "tsName": "",
      "rank": 0,
      "pctChange": 0,
      "currentPrice": 0,
      "concept": "",
      "rankReason": "",
      "hot": 0,
      "rankTime": ""
    }
  ],
  "traceId": ""
}
```

### 通达信板块基础信息（{@code stock_tdx_index}）。dataType 承载 idx_type 板块类型。
**URL:** /openapi/v1/stock/market/tdx-index

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 通达信板块基础信息（{@code stock_tdx_index}）。dataType 承载 idx_type 板块类型。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|page|int32|false|第几页，从 1 起。默认 1。0 / 负数会被当成 1。|-|
|size|int32|false|每页记录数。默认 50，硬上限 {@value #MAX_SIZE}。<br/><p>传入超过 {@value #MAX_SIZE} 时会被自动截断到 {@value #MAX_SIZE}（不报错）。</p>|-|
|tsCode|string|false|股票 / 板块 / 概念代码，如 {@code "600519.SH"} / {@code "885589.TI"}。可空。|-|
|tradeDate|string|false|单日交易日，{@code YYYYMMDD}。可空（与 startDate/endDate 互斥优先）。|-|
|startDate|string|false|起始交易日，{@code YYYYMMDD}。可空。|-|
|endDate|string|false|结束交易日，{@code YYYYMMDD}。可空。|-|
|dataType|string|false|数据类型 / 板块类型（如 ths-hot 的 data_type、tdx-index 的 idx_type、st-daily 的 type、bak-basic 的 industry）。可空。|-|
|nameKeyword|string|false|名称模糊关键字（如 hm-name 游资名、ths-index/tdx-index name 模糊匹配、ci 一级行业名 l1Name 等）。可空。|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/stock/market/tdx-index?page=0&size=0&dataType=&nameKeyword=&startDate=&tsCode=&tradeDate=&endDate='
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─tradeDate|string|交易日|-|
|└─tsCode|string|板块代码|-|
|└─name|string|板块名称|-|
|└─idxType|string|板块类型|-|
|└─idxCount|int32|成分股数量|-|
|└─totalShare|number|总股本|-|
|└─floatShare|number|流通股本|-|
|└─totalMv|number|总市值|-|
|└─floatMv|number|流通市值|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "tradeDate": "yyyy-MM-dd HH:mm:ss",
      "tsCode": "",
      "name": "",
      "idxType": "",
      "idxCount": 0,
      "totalShare": 0,
      "floatShare": 0,
      "totalMv": 0,
      "floatMv": 0
    }
  ],
  "traceId": ""
}
```

### 通达信板块日行情（{@code stock_tdx_daily}）。约 36 列宽表，含价量 / 涨跌停 / 区间动量 / 北向资金。
**URL:** /openapi/v1/stock/market/tdx-daily

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 通达信板块日行情（{@code stock_tdx_daily}）。约 36 列宽表，含价量 / 涨跌停 / 区间动量 / 北向资金。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|page|int32|false|第几页，从 1 起。默认 1。0 / 负数会被当成 1。|-|
|size|int32|false|每页记录数。默认 50，硬上限 {@value #MAX_SIZE}。<br/><p>传入超过 {@value #MAX_SIZE} 时会被自动截断到 {@value #MAX_SIZE}（不报错）。</p>|-|
|tsCode|string|false|股票 / 板块 / 概念代码，如 {@code "600519.SH"} / {@code "885589.TI"}。可空。|-|
|tradeDate|string|false|单日交易日，{@code YYYYMMDD}。可空（与 startDate/endDate 互斥优先）。|-|
|startDate|string|false|起始交易日，{@code YYYYMMDD}。可空。|-|
|endDate|string|false|结束交易日，{@code YYYYMMDD}。可空。|-|
|dataType|string|false|数据类型 / 板块类型（如 ths-hot 的 data_type、tdx-index 的 idx_type、st-daily 的 type、bak-basic 的 industry）。可空。|-|
|nameKeyword|string|false|名称模糊关键字（如 hm-name 游资名、ths-index/tdx-index name 模糊匹配、ci 一级行业名 l1Name 等）。可空。|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/stock/market/tdx-daily?page=0&size=0&tradeDate=&nameKeyword=&endDate=&tsCode=&dataType=&startDate='
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─tradeDate|string|交易日|-|
|└─tsCode|string|板块代码|-|
|└─close|number|收盘价|-|
|└─open|number|开盘价|-|
|└─high|number|最高价|-|
|└─low|number|最低价|-|
|└─preClose|number|昨收价|-|
|└─change|number|涨跌额|-|
|└─pctChange|number|涨跌幅(%)|-|
|└─vol|number|成交量|-|
|└─amount|number|成交额|-|
|└─volRatio|number|量比|-|
|└─turnoverRate|number|换手率(%)|-|
|└─swing|number|振幅(%)|-|
|└─upNum|int32|上涨家数|-|
|└─downNum|int32|下跌家数|-|
|└─limitUpNum|int32|涨停家数|-|
|└─limitDownNum|int32|跌停家数|-|
|└─luDays|int32|连板天数|-|
|└─return3Day|number|3 日涨幅(%)|-|
|└─return5Day|number|5 日涨幅(%)|-|
|└─return10Day|number|10 日涨幅(%)|-|
|└─return20Day|number|20 日涨幅(%)|-|
|└─return60Day|number|60 日涨幅(%)|-|
|└─mtd|number|月初至今涨幅(%)|-|
|└─ytd|number|年初至今涨幅(%)|-|
|└─return1Year|number|一年涨幅(%)|-|
|└─floatMv|number|流通市值|-|
|└─abTotalMv|number|AB 股总市值|-|
|└─floatShare|number|流通股本|-|
|└─totalShare|number|总股本|-|
|└─bmBuyNet|number|北向资金净买入额|-|
|└─bmBuyRatio|number|北向资金买入占比(%)|-|
|└─bmNet|number|北向资金净流入|-|
|└─bmRatio|number|北向资金流入占比(%)|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "tradeDate": "yyyy-MM-dd HH:mm:ss",
      "tsCode": "",
      "close": 0,
      "open": 0,
      "high": 0,
      "low": 0,
      "preClose": 0,
      "change": 0,
      "pctChange": 0,
      "vol": 0,
      "amount": 0,
      "volRatio": 0,
      "turnoverRate": 0,
      "swing": 0,
      "upNum": 0,
      "downNum": 0,
      "limitUpNum": 0,
      "limitDownNum": 0,
      "luDays": 0,
      "return3Day": 0,
      "return5Day": 0,
      "return10Day": 0,
      "return20Day": 0,
      "return60Day": 0,
      "mtd": 0,
      "ytd": 0,
      "return1Year": 0,
      "floatMv": 0,
      "abTotalMv": 0,
      "floatShare": 0,
      "totalShare": 0,
      "bmBuyNet": 0,
      "bmBuyRatio": 0,
      "bmNet": 0,
      "bmRatio": 0
    }
  ],
  "traceId": ""
}
```

### 通达信板块成分股（{@code stock_tdx_member}）。tsCode 是板块代码。
**URL:** /openapi/v1/stock/market/tdx-member

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 通达信板块成分股（{@code stock_tdx_member}）。tsCode 是板块代码。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|page|int32|false|第几页，从 1 起。默认 1。0 / 负数会被当成 1。|-|
|size|int32|false|每页记录数。默认 50，硬上限 {@value #MAX_SIZE}。<br/><p>传入超过 {@value #MAX_SIZE} 时会被自动截断到 {@value #MAX_SIZE}（不报错）。</p>|-|
|tsCode|string|false|股票 / 板块 / 概念代码，如 {@code "600519.SH"} / {@code "885589.TI"}。可空。|-|
|tradeDate|string|false|单日交易日，{@code YYYYMMDD}。可空（与 startDate/endDate 互斥优先）。|-|
|startDate|string|false|起始交易日，{@code YYYYMMDD}。可空。|-|
|endDate|string|false|结束交易日，{@code YYYYMMDD}。可空。|-|
|dataType|string|false|数据类型 / 板块类型（如 ths-hot 的 data_type、tdx-index 的 idx_type、st-daily 的 type、bak-basic 的 industry）。可空。|-|
|nameKeyword|string|false|名称模糊关键字（如 hm-name 游资名、ths-index/tdx-index name 模糊匹配、ci 一级行业名 l1Name 等）。可空。|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/stock/market/tdx-member?page=0&size=0&tsCode=&dataType=&nameKeyword=&endDate=&startDate=&tradeDate='
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─tradeDate|string|交易日|-|
|└─tsCode|string|板块代码|-|
|└─conCode|string|成分股代码|-|
|└─conName|string|成分股名称|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "tradeDate": "yyyy-MM-dd HH:mm:ss",
      "tsCode": "",
      "conCode": "",
      "conName": ""
    }
  ],
  "traceId": ""
}
```

### 中信行业指数日行情（{@code stock_ci_daily}）。中信一级 / 二级 / 三级行业指数共用此表。
**URL:** /openapi/v1/stock/market/ci-daily

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 中信行业指数日行情（{@code stock_ci_daily}）。中信一级 / 二级 / 三级行业指数共用此表。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|page|int32|false|第几页，从 1 起。默认 1。0 / 负数会被当成 1。|-|
|size|int32|false|每页记录数。默认 50，硬上限 {@value #MAX_SIZE}。<br/><p>传入超过 {@value #MAX_SIZE} 时会被自动截断到 {@value #MAX_SIZE}（不报错）。</p>|-|
|tsCode|string|false|股票 / 板块 / 概念代码，如 {@code "600519.SH"} / {@code "885589.TI"}。可空。|-|
|tradeDate|string|false|单日交易日，{@code YYYYMMDD}。可空（与 startDate/endDate 互斥优先）。|-|
|startDate|string|false|起始交易日，{@code YYYYMMDD}。可空。|-|
|endDate|string|false|结束交易日，{@code YYYYMMDD}。可空。|-|
|dataType|string|false|数据类型 / 板块类型（如 ths-hot 的 data_type、tdx-index 的 idx_type、st-daily 的 type、bak-basic 的 industry）。可空。|-|
|nameKeyword|string|false|名称模糊关键字（如 hm-name 游资名、ths-index/tdx-index name 模糊匹配、ci 一级行业名 l1Name 等）。可空。|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/stock/market/ci-daily?page=0&size=0&startDate=&nameKeyword=&tradeDate=&tsCode=&dataType=&endDate='
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─tradeDate|string|交易日|-|
|└─tsCode|string|中信行业指数代码|-|
|└─open|number|开盘价|-|
|└─high|number|最高价|-|
|└─low|number|最低价|-|
|└─close|number|收盘价|-|
|└─preClose|number|昨收价|-|
|└─change|number|涨跌额|-|
|└─pctChange|number|涨跌幅(%)|-|
|└─vol|number|成交量|-|
|└─amount|number|成交额|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "tradeDate": "yyyy-MM-dd HH:mm:ss",
      "tsCode": "",
      "open": 0,
      "high": 0,
      "low": 0,
      "close": 0,
      "preClose": 0,
      "change": 0,
      "pctChange": 0,
      "vol": 0,
      "amount": 0
    }
  ],
  "traceId": ""
}
```

### 中信行业成分（{@code stock_ci_index_member}）。tsCode 个股代码反查三级行业归属；dataType 承载 isNew 过滤。
**URL:** /openapi/v1/stock/market/ci-index-member

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 中信行业成分（{@code stock_ci_index_member}）。tsCode 个股代码反查三级行业归属；dataType 承载 isNew 过滤。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|page|int32|false|第几页，从 1 起。默认 1。0 / 负数会被当成 1。|-|
|size|int32|false|每页记录数。默认 50，硬上限 {@value #MAX_SIZE}。<br/><p>传入超过 {@value #MAX_SIZE} 时会被自动截断到 {@value #MAX_SIZE}（不报错）。</p>|-|
|tsCode|string|false|股票 / 板块 / 概念代码，如 {@code "600519.SH"} / {@code "885589.TI"}。可空。|-|
|tradeDate|string|false|单日交易日，{@code YYYYMMDD}。可空（与 startDate/endDate 互斥优先）。|-|
|startDate|string|false|起始交易日，{@code YYYYMMDD}。可空。|-|
|endDate|string|false|结束交易日，{@code YYYYMMDD}。可空。|-|
|dataType|string|false|数据类型 / 板块类型（如 ths-hot 的 data_type、tdx-index 的 idx_type、st-daily 的 type、bak-basic 的 industry）。可空。|-|
|nameKeyword|string|false|名称模糊关键字（如 hm-name 游资名、ths-index/tdx-index name 模糊匹配、ci 一级行业名 l1Name 等）。可空。|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/stock/market/ci-index-member?page=0&size=0&tsCode=&tradeDate=&dataType=&endDate=&nameKeyword=&startDate='
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─l1Code|string|一级行业代码|-|
|└─l1Name|string|一级行业名称|-|
|└─l2Code|string|二级行业代码|-|
|└─l2Name|string|二级行业名称|-|
|└─l3Code|string|三级行业代码|-|
|└─l3Name|string|三级行业名称|-|
|└─tsCode|string|股票代码|-|
|└─name|string|股票名称|-|
|└─inDate|string|纳入日期|-|
|└─outDate|string|剔除日期（可空）|-|
|└─isNew|string|是否最新成份（Y/N）|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "l1Code": "",
      "l1Name": "",
      "l2Code": "",
      "l2Name": "",
      "l3Code": "",
      "l3Name": "",
      "tsCode": "",
      "name": "",
      "inDate": "yyyy-MM-dd HH:mm:ss",
      "outDate": "yyyy-MM-dd HH:mm:ss",
      "isNew": ""
    }
  ],
  "traceId": ""
}
```

### 开盘啦题材成分（{@code stock_kpl_concept_cons}）。tsCode 题材代码，nameKeyword 承载个股代码反查。
**URL:** /openapi/v1/stock/market/kpl-concept-cons

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 开盘啦题材成分（{@code stock_kpl_concept_cons}）。tsCode 题材代码，nameKeyword 承载个股代码反查。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|page|int32|false|第几页，从 1 起。默认 1。0 / 负数会被当成 1。|-|
|size|int32|false|每页记录数。默认 50，硬上限 {@value #MAX_SIZE}。<br/><p>传入超过 {@value #MAX_SIZE} 时会被自动截断到 {@value #MAX_SIZE}（不报错）。</p>|-|
|tsCode|string|false|股票 / 板块 / 概念代码，如 {@code "600519.SH"} / {@code "885589.TI"}。可空。|-|
|tradeDate|string|false|单日交易日，{@code YYYYMMDD}。可空（与 startDate/endDate 互斥优先）。|-|
|startDate|string|false|起始交易日，{@code YYYYMMDD}。可空。|-|
|endDate|string|false|结束交易日，{@code YYYYMMDD}。可空。|-|
|dataType|string|false|数据类型 / 板块类型（如 ths-hot 的 data_type、tdx-index 的 idx_type、st-daily 的 type、bak-basic 的 industry）。可空。|-|
|nameKeyword|string|false|名称模糊关键字（如 hm-name 游资名、ths-index/tdx-index name 模糊匹配、ci 一级行业名 l1Name 等）。可空。|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/stock/market/kpl-concept-cons?page=0&size=0&endDate=&tradeDate=&startDate=&tsCode=&nameKeyword=&dataType='
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─tradeDate|string|交易日|-|
|└─tsCode|string|题材代码|-|
|└─name|string|题材名称|-|
|└─conCode|string|个股代码|-|
|└─conName|string|个股名称|-|
|└─description|string|题材描述|-|
|└─hotNum|int32|人气值|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "tradeDate": "yyyy-MM-dd HH:mm:ss",
      "tsCode": "",
      "name": "",
      "conCode": "",
      "conName": "",
      "description": "",
      "hotNum": 0
    }
  ],
  "traceId": ""
}
```

### 涨停股票连板天梯（{@code stock_limit_step}）。nums 为连扳数（字符串 &amp;quot;2&amp;quot;/&amp;quot;3&amp;quot;/...）。
**URL:** /openapi/v1/stock/market/limit-step

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 涨停股票连板天梯（{@code stock_limit_step}）。nums 为连扳数（字符串 "2"/"3"/...）。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|page|int32|false|第几页，从 1 起。默认 1。0 / 负数会被当成 1。|-|
|size|int32|false|每页记录数。默认 50，硬上限 {@value #MAX_SIZE}。<br/><p>传入超过 {@value #MAX_SIZE} 时会被自动截断到 {@value #MAX_SIZE}（不报错）。</p>|-|
|tsCode|string|false|股票 / 板块 / 概念代码，如 {@code "600519.SH"} / {@code "885589.TI"}。可空。|-|
|tradeDate|string|false|单日交易日，{@code YYYYMMDD}。可空（与 startDate/endDate 互斥优先）。|-|
|startDate|string|false|起始交易日，{@code YYYYMMDD}。可空。|-|
|endDate|string|false|结束交易日，{@code YYYYMMDD}。可空。|-|
|dataType|string|false|数据类型 / 板块类型（如 ths-hot 的 data_type、tdx-index 的 idx_type、st-daily 的 type、bak-basic 的 industry）。可空。|-|
|nameKeyword|string|false|名称模糊关键字（如 hm-name 游资名、ths-index/tdx-index name 模糊匹配、ci 一级行业名 l1Name 等）。可空。|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/stock/market/limit-step?page=0&size=0&tsCode=&nameKeyword=&dataType=&endDate=&tradeDate=&startDate='
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─tradeDate|string|交易日|-|
|└─tsCode|string|TS 代码|-|
|└─name|string|股票名称|-|
|└─nums|string|连扳数|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "tradeDate": "yyyy-MM-dd HH:mm:ss",
      "tsCode": "",
      "name": "",
      "nums": ""
    }
  ],
  "traceId": ""
}
```

### 涨停最强板块统计（{@code stock_limit_cpt_list}）。upStat 是连涨梯队（如 &amp;quot;5/3/2&amp;quot;）。
**URL:** /openapi/v1/stock/market/limit-cpt-list

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 涨停最强板块统计（{@code stock_limit_cpt_list}）。upStat 是连涨梯队（如 "5/3/2"）。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|page|int32|false|第几页，从 1 起。默认 1。0 / 负数会被当成 1。|-|
|size|int32|false|每页记录数。默认 50，硬上限 {@value #MAX_SIZE}。<br/><p>传入超过 {@value #MAX_SIZE} 时会被自动截断到 {@value #MAX_SIZE}（不报错）。</p>|-|
|tsCode|string|false|股票 / 板块 / 概念代码，如 {@code "600519.SH"} / {@code "885589.TI"}。可空。|-|
|tradeDate|string|false|单日交易日，{@code YYYYMMDD}。可空（与 startDate/endDate 互斥优先）。|-|
|startDate|string|false|起始交易日，{@code YYYYMMDD}。可空。|-|
|endDate|string|false|结束交易日，{@code YYYYMMDD}。可空。|-|
|dataType|string|false|数据类型 / 板块类型（如 ths-hot 的 data_type、tdx-index 的 idx_type、st-daily 的 type、bak-basic 的 industry）。可空。|-|
|nameKeyword|string|false|名称模糊关键字（如 hm-name 游资名、ths-index/tdx-index name 模糊匹配、ci 一级行业名 l1Name 等）。可空。|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/stock/market/limit-cpt-list?page=0&size=0&startDate=&tsCode=&tradeDate=&nameKeyword=&endDate=&dataType='
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─tradeDate|string|交易日|-|
|└─tsCode|string|板块代码|-|
|└─name|string|板块名称|-|
|└─days|int32|上榜天数|-|
|└─upStat|string|连涨梯队（如 "5/3/2"）|-|
|└─consNums|int32|连扳数量|-|
|└─upNums|int32|涨停数量|-|
|└─pctChg|number|涨跌幅(%)|-|
|└─rank|string|板块热度排名|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "tradeDate": "yyyy-MM-dd HH:mm:ss",
      "tsCode": "",
      "name": "",
      "days": 0,
      "upStat": "",
      "consNums": 0,
      "upNums": 0,
      "pctChg": 0,
      "rank": ""
    }
  ],
  "traceId": ""
}
```

### 游资交易明细（{@code stock_hm_detail}）。nameKeyword 模糊匹配 hm_name（游资名）。<br>与 /hm-list（仅游资名册）互补。
**URL:** /openapi/v1/stock/market/hm-detail

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 游资交易明细（{@code stock_hm_detail}）。nameKeyword 模糊匹配 hm_name（游资名）。
与 /hm-list（仅游资名册）互补。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|page|int32|false|第几页，从 1 起。默认 1。0 / 负数会被当成 1。|-|
|size|int32|false|每页记录数。默认 50，硬上限 {@value #MAX_SIZE}。<br/><p>传入超过 {@value #MAX_SIZE} 时会被自动截断到 {@value #MAX_SIZE}（不报错）。</p>|-|
|tsCode|string|false|股票 / 板块 / 概念代码，如 {@code "600519.SH"} / {@code "885589.TI"}。可空。|-|
|tradeDate|string|false|单日交易日，{@code YYYYMMDD}。可空（与 startDate/endDate 互斥优先）。|-|
|startDate|string|false|起始交易日，{@code YYYYMMDD}。可空。|-|
|endDate|string|false|结束交易日，{@code YYYYMMDD}。可空。|-|
|dataType|string|false|数据类型 / 板块类型（如 ths-hot 的 data_type、tdx-index 的 idx_type、st-daily 的 type、bak-basic 的 industry）。可空。|-|
|nameKeyword|string|false|名称模糊关键字（如 hm-name 游资名、ths-index/tdx-index name 模糊匹配、ci 一级行业名 l1Name 等）。可空。|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/stock/market/hm-detail?page=0&size=0&dataType=&tradeDate=&nameKeyword=&endDate=&startDate=&tsCode='
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─tradeDate|string|交易日|-|
|└─tsCode|string|TS 代码|-|
|└─tsName|string|股票名称|-|
|└─buyAmount|number|买入金额|-|
|└─sellAmount|number|卖出金额|-|
|└─netAmount|number|净买卖额|-|
|└─hmName|string|游资名称|-|
|└─hmOrgs|string|关联机构（营业部 / 席位）|-|
|└─tag|string|游资标签|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "tradeDate": "yyyy-MM-dd HH:mm:ss",
      "tsCode": "",
      "tsName": "",
      "buyAmount": 0,
      "sellAmount": 0,
      "netAmount": 0,
      "hmName": "",
      "hmOrgs": "",
      "tag": ""
    }
  ],
  "traceId": ""
}
```

### 每日筹码分布明细（{@code stock_cyq_chips}）。tsCode 必填，缺失返回空。<br>与 /cyq-perf（性能聚合指标）互补。
**URL:** /openapi/v1/stock/market/cyq-chips

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 每日筹码分布明细（{@code stock_cyq_chips}）。tsCode 必填，缺失返回空。
与 /cyq-perf（性能聚合指标）互补。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|page|int32|false|第几页，从 1 起。默认 1。0 / 负数会被当成 1。|-|
|size|int32|false|每页记录数。默认 50，硬上限 {@value #MAX_SIZE}。<br/><p>传入超过 {@value #MAX_SIZE} 时会被自动截断到 {@value #MAX_SIZE}（不报错）。</p>|-|
|tsCode|string|false|股票 / 板块 / 概念代码，如 {@code "600519.SH"} / {@code "885589.TI"}。可空。|-|
|tradeDate|string|false|单日交易日，{@code YYYYMMDD}。可空（与 startDate/endDate 互斥优先）。|-|
|startDate|string|false|起始交易日，{@code YYYYMMDD}。可空。|-|
|endDate|string|false|结束交易日，{@code YYYYMMDD}。可空。|-|
|dataType|string|false|数据类型 / 板块类型（如 ths-hot 的 data_type、tdx-index 的 idx_type、st-daily 的 type、bak-basic 的 industry）。可空。|-|
|nameKeyword|string|false|名称模糊关键字（如 hm-name 游资名、ths-index/tdx-index name 模糊匹配、ci 一级行业名 l1Name 等）。可空。|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/stock/market/cyq-chips?page=0&size=0&tradeDate=&tsCode=&startDate=&dataType=&nameKeyword=&endDate='
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─tradeDate|string|交易日|-|
|└─tsCode|string|TS 代码|-|
|└─price|number|价格档位|-|
|└─percent|number|价位占比(%)|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "tradeDate": "yyyy-MM-dd HH:mm:ss",
      "tsCode": "",
      "price": 0,
      "percent": 0
    }
  ],
  "traceId": ""
}
```

### ST 股票每日列表（{@code stock_st_daily}）。dataType 承载 type 过滤（*ST / ST / NST 等）。
**URL:** /openapi/v1/stock/market/st-daily

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** ST 股票每日列表（{@code stock_st_daily}）。dataType 承载 type 过滤（*ST / ST / NST 等）。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|page|int32|false|第几页，从 1 起。默认 1。0 / 负数会被当成 1。|-|
|size|int32|false|每页记录数。默认 50，硬上限 {@value #MAX_SIZE}。<br/><p>传入超过 {@value #MAX_SIZE} 时会被自动截断到 {@value #MAX_SIZE}（不报错）。</p>|-|
|tsCode|string|false|股票 / 板块 / 概念代码，如 {@code "600519.SH"} / {@code "885589.TI"}。可空。|-|
|tradeDate|string|false|单日交易日，{@code YYYYMMDD}。可空（与 startDate/endDate 互斥优先）。|-|
|startDate|string|false|起始交易日，{@code YYYYMMDD}。可空。|-|
|endDate|string|false|结束交易日，{@code YYYYMMDD}。可空。|-|
|dataType|string|false|数据类型 / 板块类型（如 ths-hot 的 data_type、tdx-index 的 idx_type、st-daily 的 type、bak-basic 的 industry）。可空。|-|
|nameKeyword|string|false|名称模糊关键字（如 hm-name 游资名、ths-index/tdx-index name 模糊匹配、ci 一级行业名 l1Name 等）。可空。|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/stock/market/st-daily?page=0&size=0&endDate=&startDate=&dataType=&tsCode=&nameKeyword=&tradeDate='
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─tradeDate|string|交易日|-|
|└─tsCode|string|TS 代码|-|
|└─name|string|股票名称|-|
|└─type|string|ST 类型|-|
|└─typeName|string|ST 类型名称|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "tradeDate": "yyyy-MM-dd HH:mm:ss",
      "tsCode": "",
      "name": "",
      "type": "",
      "typeName": ""
    }
  ],
  "traceId": ""
}
```

### ST 风险警示事件（{@code stock_st_warning}）。事件型（pubDate 公告 / impDate 实施）。<br>dataType 承载 stType；startDate/endDate 按公告日期过滤。
**URL:** /openapi/v1/stock/market/st-warning

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** ST 风险警示事件（{@code stock_st_warning}）。事件型（pubDate 公告 / impDate 实施）。
dataType 承载 stType；startDate/endDate 按公告日期过滤。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|page|int32|false|第几页，从 1 起。默认 1。0 / 负数会被当成 1。|-|
|size|int32|false|每页记录数。默认 50，硬上限 {@value #MAX_SIZE}。<br/><p>传入超过 {@value #MAX_SIZE} 时会被自动截断到 {@value #MAX_SIZE}（不报错）。</p>|-|
|tsCode|string|false|股票 / 板块 / 概念代码，如 {@code "600519.SH"} / {@code "885589.TI"}。可空。|-|
|tradeDate|string|false|单日交易日，{@code YYYYMMDD}。可空（与 startDate/endDate 互斥优先）。|-|
|startDate|string|false|起始交易日，{@code YYYYMMDD}。可空。|-|
|endDate|string|false|结束交易日，{@code YYYYMMDD}。可空。|-|
|dataType|string|false|数据类型 / 板块类型（如 ths-hot 的 data_type、tdx-index 的 idx_type、st-daily 的 type、bak-basic 的 industry）。可空。|-|
|nameKeyword|string|false|名称模糊关键字（如 hm-name 游资名、ths-index/tdx-index name 模糊匹配、ci 一级行业名 l1Name 等）。可空。|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/stock/market/st-warning?page=0&size=0&startDate=&dataType=&nameKeyword=&tradeDate=&tsCode=&endDate='
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─tsCode|string|TS 代码|-|
|└─name|string|证券名称|-|
|└─pubDate|string|公告日期|-|
|└─impDate|string|实施日期|-|
|└─stType|string|ST 类型|-|
|└─stReason|string|ST 原因|-|
|└─stExplain|string|ST 说明|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "tsCode": "",
      "name": "",
      "pubDate": "yyyy-MM-dd HH:mm:ss",
      "impDate": "yyyy-MM-dd HH:mm:ss",
      "stType": "",
      "stReason": "",
      "stExplain": ""
    }
  ],
  "traceId": ""
}
```

### 备用基础数据（{@code stock_bak_basic}）。每日股票基础快照（含估值 / 财务 / 股本 / 股东户数）。<br>dataType 承载 industry 过滤。
**URL:** /openapi/v1/stock/market/bak-basic

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 备用基础数据（{@code stock_bak_basic}）。每日股票基础快照（含估值 / 财务 / 股本 / 股东户数）。
dataType 承载 industry 过滤。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|page|int32|false|第几页，从 1 起。默认 1。0 / 负数会被当成 1。|-|
|size|int32|false|每页记录数。默认 50，硬上限 {@value #MAX_SIZE}。<br/><p>传入超过 {@value #MAX_SIZE} 时会被自动截断到 {@value #MAX_SIZE}（不报错）。</p>|-|
|tsCode|string|false|股票 / 板块 / 概念代码，如 {@code "600519.SH"} / {@code "885589.TI"}。可空。|-|
|tradeDate|string|false|单日交易日，{@code YYYYMMDD}。可空（与 startDate/endDate 互斥优先）。|-|
|startDate|string|false|起始交易日，{@code YYYYMMDD}。可空。|-|
|endDate|string|false|结束交易日，{@code YYYYMMDD}。可空。|-|
|dataType|string|false|数据类型 / 板块类型（如 ths-hot 的 data_type、tdx-index 的 idx_type、st-daily 的 type、bak-basic 的 industry）。可空。|-|
|nameKeyword|string|false|名称模糊关键字（如 hm-name 游资名、ths-index/tdx-index name 模糊匹配、ci 一级行业名 l1Name 等）。可空。|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/stock/market/bak-basic?page=0&size=0&nameKeyword=&tradeDate=&endDate=&startDate=&tsCode=&dataType='
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─tradeDate|string|交易日|-|
|└─tsCode|string|TS 代码|-|
|└─name|string|股票名称|-|
|└─industry|string|所属行业|-|
|└─area|string|所属区域|-|
|└─pe|number|市盈率|-|
|└─floatShare|number|流通股本（万股）|-|
|└─totalShare|number|总股本（万股）|-|
|└─totalAssets|number|总资产（万元）|-|
|└─liquidAssets|number|流动资产（万元）|-|
|└─fixedAssets|number|固定资产（万元）|-|
|└─reserved|number|公积金（万元）|-|
|└─reservedPershare|number|每股公积金|-|
|└─eps|number|每股收益|-|
|└─bvps|number|每股净资产|-|
|└─pb|number|市净率|-|
|└─listDate|string|上市日期|-|
|└─undp|number|未分配利润（万元）|-|
|└─perUndp|number|每股未分配利润|-|
|└─revYoy|number|营收同比(%)|-|
|└─profitYoy|number|净利润同比(%)|-|
|└─gpr|number|毛利率|-|
|└─npr|number|净利率|-|
|└─holderNum|int32|股东户数|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "tradeDate": "yyyy-MM-dd HH:mm:ss",
      "tsCode": "",
      "name": "",
      "industry": "",
      "area": "",
      "pe": 0,
      "floatShare": 0,
      "totalShare": 0,
      "totalAssets": 0,
      "liquidAssets": 0,
      "fixedAssets": 0,
      "reserved": 0,
      "reservedPershare": 0,
      "eps": 0,
      "bvps": 0,
      "pb": 0,
      "listDate": "yyyy-MM-dd HH:mm:ss",
      "undp": 0,
      "perUndp": 0,
      "revYoy": 0,
      "profitYoy": 0,
      "gpr": 0,
      "npr": 0,
      "holderNum": 0
    }
  ],
  "traceId": ""
}
```

### 备用行情（{@code stock_bak_daily}）。扩展字段：振幅 / 活跃度 / 区间动量 / 平均换手。<br>dataType 承载 industry 过滤。
**URL:** /openapi/v1/stock/market/bak-daily

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 备用行情（{@code stock_bak_daily}）。扩展字段：振幅 / 活跃度 / 区间动量 / 平均换手。
dataType 承载 industry 过滤。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|page|int32|false|第几页，从 1 起。默认 1。0 / 负数会被当成 1。|-|
|size|int32|false|每页记录数。默认 50，硬上限 {@value #MAX_SIZE}。<br/><p>传入超过 {@value #MAX_SIZE} 时会被自动截断到 {@value #MAX_SIZE}（不报错）。</p>|-|
|tsCode|string|false|股票 / 板块 / 概念代码，如 {@code "600519.SH"} / {@code "885589.TI"}。可空。|-|
|tradeDate|string|false|单日交易日，{@code YYYYMMDD}。可空（与 startDate/endDate 互斥优先）。|-|
|startDate|string|false|起始交易日，{@code YYYYMMDD}。可空。|-|
|endDate|string|false|结束交易日，{@code YYYYMMDD}。可空。|-|
|dataType|string|false|数据类型 / 板块类型（如 ths-hot 的 data_type、tdx-index 的 idx_type、st-daily 的 type、bak-basic 的 industry）。可空。|-|
|nameKeyword|string|false|名称模糊关键字（如 hm-name 游资名、ths-index/tdx-index name 模糊匹配、ci 一级行业名 l1Name 等）。可空。|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/stock/market/bak-daily?page=0&size=0&startDate=&dataType=&endDate=&nameKeyword=&tsCode=&tradeDate='
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─tsCode|string|TS 代码|-|
|└─tradeDate|string|交易日|-|
|└─name|string|股票名称|-|
|└─pctChange|number|涨跌幅(%)|-|
|└─close|number|收盘价|-|
|└─change|number|涨跌额|-|
|└─open|number|开盘价|-|
|└─high|number|最高价|-|
|└─low|number|最低价|-|
|└─preClose|number|昨收价|-|
|└─volRatio|number|量比|-|
|└─turnOver|number|换手率(%)|-|
|└─swing|number|振幅(%)|-|
|└─vol|number|成交量|-|
|└─amount|number|成交额|-|
|└─selling|number|内盘成交额|-|
|└─buying|number|外盘成交额|-|
|└─totalShare|number|总股本（万股）|-|
|└─floatShare|number|流通股本（万股）|-|
|└─pe|number|市盈率|-|
|└─industry|string|所属行业|-|
|└─area|string|所属区域|-|
|└─floatMv|number|流通市值|-|
|└─totalMv|number|总市值|-|
|└─avgPrice|number|均价|-|
|└─strength|number|强弱度|-|
|└─activity|number|活跃度|-|
|└─avgTurnover|number|平均换手率|-|
|└─attack|number|攻击波(%)|-|
|└─interval3|number|近 3 月涨幅(%)|-|
|└─interval6|number|近 6 月涨幅(%)|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "tsCode": "",
      "tradeDate": "yyyy-MM-dd HH:mm:ss",
      "name": "",
      "pctChange": 0,
      "close": 0,
      "change": 0,
      "open": 0,
      "high": 0,
      "low": 0,
      "preClose": 0,
      "volRatio": 0,
      "turnOver": 0,
      "swing": 0,
      "vol": 0,
      "amount": 0,
      "selling": 0,
      "buying": 0,
      "totalShare": 0,
      "floatShare": 0,
      "pe": 0,
      "industry": "",
      "area": "",
      "floatMv": 0,
      "totalMv": 0,
      "avgPrice": 0,
      "strength": 0,
      "activity": 0,
      "avgTurnover": 0,
      "attack": 0,
      "interval3": 0,
      "interval6": 0
    }
  ],
  "traceId": ""
}
```

## OpenAPI v1 —— 技术指标历史时间序列端点（stock.indicator scope）。

&lt;p&gt;覆盖 6 张 PG 表：
&lt;ul&gt;
  &lt;li&gt;{@code stock_tech_ma_channel}（86 列：均线 + 通道）&lt;/li&gt;
  &lt;li&gt;{@code stock_tech_oscillator}（62 列：振荡指标）&lt;/li&gt;
  &lt;li&gt;{@code stock_tech_trend_volume}（47 列：趋势量能）&lt;/li&gt;
  &lt;li&gt;{@code stock_short_term_tech_indicators}（19 个短线因子）&lt;/li&gt;
  &lt;li&gt;{@code stock_quo_indicator_daily}（PE/PB/换手率/市值历史）&lt;/li&gt;
  &lt;li&gt;{@code stock_nine_turn}（DeMark 九转序列）&lt;/li&gt;
&lt;/ul&gt;

&lt;p&gt;共享 {@link StockTechIndicatorForm}：tsCode（必填）+ startDate + endDate + adjType + page/size。
adjType 仅前 3 个端点生效，仅接受 &lt;code&gt;bfq&lt;/code&gt;/&lt;code&gt;hfq&lt;/code&gt;/&lt;code&gt;qfq&lt;/code&gt;。

&lt;p&gt;套餐归属：Free 及以上（免费档即含；详见 docs/openapi-token.md）。

&lt;p&gt;对应 MCP 工具：见 {@code stock_mcp/src/stock_mcp/tools/indicator.py}。
### MA / EMA / BOLL / BBI / KTN / TAQ / EXPMA 均线与通道指标。
**URL:** /openapi/v1/stock/indicator/ma-channel

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** MA / EMA / BOLL / BBI / KTN / TAQ / EXPMA 均线与通道指标。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|page|int32|false|第几页，从 1 起。默认 1。0 / 负数会被当成 1。|-|
|size|int32|false|每页记录数。默认 50，硬上限 {@value #MAX_SIZE}。<br/><p>传入超过 {@value #MAX_SIZE} 时会被自动截断到 {@value #MAX_SIZE}（不报错）。</p>|-|
|tsCode|string|false|股票代码（带交易所后缀），如 {@code "600519.SH"} / {@code "000001.SZ"}。<b>必填</b>。|-|
|startDate|string|false|起始日期，格式 {@code YYYYMMDD}（如 {@code "20260301"}）。可空。<br/><p>不传时取最近 60 个交易日（约 3 个月）窗口。</p>|-|
|endDate|string|false|结束日期，格式 {@code YYYYMMDD}（如 {@code "20260430"}）。可空。<br/><p>不传时取最新交易日。</p>|-|
|adjType|string|false|复权类型：{@code "bfq"}（不复权，默认）/ {@code "hfq"}（后复权）/ {@code "qfq"}（前复权）。<br/><br/><p><b>怎么选</b>：</p><br/><ul><br/>  <li>看图 / 看趋势 → {@code "bfq"} 或 {@code "qfq"}</li><br/>  <li>量化策略 / 跨除权日比较 → {@code "hfq"}（基准固定，最稳）</li><br/></ul><br/><br/><p>仅 {@code ma-channel} / {@code oscillator} / {@code trend-volume} 三个端点生效，其余端点忽略此字段。</p>|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/stock/indicator/ma-channel?page=0&size=0&endDate=&adjType=&tsCode=&startDate='
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─tsCode|string|股票代码（带交易所后缀），如 {@code "600519.SH"}。|-|
|└─tradeDate|string|交易日期。|-|
|└─ma5|number|MA5：5 日简单移动平均（短期支撑 / 阻力）。|-|
|└─ma10|number|MA10：10 日简单移动平均。|-|
|└─ma20|number|MA20：20 日简单移动平均（月线，趋势分水岭）。|-|
|└─ma30|number|MA30：30 日简单移动平均。|-|
|└─ma60|number|MA60：60 日简单移动平均（季线，中期趋势）。|-|
|└─ma90|number|MA90：90 日简单移动平均。|-|
|└─ma250|number|MA250：250 日简单移动平均（年线，长期趋势）。|-|
|└─ema5|number|EMA5：5 日指数移动平均（对近期价格更敏感）。|-|
|└─ema10|number|EMA10：10 日指数移动平均。|-|
|└─ema20|number|EMA20：20 日指数移动平均。|-|
|└─ema30|number|EMA30：30 日指数移动平均。|-|
|└─ema60|number|EMA60：60 日指数移动平均。|-|
|└─ema90|number|EMA90：90 日指数移动平均。|-|
|└─ema250|number|EMA250：250 日指数移动平均。|-|
|└─bollUpper|number|布林线上轨 = MA20 + 2 × StdDev20（突破上轨可能超买）。|-|
|└─bollMid|number|布林线中轨 = MA20。|-|
|└─bollLower|number|布林线下轨 = MA20 − 2 × StdDev20（跌破下轨可能超卖）。|-|
|└─bbi|number|BBI：多空指标 = (MA3 + MA6 + MA12 + MA24) / 4，用于判断多空力量平衡。|-|
|└─ktnUpper|number|肯特纳通道上轨 = EMA20 + 2 × ATR。|-|
|└─ktnMid|number|肯特纳通道中轨 = EMA20。|-|
|└─ktnDown|number|肯特纳通道下轨 = EMA20 − 2 × ATR。|-|
|└─taqUp|number|唐安奇通道上轨 = 近 N 日最高价（突破即买入信号）。|-|
|└─taqMid|number|唐安奇通道中轨 = (taqUp + taqDown) / 2。|-|
|└─taqDown|number|唐安奇通道下轨 = 近 N 日最低价。|-|
|└─expma12|number|EXPMA12：12 日指数平均。|-|
|└─expma50|number|EXPMA50：50 日指数平均。|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "tsCode": "",
      "tradeDate": "yyyy-MM-dd HH:mm:ss",
      "ma5": 0,
      "ma10": 0,
      "ma20": 0,
      "ma30": 0,
      "ma60": 0,
      "ma90": 0,
      "ma250": 0,
      "ema5": 0,
      "ema10": 0,
      "ema20": 0,
      "ema30": 0,
      "ema60": 0,
      "ema90": 0,
      "ema250": 0,
      "bollUpper": 0,
      "bollMid": 0,
      "bollLower": 0,
      "bbi": 0,
      "ktnUpper": 0,
      "ktnMid": 0,
      "ktnDown": 0,
      "taqUp": 0,
      "taqMid": 0,
      "taqDown": 0,
      "expma12": 0,
      "expma50": 0
    }
  ],
  "traceId": ""
}
```

### MACD / KDJ / RSI / BIAS / DMI / CCI / WR / BRAR / CR 振荡与情绪指标。
**URL:** /openapi/v1/stock/indicator/oscillator

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** MACD / KDJ / RSI / BIAS / DMI / CCI / WR / BRAR / CR 振荡与情绪指标。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|page|int32|false|第几页，从 1 起。默认 1。0 / 负数会被当成 1。|-|
|size|int32|false|每页记录数。默认 50，硬上限 {@value #MAX_SIZE}。<br/><p>传入超过 {@value #MAX_SIZE} 时会被自动截断到 {@value #MAX_SIZE}（不报错）。</p>|-|
|tsCode|string|false|股票代码（带交易所后缀），如 {@code "600519.SH"} / {@code "000001.SZ"}。<b>必填</b>。|-|
|startDate|string|false|起始日期，格式 {@code YYYYMMDD}（如 {@code "20260301"}）。可空。<br/><p>不传时取最近 60 个交易日（约 3 个月）窗口。</p>|-|
|endDate|string|false|结束日期，格式 {@code YYYYMMDD}（如 {@code "20260430"}）。可空。<br/><p>不传时取最新交易日。</p>|-|
|adjType|string|false|复权类型：{@code "bfq"}（不复权，默认）/ {@code "hfq"}（后复权）/ {@code "qfq"}（前复权）。<br/><br/><p><b>怎么选</b>：</p><br/><ul><br/>  <li>看图 / 看趋势 → {@code "bfq"} 或 {@code "qfq"}</li><br/>  <li>量化策略 / 跨除权日比较 → {@code "hfq"}（基准固定，最稳）</li><br/></ul><br/><br/><p>仅 {@code ma-channel} / {@code oscillator} / {@code trend-volume} 三个端点生效，其余端点忽略此字段。</p>|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/stock/indicator/oscillator?page=0&size=0&startDate=&tsCode=&adjType=&endDate='
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─tsCode|string|股票代码（带交易所后缀），如 {@code "600519.SH"}。|-|
|└─tradeDate|string|交易日期。|-|
|└─macd|number|MACD 柱状值（DIF − DEA）。{@code > 0} 多头，{@code < 0} 空头。|-|
|└─macdDif|number|MACD DIF（快线）= EMA12 − EMA26。|-|
|└─macdDea|number|MACD DEA（慢线）= DIF 的 9 日 EMA。DIF 上穿 DEA = 金叉。|-|
|└─kdjK|number|KDJ K 值（[0,100]）。{@code > 80} 超买，{@code < 20} 超卖。|-|
|└─kdjD|number|KDJ D 值（K 的平滑均线）。|-|
|└─kdjJ|number|KDJ J 值 = 3K − 2D（更敏感，可超出 [0,100]）。|-|
|└─rsi6|number|RSI 6 日（短期，[0,100]）。{@code > 80} 超买，{@code < 20} 超卖。|-|
|└─rsi12|number|RSI 12 日。|-|
|└─rsi24|number|RSI 24 日（长期）。|-|
|└─bias1|number|BIAS1：6 日乖离率（%）= (close − MA6) / MA6 × 100。|-|
|└─bias2|number|BIAS2：12 日乖离率。|-|
|└─bias3|number|BIAS3：24 日乖离率。|-|
|└─dmiPdi|number|DMI +DI：上升动向指标。+DI 上穿 −DI 看多。|-|
|└─dmiMdi|number|DMI −DI：下降动向指标。|-|
|└─dmiAdx|number|DMI ADX：平均趋向。{@code > 25} 趋势明显。|-|
|└─dmiAdxr|number|DMI ADXR：平均趋向评估。|-|
|└─cci|number|CCI：顺势指标。{@code > +100} 超买，{@code < −100} 超卖。|-|
|└─wr|number|WR：威廉指标（[0,100]，反向）。{@code < 20} 超买，{@code > 80} 超卖。|-|
|└─wr1|number|WR1：威廉指标（更长周期）。|-|
|└─brarAr|number|BRAR AR：人气指标。{@code > 150} 强势。|-|
|└─brarBr|number|BRAR BR：意愿指标。AR / BR 同向上升 = 多方占优。|-|
|└─cr|number|CR：价格动量指标。{@code > 200} 高位，{@code < 50} 低位。|-|
|└─upDays|int32|当前已连续上涨 N 天。|-|
|└─downDays|int32|当前已连续下跌 N 天。|-|
|└─lowDays|int32|距离最近创新低 N 天（{@code 0} 表示当日就是最新低点）。|-|
|└─topDays|int32|距离最近创新高 N 天。|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "tsCode": "",
      "tradeDate": "yyyy-MM-dd HH:mm:ss",
      "macd": 0,
      "macdDif": 0,
      "macdDea": 0,
      "kdjK": 0,
      "kdjD": 0,
      "kdjJ": 0,
      "rsi6": 0,
      "rsi12": 0,
      "rsi24": 0,
      "bias1": 0,
      "bias2": 0,
      "bias3": 0,
      "dmiPdi": 0,
      "dmiMdi": 0,
      "dmiAdx": 0,
      "dmiAdxr": 0,
      "cci": 0,
      "wr": 0,
      "wr1": 0,
      "brarAr": 0,
      "brarBr": 0,
      "cr": 0,
      "upDays": 0,
      "downDays": 0,
      "lowDays": 0,
      "topDays": 0
    }
  ],
  "traceId": ""
}
```

### ATR / OBV / ASI / TRIX / VR / PSY / MTM / ROC / EMV / DFMA / DPO / MASS / MFI / XSII<br>趋势、量能与动量指标。
**URL:** /openapi/v1/stock/indicator/trend-volume

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** ATR / OBV / ASI / TRIX / VR / PSY / MTM / ROC / EMV / DFMA / DPO / MASS / MFI / XSII
趋势、量能与动量指标。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|page|int32|false|第几页，从 1 起。默认 1。0 / 负数会被当成 1。|-|
|size|int32|false|每页记录数。默认 50，硬上限 {@value #MAX_SIZE}。<br/><p>传入超过 {@value #MAX_SIZE} 时会被自动截断到 {@value #MAX_SIZE}（不报错）。</p>|-|
|tsCode|string|false|股票代码（带交易所后缀），如 {@code "600519.SH"} / {@code "000001.SZ"}。<b>必填</b>。|-|
|startDate|string|false|起始日期，格式 {@code YYYYMMDD}（如 {@code "20260301"}）。可空。<br/><p>不传时取最近 60 个交易日（约 3 个月）窗口。</p>|-|
|endDate|string|false|结束日期，格式 {@code YYYYMMDD}（如 {@code "20260430"}）。可空。<br/><p>不传时取最新交易日。</p>|-|
|adjType|string|false|复权类型：{@code "bfq"}（不复权，默认）/ {@code "hfq"}（后复权）/ {@code "qfq"}（前复权）。<br/><br/><p><b>怎么选</b>：</p><br/><ul><br/>  <li>看图 / 看趋势 → {@code "bfq"} 或 {@code "qfq"}</li><br/>  <li>量化策略 / 跨除权日比较 → {@code "hfq"}（基准固定，最稳）</li><br/></ul><br/><br/><p>仅 {@code ma-channel} / {@code oscillator} / {@code trend-volume} 三个端点生效，其余端点忽略此字段。</p>|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/stock/indicator/trend-volume?page=0&size=0&startDate=&endDate=&tsCode=&adjType='
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─tsCode|string|股票代码（带交易所后缀），如 {@code "600519.SH"}。|-|
|└─tradeDate|string|交易日期。|-|
|└─atr|number|ATR：真实波动幅度（绝对波动量）。{@code ATR / close} 越大波动越大。|-|
|└─obv|number|OBV：能量潮（累计净买卖量）。OBV 创新高 + 价格未创新高 = 多头确认。|-|
|└─asi|number|ASI：振动升降指标。趋势确认。|-|
|└─asit|number|ASIT：ASI 累计值。|-|
|└─trix|number|TRIX：三重指数平滑（消除噪音的趋势）。|-|
|└─trma|number|TRMA：TRIX 的均线（信号线）。TRIX 上穿 TRMA = 买入。|-|
|└─vr|number|VR：容量比率。{@code > 250} 高位需谨慎，{@code < 70} 低位可关注。|-|
|└─psy|number|PSY：心理线（[0,100]）。{@code > 75} 超买，{@code < 25} 超卖。|-|
|└─psyMa|number|PSY 的均线（平滑信号）。|-|
|└─mtm|number|MTM：动量指标 = close − close[N]。|-|
|└─mtmMa|number|MTM 的均线。|-|
|└─roc|number|ROC：变动率（%）= (close − close[N]) / close[N] × 100。|-|
|└─maRoc|number|ROC 的均线。|-|
|└─emv|number|EMV：简易波动指标。判断量价配合，{@code > 0} 量价齐升。|-|
|└─maemv|number|EMV 的均线。|-|
|└─dfmaDif|number|DFMA DIF：平行线差。|-|
|└─dfmaDifma|number|DFMA DIFMA：DIF 的均线。|-|
|└─dpo|number|DPO：区间震荡指标（剔除趋势看震荡）。|-|
|└─madpo|number|DPO 的均线。|-|
|└─mass|number|MASS：梅斯线（看反转，{@code > 27} 即将反转）。|-|
|└─maMass|number|MASS 的均线。|-|
|└─mfi|number|MFI：资金流量指标（带量的 RSI，[0,100]）。{@code > 80} 超买，{@code < 20} 超卖。|-|
|└─xsiiTd1|number|XSII TD1：薛斯通道 II 第 1 线（强阻力位）。|-|
|└─xsiiTd2|number|XSII TD2：第 2 线（弱阻力位）。|-|
|└─xsiiTd3|number|XSII TD3：第 3 线（弱支撑位）。|-|
|└─xsiiTd4|number|XSII TD4：第 4 线（强支撑位）。|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "tsCode": "",
      "tradeDate": "yyyy-MM-dd HH:mm:ss",
      "atr": 0,
      "obv": 0,
      "asi": 0,
      "asit": 0,
      "trix": 0,
      "trma": 0,
      "vr": 0,
      "psy": 0,
      "psyMa": 0,
      "mtm": 0,
      "mtmMa": 0,
      "roc": 0,
      "maRoc": 0,
      "emv": 0,
      "maemv": 0,
      "dfmaDif": 0,
      "dfmaDifma": 0,
      "dpo": 0,
      "madpo": 0,
      "mass": 0,
      "maMass": 0,
      "mfi": 0,
      "xsiiTd1": 0,
      "xsiiTd2": 0,
      "xsiiTd3": 0,
      "xsiiTd4": 0
    }
  ],
  "traceId": ""
}
```

### 19 个短线量化因子（动量、波动、量能、位置、情绪、盘中）。<br>不需要 adjType。
**URL:** /openapi/v1/stock/indicator/short-term

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 19 个短线量化因子（动量、波动、量能、位置、情绪、盘中）。
不需要 adjType。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|page|int32|false|第几页，从 1 起。默认 1。0 / 负数会被当成 1。|-|
|size|int32|false|每页记录数。默认 50，硬上限 {@value #MAX_SIZE}。<br/><p>传入超过 {@value #MAX_SIZE} 时会被自动截断到 {@value #MAX_SIZE}（不报错）。</p>|-|
|tsCode|string|false|股票代码（带交易所后缀），如 {@code "600519.SH"} / {@code "000001.SZ"}。<b>必填</b>。|-|
|startDate|string|false|起始日期，格式 {@code YYYYMMDD}（如 {@code "20260301"}）。可空。<br/><p>不传时取最近 60 个交易日（约 3 个月）窗口。</p>|-|
|endDate|string|false|结束日期，格式 {@code YYYYMMDD}（如 {@code "20260430"}）。可空。<br/><p>不传时取最新交易日。</p>|-|
|adjType|string|false|复权类型：{@code "bfq"}（不复权，默认）/ {@code "hfq"}（后复权）/ {@code "qfq"}（前复权）。<br/><br/><p><b>怎么选</b>：</p><br/><ul><br/>  <li>看图 / 看趋势 → {@code "bfq"} 或 {@code "qfq"}</li><br/>  <li>量化策略 / 跨除权日比较 → {@code "hfq"}（基准固定，最稳）</li><br/></ul><br/><br/><p>仅 {@code ma-channel} / {@code oscillator} / {@code trend-volume} 三个端点生效，其余端点忽略此字段。</p>|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/stock/indicator/short-term?page=0&size=0&startDate=&tsCode=&endDate=&adjType='
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─tsCode|string|股票代码（带交易所后缀）。|-|
|└─tradeDate|string|交易日期。|-|
|└─momentum5|number|5 日动量（涨跌幅 %）。|-|
|└─momentum10|number|10 日动量。|-|
|└─rateOfChange|number|当日变动率（%）。|-|
|└─volatility10|number|10 日波动率（标准差）。|-|
|└─volatility20|number|20 日波动率。|-|
|└─historicalVol|number|年化历史波动率（%）。|-|
|└─volumeMa5|number|5 日成交量均量。|-|
|└─volumeMa20|number|20 日成交量均量。|-|
|└─volumeBias|number|量能乖离率：当日量 / 均量 − 1。{@code > 1} 显著放量。|-|
|└─accumulation|number|累积分布（OBV 类）。|-|
|└─position20|number|20 日价格位置：(close − low20) / (high20 − low20) × 100，[0,100]。{@code > 80} 高位。|-|
|└─position60|number|60 日价格位置。|-|
|└─resistanceLevel|number|阻力位估值（元）：基于近期高点测算。|-|
|└─supportLevel|number|支撑位估值（元）：基于近期低点测算。|-|
|└─marketHeat|number|市场热度评分（[0,100]）：综合换手 / 量比 / 涨幅。|-|
|└─attentionScore|number|关注度评分（[0,100]）：股吧 / 新闻提及频次。|-|
|└─sentimentIndex|number|情绪指数（[-100,100]）：负向 = 恐慌，正向 = 贪婪。|-|
|└─intradayAmplitude|number|日内振幅（%）= (high − low) / preClose × 100。|-|
|└─morningStrength|number|早盘强度（[0,100]）：开盘前 30 分钟表现。|-|
|└─afternoonTrend|number|尾盘趋势（[-100,100]）：尾盘 30 分钟买卖压力。|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "tsCode": "",
      "tradeDate": "yyyy-MM-dd HH:mm:ss",
      "momentum5": 0,
      "momentum10": 0,
      "rateOfChange": 0,
      "volatility10": 0,
      "volatility20": 0,
      "historicalVol": 0,
      "volumeMa5": 0,
      "volumeMa20": 0,
      "volumeBias": 0,
      "accumulation": 0,
      "position20": 0,
      "position60": 0,
      "resistanceLevel": 0,
      "supportLevel": 0,
      "marketHeat": 0,
      "attentionScore": 0,
      "sentimentIndex": 0,
      "intradayAmplitude": 0,
      "morningStrength": 0,
      "afternoonTrend": 0
    }
  ],
  "traceId": ""
}
```

### 估值指标历史时间序列（PE / PB / 换手率 / 市值 等）。<br>与 {@code /openapi/v1/stock/indicator/latest} 区别：latest 只返回最新交易日，<br>此端点返回历史区间。
**URL:** /openapi/v1/stock/indicator/valuation/history

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 估值指标历史时间序列（PE / PB / 换手率 / 市值 等）。
与 {@code /openapi/v1/stock/indicator/latest} 区别：latest 只返回最新交易日，
此端点返回历史区间。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|page|int32|false|第几页，从 1 起。默认 1。0 / 负数会被当成 1。|-|
|size|int32|false|每页记录数。默认 50，硬上限 {@value #MAX_SIZE}。<br/><p>传入超过 {@value #MAX_SIZE} 时会被自动截断到 {@value #MAX_SIZE}（不报错）。</p>|-|
|tsCode|string|false|股票代码（带交易所后缀），如 {@code "600519.SH"} / {@code "000001.SZ"}。<b>必填</b>。|-|
|startDate|string|false|起始日期，格式 {@code YYYYMMDD}（如 {@code "20260301"}）。可空。<br/><p>不传时取最近 60 个交易日（约 3 个月）窗口。</p>|-|
|endDate|string|false|结束日期，格式 {@code YYYYMMDD}（如 {@code "20260430"}）。可空。<br/><p>不传时取最新交易日。</p>|-|
|adjType|string|false|复权类型：{@code "bfq"}（不复权，默认）/ {@code "hfq"}（后复权）/ {@code "qfq"}（前复权）。<br/><br/><p><b>怎么选</b>：</p><br/><ul><br/>  <li>看图 / 看趋势 → {@code "bfq"} 或 {@code "qfq"}</li><br/>  <li>量化策略 / 跨除权日比较 → {@code "hfq"}（基准固定，最稳）</li><br/></ul><br/><br/><p>仅 {@code ma-channel} / {@code oscillator} / {@code trend-volume} 三个端点生效，其余端点忽略此字段。</p>|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/stock/indicator/valuation/history?page=0&size=0&endDate=&startDate=&adjType=&tsCode='
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─tsCode|string|股票代码（带交易所后缀），如 {@code "600519.SH"}。|-|
|└─symbol|string|纯数字股票代码，如 {@code "600519"}。|-|
|└─name|string|股票中文简称，如 {@code "贵州茅台"}。|-|
|└─tradeDate|string|数据所属交易日。|-|
|└─close|number|当日收盘价（元）。|-|
|└─turnoverRate|number|换手率（%）= 当日成交量 / 流通股本 × 100。|-|
|└─turnoverRateF|number|自由流通换手率（%）= 当日成交量 / 自由流通股本 × 100。一般比 {@link #turnoverRate} 更高。|-|
|└─volumeRatio|number|量比 = 当日成交量 / 近 5 日平均成交量。{@code > 1} 表示放量，{@code > 2} 显著放量。|-|
|└─pe|number|静态市盈率：股价 / 上一年度 EPS。|-|
|└─peTtm|number|滚动市盈率：股价 / 最近 4 个季度 EPS（最常用）。|-|
|└─pb|number|市净率：股价 / 每股净资产。|-|
|└─ps|number|静态市销率：股价 / 上一年度 EPS_revenue。|-|
|└─psTtm|number|滚动市销率：股价 / 最近 4 个季度营收（更平滑）。|-|
|└─dvRatio|number|静态股息率（%）= 上一年度每股分红 / 股价 × 100。|-|
|└─dvTtm|number|滚动股息率（%）= 最近 4 个季度每股分红 / 股价 × 100。|-|
|└─totalShare|number|总股本（万股）。|-|
|└─floatShare|number|流通股本（万股）。|-|
|└─freeShare|number|自由流通股本（万股）。剔除限售 / 高管 / 国资等长期不流通部分。|-|
|└─totalMv|number|总市值（万元）= 总股本 × 当日收盘价。|-|
|└─circMv|number|流通市值（万元）= 流通股本 × 当日收盘价。|-|
|└─limitStatus|int8|涨跌停状态。<br/><ul><br/>  <li>{@code 0} —— 普通</li><br/>  <li>{@code 1} —— 涨停</li><br/>  <li>{@code 2} —— 跌停</li><br/>  <li>{@code 3} —— 一字涨停（开盘即涨停）</li><br/>  <li>{@code 4} —— 一字跌停</li><br/></ul><br/><p>具体编码以后端 {@code com.common.enums.LimitStatus} 为准。</p>|-|
|└─roe|number|净资产收益率（%，最近一期）。{@code > 15%} 普遍认为是优秀。|-|
|└─chg|number|涨跌额（元）= close - preClose。|-|
|└─pctChg|number|涨跌幅（%）。|-|
|└─roeDate|string|ROE 数据所属报告期日（季末日期，如 {@code 2026-03-31}）。|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{"code":0,"msg":"","data":[{"tsCode":"","symbol":"","name":"","tradeDate":"yyyy-MM-dd HH:mm:ss","close":0,"turnoverRate":0,"turnoverRateF":0,"volumeRatio":0,"pe":0,"peTtm":0,"pb":0,"ps":0,"psTtm":0,"dvRatio":0,"dvTtm":0,"totalShare":0,"floatShare":0,"freeShare":0,"totalMv":0,"circMv":0,"limitStatus":,"roe":0,"chg":0,"pctChg":0,"roeDate":"yyyy-MM-dd HH:mm:ss"}],"traceId":""}
```

### DeMark 九转序列信号（识别趋势衰竭与反转点）。
**URL:** /openapi/v1/stock/indicator/nine-turn

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** DeMark 九转序列信号（识别趋势衰竭与反转点）。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|page|int32|false|第几页，从 1 起。默认 1。0 / 负数会被当成 1。|-|
|size|int32|false|每页记录数。默认 50，硬上限 {@value #MAX_SIZE}。<br/><p>传入超过 {@value #MAX_SIZE} 时会被自动截断到 {@value #MAX_SIZE}（不报错）。</p>|-|
|tsCode|string|false|股票代码（带交易所后缀），如 {@code "600519.SH"} / {@code "000001.SZ"}。<b>必填</b>。|-|
|startDate|string|false|起始日期，格式 {@code YYYYMMDD}（如 {@code "20260301"}）。可空。<br/><p>不传时取最近 60 个交易日（约 3 个月）窗口。</p>|-|
|endDate|string|false|结束日期，格式 {@code YYYYMMDD}（如 {@code "20260430"}）。可空。<br/><p>不传时取最新交易日。</p>|-|
|adjType|string|false|复权类型：{@code "bfq"}（不复权，默认）/ {@code "hfq"}（后复权）/ {@code "qfq"}（前复权）。<br/><br/><p><b>怎么选</b>：</p><br/><ul><br/>  <li>看图 / 看趋势 → {@code "bfq"} 或 {@code "qfq"}</li><br/>  <li>量化策略 / 跨除权日比较 → {@code "hfq"}（基准固定，最稳）</li><br/></ul><br/><br/><p>仅 {@code ma-channel} / {@code oscillator} / {@code trend-volume} 三个端点生效，其余端点忽略此字段。</p>|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/stock/indicator/nine-turn?page=0&size=0&tsCode=&startDate=&adjType=&endDate='
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─tsCode|string|No comments found.|-|
|└─tradeDate|string|No comments found.|-|
|└─freq|string|周期：D 日 / W 周 / M 月|-|
|└─open|number|No comments found.|-|
|└─high|number|No comments found.|-|
|└─low|number|No comments found.|-|
|└─close|number|No comments found.|-|
|└─vol|number|No comments found.|-|
|└─amount|number|No comments found.|-|
|└─upCount|int32|连续上涨计数|-|
|└─downCount|int32|连续下跌计数|-|
|└─nineUpTurn|string|九上转信号文本（如 "9-up" / null）|-|
|└─nineDownTurn|string|九下转信号文本（如 "9-down" / null）|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "tsCode": "",
      "tradeDate": "yyyy-MM-dd HH:mm:ss",
      "freq": "",
      "open": 0,
      "high": 0,
      "low": 0,
      "close": 0,
      "vol": 0,
      "amount": 0,
      "upCount": 0,
      "downCount": 0,
      "nineUpTurn": "",
      "nineDownTurn": ""
    }
  ],
  "traceId": ""
}
```

### 估值 / 资金面最新快照（按板块或行业拿全部成分股的当前 PE/PB/换手率/市值/量比/涨跌幅 等）。<br><br>对应 site internal: &lt;code&gt;POST /stock/api/stock/stockIndicatorListLast&lt;/code&gt;。
**URL:** /openapi/v1/stock/indicator/last

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 估值 / 资金面最新快照（按板块或行业拿全部成分股的当前 PE/PB/换手率/市值/量比/涨跌幅 等）。

<p>对应 site internal: <code>POST /stock/api/stock/stockIndicatorListLast</code>。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|page|int32|false|第几页，从 1 起。默认 1。0 / 负数会被当成 1。|-|
|size|int32|false|每页记录数。默认 50，硬上限 {@value #MAX_SIZE}。<br/><p>传入超过 {@value #MAX_SIZE} 时会被自动截断到 {@value #MAX_SIZE}（不报错）。</p>|-|
|id|int32|false|申万行业分类 ID（与 {@link #level} 配合使用）。<br/><p>由 {@code /openapi/v1/stock/basic/classify} 端点获得。</p>|-|
|name|string|false|分类下的细类名称（可选）。一般不需要填，留 null 即可（id+level 已能唯一确定行业）。|-|
|level|int32|false|申万行业级别：{@code 1}（一级，约 31 个）/ {@code 2}（二级，约 134 个）/ {@code 3}（三级，约 346 个）。|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/stock/indicator/last?page=0&size=0&id=0&level=0&name='
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─tsCode|string|股票代码（带交易所后缀），如 {@code "600519.SH"}。|-|
|└─symbol|string|纯数字股票代码，如 {@code "600519"}。|-|
|└─name|string|股票中文简称，如 {@code "贵州茅台"}。|-|
|└─tradeDate|string|数据所属交易日。|-|
|└─close|number|当日收盘价（元）。|-|
|└─turnoverRate|number|换手率（%）= 当日成交量 / 流通股本 × 100。|-|
|└─turnoverRateF|number|自由流通换手率（%）= 当日成交量 / 自由流通股本 × 100。一般比 {@link #turnoverRate} 更高。|-|
|└─volumeRatio|number|量比 = 当日成交量 / 近 5 日平均成交量。{@code > 1} 表示放量，{@code > 2} 显著放量。|-|
|└─pe|number|静态市盈率：股价 / 上一年度 EPS。|-|
|└─peTtm|number|滚动市盈率：股价 / 最近 4 个季度 EPS（最常用）。|-|
|└─pb|number|市净率：股价 / 每股净资产。|-|
|└─ps|number|静态市销率：股价 / 上一年度 EPS_revenue。|-|
|└─psTtm|number|滚动市销率：股价 / 最近 4 个季度营收（更平滑）。|-|
|└─dvRatio|number|静态股息率（%）= 上一年度每股分红 / 股价 × 100。|-|
|└─dvTtm|number|滚动股息率（%）= 最近 4 个季度每股分红 / 股价 × 100。|-|
|└─totalShare|number|总股本（万股）。|-|
|└─floatShare|number|流通股本（万股）。|-|
|└─freeShare|number|自由流通股本（万股）。剔除限售 / 高管 / 国资等长期不流通部分。|-|
|└─totalMv|number|总市值（万元）= 总股本 × 当日收盘价。|-|
|└─circMv|number|流通市值（万元）= 流通股本 × 当日收盘价。|-|
|└─limitStatus|int8|涨跌停状态。<br/><ul><br/>  <li>{@code 0} —— 普通</li><br/>  <li>{@code 1} —— 涨停</li><br/>  <li>{@code 2} —— 跌停</li><br/>  <li>{@code 3} —— 一字涨停（开盘即涨停）</li><br/>  <li>{@code 4} —— 一字跌停</li><br/></ul><br/><p>具体编码以后端 {@code com.common.enums.LimitStatus} 为准。</p>|-|
|└─roe|number|净资产收益率（%，最近一期）。{@code > 15%} 普遍认为是优秀。|-|
|└─chg|number|涨跌额（元）= close - preClose。|-|
|└─pctChg|number|涨跌幅（%）。|-|
|└─roeDate|string|ROE 数据所属报告期日（季末日期，如 {@code 2026-03-31}）。|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{"code":0,"msg":"","data":[{"tsCode":"","symbol":"","name":"","tradeDate":"yyyy-MM-dd HH:mm:ss","close":0,"turnoverRate":0,"turnoverRateF":0,"volumeRatio":0,"pe":0,"peTtm":0,"pb":0,"ps":0,"psTtm":0,"dvRatio":0,"dvTtm":0,"totalShare":0,"floatShare":0,"freeShare":0,"totalMv":0,"circMv":0,"limitStatus":,"roe":0,"chg":0,"pctChg":0,"roeDate":"yyyy-MM-dd HH:mm:ss"}],"traceId":""}
```

### 估值最新快照（按精确 tsCodes 列表批量查询，最多 100 只）。<br><br>对应 site internal: &lt;code&gt;POST /stock/api/stock/stockIndicatorListLastByTsCodes&lt;/code&gt;。
**URL:** /openapi/v1/stock/indicator/last/by-codes

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 估值最新快照（按精确 tsCodes 列表批量查询，最多 100 只）。

<p>对应 site internal: <code>POST /stock/api/stock/stockIndicatorListLastByTsCodes</code>。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|tsCodes|array|false|股票代码列表（带交易所后缀）。<br/><br/><p><b>示例</b>：</p><br/><pre><br/>["600519.SH", "000858.SZ", "300750.SZ"]<br/></pre><br/><br/><p>建议单次 ≤ 50 个；超出可能被截断。同一只票多次出现会被去重。</p>|-|
|tradeDate|string|false|交易日期，格式 {@code YYYYMMDD}（如 {@code "20260430"}）。<br/><br/><p>可选；不传时取数据库里最新交易日。多数批量查询接口默认就是最新一日，<br/>只在用户明确说"看 X 月 Y 日"时才需要传。</p>|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/stock/indicator/last/by-codes?tsCodes=,&tradeDate='
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─tsCode|string|股票代码（带交易所后缀），如 {@code "600519.SH"}。|-|
|└─symbol|string|纯数字股票代码，如 {@code "600519"}。|-|
|└─name|string|股票中文简称，如 {@code "贵州茅台"}。|-|
|└─tradeDate|string|数据所属交易日。|-|
|└─close|number|当日收盘价（元）。|-|
|└─turnoverRate|number|换手率（%）= 当日成交量 / 流通股本 × 100。|-|
|└─turnoverRateF|number|自由流通换手率（%）= 当日成交量 / 自由流通股本 × 100。一般比 {@link #turnoverRate} 更高。|-|
|└─volumeRatio|number|量比 = 当日成交量 / 近 5 日平均成交量。{@code > 1} 表示放量，{@code > 2} 显著放量。|-|
|└─pe|number|静态市盈率：股价 / 上一年度 EPS。|-|
|└─peTtm|number|滚动市盈率：股价 / 最近 4 个季度 EPS（最常用）。|-|
|└─pb|number|市净率：股价 / 每股净资产。|-|
|└─ps|number|静态市销率：股价 / 上一年度 EPS_revenue。|-|
|└─psTtm|number|滚动市销率：股价 / 最近 4 个季度营收（更平滑）。|-|
|└─dvRatio|number|静态股息率（%）= 上一年度每股分红 / 股价 × 100。|-|
|└─dvTtm|number|滚动股息率（%）= 最近 4 个季度每股分红 / 股价 × 100。|-|
|└─totalShare|number|总股本（万股）。|-|
|└─floatShare|number|流通股本（万股）。|-|
|└─freeShare|number|自由流通股本（万股）。剔除限售 / 高管 / 国资等长期不流通部分。|-|
|└─totalMv|number|总市值（万元）= 总股本 × 当日收盘价。|-|
|└─circMv|number|流通市值（万元）= 流通股本 × 当日收盘价。|-|
|└─limitStatus|int8|涨跌停状态。<br/><ul><br/>  <li>{@code 0} —— 普通</li><br/>  <li>{@code 1} —— 涨停</li><br/>  <li>{@code 2} —— 跌停</li><br/>  <li>{@code 3} —— 一字涨停（开盘即涨停）</li><br/>  <li>{@code 4} —— 一字跌停</li><br/></ul><br/><p>具体编码以后端 {@code com.common.enums.LimitStatus} 为准。</p>|-|
|└─roe|number|净资产收益率（%，最近一期）。{@code > 15%} 普遍认为是优秀。|-|
|└─chg|number|涨跌额（元）= close - preClose。|-|
|└─pctChg|number|涨跌幅（%）。|-|
|└─roeDate|string|ROE 数据所属报告期日（季末日期，如 {@code 2026-03-31}）。|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{"code":0,"msg":"","data":[{"tsCode":"","symbol":"","name":"","tradeDate":"yyyy-MM-dd HH:mm:ss","close":0,"turnoverRate":0,"turnoverRateF":0,"volumeRatio":0,"pe":0,"peTtm":0,"pb":0,"ps":0,"psTtm":0,"dvRatio":0,"dvTtm":0,"totalShare":0,"floatShare":0,"freeShare":0,"totalMv":0,"circMv":0,"limitStatus":,"roe":0,"chg":0,"pctChg":0,"roeDate":"yyyy-MM-dd HH:mm:ss"}],"traceId":""}
```

### 单只股票 ROE 历史时间序列。复用 {@link StockCandlesDailyForm}（仅 tsCode + startDate + endDate 字段生效）。<br><br>对应 site internal: &lt;code&gt;POST /stock/api/stock/stockRoeList&lt;/code&gt;。
**URL:** /openapi/v1/stock/indicator/roe

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 单只股票 ROE 历史时间序列。复用 {@link StockCandlesDailyForm}（仅 tsCode + startDate + endDate 字段生效）。

<p>对应 site internal: <code>POST /stock/api/stock/stockRoeList</code>。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|page|int32|false|第几页，从 1 起。默认 1。0 / 负数会被当成 1。|-|
|size|int32|false|每页记录数。默认 50，硬上限 {@value #MAX_SIZE}。<br/><p>传入超过 {@value #MAX_SIZE} 时会被自动截断到 {@value #MAX_SIZE}（不报错）。</p>|-|
|startDate|string|false|起始日期（含），格式 {@code YYYYMMDD}（如 {@code "20260101"}）。<br/><p>可空。不传时由 page/size 决定窗口（最近 N 个交易日往前）。</p>|-|
|endDate|string|false|结束日期（含），格式 {@code YYYYMMDD}（如 {@code "20260430"}）。<br/><p>可空。不传时取最新交易日。</p>|-|
|type|int32|false|K 线类型枚举值（来自 {@code com.common.enums.StockKLineType}）：<br/><ul><br/>  <li>{@code 11} —— 日 K（默认）</li><br/>  <li>{@code 12} —— 周 K</li><br/>  <li>{@code 13} —— 月 K</li><br/></ul><br/><br/><p>带默认值 {@code 11}（日 K）：调用方不传时按日 K 处理。<br/>历史缺陷：此前无默认值，不传 type 时反序列化为 0，服务层查表 miss 静默返回空列表<br/>且被 @Cacheable 缓存，调用方误判"无数据"。</p>|-|
|tsCode|string|false|股票代码（带交易所后缀），如 {@code "600519.SH"} / {@code "000001.SZ"}。<b>必填</b>。|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/stock/indicator/roe?page=0&size=0&type=0&endDate=&startDate=&tsCode='
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─period|string|季度标识：{@code "Q1"} / {@code "Q2"} / {@code "Q3"} / {@code "Q4"}。<br/><p>例如 {@code "Q3"} 表示三季报。</p>|-|
|└─roe|number|净资产收益率（%，单期口径）。例如 {@code 12.34} 表示 12.34%。<br/><p>注：报告期内的 ROE 一般用累计口径（YTD），单季度可由相邻报告期相减得到。</p>|-|
|└─endDate|string|报告期截止日期（季末日期，如 {@code 2026-03-31} / {@code 2026-06-30}）。|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "period": "",
      "roe": 0,
      "endDate": "yyyy-MM-dd HH:mm:ss"
    }
  ],
  "traceId": ""
}
```

### 指数因子（专业版）—— 88 列宽表（OHLCV + 88 个技术指标，全部 BFQ 不复权）。<br><br>对应 PG 表 {@code stock_idx_factor_pro}，含 MA/EMA/BOLL/KTN/TAQ 通道 +<br>MACD/KDJ/RSI/BIAS/CCI/WR/BRAR/CR 振荡 + DMI/ASI/ATR/TRIX/DPO/MASS 趋势 +<br>OBV/VR/MFI/MTM/ROC/EMV 量能 + PSY 心理 + XSII 薛斯通道 + updays/downdays/lowdays/topdays。 <br><br>用途：指数级技术分析、量化因子回测。tsCode 必填（指数代码，如 {@code 000001.SH}）。 
**URL:** /openapi/v1/stock/indicator/idx-factor-pro

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 指数因子（专业版）—— 88 列宽表（OHLCV + 88 个技术指标，全部 BFQ 不复权）。

<p>对应 PG 表 {@code stock_idx_factor_pro}，含 MA/EMA/BOLL/KTN/TAQ 通道 +
MACD/KDJ/RSI/BIAS/CCI/WR/BRAR/CR 振荡 + DMI/ASI/ATR/TRIX/DPO/MASS 趋势 +
OBV/VR/MFI/MTM/ROC/EMV 量能 + PSY 心理 + XSII 薛斯通道 + updays/downdays/lowdays/topdays。</p>

<p>用途：指数级技术分析、量化因子回测。tsCode 必填（指数代码，如 {@code 000001.SH}）。</p>

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|page|int32|false|第几页，从 1 起。默认 1。0 / 负数会被当成 1。|-|
|size|int32|false|每页记录数。默认 50，硬上限 {@value #MAX_SIZE}。<br/><p>传入超过 {@value #MAX_SIZE} 时会被自动截断到 {@value #MAX_SIZE}（不报错）。</p>|-|
|tsCode|string|false|指数 TS 代码（必填，如 {@code "000001.SH"}）|-|
|startDate|string|false|起始日期，{@code YYYYMMDD}。可空。|-|
|endDate|string|false|结束日期，{@code YYYYMMDD}。可空。|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/stock/indicator/idx-factor-pro?page=0&size=0&tsCode=&endDate=&startDate='
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─tradeDate|string|交易日|-|
|└─tsCode|string|TS 指数代码|-|
|└─open|number|No comments found.|-|
|└─high|number|No comments found.|-|
|└─low|number|No comments found.|-|
|└─close|number|No comments found.|-|
|└─preClose|number|No comments found.|-|
|└─change|number|No comments found.|-|
|└─pctChange|number|No comments found.|-|
|└─vol|number|No comments found.|-|
|└─amount|number|No comments found.|-|
|└─asiBfq|number|No comments found.|-|
|└─asitBfq|number|No comments found.|-|
|└─atrBfq|number|No comments found.|-|
|└─bbiBfq|number|No comments found.|-|
|└─bias1Bfq|number|No comments found.|-|
|└─bias2Bfq|number|No comments found.|-|
|└─bias3Bfq|number|No comments found.|-|
|└─bollUpperBfq|number|No comments found.|-|
|└─bollMidBfq|number|No comments found.|-|
|└─bollLowerBfq|number|No comments found.|-|
|└─brarArBfq|number|No comments found.|-|
|└─brarBrBfq|number|No comments found.|-|
|└─cciBfq|number|No comments found.|-|
|└─crBfq|number|No comments found.|-|
|└─dfmaDifBfq|number|No comments found.|-|
|└─dfmaDifmaBfq|number|No comments found.|-|
|└─dmiPdiBfq|number|No comments found.|-|
|└─dmiMdiBfq|number|No comments found.|-|
|└─dmiAdxBfq|number|No comments found.|-|
|└─dmiAdxrBfq|number|No comments found.|-|
|└─downdays|number|No comments found.|-|
|└─updays|number|No comments found.|-|
|└─dpoBfq|number|No comments found.|-|
|└─madpoBfq|number|No comments found.|-|
|└─emaBfq5|number|No comments found.|-|
|└─emaBfq10|number|No comments found.|-|
|└─emaBfq20|number|No comments found.|-|
|└─emaBfq30|number|No comments found.|-|
|└─emaBfq60|number|No comments found.|-|
|└─emaBfq90|number|No comments found.|-|
|└─emaBfq250|number|No comments found.|-|
|└─emvBfq|number|No comments found.|-|
|└─maemvBfq|number|No comments found.|-|
|└─expma12Bfq|number|No comments found.|-|
|└─expma50Bfq|number|No comments found.|-|
|└─kdjBfq|number|No comments found.|-|
|└─kdjKBfq|number|No comments found.|-|
|└─kdjDBfq|number|No comments found.|-|
|└─ktnUpperBfq|number|No comments found.|-|
|└─ktnMidBfq|number|No comments found.|-|
|└─ktnDownBfq|number|No comments found.|-|
|└─lowdays|number|No comments found.|-|
|└─topdays|number|No comments found.|-|
|└─maBfq5|number|No comments found.|-|
|└─maBfq10|number|No comments found.|-|
|└─maBfq20|number|No comments found.|-|
|└─maBfq30|number|No comments found.|-|
|└─maBfq60|number|No comments found.|-|
|└─maBfq90|number|No comments found.|-|
|└─maBfq250|number|No comments found.|-|
|└─macdBfq|number|No comments found.|-|
|└─macdDifBfq|number|No comments found.|-|
|└─macdDeaBfq|number|No comments found.|-|
|└─massBfq|number|No comments found.|-|
|└─maMassBfq|number|No comments found.|-|
|└─mfiBfq|number|No comments found.|-|
|└─mtmBfq|number|No comments found.|-|
|└─mtmmaBfq|number|No comments found.|-|
|└─obvBfq|number|No comments found.|-|
|└─psyBfq|number|No comments found.|-|
|└─psymaBfq|number|No comments found.|-|
|└─rocBfq|number|No comments found.|-|
|└─marocBfq|number|No comments found.|-|
|└─rsiBfq6|number|No comments found.|-|
|└─rsiBfq12|number|No comments found.|-|
|└─rsiBfq24|number|No comments found.|-|
|└─taqUpBfq|number|No comments found.|-|
|└─taqMidBfq|number|No comments found.|-|
|└─taqDownBfq|number|No comments found.|-|
|└─trixBfq|number|No comments found.|-|
|└─trmaBfq|number|No comments found.|-|
|└─vrBfq|number|No comments found.|-|
|└─wrBfq|number|No comments found.|-|
|└─wr1Bfq|number|No comments found.|-|
|└─xsiiTd1Bfq|number|No comments found.|-|
|└─xsiiTd2Bfq|number|No comments found.|-|
|└─xsiiTd3Bfq|number|No comments found.|-|
|└─xsiiTd4Bfq|number|No comments found.|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "tradeDate": "yyyy-MM-dd HH:mm:ss",
      "tsCode": "",
      "open": 0,
      "high": 0,
      "low": 0,
      "close": 0,
      "preClose": 0,
      "change": 0,
      "pctChange": 0,
      "vol": 0,
      "amount": 0,
      "asiBfq": 0,
      "asitBfq": 0,
      "atrBfq": 0,
      "bbiBfq": 0,
      "bias1Bfq": 0,
      "bias2Bfq": 0,
      "bias3Bfq": 0,
      "bollUpperBfq": 0,
      "bollMidBfq": 0,
      "bollLowerBfq": 0,
      "brarArBfq": 0,
      "brarBrBfq": 0,
      "cciBfq": 0,
      "crBfq": 0,
      "dfmaDifBfq": 0,
      "dfmaDifmaBfq": 0,
      "dmiPdiBfq": 0,
      "dmiMdiBfq": 0,
      "dmiAdxBfq": 0,
      "dmiAdxrBfq": 0,
      "downdays": 0,
      "updays": 0,
      "dpoBfq": 0,
      "madpoBfq": 0,
      "emaBfq5": 0,
      "emaBfq10": 0,
      "emaBfq20": 0,
      "emaBfq30": 0,
      "emaBfq60": 0,
      "emaBfq90": 0,
      "emaBfq250": 0,
      "emvBfq": 0,
      "maemvBfq": 0,
      "expma12Bfq": 0,
      "expma50Bfq": 0,
      "kdjBfq": 0,
      "kdjKBfq": 0,
      "kdjDBfq": 0,
      "ktnUpperBfq": 0,
      "ktnMidBfq": 0,
      "ktnDownBfq": 0,
      "lowdays": 0,
      "topdays": 0,
      "maBfq5": 0,
      "maBfq10": 0,
      "maBfq20": 0,
      "maBfq30": 0,
      "maBfq60": 0,
      "maBfq90": 0,
      "maBfq250": 0,
      "macdBfq": 0,
      "macdDifBfq": 0,
      "macdDeaBfq": 0,
      "massBfq": 0,
      "maMassBfq": 0,
      "mfiBfq": 0,
      "mtmBfq": 0,
      "mtmmaBfq": 0,
      "obvBfq": 0,
      "psyBfq": 0,
      "psymaBfq": 0,
      "rocBfq": 0,
      "marocBfq": 0,
      "rsiBfq6": 0,
      "rsiBfq12": 0,
      "rsiBfq24": 0,
      "taqUpBfq": 0,
      "taqMidBfq": 0,
      "taqDownBfq": 0,
      "trixBfq": 0,
      "trmaBfq": 0,
      "vrBfq": 0,
      "wrBfq": 0,
      "wr1Bfq": 0,
      "xsiiTd1Bfq": 0,
      "xsiiTd2Bfq": 0,
      "xsiiTd3Bfq": 0,
      "xsiiTd4Bfq": 0
    }
  ],
  "traceId": ""
}
```

## OpenAPI v1 —— 市场上下文（新闻 + 宏观）端点。

&lt;p&gt;2026-06 拆分 scope（与 claw-server 套餐对齐）：
&lt;ul&gt;
  &lt;li&gt;&lt;b&gt;宏观&lt;/b&gt; &lt;code&gt;/macro/*&lt;/code&gt; → &lt;code&gt;@OpenApiScope(&quot;market&quot;)&lt;/code&gt;，归 &lt;b&gt;pro&lt;/b&gt;（↔ claw LOW）。
      含 CPI/PPI/PMI/GDP/货币供应/社融/Shibor/LPR/月度综合 + 经济事件日历 + 政策档案。&lt;/li&gt;
  &lt;li&gt;&lt;b&gt;新闻&lt;/b&gt; &lt;code&gt;/news/*&lt;/code&gt; → &lt;code&gt;@OpenApiScope(&quot;news&quot;)&lt;/code&gt;，归 &lt;b&gt;max&lt;/b&gt;（↔ claw HIGH）。
      实时新闻/资讯作为高级档差异化卖点。&lt;/li&gt;
&lt;/ul&gt;
### 新闻列表（按类型 / 关键字 / 时间范围筛选）。
**URL:** /openapi/v1/market/news/list

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 新闻列表（按类型 / 关键字 / 时间范围筛选）。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|page|int32|false|第几页，从 1 起。默认 1。0 / 负数会被当成 1。|-|
|size|int32|false|每页记录数。默认 50，硬上限 {@value #MAX_SIZE}。<br/><p>传入超过 {@value #MAX_SIZE} 时会被自动截断到 {@value #MAX_SIZE}（不报错）。</p>|-|
|type|int32|false|新闻类型 ID（整数）。<br/><p>具体 type 字典见 {@code POST /openapi/v1/market/news/types} 端点返回结果。</p>|-|
|titleKeyword|string|false|标题模糊匹配关键字（中文）。<br/><p>例如 {@code "降息"} / {@code "宁德时代"} / {@code "关税"}。</p>|-|
|startDate|string|false|起始时间，格式 {@code YYYYMMDD}（如 {@code "20260424"}）。按 news_time 过滤。|-|
|endDate|string|false|结束时间，格式 {@code YYYYMMDD}。|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/market/news/list?page=0&size=0&type=0&endDate=&titleKeyword=&startDate='
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─id|int64|No comments found.|-|
|└─newsTimeStr|string|新闻时间（字符串原文，便于直接展示）|-|
|└─newsTime|string|新闻时间（带时区，便于排序 / 算时间差）|-|
|└─title|string|No comments found.|-|
|└─channels|string|频道（CSV，多个用逗号分隔）|-|
|└─score|string|评分|-|
|└─src|string|来源|-|
|└─type|int32|类型|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "id": 0,
      "newsTimeStr": "",
      "newsTime": "yyyy-MM-dd HH:mm:ss",
      "title": "",
      "channels": "",
      "score": "",
      "src": "",
      "type": 0
    }
  ],
  "traceId": ""
}
```

### CPI 居民消费价格指数（月度，YYYYMM 字符串）。返回全国/城市/农村三套数据。
**URL:** /openapi/v1/market/macro/cpi

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** CPI 居民消费价格指数（月度，YYYYMM 字符串）。返回全国/城市/农村三套数据。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|page|int32|false|第几页，从 1 起。默认 1。0 / 负数会被当成 1。|-|
|size|int32|false|每页记录数。默认 50，硬上限 {@value #MAX_SIZE}。<br/><p>传入超过 {@value #MAX_SIZE} 时会被自动截断到 {@value #MAX_SIZE}（不报错）。</p>|-|
|startDate|string|false|起始时间。格式因端点而异：<br/><ul><br/>  <li>月度端点：{@code YYYYMM}（如 {@code "202601"}）</li><br/>  <li>季度端点：{@code YYYYQX}（如 {@code "2026Q1"}）</li><br/>  <li>日度端点：{@code YYYYMMDD}（如 {@code "20260101"}）</li><br/></ul><br/>可空，不传时取最近一段数据。|-|
|endDate|string|false|结束时间。格式同 {@link #startDate}，可空。|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/market/macro/cpi?page=0&size=0&endDate=&startDate='
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─month|string|月份，格式 {@code YYYYMM}。|-|
|└─ntVal|number|⭐ 全国 CPI 指数（基期 = 100）。|-|
|└─ntYoy|number|⭐ 全国 CPI 同比涨幅（%）。{@code > 0} 通胀，{@code < 0} 通缩。最常关注的口径。|-|
|└─ntMom|number|全国 CPI 环比涨幅（%）。|-|
|└─ntAccu|number|全国 CPI 累计同比涨幅（%，年内累计）。|-|
|└─townVal|number|城市 CPI 指数。|-|
|└─townYoy|number|城市 CPI 同比涨幅（%）。|-|
|└─townMom|number|城市 CPI 环比涨幅（%）。|-|
|└─townAccu|number|城市 CPI 累计同比涨幅（%）。|-|
|└─cntVal|number|农村 CPI 指数。|-|
|└─cntYoy|number|农村 CPI 同比涨幅（%）。|-|
|└─cntMom|number|农村 CPI 环比涨幅（%）。|-|
|└─cntAccu|number|农村 CPI 累计同比涨幅（%）。|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "month": "",
      "ntVal": 0,
      "ntYoy": 0,
      "ntMom": 0,
      "ntAccu": 0,
      "townVal": 0,
      "townYoy": 0,
      "townMom": 0,
      "townAccu": 0,
      "cntVal": 0,
      "cntYoy": 0,
      "cntMom": 0,
      "cntAccu": 0
    }
  ],
  "traceId": ""
}
```

### PPI 工业生产者出厂价格指数（月度）。含生产资料 / 生活资料细分。
**URL:** /openapi/v1/market/macro/ppi

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** PPI 工业生产者出厂价格指数（月度）。含生产资料 / 生活资料细分。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|page|int32|false|第几页，从 1 起。默认 1。0 / 负数会被当成 1。|-|
|size|int32|false|每页记录数。默认 50，硬上限 {@value #MAX_SIZE}。<br/><p>传入超过 {@value #MAX_SIZE} 时会被自动截断到 {@value #MAX_SIZE}（不报错）。</p>|-|
|startDate|string|false|起始时间。格式因端点而异：<br/><ul><br/>  <li>月度端点：{@code YYYYMM}（如 {@code "202601"}）</li><br/>  <li>季度端点：{@code YYYYQX}（如 {@code "2026Q1"}）</li><br/>  <li>日度端点：{@code YYYYMMDD}（如 {@code "20260101"}）</li><br/></ul><br/>可空，不传时取最近一段数据。|-|
|endDate|string|false|结束时间。格式同 {@link #startDate}，可空。|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/market/macro/ppi?page=0&size=0&endDate=&startDate='
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─month|string|月份 YYYYMM|-|
|└─ppiYoy|number|PPI 总指数同比（%）|-|
|└─ppiMom|number|PPI 总指数环比（%）|-|
|└─ppiAccu|number|PPI 总指数累计同比（%）|-|
|└─ppiMpYoy|number|生产资料同比|-|
|└─ppiMpQmYoy|number|生产资料采掘业同比|-|
|└─ppiMpRmYoy|number|生产资料原材料同比|-|
|└─ppiMpPYoy|number|生产资料加工业同比|-|
|└─ppiCgYoy|number|生活资料同比|-|
|└─ppiCgFYoy|number|生活资料食品同比|-|
|└─ppiCgCYoy|number|生活资料衣着同比|-|
|└─ppiCgAduYoy|number|生活资料一般日用品同比|-|
|└─ppiCgDcgYoy|number|生活资料耐用消费品同比|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "month": "",
      "ppiYoy": 0,
      "ppiMom": 0,
      "ppiAccu": 0,
      "ppiMpYoy": 0,
      "ppiMpQmYoy": 0,
      "ppiMpRmYoy": 0,
      "ppiMpPYoy": 0,
      "ppiCgYoy": 0,
      "ppiCgFYoy": 0,
      "ppiCgCYoy": 0,
      "ppiCgAduYoy": 0,
      "ppiCgDcgYoy": 0
    }
  ],
  "traceId": ""
}
```

### PMI 采购经理指数（月度，35 列细分）。<br>核心字段：pmi010000（制造业）/ pmi020100（非制造业商务活动）/ pmi030000（综合 PMI）。
**URL:** /openapi/v1/market/macro/pmi

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** PMI 采购经理指数（月度，35 列细分）。
核心字段：pmi010000（制造业）/ pmi020100（非制造业商务活动）/ pmi030000（综合 PMI）。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|page|int32|false|第几页，从 1 起。默认 1。0 / 负数会被当成 1。|-|
|size|int32|false|每页记录数。默认 50，硬上限 {@value #MAX_SIZE}。<br/><p>传入超过 {@value #MAX_SIZE} 时会被自动截断到 {@value #MAX_SIZE}（不报错）。</p>|-|
|startDate|string|false|起始时间。格式因端点而异：<br/><ul><br/>  <li>月度端点：{@code YYYYMM}（如 {@code "202601"}）</li><br/>  <li>季度端点：{@code YYYYQX}（如 {@code "2026Q1"}）</li><br/>  <li>日度端点：{@code YYYYMMDD}（如 {@code "20260101"}）</li><br/></ul><br/>可空，不传时取最近一段数据。|-|
|endDate|string|false|结束时间。格式同 {@link #startDate}，可空。|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/market/macro/pmi?page=0&size=0&startDate=&endDate='
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─month|string|月份，格式 {@code YYYYMM}（如 {@code "202604"}）。|-|
|└─pmi010000|number|⭐ 制造业 PMI 总指数。{@code > 50} 扩张，{@code < 50} 收缩——景气度核心指标。|-|
|└─pmi010100|number|⭐ 制造业生产指数。|-|
|└─pmi010200|number|⭐ 制造业新订单指数。前瞻意义最强。|-|
|└─pmi010300|number|⭐ 制造业新出口订单指数。反映外需。|-|
|└─pmi010400|number|制造业在手订单指数。|-|
|└─pmi010401|number|在手订单 — 大型企业。|-|
|└─pmi010402|number|在手订单 — 中型企业。|-|
|└─pmi010403|number|在手订单 — 小型企业。|-|
|└─pmi010500|number|制造业产成品库存指数。|-|
|└─pmi010501|number|主要原材料购进价格。|-|
|└─pmi010502|number|出厂价格。|-|
|└─pmi010503|number|主要原材料库存。|-|
|└─pmi010504|number|从业人员指数。|-|
|└─pmi010505|number|供应商配送时间指数。|-|
|└─pmi010506|number|生产经营活动预期指数。|-|
|└─pmi010507|number|采购量指数。|-|
|└─pmi020100|number|⭐ 非制造业商务活动指数。{@code > 50} 服务业 + 建筑业扩张。|-|
|└─pmi020101|number|非制造业 — 服务业。|-|
|└─pmi020102|number|非制造业 — 建筑业。|-|
|└─pmi020200|number|⭐ 非制造业新订单指数。|-|
|└─pmi020201|number|非制造业新订单 — 服务业。|-|
|└─pmi020202|number|非制造业新订单 — 建筑业。|-|
|└─pmi020300|number|非制造业投入品价格指数。|-|
|└─pmi020301|number|非制造业投入品价格 — 服务业。|-|
|└─pmi020302|number|非制造业投入品价格 — 建筑业。|-|
|└─pmi020400|number|非制造业销售价格指数。|-|
|└─pmi020401|number|销售价格 — 服务业。|-|
|└─pmi020402|number|销售价格 — 建筑业。|-|
|└─pmi020500|number|非制造业从业人员指数。|-|
|└─pmi020501|number|从业人员 — 服务业。|-|
|└─pmi020502|number|从业人员 — 建筑业。|-|
|└─pmi020600|number|非制造业业务活动预期指数。|-|
|└─pmi020601|number|业务活动预期 — 服务业。|-|
|└─pmi020602|number|业务活动预期 — 建筑业。|-|
|└─pmi030000|number|⭐ 综合 PMI 产出指数 = 制造业生产 + 非制造业商务活动加权。整体经济景气度。|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "month": "",
      "pmi010000": 0,
      "pmi010100": 0,
      "pmi010200": 0,
      "pmi010300": 0,
      "pmi010400": 0,
      "pmi010401": 0,
      "pmi010402": 0,
      "pmi010403": 0,
      "pmi010500": 0,
      "pmi010501": 0,
      "pmi010502": 0,
      "pmi010503": 0,
      "pmi010504": 0,
      "pmi010505": 0,
      "pmi010506": 0,
      "pmi010507": 0,
      "pmi020100": 0,
      "pmi020101": 0,
      "pmi020102": 0,
      "pmi020200": 0,
      "pmi020201": 0,
      "pmi020202": 0,
      "pmi020300": 0,
      "pmi020301": 0,
      "pmi020302": 0,
      "pmi020400": 0,
      "pmi020401": 0,
      "pmi020402": 0,
      "pmi020500": 0,
      "pmi020501": 0,
      "pmi020502": 0,
      "pmi020600": 0,
      "pmi020601": 0,
      "pmi020602": 0,
      "pmi030000": 0
    }
  ],
  "traceId": ""
}
```

### GDP 国内生产总值（季度，YYYYQX 字符串如 2024Q1）。含三产业划分。
**URL:** /openapi/v1/market/macro/gdp

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** GDP 国内生产总值（季度，YYYYQX 字符串如 2024Q1）。含三产业划分。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|page|int32|false|第几页，从 1 起。默认 1。0 / 负数会被当成 1。|-|
|size|int32|false|每页记录数。默认 50，硬上限 {@value #MAX_SIZE}。<br/><p>传入超过 {@value #MAX_SIZE} 时会被自动截断到 {@value #MAX_SIZE}（不报错）。</p>|-|
|startDate|string|false|起始时间。格式因端点而异：<br/><ul><br/>  <li>月度端点：{@code YYYYMM}（如 {@code "202601"}）</li><br/>  <li>季度端点：{@code YYYYQX}（如 {@code "2026Q1"}）</li><br/>  <li>日度端点：{@code YYYYMMDD}（如 {@code "20260101"}）</li><br/></ul><br/>可空，不传时取最近一段数据。|-|
|endDate|string|false|结束时间。格式同 {@link #startDate}，可空。|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/market/macro/gdp?page=0&size=0&startDate=&endDate='
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─quarter|string|季度（如 2024Q1）|-|
|└─gdp|number|GDP 总额（亿元）|-|
|└─gdpYoy|number|GDP 同比增速（%）|-|
|└─pi|number|第一产业（亿元）|-|
|└─piYoy|number|No comments found.|-|
|└─si|number|第二产业（亿元）|-|
|└─siYoy|number|No comments found.|-|
|└─ti|number|第三产业（亿元）|-|
|└─tiYoy|number|No comments found.|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "quarter": "",
      "gdp": 0,
      "gdpYoy": 0,
      "pi": 0,
      "piYoy": 0,
      "si": 0,
      "siYoy": 0,
      "ti": 0,
      "tiYoy": 0
    }
  ],
  "traceId": ""
}
```

### M0/M1/M2 货币供应量（月度）。含同比 / 环比。
**URL:** /openapi/v1/market/macro/money-supply

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** M0/M1/M2 货币供应量（月度）。含同比 / 环比。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|page|int32|false|第几页，从 1 起。默认 1。0 / 负数会被当成 1。|-|
|size|int32|false|每页记录数。默认 50，硬上限 {@value #MAX_SIZE}。<br/><p>传入超过 {@value #MAX_SIZE} 时会被自动截断到 {@value #MAX_SIZE}（不报错）。</p>|-|
|startDate|string|false|起始时间。格式因端点而异：<br/><ul><br/>  <li>月度端点：{@code YYYYMM}（如 {@code "202601"}）</li><br/>  <li>季度端点：{@code YYYYQX}（如 {@code "2026Q1"}）</li><br/>  <li>日度端点：{@code YYYYMMDD}（如 {@code "20260101"}）</li><br/></ul><br/>可空，不传时取最近一段数据。|-|
|endDate|string|false|结束时间。格式同 {@link #startDate}，可空。|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/market/macro/money-supply?page=0&size=0&endDate=&startDate='
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─month|string|月份 YYYYMM|-|
|└─m0|number|M0 流通中现金（亿元）|-|
|└─m0Yoy|number|No comments found.|-|
|└─m0Mom|number|No comments found.|-|
|└─m1|number|M1 狭义货币（亿元）= M0 + 单位活期存款|-|
|└─m1Yoy|number|No comments found.|-|
|└─m1Mom|number|No comments found.|-|
|└─m2|number|M2 广义货币（亿元）= M1 + 单位定期存款 + 居民储蓄 + 其他|-|
|└─m2Yoy|number|No comments found.|-|
|└─m2Mom|number|No comments found.|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "month": "",
      "m0": 0,
      "m0Yoy": 0,
      "m0Mom": 0,
      "m1": 0,
      "m1Yoy": 0,
      "m1Mom": 0,
      "m2": 0,
      "m2Yoy": 0,
      "m2Mom": 0
    }
  ],
  "traceId": ""
}
```

### 社会融资规模增量（月度）。
**URL:** /openapi/v1/market/macro/social-finance

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 社会融资规模增量（月度）。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|page|int32|false|第几页，从 1 起。默认 1。0 / 负数会被当成 1。|-|
|size|int32|false|每页记录数。默认 50，硬上限 {@value #MAX_SIZE}。<br/><p>传入超过 {@value #MAX_SIZE} 时会被自动截断到 {@value #MAX_SIZE}（不报错）。</p>|-|
|startDate|string|false|起始时间。格式因端点而异：<br/><ul><br/>  <li>月度端点：{@code YYYYMM}（如 {@code "202601"}）</li><br/>  <li>季度端点：{@code YYYYQX}（如 {@code "2026Q1"}）</li><br/>  <li>日度端点：{@code YYYYMMDD}（如 {@code "20260101"}）</li><br/></ul><br/>可空，不传时取最近一段数据。|-|
|endDate|string|false|结束时间。格式同 {@link #startDate}，可空。|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/market/macro/social-finance?page=0&size=0&startDate=&endDate='
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─month|string|月份 YYYYMM|-|
|└─incMonth|number|当月社融增量（亿元）|-|
|└─incCumval|number|累计值（亿元，年内累计）|-|
|└─rmbLoan|number|人民币贷款|-|
|└─fxLoan|number|外币贷款|-|
|└─entTrust|number|委托贷款（企业贷款）|-|
|└─entBill|number|银行承兑汇票|-|
|└─unbFinance|number|未贴现的银行承兑汇票|-|
|└─corpBond|number|企业债券|-|
|└─nonFinStock|number|非金融企业境内股票融资|-|
|└─govBond|number|政府债券|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "month": "",
      "incMonth": 0,
      "incCumval": 0,
      "rmbLoan": 0,
      "fxLoan": 0,
      "entTrust": 0,
      "entBill": 0,
      "unbFinance": 0,
      "corpBond": 0,
      "nonFinStock": 0,
      "govBond": 0
    }
  ],
  "traceId": ""
}
```

### Shibor 上海银行间同业拆放利率（日度，YYYYMMDD 字符串）。9 个期限。
**URL:** /openapi/v1/market/macro/shibor

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** Shibor 上海银行间同业拆放利率（日度，YYYYMMDD 字符串）。9 个期限。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|page|int32|false|第几页，从 1 起。默认 1。0 / 负数会被当成 1。|-|
|size|int32|false|每页记录数。默认 50，硬上限 {@value #MAX_SIZE}。<br/><p>传入超过 {@value #MAX_SIZE} 时会被自动截断到 {@value #MAX_SIZE}（不报错）。</p>|-|
|startDate|string|false|起始时间。格式因端点而异：<br/><ul><br/>  <li>月度端点：{@code YYYYMM}（如 {@code "202601"}）</li><br/>  <li>季度端点：{@code YYYYQX}（如 {@code "2026Q1"}）</li><br/>  <li>日度端点：{@code YYYYMMDD}（如 {@code "20260101"}）</li><br/></ul><br/>可空，不传时取最近一段数据。|-|
|endDate|string|false|结束时间。格式同 {@link #startDate}，可空。|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/market/macro/shibor?page=0&size=0&endDate=&startDate='
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─date|string|日期 YYYYMMDD|-|
|└─onRate|number|隔夜 (Overnight)|-|
|└─w1|number|1 周|-|
|└─w2|number|2 周|-|
|└─m1|number|1 月|-|
|└─m3|number|3 月|-|
|└─m6|number|6 月|-|
|└─m9|number|9 月|-|
|└─y1|number|1 年|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "date": "",
      "onRate": 0,
      "w1": 0,
      "w2": 0,
      "m1": 0,
      "m3": 0,
      "m6": 0,
      "m9": 0,
      "y1": 0
    }
  ],
  "traceId": ""
}
```

### LPR 贷款基础利率（每月公布，YYYYMMDD 字符串）。1 年 / 5 年期。
**URL:** /openapi/v1/market/macro/lpr

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** LPR 贷款基础利率（每月公布，YYYYMMDD 字符串）。1 年 / 5 年期。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|page|int32|false|第几页，从 1 起。默认 1。0 / 负数会被当成 1。|-|
|size|int32|false|每页记录数。默认 50，硬上限 {@value #MAX_SIZE}。<br/><p>传入超过 {@value #MAX_SIZE} 时会被自动截断到 {@value #MAX_SIZE}（不报错）。</p>|-|
|startDate|string|false|起始时间。格式因端点而异：<br/><ul><br/>  <li>月度端点：{@code YYYYMM}（如 {@code "202601"}）</li><br/>  <li>季度端点：{@code YYYYQX}（如 {@code "2026Q1"}）</li><br/>  <li>日度端点：{@code YYYYMMDD}（如 {@code "20260101"}）</li><br/></ul><br/>可空，不传时取最近一段数据。|-|
|endDate|string|false|结束时间。格式同 {@link #startDate}，可空。|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/market/macro/lpr?page=0&size=0&endDate=&startDate='
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─date|string|公布日期 YYYYMMDD|-|
|└─y1|number|1 年期 LPR（%）|-|
|└─y5|number|5 年期 LPR（%）|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "date": "",
      "y1": 0,
      "y5": 0
    }
  ],
  "traceId": ""
}
```

### 宏观月度综合（CPI/PPI/PMI/M2/LPR/社融拼一行）。startDate/endDate 用 YYYYMM。<br>一次拿全宏观面用此端点；分项更细的单表查询请用 /macro/{cpi,ppi,...}。
**URL:** /openapi/v1/market/macro/monthly

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 宏观月度综合（CPI/PPI/PMI/M2/LPR/社融拼一行）。startDate/endDate 用 YYYYMM。
一次拿全宏观面用此端点；分项更细的单表查询请用 /macro/{cpi,ppi,...}。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|page|int32|false|第几页，从 1 起。默认 1。0 / 负数会被当成 1。|-|
|size|int32|false|每页记录数。默认 50，硬上限 {@value #MAX_SIZE}。<br/><p>传入超过 {@value #MAX_SIZE} 时会被自动截断到 {@value #MAX_SIZE}（不报错）。</p>|-|
|startDate|string|false|起始时间。格式因端点而异：<br/><ul><br/>  <li>月度端点：{@code YYYYMM}（如 {@code "202601"}）</li><br/>  <li>季度端点：{@code YYYYQX}（如 {@code "2026Q1"}）</li><br/>  <li>日度端点：{@code YYYYMMDD}（如 {@code "20260101"}）</li><br/></ul><br/>可空，不传时取最近一段数据。|-|
|endDate|string|false|结束时间。格式同 {@link #startDate}，可空。|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/market/macro/monthly?page=0&size=0&startDate=&endDate='
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─month|string|YYYYMM|-|
|└─cpiYoy|number|CPI 同比（%）|-|
|└─ppiYoy|number|PPI 同比（%）|-|
|└─pmi|number|制造业 PMI|-|
|└─pmiNonMfg|number|非制造业 PMI|-|
|└─m2Yoy|number|M2 同比（%）|-|
|└─socialFinance|number|社会融资增量（亿元）|-|
|└─lpr1y|number|1 年期 LPR（%）|-|
|└─lpr5y|number|5 年期 LPR（%）|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "month": "",
      "cpiYoy": 0,
      "ppiYoy": 0,
      "pmi": 0,
      "pmiNonMfg": 0,
      "m2Yoy": 0,
      "socialFinance": 0,
      "lpr1y": 0,
      "lpr5y": 0
    }
  ],
  "traceId": ""
}
```

### 新闻类型字典（type → name）。<br><br>对应 site internal: &lt;code&gt;POST /stock/api/news/types&lt;/code&gt;。<br>阶段 11 迁到 OpenAPI；返回 {@link NewsSourceEnum#getAll()} 的列表。<br>用此结果的 type 值填充 {@code /openapi/v1/market/news/list} 的 type 字段。
**URL:** /openapi/v1/market/news/types

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 新闻类型字典（type → name）。

<p>对应 site internal: <code>POST /stock/api/news/types</code>。
阶段 11 迁到 OpenAPI；返回 {@link NewsSourceEnum#getAll()} 的列表。
用此结果的 type 值填充 {@code /openapi/v1/market/news/list} 的 type 字段。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/market/news/types'
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─mapKey|string|A map key.|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "mapKey1": "",
      "mapKey2": ""
    }
  ],
  "traceId": ""
}
```

### 全球财经事件日历（{@code macro_eco_cal}）。<br><br>可按 country / currency / keyword（event 模糊） / 日期范围（YYYYMMDD）过滤。<br>含全球宏观经济关键数据公布预告 + 实际值 + 前值 + 预期值（字符串可能含 % / B / M 等单位后缀）。 
**URL:** /openapi/v1/market/macro/eco-cal

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 全球财经事件日历（{@code macro_eco_cal}）。

<p>可按 country / currency / keyword（event 模糊） / 日期范围（YYYYMMDD）过滤。
含全球宏观经济关键数据公布预告 + 实际值 + 前值 + 预期值（字符串可能含 % / B / M 等单位后缀）。</p>

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|page|int32|false|第几页，从 1 起。默认 1。0 / 负数会被当成 1。|-|
|size|int32|false|每页记录数。默认 50，硬上限 {@value #MAX_SIZE}。<br/><p>传入超过 {@value #MAX_SIZE} 时会被自动截断到 {@value #MAX_SIZE}（不报错）。</p>|-|
|keyword|string|false|通用关键字（按表内最关键文本列模糊匹配，参类级注释）。|-|
|year|int32|false|年度（fund-sales-ratio / fund-sales-vol 用）。|-|
|startYear|int32|false|起始年度（fund-sales-ratio 区间）。|-|
|endYear|int32|false|结束年度（fund-sales-ratio 区间）。|-|
|quarter|string|false|季度（fund-sales-vol，如 "1"/"2"/"3"/"4" 或 "Q1"/...）。|-|
|startDate|string|false|起始日期 {@code YYYYMMDD}。|-|
|endDate|string|false|结束日期 {@code YYYYMMDD}。|-|
|country|string|false|国家代码（eco-cal）。|-|
|currency|string|false|货币代码（eco-cal，USD/EUR/CNY/...）。|-|
|ptype|string|false|政策类型（policy-npr）。|-|
|puborg|string|false|发布机构（policy-npr）。|-|
|exchange|string|false|交易所（futures-weekly-detail，DCE/CFFEX/CZCE/SHFE/INE）。|-|
|prd|string|false|期货品种代码（futures-weekly-detail，如 CU/RB/IF）。|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/market/macro/eco-cal?page=0&size=0&year=0&startYear=0&endYear=0&puborg=&keyword=&endDate=&country=&quarter=&exchange=&prd=&startDate=&currency=&ptype='
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─date|string|事件日期|-|
|└─time|string|事件时间（HH:mm 字符串）|-|
|└─currency|string|货币代码（USD/EUR/CNY/JPY/...）|-|
|└─country|string|国家 / 地区|-|
|└─event|string|事件名称|-|
|└─value|string|公布值|-|
|└─preValue|string|前值|-|
|└─foreValue|string|预期值|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "date": "yyyy-MM-dd HH:mm:ss",
      "time": "",
      "currency": "",
      "country": "",
      "event": "",
      "value": "",
      "preValue": "",
      "foreValue": ""
    }
  ],
  "traceId": ""
}
```

### 国家政策档案（{@code macro_policy_npr}）。<br><br>可按 keyword（title 模糊） / ptype / puborg / 日期范围（YYYYMMDD 按 pubtime 字符串前缀）过滤。<br>&lt;b&gt;注意&lt;/b&gt;：contentHtml 单条可能 100KB+，size 建议 &amp;amp;le; 20。 
**URL:** /openapi/v1/market/macro/policy-npr

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 国家政策档案（{@code macro_policy_npr}）。

<p>可按 keyword（title 模糊） / ptype / puborg / 日期范围（YYYYMMDD 按 pubtime 字符串前缀）过滤。
<b>注意</b>：contentHtml 单条可能 100KB+，size 建议 &le; 20。</p>

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|page|int32|false|第几页，从 1 起。默认 1。0 / 负数会被当成 1。|-|
|size|int32|false|每页记录数。默认 50，硬上限 {@value #MAX_SIZE}。<br/><p>传入超过 {@value #MAX_SIZE} 时会被自动截断到 {@value #MAX_SIZE}（不报错）。</p>|-|
|keyword|string|false|通用关键字（按表内最关键文本列模糊匹配，参类级注释）。|-|
|year|int32|false|年度（fund-sales-ratio / fund-sales-vol 用）。|-|
|startYear|int32|false|起始年度（fund-sales-ratio 区间）。|-|
|endYear|int32|false|结束年度（fund-sales-ratio 区间）。|-|
|quarter|string|false|季度（fund-sales-vol，如 "1"/"2"/"3"/"4" 或 "Q1"/...）。|-|
|startDate|string|false|起始日期 {@code YYYYMMDD}。|-|
|endDate|string|false|结束日期 {@code YYYYMMDD}。|-|
|country|string|false|国家代码（eco-cal）。|-|
|currency|string|false|货币代码（eco-cal，USD/EUR/CNY/...）。|-|
|ptype|string|false|政策类型（policy-npr）。|-|
|puborg|string|false|发布机构（policy-npr）。|-|
|exchange|string|false|交易所（futures-weekly-detail，DCE/CFFEX/CZCE/SHFE/INE）。|-|
|prd|string|false|期货品种代码（futures-weekly-detail，如 CU/RB/IF）。|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/market/macro/policy-npr?page=0&size=0&year=0&startYear=0&endYear=0&country=&ptype=&startDate=&puborg=&exchange=&prd=&quarter=&currency=&keyword=&endDate='
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─pcode|string|政策编号（业务唯一键）|-|
|└─pubtime|string|发布时间（datetime 字符串）|-|
|└─title|string|政策标题|-|
|└─url|string|政策详情 URL|-|
|└─contentHtml|string|政策正文 HTML（TEXT 大字段）|-|
|└─puborg|string|发布机构|-|
|└─ptype|string|政策类型|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "pcode": "",
      "pubtime": "",
      "title": "",
      "url": "",
      "contentHtml": "",
      "puborg": "",
      "ptype": ""
    }
  ],
  "traceId": ""
}
```

## OpenAPI v1 —— 美股全量端点（{@code stock.us} scope，Max 套餐及以上）。

&lt;p&gt;覆盖 9 张 PG 表的 9 个端点：
&lt;ul&gt;
  &lt;li&gt;{@code POST /openapi/v1/stock/us/basic}        — 美股基础信息&lt;/li&gt;
  &lt;li&gt;{@code POST /openapi/v1/stock/us/tradecal}     — 美股交易日历&lt;/li&gt;
  &lt;li&gt;{@code POST /openapi/v1/stock/us/kline}        — 美股日 K 线（不复权，含估值快照）&lt;/li&gt;
  &lt;li&gt;{@code POST /openapi/v1/stock/us/kline-adj}    — 美股日 K 线（复权 + 估值快照）&lt;/li&gt;
  &lt;li&gt;{@code POST /openapi/v1/stock/us/adj-factor}   — 美股复权因子&lt;/li&gt;
  &lt;li&gt;{@code POST /openapi/v1/stock/us/income}       — 美股利润表（long format）&lt;/li&gt;
  &lt;li&gt;{@code POST /openapi/v1/stock/us/balance-sheet}— 美股资产负债表（long format）&lt;/li&gt;
  &lt;li&gt;{@code POST /openapi/v1/stock/us/cash-flow}    — 美股现金流量表（long format）&lt;/li&gt;
  &lt;li&gt;{@code POST /openapi/v1/stock/us/fina-indicator}— 美股财务指标（精简 22 核心列）&lt;/li&gt;
&lt;/ul&gt;
### 美股基础信息（{@code stock_us_basic}）。<br><br>{@code tsCode} 可空（列全市场），可选 {@code classify} 过滤（{@code ADR} / {@code GDR} / {@code EQ}）。
**URL:** /openapi/v1/stock/us/basic

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 美股基础信息（{@code stock_us_basic}）。

<p>{@code tsCode} 可空（列全市场），可选 {@code classify} 过滤（{@code ADR} / {@code GDR} / {@code EQ}）。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|page|int32|false|第几页，从 1 起。默认 1。0 / 负数会被当成 1。|-|
|size|int32|false|每页记录数。默认 50，硬上限 {@value #MAX_SIZE}。<br/><p>传入超过 {@value #MAX_SIZE} 时会被自动截断到 {@value #MAX_SIZE}（不报错）。</p>|-|
|tsCode|string|false|美股 TS 代码，如 {@code "AAPL.O"}（纳斯达克）/ {@code "MSFT.O"} / {@code "JPM.N"}（纽交所）。<br/><p>K 线 / 复权因子 / 三大表 / 财务指标必填；basic / tradecal 可空。</p>|-|
|startDate|string|false|起始日期，格式 {@code YYYYMMDD}。可空。|-|
|endDate|string|false|结束日期，格式 {@code YYYYMMDD}。可空。|-|
|reportType|string|false|报告期（仅 fina-indicator 端点用，精确等值匹配 report_type 列）。<b>值是完整报告期串</b>，<br/>形如 {@code "2025/Q1"} / {@code "2023/FY"}（东财口径，{@code FY}=年报、{@code Q1/Q2/...}=季度累计）。<br/><b>不要</b>传 {@code "A"}/{@code "S1"}/{@code "Q1"} 这种纯代码——匹配不到、返回空。<br/><b>不确定就别传</b>（返回全部报告期，自己再筛）。可空。|-|
|listStatus|string|false|上市状态（仅 basic 端点用）：{@code L} 上市 / {@code D} 退市 / {@code P} 暂停。可空。<br/><p>注：美股 us_basic 表无该列；该字段保留以维持 form 一致性，basic 端点忽略。</p>|-|
|classify|string|false|分类（仅 basic 端点用）：{@code "ADR"} / {@code "GDR"} / {@code "EQ"}。可空。|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/stock/us/basic?page=0&size=0&endDate=&reportType=&listStatus=&tsCode=&startDate=&classify='
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─tsCode|string|TS 代码（如 {@code AAPL.O} / {@code MSFT.O} / {@code JPM.N}）|-|
|└─name|string|股票简称|-|
|└─enname|string|英文名称|-|
|└─classify|string|分类（{@code ADR} / {@code GDR} / {@code EQ}）|-|
|└─listDate|string|上市日期|-|
|└─delistDate|string|退市日期|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "tsCode": "",
      "name": "",
      "enname": "",
      "classify": "",
      "listDate": "yyyy-MM-dd HH:mm:ss",
      "delistDate": "yyyy-MM-dd HH:mm:ss"
    }
  ],
  "traceId": ""
}
```

### 美股交易日历（{@code stock_us_tradecal}）。<br><br>用途：判断美股是否交易日、计算上一/下一交易日。{@code startDate} / {@code endDate} 可空。
**URL:** /openapi/v1/stock/us/tradecal

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 美股交易日历（{@code stock_us_tradecal}）。

<p>用途：判断美股是否交易日、计算上一/下一交易日。{@code startDate} / {@code endDate} 可空。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|page|int32|false|第几页，从 1 起。默认 1。0 / 负数会被当成 1。|-|
|size|int32|false|每页记录数。默认 50，硬上限 {@value #MAX_SIZE}。<br/><p>传入超过 {@value #MAX_SIZE} 时会被自动截断到 {@value #MAX_SIZE}（不报错）。</p>|-|
|tsCode|string|false|美股 TS 代码，如 {@code "AAPL.O"}（纳斯达克）/ {@code "MSFT.O"} / {@code "JPM.N"}（纽交所）。<br/><p>K 线 / 复权因子 / 三大表 / 财务指标必填；basic / tradecal 可空。</p>|-|
|startDate|string|false|起始日期，格式 {@code YYYYMMDD}。可空。|-|
|endDate|string|false|结束日期，格式 {@code YYYYMMDD}。可空。|-|
|reportType|string|false|报告期（仅 fina-indicator 端点用，精确等值匹配 report_type 列）。<b>值是完整报告期串</b>，<br/>形如 {@code "2025/Q1"} / {@code "2023/FY"}（东财口径，{@code FY}=年报、{@code Q1/Q2/...}=季度累计）。<br/><b>不要</b>传 {@code "A"}/{@code "S1"}/{@code "Q1"} 这种纯代码——匹配不到、返回空。<br/><b>不确定就别传</b>（返回全部报告期，自己再筛）。可空。|-|
|listStatus|string|false|上市状态（仅 basic 端点用）：{@code L} 上市 / {@code D} 退市 / {@code P} 暂停。可空。<br/><p>注：美股 us_basic 表无该列；该字段保留以维持 form 一致性，basic 端点忽略。</p>|-|
|classify|string|false|分类（仅 basic 端点用）：{@code "ADR"} / {@code "GDR"} / {@code "EQ"}。可空。|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/stock/us/tradecal?page=0&size=0&classify=&listStatus=&reportType=&startDate=&endDate=&tsCode='
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─calDate|string|日历日期|-|
|└─isOpen|int32|是否交易：0 休市 / 1 交易|-|
|└─pretradeDate|string|上一个交易日|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "calDate": "yyyy-MM-dd HH:mm:ss",
      "isOpen": 0,
      "pretradeDate": "yyyy-MM-dd HH:mm:ss"
    }
  ],
  "traceId": ""
}
```

### 美股日 K 线（不复权 + 估值快照，{@code stock_us_daily}）。{@code tsCode} 必填。<br><br>一站式美股数据：OHLCV + vwap + turnover_ratio + total_mv + pe + pb。<br>跨除权日比较股价时建议改用 {@code /kline-adj}（含复权）或配合 {@code /adj-factor} 自行换算。
**URL:** /openapi/v1/stock/us/kline

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 美股日 K 线（不复权 + 估值快照，{@code stock_us_daily}）。{@code tsCode} 必填。

<p>一站式美股数据：OHLCV + vwap + turnover_ratio + total_mv + pe + pb。
跨除权日比较股价时建议改用 {@code /kline-adj}（含复权）或配合 {@code /adj-factor} 自行换算。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|page|int32|false|第几页，从 1 起。默认 1。0 / 负数会被当成 1。|-|
|size|int32|false|每页记录数。默认 50，硬上限 {@value #MAX_SIZE}。<br/><p>传入超过 {@value #MAX_SIZE} 时会被自动截断到 {@value #MAX_SIZE}（不报错）。</p>|-|
|tsCode|string|false|美股 TS 代码，如 {@code "AAPL.O"}（纳斯达克）/ {@code "MSFT.O"} / {@code "JPM.N"}（纽交所）。<br/><p>K 线 / 复权因子 / 三大表 / 财务指标必填；basic / tradecal 可空。</p>|-|
|startDate|string|false|起始日期，格式 {@code YYYYMMDD}。可空。|-|
|endDate|string|false|结束日期，格式 {@code YYYYMMDD}。可空。|-|
|reportType|string|false|报告期（仅 fina-indicator 端点用，精确等值匹配 report_type 列）。<b>值是完整报告期串</b>，<br/>形如 {@code "2025/Q1"} / {@code "2023/FY"}（东财口径，{@code FY}=年报、{@code Q1/Q2/...}=季度累计）。<br/><b>不要</b>传 {@code "A"}/{@code "S1"}/{@code "Q1"} 这种纯代码——匹配不到、返回空。<br/><b>不确定就别传</b>（返回全部报告期，自己再筛）。可空。|-|
|listStatus|string|false|上市状态（仅 basic 端点用）：{@code L} 上市 / {@code D} 退市 / {@code P} 暂停。可空。<br/><p>注：美股 us_basic 表无该列；该字段保留以维持 form 一致性，basic 端点忽略。</p>|-|
|classify|string|false|分类（仅 basic 端点用）：{@code "ADR"} / {@code "GDR"} / {@code "EQ"}。可空。|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/stock/us/kline?page=0&size=0&tsCode=&reportType=&endDate=&listStatus=&classify=&startDate='
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─tsCode|string|TS 代码|-|
|└─tradeDate|string|交易日期|-|
|└─open|number|开盘价|-|
|└─high|number|最高价|-|
|└─low|number|最低价|-|
|└─close|number|收盘价|-|
|└─preClose|number|昨收价|-|
|└─change|number|涨跌额|-|
|└─pctChange|number|涨跌幅（%）|-|
|└─vol|number|成交量|-|
|└─amount|number|成交额|-|
|└─vwap|number|成交均价|-|
|└─turnoverRatio|number|换手率（%）|-|
|└─totalMv|number|总市值|-|
|└─pe|number|市盈率|-|
|└─pb|number|市净率|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "tsCode": "",
      "tradeDate": "yyyy-MM-dd HH:mm:ss",
      "open": 0,
      "high": 0,
      "low": 0,
      "close": 0,
      "preClose": 0,
      "change": 0,
      "pctChange": 0,
      "vol": 0,
      "amount": 0,
      "vwap": 0,
      "turnoverRatio": 0,
      "totalMv": 0,
      "pe": 0,
      "pb": 0
    }
  ],
  "traceId": ""
}
```

### 美股日 K 线（复权 + 估值快照，{@code stock_us_daily_adj}）。{@code tsCode} 必填。<br><br>含 vwap + adj_factor + turnover_ratio + 流通/总股本 + 流通/总市值 + exchange。
**URL:** /openapi/v1/stock/us/kline-adj

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 美股日 K 线（复权 + 估值快照，{@code stock_us_daily_adj}）。{@code tsCode} 必填。

<p>含 vwap + adj_factor + turnover_ratio + 流通/总股本 + 流通/总市值 + exchange。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|page|int32|false|第几页，从 1 起。默认 1。0 / 负数会被当成 1。|-|
|size|int32|false|每页记录数。默认 50，硬上限 {@value #MAX_SIZE}。<br/><p>传入超过 {@value #MAX_SIZE} 时会被自动截断到 {@value #MAX_SIZE}（不报错）。</p>|-|
|tsCode|string|false|美股 TS 代码，如 {@code "AAPL.O"}（纳斯达克）/ {@code "MSFT.O"} / {@code "JPM.N"}（纽交所）。<br/><p>K 线 / 复权因子 / 三大表 / 财务指标必填；basic / tradecal 可空。</p>|-|
|startDate|string|false|起始日期，格式 {@code YYYYMMDD}。可空。|-|
|endDate|string|false|结束日期，格式 {@code YYYYMMDD}。可空。|-|
|reportType|string|false|报告期（仅 fina-indicator 端点用，精确等值匹配 report_type 列）。<b>值是完整报告期串</b>，<br/>形如 {@code "2025/Q1"} / {@code "2023/FY"}（东财口径，{@code FY}=年报、{@code Q1/Q2/...}=季度累计）。<br/><b>不要</b>传 {@code "A"}/{@code "S1"}/{@code "Q1"} 这种纯代码——匹配不到、返回空。<br/><b>不确定就别传</b>（返回全部报告期，自己再筛）。可空。|-|
|listStatus|string|false|上市状态（仅 basic 端点用）：{@code L} 上市 / {@code D} 退市 / {@code P} 暂停。可空。<br/><p>注：美股 us_basic 表无该列；该字段保留以维持 form 一致性，basic 端点忽略。</p>|-|
|classify|string|false|分类（仅 basic 端点用）：{@code "ADR"} / {@code "GDR"} / {@code "EQ"}。可空。|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/stock/us/kline-adj?page=0&size=0&listStatus=&reportType=&endDate=&startDate=&classify=&tsCode='
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─tsCode|string|TS 代码|-|
|└─tradeDate|string|交易日期|-|
|└─close|number|收盘价|-|
|└─open|number|开盘价|-|
|└─high|number|最高价|-|
|└─low|number|最低价|-|
|└─preClose|number|昨收价|-|
|└─change|number|涨跌额|-|
|└─pctChange|number|涨跌幅（%）|-|
|└─vol|number|成交量|-|
|└─amount|number|成交额|-|
|└─vwap|number|成交均价|-|
|└─adjFactor|number|复权因子|-|
|└─turnoverRatio|number|换手率（%）|-|
|└─freeShare|number|流通股本|-|
|└─totalShare|number|总股本|-|
|└─freeMv|number|流通市值|-|
|└─totalMv|number|总市值|-|
|└─exchange|string|交易所（{@code NAS} 纳斯达克 / {@code NYS} 纽交所 / {@code OTC}）|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "tsCode": "",
      "tradeDate": "yyyy-MM-dd HH:mm:ss",
      "close": 0,
      "open": 0,
      "high": 0,
      "low": 0,
      "preClose": 0,
      "change": 0,
      "pctChange": 0,
      "vol": 0,
      "amount": 0,
      "vwap": 0,
      "adjFactor": 0,
      "turnoverRatio": 0,
      "freeShare": 0,
      "totalShare": 0,
      "freeMv": 0,
      "totalMv": 0,
      "exchange": ""
    }
  ],
  "traceId": ""
}
```

### 美股复权因子（{@code stock_us_adjfactor}）。{@code tsCode} 必填。<br><br>用法：HFQ_price = BFQ_price × cum_adjfactor / 当日最新 cum_adjfactor。
**URL:** /openapi/v1/stock/us/adj-factor

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 美股复权因子（{@code stock_us_adjfactor}）。{@code tsCode} 必填。

<p>用法：HFQ_price = BFQ_price × cum_adjfactor / 当日最新 cum_adjfactor。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|page|int32|false|第几页，从 1 起。默认 1。0 / 负数会被当成 1。|-|
|size|int32|false|每页记录数。默认 50，硬上限 {@value #MAX_SIZE}。<br/><p>传入超过 {@value #MAX_SIZE} 时会被自动截断到 {@value #MAX_SIZE}（不报错）。</p>|-|
|tsCode|string|false|美股 TS 代码，如 {@code "AAPL.O"}（纳斯达克）/ {@code "MSFT.O"} / {@code "JPM.N"}（纽交所）。<br/><p>K 线 / 复权因子 / 三大表 / 财务指标必填；basic / tradecal 可空。</p>|-|
|startDate|string|false|起始日期，格式 {@code YYYYMMDD}。可空。|-|
|endDate|string|false|结束日期，格式 {@code YYYYMMDD}。可空。|-|
|reportType|string|false|报告期（仅 fina-indicator 端点用，精确等值匹配 report_type 列）。<b>值是完整报告期串</b>，<br/>形如 {@code "2025/Q1"} / {@code "2023/FY"}（东财口径，{@code FY}=年报、{@code Q1/Q2/...}=季度累计）。<br/><b>不要</b>传 {@code "A"}/{@code "S1"}/{@code "Q1"} 这种纯代码——匹配不到、返回空。<br/><b>不确定就别传</b>（返回全部报告期，自己再筛）。可空。|-|
|listStatus|string|false|上市状态（仅 basic 端点用）：{@code L} 上市 / {@code D} 退市 / {@code P} 暂停。可空。<br/><p>注：美股 us_basic 表无该列；该字段保留以维持 form 一致性，basic 端点忽略。</p>|-|
|classify|string|false|分类（仅 basic 端点用）：{@code "ADR"} / {@code "GDR"} / {@code "EQ"}。可空。|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/stock/us/adj-factor?page=0&size=0&endDate=&reportType=&startDate=&classify=&tsCode=&listStatus='
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─tsCode|string|TS 代码|-|
|└─tradeDate|string|交易日期|-|
|└─exchange|string|交易所（{@code NAS} / {@code NYS} / {@code OTC}）|-|
|└─cumAdjfactor|number|累计复权因子|-|
|└─closePrice|number|当日收盘价|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "tsCode": "",
      "tradeDate": "yyyy-MM-dd HH:mm:ss",
      "exchange": "",
      "cumAdjfactor": 0,
      "closePrice": 0
    }
  ],
  "traceId": ""
}
```

### 美股利润表（long format，{@code stock_us_income}）。{@code tsCode} 必填。<br><br>每行一个 {@code (indType, indName)} → {@code indValue} 键值对。需在客户端做透视成宽表。
**URL:** /openapi/v1/stock/us/income

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 美股利润表（long format，{@code stock_us_income}）。{@code tsCode} 必填。

<p>每行一个 {@code (indType, indName)} → {@code indValue} 键值对。需在客户端做透视成宽表。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|page|int32|false|第几页，从 1 起。默认 1。0 / 负数会被当成 1。|-|
|size|int32|false|每页记录数。默认 50，硬上限 {@value #MAX_SIZE}。<br/><p>传入超过 {@value #MAX_SIZE} 时会被自动截断到 {@value #MAX_SIZE}（不报错）。</p>|-|
|tsCode|string|false|美股 TS 代码，如 {@code "AAPL.O"}（纳斯达克）/ {@code "MSFT.O"} / {@code "JPM.N"}（纽交所）。<br/><p>K 线 / 复权因子 / 三大表 / 财务指标必填；basic / tradecal 可空。</p>|-|
|startDate|string|false|起始日期，格式 {@code YYYYMMDD}。可空。|-|
|endDate|string|false|结束日期，格式 {@code YYYYMMDD}。可空。|-|
|reportType|string|false|报告期（仅 fina-indicator 端点用，精确等值匹配 report_type 列）。<b>值是完整报告期串</b>，<br/>形如 {@code "2025/Q1"} / {@code "2023/FY"}（东财口径，{@code FY}=年报、{@code Q1/Q2/...}=季度累计）。<br/><b>不要</b>传 {@code "A"}/{@code "S1"}/{@code "Q1"} 这种纯代码——匹配不到、返回空。<br/><b>不确定就别传</b>（返回全部报告期，自己再筛）。可空。|-|
|listStatus|string|false|上市状态（仅 basic 端点用）：{@code L} 上市 / {@code D} 退市 / {@code P} 暂停。可空。<br/><p>注：美股 us_basic 表无该列；该字段保留以维持 form 一致性，basic 端点忽略。</p>|-|
|classify|string|false|分类（仅 basic 端点用）：{@code "ADR"} / {@code "GDR"} / {@code "EQ"}。可空。|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/stock/us/income?page=0&size=0&startDate=&tsCode=&endDate=&reportType=&listStatus=&classify='
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─tsCode|string|TS 代码|-|
|└─endDate|string|报告期|-|
|└─indType|string|报告类型（{@code Q1} / {@code Q2} / {@code Q3} / {@code Q4} / {@code A} 年报 等）|-|
|└─name|string|股票名称|-|
|└─indName|string|指标名称|-|
|└─indValue|number|指标值|-|
|└─reportType|string|报告类型|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "tsCode": "",
      "endDate": "yyyy-MM-dd HH:mm:ss",
      "indType": "",
      "name": "",
      "indName": "",
      "indValue": 0,
      "reportType": ""
    }
  ],
  "traceId": ""
}
```

### 美股资产负债表（long format，{@code stock_us_balancesheet}）。{@code tsCode} 必填。
**URL:** /openapi/v1/stock/us/balance-sheet

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 美股资产负债表（long format，{@code stock_us_balancesheet}）。{@code tsCode} 必填。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|page|int32|false|第几页，从 1 起。默认 1。0 / 负数会被当成 1。|-|
|size|int32|false|每页记录数。默认 50，硬上限 {@value #MAX_SIZE}。<br/><p>传入超过 {@value #MAX_SIZE} 时会被自动截断到 {@value #MAX_SIZE}（不报错）。</p>|-|
|tsCode|string|false|美股 TS 代码，如 {@code "AAPL.O"}（纳斯达克）/ {@code "MSFT.O"} / {@code "JPM.N"}（纽交所）。<br/><p>K 线 / 复权因子 / 三大表 / 财务指标必填；basic / tradecal 可空。</p>|-|
|startDate|string|false|起始日期，格式 {@code YYYYMMDD}。可空。|-|
|endDate|string|false|结束日期，格式 {@code YYYYMMDD}。可空。|-|
|reportType|string|false|报告期（仅 fina-indicator 端点用，精确等值匹配 report_type 列）。<b>值是完整报告期串</b>，<br/>形如 {@code "2025/Q1"} / {@code "2023/FY"}（东财口径，{@code FY}=年报、{@code Q1/Q2/...}=季度累计）。<br/><b>不要</b>传 {@code "A"}/{@code "S1"}/{@code "Q1"} 这种纯代码——匹配不到、返回空。<br/><b>不确定就别传</b>（返回全部报告期，自己再筛）。可空。|-|
|listStatus|string|false|上市状态（仅 basic 端点用）：{@code L} 上市 / {@code D} 退市 / {@code P} 暂停。可空。<br/><p>注：美股 us_basic 表无该列；该字段保留以维持 form 一致性，basic 端点忽略。</p>|-|
|classify|string|false|分类（仅 basic 端点用）：{@code "ADR"} / {@code "GDR"} / {@code "EQ"}。可空。|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/stock/us/balance-sheet?page=0&size=0&tsCode=&listStatus=&endDate=&reportType=&classify=&startDate='
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─tsCode|string|TS 代码|-|
|└─endDate|string|报告期|-|
|└─indType|string|报告类型（{@code Q1} / {@code Q2} / {@code Q3} / {@code Q4} / {@code A} 年报 等）|-|
|└─name|string|股票名称|-|
|└─indName|string|指标名称|-|
|└─indValue|number|指标值|-|
|└─reportType|string|报告类型|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "tsCode": "",
      "endDate": "yyyy-MM-dd HH:mm:ss",
      "indType": "",
      "name": "",
      "indName": "",
      "indValue": 0,
      "reportType": ""
    }
  ],
  "traceId": ""
}
```

### 美股现金流量表（long format，{@code stock_us_cashflow}）。{@code tsCode} 必填。
**URL:** /openapi/v1/stock/us/cash-flow

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 美股现金流量表（long format，{@code stock_us_cashflow}）。{@code tsCode} 必填。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|page|int32|false|第几页，从 1 起。默认 1。0 / 负数会被当成 1。|-|
|size|int32|false|每页记录数。默认 50，硬上限 {@value #MAX_SIZE}。<br/><p>传入超过 {@value #MAX_SIZE} 时会被自动截断到 {@value #MAX_SIZE}（不报错）。</p>|-|
|tsCode|string|false|美股 TS 代码，如 {@code "AAPL.O"}（纳斯达克）/ {@code "MSFT.O"} / {@code "JPM.N"}（纽交所）。<br/><p>K 线 / 复权因子 / 三大表 / 财务指标必填；basic / tradecal 可空。</p>|-|
|startDate|string|false|起始日期，格式 {@code YYYYMMDD}。可空。|-|
|endDate|string|false|结束日期，格式 {@code YYYYMMDD}。可空。|-|
|reportType|string|false|报告期（仅 fina-indicator 端点用，精确等值匹配 report_type 列）。<b>值是完整报告期串</b>，<br/>形如 {@code "2025/Q1"} / {@code "2023/FY"}（东财口径，{@code FY}=年报、{@code Q1/Q2/...}=季度累计）。<br/><b>不要</b>传 {@code "A"}/{@code "S1"}/{@code "Q1"} 这种纯代码——匹配不到、返回空。<br/><b>不确定就别传</b>（返回全部报告期，自己再筛）。可空。|-|
|listStatus|string|false|上市状态（仅 basic 端点用）：{@code L} 上市 / {@code D} 退市 / {@code P} 暂停。可空。<br/><p>注：美股 us_basic 表无该列；该字段保留以维持 form 一致性，basic 端点忽略。</p>|-|
|classify|string|false|分类（仅 basic 端点用）：{@code "ADR"} / {@code "GDR"} / {@code "EQ"}。可空。|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/stock/us/cash-flow?page=0&size=0&endDate=&reportType=&listStatus=&startDate=&classify=&tsCode='
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─tsCode|string|TS 代码|-|
|└─endDate|string|报告期|-|
|└─indType|string|报告类型（{@code Q1} / {@code Q2} / {@code Q3} / {@code Q4} / {@code A} 年报 等）|-|
|└─name|string|股票名称|-|
|└─indName|string|指标名称|-|
|└─indValue|number|指标值|-|
|└─reportType|string|报告类型|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "tsCode": "",
      "endDate": "yyyy-MM-dd HH:mm:ss",
      "indType": "",
      "name": "",
      "indName": "",
      "indValue": 0,
      "reportType": ""
    }
  ],
  "traceId": ""
}
```

### 美股财务指标（精简 22 核心列，{@code stock_us_fina_indicator}）。{@code tsCode} 必填。<br><br>每股 / 盈利能力 / 偿债 / 周转 / 同比。{@code reportType} 可选过滤（年报 / 季报 / 半年报）。<br>上游表共 ~66 列，本端点只暴露 22 个高频字段；银行保险特有指标（保费 / 利息 / 贷款）不在此暴露。
**URL:** /openapi/v1/stock/us/fina-indicator

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 美股财务指标（精简 22 核心列，{@code stock_us_fina_indicator}）。{@code tsCode} 必填。

<p>每股 / 盈利能力 / 偿债 / 周转 / 同比。{@code reportType} 可选过滤（年报 / 季报 / 半年报）。
<p>上游表共 ~66 列，本端点只暴露 22 个高频字段；银行保险特有指标（保费 / 利息 / 贷款）不在此暴露。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|page|int32|false|第几页，从 1 起。默认 1。0 / 负数会被当成 1。|-|
|size|int32|false|每页记录数。默认 50，硬上限 {@value #MAX_SIZE}。<br/><p>传入超过 {@value #MAX_SIZE} 时会被自动截断到 {@value #MAX_SIZE}（不报错）。</p>|-|
|tsCode|string|false|美股 TS 代码，如 {@code "AAPL.O"}（纳斯达克）/ {@code "MSFT.O"} / {@code "JPM.N"}（纽交所）。<br/><p>K 线 / 复权因子 / 三大表 / 财务指标必填；basic / tradecal 可空。</p>|-|
|startDate|string|false|起始日期，格式 {@code YYYYMMDD}。可空。|-|
|endDate|string|false|结束日期，格式 {@code YYYYMMDD}。可空。|-|
|reportType|string|false|报告期（仅 fina-indicator 端点用，精确等值匹配 report_type 列）。<b>值是完整报告期串</b>，<br/>形如 {@code "2025/Q1"} / {@code "2023/FY"}（东财口径，{@code FY}=年报、{@code Q1/Q2/...}=季度累计）。<br/><b>不要</b>传 {@code "A"}/{@code "S1"}/{@code "Q1"} 这种纯代码——匹配不到、返回空。<br/><b>不确定就别传</b>（返回全部报告期，自己再筛）。可空。|-|
|listStatus|string|false|上市状态（仅 basic 端点用）：{@code L} 上市 / {@code D} 退市 / {@code P} 暂停。可空。<br/><p>注：美股 us_basic 表无该列；该字段保留以维持 form 一致性，basic 端点忽略。</p>|-|
|classify|string|false|分类（仅 basic 端点用）：{@code "ADR"} / {@code "GDR"} / {@code "EQ"}。可空。|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/stock/us/fina-indicator?page=0&size=0&startDate=&listStatus=&classify=&endDate=&reportType=&tsCode='
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─tsCode|string|TS 代码|-|
|└─securityNameAbbr|string|证券简称|-|
|└─endDate|string|报告期|-|
|└─reportType|string|报告类型|-|
|└─indType|string|报告类型/口径（同 ind_type）|-|
|└─accountingStandards|string|会计准则|-|
|└─currency|string|币种|-|
|└─operateIncome|number|营业收入|-|
|└─operateIncomeYoy|number|营业收入同比|-|
|└─grossProfit|number|毛利润|-|
|└─grossProfitYoy|number|毛利润同比|-|
|└─parentHolderNetprofit|number|归母净利润|-|
|└─parentHolderNetprofitYoy|number|归母净利润同比|-|
|└─basicEps|number|基本每股收益|-|
|└─dilutedEps|number|稀释每股收益|-|
|└─basicEpsYoy|number|基本 EPS 同比|-|
|└─grossProfitRatio|number|毛利率|-|
|└─netProfitRatio|number|净利率|-|
|└─roeAvg|number|平均 ROE|-|
|└─roa|number|ROA|-|
|└─debtAssetRatio|number|资产负债率|-|
|└─currentRatio|number|流动比率|-|
|└─speedRatio|number|速动比率|-|
|└─equityRatio|number|权益比率|-|
|└─totalAssetsTr|number|总资产周转率|-|
|└─inventoryTr|number|存货周转率|-|
|└─accountsReceTr|number|应收账款周转率|-|
|└─totalIncome|number|总收入|-|
|└─payoutRatio|number|派息比率|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "tsCode": "",
      "securityNameAbbr": "",
      "endDate": "yyyy-MM-dd HH:mm:ss",
      "reportType": "",
      "indType": "",
      "accountingStandards": "",
      "currency": "",
      "operateIncome": 0,
      "operateIncomeYoy": 0,
      "grossProfit": 0,
      "grossProfitYoy": 0,
      "parentHolderNetprofit": 0,
      "parentHolderNetprofitYoy": 0,
      "basicEps": 0,
      "dilutedEps": 0,
      "basicEpsYoy": 0,
      "grossProfitRatio": 0,
      "netProfitRatio": 0,
      "roeAvg": 0,
      "roa": 0,
      "debtAssetRatio": 0,
      "currentRatio": 0,
      "speedRatio": 0,
      "equityRatio": 0,
      "totalAssetsTr": 0,
      "inventoryTr": 0,
      "accountsReceTr": 0,
      "totalIncome": 0,
      "payoutRatio": 0
    }
  ],
  "traceId": ""
}
```

## OpenAPI v1 —— 机器对机器（M2M）套餐数据 token 发放端点。

&lt;p&gt;供 claw-server 在用户买套餐 / 续费 / 升降档时调用，按套餐档位换取 / 管理用户的 stock 数据
token（{@code stk_live_*}）。claw 持有一把带 scope {@code admin.provision} 的服务令牌
（IP 锁死 claw 出口）调本控制器。

&lt;p&gt;&lt;b&gt;鉴权&lt;/b&gt;：类级 {@link OpenApiScope}{@code (&quot;admin.provision&quot;)} —— 路径落在 {@code /openapi/**}
自动被 {@code OpenApiTokenInterceptor} 拦截，校验 token / IP / 频率 + 本 scope，持有
{@code admin.provision} 或 {@code *} 才放行。普通数据 token（pro/max/plus）不含此 scope，调不到。

&lt;p&gt;设计稿见 {@code stock/docs/claw-data-integration.md} §四。
### 按套餐档位发放数据 token。用户买套餐时由 claw 调用。<br><br>请求体 {@code data.rawToken} 为一次性明文，claw 须立即落库 + 注入用户 Agent 实例。<br>{@code clientRequestId}（如订单号）非空时 24h 内幂等：重复请求返回同一 token，不重复发。
**URL:** /openapi/admin/provision

**Type:** POST


**Content-Type:** application/json

**Description:** 按套餐档位发放数据 token。用户买套餐时由 claw 调用。

<p>请求体 {@code data.rawToken} 为一次性明文，claw 须立即落库 + 注入用户 Agent 实例。
{@code clientRequestId}（如订单号）非空时 24h 内幂等：重复请求返回同一 token，不重复发。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Body-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|userId|int64|false|No comments found.|-|
|d|int32|false|No comments found.|-|
|ip|string|false|No comments found.|-|
|market|string|false|No comments found.|-|
|vn|string|false|No comments found.|-|
|vc|int32|false|No comments found.|-|
|appsFlyerId|string|false|appsflyer 设备AF唯一ID|-|
|l|string|false|No comments found.|-|
|plan|string|false|套餐档位（required）：{@code free / plus / pro / max} 之一（由低到高），对应 ScopeRegistry 的预设 scope 集合。|-|
|clientRef|string|false|claw 侧 user_package id（required）：用于拼出 ownerName 标识（{@code claw:<clientRef>}），便于审计与回查。|-|
|allowedIps|string|false|该用户 Agent 实例出口 IP / CIDR（required）：签发 token 绑定到此 IP，泄露也无法在他处使用。|-|
|expireDays|int32|false|套餐剩余天数（required）：作为 token 有效期，与套餐到期对齐。|-|
|rateLimitPerMin|int32|false|每分钟请求上限（可空）：留空则用该套餐默认值 {@code plan.getDefaultRateLimitPerMin()}。|-|
|clientRequestId|string|false|幂等键（可空）：如 claw 订单号 order_no；非空时 24h 内重复请求返回同一 token，不重复发。|-|

**Request-example:**
```bash
curl -X POST -H "Content-Type: application/json" -H "Authorization:Bearer {{token}}" -i '/openapi/admin/provision' --data '{
  "userId": 0,
  "d": 0,
  "ip": "",
  "market": "",
  "vn": "",
  "vc": 0,
  "appsFlyerId": "",
  "l": "",
  "plan": "",
  "clientRef": "",
  "allowedIps": "",
  "expireDays": 0,
  "rateLimitPerMin": 0,
  "clientRequestId": ""
}'
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|object|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─id|int64|No comments found.|-|
|└─rawToken|string|No comments found.|-|
|└─tokenPrefix|string|No comments found.|-|
|└─ownerName|string|No comments found.|-|
|└─scopes|string|No comments found.|-|
|└─allowedIps|string|No comments found.|-|
|└─allowedPaths|string|单接口级路径白/黑名单 CSV（方案 B）。null/空 = 不限路径。|-|
|└─rateLimitPerMin|int32|No comments found.|-|
|└─expireAt|string|No comments found.|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": {
    "id": 0,
    "rawToken": "",
    "tokenPrefix": "",
    "ownerName": "",
    "scopes": "",
    "allowedIps": "",
    "allowedPaths": "",
    "rateLimitPerMin": 0,
    "expireAt": "yyyy-MM-dd HH:mm:ss"
  },
  "traceId": ""
}
```

### 吊销数据 token。用户退订 / 套餐过期 / 实例销毁时由 claw 调用，立即生效不可恢复。
**URL:** /openapi/admin/revoke

**Type:** POST


**Content-Type:** application/json

**Description:** 吊销数据 token。用户退订 / 套餐过期 / 实例销毁时由 claw 调用，立即生效不可恢复。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Body-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|userId|int64|false|No comments found.|-|
|d|int32|false|No comments found.|-|
|ip|string|false|No comments found.|-|
|market|string|false|No comments found.|-|
|vn|string|false|No comments found.|-|
|vc|int32|false|No comments found.|-|
|appsFlyerId|string|false|appsflyer 设备AF唯一ID|-|
|l|string|false|No comments found.|-|
|tokenId|int64|false|要吊销的 token id|-|

**Request-example:**
```bash
curl -X POST -H "Content-Type: application/json" -H "Authorization:Bearer {{token}}" -i '/openapi/admin/revoke' --data '{
  "userId": 0,
  "d": 0,
  "ip": "",
  "market": "",
  "vn": "",
  "vc": 0,
  "appsFlyerId": "",
  "l": "",
  "tokenId": 0
}'
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|object|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "traceId": ""
}
```

### 轮换 / 续期数据 token：id 不变、明文刷新，可同时延长有效期。续费时由 claw 调用。
**URL:** /openapi/admin/rotate

**Type:** POST


**Content-Type:** application/json

**Description:** 轮换 / 续期数据 token：id 不变、明文刷新，可同时延长有效期。续费时由 claw 调用。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Body-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|userId|int64|false|No comments found.|-|
|d|int32|false|No comments found.|-|
|ip|string|false|No comments found.|-|
|market|string|false|No comments found.|-|
|vn|string|false|No comments found.|-|
|vc|int32|false|No comments found.|-|
|appsFlyerId|string|false|appsflyer 设备AF唯一ID|-|
|l|string|false|No comments found.|-|
|tokenId|int64|false|No comments found.|-|
|expireDays|int32|false|新有效期天数，默认沿用原值，可覆盖|-|

**Request-example:**
```bash
curl -X POST -H "Content-Type: application/json" -H "Authorization:Bearer {{token}}" -i '/openapi/admin/rotate' --data '{
  "userId": 0,
  "d": 0,
  "ip": "",
  "market": "",
  "vn": "",
  "vc": 0,
  "appsFlyerId": "",
  "l": "",
  "tokenId": 0,
  "expireDays": 0
}'
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|object|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─id|int64|No comments found.|-|
|└─rawToken|string|No comments found.|-|
|└─tokenPrefix|string|No comments found.|-|
|└─ownerName|string|No comments found.|-|
|└─scopes|string|No comments found.|-|
|└─allowedIps|string|No comments found.|-|
|└─allowedPaths|string|单接口级路径白/黑名单 CSV（方案 B）。null/空 = 不限路径。|-|
|└─rateLimitPerMin|int32|No comments found.|-|
|└─expireAt|string|No comments found.|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": {
    "id": 0,
    "rawToken": "",
    "tokenPrefix": "",
    "ownerName": "",
    "scopes": "",
    "allowedIps": "",
    "allowedPaths": "",
    "rateLimitPerMin": 0,
    "expireAt": "yyyy-MM-dd HH:mm:ss"
  },
  "traceId": ""
}
```

### 升级 / 降级：把已发 token 的 scope &lt;b&gt;整体覆盖&lt;/b&gt;为新套餐档位预设。<br>用户在 claw 改套餐（LOW↔MID↔HIGH）时调用 —— 不换明文 token、不必重新注入实例，秒级生效。
**URL:** /openapi/admin/apply-plan

**Type:** POST


**Content-Type:** application/json

**Description:** 升级 / 降级：把已发 token 的 scope <b>整体覆盖</b>为新套餐档位预设。
用户在 claw 改套餐（LOW↔MID↔HIGH）时调用 —— 不换明文 token、不必重新注入实例，秒级生效。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Body-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|userId|int64|false|No comments found.|-|
|d|int32|false|No comments found.|-|
|ip|string|false|No comments found.|-|
|market|string|false|No comments found.|-|
|vn|string|false|No comments found.|-|
|vc|int32|false|No comments found.|-|
|appsFlyerId|string|false|appsflyer 设备AF唯一ID|-|
|l|string|false|No comments found.|-|
|tokenId|int64|false|必填。|-|
|plan|string|false|必填。套餐名（不区分大小写）：{@code free / plus / pro / max / ultra}（由低到高）。|-|

**Request-example:**
```bash
curl -X POST -H "Content-Type: application/json" -H "Authorization:Bearer {{token}}" -i '/openapi/admin/apply-plan' --data '{
  "userId": 0,
  "d": 0,
  "ip": "",
  "market": "",
  "vn": "",
  "vc": 0,
  "appsFlyerId": "",
  "l": "",
  "tokenId": 0,
  "plan": ""
}'
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|object|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─id|int64|No comments found.|-|
|└─tokenPrefix|string|No comments found.|-|
|└─ownerName|string|No comments found.|-|
|└─ownerEmail|string|No comments found.|-|
|└─scopes|string|No comments found.|-|
|└─allowedIps|string|No comments found.|-|
|└─allowedPaths|string|单接口级路径白/黑名单 CSV（方案 B）。null/空 = 不限路径。|-|
|└─rateLimitPerMin|int32|No comments found.|-|
|└─status|int8|No comments found.|-|
|└─expireAt|string|No comments found.|-|
|└─lastUsedAt|string|No comments found.|-|
|└─lastUsedIp|string|No comments found.|-|
|└─description|string|No comments found.|-|
|└─createTime|string|No comments found.|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{"code":0,"msg":"","data":{"id":0,"tokenPrefix":"","ownerName":"","ownerEmail":"","scopes":"","allowedIps":"","allowedPaths":"","rateLimitPerMin":0,"status":,"expireAt":"yyyy-MM-dd HH:mm:ss","lastUsedAt":"yyyy-MM-dd HH:mm:ss","lastUsedIp":"","description":"","createTime":"yyyy-MM-dd HH:mm:ss"},"traceId":""}
```

### 续期：延长 token 有效期（默认 +15 天）、复位 status=ACTIVE，&lt;b&gt;不换明文 token&lt;/b&gt;。<br><br>主要服务 free 档 token 的半月续期闭环：用户打开 claw_client 小程序时由 claw 调用 ——<br>free 档 token 15 天有效，到期由 {@code verify} 拦截禁用；打开小程序触发本续期即重新启用，<br>形成&amp;quot;半月打开一次小程序&amp;quot;的留存机制。
**URL:** /openapi/admin/renew

**Type:** POST


**Content-Type:** application/json

**Description:** 续期：延长 token 有效期（默认 +15 天）、复位 status=ACTIVE，<b>不换明文 token</b>。

<p>主要服务 free 档 token 的半月续期闭环：用户打开 claw_client 小程序时由 claw 调用 ——
free 档 token 15 天有效，到期由 {@code verify} 拦截禁用；打开小程序触发本续期即重新启用，
形成"半月打开一次小程序"的留存机制。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Body-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|userId|int64|false|No comments found.|-|
|d|int32|false|No comments found.|-|
|ip|string|false|No comments found.|-|
|market|string|false|No comments found.|-|
|vn|string|false|No comments found.|-|
|vc|int32|false|No comments found.|-|
|appsFlyerId|string|false|appsflyer 设备AF唯一ID|-|
|l|string|false|No comments found.|-|
|tokenId|int64|false|待续期 token id（必填）。|-|
|expireDays|int32|false|续期天数；null 或 &lt;=0 取 15 天默认（半个月）；超过 5 年上限则 clamp。|-|

**Request-example:**
```bash
curl -X POST -H "Content-Type: application/json" -H "Authorization:Bearer {{token}}" -i '/openapi/admin/renew' --data '{
  "userId": 0,
  "d": 0,
  "ip": "",
  "market": "",
  "vn": "",
  "vc": 0,
  "appsFlyerId": "",
  "l": "",
  "tokenId": 0,
  "expireDays": 0
}'
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|object|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─id|int64|No comments found.|-|
|└─tokenPrefix|string|No comments found.|-|
|└─ownerName|string|No comments found.|-|
|└─ownerEmail|string|No comments found.|-|
|└─scopes|string|No comments found.|-|
|└─allowedIps|string|No comments found.|-|
|└─allowedPaths|string|单接口级路径白/黑名单 CSV（方案 B）。null/空 = 不限路径。|-|
|└─rateLimitPerMin|int32|No comments found.|-|
|└─status|int8|No comments found.|-|
|└─expireAt|string|No comments found.|-|
|└─lastUsedAt|string|No comments found.|-|
|└─lastUsedIp|string|No comments found.|-|
|└─description|string|No comments found.|-|
|└─createTime|string|No comments found.|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{"code":0,"msg":"","data":{"id":0,"tokenPrefix":"","ownerName":"","ownerEmail":"","scopes":"","allowedIps":"","allowedPaths":"","rateLimitPerMin":0,"status":,"expireAt":"yyyy-MM-dd HH:mm:ss","lastUsedAt":"yyyy-MM-dd HH:mm:ss","lastUsedIp":"","description":"","createTime":"yyyy-MM-dd HH:mm:ss"},"traceId":""}
```

### 单维度加 scope（增量、去重）。claw 后台在档位基础上勾选某个数据维度时调用。<br>非法 scope 名抛 {@code ERROR_PARAM_EXCEPTION}；不换明文、秒级生效。
**URL:** /openapi/admin/scope/add

**Type:** POST


**Content-Type:** application/json

**Description:** 单维度加 scope（增量、去重）。claw 后台在档位基础上勾选某个数据维度时调用。
非法 scope 名抛 {@code ERROR_PARAM_EXCEPTION}；不换明文、秒级生效。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Body-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|userId|int64|false|No comments found.|-|
|d|int32|false|No comments found.|-|
|ip|string|false|No comments found.|-|
|market|string|false|No comments found.|-|
|vn|string|false|No comments found.|-|
|vc|int32|false|No comments found.|-|
|appsFlyerId|string|false|appsflyer 设备AF唯一ID|-|
|l|string|false|No comments found.|-|
|tokenId|int64|false|必填。|-|
|scopes|string|false|逗号分隔的 scope 列表，如 "stock.kline,stock.minute"。空 / 全空白将被拒绝。|-|

**Request-example:**
```bash
curl -X POST -H "Content-Type: application/json" -H "Authorization:Bearer {{token}}" -i '/openapi/admin/scope/add' --data '{
  "userId": 0,
  "d": 0,
  "ip": "",
  "market": "",
  "vn": "",
  "vc": 0,
  "appsFlyerId": "",
  "l": "",
  "tokenId": 0,
  "scopes": ""
}'
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|object|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─id|int64|No comments found.|-|
|└─tokenPrefix|string|No comments found.|-|
|└─ownerName|string|No comments found.|-|
|└─ownerEmail|string|No comments found.|-|
|└─scopes|string|No comments found.|-|
|└─allowedIps|string|No comments found.|-|
|└─allowedPaths|string|单接口级路径白/黑名单 CSV（方案 B）。null/空 = 不限路径。|-|
|└─rateLimitPerMin|int32|No comments found.|-|
|└─status|int8|No comments found.|-|
|└─expireAt|string|No comments found.|-|
|└─lastUsedAt|string|No comments found.|-|
|└─lastUsedIp|string|No comments found.|-|
|└─description|string|No comments found.|-|
|└─createTime|string|No comments found.|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{"code":0,"msg":"","data":{"id":0,"tokenPrefix":"","ownerName":"","ownerEmail":"","scopes":"","allowedIps":"","allowedPaths":"","rateLimitPerMin":0,"status":,"expireAt":"yyyy-MM-dd HH:mm:ss","lastUsedAt":"yyyy-MM-dd HH:mm:ss","lastUsedIp":"","description":"","createTime":"yyyy-MM-dd HH:mm:ss"},"traceId":""}
```

### 单维度移除 scope（增量）。claw 后台取消勾选某个数据维度时调用。<br>移除后 scope 集合为空将被拒绝（防锁死，禁用请走 /revoke）。
**URL:** /openapi/admin/scope/remove

**Type:** POST


**Content-Type:** application/json

**Description:** 单维度移除 scope（增量）。claw 后台取消勾选某个数据维度时调用。
移除后 scope 集合为空将被拒绝（防锁死，禁用请走 /revoke）。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Body-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|userId|int64|false|No comments found.|-|
|d|int32|false|No comments found.|-|
|ip|string|false|No comments found.|-|
|market|string|false|No comments found.|-|
|vn|string|false|No comments found.|-|
|vc|int32|false|No comments found.|-|
|appsFlyerId|string|false|appsflyer 设备AF唯一ID|-|
|l|string|false|No comments found.|-|
|tokenId|int64|false|必填。|-|
|scopes|string|false|逗号分隔的 scope 列表，如 "stock.kline,stock.minute"。空 / 全空白将被拒绝。|-|

**Request-example:**
```bash
curl -X POST -H "Content-Type: application/json" -H "Authorization:Bearer {{token}}" -i '/openapi/admin/scope/remove' --data '{
  "userId": 0,
  "d": 0,
  "ip": "",
  "market": "",
  "vn": "",
  "vc": 0,
  "appsFlyerId": "",
  "l": "",
  "tokenId": 0,
  "scopes": ""
}'
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|object|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─id|int64|No comments found.|-|
|└─tokenPrefix|string|No comments found.|-|
|└─ownerName|string|No comments found.|-|
|└─ownerEmail|string|No comments found.|-|
|└─scopes|string|No comments found.|-|
|└─allowedIps|string|No comments found.|-|
|└─allowedPaths|string|单接口级路径白/黑名单 CSV（方案 B）。null/空 = 不限路径。|-|
|└─rateLimitPerMin|int32|No comments found.|-|
|└─status|int8|No comments found.|-|
|└─expireAt|string|No comments found.|-|
|└─lastUsedAt|string|No comments found.|-|
|└─lastUsedIp|string|No comments found.|-|
|└─description|string|No comments found.|-|
|└─createTime|string|No comments found.|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{"code":0,"msg":"","data":{"id":0,"tokenPrefix":"","ownerName":"","ownerEmail":"","scopes":"","allowedIps":"","allowedPaths":"","rateLimitPerMin":0,"status":,"expireAt":"yyyy-MM-dd HH:mm:ss","lastUsedAt":"yyyy-MM-dd HH:mm:ss","lastUsedIp":"","description":"","createTime":"yyyy-MM-dd HH:mm:ss"},"traceId":""}
```

### 设置单接口级路径白/黑名单 allowed_paths（方案 B，整体覆盖）。claw 后台在档位 scope 之上<br>对单个 / 一组接口精细化放开或排除时调用（如 pro 档但排除龙虎榜详情）。不换明文、秒级生效。<br>{@code allowedPaths} 逗号分隔 Ant 路径：普通项=允许、{@code !} 前缀=拒绝；空 / null = 清空限制。
**URL:** /openapi/admin/path/set

**Type:** POST


**Content-Type:** application/json

**Description:** 设置单接口级路径白/黑名单 allowed_paths（方案 B，整体覆盖）。claw 后台在档位 scope 之上
对单个 / 一组接口精细化放开或排除时调用（如 pro 档但排除龙虎榜详情）。不换明文、秒级生效。
<p>{@code allowedPaths} 逗号分隔 Ant 路径：普通项=允许、{@code !} 前缀=拒绝；空 / null = 清空限制。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Body-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|userId|int64|false|No comments found.|-|
|d|int32|false|No comments found.|-|
|ip|string|false|No comments found.|-|
|market|string|false|No comments found.|-|
|vn|string|false|No comments found.|-|
|vc|int32|false|No comments found.|-|
|appsFlyerId|string|false|appsflyer 设备AF唯一ID|-|
|l|string|false|No comments found.|-|
|tokenId|int64|false|必填。|-|
|allowedPaths|string|false|逗号分隔的 Ant 风格路径模式；{@code !} 前缀表示拒绝；空 / null 表示清空路径限制。|-|

**Request-example:**
```bash
curl -X POST -H "Content-Type: application/json" -H "Authorization:Bearer {{token}}" -i '/openapi/admin/path/set' --data '{
  "userId": 0,
  "d": 0,
  "ip": "",
  "market": "",
  "vn": "",
  "vc": 0,
  "appsFlyerId": "",
  "l": "",
  "tokenId": 0,
  "allowedPaths": ""
}'
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|object|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─id|int64|No comments found.|-|
|└─tokenPrefix|string|No comments found.|-|
|└─ownerName|string|No comments found.|-|
|└─ownerEmail|string|No comments found.|-|
|└─scopes|string|No comments found.|-|
|└─allowedIps|string|No comments found.|-|
|└─allowedPaths|string|单接口级路径白/黑名单 CSV（方案 B）。null/空 = 不限路径。|-|
|└─rateLimitPerMin|int32|No comments found.|-|
|└─status|int8|No comments found.|-|
|└─expireAt|string|No comments found.|-|
|└─lastUsedAt|string|No comments found.|-|
|└─lastUsedIp|string|No comments found.|-|
|└─description|string|No comments found.|-|
|└─createTime|string|No comments found.|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{"code":0,"msg":"","data":{"id":0,"tokenPrefix":"","ownerName":"","ownerEmail":"","scopes":"","allowedIps":"","allowedPaths":"","rateLimitPerMin":0,"status":,"expireAt":"yyyy-MM-dd HH:mm:ss","lastUsedAt":"yyyy-MM-dd HH:mm:ss","lastUsedIp":"","description":"","createTime":"yyyy-MM-dd HH:mm:ss"},"traceId":""}
```

### 设置&lt;b&gt;绝对&lt;/b&gt;到期时间（epoch 毫秒）：把 token 有效期覆写为精确时刻并复位 status=ACTIVE。<br>区别于 {@link #renew}（相对 +N 天）。claw 后台用日期选择器设定到期日时调用。
**URL:** /openapi/admin/set-expiry

**Type:** POST


**Content-Type:** application/json

**Description:** 设置<b>绝对</b>到期时间（epoch 毫秒）：把 token 有效期覆写为精确时刻并复位 status=ACTIVE。
区别于 {@link #renew}（相对 +N 天）。claw 后台用日期选择器设定到期日时调用。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Body-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|userId|int64|false|No comments found.|-|
|d|int32|false|No comments found.|-|
|ip|string|false|No comments found.|-|
|market|string|false|No comments found.|-|
|vn|string|false|No comments found.|-|
|vc|int32|false|No comments found.|-|
|appsFlyerId|string|false|appsflyer 设备AF唯一ID|-|
|l|string|false|No comments found.|-|
|tokenId|int64|false|待设置的 token id（必填）。|-|
|expireAt|int64|false|绝对到期时间（epoch 毫秒，必填）。|-|

**Request-example:**
```bash
curl -X POST -H "Content-Type: application/json" -H "Authorization:Bearer {{token}}" -i '/openapi/admin/set-expiry' --data '{
  "userId": 0,
  "d": 0,
  "ip": "",
  "market": "",
  "vn": "",
  "vc": 0,
  "appsFlyerId": "",
  "l": "",
  "tokenId": 0,
  "expireAt": 0
}'
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|object|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─id|int64|No comments found.|-|
|└─tokenPrefix|string|No comments found.|-|
|└─ownerName|string|No comments found.|-|
|└─ownerEmail|string|No comments found.|-|
|└─scopes|string|No comments found.|-|
|└─allowedIps|string|No comments found.|-|
|└─allowedPaths|string|单接口级路径白/黑名单 CSV（方案 B）。null/空 = 不限路径。|-|
|└─rateLimitPerMin|int32|No comments found.|-|
|└─status|int8|No comments found.|-|
|└─expireAt|string|No comments found.|-|
|└─lastUsedAt|string|No comments found.|-|
|└─lastUsedIp|string|No comments found.|-|
|└─description|string|No comments found.|-|
|└─createTime|string|No comments found.|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{"code":0,"msg":"","data":{"id":0,"tokenPrefix":"","ownerName":"","ownerEmail":"","scopes":"","allowedIps":"","allowedPaths":"","rateLimitPerMin":0,"status":,"expireAt":"yyyy-MM-dd HH:mm:ss","lastUsedAt":"yyyy-MM-dd HH:mm:ss","lastUsedIp":"","description":"","createTime":"yyyy-MM-dd HH:mm:ss"},"traceId":""}
```

### 增量加 IP 白名单（去重）。claw 后台给 token 放开新来源 IP / CIDR 时调用，秒级生效。
**URL:** /openapi/admin/ip/add

**Type:** POST


**Content-Type:** application/json

**Description:** 增量加 IP 白名单（去重）。claw 后台给 token 放开新来源 IP / CIDR 时调用，秒级生效。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Body-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|userId|int64|false|No comments found.|-|
|d|int32|false|No comments found.|-|
|ip|string|false|No comments found.|-|
|market|string|false|No comments found.|-|
|vn|string|false|No comments found.|-|
|vc|int32|false|No comments found.|-|
|appsFlyerId|string|false|appsflyer 设备AF唯一ID|-|
|l|string|false|No comments found.|-|
|tokenId|int64|false|必填。|-|
|ips|string|false|逗号分隔的 IP / CIDR 列表，如 "1.2.3.4,10.0.0.0/8"。空 / 全空白将被拒绝。|-|

**Request-example:**
```bash
curl -X POST -H "Content-Type: application/json" -H "Authorization:Bearer {{token}}" -i '/openapi/admin/ip/add' --data '{
  "userId": 0,
  "d": 0,
  "ip": "",
  "market": "",
  "vn": "",
  "vc": 0,
  "appsFlyerId": "",
  "l": "",
  "tokenId": 0,
  "ips": ""
}'
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|object|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─id|int64|No comments found.|-|
|└─tokenPrefix|string|No comments found.|-|
|└─ownerName|string|No comments found.|-|
|└─ownerEmail|string|No comments found.|-|
|└─scopes|string|No comments found.|-|
|└─allowedIps|string|No comments found.|-|
|└─allowedPaths|string|单接口级路径白/黑名单 CSV（方案 B）。null/空 = 不限路径。|-|
|└─rateLimitPerMin|int32|No comments found.|-|
|└─status|int8|No comments found.|-|
|└─expireAt|string|No comments found.|-|
|└─lastUsedAt|string|No comments found.|-|
|└─lastUsedIp|string|No comments found.|-|
|└─description|string|No comments found.|-|
|└─createTime|string|No comments found.|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{"code":0,"msg":"","data":{"id":0,"tokenPrefix":"","ownerName":"","ownerEmail":"","scopes":"","allowedIps":"","allowedPaths":"","rateLimitPerMin":0,"status":,"expireAt":"yyyy-MM-dd HH:mm:ss","lastUsedAt":"yyyy-MM-dd HH:mm:ss","lastUsedIp":"","description":"","createTime":"yyyy-MM-dd HH:mm:ss"},"traceId":""}
```

### 增量移除 IP 白名单。移除后为空将被拒绝（防锁死）。
**URL:** /openapi/admin/ip/remove

**Type:** POST


**Content-Type:** application/json

**Description:** 增量移除 IP 白名单。移除后为空将被拒绝（防锁死）。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Body-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|userId|int64|false|No comments found.|-|
|d|int32|false|No comments found.|-|
|ip|string|false|No comments found.|-|
|market|string|false|No comments found.|-|
|vn|string|false|No comments found.|-|
|vc|int32|false|No comments found.|-|
|appsFlyerId|string|false|appsflyer 设备AF唯一ID|-|
|l|string|false|No comments found.|-|
|tokenId|int64|false|必填。|-|
|ips|string|false|逗号分隔的 IP / CIDR 列表，如 "1.2.3.4,10.0.0.0/8"。空 / 全空白将被拒绝。|-|

**Request-example:**
```bash
curl -X POST -H "Content-Type: application/json" -H "Authorization:Bearer {{token}}" -i '/openapi/admin/ip/remove' --data '{
  "userId": 0,
  "d": 0,
  "ip": "",
  "market": "",
  "vn": "",
  "vc": 0,
  "appsFlyerId": "",
  "l": "",
  "tokenId": 0,
  "ips": ""
}'
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|object|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─id|int64|No comments found.|-|
|└─tokenPrefix|string|No comments found.|-|
|└─ownerName|string|No comments found.|-|
|└─ownerEmail|string|No comments found.|-|
|└─scopes|string|No comments found.|-|
|└─allowedIps|string|No comments found.|-|
|└─allowedPaths|string|单接口级路径白/黑名单 CSV（方案 B）。null/空 = 不限路径。|-|
|└─rateLimitPerMin|int32|No comments found.|-|
|└─status|int8|No comments found.|-|
|└─expireAt|string|No comments found.|-|
|└─lastUsedAt|string|No comments found.|-|
|└─lastUsedIp|string|No comments found.|-|
|└─description|string|No comments found.|-|
|└─createTime|string|No comments found.|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{"code":0,"msg":"","data":{"id":0,"tokenPrefix":"","ownerName":"","ownerEmail":"","scopes":"","allowedIps":"","allowedPaths":"","rateLimitPerMin":0,"status":,"expireAt":"yyyy-MM-dd HH:mm:ss","lastUsedAt":"yyyy-MM-dd HH:mm:ss","lastUsedIp":"","description":"","createTime":"yyyy-MM-dd HH:mm:ss"},"traceId":""}
```

### 修改每分钟频率上限。claw 后台单独调整某 token 限频时调用，不动 scope / IP。
**URL:** /openapi/admin/rate-limit

**Type:** POST


**Content-Type:** application/json

**Description:** 修改每分钟频率上限。claw 后台单独调整某 token 限频时调用，不动 scope / IP。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Body-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|userId|int64|false|No comments found.|-|
|d|int32|false|No comments found.|-|
|ip|string|false|No comments found.|-|
|market|string|false|No comments found.|-|
|vn|string|false|No comments found.|-|
|vc|int32|false|No comments found.|-|
|appsFlyerId|string|false|appsflyer 设备AF唯一ID|-|
|l|string|false|No comments found.|-|
|tokenId|int64|false|必填。|-|
|rateLimitPerMin|int32|false|必填。每分钟请求上限，1 ~ 3000。|-|

**Request-example:**
```bash
curl -X POST -H "Content-Type: application/json" -H "Authorization:Bearer {{token}}" -i '/openapi/admin/rate-limit' --data '{
  "userId": 0,
  "d": 0,
  "ip": "",
  "market": "",
  "vn": "",
  "vc": 0,
  "appsFlyerId": "",
  "l": "",
  "tokenId": 0,
  "rateLimitPerMin": 0
}'
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|object|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─id|int64|No comments found.|-|
|└─tokenPrefix|string|No comments found.|-|
|└─ownerName|string|No comments found.|-|
|└─ownerEmail|string|No comments found.|-|
|└─scopes|string|No comments found.|-|
|└─allowedIps|string|No comments found.|-|
|└─allowedPaths|string|单接口级路径白/黑名单 CSV（方案 B）。null/空 = 不限路径。|-|
|└─rateLimitPerMin|int32|No comments found.|-|
|└─status|int8|No comments found.|-|
|└─expireAt|string|No comments found.|-|
|└─lastUsedAt|string|No comments found.|-|
|└─lastUsedIp|string|No comments found.|-|
|└─description|string|No comments found.|-|
|└─createTime|string|No comments found.|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{"code":0,"msg":"","data":{"id":0,"tokenPrefix":"","ownerName":"","ownerEmail":"","scopes":"","allowedIps":"","allowedPaths":"","rateLimitPerMin":0,"status":,"expireAt":"yyyy-MM-dd HH:mm:ss","lastUsedAt":"yyyy-MM-dd HH:mm:ss","lastUsedIp":"","description":"","createTime":"yyyy-MM-dd HH:mm:ss"},"traceId":""}
```

### 按 id 读取 token 元信息（scope / 到期 / 状态 / 频率等，无明文）。<br>claw 后台&amp;quot;从 stock 刷新&amp;quot;对账用 —— 以 stock 为权威源回灌本地镜像。
**URL:** /openapi/admin/token/{id}

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 按 id 读取 token 元信息（scope / 到期 / 状态 / 频率等，无明文）。
claw 后台"从 stock 刷新"对账用 —— 以 stock 为权威源回灌本地镜像。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Path-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|id|int64|true|token id|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/admin/token/{id}'
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|object|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─id|int64|No comments found.|-|
|└─tokenPrefix|string|No comments found.|-|
|└─ownerName|string|No comments found.|-|
|└─ownerEmail|string|No comments found.|-|
|└─scopes|string|No comments found.|-|
|└─allowedIps|string|No comments found.|-|
|└─allowedPaths|string|单接口级路径白/黑名单 CSV（方案 B）。null/空 = 不限路径。|-|
|└─rateLimitPerMin|int32|No comments found.|-|
|└─status|int8|No comments found.|-|
|└─expireAt|string|No comments found.|-|
|└─lastUsedAt|string|No comments found.|-|
|└─lastUsedIp|string|No comments found.|-|
|└─description|string|No comments found.|-|
|└─createTime|string|No comments found.|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{"code":0,"msg":"","data":{"id":0,"tokenPrefix":"","ownerName":"","ownerEmail":"","scopes":"","allowedIps":"","allowedPaths":"","rateLimitPerMin":0,"status":,"expireAt":"yyyy-MM-dd HH:mm:ss","lastUsedAt":"yyyy-MM-dd HH:mm:ss","lastUsedIp":"","description":"","createTime":"yyyy-MM-dd HH:mm:ss"},"traceId":""}
```

### 列出全部数据维度（scope）元数据，供 claw 后台 scope 多选 UI 渲染。
**URL:** /openapi/admin/scopes

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 列出全部数据维度（scope）元数据，供 claw 后台 scope 多选 UI 渲染。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/admin/scopes'
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─name|string|scope 全名，如 "stock.kline" / "stock.minute"。|-|
|└─description|string|中文说明，如 "日/周/月 K 线、复权因子、多周期涨跌幅"。|-|
|└─minPlan|string|最低套餐档位（包含该 scope 的最低档）：free / pro / max / plus / ultra。|-|
|└─tableCount|int32|该 scope 覆盖的 PG 表数量（参考值）。|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "name": "",
      "description": "",
      "minPlan": "",
      "tableCount": 0
    }
  ],
  "traceId": ""
}
```

### 列出全部套餐档位元数据（含各档 scope 集合 + 推荐频率），供 claw 后台档位下拉 + 预设用。
**URL:** /openapi/admin/plans

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 列出全部套餐档位元数据（含各档 scope 集合 + 推荐频率），供 claw 后台档位下拉 + 预设用。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/admin/plans'
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─name|string|套餐名：free / pro / max / plus / ultra。|-|
|└─description|string|中文说明：例如 "免费版 · 仅基础行情" / "Pro · 加技术指标 + 财务报表"。|-|
|└─scopes|array|该套餐包含的 scope 列表（应用后整体覆盖 token.scopes）。|-|
|└─defaultRateLimitPerMin|int32|推荐默认每分钟频率上限。|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "name": "",
      "description": "",
      "scopes": [
        ""
      ],
      "defaultRateLimitPerMin": 0
    }
  ],
  "traceId": ""
}
```

## OpenAPI v1 —— 外汇数据全量端点（{@code forex} scope，Max 套餐及以上）。

&lt;p&gt;覆盖 2 张 PG 表的 2 个端点：
&lt;ul&gt;
  &lt;li&gt;{@code POST /openapi/v1/forex/obasic} — 外汇产品基础信息（forex_obasic）&lt;/li&gt;
  &lt;li&gt;{@code POST /openapi/v1/forex/daily}  — 外汇日线行情（forex_daily）&lt;/li&gt;
&lt;/ul&gt;

&lt;p&gt;数据来源：Tushare {@code fx_obasic} / {@code fx_daily} 接口（海外外汇 / CFD）。
### 外汇产品基础信息（{@code forex_obasic}）。<br><br>海外外汇 / CFD 产品的元数据：产品分类、交易商、最小 / 最大交易单位、<br>点 / 点值、目标点差、最小止损距离、交易时段、休市时段。<br>可按 {@code tsCode} / {@code classify} / {@code exchange} 任意组合过滤；<br>全部为空时按 {@code ts_code} 升序返回前 N 行。
**URL:** /openapi/v1/forex/obasic

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 外汇产品基础信息（{@code forex_obasic}）。

<p>海外外汇 / CFD 产品的元数据：产品分类、交易商、最小 / 最大交易单位、
点 / 点值、目标点差、最小止损距离、交易时段、休市时段。
<p>可按 {@code tsCode} / {@code classify} / {@code exchange} 任意组合过滤；
全部为空时按 {@code ts_code} 升序返回前 N 行。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|page|int32|false|第几页，从 1 起。默认 1。0 / 负数会被当成 1。|-|
|size|int32|false|每页记录数。默认 50，硬上限 {@value #MAX_SIZE}。<br/><p>传入超过 {@value #MAX_SIZE} 时会被自动截断到 {@value #MAX_SIZE}（不报错）。</p>|-|
|tsCode|string|false|外汇代码，如 {@code "USDCNH.FXCM"} / {@code "EURUSD.FXCM"}。可空。|-|
|startDate|string|false|起始日期，格式 {@code YYYYMMDD}。可空（仅 daily 端点用）。|-|
|endDate|string|false|结束日期，格式 {@code YYYYMMDD}。可空（仅 daily 端点用）。|-|
|classify|string|false|分类（仅 obasic 端点用）：如 {@code "FX"} 外汇 / {@code "CFD"} 差价合约。可空。|-|
|exchange|string|false|交易商（仅 obasic 端点用）：如 {@code "FXCM"} / {@code "OANDA"}。可空。|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/forex/obasic?page=0&size=0&classify=&tsCode=&startDate=&endDate=&exchange='
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─tsCode|string|外汇代码（如 USDCNH.FXCM / EURUSD.FXCM）|-|
|└─name|string|名称|-|
|└─classify|string|分类（如 FX 外汇 / CFD 差价合约）|-|
|└─exchange|string|交易商（如 FXCM / OANDA）|-|
|└─minUnit|number|最小交易单位|-|
|└─maxUnit|number|最大交易单位|-|
|└─pip|number|点|-|
|└─pipCost|number|点值|-|
|└─targetSpread|number|目标点差|-|
|└─minStopDistance|number|最小止损距离|-|
|└─tradingHours|string|交易时间|-|
|└─breakTime|string|休市时间|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "tsCode": "",
      "name": "",
      "classify": "",
      "exchange": "",
      "minUnit": 0,
      "maxUnit": 0,
      "pip": 0,
      "pipCost": 0,
      "targetSpread": 0,
      "minStopDistance": 0,
      "tradingHours": "",
      "breakTime": ""
    }
  ],
  "traceId": ""
}
```

### 外汇日线行情（{@code forex_daily}）。<br><br>双边报价（bid 买价 / ask 卖价）的日 OHLC + 报价笔数 + 交易所。<br>{@code tsCode} 建议必填（不传则跨产品按 trade_date DESC 列），<br>{@code startDate} / {@code endDate} 可空，按 {@code YYYYMMDD}。<br>点差（spread）= ask_close − bid_close，由调用方按需计算。
**URL:** /openapi/v1/forex/daily

**Type:** GET


**Content-Type:** application/x-www-form-urlencoded

**Description:** 外汇日线行情（{@code forex_daily}）。

<p>双边报价（bid 买价 / ask 卖价）的日 OHLC + 报价笔数 + 交易所。
<p>{@code tsCode} 建议必填（不传则跨产品按 trade_date DESC 列），
{@code startDate} / {@code endDate} 可空，按 {@code YYYYMMDD}。
<p>点差（spread）= ask_close − bid_close，由调用方按需计算。

**Request-headers:**

| Header | Type | Required | Description | Since |
|--------|------|----------|-------------|-------|
|Authorization|string|true|Bearer 认证令牌|-|


**Query-parameters:**

| Parameter | Type | Required | Description | Since |
|-----------|------|----------|-------------|-------|
|page|int32|false|第几页，从 1 起。默认 1。0 / 负数会被当成 1。|-|
|size|int32|false|每页记录数。默认 50，硬上限 {@value #MAX_SIZE}。<br/><p>传入超过 {@value #MAX_SIZE} 时会被自动截断到 {@value #MAX_SIZE}（不报错）。</p>|-|
|tsCode|string|false|外汇代码，如 {@code "USDCNH.FXCM"} / {@code "EURUSD.FXCM"}。可空。|-|
|startDate|string|false|起始日期，格式 {@code YYYYMMDD}。可空（仅 daily 端点用）。|-|
|endDate|string|false|结束日期，格式 {@code YYYYMMDD}。可空（仅 daily 端点用）。|-|
|classify|string|false|分类（仅 obasic 端点用）：如 {@code "FX"} 外汇 / {@code "CFD"} 差价合约。可空。|-|
|exchange|string|false|交易商（仅 obasic 端点用）：如 {@code "FXCM"} / {@code "OANDA"}。可空。|-|

**Request-example:**
```bash
curl -X GET -H "Authorization:Bearer {{token}}" -i '/openapi/v1/forex/daily?page=0&size=0&classify=&startDate=&tsCode=&endDate=&exchange='
```
**Response-fields:**

| Field | Type | Description | Since |
|-------|------|-------------|-------|
|code|int32|业务状态码。<br/><ul><br/>  <li>{@code 0} / {@code 200} —— 成功</li><br/>  <li>其他 —— 失败，具体语义见 {@link #msg}</li><br/></ul>|-|
|msg|string|状态描述。成功时通常 {@code "success"}；失败时是中文错误信息（如"参数缺失"/"token 无效"等）。|-|
|data|array|业务数据载体。成功时按各端点契约填充；失败时通常为 null。|-|
|└─tsCode|string|外汇代码|-|
|└─tradeDate|string|交易日|-|
|└─bidOpen|number|买报价开盘价|-|
|└─bidClose|number|买报价收盘价|-|
|└─bidHigh|number|买报价最高价|-|
|└─bidLow|number|买报价最低价|-|
|└─askOpen|number|卖报价开盘价|-|
|└─askClose|number|卖报价收盘价|-|
|└─askHigh|number|卖报价最高价|-|
|└─askLow|number|卖报价最低价|-|
|└─tickQty|int64|报价笔数|-|
|└─exchange|string|交易所|-|
|traceId|string|服务端为本次请求分配的全局唯一 traceId。<br/><p>失败排查时把这个值给后端管理员，可在服务端日志快速定位。</p>|-|

**Response-example:**
```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "tsCode": "",
      "tradeDate": "yyyy-MM-dd HH:mm:ss",
      "bidOpen": 0,
      "bidClose": 0,
      "bidHigh": 0,
      "bidLow": 0,
      "askOpen": 0,
      "askClose": 0,
      "askHigh": 0,
      "askLow": 0,
      "tickQty": 0,
      "exchange": ""
    }
  ],
  "traceId": ""
}
```


