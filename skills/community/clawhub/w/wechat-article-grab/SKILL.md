---
name: wechat-article-reader
description: "抓取微信公众号文章、搜索公众号、文章列表、爆款查询与分析。触发场景：mp.weixin.qq.com 链接、微信公众号文章、公众号文章分析。"
metadata:
  allowed-tools: ["exec", "read", "write", "edit"]
---

# 微信公众号文章读取器

## 入口
```bash
cd ~/.openclaw/agents/xingchen/workspace/skills/wechat-article-reader
python3 scripts/gzh_article.py <command> [args]
```

## 环境变量配置

详见 `env-guide.md`（MPTEXT_API_KEY 和 Cookie 的获取与配置说明）。

## 命令（12个）

### 常用命令
| 命令 | 说明 |
|------|------|
| `fetch "<url>"` | 抓取单篇文章全文（标题+正文），curl 优先，不需要公众号名 |
| `full "公众号名" [数量]` | 列出某公众号文章+每篇预览前800字，不含阅读量 |
| `list "公众号名" [数量]` | 列出文章标题+摘要digest，不含正文 |
| `mpsearch "<关键字>"` | 按名称搜索公众号，返回名称和fakeid |
| `stats "<url>"` | 拿文章标题搜 trends API，返回相似爆款文章的互动数据（新文章可能无结果） |
| `trends "<关键词>"` | 查某关键词下的爆款文章列表，含阅读/点赞/评论数据 |
| `compare --accounts "名1,名2" [--count N]` | 对比多个公众号的文章列表 |
| `compare --urls "url1,url2"` | 对比多个链接对应的公众号文章列表 |
| `compare "<关键词>"` | 按关键词查爆款文章（不是对比，是搜索） |
| `resolve "<标题>"` | 根据标题搜索并匹配文章链接 |

### 专用命令
| 命令 | 说明 |
|------|------|
| `mparticles "<fakeid>" [数量]` | 从 fakeid 查文章列表 |
| `mparticles_by_url "<url>" [数量]` | 从 URL 提取 biz 再查文章列表（URL 需含 `__biz`） |
| `mpinfo "<fakeid>"` | 查公众号主体信息（公司名、是否认证、原创文章数） |
| `mpdownload "<url>" [格式]` | 下载文章正文（mptext 方式，不含标题） |

## 自动降级链路

### 3 层路径
| 命令 | P1 | P2 | P3 |
|------|----|----|-----|
| fetch | curl（免费） | mptext | Cookie |
| compare --urls | biz→mptext | 正文识别账号名→mptext | Cookie |
| mparticles_by_url | biz→mptext | 正文识别账号名→mptext | Cookie |

### 2 层路径
| 命令 | P1 | P2 |
|------|----|----|
| list | mptext | Cookie |
| full | mptext | Cookie |
| compare --accounts | mptext | Cookie |
| resolve | mptext | Cookie |
| mpsearch | mptext | Cookie |
| mparticles | mptext | Cookie |
| mpdownload | mptext | curl |

### 单路径
| 命令 | 唯一路径 |
|------|----------|
| stats | trends API |
| trends | trends API |
| mpinfo | mptext |

## 已知局限
- **fetch 内容截断**：JS验证拦截的文章只能拿 ~800 字，换 P2 可能完整
- **mparticles_by_url**：URL 不含 `__biz` 时走正文识别公众号名路径，无需 biz
- **stats**：仅对爆款文章有效，新文章无结果时提示"所有关键词查询均失败"
- **历史列表不全**：原生 API 最多约 436 篇

详细说明见 `references/priority.md`