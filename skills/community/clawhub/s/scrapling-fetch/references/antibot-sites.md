# 已知反爬网站列表

本文档维护需要使用 Scrapling 抓取的网站列表。

## 确认支持（✅）

| 网站 | 反爬机制 | Scrapling 支持 |
|------|---------|--------------|
| 微信公众号 | User-Agent 检测 + Cookie 验证 | ✅ 已测试 |
| Medium.com | 反爬虫系统 | ✅ 理论支持 |
| Substack.com | 基础反爬 | ✅ 理论支持 |
| 知乎 | 登录墙（部分内容） | ⚠️ 仅公开部分 |
| Cloudflare Turnstile | JavaScript 挑战 | ✅ 已支持 |

## 需要登录（❌）

这些网站强制登录，Scrapling 无法抓取：

- Twitter/X（推特）
- 微博
- Instagram
- Facebook

**解决方案：**
- Twitter → 使用 `xurl` 技能（需配置 API）
- 微博 → 使用浏览器自动化（需手动登录）

## 付费内容

- 付费专栏
- 会员文章
- 订阅内容

Scrapling 只能抓取公开部分。

---

## 贡献

发现新的反爬网站？请更新此列表！
