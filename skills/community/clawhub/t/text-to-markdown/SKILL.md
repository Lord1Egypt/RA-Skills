---
name: text-to-markdown
description: 纯文本格式预处理工具，自动插入换行、拆分长段落，为后续 AI/LLM 生成 Markdown 提供结构化输入。
---

# Text to Markdown

## 描述

纯文本格式预处理工具，自动插入换行、拆分长段落，为后续 AI/LLM 生成 Markdown 提供结构化输入。

## 触发词

`转markdown`、`整理成markdown`、`格式化成markdown`、`转成md格式`

---

## 功能：文本预处理

本 skill 专注于**格式预处理**，将无结构的纯文本转换为结构化输出，为 AI/LLM 生成 Markdown 提供良好基础。

### 预处理能力

| 能力 | 说明 |
|------|------|
| **插入换行** | 在标题前、转折词处自动插入换行 |
| **长段落拆分** | 按语义（转折、因果）智能分段落 |
| **特殊符号保留** | → ↔ ✓ ✗ 等符号保留原样 |
| **IMA 笔记优化** | 专为无换行的 IMA 导出文本优化 |

### 特殊场景：IMA 笔记导出

IMA 导出的纯文本特征：无换行、长段落、标题混在段落中。

**处理策略**：
1. 用 `scripts/preprocess.py` 预处理（插入换行）
2. 自动在标题前、转折词处分段
3. 中文序号标题自动识别

```powershell
# 预处理 IMA 笔记
python "C:\Users\17116\.workbuddy\skills\Text to Markdown\scripts\preprocess.py" input.txt output.md
```

### 执行流程

1. **预处理**：用 `scripts/preprocess.py` 插入换行、拆分段落
2. **AI 增强**：AI/LLM 基于预处理结果生成完整 Markdown（标题层级、加粗、列表等）

### 核心原则

> **只改格式，不改文字**：预处理过程中保持原文一字不变。

---

## 快速核查

预处理完成后快速检查：

- [ ] 原文文字一字未改
- [ ] 标题前已插入换行
- [ ] 长段落已拆分
- [ ] 特殊符号保留原样

---

## 参考资料

- **IMA 笔记示例**：见 [references/examples.md](references/examples.md)

---

## 注意事项

预处理只负责格式调整，Markdown 语法（标题层级、加粗、列表等）由 AI/LLM 后续生成。
