---
name: workvivo-fpx
description: Read your organization's Workvivo (Zoom Workvivo employee-experience platform, <org>.workvivo.us/.com/.io) from a shell — the home feed, company news articles, posts and shoutouts with their comments, spaces and their feeds/news/events/content pages, linked documents, upcoming events, the people directory and profiles, your team, notifications, and full-text federated search — through your signed-in Workvivo browser tab with the fpx CLI. Read-only. Use when asked about Workvivo, the company intranet feed, internal news, a Workvivo space, colleagues' profiles, or what's happening at work.
---

# Workvivo via fpx

Workvivo sits behind your company's SSO, so there is no server-side login: every
call rides your already-signed-in Workvivo tab through the **ContextMint Bridge**
extension and the `fpx` CLI (`npm i -g @fetchproxy/cli`).

## One-time setup

```sh
fpx profile add workvivo --domain workvivo.us      # the apex of YOUR host (.us / .com / .io)
fpx profile declare workvivo --cookie XSRF-TOKEN --allow-download
fpx get https://acme.workvivo.us/ -p workvivo >/dev/null   # prints a pair code on stderr
```

Approve the pair code in the ContextMint Bridge popup **of the browser where you are
signed in to Workvivo**. If a second browser also runs the extension, every call
prints a fresh pair code on stderr while stdout still carries the data — that is the
other browser being turned away; do not approve it (`fpx trust list` shows the pin,
`fpx trust clear fpx-workvivo` re-pairs).

## Call pattern

Source the helper — it reads the session CSRF token once and adds the headers
Workvivo's `/api/*` routes require (`X-CSRF-Token` from the page's
`<meta name="csrf_token">` + `X-Requested-With: XMLHttpRequest`; without them every
call is `401 {"message":"Unauthenticated."}`, GETs included):

```sh
export WORKVIVO_HOST=acme.workvivo.us
source ~/.claude/skills/workvivo-fpx/scripts/wv.sh     # or wherever this skill lives
wv_get 'activity' | jq '.data[] | {type: .item_type, by: (.item.creator // .item.user // .item.giver).full_name, title: .item.title, text: (.item.short_text // .item.text)}'
wv_search 'benefits enrollment' article event | jq '.data[] | {type, title, url}'
```

- `wv_get <path>` — GET `https://$WORKVIVO_HOST/api/<path>`.
- `wv_search <query> [type…]` — POST `federated-search` (`WV_PAGE=2` for more). It adds
  an entry to **your own** Workvivo search history; that is its only side effect.
- Return codes: `0` ok · `1` usage · `2` bridge down · `3` bot wall · `4` upstream HTTP
  error (body on stdout) · `5` not signed in to Workvivo in the paired browser.

**Resolve first.** Most detail endpoints take a numeric id: find it from a list or
search result (`url` like `news/7001`, `events/8001`, `comments/update/5001`),
then read the detail. Times are UTC (`*_utc` fields where present).

## Never dump raw

Several responses carry fields that are not yours to relay — always project with `jq`:
`user` (your own record) includes realtime/analytics tokens and org config; events
include `zoom_webinar_password`; people records include phone numbers. The recipes in
`references/endpoints.md` select named fields only.

Everything readable is in **`references/endpoints.md`** — live-verified paths, paging,
and `jq` recipes for each.
