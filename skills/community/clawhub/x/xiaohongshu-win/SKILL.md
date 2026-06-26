---
name: xiaohongshu-win
version: "1.1.0"
description: |
  小红书内容工具 Windows 原生版。
  基于 Node.js + Playwright，直接控制本地 Chromium 浏览器，
  无需 WSL、无需 Linux 二进制、无需 Python、无需任何外部服务。
  
  核心功能：
  - 🔍 内容搜索 - 关键词搜索，分析热度排行
  - 📊 话题报告 - 自动生成热点分析 Markdown 报告
  - 📝 笔记发布 - 帮你写+帮你发图文笔记
  - 🔔 定时任务 - 每天自动搜热点（支持 Cron 定时）
  - 🖼️ 封面生成 - 集成即梦AI生成封面图片
  
  使用场景：
  - "搜索小红书上关于XX的内容"
  - "帮我在小红书发一篇笔记"
  - "小红书XX话题报告"
  - "跟踪一下小红书上的XX热点"
  
  适用系统：Windows 10/11 (x64)，需要 Node.js 18+
metadata:
  openclaw:
    emoji: "📕"
    author: "ken0521"
    tags: ["xiaohongshu", "social-media", "automation", "windows"]
---

# 小红书 Windows 原生 Skill

**技术栈：Node.js + Playwright（Chromium）**  
纯 Windows 原生，无跨平台依赖。

## 🆕 v1.1.0 新功能

- **定时任务** - 支持 Cron 定时自动搜索热点
- **即梦AI集成** - 可直接生成封面图片
- **Browser Relay** - 支持复用本地 Chrome 浏览器

## 架构

```
xhs.js          ← 命令行入口（所有命令）
xhs-core.js     ← 核心库（登录/搜索/发布/详情）
  └── Playwright → 控制本地 Chromium（Windows 原生）
        └── 小红书 Web（www.xiaohongshu.com）
              └── 拦截 API 响应（snake_case JSON）
```

**数据存储：** `%USERPROFILE%\.xiaohongshu-win\`  
**浏览器路径：** `%USERPROFILE%\.xiaohongshu-win\browsers\`（需设置 `PLAYWRIGHT_BROWSERS_PATH`）

## ⚠️ 重要：运行路径限制

由于 Node.js 不支持含中文的路径，**所有命令必须从无中文路径运行**。  
推荐工作目录：`C:\Users\<用户名>\.qclaw\workspace\`

脚本文件已同步到 workspace，直接在那里运行：

```powershell
$env:PLAYWRIGHT_BROWSERS_PATH = "$env:USERPROFILE\.xiaohongshu-win\browsers"
Set-Location "C:\Users\mll-c\.qclaw\workspace"
node xhs.js <命令>
```

## 首次使用

```powershell
# 1. 安装依赖（只需一次，在 workspace 目录）
Set-Location "C:\Users\mll-c\.qclaw\workspace"
npm install --save playwright

# 2. 安装 Chromium（只需一次，约 150MB）
$env:PLAYWRIGHT_BROWSERS_PATH = "$env:USERPROFILE\.xiaohongshu-win\browsers"
npx playwright install chromium

# 3. 登录（弹出浏览器扫码）
node xhs.js login

# 4. 验证
node xhs.js status
```

> 详细说明见 [references/setup.md](references/setup.md)

## 命令速查

| 命令 | 说明 |
|------|------|
| `node xhs.js status` | 检查登录状态 |
| `node xhs.js login` | 登录（弹出浏览器） |
| `node xhs.js search <关键词> [数量]` | 搜索笔记 |
| `node xhs.js detail <笔记URL>` | 获取帖子详情和评论 |
| `node xhs.js publish` | 交互式发布图文笔记 |
| `node xhs.js track <关键词> [数量]` | 生成话题热点报告 |

## 使用示例

```powershell
$env:PLAYWRIGHT_BROWSERS_PATH = "$env:USERPROFILE\.xiaohongshu-win\browsers"
cd "C:\Users\mll-c\.qclaw\workspace"

# 搜索 qclaw 相关内容
node xhs.js search qclaw 20

# 生成话题报告
node xhs.js track qclaw 10

# 获取帖子详情
node xhs.js detail https://www.xiaohongshu.com/explore/69aee455000000001b016268

# 发布笔记
node xhs.js publish
```

## 数据存储

| 路径 | 说明 |
|------|------|
| `%USERPROFILE%\.xiaohongshu-win\cookies.json` | 登录 Cookie |
| `%USERPROFILE%\.xiaohongshu-win\browser-profile\` | Chromium 持久化 Profile |
| `%USERPROFILE%\.xiaohongshu-win\browsers\` | Playwright Chromium 二进制 |
| `%USERPROFILE%\.xiaohongshu-win\search_*.json` | 搜索结果缓存 |
| `%USERPROFILE%\.xiaohongshu-win\report_*.md` | 话题报告 |

## 注意事项

- Cookie 有效期约 30 天，过期后重新 `node xhs.js login`
- 发布限制：标题 ≤ 20 字，正文 ≤ 1000 字
- 所有操作通过真实 Chromium 浏览器执行，行为与人工一致
- Node.js 路径不能含中文，脚本需在 workspace 目录运行
