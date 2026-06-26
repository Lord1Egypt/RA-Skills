
# 天天基金信息skill


通过**自然语言**或结构化参数调用 `FUND_BASE_INFOS` 对应能力，接口返回 JSON 格式内容。


- 当前 skill 版本：`1.0.0`


## 使用方式


1. 在调用任何接口前，必须先检查本地环境变量 `TTFUND_APIKEY` 是否存在。
2. 若本地已存在 `TTFUND_APIKEY`，则直接使用该 apikey 发起请求。
3. 若本地不存在 `TTFUND_APIKEY`，必须强制引导用户先配置 apikey，不得跳过。
4. apikey 获取路径：
   - 打开 **天天基金**
   - 搜索 **skills**
   - 在对应 Skills 页面获取 `天天基金信息skill` 对应的 apikey
5. 当检测到 apikey 缺失时，必须明确提示用户：
   - `当前未检测到本地环境变量 TTFUND_APIKEY，请先前往天天基金搜索 skills 获取 apikey，并在本机配置环境变量后再继续使用。`
6. 在用户未完成 apikey 配置前，不继续执行 skill 查询请求。
7. 配置完成后，使用 **POST** 请求调用统一网关接口，并将 apikey 放入 `X-API-Key` 请求头中。
8. 每次请求体都必须同时携带 `skill_id` 和 `_skill_version`。
9. `_skill_version` 必须填写当前安装版本：`1.0.0`。


编写调用方式脚本


```bash
curl --location 'https://skills.tiantianfunds.com/ai-smart-skill-service/openapi/skill/invoke' \
--header "X-API-Key: $TTFUND_APIKEY" \
--header 'Content-Type: application/json' \
--data '{
  "skill_id": "FUND_BASE_INFOS",
  "_skill_version": "1.0.0",
  "fcode": "000006"
}'
```


如果当前底层接口未强制校验 apikey，也必须先检查并要求配置 `TTFUND_APIKEY`，不可省略该步骤。


## 请求参数说明


以下表格说明统一网关接收的请求字段及其与下游接口字段的映射关系；`fixed` 表示系统自动注入，`context` 表示平台上下文注入。


| 请求字段 | 下游字段 | 来源 | 类型 | 必填 | 说明 | 示例/默认值 |
|----|----|----|----|----|----|----|
| `fcode` | `FCODES` | `query` | `string` | 是 | 基金代码，例如 000006 | `000006` |
| `fields` | `FIELDS` | `fixed` | `string` | 是 | 固定查询字段列表；系统自动注入 | `JJGS,ESTDIFF,FEGMRQ,TTYPE,YDDT_FY,ESTABDATE,SHRATE7,ISZHDT,DWJZ,ISSBDATE,MBDT_Y,TSRQ,TTYPENAME,MBDT_TRY,ABNORMALDATE,BTYPE,SOURCERATE,SYL_LN,DWDT_TRY,RZDF,PTDT_TRY,YDDT_TRY,NEWINDEXTEXCH,ETFCODE,RSFUNDTYPE,MAXRGINVESTED,DWDT_Y,INDEXNAME,FTYPE,DISCOUNT,LINKZSB,ENDNAV,RATE,PTDT_Y,FCODE,YDDT_Y,FUNDEXCHG,LJJZ,NEWTEXCH,BENCH_CORR,ISABNORMAL_NDATE,MBDT_TWY,FSRQ,RLEVEL_SZ,INDEXCODE,TRKERROR,RLEVEL_CX,BENCHCODE,DWDT_TWY,TJDLIST,MBDT_FY,PTDT_TWY,YDDT_TWY,BFUNDTYPE,DWDT_FY,BAGTYPE,ISSEDATE,SHORTNAME,CYCLE,FEATURE,SHRATE30,RISKLEVEL,SYL_1N,SYL_Z,RSBTYPE,BENCH,MINRG,BESTDT_STRATEGY,MAXSG,PTDT_FY,JJGSID,STDDEV1,MAXRETRA1` |


## 问句示例


| 类型 | query |
|----|----|
| 查询 天天基金信息skill | 帮我调用 FUND_BASE_INFOS |
| 按示例参数调用 | 使用 FUND_BASE_INFOS，参数参考请求示例 |
| 查询结果解释 | 帮我读取 FUND_BASE_INFOS 的返回结果并解释关键字段 |


## 接口结果释义


### 一、根节点 (Root Level)


这些是接口最外层的通用状态响应字段。


