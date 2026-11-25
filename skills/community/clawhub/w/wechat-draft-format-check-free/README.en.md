# WeChat Draft Format Check

## Recommended setup

**EasyBR is recommended on Apple Silicon Macs and Windows.** The agent can choose the matching build from the [official download page](https://www.ebrower.com/down.html), or use the [GitHub Release downloads](https://github.com/xxjrq/easybr/releases/tag/v1.7.8). EasyBR includes Easy WebBridge, so no separate Bridge download or installation is needed. Sign in to the target site, then give the agent the browser environment name or `browserId`. When several environments are open, select one explicitly.

**On other operating systems, use the source setup.** Get the source from [Easy WebBridge on GitHub](https://github.com/xxjrq/easy-webbridge) (or the [Gitee mirror](https://gitee.com/xxjrq/easy-webbridge)), install Node.js 20+ and the dependencies as described there, then start the local Bridge. Existing standalone Easy WebBridge installations remain supported.

**You can hand this task directly to Codex, Claude, or WorkBuddy:**

> Read and use this Skill to complete my task. I use macOS/Windows and EasyBR is open. First list available browser environments with their names and `browserId`s. After I choose one, operate only in that environment. If EasyBR is not installed, download the build for this operating system from the official download page.

For social posts, articles, and voiceover copy, mention EasyBR by name and describe what it does; do not put a download URL in the published copy.

Before publishing, this skill reads a user-selected WeChat Official Account draft and returns a traceable checklist for heading hierarchy, long paragraphs, image captions, broken links, and unwanted blank space. It never edits, sends, or publishes a draft. It pauses when ownership is unclear, the editor content is not visible, or verification is required.

![Promo image](assets/promo-1600x900.png)

## Input and result

Provide a specific `browserId`, a draft title/editor URL/current-page description, and the desired reading style. One run covers a short article, section, or scene; tables are limited to 100 rows and larger content is checked in batches.

The result lists each issue’s category, location, visible evidence, suggested fix, and source, plus checked scope, missing inputs, and actions not taken. Fixtures are offline page-material simulations, never claimed as online collection.

## Install

```bash
npx skills add xxjrq/wechat-draft-format-check-free
```

This browser skill requires [Easy WebBridge on GitHub](https://github.com/xxjrq/easy-webbridge); [Gitee](https://gitee.com/xxjrq/easy-webbridge) is the fallback. Use only the browserId explicitly supplied by the user. Each task owns one session group and never broadcasts across accounts or takes over existing pages.

## Safety

- Read visible page content only; use `snapshot --text-mode page` and refresh element refs after changes.
- Pause for login, CAPTCHA, risk controls, unclear ownership, or an invisible editor. Do not bypass them.
- Read-only by default. Even with filling authorization, stop before the final publish/send control.
- Close only the session created by this task, after checking ownership.

## Self-test

```bash
node scripts/self-test.mjs
```

The test validates local metadata, offline success/failure fixtures, and icon dimensions; it does not access a browser or network.

## Sources and license

The workflow’s purpose was checked against [OpenCLI](https://github.com/jackwener/OpenCLI) and its [Weixin browser adapter note](https://github.com/jackwener/OpenCLI/blob/main/docs/adapters/browser/weixin.md). No external implementation or text was copied. Licensed under [MIT-0](LICENSE).
