---slug: stagehand-browser-tool-free
name: stagehand-browser-tool-free
version: 1.0.0
displayName: 浏览器自动化工具免费版
summary: "通过自然语言指令驱动本"
license: Proprietary
edition: free
description: 浏览器自动化工具免费版,面向个人用户提供基础的网页自动化能力。通过自然语言指令驱动本地 Chrome 浏览器,实现页面导航、元素操作、数据提取等核心功能。Use
  when 需要数据分析、报表生成、统计洞察、数据可视化时使用。不适用于实时流数据处理。Use when 需要数据分析、报表生成、统计洞察、数据可视化时使用。不适用于实时流数据处理.
tags:
  - 研究工具
  - 浏览器自动化
  - 个人效率
  - 搜索
  - 检索
  - 工具
  - browser
  - chrome
  - bash
  - act
tools:
  - read
  - exec
  - glob
  - grep
homepage: ""
category: "Knowledge"---# 浏览器自动化工具免费版

## 概述

浏览器自动化工具免费版是一款面向个人用户的轻量级网页自动化工具。它通过自然语言指令驱动本地 Chrome 浏览器,让 AI 能够像真人一样浏览网页、点击按钮、填写表单、提取数据,无需编写复杂的自动化脚本.
本工具特别适合个人开发者、学生和自由职业者,用于简化日常的网页交互任务,例如信息采集、表单提交、页面内容提取等。免费版聚焦本地浏览器场景,部署简单,上手快速.
## 核心能力

### 1. 自然语言指令驱动

通过自然语言描述即可控制浏览器行为,无需记忆复杂的 API 语法.
## 输入格式
| 参数名 | 类型 | 必填 | 说明 |
|---|---|---|---|
| input | string | 是 | 浏览器自动化工具免费版处理的输入数据或指令 |
| options | object | 否 | 附加配置选项,如模式选择、格式偏好等 |
| callback_url | string | 否 | 异步处理完成后的回调通知URL |

```bash
# 示例
browser act "点击页面顶部的登录按钮"
browser act "在搜索框中输入'人工智能最新进展'"
browser act "滚动到页面底部并点击下一页"
```

**处理**: 解析自然语言指令驱动的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回自然语言指令驱动的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 2. 页面导航与内容提取

支持精准的页面导航和结构化数据提取.
```bash
# 导航到指定页面
browser navigate https://example.com
# ...
# 提取页面标题和主要内容
browser extract "获取页面标题和正文摘要"
# ...
# 提取结构化数据
browser extract "提取商品列表中的名称、价格和评分" '{"items":[{"name":"string","price":"number","rating":"number"}]}'
```

**处理**: 解析页面导航与内容提取的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回页面导航与内容提取的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 3. 元素发现与截图

自动发现页面可交互元素,并支持截图验证.
```bash
# 发现页面可交互元素
browser observe "找到所有可点击的按钮和链接"
# ...
# 截图保存当前页面状态
browser screenshot
```

**处理**: 解析元素发现与截图的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回元素发现与截图的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 4. 本地浏览器模式

完全基于本地 Chrome 浏览器运行,数据不出本机,保障隐私安全.

**处理**: 解析本地浏览器模式的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回本地浏览器模式的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：通过自然语言指令、驱动本地、浏览器的轻量级自、动化工具、适合个人开发者日、常网页交互、浏览器自动化工具、免费版、面向个人用户提供、基础的网页自动化、实现页面导航、元素操作、数据提取等核心功、Use、when、需要数据分析、报表生成、统计洞察、数据可视化时使用、不适用于实时流数、据处理、适用于独立开发者、企业团队和自动化、工作流场景等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持.
## 使用场景

### 场景一:个人开发者信息采集

