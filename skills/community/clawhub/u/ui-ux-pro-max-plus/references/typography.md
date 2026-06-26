# 字体配对指南 - 精选字体组合

专业设计师推荐的字体搭配，包含 Google Fonts 链接和 Tailwind CSS 配置。

---

## 🎯 现代无衬线组合

### Inter + Inter（单一字体家族）
```css
/* 最简单、最安全的选择 */
font-family: 'Inter', sans-serif;

/* 字重使用 */
font-thin:       100
font-extralight: 200
font-light:      300
font-normal:     400
font-medium:     500
font-semibold:   600
font-bold:       700
font-extrabold:  800
font-black:      900

/* 使用建议 */
标题: font-bold text-4xl tracking-tight
正文: font-normal text-base leading-relaxed
```
**适用：** 科技产品、SaaS、数据仪表盘
**Google Fonts：** `https://fonts.googleapis.com/css2?family=Inter:wght@100..900&display=swap`

---

### Inter + JetBrains Mono（科技风）
```css
/* 标题 */
font-heading: 'Inter', sans-serif;
font-bold text-3xl tracking-tight;

/* 正文 */
font-body: 'Inter', sans-serif;
font-normal text-base leading-7;

/* 代码/数据 */
font-mono: 'JetBrains Mono', monospace;
font-mono text-sm;
```
**适用：** 开发者工具、技术文档、代码编辑器
**Google Fonts：**
- Inter: `family=Inter:wght@400;500;600;700`
- JetBrains Mono: `family=JetBrains+Mono:wght@400;500`

---

### Plus Jakarta Sans + Plus Jakarta Sans（几何现代）
```css
font-family: 'Plus Jakarta Sans', sans-serif;

/* 特点：几何感强，比 Inter 更有性格 */
标题: font-extrabold text-4xl
正文: font-normal text-base
```
**适用：** 创业公司、现代品牌、创意机构

---

## 📚 衬线+无衬线经典组合

### Playfair Display + Inter（编辑/杂志）
```css
/* 标题 - 优雅衬线 */
font-heading: 'Playfair Display', serif;
font-bold text-5xl leading-tight;

/* 正文 - 清晰无衬线 */
font-body: 'Inter', sans-serif;
font-normal text-lg leading-8;

/* 副标题 */
font-subheading: 'Playfair Display', serif;
font-medium text-2xl italic;
```
**适用：** 博客、杂志、时尚品牌、奢华产品
**特点：** 高端、优雅、有文化底蕴

---

### Cormorant Garamond + Open Sans（精致文艺）
```css
/* 标题 */
font-heading: 'Cormorant Garamond', serif;
font-semibold text-4xl;

/* 正文 */
font-body: 'Open Sans', sans-serif;
font-normal text-base leading-7;
```
**适用：** 文学网站、艺术画廊、婚礼策划

---

### Libre Baskerville + Source Sans Pro（经典阅读）
```css
/* 标题 */
font-heading: 'Libre Baskerville', serif;
font-bold text-3xl;

/* 正文 - 特别优化屏幕阅读 */
font-body: 'Source Sans Pro', sans-serif;
font-normal text-lg leading-8;
```
**适用：** 长文章、新闻网站、电子书

---

## 😊 友好亲和组合

### Nunito + Nunito（圆润可爱）
```css
font-family: 'Nunito', sans-serif;

/* 特点：圆角笔画，友好亲和 */
标题: font-extrabold text-4xl
正文: font-normal text-base
```
**适用：** 儿童应用、教育平台、生活方式

---

### Quicksand + Open Sans（现代友好）
```css
/* 标题 */
font-heading: 'Quicksand', sans-serif;
font-bold text-3xl;

/* 正文 */
font-body: 'Open Sans', sans-serif;
font-normal text-base;
```
**适用：** 健康应用、健身平台、个人品牌

---

### Fredoka + Varela Round（活泼有趣）
```css
/* 标题 - 非常有个性 */
font-heading: 'Fredoka', sans-serif;
font-semibold text-4xl;

/* 正文 */
font-body: 'Varela Round', sans-serif;
font-normal text-base;
```
**适用：** 游戏、儿童产品、娱乐应用

---

## 💼 企业专业组合

### Roboto + Roboto（Material Design 标准）
```css
font-family: 'Roboto', sans-serif;

/* Google 标准 */
标题: font-medium text-3xl
正文: font-normal text-base tracking-wide
```
**适用：** Android 应用、企业系统、工具类

---

### Work Sans + Work Sans（清晰专业）
```css
font-family: 'Work Sans', sans-serif;

/* 特点：优化的数字显示 */
标题: font-semibold text-4xl
正文: font-normal text-base
数据: font-medium text-sm tabular-nums
```
**适用：** 金融应用、数据密集产品

