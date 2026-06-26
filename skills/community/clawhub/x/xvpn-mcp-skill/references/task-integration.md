# Task integration — VPN as task infrastructure

X-VPN MCP isn't a feature you offer the user. It's a tool you reach
for when geography is blocking the task they actually want done.

## Two ways VPN enters your plan

### Reactive — your task already failed

The most common entry point. You tried to do the actual task — fetch
a page, hit an API, read a regional report — and the failure looks
geo-related.

**Strong signals (act on these):**
- HTTP 403, 451, or 429 from a content endpoint
- Response body containing phrases like:
  - "not available in your region / country / location"
  - "this content is geo-restricted"
  - "please access from <country>"
- A page rendered, but visibly truncated or generic compared to what
  the user described
- A service returning a region-defaulted version (a streaming catalog
  clearly missing the show the user named, a search API returning
  local-default results)

**Weak signals (don't act on alone):**
- Slow response (could be many things)
- A 4xx whose body is actually about authentication. Read the body —
  geo-blocks talk about region; auth failures talk about login.

When the signal is strong, follow Pattern A in `call-patterns.md`:
identify the right region, connect, retry the original request,
disconnect (or restore the prior egress), continue your task.

### Anticipatory — the task is intrinsically geographic

Less frequent but cleaner. You read the user's request and notice
geographic dependency baked in:

- "What's currently trending on US Reddit?"
- "Run a Lighthouse audit on our JP site"
- "Compare our Germany pricing page to our France one"
- "Pull the top 10 search results for X as Singapore would see them"

Connect first, do the task, restore the prior egress. You're not
reacting to a failure; you're routing the task correctly from the
start. Pattern B in `call-patterns.md`.

## Disambiguating geo from other failures

Before you reach for the VPN, rule out the other things that look
like it. Connecting unnecessarily costs the user latency and free-tier
quota, and can silently change what they see.

| Looks like geo, but probably isn't if… | What it is instead |
|---|---|
| 401 / 403 with login redirect or body talking about credentials, missing API keys, expired tokens | Auth failure. VPN won't help. |
| 429 with `Retry-After` and no region language in the body | Rate limit. Wait, then retry. |
| Connection refused, DNS error, TLS handshake fail | Network path issue. VPN may help, but more often it won't. |
| Content differs by language, account, or A/B bucket | Not geographic. Switching country won't help. |

If you're uncertain, surface the failure to the user with your best
hypothesis and ask before connecting. A wrong VPN switch can put the
user's other apps on a slower egress for nothing.

## Picking the right region

Use the smallest specificity the task implies. Cities are narrower
than states; states narrower than countries. More specific tends to
mean fewer servers and higher latency variance, so don't over-specify.

| What's in the task | Pass to `connect` |
|---|---|
| "the US", "American site" | `united-states` |
| "Tokyo", "from Tokyo's perspective" | `japan/tokyo` |
| "Asia" (no country) | Pick a representative country (`singapore`, `japan`) and tell the user which you picked |
| "Europe" (no country) | Same — pick one and explain |
| Nothing specific, but you need *some* egress | `the-fastest-server` (premium) or `free` (free tier) |

If a city or state lookup fails, fall back up the hierarchy: city →
state → country.

## Keep VPN use proportional to the task

A few habits keep tunnel use minimal:

1. **Don't preemptively switch when there's no signal.** If the user
   asks "fetch this URL" and the URL is a global service, don't
   speculatively connect. Try first; switch only if the response
   shows a geo issue.
2. **Don't keep the tunnel open beyond the geo-sensitive step.**
   Connect right before the call that needs it; disconnect right
   after. Leaving it open while you do unrelated work routes that
   work through the VPN too — slower, possibly geo-defaulted, and
   eating quota if the user is free-tier.
3. **Don't change region mid-task without telling the user.** If
   your reply depends on what you saw from a particular country,
   mention the region you used. Silent geographic switches are
   confusing when the user later asks "wait, why does that look
   different from what I see?"

## Restoring the prior egress

If `xvpn_get_overview` at task start showed a connection already in
place, note that location before you change it. When you're done,
reconnect to it instead of just disconnecting. The user was relying
on that egress for other things; silently leaving them on a different
egress (or no VPN at all) is worse than an extra reconnect.

If they had no connection at start, `xvpn_disconnect` is the cleanup.

## Mental model

VPN is a setting on a request, not a state of the world. Treat it
the same way you'd treat an HTTP header: set it before the call you
need it for, clear it (or restore it) after.
