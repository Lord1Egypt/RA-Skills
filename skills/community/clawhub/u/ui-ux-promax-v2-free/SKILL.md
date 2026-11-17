---
name: "ui-ux-promax-v2-free"
description: "优先级驱动的设计指南数据库,含50+风格、97配色、57字体配对,适合个人快速查询"
license: Proprietary
allowed-tools: read exec
compatibility: "Requires LLM with tool-use capability"
metadata:
  displayName: "UI/UX ProMax V2免费版"
  version: "1.0.0"
  summary: "优先级驱动的设计指南数据库,含50+风格、97配色、57字体配对,适合个人快速查询"
  tags:
    - "设计"
    - "UI"
    - "UX"
    - "配色"
    - "字体"
    - "前端"
    - "规则"
  source: "SkillHub"
  converted_at: "2026-07-22T17:58:36"
---

# UI/UX ProMax V2 - 免费版

## 概述

UI/UX ProMax V2免费版是一款面向个人开发者的优先级驱动设计指南工具。内置涵盖50+种界面风格、97套配色方案、57组字体配对、99条UX规则和25种图表类型的设计资源数据库,通过Python CLI工具按关键词查询,帮助开发者快速获取专业设计建议。

免费版提供8级优先级分层规则体系,确保关键设计问题(无障碍、交互)优先处理,适合个人项目的快速设计决策。

## 核心能力

### 1. 优先级分层规则体系

设计规则按影响等级分为8级,确保关键问题优先处理:

| 优先级 | 类别 | 影响等级 | 核心规则 |
|--------|------|----------|----------|
| 1 | 无障碍设计 | 关键 | 颜色对比4.5:1、焦点状态、alt文本、aria标签、键盘导航、表单标签 |
| 2 | 触摸与交互 | 关键 | 触摸目标44x44px、点击为主交互、异步禁用按钮、错误反馈、cursor-pointer |
| 3 | 性能优化 | 高 | WebP图片、srcset、懒加载、reduced-motion、预留异步内容空间 |
| 4 | 布局与响应式 | 高 | viewport meta、16px最小字号、无横向滚动、z-index管理 |
| 5 | 字体与配色 | 中 | 行高1.5-1.75、行宽65-75字符、字体配对协调 |
| 6 | 动画效果 | 中 | 150-300ms微交互、transform/opacity动画、骨架屏加载 |
| 7 | 风格选择 | 中 | 风格匹配产品类型、全站一致性、SVG图标非emoji |
| 8 | 图表与数据 | 低 | 图表类型匹配数据、无障碍配色、表格替代方案 |

**输入**: 用户提供优先级分层规则体系所需的指令和必要参数。
**处理**: 按照skill规范执行优先级分层规则体系操作,遵循单一意图原则。
**输出**: 返回优先级分层规则体系的执行结果,包含操作状态和输出数据。

### 2. 基础设计域搜索

```bash
# 按产品类型生成设计系统
python3 scripts/search.py "SaaS dashboard fintech" --design-system

# 按域搜索详细信息
python3 scripts/search.py "glassmorphism dark" --domain style
python3 scripts/search.py "elegant luxury" --domain typography
python3 scripts/search.py "animation accessibility" --domain ux
```

| 域 | 用途 | 示例关键词 |
|----|------|-----------|
| `product` | 产品类型推荐 | SaaS, 电商, 作品集, 医疗, 美容, 服务 |
| `style` | UI风格与效果 | 玻璃态, 极简, 暗色模式, 粗野主义 |
| `typography` | 字体配对 | 优雅, 活泼, 专业, 现代 |
| `color` | 配色方案 | saas, ecommerce, healthcare, fintech |
| `ux` | 最佳实践与反模式 | 动画, 无障碍, z-index, 加载 |

**输入**: 用户提供基础设计域搜索所需的指令和必要参数。
**处理**: 按照skill规范执行基础设计域搜索操作,遵循单一意图原则。
**输出**: 返回基础设计域搜索的执行结果,包含操作状态和输出数据。

### 3. 设计系统生成

```bash
# 生成完整设计系统(风格+配色+字体+效果+反模式)
python3 scripts/search.py "beauty spa wellness elegant" --design-system -p "Serenity Spa"
```

输出包含:
- 推荐的设计风格
- 配色方案(主色+辅助色+强调色)
- 字体配对(标题+正文)
- 视觉效果建议
- 应避免的反模式

**输入**: 用户提供设计系统生成所需的指令和必要参数。
**处理**: 按照skill规范执行设计系统生成操作,遵循单一意图原则。
**输出**: 返回设计系统生成的执行结果,包含操作状态和输出数据。

### 4. 默认技术栈指引

```bash
# 获取Tailwind CSS实现建议(默认技术栈)
python3 scripts/search.py "layout responsive form" --stack html-tailwind
```

