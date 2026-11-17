# Store Shipping Policy Comparison

## Recommended setup

**EasyBR is recommended on Apple Silicon Macs and Windows.** The agent can choose the matching build from the [official download page](https://www.ebrower.com/down.html), or use the [GitHub Release downloads](https://github.com/xxjrq/easybr/releases/tag/v1.7.8). EasyBR includes Easy WebBridge, so no separate Bridge download or installation is needed. Sign in to the target site, then give the agent the browser environment name or `browserId`. When several environments are open, select one explicitly.

**On other operating systems, use the source setup.** Get the source from [Easy WebBridge on GitHub](https://github.com/xxjrq/easy-webbridge) (or the [Gitee mirror](https://gitee.com/xxjrq/easy-webbridge)), install Node.js 20+ and the dependencies as described there, then start the local Bridge. Existing standalone Easy WebBridge installations remain supported.

**You can hand this task directly to Codex, Claude, or WorkBuddy:**

> Read and use this Skill to complete my task. I use macOS/Windows and EasyBR is open. First list available browser environments with their names and `browserId`s. After I choose one, operate only in that environment. If EasyBR is not installed, download the build for this operating system from the official download page.

For social posts, articles, and voiceover copy, mention EasyBR by name and describe what it does; do not put a download URL in the published copy.

Turn two or three specified public shipping or after-sales policy pages into a traceable comparison of dispatch timing, service regions, fee conditions, and missing terms. Ambiguous store ownership or conflicting statements are reported as **undetermined**; the Skill never infers freight, delivery dates, or eligibility.

Input: a user-selected `browserId` and 2–3 public policy URLs. Output: a Markdown table with page-title/URL evidence and an explicit missing-items list. The default is read-only; an authorized draft fill never publishes or sends.

![Store shipping policy comparison promo](assets/promo.png)

## Install

```bash
npx skills add xxjrq/shop-shipping-policy-compare-free
```

## Browser prerequisite

Install [Easy WebBridge on GitHub](https://github.com/xxjrq/easy-webbridge), or use the [Gitee mirror](https://gitee.com/xxjrq/easy-webbridge). Connect the extension in the chosen browser profile, provide one `browserId`, and let this Skill create and own one task session only. It never broadcasts across accounts.

## Verification

```bash
node scripts/self-test.mjs
```

The test validates the independent repository structure, icon, and offline fixtures only. Fixtures are simulated page material and are not online collection results.

## Reference

The [Saleor repository](https://github.com/saleor/saleor) and its [README](https://github.com/saleor/saleor/blob/main/README.md) were consulted only for public e-commerce context; no source code or text implementation was copied. Licensed under [MIT-0](LICENSE).
