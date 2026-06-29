---
name: tree-view-craft
version: 1.0.0
description: 目录结构转可折叠、可搜索、可点击的交互式HTML目录树
author: wuwenbin-beijing-st
homepage: https://github.com/wwbwin/clawhub-skills
tags: [visualization, html, tool]
---

# 【简介】

项目文档、代码仓库、知识库的目录结构展示是个看似简单但实际困扰很多人的问题。纯文本的 tree 输出无法折叠，大项目看起来非常乱；没有文件类型图标无法快速区分文件类型；静态截图一经生成就无法更新，更无法交互操作。

本 Skill 将目录结构转化为可折叠、可搜索、可点击的交互式 HTML 页面。支持 7 种展示风格（资源管理器、思维导图、旭日图、紧凑列表、带注释型、筛选型、大小可视化），内置文件类型配色和统计面板，让目录树从静态截图升级为动态工具。

---

# Tree View Craft — 目录树生成器 Skill

> 将项目目录结构转化为可折叠、可搜索、可点击的交互式目录树 HTML。
>
> 作者：wuwenbin-beijing-st

## 使用说明

运行此 Skill 后，按以下步骤操作：

1. **输入目录结构**：粘贴 `tree` 命令输出、`find` 输出，或手动描述目录层级
2. **选择展示风格**：从映射表中选择最适合的呈现方式
3. **选择配色方案**：选择文件类型配色主题
4. **生成目录树**：输出交互式单文件 HTML

### 输入格式建议

```
project/
├── src/
│   ├── index.js
│   └── utils.js
├── docs/
│   └── README.md
└── package.json
```

或直接粘贴 `tree -L 3` 命令的输出。

## 场景-模式映射表

| 项目类型 | 推荐模式 | 特点 |
|---------|---------|------|
| 代码项目 | explorer（资源管理器） | 类似 VS Code 侧栏，文件类型图标，可折叠 |
| 知识库/文档 | mindmap（思维导图） | 放射状布局，适合展示知识结构 |
| 存储分析 | sunburst（旭日图） | 展示各目录文件大小占比 |
| 快速参考 | compact（紧凑列表） | 纯文本风格，节省空间 |
| 架构文档 | annotated（带注释） | 每个节点可添加说明文字 |
| 审计/排查 | filtered（按类型筛选） | 按 .js/.md/.json 等类型快速筛选 |
| 存储管理 | size-chart（大小可视化） | 文件大小+数量统计可视化 |

## 配色方案库

### 文件类型配色
- **代码文件**（.js, .ts, .py, .java）：`#2563eb` 蓝
- **文档文件**（.md, .txt, .pdf, .doc）：`#d97706` 黄
- **配置文件**（.json, .yaml, .toml, .env）：`#6b7280` 灰
- **媒体文件**（.png, .jpg, .mp4, .mp3）：`#7c3aed` 紫
- **样式文件**（.css, .scss, .less）：`#db2777` 粉
- **数据文件**（.csv, .xlsx, .db, .sql）：`#059669` 绿

### 4 套主题配色

#### 1. 浅色经典
```
--bg: #ffffff
--text: #1f2937
--node-hover: #f3f4f6
--node-active: #e5e7eb
--border: #d1d5db
--folder: #f59e0b
```

#### 2. 深色专业
```
--bg: #0f172a
--text: #e2e8f0
--node-hover: #1e293b
--node-active: #334155
--border: #475569
--folder: #fbbf24
```

#### 3. 清爽绿
```
--bg: #f0fdf4
--text: #14532d
--node-hover: #dcfce7
--node-active: #bbf7d0
--border: #86efac
--folder: #22c55e
```

#### 4. 暗紫科技
```
--bg: #1e1b4b
--text: #e0e7ff
--node-hover: #312e81
--node-active: #3730a3
--border: #4338ca
--folder: #a78bfa
```

## 交互增强包列表

### 基础交互
- 节点折叠/展开
- 搜索过滤（实时高亮匹配项）
- 文件类型图例
- 统计信息面板（总文件数、目录数、文件类型分布）

### 高级交互
- 按文件类型筛选
- 按大小/名称排序
- 复制文件路径
- 导出结构文本（方便嵌入 Markdown）
- 展开/折叠全部

## 限制说明

- **单文件 HTML**：所有输出均为单一 HTML 文件，CSS 和 JS 全部内联
- **零外部依赖**：不加载任何 CDN 资源、字体、图标库
- **文件类型图标**：纯 CSS 绘制，无需图标库
- **系统字体栈**：font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Noto Sans SC", sans-serif
- **浏览器兼容**：Chrome/Firefox/Safari/Edge 最新两版
- **响应式布局**：桌面和移动端均可正常浏览

## 命令定义

### `/tree-view`
主入口命令。输入目录结构后生成可折叠交互式目录树 HTML。

### `/tree-stats`
生成带统计信息的目录分析页。包含文件数量、类型分布、目录深度等统计面板。

## 文件结构

```
skills/tree-view-craft/
├── SKILL.md
├── patterns/
│   ├── explorer.json        # 文件资源管理器风格
│   ├── mindmap.json         # 思维导图风格
│   ├── sunburst.json        # 旭日图（大小占比）
│   ├── compact.json         # 紧凑列表
│   ├── annotated.json       # 带注释说明
│   ├── filtered.json        # 按类型筛选
│   └── size-chart.json      # 文件大小可视化
└── templates/
    ├── base.html
    ├── explorer.html
    ├── mindmap.html
    ├── sunburst.html
    ├── compact.html
    ├── annotated.html
    ├── filtered.html
    └── size-chart.html
```
