# Product Listing Missing-Field Check

## Recommended setup

**EasyBR is recommended on Apple Silicon Macs and Windows.** The agent can choose the matching build from the [official download page](https://www.ebrower.com/down.html), or use the [GitHub Release downloads](https://github.com/xxjrq/easybr/releases/tag/v1.7.8). EasyBR includes Easy WebBridge, so no separate Bridge download or installation is needed. Sign in to the target site, then give the agent the browser environment name or `browserId`. When several environments are open, select one explicitly.

**On other operating systems, use the source setup.** Get the source from [Easy WebBridge on GitHub](https://github.com/xxjrq/easy-webbridge) (or the [Gitee mirror](https://gitee.com/xxjrq/easy-webbridge)), install Node.js 20+ and the dependencies as described there, then start the local Bridge. Existing standalone Easy WebBridge installations remain supported.

**You can hand this task directly to Codex, Claude, or WorkBuddy:**

> Read and use this Skill to complete my task. I use macOS/Windows and EasyBR is open. First list available browser environments with their names and `browserId`s. After I choose one, operate only in that environment. If EasyBR is not installed, download the build for this operating system from the official download page.

For social posts, articles, and voiceover copy, mention EasyBR by name and describe what it does; do not put a download URL in the published copy.

Turn the visible information on a user-selected product-editing page into a practical table for specifications, media, shipping, and after-sales gaps or conflicts. Input: that page, optional merchant rules, and a user-selected browser environment. Each row includes a status (`已见`, `缺项`, `冲突`, or `待确认`), visible value, source, and suggested human action. Fields absent from the page snapshot are `待确认`; only explicitly empty values are `缺项`. It never saves, submits, or publishes.

![Product listing check promo](assets/promo.png)

## Run

```bash
npx skills add xxjrq/shop-listing-missing-fields-free
npm run self_test
node scripts/check-listing.mjs --offline-page fixtures/success-page.json --rules fixtures/rules.json
```

The fixtures are offline page-material simulations, not live collection results. A result row has category, field, status, visible value, source, and an action for a human reviewer.

## Browser prerequisite and safety

For a live page, install [Easy WebBridge on GitHub](https://github.com/xxjrq/easy-webbridge), or use the [Gitee mirror](https://gitee.com/xxjrq/easy-webbridge). The runtime uses exactly one user-specified `browserId`, one owned task session, and one task tab group. It does not broadcast to accounts, take over existing pages, or close user tabs.

Run the checker with the user-selected `browserId` and `--page-url`. It creates an owned session and tab group, confirms ownership with `list_tabs`, reads visible page text plus explicit visible control-label relationships (`label[for]`, wrapping labels, or `aria-labelledby`), then closes only its own session. It never pairs controls by order or nearby text. Source URLs retain only origin and path, removing queries and fragments. If a merchant rule targets an unread field, its expected value and action remain in the human task. Login, CAPTCHA, risk control, truncated snapshots, and malformed JSON stop the run without producing a gap table. Fields absent from the snapshot are marked `待确认`; only explicitly empty values are `缺项`. Default mode is read-only; even when draft filling is separately authorized, it must not click a final publish or send action.

Business use was informed by [ERPNext](https://github.com/frappe/erpnext), without copying source or implementation text. Licensed under [MIT-0](LICENSE).
