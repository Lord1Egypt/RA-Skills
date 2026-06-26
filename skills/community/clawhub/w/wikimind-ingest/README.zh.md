<div align="center">

# wiki-ingest

**用于将内容写入 [WikiMind](https://github.com/HAL-9909/llm-wikimind) 知识库的 CatDesk / OpenClaw Skill。**

[![ClawHub](https://img.shields.io/badge/ClawHub-wikimind--ingest-blue?style=flat-square)](https://clawhub.ai/skills/wikimind-ingest)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](LICENSE)

[English](README.md) | **中文**

*[WikiMind](https://github.com/HAL-9909/llm-wikimind) 生态的一部分 — [Karpathy LLM Wiki 方法](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) 的生产级实现。*

</div>

---

## 它做什么

说一句 **"把这个加到我的知识库"**，AI 会自动：

1. 读取你的 Wiki 结构，理解领域分类
2. 判断内容类型（`concept` / `entity` / `comparison` / `source-summary`）
3. 写入带 frontmatter 的标准 Markdown 页面
4. 更新 BM25 搜索索引
5. 记录操作日志

下次你问到相关话题，AI 会优先搜索你的 Wiki，而不是去网上找。

---

## 前置条件

- 已安装并配置 [WikiMind](https://github.com/HAL-9909/llm-wikimind)
- 在 CatDesk/OpenClaw 中注册了 `wiki-kb` MCP Server
- 已安装 `qmd`：`pip3 install qmd`

---

## 安装

```bash
# 通过 ClawHub
npx clawhub@latest install wikimind-ingest

# 手动安装
cp SKILL.md ~/.catpaw/skills/wiki-ingest/SKILL.md
```

---

## 触发短语

| 语言 | 短语 |
|------|------|
| 中文 | `加到知识库`、`写入知识库`、`保存到 wiki`、`记录到知识库`、`把这个存起来`、`整理成知识库页面` |
| 英文 | `add to knowledge base`、`ingest this`、`save to wiki`、`store this note`、`wiki_ingest` |

---

## 相关链接

- [WikiMind](https://github.com/HAL-9909/llm-wikimind) — 本 Skill 写入的知识库系统
- [Karpathy LLM Wiki Gist](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) — 原始方法论

---

## License

MIT
