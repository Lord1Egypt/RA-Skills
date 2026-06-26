# Session 2026-05-18 — All Detail Pages Need Mixed Sidebar Modules

## Trigger

After an initial detail-page repair, the user corrected the scope:

```text
是所有详情页,
并且,右侧排版过于单一,只有攻略,没有游戏应用.
```

The first fix had focused on representative software/game/news detail pages and allowed the PC right sidebar to be too list-like and guide-heavy. The real acceptance target is every active detail template and a mixed data ecosystem in the right/sidebar and bottom areas.

## Durable Rule

For xz01, "详情页" means all active detail templates in the theme, not just one reported URL or three representative pages. At minimum, enumerate and handle:

- PC software/app detail (`cms/show_soft_detail.html` or equivalent)
- PC game detail (`cms/show_game_detail.html` or equivalent)
- PC news/article detail (`cms/show_news.html` or equivalent)
- PC collection/topic detail (`cms/show_collection.html` or equivalent) when present
- The corresponding mobile detail templates (`mobile/show_*.html`)

If the theme contains additional `show_*` or `*detail*` templates, include them too.

## Sidebar Composition Rule

PC right sidebars must not be only攻略/资讯排行. They should include a mixed set of real data modules appropriate to the current detail type:

- Software/app detail: hot apps/downloads + game recommendations/ranking + guide/news ranking.
- Game detail: game ranking + hot apps/software + guide/news ranking.
- News/article detail: hot news/guide ranking + game recommendations + hot apps/software.
- Collection/topic detail: related collection/topic content when available + game recommendations + hot apps/software + guide/news.

Use different visual patterns when practical (e.g. compact app/game cards + ranking list + text/news list) so the sidebar is not a monotonous stack of identical攻略 lists.

## Bottom Composition Rule

Bottom modules should also keep a mixed ecosystem:

- same-category resources/articles
- app/software recommendations
- game recommendations/rankings
- more news/guides
- guesses/recommendations appropriate to the detail type

Mobile may render these as stacked single-column modules, but it still needs mixed app/game/news/guide content.

## Data and Route Boundary

Use real existing data through current template helpers such as `getAllData()`, with existing filters (`a.is_hide=0`, `a.status=1`, `a.delete_time=0`) where appropriate.

Do not:

- create routes
- patch PHP/controllers/models/config
- use fake SVG/data placeholders
- hardcode nonexistent links
- assume a template file route exists if the database has no route

## Validation Requirements

Validation must prove both scope and composition:

1. Static enumerate all `show_*` / detail templates on PC and mobile.
2. For every active detail template type, find an existing representative PC and mobile URL. If one cannot be found, report the lookup method and limitation; do not create a route.
3. Check HTTP 200 and no ThinkPHP/template/PHP errors.
4. Source/DOM check that PC right sidebar includes at least two categories among app/software, game, news/guide, and preferably all three.
5. Source/DOM check that mobile detail pages include mixed recommendation modules, not only guide/news.
6. Run static hard gates: no mobile `target="_blank"`, no `cms/page/index/id`, no `data:image/svg`, no duplicate host, balanced `foreach/if` tags.
7. Capture screenshots and run AI visual review for representative software/game/news/collection detail pages on PC and mobile.
8. AI review must explicitly answer whether the PC right sidebar is still单一/only攻略 and whether game/app modules are visible.

## Known Good Validation Example

A successful validation covered 8 templates:

- PC: `show_soft_detail.html`, `show_game_detail.html`, `show_news.html`, `show_collection.html`
- Mobile: `show_soft_detail.html`, `show_game_detail.html`, `show_news.html`, `show_collection.html`

Representative existing URLs included:

- Software: `/azos07/1553.html`
- Game: `/gzos10/1564.html`
- News: `/zoszx03/6578.html`
- Collection/topic: `/yyalzos001/6065.html`

All PC sidebars showed `soft_app`, `game`, `news`, and `guide` categories, and mobile pages showed mixed modules as well.
