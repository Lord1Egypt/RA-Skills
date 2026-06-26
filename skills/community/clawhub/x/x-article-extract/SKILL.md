---
name: x-article-extract
description: "提取 X/Twitter 内容：普通推文、X Article 长文、t.co 短链背后的外部网页"
metadata: {"openclaw":{"emoji":"𝕏","requires":{"bins":["python3","xreach","curl"]}}}
---

# X Article 内容提取技能

## 能力

从 X/Twitter 链接中提取完整内容，支持三种场景：

| 场景 | 方法 | 说明 |
|------|------|------|
| 普通推文 | xreach tweet | 直接提取推文文本+媒体 |
| X Article 长文 | Playwright + xreach cookie | 用无头浏览器打开 Article 页面抓取正文 |
| 推文分享外部链接 | Firecrawl API | 解析 t.co → 抓取目标网页内容 |

所有场景自动附带互动数据（浏览/赞/转发/收藏/评论数）。

## 触发条件

当用户要求提取 X/Twitter 内容时触发，包括但不限于：
- 「提取这条推文」「抓一下这个 X 链接」
- 「这条 X Article 讲了什么」
- 「帮我把这条推文内容拉出来」
- 直接给出 x.com / twitter.com 链接并要求分析内容

## 使用方式

### 1. 提取单条 X 链接

```bash
python3 ~/.openclaw/workspace/skills/x-article-extract/scripts/extract.py \
  --url "https://x.com/username/status/123456789"
```

输出 JSON，包含：
- `title`: 标题
- `author`: 作者
- `description`: 完整内容
- `engagement`: 互动数据
- `content_type`: `tweet` / `x_article` / `external_page`
- `word_count`: 内容字数

### 2. 提取并入库到内容工厂

```bash
python3 ~/.openclaw/workspace/skills/x-article-extract/scripts/extract.py \
  --url "https://x.com/username/status/123456789" \
  --ingest
```

自动将提取的内容写入内容工厂素材库（ObsidianAdapter），等同于在飞书群发链接 + 入库。

### 3. 批量提取

```bash
python3 ~/.openclaw/workspace/skills/x-article-extract/scripts/extract.py \
  --url "https://x.com/a/status/111" \
  --url "https://x.com/b/status/222"
```

### 4. 仅解析 t.co 短链（不提取内容）

```bash
python3 ~/.openclaw/workspace/skills/x-article-extract/scripts/extract.py \
  --resolve "https://t.co/abc123"
```

## 参数说明

| 参数 | 必填 | 说明 |
|------|------|------|
| `--url` | 是 | X/Twitter 链接（可多个） |
| `--ingest` | 否 | 提取后自动入库到内容工厂 |
| `--resolve` | 否 | 仅解析 t.co 短链，不提取内容 |
| `--json` | 否 | 输出原始 JSON（默认人类可读格式） |
| `--proxy` | 否 | 代理地址（默认从环境变量 HTTPS_PROXY 读取） |
| `-v` | 否 | 详细日志 |

## 依赖

- **xreach** (v0.3.0+): X/Twitter CLI，需已认证（`xreach auth check`）
- **Playwright** (python): 用于抓取 X Article（`pip install playwright && python3 -m playwright install chromium`）
- **Firecrawl API Key**: 用于抓取外部网页（环境变量 `FIRECRAWL_API_KEY`）
- **VPS 代理**: X 在国内被屏蔽，需走代理

## 注意事项

- xreach 认证 cookie 保存在 `~/.config/xfetch/session.json`，过期后需重新认证：`xreach auth extract --cookie-source chrome`
- Playwright 首次使用需安装浏览器：`python3 -m playwright install chromium`
- X Article 抓取需要 ~10 秒（Playwright 启动 + 页面渲染），普通推文 ~2 秒
- 如果 Playwright 失败，自动降级为 xreach thread 获取讨论上下文
