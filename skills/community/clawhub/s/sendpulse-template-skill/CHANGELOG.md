# Changelog — sendpulse-template-skill

Versioning: `vMAJOR.MINOR`. MAJOR = breaking changes to rules/structure; MINOR = additive rules,
references, examples, or fixes.

## v1.5 — 2026-07-13
- **Published to GitHub.** Placeholder repository URLs replaced with the real monorepo paths
  (`github.com/sendpulse/sendpulse-skills`, folder `sendpulse-template-skill/`); the version
  self-check added in v1.4 now points at the live
  `raw.githubusercontent.com/sendpulse/sendpulse-skills/main/sendpulse-template-skill/VERSION`.

## v1.4 — 2026-07-06
- **Self-update check.** Added a `VERSION` file and a "Keeping this skill up to date" section in
  SKILL.md: with web access, the assistant may compare the local version against the published
  `VERSION` on GitHub raw once per conversation and suggest updating; never blocks the task.
- **Skill-family cross-links.** New Output step 6 hands off out-of-scope work: campaign management
  (books, segments, scheduling, analytics) → `sendpulse-email-skill`; transactional sends →
  `sendpulse-smtp-skill`. Added `metadata.homepage`.

## v1.3 — 2026-06-19
- **Switched output to a complete HTML document** (`<!DOCTYPE/html/head/body`, `<style>` in `<head>`) —
  matches SendPulse's own exports and the *Upload a file* path. Updated the rule in SKILL.md and
  html-rules.md (§1, R1.1); a body-only fragment is still noted as valid for the *Insert code* editor.
  All `assets/examples/` are now full documents.
- **Fixed Outlook conditional comments** that an HTML formatter had split across lines (broke ghost
  tables / VML). Restored intact examples; added an anti-pattern: never prettify a finished template.
- Corrected this changelog (4 real example templates, not 2).

## v1.2 — 2026-06-19
- **Media-query-independent responsiveness (R3.0).** Responsive behavior (column stacking, fluid
  width) is built on inline styles (`display:inline-block` + `max-width` + MSO ghost tables, fluid
  `bodyTable`) so it survives clients that strip `<style>` (notably the Gmail app); `@media` becomes a
  progressive-enhancement layer only. Replaces the media-query-only `.tc responsive` column approach.
- Added rules: button rows stack media-query-free (+ `padding-bottom`); pad content away from the
  seam between differently colored sections.

## v1.0 — 2026-06-15
Initial public release.

- Generates responsive **HTML email documents** for the SendPulse builder (600px; light & dark;
  any language including RTL and Cyrillic).
- **Dual-mode** behavior: Quick (beginners — fast, few questions) and Pro (marketers — full depth).
- **references/**: `html-rules.md` (canonical, derived from 15 production SendPulse templates),
  `email-types.md`, `content-copywriting.md`, `i18n.md`, `dark-mode-accessibility.md`,
  `style-directions.md`, `variables-analytics.md`, `brand-profile.md`, `sendpulse-mcp.md`,
  `sendpulse-api.md`.
- **assets/examples/**: 3 teaching templates (promo, welcome, transactional) + 4 real SendPulse
  production templates (`real-sendpulse-*`: black-friday, webinar, digest/newsletter, welcome) as
  ground truth.
- Covers MCP/API upload, File Manager image URLs, UTM, analytics, A/B testing, unsubscribe,
  personalization variables, layout variety, and a platform-neutral Self-QA checklist.
- Documents the **ZIP-with-images upload** path (New template → Upload a file → zip of HTML + images
  in the archive root, bare-filename `src`, "Upload images to the server SendPulse") — verified working.
