# HTML 引擎结构规范（html-template.md）

> 仅 HTML 引擎时读本文件。目标：agent 手写单文件 HTML 知识卡，
> 文字 100% 准确、排版完全可控，最后截图出 PNG。
> 生成前必读：`html-base.css`（全文内联）+ 该卡的「禁止出现」段 + `gotchas.md`。

---

## 硬性规则

1. **单文件自包含**：全部 CSS 内联在 `<style>`；无 JS 依赖（静态卡不需要 JS）；无外部图片（装饰用 CSS 形状/emoji/Unicode 符号，确需图片必须 base64）
2. **必带底座**：`html-base.css` 全文复制进 `<style>` 最顶部，通过 CSS 变量覆盖底色和画布尺寸
3. **只用 Google Fonts**：中文 `Noto Sans SC`（正文/标题）、`ZCOOL KuaiLe`（手绘感）、`ZCOOL QingKe HuangYou`（像素/复古感）；英文可用 `Space Grotesk`、`JetBrains Mono` 等。禁止系统字体作 display 字体
4. **固定画布**：按卡的画幅设 `--card-width/--card-height`（3:4 → 1170x1560；4:3 → 1560x1170；16:9 → 1920x1080），`overflow:hidden`
5. **注释是善意**：每个区块用 `/* === 区块名 === */` 注释，槽位填的是卡里哪一段要可追溯
6. **内容来自卡**：布局严格按卡的第 4 段构图线框，配色严格按第 3 段色板，文字严格按第 7 段槽位——卡是唯一事实源

## HTML 骨架

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@400;700;900&family=ZCOOL+QingKe+HuangYou&display=swap" rel="stylesheet">
<style>
/* html-base.css 全文（复制进来） */
/* === 卡片覆盖变量 === */
:root { --bg-page: #F5EFE0; --card-width: 1170px; --card-height: 1560px; }
/* === 区块1：标题带 === */
/* === 区块2：... === */
</style>
</head>
<body>
<div class="card">
  <!-- 按卡的构图线框逐区块实现 -->
</div>
</body>
</html>
```

## 动画模式（html-anim 引擎附加规则）

- **统一时间轴**：整轮动画定义一个总时长（如 10s），所有 `@keyframes` 用同一
  时长 + 不同百分比区间编排，禁止各元素各自循环——否则永远无法同步
- **四种标准动效**（按卡）：token 沿路径移动（`offset-path` 或分段 translate）、
  当前节点描边高亮（border-color + box-shadow）、步骤文字切换（opacity 渐变）、
  卡片渐次浮现（opacity + translateY 小位移）
- **节奏**：每步 1.5-2s，整轮 8-12s，`animation-iteration-count: infinite`
- **导出**：交付自循环 HTML；GIF 用录屏或 Playwright 多帧截图 + ffmpeg 合成

## 反 AI Slop 清单（同 frontend-slides 精神）

- ❌ 禁 `Inter`/`Roboto`/系统默认字体作标题
- ❌ 禁白底紫渐变、无意义毛玻璃、无目的阴影
- ❌ 禁"全部居中"的模板脸——按卡的布局线框来
- ❌ 禁 emoji 当全部插画（≤3 个点缀可以，成片用 = 偷懒）

## 导出 PNG

```bash
bash scripts/export-png.sh card.html card.png          # 默认按 html 的画布尺寸
bash scripts/export-png.sh card.html card.png 1170 1560 # 手动指定宽高
```

脚本用 Playwright 无头截图，首次运行会自动装 Chromium（约 150MB，告知用户等 30-60 秒）。

## 自检清单（交付前逐项过）

- [ ] Google Fonts 加载成功（截图前浏览器需联网）
- [ ] 文字无溢出画布、无截断（中文卡片重点查最后一行）
- [ ] 配色与卡的色板 hex 一致
- [ ] 槽位内容与用户文本逐字一致（不许 AI 改写）
- [ ] 「禁止出现」段逐条过关
