---
name: ai-topic-scout
description: AI短视频选题追踪系统。自动抓取指定YouTube博主视频和Twitter博主推文，分析内容，聚合跨平台热点主题，生成带热度评分和选题建议的分析报告，结果写入钉钉AI表格。适用于：定时抓取AI领域博主内容、分析短视频选题热度、跨平台话题聚合、生成选题建议。触发词："抓取选题"、"分析选题"、"选题scout"、"topic scout"、"抓取博主内容"、"选题分析"。
---

# AI短视频选题追踪系统

## 依赖安装

首次使用前，检查并安装所有依赖。按顺序执行：

### 1. CLI 工具

```bash
# mcporter — MCP Server 调用工具
npm install -g mcporter

# bird — Twitter/X CLI
npm install -g @steipete/bird

# yt-dlp — YouTube 视频/字幕下载
pip install yt-dlp
```

### 2. 依赖技能（通过 clawhub 安装）

```bash
# 钉钉 AI 表格操作
clawhub install dingtalk-ai-table

# YouTube 字幕抓取
clawhub install youtube-watcher
```

> 如果 clawhub 未安装：`npm install -g clawhub`

### 3. 环境配置

**钉钉 MCP Server**：
1. 打开 https://mcp.dingtalk.com/#/detail?mcpId=9555&detailType=marketMcpDetail
2. 点击「获取 MCP Server 配置」，复制 Streamable HTTP URL
3. 注册到 mcporter：
```bash
mcporter config add dingtalk-ai-table --url "<你的URL>"
```

**Twitter Cookie**：
1. 在浏览器登录 x.com，从 DevTools → Application → Cookies 获取 `auth_token` 和 `ct0`
2. 配置到 `~/.config/bird/config.json5`：
```json5
{
  authToken: "<你的auth_token>",
  ct0: "<你的ct0>"
}
```
> ⚠️ 当前版本 bird 不会自动读取 config.json5，CLI 调用时仍需通过 `--auth-token` 和 `--ct0` 参数传入。

### 4. 验证安装

```bash
mcporter --version
mcporter list dingtalk-ai-table --schema   # 确认出现 list_bases / create_records 等新版 tools
bird check
yt-dlp --version
```

## 数据架构

### 钉钉AI表格结构

Base 名称：`AI短视频选题`

需要 4 张数据表，首次运行时自动创建（参见 `references/setup-guide.md`）：

| 表名 | 用途 |
|------|------|
| YouTube博主 | 追踪的油管频道列表 |
| Twitter博主 | 追踪的推特账号列表 |
| 抓取内容 | 原始抓取记录（视频/推文） |
| 选题分析 | 聚合分析后的选题 |

表结构详见 `references/table-schema.md`。

## 工作流

### 一、首次初始化

仅第一次使用时执行，步骤详见 `references/setup-guide.md`：

1. 创建钉钉AI表格 Base
2. 创建 4 张数据表（含字段定义）
3. 填入初始博主列表
4. 将 baseId 和各 tableId 保存到 `references/config.json`

### 二、定时抓取（每小时执行）

按顺序执行：

#### 1. 读取配置

```bash
cat {baseDir}/references/config.json
```

读取 baseId、各 tableId、各字段 fieldId。

#### 2. 抓取 YouTube 内容

对「YouTube博主」表中状态为「活跃」的每个博主：

```bash
# 获取最新3个视频ID
yt-dlp --flat-playlist --print "%(id)s %(title)s" -I 1:3 "https://www.youtube.com/@{频道ID}/videos"

# 对每个视频，先检查 fetch 表是否已存在（用原文链接去重）
mcporter call dingtalk-ai-table query_records --args '{
  "baseId":"<baseId>","tableId":"<fetchTableId>",
  "keyword":"youtube.com/watch?v=<videoId>"
}' --output json

# 如果不存在，抓取字幕
python3 {youtube-watcher-baseDir}/scripts/get_transcript.py "https://www.youtube.com/watch?v=<videoId>"

# 用字幕内容生成摘要，写入 fetch 表
```

#### 3. 抓取 Twitter 内容

对「Twitter博主」表中状态为「活跃」的每个博主：

```bash
bird user-tweets @{用户名} -n 5 --plain --auth-token "<token>" --ct0 "<ct0>"
```

对每条推文，检查 fetch 表是否已存在（用原文链接去重），新内容写入 fetch 表。

#### 4. 写入 fetch 表的格式