| 字段路径 | 类型 | 核心释义 |
|----|----|----|
| `data` | array | 核心业务数据 |
| `errorCode` | number | 接口全局错误码，0 = 成功 |
| `firstError` | null | 首个错误信息，失败时用于定位问题 |
| `success` | boolean | 接口是否成功，true = 成功 |
| `hasWrongToken` | null | 鉴权异常标记 |
| `totalCount` | number | 返回结果数量 |
| `expansion` | null | 扩展字段 |
| `jf` | string | 来源标识 |


### 二、核心字段说明


| 字段 Key | 含义说明 |
| --- | --- |
| `success` | 接口是否成功；true 表示接口调用成功 |
| `errorCode` | 错误码；0 表示成功，非 0 表示失败 |
| `totalCount` | 返回基金数量；本接口通常按基金代码返回对应基金条数 |
| `data.FCODE` | 基金代码列表；用于确认返回的基金代码 |
| `data.SHORTNAME` | 基金简称列表；用于展示基金名称 |
| `data.FTYPE` | 基金类型列表；用于识别基金属于偏股、偏债、指数等类型 |
| `data.JJGS` | 基金公司列表；用于展示基金管理人 |
| `data.DWJZ` | 单位净值列表；用于查看基金当前净值 |
| `data.LJJZ` | 累计净值列表；用于查看基金累计净值表现 |
| `data.RISKLEVEL` | 风险等级列表；用于判断基金风险等级 |
| `data.RLEVEL_SZ` | 基金风险等级（字段一）；用于补充风险标识 |
| `data.RLEVEL_CX` | 基金风险等级（字段二）；用于补充风险标识 |
| `data.ESTABDATE` | 基金成立日期列表；用于判断基金成立时间长短 |
| `data.FSRQ` | 净值日期列表；用于确认当前净值对应日期 |
| `data.RATE` | 当前费率列表；用于查看当前申购费率 |
| `data.SOURCERATE` | 原始费率列表；用于查看原始申购费率 |
| `data.SYL_Z` | 近一周收益率列表；用于评估短期表现 |
| `data.SYL_1N` | 近一年收益率列表；用于评估中期表现 |
| `data.SYL_LN` | 成立以来收益率列表；用于评估长期累计收益表现 |
| `data.STDDEV1` | 波动率列表；用于评估基金波动水平 |
| `data.MAXRETRA1` | 最大回撤列表；用于评估基金回撤风险 |
| `data.ESTDIFF` | 平均估算偏差 |
| `data.FEGMRQ` | 最新净资产日期（净值） |
| `data.TTYPE` | 主题id（主题占比最高一个） |
| `data.YDDT_FY` | 移动止盈定投近5年收益 |
| `data.SHRATE7` | 大于7天的赎回费（指数基金） |
| `data.ISZHDT` | 是否智慧定投（低位多投） |
| `data.ISSBDATE` | 认购起始日期 |
| `data.MBDT_Y` | 目标止盈定投近1年收益 |
| `data.TSRQ` | 退市日期 |
| `data.TTYPENAME` | 主题名称（主题占比最高一个） |
| `data.MBDT_TRY` | 目标止盈定投近3年收益 |
| `data.ABNORMALDATE` | 最近一次异常涨幅时间 |
| `data.BTYPE` | 二级分类 |
| `data.DWDT_TRY` | 低位多投定投近3年收益 |
| `data.RZDF` | 日涨跌幅 |
| `data.PTDT_TRY` | 普通定投近3年收益 |
| `data.YDDT_TRY` | 移动止盈定投近3年收益 |
| `data.NEWINDEXTEXCH` | 跟踪指数新市场 |
| `data.ETFCODE` | ETF联接对应ETF基金 |
| `data.RSFUNDTYPE` | 一级分类 （研究） |
| `data.MAXRGINVESTED` | 最大认购 |
| `data.DWDT_Y` | 低位多投定投近1年收益 |
| `data.INDEXNAME` | 指数名称 |
| `data.DISCOUNT` | 折扣 |
| `data.LINKZSB` | 是否跳转指数宝3.0 |
| `data.ENDNAV` | 最新净资产（净值） |
| `data.PTDT_Y` | 普通定投近1年收益 |
| `data.YDDT_Y` | 移动止盈定投近1年收益 |
| `data.FUNDEXCHG` | 超级转换（含QDII）（890IN） |
| `data.NEWTEXCH` | 场内基金新市场号 |
| `data.BENCH_CORR` | 日收益相关性 |
| `data.ISABNORMAL_NDATE` | 异常涨幅（非公告类)时间 |
| `data.MBDT_TWY` | 目标止盈定投近2年收益 |
| `data.INDEXCODE` | 指数代码 |
| `data.TRKERROR` | 跟踪误差 |
| `data.BENCHCODE` | 业绩基准指数 |
| `data.DWDT_TWY` | 低位多投定投近2年收益 |
| `data.TJDLIST` | 支持条件单类型列表 多个逗号分开 |
| `data.MBDT_FY` | 目标止盈定投近5年收益 |
| `data.PTDT_TWY` | 普通定投近2年收益 |
| `data.YDDT_TWY` | 移动止盈定投近2年收益 |
| `data.BFUNDTYPE` | 基金新类型 |
| `data.DWDT_FY` | 低位多投定投近5年收益 |
| `data.BAGTYPE` | 是否宝类基金 |
| `data.ISSEDATE` | 认购截止日期 |
| `data.CYCLE` | 运作周期（封闭期，无封闭期的为存续期）（PC品种页展示） |
| `data.FEATURE` | 基金属性 |
| `data.SHRATE30` | 30天的赎回费率 |
| `data.RSBTYPE` | 二级分类（研究） |
| `data.BENCH` | 业绩比较基准 |
| `data.MINRG` | 首次认购最低额 |
| `data.BESTDT_STRATEGY` | 最佳定投策略 |
| `data.MAXSG` | 最大申购限额 |
| `data.PTDT_FY` | 普通定投近5年收益 |
| `data.JJGSID` | 基金公司id |


