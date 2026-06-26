# Prompts 目录说明

本目录集中管理 Smart Illustrator 的所有 AI prompt 模板。

## 为什么集中管理？

- **修改方便**：不需要修改代码，直接编辑 Markdown 文件
- **便于迭代**：方便对比不同版本的 prompt 效果
- **易于分享**：其他用户可以轻松自定义 prompt
- **降低门槛**：非技术用户也能调整生成策略

## Prompt 文件列表

| 文件 | 用途 | 被调用位置 |
|------|------|-----------|
| `varied-styles.md` | Varied 模式的两种风格提示（dramatic/minimal） | `scripts/generate-image.ts` |
| `learning-analysis.md` | 封面学习分析的 AI prompt | `scripts/cover-learner.ts` |

## 其他 Prompt 在哪里？

- **风格文件**：`styles/style-light.md` 和 `styles/style-dark.md` 定义了核心设计规则
- **品牌配色**：`styles/brand-colors.md` 定义了配色方案
- **封面学习记录**：`~/.smart-illustrator/cover-learnings.md`（运行时生成）

## 如何自定义？

1. **修改风格提示**：编辑 `varied-styles.md`，调整 dramatic/minimal 的具体描述
2. **修改学习分析**：编辑 `learning-analysis.md`，调整 AI 分析封面时关注的要素

修改后无需重启，下次生成时自动生效。

## 注意事项

- ⚠️ 修改 prompt 后建议先测试生成效果
- ⚠️ 保持 JSON 格式的正确性（如 `learning-analysis.md`）
- ⚠️ 不要删除必需的字段，可以调整描述和说明
