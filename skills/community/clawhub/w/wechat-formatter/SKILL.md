---
name: wechat-formatter
description: 【爆款标题】公众号排版太麻烦？3秒转换 Markdown，告别手动调整！

你是不是写完公众号文章，还要一点点调整格式？加粗要换成【】，列表要改圆点，代码块要标记...每次排版半小时？

本工具用 3 秒将 Markdown 直接转换成公众号粘贴格式，保留段落层次，智能转换加粗/列表/代码块，复制即发布！

✨ **核心亮点**：
- 一键转换：Markdown → 公众号粘贴格式
- 智能映射：`**加粗**` → `【加粗】`，`*斜体*` → 去掉星号
- 保留结构：标题、列表、代码块全部识别
- 直接可用：输出纯文本，Ctrl+C 就发布

📁 **典型场景**：
- 公众号运营：快速发布技术文章
- 内容创作者：Markdown 写作族福音
- 技术博客：代码块自动标记

🎯 **为什么选我**：
✅ 专注公众号，format 最精准
✅ 零学习成本，命令行即用
✅ 保持段落，阅读体验好

👉 立即体验：`clawhub install wechat-formatter`
---

# 微信公众号格式化工具

## Features
- 去除 Markdown 语法，保留段落结构
- `**加粗**` → `【加粗】`
- `*斜体*` → `斜体`（去掉星号）
- 标题转换为缩进段落
- 列表转换为带圆点格式
- 代码块标记为 `【代码块】`
- 纯文本输出，可直接复制到公众号

## Installation

已安装到 `~/.openclaw/skills/wechat-formatter/`

## Usage

### 格式化文件
```bash
wechat-formatter article.md
```

### 通过管道
```bash
cat article.md | wechat-formatter --stdin
```

### 结合第五篇日记
```bash
wechat-formatter ~/.openclaw/workspace/memory/2026-03-09-day2.md | pbcopy
```

## Example

**Input** (`test.md`):
```markdown
# 标题

这是**加粗**和*斜体*。

- 列表1
- 列表2
```

**Output**:
```
标题

这是【加粗】和斜体。

• 列表1
• 列表2
```

## 为什么需要这个？

公众号编辑器不支持 Markdown 语法，直接粘贴会丢失格式。这个工具帮你转换成**纯文本但保留排版层次**的格式，粘贴后不需要再调整。

## Integration

也可以在其他技能中调用：
```python
from wechat_formatter import format_for_wechat
formatted = format_for_wechat(markdown_content)
```

## License

MIT