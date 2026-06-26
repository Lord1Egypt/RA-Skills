# 配色方案（bslib bs_theme）

用 **bslib** 的 `bs_theme()` 统一 dashboard 配色（Bootstrap 5）。5 套按教学语境设计，每套给：`bs_theme()` 代码 + 配套图表调色板 + 适用场景。选定一套，把 `theme <- bs_theme(...)` 放进 `app.R` 顶部，传给 `page_navbar(theme = theme)` / `page_sidebar(theme = theme)`。

## 三个关键约定（先读）

1. **字体走系统栈，不用 `font_google()`**。`font_google()` 从 Google Fonts 下载，国内常被墙/超时拖慢启动。教学场景直接用系统中文字体栈即可（下面每套都已设好）。
2. **图表配色用 `thematic` 自动同步**。在 `server` 里或 app 顶部调一次 `thematic::thematic_shiny()`，base R / ggplot2 图的背景、前景、默认色会**自动跟随当前 bslib 主题**，不用手调。分类数据系列的颜色另用下面的 `palette` 向量。
3. **plot 里的中文要额外处理**（否则是方框）——见 `setup-and-run.md` 的 showtext 一节。UI 里的中文（标题、文字、按钮）没问题，是浏览器渲染的。

```r
# 通用：app.R 顶部
library(shiny); library(bslib)
thematic::thematic_shiny(font = "auto")   # 图表自动跟随主题配色
```

---

## 1. 学院蓝 Academic Blue（亮）

**适合**：理工、社科、经管、常规大学课堂。沉稳可信，投影清晰，最百搭。

```r
theme <- bs_theme(
  version = 5,
  bg = "#ffffff", fg = "#1f2933",
  primary = "#1f4e79", secondary = "#5b7a99",
  success = "#15803d", info = "#0e7490", warning = "#b45309", danger = "#b91c1c",
  base_font = c("system-ui", "-apple-system", "Segoe UI", "PingFang SC", "Microsoft YaHei", "sans-serif"),
  heading_font = c("Georgia", "Songti SC", "STSong", "serif")
)
palette <- c("#1f4e79", "#0e7490", "#b45309", "#6b8e6b", "#8d6e97", "#c2410c")
```

## 2. 暖阳人文 Warm Humanities（亮）

**适合**：历史、文学、语言、艺术、哲学。暖纸感 + 赤陶色，温润，适合大段文字阅读型讲解。

```r
theme <- bs_theme(
  version = 5,
  bg = "#fdf8f0", fg = "#382c22",
  primary = "#9a3412", secondary = "#a8794f",
  success = "#4d7c0f", info = "#0e7490", warning = "#ca8a04", danger = "#9f1239",
  base_font = c("system-ui", "PingFang SC", "Microsoft YaHei", "sans-serif"),
  heading_font = c("Georgia", "Songti SC", "STKaiti", "serif")
)
palette <- c("#9a3412", "#ca8a04", "#4d7c0f", "#0e7490", "#7c4a2d", "#9f1239")
```

## 3. 清新理科 Fresh Science（亮）

**适合**：生物、医学、化学、自然科学、面向中小学/低年级。teal 主色干净友好。

```r
theme <- bs_theme(
  version = 5,
  bg = "#f7fcfa", fg = "#15302b",
  primary = "#0d9488", secondary = "#577590",
  success = "#16a34a", info = "#0891b2", warning = "#f59e0b", danger = "#e11d48",
  base_font = c("system-ui", "-apple-system", "PingFang SC", "Microsoft YaHei", "sans-serif")
)
palette <- c("#0d9488", "#34a0a4", "#76c893", "#f59e0b", "#ef767a", "#577590")
```

## 4. 暗夜讲堂 Dark Lecture（暗）

**适合**：计算机、数据科学、晚间课、暗光教室。暗底减少投影炫光，代码/终端演示尤其舒服。

```r
theme <- bs_theme(
  version = 5,
  bg = "#0f172a", fg = "#e2e8f0",
  primary = "#60a5fa", secondary = "#94a3b8",
  success = "#34d399", info = "#22d3ee", warning = "#fbbf24", danger = "#f87171",
  base_font = c("system-ui", "PingFang SC", "Microsoft YaHei", "sans-serif"),
  code_font = c("SF Mono", "JetBrains Mono", "Consolas", "monospace")
)
palette <- c("#60a5fa", "#22d3ee", "#a78bfa", "#fbbf24", "#f472b6", "#34d399")
```
> 暗色主题下 `thematic_shiny()` 会把图也变暗底，和 dashboard 融为一体。

## 5. 高对比投影 High-Contrast Projection（亮）

**适合**：**老旧投影仪 / 大教室后排看不清 / 强光环境**——这是最"替代幻灯片"的一套：纯白底、近黑字、高饱和主色、配合 `setup-and-run.md` 里的放大字号。元素要少而大。

```r
theme <- bs_theme(
  version = 5,
  bg = "#ffffff", fg = "#0a0a0a",
  primary = "#0033cc", secondary = "#444444",
  success = "#067647", info = "#005f73", warning = "#b45309", danger = "#cc0000",
  base_font = c("system-ui", "-apple-system", "PingFang SC", "Microsoft YaHei", "sans-serif"),
  "font-size-base" = "1.15rem",     # 整体字号上调，后排能看清
  "headings-font-weight" = "700"
)
palette <- c("#0033cc", "#cc0000", "#067647", "#b45309", "#6a0dad", "#005f73")
```
> `bs_theme()` 里用字符串键（如 `"font-size-base"`）可直接覆盖 Bootstrap 的 Sass 变量，无需写 CSS。

---

## 让图表用上 palette

`thematic` 管背景/前景/默认单色；**多分类数据系列**的配色用上面的 `palette`：

```r
# ggplot2
ggplot(df, aes(x, y, color = grp)) + geom_line(linewidth = 1.2) +
  scale_color_manual(values = palette) + theme_minimal(base_size = 15)

# plotly：用 colorway 设整张图的分类色序
plot_ly(df, x = ~x, y = ~y, color = ~grp, colors = palette, type = "scatter", mode = "lines") |>
  layout(colorway = palette)

# DT 表格：跟随主题，无需额外配色
```

## 配深浅切换（可选）

bslib 支持运行时切换：UI 里放 `input_dark_mode()`（bslib ≥ 0.6），或给两套 theme 用 `bs_theme_update()`。课堂演示一般选定一套即可，不必都做。

## 用内置 bootswatch 主题（更省事的备选）

不想调色值时，`bs_theme(version = 5, bootswatch = "flatly")` 一行套用现成主题。教学友好的几个：`flatly`(清爽蓝绿)、`cosmo`(明快)、`lumen`(柔和)、`journal`(暖红)、`minty`(薄荷)、`darkly`/`solar`/`superhero`(暗)。套 bootswatch 后仍可叠加 `primary =` 等微调。
