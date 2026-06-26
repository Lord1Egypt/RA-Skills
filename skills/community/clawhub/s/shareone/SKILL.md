---
name: shareone
slug: shareone
displayName: ShareOne
version: 1.2.2
summary: 发布文件或内容到 ShareOne 并生成公网分享链接
description: 发布本地生成的 HTML、Markdown、TXT、PDF、Word 或 PPTX 到 ShareOne 平台，生成公网分享短链接；或者当用户提供 ShareOne 链接并要求下载文件、修改文件、拉取/处理评论时使用此技能。当用户要求“发布”、“分享”、“生成链接”、“上线”，或者“下载这个链接的文件”、“修改这个 ShareOne 链接的内容”、“拉取这个链接的评论”时，必须使用此技能。
tags: [shareone, publish, sharing]
license: MIT
---

# AI Agent 技能：发布到 ShareOne (shareone)

这个 Skill 允许 AI Agent 将当前生成的历史会话以及 HTML/Markdown/TXT/PDF/PPT 等文件发布到 ShareOne 线上托管服务，并为用户生成一个持久化的公网分享链接；也可以对已有 ShareOne 链接执行下载、内容更新、设置修改和评论处理。

## 脚本执行基准

本文档中所有 `node scripts/xxx.js` 命令的路径都以 **本 skill 的安装目录**（即本 `SKILL.md` 所在目录）为基准。当前工作目录通常是用户的项目目录，直接执行相对路径会失败。执行前先确定 skill 目录，使用绝对路径或先 `cd` 到 skill 目录，例如：

```bash
node /path/to/shareone-skill/scripts/ensure_credentials.js
```

## 入口隔离规则

本 skill 和用户本机可能安装的 `shareone` CLI 是两个独立入口。除非用户明确要求“使用 CLI”或指定执行 `shareone ...` 命令，否则不要调用系统 PATH 中的 `shareone` 命令。即使 `which shareone` 能找到 CLI，也不要把自然语言的发布、下载、评论处理任务改走 CLI。所有 ShareOne 操作都必须调用本 skill 目录内 `scripts/` 下的脚本。

## 使用说明与触发条件

当用户表达出以下意图时，应主动使用此技能：

- "帮我把 `index.html` 发布到 ShareOne"
- "把我刚才生成的网页发布，给我个链接"
- "生成一个可分享的链接给我的团队看"
- "Upload this presentation to ShareOne and protect it with password 'secret'"
- "发布这个 PDF 到 ShareOne，并加上密码 1234"
- "把这个网页发布到 ShareOne，加上水印 '内部绝密'"
- "把这个网页发布到 ShareOne，链接叫 product-demo"
- "发布这份设计稿并开启协同评论模式"
- "用 shareone 分享上一轮对话"
- "把我刚才写的代码/大段文字分享出去"
- "Share your last response as a note"
- "帮我下载这个 ShareOne 链接的文件：https://s.shareone.vip/s/xxx"
- "拉取一下这个链接的评论：https://s.shareone.vip/s/xxx"
- "给这个 ShareOne 链接加水印：https://s.shareone.vip/s/xxx"
- "根据这个链接的评论修改页面：https://s.shareone.vip/s/xxx"
- "修改这个 ShareOne 链接的内容：https://s.shareone.vip/s/xxx"

## 路由判定顺序（唯一路由依据）

入口文件只负责判断用户意图、选择需要阅读的 workflow。不要一次性读取所有 `workflows/*.md`；只读取当前任务命中的子文件。

按以下顺序从上到下判断，**命中第一条即停止**，按该条给出的阅读顺序执行：

1. **删除/清除/移除/重置 ShareOne API Key**
   → 读 `workflows/delete-api-key.md`。无需凭据检查。

2. **用户提供已有 ShareOne 链接、`share_id` 或 slug，且只要求修改水印、访问密码、自定义短链接或评论开关（不改内容本身）**
   → 先读 `workflows/environment-and-credentials.md`，再读 `workflows/update-share-settings.md`，最后读 `workflows/result-and-errors.md`。
   这是元数据更新：不要按文件类型路由，不要下载源文件，不要使用 `publish.js`，不要重新上传内容。对二进制文件链接（`/pdf/`、`/ppt/`、`/word/`）同样适用本条。

3. **下载 ShareOne 链接的文件或取回源内容**
   → 读 `workflows/download-file.md`。下载脚本会在已有凭据时优先尝试 owner 下载，没有凭据时自动走公开下载；不要为了普通下载强制配置 API Key。

4. **只查看、拉取、总结 ShareOne 链接评论（用户没有要求修改）**
   → 读 `workflows/comments-view.md`。查看评论走公开接口，无需凭据检查。

5. **处理评论、根据评论修改页面、修复 ShareOne 链接内容**
   → 先读 `workflows/environment-and-credentials.md`，再读 `workflows/comments-process.md`（其中的重新发布步骤会引用 `workflows/publish-text-page.md`），最后读 `workflows/result-and-errors.md`。

6. **发布、分享、生成链接、上线（创建新链接或更新已有链接的内容）**
   → 先读 `workflows/environment-and-credentials.md`，再按目标文件类型二选一，最后读 `workflows/result-and-errors.md`：
   - `.ppt`、`.pptx`、`.pdf`、`.doc`、`.docx`、`.png`、`.jpg`、`.jpeg`、`.gif`、`.zip` 或其他二进制文件 → `workflows/publish-binary-file.md`
   - `.html`、`.md`、`.txt`、对话内容、大段文本、代码块、已包装成 HTML 的内容 → `workflows/publish-text-page.md`。注意：`.md`/`.txt` 一律按原格式发布，不要因为内容包含图表就转成 HTML；只有目标本来就是 HTML 页面时才参考其中的 Mermaid.js 章节。

