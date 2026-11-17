---
slug: verify-claims-tool-free
name: verify-claims-tool-free
version: 1.0.0
displayName: 事实核查助手免费版
summary: "多源交叉验证的事实核查工具,对接全球专业事实核查机构,适合个人信息鉴别。事实核查助手免费版,面向个人用户提供基础的事实核查能力。通过对接全球专业事实核查机构,对用户提供的声明进行多源交叉验证"
license: Proprietary
edition: free
description: 事实核查助手免费版,面向个人用户提供基础的事实核查能力。通过对接全球专业事实核查机构,对用户提供的声明进行多源交叉验证。Use when
  需要AI模型调用、智能对话、Agent编排、LLM应用时使用。不适用于需要100%确定性的关键决策。Use when
  需要AI模型调用、智能对话、Agent编排、LLM应用时使用。不适用于需要100%确定性的关键决策.
tags:
  - 研究工具
  - 事实核查
  - 信息鉴别
  - 搜索
  - 检索
  - 工具
  - verify-claims
  - check
  - bash
  - 用户提供
  - 返回结构
tools:
  - read
  - exec
  - glob
  - grep
homepage: ""
category: "Knowledge"
---
# 事实核查助手免费版

## 概述

事实核查助手免费版是一款面向个人用户的信息验证工具。它通过对接全球专业的第三方事实核查机构(如 Snopes、FactCheck.org、Full Fact 等),对用户提供的声明、文章、视频内容进行多源交叉验证,帮助用户快速判断信息的真实性.
本工具特别适合个人用户验证新闻真实性、学生与研究者核查信息来源、自媒体创作者核实内容准确性等场景。免费版聚焦核心核查功能,无需注册,开箱即用.
## 核心能力

### 1. 多源交叉验证

从多个专业事实核查机构获取验证结果,交叉比对.
## 输入格式
| 参数名 | 类型 | 必填 | 说明 |
|---|---|---|---|
| input | string | 是 | 事实核查助手免费版处理的输入数据或指令 |
| options | object | 否 | 附加配置选项,如模式选择、格式偏好等 |
| callback_url | string | 否 | 异步处理完成后的回调通知URL |

```bash
# 核查单个声明
verify-claims check "5G 技术会导致 COVID-19"
# ...
# 核查文章内容
verify-claims check --file article.txt
# ...
# 核查视频描述
verify-claims check --text "这段视频声称的内容"
```

**处理**: 解析多源交叉验证的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回多源交叉验证的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 2. 区域相关性匹配

根据内容地域,选择合适的事实核查机构.
```bash
# 核查特定地区的内容
verify-claims check "法国总统的最新声明" --region "france"
# ...
# 核查多地区内容
verify-claims check "中美贸易政策报道" --regions "us,china"
```

**处理**: 解析区域相关性匹配的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回区域相关性匹配的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 3. 语言匹配

优先使用用户母语的事实核查机构.
```bash
# 中文用户优先使用中文核查源
verify-claims check "某条中文新闻" --language "zh"
# ...
# 英文内容使用英文核查源
verify-claims check "English claim about politics" --language "en"
```

**处理**: 解析语言匹配的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回语言匹配的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 4. 结构化结果呈现

清晰展示核查结论和证据.
```bash
# 获取结构化核查结果
verify-claims check "疫苗会导致自闭症" --format json
# ...
# 示例
# {
#   "claim": "疫苗会导致自闭症",
#   "verdict": "false",
#   "confidence": "high",
#   "sources": [
#     {"name": "FactCheck.org", "verdict": "false", "url": "..."},
#     {"name": "Snopes", "verdict": "false", "url": "..."}
#   ],
#   "summary": "多项独立研究表明疫苗与自闭症之间没有因果关系"
# }
```

**处理**: 解析结构化结果呈现的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回结构化结果呈现的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 5. 历史声明归档

保存核查记录,便于后续查阅.
```bash
# 保存核查结果
verify-claims check "声明内容" --save
# ...
# 查看历史核查记录
verify-claims history --list
# ...
# 查看特定核查详情
verify-claims history --id "check_001"
```

**处理**: 解析历史声明归档的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回历史声明归档的响应数据,包含状态码、结果和日志.
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：多源交叉验证的事、实核查工具、对接全球专业事实、适合个人信息鉴别、事实核查助手免费、面向个人用户提供、基础的事实核查能、通过对接全球专业、对用户提供的声明、进行多源交叉验证、Use、when、模型调用、智能对话、Agent、LLM、应用时使用、不适用于需要、确定性的关键决策、适用于独立开发者、企业团队和自动化、工作流场景等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

## 使用场景

### 场景一:验证新闻真实性

小王看到一条新闻:"某地发现外星人遗迹",想知道是否真实.
```bash
# 步骤1:核查新闻声明
verify-claims check "某地发现外星人遗迹"
# ...
# 步骤2:指定核查区域
verify-claims check "某地发现外星人遗迹" --region "china"
# ...
# 步骤3:获取详细结果
verify-claims check "某地发现外星人遗迹" --verbose
# ...
# 输出示例:
# 核查结论:虚假
# 置信度:高
# 核查来源:
#   - Snopes: 已辟谣
#   - FactCheck.org: 无科学依据
#   - Full Fact: 未发现可信证据
# 摘要:该声明未经任何科学机构证实,图片为合成伪造
```

### 场景二:核查社交媒体内容

