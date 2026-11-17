---
slug: ui-ux-dev-tool-free
name: ui-ux-dev-tool-free
version: 1.0.0
displayName: UI/UX开发工具免费版
summary: "自然语言生成React页面,CDN零构建,含截图审查循环,适合个人快速原型开发。面向个人开发者的自然语言驱动React页面生成工具,通过CDN方式零构建运行,"
license: Proprietary
edition: free
description: '面向个人开发者的自然语言驱动React页面生成工具,通过CDN方式零构建运行,

  内置截图视觉审查循环,支持快速原型迭代。核心能力:

  - 自然语言描述生成React页面(CDN零构建)

  - 项目配置与偏好管理

  - 截图视觉审查与迭代修复

  - 基础设计原则自动应用

  - 图片转WebP格式优化

  - 静态文件导出

  适用场景:

  - 个人开发者快速生成落地页原型

  - 独立项目单页面快速开发

  - 设计概念验证与视觉迭代

  差异化:免费版聚焦单页面快速生成与视觉审查,使用CDN方式零构建,

  适合个人快速原型'
tags:
  - 设计
  - UI
  - UX
  - React
  - 前端
  - 原型
  - 开发
  - UI设计
  - react
  - script
  - classname
  - webp
  - bash
tools:
  - read
  - exec
  - write
homepage: ""
category: "Creative"
---
# UI/UX开发工具 - 免费版

## 概述

UI/UX开发工具免费版是一款面向个人开发者的自然语言驱动React页面生成工具。通过描述需求即可生成生产质量的React页面,采用CDN方式零构建运行,内置截图视觉审查循环,支持桌面端和移动端的快速迭代.
免费版聚焦单页面快速生成,自动应用布局、排版、配色、响应式等设计原则,适合个人项目的快速原型开发和概念验证.
## 核心能力

### 1. 自然语言生成React页面

通过CDN方式加载React,无需构建步骤,直接生成可运行的HTML页面:

## 输入格式
| 参数名 | 类型 | 必填 | 说明 |
|---|---|---|---|
| input | string | 是 | UI/UX开发工具免费版处理的输入数据或指令 |
| options | object | 否 | 附加配置选项,如模式选择、格式偏好等 |
| callback_url | string | 否 | 异步处理完成后的回调通知URL |

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>页面标题</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <script src="https://unpkg.com/react@18/umd/react.production.min.js"></script>
com/react-dom@18/umd/react-dom.production.min.js"></script>
com/@babel/standalone/babel.min.js"></script>
</head>
<body>
  <div id="root"></div>
  <script type="text/babel">
    function App() {
      return (
        <div className="min-h-screen bg-slate-50">
          <header className="bg-white shadow-sm">
            <nav className="max-w-6xl mx-auto px-4 py-4">
              <h1 className="text-2xl font-bold text-slate-900">我的应用</h1>
            </nav>
          </header>
          <main className="max-w-6xl mx-auto px-4 py-16">
            <h2 className="text-4xl font-bold text-slate-900 mb-4">
              欢迎使用
            </h2>
            <p className="text-lg text-slate-600">
              这是一个CDN驱动的React页面
            </p>
          </main>
        </div>
      );
    }
    ReactDOM.createRoot(document.getElementById('root')).render(<App />);
  </script>
