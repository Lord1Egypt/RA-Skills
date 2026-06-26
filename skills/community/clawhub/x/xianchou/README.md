# Xianchou CLI — Agent Skill

面向 AI Agent 和内容作者的 Markdown/MDX 自动配图工具。

本目录是 `xianchou` CLI 的 Agent Skill 定义。它指导 Agent 使用献丑 `/api/cli` 专用接口，为任意 Markdown/MDX 生成并插入图片。

ClawHub 地址：[https://clawhub.ai/starlying/xianchou](https://clawhub.ai/starlying/xianchou)

GitHub 地址：[https://github.com/xianchou-ai/skills](https://github.com/xianchou-ai/skills)

CLI 地址：[https://www.npmjs.com/package/@xianchou/cli](https://www.npmjs.com/package/@xianchou/cli)

## 目录结构

```text
xianchou/
├── SKILL.md
└── references/
    ├── cli-command-guide.md
    ├── api-generation-guide.md
    ├── markdown-image-guide.md
    ├── api-contract-guide.md
    └── common-pitfalls.md
```

## 核心能力

- AI 生图：通过 `/api/cli/images/generate` 提交任务并轮询。
- Markdown 插图：解析 Markdown/MDX 标题结构，自动插入图片。
- Markdown 封面：通过 `--cover` 更新通用 frontmatter 的 `cover` 与 `coverAlt`。
- 稳定接口：CLI 只调用 `/api/cli/*`，避免依赖 Web 内部接口。

## 快速开始

```bash
npm install -g @xianchou/cli
xianchou auth login --key <ACCESS_KEY> --project-id <PROJECT_ID>
xianchou markdown images ./article.md --count 3 --write
```

详细命令、工作流和易错点请参阅 [SKILL.md](./SKILL.md)。
