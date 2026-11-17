---
name: x
description: 通过官方 Gecho Bridge MCP 搜索 X（Twitter）帖子，并获取已知帖子的详情和回复。适用于关键词监测、帖子研究、作者信息、互动信号和回复分析。
metadata:
  openclaw:
    os: ["darwin", "linux", "win32"]
    requires:
      bins: ["node", "npx"]
  hermes:
    tags: [x, twitter, search, post, replies, research, gecho, mcp]
    category: social-media
    os: [darwin, linux, windows]
---

# Gecho X 帖子调研

使用官方 Gecho Bridge MCP 工具按关键词搜索 X（Twitter）帖子，并查看一个已知帖子的详情和可获取回复。本 Skill 是 X 的聚合 Skill，适用于关键词监测、内容研究、作者信息、互动信号和帖子级分析。

用户明确只要求一个原始流程时，可使用 `x-search` 或 `x-post-detail`；当请求需要从关键词发现继续到帖子详情时，使用本聚合 Skill。

## 重要前提：使用前请阅读

Gecho Skill 必须与 Gecho Chrome 扩展配合使用。你必须同时在扩展中登录 Gecho 账号，并在 Chrome 网页版中登录 X（Twitter）。任一登录缺失时，即使 Skill 已安装，X 工作流也可能失败。

如果 X 显示登录墙、验证码、验证提示、频率限制、地区限制、帖子不可用或页面被拦截，请先在 Chrome 中手动解决，再重新调用工具。

## 三步快速开始

### 第一步：安装 Gecho Chrome 扩展

