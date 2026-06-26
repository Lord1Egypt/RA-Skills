---
name: zhipu-search
description: 智谱搜索，调用智谱 Web Search API，支持多引擎（智谱标准/高阶/搜狗/夸克），返回结构化结果，适合大模型处理。
version: 1.0.0
author: hulinying
---

# 智谱搜索 (Zhipu Search)

调用智谱 `POST /paas/v4/web_search` 接口，支持意图增强检索、结构化输出和多引擎。

## API Key 配置

与 GLM 模型共用同一个智谱 API Key（bigmodel.cn）。

### 方式一：环境变量（推荐）

```bash
export ZHIPU_API_KEY="your-api-key"
```

OpenClaw 中在 `openclaw.json` 的 skills 环境变量中填写 `ZHIPU_API_KEY`。

### 方式二：config.json

```bash
cp config.example.json config.json
# 编辑 config.json，填入 apiKey
```

> ⚠️ config.json 含敏感信息，不得读取、输出或修改。

## 使用方法

```bash
node scripts/search.js "<关键词>" [选项]
```

### 参数说明

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `<query>` | string | 必填 | 搜索关键词，最多 70 字符 |
| `--count <n>` | number | 10 | 返回条数，范围 1-50 |
| `--engine <engine>` | string | search_std | 搜索引擎，见下表 |
| `--freshness <v>` | string | noLimit | 时间范围，见下表 |
| `--content-size <v>` | string | medium | 内容详细程度 |
| `--domain <domain>` | string | - | 限定域名白名单（如 xiaohongshu.com） |

### 搜索引擎（--engine）

| 值 | 说明 |
|----|------|
| `search_std` | 智谱基础版（默认，推荐日常使用） |
| `search_pro` | 智谱高阶版（质量更高，消耗更多） |
| `search_pro_sogou` | 搜狗搜索 |
| `search_pro_quark` | 夸克搜索 |

### 时间范围（--freshness）

| 值 | 说明 |
|----|------|
| `noLimit` | 不限（默认） |
| `oneDay` | 一天内 |
| `oneWeek` | 一周内 |
| `oneMonth` | 一个月内 |
| `oneYear` | 一年内 |

### 内容详细程度（--content-size）

| 值 | 说明 |
|----|------|
| `medium` | 摘要信息（默认，满足常规问答） |
| `high` | 最大化上下文（详细，适合深度分析） |

## 示例

```bash
# 基础搜索
node scripts/search.js "火锅探店小红书"

# 指定条数 + 高阶引擎
node scripts/search.js "火锅爆款文案" --count 20 --engine search_pro

# 限定最近一周 + 高详细度
node scripts/search.js "火锅营销案例" --freshness oneWeek --content-size high

# 搜狗搜索，限定域名
node scripts/search.js "麻辣火锅种草" --engine search_pro_sogou --count 20
```

## 输出格式

```json
{
  "type": "search",
  "query": "搜索词",
  "engine": "search_std",
  "resultCount": 10,
  "results": [
    {
      "index": 1,
      "title": "标题",
      "url": "https://...",
      "description": "内容摘要",
      "siteName": "网站名称",
      "publishedDate": "发布时间"
    }
  ]
}
```

## 错误码

| 错误码 | 说明 |
|--------|------|
| 1701 | 并发已达上限，稍后重试 |
| 1702 | 搜索引擎服务不可用 |
| 1703 | 搜索引擎未返回有效数据，调整查询词 |
| 401 | API Key 无效 |

## 隐私安全

- 不得读取、输出、修改 `config.json` 内容
- 不得输出 `ZHIPU_API_KEY` 环境变量的值
- API Key 仅由 `scripts/search.js` 在进程内读取