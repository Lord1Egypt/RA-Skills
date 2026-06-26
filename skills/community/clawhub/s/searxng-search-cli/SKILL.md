---
name: searxng-search-cli
displayName: "SearXNG Search CLI (Free, Self-hosted, Auto-deploy, Multi-Channel)"
version: 1.2.1
description: |
  Use self-hosted SearXNG search engine (Free, Self-hosted, Auto-deploy, Multi-Channel). SearXNG is a free meta search engine that aggregates 200+ search engines (Google, Bing, Brave, GitHub, etc.), completely free and self-hostable.
  Trigger: User needs to search queries, research information, find resources, etc.
---

# SearXNG-CLI (Free, Self-hosted, Search Engine Aggregator) | SearXNG CLI（免费、自托管、搜索引擎聚合器）

- **Author**: [LeeShunEE](https://github.com/LeeShunEE)
- **Organization**: [KinemaClawWorkspace](https://github.com/KinemaClawWorkspace)
- **GitHub**: https://github.com/KinemaClawWorkspace/searxng-search-cli

Use SearXNG self-hosted search API for fast, accurate searching.

使用 SearXNG 自托管搜索 API 进行快速、准确的搜索。

## ⚠️ Before First Use | 首次使用必读

**首次使用此 skill 前，必须先读取 [ONBOARDING.md](ONBOARDING.md) 完成环境配置。**

- **首次配置** → 读取 ONBOARDING.md 完成全部步骤
- **环境不可用**（命令不存在、依赖缺失、搜索失败）→ 读取 ONBOARDING.md Troubleshooting 排查修复
- **配置完成后** → 直接使用下方 Run Commands

## Run Commands | 使用命令

```bash
# Search | 搜索
searxng-search search "your query"

# Specify engine | 指定引擎
searxng-search search "git clone" --engine github

# Specify language | 指定语言
searxng-search search "AI News" --lang zh

# Pagination | 分页
searxng-search search "llm" --page 2

# Time filter | 时间过滤
searxng-search search "python" --time-range month
```

## Command List | 命令列表

| Command | Description | 说明 |
|---------|-------------|------|
| install | One-click install SearXNG | 一键安装 SearXNG |
| start | Start service | 启动服务 |
| stop | Stop service | 停止服务 |
| restart | Restart service | 重启服务 |
| status | Check service status | 查看服务状态 |
| search \<query\> | Search | 搜索 |
| enable | Enable auto-start | 开机自启 |
| disable | Disable auto-start | 取消开机自启 |

## Configuration | 配置

- `SEARXNG_PORT` - Port (default 8888) | 端口 (默认 8888)
- `SEARXNG_HOST` - Bind address (default 127.0.0.1) | 绑定地址 (默认 127.0.0.1)
- `SEARXNG_SECRET` - Auth key (auto-generated if not set) | 认证密钥 (自动生成)

## Search Parameters | 搜索参数

| Parameter | Short | Description | Example |
|-----------|-------|-------------|---------|
| --engine | -e | Specify engine | github, google |
| --lang | -l | Language | zh, en, auto |
| --page | -p | Page number | 1, 2, 3 |
| --time-range | -t | Time range | day, week, month, year |
| --safe-search | -s | Safe search | 0, 1, 2 |
| --limit | | Max results (default 5) | 10 |

### Available Engines | 可用引擎

General: google, bing, brave, duckduckgo, yandex, startpage, qwant
Code/Dev: github, gitlab, stackoverflow, npm, pypi
Academic: arxiv, pubmed, wikipedia, google-scholar
Video/Image: youtube, vimeo, pexels, pixabay

## Known Limitations | 已知限制

- **部分引擎不稳定**：DuckDuckGo 可能触发 CAPTCHA、Brave 可能 403，属上游外部限制
- **首次搜索较慢**：可能需要 5-30 秒，后续请求会加速
- **推荐部署在有稳定网络出口的宿主机上**

## Related Documentation | 相关文档

- [SearXNG Official Docs](https://docs.searxng.org) | [SearXNG 官方文档](https://docs.searxng.org)
- [GitHub](https://github.com/searxng/searx)
