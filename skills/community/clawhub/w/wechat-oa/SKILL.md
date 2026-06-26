---
name: wechat-oa
description: WeChat Official Account draft management toolkit. Trigger words: 看看草稿箱/查看草稿/草稿列表/公众号草稿/搜草稿/搜索草稿/创建草稿/新建草稿/发文章到公众号/推送文章/更新草稿/删除草稿/生成封面图/上传图片/生成配图. Official API, no third-party dependencies.
description_zh: 微信公众号草稿箱管理工具集。触发词（满足任一即触发）：看看草稿箱/查看草稿/草稿列表/公众号草稿/搜草稿/搜索草稿/按关键词找草稿/按标题搜/创建草稿/新建草稿/发文章到公众号/推送文章/更新草稿/删除草稿/批量删除草稿/生成封面图/上传图片到公众号/上传图片到素材库/已发布文章列表/公众号素材列表/素材管理/删除素材/交互式删除/批量删除素材/关键词过滤素材/生成配图/生成信息图。官方API，无需第三方依赖。
version: "1.4.0"
author: Woody
email: andy8663@163.com
wechat_mp: 用技术定义未来
homepage: https://github.com/andy8663/wechat-oa
metadata:
  openclaw:
    emoji: "📝"
    category: "publishing"
    requires:
      bins: ["python3"]
    voice_commands:
      - "查看草稿箱"
      - "看看公众号草稿"
      - "创建一篇公众号文章"
      - "推送文章到公众号"
      - "生成封面图"
      - "上传图片到素材库"
      - "生成正文配图"
---

# wechat-oa

微信公众号草稿箱管理工具集。基于官方微信 API，无需第三方依赖。

WeChat Official Account draft management toolkit. Built on official WeChat APIs, no third-party dependencies required.

## 特性 / Features

- **公众号排版规范** / WeChat MP layout specification：内置 `design.md` 排版规范，AI 生成 HTML 时必须遵循，确保公众号渲染兼容 / Built-in `design.md` layout spec that AI must follow when generating HTML, ensuring WeChat rendering compatibility
- **行内样式转换** / Inline-style conversion：自动将 HTML 中的 `<style>` 标签转换为行内 `style=""` 属性，兼容微信文章渲染（已固化到 skill） / Auto-converts `<style>` tags into inline `style=""` attributes for WeChat-compatible rendering (baked into this skill)
- **自动封面生成** / Auto cover generation：根据文章标题 AI 生成科技风封面图（2.35:1 比例） / AI-generated tech-style cover image from article title (2.35:1 ratio)
- **正文图片自动上传** / Auto inline image upload：自动提取 HTML/MD 中的本地图片，上传到微信素材库并替换 URL / Automatically extracts local images from HTML/MD, uploads to WeChat material library and replaces URLs
- **智能摘要** / Smart digest：自动从正文中选取含功能关键词的段落作为摘要，而非机械截取前80字 / Intelligently selects keyword-rich paragraphs as digest instead of blindly truncating at 80 chars

## ⚠️ 排版规范（必读） / Layout Specification (MUST READ)

**创建或更新公众号文章前，AI 必须先阅读 `design.md`，严格按其规范生成 HTML。**

Before creating or updating any WeChat article, AI MUST read `design.md` and strictly follow its rules to generate HTML.

`design.md` 规范涵盖 / `design.md` covers:
- 容器宽度（文章 677px / 图文卡片 375px）
- 字体规范（clamp() 响应式字号）
- 配色规范（≤5 主体色，对比度 ≥4.5:1）
- 布局规范（Flex/Grid only，禁止 absolute/float）
- 标题规范（禁止重复主标题、header 标签、左边框装饰）
- 内容结构（扁平结构，有/无背景色的 padding 规则不同）
- CSS/HTML/JS 限制（公众号渲染器兼容性白名单）

支持的创作类型 / Supported creation types:
- **文章**：通用类型，页面默认宽度 677px
- **贴图**：图文卡片（小绿书/小红书风格），页面默认宽度 375px，固定分页比例（默认 3:4）

## 功能与对应API / Commands & APIs

