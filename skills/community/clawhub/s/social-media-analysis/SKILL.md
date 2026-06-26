---
name: social-media-analysis
description: |
  社交媒体舆情数据分析工具。从飞书多维表格读取 URL，下载媒体，分析内容，生成摘要。

entrypoint:
  command: "node"
  args:
    - "scripts/run_backfill.js"

inputs:
  - name: app_id
    type: string
    required: false
    description: 飞书开放平台应用 APP_ID
  - name: app_secret
    type: string
    required: false
    description: 飞书开放平台应用 APP_SECRET
  - name: bitable_url
    type: string
    required: false
    description: 飞书多维表视图链接（base/...?...&table=...）

  - name: only_empty
    type: string
    required: false
    default: "1"
    description: 只补空值（1/0），默认只填空
  - name: limit
    type: integer
    required: false
    default: 50
    description: 本次最多回填多少条记录（测试/防爆用）

  - name: workers
    type: integer
    required: false
    default: 4
    description: 并发 worker 数

  - name: max_chars
    type: integer
    required: false
    default: 100
    description: 内容解析最大长度

  - name: source_channel_field
    type: string
    required: false
    default: "来源渠道"
    description: 多维表字段名（来源渠道）
  - name: original_url_field
    type: string
    required: false
    default: "原文URL"
    description: 多维表字段名（原文URL；脚本内也做了候选兜底）

  - name: xhs_cookie
    type: string
    required: false
    description: 小红书 Cookie（可选）

permissions:
  network:
    - "https://open.feishu.cn"

outputs:
  - name: ok
    type: boolean
    description: 执行是否成功
---

  **脚本清单**：
  - `scripts/run_backfill.js` - Clawhub 入口（依次跑多渠道回填 + 微博回填）
  - `extract-douyin-images.js` - 抖音图集下载
  - `parse-douyin-video.js` - 抖音视频/音频下载
  - `parse-weibo.js` - 微博图集下载
  - `backfill-weibo-content-analysis.js` - 微博正文回填到「内容解析」
  - `backfill-content-analysis-by-source.js` - 多渠道原文URL回填「内容解析」
  - `parse-xiaohongshu.js` - 小红书图集下载
  - `parse-toutiao-playwright.js` - 今日头条 Playwright 渲染下载
  - `parse-bilibili.js` - B 站视频下载
  - `build-content-analysis.js` - 统一内容解析生成（100字内，带兜底）

  **使用场景**：
  (1) 分析飞书多维表格中的社交媒体数据
  (2) 批量下载媒体文件（图片/视频）
  (3) 生成 100 字内容解析
 (4) 用户提到"舆情分析"、"社交媒体分析"

# Social Media Analysis Skill

## 🎯 功能

- URL 有效性检查
- 媒体类型判断（图片/视频）
- 媒体文件下载
- 视频抽帧（每 5 秒 1 帧）
- 内容解析生成（100 字以内）

---

## 📋 工作流

```
1. 创建字段 → 2. 链接检查 → 3. 下载媒体 → 4. 抽帧分析 → 5. 更新表格
```

### 步骤 1: 创建字段

```bash
# 链接是否有效（单选）
# 包含多媒体类型（单选：图片/视频）
# 内容解析（文本）
```

### 步骤 2: 链接检查

| 平台 | 方法 |
|------|------|
| 抖音 | 脚本解析（不能用 HEAD） |
| 微博/今日头条/B 站 | HEAD 请求 |
| 快手 | 特殊处理 |

### 步骤 3: 下载媒体

| 平台 | 视频 | 图集 |
|------|------|------|
| 抖音 | `parse-douyin-video.js` | `extract-douyin-images.js` |
| 微博 | `yt-dlp` | `parse-weibo.js` |
| 今日头条 | `yt-dlp` | `parse-toutiao-playwright.js` |
| B 站 | `yt-dlp` | - |

### 步骤 4: 抽帧分析

```bash
# 视频抽帧（每 5 秒）
ffmpeg -i video.mp4 -vf "fps=1/5" frames/frame_%03d.jpg

# 图片分析
image frame_001.jpg "描述画面内容"
```

### 步骤 4.5: 统一生成内容解析（强制）

```bash
node scripts/build-content-analysis.js \
  --title "标题" \
  --text "正文" \
  --platform "微博" \
  --media-type "视频" \
  --visual "抽帧/图片识别结果"
```