所有需要 ShareOne API 的操作（上面第 2、3、5、6 条），都先运行 `node scripts/ensure_credentials.js`，输出 token 含义与处理流程见 `workflows/environment-and-credentials.md`，这里不重复。

## ShareOne 链接与 share_id

- 用户提供的目标可以是完整链接、`/s/<ref>` 等路径、裸 `share_id`（16 位字符串）或自定义短链 slug。服务端接口同时接受 `share_id` 和 slug，无需自行区分两者。
- `/s/<share_id>` 是最终给用户访问的分享链接，**不是上传 API endpoint**。不要把 `/s/<share_id>` 当作发布地址，也不要直接向 `/s/<share_id>` PUT/POST 文件。
- 路径前缀与内容类型的对应关系：`/s/`、`/md/` 是文本/HTML/Markdown 页面；`/pdf/`、`/ppt/`、`/word/` 是二进制文件。元数据更新时 `update_share_settings.js` 会按此前缀自动选择 endpoint，裸 `share_id` 或 slug 由脚本先试页面 endpoint、必要时回退文件 endpoint，整个过程不下载源文件。
- 内容发布与更新统一使用 `publish.js`，脚本会按文件类型自动分发到文本通道或二进制直传通道（stderr 输出 `INFO:CHANNEL:text|binary`），不需要也不应该自行选择底层上传脚本。不要因为会话里存在旧的 `/s/<share_id>` 就把二进制文件改走文本页面 PUT；二进制文件传 `--share-id` 会被脚本拒绝（`ERROR:BINARY_NO_SHARE_ID`）。
- 如果当前会话中已经为同一个文本/HTML 文件生成过 ShareOne 链接，可复用之前的 `share_id` 执行文本页面 PUT 更新；否则执行首次创建。
- 非 owner 下载要求链接已开启允许下载；若脚本输出 `ERROR:DOWNLOAD_NOT_ALLOWED`，直接提示用户让链接 owner 先开启允许下载。

## 发布前安全确认（范围明确）

- **需要确认**：本会话内每次**创建新分享链接**（首次 POST 新页面或首次上传新文件）前，必须展示以下安全提示，并等待用户明确回复“同意”或 `agree` 后才能继续：
  > 发布前安全提示：在将页面发布到公网前，请您确认该页面内容符合相关法律法规要求。禁止发布反动、涉政、暴力、色情、侵权或恶意代码。上传的内容将免费托管保留 90 天。
  > 如果您的内容符合要求，请回复“同意”，我将为您发布。
- **不需要重复确认**：对本会话中已经过确认的同一链接执行后续操作时——包括内容 PUT 更新、评论处理闭环中的重新发布、水印/密码/短链/评论开关等元数据修改——不再重复展示安全提示。
- 下载、查看评论、删除 API Key 等不发布内容的操作不需要安全确认。

## 不可跳过的阻塞步骤

以下步骤是阻塞性用户通知，不是可选说明。触发后必须先发给用户，再继续后续操作。

- 如果 `ensure_credentials.js --create-guest` 或底层 `create_guest_key.js` 输出 `GUEST_KEY_CREATED:<api_key>`，必须立即向用户发送临时 API Key、绑定账号链接和保存提醒（话术见 `workflows/environment-and-credentials.md`）。即使 key 已经自动保存，也不能省略该通知；发送前不得继续执行原任务的上传、下载、评论处理命令。
- 本会话首次向用户展示生成的 `share_url` 时，必须按 `workflows/result-and-errors.md` 提示所有未使用的高级功能：自定义短链接名称、访问密码、水印。已使用的能力不再提示；三项都已使用则不提示。

## 全局约束

- 发布前必须完成凭据检查和必要的凭据配置。
- 发布成功后必须直接使用脚本返回的 `share_url`，不要自行拼接分享链接；不要展示备用链接。
- 只有当用户明确要求开启评论、允许讨论或协同模式时，才添加 `--allow-comments true`。默认不开启评论。
- 自定义短链接（slug）：服务端会根据文件名自动生成可读的 slug（如 `quarterly-report`），客户端无需额外操作。只有用户明确要求“链接叫 xxx”、“自定义短链接 xxx”、“URL 后缀 xxx”时，才在发布命令添加 `--slug xxx` 覆盖自动生成；slug 冲突时把服务端提示反馈给用户，不要静默改名。
- 评论处理必须形成闭环：认领、修改、重新发布、回复、关闭或 dismiss。

## 最终回复前检查清单

在回复用户前，逐项检查：

- 如果本轮创建了临时 API Key，是否已经把 API Key、绑定账号链接和保存提醒发给用户。
- 如果本轮**创建了新分享链接**，是否在执行创建命令前获得用户明确回复“同意”或 `agree`；如果只是更新已确认的链接，则无需此项。
- 如果发布成功，是否直接展示返回的 `share_url`，没有自行拼接链接。
- 如果返回中包含 `custom_slug_warning` 或 `custom_slug_suggestions`，是否展示给用户。
- 如果这是本会话首次展示生成的 `share_url`，是否提示所有未使用的高级功能。
