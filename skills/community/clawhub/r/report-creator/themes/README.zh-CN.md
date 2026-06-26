# 自定义主题

在这个目录下放置文件夹，即可为 kai-report-creator 添加自己的主题。

## 目录结构

```
themes/
  your-theme-name/
    reference.md   ← 风格描述文件（AI 读取后生成 CSS 变量）
    theme.css      ← 直接定义 CSS（可选，优先级高于 reference.md）
```

两种文件可以单独使用，也可以同时存在：

| 情况 | 行为 |
|------|------|
| 只有 `reference.md` | AI 读取风格描述，推导并生成 `:root` CSS 变量 |
| 只有 `theme.css` | 直接使用该文件中的 CSS 变量，完全可预期 |
| 两者都有 | `theme.css` 优先；`reference.md` 作为风格说明供参考 |

## 调用方式

```bash
/report --theme your-theme-name "报告主题"
```

或在 `.report.md` 的 frontmatter 中指定：

```yaml
theme: your-theme-name
```

## reference.md 格式

```markdown
# 主题名称 — 风格参考

一句话描述。灵感来源 / 美学风格 / 氛围。

---

## Colors

​```css
:root {
  --primary:      #...;   /* 主色，用于标题下划线、链接、强调 */
  --bg:           #...;   /* 页面背景 */
  --surface:      #...;   /* 卡片背景 */
  --text:         #...;   /* 正文 */
  --text-muted:   #...;   /* 次要文字 */
  --border:       #...;   /* 边框/分割线 */
}
​```

## Typography

字体选择说明。衬线 or 无衬线？几何 or 人文？推荐 Google Fonts 链接。

## Layout

留白风格、卡片圆角、最大宽度等布局偏好。

## Best For

适用场景：品牌报告、研究文档、内部周报……
```

## theme.css 格式

直接定义 `:root` CSS 变量，覆盖内置主题的默认值。

```css
:root {
  --primary:      #C2410C;  /* 主色 */
  --primary-light:#FFF7ED;  /* 主色浅色背景 */
  --accent:       #EA580C;  /* 强调色 */
  --bg:           #FFFBF7;  /* 页面背景 */
  --surface:      #FFFFFF;  /* 卡片背景 */
  --text:         #1C1917;  /* 正文 */
  --text-muted:   #78716C;  /* 次要文字 */
  --border:       #E7E5E4;  /* 边框 */
  --font-sans:    'Inter', system-ui, sans-serif;
  --font-mono:    'JetBrains Mono', monospace;
  --radius:       6px;
}
```

可用变量参考内置主题 `templates/themes/corporate-blue.css`。

## 注意事项

- 以 `_` 开头的目录（如 `_example-warm-editorial`）会被自动忽略，不会出现在主题列表中
- 主题名只支持字母、数字和连字符，例如 `my-brand`、`warm-editorial`
- 自定义主题与内置主题同等优先级，同名时自定义主题优先

## 分享主题

将主题文件夹发布为 git 仓库，其他人 clone 进自己的 `themes/` 目录即可使用：

```bash
git clone https://github.com/yourname/report-theme-mybrand \
  ~/.claude/skills/report-creator/themes/mybrand
```
