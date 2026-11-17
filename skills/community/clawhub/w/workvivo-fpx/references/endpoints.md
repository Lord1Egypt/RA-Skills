# Workvivo read endpoints — live-verified

All paths are relative to `https://$WORKVIVO_HOST/api/` and are called with
`wv_get` / `wv_search` from `scripts/wv.sh` (which adds `X-CSRF-Token` +
`X-Requested-With`). Verified 2026-11-03 against a live tenant. Every recipe selects
named fields — do not dump raw responses (see SKILL.md, "Never dump raw").

Paging comes in two shapes:

- **Laravel pages** — `?page=N`; the response carries `next_page_url` (`null` on the
  last page). Most lists return 5–25 items a page.
- **Cursor** (the feeds) — the response carries `next_cursor`; pass it back as
  `?next_cursor=<value>`.

## You

```sh
wv_get user | jq '{id, full_name, email, job_title, department_name, location_name, cost_centre_name}'
wv_get notifications/unread                   # {"notifications":N,"pulse":N,"chat":N}
wv_get 'notifications?page=1' | jq '{next: .next_page_url, items: [.data[] | {id, read: (.read_at != null), at: .created_at, kind: (.type | sub("^App\\\\Notifications\\\\"; "")), title: .data.title, item: .data.type, item_id: .data.id}]}'
wv_get people/my/team | jq '[.[] | {id, full_name, job_title, email}]'
```

`user` is ~80 KB and carries realtime/analytics tokens and org settings — never print it whole.

## Feeds

```sh
FEED='{next_cursor, items: [.data[] | {id: .item_id, type: .item_type, at: .created_at, by: (.item.creator // .item.user // .item.giver).full_name, title: .item.title, text: ((.item.short_text // .item.text // "")[0:300]), comments: .item.comments_count, likes: .item.likes_count, spaces: [.spaces[]?.name], url: .item.relative_permalink}]}'
wv_get activity | jq "$FEED"                                  # your home feed (5 per page)
wv_get "activity?next_cursor=$CURSOR" | jq "$FEED"           # next page
wv_get spaces/30/feed | jq "$FEED"                         # one space's feed
wv_get 'people/1001234567/feed?page=1&removenoise=true' | jq "$FEED + {next: .next_page_url}"   # a person's posts (?page=N, not a cursor)
```

`item_type` values seen: `update` (a post), `article`, `event`, `kudos` (shoutout),
`question-post`. The `url` is the in-app path (`comments/update/5001`,
`news/112431`, `events/66030`, `spaces/<id>/questions/<id>`). Times are UTC.

## News (articles)

```sh
wv_get 'articles?page=1' | jq '{next: .next_page_url, items: [.data[] | {id, title, subtitle, published_at, by: .creator.full_name, comments: .comments_count, spaces: [.spaces[]?.name]}]}'
wv_get articles/featured | jq '[.[] | {id, title, subtitle, published_at}]'
wv_get 'spaces/30/news?page=1&type=published' | jq '{next: .next_page_url, items: [.data[] | {id, title, published_at}]}'   # ~1 MB raw: always project
wv_get articles/7002 | jq '{id, title, subtitle, published_at, by: .creator.full_name, spaces: [.spaces[]?.name], url: .permalink, html: .html_content}'
wv_get articles/read-more/7002 | jq '[.[] | {id, title}]'   # related articles
```

The article body is `html_content` (HTML); strip it before reading
(`| jq -r .html | sed -e 's/<[^>]*>//g'` is rough but fine for a skim).

## Posts, shoutouts, comments

```sh
wv_get updates/5001 | jq '{id, at: .created_at, by: (.creator // .user).full_name, text, comments: .comments_count, likes: .likes_count}'
wv_get 'kudos?page=1' | jq '{next: .next_page_url, items: [.data[] | {id, at: .created_at, by: .giver.full_name, to: [.user_mentions[]?.user.full_name], text: (.text[0:200])}]}'
wv_get kudos/6001 | jq '{id, at: .created_at, by: .giver.full_name, to: [.user_mentions[]?.user.full_name], text}'
wv_get comments/article/7001 | jq '[.[] | {id, parent: .parent_comment_id, user_id, at: .created_at, text, likes: .likes_count}]'
wv_get likedby/update/5001                                   # {"default":[names…]}
```

## Q&A (question posts)

```sh
wv_get question-posts/4001 | jq '{id, title, by: .user.full_name, at: .created_at, answered, answers_count, text: (.body | gsub("<[^>]*>"; ""))}'
wv_get 'question-posts/4001/answers?page=1' | jq '{next: .next_page_url, answers: [.data[] | {id, by: .user.full_name, accepted, votes, text: (.body | gsub("<[^>]*>"; ""))}]}'
```

The GETs don't count a view (the app does that with a separate POST). Question posts
have answers, not comments — `comments/question-post/<id>` is a 404.

