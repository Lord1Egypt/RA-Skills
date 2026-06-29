# HTML 生成规范

## ⛔ class 白名单（强制）

**生成 HTML 时，只能使用以下 class，禁止自行发明任何 class 名。**

### pptx-model 白名单

```
slide is-active skip
deck tpl-pptx-model
ts-stripe ts-stripe-b ts-chrome ts-alert-tag ts-page
ts-h1 ts-h2 ts-kicker ts-sub
ts-alert-box ts-card ts-grid-2 ts-grid-3 ts-grid-4
ts-codebox ts-checklist ts-check ts-footer
strike red ts-highlight-red
amber green ok
```

### pdf-model 白名单

```
slide is-active skip
deck tpl-pdf-model
page-dot sticker hand-box bottom-bar cover-title
num-circle tag-row ht stack avatar big-emoji
lede h1 h2 h3
pink yellow blue green
```

### ⛔ 禁止项

- 禁止使用另一格式的 class（如 pptx-model HTML 中不得出现 `.hand-box` `.sticker` 等）
- 禁止自行发明任何不在上述白名单中的 class
- 禁止在 HTML 中硬编码 deck/slide 尺寸
- 禁止引错格式的 style.css（pdf-model 不能用 pptx-model.css）
- 禁止不加 `runtime.js`——所有格式都需要它来驱动浏览器端 slide 翻页

---

不照搬 `templates/full-decks/` 中的参考模板页数，根据分析结果（5 个独立文件 `{原始文档stem}_4.N_*.md`）自行决定页数。

## 核心原则：视觉系统 = CSS 文件 + 组件 class，缺一不可

`templates/full-decks/<format>/` 中的 `style.css` 不只是配色皮肤——它定义了一整套专属**组件 class**。换 CSS 文件但不用对应的组件 class，等于只换了颜色却没换视觉语言，效果不生效。

## 两种输出格式

| | pdf-model | pptx-model |
|---|---|---|
| body class | `class="tpl-pdf-model"` | `class="tpl-pptx-model"` |
| 引用 | `assets/pdf-model.css` | `assets/pptx-model.css` |
| 组件体系 | `.hand-box` `.sticker` `.page-dot` `.bottom-bar` `.cover-title` `.big-emoji` `.num-circle` `.tag-row` `.ht` `.stack` `.avatar` `.lede` `.h1` `.h2` `.h3` | `.ts-stripe` `.ts-chrome` `.ts-alert-tag` `.ts-page` `.ts-kicker` `.ts-h1` `.ts-sub` `.ts-alert-box` `.ts-footer` `.strike` `.red` |
| 配色变量 | `--bg:#fef7f3` `--accent:#ff6b8b` 等 | `--ts-bg:#fffaf7` `--ts-red:#e0314a` 等 |
| runtime.js | ✅ | ✅ |
| 尺寸 | 由转换脚本 `@page{size:810px 1080px}` 处理 | 16:9（1920×1080截图，无CSS布局依赖） |

## Deck 骨架

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>...</title>
  <link rel="stylesheet" href="assets/fonts.css">
  <link rel="stylesheet" href="assets/base.css">
  <link rel="stylesheet" href="assets/pdf-model.css">   <!-- 或 pptx-model.css -->
  <style>/* 可选：补充 style.css 未提供的样式（如表格） */</style>
</head>
<body class="tpl-pdf-model">   <!-- 或 tpl-pptx-model -->
<div class="deck">
  <!-- slides 在此 -->
