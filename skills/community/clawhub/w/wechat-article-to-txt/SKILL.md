---
name: wechat-article-to-txt
description: "将微信公众号文章自动转为个人知识库笔记。输入公众号文章链接，自动抓取正文、AI 多维度总结（摘要/核心观点/金句/标签）、生成结构化 Markdown 笔记并存入本地。"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob
metadata:
  clawdbot:
    emoji: "📥"
    requires:
      bins:
        - python3
        - node
    install:
      - id: npm-cheerio
        kind: npm
        name: cheerio
        bins: [ ]
        label: "Install cheerio for HTML parsing"
---

# 微信公众号文章 → Obsidian 个人知识库

## 适用场景

当用户发来一个微信公众号文章链接（`https://mp.weixin.qq.com/s/...`），希望：

1. **保存到 Obsidian 知识库** — 转为结构化 Markdown 笔记
2. **自动总结** — 提取摘要、核心观点、金句、关键数据
3. **自动打标签** — 基于内容生成 Obsidian 标签
4. **建立知识关联** — 生成双向链接建议

## 工作流程

```
用户发送公众号文章链接
  │
  ▼
[步骤1] 抓取文章正文
  │   ├─ 用内置脚本提取微信文章 HTML
  │   └─ 解析标题、作者、发布时间、正文内容
  │
  ▼
[步骤2] AI 多维度总结
  │   ├─ 使用 agent 内置能力进行总结
  │   ├─ 生成：摘要(200字) / 核心观点(3-5条) / 金句 / 关键数据
  │   └─ 生成：标签(3-8个) / 相关主题建议
  │
  ▼
[步骤3] 生成 Obsidian Markdown 笔记
  │   ├─ 应用标准笔记模板
  │   ├─ 添加 YAML frontmatter（标题/来源/日期/标签/作者）
  │   └─ 组织为结构化笔记
  │
  ▼
[步骤4] 存入 Obsidian Vault
  │   ├─ 确定 Obsidian vault 路径（从配置文件读取）
  │   ├─ 按「来源/主题/日期」组织目录结构
  │   └─ 写入 .md 文件到 vault
```

## 前置条件

本技能依赖以下组件：

### 1. Node.js + cheerio（文章正文抓取）

```bash
npm install -g cheerio
```

### 2. Obsidian Vault 路径配置

首次使用需要配置你的 Obsidian vault 路径。默认从 Obsidian 配置文件读取：

```bash
cat ~/Library/Application\ Support/obsidian/obsidian.json
```

你也可以在 `scripts/config.json` 中手动指定：

```json
{
  "vault_path": "/path/to/your/vault",
  "article_dir": "Inbox/微信公众号",
  "default_tags": ["wechat"],
  "language": "zh"
}
```

本技能使用 agent 内置的 AI 能力进行总结，无需额外配置 API Key。

## 使用方法

### 方式一：发送链接直接处理

用户发送微信公众号文章链接，agent 自动执行全部流程：

```
用户: https://mp.weixin.qq.com/s/xxxxx
agent: 开始处理这篇文章...
       ✅ 已抓取正文: 《文章标题》
       ✅ 已生成摘要和总结
       ✅ 已存入 Obsidian: Inbox/微信公众号/文章标题.md
```

### 方式二：批量处理

用户发送多个链接，agent 逐个处理：

```
用户: 帮我保存这几篇文章到知识库
      https://mp.weixin.qq.com/s/aaa
      https://mp.weixin.qq.com/s/bbb
```

### 方式三：指定主题目录

```
用户: 把这篇文章存到「AI/大模型」目录下
      https://mp.weixin.qq.com/s/xxxxx
```

## 步骤详解

### 步骤1: 抓取文章正文

使用 `scripts/fetch_article.js` 抓取微信公众号文章：

```bash
node scripts/fetch_article.js "https://mp.weixin.qq.com/s/xxxxx"
```

**输出：** 文章原始 JSON 数据（标题、作者、发布时间、正文HTML、正文Markdown）

**脚本说明：**
- 使用 cheerio 解析微信文章页面
- 提取文章标题、公众号名称、发布时间
- 将正文 HTML 转为纯文本/Markdown（保留图片链接）
- 自动处理微信反爬机制（User-Agent、Cookie）

**备用方案：**
如果 cheerio 抓取失败（微信反爬限制），使用 curl 方案：

```bash
node scripts/fetch_article_fallback.js "https://mp.weixin.qq.com/s/xxxxx"
```

### 步骤2: AI 多维度总结

使用 agent 内置 AI 能力对文章内容进行多维度总结。

**总结维度：**

| 维度 | 说明 | 长度 |
|------|------|------|
| 摘要 | 文章核心内容概述 | 200-300字 |
| 核心观点 | 3-5条主要论点 | 每条30-50字 |
| 金句 | 原文中值得记录的话 | 3-5条 |
| 关键数据 | 文章中提到的数字、数据 | 按需 |
| 标签 | 基于内容自动生成 | 3-8个 |
| 相关主题 | 与知识库中其他笔记的关联建议 | 2-5条 |

**Prompt 参考：**

```
请对以下微信公众号文章进行多维度总结，输出 JSON 格式：

文章标题：{title}
公众号：{author}
正文：{content}

请输出以下格式：
{
  "summary": "200-300字的摘要",
  "key_points": ["观点1", "观点2", ...],
  "quotes": ["金句1", "金句2", ...],
  "key_data": ["数据1", "数据2", ...],
  "tags": ["标签1", "标签2", ...],
  "related_topics": ["主题1", "主题2", ...]
}
```

