---
name: website-pickpocket
description: 网站扒手 - 完美复刻任意网站的工具。支持静态/动态页面抓取、资源下载、多框架输出（原生HTML/React/Vue/Angular）。触发场景：(1) 抓取网站生成静态副本 (2) 将网站转换为React/Vue项目 (3) 离线浏览网站 (4) 网站备份迁移
---

# 网站扒手 (Website Pickpocket)

一键复刻任意网站，生成可离线运行的静态版本或多框架项目。

## 快速开始

### 基础用法

```bash
# 原生HTML输出（默认）
pickpocket https://example.com

# 指定输出目录
pickpocket https://example.com -o my-project

# React项目输出
pickpocket https://example.com --framework react

# Vue项目输出
pickpocket https://example.com --framework vue
```

### 交互式引导

```bash
pickpocket
? 请输入要抓取的网站URL: https://example.com
? 选择输出框架: [原生HTML/React/Vue/Angular/Svelte]
? 爬取深度: [0=仅首页/1=首页+链接/2=递归2层/...]
```

## 核心功能

### 1. 智能爬取

- **静态页面**: 使用Cheerio快速解析
- **动态页面(SPA)**: Playwright等待DOM稳定后抓取
- **深度控制**: 0-5层递归爬取
- **去重机制**: URL规范化 + 已访问记录

### 2. 资源处理

| 资源类型 | 处理方式 |
|---------|---------|
| HTML | 解析DOM、提取结构 |
| CSS | 下载、提取内联样式 |
| JS | 下载、提取内联脚本 |
| 图片 | 下载、压缩(可选) |
| 字体 | 下载、Webfont处理 |
| 媒体 | 音视频资源下载 |

### 3. 框架输出

```
原生HTML          → 直接保存，资源本地化
React (Vite)      → .jsx组件 + react-router
Vue 3 (Vite)     → .vue单文件组件 + vue-router
Angular           → 模块化结构
Svelte            → .svelte组件
Tailwind CSS      → 原生HTML + Tailwind CSS (默认)
```

## 配置详解

### 命令行参数

```bash
pickpocket <url> [options]

# 必选参数
<url>                  # 要抓取的网站URL

# 输出选项
-o, --output <dir>    # 输出目录 (默认: ./output/[域名])
--framework <type>    # 输出框架: html|react|vue|vue3|angular|svelte|tailwind (默认: tailwind)
--name <name>        # 项目名称 (默认: 从域名提取)

# 爬取选项
-d, --depth <n>      # 爬取深度 0-5 (默认: 1)
-l, --limit <n>      # 最大页面数 (默认: 50)
--concurrency <n>    # 并发数 1-20 (默认: 5)

# 资源选项
--no-images          # 不下载图片
--no-css             # 不下载CSS
--no-js              # 不下载JavaScript
--optimize           # 压缩图片
--quality <n>        # 图片质量 1-100 (默认: 80)

# 其他
-c, --config <file>  # 配置文件路径
--verbose            # 详细输出
-h, --help           # 显示帮助
```

### 配置文件

创建 `pickpocket.yaml`:

```yaml
startUrl: https://example.com
framework: react

crawl:
  depth: 2
  maxPages: 100
  concurrency: 10
  waitStrategy: domstable

resources:
  download: true
  maxFileSize: 10485760  # 10MB
  imageQuality: 80
  optimizeImages: true

output:
  name: my-project
  directory: ./output
  overwrite: false
```

## 工作流程

```
1. 验证URL → 检查格式和网络连通性
2. 加载配置 → 合并CLI参数和配置文件
3. 爬取页面 → 按深度递归抓取
4. 下载资源 → 并发下载，本地化存储
5. 路径重写 → 修正HTML中的资源引用
6. 框架转换 → 转换为目标框架结构
7. 输出完成 → 生成可运行的项目
```

## 输出结构

### React项目

```
output/
├── src/
│   ├── components/
│   │   ├── Header.jsx
│   │   ├── Footer.jsx
│   │   └── ...
│   ├── pages/
│   │   ├── Home.jsx
│   │   └── ...
│   ├── styles/
│   ├── App.jsx
│   └── main.jsx
├── public/
│   ├── images/
│   ├── fonts/
│   └── ...
├── package.json
└── vite.config.js
```

### Vue项目

```
output/
├── src/
│   ├── components/
│   ├── views/
│   ├── assets/
│   ├── App.vue
│   └── main.js
├── public/
├── package.json
└── vite.config.js
```

### Tailwind CSS项目

```
output/
├── src/
│   └── css/
│       └── main.css
├── index.html
├── package.json
├── vite.config.js
├── tailwind.config.js
└── postcss.config.js
```

## 高级用法

### 登录态保持

```yaml
session:
  cookies:
    - name: session_id
      value: "xxx"
  localStorage:
    - key: user
      value: '{"id": 1}'
```

### 自定义等待条件

```yaml
crawl:
  waitStrategy: custom
  waitForSelector: "#app.loaded"
  waitTimeout: 30000
```

### URL过滤规则

```yaml
filter:
  allowedDomains:
    - example.com
    - api.example.com
  blockedDomains:
    - admin.example.com
  allowedPaths:
    - /blog/*
    - /docs/*
  blockedPaths:
    - /admin/*
    - /api/*
```

## 故障排查

### 问题: 页面内容为空

- 原因: SPA等待时间不足
- 解决: 增加 `waitTimeout` 或使用 `domstable` 策略

### 问题: 资源404错误

- 原因: 相对路径转换失败
- 解决: 检查 `baseUrl` 配置是否正确

### 问题: 反爬虫拦截

- 原因: 网站有防护机制
- 解决: 使用 `--user-agent` 伪装或配置代理

### 问题: 内存溢出

- 原因: 爬取页面过多
- 解决: 减少 `depth` 和 `maxPages` 参数

## 技术栈

- **Playwright** - 浏览器自动化
- **Cheerio** - HTML解析
- **Axios** - HTTP请求
- **Sharp** - 图片处理
- **PostCSS** - CSS转换
- **Zod** - 配置验证
- **Clack** - 交互式CLI
