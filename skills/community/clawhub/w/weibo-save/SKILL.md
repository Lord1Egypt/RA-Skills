---
name: weibo-save
description: 微博内容保存工作流。当用户发送微博链接（t.cn 短链接或 weibo.com 正文链接），或转发微博到微博龙虾助手时，自动执行：展开短链接 → 用 browser 抓取正文+图片 → 保存 Obsidian Markdown →（可选）推送飞书多维表格 →（可选）同步 Notion（含图片+作者头像）→（可选）生成发芽笔记。触发词：微博链接、t.cn、weibo.com、转发微博、保存微博。
---

# 微博内容保存工作流

收到微博链接或转发内容后，按以下步骤执行。

---

## 配置项（必须填写）

| 变量名 | 说明 | 示例 |
|--------|------|------|
| `{{OBSIDIAN_ROOT}}` | Obsidian 根目录（末尾无斜杠） | `/Users/xxx/Documents/notes` |
| `{{WEIBO_SAVE_SUBPATH}}` | 微博保存子目录 | `09_知识库/04_微博收藏日报` |
| `{{FEISHU_APP_TOKEN}}` | 飞书多维表格 app_token（不使用则留空） | `T5o8bAfiraUEI5sf1d0cQGAHnVd` |
| `{{FEISHU_TABLE_ID}}` | 飞书 table_id（不使用则留空） | `tblgXzbq712PlmwX` |
| `{{NOTION_API_KEY}}` | Notion API Key 路径（不使用则留空） | `~/.config/notion/api_key` |
| `{{NOTION_DATABASE_ID}}` | Notion database_id（不使用则留空） | `2ed1b1d7-1d88-81f5-bc5f-e1820c9e6d97` |
| `{{SPROUT_PROMPT_PATH}}` | 发芽笔记提示词路径（默认已设，无需修改） | `{{OBSIDIAN_ROOT}}/06_提示词库/文章内容处理/🌱发芽笔记.md` |
| `{{BROWSER_PROFILE}}` | Browser profile，推荐 `openclaw` | `openclaw` |

---

## Step 1 — 展开短链接并提取微博信息

### 1.1 展开 t.cn 短链接

```bash
curl -sIL "https://t.cn/xxx" 2>&1 | grep -i "^location:" | tail -1
```

解析重定向后的完整 URL，格式类似：`https://weibo.com/<uid>/<mid>`

### 1.2 识别微博正文页

- ✅ `https://weibo.com/<uid>/<mid>` — 微博正文页，需抓取
- ❌ `https://weibo.com/u/<uid>` — 用户主页，不抓
- ❌ `https://weibo.com/<uid>/<mid>#comment` — 评论页，去掉锚点取正文

## Step 2 — 用 browser 抓取微博正文

**⚠️ 重要：每次操作前必须先查 tab 列表！**

**抓取方式**：
1. 用 `browser action=tabs` 查询当前所有 tab，找到有没有已存在的 weibo tab
2. 如果有，用那个 tab 的 `suggestedTargetId`；如果没有，用 `browser action=open` 打开新 tab
3. 等待页面加载（`wait 3000-5000ms`）
4. 用 `snapshot` 或 `evaluate` 提取正文内容
5. **每次 evaluate/act 后都要验证 targetId 是否还匹配**，如果不匹配，重新 tabs 查询并获取新 targetId

**tab 查找逻辑**：
```javascript
// 先 tabs 拿到列表，找 url 包含 weibo.com 且不是个人主页的 tab
const weiboTab = tabs.find(t => 
  t.url && t.url.includes('weibo.com') && 
  !t.url.includes('/u/') &&
  t.label !== 'profile-picker'
);
// 用 weiboTab.tabId 或 weiboTab.suggestedTargetId 作为 targetId
```

**browser profile**：使用 `{{BROWSER_PROFILE}}` 配置的值（推荐 `openclaw`）。

**若 browser 方式失败（targetId stale 或 tab 失效）**：用 Jina Reader fallback：
```bash
curl -s "https://r.jina.ai/https://weibo.com/<uid>/<mid>"
```

## Step 3 — 下载微博图片（解决 Sinaimg 私网 IP 阻断）

**问题**：Sinaimg 域名解析到 `198.18.x.x` 私网 IP，被 SSRF 策略阻止，无法直接下载。

**解决方式**：
1. 用 browser 打开微博正文页时，通过 CDP evaluate 提取所有图片 URL
2. 遍历图片 URL，用 browser 的 `evaluate` 在页面内发请求获取图片 blob
3. 或直接用 browser 页面中已加载的图片元素提取其 blob URL

**图片保存目录**：
```
{{OBSIDIAN_ROOT}}/{{WEIBO_SAVE_SUBPATH}}/{YYYY}/{MM}/imgs/
```
统一保存到 `imgs/` 文件夹，不要按帖子分子目录。