**输入**: 用户提供默认技术栈指引所需的指令和必要参数。
**处理**: 按照skill规范执行默认技术栈指引操作,遵循单一意图原则。
**输出**: 返回默认技术栈指引的执行结果,包含操作状态和输出数据。
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：优先级驱动的设计、指南数据库、适合个人快速查询、面向个人开发者的、优先级驱动、设计指南、种界面风格、套配色方案、组字体配对、规则和、种图表类型、CLI、按关键词查询、核心能力、优先级分层的设计、级优先级、设计系统一键生成、质量检查清单等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持。
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

## 使用场景

### 场景一:健康医疗SaaS设计决策

独立开发者在构建一款健康管理SaaS,需要确定整体设计方向。

```bash
# 步骤1:生成设计系统
python3 scripts/search.py "healthcare SaaS dashboard clean professional" --design-system -p "HealthApp"

# 步骤2:补充UX规则检查
python3 scripts/search.py "accessibility form validation" --domain ux

# 步骤3:获取Tailwind实现指引
python3 scripts/search.py "dashboard card table" --stack html-tailwind
```

### 场景二:电商落地页风格选择

为一个新的电商平台选择视觉风格和配色方案。

```bash
# 搜索电商风格
python3 scripts/search.py "ecommerce modern luxury" --domain style

# 搜索电商配色
python3 scripts/search.py "ecommerce fashion" --domain color

# 搜索落地页结构
python3 scripts/search.py "hero testimonial pricing" --domain landing
```

### 场景三:UX规则优先级自查

开发完成后,按优先级检查UX规则:

```bash
# 优先级1-2:无障碍和交互(关键)
python3 scripts/search.py "color-contrast focus-states touch-target" --domain ux

# 优先级3-4:性能和布局(高)
python3 scripts/search.py "image-optimization viewport z-index" --domain ux

# 优先级5-6:字体和动画(中)
python3 scripts/search.py "line-height animation duration" --domain ux
```

## 不适用场景

以下场景UI/UX ProMax V2免费版不适合处理：

- 3D建模和动画制作
- 照片级写实渲染
- 手绘原创插画

## 触发条件

需要设计创作、UI设计、海报制作、品牌视觉时使用。不适用于非本工具能力范围的需求。

## 快速开始

1. 阅读## 核心能力章节了解skill功能
2. 按## 依赖说明配置环境
3. 执行所需能力对应的命令
4. 参考## 错误处理章节处理异常
5. 查看## FAQ解答常见疑问

### 环境验证

```bash
# 验证Python环境
python3 --version || python --version
# 预期: Python 3.8+

# 验证搜索工具
python3 scripts/search.py "minimal" --domain style -n 3
```

### 三步设计流程

```bash
# 第1步:分析需求并生成设计系统
python3 scripts/search.py "beauty spa wellness elegant" --design-system -p "Serenity Spa"

# 第2步:补充域搜索
python3 scripts/search.py "animation accessibility" --domain ux
python3 scripts/search.py "elegant luxury serif" --domain typography

# 第3步:技术栈指引
python3 scripts/search.py "layout responsive form" --stack html-tailwind
```

**结果处理**: 执行完成后,查看输出结果确认操作状态。成功时输出包含处理摘要和结果数据;失败时根据错误信息排查问题,查阅错误处理章节获取恢复步骤。


## 示例

### 设计决策记录文件

```json
{
  "project_name": "HealthApp",
  "product_type": "SaaS",
  "industry": "healthcare",
  "design_system": {
    "style": "clean professional",
    "colors": {
      "primary": "#0D9488",
      "secondary": "#64748B",
      "accent": "#14B8A6",
      "background": "#FFFFFF",
      "text": "#0F172A"
    },
    "typography": {
      "heading": "Inter",
      "body": "Inter"
    }
  },
  "priority_checks": [
    {"level": 1, "category": "无障碍", "status": "passed"},
    {"level": 2, "category": "触摸交互", "status": "passed"},
    {"level": 3, "category": "性能", "status": "pending"},
    {"level": 4, "category": "布局响应式", "status": "pending"}
  ],
  "stack": "html-tailwind"
}
```

### 免费版与专业版功能对比

| 功能项 | 免费版 | 专业版 |
|--------|--------|--------|
| 设计域 | 5个基础域 | 全部10个域 |
| 技术栈 | html-tailwind | 全部10种技术栈 |
| 设计系统持久化 | 不支持 | MASTER+页面覆盖 |
| 推理规则引擎 | 不支持 | ui-reasoning.csv |
| 批量搜索 | 不支持 | 支持 |
| 输出格式 | 纯文本 | Markdown+JSON |
| 优先级体系 | 8级分层 | 8级+深度审计 |
| 适用对象 | 个人开发者 | 团队/企业 |

