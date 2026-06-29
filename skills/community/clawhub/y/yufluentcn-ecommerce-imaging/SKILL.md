---
name: yufluentcn-ecommerce-imaging
description: >-
  跨境电商 AI 生图：白底图、场景图、实拍抠图、多角度套装、多平台尺寸。
  经 Yufluent 云端 Replicate 代理（Qwen-Image 等），按张计费。
  配合 visual-craft 工作流 brief→生图→合规。
  Use for 生成产品白底图、场景图、AI 电商图片、产品摄影、主图.
version: 1.1.2
author: 元畅 · Yufluent
metadata:
  category: ecommerce
  tags: [image-generation, product-photography, amazon, shopify, tiktok, flux, yufluent, b2b]
  billing: yufluent
  languages: [zh, en]
  homepage: https://claw.changzhiai.com
  license: MIT
  openclaw: '{"requires":{"env":["TOKENAPI_KEY"]},"primaryEnv":"TOKENAPI_KEY","install":[{"id":"deps","kind":"pip","label":"Install requests","packages":["requests>=2.31.0"]}]}'
---

# 电商 AI 生图

跨境 **白底图 / 场景图 / 实拍抠图 / 多角度套装** 生成。**ClawHub / OpenClaw 云端模式** — 生图在 Yufluent 服务端通过 Replicate 代理执行，按张计费；本机只需 `TOKENAPI_KEY`（`tk-*`）与 `requests`。

支持上传实拍图 URL 或本地路径做 img2img（多角度套装必填）。

## 快速开始（3 步，60 秒）

1. **注册获取 API 密钥** → https://claw.changzhiai.com/login （新用户即送体验积分，无需绑卡）
2. **设置环境变量**：export TOKENAPI_KEY=*** 或写入 .env 文件
3. **运行**：参照下方 Examples 示例执行 python scripts/run.py ...

> 还没注册？前往 https://claw.changzhiai.com/login 免费获取密钥。

## OpenClaw 与 Yufluent（必读）

OpenClaw 对话与技能调用**共用同一 `tk-*`**。接入见 https://claw.changzhiai.com/app/openclaw。

| 层 | 走哪里 | 干什么 |
|----|--------|--------|
| **OpenClaw 对话** | Yufluent `/v1/chat/completions`（同一 tk-*） | 选场景/角度/尺寸、调 `run.py` |
| **生图正式输出** | `POST /v1/skills/ecommerce-imaging/run`（同一 tk-*） | 服务端 Replicate → 图片 URL |

**Agent 硬性规则：**

1. **禁止**用对话模型自行生成图片或给出图片生成指令替代本技能。
2. **必须**通过 `python scripts/run.py ...`（或 `POST /v1/skills/ecommerce-imaging/run`）获取输出。
3. 对话模型仅用于：确认场景、尺寸、角度、上传实拍图路径、解释结果。
4. 只需 `TOKENAPI_KEY`，**不要**要求用户另配厂商 LLM Key 或 Replicate Token。

## Instructions（Agent 工作流）

1. **确认场景**（见下表）；默认 `white_bg`。客户有实拍图 → `--source-image`。
2. **收集参数**：
   - `--product`（必填）
   - `--scene`：白底/厨房/客厅/多角度套装/节日场景等
   - `--platform-size`：如 `amazon-main`、`amazon-aplus-banner`
   - `--source-image`：实拍图 URL 或本地路径
   - `--brand-style`：品牌调性叠加（luxury_minimal / youthful_pop 等）
3. **调用（必须 — 云端）**：
   ```bash
   python scripts/run.py \
     --product "不锈钢不粘锅" \
     --scene white_bg \
     --platform-size amazon-main
   ```
4. **多角度套装**：
   ```bash
   python scripts/run.py \
     --product "蓝牙耳机" \
     --scene multi_angle_pack \
     --source-image "./front.jpg"
   ```
5. **计费**：按张计费；402 余额不足；401 密钥无效。

## 场景列表

| 场景 key | 说明 |
|----------|------|
| `white_bg` | 纯白背景产品图 |
| `minimal_white` | 极简白底 |
| `modern_kitchen` | 现代厨房 |
| `living_room` | 客厅场景 |
| `lifestyle` | 生活场景 |
| `desk_setup` | 桌面场景 |
| `multi_angle_pack` | 多角度套装（需 `--source-image`） |
| 节日/促销 | `christmas`, `prime_day`, `black_friday`, `valentine`, `summer_sale` |

## 环境变量

| 变量 | 必填 | 说明 |
|------|------|------|
| `TOKENAPI_KEY` | 是 | `tk-*`，[Yufluent 控制台](https://claw.changzhiai.com) 获取 |
| `TOKENAPI_BASE_URL` | 否 | 默认 `http://localhost:8080/v1` |

## 触发词

- "生成产品白底图"
- "做场景图"
- "AI 生成电商图片"
- "产品主图"
- "多角度展示"
- "product image"

## Examples

**白底图**

```bash
python scripts/run.py \
  --product "不锈钢不粘锅" \
  --scene white_bg \
  --platform-size amazon-main
```

**厨房场景图**

```bash
python scripts/run.py \
  --product "陶瓷餐具套装" \
  --scene modern_kitchen \
  --brand-style eco_natural
```

**实拍图抠图换背景**

```bash
python scripts/run.py \
  --product "蓝牙耳机" \
  --scene white_bg \
  --source-image "./product.jpg"
```

**多角度套装**

```bash
python scripts/run.py \
  --product "蓝牙耳机" \
  --scene multi_angle_pack \
  --source-image "./front.jpg"
```

## 工作流联动

`visual-to-imaging`：visual-craft (main_image brief) → ecommerce-imaging 生图 → visual-craft (image_compliance) 合规检查。

## Monorepo 本地开发

在完整 TokenApi 仓库中可用 `scripts/image_generator.py`（直连 Replicate + `REPLICATE_API_TOKEN`）与 `scripts/prompt_library.py`。ClawHub 分发包**不包含**此路径；卖家/OpenClaw 仅使用 `scripts/run.py`（Yufluent 云端 Replicate 代理）。

## 合规声明

- AI 生成图片需人工审核产品质量一致性后再上架
- 不生成侵权商品图、违禁品或虚假宣传图片
- 平台主图规则（如 Amazon 纯白底不低于 85%）以平台最新要求为准

## 版本记录

| 版本 | 日期 | 变更 |
|------|------|------|
| v1.1.0 | 2026-06-14 | SKILL.md added quickstart registration guide; 401/402 error messages now in Chinese with register links |
| v1.0.0 | 2026-06-13 | 规范 SKILL.md：补充 Agent 规则、Instructions、触发词、示例、环境变量、合规、版本记录 |
| v0.1.0 | — | 初始电商 AI 生图技能 |
