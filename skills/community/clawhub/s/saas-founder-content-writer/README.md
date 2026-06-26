# SaaS Founder Content Writer

**Platforms:** Claude · Openclaw · Codex
**Domain:** Writing

## Purpose

A content editor for founders and creators — SaaS founders, indie hackers, and product builders. It turns what the author actually knows — product updates, support tickets, technical lessons, usage data, personal observations, or a topic they can teach — into high-signal posts for X, Reddit, LinkedIn, Xiaohongshu, and YouTube. It works in two modes: a **Product** mode for posts about your own product, and a **Knowledge** mode for teaching a topic with no product gate. It refuses to write generic marketing copy: posts earn attention by being specific, honest, and useful to the reader first.

## When to Use

- When you have a product update, launch, or changelog and want a post that leads with what users can now do
- When a user pain point, support pattern, or piece of feedback could become a useful public post
- When you want to share a build-in-public metric, a lesson learned, or a market opinion
- When you want to teach or explain a topic (Knowledge mode) — explainer, how-it-works, myth-busting, pitfalls·retrospective — with no product to pitch
- When you need a feedback request that people will actually answer
- When you want the same material adapted to X, Reddit, LinkedIn, Xiaohongshu, or YouTube norms
- When you need an image — a Xiaohongshu cover, a YouTube 9:16 thumbnail, a quote card, or a data card — rendered from HTML/CSS
- When you want finalized drafts (and their rendered images) archived to your Obsidian vault

It is **not** for ad creative, generic brand copy, or posts with no underlying substance.

## What It Does

**Phase 1: Intake**
0. Picks the content mode — Product or Knowledge
1. In Product mode, captures a portable product profile (category, users, pain point, optional house themes) — never hardcoded; in Knowledge mode, captures a topic profile (topic, target reader, takeaway, raw knowledge material) with no product gate
2. Captures the assignment (raw material, platform, format) and refuses to draft without real material
3. Sets the goal and reader takeaway

**Phase 2: Choose the angle**
4. Selects from 8 product angles (Product mode) or 6 knowledge angles (Knowledge mode: explainer, how-it-works, myth-busting, pitfalls·retrospective, comparison, "what this means for you")

**Phase 3: Draft**
5. Applies six writing principles (specific, useful-before-promotional, honest, scene-first, no forced profundity, no hype) with before/after examples
6. Applies platform rules for X, Reddit, LinkedIn, Xiaohongshu, and YouTube
7. Decides whether an image helps (Xiaohongshu always needs a cover, plus a content-derived card count — one card per distinct body point, capped at 18; YouTube Shorts uses a 9:16 thumbnail) and, for text/data graphics, renders it from HTML/CSS
8. Writes an open that earns the next line

**Phase 4: Review**
9. Scores against a rubric (not-an-ad, specific, angle clear, platform fit, honest, human voice, strong open, image fit) and revises — Xiaohongshu posts also get a one-pass virality-readiness check (cover hook, title pull, opening retention, save value, tag fit), and YouTube gets a one-pass click-readiness check (thumbnail hook, title pull, description hook, Shorts hygiene); both run in the single revise pass with no re-optimize loop
10. Optionally saves the finalized draft — and any rendered cover/cards — to an Obsidian vault subfolder (`Founder Posts/`), opt-in and never to your own notes

## Image Generation

For text- and data-driven graphics — Xiaohongshu covers and image cards, YouTube 9:16 Shorts thumbnails, quote cards, data/metric cards, frameworks, comparisons, changelog cards — the skill can render a PNG from HTML/CSS using headless Chrome (`scripts/render-image.js`, Puppeteer-based). This is deterministic and batchable. Photographic images and real product screenshots are out of scope for the renderer. First-time setup is in [`render-image-setup.md`](render-image-setup.md); example templates live in `assets/` (including `youtube-thumbnail.html` for 9:16 Shorts).

## Notes

This skill is self-contained and does not depend on other skills. For general-purpose X drafting from any source material (not founder-specific), see [x-post-strategist](../x-post-strategist/README.md).

Reddit self-promotion rules vary by subreddit; the skill always reminds you to check the target subreddit's rules before posting. Xiaohongshu penalizes hard ads and off-platform redirection, so the skill keeps promotion soft and reminds you to check the platform's rules. The skill never invents metrics, quotes, or results, and never posts on your behalf.

## Feedback & Contributions

Found a gap or have a suggestion? [Open an issue or PR](https://github.com/archlab-space/open-skill-hub/issues) — improvements are welcome.