---

### IBM Plex Sans + IBM Plex Mono（企业技术）
```css
/* 标题 */
font-heading: 'IBM Plex Sans', sans-serif;
font-semibold text-3xl;

/* 正文 */
font-body: 'IBM Plex Sans', sans-serif;
font-normal text-base;

/* 代码 */
font-mono: 'IBM Plex Mono', monospace;
```
**适用：** 企业服务、技术文档、IBM 风格

---

## 🎨 创意独特组合

### Space Grotesk + Space Grotesk（几何现代）
```css
font-family: 'Space Grotesk', sans-serif;

/* 特点：几何感、略带复古未来感 */
标题: font-bold text-5xl tracking-tight
正文: font-normal text-lg
```
**适用：** 创意机构、设计作品集、科技品牌

---

### Clash Display + Inter（大胆现代）
```css
/* 标题 - 非常有冲击力 */
font-heading: 'Clash Display', sans-serif;
font-semibold text-6xl uppercase;

/* 正文 */
font-body: 'Inter', sans-serif;
font-normal text-base;
```
**适用：** 时尚品牌、海报、着陆页
**注意：** Clash Display 不在 Google Fonts，需从 Fontshare 获取

---

### Bebas Neue + Montserrat（海报风格）
```css
/* 标题 - 全大写、超粗 */
font-heading: 'Bebas Neue', sans-serif;
font-normal text-7xl uppercase tracking-wide;

/* 正文 */
font-body: 'Montserrat', sans-serif;
font-normal text-base;
```
**适用：** 着陆页、海报、大标题设计

---

## 🌏 中日韩字体组合

### Noto Sans SC + Noto Sans SC（中文标准）
```css
font-family: 'Noto Sans SC', sans-serif;

/* 思源黑体，最安全的跨平台选择 */
标题: font-bold text-3xl
正文: font-normal text-base leading-7
```
**适用：** 所有中文产品

---

### Noto Serif SC + Noto Sans SC（中文衬线）
```css
/* 标题 - 思源宋体 */
font-heading: 'Noto Serif SC', serif;
font-bold text-3xl;

/* 正文 - 思源黑体 */
font-body: 'Noto Sans SC', sans-serif;
font-normal text-base leading-8;
```
**适用：** 文化类、文学类中文网站

---

## 📏 字体大小系统

### 桌面端（标准）
```
Hero:     48-72px / font-bold / line-height: 1.1
H1:       36-48px / font-bold / line-height: 1.2
H2:       30-36px / font-semibold / line-height: 1.25
H3:       24-30px / font-semibold / line-height: 1.3
H4:       20-24px / font-medium / line-height: 1.4
Body:     16-18px / font-normal / line-height: 1.6-1.75
Small:    14px / font-normal / line-height: 1.5
Caption:  12px / font-normal / line-height: 1.5
```

### 移动端调整
```
Hero:     32-40px
H1:       28-32px
H2:       24-28px
H3:       20-24px
Body:     16px
```

---

## 🎯 按场景推荐

| 场景 | 标题字体 | 正文字体 |
|-----|---------|---------|
| **科技/SaaS** | Inter, Plus Jakarta Sans | Inter |
| **金融/企业** | Work Sans, IBM Plex Sans | Work Sans |
| **时尚/杂志** | Playfair Display | Inter |
| **博客/阅读** | Libre Baskerville | Source Sans Pro |
| **创意/设计** | Space Grotesk | Inter |
| **教育/儿童** | Nunito, Fredoka | Nunito |
| **工具/效率** | Inter, Roboto | Inter |
| **奢华/高端** | Cormorant Garamond | Open Sans |

---

## 💡 字体使用技巧

### 性能优化
```html
<!-- 只加载需要的字重 -->
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">

<!-- 使用 font-display: swap 防止 FOIT -->
<style>
  @font-face {
    font-family: 'Inter';
    font-display: swap;
    /* ... */
  }
</style>
```

### 回退字体栈
```css
/* 西文 */
font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;

/* 中文 */
font-family: 'Noto Sans SC', 'PingFang SC', 'Microsoft YaHei', sans-serif;

/* 等宽 */
font-family: 'JetBrains Mono', 'Fira Code', Consolas, Monaco, monospace;
```

### 排版细节
```css
/* 更好的文字渲染 */
body {
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-rendering: optimizeLegibility;
}

/* 数字等宽（表格用） */
.tabular-nums {
  font-variant-numeric: tabular-nums;
}

/* 小型大写字母（装饰用） */
.small-caps {
  font-variant-caps: small-caps;
}
```

---

**记住：** 字体是设计的声音。衬线=传统/优雅，无衬线=现代/简洁，圆体=友好/亲和。
