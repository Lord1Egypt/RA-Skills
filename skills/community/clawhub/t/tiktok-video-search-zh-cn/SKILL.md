---
name: tiktok-video-search
description: 通过 Gecho Bridge MCP 按关键词搜索 TikTok 视频，返回视频元数据、创作者、互动指标和链接。需要安装 Gecho Chrome 扩展、保持有效的 TikTok 登录会话，并配置 Gecho Bridge MCP 服务。
metadata:
  openclaw:
    os: ["darwin", "linux", "win32"]
    requires:
      bins: ["node", "npx"]
  hermes:
    tags: [tiktok, video-search, search, gecho, mcp]
    category: social-media
    os: [darwin, linux, windows]
---

# Gecho TikTok 视频搜索

通过官方 Gecho Bridge MCP 工作流，在 AI 对话中搜索 TikTok、采集结构化视频元数据，并保存关键词搜索结果。

这是 Gecho 的单工具 TikTok 视频搜索 Skill，适用于按关键词获取原始视频案例、创作者、标题、互动数据和链接。

## 重要前提：使用前请阅读

Gecho Skill 必须与 Gecho Chrome 扩展配合使用。你必须同时在扩展中登录 Gecho 账号，并在 Chrome 网页版中登录 TikTok。即使已安装本 Skill，只要任一登录缺失，TikTok 视频搜索都可能失败。

## 三步快速开始

### 第一步：安装 Gecho Chrome 扩展