**文件名命名**：使用原微博图片的文件名（从 URL 提取，如 `5d098bccly1icntlfpye7j20xb0c7dii.jpg`），不同帖子图片重名时自动覆盖。

**Markdown 图片语法**（必须使用，以便 Obsidian 渲染）：
```markdown
![](imgs/图片文件名.jpg)
```

## Step 4 — 保存 Obsidian Markdown

**目录**：`{{OBSIDIAN_ROOT}}/{{WEIBO_SAVE_SUBPATH}}/`

**子目录结构**：`年份/月份/`

**命名格式**：`{日期}-{标题清理后}.md`
- 日期格式：`YYYYMMDD`
- 标题清理：去掉非法字符（`/ \ : * ? " < > |`），过长截断至 80 字符，空格替换为 `-`

**文件内容格式**：
```markdown
---
url: https://weibo.com/1560906700/5293103692120235
title: DeepSeek突然更新了「识图模式」，正式入门了多模态的能力圈
author: 阑夕
published: 2026-04-29
source: 微博
platform: weibo
captured_at: 2026-05-03
---

微博正文内容...

---
图片: 
![](imgs/图片1.jpg)
![](imgs/图片2.jpg)

微博ID: <mid>
---
```

## Step 5 —（可选）推送飞书多维表格

**条件**：`{{FEISHU_APP_TOKEN}}` 和 `{{FEISHU_TABLE_ID}}` 均已填写。

**Bitable 配置**（需要在飞书建表并配置对应字段）：
- app_token：`{{FEISHU_APP_TOKEN}}`
- table_id：`{{FEISHU_TABLE_ID}}`
- 字段：微博链接、标题、作者、发布时间、全文、处理状态、平台

**字段名映射**（需要与实际表格字段名一致）：
| 功能字段 | 示例字段名 |
|----------|-----------|
| 微博链接 | `微博链接` |
| 标题 | `标题` |
| 作者 | `作者` |
| 发布时间 | `发布时间` |
| 全文 | `全文` |
| 处理状态 | `处理状态` |
| 平台 | `平台` |

**写入字段**：
- `微博链接`：`{"link": "https://weibo.com/...", "text": "微博标题"}`（URL 字段）
- `标题`：微博标题
- `作者`：微博作者
- `发布时间`：DateTime 毫秒时间戳
- `全文`：微博正文
- `处理状态` = `new`
- `平台` = `微博`

**写入方式**：
1. 先用 `feishu_bitable_create_record` 创建记录
2. 再用 `feishu_bitable_update_record` 更新 URL 字段

## Step 6 —（可选）同步 Notion（含图片文件）

**条件**：`{{NOTION_API_KEY}}` 和 `{{NOTION_DATABASE_ID}}` 均已填写。

### 6.1 微博收藏 Database

- database_id：`{{NOTION_DATABASE_ID}}`
- 字段：微博（title）、作者（rich_text）、微博链接（url）、评论时间（rich_text）、标签（multi_select）、我的评论（rich_text）

### 6.2 获取作者头像 URL

⚠️ **重要**：不要在微博正文页提取头像——正文页同时渲染当前登录用户头像（导航栏）和作者头像，容易混淆取到错误的。

**正确做法**：单独打开作者主页 `https://weibo.com/u/<uid>` 提取头像。

```javascript
// 在作者主页（weibo.com/u/<uid>）执行：
() => {
  // 方法1：找 class="photo" 的 img（个人主页头像）
  const photo = document.querySelector('img.photo');
  if (photo && photo.src.includes('sinaimg')) return photo.src;
  
  // 方法2：找 180x180 的一级页面大头像
  const imgs = document.querySelectorAll('img');
  for (const img of imgs) {
    if (img.naturalWidth === 180 && img.naturalHeight === 180 
        && img.src.includes('sinaimg.cn') && !img.src.includes('member') && !img.src.includes('vip')) {
      return img.src;
    }
  }
  return 'not found';
}
```

**验证头像 URL**：确保返回的 URL 包含 `/crop.0.0.` 或 `/180.180/`，格式如 `https://tva1.sinaimg.cn/crop.0.0.180.180/...`，这才是真实用户头像。

**uid 从何来**：从微博正文页 URL `https://weibo.com/<uid>/<mid>` 中提取第一个路径段即为作者 uid。

### 6.3 创建 Notion 页面（完整流程）

**Step A：用 Notion File Upload API 上传图片**

Notion 不支持外部 URL 图片块，只支持：
- `external`：外部公开 URL（私网 IP 不行）
- `file_upload`：**必须先通过 File Upload API 上传获取 file_upload id**

