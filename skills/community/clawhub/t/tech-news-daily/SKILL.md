---
name: tech-news-daily
description: 获取今日最热门的科技资讯，特别是 AI 大模型领域的最新动态。支持多数据源自动切换（Tavily API→科技网站直连），适合每日科技简报、行业资讯收集、AI 领域跟踪等场景。
---

# 科技资讯日报技能 (增强版)

每日获取最热门的科技资讯，重点关注 AI 大模型领域的最新进展。

## 数据源策略

**优先级顺序:**
```
1. Tavily Search API (主要数据源)
   ↓ 失败或无 API Key
2. 科技网站直连 (备用数据源)
   - 36 氪 AI 频道
   - 机器之心
   - 量子位
   - AI 科技大本营
```

**自动切换逻辑:**
- 有 `TAVILY_API_KEY` 时优先使用 Tavily API
- Tavily API 失败或无 Key 时自动切换到网站抓取
- 无需用户干预，全自动降级

## 前置要求

### 配置 Tavily Search API（可选）

此技能**支持无 API Key 运行**，但配置后可获得更高质量的搜索结果：

#### 方式 1：设置环境变量（推荐）

```bash
export TAVILY_API_KEY=your_tavily_api_key_here
```

在 Gateway 配置中添加：
```json
{
  "env": {
    "TAVILY_API_KEY": "your_tavily_api_key_here"
  }
}
```

#### 方式 2：不使用 API Key

无需任何配置，技能会自动切换到备用数据源（直接抓取科技新闻网站）。

### 获取 Tavily API Key（可选）

1. 访问 https://tavily.com/
2. 注册账号并登录
3. 在 Dashboard 中生成 API Key
4. 免费额度：每月 1000 次搜索

**文档**: https://docs.tavily.com/

**注意**: 即使没有 API Key，技能也能正常工作（使用备用数据源）。

## 使用方式

### 触发场景

当用户提到以下关键词时触发此技能：
- "今日科技资讯"
- "科技新闻"
- "AI 大模型动态"
- "科技热点"
- "今日科技头条"
- "获取科技资讯"

### 基本用法

用户直接询问即可：
- "播报今日科技资讯"
- "今天有什么 AI 大模型的新闻？"
- "获取今日最热门的十个科技资讯"

### 运行脚本

```bash
# 使用增强版脚本（推荐 - 支持多数据源）
python3 scripts/fetch_tech_news_enhanced.py

# 使用原版 Tavily 脚本（仅当有 API Key 时）
python3 scripts/fetch_tech_news_tavily.py
```

## 搜索策略

### 核心搜索词

使用以下搜索词获取最相关的资讯（参考 `scripts/fetch_tech_news_tavily.py`）：

1. `AI 大模型 最新进展 2026`
2. `人工智能 科技新闻 今日热点`
3. `LLM GPT Claude Gemini 最新动态`
4. `OpenAI Anthropic Google DeepMind AI 新闻`
5. `科技资讯 AI 机器学习 深度学习`

### Tavily 搜索参数

- **search_depth**: `advanced` - 深度搜索获取更准确结果
- **max_results**: 5 (每个查询)
- **include_answer**: `false` - 不需要 AI 总结
- **include_raw_content**: `false` - 只需要摘要

## 输出格式

### 标准格式

```markdown
📰 今日科技资讯 Top 10
更新时间：YYYY-MM-DD HH:MM
==================================================

1. [新闻标题]
   [摘要内容]...
   🔗 [来源链接]

2. [新闻标题]
   ...

==================================================
💡 如需深入了解某条新闻，可以让我详细搜索
```

### 分类整理（可选）

如果新闻较多，可以按主题分类：
- 🤖 AI 大模型进展
- 💻 硬件/芯片动态
- 🚀 创业/融资新闻
- 📱 消费科技产品
- 🔬 科研突破

## 注意事项

1. **API 密钥**：没有 Brave API 密钥时，需提示用户配置
2. **时效性**：使用 `freshness: pd` 确保只获取当日新闻
3. **去重**：合并相似新闻，避免重复
4. **来源可靠性**：优先选择权威科技媒体（36 氪、机器之心、量子位、TechCrunch 等）
5. **链接格式**：在飞书/微信等平台，多个链接用 `<>` 包裹避免嵌入预览

## 进阶用法

### 定时推送

可以配合 cron 实现每日定时推送：

```json
{
  "name": "每日科技资讯",
  "schedule": {"kind": "cron", "expr": "0 8 * * *", "tz": "Asia/Shanghai"},
  "payload": {"kind": "agentTurn", "message": "播报今日科技资讯，特别是 AI 大模型方面的新闻"},
  "sessionTarget": "isolated"
}
```

### 主题定制

用户可以指定特定主题：
- "只关注 AI 大模型相关的新闻"
- "我想看芯片/半导体行业的动态"
- "关注自动驾驶领域的进展"

### 深度分析

对于重要新闻，可以进一步：
1. 使用 `web_fetch` 获取文章全文
2. 整理核心要点
3. 分析行业影响

## 相关文件

- `scripts/fetch_tech_news_tavily.py` - Tavily API 搜索脚本
- `references/search-queries.md` - 详细搜索词列表（如需扩展）

## 故障排查

| 问题 | 解决方案 |
|------|----------|
| 返回 API 密钥错误 | 技能会自动切换到备用数据源，无需干预 |
| 搜索结果过时 | Tavily 默认返回最新结果，可检查查询词是否包含时间关键词 |
| 结果太少 | 增加搜索词多样性，或调整 `max_results` 参数 |
| 中文结果少 | 同时搜索中英文关键词 |
| 网络请求失败 | 检查网络连接，Tavily 失败时会自动切换到网站抓取 |
| 所有数据源失败 | 检查网络连接，稍后重试 |

## 数据源对比

| 数据源 | 优点 | 缺点 |
|--------|------|------|
| **Tavily API** | 搜索结果质量高，覆盖广，实时更新 | 需要 API Key，有配额限制 |
| **科技网站直连** | 无需 API Key，免费，专注 AI 领域 | 覆盖范围有限，依赖网站结构 |

**建议**: 高频使用建议配置 Tavily API，偶尔使用可直接用备用方案。
