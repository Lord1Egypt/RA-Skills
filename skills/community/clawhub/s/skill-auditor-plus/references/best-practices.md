# AgentSkill 最佳实践指南

## 核心原则

### 1. 简洁至上 (Concise is Key)

Context window 是公共资源。Skills 与系统提示、对话历史、其他技能的元数据共享 context window。

**默认假设：Codex 已经很聪明了。** 只添加 Codex 没有的知识。挑战每一条信息："Codex 真的需要这个解释吗？" 和 "这个段落是否值得占用 token？"

优先使用简洁的示例，而不是冗长的解释。

### 2. 设置适当的自由度

根据任务的脆弱性和可变性匹配 specificity 级别：

**高自由度（基于文本的指令）**：当多种方法都有效、决策取决于上下文、或启发式方法指导方法时使用。

**中等自由度（伪代码或带参数的脚本）**：当存在首选模式、一些变化可接受、或配置影响行为时使用。

**低自由度（特定脚本、少参数）**：当操作脆弱且容易出错、一致性至关重要、或必须遵循特定序列时使用。

将 Codex 想象成在探索路径：有悬崖的窄桥需要特定的护栏（低自由度），而开阔的田野允许多条路线（高自由度）。

## SKILL.md 结构

### Frontmatter (YAML)

```yaml
---
name: skill-name
description: Clear description of what the skill does and when to use it
---
```

**重要：**
- `name`: 技能名称（小写字母、数字、连字符）
- `description`: 主要触发机制，帮助 Codex 理解何时使用技能
  - 包含技能做什么以及特定触发/上下文
  - 包含所有"何时使用"信息 - 不要在 body 中
  - 示例："用于处理专业文档（.docx 文件）的综合文档创建、编辑和分析：创建新文档、修改或编辑内容、使用修订跟踪、添加评论，或任何其他文档任务"

### Body (Markdown)

指令和使用技能的指导。仅在技能触发后加载。

## 渐进式披露设计原则

Skills 使用三级加载系统来高效管理 context：

1. **Metadata（name + description）** - 始终在 context 中（~100 词）
2. **SKILL.md body** - 当技能触发时（<5k 词）
3. **Bundled resources** - Codex 需要时（无限，因为脚本可以在不读取到 context window 的情况下执行）

### 渐进式披露模式

保持 SKILL.md body 精简且低于 500 行，以减少 context 膨胀。当接近此限制时，将内容拆分到单独的文件中。拆分内容时，重要的是从 SKILL.md 引用它们，并清楚地描述何时读取它们，以确保技能读者知道它们的存在以及何时使用它们。

**关键原则：** 当技能支持多个变体、框架或选项时，仅在 SKILL.md 中保留核心工作流和选择指导。将变体特定的细节（模式、示例、配置）移动到单独的 reference 文件中。

**模式 1：高级指南 + 引用**

```markdown
# PDF Processing

## Quick start

Extract text with pdfplumber:
[code example]

## Advanced features

- **Form filling**: See [FORMS.md](FORMS.md) for complete guide
- **API reference**: See [REFERENCE.md](REFERENCE.md) for all methods
- **Examples**: See [EXAMPLES.md](EXAMPLES.md) for common patterns
```

Codex 仅在需要时加载 FORMS.md、REFERENCE.md 或 EXAMPLES.md。

**模式 2：特定领域组织**

对于支持多个领域的 Skills，按领域组织内容以加载不相关的 context：

```
bigquery-skill/
├── SKILL.md (overview and navigation)
└── reference/
    ├── finance.md (revenue, billing metrics)
    ├── sales.md (opportunities, pipeline)
    ├── product.md (API usage, features)
    └── marketing.md (campaigns, attribution)
```

当用户询问销售指标时，Codex 仅读取 sales.md。

**模式 3：条件细节**

显示基本内容，链接到高级内容：

```markdown
# DOCX Processing

## Creating documents

Use docx-js for new documents. See [DOCX-JS.md](DOCX-JS.md).

## Editing documents

For simple edits, modify the XML directly.

**For tracked changes**: See [REDLINING.md](REDLINING.md)
**For OOXML details**: See [OOXML.md](OOXML.md)
```