</div>
<script src="assets/runtime.js"></script>
</body></html>
```

注意：`base.css` 必须保留——它提供 `tpl-pdf-model` / `tpl-pptx-model` 的基础（`.deck` `.slide` 定义），由格式专属 `style.css` 覆写配色和尺寸。

## Slide 组装规则（pdf-model）

1. 参考模板 `templates/full-decks/pdf-model/index.html`，按内容需求组合以下组件：

| 组件 | class | 用途 |
|------|-------|------|
| 页码贴纸 | `.page-dot` | 右上角 `N / 11` 页码 |
| 旋转便签 | `.sticker` `.sticker.pink\|yellow\|blue\|green` | 关键词/标签装饰 |
| 手帐卡片 | `.hand-box` | 主内容容器，厚边框+圆角阴影 |
| 底栏 | `.bottom-bar` | 页脚（作者/页码信息） |
| 渐变标题 | `.cover-title` | 封面/标题下划线高亮 |
| 编号圆圈 | `.num-circle` | 步骤/序号圆标 |
| 话题标签 | `.tag-row` + `.ht` | 话题 tag 行 |
| 竖排堆叠 | `.stack` | 多个 `.hand-box` 纵向排列 |
| 大图标 | `.big-emoji` | 超大居中 emoji/图标 |
| 头像圆 | `.avatar` | 小型圆形头像装饰 |

2. 第一个 slide 加 `is-active` class，其余不加
3. 禁止自写 CSS class —— 只能使用上表中的组件 class
4. 如内容需要表格，在内联 `<style>` 中补充 `.tbl` 样式（保持最小化，不覆盖模板变量）
5. 排版、动效相关属性（`data-anim`、`anim-stagger-list` 等）可以移除

## Slide 组装规则（pptx-model）

1. **每页必须的骨架**（参考 `templates/full-decks/pptx-model/index.html`）：

```html
<section class="slide">
  <div class="ts-stripe"></div>                               <!-- 顶部红黑斜条纹警示带 -->
  <div class="ts-chrome">
    <span class="ts-alert-tag">标签</span>                     <!-- 可加 amber green -->
    <span class="ts-page">01 / 12</span>
  </div>
  <!-- 页面内容在此 -->
  <div class="ts-stripe-b"></div>                             <!-- 底部副条纹 -->
  <div class="ts-footer"><span>页脚信息</span><span>01 / 12</span></div>
</section>
```

2. 组件表：

| 组件 | class | 用途 |
|------|-------|------|
| 顶部警示带 | `.ts-stripe` | 45° 红黑斜条纹，每页顶部 |
| 底部副条纹 | `.ts-stripe-b` | 窄版副条纹，每页底部 |
| 顶部 chrome 栏 | `.ts-chrome` | 包裹标签+页码的横栏 |
| 标签 pill | `.ts-alert-tag`（可加 `amber` `green`） | 页面分类标签 |
| 页码 | `.ts-page` | 右上角 `N / N` 页码 |
| 标题 | `.ts-h1` `.ts-h2` | 主标题/副标题 |
| kicker | `.ts-kicker` | 标题上方的引导语 |
| 副文本 | `.ts-sub` | 标题下方的描述段落 |
| 警示框 | `.ts-alert-box`（可加 `amber` `green`） | 突出警告/提示内容 |
| 卡片 | `.ts-card` | 带彩色顶边的内容卡 |
| 三栏 grid | `.ts-grid-3` | 三个 `.ts-card` 并排 |
| 代码块 | `.ts-codebox` | policy-as-code YAML 块 |
| 清单 | `.ts-checklist` → `.ts-check` `.ok` | 红/绿复选框清单 |
| 底栏 | `.ts-footer` | 页脚信息+页码 |
| 删除线 | `.strike` | 红色斜切删除线 |
| 红色高亮 | `.red` | 红色强调文字 |
| 红色标记 | `.ts-highlight-red` | 红色背景标记 |

3. 第一个 slide 加 `is-active` class，其余不加
4. 禁止自写 CSS class —— 只能用上表中的组件 class
5. 转换方式：`convert_pptx_model.py` 使用**逐页截图法**（1920×1080→PIL→python-pptx），不依赖 CSS 布局修复，不存在 pdf-model 同类正则匹配 bug
6. 必须包含 `<script src="assets/runtime.js">`

## 颜色变量

颜色使用 CSS 变量，由对应 `pdf-model.css` / `pptx-model.css` 提供：

| 变量 | 含义 | 用途 |
|------|------|------|
| `var(--bad)` | 红灯 | 禁止/强制条款（如 `.red` `.strike` `.ts-highlight-red`） |
| `var(--warn)` | 黄灯 | 建议/鼓励条款 |
| `var(--good)` | 绿灯 | 灵活选择条款 |
| `var(--accent)` | 强调色 | 装饰性高亮 |
