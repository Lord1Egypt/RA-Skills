---
name: wechatsync
description: "Multi-platform article publisher and content distribution tool. Sync and cross-post Markdown/HTML articles to 27+ platforms including Zhihu (知乎), Juejin (掘金), CSDN, Toutiao (头条), Weibo (微博), Xiaohongshu (小红书), Bilibili (B站), WordPress, Typecho, WeChat (微信公众号), and more. Use when the user wants to publish, sync, cross-post, or distribute articles (文章同步/多平台发布/一键发布) to Chinese content platforms, tech communities, blogging sites, or self-hosted blogs. Also use when checking platform login status or extracting articles from web pages. Keywords: content syndication, blog distribution, multi-platform publishing, self-media (自媒体), content creator tools."
metadata:
  openclaw:
    requires:
      env:
        - WECHATSYNC_TOKEN
      bins:
        - wechatsync
    primaryEnv: WECHATSYNC_TOKEN
    emoji: "\U0001F4DD"
    homepage: https://github.com/wechatsync/Wechatsync
    install:
      - kind: node
        package: "@wechatsync/cli"
        bins: [wechatsync]
---

# WechatSync

Publish and sync Markdown/HTML articles to 27+ content platforms via CLI.

## Prerequisites

This skill requires external tools that the user must install themselves:

1. **CLI tool** (`@wechatsync/cli`): Open-source npm package ([source code](https://github.com/wechatsync/Wechatsync/tree/v2/packages/cli)). Install with `npm install -g @wechatsync/cli`
2. **Chrome extension**: Open-source browser extension ([source code](https://github.com/wechatsync/Wechatsync/tree/v2/packages/extension)). Install from [Chrome Web Store](https://chrome.google.com/webstore/detail/hchobocdmclopcbnibdnoafilagadion) or [download ZIP](https://www.wechatsync.com/#install)
3. **Token**: User-generated token set in extension settings. The token is created locally by the user and used only for localhost communication between CLI and extension. Set via `export WECHATSYNC_TOKEN="your-token"`
4. **Platform logins**: Log in to target platforms in browser (extension uses existing browser cookies, no credentials are stored or transmitted)

**Security model**: All data stays local. The CLI communicates with the Chrome extension over localhost. The extension calls platform APIs directly from the browser using existing login sessions. No third-party server involved. Full source code is open and auditable.

Before running any command, confirm the user has completed the prerequisites. Do not install packages on the user's behalf without explicit consent.

## Commands

### Sync

```bash
wechatsync sync article.md -p juejin              # single platform
wechatsync sync article.md -p juejin,zhihu,csdn   # multiple platforms
wechatsync sync article.md -p juejin -t "Title"   # custom title
wechatsync sync article.md -p juejin --cover ./cover.png  # cover image
wechatsync sync article.md -p juejin --dry-run     # preview only
```

### Platforms & Auth

```bash
wechatsync platforms          # list all platforms
wechatsync platforms --auth   # show login status
wechatsync auth zhihu         # check single platform
```

### Extract

```bash
wechatsync extract              # extract from current browser page
wechatsync extract -o article.md  # save to file
```

## Platform IDs

zhihu, juejin, csdn, jianshu, toutiao, weibo, bilibili, xiaohongshu, baijiahao, weixin, yuque, douban, sohu, xueqiu, woshipm, dayu, yidian, 51cto, sohufocus, imooc, oschina, segmentfault, cnblogs, x, eastmoney, smzdm, netease, wordpress, typecho

## Notes

- Images auto-uploaded to target platform CDN (PNG, JPG, GIF, WebP, SVG)
- Markdown title extracted from front matter `title` or first `# heading`
- Articles sync as **drafts** by default — user reviews before publishing

## Workflow

1. Confirm prerequisites are installed (ask user if unsure)
2. Check login: `wechatsync platforms --auth`
3. Sync: `wechatsync sync <file> -p <platform1>,<platform2>`
4. Report results with draft URLs

Example prompts:
- "Sync this article to Juejin and Zhihu"
- "Which platforms am I logged into?"
- "Extract the article from browser and save it"
- "把这篇文章同步到掘金和知乎"
