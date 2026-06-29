---
name: yufluentcn-ecommerce-render
description: >-
  跨境电商模板渲染：尺码表、参数卡、卖点网格、对比表、促销 banner。
  Pillow 确定性出图，经 Yufluent 服务端渲染按张计费。
  Use for 尺码表、参数对比、信息图、促销 banner、模板渲染.
version: 1.1.2
author: 元畅 · Yufluent
metadata:
  category: ecommerce
  tags: [template, render, infographic, size-chart, pillow, yufluent, b2b]
  billing: yufluent
  languages: [zh, en]
  homepage: https://claw.changzhiai.com
  license: MIT
  openclaw: '{"requires":{"env":["TOKENAPI_KEY"]},"primaryEnv":"TOKENAPI_KEY","install":[{"id":"deps","kind":"pip","label":"Install requests","packages":["requests>=2.31.0"]}]}'
---

# 模板渲染

结构化数据 → PNG 信息图（Pillow 确定性渲染）。**ClawHub / OpenClaw 云端模式** — 渲染在 **Yufluent 服务端**执行，按张计费；本机只需 `TOKENAPI_KEY`（`tk-*`）与 `requests`。

## 快速开始（3 步，60 秒）

1. **注册获取 API 密钥** → https://claw.changzhiai.com/login （新用户即送体验积分，无需绑卡）
2. **设置环境变量**：export TOKENAPI_KEY=*** 或写入 .env 文件
3. **运行**：参照下方 Examples 示例执行 python scripts/run.py ...

> 还没注册？前往 https://claw.changzhiai.com/login 免费获取密钥。

## OpenClaw 与 Yufluent（必读）

OpenClaw 对话与技能调用**共用同一 `tk-*`**。接入见 https://claw.changzhiai.com/app/openclaw。

| 层 | 走哪里 | 干什么 |
|----|--------|--------|
| **OpenClaw 对话** | Yufluent `/v1/chat/completions`（同一 tk-*） | 收集数据、选模板、调 `run.py` |
| **渲染正式输出** | `POST /v1/skills/commerce-render/run`（同一 tk-*） | 服务端 Pillow → PNG |

**Agent 硬性规则：**

1. **禁止**用对话模型自行生成图片或给出像素级渲染指令。
2. **必须**通过 `python scripts/run.py ...`（或 `POST /v1/skills/commerce-render/run`）获取输出。
3. 对话模型仅用于：确认模板类型、帮助构造 JSON 数据、选品牌色。
4. 只需 `TOKENAPI_KEY`，**不要**要求用户另配厂商 LLM Key。

## Instructions（Agent 工作流）

1. **确认模板**（见下表）；根据用户意图选择：尺码表 → `size_chart`，参数卡 → `spec_card`，卖点 → `feature_grid`。
2. **收集数据**：
   - `--product`（必填）：产品名
   - `--template` / `-t`：模板类型
   - `--render-data`：JSON 数据文件或 JSON 字符串
   - `--brand-color`：品牌色 hex（默认 `#1a56db`）
   - `--platform-size`：如 `amazon-main`、`amazon-aplus-banner`
3. **调用（必须 — 云端）**：
   ```bash
   python scripts/run.py \
     --product "无线蓝牙耳机" \
     --template size_chart \
     --render-data data.json \
     --brand-color "#1a56db"
   ```
4. **计费**：按张计费；402 余额不足；401 密钥无效。

## 模板类型

| template | 用途 | 数据要求 |
|----------|------|----------|
| `size_chart` | 尺码表 | 表头 + 行数据 |
| `spec_card` | 参数信息图 | 键值对参数 |
| `feature_grid` | 卖点网格 | 卖点列表 |
| `compare_table` | 功能对比表 | 对比矩阵 |
| `promo_banner` | 促销 banner | 标题 + 副标题 |

## 与 ecommerce-imaging 分工

| commerce-render | ecommerce-imaging |
|-----------------|-------------------|
| 表格/文字/参数 — Pillow 确定性 | 照片/场景/白底 — AI 生图 |
| 可预测、可重复 | 创意、概率性 |

## 环境变量

| 变量 | 必填 | 说明 |
|------|------|------|
| `TOKENAPI_KEY` | 是 | `tk-*`，[Yufluent 控制台](https://claw.changzhiai.com) 获取 |
| `TOKENAPI_BASE_URL` | 否 | 默认 `http://localhost:8080/v1` |
| `RENDER_FONT_PATH` | 否 | 服务端中文字体路径（Pillow 渲染） |

## 触发词

- "生成尺码表"
- "做参数对比图"
- "卖点信息图"
- "促销 banner"
- "size chart"
- "spec card"
- "模板渲染"

## Examples

**尺码表**

```bash
python scripts/run.py \
  --product "运动T恤" \
  --template size_chart \
  --render-data examples/size_chart.json \
  --brand-color "#1a56db"
```

**参数卡**

```bash
python scripts/run.py \
  --product "蓝牙耳机" \
  --template spec_card \
  --specs '{"蓝牙版本":"5.3","续航":"30h","防水":"IPX5","重量":"45g"}' \
  --platform-size amazon-aplus-banner
```

**促销 Banner**

```bash
python scripts/run.py \
  --product "夏季美妆套装" \
  --template promo_banner \
  --title "夏日美肌季" \
  --subtitle "全场满300减50 · 限时3天" \
  --brand-color "#e63946"
```

## 工作流联动

`visual-to-render`：visual-craft brief → commerce-render 出图。

## 合规声明

- 渲染内容须与产品事实一致，不虚构参数
- 字体版权需自行检查（建议 Noto Sans SC 或系统自带字体）

## 版本记录

| 版本 | 日期 | 变更 |
|------|------|------|
| v1.1.0 | 2026-06-14 | SKILL.md added quickstart registration guide; 401/402 error messages now in Chinese with register links |
| v1.0.0 | 2026-06-13 | 规范 SKILL.md：补充 Agent 规则、Instructions、触发词、示例、环境变量、合规、版本记录 |
| v0.1.0 | — | 初始模板渲染技能 |
