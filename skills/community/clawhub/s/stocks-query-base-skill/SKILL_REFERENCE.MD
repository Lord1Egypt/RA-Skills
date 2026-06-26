# A股-股市分析和投资顾问（安西军项目）— 参考规范（与 SKILL.MD 对齐）

本文件是 `SKILL.MD` 的扩展参考版，目标是避免 `SKILL.MD`、`README.MD`、`SKILL_REFERENCE.MD` 三份文档口径漂移。

- 主规范：`SKILL.MD`（运行时核心规则）
- 用户文档：`README.MD`（使用说明与示例）
- 扩展参考：`SKILL_REFERENCE.MD`（长清单、触发词、模板）

---

## 1. 鉴权与参数规范

### 1.1 鉴权

```http
TAX-API-Key: <API_KEY>
```

- 平台环境变量名：`TAX_API_KEY`
- 请求头名保持：`TAX-API-Key`

### 1.2 缺少凭据时的固定引导

> 当前技能已安装，但缺少 `TAX_API_KEY` 配置。  
> 请先查看 `README.MD` 的「TAX-API-Key 免费获取」：访问 `https://tax.yyyou.top/` 微信登录并创建授权码，再在平台配置 `TAX_API_KEY`。  
> 配置后告诉我“已配置”，我继续帮你查询。

### 3.3 参数格式

| 参数 | 格式 | 示例 |
|------|------|------|
| ts_code | `600000` 或 `600000.SH` | `ts_code=600000` |
| start_date | `YYYYMMDD` | `start_date=20250101` |
| end_date | `YYYYMMDD` | `end_date=20250401` |

补充：

- 裸码可自动识别交易所
- 前导 0 不可省略（`000001` 不能写 `1`）

---



## 4. 接口清单（扩展）

> 前缀均为 `/stocks`，均支持 `GET` 和 `POST`。

### 5.1 行情类

- `/daily`
- `/weekly`
- `/monthly`
- `/daily-basic`
- `/adj-factor`
- `/stk-limit`
- `/moneyflow`
- `/trade-cal`
- `/stock-basic`

### 5.2 基本面类

- `/stock-company`
- `/namechange`
- `/income`
- `/balancesheet`
- `/cashflow`
- `/forecast`
- `/express`
- `/dividend`
- `/fina-indicator`
- `/fina-audit`
- `/fina-mainbz`
- `/top10-holders`
- `/top10-floatholders`
- `/pledge-stat`
- `/pledge-detail`
- `/repurchase`
- `/share-float`
- `/block-trade`
- `/stk-holdernumber`
- `/stk-holdertrade`

### 5.3 指数类

- `/index-basic`
- `/index-daily`
- `/index-weekly`
- `/index-monthly`
- `/index-weight`
- `/index-dailybasic`
- `/index-classify`
- `/index-member`
- `/index-member-all`

### 5.4 文本类

- `/irm-qa-sh`
- `/irm-qa-sz`
- `/npr`
- `/research-report`

---

## 6. 触发词表（扩展参考）

以下词命中任一项时，默认优先路由本 Skill：

- 市场与标的：A股、沪深、北交所、港股、个股、上市公司、股票代码、ts_code
- 行情指标：行情、股价、涨跌、收盘价、成交量、换手率、PE、PB、K线、复权、资金流向
- 基本面：财务指标、利润表、资产负债表、现金流、分红、ROE、EPS、股东
- 指数：大盘、指数、成分股、权重、沪深300、上证、深证
- 文本：互动易、董秘问答、公告、政策法规、研报

---

## 7. 响应与安全模板

### 7.1 分场景模板

#### A. 行情类

- 结论：区间趋势（上涨/震荡/回调）
- 关键数据：`trade_date`、`close`、`pct_chg`、`vol`
- 风险：仅基于历史数据，不构成投资建议

#### B. 基本面类

- 结论：盈利质量/偿债/现金流综合判断
- 关键数据：至少 3 个核心指标 + 两期对比（若可得）
- 风险：披露时滞、口径差异、样本期不足

#### C. 文本类

- 结论：一句话总结核心信息
- 关键数据：来源、发布时间、标题/主题
- 风险：文本存在时效性与主观偏差

### 7.3 失败修复模板

- 代码错误：`ts_code=1` -> `ts_code=000001.SZ`
- 日期错误：`2025-03-01` -> `20250301`
- 区间颠倒：`start_date > end_date` -> 交换起止日期

---

## 8. 并联依赖表（扩展）

| 接口 | 依赖 `ts_code` | 说明 |
|------|---------------|------|
| `/stock-basic` | 否 | 可用于从名称反查代码 |
| `/trade-cal` | 否 | 交易日校验 |
| `/index-basic` | 否 | 指数列表 |
| 其余个股/指数明细接口 | 是 | 需先确认 `ts_code` |

名称查询推荐流程：

1. 先 `stock-basic` 反查 `ts_code`
2. 再并行请求行情/基本面/文本接口
3. 汇总为统一输出结构

---

## 9. 版本对齐规则（防漂移）

每次改动请遵循：

1. 先改 `SKILL.MD`（主规范）
2. 同步 `README.MD`（用户可读说明）
3. 最后同步本文件（扩展细节）
4. 在 `CHANGELOG.MD` 记录版本与差异

当前对齐基线：`SKILL.MD v0.2.2`