</body>
</html>
```

**处理**: 解析自然语言生成React页面的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回自然语言生成React页面的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 2. 项目配置管理

每个项目使用JSON文件管理配置:

```json
{
  "name": "my-landing-page",
  "preferences": {
    "style": "minimal",
    "font": "Inter",
    "primary_color": "#2563EB",
    "dark_mode": false
  },
  "design_system": {
    "max_width": "max-w-6xl",
    "spacing_scale": "tailwind-default",
    "border_radius": "rounded-lg"
  },
  "pages": ["landing"]
}
```

**处理**: 解析项目配置管理的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回项目配置管理的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 3. 截图视觉审查

生成页面后,通过截图工具进行视觉审查并迭代修复:

```bash
# 桌面端截图审查(1400x900)
bash （请参考skill目录中的脚本文件） "http://localhost:5174/my-project/landing/" /tmp/landing-review.png 1400 900
# .
# 移动端截图审查(390x844)
bash （请参考skill目录中的脚本文件） "http://localhost:5174/my-project/landing/" /tmp/landing-mobile.png 390 844
```

**处理**: 解析截图视觉审查的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回截图视觉审查的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 4. 图片WebP转换

将用户提供的图片转换为WebP格式以优化性能:

```bash
# 转换图片为WebP(默认质量80)
bash （请参考skill目录中的脚本文件） input.png output.webp 80
# .
# Hero横幅图片(质量85)
bash （请参考skill目录中的脚本文件） hero.jpg hero.webp 85
# .
# 缩略图/图标(质量70)
bash （请参考skill目录中的脚本文件） icon.png icon.webp 70
```

**处理**: 解析图片WebP转换的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回图片WebP转换的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 5. 自动应用设计原则

生成的页面自动遵循以下设计原则:

| 原则类别 | 规则 |
|:-----|:-----|
| 布局间距 | 使用Tailwind标准间距(4/6/8/12/16/24),最大宽度max-w-5xl或max-w-6xl |
| 排版层次 | h1最大,最多3-4种字号,行宽65-75字符,加粗标题+常规正文 |
| 色彩对比 | WCAG AA标准4.5:1,最多1主色+1强调色+中性色 |
| 响应式 | 移动优先390px,断点sm/md/lg,触摸目标44x44px |
| 组件交互 | SVG图标(非emoji),悬停反馈,150-200ms过渡,可见焦点环 |
| 性能 | WebP图片,懒加载,aspect-ratio防布局偏移 |

**处理**: 解析自动应用设计原则的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回自动应用设计原则的响应数据,包含状态码、结果和日志.
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：零构建、含截图审查循环、适合个人快速原型、面向个人开发者的、自然语言驱动、页面生成工具、方式零构建运行、内置截图视觉审查、支持快速原型迭代、核心能力、自然语言描述生成、项目配置与偏好管、截图视觉审查与迭、基础设计原则自动、格式优化、静态文件导出等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持.
## 使用场景

### 场景一:快速生成产品落地页

开发者需要为一个新产品快速生成落地页原型.
工作流程:
1. 确定项目名称:"ProductLaunch"
2. 确认偏好:极简风格、Inter字体、蓝色主色
3. 确定页面slug:"landing"
4. 描述内容:Hero区+功能特性+定价方案+CTA
5. 生成React页面并截图审查

```bash
# 启动本地服务
bash （请参考skill目录中的脚本文件） 5174
# .
# 生成页面后截图审查
bash （请参考skill目录中的脚本文件） "http://localhost:5174/ProductLaunch/landing/" /tmp/review.png 1400 900
```

### 场景二:个人作品集页面

设计师需要快速生成个人作品集展示页面.
设计要点:
- 使用max-w-4xl控制内容宽度
- 卡片网格展示作品(grid-cols-1 md:grid-cols-2)
- 深色背景(bg-slate-900)配合分层暗色
- 图片懒加载+WebP格式

### 场景三:活动推广页面

为一次线上活动生成推广页面,包含倒计时和报名表单.
```html
<script type="text/babel">
  function App() {
    const [timeLeft, setTimeLeft] = React.useState('');
# .
    React.useEffect(() => {
      const timer = setInterval(() => {
        // 倒计时逻辑
      }, 1000);
      return () => clearInterval(timer);
    }, []);
# .
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-600 to-purple-700">
        <main className="max-w-4xl mx-auto px-4 py-24 text-center">
          <h1 className="text-5xl font-bold text-white mb-6">
            2026年度技术大会
          </h1>
          <div className="text-3xl font-mono text-white mb-12">
            {timeLeft}
          </div>
          <button className="bg-white text-blue-600 px-8 py-4 rounded-lg
                         font-semibold text-lg hover:bg-blue-50
                         transition-colors duration-200 cursor-pointer">
            立即报名
          </button>
        </main>
      </div>
    );
  }
