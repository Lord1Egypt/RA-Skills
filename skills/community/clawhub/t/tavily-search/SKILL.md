---
name: tavily-search
version: 1.0.0
description: Tavily AI 搜索工具，专为AI Agent设计的联网搜索能力，支持实时搜索、深度研究、图片搜索、引用生成，返回结构化搜索结果。
metadata:
  author: tavily-ai
  category: tool
  capabilities:
    - 实时联网搜索，获取最新信息
    - 深度研究模式，多网页内容整合
    - 图片搜索，返回相关图片URL
    - 自动生成引用来源
    - 结构化结果返回，适配AI Agent调用
    - 支持中文/英文多语言搜索
---

# Tavily Search AI 搜索工具

Tavily是专为AI Agent优化的搜索引擎，提供快速、准确、结构化的联网搜索能力，支持获取实时信息、深度研究资料、相关图片等，返回结果包含来源引用，方便溯源。

## 核心功能
### 1. 基础搜索
快速获取实时搜索结果，返回标题、摘要、来源URL、发布时间：
- 支持最新资讯、热点事件查询
- 支持事实类问题搜索
- 自动过滤低质量/广告内容

### 2. 深度搜索（Research Mode）
针对复杂问题进行多网页整合分析：
- 自动检索多个相关网页
- 整合内容生成结构化研究报告
- 保留所有来源引用
- 支持最多提取50个页面内容

### 3. 图片搜索
返回与关键词相关的高清图片URL：
- 支持多关键词组合搜索
- 自动过滤违规/低质量图片
- 返回直接可访问的图片链接

### 4. 搜索结果分析
自动提取搜索结果中的核心信息：
- 关键点摘要
- 时间线整理
- 多方观点对比
- 数据/事实统计

## 配置方法
### API密钥申请
1. 访问 [Tavily官网](https://tavily.com/) 注册账号
2. 免费版每月提供1000次搜索请求，足够日常使用
3. 获取你的API密钥（格式: `tvly-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`）

### 本地配置
```powershell
# 配置API密钥
tavily config --api-key tvly-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```
配置会自动保存到`config.json`文件中，无需重复配置。

## 使用示例
### 基础搜索
```powershell
tavily search "2026年AI大模型最新进展"
```

### 深度研究
```powershell
tavily research "企业AI安全建设方案" --max-pages 10
```

### 图片搜索
```powershell
tavily image "2026年新款AI硬件产品" --count 5
```

### 结构化JSON输出
```powershell
tavily search "OpenClaw最新版本" --format json
```

## API参数说明
| 参数 | 说明 | 默认值 |
|------|------|--------|
| query | 搜索关键词 | 必填 |
| search_depth | 搜索深度：`basic`/`advanced` | `basic` |
| max_results | 返回结果数量 | 5 |
| include_images | 是否返回图片 | false |
| include_answer | 是否生成自然语言答案 | true |
| include_raw_content | 是否返回网页原始内容 | false |
| domain | 限定搜索域名（可选） | 无 |

## 返回结果示例
```json
{
  "query": "2026年AI大模型最新进展",
  "answer": "2026年AI大模型主要进展包括多模态能力大幅提升、推理成本下降90%、端侧大模型普及等...",
  "results": [
    {
      "title": "2026年大模型技术白皮书",
      "url": "https://example.com/report/2026-ai-report",
      "content": "2026年大模型推理成本相比2023年下降90%，千亿参数模型推理成本降至每千tokens 0.001元...",
      "published_date": "2026-04-01"
    }
  ],
  "images": [
    "https://example.com/image/ai-model-2026.jpg"
  ],
  "response_time": 1.23
}
```
