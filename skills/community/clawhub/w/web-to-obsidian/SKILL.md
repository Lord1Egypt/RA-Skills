---
name: web-to-obsidian
description: 抓取网页文章并保存到 Obsidian vault。当用户想要保存网页文章、博客、文档到 Obsidian 时使用，特别是提到"保存到 Obsidian"、"存到 Obsidian"、"抓取网页"、"网页转 Obsidian"、"导入文章"等场景。支持自动翻译非中文内容为中文，生成元数据（标签、摘要、标题），并以 Obsidian Markdown 格式存储。
---

# Web to Obsidian

将网页文章抓取并保存到 Obsidian vault，支持自动翻译和内容元数据生成。

## 工作流程

### 1. 抓取网页内容

使用 scripts/fetch.py 获取网页的 Markdown 内容：

```bash
python3 scripts/fetch.py "<URL>" --json
```

**返回格式：**
```json
{
  "success": true,
  "url": "https://r.jina.ai/http://example.com/article",
  "content": "# Article Title\n\nClean markdown content here...",
  "source": "jina",
  "error": null
}
```

### 2. 翻译非中文内容

如果内容不是以中文为主，则进行高质量翻译：

**1. 术语精准**
- 术语专业：使用行业通用标准术语（如将 "Buffer" 译为 "缓冲区"）。
- 保持英文：对于专有名词、缩写、库名（如 React, Kubernetes, PyTorch）保持原样。
- 自创术语：若作者自创概念，保留英文并创建中文对应概念

**2. 句式重构**
- 将英文长句拆分为符合中文表达习惯的短句
- 被动语态转为主动语态（如："is used to" → "可以用来"）
- 删除不必要的代词和介词短语冗余

**3. 格式保持**
- Markdown 格式保持不变：代码块、表格、列表、链接、粗体斜体
- 图片链接和引用标记保持不变
- 不翻译代码和命令，但翻译代码块中的注释

**4. 语境优化**
- 代词根据上下文明确化（英文常用 it/this，中文需明确指代对象）
- 补充必要的逻辑连接词（因此、此外、具体来说）
- 保留原作者的强调语气（通过"注意"、"重要"等提示词）
- 去掉翻译腔：避免使用过多的“被”、“的”等冗余词汇，确保语气专业、清晰、自然、简介。


### 3. 生成元数据

基于内容分析生成以下元数据：

**必需字段：**
- `title`: 文章标题（从内容中提取或使用网页标题）
- `source`: 原始 URL
- `date`: 抓取日期（ISO 8601 格式）
- `tags`: 相关标签（3-7 个）
- `summary`: 文章摘要（100-200 字）

**可选字段：**
- `author`: 作者（如有）
- `language`: 内容语言（zh/en/ja 等）
- `translated`: 是否经过翻译（true/false）

**标签生成规则：**
1. 提取文章的核心主题（技术领域、学科等）
2. 识别文章类型（教程、新闻、论文、博客等）
3. 识别关键技术/概念
4. 使用小写字母，空格用连字符替代

**示例：**
- 技术教程 → `#tutorial`, `#programming`, `#python`
- AI 文章 → `#ai`, `#machine-learning`, `#llm`
- 新闻 → `#news`, `#technology`

### 4. 创建 Obsidian Markdown 文件，并写入temp.md中

生成符合 Obsidian 格式的 Markdown 文件，包含：

**Frontmatter（YAML 头部）：**
```yaml
---
title: "文章标题"
date: "2024-01-15"
source: "https://example.com/article"
tags:
  - tag1
  - tag2
  - tag3
author: "作者名"
summary: "文章摘要"
language: "en"
translated: true
---
```

**内容主体：**
```markdown

正文内容...

```

将生成的内容生写入 ***当前目录下的temp.md中*** ，***注意：正文内容部分不要进行任何修改、抽象和演绎，直接写入即可***。

   ，
### 7. 导入到 Obsidian

使用 obsidian-cli 将文件导入到 Obsidian vault：

```bash
# 方法1：使用 create 命令直接创建
obsidian create name="文章标题" content="$(cat temp.md)"

# 方法2：如果支持从文件创建
# obsidian create --file "$TEMP_FILE" name="文章标题"
```

**指定目标文件夹（可选）：**
- 默认导入到 vault 根目录
- 用户可以指定文件夹路径，例如：`--folder="articles/web"`

### 8. 清理临时文件

导入完成后删除临时文件：

```bash
rm -f temp.md
```

## 使用示例

### 基本用法

用户："帮我抓取这篇文章 https://example.com/article 保存到 Obsidian"

执行步骤：
1. 抓取网页内容
2. 判断语言，需要翻译则翻译
3. 生成元数据
4. 创建 Obsidian Markdown 文件
5. 导入到 Obsidian
6. 清理临时文件

### 指定文件夹

用户："抓取 https://example.com/article 保存到 Obsidian 的 articles/tech 文件夹"

在创建时指定文件夹路径。

### 批量抓取

用户："帮我抓取这几篇文章到 Obsidian：[url1], [url2], [url3]"

对每篇文章依次执行抓取流程。


## 注意事项

1. **翻译质量**：确保翻译质量。如果翻译不理想，提示用户可以手动调整。

2. **网络问题**：如果抓取失败，scripts/fetch.py 会自动降级到备用服务。如果全部失败，提示用户检查 URL。

3. **Obsidian 连接**：obsidian-cli 需要 Obsidian 正在运行。如果连接失败，提示用户打开 Obsidian。

4. **文件名处理**：
   - 使用文章标题作为文件名（去除特殊字符）
   - 如果标题为空，使用 URL 的最后部分
   - 避免文件名冲突（添加时间戳或序号）

5. **隐私注意**：抓取的网页内容可能包含隐私信息，提醒用户注意。

## 错误处理

**抓取失败：**
- 检查 URL 是否可访问
- 尝试使用本地web fetch工具进行抓取
- 提示用户提供文章内容

**Obsidian 导入失败：**
- 检查 Obsidian 是否运行
- 检查 vault 名称是否正确
- 提示用户手动导入临时文件

**翻译失败：**
- 使用原始语言保存
- 在元数据中标记为未翻译

## 完整流程示例

```
用户: 帮我保存这篇文章到 Obsidian: https://python.langchain.com/docs/get_started/introduction

步骤:
1. 抓取 → 获取英文 Markdown 内容
2. 检测 → 判断为英文内容（需要翻译）
3. 翻译 → 翻译为中文，保持格式
4. 元数据 → 
   - title: "LangChain 入门介绍"
   - tags: ["python", "langchain", "llm", "tutorial"]
   - summary: "LangChain 是一个用于构建 LLM 应用的框架..."
5. 创建文件 → 生成带 frontmatter 的 Markdown
6. 导入 → 使用 obsidian-cli 导入
7. 清理 → 删除临时文件
8. 反馈 → 告诉用户已保存成功，文件名是 "LangChain 入门介绍.md"
```
