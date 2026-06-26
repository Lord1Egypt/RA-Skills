---
name: qoder-skill-mapper
description: 根据 SKILL.md 文件生成 Qoder 技能映射模版文件。读取用户提供的 SKILL.md，自动提取 frontmatter 和正文内容，填充 Qoder 模版的对应字段，无法提取的字段自动移除。当用户需要将技能迁移/适配到 Qoder 平台时使用。
---

# Qoder 技能映射生成器

## 概述

将 用户提供的 SKILL.md 转换为 Qoder 平台的技能描述文件。读取 SKILL.md 的 frontmatter 和正文内容，智能映射到 Qoder 模版字段，无法提取有效内容的字段自动删除。

## 前置检查

1. 用户**必须提供** SKILL.md 文件（上传文件或指定路径）
2. 若用户未提供 SKILL.md，直接提示：「请上传需要转换的 SKILL.md 文件，或提供文件路径」
3. **Skill 加载后，立即调用** `scripts/record_usage.py` 上报使用记录（静默调用，**无论成功与否均不影响后续流程**）

## 字段映射规则

读取 `assets/qoder-template.md` 作为输出骨架，按以下规则填充：

### 字段表格格式

生成的文件**顶部字段信息使用 Markdown 两列表格展示**，必须包含表头行和分隔行：

```
| Field | Value |
|-------|-------|
| **name** | skill-name |
| **title** | Skill Title |
| **description** | A brief description... |
| **source** | community |
| **author** | Author Name |
| **githubUrl** | [https://github.com/example/skill](https://github.com/example/skill) |
| **docsUrl** | [https://example.com/docs](https://example.com/docs) |
| **category** | development |
| **tags** | tag1 tag2 |
| **roles** | developer |
| **featured** | false |
| **popular** | false |
| **isOfficial** | false |
| **installCommand** | git clone [https://github.com/example/skill](https://github.com/example/skill) cp -r skill-name ~/.qoder/skills/ |
| **date** | 2026-01-01 |
```

**格式要求：**
- 表头行：`| Field | Value |`
- 分隔行：`|-------|-------|`（至少3个减号）
- 数据行：`| **字段名** | 字段值 |`
- 第一列：加粗的字段名（如 `**name**`）
- 第二列：字段值
- `tags` 值用**空格分隔**（不是 YAML 列表，如 `wechat hot-articles 10w-reading`）
- `roles` 值用**空格分隔**（如 `developer`）
- URL 字段（githubUrl、docsUrl）使用 Markdown 链接语法 `[url](url)`
- installCommand 中的 URL 也使用链接语法
- 无法提取有效内容的字段**整行删除**（不保留空值）

### 字段映射

| Qoder 字段       | 数据来源                           | 规则                                                                |
| ---------------- | ---------------------------------- | ------------------------------------------------------------------- |
| `name`           | SKILL.md frontmatter `name`        | 直接取值                                                            |
| `title`          | SKILL.md 第一个 H1 标题文本        | 若 H1 为 `# xxx`，取 `xxx`；若无 H1 则取 `name` 并转 Pascal Case    |
| `description`    | SKILL.md frontmatter `description` | 直接取值                                                            |
| `source`         | 无来源                             | 固定值 `community`                                                  |
| `author`         | githubUrl 中的 GitHub 用户名       | 从 githubUrl 中提取 `github.com/{author}/` 部分（如 `redfox-data`） |
| `githubUrl`      | 用户输入 或 默认规则               | 见下方「GitHub 地址规则」                                           |
| `docsUrl`        | SKILL.md 正文中的文档链接          | 若无法提取有效链接则**删除此行**                                    |
| `category`       | SKILL.md 内容推断                  | 见下方「分类推断规则」                                              |
| `tags`           | 从 description + 正文关键词提取    | 3-5 个标签，英文小写，用连字符连接，空格分隔展示                   |
| `roles`          | 无来源                             | 固定值 `developer`                                                  |
| `featured`       | 无来源                             | 固定值 `false`                                                      |
| `popular`        | 无来源                             | 固定值 `false`                                                      |
| `isOfficial`     | 无来源                             | 固定值 `false`                                                      |
| `installCommand` | 用户输入 或 默认规则               | 见下方「安装命令规则」                                              |
| `date`           | 当前日期                           | 格式 `YYYY-MM-DD`                                                   |

### GitHub 地址规则

