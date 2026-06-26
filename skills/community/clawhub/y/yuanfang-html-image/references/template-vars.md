# 模板变量系统

`cover.html` 是 token-only 结构，用 `{{TOKEN}}` 占位符。渲染引擎替换这些变量：

| 变量 | 来源 | 说明 |
|------|------|------|
| `{{TITLE}}` | content.title | 主标题 |
| `{{CONTENT}}` | content.body / content.content | 正文（自动 `<br>` 换行） |
| `{{SOURCE}}` | content.source |文章来源 |
| `{{POINTS_HTML}}` | content.points | 要点列表 (`<li>` 拼接) |
| `{{W}}` / `{{H}}` | 平台配置 | 输出图片宽高 |
| `{{BG}}` / `{{TEXT}}` | config.colors | 背景色 / 文字色 |
| `{{ACCENT}}` / `{{SECONDARY}}` | config.colors | 品牌色 / 次要色 |
| `{{FONT_TITLE}}` / `{{FONT_BODY}}` | config.fonts | 标题 / 正文字体栈 |
| `{{TITLE_SIZE_V/S/W/C}}` | config.layout | 不同宽高比下的标题字号 |
| `{{CONTENT_SIZE}}` | config.layout | 正文字号基准 |
| `{{BRAND}}` | content.brandImage | 品牌 logo `<img>` 标签（已生成） |
| `{{BADGE}}` | content.badge → config.badge | 徽章文字（如 "FEATURED"） |
| `{{SEAL}}` | config.seal → config.brand → content.seal | 印章文字 |
| `{{METRIC_1/2/3}}` | content.metric1/2/3 | 数据指标数值 |
| `{{METRIC_LABEL_1/2/3}}` | content.metricLabel1/2/3 | 数据指标标签 |

## 高级语法

### 1. `{{COLOR__Axx}}` 带透明度品牌色

`{{ACCENT__A08}}` → `rgba(79,70,229,0.031)`，其中 `xx` 是十六进制透明度（00-FF）。

渲染引擎在 `{{TOKEN}}` 简单替换之前预处理。

### 2. `{{SIZE__PRINT}}` 打印自动缩放

`calc({{CONTENT_SIZE__PRINT}} * 0.7)` 在 A4/A3 平台渲染时以 `calc(X * 2.5)` 输出，屏幕平台以 `calc(X * 1)` 输出。

确保小字（source/badge/brand）在打印时自动放大。

### 3. 配置优先级

- `{{BADGE}}` 优先取 `content.badge`，回退到 `config.badge`，再回退到字面量 `{{BADGE}}`
- `{{SEAL}}` 类似，多一个回退到 `config.brand` 的层级

## 设计原则（layout-types/cover.html）

所有模板遵循：

1. **3 级视觉层次**: 钩子（超大 2-3x）→ 上下文（50% 钩子大小）→ 品牌（最小）
2. **60-30-10 配色**: 60% 底色, 30% 次要色块, 10% 强调色
3. **每个模板有标志性视觉元素**: 色块分割、装饰图形、背景纹理
4. **响应式 CSS**: 一个 HTML 模板适配 5 种宽高比，布局自动调整
5. **零外部资源**: 所有装饰元素用纯 CSS 实现
6. **内容长度限制**: 标题 ≤ 30 字，正文 ≤ 100 字，每条要点 ≤ 20 字，超长会被 CSS line-clamp 截断
