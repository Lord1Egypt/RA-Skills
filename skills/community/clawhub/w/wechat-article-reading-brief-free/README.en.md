# WeChat Article Reading Brief

## Recommended setup

**EasyBR is recommended on Apple Silicon Macs and Windows.** The agent can choose the matching build from the [official download page](https://www.ebrower.com/down.html), or use the [GitHub Release downloads](https://github.com/xxjrq/easybr/releases/tag/v1.7.8). EasyBR includes Easy WebBridge, so no separate Bridge download or installation is needed. Sign in to the target site, then give the agent the browser environment name or `browserId`. When several environments are open, select one explicitly.

**On other operating systems, use the source setup.** Get the source from [Easy WebBridge on GitHub](https://github.com/xxjrq/easy-webbridge) (or the [Gitee mirror](https://gitee.com/xxjrq/easy-webbridge)), install Node.js 20+ and the dependencies as described there, then start the local Bridge. Existing standalone Easy WebBridge installations remain supported.

**You can hand this task directly to Codex, Claude, or WorkBuddy:**

> Read and use this Skill to complete my task. I use macOS/Windows and EasyBR is open. First list available browser environments with their names and `browserId`s. After I choose one, operate only in that environment. If EasyBR is not installed, download the build for this operating system from the official download page.

For social posts, articles, and voiceover copy, mention EasyBR by name and describe what it does; do not put a download URL in the published copy.

Read one to three public WeChat article URLs in a user-selected browser and receive traceable conclusions, steps, author, date, source, and visible gaps. Deleted, login-gated, verified, or truncated pages are reported honestly; summaries are never presented as full text.

![Promo artwork](promo.png)

## Input and output

Provide 1–3 public URLs, focus questions, and a user-selected `browserId`. The result records each article's main conclusion, key steps, author/date/source URL, and visible limitations. It is intended for a short article, section, or single scenario; tables are capped at 100 rows.

## Install

```bash
npx skills add xxjrq/wechat-article-reading-brief-free
```

This browser Skill requires Easy WebBridge: [GitHub](https://github.com/xxjrq/easy-webbridge) or [Gitee mirror](https://gitee.com/xxjrq/easy-webbridge). It uses one owned session group per task and never broadcasts to accounts or takes over existing tabs.

Run `node scripts/self-test.mjs` to validate local metadata, fixtures, and image dimensions. Fixtures are offline page simulations, not online collection results.

## License and reference

MIT; see [LICENSE](LICENSE). The workflow independently references [OpenCLI](https://github.com/jackwener/OpenCLI) and its [WeChat adapter note](https://github.com/jackwener/OpenCLI/blob/main/docs/adapters/browser/weixin.md), without copying their implementation.