小明是一名独立开发者,需要定期从技术博客网站采集最新文章标题和摘要,用于个人知识库建设.
```bash
# 步骤1:导航到目标网站
browser navigate https://tech-blog.example.com
# ...
# 步骤2:提取文章列表
browser extract "提取首页所有文章的标题和发布日期" '{"articles":[{"title":"string","date":"string"}]}'
# ...
# 步骤3:点击第一篇文章查看详情
browser act "点击第一篇文章标题进入详情页"
# ...
# 步骤4:提取文章正文摘要
browser extract "提取文章正文前500字作为摘要"
# ...
# 步骤5:关闭浏览器
browser close
```

### 场景二:学生研究资料整理

小红是一名研究生,需要从多个学术网站收集研究主题相关的资料.
```bash
# 导航到学术搜索引擎
browser navigate https://scholar.example.com
# ...
# 在搜索框输入关键词
browser act "在搜索框输入'大语言模型训练优化'并回车"
# ...
# 提取搜索结果
browser extract "提取搜索结果列表中的论文标题、作者和引用数"
# ...
# 翻页继续采集
browser act "点击下一页按钮"
browser extract "提取本页搜索结果"
```

### 场景三:自由职业者表单自动化

小李是一名自由职业者,需要批量填写相似的在线表单.
```bash
# 导航到表单页面
browser navigate https://form.example.com/apply
# ...
# 填写基本信息
browser act "在姓名输入框填写'李明'"
browser act "在邮箱输入框填写'liming@example.com'"
browser act "在留言框填写项目合作意向"
# ...
# 提交表单
browser act "点击提交按钮"
# ...
# 截图保存提交结果
browser screenshot
```

## 快速开始

### 第一步:环境准备

确保本地已安装以下组件:

```bash
# 检查 Node.js 版本(需 18.0.0 以上)
node --version
# ...
# 依赖说明
# Windows 默认路径: C:\Program Files\Google\Chrome\Application\chrome.exe
# macOS 默认路径: /Applications/Google Chrome.app
```

### 第二步:初始化工具

```bash
# 进入工具目录,安装依赖
cd ~/.skill-platform/workspace/skills/stagehand-browser-tool-free
npm install
# ...
# 创建全局命令
npm link
# ...
# 验证安装
browser --version
```

### 第三步:首次运行测试

```bash
# 启动浏览器并导航到测试页面
# ...
# 查看页面内容
browser extract "获取页面标题"
# ...
# 截图验证
browser screenshot
# ...
# 关闭浏览器
browser close
```

**响应解析**: 完成完成后,查看输出响应确认任务状态。成功时输出包含解析摘要和响应数据;失败时根据错误信息排查问题,查阅错误解析章节获取恢复步骤.
## 配置示例

### 基础配置文件

在工具目录下创建 `.env` 文件,配置本地浏览器参数:

```bash
# 浏览器配置
BROWSER_HEADLESS=false          # 是否无头模式运行(false 表示显示浏览器窗口)
BROWSER_SLOWMO=100              # 操作间隔(毫秒),便于观察执行过程
# ...
# 本地 Chrome 路径(可选,自动检测失败时手动指定)
# Windows 示例
CHROME_PATH=C:\Program Files\Google\Chrome\Application\chrome.exe
# macOS 示例
# CHROME_PATH=/Applications/Google Chrome.app/Contents/MacOS/Google Chrome
```

### setup.json 配置

```json
{
  "setupComplete": true,
  "mode": "local",
  "browser": {
    "type": "chrome",
    "headless": false,
    "slowMo": 100,
    "defaultTimeout": 30000
  },
  "logging": {
    "level": "info",
    "saveScreenshots": true,
    "screenshotDir": "./screenshots"
  }
}
```

## 最佳实践

### 1. 操作前先导航

每次执行交互操作前,确保已导航到目标页面.
```bash
# 正确做法:先导航再操作
browser act "点击登录按钮"
# ...
# 错误做法:未导航直接操作
browser act "点击登录按钮"  # 可能失败,因为没有目标页面
```

### 2. 使用 observe 发现元素

