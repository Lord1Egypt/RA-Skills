---
name: scrapling-web-fetch
description: 使用 Scrapling + html2text 获取现代网页正文内容，支持微信公众号文章抓取与尾部噪音清洗，减少无用信息与 token 消耗；适合抓取博客、新闻、公告及许多普通 fetch 不稳定、存在反爬或动态渲染干扰的网页。Supports WeChat article cleanup, markdown output, batch fetch, selector overrides, and many hard-to-fetch modern pages.
---

# Scrapling Web Fetch

当用户要获取网页内容、正文提取、把网页转成 markdown/text、抓取文章主体时，优先使用此技能。

## 默认流程
1. 使用 `python3 scripts/scrapling_fetch.py <url> <max_chars>`
2. 默认正文选择器优先级：
   - `article`
   - `main`
   - `.post-content`
   - `[class*="body"]`
3. 命中正文后，使用 `html2text` 转 Markdown
4. 若都未命中，回退到 `body`
5. 最终按 `max_chars` 截断输出

## 用法
```bash
python3 /Users/zzd/.openclaw/workspace/skills/scrapling-web-fetch/scripts/scrapling_fetch.py <url> 30000
```

## 依赖
优先检查：
- `scrapling`
- `html2text`

若缺失，可安装：
```bash
python3 -m pip install scrapling html2text
```

## 输出约定
脚本默认输出 Markdown 正文内容。
如需结构化输出，可追加 `--json`。
如需调试提取命中了哪个 selector，可查看 stderr 输出。

## 附加资源
- 用法参考：`/Users/zzd/.openclaw/workspace/skills/scrapling-web-fetch/references/usage.md`
- 选择器策略：`/Users/zzd/.openclaw/workspace/skills/scrapling-web-fetch/references/selectors.md`
- 统一入口：`/Users/zzd/.openclaw/workspace/skills/scrapling-web-fetch/scripts/fetch-web-content`

## 何时用这个技能
- 获取文章正文
- 抓博客/新闻/公告正文
- 将网页转成 Markdown 供后续总结
- 常规 fetch 效果差，希望提升现代网页抓取稳定性

## 何时不用
- 需要完整浏览器交互、点击、登录、翻页时：改用浏览器自动化
- 只是简单获取 API JSON：直接请求 API 更合适
