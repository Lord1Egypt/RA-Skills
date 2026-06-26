---
name: web-front
description: |
  网站前端生成技能。根据用户需求生成HTML/CSS/JS前端页面，
  自动保存到指定目录并在浏览器中打开预览。
  学习主流网站的设计并记录在学习资源目录中。
metadata: {"clawdbot":{"emoji":"🌐","priority":50}}
---

# 网站前端生成

根据用户描述生成前端网页，自动保存并在浏览器中预览。

## 输出目录

所有生成的网页文件保存在：
```
{baseDir}/html/
```

## 使用流程

### 步骤 1：理解需求

分析用户想要什么样的网页：
- 页面类型（落地页、表单、展示页、游戏等）
- 风格要求（简约、炫酷、商务、可爱等）
- 功能需求（动画、交互、响应式等）

### 步骤 2：生成文件

根据需求生成以下文件：

```
html/
├── {项目名}/
│   ├── index.html      # 主页面
│   ├── style.css       # 样式文件（可选）
│   └── script.js       # 脚本文件（可选）
```

**命名规则**：
- 项目名使用英文小写 + 连字符，如 `my-landing-page`
- 单页面可直接命名为 `index.html`

### 步骤 3：保存文件

使用 Write 工具将生成的代码保存到对应目录：

```
{baseDir}/html/{项目名}/index.html
{baseDir}/html/{项目名}/style.css
{baseDir}/html/{项目名}/script.js
```

### 步骤 4：打开浏览器预览

生成完成后，使用系统命令在浏览器中打开：

**Windows**：
```bash
start "" "{baseDir}/html/{项目名}/index.html"
```

**macOS**：
```bash
open "{baseDir}/html/{项目名}/index.html"
```

**Linux**：
```bash
xdg-open "{baseDir}/html/{项目名}/index.html"
```

## 学习机制

为了提升生成质量，本技能会主动学习主流前端平台的优秀设计。

### 学习资源目录

学习资料保存在 `{baseDir}/learning/` 目录：

```
learning/
├── design-patterns.md    # 设计模式与布局技巧
├── color-schemes.md      # 配色方案
├── animations.md         # 动画效果库
├── components.md         # 常用组件模板
├── typography.md         # 字体排版规范
└── inspirations.md       # 优秀案例收集
```

每个文件都包含该领域的核心知识和最佳实践，生成网页时会自动读取并应用。

### 学习流程

当用户请求生成网页时：

1. **读取学习资料**：先读取 `learning/` 目录下的相关学习文件
2. **分析需求匹配**：根据用户需求匹配对应的设计模式和组件
3. **应用最佳实践**：将学到的技巧应用到生成的代码中
4. **持续改进**：每次生成后总结经验，更新学习资料

### 主流学习平台

生成代码时参考以下平台的优秀实践：

| 平台 | 网址 | 学习重点 |
|------|------|----------|
| Dribbble | https://dribbble.com | UI设计灵感、配色方案 |
| Awwwards | https://www.awwwards.com | 创意交互、动效设计 |
| CodePen | https://codepen.io | 前端代码实现、组件模板 |
| CSS-Tricks | https://css-tricks.com | CSS技巧、布局方案 |
| Tailwind UI | https://tailwindui.com | 组件设计、响应式模式 |
| Stripe | https://stripe.com | 现代商务风格 |
| Apple | https://apple.com | 极简设计、动效细节 |
| Vercel | https://vercel.com | 技术产品落地页 |

### 学习触发条件

以下情况会主动学习并更新资料：

- 用户要求"参考 xxx 风格"
- 用户对生成结果不满意
- 用户要求"做得更好看"
- 遇到新的设计趋势

### 学习资料内容要求

每个学习文件应包含：

**design-patterns.md** - 设计模式
- 常见的布局模式（Z-pattern、F-pattern、Golden pattern）
- 导航设计模式
- 卡片设计模式
- 响应式 breakpoints

**color-schemes.md** - 配色方案
- 主色、辅助色、中性色定义
- 渐变色使用规范
- 深色模式配色
- 色彩心理学应用

**animations.md** - 动画效果
- 过渡效果时长（200-500ms）
- 缓动函数选择
- 微交互设计
- 滚动动画

**components.md** - 组件模板
- 按钮的各种状态
- 卡片组件
- 表单组件
- 导航栏
- Hero 区域

**typography.md** - 字体排版
- 字体大小比例（1.25/1.333）
- 行高规范
- 字重选择
- 中英文混排

**inspirations.md** - 优秀案例
- 收集的灵感链接
- 设计亮点分析
- 可复用的设计思路

### 质量检查清单

每次生成网页后自检：

- [ ] 布局：是否符合常见设计模式
- [ ] 配色：是否符合配色规范
- [ ] 字体：是否有层次感
- [ ] 间距：是否保持一致
- [ ] 动画：是否流畅自然
- [ ] 响应式：是否适配各种屏幕
- [ ] 可访问性：颜色对比度是否足够

## 代码规范

### HTML

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>页面标题</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <!-- 页面内容 -->
    <script src="script.js"></script>
