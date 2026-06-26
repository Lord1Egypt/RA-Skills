# Changelog

## [0.12.0] - 2026-06-23

### Changed
- Decide drafting mode by **output length**, not account type. Long-form output (any thread, or a Premium single post) now produces one draft whose depth matches the source material, then iterates collaboratively — offer other angles for the user to opt into and/or propose specific improvements, revising until satisfied — instead of dumping multiple parallel drafts. Parallel multi-variant drafting (the 3-combinations / 2–3 drafts behavior) is now reserved for short Non-Premium single posts (≤ 280 chars).
- Clarify Step 4 Premium guidance: "tight" means no filler, not necessarily short; match length to the material and default to a fuller treatment for long/rich/structured sources. Scope the "3 best style combinations" rule (Step 1 and Key Rules) to short Non-Premium single posts. Prevents reflexively under-using the Premium character budget on rich source material.

## [0.11.0] - 2026-06-23

### Added
- `chinese-ai-tech-posts.md`: a language-specific reference for writing Chinese AI / Agent / LLM / tech-frontier X posts — hook types, structures, high-reuse sentence patterns, 10 reusable templates, media/hashtag discipline, posting-timing heuristics, a pre-publish checklist, A/B test variables, and a trimmed study-sources list. English instructions with Chinese example strings, matching the skill's existing EN/ZH precedent.
- Conditional pointer to the new reference from `SKILL.md` Step 5 and Key Rules; it applies only to Chinese AI/tech posts and supplements the Writing Principles.

## [0.10.0] - 2026-06-11

### Changed
- Authoring-standards compliance: added a "Not for…" scope boundary to the description (R2), and reworded the vault-write step to reference a notes-vault skill by capability ("a skill that writes to your notes vault, such as an `obsidian` skill") rather than by hardcoded name (R3), matching `saas-founder-content-writer` (R5). Bilingual EN/ZH voice examples retained intentionally.

## [0.7.3] - 2026-06-08

### Changed
- Rewrite Step 10 saving: drafts now go to a dedicated `X Posts/` subfolder with one file per day (`YYYY-MM-DD.md`) instead of the user's daily note.
- Add an explicit first-save location flow: use `OBSIDIAN_VAULT_PATH` if set, else a three-option prompt (folder path / `~/obsidianVault/X Posts/` default / skip). Resolve to an absolute path before writing.
- Define the write mechanism: delegate to an available `obsidian` skill when present, otherwise write the markdown file directly; on any write failure, paste the block in chat so content is never lost.
- Add a macOS-only hint shown only when a write fails under `~/Documents/` (iCloud sync / TCC permissions).
- Update the Output Format save prompt and Key Rules to match.

## [0.7.2] - 2026-06-07

### Changed
- `render-image-setup.md` / `CHANGELOG.md`: remove the literal Chromium sandbox-disabling flag tokens from prose. Docs now use a `<chromium-flags>` placeholder and link to Puppeteer's troubleshooting guide, so static security scanners no longer flag the documentation as a privilege-escalation pattern. No behavior change.

## [0.7.1] - 2026-06-07

### Changed
- `scripts/render-image.js`: stop hardcoding the Chromium sandbox-disabling launch flags; launch Chromium with the OS sandbox enabled by default and read optional extra flags from the `RENDER_CHROME_ARGS` environment variable. Linux/container users that need a disabled sandbox now opt in explicitly. Behavior is unchanged on macOS and standard desktops.
- `render-image-setup.md`: document the `RENDER_CHROME_ARGS` env var for sandbox-restricted environments.
- `README.md` / `SKILL.md`: clarify that Phase 1 research runs only when web/search tools are available and uses only the user-provided topic text, with no credentials or personal data transmitted.

## [0.7.0] - 2026-06-05

### Added
- HTML/CSS + headless Chrome image rendering for text/data graphics: `scripts/render-image.js` (Puppeteer, with system-Chrome and manual fallback), `scripts/package.json`, `render-image-setup.md`, and example templates `assets/quote-card.html`, `assets/data-card.html`.
- New "Rendering Text/Data Graphics" subsection and a decision rule for when to render via HTML/CSS vs. an image model vs. a real screenshot.

### Changed
- Extended Step 8 image brief with a `Render method:` line and guidance to render text/data graphics directly to PNG.

## [0.5.7] - 2026-05-29
- Remove hardcoded `obsidian-vault-writer` skill reference in Step 10; now uses generic language to support any installed Obsidian skill.

## [0.5.6] - 2026-05-28
Rewrote frontmatter description to concise 200–500 character format for improved agent-trigger clarity.

## [0.5.5] - 2026-05-28

- Replace Google Sheets output (Step 10) with Obsidian vault writing via `obsidian-vault-writer` skill
- Remove `google-sheet-sync.md` and `scripts/` directory

## [0.5.4] - 2026-05-21

### Added
- Feedback prompt in README.md and conditional feedback section in SKILL.md

## [0.5.3] - 2026-05-20
- Fix `getCredentials()` in `save_to_sheet.js`: load `client_id`/`client_secret` from `credentials.json` before token cache check so token refresh works correctly
- Add `normalizeToken()` to handle Python-client token format (`token` → `access_token`, `expiry` → `expiry_date`) so tokens created by other Google OAuth clients are reused without re-auth

## [0.5.2] - 2026-05-20
- Migrate `scripts/save_to_sheet.py` → `scripts/save_to_sheet.js` (Node.js); identical CLI interface and output; depends only on `googleapis` via `npm install` in the `scripts/` directory; removes Python runtime requirement
- Add `scripts/package.json`; delete `scripts/save_to_sheet.py`
- Update `google-sheet-sync.md` and `SKILL.md` to reference `node` / `npm install` instead of `python` / `pip`

## [0.5.1] - 2026-05-20
- Rewrite `google-sheet-sync.md` with wizard structure: First-time setup (Python dependency install as step 1, OAuth2 promoted to Option A for personal use), Daily use, and Reference sections; add verify command
- Fix `SKILL.md` Step 10 to clarify script path resolution and surface dependency install check before first save

## [0.5.0] - 2026-05-20
- Add Step 10: optional Google Sheets storage with session mode and per-tweet mode
- Add `google-sheet-sync.md`: sheet column structure, deeplink format, auth setup (service account + OAuth2), usage examples
- Add `scripts/save_to_sheet.py`: appends variants as side-by-side columns with `=HYPERLINK()` deeplinks for one-click X publishing; CSV fallback on failure

## [0.4.2] - 2026-05-18
Added Writing Principles section with 7 concrete principles (natural voice, subjective perspective, scene grounding, cut ornate language, no forced profundity, specific beats vague, leave room). Each principle includes before/after examples in English and Chinese. Added Writing Principles row to Step 9 review rubric.

## [0.4.1] - 2026-05-14
Added two-phase workflow: research phase with context enrichment and fact verification, plus voice calibration to preserve the author's writing style.

## [0.3.1] - 2026-05-01
Improved required inputs and smarter defaults for format selection and thread structure.
