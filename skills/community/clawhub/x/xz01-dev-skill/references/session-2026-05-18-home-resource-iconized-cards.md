# Session note: homepage resource items must be iconized

## Trigger / correction

User corrected the xz01 homepage layout after reviewing `https://www.900az.com/`:

> 所有的app(游戏/应用), 不能以无图标+标题在板块内, 横着的方式进行排版, 首页的最新资源, 推荐资源, 处理下, 以及看怎么更新xz01规范

This is a durable xz01 template rule, not a one-off visual preference.

## Class-level rule

For app/game/application resources on xz01 pages:

- Every resource item must include an icon, thumbnail, or cover image.
- The layout must be one of:
  - card / tile
  - icon grid
  - image-text list
  - ranking row with icon
- Forbidden for app/game/application resources:
  - no icon/thumbnail/cover
  - title-only horizontal rows inside a module
  - text-only resource blocks that look like article lists

Article/news/guide lists may remain text-only when they are clearly not software/game/app resource items.

## Implementation pattern from this session

Affected homepage modules:

- PC `推荐资源`
- PC `最新资源`
- Mobile `最新资源`
- Mobile `推荐资源`
- Related homepage resource modules such as `每日推荐`, `热门游戏`, `热门应用`, ranking/resource shortcut rows

Theme-only repair pattern:

1. Keep data source in ThinkPHP templates; do not modify PHP/controllers/routes.
2. Use existing resource image fields such as `cmf_get_image_url($vo.more.thumbnail)`.
3. Convert resource rows into iconized markup:
   - PC latest/recommend: icon + title + category/size + download/action
   - Mobile latest: image-text list with icon, title, description/meta, download button
   - Mobile recommend: icon grid/card items
4. Add shrink-safe CSS:
   - `min-width:0` on text containers
   - fixed icon dimensions
   - `white-space:nowrap; overflow:hidden; text-overflow:ellipsis` for long titles
   - card/list borders and spacing so the module reads as resource UI, not article text
5. Clear `/www/wwwroot/www.900az.com/runtime/` before validation.
6. Validate with PC/mobile full-page screenshots and AI visual review.

## Verification signals

A PASS requires:

- PC homepage latest/recommended resource modules contain visible icons/thumbnails.
- Mobile homepage latest/recommended resource modules contain visible icons/thumbnails.
- No app/game/application resource appears as a no-icon title-only horizontal row.
- News/guide text lists are not falsely failed when they are clearly article modules.
- DOM/static spot checks can count images in resource sections, but final acceptance still needs full-page visual QA.

## Pitfall

Do not fix only `最新资源` / `推荐资源` by name while leaving equivalent app/game/application resource rows elsewhere (rankings, sidebars, related resources, detail modules) as text-only. The rule applies by content type, not only by module title.