### 步骤3: 生成 Obsidian Markdown 笔记

使用 `scripts/generate_note.py` 生成标准化笔记：

```bash
python3 scripts/generate_note.py \
  --title "文章标题" \
  --author "公众号名称" \
  --source "https://mp.weixin.qq.com/s/xxxxx" \
  --date "2026-06-17" \
  --content "文章正文" \
  --summary "{\"summary\":\"...\",\"key_points\":[...]}" \
  --tags "wechat,AI,大模型" \
  --output /path/to/output.md
```

### 步骤4: 存入 Obsidian Vault

使用 `scripts/save_to_vault.py` 写入 Obsidian：

```bash
python3 scripts/save_to_vault.py \
  --note /path/to/note.md \
  --vault /path/to/your/vault \
  --dir "Inbox/微信公众号/AI"
```

或者直接复制到 vault：

```bash
cp /tmp/note.md "/path/to/your/vault/Inbox/微信公众号/文章标题.md"
```

## 笔记模板

生成的 Obsidian 笔记格式如下：

```markdown
---
title: "{{title}}"
source: "{{source_url}}"
author: "{{author}}"
date: {{date}}
tags:
  - wechat
  - {{tag1}}
  - {{tag2}}
status: inbox
---

# {{title}}

> **摘要：** {{summary}}

## 📌 核心观点

- {{key_point_1}}
- {{key_point_2}}
- {{key_point_3}}

## 💬 金句

> {{quote_1}}

> {{quote_2}}

## 📊 关键数据

- {{data_1}}

## 📝 笔记与思考

*（在此记录你的思考和延伸阅读）*

## 🔗 相关笔记

- [[相关笔记1]]
- [[相关笔记2]]

## 📎 原文链接

[{{title}}]({{source_url}})

---

*自动收录于 {{date}} | 来源：{{author}}*
```

## 目录组织

建议的 Obsidian 知识库结构：

```
Obsidian Vault/
├── Inbox/
│   └── 微信公众号/
│       ├── AI/
│       │   ├── 文章标题1.md
│       │   └── 文章标题2.md
│       ├── 科技/
│       ├── 财经/
│       └── 未分类/
├── Tags/
│   └── wechat.md          (MOC: Map of Content)
└── Templates/
    └── wechat-article.md   (笔记模板)
```

## 一键处理脚本

为方便使用，提供一键处理脚本：

```bash
node scripts/process_article.js "https://mp.weixin.qq.com/s/xxxxx"
```

参数说明：
- `--dir, -d`：指定 Obsidian 子目录（默认 `未分类`）
- `--tags, -t`：额外添加标签（逗号分隔）
- `--dry-run, -n`：仅预览，不写入 vault
- `--vault, -v`：指定 vault 路径（覆盖配置）
- `--output, -o`：输出到指定文件（不写入 vault）

### 示例

```bash
# 基本用法
node scripts/process_article.js "https://mp.weixin.qq.com/s/xxxxx"

# 指定目录和标签
node scripts/process_article.js "https://mp.weixin.qq.com/s/xxxxx" -d "AI/大模型" -t "深度学习,Transformer"

# 仅预览不保存
node scripts/process_article.js "https://mp.weixin.qq.com/s/xxxxx" --dry-run

# 输出到指定文件
node scripts/process_article.js "https://mp.weixin.qq.com/s/xxxxx" -o ~/Desktop/note.md
```

## 配置

默认配置文件位于 `scripts/config.json`：

```json
{
  "vault_path": "",
  "article_dir": "Inbox/微信公众号",
  "default_tags": ["wechat"],
  "language": "zh",
  "summarize_model": "default",
  "max_content_length": 10000
}
```

- `vault_path`：Obsidian vault 根目录（留空则自动从 Obsidian 配置读取）
- `article_dir`：文章存放目录（相对于 vault 根目录）
- `default_tags`：默认添加的标签
- `language`：输出语言（zh/en）
- `summarize_model`：总结模型（default 使用 agent 内置能力）
- `max_content_length`：截断过长的文章正文

## 常见问题

### 抓取失败

微信文章有反爬机制，如果抓取失败：

1. 文章可能已被删除
2. 需要登录才能查看
3. 微信反爬限制

**解决办法：**
- 尝试使用 `--fallback` 参数重试
- 手动复制文章内容粘贴给 agent
- 或者用 `curl` 带上 Cookie 重试

### 没有 Obsidian vault

如果没有安装 Obsidian，本技能仍可以：

1. 输出 Markdown 文件到指定目录
2. 生成纯文本格式的知识卡片
3. 后续随时可以导入 Obsidian

### 目录不存在

如果指定的 vault 子目录不存在，脚本会自动创建。

## 安全与隐私

- 所有数据处理在本地完成
- 文章内容仅用于生成知识笔记
- 不向第三方发送数据
- 所有 AI 总结在 agent 内部完成，数据不离开本地

## 注意事项

- 请遵守微信公众号平台的使用条款
- 抓取频率不宜过高，避免触发反爬
- 文章版权归原作者所有，笔记仅供个人学习使用
- 建议定期整理 Inbox 目录中的未分类文章
