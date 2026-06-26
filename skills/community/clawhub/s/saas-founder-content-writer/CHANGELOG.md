# Changelog

## [0.12.0] - 2026-06-15

### Added
- Step 8 gains two one-pass platform readiness checks that run inside the single revise pass:
  - **Xiaohongshu virality-readiness check** (cover hook, title pull, opening retention, save value, tag fit). It catches structural misses rather than predicting virality, and forbids a re-score / re-optimize loop (which regresses drafts toward generic copy).
  - **YouTube Shorts click-readiness check** (thumbnail hook, title pull, description hook, Shorts hygiene), scoped only to the click surface this skill produces — retention/script quality stays out of scope, owned by the video pipeline.

  Both forbid a re-score / re-optimize loop. Synced the README Phase 4 summary.

## [0.11.0] - 2026-06-12

### Changed
- Step 7 now defines an explicit Xiaohongshu image-count rule: the carousel size is derived from the finished draft (1 cover + one card per distinct body unit — a numbered/bulleted point, data/metric block, framework/comparison, or standout quote), with a floor of 1 and a hard ceiling of 18. The image brief gains a `Cards:` line that states the planned count and what each card shows; the set is produced in one pass without a confirmation prompt. Synced the Step 8 "Image fit" rubric row, the Output Format image block, the carousel rendering note, and Key Rules.

## [0.10.0] - 2026-06-11

### Added
- Product/Knowledge content-angle mode: Knowledge mode drops the product gate, captures a topic profile instead, and uses knowledge angles (explainer / how-it-works / myth-busting / pitfalls·retrospective / comparison / "what this means for you").
- YouTube platform rules (title / description / thumbnail brief; default 9:16 Shorts) and a 9:16 `youtube-thumbnail.html` template for `render-image.js`.

### Changed
- Broadened the skill identity (description, intro, core principle) from SaaS-only to founders **and** creators, covering knowledge content and YouTube. Skill name unchanged.
- Converted all skill text, examples, and templates to English (Product/Knowledge mode labels; Xiaohongshu Title/Body/Tags); vault delegation now references a notes-vault skill by capability rather than a hardcoded name.

## [0.8.0] - 2026-06-08

### Added
- New Step 9 "Save To Vault (Optional)": opt-in archiving of finalized drafts to `<vault>/Founder Posts/YYYY-MM-DD.md`, one file per day. Reuses the env-var / named-path / three-option location resolution, `obsidian`-skill delegation, and graceful chat fallback. Rendered PNGs (Xiaohongshu covers / data cards) are copied into `Founder Posts/attachments/` and embedded with Obsidian `![[...]]`; when no PNG was rendered, the image brief is saved instead. The per-section file format records angle, platform, and platform-specific fields (X thread numbering, Reddit title/body, Xiaohongshu Title/Body/#Tags).

### Changed
- Output Format gains a first-draft "Save to vault?" prompt line; Key Rules document the opt-in save behavior. README lists the new step.

## [0.7.2] - 2026-06-07

### Changed
- `scripts/render-image.js`: stop hardcoding the Chromium sandbox-disabling launch flags; launch Chromium with the OS sandbox enabled by default and read optional extra flags from the `RENDER_CHROME_ARGS` environment variable. Container/CI users opt in explicitly. No behavior change on macOS / standard desktops. This removes the privilege-escalation pattern that static security scanners flagged.
- `render-image-setup.md`: document `RENDER_CHROME_ARGS` using a `<chromium-flags>` placeholder and a link to Puppeteer's troubleshooting guide, with no literal flag tokens in prose.

## [0.7.0] - 2026-06-05

### Added
- Xiaohongshu platform support: platform option in intake, a dedicated Platform Rules section (image-first cover, title/body/tags conventions, soft-promotion norms), output format and key-rule updates, and Chinese-by-default behavior.
- New Step 7 "Decide Whether An Image Helps" with an image brief, plus a "Rendering Text/Data Graphics" subsection for HTML/CSS + headless Chrome rendering and a decision rule for when to render vs. use an image model vs. a real screenshot. Xiaohongshu always requires a cover.
- Rendering tooling: `scripts/render-image.js` (Puppeteer, with system-Chrome and manual fallback), `scripts/package.json`, `render-image-setup.md`, and example templates `assets/xiaohongshu-cover.html`, `assets/data-card.html`.

### Changed
- Renumbered the review step (Score And Revise) to Step 8 and added an "Image fit" rubric row. Updated the skill description and README to cover Xiaohongshu and image rendering.

## [0.6.0] - 2026-06-02
- Initial release of `saas-founder-content-writer`: a self-contained skill that turns founder product updates, user pain points, technical lessons, and observations into high-signal posts for X, Reddit, and LinkedIn.
- Four-phase workflow (Intake → Choose the angle → Draft → Review) with a portable product profile, 8 content angles, six writing principles with before/after examples, per-platform rules (X / Reddit / LinkedIn), a review rubric, and safety boundaries against fabricated claims.
