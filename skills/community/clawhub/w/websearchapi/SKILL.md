---
name: websearchapi
description: "网页/新闻/财经/视频/地图/酒店/航班搜索工具，基于 SearchAPI (Google)。支持多种搜索类型，适合 Agent 获取实时网络信息。"
metadata: { "openclaw": { "emoji": "🔍", "requires": { "bins": ["node"] } } }
---

# WebSearchAPI

基于 SearchAPI (Google) 的多类型搜索工具，适合 Agent 获取实时网络信息。

## 功能特点

- **多种搜索类型**: 网页、新闻、视频、财经、地图、酒店、航班
- **自动重试**: 网络错误自动重试，提高稳定性
- **结构化返回**: Agent 直接可用的 JSON 格式
- **零外部依赖**: 纯 Node.js 内置模块

## 安装

```bash
# 复制 tools/websearchapi 目录到你的项目
# 配置 API Key
cd tools/websearchapi
node websearchapi.js config set-key YOUR_API_KEY
```

API Key 获取: https://searchapi.io (免费注册)

## 使用方法

使用 `exec` 工具调用：

```bash
node <path>/websearchapi.js <命令> [关键词] [选项]
```

### 搜索类型

| 类型 | 命令 | 说明 |
|------|------|------|
| 网页 | `s` 或 `search` | 通用网页搜索 |
| 新闻 | `news` | 最新新闻 |
| 视频 | `video` | 视频搜索 |
| 财经 | `finance` | 股票/金融信息 |
| 地图 | `maps` | 地点/商户 |
| 酒店 | `hotels` | 酒店搜索 |
| 航班 | `flights` | 航班搜索 |

### 选项

| 选项 | 说明 | 默认值 |
|------|------|--------|
| `--num` | 结果数量 | 5 |
| `--lang` | 语言 | zh-CN |
| `--gl` | 地区 | cn |
| `--json` | JSON 格式输出 | 文本 |

## Agent 调用示例

```bash
# 网页搜索
node websearchapi.js s "MCP 协议"

# 新闻搜索
node websearchapi.js news "人工智能"

# 财经搜索 (用股票代码)
node websearchapi.js finance "AAPL"

# JSON 格式 (推荐，便于解析)
node websearchapi.js s "关键词" --json
```

## 返回格式

JSON 模式返回：

```json
{
  "success": true,
  "query": "关键词",
  "type": "google",
  "count": 5,
  "results": [
    {
      "title": "结果标题",
      "link": "链接地址",
      "snippet": "摘要内容",
      "source": "来源"
    }
  ],
  "metadata": {
    "totalResults": 数量,
    "timeTaken": 耗时,
    "engine": "google"
  }
}
```

## 配置

### 查看配置

```bash
node websearchapi.js config
```

### 设置 API Key

```bash
node websearchapi.js config set-key YOUR_API_KEY
```

### 修改默认选项

```bash
node websearchapi.js config set-num 10      # 默认结果数
node websearchapi.js config set-lang en     # 默认语言
node websearchapi.js config set-gl us       # 默认地区
node websearchapi.js config set-retry 5     # 重试次数
```

## 迁移部署

将整个 tools 目录复制到新机器：

```bash
# 复制到新机器
scp -r ./tools/websearchapi user@new-server:/path/to/tools/

# 配置 API Key
cd /path/to/tools/websearchapi
node websearchapi.js config set-key YOUR_API_KEY

# 测试
node websearchapi.js test
```

## 故障排除

### 搜索失败
- 检查 API Key 是否正确: `node websearchapi.js config`
- 检查网络连接

### 财经搜索无结果
- 尝试用股票代码: `finance "AAPL"`
- 尝试英文: `finance "Tesla stock"`

### 请求超时
- 网络较慢时可增加重试次数: `config set-retry 5`