规则：
- 必须输出 `content_analysis`，不可为空。
- 长度限制 100 字以内。
- 优先描述与“小米/小爱”相关信息；无相关信息时如实描述内容。

### 步骤 5: 更新表格

```bash
curl -X PUT "https://open.feishu.cn/open-apis/bitable/v1/apps/APP/tables/TBL/records/REC" \
  -H "Authorization: Bearer TOKEN" \
  -d '{"fields": {"链接是否有效": "是", "包含多媒体类型": "视频", "内容解析": "..."}}'
```

---

## 🔧 前置准备

### 认证

```bash
APP_ID="cli_a93d6e8a913a5bc8"
APP_SECRET="<your_secret>"

TOKEN=$(curl -s -X POST https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal \
  -H "Content-Type: application/json" \
  -d "{\"app_id\": \"$APP_ID\", \"app_secret\": \"$APP_SECRET\"}" | jq -r '.tenant_access_token')
```

### 工具

| 工具 | 用途 |
|------|------|
| `yt-dlp` | 微博/B 站视频下载 |
| `ffmpeg` | 视频抽帧 |
| `node` | 运行 JS 脚本 |
| `playwright` | 今日头条渲染 |

---

## 📱 平台下载方法

### 抖音

```bash
# 判断类型
node scripts/extract-douyin-images.js URL /tmp/check

# 视频
node scripts/parse-douyin-video.js URL --download

# 图集
node scripts/extract-douyin-images.js URL ./images
```

### 微博

**判断类型**：
```bash
yt-dlp --list-formats URL 2>&1 | grep -q "No video formats"
# 有 "No video formats" = 图文，无 = 视频
```

**下载方法**：

| 类型 | 方法 |
|------|------|
| **视频** | `yt-dlp -o video.mp4 URL` |
| **图文（1-9 张）** | 浏览器获取 + curl 下载 |

**图文下载脚本**：
```bash
# 方法 1：浏览器获取图片 URL
node -e "
const { chromium } = require('playwright');
(async () => {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();
  await page.goto('https://weibo.com/USER/ID', { waitUntil: 'domcontentloaded' });
  await page.waitForTimeout(5000);
  const images = await page.evaluate(() => {
    return Array.from(document.querySelectorAll('img[src*=\\\"sinaimg\\\"]'))
      .map(img => img.src.replace('orj360', 'mw690'));
  });
  console.log(images.join('\n'));
  await browser.close();
})().catch(console.error);
"

# 方法 2：curl 下载
curl -sL "IMAGE_URL" -o "images/image-01.jpg"
```

**注意**：
- parse-weibo 脚本可能误判，应以 yt-dlp 为准
- 微博图片域名：sinaimg.cn（wx1-4, tvax1-4, ww1-3）
- 图片尺寸：orj360（小）→ mw690（中）→ mw2000（大）

### 今日头条

```bash
# 文章图片
node scripts/parse-toutiao-playwright.js URL ./output

# 视频（yt-dlp 原生支持）
yt-dlp -o video.mp4 URL
```

### B 站

```bash
yt-dlp -o video.mp4 URL
```

### 小红书

```bash
# 判断类型
yt-dlp --dump-json URL | jq '.duration'

# 视频
yt-dlp -o video.mp4 URL

# 图集（需 Cookie）
node scripts/parse-xiaohongshu.js URL ./images
```

---

## ⚠️ 注意事项

1. **抖音链接检查**：必须用脚本解析，HEAD 请求会触发反爬
2. **抖音图集**：只有音频（M4A）+ 图片（WebP），无视频流
3. **今日头条**：需要 Playwright 渲染，静态 HTML 无图片
4. **抽帧标准**：统一每 5 秒 1 帧
5. **内容解析**：基于实际画面描述，不编造

---

## 📚 示例

### 处理单条记录

```bash
# 1. 检查链接
node scripts/parse-douyin-video.js URL --download

# 2. 抽帧
ffmpeg -i video.mp4 -vf "fps=1/5" frames/frame_%03d.jpg

# 3. 分析
image frames/frame_001.jpg "描述画面"

# 4. 更新表格
curl -X PUT "..." -d '{"fields": {...}}'
```

### 批量处理

```bash
# 见 WORKFLOW_V2.md 完整脚本
```

---

## 🔗 相关文档

- `WORKFLOW_V2.md` - 完整工作流脚本
- `memory/2026-03-23.md` - 执行记录
