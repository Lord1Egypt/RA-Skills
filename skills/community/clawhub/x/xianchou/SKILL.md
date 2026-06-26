---
name: xianchou
description: >-
  Xianchou CLI (xianchou) — 面向 AI Agent 的 Markdown/MDX 自动配图与 AI 视频生成工具。
  支持调用献丑 /api/cli 专用接口进行 AI 生图、AI 生视频、模型查询、任务轮询，
  以及为任意 Markdown/MDX 插入图片。Use when editing Markdown documents,
  generating cover images, inserting article images, generating AI videos, or
  interacting with Xianchou image/video generation via command line.
version: 0.1.0
license: MIT-0
author: Xianchou Team
homepage: https://xianchou.com
user-invocable: true
metadata: {"openclaw":{"requires":{"bins":["xianchou"],"env":["XIANCHOU_ACCESS_KEY","XIANCHOU_PROJECT_ID","XIANCHOU_API_URL","XIANCHOU_CONFIG_DIR"]},"primaryEnv":"XIANCHOU_ACCESS_KEY","credentials":{"storage":"~/.xianchou/config.json","configDirEnv":"XIANCHOU_CONFIG_DIR","description":"xianchou auth login 写入的访问凭据，JSON 格式，存储 accessKey、projectId 和 apiUrl。"},"install":[{"id":"npm","kind":"node","package":"@xianchou/cli","bins":["xianchou"],"label":"Install Xianchou CLI (npm)"}],"category":"AIGC","tags":["xianchou","markdown","image-generation","video-generation","cli","ai-tools"]}}
---

# Xianchou CLI (xianchou)

面向 AI Agent 和内容作者的 Markdown/MDX 自动配图与 AI 视频生成命令行工具。所有远程能力统一走献丑 `/api/cli` 专用接口，不直接调用 Web 端内部接口。

## 安装 & 配置

```bash
npm install -g @xianchou/cli

# 配置访问凭据
# 在 Web 头像菜单 Access Key 中创建并复制
xianchou auth login --key <ACCESS_KEY> --project-id <PROJECT_ID>

# 或使用环境变量
export XIANCHOU_ACCESS_KEY=<ACCESS_KEY>
export XIANCHOU_PROJECT_ID=<PROJECT_ID>
export XIANCHOU_API_URL=https://api.xianchou.com
```

## 命令速查

```bash
# 认证
xianchou auth login --key <key> [--project-id <id>] [--api-url <url>]

# 模型
xianchou models image --project-id <id>
xianchou models video --project-id <id>

# 上传本地文件获取 URL
xianchou upload <file>

# 单张生图（文生图）
xianchou generate image --prompt "描述" --project-id <id> --poll

# 图生图（传入参考图，支持本地文件路径或 URL）
xianchou generate image --prompt "描述" --image-urls "./ref.png" --project-id <id> --poll

# AI 生视频（常见模式：文生视频 / 首帧生视频 / 首尾帧 / 参考生视频）
xianchou generate video --prompt "镜头描述" --project-id <id> --poll
xianchou generate video --mode first --prompt "让参考图动起来" --project-id <id> --first-frame-url "url_or_local_path" --poll
xianchou generate video --mode first-last --prompt "从首帧过渡到尾帧" --project-id <id> --first-frame-url "url" --last-frame-url "url" --poll
xianchou generate video --mode reference --prompt "保留主体与风格生成镜头" --project-id <id> --reference-url "url" --poll

# 任意 Markdown/MDX 插图（默认 dry-run 生成图片和 JSON 结果，不改原文）
xianchou markdown images ./article.md --count 3

# 写回 Markdown/MDX
xianchou markdown images ./article.md --count 3 --write

# 通用 Markdown 封面和正文图
xianchou markdown images ./article.md --cover --count 3 --write
```

## 关键工作流：Markdown 配图