</body>
</html>
```

### CSS

- 使用现代 CSS 特性（Flexbox、Grid、CSS Variables）
- 支持响应式设计
- 添加必要的动画效果
- 遵循 BEM 或其他命名规范
- 使用 CSS 变量管理主题色

### JavaScript

- 使用 ES6+ 语法
- 代码简洁清晰
- 添加必要的事件处理
- 使用 IntersectionObserver 实现滚动动画
- 使用 requestAnimationFrame 优化动画性能

## 示例

### 用户请求

> 帮我生成一个个人介绍页面，简约风格，包含头像、名字、简介和社交链接

### 生成结果

```
html/
└── personal-intro/
    ├── index.html
    ├── style.css
    └── avatar.svg
```

### 自动打开

生成完成后自动在默认浏览器中打开 `index.html`。

## 常见页面类型

| 类型 | 说明 | 特点 |
|------|------|------|
| 落地页 | 产品/服务介绍 | 突出CTA、视觉冲击 |
| 个人主页 | 个人介绍展示 | 头像、简介、链接 |
| 表单页 | 数据收集 | 表单验证、提交 |
| 展示页 | 作品/项目展示 | 图片画廊、卡片布局 |
| 登录页 | 用户认证 | 表单、社交登录 |
| 游戏页 | 小游戏 | Canvas、交互逻辑 |

## 注意事项

1. **单文件优先**：简单页面尽量合并到单个 HTML 文件中（内联 CSS/JS）
2. **资源路径**：使用相对路径，确保本地打开时资源正常加载
3. **编码格式**：统一使用 UTF-8 编码
4. **移动适配**：添加 viewport meta 标签，支持移动端浏览
5. **浏览器兼容**：避免使用过于前沿的特性，确保主流浏览器兼容

## 快速模板

### 单文件模板

适用于简单页面，所有代码在一个 HTML 文件中：

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{标题}</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: system-ui, sans-serif; }
        /* 样式代码 */
    </style>
</head>
<body>
    <!-- 页面内容 -->
    <script>
        // 脚本代码
    </script>
</body>
</html>
```

## 网站管理

### 列出所有网站

当用户说"列出所有网站"、"有哪些网站"、"查看网站列表"时：

1. 扫描 `{baseDir}/html/` 目录
2. 列出所有子目录（每个子目录代表一个网站项目）
3. 显示每个项目的基本信息

**示例输出**：
```
📁 已生成的网站列表：

1. personal-intro
   📄 文件：index.html, style.css
   📅 创建：2026-03-20

2. todo-app
   📄 文件：index.html, style.css, script.js
   📅 创建：2026-03-19

3. game-snake
   📄 文件：index.html
   📅 创建：2026-03-18

共 3 个网站项目
```

### 打开网站

当用户说"打开 xxx 网站"、"预览 xxx"时：

1. 在 `{baseDir}/html/` 中查找对应项目
2. 使用系统命令在浏览器中打开

**命令**：
```bash
# Windows
start "" "{baseDir}/html/{项目名}/index.html"

# macOS
open "{baseDir}/html/{项目名}/index.html"

# Linux
xdg-open "{baseDir}/html/{项目名}/index.html"
```

### 修改网站

当用户说"修改 xxx 网站"、"更新 xxx 页面"时：

1. 先读取现有文件内容
2. 根据用户需求修改代码
3. 保存更新后的文件
4. 可选择自动刷新浏览器预览

**修改流程**：
```
用户请求修改 → 读取现有文件 → 理解修改需求 → 更新代码 → 保存 → 预览
```

### 删除网站

当用户说"删除 xxx 网站"、"移除 xxx 项目"时：

1. 确认删除操作（避免误删）
2. 删除整个项目目录

**删除命令**：
```bash
# 删除整个项目目录
rm -rf "{baseDir}/html/{项目名}"
```

**安全确认**：
```
⚠️ 确认删除

项目名称：{项目名}
项目路径：{baseDir}/html/{项目名}/
包含文件：index.html, style.css, ...

确定要删除吗？此操作不可恢复。
```

### 重命名网站

当用户说"重命名 xxx 为 yyy"时：

1. 检查新名称是否已存在
2. 重命名项目目录

**命令**：
```bash
mv "{baseDir}/html/{旧名称}" "{baseDir}/html/{新名称}"
```

## 管理命令速查

| 用户说 | 操作 |
|--------|------|
| "列出所有网站" | 扫描并显示 html/ 目录下的所有项目 |
| "打开 xxx" | 在浏览器中打开指定网站 |
| "修改 xxx" | 读取并更新指定网站的代码 |
| "删除 xxx" | 删除指定网站项目 |
| "重命名 xxx 为 yyy" | 重命名项目目录 |
| "查看 xxx 代码" | 显示指定网站的源代码 |

## 目录结构

```
web_front/
├── SKILL.md           # 技能说明文档
└── html/              # 生成的网页存放目录
    ├── project-a/
    │   └── index.html
    ├── project-b/
    │   ├── index.html
    │   ├── style.css
    │   └── script.js
    └── ...
```
