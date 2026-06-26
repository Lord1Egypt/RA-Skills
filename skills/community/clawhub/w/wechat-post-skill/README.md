# WeChat Post Skill / 微信公众号发布技能

[English](#english) | [中文](#中文)

---

## 中文

**WeChat Post Skill** 是一个面向 OpenClaw / AgentSkill 的微信公众号文章工作流技能。

它负责把“我要发一篇公众号”变成一套稳定流程：

```text
选题 → 写稿 → 去 AI 味 → 配图规划 → 自审 → 交给用户授权的发布工具生成草稿
```

这个技能本身不包含微信发布代码，也不保存任何账号密钥。真正发布到微信公众号草稿箱时，需要用户自己配置并授权对应的发布工具，例如 `baoyu-post-to-wechat`。

### 能做什么

- 根据热点或用户主题策划公众号选题
- 写 900–1300 字左右的中文公众号文章
- 规划封面图和正文配图
- 检查占位符、图片文件、标题、开头、结尾和排版节奏
- 在用户授权环境中，把文章交给已安装的微信公众号发布工具

### 安全边界

- 只用于用户自己拥有或被授权运营的公众号
- 不要求用户把密钥粘贴到聊天里
- 不保存、不打印、不提交 `WECHAT_APP_SECRET`、Token、Cookie 或浏览器配置
- 默认目标是微信公众号草稿箱
- 遇到凭证、权限、IP 白名单问题时，要求用户修复账号配置，不绕过限制
- 浏览器发布/浏览器图片生成不在本技能内执行；需要时使用单独的配套技能

### 需要什么

真实发布时通常需要：

- 用户自己的微信公众号账号权限
- `WECHAT_APP_ID`
- `WECHAT_APP_SECRET`
- 一个经过用户信任的发布工具，例如 `baoyu-post-to-wechat`

推荐配套技能：

| 技能/工具 | 用途 |
|---|---|
| `baoyu-post-to-wechat` | 把 Markdown / HTML 文章提交到微信公众号草稿箱 |
| [`gemini-browser-image`](https://github.com/jiao1yin2he3/gemini-browser-image-skill) | 需要 Gemini 网页生成配图时使用的独立配套技能 |
| `ai-humanizer` | 分析并降低文章 AI 味 |

### 安装

```bash
clawhub install wechat-post-skill
```

或者手动复制：

```text
~/.openclaw/skills/wechat-post-skill/
├── SKILL.md
└── references/
    ├── content-playbook.md
    └── publishing-notes.md
```

### 适用场景

- “帮我发一篇公众号”
- “写一篇公众号文章并放草稿箱”
- “根据今天热点做一篇推送”
- “把这篇内容整理成微信公众号文章”

### 致谢

- [`baoyu-post-to-wechat`](https://github.com/JimLiu/baoyu-skills#baoyu-post-to-wechat)
- OpenClaw AgentSkill 机制

---

## English

**WeChat Post Skill** is an OpenClaw / AgentSkill workflow for preparing WeChat Official Account articles.

It turns a request like “publish a WeChat post” into a structured workflow:

```text
topic selection → drafting → humanized editing → image planning → self-review → handoff to a user-authorized publisher
```

This skill does not include WeChat publishing code and does not store account secrets. Actual draft-box publishing requires a user-configured and user-authorized publishing tool, such as `baoyu-post-to-wechat`.

### What it does

- Plans WeChat article topics from trends or user-provided themes
- Drafts Chinese WeChat-style articles
- Plans cover and body image assets
- Checks placeholders, image files, title, opening, ending, and layout rhythm
- Hands the prepared article to a trusted WeChat publishing companion tool in the user's authorized environment

### Safety boundaries

- Use only for accounts owned or authorized by the user
- Do not ask the user to paste secrets into chat
- Do not store, print, commit, or publish `WECHAT_APP_SECRET`, tokens, cookies, or browser profile data
- Default target is the WeChat draft box
- If credentials, permissions, or IP allowlist settings fail, ask the user to fix account configuration instead of bypassing controls
- Browser-based publishing or image generation is handled only by separate companion skills when explicitly chosen by the user

### Requirements

For real publishing, users typically need:

- their own WeChat Official Account access
- `WECHAT_APP_ID`
- `WECHAT_APP_SECRET`
- a trusted publishing companion tool such as `baoyu-post-to-wechat`

Recommended companion tools:

| Skill/tool | Purpose |
|---|---|
| `baoyu-post-to-wechat` | Submit Markdown / HTML articles to the WeChat draft box |
| [`gemini-browser-image`](https://github.com/jiao1yin2he3/gemini-browser-image-skill) | Separate companion skill for Gemini web UI image generation |
| `ai-humanizer` | Analyze and reduce AI-like writing patterns |

### Install

```bash
clawhub install wechat-post-skill
```

Manual copy:

```text
~/.openclaw/skills/wechat-post-skill/
├── SKILL.md
└── references/
    ├── content-playbook.md
    └── publishing-notes.md
```

### Use cases

- “Help me publish a WeChat Official Account article.”
- “Write a WeChat article and put it in the draft box.”
- “Turn today's trend into a WeChat post.”
- “Rewrite this content as a WeChat article.”

### Acknowledgements

- [`baoyu-post-to-wechat`](https://github.com/JimLiu/baoyu-skills#baoyu-post-to-wechat)
- The OpenClaw AgentSkill system
