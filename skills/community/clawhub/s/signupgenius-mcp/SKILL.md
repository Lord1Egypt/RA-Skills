---
name: signupgenius-mcp
description: Read sign-up sheets, slot reports, and groups on SignUpGenius — and add members to your groups. Triggers on phrases like "check SignUpGenius", "what am I signed up for", "what slots are left for [event]", "available slots", "list my SignUpGenius groups", "add [person] to my [group] group", or any request involving SignUpGenius sign-ups, RSVPs, volunteer slots, potlucks, carpools, classroom helpers, or PTA/HOA/Scout/team sign-ups. Works against your own signed-in account; supports Pro key for full slot reports.
---

# signupgenius-mcp

MCP server for [SignUpGenius](https://www.signupgenius.com) — 14 read tools + 2 write across profile, groups, sign-ups, and reports.

- **npm:** [npmjs.com/package/signupgenius-mcp](https://www.npmjs.com/package/signupgenius-mcp)
- **Source:** [github.com/chrischall/signupgenius-mcp](https://github.com/chrischall/signupgenius-mcp)

## Setup

Three auth modes, tried in priority order — first match wins. **You only need one.**

### Mode 1 — fetchproxy fallback (zero env vars, recommended)

Install the [fetchproxy extension](https://github.com/chrischall/fetchproxy) once, sign into [signupgenius.com](https://www.signupgenius.com), and add to `.mcp.json` (project) or `~/.claude/mcp.json` (global):

```json
{
  "mcpServers": {
    "signupgenius": {
      "command": "npx",
      "args": ["-y", "signupgenius-mcp"]
    }
  }
}
```

At startup the MCP reads your `accessToken` / `cfid` / `cftoken` cookies once via the extension, then talks to SignUpGenius directly — the extension is **not** in the request hot path after that. Works with free accounts.

### Mode 2 — session login (email + password)

Add an env block with your direct-login credentials (won't work with Google/Apple/Facebook/Microsoft SSO or 2FA):

```json
{
  "mcpServers": {
    "signupgenius": {
      "command": "npx",
      "args": ["-y", "signupgenius-mcp"],
      "env": {
        "SIGNUPGENIUS_EMAIL": "you@example.com",
        "SIGNUPGENIUS_PASSWORD": "your-password"
      }
    }
  }
}
```

### Mode 3 — Pro API key (required for slot reports)

The three `signupgenius_report_*` tools that list filled / available / all participants for a given sign-up only work against the documented Pro v2 API. Get a key from **Pro Tools → API Management** in your SignUpGenius dashboard (Pro subscription required), then:

```json
"env": { "SIGNUPGENIUS_USER_KEY": "your-api-key" }
```

Modes can be combined; Pro key wins where it applies, session/fetchproxy handles everything else.

## Tools

### Profile

- **`signupgenius_get_profile`** — Your own profile (name, email, account type).

### Groups

- **`signupgenius_list_groups`** — Every group you own or belong to.
- **`signupgenius_list_group_members`** — Members of one of your groups.
- **`signupgenius_get_group_member`** — One member's full record.
- **`signupgenius_add_group_member`** *(write)* — Add a person to one of your groups.

### Sign-ups — created by you

- **`signupgenius_list_created_active`** — Sign-ups you've created that are still open.
- **`signupgenius_list_created_expired`** — Sign-ups you've created that have ended.
- **`signupgenius_list_created_all`** — Both active and expired in one call.

### Sign-ups — others'

- **`signupgenius_list_invited`** — Sign-ups you've been invited to.
- **`signupgenius_list_signedupfor`** — Sign-ups you've taken a slot on. (Session-mode also includes the bonus `signupgenius_legacy_get_my_signups` which calls the same backend the SignUpGenius web wizard uses and sometimes returns fuller data.)
- **`signupgenius_legacy_get_my_signups`** *(session only)* — Bonus richer "what am I signed up for" lookup.

### Public sign-up

- **`signupgenius_get_public_signup`** — Fetch a public sign-up page by URL or slug. No auth required.
- **`signupgenius_rsvp`** *(write)* — RSVP to a public sign-up slot.

### Reports — slots for a sign-up (Pro key only)

- **`signupgenius_report_all`** — Every slot + participant on a sign-up.
- **`signupgenius_report_filled`** — Filled slots only.
- **`signupgenius_report_available`** — Available slots only.

Session-mode users hit a fast `ModeMismatchError` on the report tools with a clear instruction to set `SIGNUPGENIUS_USER_KEY`.

## Trigger examples

- "Check SignUpGenius — what am I signed up for this week?" → `signupgenius_list_signedupfor` (+ `_legacy_get_my_signups` in session mode)
- "What slots are still open on the PTA potluck sign-up?" → `signupgenius_report_available` (Pro key)
- "List my SignUpGenius groups" → `signupgenius_list_groups`
- "Add Jordan Smith (<jordan@example.com>) to my Scouts group" → `signupgenius_add_group_member`
- "What sign-ups have I created that are still active?" → `signupgenius_list_created_active`
- "RSVP me to slot 3 on this SignUpGenius link" → `signupgenius_rsvp`

## Gotchas

- **Reports require Pro.** `signupgenius_report_*` only work with `SIGNUPGENIUS_USER_KEY` — session/fetchproxy users get a clear error pointing at the key.
- **SSO accounts not supported.** Session mode is direct email/password only — no Google/Apple/Facebook/Microsoft SSO, no 2FA. Use fetchproxy mode instead if your account uses SSO.
- **Session listings collapse.** In session mode the v3 `signups/created` endpoint returns active + expired in one paginated call — the three `list_created_*` tools all hit the same endpoint and filter client-side. Pro key mode has separate endpoints and exposes the real distinction.
- **Write surface is small.** Only `signupgenius_add_group_member` and `signupgenius_rsvp` mutate; everything else is read-only.
- **ToS caveat.** SignUpGenius's terms generally prohibit scripted/automated access. Personal-account, personal-scale use is the intended audience; running this against accounts you don't own or at scale is your problem.
