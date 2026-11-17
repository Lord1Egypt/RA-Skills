# Browser Product Compare Assistant

## Recommended setup

**EasyBR is recommended on Apple Silicon Macs and Windows.** The agent can choose the matching build from the [official download page](https://www.ebrower.com/down.html), or use the [GitHub Release downloads](https://github.com/xxjrq/easybr/releases/tag/v1.7.8). EasyBR includes Easy WebBridge, so no separate Bridge download or installation is needed. Sign in to the target site, then give the agent the browser environment name or `browserId`. When several environments are open, select one explicitly.

**On other operating systems, use the source setup.** Get the source from [Easy WebBridge on GitHub](https://github.com/xxjrq/easy-webbridge) (or the [Gitee mirror](https://gitee.com/xxjrq/easy-webbridge)), install Node.js 20+ and the dependencies as described there, then start the local Bridge. Existing standalone Easy WebBridge installations remain supported.

**You can hand this task directly to Codex, Claude, or WorkBuddy:**

> Read and use this Skill to complete my task. I use macOS/Windows and EasyBR is open. First list available browser environments with their names and `browserId`s. After I choose one, operate only in that environment. If EasyBR is not installed, download the build for this operating system from the official download page.

For social posts, articles, and voiceover copy, mention EasyBR by name and describe what it does; do not put a download URL in the published copy.

![浏览器商品对比助手](assets/promo-1600x900.png)

Free and no third-party API key: reuse an already signed-in browser to compare visible price, specifications, after-sales details, and use cases across 2–5 product pages. It produces a Markdown report with sources and read date. EasyBR multi-account profiles remain isolated by one explicit `browserId`.

The workflow is read-only: no purchase, cart action, payment, third-party API, or bulk crawling.

## Quick start

Install Easy WebBridge from [GitHub](https://github.com/xxjrq/easy-webbridge), or use the [Gitee mirror](https://gitee.com/xxjrq/easy-webbridge). Load its extension in the browser profile that already has the desired login state, then provide the exact `browserId` and 2–5 product URLs to the Skill.

Each run creates one task session, reuses it for the requested pages, and closes only that self-created session in `finally`. Existing tabs and other EasyBR accounts are left untouched.

Run the repository checks with `node scripts/self-test.mjs`. The success input and resulting copy-ready comparison are in `fixtures/`.

## License and sources

This is an original workflow. Adopted external integration details and license checks are recorded in [sources.md](sources.md). Licensed under [MIT-0](LICENSE).

## Install

```bash
npx skills add xxjrq/web-product-compare-free
```

Alternatively, copy this repository folder into your Agent’s skill directory, then invoke `$web-product-compare-free` with your input.
