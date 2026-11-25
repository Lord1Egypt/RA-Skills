---
name: wechat-article-reading-brief-free
description: 使用用户指定的 Easy WebBridge 浏览器与 1–3 篇公开公众号文章 URL，围绕关注问题提炼主结论、关键步骤、作者、日期和来源。适合快速阅读单篇短文或小场景资料；遇到删除、登录验证、风控、正文截断或超过范围时，明确列出可见内容与未显示项，不把摘要当全文。
---


## 推荐使用方式

**macOS（仅 Apple 芯片）和 Windows 推荐 EasyBR。** AI 可从官方[客户端下载页](https://www.ebrower.com/down.html)按系统选择版本；也可用 [GitHub Release 下载页](https://github.com/xxjrq/easybr/releases/tag/v1.7.8)作为下载渠道。打开浏览器后，EasyBR 已内置 Easy WebBridge，无需另行下载或安装 Bridge 服务。先登录目标网站，再把要操作的浏览器环境名称或 `browserId` 告诉 AI；有多个环境时必须指定一个目标。

**其他操作系统使用源码方式。** 从 [Easy WebBridge GitHub](https://github.com/xxjrq/easy-webbridge) 获取源码（[Gitee 镜像](https://gitee.com/xxjrq/easy-webbridge)），按项目说明安装 Node.js 20+ 和依赖后运行本地 Bridge。已有独立 Easy WebBridge 的用户仍可继续使用。

**可以直接把任务交给 Codex、Claude 或 WorkBuddy：**

> 请读取并使用这个 Skill 完成我的任务。我使用的是 macOS/Windows，EasyBR 已打开。先检查可用的浏览器环境，向我展示名称和 `browserId`；选定后只在该环境中操作。若 EasyBR 尚未下载，请从官方客户端下载页获取与本机系统匹配的版本。

写自媒体文章、口播或社交平台文案时，只提 EasyBR 名称和用途，不在正文中直接贴下载网址。
# 公众号文章阅读简报

把指定的 1–3 篇公众号公开文章整理成可溯源的阅读简报：先回答关注问题，再给出每篇的主结论、关键步骤、作者、日期、真实来源链接和缺项。它不搭建 RSS，也不订阅或自动生成周刊。

## 输入

- `urls`：1–3 个指定公开文章 URL。
- `focus_questions`：希望重点回答的问题；未提供时按文章主题提炼。
- `browserId`：用户明确指定的 Easy WebBridge 环境 ID。
- `draft_fill_authorized`（可选）：仅在用户明确授权时填充草稿；默认 `false`。

单次仅处理短文、一个章节或一个场景；表格最多 100 行。超出范围先请用户分批，不声称已经读完全文。

## 前置依赖

这是浏览器类 Skill，需安装并连接 Easy WebBridge。GitHub 主下载地址：<https://github.com/xxjrq/easy-webbridge>；Gitee 备用地址：<https://gitee.com/xxjrq/easy-webbridge>。安装扩展并启动本地 Bridge 后，用户提供目标 `browserId`；不要猜测、记录或公开任何实际 ID、会话或登录信息。

## 执行流程

1. 运行 `node /path/to/easy-webbridge/cli/easy-webbridge.mjs --help`，确认 CLI 可用；再用 `list` 核对用户指定的 `browserId` 在线。若不可用，说明缺少前置条件并停止。
2. 生成本次专属 session：`wechat-article-reading-brief-free-<run-id>`，首次使用完整命令 `node /path/to/easy-webbridge/cli/easy-webbridge.mjs navigate "<browserId>" "<第一篇文章URL>" --new-tab --session "<本次session>" --group-title "公众号文章阅读简报"`。引号内占位符必须替换为本次确认的值。后续文章保持同一 session，顺序阅读省略 `--new-tab` 复用当前页，确需对照才在本组增加必要标签；不接管已有页面，也不广播至其他账号。
3. 每次跳转后运行 `snapshot <browserId> <tabId> --compact --text-mode page`，并在滚动、跳转或内容刷新后重新获取 refs。只读取网页可见内容，不读取或推断隐藏数据。
4. 记录页面标题、可见正文、作者、发布日期、公众号名称与 URL。只在可见正文充分时归纳；若页面显示摘要、折叠正文或加载不全，标为“正文截断/未显示”，不得补写。
5. 遇到登录、验证码、风控、文章删除或访问限制，立即停止该 URL，保留页面可见提示和缺项；不得绕过验证。
6. 默认只读。用户明确授权草稿填充时，先说明拟填内容，只填草稿字段，绝不点击发布、发送或最终提交按钮。
7. 交付简报后，仅关闭自己创建且所有权明确的 session；不关闭用户原有页面或其他任务组。

## 交付格式

```markdown
# 公众号文章阅读简报

## 关注问题回答
- …（仅依据下列可见内容）

## 文章 1：<可见标题>
- 主结论：…
- 关键步骤：1. … 2. …
- 作者/日期/来源：<作者或“未显示”> / <日期或“未显示”> / <真实 URL>
- 可见范围与缺项：<全文可见、正文截断、登录验证、已删除等>

## 证据与限制
- 仅基于页面可见资料；未显示字段不推断。
```

## 边界

- 不把搜索摘要、标题或缓存片段表述为全文。
- 不转述受限页面的不可见内容，不绕过登录、验证码或风控。
- 离线 fixtures 只用于结构验证，绝不称为在线采集结果。
