---
name: yufluentcn-ad-optimize
description: >-
  Cross-border paid ads optimization coach across five dimensions (targeting,
  creatives, bidding, landing page, analytics) via Yufluent cloud Harness. Use
  for 广告投放优化、Meta/TikTok/Google 广告、ROAS、受众定向、素材测试、落地页、Pixel 归因.
version: 1.1.2
author: 元畅 · Yufluent
metadata:
  category: ecommerce
  tags: [ads, meta, facebook, instagram, tiktok, google, roas, yufluent, b2b]
  billing: yufluent
  languages: [zh, en, es, de, fr, ja]
  homepage: https://claw.changzhiai.com
  license: MIT
  openclaw: '{"requires":{"env":["TOKENAPI_KEY"]},"primaryEnv":"TOKENAPI_KEY","install":[{"id":"deps","kind":"pip","label":"Install requests","packages":["requests>=2.31.0"]}]}'
---

# 广告投放优化

跨境 **Meta / TikTok / Google** 广告投放五维优化教练。**ClawHub / OpenClaw 用户使用云端模式** — Harness 在 Yufluent 服务端执行，本机只需 `TOKENAPI_KEY`（`tk-*`）与 `requests`。

## 快速开始（3 步，60 秒）

1. **注册获取 API 密钥** → https://claw.changzhiai.com/login （新用户即送体验积分，无需绑卡）
2. **设置环境变量**：export TOKENAPI_KEY=*** 或写入 .env 文件
3. **运行**：参照下方 Examples 示例执行 python scripts/run.py ...

> 还没注册？前往 https://claw.changzhiai.com/login 免费获取密钥。

## OpenClaw 与 Yufluent（必读）

OpenClaw 对话与技能调用**共用同一 `tk-*`**。接入见 https://claw.changzhiai.com/app/openclaw 。

| 层 | 走哪里 | 干什么 |
|----|--------|--------|
| **OpenClaw 对话** | Yufluent `/v1/chat/completions`（同一 tk-*） | 理解意图、选维度/渠道、调 `run.py`、整理回复 |
| **优化方案正式输出** | `POST /v1/skills/ad-optimize/run`（同一 tk-*） | Harness + 五维策略 → 优化方案正文 |

**Agent 硬性规则：**

1. **禁止**用对话模型自行撰写完整投放优化方案（受众表、素材矩阵、预算表、A/B 方案等长文）。
2. **必须**通过 `python scripts/run.py ...`（或 `POST /v1/skills/ad-optimize/run`）获取输出。
3. 对话模型仅用于：确认渠道与维度、收集 metrics / market / context、解释结果、建议下一步。
4. 只需 `TOKENAPI_KEY`，**不要**要求用户另配厂商 LLM Key。

## Instructions（Agent 工作流）

1. **确认渠道**：`meta`（Facebook/Instagram）/ `tiktok` / `google` / `multi`（跨渠道）。
2. **选择 dimension**（见下表）；未说明时根据 message 推断（如 ROAS 低 → `bidding` 或 `analytics`；素材疲劳 → `creatives`）。
3. **收集上下文**：
   - `message`（必填）
   - `product`：产品或品类
   - `market`：目标市场（如 Vietnam、美国）
   - `metrics`：ROAS、CTR、CPC、CPA、花费等快照
   - `context`：账户阶段、预算、近期已尝试动作
4. **调用（必须 — 云端）**：
   ```bash
   python scripts/run.py \
     --dimension bidding \
     --platform meta \
     -m "ROAS 从 2.1 降到 1.4，请给预算重组建议" \
     --product "宠物牵引绳" \
     --market "Vietnam" \
     --metrics "7d spend $800, ROAS 1.4, CPA $12" \
     --lang zh
   ```
5. **计费**：402 余额不足；401 密钥无效。

### 五维优化（dimension）

| dimension | 核心问题 | 典型输出 |
|-----------|----------|----------|
| `targeting` | 找对人 | 受众分层、再营销、Lookalike、排除清单 |
| `creatives` | 说对话 | 素材测试矩阵、文案变体、版位 brief |
| `bidding` | 出对价 | 出价策略、预算倾斜、时段系数 |
| `landing` | 接住人 | 落地页审计表、速度/一致性/结账检查 |
| `analytics` | 做对决策 | Pixel 检查、A/B backlog、归因与周复盘 |

### 与其他技能联动

| 需求 | 技能 |
|------|------|
| 落地页产品文案 | `yufluentcn-ecommerce-listing` |
| 落地页 SEO 关键词 | `yufluentcn-seo-pro` |
| 评论洞察驱动素材 | `yufluentcn-review-intel` |
| 独立站全店运营 | `yufluentcn-shopify-operator` |

本技能 **不**直连 Ads Manager、不自动改出价、不代投。

## 环境变量

| 变量 | 必填 | 说明 |
|------|------|------|
| `TOKENAPI_KEY` | 是 | `tk-*` |
| `TOKENAPI_BASE_URL` | 否 | 默认 `http://localhost:8080/v1` |

## 触发词

- "广告投放优化"
- "Facebook 广告 ROAS 低"
- "TikTok 素材怎么测"
- "再营销受众怎么设"
- "落地页转化差"
- "Pixel 转化追踪"
- "越南市场投放时段"
- "A/B 测试方案"

## Examples

**定向 — Meta 再营销**

```bash
python scripts/run.py \
  --dimension targeting \
  --platform meta \
  -m "加购未下单用户很多，请给再营销分层方案" \
  --market "Vietnam" \
  --lang zh
```

**素材 — TikTok 本土化**

```bash
python scripts/run.py \
  --dimension creatives \
  --platform tiktok \
  -m "CTR 下滑，请给 4 周素材轮换测试表" \
  --product "美妆套装" \
  --market "Vietnam" \
  --lang zh
```

**数据 — 跨渠道归因**

```bash
python scripts/run.py \
  --dimension analytics \
  --platform multi \
  -m "FB 和 Google 都在投，如何看归因和分配预算？" \
  --metrics "FB ROAS 1.8, Google ROAS 3.2, MER 2.1" \
  --lang zh
```

## 合规声明

- 方案需人工审核后在广告平台执行
- 遵守各平台广告政策与目标市场法规
- 不虚构投放数据或已修改账户状态

## 版本记录

| 版本 | 日期 | 变更 |
|------|------|------|
| v1.1.0 | 2026-06-14 | SKILL.md added quickstart registration guide; 401/402 error messages now in Chinese with register links |
| v0.1.0 | 2026-05-28 | 初始五维广告投放优化技能 |