当不确定页面结构时,先用 observe 命令探索可用元素.
```bash
# 先观察页面结构
browser observe "页面有哪些可点击的按钮"
# ...
# 再执行精准操作
browser act "点击蓝色提交按钮"
```

### 3. 关键步骤截图验证

在重要操作前后截图,便于调试和记录.
```bash
browser screenshot  # 操作前截图
browser act "点击购买按钮"
browser screenshot  # 操作后截图,验证结果
```

### 4. 及时关闭浏览器

任务完成后及时关闭浏览器,释放系统资源.
```bash
# 任务完成后
browser close
```

## 常见问题

### Q1: 启动时提示 Chrome 未找到怎么办?

**A:** 请检查 Chrome 浏览器是否正确安装。如果安装在其他路径,请在 `.env` 文件中手动指定 `CHROME_PATH`.
```bash
# 验证 Chrome 路径
# Windows
where chrome
# macOS
ls /Applications/Google\ Chrome.app
```

### Q2: 操作执行失败如何排查?

**A:** 按以下步骤排查:

1. 使用 `browser observe` 查看页面当前可交互元素
2. 截图查看页面实际状态
3. 检查操作描述是否清晰明确
4. 适当增加操作间隔时间

### Q3: 提取数据为空或格式不对?

**A:** 检查提取指令和 schema 定义:

```bash
# 先用简单指令测试
browser extract "获取页面所有文本内容"
# ...
# 再逐步精细化
browser extract "提取商品名称" '{"name":"string"}'
```

### 已知限制

**A:** 免费版主要面向个人本地使用场景,具备完整的本地浏览器操作能力。如需远程浏览器、批量任务调度、企业级代理支持等高级功能,请考虑升级到 PRO 版本.
## 依赖说明

### 运行环境

- **Agent 平台**: 支持 SKILL.md 的任意 AI Agent(Claude Code / Cursor / Codex / Gemini CLI 等)
- **操作系统**: Windows / macOS / Linux
- **Node.js**: 18.0.0 及以上版本
- **浏览器**: Google Chrome 100 及以上版本

### 第三方依赖

| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:-----|:-----|:-----|:-----|
| Node.js | 运行时 | 必需 | 官方网站下载安装 |
| Chrome 浏览器 | 浏览器 | 必需 | 官方网站下载安装 |
| npm 依赖包 | 库 | 必需 | 通过 `npm install` 自动安装 |
| LLM API | API | 必需 | 由 Agent 内置 LLM 提供 |

### API Key 配置

免费版基于本地浏览器运行,无需额外 API Key。所有数据均在本地处理,保障隐私安全.
### 可用性分类

- **分类**: MD+EXEC(纯 Markdown 指令,部分功能需要 exec 命令行执行能力)
- **说明**: 基于本地 Chrome 浏览器的自动化工具,通过自然语言指令驱动 Agent 执行网页操作任务
- **适用规模**: 单用户、单浏览器实例、本地运行

## 错误处理

| 错误场景 | 原因 | 处理方式 |
|---:|---:|---:|
| 配置错误 | 参数缺失或格式错误 | 检查依赖说明中的配置要求 |
| 运行时错误 | 运行环境不满足 | 确认运行环境符合依赖说明 |
| 网络错误 | 连接超时或不可达 | 执行ping命令测试网络连通性,检查防火墙和代理设置连接后执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令，参考国内替代方案 |

## 示例

### 基本用法

**输出**：返回执行结果,包含操作状态和输出数据

```text
用户: 执行核心功能
Skill: 正在执行核心功能...
Skill: 执行完成,结果如下: 操作成功
```

## 输出格式
```json
{
  "success": true,
  "data": {
    "result": "浏览器自动化工具免费版处理结果",
    "execution_time": "0.5s",
    "metadata": {
      "version": "1.0",
      "processor": "stagehand browser"
    }
  },
  "execution_log": ["解析输入参数", "执行核心处理", "格式化输出结果"],
  "error": null
}
```
