# Shop Customer Reply Drafts

## Recommended setup

**EasyBR is recommended on Apple Silicon Macs and Windows.** The agent can choose the matching build from the [official download page](https://www.ebrower.com/down.html), or use the [GitHub Release downloads](https://github.com/xxjrq/easybr/releases/tag/v1.7.8). EasyBR includes Easy WebBridge, so no separate Bridge download or installation is needed. Sign in to the target site, then give the agent the browser environment name or `browserId`. When several environments are open, select one explicitly.

**On other operating systems, use the source setup.** Get the source from [Easy WebBridge on GitHub](https://github.com/xxjrq/easy-webbridge) (or the [Gitee mirror](https://gitee.com/xxjrq/easy-webbridge)), install Node.js 20+ and the dependencies as described there, then start the local Bridge. Existing standalone Easy WebBridge installations remain supported.

**You can hand this task directly to Codex, Claude, or WorkBuddy:**

> Read and use this Skill to complete my task. I use macOS/Windows and EasyBR is open. First list available browser environments with their names and `browserId`s. After I choose one, operate only in that environment. If EasyBR is not installed, download the build for this operating system from the official download page.

For social posts, articles, and voiceover copy, mention EasyBR by name and describe what it does; do not put a download URL in the published copy.

![Shop reply drafts: turn buyer questions into ready-to-copy replies](assets/promo-1600x900.png)
A free Markdown Skill with no third-party API key required. It turns product facts, store policies, and buyer questions into short, copy-ready customer-service drafts. It does not connect to a customer-service API or send messages. Provide the facts and question to receive a reply draft and a short list of any missing information.

## What it does

It returns a pre-sales, after-sales, or manual-review classification; a natural Chinese reply draft; missing information; and items to verify. It never invents stock, refund eligibility, shipping dates, delivery dates, discounts, or order status.

Use [fixtures/success.json](fixtures/success.json) for a ready-to-run input and compare it with [fixtures/success.expected.md](fixtures/success.expected.md). [fixtures/failure.json](fixtures/failure.json) demonstrates how missing order and policy data is surfaced instead of guessed.

## Optional browser verification

The Skill works without a browser. For separately authorized checks in an already logged-in shop page, install [Easy WebBridge on GitHub](https://github.com/xxjrq/easy-webbridge), with [Gitee](https://gitee.com/xxjrq/easy-webbridge) as a mirror. Select one explicit `browserId`, create one isolated session group per task, and never broadcast across accounts. Verification only informs a draft; sending remains a user decision.

## Self-test

```bash
node scripts/self-test.mjs
```

## Attribution and license

This is an original implementation under the [MIT-0 License](LICENSE). It only checked the public Skill directory conventions in [Anthropic Skills](https://github.com/anthropics/skills) and the installation entry point of [Easy WebBridge](https://github.com/xxjrq/easy-webbridge); no code or documentation was copied. Each referenced repository retains its own license.

## Install

```bash
npx skills add xxjrq/shop-customer-reply-drafts
```

Alternatively, copy this repository folder into your Agent’s skill directory, then invoke `$shop-customer-reply-drafts` with your input.