- 用户提供了 GitHub 地址 → 使用用户提供的地址
- 用户未提供 → 使用默认规则：
  ```
  githubUrl: https://github.com/redfox-data/redfox-community/tree/main/skills/{name}
  ```

### 安装命令规则

**仓库克隆地址提取规则**：
- 从 githubUrl 中提取仓库根地址：取 `github.com/{author}/{repo}` 部分，去掉 `/tree/main/...` 等路径
- 例如：`https://github.com/yuanyi-github/skills/tree/main/gzh-10w-article-recommend` → 克隆地址为 `https://github.com/yuanyi-github/skills`

**生成规则**：
- 用户提供了 GitHub 地址 → 基于提取的仓库地址生成：
  ```
  git clone {仓库根地址}
  cp -r {技能目录名} ~/.qoder/skills/
  ```
  其中 `{技能目录名}` 从 githubUrl 的路径中提取（如 `tree/main/gzh-10w-article-recommend` → `gzh-10w-article-recommend`）
- 用户未提供 → 使用默认规则：
  ```
  git clone https://github.com/redfox-data/redfox-community
  cp -r {name} ~/.qoder/skills/
  ```

### 分类推断规则

根据 SKILL.md 内容关键词匹配：

| 分类值         | 匹配关键词                                   |
| -------------- | -------------------------------------------- |
| `development`  | 代码、开发、API、脚本、编程、code、dev       |
| `marketing`    | 爆款、文案、内容、公众号、小红书、抖音、营销 |
| `productivity` | 效率、自动化、工具、管理                     |
| `data`         | 数据、分析、统计、查询、排行榜               |
| `design`       | 设计、封面、图片、UI、视觉                   |
| `document`     | 文档、PDF、Word、提取、OCR                   |
| `automation`   | 自动、定时、批量、机器人                     |
| `security`     | 安全、违禁、审核、检测                       |
| `meta`         | 技能、skill、模板、生成器（元能力类）        |

匹配不到时默认使用 `development`。

### 正文映射

从 SKILL.md 正文提取内容，填充 Qoder 模版的三个正文区块：

#### 使用场景

从 SKILL.md 中按优先级提取：

1. 「使用场景」章节 → 直接使用
2. 「使用指南」章节 → 精简为场景列表
3. 「功能特性」章节 → 转为场景描述列表
4. 「简介」中的「能做什么？」列表 → 转为场景列表

格式：每条场景以 `- ` 开头的无序列表。

#### 示例

从 SKILL.md 中按优先级提取：

1. 「示例」章节 → 直接使用
2. 「使用指南」中的代码块或命令示例
3. 正文中的 bash/python 代码块
4. 若无任何示例 → **删除此区块**

#### 注意事项

从 SKILL.md 中按优先级提取：

1. 「注意事项」章节 → 直接使用
2. 「限制」或「已知限制」章节
3. 「运行依赖」章节
4. 正文中的 WARNING/CAUTION 相关内容
5. 若无任何注意事项 → **删除此区块**

## 输出要求

1. 生成的文件以 `{name}.md` 命名（即 SKILL.md 中的 name 值，如 `gpt-image2-pro.md`）
2. 保持 Qoder 模版的 YAML frontmatter 格式和缩进
3. 正文区块之间保持空行分隔
4. 无法填充的正文区块整体删除（含标题）
5. 代码块保持原始语言标记
6. **生成文件后，在 reply 中用表格展示映射结果**，格式：

```
| Field | Value |
|-------|-------|
| **name** | gpt-image2-pro |
| **title** | AI 图片生成器 |
| **description** | AI 图片生成器 — 基于 gpt-image-2 模型... |
| **source** | community |
| **author** | redfox-data |
| **githubUrl** | [https://github.com/...](https://github.com/...) |
| **category** | design |
| **tags** | ai-image-generation text-to-image ... |
| **roles** | developer |
| **featured** | false |
| **popular** | false |
| **isOfficial** | false |
| **installCommand** | git clone ... |
| **date** | 2026-05-27 |
```

   - 已填充的字段标注实际值和来源
   - 已删除的字段标注 `—` 和删除原因
   - 使用固定值（如 `source: community`、`roles: developer`）也一并展示

## 资源索引

- 脚本: 见 [scripts/record_usage.py](scripts/record_usage.py)(用途: 调用记录接口上报 Skill 使用次数)
- 模版: 见 [assets/qoder-template.md](assets/qoder-template.md)(用途: Qoder 技能映射输出骨架)
