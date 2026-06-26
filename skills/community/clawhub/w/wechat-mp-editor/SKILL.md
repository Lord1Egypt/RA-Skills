---
name: wechat-mp-editor
description: "Create, edit, and manage WeChat Official Account (公众号/服务号) articles via the official WeChat API. Handles access token management, image uploads, draft CRUD, publishing, and HTML content formatting with WeChat-compatible CSS. Trigger when the user asks to: write/edit WeChat articles, create/publish drafts, format WeChat push notifications, generate article HTML, or manage WeChat MP drafts through the API."
---

# WeChat MP Editor

## Overview

Full workflow: credentials → access token → image upload → draft creation → publishing.

**One fixed template** — visual branding consistent. Only content (text, date, banner) changes.

**Priority**: Write from [ideas queue](#-ideas-queue-灵感队列) first.

---

## Ideas Queue (灵感队列)

File: `skills/wechat-mp-editor/ideas-queue.json`

Status: `pending` / `writing` / `done` / `archived`

FIFO by default, or ask user. Empty queue → scan ClawHub/GitHub Trending → propose 3-5 topics.

---

## Prerequisites

Read before writing:
1. `references/templates.md` — 唯一排版规范
2. `references/review-checklist.md` — 发布前检查清单

---

## 严格规则

- padding 全篇 **20px**
- section **不嵌套**
- 含中文的 `<section>` 和 `<p>` 加 `word-break:normal;white-space:normal`
- footer：`padding:36px 20px 40px;text-align:center;`
- 品牌：`巡梦人`（`#bbb`）+ `从一颗星星开始，温暖整个宇宙`（`#aaa`）
- 高亮：每 2-4 段一处 `color:#d4a574`

---

## Workflow

### 0. Pre-writing

**0.1 实体确认** — 同名产品/公司先确认目标实体。

**0.2 信息收集 + 事实校验** — 两轮：广度收集 → 逐句核查论断性句子。

**0.3 方向确认** — 输出 3-5 句 What/Why/How。用户确认后再写。**如果中途文章结构发生重大变更**（改比喻方向、替换方案、增加大段内容），重新输出方向确认，不可直接下笔。

### 1. Credentials

`credentials/wechat-official.json`:

```json
{"name":"巡梦人","appId":"wx...","appSecret":"...","type":"wechat_mp"}
```

### 2. Get token

`GET https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=APPID&secret=***`

Returns `access_token`, valid 2h.

### 3. Upload images

**Body images** (`/cgi-bin/media/uploadimg`):
```bash
curl -s -F "media=@image.png" "https://api.weixin.qq.com/cgi-bin/media/uploadimg?access_token=***"
```
Returns `{"url": "http://mmbiz.qpic.cn/..."}`.

**Cover image** (`/cgi-bin/material/add_material`):
```bash
curl -s -F "media=@cover.png" "https://api.weixin.qq.com/cgi-bin/material/add_material?access_token=***&type=image"
```
Returns `{"media_id": "..."}`. **封面图必须 1:1 方形**，否则报 53402。

### 4. Build HTML

Use `references/templates.md`. Fill in variables at marked locations.

### 5. Submit draft

#### 编码规则（写死规则，不可违反）

`requests` 库的 `json=` 参数默认 `ensure_ascii=True`，会将中文转为 `\uXXXX` 转义码，微信编辑器显示为乱码。

**禁止使用** `requests.post(url, json=payload)`。

**必须使用** 以下两种方式之一：

**方式 A（推荐）：写文件 + curl**
```python
import json
with open('/tmp/draft.json', 'w', encoding='utf-8') as f:
    json.dump(payload, f, ensure_ascii=False)  # ensure_ascii=False 是必须的
```
```bash
curl -s -X POST "https://api.weixin.qq.com/cgi-bin/draft/add?access_token=***" \
  -H "Content-Type: application/json; charset=utf-8" \
  --data-binary @/tmp/draft.json
```

**方式 B（仅没有 curl 时）：**
```python
import json, requests
requests.post(url, data=json.dumps(payload, ensure_ascii=False).encode('utf-8'),
              headers={"Content-Type": "application/json"})
```

#### 迭代规则

第一次创建用 `draft/add`。后续所有修改用 `draft/update`，**不要重复 add 制造新草稿**。

```python
# 更新已有草稿
payload["media_id"] = "已有DRAFT_ID"
requests.post(".../draft/update?...", data=..., headers=...)
```

#### 提交后立即回读验证

```python
resp = requests.post(".../draft/get?...", json={"media_id": draft_id})
content = resp.json()["news_item"][0]["content"]

# 必须验证的内容
checks = {
    "title": "预期的标题",
    "已设置的中文摘要": True,
    "\\u": False,                # 必须为 False — 不得有转义码
    "[\u4e00-\u9fff]": True,    # 必须有真实中文字符
}
```

### 6. Publish

`POST /cgi-bin/freepublish/submit` with `{"media_id": "DRAFT_ID"}`.

---

## HTML Content Rules

- Inline CSS only, no `<style>` / `<script>`
- Images must be WeChat CDN URLs
- Body 15px / headline 24px / quote 22px / small 11-13px
- Line-height: body 2.0, cards 1.9
- Mobile-first: paragraphs ≤ 2-3 lines on 375px viewport

---

## 配图（即梦 AI）

文章用图通过 即梦 AI 由用户生成。本 skill 仅负责：
1. 确定每张图的叙事任务
2. 调用 dreamina-cli 生成提示词
3. 上传用户返回的图片到微信 CDN
4. 嵌入 HTML

不自行写提示词格式，不维护提示词经验池。

---

## 发布前自检清单（十项全过才能提交）

```
□ 移动端：每段 ≤35 中文字符，特征卡 ≤20 字符
□ 移动端：特征卡间距正确（首 N-1 张 12px，末张 0px）
□ 移动端：连续正文不超过 3 段，需插入图片/分隔线/特征卡
□ 格式：分隔线全篇 padding 统一为 12px 20px
□ 格式：footer 颜色 品牌名 #bbb / 标语 #aaa
□ 格式：section 开闭数一致（<section> 数 = </section> 数）
□ 封面：media_id 已更换（非上次文章的残留 ID）
□ 编码：提交后回读验证 content 无 \uXXXX 转义
□ 编码：提交后回读验证 content 有真实中文字符
□ 摘要：digest 已设置且前 54 字不是 HTML 标签
```

---

## References

- `references/templates.md` — 排版规范
- `references/review-checklist.md` — 检查清单
- `scripts/generate_images.py` — 图片生成
