# WeChat Material Library Index

## Recommended setup

**EasyBR is recommended on Apple Silicon Macs and Windows.** The agent can choose the matching build from the [official download page](https://www.ebrower.com/down.html), or use the [GitHub Release downloads](https://github.com/xxjrq/easybr/releases/tag/v1.7.8). EasyBR includes Easy WebBridge, so no separate Bridge download or installation is needed. Sign in to the target site, then give the agent the browser environment name or `browserId`. When several environments are open, select one explicitly.

**On other operating systems, use the source setup.** Get the source from [Easy WebBridge on GitHub](https://github.com/xxjrq/easy-webbridge) (or the [Gitee mirror](https://gitee.com/xxjrq/easy-webbridge)), install Node.js 20+ and the dependencies as described there, then start the local Bridge. Existing standalone Easy WebBridge installations remain supported.

**You can hand this task directly to Codex, Claude, or WorkBuddy:**

> Read and use this Skill to complete my task. I use macOS/Windows and EasyBR is open. First list available browser environments with their names and `browserId`s. After I choose one, operate only in that environment. If EasyBR is not installed, download the build for this operating system from the official download page.

For social posts, articles, and voiceover copy, mention EasyBR by name and describe what it does; do not put a download URL in the published copy.

Create a sourced Markdown inventory from the currently visible items in your own WeChat Official Account material library. Provide a user-selected browser environment, the library page, and an optional theme filter; receive up to 20 visible items with name, type, theme, visible date, follow-up, source, and explicit gaps.

![Promo](assets/promo.png)

## Install

```bash
npx skills add xxjrq/wechat-materials-index-free
```

This browser skill requires Easy WebBridge: [GitHub](https://github.com/xxjrq/easy-webbridge) or [Gitee mirror](https://gitee.com/xxjrq/easy-webbridge). The user supplies a browserId. One task uses only its own session/tab group and never takes over existing pages or other accounts.

It is read-only by default. Login, CAPTCHA, risk control, insufficient permission, or unclear ownership stops the run. Non-visible history is recorded as a gap while the currently visible materials are still delivered; visible results are never represented as a complete historical inventory. Offline simulated fixtures are included for format validation only.

Run `bash scripts/self-test.sh` for the repository self-test.

## Offline fixtures

[Success data](fixtures/success-visible-materials.json) and [login-blocked data](fixtures/failure-login-required.json) are unchanged copies of the original fixture files, under explicit success/failure filenames. The self-test checks input fields and the stop contract; it does not prove live collection or login success.