## 最佳实践

### 1. 按优先级处理设计问题

```text
关键(优先级1-2): 无障碍、触摸交互 -> 必须解决
高  (优先级3-4): 性能、布局响应式 -> 应该解决
中  (优先级5-7): 字体、动画、风格 -> 建议解决
低  (优先级8):   图表与数据       -> 可选优化
```

### 2. 关键词具体化

```bash
# 不推荐
python3 scripts/search.py "app" --design-system

# 推荐
python3 scripts/search.py "healthcare SaaS dashboard clean minimal" --design-system
```

### 3. 专业UI质量检查清单

| 检查项 | 正确 | 错误 |
|--------|------|------|
| 图标 | SVG(Heroicons/Lucide) | emoji |
| 悬停 | 颜色/透明度过渡 | 缩放导致布局偏移 |
| 光标 | cursor-pointer | 默认光标 |
| 过渡 | 150-300ms | 即时或>500ms |
| 对比度 | 4.5:1 | 低对比灰色 |
| 玻璃态浅色 | bg-white/80+ | bg-white/10 |
| 浅色文字 | #0F172A(slate-900) | #94A3B8(slate-400) |
| 浅色边框 | border-gray-200 | border-white/10 |
| 浮动导航 | top-4 left-4 right-4 | top-0 left-0 right-0 |
| 容器宽度 | 统一max-w-6xl | 混合不同宽度 |

### 4. 交付前检查矩阵

| 维度 | 检查内容 | 标准 |
|------|----------|------|
| 视觉质量 | 图标/Logo/悬停/主题色 | SVG图标,品牌验证,无布局偏移 |
| 交互 | 光标/悬停/过渡/焦点 | cursor-pointer,150-300ms,可见焦点 |
| 明暗模式 | 对比度/玻璃态/边框 | 4.5:1,可见元素,双模测试 |
| 布局 | 浮动间距/遮挡/响应式 | 375/768/1024/1440px适配 |
| 无障碍 | alt文本/标签/颜色指示/动画 | 全覆盖,prefers-reduced-motion |

## 常见问题

### Q1: 免费版与专业版的主要区别?

免费版提供5个基础设计域和默认html-tailwind技术栈,适合个人快速查询。专业版扩展至全部10个域、10种技术栈,并新增设计系统持久化、推理引擎和批量搜索。

### Q2: 优先级分层如何帮助设计决策?

8级优先级确保你先解决关键问题(无障碍、交互),再处理高优先级问题(性能、布局),最后优化中低优先级项。避免在次要细节上浪费时间而忽略关键体验问题。

### Q3: 可以搜索图表类型推荐吗?

免费版不包含chart域搜索。图表类型匹配(25种图表)是专业版功能,支持趋势图、对比图、时间线、漏斗图等推荐。

### Q4: 设计系统可以保存吗?

免费版不支持持久化。每次搜索为即时输出。如需跨会话保存和页面级覆盖,请使用专业版的--persist功能。

### Q5: Python版本要求?

需要Python 3.8及以上。通过`python3 --version`检查。

## 依赖说明

### 运行环境

- **Agent平台**: 支持SKILL.md的任意AI Agent(Claude Code / Cursor / Codex / Gemini CLI等)
- **操作系统**: Windows / macOS / Linux
- **Python版本**: 3.8及以上

### 依赖详情

| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:-------|:-----|:---------|:---------|
| Python 3 | 运行时 | 必需 | 系统包管理器安装 |
| LLM API | API | 必需 | 由Agent内置LLM提供 |

Python安装:

```bash
# macOS
brew install python3

# Ubuntu/Debian
sudo apt update && sudo apt install python3

# Windows
winget install Python.Python.3.12
```

### API Key 配置

本Skill的CLI搜索工具基于本地数据文件运行,无需额外API Key。设计建议由Agent内置LLM驱动。

### 可用性分类

- **分类**: MD+EXEC(纯Markdown指令,部分功能需exec命令行执行)
- **说明**: 基于Markdown的AI Skill,通过自然语言指令驱动Agent完成操作。核心查询功能依赖Python CLI脚本,需确保exec工具可用。

## 错误处理


| 错误场景 | 原因 | 处理方式 |
|---------|------|---------|
| 配置错误 | 参数缺失或格式错误 | 检查依赖说明中的配置要求 |
| 运行时错误 | 运行环境不满足 | 确认运行环境符合依赖说明 |
| 网络错误 | 连接超时或不可达 | 执行ping命令测试网络连通性,检查防火墙和代理设置连接后执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令，参考国内替代方案 |

## 已知限制

- 需LLM支持,无LLM环境不可用
- 复杂业务场景建议结合人工经验判断
- 执行效率受模型能力与网络环境影响
- 当前为免费版本,如需完整功能请升级到付费版获取全部能力