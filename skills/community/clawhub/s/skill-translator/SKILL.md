---
name: skill-translator
description: 翻译技能文档的工具。当用户想要翻译 SKILL.md 文件的内容为中文时使用此技能。用户输入技能路径，工具会读取该路径下的 SKILL.md 文件，将其内容翻译成中文，并输出命名为 SKILL(1).md 的文件到同一文件夹中。
---

# 技能文档翻译工具

这是一个用于翻译技能文档的工具，可以将 SKILL.md 文件的内容翻译成中文。

## 使用方法

用户输入技能路径，工具将执行以下步骤：

1. **读取源文件**：从用户提供的路径读取 SKILL.md 文件
2. **翻译内容**：将文件内容翻译成中文
3. **生成输出**：在相同路径下创建 SKILL(1).md 文件

## 工作流程

### 输入
- 用户提供的技能路径（例如：`C:\Users\LJT\.agents\skills\autoglm-browser-agent\`）

### 处理步骤
1. 读取指定路径下的 SKILL.md 文件
2. 将文件内容翻译成中文
3. 在相同目录下创建 SKILL(1).md 文件

### 输出
- 新文件：`SKILL(1).md`（翻译后的中文内容）
- 位置：与原 SKILL.md 文件相同目录

## 注意事项

- 确保输入的路径正确且包含 SKILL.md 文件
- 翻译时会保持原有的 Markdown 格式
- 输出文件会覆盖同名的 SKILL(1).md 文件（如果存在）
- 保留原有的 YAML frontmatter（名称和描述字段除外，需要翻译）

## 示例

**用户输入**：
```
帮我翻译这个技能文档：C:\Users\LJT\.agents\skills\autoglm-browser-agent\
```

**工具执行**：
1. 读取 `C:\Users\LJT\.agents\skills\autoglm-browser-agent\SKILL.md`
2. 翻译内容为中文
3. 创建 `C:\Users\LJT\.agents\skills\autoglm-browser-agent\SKILL(1).md`

---

## 触发条件

当用户提到：
- "翻译技能文档"
- "把 SKILL.md 翻译成中文"
- "技能路径" + "翻译"
- 提供具体的技能路径并要求翻译

时使用此技能。