1. 读取目标 Markdown/MDX，提取 frontmatter、标题和二级标题。
2. 调用 `/api/cli/markdown/images/plan` 生成封面与章节图片提示词。
3. 调用 `/api/cli/images/generate` 提交生图任务。
4. 调用 `/api/cli/tasks/{task_id}` 轮询任务。
5. 成功后调用 `/api/cli/tasks/{task_id}/settle`。
6. 下载图片到 `--assets-dir`，将 Markdown 图片语法插入到正文。
7. 只有传入 `--write` 才写回原文件。

## 关键工作流：AI 生视频

1. 先运行 `xianchou models video --project-id <id>` 获取可用视频模型、驱动模式、时长、比例、分辨率和音频能力。
2. 根据素材选择模式：无素材用文生视频；单张图用首帧/图生视频；首尾帧明确时用首尾帧；需要保留主体或风格时用参考生视频。
3. 提交视频生成任务时传入 `--project-id`、动态获取的模型参数、prompt 和所需参考图（支持本地文件路径，CLI 会自动上传）。
4. 使用 `--poll` 或 `xianchou generate task <task_id> --poll` 轮询任务。
5. 任务成功后 settle，记录或下载返回的视频 URL。

## 关键工作流：上传本地文件

当需要将本地图片/视频/音频用于生成任务时：

1. **自动上传**：`generate video` 和 `generate image` 的 URL 参数（如 `--first-frame-url`、`--image-urls`）支持直接传入本地文件路径，CLI 会自动检测并上传。
2. **手动上传**：使用 `xianchou upload <file>` 独立上传文件，获取返回的 URL 后再用于后续命令。

```bash
# 自动上传（推荐）
xianchou generate video --mode first --prompt "描述" --first-frame-url ./01.png --poll

# 手动上传
xianchou upload ./01.png
# 输出: {"success": true, "url": "https://..."}
```

## 重要规则

1. **CLI 只调用 `/api/cli/*`**，不要直接调用 `/run`、`/canvas` 等内部接口。
2. **模型 ID 必须动态获取**：生图先运行 `xianchou models image`，生视频先运行 `xianchou models video`，不要猜测或硬编码。
3. **视频模式按素材选择**：文生视频不传参考图；首帧/图生视频传首帧；首尾帧必须同时传首帧和尾帧；参考生视频传角色、主体、风格或视频参考素材。
4. **视频和图生图的 URL 参数支持本地文件路径**：CLI 会自动检测本地路径并上传到平台获取可访问 URL。也可以使用 `xianchou upload <file>` 手动上传。
5. **默认 dry-run**：`xianchou markdown images` 不带 `--write` 时不改 Markdown。
6. **路径要区分**：`--assets-dir` 是本地保存目录；`--public-url-prefix` 是写入 Markdown 的 URL 前缀。
7. **只有 `--cover` 才更新封面字段**：默认只插入正文图片；`--cover` 才会写入 frontmatter 的 `cover` 与 `coverAlt`。
8. **避免重复插图**：回写时依赖 `<!-- xianchou:image ... -->` 标记更新已生成图片。
9. **任务成功后必须 settle**：生成成功后调用 settle，保持积分和额度状态正确。
10. **如果本地旧版 CLI 未列出 video 子命令**，先升级 CLI，不要改用内部接口绕过。
11. **不确定参数时先查 references 或 `--help`**，不要臆造 CLI flag 或 API 字段。

## 深度指南 (references/)

| 文档 | 何时阅读 |
|------|----------|
| [`references/cli-command-guide.md`](references/cli-command-guide.md) | 不确定安装、认证、命令参数或输出格式 |
| [`references/api-generation-guide.md`](references/api-generation-guide.md) | 不确定模型查询、生图、轮询、settle 流程 |
| [`references/markdown-image-guide.md`](references/markdown-image-guide.md) | 不确定 Markdown/MDX 插图、路径、封面和回写规则 |
| [`references/api-contract-guide.md`](references/api-contract-guide.md) | 不确定 `/api/cli` 接口契约或错误格式 |
| [`references/common-pitfalls.md`](references/common-pitfalls.md) | 遇到 Access Key、projectId、路径、重复插图或内部接口误用问题 |
