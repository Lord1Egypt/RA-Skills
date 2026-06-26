---
name: site-analyzer/robots
description: robots.txt 抓取与解析子 skill。自动尝试 https/http 两种协议，解析 User-agent/Allow/Disallow/Sitemap/Crawl-delay，判断站点对各主要爬虫（*、Googlebot、Baiduspider 等）的开放策略。当用户要查某站点是否允许爬取、robots 策略内容时使用。
---

# robots.txt 解析 (robots)

## 快速调用

```bash
# 域名（自动拼接 /robots.txt）
python3 ./06_robots.py <domain>

# 完整 URL
python3 ./06_robots.py https://example.com

# JSON 输出
python3 ./06_robots.py <domain> --json
```

## 输出说明

```
=== robots.txt: <domain> ===
  URL: https://<domain>/robots.txt  [HTTP 200]

爬虫规则摘要:
  ✅ *: allowed
  ✅ googlebot: allowed
  ⚠️  baiduspider: partial
     Disallow(3): /admin, /private, /tmp
  🚫 yandexbot: blocked
     Disallow(1): /

  Sitemaps (2): https://example.com/sitemap.xml, ...
```

## 状态符号

| 符号 | 含义 |
|------|------|
| ✅ allowed | 无 Disallow 或全部 Allow，可自由抓取 |
| ⚠️ partial | 部分路径被禁止 |
| 🚫 blocked | `Disallow: /`，完全禁止 |

## HTTP 状态码解读

| 状态码 | 含义 |
|--------|------|
| 200 | 有 robots.txt，解析规则 |
| 404 | 无 robots.txt，视为全部允许 |
| 403/401 | robots.txt 本身被保护 |
| 301/302 | 有重定向，注意最终 URL |

## 注意

- User-Agent 模拟 Googlebot 发起请求
- 自动跟随重定向，记录重定向链
- `Crawl-delay` 有值时会在摘要中显示
