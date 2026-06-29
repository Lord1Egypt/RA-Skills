---
name: yufluentcn-inventory-pilot
description: >-
  库存驾驭助手：销量预测、补货建议、滞销预警、资金占用分析。
  基于卖家提供的销量/库存数据，经 Yufluent 云端 Harness 输出结构化 JSON。
  Use for 补货、库存预测、滞销、清仓、资金占用、库存管理.
version: 1.1.2
author: 元畅 · Yufluent
metadata:
  category: ecommerce
  tags: [inventory, forecast, replenishment, clearance, sku, yufluent, b2b]
  billing: yufluent
  languages: [zh, en, es, de, fr, ja]
  homepage: https://claw.changzhiai.com
  license: MIT
  openclaw: '{"requires":{"env":["TOKENAPI_KEY"]},"primaryEnv":"TOKENAPI_KEY","install":[{"id":"deps","kind":"pip","label":"Install requests","packages":["requests>=2.31.0"]}]}'
---

# 库存驾驭助手

基于卖家提供的 **销量/库存数据** 做预测、补货建议、滞销预警与资金占用分析。**ClawHub / OpenClaw 云端模式** — Harness `inventory_forecast` 输出结构化 **JSON**；本机只需 `TOKENAPI_KEY`（`tk-*`）与 `requests`。

不直连 ERP、不自动下单、不连接平台 API。

## 快速开始（3 步，60 秒）

1. **注册获取 API 密钥** → https://claw.changzhiai.com/login （新用户即送体验积分，无需绑卡）
2. **设置环境变量**：export TOKENAPI_KEY=*** 或写入 .env 文件
3. **运行**：参照下方 Examples 示例执行 python scripts/run.py ...

> 还没注册？前往 https://claw.changzhiai.com/login 免费获取密钥。

## OpenClaw 与 Yufluent（必读）

OpenClaw 对话与技能调用**共用同一 `tk-*`**。接入见 https://claw.changzhiai.com/app/openclaw。

| 层 | 走哪里 | 干什么 |
|----|--------|--------|
| **OpenClaw 对话** | Yufluent `/v1/chat/completions`（同一 tk-*） | 收集销量/库存数据、选模式、调 `run.py`、解读 JSON |
| **分析正式输出** | `POST /v1/skills/inventory-pilot/run`（同一 tk-*） | Harness → 预测/补货/滞销 JSON |

**Agent 硬性规则：**
- **禁止**用对话模型自行撰写完整补货计划表
- **必须**通过 `python scripts/run.py ...` 获取输出
- 只需 `TOKENAPI_KEY`，不要另配厂商 Key

## Instructions（Agent 工作流）

1. **确认模式**（见下表）；用户说"要不要补货" → `replenish`；"预测销量" → `forecast`。
2. **收集数据**：
   - `--message`（必填）：本轮问题
   - `--mode`：`forecast` | `replenish` | `clearance` | `capital`
   - `--sales-data`：历史销量 CSV 或文件路径
   - `--current-stock`：当前库存（如 `SKU-A:120, SKU-B:45`）
   - `--inventory-data`：库存明细（含库龄）
   - `--lead-time`：供应商交期（天）
   - `--transit-days`：头程时效（天）
3. **调用（必须 — 云端）**：
   ```bash
   python scripts/run.py \
     --mode replenish \
     -m "帮我算要不要补货" \
     --sales-data sales.csv \
     --current-stock "SKU-A:120, SKU-B:45" \
     --lead-time 21 \
     --transit-days 14 \
     --lang zh
   ```
4. **计费**：402 余额不足；401 密钥无效。

## 四模式

| mode | 用途 | 必填数据 |
|------|------|---------|
| `forecast` | 销量预测 | `sales_data` |
| `replenish` | 补货建议 | `sales_data`, `current_stock` |
| `clearance` | 滞销预警与清仓建议 | `inventory_data` |
| `capital` | 资金占用分析 | `inventory_data` |

## 与其他技能联动

| 需求 | 技能 |
|------|------|
| 清仓促销 Listing | `yufluentcn-ecommerce-listing` |
| 竞品变化 → 补货节奏调整 | `yufluentcn-comp-track` |

## 环境变量

| 变量 | 必填 | 说明 |
|------|------|------|
| `TOKENAPI_KEY` | 是 | `tk-*`，[Yufluent 控制台](https://claw.changzhiai.com) 获取 |
| `TOKENAPI_BASE_URL` | 否 | 默认 `http://localhost:8080/v1` |

## 触发词

- "帮我算一下要不要补货"
- "哪些 SKU 快滞销了"
- "预测下个月销量"
- "资金占用分析"
- "库存管理"
- "清仓建议"
- "inventory forecast"

## Examples

**补货建议**

```bash
python scripts/run.py \
  --mode replenish \
  -m "SKU-A 日均卖15件，当前库存120，要不要补？" \
  --sales-data sales.csv \
  --current-stock "SKU-A:120, SKU-B:45" \
  --lead-time 21 \
  --transit-days 14 \
  --lang zh
```

**滞销预警**

```bash
python scripts/run.py \
  --mode clearance \
  -m "哪些 SKU 超过90天没动销？" \
  --inventory-data inventory.csv \
  --age-threshold "90" \
  --lang zh
```

**销量预测**

```bash
python scripts/run.py \
  --mode forecast \
  -m "预测未来30天销量" \
  --sales-data sales.csv \
  --lang zh
```

## 合规声明

- 输出仅供参考，不构成采购或财务决策建议
- 不连接平台 API 自动拉取库存/销量数据
- 不自动生成采购单/下单指令

## 版本记录

| 版本 | 日期 | 变更 |
|------|------|------|
| v1.1.0 | 2026-06-14 | SKILL.md added quickstart registration guide; 401/402 error messages now in Chinese with register links |
| v1.0.0 | 2026-06-13 | 规范 SKILL.md：补充 Agent 规则、Instructions、触发词、示例、环境变量、合规、版本记录 |
| v0.1.0 | — | 初始库存驾驭技能 |
