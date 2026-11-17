---
slug: wechat-oa
displayName: 微信公众号草稿箱管理工具
summary: 微信公众号草稿箱管理工具集，支持创建/更新/删除草稿、上传素材、生成封面图，基于官方API。
license: MIT
name: wechat-oa
description: WeChat Official Account draft management toolkit. Trigger words: 看看草稿箱/查看草稿/草稿列表/公众号草稿/创建草稿/新建草稿/发文章到公众号/推送文章/更新草稿/删除草稿/生成封面图/上传图片. Official API.
description_zh: 微信公众号草稿箱管理工具集。触发词（满足任一即触发）：看看草稿箱/查看草稿/草稿列表/公众号草稿/创建草稿/新建草稿/发文章到公众号/推送文章/更新草稿/删除草稿/生成封面图/上传图片到公众号/上传图片到素材库/公众号素材列表/素材管理/删除素材/摘要生成/生成文章摘要。官方API。
version: "3.0.3"
author: Woody
email: andy8663@126.com
wechat_mp: 技术定义未来
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
      - "生成文章摘要"
---

# wechat-oa

微信公众号草稿箱管理工具集。基于官方微信 API。

WeChat Official Account draft management toolkit. Built on official WeChat APIs.

---

## ⚠️ 使用前必读 / MUST READ BEFORE USE

**创建或更新公众号文章前，AI 必须先阅读 `design.md` 排版规范。**

Before creating or updating any WeChat article, AI MUST read `design.md` layout specification first.

**涵盖内容 / Covers:**
- 容器宽度（文章 677px / 图文卡片 375px）
- 字体规范（clamp() 响应式字号）
- 配色规范（≤5 主体色，对比度 ≥4.5:1）
- 布局规范（Flex/Grid only，禁止 absolute/float）
- 标题规范（禁止重复主标题、header 标签、左边框装饰）
- 内容结构（扁平结构，有/无背景色的 padding 规则不同）
- CSS/HTML/JS 限制（公众号渲染器兼容性白名单）

📖 **完整规范见 `design.md`**

---

## 🚀 快速开始 / Quick Start

### 1. 安装 / Install

```bash
pip install wechat-oa
```

### 2. 配置凭证 / Configure Credentials

```bash
cp config.example.json config.json
# 编辑 config.json，填入 APP_ID 和 APP_SECRET
# Edit config.json, fill in APP_ID and APP_SECRET
```

### 3. 试试看 / Try It Out

```bash
# 查看草稿列表
wechat-oa list

# 创建新草稿
wechat-oa create article.md --digest "这是文章摘要"
```

---

## 📦 安装与配置 / Installation & Configuration

### 获取 AppID 和 AppSecret / Get AppID & AppSecret