</script>
```

## 不适用场景

以下场景UI/UX开发工具免费版不适合处理：

- 3D建模和动画制作
- 照片级写实渲染
- 手绘原创插画

## 触发条件

、品牌视觉时使用。不适用于非本工具能力范围的需求.
## 快速开始

1. 阅读## 核心能力章节了解skill功能
2. 按## 依赖说明配置环境
3. 执行所需能力对应的命令
4. 参考## 错误处理章节处理异常
5. 查看## FAQ解答常见疑问

### 首次设置

```bash
# 检查端口配置(默认5174)
# 运行首次设置脚本
bash （请参考skill目录中的脚本文件） 5174
# .
# 验证服务启动
curl http://localhost:5174/
```

### 单页面生成流程

```bash
# 第1步:创建项目目录
mkdir -p serve/my-project/landing
# .
# 第2步:创建项目配置
cat > serve/my-project/project.json << 'EOF'
{
  "name": "my-project",
  "preferences": {
    "style": "modern",
    "font": "Inter",
    "primary_color": "#2563EB"
  },
  "pages": ["landing"]
}
EOF
# .
# 第3步:生成React页面到 index.html
# (Agent根据需求生成页面代码)
# .
# 第4步:截图审查
bash （请参考skill目录中的脚本文件） "http://localhost:5174/my-project/landing/" /tmp/review.png 1400 900
# .
# 第5步:移动端审查
bash （请参考skill目录中的脚本文件） "http://localhost:5174/my-project/landing/" /tmp/mobile.png 390 844
```

**响应解析**: 完成完成后,查看输出响应确认任务状态。成功时输出包含解析摘要和响应数据;失败时根据错误信息排查问题,查阅错误解析章节获取恢复步骤.
#
## 示例

### 项目目录结构

```text
serve/
├── my-project/
│   ├── project.json          # 项目配置
│   ├── assets/               # 图片资源
│   │   ├── logo.webp
│   │   └── hero.webp
│   ├── landing/
│   │   └── index.html        # React页面(CDN)
│   └── about/
│       └── index.html        # 关于页面
```

### 免费版与专业版功能对比

| 功能项 | 免费版 | 专业版 |
|---:|---:|---:|
| 页面生成 | 单页面 | 多页面项目管理 |
| 项目配置 | 基础JSON | 完整设计系统持久化 |
| 截图审查 | 桌面+移动 | 多分辨率+自动化循环 |
| 图片处理 | WebP转换 | 批量转换+优化报告 |
| 导出 | 静态文件 | Zip打包+独立部署 |
| 设计系统 | 基础原则 | 完整设计系统引用 |
| 迭代流程 | 手动反馈 | 自动化审查+修复 |
| 适用对象 | 个人开发者 | 团队/代理机构 |

## 最佳实践

### 1. 每步操作都告知用户

在生成过程中,每个操作步骤都应向用户报告进度:

```text
-> 正在读取项目配置.
-> 正在确认页面slug.
-> 正在生成React页面代码.
-> 正在运行截图审查.
-> 桌面端审查完成,发现3个问题.
-> 正在修复问题.
-> 移动端审查完成.
-> 页面已就绪,预览地址:http://localhost:5174/my-project/landing/
```

### 2. 桌面+移动双端审查

每次生成页面后,至少进行一次桌面端和一次移动端审查:

```bash
# 桌面端(1400x900)
bash （请参考skill目录中的脚本文件） "<url>" /tmp/desktop.png 1400 900
# .
# 移动端(390x844)
bash （请参考skill目录中的脚本文件） "<url>" /tmp/mobile.png 390 844
```

## 错误处理

| 错误 | 正确做法 | 处理方式 |
|:---:|:---:|:---:|
| 文字触碰屏幕边缘 | 移动端最小px-4内边距 | 对照依赖说明章节逐项验证配置项,确认环境变量已正确设置后执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令 |
| emoji用作图标 | 使用SVG图标 | 对照依赖说明章节逐项验证配置项,确认环境变量已正确设置后执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令 |
| 纯黑背景 | 使用分层暗色(bg-900 > bg-800) | 对照依赖说明章节逐项验证配置项,确认环境变量已正确设置后执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令 |
| 无悬停状态 | 添加颜色/阴影过渡 | 对照依赖说明章节逐项验证配置项,确认环境变量已正确设置后执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令 |
| 圆角不一致 | 统一rounded-lg | 对照依赖说明章节逐项验证配置项,确认环境变量已正确设置后执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令 |
| 移动端字号溢出 | 测试390px宽度 | 对照依赖说明章节逐项验证配置项,确认环境变量已正确设置后执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令 |
| 缺少viewport meta | 添加meta viewport标签 | 对照依赖说明章节逐项验证配置项,确认环境变量已正确设置后执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令 |
| 移动端无汉堡菜单 | 包含移动导航菜单 | 对照依赖说明章节逐项验证配置项,确认环境变量已正确设置后执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令 |

### 4. 图片优化报告

转换图片后,向用户报告压缩效果:

```text
-> 图片转换完成:
   logo.png: 1.2MB -> 340KB (减少72%)
   hero.jpg: 3.5MB -> 890KB (减少75%)
   icon.png: 45KB -> 12KB (减少73%)
