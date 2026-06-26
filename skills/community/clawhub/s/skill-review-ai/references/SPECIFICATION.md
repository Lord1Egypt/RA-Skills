# Agent Skills 规范

Agent Skills 的完整格式规范。

## 目录结构

```
skill-name/
├── SKILL.md          # 必需: 元数据 + 指令
├── scripts/          # 可选: 可执行代码
├── references/       # 可选: 文档参考
├── assets/           # 可选: 模板、资源
└── ...               # 其他文件或目录
```

## SKILL.md 格式

SKILL.md 文件必须包含 YAML frontmatter，后跟 Markdown 内容。

### Frontmatter

| 字段 | 必需 | 约束 |
|------|------|------|
| `name` | 是 | 最多 64 字符。仅小写字母、数字和连字符。不能以连字符开头或结尾。 |
| `description` | 是 | 最多 1024 字符。非空。描述 skill 的功能和使用场景。 |
| `license` | 否 | 许可证名称或 bundled 许可证文件引用。 |
| `compatibility` | 否 | 最多 500 字符。指示环境要求（目标产品、系统包、网络访问等）。 |
| `metadata` | 否 | 任意键值映射，用于额外元数据。 |
| `allowed-tools` | 否 | 预批准工具的空格分隔字符串。（实验性） |

### 最小示例

```markdown
---
name: skill-name
description: A description of what this skill does and when to use it.
---
```

### 完整示例

```markdown
---
name: pdf-processing
description: Extract PDF text, fill forms, merge files. Use when handling PDFs.
license: Apache-2.0
metadata:
  author: example-org
  version: "1.0"
---
```

### name 字段

必需字段，约束：
- 1-64 字符
- 仅小写字母（`a-z`）和连字符（`-`）
- 不能以连字符开头或结尾
- 不能包含连续连字符（`--`）
- 必须与父目录名匹配

**有效示例：**
```yaml
name: pdf-processing
name: data-analysis
name: code-review
```

**无效示例：**
```yaml
name: PDF-Processing  # 不允许大写
name: -pdf             # 不能以连字符开头
name: pdf--processing  # 不允许连续连字符
```

### description 字段

必需字段，约束：
- 1-1024 字符
- 应描述 skill 的功能和使用场景
- 应包含帮助 agent 识别相关任务的关键词

**良好示例：**
```yaml
description: Extracts text and tables from PDF files, fills PDF forms, and merges multiple PDFs. Use when working with PDF documents or when the user mentions PDFs, forms, or document extraction.
```

**不良示例：**
```yaml
description: Helps with PDFs.
```

### license 字段

可选字段，指定 skill 的许可证。

**示例：**
```yaml
license: Proprietary. LICENSE.txt has complete terms
```

### compatibility 字段

可选字段，指示环境要求。

**示例：**
```yaml
compatibility: Designed for Claude Code (or similar products)
compatibility: Requires git, docker, jq, and access to the internet
compatibility: Requires Python 3.14+ and uv
```

### metadata 字段

可选字段，字符串键值对映射。

**示例：**
```yaml
metadata:
  author: example-org
  version: "1.0"
```

### allowed-tools 字段

可选字段，预批准工具的空格分隔字符串。

**示例：**
```yaml
allowed-tools: Bash(git:*) Bash(jq:*) Read
```

## 正文内容

YAML frontmatter 后的 Markdown 内容包含 skill 指令。没有格式限制，写入任何有助于 agent 有效执行任务的内容。

推荐章节：
- 分步说明
- 输入输出示例
- 常见边界情况

## 可选目录

### scripts/

包含 agent 可以运行的可执行代码。脚本应该：
- 自包含或清晰记录依赖关系
- 包含有用的错误消息
- 优雅地处理边界情况

支持的语言取决于 agent 实现。常见选项包括 Python、Bash 和 JavaScript。

### references/

包含 agent 需要时可以读取的额外文档：
- `REFERENCE.md` - 详细技术参考
- `FORMS.md` - 表单模板或结构化数据格式
- 特定领域文件（`finance.md`、`legal.md` 等）

保持单个参考文件聚焦。Agent 按需加载这些文件，因此较小的文件意味着更少的上下文使用。

### assets/

包含静态资源：
- 模板（文档模板、配置模板）
- 图片（图表、示例）
- 数据文件（查找表、模式）

## 渐进式披露

Skills 应该为高效使用上下文而结构化：

1. **元数据**（~100 tokens）：`name` 和 `description` 字段在启动时为所有 skills 加载
2. **指令**（建议 < 5000 tokens）：当 skill 被激活时加载完整的 `SKILL.md` 正文
3. **资源**（按需）：文件（例如 `scripts/`、`references/` 或 `assets/` 中的文件）仅在需要时加载

保持主 `SKILL.md` 在 500 行以下。将详细参考材料移到单独的文件中。

## 文件引用

引用 skill 中的其他文件时，使用从 skill 根目录开始的相对路径：

```markdown
See [the reference guide](references/REFERENCE.md) for details.

Run the extraction script:
scripts/extract.py
```

保持文件引用从 `SKILL.md` 开始只有一级深度。避免深层嵌套的引用链。