File Upload 分三步：
```bash
# Step 1: 创建上传对象
curl -X POST "https://api.notion.com/v1/file_uploads" \
  -H "Authorization: Bearer $NOTION_KEY" \
  -H "Notion-Version: 2026-03-11" \
  -H "Content-Type: application/json" \
  -d '{"filename": "xxx.jpg", "content_type": "image/jpeg"}'
# 返回 upload_url 和 id

# Step 2: 上传文件内容（multipart/form-data）
curl -X POST "$upload_url" \
  -H "Authorization: Bearer $NOTION_KEY" \
  -H "Notion-Version: 2026-03-11" \
  -F "file=@/path/to/image.jpg"

# Step 3: 在创建 page 或 append block 时使用 file_upload id
{
  "type": "file_upload",
  "file_upload": { "id": "<file_upload_id>" }
}
```

**Step B：创建 page 时带上 children blocks（含图片块）**

```python
def create_page(title, author, author_url, weibo_url, date_str, img_file_ids):
    blocks = [
        {"object": "block", "type": "callout", "callout": {
            "rich_text": [
                {"type": "text", "text": {"content": f"@{author}"}, "annotations": {"bold": True}},
                {"type": "text", "text": {"content": "  "}},
                {"type": "text", "text": {"content": weibo_url, "link": {"url": weibo_url}}},
            ],
            "icon": {"emoji": "📖"}  # 或 external 头像 URL
        }},
        {"object": "block", "type": "divider", "divider": {}}
    ]
    for p in body_paragraphs:
        blocks.append({"object": "block", "type": "paragraph", "paragraph": {
            "rich_text": [{"type": "text", "text": {"content": p}}]
        }})
        if "📸" in p:  # 找到图片标记段落
            for fid in img_file_ids:
                blocks.append({
                    "object": "block", "type": "image", "image": {
                        "type": "file_upload",
                        "file_upload": {"id": fid}
                    }
                })
    
    payload = {
        "parent": {"database_id": DB_ID},
        "properties": {...},
        "children": blocks
    }
```

**Step C：设置页面图标（page icon）为作者头像**

页面图标用 `PATCH /v1/pages/{page_id}` 设置：
```json
{
  "icon": {
    "type": "external",
    "external": {"url": "https://tva1.sinaimg.cn/crop.0.0.180.180/....jpg"}
  }
}
```

**Step D：设置 callout 块图标（callout icon）**

callout 图标同样用 `PATCH /v1/blocks/{block_id}` 设置：
```json
{
  "callout": {
    "icon": {
      "type": "external",
      "external": {"url": "https://tva1.sinaimg.cn/crop.0.0.180.180/....jpg"}
    }
  }
}
```

## Step 7 —（可选）生成发芽笔记

**条件**：`{{SPROUT_PROMPT_PATH}}` 文件存在。

### 7.1 何时跳过

用户明确说"仅保存"或"不发芽"时跳过。

### 7.2 提示词来源

路径：`{{SPROUT_PROMPT_PATH}}`

### 7.3 生成流程

1. 读取发芽提示词
2. 将微博正文作为"材料"输入
3. 使用默认模型生成发芽报告
4. 保存到同目录：`{微博文件名}__🌱发芽笔记.md`

## Step 8 — 完成后回复

回复用户，格式：
> ✅ 已保存  
> **标题**：《{微博标题}》  
> **作者**：{作者}  
> **保存路径**：`{{WEIBO_SAVE_SUBPATH}}/{年份}/{月份}/{文件名}.md`  
> **飞书**：已推送/未配置（按实际情况）  
> **Notion**：已同步/未配置（按实际情况，含{图片数}张图片 + 作者头像）  
> **发芽笔记**：已生成/已跳过（按用户要求）

---

## 附录：微博链接识别参考

| 类型 | 示例 | 处理方式 |
|------|------|----------|
| t.cn 短链接 | `http://t.cn/AXJZipwg` | 展开重定向获取真实 URL → 抓取 |
| 微博正文链接 | `https://weibo.com/1560906700/5293103692120235` | 直接抓取 |
| 用户主页 | `https://weibo.com/u/2803301703` | 不抓（仅链接） |
| 评论页 | `https://weibo.com/2803301703/N4O1SBV4b#comment` | 去掉锚点取正文 |

## 附录：已知的坑

1. **Sinaimg 私网 IP（198.18.x.x）**：不能用 curl/wget 直接下载，必须通过 browser 提取 blob
2. **baoyu 与 OpenClaw Chrome CDP 冲突**：必须用 `profile="openclaw"` 的 browser 方式
3. **Notion image block 只能通过 file_upload**：不能用 external URL（私网 IP）；也不能直接传 base64
4. **Notion page icon 和 callout icon 支持 external URL**：实测 external URL 可以直接设置，无需上传
5. **图片统一保存到 imgs/ 文件夹**：不要按帖子分子目录，避免引用路径混乱
6. **⚠️ 作者头像易混淆**：微博正文页会同时渲染当前登录用户头像（导航栏）和作者头像，在正文页用 `naturalWidth===180` 筛选会取到错误的用户头像。**必须**单独打开作者主页 `weibo.com/u/<uid>` 提取头像。
7. **飞书/Notion 可选**：如未配置对应 token，相关步骤自动跳过，不影响核心保存功能