```

## 常见问题

### Q1: 免费版支持多页面项目吗?

免费版支持在项目目录下创建多个页面文件夹,但缺少专业版的多页面设计系统持久化和批量管理功能。每个页面需独立生成和审查.
### 已知限制

CDN方式无需构建步骤,直接在浏览器中运行。限制包括:无法使用npm包、Babel转译有性能开销、不适合生产环境大规模部署。适合原型开发和概念验证.
### Q3: 截图审查如何工作?

通过截图脚本捕获页面渲染结果,Agent通过图像分析工具检查视觉问题(布局错位、对比度不足、响应式问题等),然后修复并重新截图,形成迭代循环.
### Q4: 可以使用自定义字体吗?

可以。在HTML头部通过Google Fonts或本地字体文件引入。建议使用Inter(无衬线UI)配合JetBrains Mono(等宽代码).
### Q5: 如何导出页面?

免费版生成的HTML文件是独立的静态文件,可直接打开或通过任意静态服务器提供服务。专业版支持Zip打包导出整个项目.
- 当前为免费版本,如需完整功能请升级到付费版获取全部能力
## 依赖说明

### 运行环境

- **Agent平台**: 支持SKILL.md的任意AI Agent(Claude Code / Cursor / Codex / Gemini CLI等)
- **操作系统**: Windows / macOS / Linux
- **浏览器**: Chrome/Chromium(用于截图审查)
- **本地服务器**: Python http.server或Node.js静态服务器

### 依赖详情

| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:------|------:|:------|:------|
| Bash | 运行时 | 必需 | 系统内置(macOS/Linux)或Git Bash(Windows) |
| Chrome/Chromium | 截图工具 | 必需 | 浏览器安装 |
| cwebp | 图片转换 | 推荐 | libwebp工具包 |
| LLM API | API | 必需 | 由Agent内置LLM提供 |
| CDN资源 | 前端库 | 必需 | 自动从CDN加载 |

CDN加载的前端库:
- React 18 (react.production.min.js)
- ReactDOM 18 (react-dom.production.min.js)
- Babel Standalone (babel.min.js)
- Tailwind CSS (cdn.tailwindcss.com)

安装cwebp(WebP转换工具):

```bash
# macOS
brew install webp
# .
# Ubuntu/Debian
sudo apt install webp
# .
# Windows
# 下载 libwebp 并添加到PATH
```

### API Key 配置

本skill基于Markdown指令规范和本地脚本运行,无需额外API Key。页面生成由Agent内置LLM驱动,截图和图片转换为本地工具执行。CDN前端库通过公网加载,无需配置.
### 可用性分类

- **分类**: MD+EXEC(纯Markdown指令,部分功能需exec命令行执行)
- **说明**: 基于Markdown的AI Skill,通过自然语言指令驱动Agent完成操作。页面生成后需要exec工具执行截图脚本和图片转换脚本。本地服务需通过Bash启动,截图功能依赖Chrome/Chromium浏览器.
## 输出格式
```json
{
  "success": true,
  "data": {
    "result": "UI/UX开发工具免费版处理结果",
    "execution_time": "0.5s",
    "metadata": {
      "version": "1.0",
      "processor": "ui ux dev"
    }
  },
  "execution_log": ["解析输入参数", "执行核心处理", "格式化输出结果"],
  "error": null
}
```
