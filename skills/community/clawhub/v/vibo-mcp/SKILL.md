---
name: vibo-mcp
description: Access your Vibo (vibodj.com) event music planning via MCP. Use when the user asks about their Vibo events, wedding/event timeline, song requests, playlists, or "do not play" list, or wants to add or like songs, join an event from a share link, or export songs to Spotify/Apple Music. Triggers on phrases like "what's on my Vibo timeline", "add this song to the first dance", "what songs did guests request", "join this Vibo event", or "export our playlist to Spotify". Requires vibo-mcp installed and the vibo server registered (see Setup below).
---

# vibo-mcp

MCP server for [Vibo](https://vibodj.com) — plan your event music as a host/couple: events, timeline sections, song requests, playlists, and exports, via natural language.

- **npm:** [npmjs.com/package/vibo-mcp](https://www.npmjs.com/package/vibo-mcp)
- **Source:** [github.com/chrischall/vibo-mcp](https://github.com/chrischall/vibo-mcp)

## Setup

### Option A — npx (recommended)

Add to `.mcp.json` in your project or `~/.claude/mcp.json`:

```json
{
  "mcpServers": {
    "vibo": {
      "command": "npx",
      "args": ["-y", "vibo-mcp"],
      "env": {
        "VIBO_EMAIL": "you@example.com",
        "VIBO_PASSWORD": "your_password"
      }
    }
  }
}
```

### Authentication

Pick one:

- **Email + password (recommended):** set `VIBO_EMAIL` and `VIBO_PASSWORD`. The
  server signs in server-side and manages the token (refreshing as needed).
- **Captured token (for Apple/Google/Facebook accounts):** set
  `VIBO_ACCESS_TOKEN` (and `VIBO_REFRESH_TOKEN`) with values captured from a
  signed-in `web.vibodj.com` session — no password needed.
- **Browser capture (SSO, automatic):** with the ContextMint Bridge browser extension
  (https://github.com/nullnet-app/contextmint-bridge/releases — the fetchproxy
  extension renamed, same maintainer, public source; Chrome only for now)
  installed and yourself signed into https://web.vibodj.com, run
  `vibo_capture_session` once — it grabs the token from your tab (approve the
  pair code), saves it to `~/.vibo-mcp/session.json`, and reuses it thereafter.

The server boots without credentials (so it can be installed and probed); the
config error only appears on the first tool call.

## Tools

### Reads
- `vibo_get_me` — your profile (and whether Spotify/Apple Music are connected).
- `vibo_list_events` — your upcoming (or `past:true`) events.
- `vibo_get_event` — full details for one event.
- `vibo_list_sections` — an event's timeline (Ceremony, First Dance, Dinner, …).
- `vibo_get_section_songs` — songs requested in a section, with likes/flags/comments.
- `vibo_list_section_questions` — the DJ's planning questions for a section (type, options, current answer).
- `vibo_search_songs` — find songs to add (Vibo catalog or connected Spotify).
- `vibo_list_section_song_ideas` / `vibo_list_song_ideas_songs` — browse the DJ's suggested song collections per section.
- `vibo_get_playlists` / `vibo_get_playlist_songs` — your connected-service playlists.
- `vibo_list_event_users` — the hosts and guests on an event.
- `vibo_list_notifications` / `vibo_get_notifications_count`.
- `vibo_healthcheck` — confirm connectivity + auth.

### Writes (confirmation-gated)
Each mutating tool asks the user to confirm before anything is sent. Where the
client can show a confirmation prompt, it does (unless the server sets
`MCP_CONFIRM_ELICITATION=off`, which sends every client down the token path
below). Otherwise the first call makes
**no** network call and returns `status: "confirmation-required"` with a preview
of exactly what would be sent (`preview.action` + `preview.willSend`) and a
`confirmToken`. Show that preview to the user, and only after they approve in
chat call the tool again with the **same arguments** plus `confirmToken`. A
token works once; changing any argument is refused as `DRAFT_CHANGED` (with a
fresh preview and token to re-approve), and a reused one as `TOKEN_REUSED`.
`MCP_CONFIRM_MODE` (`ask-user` default / `auto` / `refuse`) controls this flow.

- `vibo_add_song_to_section` — add a searched song to a section.
- `vibo_remove_song_from_section` — every id is checked against the section first; unknown ids are listed and nothing is sent.
- `vibo_move_song` / `vibo_reorder_songs` — reorder places `sourceSongIds` directly after `targetSongId` (omit it for the top). A host needs the section's "hosts can order songs" setting on — Vibo turns it off for sections a host creates, and only the DJ can turn it on.
- `vibo_update_song` — mark must-play / do-not-play, or set a comment (at most 90 characters; an emoji counts as 2).
- `vibo_add_song_to_section` re-reads the section after adding and errors if the song isn't actually there.
- `vibo_toggle_song_like` — like/unlike a song.
- `vibo_comment_on_song` / `vibo_comment_on_section` — leave the DJ notes.
- `vibo_delete_song_comment` / `vibo_delete_section_comment` — remove a comment you left (e.g. undo one you just posted).
- `vibo_import_playlist_to_section` — pull tracks from a connected Spotify/Apple playlist.
- `vibo_join_event` — join via a share link/hash (e.g. a `vibodj.app.link/...` URL).
- `vibo_leave_event`.
- `vibo_create_event_contact` — add a host/guest contact.
- `vibo_invite_users` / `vibo_change_user_role` / `vibo_remove_user` — manage who's on the event.
- `vibo_update_section` — edit a section's name, time, or note.
- `vibo_create_section` — add a section (name ≤ 45 characters; `visibility` host/public; optional time and note — Vibo drops a host's description) and place it with `afterSectionId` or `position`. Returns the new `_id`.
- `vibo_delete_section` — delete a section; the preview shows its name, song count and answered questions. `dontPlay`/`headline` sections need `force: true`.
- `vibo_reorder_sections` — move sections to directly after `targetSectionId` (omit for the start).
- `vibo_answer_question` — answer a planning question (text / option ids / link / image+file uploads).
- `vibo_set_profile_photo` — set your profile photo from exactly one of: a local image `path` in the upload directory (`VIBO_UPLOAD_DIR`, default `~/Downloads/vibo-mcp`; local installs only), base64 `fileData`, or a `blobKey` from `vibo_upload_slots`.
- `vibo_upload_slots` — on a hosted deployment, get signed PUT URLs for files (`curl` each one up), then pass the returned `blobKey`s to `vibo_set_profile_photo` / `vibo_answer_question` (`imageBlobKeys`/`fileBlobKeys`). Uploads cap at 25 MiB; the stored copy is deleted once Vibo accepts it.
- `vibo_capture_session` — capture your login from a signed-in browser tab (SSO accounts).
- `vibo_mark_notifications_read`.
- `vibo_export_event_to_spotify` / `vibo_export_event_to_apple_music`.

## Response shape (`view`)

**Eight of this server's 43 tools take `view: "compact" | "full"`**, and on every
one of them **`compact` is the DEFAULT**. You get the slim rung without asking.

They are exactly the eight reads whose GraphQL document asks Vibo for media:

| Tool | What compact drops |
| --- | --- |
| `vibo_search_songs` | `thumbnails { s180x180 original }` per track |
| `vibo_get_section_songs` | `thumbnails { s180x180 original }` per song |
| `vibo_list_song_ideas_songs` | `thumbnails { s180x180 original }` per song |
| `vibo_list_event_users` | `email` + `imageUrl` per person — projected to `_id`/`firstName`/`lastName`/`role` on both exits (merged and filtered); `view: "full"` for emails |
| `vibo_list_notifications` | `imageUrl` per notification |
| `vibo_get_me` | `imageUrl` |
| `vibo_get_playlists` | `images { url width height }` (cover art) per playlist |
| `vibo_get_playlist_songs` | `images { url width height }` (artwork) per track — `songUrl` survives |

That correspondence is not a coincidence to be maintained by hand: a test in
`tests/view.test.ts` counts the media selections in `src/gql.ts` and asserts
the roster of `view`-taking tools matches. Add a ninth selection and it fails.

**Compact here is media stripping, not a field projection.** `src/view.ts`
writes no field list, because this repo holds no captured Vibo payload to
derive one from honestly; instead it removes keys whose value is a picture,
which is subtractive and so cannot drop a field nobody knew about.

The one exception is `vibo_list_event_users`: its query fixes the member field
list, so compact projects each member to `_id`/`firstName`/`lastName`/`role`
and keeps other people's email addresses out of the default answer (fleet-audit
#1136). Ask for `view: "full"` only when an email is actually needed.

What compact does **not** touch is the point of these tools: `songUrl`, the
`links` block (`spotify` / `youtube` / `appleMusic`) and the `quality` verdict
all survive. A streaming link is this server's product, not decoration —
`vibo_add_song_to_section` cannot add anything without `songUrl`, and the
quality verdict is computed from how many services carry a track. A `null` link
survives too: an absent key and a null one are the same to `JSON.parse` but not
to a reader deciding whether a service was checked.

`view: "full"` returns Vibo's payload untouched, cover art included. There is
deliberately **no `raw` rung**: nothing here re-serialises or normalises the
GraphQL response, so `full` already IS the upstream payload and a third value
would silently alias one that exists.

### `view: "brief"` on the two context-group reads

`vibo_list_notifications` also takes `view: "brief"`, and `vibo_list_events`
takes `view: "full" | "brief"` (`full`, the default, is Vibo's payload as it
arrived — its document selects no media, so it has no compact rung). Brief
answers one line per item, at most 120 characters, inside the untrusted-data
envelope (`{"untrusted_content":true,"note":…,"data":[…lines]}`), because the
titles and headers are written by other people:

- events: `title — <ISO date | no date> — <your role>, <open|locked>`
- notifications: `header — <ISO date | no date> — <read|unread>`

A line starting with `-- ` is a note, not an item: `-- none` for an empty
page, `-- N of M shown` when Vibo's `totalCount` says more exist, `-- more`
when a next page exists with no total. Page with `skip`/`limit` as usual.

### The other 33 tools have no `view`

- **The 27 mutating tools** (every confirmation-gated write, plus
  `vibo_capture_session`) answer with a confirmation preview or a receipt — an id,
  a count, a status. Nothing in a receipt is decoration, and slimming one is
  how you lose the field that says what actually happened.
- **`vibo_healthcheck`** answers with a connectivity/auth diagnostic. It runs
  the same `GET_ME` document as `vibo_get_me` and still takes no rung, because
  it never returns Vibo's user object — it builds `{ok, userId, email}` here.
  A `view` on it would be a parameter that changes nothing.
- **The 5 remaining reads** (`vibo_get_event`,
  `vibo_list_sections`, `vibo_list_section_questions`,
  `vibo_list_section_song_ideas`, `vibo_get_notifications_count`) **hand back
  Vibo's GraphQL payload as it arrived**, and their documents select no media,
  so there is nothing for a rung to remove.

A `view` passed to a tool that does not declare one is dropped by zod without a
warning, so a successful call is never evidence the rung was honoured. Check
the table above rather than assuming.

## In context groups

This server joins the **family** context group (mcp-host's `_meta.mint`
hints; every tool except `vibo_healthcheck` carries one).

- **What's on:** `vibo_list_events` is the group's canonical read — your
  upcoming events, asked for with `view: "brief"`. It takes no date range
  (Vibo lists upcoming or past, not a window) and no subject: nothing here
  lists people or properties to pick between, so the group asks it for all of
  your events.
- **What's new:** `vibo_list_notifications` is canonical — song additions,
  comments and DJ updates, newest first, with read state.
  `vibo_get_notifications_count` is a non-canonical what's-new read (the
  unread total).
- **What's due:** nothing here answers it — Vibo has no due dates to list, so
  no tool claims it.
- Every other read is a `lookup` and every write a `change` (comments and
  invitations are `send`; the playlist exports and `vibo_capture_session` are
  `other`). Writes keep their confirmation gate whatever group asks.

A compound ask reaches this server through the group, e.g. "what's coming up
for the family this month — anything new from the DJ?" puts the brief event
list and the brief notification list beside the group's other members.

This member is not browser-bridged in normal use: the reads go straight to
Vibo's API with the server-side sign-in (email + password, or a captured
token), so the group never needs your browser open for it. Only
`vibo_capture_session` uses the browser (your signed-in web.vibodj.com tab and
the ContextMint Bridge extension), and only when you run it to capture or
refresh an SSO login.

## Typical flow

1. `vibo_list_events` → pick an event id.
2. `vibo_list_sections` → pick a section id.
3. `vibo_search_songs` → get a song's `songUrl`/`viboSongId`.
4. `vibo_add_song_to_section` — show the user the preview it returns, then call
   again with the `confirmToken` once they approve.
