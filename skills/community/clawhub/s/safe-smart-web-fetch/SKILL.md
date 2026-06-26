---
name: safe-smart-web-fetch
description: 安全网页抓取技能。获取网页内容时，默认先判断 URL 是否可能包含 token、是否为内网/本地域名、是否为私密链接；这三类一律不走第三方清洗服务，只走直接抓取。其余公开网页可按顺序尝试 Jina Reader、markdown.new、defuddle.md 获取干净 Markdown，失败再回退原始抓取。
---

# Safe Smart Web Fetch

用于安全地获取网页内容。

## 规则

先判断目标 URL：

### 一律禁止走第三方清洗的情况
- URL query 或 fragment 中带明显 token / key / signature / auth / session / code 参数
- localhost / 127.0.0.1 / 10.x / 172.16-31.x / 192.168.x / `.local` / 内网主机名
- 明显私密页面：带登录态回调、管理后台、分享密钥、重置链接、单次授权链接等
- 非 http/https URL

以上情况：
- 只允许本地直接抓取
- 不发送到 Jina / markdown.new / defuddle.md

### 可走第三方清洗的情况
- 普通公开网页
- 不含敏感 query 参数
- 非内网/本地地址

第三方顺序：
1. Jina Reader
2. markdown.new
3. defuddle.md
4. 原始抓取回退

## 用法

```bash
python3 {baseDir}/scripts/fetch.py "https://example.com/article"
python3 {baseDir}/scripts/fetch.py "https://example.com/article" --json
```

## 输出

JSON 模式会返回：
- `success`
- `url`
- `content`
- `source`
- `used_third_party`
- `blocked_reason`
- `error`

## 注意

- 这是公开网页优先清洗、敏感链接严格本地抓取的安全版本
- 不修改 OpenClaw 全局工具配置
- 不强制禁用内置 `web_fetch`
