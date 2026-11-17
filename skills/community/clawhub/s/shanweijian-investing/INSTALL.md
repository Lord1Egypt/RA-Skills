# 安装指南 / Installation Guide

## Codex Desktop (macOS / Windows)

**中文：**
1. 下载或 clone 本仓库
2. 把整个 `shanweijian-investing` 文件夹复制到：
   - Windows: `C:\Users\<你>\.codex\skills\shanweijian-investing\`
   - macOS/Linux: `~/.codex/skills/shanweijian-investing/`
3. 重启 Codex，直接问：「用单伟建的思维分析……」

**English:**
1. Clone this repo
2. Copy the whole `shanweijian-investing` folder to `~/.codex/skills/` (Windows: `C:\Users\<you>\.codex\skills\`)
3. Restart Codex and ask: "How would Shan Weijian analyze this deal?"

## Claude Desktop / Other Agent Runtimes

Place the folder in the runtimes skills directory and reference `SKILL.md` as the entry point. The structure follows the open [Agent Skills](https://github.com/openai/codex/blob/main/docs/skills.md) convention:

```
<skill-root>/
├── SKILL.md          # entry point with routing instructions
└── references/       # knowledge base (loaded on demand)
```

## Verify Installation

Ask your agent: 「单伟建的五环筛选体系是什么？」 Expected: it reads `references/framework/deal-screening-system.md` and answers with the five rings and weights.