1. 登录 [微信公众平台](https://mp.weixin.qq.com)
2. 进入 **设置与开发 → 基本设置**
3. 复制 **公众号 AppID** 和 **公众号 AppSecret**（如未设置需先启用）

### IP 白名单配置 / IP Whitelist Configuration

调用微信 API 前，必须将服务器 IP 加入白名单：

| 推送模式 | 需要加入白名单的 IP | 说明 |
|---------|------------------|------|
| `direct` | 本机出口 IP | 直连微信 API，配本机 IP |
| `hybrid` | 本机出口 IP | 优先直连，失败自动切中转 |
| `relay` | **服务器 IP** `120.79.2.44` | 通过中转服务器调用微信 API |

**配置步骤：**
1. 登录微信公众平台
2. 进入 **设置与开发 → 安全中心 → IP 白名单 → 点击「配置」**
3. 填入对应模式的 IP（多个 IP 用回车分隔）
4. 保存

> ⚠️ **不添加 IP 白名单会导致 API 调用失败！**

💡 **不方便配本机 IP 白名单？** 使用 `hybrid` 或 `relay` 模式，只需将服务器 IP `120.79.2.44` 加入白名单即可。

### 配置文件 / Config File

将 `config.example.json` 复制为 `config.json`，填入你的凭证：

> ⚠️ **注意**：`config.json` 必须使用标准 JSON 格式，**不要保留 `//` 注释**，否则会导致解析错误。

```json
{
  "default_account": "main",
  "current_account": "main",
  "PUSH_MODE": "hybrid",
  "WECHAT_OA_SERVER": "https://synergyinfo.tech",
  "WECHAT_OA_SERVER_KEY": "",
  "ENV": "prod",
  "accounts": {
    "main": {
      "name": "主公众号",
      "author": "你的名字",
      "voice_name": ["主号", "主公众号"],
      "APP_ID": "wx0000000000000000",
      "APP_SECRET": "00000000000000000000000000000000"
    }
  }
}
```

`PUSH_MODE` 说明：

| 模式 | 说明 | 适用场景 |
|------|------|----------|
| `direct` | 直连微信官方 API | IP 固定且可配白名单 |
| `relay` | 通过中转服务器推送 | IP 不固定，无法配白名单 |
| `hybrid` | 优先直连，失败自动切换中转 | **推荐** — 兼顾速度与稳定性 |

> 🔑 **如何获取 WECHAT_OA_SERVER_KEY？**  
> 访问同协云平台订购月卡获取卡密：[https://saas.synergyinfo.tech/products/wechat-oa](https://saas.synergyinfo.tech/products/wechat-oa)

> ⚠️ `config.json` 包含凭证，**不要提交到 GitHub**！已在 `.gitignore` 中忽略。

---

## 📝 核心功能 / Core Features

### 草稿管理 / Draft Management

| 命令 | 说明 | 示例 |
|------|------|------|
| `list` | 查看草稿列表 | `wechat-oa list` |
| `create <文件>` | 创建新草稿（支持 .html 和 .md） | `wechat-oa create article.md` |
| `update <media_id> <文件>` | 更新已有草稿 | `wechat-oa update <media_id> article.md` |
| `delete <media_id>` | 删除草稿 | `wechat-oa delete <media_id>` |

### 素材管理 / Material Management

| 命令 | 说明 | 示例 |
|------|------|------|
| `upload <图片>` | 上传图片到永久素材库 | `wechat-oa upload cover.png` |
| `count` | 获取素材总数 | `wechat-oa count` |
| `materials [type]` | 批量获取素材列表 | `wechat-oa materials image` |
| `del-material <media_id>` | 删除素材 | `wechat-oa del-material <media_id>` |

### 自动功能 / Auto Features

- **自动封面生成**：根据文章标题生成科技风封面图（2.35:1 比例）
- **智能摘要**：AI 推送文章时生成 1-2 句精准摘要传入 `--digest` 参数

---

## 🎨 高级功能 / Advanced Features

### 中继模式 (Relay Mode) / AI 收支付

当 `config.json` 中 `PUSH_MODE` 设为 `relay` 时，文章通过公网服务器（wechat-oa-server）中转推送到微信公众号。中继模式支持 **支付宝 AI 收** 标准协议（HTTP 402 + Payment-Needed）。

**推送流程（免费模式）：**
```bash
wechat-oa create article.md
```

**推送流程（收费模式）：**
1. 调用 create → 服务端返回 HTTP 402 + Payment-Needed
2. 客户端保存 Payment-Needed → 调用 `alipay-bot` 发起支付
3. 用户扫码完成支付 → 告诉 Agent "已支付"
4. 调用 `finish_push(trade_no, payload)` → 服务端验证 → 执行推送

### 摘要（digest）生成规范 / Digest Generation

**推送或更新文章时，AI 必须生成摘要并传入 `--digest` 参数，不要留空让服务端自动提取。**

**摘要生成步骤：**
1. 读取文章全文（MD/HTML 文件内容）
2. 识别文章类型（技术文章、产品介绍、资讯、教程等）
3. 提取核心观点或亮点（不是简单截取开头）
4. 用 1-2 句话概括，语言简洁有吸引力
5. 确保不超过 120 字（微信限制 128 字，留余量）

**摘要要求：**

| 维度 | 规范 |
|------|------|
| 长度 | 1-2 句话，不超过 120 字（微信限制 128 字，留余量） |
| 内容 | 概括文章核心观点或亮点，不是机械截取正文前几句 |
| 风格 | 简洁有吸引力，让读者在公众号消息列表中有点击欲望 |
| 语言 | 与文章正文语言一致 |

**示例：**
- 文章：介绍一款新的 AI 编程工具
- 摘要："这款 AI 编程助手能自动补全代码，支持 20+ 编程语言，让你的开发效率提升 3 倍！"

**命令示例：**
```bash
wechat-oa create article.md --digest "这款 AI 编程助手能自动补全代码..."
```

---

## 📚 命令参考 / Command Reference

| 命令 Command | 说明 Description | 底层API Underlying API |
|------|------|---------|
| `list` | 查看草稿列表（含标题+时间） | `draft/batchget` |
| `get <media_id>` | 获取单篇草稿详情 | `draft/get` |
| `create <文件> --digest <摘要>` | 创建新草稿（支持 .html 和 .md） | `draft/add` |
| `create <文件> --force-cover` | 创建草稿并强制生成封面 | `draft/add` |
| `update <media_id> <文件>` | 更新已有草稿 | `draft/update` |
| `delete <media_id>` | 删除草稿 | `draft/delete` |
| `upload <图片文件>` | 上传图片到永久素材库 | `material/add_material` |
| `count` | 获取各类永久素材总数 | `material/get_materialcount` |
| `materials [type]` | 批量获取素材列表 | `material/batchget_material` |
| `del-material <media_id>` | 删除素材 | `material/del_material` |
| `cover <标题>` | 生成封面图预览（不推送） | PIL local generation |

---

## 🖼️ 正文图片处理 / Inline Image Processing

### 自动上传流程 / Auto-upload Flow

创建或更新草稿时，系统会自动处理正文中的图片：

```
HTML/MD 文件
    ↓
提取 <img src="..."> 或 ![alt](path)
    ↓
本地图片？ ──是──→ 上传到微信素材库 ──→ 获取微信 URL
    ↓ 否
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

---

## ❓ 常见问题 / FAQ

### Q1：为什么我的文章段落之间没间距？

A：微信渲染器会删除所有 `margin`。解决方法：用 `<br>` 代替，详见 `design.md`。

### Q2：为什么标题颜色没生效？

A：可能 CSS 里 `color` 属性出现了两次，后面的覆盖前面的。检查 `design.md` 的 CSS 限制章节。

### Q3：推送时提示 IP 不在白名单？

A：按照"安装与配置 → IP 白名单配置"章节，将对应 IP 加入白名单。

---

## 💡 特性 / Features

- **公众号排版规范** / WeChat MP layout specification：内置 `design.md` 排版规范，AI 生成 HTML 时必须遵循
- **行内样式转换** / Inline-style conversion：自动将 HTML 中的 `<style>` 标签转换为行内 `style=""` 属性，兼容微信文章渲染
- **自动封面生成** / Auto cover generation：根据文章标题生成科技风封面图（2.35:1 比例）
- **正文图片自动上传** / Auto inline image upload：自动提取 HTML/MD 中的本地图片，上传到微信素材库并替换 URL
- **智能摘要** / Smart digest：AI 推送文章时生成 1-2 句精准摘要

---

## 📝 输出文件 / Output Files

- 封面图默认保存在 `.cache/cover.png`

---

## 🐛 问题反馈 / Feedback

- 🌐 **GitHub Issues**：[https://github.com/andy8663/wechat-oa](https://github.com/andy8663/wechat-oa)
- 📧 **邮箱**：`andy8663@126.com`
- 🔔 **微信公众号**：技术定义未来（ID: `gh_b906288c4c2f`）

> 💡 提交 Issue 前建议先搜索是否已有类似问题

---

## 📖 相关文档 / Related Documents

- **`design.md`** - 排版风格规范（必读）
- **`README.md`** - 项目介绍与安装指南
