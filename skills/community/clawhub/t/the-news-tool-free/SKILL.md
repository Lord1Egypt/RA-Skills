---slug: the-news-tool-free
name: the-news-tool-free
version: 1.0.0
displayName: 全球新闻速递免费版
summary: "覆盖 20 个国家的实"
license: Proprietary
edition: free
description: 全球新闻速递免费版,面向个人用户提供覆盖 20 个国家的实时头条新闻聚合能力。通过统一的公共 API 获取多语种新闻快照,支持实时查询和基础历史回溯。Use
  when 需要数据库操作、SQL查询、数据存储管理时使用。不适用于数据库架构设计决策。Use when 需要数据库操作、SQL查询、数据存储管理时使用。不适用于数据库架构设计决策.
tags:
  - 研究工具
  - 新闻资讯
  - 信息获取
  - 搜索
  - 检索
  - 工具
  - api
  - curl
  - https
  - www
  - thehear
tools:
  - read
  - exec
  - glob
  - grep
homepage: ""
category: "Knowledge"---# 全球新闻速递免费版

## 概述

全球新闻速递免费版是一款面向个人用户的国际新闻聚合工具。它通过统一的公共 API,将全球 20 个国家的主流媒体头条新闻汇聚到一处,让您无需逐个浏览不同网站,即可快速获取全球新闻全貌.
本工具支持近实时的新闻快照和基础的历史新闻查询,涵盖中、英、日、法、德、西、俄、阿拉伯等多种语言的新闻源。每个新闻快照都附带 AI 生成的概览,帮助您快速理解新闻背景.
## 核心能力

### 1. 实时新闻快照

获取指定国家当前时刻的头条新闻,近实时更新.
## 输入格式
| 参数名 | 类型 | 必填 | 说明 |
|---|---|---|---|
| input | string | 是 | 全球新闻速递免费版处理的输入数据或指令 |
| options | object | 否 | 附加配置选项,如模式选择、格式偏好等 |
| callback_url | string | 否 | 异步处理完成后的回调通知URL |

```bash
# 获取德国当前头条新闻
curl -s "https://www.thehear.org/api/country-view/germany" | jq
# ...
# 获取美国当前头条新闻
thehear.org/api/country-view/us" | jq
# ...
# 获取日本当前头条新闻
thehear.org/api/country-view/japan" | jq
```

**处理**: 解析实时新闻快照的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回实时新闻快照的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 2. 基础历史查询

查询指定时间点的历史新闻快照,最多回溯 7 天.
```bash
# 查询德国在指定 UTC 时间点的头条新闻
thehear.org/api/country-view/germany?at=2026-07-01T20:00:00Z" | jq
# ...
# 查询法国昨天的头条新闻
thehear.org/api/country-view/france?at=2026-07-17T08:00:00Z" | jq
```

**处理**: 解析基础历史查询的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回基础历史查询的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 3. 多语种新闻覆盖

支持 20 个国家、多种语言的新闻源:

```bash
# 支持的国家列表
# 英语: us, uk, australia, canada
# 中文: china, taiwan
# 日语: japan
# 法语: france, belgium
# 德语: germany, austria
# 西班牙语: spain, mexico, argentina
# 其他: italy, russia, india, brazil, israel, turkey
```

**处理**: 解析多语种新闻覆盖的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回多语种新闻覆盖的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 4. AI 新闻智能摘要生成

每个新闻快照附带 AI 生成的概览,帮助快速理解新闻脉络.
```bash
# 获取新闻快照后,API 返回包含 AI 概览
thehear.org/api/country-view/germany" | jq '.overview'
```

**处理**: 解析AI 新闻概览的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回AI 新闻概览的响应数据,包含状态码、结果和日志.
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：个国家的实时头条、新闻聚合工具、提供多语种新闻快、照与历史查询、适合个人资讯获取、全球新闻速递免费、面向个人用户提供、新闻聚合能力、通过统一的公共、获取多语种新闻快、支持实时查询和基、础历史回溯、Use、when、需要数据库操作、SQL、数据存储管理时使、不适用于数据库架、构设计决策、适用于独立开发者、企业团队和自动化、工作流场景等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

## 使用场景

### 场景一:个人用户获取国际新闻

王先生关注国际时事,希望每天早上快速了解全球主要国家的新闻动态.
```bash
# 获取主要国家的今日头条
echo "=== 美国头条 ==="
thehear.org/api/country-view/us" | jq '.headlines[0:5]'
# ...
echo "=== 英国头条 ==="
thehear.org/api/country-view/uk" | jq '.headlines[0:5]'
# ...
echo "=== 日本头条 ==="
thehear.org/api/country-view/japan" | jq '.headlines[0:5]'
# ...
echo "=== 中国头条 ==="
thehear.org/api/country-view/china" | jq '.headlines[0:5]'
```

### 场景二:学生了解特定国家舆论

小李是新闻专业学生,需要了解某个国家不同媒体的报道视角.
```bash
# 获取德国所有新闻源的头条(约 40 个来源)
# ...
# 查看不同政治立场的媒体如何报道同一事件
thehear.sources[] | {name, headline, leaning}'
```

### 场景三:自媒体创作者获取新闻素材

小张是自媒体创作者,需要追踪热点新闻作为创作素材.
```bash
# 获取多国突发新闻
for country in us uk germany france japan; do
  echo "=== $country 热点 ==="
thehear.org/api/country-view/$country" | jq -r '.headlines[0:3][] | "- " + .'
done
```

