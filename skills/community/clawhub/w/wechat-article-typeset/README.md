# OpenClaw 中使用本技能

## 加载方式

本技能（`wechat-article-preset-preview`）放在**工作区**目录 `.openclaw/skills/wechat-article-typeset/` 下（目录名可保持不变），在 OpenClaw 中打开本仓库（`wework`）时，会按工作区技能优先加载。

- 若未自动加载：确认 OpenClaw 的「工作区」或「当前目录」为本项目根目录。
- 全局使用：可把整个 `wechat-article-typeset` 目录复制到 `~/.openclaw/skills/`，则任意工作区都会加载（技能名以 `SKILL.md` 的 `name` 为准）。

## 触发方式

`SKILL.md` 中已配置 `trigger`，当用户输入包含以下关键词时会激活本技能：

- 预设主题排版  
- 公众号主题排版  
- 主题排版 / preset排版  
- 主题预览  

也可在对话中直接说「用预设主题把这篇 md 排成公众号并生成复制链接」等。

## 可选配置（Gate / 专属 Agent）

若希望仅在某些场景或某个 Agent 下启用，可在 OpenClaw 配置中为该技能设置 gate 或 agents，例如：

```yaml
skills:
  wechat-article-preset-preview:
    enabled: true
    # gate:
    #   keywords: ["公众号", "排版"]
    # agents: ["your-agent-name"]
```

## 流程（输入 = 用户 Md，输出 = 预设主题预览链接）

1. **输入**：用户提供的 **Markdown 文件**（如 article.md）。
2. 在技能目录下执行（推荐用纯英文参数，避免终端对中文参数的兼容问题）：  
   - **推荐**：`node wechat-copy.js <input.md> --preset <预设名>`  
   - 可选：`node wechat-copy.js <input.md> --theme <themeId> --layout <layoutId>`
3. 脚本会输出一条预览链接（预设主题渲染版），并在 md 同目录写入：
   - `article.preset.html`（预设主题 HTML）
   - `wechat-preview-url.txt`（预览链接）
4. 将链接交给用户，浏览器打开后复制再粘贴到公众号。

常用等价示例：

- `墨色下划线` ≈ `--theme ink-seri --layout underline`

## 技能目录内的文件

- **wechat-copy.js**：输入一个 md，生成预设主题 HTML 并 POST 到 edit.shiker.tech，输出单条预览链接（并写入 `article.preset.html` 与 `wechat-preview-url.txt`）。
- **wechat-html.js**：仅生成预设主题 HTML（不请求预览链接）。

## 依赖

- Node.js（支持 ES Module）。
- 网络：需能请求 `https://edit.shiker.tech/api/copy` 以获取复制页链接。
- 本技能不依赖额外 npm 包，无需 `npm install`。
