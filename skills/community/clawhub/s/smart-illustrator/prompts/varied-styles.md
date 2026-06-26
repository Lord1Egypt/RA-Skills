# Varied 模式风格提示

当使用 `--varied` 参数时，会生成两种不同风格的封面供选择。以下是两种风格的提示文本，会自动追加到 prompt 末尾。

## Candidate 1: Dramatic & High-Contrast

**风格提示（Candidate 1）**：dramatic & high-contrast（戏剧性高对比）
- 使用强烈的明暗对比
- 情绪张力强
- 视觉冲击力优先

## Candidate 2: Minimal & Professional

**风格提示（Candidate 2）**：minimal & professional（极简专业）
- 极简构图，留白充足
- 专业、克制、高级感
- 信息清晰优先

---

## 使用说明

- **自动应用**：当检测到是封面生成（prompt 包含 cover/封面/youtube/thumbnail）且开启 `--varied` 时自动使用
- **覆盖范围**：这些提示会追加到用户的 prompt 之后
- **与 style 关系**：这些提示是对 `styles/style-dark.md` 的补充，不会覆盖核心规则

## 自定义建议

你可以修改上面两种风格的描述来调整生成效果：

- **风格 1**：适合传达强烈情绪、吸引注意力的场景
- **风格 2**：适合专业内容、教程类视频的场景

修改后保存，下次 `--varied` 生成时自动生效。
