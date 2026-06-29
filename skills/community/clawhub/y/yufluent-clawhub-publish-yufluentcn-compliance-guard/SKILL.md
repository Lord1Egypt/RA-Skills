---
name: yufluentcn-compliance-guard
description: >-
  跨境合规与贸易参考助手：认证清单（CE/FCC/GPSR）、关税估算、标签要求、
  平台规则检查。经 Yufluent 云端 Harness 输出结构化 JSON 建议。
  非法律或税务建议，结果须人工核实。Use for 合规、认证、关税、GPSR、CE、FCC、VAT、HS编码.
version: 1.1.2
author: 元畅 · Yufluent
metadata:
  category: ecommerce
  tags: [compliance, customs, gpsr, ce, fcc, vat, hs-code, yufluent, b2b]
  billing: yufluent
  languages: [zh, en, es, de, fr, ja]
  homepage: https://claw.changzhiai.com
  license: MIT
  openclaw: '{"requires":{"env":["TOKENAPI_KEY"]},"primaryEnv":"TOKENAPI_KEY","install":[{"id":"deps","kind":"pip","label":"Install requests","packages":["requests>=2.31.0"]}]}'
---

# 合规卫士

跨境 **认证清单 / 关税估算 / 标签要求 / 平台规则** 参考助手。**ClawHub / OpenClaw 云端模式** — Harness `compliance_check` 输出结构化 **JSON**；本机只需 `TOKENAPI_KEY`（`tk-*`）与 `requests`。

⚠️ **非法律或税务建议**；结果须人工核实官方来源与最新法规。

## 快速开始（3 步，60 秒）

1. **注册获取 API 密钥** → https://claw.changzhiai.com/login （新用户即送体验积分，无需绑卡）
2. **设置环境变量**：export TOKENAPI_KEY=*** 或写入 .env 文件
3. **运行**：参照下方 Examples 示例执行 python scripts/run.py ...

> 还没注册？前往 https://claw.changzhiai.com/login 免费获取密钥。

## OpenClaw 与 Yufluent（必读）

OpenClaw 对话与技能调用**共用同一 `tk-*`**。接入见 https://claw.changzhiai.com/app/openclaw。

| 层 | 走哪里 | 干什么 |
|----|--------|--------|
| **OpenClaw 对话** | Yufluent `/v1/chat/completions`（同一 tk-*） | 收集产品/市场/材质等、调 `run.py`、解读 JSON |
| **合规正式输出** | `POST /v1/skills/compliance-guard/run`（同一 tk-*） | Harness 合规分析 → JSON |

**Agent 硬性规则：**

1. **禁止**用对话模型自行撰写完整合规认证清单或关税计算表。
2. **必须**通过 `python scripts/run.py ...`（或 `POST /v1/skills/compliance-guard/run`）获取输出。
3. 对话模型仅用于：收集产品信息、确认目标市场、解读输出、提醒人工核实。
4. 只需 `TOKENAPI_KEY`，**不要**要求用户另配厂商 LLM Key。

## Instructions（Agent 工作流）

1. **选择 mode**（见下表）；用户说"出口欧盟需要什么认证" → `certification`；"帮我算关税" → `tariff`。
2. **收集上下文**（尽量一次问齐）：
   - `--message`（必填）
   - `--product`（必填）
   - `--target-market`：目标市场（如 美国、欧盟、日本）
   - `--material`：材质或成分
   - `--category`：产品类目
   - `--declared-value`：申报货值
   - `--hs-code`：已知 HS 编码（可选）
   - `--origin-country`：原产国
3. **调用（必须 — 云端）**：
   ```bash
   python scripts/run.py \
     --mode certification \
     -m "蓝牙耳机出口美国需要什么认证" \
     --product "蓝牙耳机" \
     --target-market "美国" \
     --material "塑料+锂电池" \
     --lang zh
   ```
4. **计费**：402 余额不足；401 密钥无效。

## 四模式

| mode | 用途 | 示例 |
|------|------|------|
| `certification` | CE/FCC/CPSC/GPSR 等认证清单 | "出口欧盟需要什么认证" |
| `tariff` | HS 编码建议、税率与税费估算 | "蓝牙耳机到美国关税多少" |
| `labeling` | 成分、警示语、能效等标签要求 | "德国食品标签规范" |
| `platform_rules` | 亚马逊/Shopify/TikTok 类目限制 | "这个能上亚马逊吗" |

## 环境变量

| 变量 | 必填 | 说明 |
|------|------|------|
| `TOKENAPI_KEY` | 是 | `tk-*`，[Yufluent 控制台](https://claw.changzhiai.com) 获取 |
| `TOKENAPI_BASE_URL` | 否 | 默认 `http://localhost:8080/v1` |

## 触发词

- "出口美国需要什么认证"
- "帮我算关税"
- "GPSR 合规吗"
- "欧盟标签要求"
- "亚马逊新规影响"
- "HS 编码"
- "CE 认证"
- "platform rules"

## Examples

**认证清单**

```bash
python scripts/run.py \
  --mode certification \
  -m "儿童玩具出口欧盟需要什么认证" \
  --product "塑料积木玩具" \
  --target-market "欧盟" \
  --material "ABS塑料" \
  --lang zh
```

**关税估算**

```bash
python scripts/run.py \
  --mode tariff \
  -m "蓝牙耳机 HS 编码和关税" \
  --product "TWS蓝牙耳机" \
  --target-market "美国" \
  --declared-value "USD 15,000" \
  --hs-code "8518.30" \
  --lang zh
```

**平台规则**

```bash
python scripts/run.py \
  --mode platform_rules \
  -m "这个产品能上亚马逊德国站吗" \
  --product "电子体温计" \
  --platform amazon \
  --target-market "德国" \
  --lang zh
```

## 合规声明

- 输出仅供参考，**不构成法律或税务建议**
- 不虚构已获批认证号或实时海关数据
- 最终认证申请须经专业机构

## 版本记录

| 版本 | 日期 | 变更 |
|------|------|------|
| v1.1.0 | 2026-06-14 | SKILL.md added quickstart registration guide; 401/402 error messages now in Chinese with register links |
| v1.0.0 | 2026-06-13 | 规范 SKILL.md：补充 Agent 规则、Instructions、触发词、示例、环境变量、合规、版本记录 |
| v0.1.0 | — | 初始合规卫士技能 |