| 命令 Command | 说明 Description | 底层API Underlying API |
|------|------|---------|
| `list` | 查看草稿列表（含标题+时间）/ View draft list with title+time | `draft/batchget` |
| `find <关键词>` | 按标题关键词搜索草稿 / Search drafts by title keyword | `draft/batchget` |
| `create <文件>` | 创建新草稿（支持 .html 和 .md，自动上传正文配图）/ Create draft from HTML or MD (auto-upload inline images) | `draft/add` + 永久素材上传 |
| `update <media_id> <文件>` | 更新已有草稿（自动上传正文配图）/ Update existing draft (auto-upload inline images) | `draft/update` |
| `update <media_id> <文件> --force-cover` | 更新草稿并强制重新生成封面 / Update draft + force-regenerate cover | `draft/update` |
| `delete <media_id>` | 删除草稿 / Delete draft | `draft/delete` |
| `batch-del <id1> [id2] ...` | 批量删除草稿 / Batch delete drafts | `draft/delete` |
| `upload <图片文件>` | 上传图片到永久素材库 / Upload image to permanent material | `material/add_material` |
| `materialcount` | 获取各类永久素材总数 / Get permanent material count by type | `material/get_materialcount` |
| `materials [type] [count] [offset] [keyword]` | 批量获取素材列表，支持关键词过滤 / Batch list with keyword filter | `material/batchget_material` |
| `materialdel [media_id...]` | 批量删除素材（多个空格分隔）/ Batch delete materials | `material/del_material` |
| `materialdel` | 交互式删除（列出→选编号→确认）/ Interactive material deletion | `material/del_material` |
| `materialdel <type>` | 交互式删除指定类型 / Interactive deletion by type (news/image/video/voice) | `material/del_material` |
| `published` | 获取已发布文章列表 / List published articles | `material/batchget_material` |
| `cover <标题>` | 生成封面图预览（不推送）/ Generate cover preview (no push) | PIL local generation |
| `infographic <类型> <输出路径> [参数]` | 生成正文配图（流程图/对比图/时间线/文字卡片/统计图）/ Generate inline image (steps/comparison/timeline/textcard/stats) | PIL local generation |
| `userinfo <openid>` | 获取用户基本信息（需认证账号）/ Get user info by openid | `user/info` |
| `userlist [next_openid]` | 获取用户列表（需认证账号）/ List all users | `user/get` |

## 初始化配置 / Initial Setup

使用前必须完成以下配置：Complete the following before first use:

### 1. 获取 AppID 和 AppSecret / Get AppID & AppSecret

