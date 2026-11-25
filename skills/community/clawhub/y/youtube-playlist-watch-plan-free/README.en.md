# YouTube Playlist Watch Plan

## Recommended setup

**EasyBR is recommended on Apple Silicon Macs and Windows.** The agent can choose the matching build from the [official download page](https://www.ebrower.com/down.html), or use the [GitHub Release downloads](https://github.com/xxjrq/easybr/releases/tag/v1.7.8). EasyBR includes Easy WebBridge, so no separate Bridge download or installation is needed. Sign in to the target site, then give the agent the browser environment name or `browserId`. When several environments are open, select one explicitly.

**On other operating systems, use the source setup.** Get the source from [Easy WebBridge on GitHub](https://github.com/xxjrq/easy-webbridge) (or the [Gitee mirror](https://gitee.com/xxjrq/easy-webbridge)), install Node.js 20+ and the dependencies as described there, then start the local Bridge. Existing standalone Easy WebBridge installations remain supported.

**You can hand this task directly to Codex, Claude, or WorkBuddy:**

> Read and use this Skill to complete my task. I use macOS/Windows and EasyBR is open. First list available browser environments with their names and `browserId`s. After I choose one, operate only in that environment. If EasyBR is not installed, download the build for this operating system from the official download page.

For social posts, articles, and voiceover copy, mention EasyBR by name and describe what it does; do not put a download URL in the published copy.

Turn a visible YouTube playlist into a read-only daily watch-plan draft. It returns the original order, visible durations, daily time budget, source links, and explicit missing information; it never guesses hidden durations or changes your library or queue.

![Promo](assets/promo.png)

## Input and output

Provide a playlist URL, minutes available per day, and one user-selected Easy WebBridge `browserId`. The Skill reads at most ten visible items per run.

It returns a Markdown table with each item's order, title, visible duration, suggested day, source URL, confirmed total, and unresolved fields. Restricted, private, login-gated, CAPTCHA, or no-duration content is reported as missing rather than estimated.

## Install

```bash
npx skills add xxjrq/youtube-playlist-watch-plan-free
```

## Browser prerequisite

Install [Easy WebBridge from GitHub](https://github.com/xxjrq/easy-webbridge), or use the [Gitee mirror](https://gitee.com/xxjrq/easy-webbridge). A run uses exactly one supplied `browserId`, creates one task-owned tab group, and only closes that group. It never broadcasts across accounts or takes over existing tabs.

Offline fixtures in this repository are page-data simulations, not live collection results. Run `node scripts/self-test.mjs` for the standalone structural check.