```bash
mcporter call dingtalk-ai-table create_records --args '{
  "baseId":"<baseId>",
  "tableId":"<fetchTableId>",
  "records":[{
    "cells":{
      "<来源fieldId>":"YouTube 或 Twitter",
      "<博主名称fieldId>":"博主名",
      "<标题fieldId>":"内容标题",
      "<内容摘要fieldId>":"200字以内摘要",
      "<原文链接fieldId>":"完整URL",
      "<发布时间fieldId>":"YYYY-MM-DD",
      "<抓取时间fieldId>":"YYYY-MM-DD HH:mm",
      "<内容类型fieldId>":"视频/推文/长推文/转推评论",
      "<关键词标签fieldId>":"逗号分隔的标签",
      "<处理状态fieldId>":"待分析"
    }
  }]
}' --output json
```

### 三、选题分析（每次抓取后执行）

#### 1. 读取待分析内容

```bash
mcporter call dingtalk-ai-table query_records --args '{
  "baseId":"<baseId>","tableId":"<fetchTableId>",
  "filters":{"operator":"and","operands":[
    {"operator":"eq","operands":["<处理状态fieldId>","<待分析optionId>"]}
  ]}
}' --output json
```

#### 2. 主题聚合

分析所有「待分析」记录，按以下规则聚合成选题：

- **关键词匹配**：相同关键词标签的内容归为同一选题
- **语义相似**：标题或摘要讨论同一事件/技术的合并
- **跨平台加权**：YouTube + Twitter 同时出现的话题热度更高

#### 3. 热度评分规则

满分 100，计算维度：

| 维度 | 权重 |
|------|------|
| 相关内容数量 | 25% |
| 跨平台覆盖（YouTube+Twitter都有） | 20% |
| 跨博主覆盖（多人提到） | 20% |
| 内容深度（长推文/视频 vs 短推文） | 15% |
| 时效性（越新越高） | 10% |
| 主流媒体报道（通过搜索验证） | 10% |

#### 4. 搜索背景信息

对每个选题用可用的搜索工具（如 Tavily、web search 等）补充背景知识。搜索关键词 + 当前年份，取新闻类结果。

#### 5. 生成选题建议

每条选题包含：

- 🎯 **目标受众** — 这个视频谁会看
- ⏱ **建议时长** — 短视频多长合适
- 📐 **内容结构** — 分几段讲什么（3-5个要点）
- **多个标题参考** — 至少3个不同角度的标题

#### 6. 写入选题分析表

```bash
mcporter call dingtalk-ai-table create_records --args '{
  "baseId":"<baseId>",
  "tableId":"<analysisTableId>",
  "records":[{
    "cells":{
      "<主题fieldId>":"emoji + 主题标题",
      "<热度评分fieldId>":85,
      "<相关内容数fieldId>":3,
      "<来源博主fieldId>":"博主1, 博主2",
      "<主题分类fieldId>":"大模型/AI应用/AI编程/AI硬件/AI政策/AI创业/AI开源/其他",
      "<背景信息fieldId>":"背景描述...",
      "<选题建议fieldId>":"完整建议...",
      "<分析时间fieldId>":"YYYY-MM-DD HH:mm",
      "<状态fieldId>":"待审核"
    }
  }]
}' --output json
```

#### 7. 设置关联

**关键**：关联字段写入必须用 `{"linkedRecordIds":[...]}` 格式，不能直接传数组：

```bash
mcporter call dingtalk-ai-table update_records --args '{
  "baseId":"<baseId>",
  "tableId":"<analysisTableId>",
  "records":[{
    "recordId":"<选题recordId>",
    "cells":{
      "<相关内容fieldId>":{"linkedRecordIds":["<fetchRecordId1>","<fetchRecordId2>"]}
    }
  }]
}' --output json
```

#### 8. 更新 fetch 记录状态

将已关联到选题的 fetch 记录标记为「已分析」。
对不值得做选题的内容（非AI相关、过于轻量）标记为「已忽略」。

## 踩坑记录

详见 `references/gotchas.md`，包含钉钉 API 的坑和 bird/yt-dlp 使用注意事项。

## 主题分类选项

- 大模型（GPT/Claude/Gemini/开源模型等）
- AI应用（自动驾驶/医疗/教育/创意工具等）
- AI编程（Copilot/Codex/代码生成等）
- AI硬件（GPU/芯片/机器人/传感器等）
- AI政策（监管/伦理/安全/就业影响等）
- AI创业（融资/新公司/商业模式等）
- AI开源（开源模型/框架/数据集等）
- 其他

## 聚合策略补充

当同一话题被多条内容覆盖时，将相关内容全部关联到同一选题。选题标题应反映聚合后的更大视角，而非单条内容的标题。

示例：Sam Altman 的 GPT-5.4 推文 + Codex Security 转推 + NVIDIA 算力扩展推文 + Mollick 的算力经济学分析 → 聚合为「OpenAI一周三连发：GPT-5.4 + Codex Security + 算力军备竞赛」