## 交互规范


1. 优先检查环境变量 `TTFUND_APIKEY`。
2. 若环境变量存在，则直接继续调用接口。
3. 若环境变量不存在，必须中断当前调用，并强制提示用户先完成 apikey 配置。
4. 引导文案必须明确包含：
   - 环境变量名：`TTFUND_APIKEY`
   - apikey 获取路径：`天天基金搜索 skills`
5. 每次请求都必须带上 `skill_id` 和 `_skill_version`。
6. `_skill_version` 固定使用当前安装版本：`1.0.0`。
7. 若缺少必填参数，应提示用户补充 `fcode`。
8. 返回结果时，应优先提炼核心信息，而不是直接原样堆砌所有字段。
9. 结果解释顺序必须是：先看业务结果，再看 `version_info`，最后决定是否追加升级建议。


## 输出建议


返回时优先展示：
- `success`
- `errorCode`
- `totalCount`
- `data.FCODE`
- `data.SHORTNAME`
- `data.FTYPE`
- `data.JJGS`
- `data.DWJZ`


如需结构化输出，建议包含两部分：


- `raw_result`：原始接口返回
- `explanation_document`：对关键字段和结果差异的说明
- `version_info`：版本状态与升级提示（若返回）


后处理要求：


- 若 `data.version_info.is_outdated = true`，先完成本次结果回答，再附上一句简洁升级提醒。
- 若接口返回升级导向错误，不要重复盲重试，也不要误判为普通网络问题，应直接提示用户升级 skill。
- 若接口返回普通业务错误且没有版本归因信号，则按原有逻辑处理，不额外渲染升级提示。


## 错误处理


- 若缺少 apikey，应提示用户：
  - `当前未检测到 TTFUND_APIKEY，请先前往天天基金搜索 skills 获取 apikey，并在本机配置该环境变量后重试。`
- 若缺少 `_skill_version`，应提示用户：
  - `当前安装的 skill 可能为旧版本，未携带版本信息。请升级到最新版本 1.0.0 后重试。`
- 若 `_skill_version` 为空或无效，应提示用户：
  - `当前安装的 skill 版本信息无效，可能为旧版本或安装不完整。请升级到最新版本 1.0.0 后重试。`
- 若 HTTP 请求失败、超时或返回非 2xx 状态码，应提示用户：
  - `天天基金信息skill服务暂时不可用，请稍后重试。`
- 若返回 `version_info` 表示本地版本落后，应优先提示用户尽快升级 skill。
- 若版本落后且本次错误属于参数缺失、字段不兼容或调用协议不匹配，应优先提示用户先升级 skill 再重试。
- 若业务成功字段 `errorCode` 校验失败，则视为业务失败：
  - 简要说明错误信息
  - 不自行猜测结果或伪造成功
- 若核心返回数据为空，应提示用户检查输入参数是否正确。


## 安全与边界


- 该 Skill 返回的是 `天天基金信息skill` 对应的业务数据，请按业务场景谨慎使用。
- 返回内容仅用于当前用户请求的查询与分析，不应伪造结果或输出未验证内容。
