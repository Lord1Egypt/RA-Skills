---
name: smart-web-fetch
description: 智能网页抓取技能 - 替代内置 web_fetch，自动使用 Jina Reader / markdown.new / defuddle.md 清洗服务获取干净 Markdown。支持多级降级策略，大幅降低 Token 消耗。当 Agent 需要获取网页内容时使用本技能替代 web_fetch。
---

# Smart Web Fetch

智能网页内容获取技能，完全替代 web_fetch，自动通过清洗服务获取干净 Markdown。

## 核心功能

- **完全替代 web_fetch**: 获取的已经是清洗后的 Markdown，而非原始 HTML
- **四级降级策略**: Jina → markdown.new → defuddle.md → 原始内容
- **Token 优化**: 清洗后的内容比原始 HTML 节省 50-80% Token

## 使用方式

### 命令行获取网页内容

```bash
# 获取清洗后的 Markdown（文本输出）
python3 {baseDir}/scripts/fetch.py "https://example.com/article"

# 获取 JSON 格式（包含元信息）
python3 {baseDir}/scripts/fetch.py "https://example.com/article" --json
```

### 在 Agent 中使用

**当用户需要获取网页内容时：**

```
用户: "帮我查一下 https://example.com/article 的内容"

Agent 应该:
1. 运行: python3 ~/.openclaw/skills/smart-web-fetch/scripts/fetch.py "https://example.com/article"
2. 直接获得清洗后的 Markdown 内容
```

## JSON 输出格式

```json
{
  "success": true,
  "url": "https://r.jina.ai/http://example.com/article",
  "content": "# Article Title\n\nClean markdown content here...",
  "source": "jina",
  "error": null
}
```

## 降级策略

1. **Jina Reader** (首选)
   - URL: `https://r.jina.ai/http://{target}`
   - 免费，无需 API Key，中文支持好

2. **markdown.new** (降级)
   - URL: `https://markdown.new/{target}`

3. **defuddle.md** (降级)
   - URL: `https://defuddle.md/{target}`

4. **原始内容** (最终兜底)
   - 直接获取原始 HTML

## Agent 配置建议

为了强制使用本技能替代 web_fetch，在 `openclaw.json` 中配置：

```json
{
  "agents": {
    "list": [
      {
        "id": "your-agent",
        "tools": {
          "deny": ["web_fetch"]
        }
      }
    ]
  }
}
```

这样 Agent 就无法调用内置 web_fetch，只能通过本技能获取网页内容。

## 优势

- 🚀 **Token 节省 50-80%**: 去除广告、导航栏等噪音
- 🔄 **自动容错**: 四级服务降级，确保可用性
- 🆓 **零成本**: 全部使用免费服务
- 🔌 **即插即用**: 不需要 API Key
- 📝 **干净输出**: 纯 Markdown，无需额外解析
