---
name: yufluentcn-visual-craft
description: >-
  跨境电商视觉内容教练：A+ 页面结构、视频分镜脚本、主图差异化 brief、
  图片合规检查。经 Yufluent 云端 Harness 输出 Markdown 方案。
  配合 ecommerce-imaging 和 commerce-render 串联工作流。
  Use for A+页面、视频脚本、主图差异化、图片合规、TikTok视频、分镜.
version: 1.1.2
author: 元畅 · Yufluent
metadata:
  category: ecommerce
  tags: [visual, a-plus, video, creative, amazon, shopify, tiktok, yufluent, b2b]
  billing: yufluent
  languages: [zh, en, es, de, fr, ja]
  homepage: https://claw.changzhiai.com
  license: MIT
  openclaw: '{"requires":{"env":["TOKENAPI_KEY"]},"primaryEnv":"TOKENAPI_KEY","install":[{"id":"deps","kind":"pip","label":"Install requests","packages":["requests>=2.31.0"]}]}'
---

# 视觉工坊

**Amazon / Shopify / TikTok** 视觉内容教练：A+ 模块结构、视频分镜脚本、主图差异化 brief、图片合规清单。**ClawHub / OpenClaw 云端模式** — Harness `visual_content` 在 Yufluent 服务端执行；本机只需 `TOKENAPI_KEY`（`tk-*`）与 `requests`。

不生成实际图片/视频文件，输出为 Markdown 文案方案（可传给 imaging/render 出图）。

## 快速开始（3 步，60 秒）

1. **注册获取 API 密钥** → https://claw.changzhiai.com/login （新用户即送体验积分，无需绑卡）
2. **设置环境变量**：export TOKENAPI_KEY=*** 或写入 .env 文件
3. **运行**：参照下方 Examples 示例执行 python scripts/run.py ...

> 还没注册？前往 https://claw.changzhiai.com/login 免费获取密钥。

## OpenClaw 与 Yufluent（必读）

OpenClaw 对话与技能调用**共用同一 `tk-*`**。接入见 https://claw.changzhiai.com/app/openclaw。

| 层 | 走哪里 | 干什么 |
|----|--------|--------|
| **OpenClaw 对话** | Yufluent `/v1/chat/completions`（同一 tk-*） | 收集产品信息、选模式、调 `run.py` |
| **视觉方案正式输出** | `POST /v1/skills/visual-craft/run`（同一 tk-*） | Harness → Markdown 视觉方案 |

**Agent 硬性规则：**

1. **禁止**用对话模型自行撰写完整 A+ 或视频脚本。
2. **必须**通过 `python scripts/run.py ...`（或 `POST /v1/skills/visual-craft/run`）获取输出。
3. 只需 `TOKENAPI_KEY`，**不要**要求用户另配厂商 LLM Key。

## Instructions（Agent 工作流）

1. **选择 mode**（见下表）；用户说"帮我写 A+ 页面" → `a_plus`；"TikTok 视频脚本" → `video_script`。
2. **收集信息**：
   - `--message`（必填）：具体需求
   - `--product`（必填）：产品名
   - `--mode`：`a_plus` | `video_script` | `main_image` | `image_compliance`
   - `--platform`：`amazon` | `shopify` | `tiktok`
   - `--duration`：视频时长（`15s`/`30s`/`60s`，默认 `30s`）
   - `--listing-context`：已有 Listing 文案或文件路径
3. **调用（必须 — 云端）**：
   ```bash
   python scripts/run.py \
     --mode a_plus \
     --platform amazon \
     -m "帮我写 A+ 页面结构" \
     --product "宠物牵引绳" \
     --lang zh
   ```
4. **计费**：402 余额不足；401 密钥无效。

## 四模式

| mode | 用途 | 输出 |
|------|------|------|
| `a_plus` | A+ 模块顺序 + 文案 + 配图 brief | Markdown 方案 |
| `video_script` | 视频分镜脚本（`--duration` 控制长度） | 分镜表 + 口播文案 |
| `main_image` | 主图差异化创意方向 | brief + 构图建议 |
| `image_compliance` | 图片规格与合规检查清单 | 检查表 |

## 与下游技能联动

| 工作流 | 说明 |
|------|--------|
| `visual-to-imaging` | visual-craft (main_image brief) → ecommerce-imaging 生图 → visual-craft (image_compliance) 合规检查 |
| `visual-to-render` | visual-craft brief → commerce-render 模板出图 |

## 环境变量

| 变量 | 必填 | 说明 |
|------|------|------|
| `TOKENAPI_KEY` | 是 | `tk-*`，[Yufluent 控制台](https://claw.changzhiai.com) 获取 |
| `TOKENAPI_BASE_URL` | 否 | 默认 `http://localhost:8080/v1` |

## 触发词

- "帮我写 A+ 页面"
- "TikTok 视频脚本"
- "主图差异化建议"
- "图片合规检查"
- "A+ 内容"
- "分镜脚本"
- "video script"
- "image compliance"

## Examples

**A+ 页面**

```bash
python scripts/run.py \
  --mode a_plus \
  --platform amazon \
  -m "帮我写宠物牵引绳的 A+ 页面" \
  --product "反光宠物牵引绳 5m" \
  --listing-context "遛狗牵引绳，反光材质，5米可调" \
  --lang zh
```

**TikTok 视频脚本**

```bash
python scripts/run.py \
  --mode video_script \
  --platform tiktok \
  -m "TikTok 30秒产品展示视频脚本" \
  --product "美妆精华液" \
  --duration 30s \
  --lang zh
```

**主图差异化**

```bash
python scripts/run.py \
  --mode main_image \
  --platform amazon \
  -m "同类产品都是白底，我怎么做差异化主图" \
  --product "便携式咖啡机" \
  --competitor-ref "竞品主图都是正面白底" \
  --lang zh
```

**图片合规检查**

```bash
python scripts/run.py \
  --mode image_compliance \
  --platform amazon \
  -m "帮我检查这套主图是否符合 Amazon 要求" \
  --product "蓝牙耳机" \
  --image-description "白底主图+侧面图+场景图+尺寸对比图+包装图" \
  --lang zh
```

## 合规声明

- 不生成实际图片/视频文件
- 方案需人工审核后执行
- 遵守各平台内容政策与广告法规

## 版本记录

| 版本 | 日期 | 变更 |
|------|------|------|
| v1.1.0 | 2026-06-14 | SKILL.md added quickstart registration guide; 401/402 error messages now in Chinese with register links |
| v1.0.0 | 2026-06-13 | 规范 SKILL.md：补充 Agent 规则、Instructions、触发词、示例、环境变量、合规、版本记录 |
| v0.1.0 | — | 初始视觉工坊技能 |
