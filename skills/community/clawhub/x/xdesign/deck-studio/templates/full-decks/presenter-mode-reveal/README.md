---
name: 演讲者模式模板 · Presenter Mode Reveal 🎤
mode: deck
scenario: general
surface: slides
recommended: 50
tags: ["presentation", "speaker", "presenter", "notes"]
example_id: sample-presenter-mode-reveal
example_format: markdown
---
# 演讲者模式模板 · Presenter Mode Reveal 🎤

**专门为带逐字稿的技术分享/演讲设计的 deck 模板。**

- 6 页示例 deck，每页含完整 150-300 字逐字稿 (`<aside class="notes">`)
- 按 **S** 进入演讲者视图（4 磁力卡片：当前页/下一页/逐字稿/计时器）
- 5 种默认主题 (tokyo-night/dracula/catppuccin-mocha/nord/corporate-clean)

**样式范围**：`tpl-presenter-mode-reveal`

### 使用方式
```bash
cp -r templates/full-decks/presenter-mode-reveal examples/my-talk
# 替换内容 + 每页的 <aside class="notes"> 逐字稿
open examples/my-talk/index.html
# 按 S 进入演讲者模式
```
