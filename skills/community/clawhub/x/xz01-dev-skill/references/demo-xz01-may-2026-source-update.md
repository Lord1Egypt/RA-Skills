# demo_xz01 May 2026 source update learning

Context: user reported `/root/.openclaw/workspace/demo_xz01` source was updated and asked to learn differences from previous content. The analysis was read-only; do not modify `demo_xz01`.

## Compared materials

Updated archives observed around 2026-05-15:

- `www.277zy.com/public/themes/default_2GmaD.zip` compared against older `default_HrJZZ.zip`
- `www.400zyw.com/public/themes/default_6amTZ.zip` compared against older `default_KntTK.tar.gz`
- `www.988zyw.com/public/themes/default_7MikX.zip` compared against older `default_mCYYn.tar.gz`
- `www.866zyw.com/public/themes/default_L2GB4.zip` compared against current `public/themes/default`; no content delta found

## Durable learning

### Front-end dual-end search is canceled/weakened

The user explicitly confirmed the example: “其中前台双端搜索，已取消.” Treat this as a rule for future xz01-style template work:

- PC/mobile header search forms are no longer mandatory.
- Do not fail QA solely because a PC or mobile header lacks a complete `form action="...Search/index"` search submission flow.
- Search pages such as `cms/search.html` and `mobile/search.html` may still exist; their presence does not mean the front-end header must expose full search.
- Some updated templates retain only a search icon, placeholder input, hot tags, or static search entrance.

Observed examples:

- `www.277zy.com`: PC header form removed; mobile header form replaced by non-form `searchBox`/input/icon.
- `www.400zyw.com`: PC and mobile header forms removed/weakly represented.
- `www.988zyw.com`: no full header form baseline; search UI moved/reshaped.
- `www.866zyw.com`: no archive-to-current change; if a specific template still keeps search, respect that template.

### Template structure is no longer uniform

Updated templates diverge more strongly from each other:

- `www.277zy.com` removed `common_cms/common/zyxz_module/*` entirely in the new archive.
- `www.400zyw.com` and `www.988zyw.com` still have many `zyxz_module` files, but pages/partials changed substantially.
- Some templates add many mobile bottom/related partials; others reduce PC/mobile partials and inline sidebars/recommendation blocks directly in page templates.

Future dev/test work should not require a fixed `zyxz_module` inventory or a fixed set of `_side_*.html` includes.

### Page composition changes

Observed updated patterns:

- Home pages increasingly use page-local blocks and `getAllData()` calls for hot data, new data, recommendations, news, slides, videos, rankings, etc.
- List pages may replace sidebar includes with inline ranking/recommendation/news blocks.
- Game detail pages emphasize platform/download completeness: Android/iOS availability, QR scan download, screenshots/slider, related games, related news, and rankings.
- Rank pages may use `cms_appranking`, bind IDs, `$rank_channel_list`, and `$game_list` instead of plain appsoft list calls.

### Existing hard rules still apply

Do not blindly copy risky constructs from updated source:

- Mobile `target="_blank"` remains disallowed by user rule even if some updated templates contain residue.
- Large-scale `uk-cover` remains risky/disallowed in implementation even if updated archives contain many occurrences; prefer custom `object-fit: cover` approaches when building.
- Database routes remain authoritative; do not create or fix routes simply because a template file exists.

## Future checklist

When asked to learn or implement against updated `demo_xz01`:

1. Treat `/root/.openclaw/workspace/demo_xz01` as read-only.
2. Inventory updated archives and compare against older package/current directory if available.
3. Separate durable standard changes from source quirks.
4. For search: do not require full front-end PC/mobile header search unless the specific requested template/design explicitly includes it.
5. For testing: remove “missing header search” from default fail criteria; keep validation for navigation, carousel/data rendering, responsive layout, and actual routes.
6. For implementation: preserve template-specific structure rather than forcing all templates into old module/include patterns.
