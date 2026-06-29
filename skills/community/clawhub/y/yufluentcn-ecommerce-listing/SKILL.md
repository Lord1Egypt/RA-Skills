---
name: yufluentcn-ecommerce-listing
description: >-
  跨境电商智能 Listing 生成器 — 亚马逊 / Shopify / TikTok Shop 多平台多语言产品文案
（标题/五点/描述/搜索词），经 Yufluent 云端 Harness 执行，SEO 导向。Cross-border
listing generator for Amazon, Shopify & TikTok Shop with SEO copy & multi-language
output. Use for 亚马逊 Listing、产品标题、五点描述、Shopify 产品页、TikTok 商品文案.
version: 1.3.2
author: 元畅 · Yufluent
metadata:
  category: ecommerce
  tags: [amazon, shopify, tiktok, listing, seo, yufluent, b2b]
  billing: yufluent
  languages: [zh, en, es, de, fr, ja]
  homepage: https://claw.changzhiai.com
  license: MIT
  openclaw: '{"requires":{"env":["TOKENAPI_KEY"]},"primaryEnv":"TOKENAPI_KEY","install":[{"id":"deps","kind":"pip","label":"Install requests","packages":["requests>=2.31.0"]}]}'
---

# Yufluent 电商 Listing 生成器

跨境电商多平台 Listing 生成技能。**ClawHub / OpenClaw 用户使用云端模式**：Harness 在 Yufluent 服务端执行，本机只需 `TOKENAPI_KEY`（`tk-*`）与 `requests`。

## 快速开始（3 步，60 秒）

1. **注册获取 API 密钥** → https://claw.changzhiai.com/login （新用户即送体验积分，无需绑卡）
2. **设置环境变量**：export TOKENAPI_KEY=*** 或写入 .env 文件
3. **运行**：参照下方 Examples 示例执行 python scripts/run.py ...

> 还没注册？前往 https://claw.changzhiai.com/login 免费获取密钥。

## OpenClaw 与 Yufluent（必读）

OpenClaw 对话与技能调用**共用同一 `tk-*`**（配置 `yufluent` 模型提供商 + `TOKENAPI_*` 环境变量）。接入见 https://claw.changzhiai.com/app/openclaw 。

| 层 | 走哪里 | 干什么 |
|----|--------|--------|
| **OpenClaw 对话** | Yufluent `/v1/chat/completions`（同一 tk-*） | 理解意图、读本 SKILL、决定调 `run.py`、整理回复 |
| **Listing 正式输出** | `POST /v1/skills/listing/run`（同一 tk-*） | Harness + 平台规则 → 标题/五点/描述 |

```text
用户 → OpenClaw（yufluent provider）→ python scripts/run.py → Yufluent API → Harness → Listing 正文
```

**Agent 硬性规则（违反则视为未正确使用本技能）：**

1. **禁止**用对话模型自行撰写 Listing 正文（标题、五点、描述、关键词等）。
2. **必须**通过 `python scripts/run.py ...`（或 `POST /v1/skills/listing/run`）获取输出，并将 stdout / `-o` 文件作为交付物。
3. 对话模型仅用于：收集字段、确认平台/语言、解释结果、提醒人工审核。
4. 只需 `TOKENAPI_KEY`，**不要**要求用户另配 DeepSeek / OpenAI 等厂商 Key。

## Instructions（Agent 工作流）

1. **确认平台与语言**：`amazon` / `shopify` / `tiktok`，语言 `zh|en|es|de|fr|ja`。
2. **收集必填字段**：产品名、核心关键词（逗号分隔）；可选卖点、受众、品牌调性。
3. **调用生成（必须 — 云端）**：
   ```bash
   python scripts/run.py \
     --product "..." \
     --keywords "..." \
     --platform amazon \
     --lang zh \
     --format amazon \
     -o listing.txt
   ```
   - API：`POST {TOKENAPI_BASE_URL}/skills/listing/run`
   - 默认 `TOKENAPI_BASE_URL=http://localhost:8080/v1`；生产环境为控制台同域 `/api/v1`
4. **输出**：`--format amazon|shopify|tiktok|json`；提醒用户**人工审核后再上架**。
5. **计费**：余额不足返回 402；无效密钥返回 401。

### 仓库内开发（可选）

在完整 TokenApi 仓库中可用 `scripts/listing_generator.py`（本地 Harness + `yufluentcn-harness`），需 `pip install -r requirements-dev.txt`。ClawHub 分发包**不包含**此路径。

## 环境变量

| 变量 | 必填 | 说明 |
|------|------|------|
| `TOKENAPI_KEY` | 是 | `tk-*`，[Yufluent 控制台](https://claw.changzhiai.com) 获取 |
| `TOKENAPI_BASE_URL` | 否 | 默认 `http://localhost:8080/v1` |

模型档位由平台 Harness 自动选择，无需卖家配置。

## 触发词

- "生成亚马逊 Listing"
- "写个 Shopify 产品描述"
- "TikTok 商品文案"
- "优化产品标题"
- "做多语言 Listing"

## Examples

**用户**：帮我写一个英文亚马逊 Listing，产品是便携式咖啡机，关键词 espresso, camping, mini。

**Agent**：

```bash
export TOKENAPI_KEY="tk-..."
export TOKENAPI_BASE_URL="http://localhost:8080/v1"
python scripts/run.py \
  --product "Portable Espresso Coffee Maker" \
  --keywords "espresso,camping,mini" \
  --platform amazon --lang en \
  --format amazon -o listing.txt
```

## 文件结构

**Monorepo 源码**（`skills/yufluentcn-ecommerce-listing/`）：

```
yufluentcn-ecommerce-listing/
  SKILL.md
  scripts/
    run.py                  # 主入口（云端）
    listing_generator.py    # 仅仓库内本地 Harness（不进 ClawHub 包）
    format_listing.py         # 仅 listing_generator 使用（不进 ClawHub 包）
  requirements.txt
  requirements-dev.txt      # 本地 Harness 可选依赖
```

云端客户端 `yufluent_api.py`、`cloud_cli.py`、`bootstrap.py` 的 **SoT 在 `skills/_shared/`**；`run.py` 启动时经 `sys.path` 引用，**不要**在技能目录 `scripts/` 下找这些文件的源码副本。

**ClawHub 安装包**（`package-skill.ps1` 打包后）：

```
yufluentcn-ecommerce-listing/
  SKILL.md
  README.md
  .env.example
  requirements.txt          # 仅 requests
  scripts/
    run.py                  # 主入口（云端）
    yufluent_api.py         # 由 _shared/ 注入
    cloud_cli.py            # 由 _shared/ 注入
    bootstrap.py            # 由 _shared/ 注入
```

## 合规声明

- 生成内容需人工审核后上架
- 遵守各平台卖家条款，不生成虚假宣传内容

## 版本记录

| 版本 | 日期 | 变更 |
|------|------|------|
| v1.3.0 | 2026-06-14 | SKILL.md added quickstart registration guide; 401/402 error messages now in Chinese with register links |
| v1.1.1 | 2026-05-24 | OpenClaw 双模型说明；禁止 Agent 自行生成 Listing |
| v1.1.0 | 2026-05-24 | Yufluent 品牌；ClawHub 云端薄客户端 `run.py` |
| v1.0.0 | 2026-05-21 | 初始 Listing 技能 |