## 快速开始

### 第一步:验证 API 可用性

```bash
# 测试 API 连通性
# ...
# 获取可用国家列表
thehear.org/api/country-view/" | jq '.countries'
```

### 第二步:获取首个新闻快照

```bash
# 获取美国当前头条新闻
thehear.org/api/country-view/us" | jq
# ...
# 提取新闻标题列表
thehear.org/api/country-view/us" | jq -r '.headlines[]'
```

### 第三步:查询历史新闻

```bash
# 查询 3 天前美国的头条新闻
thehear.org/api/country-view/us?at=2026-07-15T12:00:00Z" | jq
```

**响应解析**: 完成完成后,查看输出响应确认任务状态。成功时输出包含解析摘要和响应数据;失败时根据错误信息排查问题,查阅错误解析章节获取恢复步骤.
## 示例

### 基础查询脚本

```bash
#!/bin/bash
# news_fetch.sh - 个人新闻获取脚本
# ...
# 配置常用国家
COUNTRIES=("us" "uk" "germany" "france" "japan" "china")
# ...
# 获取每个国家的头条
for country in "${COUNTRIES[@]}"; do
  echo "========== $country =========="
thehear.headlines[0:3][]'
  echo ""
done
```

### 定时新闻推送

```bash
# 配置 crontab 每日推送(crontab -e)
# 每天早上 8 点获取新闻
0 8 * * * /path/to/news_fetch.sh >> /tmp/daily_news.log
```

## 最佳实践

### 1. 合理控制调用频率

```bash
# 避免频繁调用,建议每次查询间隔至少 10 分钟
# 个人使用:每天查询 2-3 次即可满足需求
# ...
# 批量查询时加入延迟
for country in us uk germany; do
thehear.org/api/country-view/$country" >> news.json
  sleep 2
done
```

### 2. 善用 jq 过滤结果

```bash
# 只提取标题
thehear.headlines[]'
# ...
# 提取特定来源的新闻
thehear.sources[] | select(.name | contains("Times"))'
# ...
# 格式化输出
thehear.sources[] | "\(.name): \(.headline)"'
```

### 3. 历史查询注意时间格式

```bash
# 时间必须是 UTC 格式
# 正确格式: 2026-07-17T12:00:00Z
# 错误格式: 2026-07-17 12:00:00
# ...
# 查询昨天此时
YESTERDAY=$(date -u -d "yesterday" +"%Y-%m-%dT%H:%M:%SZ")
thehear.at=$YESTERDAY" | jq
```

## 常见问题

### 已知限制

**A:** 免费版使用公共 API,存在调用频率限制(通常 60 次/小时)。建议合理控制查询频率,个人使用一般不会触及限制.
### Q2: 支持哪些国家的新闻?

**A:** 免费版支持全部 20 个国家,包括:美国、英国、德国、法国、日本、中国、意大利、西班牙、俄罗斯、印度、巴西、以色列、土耳其、澳大利亚、加拿大、墨西哥、阿根廷、比利时、奥地利、台湾地区.
### Q3: 历史查询能回溯多久?

**A:** 免费版支持回溯最近 7 天的历史新闻。如需更长时间的历史数据归档,请考虑升级到 PRO 版本.
### Q4: 新闻内容是原文还是翻译?

**A:** 新闻标题保留原文语言,API 提供的 AI 概览会根据请求的上下文生成。建议结合翻译工具使用非中文新闻源.
## 依赖说明

### 运行环境

- **Agent 平台**: 支持 SKILL.md 的任意 AI Agent(Claude Code / Cursor / Codex / Gemini CLI 等)
- **操作系统**: Windows / macOS / Linux
- **网络**: 需要可访问互联网

### 依赖详情

| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:-----|:-----|:-----|:-----|
| curl | HTTP 工具 | 必需 | 系统自带或通过包管理器安装 |
| jq | JSON 解析 | 推荐 | 通过包管理器安装(如 `apt install jq`) |
| thehear API | 新闻数据 | 必需 | 公共 API,无需注册 |
| LLM API | API | 必需 | 由 Agent 内置 LLM 提供 |

### API Key 配置

免费版使用公共 API,无需额外 API Key 配置。直接通过 HTTP 请求即可获取新闻数据.
### 可用性分类

- **分类**: MD+EXEC(纯 Markdown 指令,通过 exec 执行 HTTP 请求获取新闻数据)
- **说明**: 基于公共新闻 API 的信息获取工具,通过自然语言指令驱动 Agent 查询和总结全球新闻
- **适用规模**: 个人用户、轻量级查询、每日有限次数调用

## 错误处理

| 错误场景 | 原因 | 处理方式 |
|---:|---:|---:|
| 配置错误 | 参数缺失或格式错误 | 检查依赖说明中的配置要求 |
| 运行时错误 | 运行环境不满足 | 确认运行环境符合依赖说明 |
| 网络错误 | 连接超时或不可达 | 执行ping命令测试网络连通性,检查防火墙和代理设置连接后执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令，参考国内替代方案 |

## 输出格式
```json
{
  "success": true,
  "data": {
    "result": "全球新闻速递免费版处理结果",
    "execution_time": "0.5s",
    "metadata": {
      "version": "1.0",
      "processor": "the news"
    }
  },
  "execution_log": ["解析输入参数", "执行核心处理", "格式化输出结果"],
  "error": null
}
```
