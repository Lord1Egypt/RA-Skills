# Session 2026-05-18 — Detail Page Sidebar + Bottom Data Modules

## Trigger

The user reported that `https://www.900az.com/azos07/1553.html` and related game/app/news detail pages were missing right-side and bottom "other column" data, and that the implementation had not followed the `demo_xz01` detail-page design norm.

## Durable Lesson

For xz01 detail-page repairs, the acceptance target is not only that the detail body renders. “详情页” means every active PC/mobile detail template in the theme, not only the reported URL or a few representative pages. Enumerate and cover all `show_*` / detail templates, including collection/topic detail templates when present.

PC and mobile detail templates must render the surrounding data ecosystem that makes the page feel like the demo download portal:

- PC app/software detail: mixed right sidebar with hot apps/downloads + game recommendations/ranking + guide/news ranking; bottom same-category resources + more news.
- PC game detail: mixed right sidebar with game ranking + hot apps/software + guide/news ranking; bottom same-category games + more news.
- PC news/article detail: mixed right sidebar with hot news/guide ranking + game/app recommendations; bottom same-category news + guesses/recommendations.
- PC collection/topic detail: when present, mixed right/sidebar and bottom modules with related topic/category content + game recommendations + apps/software + news/guide.
- Mobile app/game/news/collection detail: stacked same-category resources, app/software recommendations, game rankings/recommendations, more news/guides, and guesses/recommendations appropriate to the page type.

A PC right sidebar that is only攻略/资讯排行 is not acceptable even if it has data; it must visibly include game and app/software modules too.

Use real existing data through the project's existing template/data helpers. Do not create routes, patch PHP/controllers, or use fake SVG/filler data.

## Implementation Pattern

1. Compare the current theme's detail templates against `demo_xz01` detail pages, treating demo as read-only.
2. Keep changes theme-only under `public/themes/<theme>/**`.
3. Add or repair existing data calls for:
   - `cms_appsoft` resources.
   - `cms_apparticle` news/guide lists.
   - Filters such as `a.is_hide = 0`, `a.status = 1`, and `a.delete_time = 0` when using existing `getAllData()` style patterns.
4. Prefer existing partials/classes/modules in the active theme; do not wholesale copy demo markup.
5. Clear `/www/wwwroot/www.900az.com/runtime/*` after changes.

## Validation Pattern

Do not accept HTTP/source checks alone. Detail sidebar/bottom repairs require:

- PC + mobile HTTP 200 checks for target and representative app/game/news/collection detail URLs.
- Source/DOM checks that every active detail template type is represented by an existing database-backed URL.
- Source/DOM checks that PC right sidebars contain mixed app/software + game + news/guide modules, not only攻略/资讯 lists.
- Source/DOM checks that mobile bottom recommendation modules also contain mixed app/game/news/guide content.
- Static hard-gate checks: no mobile `target="_blank"`, no `cms/page/index/id`, no duplicate host, no `data:image/svg` filler, and balanced template tags.
- PC/mobile screenshots plus AI visual review.
- If AI catches a layout issue, patch and re-run focused screenshot/AI verification on the failed viewport/module.

## Pitfall: Bottom Text Overflow

When adding PC bottom news/guide lists, long summaries can visually overflow the white container even if source checks pass. Fix with shrink-safe CSS on the related-news module:

- `box-sizing:border-box` for the module and descendants.
- `article { width:100%; min-width:0; overflow:hidden; }`
- content wrapper with explicit available width or flex-safe `min-width:0`.
- title/summary with `display:block; width:100%; max-width:100%; overflow:hidden; text-overflow:ellipsis;`.
- preserve readable truncation rather than allowing text to spill into the gray background.

## Artifact Boundary Reminder

Validation scripts and screenshots must not be written under `/root/.openclaw`. Use `/tmp`, `/www/wwwroot/www.900az.com/test-artifacts/...`, and `/root/.hermes/workspace/xz01-artifacts/...` instead.