# Qutedance Quotes - 行情查询技能

## 简介

基于 Qutedance 的 quotedance-service 行情接口，提供：

- A 股 / 港股 / 期货 实时行情查询
- A 股板块热门涨跌信息（涨跌幅榜单）
- 股票/期货等标的搜索（支持按名称/代码模糊搜索）

适配你的 qutedance 工作区，用于在对话中快速查看关键标的和板块表现。

---

## 配置

- 行情服务（quotedance-service）：
  - 当前已直接指向你的线上实例：
    - `serviceUrl: "https://quotedance.api.gapgap.cc"`
- Qutedance API Key：
  - 为了简单易学，**直接写在配置文件中**：
    - `apiKey: ""`
  - 如需更安全的方式，可以以后再改成环境变量。

配置文件：`skills/qutedance-quotes/config.json`

```json
{
  "serviceUrl": "https://quotedance.api.gapgap.cc",
  "apiKey": "",
  "defaults": {
    "type": "cn",
    "topPlatesCount": 10
  }
}
```

---

## 能力

### 1️⃣ A 股 / 期货 / 港股 行情查询

- A 股：`type=cn`
- 港股：`type=hk`
- 期货：`type=futures`（默认）

脚本会调用：

- `GET /quotes/?list=CODE1,CODE2&type=cn|hk|futures`

输出内容包括：

- 代码、名称
- 最新价
- 涨跌幅（相对昨收价或结算价）
- 最高价 / 最低价
- 买一 / 卖一

### 2️⃣ A 股板块热门涨跌榜

- 接口：`GET /quotes/plate-top-info?count=N`
- 展示：
  - 板块名称、平均涨跌幅（core_avg_pcp）
  - 领涨股票（symbol, name, 涨跌幅、价格变动）
  - 领跌股票（同上）

### 3️⃣ 标的搜索（股票 / 期货等）

- 接口：`GET /quotes/search`
- 支持参数：
  - `q`: 搜索关键词（如“平安”）
  - `type`: 市场类型（`cn` / `hk` / `futures` / `us` / `all` 等）
  - `limit`: 返回数量上限（默认 20）
- 输出：
  - 代码、名称、市场、交易所

---

## 在对话中如何使用

当用户说到：

- “看下 A 股 000001、600000 的行情”
- “查一下 M2605 和 RB2605 的期货报价”
- “看看今天 A 股涨跌幅榜、热门板块”
 - “搜一下平安相关的 A 股有哪些”

Agent 应该：

1. 选用本技能 `qutedance-quotes`
2. 根据语义决定调用模式：
   - 指定代码 → 调用 `/quotes/` 行情查询
   - 想看涨跌榜/热门板块 → 调用 `/quotes/plate-top-info`
3. 将脚本输出的 Markdown 表格/列表直接呈现给用户，必要时附加解释。

---

## 手动脚本用法

从 `workspace-quotedance` 目录运行：

```bash
cd ~/.openclaw/workspace-quotedance

# A 股行情
node skills/qutedance-quotes/scripts/qutedance-quotes.js --type cn --list 000001,600000

# 期货行情
node skills/qutedance-quotes/scripts/qutedance-quotes.js --type futures --list M2605,RB2605

# A 股板块涨跌幅榜（前 10 个）
node skills/qutedance-quotes/scripts/qutedance-quotes.js --plates 10

# 搜索标的（按名称模糊搜索）
node skills/qutedance-quotes/scripts/qutedance-quotes.js --search --q 平安 --type cn --limit 10
```

---

## 实现细节

目录结构：

```text
skills/qutedance-quotes/
├── SKILL.md
├── config.json
└── scripts/
    └── qutedance-quotes.js
```

脚本行为概要：

- 从 `SERVICE_URL` 和 `QUTEDANCE_API_KEY` 读取 quotedance-service 访问配置
- `getQuotes(list, type)`：
  - 调用 `/quotes/` 接口
  - 将结果格式化为 Markdown 表格
- `getPlateTopInfo(count)`：
  - 调用 `/quotes/plate-top-info`
  - 生成板块及其领涨/领跌股的列表说明

---

## 注意事项

- 请确保 quotedance-service 正常运行（或云端实例可访问）
- API Key 应通过环境变量配置，而不是写死在仓库文件中
- 行情数据仅供参考，不构成任何投资建议

