---
name: a-stock
version: "1.0.0"
homepage: https://github.com/wwzzsl/skills.git
license: MIT

# 必需的环境变量（运行前必须配置）
env:
  required:
    - name: ASTOCK_API_KEY
      description: "A股 API 密钥，从 https://aipmedia.cn/ 个人中心获取"
      secret: true

# 运行时依赖
runtime:
  requires:
    - node  # Node.js >= 18（内置 fetch API）
    - npx   # 用于执行 tsx
  scripts:
    - path: scripts/api-client.ts
      runner: "npx tsx"
      description: "A股接口 HTTP 客户端，仅访问 api.aipmedia.cn"

# 网络访问声明
network:
  allowed_hosts:
    - api.aipmedia.cn

description: A股金融数据查询与分析助手。当用户询问任何与A股相关的问题时，使用此技能——包括：查询个股信息、实时行情、分时走势、龙虎榜、行业板块、盘口异动、市场总貌等。触发词包括但不限于：股票、A股、沪市、深市、行情、涨停、跌停、板块、龙虎榜、盘口异动、个股、股价、总市值、证券，或任何带有6位股票代码的查询（如 600519、000001）。即使用户没有明确说"查股票"，只要问题涉及股市数据，都应使用此 Skill。【重要】所有接口调用必须使用 `npx tsx ~/.gemini/skills/a-stock-skill/scripts/api-client.ts`，严禁使用 curl。
---

# A股金融数据 Skill

## 🚫 调用方式硬性规定

> **严禁使用 `curl` 调用接口。唯一允许的调用方式是：
>
> - ✅ `npx tsx ~/.gemini/skills/a-stock-skill/scripts/api-client.ts /api/stock/...` — 正确
> 
> api-client.ts 会自动从 `.env` 文件或环境变量读取 `ASTOCK_API_KEY`，无需在命令行传入 apiKey。

## 概述

此 Skill 帮助用户查询 A 股各类金融数据，并以清晰易读的格式展示结果。

**API Base URL**: `https://api.aipmedia.cn`  
**认证方式**: 请求 Header 中传入 `apiKey`，用户需前往 https://aipmedia.cn/ 个人中心查看自己的 apiKey。

---

## ⚠️ 核心约束（必须遵守）

**所有 A 股数据必须通过下方 API 接口获取，严禁使用 Google Search、网页搜索或训练数据中的历史行情作为答案。**

- ✅ 正确：用 `bash_tool` 执行 TypeScript 脚本调用 `https://api.aipmedia.cn/api/stock/...`
- ❌ 错误：调用搜索引擎查询行情、引用训练数据中的股价、给出"大约/估计"的数字

如果接口调用失败，明确告知用户失败原因，不要用搜索结果替代。

### apiKey 配置规则