`comments/<type>/<id>` takes `update`, `article`, `event`, `kudos`, … (the type from
the item's `url`). Comments carry `user_id` only — resolve a name with
`wv_get people/<user_id> | jq .full_name`.

## Events

```sh
wv_get events/upcoming | jq '[.[] | {id, title, starts: .scheduled_at, ends: .ends_at, location, all_day: .all_day_event, going: .going_count}]'
wv_get events/listings | jq '{next: .next_page_url, items: [.data[] | {id, title, starts: .scheduled_at_utc, ends: .ends_at_utc, location, going: .is_going, spaces: [.spaces[]?.name], url: .permalink}]}'
wv_get 'spaces/30/events?page=1' | jq '{next: .next_page_url, items: [.data[] | {id, title, starts: .scheduled_at, location}]}'
wv_get events/show/8001 | jq '{id, title, starts: .scheduled_at, ends: .ends_at, location, all_day: .all_day_event, going: .going_count, by: .user.full_name, text}'
```

`scheduled_at`/`ends_at` are UTC without a zone suffix. `events/<id>` (no `show/`)
answers 500 — use `events/show/<id>`. Event records include `zoom_webinar_password`:
never print an event unprojected.

## People

```sh
wv_get 'people?query=smith&page=1' | jq '{total: .all, next: .next_page_url, people: [.data[] | {id, full_name, job_title, department_name, location_name, email}]}'
wv_get people/1001234567 | jq '{id, full_name, job_title, department_name, location_name, email, hire: .formatted_hire_date, manager: .manager.full_name, manager_id: .manager.id, bio: .profile.short_bio, expertise: .profile.expertise}'
wv_get 'people/1001234567/followers?page=1' | jq '[.data[] | {id, full_name}]'
wv_get terms/departments | jq '[.[] | {id, name}]'
wv_get terms/locations | jq '[.[] | {id, name}]'
wv_get 'terms/200/people?page=1' | jq '[.data[] | {id, full_name, job_title}]'   # people in a department/location
```

`people/<id>` also carries phone numbers and birthday — project them out unless asked.

## Spaces

```sh
SP='{next: .next_page_url, spaces: [.data[] | {id, name, members: .members_count, member: .is_member, official: .is_official, private, url: .relative_permalink}]}'
wv_get 'spaces?page=1&type=my&pageSize=50' | jq "$SP"         # spaces you belong to
wv_get 'spaces?page=1' | jq "$SP"                             # all visible spaces
wv_get 'spaces?page=1&type=search&query=office' | jq "$SP"    # search spaces by name (type=search — `all` ignores query)
wv_get spaces/trending | jq '[.[] | {id, name, members: .members_count}]'
wv_get 'spaces/30?info=1' | jq '{id, name, description, members: .members_count, member: .is_member, private, official: .is_official}'
wv_get spaces/30/links | jq '{title, body}'                # the space's useful-links widget
```

`spaces/<id>/members` is refused (`403 This action is unauthorized.`) unless you own
the space.

## Pages (a space's wiki-style content)

Pages are addressed by **slug** (the last URL segment: `spaces/30/pages/<slug>`), not by
id. Global "page collections" use `pages/<group>/<slug>`.

```sh
# The page tree: id, slug, title, nested
wv_get 'spaces/30/pages-v2?include_content=false' | jq -r 'def t(d): .[] | ("  " * d) + "\(.id) \(.slug)  \(.title)", ((.children // []) | t(d+1)); .pages | t(0)'

# One page's content. TinyMCE pages are HTML; Lexical pages are JSON blocks whose text is already Markdown
wv_get 'spaces/30/pages/<slug>?include_content=true' | jq -r '.page | if .editor_type == "lexical"
  then (.json_content | fromjson | [.. | objects | .content?.text? // empty] | join("\n\n"))
  else .html_content end'

# Global page collection
wv_get 'pages-v2/248?include_content=false' | jq '.pages'
wv_get 'pages/248/<slug>?include_content=true' | jq -r '.page.html_content'
```

The HTML carries signed image URLs (`?Expires=…&Signature=…`); strip or drop them
before pasting a page anywhere. For clean Markdown, use workvivo-mcp's
`workvivo_get_page`.

## Documents (`/document/link/<id>`)

Document links redirect to a signed file host, so `fpx get` fails with "Failed to
fetch". Download them through the browser instead (this needs the profile's
`--allow-download` scope, which the setup above declares):

```sh
fpx download "https://$WORKVIVO_HOST/document/link/<id>" -p workvivo | jq '{path, bytes, mime}'
```

The file lands in the browser's download folder. Downloading the same link again
saves `… (1).pdf`. Read PDFs with any PDF-to-text tool (e.g. `pdftotext <path> -`).

## Search

```sh
wv_search 'benefits enrollment' | jq '{page: .current_page, last: .last_page, results: [.data[] | {type, id, title: (.title | gsub("</?strong>"; "")), url, updated_at, by: .details.author}]}'
WV_PAGE=2 wv_search 'benefits enrollment' article event | jq '.data[] | {type, title, url}'
wv_get 'search/smith?v2=1' | jq '{people: [.people[] | {id, full_name}], spaces: [.spaces[] | {id, name}], teams: [.teams[] | {id, name}]}'   # quick people/space/team lookup
```

Federated-search `types`: `article update event user space docs page kudos
question_post question_post_answer term goal comment livestream podcast file welcome
anniversary birthday apps` — an unknown type is a `422`. Titles carry `<strong>`
highlight tags. The quick `search/<term>?v2=1` matches names only.

## Not available / not worth it

- `events`, `documents`, `updates` (bare lists) → `500` / empty: use the endpoints above.
- `page/collections/recent` → `403` for an ordinary employee.
- Chat runs on Sendbird and is not part of `/api`.
