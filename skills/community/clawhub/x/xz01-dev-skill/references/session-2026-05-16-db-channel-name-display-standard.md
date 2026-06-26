# 2026-05-16 — DB channel name is the front-end display standard

User correction about route alias `gzos`:

```sql
cmf_cms_channel.id = 6
alias = 'gzos'
name = '手游下载'
listtpl = 'list_game'
showtpl = 'show_soft_detail'
```

## Rule

For xz01 category/list pages, the database channel row is authoritative for both routing and display labels.

- The route alias such as `gzos` is only the database alias/path identifier.
- The front-end PC and mobile page display name must use the database channel `name` field.
- PC and mobile must display the same database `name` for the same channel.
- Do not treat a game route showing `手游下载` as a visual mismatch if the database `cmf_cms_channel.name` is `手游下载`.
- Do not normalize or rewrite channel names to guessed labels such as `游戏下载`, `游戏中心`, or `游戏列表` unless the user explicitly requests a template-only wording override.
- Test/AI review must validate display text against the DB channel metadata, not against inferred route semantics.

## Example

For `alias='gzos'` and `name='手游下载'`:

- PC `/gzos/` heading should display `手游下载`.
- Mobile `m.900az.com/gzos/` heading should display `手游下载`.
- This is PASS when the page renders real data, pagination is safe, and there is no HTTP/template/layout error.
