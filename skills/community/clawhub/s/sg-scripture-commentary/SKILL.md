---
name: sg-scripture-commentary
description: Format and write scripture commentary for religious texts (Buddhist sutras, Daoist classics, Bible, etc.) with original text and explanations. Use when asked to explain, annotate, or write commentary for any religious or philosophical scripture. Triggers on phrases like "解经", "注释经文", "write commentary", "explain this scripture", "annotate this text".
---

# Scripture Commentary

Format and write scripture commentary for religious texts with original text and explanations.

## Workflow

1. **Get source URL** - If user didn't provide a link to the original text, ask for it first
2. **Confirm output path** - Ask user where to save the file before starting
3. **Fetch source** - Get the original text from URL or user-provided content
4. **Check existing format** - If file exists, read it to match existing style
5. **Write in batches** - Process content section by section
6. **Report progress** - Announce progress at each 10% milestone

## Format Rules

### Basic Structure

```
原文用行内代码块包围
解释在原文下一行

段落之间有一行空行
```

### Section Dividers

- Use `---` (horizontal rule) to separate major sections/chapters from the source text
- Use `# 一级标题` for chapter/section names (品、章、篇 etc.)

### Line Length

- Keep original text segments under 30 characters per line when possible
- One thought/idea per paragraph - complete the explanation within one paragraph

### Example

```markdown
# 行由品第一

`时大师至宝林。`
当时，六祖惠能大师抵达了韶州曹溪的宝林寺。

`韶州韦刺史名璩与官僚入山。`
韶州刺史韦璩与同僚官员们一起进入宝林山。

---
`大师告众曰。善知识。`
大师对大众说道：各位善知识。
```

## Progress Reporting

Report progress at each 10% milestone:

- 10% - "已完成 10%"
- 20% - "已完成 20%"
- ... and so on

Also report when each major section/chapter is complete.

## Output

- Write to the user-specified path
- Use UTF-8 encoding
- Ask before overwriting existing files