Codex 仅在用户需要这些功能时读取 REDLINING.md 或 OOXML.md。

**重要指南：**

- **避免深层嵌套引用** - 保持引用距离 SKILL.md 一层。所有引用文件应直接从 SKILL.md 链接。
- **结构化较长的引用文件** - 对于超过 100 行的文件，在顶部包含目录，以便 Codex 在预览时可以看到完整范围。

## 安全最佳实践

### 避免危险操作

- **文件删除**：避免使用 `rm -rf`、`rmdir`、`unlink` 等危险命令
- **系统命令**：谨慎使用 `eval`、`exec`、`subprocess.call`、`os.system`
- **网络请求**：明确说明何时使用外部 API，并提供安全示例
- **凭证管理**：永远不要在代码中硬编码 API keys、secrets、tokens

### 使用环境变量

```python
# ❌ 错误：硬编码凭证
api_key = "sk-1234567890"

# ✅ 正确：使用环境变量
import os
api_key = os.getenv('API_KEY')
if not api_key:
    raise ValueError("API_KEY environment variable not set")
```

### 输入验证

```python
# 验证文件路径
from pathlib import Path

def safe_path(path: str) -> Path:
    """确保路径在允许的目录内"""
    p = Path(path).resolve()
    if not str(p).startswith(allowed_dir):
        raise ValueError(f"Path {p} is outside allowed directory")
    return p
```

## 性能优化

### 减少 Token 使用

1. **使用脚本**：对于重复代码，创建 `scripts/` 文件而不是在 SKILL.md 中重复
2. **延迟加载**：将详细文档放在 `references/` 中，仅在需要时加载
3. **避免重复**：不要在 SKILL.md 和 references/ 中重复相同信息

### 示例：使用脚本减少重复

```python
# scripts/rotate_pdf.py
import sys
from pypdf import PdfReader, PdfWriter

def rotate_pdf(input_path, output_path, degrees):
    """旋转 PDF"""
    reader = PdfReader(input_path)
    writer = PdfWriter()

    for page in reader.pages:
        writer.add_page(page.rotate(degrees))

    with open(output_path, 'wb') as f:
        writer.write(f)

if __name__ == '__main__':
    rotate_pdf(sys.argv[1], sys.argv[2], int(sys.argv[3]))
```

然后在 SKILL.md 中：

```markdown
## Rotating PDFs

Use the rotate_pdf script:

```bash
python3 scripts/rotate_pdf.py input.pdf output.pdf 90
```
```

## 文档规范

### 描述完整性

在 `description` 字段中包含：
- 技能的核心功能
- 何时触发（使用场景）
- 关键触发词或短语

### 使用场景示例

好的描述示例：

```yaml
description: Comprehensive document creation, editing, and analysis with support for tracked changes, comments, formatting preservation, and text extraction. Use when Codex needs to work with professional documents (.docx files) for: (1) Creating new documents, (2) Modifying or editing content, (3) Working with tracked changes, (4) Adding comments, or any other document tasks
```

不好的描述示例：

```yaml
description: A tool for working with documents
```

## 常见错误

### 1. 不要包含不必要的文件

❌ 错误：创建 README.md、INSTALLATION_GUIDE.md、QUICK_REFERENCE.md 等
✅ 正确：仅包含 SKILL.md 和必要的 scripts/references/assets

### 2. 不要在 SKILL.md 中重复引用内容

❌ 错误：在 SKILL.md 中详细说明，然后在 references/ 中重复
✅ 正确：在 SKILL.md 中简要概述，在 references/ 中详细说明

### 3. 不要让 SKILL.md 过长

❌ 错误：SKILL.md 超过 500 行或 5000 tokens
✅ 正确：拆分内容到 references/ 文件中

### 4. 不要忽略安全性

❌ 错误：硬编码凭证、使用危险命令而不警告
✅ 正确：使用环境变量、警告危险操作、提供安全示例
