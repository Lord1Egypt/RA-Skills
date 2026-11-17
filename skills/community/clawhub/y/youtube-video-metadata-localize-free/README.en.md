# YouTube Public Video Metadata Localization

## Recommended setup

**EasyBR is recommended on Apple Silicon Macs and Windows.** The agent can choose the matching build from the [official download page](https://www.ebrower.com/down.html), or use the [official EasyBR downloads page](https://www.ebrower.com/down.html). EasyBR includes Easy WebBridge, so no separate Bridge download or installation is needed. Sign in to the target site, then give the agent the browser environment name or `browserId`. When several environments are open, select one explicitly.

**On other operating systems, use the source setup.** Get the source from [Easy WebBridge on GitHub](https://github.com/aiispower/easy-webbridge) (or the [Gitee mirror](https://gitee.com/xxjrq/easy-webbridge)), install Node.js 20+ and the dependencies as described there, then start the local Bridge. Existing standalone Easy WebBridge installations remain supported.

**You can hand this task directly to Codex, Claude, or WorkBuddy:**

> Read and use this Skill to complete my task. I use macOS/Windows and EasyBR is open. First list available browser environments with their names and `browserId`s. After I choose one, operate only in that environment. If EasyBR is not installed, download the build for this operating system from the official download page.

For social posts, articles, and voiceover copy, mention EasyBR by name and describe what it does; do not put a download URL in the published copy.

Turn one authorized, publicly visible YouTube video into a reviewable Chinese metadata draft. Provide a video URL, Chinese audience guidance, and a chosen `browserId`; receive original-title/description points, Chinese title/description drafts, source URLs, and explicit gaps. It is read-only by default and never changes YouTube Studio.

![Promo image](assets/promo.png)

Install with `npx skills add xxjrq/youtube-video-metadata-localize-free`. On Apple Silicon Macs and Windows, use EasyBR with built-in Easy WebBridge as described in the official guide. For ordinary browsers, follow the [official EasyBR AI operation guide](https://www.ebrower.com/helperdoc/ai-agent-workflow.html) to configure standalone Bridge from [GitHub](https://github.com/aiispower/easy-webbridge) or [Gitee](https://gitee.com/xxjrq/easy-webbridge). Use one requested browser environment and a task-owned session only.

Run `node scripts/self-test.mjs` for offline fixture validation. Fixtures simulate visible pages; they are not online collection results.

See [SKILL.md](SKILL.md) for browser workflow and boundaries.


## Translation is an Agent task

The Agent translates actual visible text and adapts wording to the requested Chinese audience while preserving facts. `compose-draft.mjs` only validates and assembles separately supplied translations; it is not a local general translator. Each translated title and point must retain its exact original, index, source URL and field. The Agent must review semantic fidelity; the script cannot prove it. Invisible descriptions remain empty.

```bash
node scripts/compose-draft.mjs --input fixtures/success-page.json --translations fixtures/success-translations.json --output /tmp/localized.json
```

An independent cycling-text case demonstrates [beginner wording](fixtures/forward-beginner.json) and [experienced-audience wording](fixtures/forward-experienced.json) from the same source facts. The [hidden-description case](fixtures/forward-failure.json) does not invent details. These are actual Agent translations assembled by an executed script from offline text materials; no browser, source-page visit, or online success is claimed. The self-test checks assembly, per-point provenance and four invalid-contract rejections, not translation quality.

## EasyBR AI onboarding and task completion

Read the official [EasyBR AI operation guide](https://www.ebrower.com/helperdoc/ai-agent-workflow.html);  current EasyBR builds include the Bridge and browser extension on Apple Silicon Macs and Windows, so no separate Bridge installation is needed there. Ordinary browsers and other systems should follow the current Easy WebBridge setup described in the official guide.

For a browser task the user has authorized through this Skill, check and reuse a suitable existing environment first. If a new one is genuinely needed, create one unique environment for this task with safe defaults, read back its actual environment ID, and start it. Do not ask the user to reconfirm or supply an environment name or default parameters. After confirming the correct account and `browserId`, continue the user's current task instead of stopping at setup instructions; do not ask for approval at each necessary step. Pause only for CAPTCHA/account security checks, real ambiguity about the target account or authorization, or missing local-control capability. At completion, close only the task tab group created for this run and report results and limits under this Skill's rules.

This Skill provides the business workflow. Automatic installation, sign-in assistance, and environment management also depend on the AI agent's local-control capabilities and the components described in the official guide.
