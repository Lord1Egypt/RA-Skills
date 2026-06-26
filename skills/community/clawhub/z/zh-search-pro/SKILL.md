---
name: zh-search-pro
description: 中文搜索增强工具，整合百度、必应、微信、知乎等中文搜索引擎，支持高级搜索语法和时间过滤。
metadata:
  openclaw:
    requires:
      bins:
        - web_fetch
---

# 中文搜索增强工具 v1.0.0

整合多个中文搜索引擎，无需 API 密钥即可进行中文内容搜索。

## 支持的搜索引擎

### 中文搜索引擎 (6)
- **百度**: `https://www.baidu.com/s?wd={keyword}`
- **必应中国**: `https://cn.bing.com/search?q={keyword}`
- **微信搜索**: `https://weixin.sogou.com/weixin?type=2&query={keyword}`
- **知乎**: `https://www.zhihu.com/search?q={keyword}&type=content`
- **今日头条**: `https://so.toutiao.com/search?keyword={keyword}`
- **360 搜索**: `https://www.so.com/s?q={keyword}`

### 国际搜索引擎 (3)
- **DuckDuckGo**: `https://duckduckgo.com/html/?q={keyword}`
- **Google HK**: `https://www.google.com.hk/search?q={keyword}`
- **Startpage**: `https://www.startpage.com/sp/search?query={keyword}`

## 快速使用示例

```javascript
// 基础搜索
web_fetch({"url": "https://www.baidu.com/s?wd=Python 教程"})

// 站内搜索
web_fetch({"url": "https://www.baidu.com/s?wd=site:zhihu.com+AI 学习"})

// 时间过滤（最新内容）
web_fetch({"url": "https://cn.bing.com/search?q=AI 新闻&filters=ex1%3a%22last7%22"})

// 微信文章搜索
web_fetch({"url": "https://weixin.sogou.com/weixin?type=2&query=自媒体 运营"})

// 知乎内容搜索
web_fetch({"url": "https://www.zhihu.com/search?q=如何学习编程&type=content"})
```

## 高级搜索语法

### 百度高级语法
| 语法 | 示例 | 说明 |
|------|------|------|
| `site:` | `site:zhihu.com AI` | 站内搜索 |
| `intitle:` | `intitle:教程 Python` | 标题包含 |
| `inurl:` | `inurl:blog` | URL 包含 |
| `filetype:` | `filetype:pdf 报告` | 文件类型 |
| `""` | `"机器学习"` | 精确匹配 |
| `-` | `Python -snake` | 排除关键词 |

### 必应高级语法
| 语法 | 示例 | 说明 |
|------|------|------|
| `site:` | `site:github.com` | 站内搜索 |
| `language:` | `language:zh-CN` | 语言过滤 |
| `loc:` | `loc:CN` | 地区过滤 |
| `hasfeed:` | `hasfeed:新闻` | 包含 RSS |

## 时间过滤参数

### 必应时间过滤
- 过去 24 小时：`&filters=ex1%3a%22last24%22`
- 过去 7 天：`&filters=ex1%3a%22last7%22`
- 过去 30 天：`&filters=ex1%3a%22last30%22`
- 过去一年：`&filters=ex1%3a%22lasty%22`

### 百度时间过滤
- 一天内：`&cl=24`
- 一周内：`&cl=7`
- 一月内：`&cl=30`
- 一年内：`&cl=365`

## 使用场景

1. **市场调研** - 搜索行业报告、竞品分析
2. **内容创作** - 查找素材、热点话题
3. **学术研究** - 搜索论文、专业资料
4. **舆情监控** - 追踪品牌/产品讨论
5. **SEO 研究** - 分析关键词排名

## 注意事项

- 部分搜索引擎有反爬机制，可能需要重试
- 微信搜索需要处理验证码
- 建议配合 `web_search` 工具使用（如果有 API 密钥）

## 相关文件

- `CHANGELOG.md` - 版本历史
- `examples/` - 使用示例

## 许可证

MIT-0 - 自由使用、修改和分发