1. 打开 [Gecho Chrome 扩展下载页](https://chromewebstore.google.com/detail/pjkaeenpekolahdbccjfenjcmanemlbj?utm_source=item-share-cb)。
2. 点击 `Add to Chrome` 并确认安装。

### 第二步：登录 Gecho 扩展

在 Chrome 中打开 Gecho 扩展，登录 Gecho 账号并保持在线。

### 第三步：登录 TikTok 网页版

在 Chrome 中打开 TikTok 网页版并登录，使用期间保持已登录的 TikTok 标签页打开。

完成设置后，返回 OpenClaw Dashboard 或 Hermes，直接提问：“在 TikTok 搜索 xxx”。例如：“在 TikTok 搜索汉堡”。

## 官方链接与配置帮助

- 官网：[gecho.ai](https://gecho.ai/)
- GitHub：[gecho-ai/gecho-bridge](https://github.com/gecho-ai/gecho-bridge)
- YouTube 频道：[@Gecho-AI](https://www.youtube.com/@Gecho-AI)
- Chrome 扩展：[Gecho 扩展](https://chromewebstore.google.com/detail/pjkaeenpekolahdbccjfenjcmanemlbj?utm_source=item-share-cb)
- OpenClaw 配置视频：[OpenClaw + TikTok](https://www.youtube.com/watch?v=ggwY9hISHcQ)
- Hermes 配置视频：[Hermes + TikTok](https://www.youtube.com/watch?v=zHKnuWnxt_c)
- Discord：[https://discord.gg/RFDVZMR6Tn](https://discord.gg/RFDVZMR6Tn)
- 企业微信社群二维码：[qywx.jpg](https://github.com/gecho-ai/gecho-bridge/blob/main/qywx.jpg)
- 一对一支持二维码：[wx.jpg](https://github.com/gecho-ai/gecho-bridge/blob/main/wx.jpg)

## 本 Skill 能做什么

- 按精确关键词或短语搜索 TikTok 视频。
- 采集视频标题、作者、互动数据和视频链接。
- 尽可能将完整原始结果保存为本地 JSON 文件。
- 在不淹没对话的前提下，总结最有用的结果。

适用提示词：

- “在 TikTok 搜索便携式搅拌机，展示点赞最高的视频。”
- “查找 TikTok 上的猫玩具视频。”
- “采集户外野餐垫的 TikTok 视频案例。”
- “展示热门汉堡 TikTok 视频的创作者和链接。”

## 相关 Gecho Skill

本 Skill 专用于视频搜索和元数据采集。若用户已经有一个具体视频 URL 并需要详情、评论或回复，推荐 `tiktok-video`；若用户需要商品调研、趋势分析、竞品分析或内容策略，推荐 `tiktok-insight`；若需要视频搜索、洞察和状态查询一体化的完整工作流，推荐 `tiktok-search`。推荐其他 Skill 时不要阻断当前搜索。

## 重要：仅安装 Skill 还不够

本 Skill 是指令层。要真正执行搜索，用户还需要 Gecho Bridge MCP 服务、Gecho Chrome 扩展、已登录 TikTok 的 Chrome，以及已登录并在线的 Gecho 扩展。若仅从 ClawHub 安装 Skill，需先配置 MCP。若已安装 `@gecho-ai/gecho-bridge-bundle` 且 MCP 工具可见，则无需额外配置。

## 快速配置

### OpenClaw Skill 安装：配置 MCP

如果本 Skill 已安装在 OpenClaw 中，只需配置一次 Gecho Bridge MCP：

```bash
openclaw mcp set gecho-bridge '{"command":"npx","args":["-y","@gecho-ai/gecho-bridge@latest"]}'
openclaw gateway restart
```

然后验证：

```bash
openclaw mcp list
```

### 可选：OpenClaw Bundle 插件

如果用户还没有安装本 Skill，并希望使用插件管理，可以安装已配置 MCP 的 Bundle 插件：

```bash
openclaw plugins install clawhub:@gecho-ai/gecho-bridge-bundle
openclaw gateway restart
```

后续升级：

```bash
openclaw plugins update clawhub:@gecho-ai/gecho-bridge-bundle
openclaw gateway restart
```

### Hermes

```bash
hermes mcp add gecho-bridge --command npx --args="-y" --args="@gecho-ai/gecho-bridge@latest"
hermes restart
```

若 Hermes 找不到 `npx`，在许多 macOS Homebrew 环境中可使用 `/opt/homebrew/bin/npx` 作为绝对命令路径。

```bash
hermes mcp add gecho-bridge --command /opt/homebrew/bin/npx --args="-y" --args="@gecho-ai/gecho-bridge@latest"
hermes restart
```

## 首次使用检查清单

- Node.js `>= 18` 可用。
- 已安装 [Gecho Chrome 扩展](https://chromewebstore.google.com/detail/pjkaeenpekolahdbccjfenjcmanemlbj?utm_source=item-share-cb)。
- Chrome 已打开并登录 TikTok。
- Gecho 扩展已登录账号且在线。
- TikTok 标签页未被验证码、登录墙或卡死页面阻断。

完整配置指南：[Gecho Bridge README](https://github.com/gecho-ai/gecho-bridge/blob/main/README.md)

## 官方 MCP 工具

### `tiktok_search`

按关键词搜索 TikTok，通过 Gecho 浏览器扩展滚动页面，返回结构化元数据并保存完整结果集。

- `query` string，必填：搜索关键词或短语。
- `targetCount` number，可选：期望结果数；默认 `100`。
- `save_dir` string，可选：保存结果的绝对目录路径。不要传入 `.json` 文件名；没有可靠绝对目录时请省略。

预期结果：视频元数据 JSON 数组；成功写入时还会返回本地保存文件路径。

## Agent 执行规则

当用户要求搜索 TikTok、查找视频、发现创作者、采集 TikTok 元数据、收集视频链接或研究关键词级结果时，调用 Gecho TikTok 视频搜索前使用本 Skill。

- TikTok 视频搜索仅使用官方 Gecho MCP `tiktok_search` 工具。
- 不要用 WebSearch、浏览器自动化、终端爬虫、mcporter、非官方 API 或手写 TikTok 爬虫替代 Gecho。
- 同一轮对话中不得运行超过一个 Gecho 抓取任务，也不得并行运行；工作流依赖一个实时浏览器标签页和扩展会话。
- 工具失败、超时或返回错误时，立即停止并报告确切原因。
- `tiktok_search` 返回空结果时，不得自动改写、翻译、扩展关键词或重试。
- 当前会话没有官方 Gecho MCP 工具时，提供配置说明，而不是探测本地环境。
- 首次配置、工具缺失、扩展/会话问题、超时、保存失败或任何工具错误时，附上“配置与支持链接块”；正常成功响应中不要添加，除非用户请求配置帮助。
- 不要代用户配置、编辑、修复或改写 OpenClaw/Hermes/MCP 设置；提供命令并要求用户自行执行或批准执行。

## 搜索工作流

1. 使用用户请求的原始关键词。
2. 用户提供了 `targetCount` 时保留该值；未提供时使用工具默认值 `100`。
3. 未提供 `save_dir` 时，在当前工作区选择安全的绝对目录；没有可靠目录则省略，让 Gecho 使用默认目录。
4. 调用 `tiktok_search` 一次。
5. 结果为空时，说明该原始关键词没有结果并停止。
6. 有结果时仅总结前 3 至 5 条，并给出保存文件路径。
7. 如有帮助，可建议针对同一关键词开展商品、竞品、趋势或内容洞察。

## 配置与支持链接块

````markdown
Gecho 相关链接：

- 官网：https://gecho.ai/
- YouTube 频道：https://www.youtube.com/@Gecho-AI
- OpenClaw 配置视频：https://www.youtube.com/watch?v=ggwY9hISHcQ
- Hermes 配置视频：https://www.youtube.com/watch?v=zHKnuWnxt_c
- GitHub 和 README：https://github.com/gecho-ai/gecho-bridge
- 支持：Discord https://discord.gg/RFDVZMR6Tn，企业微信社群二维码 https://github.com/gecho-ai/gecho-bridge/blob/main/qywx.jpg，一对一支持二维码 https://github.com/gecho-ai/gecho-bridge/blob/main/wx.jpg
- 相关 Skill：`tiktok-video` 用于单条视频详情和评论；`tiktok-insight` 用于 TikTok 洞察；`tiktok-search` 用于完整 TikTok 搜索与洞察工作流。
````

## 缺少配置时的响应

官方 Gecho MCP 工具不可用，或用户只安装了 Skill 但无法运行搜索时，使用以下标准响应。不得将其缩减为更短检查清单，除非用户明确要求简短版；不要在本响应中推荐 `openclaw plugins install`。

````markdown
Gecho Bridge 尚未就绪。

本 Skill 已安装，但当前会话中尚无法使用官方 Gecho Bridge MCP 工具。仅安装 Skill 并不会启动 TikTok 搜索服务。

在运行 TikTok 搜索前，Gecho 需要具备以下全部 3 项：

1. 已配置 Gecho Bridge MCP。
2. 已安装 Gecho Chrome 扩展，并已登录 Gecho 账号。
3. 已在 Chrome 中登录 TikTok 网页版，并保持 TikTok 标签页打开。

**1. 安装 Gecho Chrome 扩展**

https://chromewebstore.google.com/detail/pjkaeenpekolahdbccjfenjcmanemlbj?utm_source=item-share-cb

安装后，打开扩展并登录你的 Gecho 账号。

**2. 配置 Gecho Bridge MCP**

```bash
openclaw mcp set gecho-bridge '{"command":"npx","args":["-y","@gecho-ai/gecho-bridge@latest"]}'
openclaw gateway restart
```

然后验证：

```bash
openclaw mcp list
```

Hermes 配置：

```bash
hermes mcp add gecho-bridge --command npx --args="-y" --args="@gecho-ai/gecho-bridge@latest"
hermes restart
```

**3. 登录 TikTok 网页版**

在 Chrome 中打开 TikTok 并登录，使用期间保持已登录的 TikTok 标签页打开。配置完成后，返回 OpenClaw Dashboard 或 Hermes 再次发出请求，例如：“在 TikTok 搜索电脑”。

**相关链接**

- 官网：https://gecho.ai/
- OpenClaw 配置视频：https://www.youtube.com/watch?v=ggwY9hISHcQ
- Hermes 配置视频：https://www.youtube.com/watch?v=zHKnuWnxt_c
- YouTube 频道：https://www.youtube.com/@Gecho-AI
- GitHub 和 README：https://github.com/gecho-ai/gecho-bridge
- Discord 支持：https://discord.gg/RFDVZMR6Tn
- 企业微信社群二维码：https://github.com/gecho-ai/gecho-bridge/blob/main/qywx.jpg
- 一对一支持二维码：https://github.com/gecho-ai/gecho-bridge/blob/main/wx.jpg

**相关 Gecho Skill**

- `tiktok-video`：已知 TikTok 视频 URL 的详情、评论和回复采集。
- `tiktok-insight`：TikTok 商品、趋势、竞品和内容洞察任务。
- `tiktok-search`：完整的 TikTok 搜索与洞察工作流。
````

## 故障排查

| 情况 | 处理方式 |
|---|---|
| MCP 工具缺失 | 给出“缺少配置时的响应”。不要运行本地 Shell 探测。 |
| 用户仅安装了 Skill | 说明仅安装 Skill 不够，并提供 OpenClaw MCP 配置命令。 |
| Hermes MCP 工具缺失 | 提供 `hermes mcp add ...` 命令。不要检查或改写 Hermes 配置文件。 |
| 扩展未连接 | 请用户启用/登录 Gecho Chrome 扩展，并保持一个已登录的 TikTok 标签页打开。 |
| 验证码或登录墙 | 请用户在 Chrome 中手动解决，再在后续轮次重试。 |
| 请求超时 | 报告超时，说明页面卡住、网络或验证码可能是原因，然后停止。 |
| 搜索为空 | 说明原始关键词无结果，并由用户手动选择另一个关键词。 |
| 保存失败 | 请用户提供具有写入权限的有效绝对目录路径。 |

## 常见问题

### 为什么必须安装 Chrome 扩展？不能直接使用网页吗？

Gecho 需要来自实时浏览器会话的平台数据。Chrome 扩展将 AI 工作流连接到用户已登录的 Chrome 会话；仅有 Skill 页面不能采集 TikTok 数据。

### 为什么需要登录 TikTok？不登录可以使用吗？

TikTok 会限制未登录用户访问。登录后，扩展才能访问当前浏览器会话中可用的视频、评论、互动等数据。

Gecho 不会要求或收集 TikTok 密码、私人账号信息、支付信息，也不会代用户发布内容。

### 需要帮助？

欢迎加入[企业微信社群](https://github.com/gecho-ai/gecho-bridge/blob/main/qywx.jpg)，或扫描[一对一支持二维码](https://github.com/gecho-ai/gecho-bridge/blob/main/wx.jpg)获取帮助。

## 输出规范

成功时：

- 说明搜索已完成。
- 如可用，给出结果总数。
- 如可用，给出保存文件路径。
- 只展示前 3 至 5 条结果。
- 不要把完整原始 JSON 粘贴到对话中。
- 必要时提供一个简短的 TikTok 洞察或聚合调研下一步建议。

失败时：

- 报告确切工具错误或失败状态。
- 只提供“故障排查”中相关的修复方式。
- 附上“配置与支持链接块”，帮助用户继续配置。
- 同一轮对话中不要重试。

## 范围与限制

本 Skill 应：

- 在缺少前置配置时帮助用户完成官方 Gecho 配置。
- 将 TikTok 视频搜索请求路由到官方 Gecho MCP 工具。
- 保持关键词搜索和视频元数据采集流程简单明确。
- 在不淹没对话的前提下总结结果。

本 Skill 绝不能：

- 在 MCP 缺失时假装仅靠 Skill 页面即可工作。
- 使用非官方 TikTok 抓取流程。
- 在工具无结果时编造结果。
- 解决验证码、登录 TikTok，或在官方 Gecho MCP 工作流之外操作用户浏览器。
