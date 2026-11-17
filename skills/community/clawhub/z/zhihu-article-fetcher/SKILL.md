---
name: zhihu-article-fetcher
description: |
  知乎专栏文章抓取器。专门用于抓取 `zhuanlan.zhihu.com/p/xxx` 单篇文章的标题和正文内容。
  支持三级认证降级（Browser Profile → File Cookie → 高仿真请求头），在无 Cookie 时也尝试绕过反爬。
  当用户提供知乎专栏文章链接、要求抓取/保存知乎文章、或 `git-repo-analyzer` 遇到知乎文章 403 无法获取时使用此技能替代。
---

# 知乎专栏文章抓取器 | Zhihu Article Fetcher

## Overview

本 skill 专门解决 **知乎专栏文章**（`zhuanlan.zhihu.com/p/xxx`）的内容获取问题。

- 参考 `zhihu-fetcher` 的三级认证降级思路
- 参考 `zhihu-keyword-content-search` 的结构化输出设计
- 核心差异：抓取**单篇专栏文章**而非热榜或问答

## 三级认证降级

```
优先级1: Browser Profile
    使用 OpenClaw browser 已登录状态（预留接口）
    ↓ 失败
优先级2: File Cookie
    读取 config/cookie.json 中的固化 Cookie
    ↓ 失败或未配置
优先级3: 高仿真请求头
    无 Cookie，但携带完整浏览器指纹（UA/Referer/Sec-Fetch 等）尝试绕过反爬
```

## 安装依赖

```bash
pip install requests beautifulsoup4
```

## 使用方法

### 1. 直接抓取（无 Cookie，尝试高仿真请求头）

```bash
python3 scripts/fetch_article.py "https://zhuanlan.zhihu.com/p/660571164"
```

### 2. 配置 Cookie 后抓取（成功率更高）

浏览器打开 https://www.zhihu.com → F12 → Network → 任意请求 → Request Headers → 复制 Cookie 中对应字段到 `config/cookie.json`：

```json
{
  "cookie": {
    "_xsrf": "你的_xsrf",
    "_zap": "你的_zap",
    "d_c0": "你的_d_c0",
    "z_c0": "你的_z_c0",
    "SESSIONID": "你的_SESSIONID"
  }
}
```

然后运行：

```bash
python3 scripts/fetch_article.py "https://zhuanlan.zhihu.com/p/660571164"
```

### 3. 保存到文件

```bash
python3 scripts/fetch_article.py "https://zhuanlan.zhihu.com/p/660571164" -o /tmp/article.json
```

## 输出格式

```json
{
  "meta": {
    "source": "zhihu-zhuanlan",
    "fetch_time": "2026-04-10T10:30:00",
    "auth_method": "simulated_headers",
    "url": "https://zhuanlan.zhihu.com/p/660571164"
  },
  "data": {
    "title": "文章标题",
    "url": "https://zhuanlan.zhihu.com/p/660571164",
    "content": "正文纯文本，段落以 \n\n 分隔...",
    "word_count": 3520,
    "fetch_method": "simulated_headers"
  }
}
```

## 与类似 skill 的对比

| skill | 抓取目标 | 认证方式 | 你的场景匹配度 |
|---|---|---|---|
| `zhihu-fetcher` | 知乎热榜 | 三级降级 | ❌ 不支持单篇文章 |
| `zhihu-keyword-content-search` | 知乎问答（按关键词搜索） | Cookie 必填 | ❌ 不支持专栏 URL |
| `zhihu-article-fetcher` | 知乎专栏单篇文章 | 三级降级 | ✅ **正对症** |

## 常见问题

**Q: 返回 "未能提取到正文内容"**
A: 知乎升级了反爬或页面结构。尝试配置有效 Cookie（方法2），或等待 skill 更新解析规则。

**Q: 503/429 频繁出现**
A: 脚本已内置动态延迟（1.5-2秒）。如仍被限，建议配置 Cookie 抓取，或间隔更长时间再试。

## File Structure

```
zhihu-article-fetcher/
├── SKILL.md                      # 本文档
├── config/
│   └── cookie.json               # Cookie 配置（需用户自行填入）
└── scripts/
    └── fetch_article.py          # 核心抓取脚本
```