执行前必须检查 apiKey 是否可用，优先级如下：
1. 项目根目录 `.env` 文件中的 `ASTOCK_API_KEY`
2. 系统环境变量 `ASTOCK_API_KEY`
3. **以上均无** → 停止调用，告知用户：
   > ❌ 未找到 API Key，请前往 [https://aipmedia.cn/](https://aipmedia.cn/) 登录后在「个人中心」查看 API Key，然后在项目根目录创建 `.env` 文件并添加：`ASTOCK_API_KEY=你的apiKey`

---

## 工作流程

1. **理解用户意图** → 判断属于哪个查询模块（见下方模块说明）
2. **收集必要参数** → 股票代码、日期、板块名称等（若缺失，向用户询问）
3. **用 `bash_tool` 执行 TypeScript 脚本** → 调用 `scripts/api-client.ts`（见下方调用示例）
4. **解析并展示** → 将返回的 JSON 数据格式化为 Markdown 表格
5. **提供解读** → 结合金融知识，给出简明的数据解读

---

## 模块一：市场总貌

### 上交所股票数据总貌
- **接口**: `GET /api/stock/sse_summary`
- **说明**: 返回最近交易日的沪市股票数据（收盘后统计）
- **参数**: 无必填（可传 `lng: zh` 或 `en`）
- **真实返回结构**: 按项目分行，列为 股票（整体）/ 主板 / 科创板
  - 项目包括：上市公司数、上市股票数、总市值、流通市值、总股本、流通股本、平均市盈率
- **展示重点**: 用三列表格（股票整体/主板/科创板）呈现各项指标，金额换算为亿元，并解读主板/科创板估值差异

### 深交所证券类别统计
- **接口**: `GET /api/stock/szse_summary`
- **说明**: 深市按日期查询
- **必填参数**: `date`（格式：YYYY-MM-DD，如 `2024-01-15`）
- **展示重点**: item/value 键值对，格式化为表格

---

## 模块二：个股查询

> 股票代码格式示例：上交所 `600519`（贵州茅台），深交所 `000001`（平安银行）

### 个股基本信息（东财）
- **接口**: `GET /api/stock/individual_info_em?symbol=<代码>`
- **展示重点**: 公司名称、行业、上市日期、总股本、流通股本等 item/value 键值对

### 个股基本信息（雪球）
- **接口**: `GET /api/stock/individual_basic_info_xq?symbol=<代码>`
- **展示重点**: 与东财互补，包含行业分类代码（ind_code）和行业名称（ind_name）
- ⚠️ **注意**: 此接口依赖雪球数据源，若返回 500，说明雪球服务暂时不可用，改用东财接口代替

### 行情报价（东财）
- **接口**: `GET /api/stock/bid_ask_em?symbol=<代码>`
- **展示重点**: 买卖五档报价、委比、委差等

### 个股实时行情

**调用优先级：先调主接口，主接口成功则不再调备用接口。**

- **主接口（东财，稳定）**: `GET /api/stock/individual_info_em?symbol=<代码>`
  - 已验证可用，返回最新价、涨跌幅、成交量、成交额、换手率、市盈率、总市值等完整行情
  - 数据格式：`[{item, value}]` 键值对数组

- **备用接口（雪球，不稳定）**: `GET /api/stock/individual_spot?symbol=<代码>`
  - ⚠️ 依赖雪球内部服务，当前存在 500 报错风险（服务端问题，非客户端问题）
  - 仅在主接口数据不完整时尝试，失败则告知用户：雪球数据源暂时不可用，已展示东财数据

### 分时行情（沪深京A股）
- **接口**: `GET /api/stock/zh_a_hist_min_em`
- **参数**: `symbol`、`start_date`（YYYY-MM-DD HH:MM:SS）、`end_date`、`adjust`（复权方式：`qfq`前复权 / `hfq`后复权 / 空字符串不复权）
- **展示重点**: 时间、开盘、收盘、最高、最低、成交量

---

## 模块三：板块分析

### 行业板块列表（东财）
- **接口**: `GET /api/stock/board_industry_name_em`
- **展示重点**: 板块排名、涨跌幅、总市值、涨跌家数、领涨股

### 行业板块实时行情（东财）
- **接口**: `GET /api/stock/board_industry_spot_em?symbol=<板块名称>`
- **参数说明**: `symbol` 为板块中文名称，例如 `小金属`、`半导体`、`新能源车`
- **展示重点**: 当前报价、涨跌幅等 item/value 数据

---

## 模块四：异动监控

### 龙虎榜详情（东财）
- **接口**: `GET /api/stock/lhb_detail_em`
- **参数**: `start_date`、`end_date`（YYYY-MM-DD）
- **展示重点**: 股票代码/名称、上榜原因（rankingReason）、龙虎榜净买额、买卖金额、后续1/2/5/10日涨跌幅

### 盘口异动（东财）
- **接口**: `GET /api/stock/changes_em?symbol=<异动类型>`
- **参数说明**: symbol 为异动类型，枚举值如下：
  - 看多信号：`火箭发射`、`快速反弹`、`大笔买入`、`封涨停板`、`有大买盘`、`竞价上涨`、`高开5日线`、`向上缺口`、`60日新高`、`60日大幅上涨`
  - 看空信号：`加速下跌`、`高台跳水`、`大笔卖出`、`封跌停板`、`有大卖盘`、`竞价下跌`、`低开5日线`、`向下缺口`、`60日新低`、`60日大幅下跌`
  - 其他：`打开跌停板`、`打开涨停板`
- **展示重点**: 时间、股票代码/名称、所属板块、异动详情

---

## 调用示例（bash_tool — 每次查询都必须执行此步骤）

**每次用户提问涉及 A 股数据，必须先用 bash_tool 执行 TypeScript 脚本，再回答。**

### 首次使用：配置 apiKey

```bash
# 在项目根目录创建 .env 文件（只需配置一次）
echo "ASTOCK_API_KEY=你的apiKey" >> .env
```

> 没有 apiKey？访问 https://aipmedia.cn/ → 登录 → 个人中心 → 查看 API Key

---

### 标准调用模式

```typescript
// 格式：npx tsx <skill目录>/scripts/api-client.ts <endpoint> [JSON参数]

// 示例1：查询上交所市场总貌（无参数）
npx tsx ~/.gemini/skills/a-stock-skill/scripts/api-client.ts /api/stock/sse_summary

// 示例2：查询个股实时行情
npx tsx ~/.gemini/skills/a-stock-skill/scripts/api-client.ts \
  /api/stock/individual_spot '{"symbol":"600519"}'

// 示例3：查询深交所统计（带日期参数）
npx tsx ~/.gemini/skills/a-stock-skill/scripts/api-client.ts \
  /api/stock/szse_summary '{"date":"2026-03-19"}'

// 示例4：查询龙虎榜（带日期范围）
npx tsx ~/.gemini/skills/a-stock-skill/scripts/api-client.ts \
  /api/stock/lhb_detail_em '{"start_date":"2026-03-10","end_date":"2026-03-20"}'

// 示例5：查询盘口异动
npx tsx ~/.gemini/skills/a-stock-skill/scripts/api-client.ts \
  /api/stock/changes_em '{"symbol":"大笔买入"}'

// 示例6：查询行业板块列表（无参数）
npx tsx ~/.gemini/skills/a-stock-skill/scripts/api-client.ts \
  /api/stock/board_industry_name_em
```

### 各接口与参数速查

| 意图 | endpoint | 必填参数 |
|---|---|---|
| 上交所总貌 | `/api/stock/sse_summary` | 无 |
| 深交所统计 | `/api/stock/szse_summary` | `date` |
| 个股信息(东财) | `/api/stock/individual_info_em` | `symbol` |
| 个股信息(雪球) | `/api/stock/individual_basic_info_xq` | `symbol` |
| 行情报价 | `/api/stock/bid_ask_em` | `symbol` |
| 实时行情 | `/api/stock/individual_spot` | `symbol` |
| 分时行情 | `/api/stock/zh_a_hist_min_em` | `symbol` |
| 行业板块列表 | `/api/stock/board_industry_name_em` | 无 |
| 板块实时行情 | `/api/stock/board_industry_spot_em` | `symbol`(板块名) |
| 龙虎榜 | `/api/stock/lhb_detail_em` | `start_date`,`end_date` |
| 盘口异动 | `/api/stock/changes_em` | `symbol`(异动类型) |

### 返回值处理

脚本成功时直接输出 `data` 字段的 JSON，失败时打印 ❌ 错误信息并退出。

- `data` 为 `[{item, value}]` 格式时：转为键值对字典后展示
- 金额字段：以"元"为单位，展示时统一换算为"亿元"（≥1亿）或"万元"（≥1万）
- 脚本输出 `❌ 未找到 API Key` 时：引导用户配置 `.env` 文件

---

## 展示规范

- **表格优先**：多行数据用 Markdown 表格展示
- **金额换算**：> 1亿 换算为"亿元"，> 10000 换算为"万元"
- **涨跌色彩**：文字提示涨（+）跌（-），不使用 HTML 颜色标签
- **数据解读**：在表格后附加 1-3 句简明解读，聚焦关键信号
- **缺失 apiKey**：提示用户将 `ASTOCK_API_KEY` 配置到 `.env` 文件或环境变量，**不得要求用户在聊天窗口中粘贴或输入 API Key**，前往 https://aipmedia.cn/ 个人中心获取

---

## 参考文档

详细的接口字段说明见 `references/api_fields.md`
