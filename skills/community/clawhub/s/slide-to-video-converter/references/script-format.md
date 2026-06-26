# Speaker Notes Script Format

The script file (`script.md`) contains per-page speaker notes in Markdown format.

## Required Format

```markdown
# Title (optional, ignored by parser)

## 第1页：Slide Title

**演讲稿**：
Speaker notes text for slide 1. This is the narration that will be
converted to speech via Edge TTS.

---

## 第2页：Another Slide

**演讲稿**：
Speaker notes for slide 2. Can be multiple sentences.
The text between **演讲稿**： and the next `---` or `## 第N页` is extracted.

---

## 第3页：Third Slide

**演讲稿**：
More narration text here...
```

## Rules

1. Each slide section starts with `## 第N页` (N = slide number, must match PDF page order)
2. Speaker notes are marked by `**演讲稿**：` followed by the text on the next line(s)
3. Sections are separated by `---` (horizontal rule)
4. Slide numbers must be sequential and match the PDF page count
5. The title after `第N页：` is used for logging only; narration comes from the `**演讲稿**` block

## Example

For a 3-page presentation about AI:

```markdown
# AI技术分享

## 第1页：封面

**演讲稿**：
大家好，今天我来分享关于AI技术的最新进展。

---

## 第2页：什么是大模型

**演讲稿**：
大模型是指参数量在数十亿以上的深度学习模型。它们通过海量数据训练，具备了强大的语言理解和生成能力。

---

## 第3页：总结

**演讲稿**：
总结一下今天的分享要点。谢谢大家。
```