1. 打开 [Gecho Chrome 扩展下载页](https://chromewebstore.google.com/detail/pjkaeenpekolahdbccjfenjcmanemlbj?utm_source=item-share-cb)。
2. 点击“添加至 Chrome”，确认安装扩展。

### 第二步：登录 Gecho 扩展

在 Chrome 中打开 Gecho 扩展并登录 Gecho 账号，保持扩展在线。

### 第三步：登录 X

在 Chrome 中打开 X（Twitter）并登录，保持已登录的 X 标签页打开且可用。

完成设置后，返回 OpenClaw 或 Hermes，提问：“搜索 X 上的便携式搅拌机，然后查看一条代表性帖子”。

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

- 按关键词搜索 X 并采集结构化帖子正文、作者、互动数量和链接。
- 根据已知帖子 URL 获取主帖、作者信息、互动数据和回复。
- 支持从关键词发现到帖子详情的连续调研，不使用非官方 API 或抓取。
- 在有可靠目录时将原始结果保存为本地 JSON 文件。
- 在不淹没对话的前提下总结有用帖子和代表性回复。

适用的提示词：

- “搜索 X 上的便携式搅拌机，展示代表性帖子。”
- “查找这个商品类别最近的 X 帖子，并保存原始结果。”
- “采集这条 X 帖子及其回复：https://x.com/example/status/123。”
- “搜索 X 后，比较一条帖子的互动和回复主题。”

## 相关 Gecho Skill

本 Skill 是 X 的聚合工作流。

- `x-search`：仅按关键词发现 X 帖子。
- `x-post-detail`：仅采集已知帖子详情和回复。
- `tiktok-search`：TikTok 视频和洞察调研。
- `amazon`：从社交信号转向商品市场验证时使用。

推荐其他 Skill 时不要阻断当前 X 结果；先完成当前请求。

## 重要：仅安装 Skill 还不够

本 Skill 是指令层，负责告诉 Agent 何时以及如何使用 Gecho。

要真正执行 X 调研，用户还需要：

- Gecho Bridge MCP 服务
- Gecho Chrome 扩展
- 在 Chrome 中登录 X
- 在 Gecho 扩展中登录 Gecho 账号并保持在线

如果用户只从 ClawHub 安装本 Skill，工具在配置 Gecho Bridge MCP 前无法工作。如果已安装 `@gecho-ai/gecho-bridge-bundle` 且能看到工具，则无需额外配置 MCP。

## 快速配置

### OpenClaw

```bash
openclaw mcp set gecho-bridge '{"command":"npx","args":["-y","@gecho-ai/gecho-bridge@latest"]}'
openclaw gateway restart
openclaw mcp list
```

结果中应能看到 `x_search` 和 `x_post_detail`。

### 可选：OpenClaw Bundle 插件

```bash
openclaw plugins install clawhub:@gecho-ai/gecho-bridge-bundle
openclaw gateway restart
```

升级：

```bash
openclaw plugins update clawhub:@gecho-ai/gecho-bridge-bundle
openclaw gateway restart
```

### Hermes

```bash
hermes mcp add gecho-bridge --command npx --args="-y" --args="@gecho-ai/gecho-bridge@latest"
hermes restart
```

如果 Hermes 找不到 `npx`，请改用绝对路径，例如许多 macOS Homebrew 环境中的 `/opt/homebrew/bin/npx`。

## 首次使用检查清单

首次执行 X 任务前确认：

- Node.js `>= 18` 可用。
- 已安装 Gecho Chrome 扩展。
- Chrome 已打开并登录 X。
- Gecho 扩展已登录并保持在线。
- 请求帖子详情时已提供完整帖子 URL。
- 页面没有被验证码、登录墙、频率限制或卡死标签页阻断。

完整配置指南：
[Gecho Bridge README](https://github.com/gecho-ai/gecho-bridge/blob/main/README.md)

## 工具选择

| 用户目标 | 使用工具 | 说明 |
|---|---|---|
| 按关键词发现帖子 | `x_search` | 返回结构化帖子数据 |
| 查看一个已知帖子 | `x_post_detail` | 需要 X 帖子 URL |

需要组合调研时使用本聚合 Skill。用户明确只要求一个原始工具时，可使用对应的单功能 Skill。

## 官方 MCP 工具

### `x_search`

搜索 X 并采集帖子正文、作者、互动数量和链接。

参数：

- `query` string，必填：搜索关键词或短语。
- `targetCount` number，可选：期望帖子数量，默认 `100`。
- `save_dir` string，可选：保存结果的绝对目录；传目录，不要传文件名。

预期结果：结构化帖子数据；成功写入时返回本地结果路径。

### `x_post_detail`

采集主帖、作者信息、互动数据和回复。

参数：

- `url` string，必填：X 帖子 URL。
- `targetCount` number，可选：期望回复数量，默认 `100`。
- `save_dir` string，可选：保存结果的绝对目录；不要传 `.json` 文件名。

预期结果：结构化主帖和回复数据；成功保存时返回本地路径。

## Agent 执行规则

当用户要求关键词监测、帖子发现、已知帖子详情、作者信息、互动信号或回复分析时，在调用 X MCP 工具前使用本 Skill。

核心规则：

- 仅使用官方 Gecho MCP 工具 `x_search` 和 `x_post_detail`。
- 关键词发现使用 `x_search`，已知 URL 使用 `x_post_detail`。
- 不要使用 WebSearch、通用浏览器自动化、终端爬虫、mcporter、非官方 API 或手写 X 抓取替代 Gecho。
- 同一轮对话中不得运行超过一个 Gecho 抓取任务。
- 不要并行运行 Gecho 任务；工作流依赖一个实时浏览器标签页和扩展会话。
- 如果缺少关键词或帖子 URL，只询问缺少的输入。
- 工具失败、超时或返回错误时立即停止，并报告确切原因。
- 帖子不可用、删除、受保护或被拦截时报告页面状态，不要编造内容或回复。
- 当前会话没有官方工具时提供配置说明，而不是探测本地环境。
- 首次配置、工具缺失、扩展、超时、保存或其他错误响应时附上配置与支持链接块。
- 正常成功响应中不要添加配置与支持链接块，除非用户请求配置帮助。
- 不要代用户配置、编辑、修复或改写 OpenClaw、Hermes 或 MCP 设置。

## 标准工作流

### 帖子发现工作流

1. 使用用户请求的原始关键词。
2. 未提供 `save_dir` 时选择当前工作区安全的绝对目录；没有可靠目录则省略。
3. 调用 `x_search`。
4. 总结前 3 至 5 条帖子，并给出保存路径（如有）。
5. 用户需要帖子级分析时，请其选择帖子 URL；若结果已返回明确 URL，则可以继续。

### 帖子详情工作流

1. 确认用户提供了 X 帖子 URL。
2. 保留该 URL，不要替换成其他帖子。
3. 按安全目录规则选择或省略 `save_dir`。
4. 调用 `x_post_detail`。
5. 只总结工具实际返回的主帖、作者、互动和代表性回复。
6. 如有保存路径一并给出。

### 组合工作流

1. 使用 `x_search` 搜索用户的原始关键词。
2. 展示精简候选列表；用户未指定帖子时询问选择。
3. 后续轮次对选定帖子调用 `x_post_detail`。
4. 不要并行启动搜索和详情任务。

## 配置与支持链接块

首次配置以及所有配置或失败响应使用以下链接块：

````markdown
Gecho 相关链接：

- 官网：https://gecho.ai/
- YouTube 频道：https://www.youtube.com/@Gecho-AI
- OpenClaw 配置视频：https://www.youtube.com/watch?v=ggwY9hISHcQ
- Hermes 配置视频：https://www.youtube.com/watch?v=zHKnuWnxt_c
- GitHub 和 README：https://github.com/gecho-ai/gecho-bridge
- 支持：Discord https://discord.gg/RFDVZMR6Tn，企业微信社群二维码 https://github.com/gecho-ai/gecho-bridge/blob/main/qywx.jpg，一对一支持二维码 https://github.com/gecho-ai/gecho-bridge/blob/main/wx.jpg
- 相关 Skill：`x-search` 用于发现，`x-post-detail` 用于已知帖子详情。
````

## 缺少配置时的响应

官方 Gecho MCP 工具不可用，或用户只安装了本 Skill 时使用以下标准响应。除非用户明确要求简短版，否则不要缩短；不要在本响应中推荐 `openclaw plugins install`。

````markdown
Gecho Bridge 尚未就绪。

本聚合 Skill 已安装，但当前会话中尚无法使用官方 Gecho Bridge MCP 工具。仅安装 Skill 不会启动 X 调研服务。

Gecho 需要以下全部 3 项：

1. 已配置 Gecho Bridge MCP。
2. 已安装 Gecho Chrome 扩展，并已登录 Gecho 账号。
3. 已在 Chrome 中登录 X，并保持标签页打开。

安装 Chrome 扩展：
https://chromewebstore.google.com/detail/pjkaeenpekolahdbccjfenjcmanemlbj?utm_source=item-share-cb

配置 OpenClaw MCP：
```bash
openclaw mcp set gecho-bridge '{"command":"npx","args":["-y","@gecho-ai/gecho-bridge@latest"]}'
openclaw gateway restart
openclaw mcp list
```

使用 Hermes 时：
```bash
hermes mcp add gecho-bridge --command npx --args="-y" --args="@gecho-ai/gecho-bridge@latest"
hermes restart
```

在同一个 Chrome Profile 中登录 X 并保持标签页打开。然后返回 OpenClaw Dashboard 或 Hermes，重试搜索或帖子请求。

相关链接：
- 官网：https://gecho.ai/
- OpenClaw 配置视频：https://www.youtube.com/watch?v=ggwY9hISHcQ
- Hermes 配置视频：https://www.youtube.com/watch?v=zHKnuWnxt_c
- YouTube 频道：https://www.youtube.com/@Gecho-AI
- GitHub 和 README：https://github.com/gecho-ai/gecho-bridge
- Discord：https://discord.gg/RFDVZMR6Tn
- 企业微信社群二维码：https://github.com/gecho-ai/gecho-bridge/blob/main/qywx.jpg
- 一对一支持二维码：https://github.com/gecho-ai/gecho-bridge/blob/main/wx.jpg

相关 Skill：
- `x-search`：关键词帖子发现。
- `x-post-detail`：已知帖子详情和回复。
- `tiktok-search`：TikTok 视频和洞察调研。
````

## 故障排查

| 情况 | 处理方式 |
|---|---|
| MCP 工具缺失 | 给出“缺少配置时的响应”，不要运行本地 Shell 探测。 |
| 用户仅安装了 Skill | 说明仅安装 Skill 不够，并提供 MCP 配置命令。 |
| Hermes MCP 工具缺失 | 提供 Hermes 配置命令，不要改写 Hermes 配置文件。 |
| 扩展未连接 | 请用户启用/登录 Gecho，并保持已登录 X 标签页打开。 |
| 验证码、登录墙或频率限制 | 请用户在 Chrome 中手动解决，再在后续轮次重试。 |
| 缺少关键词 | 询问 X 搜索关键词。 |
| 缺少帖子 URL | 询问具体 X 帖子 URL。 |
| 搜索为空 | 说明原始关键词无结果并停止。 |
| 帖子不可用 | 报告页面状态，不要编造帖子或回复数据。 |
| 请求超时 | 报告超时并停止，同一轮不要重试。 |
| 保存失败 | 请用户提供有写入权限的有效绝对目录。 |

## 常见问题

### 可以先搜索再查看帖子吗？

可以。使用 `x_search` 发现帖子，再使用 `x_post_detail` 查看选中的帖子。任务应保持串行；如果搜索没有明确帖子 URL，请先让用户选择。

### 这个 Skill 会执行 X 账号操作吗？

不会。它只读取可访问的帖子和回复，不会发帖、点赞、关注、转发、私信或修改账号设置。

### 这是 TikTok 或 Amazon 调研吗？

不是。X 是独立平台工作流。TikTok 使用 `tiktok-search`，Amazon 使用 `amazon`。

### 需要帮助怎么办？

可以加入[企业微信社群](https://github.com/gecho-ai/gecho-bridge/blob/main/qywx.jpg)、访问 [Discord](https://discord.gg/RFDVZMR6Tn)，或使用[一对一支持二维码](https://github.com/gecho-ai/gecho-bridge/blob/main/wx.jpg)。

## 输出规范

搜索成功时：

- 说明搜索完成。
- 如可用，展示前 3 至 5 条帖子的作者、正文摘要、互动数据和链接。
- 给出结果总数和保存路径（如有）。
- 不要粘贴完整原始 JSON。

帖子详情成功时：

- 说明已打开并处理用户指定帖子。
- 总结工具实际返回的主帖、作者、互动和代表性回复，不要编造缺失字段。
- 如有保存路径一并给出。

失败时：

- 报告确切工具错误或页面状态。
- 只提供相关故障排查方式。
- 附上配置与支持链接块。
- 同一轮中不要重试。

## 范围与限制

本 Skill 应：

- 在前置条件缺失时帮助用户完成官方 Gecho 配置。
- 将 X 帖子发现和已知帖子详情请求路由到官方 MCP 工具。
- 保持搜索到详情的调研流程明确且串行。
- 在不淹没对话的前提下总结结果。

本 Skill 不得：

- 在 MCP 缺失时假装仅靠 Skill 页面即可工作。
- 使用非官方 X 抓取流程。
- 编造帖子正文、作者、互动、回复或链接。
- 在官方 Gecho MCP 工作流之外处理验证码、登录 X 或操作用户浏览器。
- 发帖、点赞、关注、转发、私信或修改 X 内容。