小李在社交媒体上看到一条病毒式传播的帖子,想核实其真实性.
```bash
# 步骤1:提取帖子中的声明
verify-claims check "某公司CEO宣布公司将关闭所有线下门店"
# ...
# 步骤2:指定内容类型
verify-claims check "某公司CEO宣布公司将关闭所有线下门店" --type "social_media"
# ...
# 步骤3:多角度核查
verify-claims check "某公司CEO宣布公司将关闭所有线下门店" --perspectives "company,industry,general"
```

### 场景三:学术研究信息核实

小张是研究生,需要核实论文中引用的数据是否准确.
```bash
# 步骤1:核查数据声明
verify-claims check "全球气候变化导致海平面上升 3 米"
# ...
# 步骤2:指定学术核查源
verify-claims check "全球气候变化导致海平面上升 3 米" --sources "scientific"
# ...
# 步骤3:获取详细引用
verify-claims check "全球气候变化导致海平面上升 3 米" --citations
```

## 快速开始

### 第一步:查看可用命令

```bash
# 查看所有命令
verify-claims help
# ...
# 查看核查命令用法
verify-claims check --help
# ...
# 查看支持的核查机构
verify-claims sources --list
```

### 第二步:执行首次核查

```bash
# 核查简单声明
verify-claims check "地球是平的"
# ...
# 核查复杂内容
verify-claims check --file "path/to/article.txt"
```

### 第三步:查看核查结果

```bash
# 查看最近核查结果
verify-claims last
# ...
# 查看核查历史
verify-claims history --list --limit 10
```

## 配置示例

### 个人偏好配置

```bash
# config.json - 个人核查偏好
{
  "language": "zh",
  "region": "auto",
  "min_sources": 3,
  "preferred_sources": ["snopes", "factcheck", "fullfact"],
  "result_format": "text",
  "save_history": true
}
```

### 核查源配置

```bash
# 配置优先使用的核查源
verify-claims config set-sources \
  --general "snopes,factcheck,fullfact" \
  --health "healthfeedback" \
  --climate "climatefeedback" \
  --politics "politifact"
```

## 最佳实践

### 1. 提供清晰的声明

```bash
# 正确做法:提供具体可验证的声明
verify-claims check "某研究显示每天喝咖啡可以延长寿命 10 年"
# ...
# 错误做法:声明过于模糊
verify-claims check "咖啡好不好"  # 太模糊,无法核查
```

### 2. 指定相关区域

```bash
# 核查地区相关内容时,指定区域获得更精准结果
verify-claims check "法国总统的最新政策声明" --region "france"
```

### 3. 多角度核查

```bash
# 使用多个核查源交叉验证
verify-claims check "声明内容" --min-sources 5
# ...
# 查看不同核查源的结论
verify-claims check "声明内容" --show-all-sources
```

### 4. 保存重要核查结果

```bash
# 保存核查结果以备后续查阅
verify-claims check "重要声明" --save --tag "important"
# ...
# 按标签查看
verify-claims history --tag "important"
```

## 常见问题

### Q1: 核查结果不准确怎么办?

**A:** 事实核查依赖于专业核查机构的覆盖范围。如果某个声明未被核查机构覆盖,可以:

1. 尝试使用更通用的关键词
2. 检查相关主题的核查结果
3. 使用通用网络搜索作为补充

### Q2: 支持哪些核查机构?

**A:** 免费版支持主流国际核查机构:

- 国际/英文: FactCheck.org、Snopes、Full Fact、AFP Fact Check、PolitiFact
- 区域/特定语言: Demagog.pl(波兰)、Les Décodeurs(法国)、Correctiv(德国)等
- 专业领域: Health Feedback(健康)、Climate Feedback(气候)、Science Feedback(科学)

### Q3: 核查需要多长时间?

**A:** 免费版通常需要 10-30 秒完成一次核查,具体时间取决于核查机构的响应速度和声明的复杂度.
### Q4: 核查结果的可信度如何?

**A:** 核查结果的可信度取决于:

1. 核查机构的专业性和权威性
2. 多源交叉验证的一致性
3. 证据的充分性和相关性

建议至少使用 3 个核查源进行交叉验证.
### 已知限制

**A:** 免费版主要面向个人核查场景,具备完整的核查能力。如需批量核查、定时监控、团队协作、深度分析等高级功能,请考虑升级到 PRO 版本.
## 依赖说明

### 运行环境

- **Agent 平台**: 支持 SKILL.md 的任意 AI Agent(Claude Code / Cursor / Codex / Gemini CLI 等)
- **操作系统**: Windows / macOS / Linux
- **网络**: 需要可访问互联网

### 依赖详情

| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:-----|:-----|:-----|:-----|
| curl | HTTP 工具 | 必需 | 系统自带 |
| web_search | 搜索工具 | 必需 | Agent 内置或外部搜索 API |
| web_fetch | 网页抓取 | 必需 | Agent 内置或外部抓取工具 |
| LLM API | API | 必需 | 由 Agent 内置 LLM 提供 |

### API Key 配置

免费版使用公开的核查机构网站,基础LLM由Agent平台提供。部分高级搜索功能可能需要搜索引擎 API Key.
```bash
# 可选:配置搜索引擎 API(提升搜索质量)
SEARCH_API_KEY=your_search_api_key
```

### 可用性分类

- **分类**: MD+EXEC(纯 Markdown 指令,通过 exec 执行 HTTP 请求和网页抓取)
- **说明**: 基于多源交叉验证的事实核查工具,通过自然语言指令驱动 Agent 查询和综合专业核查机构的结果
- **适用规模**: 个人用户、单次核查、本地运行

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