(1) 登录 [微信公众平台](https://mp.weixin.qq.com) / Log in to [WeChat Official Account Platform](https://mp.weixin.qq.com)
(2) 进入 **设置与开发 → 基本设置** / Go to **Settings & Development → Basic Settings**
(3) 复制 **公众号 AppID** 和 **公众号 AppSecret**（如未设置需先启用）/ Copy **AppID** and **AppSecret** (enable if not set yet)

### 2. 添加 IP 白名单 / Add IP Whitelist

调用微信 API 前，必须将服务器 IP 加入白名单：You must add your server's public IP to the whitelist before calling WeChat APIs:

(1) 进入 **设置与开发 → 安全中心** / Go to **Settings & Development → Security Center**
(2) 点击 **IP 白名单** / Click **IP Whitelist**
(3) 添加你的服务器公网 IP（查看当前 IP：`curl ifconfig.me`）/ Add your server's public IP (check: `curl ifconfig.me`)

> ⚠️ **不添加 IP 白名单会导致 API 调用失败！** / Not adding the IP whitelist will cause all API calls to fail!

### 3. 配置凭证 / Configure Credentials

将 `config.example.json` 复制为 `config.json`，填入你的凭证：Copy `config.example.json` to `config.json` and fill in your credentials:

```bash
cp config.example.json config.json
# 然后编辑 config.json，填入 APP_ID 和 APP_SECRET
# Then edit config.json, fill in APP_ID and APP_SECRET
```

`config.json` 示例 / Example:
```json
{
  "APP_ID": "wx0000000000000000",
  "APP_SECRET": "00000000000000000000000000000000",
  "author": "龙虾"  // 文章默认作者 / Default article author
}
```

> ⚠️ `config.json` 包含凭证，**不要提交到 GitHub**！已在 `.gitignore` 中忽略。 / `config.json` contains credentials — **do NOT commit to GitHub**! Already in `.gitignore`.

## 使用示例 / Usage Examples

```bash
# 查看草稿列表 / View draft list
python wechat_push.py list

# 创建新草稿（自动生成封面）/ Create new draft (auto-generate cover)
python wechat_push.py create article.html

# 更新已有草稿 / Update existing draft
python wechat_push.py update n2BZd2CzoCKkl... article.html

# 更新草稿 + 强制重绘封面 / Update draft + force regenerate cover
python wechat_push.py update n2BZd2CzoCKkl... article.html --force-cover

# 删除草稿 / Delete draft
python wechat_push.py delete n2BZd2CzoCKkl...

# 上传图片到永久素材 / Upload image to permanent material
python wechat_push.py upload cover.png

# 生成封面图预览（不推送到微信）/ Generate cover preview (no WeChat push)
python wechat_push.py cover "你的文章标题"

# 生成正文配图 / Generate inline infographic
python generate_infographic.py steps output/step.png "步骤1" "步骤2" "步骤3"
python generate_infographic.py comparison output/compare.png "优点:很好用" "缺点:有点贵"
python generate_infographic.py timeline output/timeline.png "2024:事件1" "2025:事件2"
python generate_infographic.py textcard output/quote.png "天下没有难汇的款"
python generate_infographic.py stats output/stats.png "满意度:85" "便利性:90"
```

## 依赖 / Dependencies

```bash
pip install requests Pillow
```

## 正文配图说明 / Inline Images Guide

### 自动上传流程 / Auto-upload Flow

创建或更新草稿时，系统会自动处理正文中的图片：

When creating or updating drafts, the system automatically processes inline images:

```
HTML/MD 文件
    ↓
提取 <img src="..."> 或 ![alt](path)
    ↓
本地图片？ ──是──→ 上传到微信素材库 ──→ 获取微信 URL
    ↓ 否                    ↓
网络图片？ ──是──→ 保留原 URL（可选下载上传）
    ↓ 否
跳过（已是微信素材库图片）
    ↓
替换 HTML 中的 src 为微信 URL
    ↓
推送草稿
```

### 支持的图片格式 / Supported Formats

- **HTML**: `<img src="local/image.png">` 或 `<img src="http://example.com/img.png">`
- **Markdown**: `![描述](./images/photo.jpg)`
- **路径类型**: 相对路径、绝对路径、`file:///` 协议

### 图片处理规则 / Image Processing Rules

| 图片类型 | 处理方式 | 说明 |
|---------|---------|------|
| 本地图片（相对/绝对路径） | 自动上传 | 上传后替换为微信素材库 URL |
| 网络图片（http/https） | 跳过 | 保留原 URL（微信可能过滤） |
| 微信素材库图片 | 跳过 | 已是 `mmbiz.qpic.cn` 域名 |
| 不存在的图片 | 报错提示 | 记录到失败列表，继续处理其他图片 |

### 使用示例 / Examples

```html
<!-- HTML 示例：本地图片会被自动上传 -->
<p>请看下图：</p>
<img src="./images/diagram.png" alt="架构图">
<img src="C:\Users\Photos\screenshot.jpg">

<!-- 网络图片保留原样（微信可能过滤） -->
<img src="https://example.com/external.png">
```

```markdown
<!-- Markdown 示例 -->
![本地图片](./assets/chart.png)  ← 自动上传
![网络图片](https://site.com/img.jpg)  ← 保留原样
```

### 注意事项 / Notes

1. **图片大小**: 建议单张 < 2MB，微信素材库有容量限制
2. **图片格式**: 支持 JPG、PNG、GIF，推荐使用 PNG
3. **路径问题**: 相对路径基于 HTML/MD 文件所在目录解析
4. **失败处理**: 上传失败的图片会记录但不会影响草稿创建

## 正文配图自动生成 / Auto Infographic Generation

### 功能说明

`generate_infographic.py` 可以根据章节内容自动生成配图，无需 AI API，完全本地 PIL 生成。

### 支持的配图类型

| 类型 | 用途 | 示例 |
|------|------|------|
| `steps` | 流程图 | 汇款步骤：注册→填表→汇款→完成 |
| `comparison` | 对比图 | 传统汇款 vs 西联汇款 |
| `timeline` | 时间线 | 2020→2022→2024 发展历程 |
| `textcard` | 文字卡片 | 金句、要点提炼 |
| `stats` | 数据统计图 | 各渠道手续费对比 |

### 使用方式

```bash
# 流程图（步骤流程）
python generate_infographic.py steps output/step.png "注册西联账号" "填写汇款信息" "完成汇款" "通知收款人"

# 对比图（两列对比）
python generate_infographic.py comparison output/compare.png "传统银行:3-5个工作日" "西联:几分钟到账"

# 时间线
python generate_infographic.py timeline output/timeline.png "2020:全球扩张" "2022:数字化转型" "2024:移动端上线"

# 文字卡片（金句/要点）
python generate_infographic.py textcard output/quote.png "天下没有难汇的款"

# 数据统计
python generate_infographic.py stats output/stats.png "手续费:最低" "到账速度:最快" "覆盖范围:最广"
```

### 配图插入文章流程

1. **生成配图**: 运行 `generate_infographic.py` 生成图片
2. **插入 HTML**: 在章节末尾添加 `<img src="配图路径">`
3. **推送**: 运行 `python wechat_push.py create article.html`
4. **自动上传**: 系统自动将本地图片上传到素材库

```html
<h2>三、汇款流程</h2>
<p>以下是完整的汇款步骤：</p>
<img src="./images/remit-steps.png" alt="汇款流程图">  <!-- 自动上传 -->
```

### 配图尺寸

- **宽度**: 677px（与公众号内容宽度一致）
- **高度**: 根据内容自动计算
- **格式**: PNG（透明背景支持）
- **字体**: Windows 微软雅黑 / 黑体

## 输出文件 / Output Files

- `draft_ids.txt` - 草稿记录（创建时间、标题、media_id）/ Draft log (timestamp, title, media_id)
- 封面图默认保存在 HTML 文件同目录 / Cover images saved in the same directory as the HTML file by default

## 问题反馈 / Feedback

遇到问题或功能建议？欢迎通过以下方式联系我们：

- 🌐 **GitHub Issues**：[https://github.com/andy8663/wechat-oa](https://github.com/andy8663/wechat-oa)
  - 提交 Bug 报告或功能请求 / Submit bug reports or feature requests
- 📧 **邮箱**：`andy8663@126.com`
  - 邮件咨询 / Email for inquiries
- 🔔 **微信公众号**：技术定义未来（ID: `gh_b906288c4c2f`）
  - 公众号文章首发平台 / Primary publishing platform for MP articles

> 💡 提交 Issue 前建议先搜索是否已有类似问题 / Please search existing issues before submitting new ones.
