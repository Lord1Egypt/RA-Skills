# ruitian-html - 瑞天 HTML 企业文档生成器

## 技能描述

生成专业、精美的企业级 HTML 文档，适用于项目交付报告、技术方案、内部交流材料等场景。

**设计特点：**
- 🎨 紫色渐变主题（`#667eea → #764ba2`）
- 📦 圆角卡片式布局（16px 圆角）
- ✨ Hover 上浮动画 + 阴影加深效果
- 📊 渐变蓝色表头表格
- 🔄 响应式流程图/架构图
- 📱 移动端友好（Bootstrap 5）
- 🖼️ 支持 Base64 嵌入图片（离线可用）

## 触发词

- 生成 HTML 文档
- 创建项目交付报告
- 制作技术方案 HTML
- 企业文档风格
- 瑞天风格 HTML
- 渐变紫色主题
- 项目汇报材料

## 使用方法

### 方式一：直接生成完整 HTML

用户提供内容大纲后，直接输出完整 HTML 代码：

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>{文档标题}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.1/font/bootstrap-icons.css" rel="stylesheet">
    <style>
        /* 核心样式变量 */
        :root {
            --gradient-primary: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            --primary-color: #0d6efd;
            --card-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        /* ... 完整样式见 template.html ... */
    </style>
</head>
<body>
    <!-- 导航栏 -->
    <nav class="navbar navbar-expand-lg navbar-dark">...</nav>
    
    <!-- Hero Section -->
    <section class="hero-section">...</section>
    
    <!-- 目录 -->
    <nav class="toc-section">...</nav>
    
    <!-- 正文章节 -->
    <main class="container">
        <section id="chapter1">
            <h2 class="section-title">第一章 标题</h2>
            <div class="card">...</div>
        </section>
    </main>
    
    <!-- 页脚 -->
    <footer>...</footer>
</body>
</html>
```

### 方式二：分步构建

1. **确认文档结构** - 章节划分、标题层级
2. **生成框架** - 导航 + Hero + 目录
3. **填充内容** - 逐章生成卡片内容
4. **添加可视化** - 表格、流程图、架构图

## 核心组件

### 1. 卡片样式

```html
<div class="card mb-4 animate-fadeInUp">
    <div class="card-header">
        <i class="bi bi-{icon} me-2 text-{color}"></i>
        章节标题
    </div>
    <div class="card-body">
        <!-- 内容 -->
    </div>
</div>
```

### 2. 渐变表格

```html
<table class="table">
    <thead>
        <tr>
            <th>列 1</th>
            <th>列 2</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>数据 1</td>
            <td>数据 2</td>
        </tr>
    </tbody>
</table>
```

### 3. 流程图

```html
<div class="d-flex align-items-center justify-content-center flex-wrap" style="gap:10px;padding:20px;background:rgba(13,110,253,0.05);border-radius:12px;">
    <div class="text-center" style="min-width:100px;">
        <i class="bi bi-{icon} fs-3 text-primary"></i>
        <br><small class="fw-bold">步骤 1</small>
    </div>
    <i class="bi bi-arrow-right text-primary fs-4"></i>
    <div class="text-center" style="min-width:100px;">
        <i class="bi bi-{icon} fs-3 text-info"></i>
        <br><small class="fw-bold">步骤 2</small>
    </div>
</div>
```

### 4. 代码块

```html
<div class="code-block">
    <span class="command">命令 1</span> → 
    <span class="command">命令 2</span> → 
    <span class="command">命令 3</span>
</div>
```

### 5. 警告/提示框

```html
<div class="alert alert-info" style="border-left: 4px solid var(--info-color);">
    <strong>提示：</strong>内容
</div>
```

## 颜色规范

| 类型 | 变量 | 色值 | 用途 |
|------|------|------|------|
| 主渐变 | `--gradient-primary` | `#667eea → #764ba2` | 导航、表头、强调 |
| 主色 | `--primary-color` | `#0d6efd` | 链接、图标 |
| 成功 | `--success-color` | `#198754` | 正向状态 |
| 警告 | `--warning-color` | `#ffc107` | 注意事项 |
| 危险 | `--danger-color` | `#dc3545` | 风险、错误 |
| 信息 | `--info-color` | `#0dcaf0` | 提示、说明 |

## 最佳实践

1. **章节结构清晰** - 每章用 `<section>` 包裹，标题用 `.section-title`
2. **卡片化内容** - 每个子主题用 `.card` 包裹
3. **图标增强** - Bootstrap Icons 增加视觉层次
4. **间距统一** - `mb-4`（24px）作为标准卡片间距
5. **响应式优先** - 表格用 `.table-responsive` 包裹
6. **离线友好** - 图片可转 Base64 嵌入

## 文件结构

```
ruitian-html/
├── SKILL.md              # 技能说明（本文件）
├── template.html         # 完整 HTML 模板
├── examples/             # 示例文档
│   ├── example1.md       # 示例 1：内容大纲
│   └── example1.html     # 示例 1：生成结果
└── scripts/
    └── generate.py       # （可选）生成脚本
```

## 示例输出

用户输入：
> 生成一个项目交付报告，包含：1.项目背景 2.实施方案 3.成果展示

输出：完整 HTML 代码，包含导航栏、Hero Section、目录、三个章节卡片、页脚。

## 限制

- 不适用于：静态图片设计（用 canvas-design）、公众号配图（用 weixin-canvas-design）
- 需要联网加载 Bootstrap CDN 资源（或本地部署）
- 复杂交互需额外 JavaScript

## 版本

- **v1.0** - 初始版本，基于企业项目交付报告实践提炼
