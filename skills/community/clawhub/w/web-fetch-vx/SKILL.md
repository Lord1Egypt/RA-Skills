# Web Content Extractor - 网页内容提取器

**版本**: 2.0  
**作者**: OpenClaw Team  
**更新日期**: 2026-03-15  
**许可证**: MIT

---

## 📦 技能元数据

```yaml
name: web-content-extractor
version: 2.0.0
description: 从微信文章/博客/新闻网页提取干净内容，去除广告和侧边栏
category: 内容处理
tags: [网页提取，内容清洗，微信文章，Markdown]
author: OpenClaw Team
license: MIT
```

---

## 🎯 功能概述

基于 Readability + Firecrawl + Defuddle 三引擎的网页内容提取工具，专为中文内容优化。支持微信文章、新闻网站、博客等多种来源，自动去除广告/导航/侧边栏，输出干净的 Markdown 格式。

**核心能力**：
- ✅ 微信文章提取（mp.weixin.qq.com）
- ✅ 新闻网页清洗
- ✅ 博客文章解析
- ✅ 元数据提取（标题/作者/日期）
- ✅ 多格式输出（Markdown/JSON/纯文本）
- ✅ 批量处理支持

---

## 🚀 快速开始

### 基础调用

```python
# OpenClaw 工具调用
result = web_fetch(
    url="https://mp.weixin.qq.com/s/xxx",
    extractMode="markdown",
    maxChars=8000
)
```

### 完整参数

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| url | str | ✅ | - | 网页 URL |
| extractMode | str | ❌ | "markdown" | 输出格式（markdown/text/json） |
| maxChars | int | ❌ | 8000 | 最大字符数 |
| includeMetadata | bool | ❌ | true | 是否包含元数据 |
| timeout | int | ❌ | 30 | 超时时间（秒） |

---

## 📤 输入输出

### 输入示例

```json
{
  "url": "https://mp.weixin.qq.com/s/abcdefg",
  "extractMode": "markdown",
  "maxChars": 8000,
  "includeMetadata": true
}
```

### 输出示例

```json
{
  "success": true,
  "url": "https://mp.weixin.qq.com/s/abcdefg",
  "title": "文章标题",
  "author": "作者名",
  "publishDate": "2026-03-15",
  "content": "Markdown 格式的正文内容...",
  "wordCount": 2500,
  "readTime": "10 分钟",
  "images": ["https://..."],
  "extractTime": 0.8
}
```

---

## 🔧 技术架构

### 三引擎设计

```
                    用户请求
                       ↓
              ┌────────────────┐
              │   路由判断层    │
              └────────────────┘
                       ↓
        ┌──────────────┼──────────────┐
        ↓              ↓              ↓
   ┌─────────┐   ┌─────────┐   ┌─────────┐
   │ web_fetch│   │ defuddle│   │ browser │
   │ (快速)  │   │ (专业)  │   │ (兜底)  │
   └─────────┘   └─────────┘   └─────────┘
        ↓              ↓              ↓
              ┌────────────────┐
              │   结果聚合层    │
              └────────────────┘
                       ↓
                  返回用户
```

### 引擎对比

| 引擎 | 速度 | 成功率 | 适用场景 |
|------|------|--------|----------|
| web_fetch | <1s | 70% | 微信文章/通用网页 |
| defuddle | <1s | 75% | 博客/新闻网站 |
| browser | 5-10s | 90% | 复杂 SPA/动态页面 |

---

## 📋 使用场景

### 场景 1：微信文章提取

```python
result = web_fetch(
    url="https://mp.weixin.qq.com/s/xxx",
    extractMode="markdown"
)
print(result["content"])
```

### 场景 2：批量处理

```python
urls = ["url1", "url2", "url3"]
results = [web_fetch(url=u) for u in urls]
```

### 场景 3：带元数据提取

```python
result = web_fetch(
    url="https://example.com/article",
    includeMetadata=True
)
print(f"标题：{result['title']}")
print(f"作者：{result['author']}")
print(f"字数：{result['wordCount']}")
```

---

## ⚠️ 限制与注意事项

### 不支持的场景

- ❌ 需要登录的页面
- ❌ 付费墙内容
- ❌ 验证码保护的页面
- ❌ 纯 JavaScript 渲染的 SPA（需用 browser 引擎）

### 速率限制

| 域名类型 | 请求间隔 | 并发限制 |
|----------|----------|----------|
| 微信文章 | 2 秒 | 1 |
| 新闻网站 | 1 秒 | 3 |
| 博客 | 1 秒 | 5 |

### 合规要求

1. 仅提取公开可访问内容
2. 尊重 robots.txt 协议
3. 不用于商业用途（除非获得授权）
4. 保留原作者署名

---

## 🎛️ 高级配置

### 自定义 User-Agent

```python
result = web_fetch(
    url="https://example.com",
    userAgent="Mozilla/5.0 ..."
)
```

### 代理配置

```python
result = web_fetch(
    url="https://example.com",
    proxy="http://proxy:port"
)
```

### 缓存控制

```python
# 启用缓存（1 小时）
result = web_fetch(url, cache=True, ttl=3600)

# 强制刷新
result = web_fetch(url, cache=False)
```

---

## 📊 性能指标

| 指标 | 数值 |
|------|------|
| 平均响应时间 | 0.8 秒 |
| P95 响应时间 | 2.5 秒 |
| 成功率 | 85% |
| 缓存命中率 | 60% |

---

## 🔍 故障排查

### 问题 1：提取内容为空

**原因**：页面需要 JavaScript 渲染  
**解决**：切换到 browser 引擎

### 问题 2：微信文章提取失败

**原因**：链接过期或有反爬  
**解决**：
1. 检查链接是否有效
2. 尝试 browser 引擎
3. 手动复制内容

### 问题 3：提取内容不完整

**原因**：maxChars 限制  
**解决**：增加 maxChars 参数或分页处理

---

## 📚 依赖项

```json
{
  "readability": "^0.4.4",
  "firecrawl": "^1.0.0",
  "defuddle": "^3.0.0"
}
```

---

## 🤝 贡献指南

1. Fork 本仓库
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

---

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE)

---

## 📞 支持

- **文档**: https://docs.openclaw.ai/skills/web-content-extractor
- **问题反馈**: https://github.com/openclaw/openclaw/issues
- **社区**: https://discord.com/invite/clawd

---

**最后更新**: 2026-03-15  
**维护状态**: ✅ 活跃维护
