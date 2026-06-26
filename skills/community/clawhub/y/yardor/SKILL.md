---
name: github-stars-analyzer
description: 抓取指定 GitHub 用户 Stars 下的所有项目，并生成标准化中文 Markdown 报告。当用户提到"分析 GitHub stars"、"导出收藏项目"、"汇总 GitHub 星标"、"生成 stars 报告"，或粘贴包含 ?tab=stars 的 GitHub 链接时，必须触发此技能。始终通过 bash_tool 运行 Python 脚本完成任务，不要使用浏览器 Artifact 或 web_fetch 抓取 GitHub 数据。
---

# GitHub Stars 分析器技能

## 技能概述

通过 GitHub 公开 API 抓取用户所有 starred 仓库，按大类自动分组，生成标准化中文 Markdown 报告文件。

## 文件结构

```
github-stars-analyzer/
├── SKILL.md                  ← 本文件
├── scripts/
│   └── fetch_stars.py        ← 抓取 + 报告生成脚本
└── assets/
    └── template.md           ← 标准化报告模板（说明格式规范）
```

## 执行流程

### 第一步：解析用户名

从用户消息中提取 GitHub 用户名，支持以下格式：
- `https://github.com/USERNAME?tab=stars`
- `https://github.com/USERNAME`
- `@USERNAME`
- 裸用户名

### 第二步：运行脚本

将脚本复制到工作目录后执行：

```bash
cp /path/to/skill/scripts/fetch_stars.py /home/claude/fetch_stars.py
python3 /home/claude/fetch_stars.py USERNAME --output /home/claude/USERNAME_github_stars.md
```

可选参数：
- `--token <PAT>`：GitHub Personal Access Token，将 API 限额从 60次/小时 提升至 5000次/小时
- `--output <路径>`：指定输出文件路径，默认为 `<username>_github_stars.md`

### 第三步：交付文件

```bash
cp /home/claude/USERNAME_github_stars.md /mnt/user-data/outputs/USERNAME_github_stars.md
```

然后使用 `present_files` 工具将文件提供给用户。

## 报告大类分类规则

脚本按仓库 topics 和语言自动划分以下大类（优先级从上到下匹配）：

| 大类 | 匹配关键词（topics / 语言） |
|------|--------------------------|
| 🤖 人工智能与机器学习 | ai, ml, machine-learning, deep-learning, llm, nlp, neural-network, gpt, pytorch, tensorflow |
| 🛠️ 开发工具与效率 | cli, tool, productivity, devtools, vscode, vim, ide, automation, workflow |
| 🌐 前端与界面 | frontend, react, vue, angular, css, html, ui, design, javascript, typescript |
| ⚙️ 后端与框架 | backend, api, rest, graphql, microservice, server, django, flask, fastapi, go, rust |
| 📦 基础设施与运维 | devops, docker, kubernetes, ci-cd, cloud, aws, infra, terraform, nginx |
| 🗄️ 数据库与数据 | database, sql, nosql, redis, postgres, mongodb, data, analytics, etl |
| 🔒 安全与隐私 | security, hacking, pentest, crypto, privacy, auth, vulnerability |
| 📚 学习资源与文档 | awesome, tutorial, learning, course, book, guide, roadmap, cheatsheet |
| 🎮 游戏与创意 | game, graphics, animation, art, creative, shader |
| 🐍 Python 生态 | 语言为 Python 且未命中以上类别 |
| 其他 | 未匹配任何类别的仓库 |

## 报告模板规范

详见 `assets/template.md`，生成报告时严格遵循该模板的结构和中文命名规范。

## 错误处理

- **HTTP 404**：提示用户名不存在，终止
- **HTTP 403**：提示 API 超限，显示剩余等待秒数，建议添加 `--token`
- **网络不通**：提示检查网络连接（Claude 服务器无外网出口，脚本需在用户本地运行）

## 向用户说明

完成后告知用户：
1. 文件已生成，可直接下载
2. 如需在本地重新运行：`python3 fetch_stars.py <用户名>`
3. 如遇 API 限速，在 GitHub 设置页生成一个免费 Token（无需任何权限勾选）后加上 `--token` 参数
