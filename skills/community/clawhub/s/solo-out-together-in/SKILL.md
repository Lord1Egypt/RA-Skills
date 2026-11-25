---
name: solo-out-together-in
display_name: Solo out. Together in.
display_name_en: Solo out. Together in.
description: Start a "solo out" invitation on PowPop and keep finding people you could set off with. Triggers when the user says "I'm going to X, find me someone to go with", "I'm in A and want to go to B this weekend", or "keep watching for anyone heading the same way". How it works: it turns the origin and destination into one fixed-format post, then keeps searching three ways — people whose destination is near yours, people who set off near you, and people who have written about your destination. Both ends are judged "near" within 3 km; place names do not need to match exactly. Each candidate is offered one at a time, with a single question: want to ride along together? If nobody shows up, it offers to set up a nightly watch. **Requires the PowPop MCP server (https://global.powpow.online/api/mcp); never pretend to run without it.**
description_zh: 英文版：在泡泡上发起「一个人出发」的邀约，按目的地相近、出发地相近、提过该地点三条线持续找同行者；必须连接 PowPop MCP 才能使用。
description_en: Post a solo-out invitation on PowPop and keep finding people whose destination is near yours, who set off near you, or who wrote about your destination. Requires the PowPop MCP server.
category: Social & Travel
version: 1.0.1
author: durenzidu
---

# Solo out. Together in.

## How it works (explain this on the first run — don't skip it, don't oversell it)

You set off alone. You leave one invitation on PowPop: **where you're starting from, where you want to go, and when**.

That invitation gets pinned to your starting point and lands on the map, so other people can find it.

Then it's my job — I look for people heading somewhere **near** your destination, people who set off **near** your starting point, and people who have **written about** the place you're going.

When I find one, I ask you one question: **do you want to ride along together?**
Say yes and I hand you their post and profile as-is. Say no and I never bring them up again.

If nobody shows up, I re-scan for you every night, until someone does or the date has passed.

When you explain this, **do not add** lines like "you'll find someone fast" or "lots of people are waiting" — right now there is nobody. Saying that is lying.

---

## Requirement (state this in the first line of every run — never omit)

> **This only works with the PowPop MCP connected: `https://global.powpow.online/api/mcp`**
> Without it I can't post, and I can't find anyone — I can only chat, not act.

**Before doing anything, confirm MCP is live**:

1. Call `whoami` once. Success → continue.
2. Failure (not connected / not authorized / tool missing) → **stop**, repeat the line above as written, and give the config:

```json
{
  "mcpServers": {
    "powpop": {
      "type": "http",
      "url": "https://global.powpow.online/api/mcp"
    }
  }
}
```

Let **the user** put this into `~/.workbuddy/mcp.json`, or add the URL in their connector list, authorize it, and trust the server.

- You may write that config for them only after they explicitly say "add it for me", and **you must show the full diff and get agreement first**. Never touch a config file without consent.
- Apart from that MCP entry, this skill **reads and writes nothing** unrelated to the flow; the only local write is `orders.json` (section 7).

**Forbidden**: papering over a missing MCP with "let me simulate it" or "assume the post is published". Every action here lands on a real platform; simulating is lying.

Tools it depends on (if any is missing, the MCP version is wrong — stop and say so): `whoami`, `geocode_place`, `find_nearby`, `search_posts`, `get_post_detail`, `get_user_profile`, `nearby_attractions`, `prepare_post`, `publish_post`, `my_posts`.

**This skill only reads other people's public content. It never touches their account**: no following, no DMs, no comments, no friend requests, no contacting anyone on the user's behalf. Everything involving another person stops at handing over a post link and a profile link.

---

## 1. Ask four things

Ask only what's missing — **never all four at once**.

| Item | How to ask | Check |
|---|---|---|
| **Origin** (where you start) | "Where are you right now? A landmark is enough." | `geocode_place`; if `confidence < 0.8`, hard-error and hand the matched name back verbatim for the user to correct. **Never silently swap in a different place and retry.** |
| **Destination** (where you want to go) | "Where to?" | Same as above |
| **When** | "Which day, roughly what time?" | Needs a date, or a resolvable window like "this weekend" |
| **How many** | "How many people?" | Default 2 (you + one companion) |

The origin is the **core coordinate** of this whole flow — whether anyone can find you depends on it.

**Place names**: `geocode_place` is built on Amap, so local-language names geocode far better than English ones. If an English name comes back with low confidence, ask the user for the local name ("what's it called locally / in Chinese?") and retry once with that. Don't guess.

## 2. Post the invitation

**Body template (copy the structure, change only the content)**:

```
【Solo out. Together in.】Sat Nov 1, afternoon · from Shichahai · to Wukang Road · 2 people · route can be flexible
```

**The body must start with `【Solo out. Together in.】`.** This is not decoration, it's the index — route A finds posts by searching this marker. Without it, your post may as well not exist. This marker **cannot be reworded, abbreviated, or replaced** with anything like "【Companions wanted】".

**Self-check every item before `prepare_post`; rewrite if anything is missing — never submit a broken draft**:

| Check | Requirement |
|---|---|
| Marker | Body starts with `【Solo out. Together in.】` from the very first character |
| Date | A concrete date, or a resolvable window like "this weekend" |
| Origin | Contains `from X`, and X is the same place passed as `place` |
| Destination | Contains `to Y` |
| Party | Contains `N people` |
| `place` | Set to the **origin** (e.g. "Shichahai") — this becomes the post's map coordinate |

**Two steps, never merged**:

1. `prepare_post(content, place)` → get a `draft_id`, **show the draft to the user verbatim**
2. Only after explicit approval → `publish_post(draft_id)`

Drafts expire after 1 hour; re-prepare if it lapses. If the user never says "post it", it does not get posted.

After publishing, write `post_id`, origin, destination, date window and party size into `state/orders.json` (section 7).

## 3. Three ways to find people (both ends use "near", never "same")

Origin and destination **use the same ruler**: straight-line distance **≤3 km counts as near, ≤1 km counts as the same patch**. **Place names do not need to match** — Wukang Road and Anfu Road sit in the same patch, so they're near; the Bund and Wukang Road are not.

### Route A — the invitation pool (the only source that shows both ends)

```
search_posts("Solo out")
search_posts("一个人出发")     ← the Chinese edition uses a different marker; search both
```

- Parse each body: `date` / `from (.+?) ·` / `to (.+?) ·` / `(\d+) people` (for Chinese posts, use the Chinese patterns `从(.+?)出发` / `想去(.+?)·`)
- `geocode_place()` the origin and destination separately, then measure against your own origin and destination
- Keep only posts **created within 30 days** whose date hasn't passed
- Exclude yourself (compare `post_id` or `whoami`)
- ⚠️ This pool is currently empty (zero invitations platform-wide), so this route will **usually return nobody** — that's not your failure, don't force it

### Route B — origin side: who set off near me

```
find_nearby(place=my origin, radius_meters=3000, types=['posts'])
```

- The authors of these posts are **people who have set off near you**
- Keep only posts **created within 30 days**
- Look for place names in their bodies to learn where they went; if there are none, say "I don't know where they were headed, only that they started here"
- `types` must be passed explicitly, and must not include `users` (people-nearby is permanently empty on this platform — a wasted call)

### Route C — destination side: who has mentioned where I'm going (do not skip this one)

```
search_posts("my destination name")
```

- `search_posts` does an ILIKE on post bodies and **does not depend on the invitation pool**, which makes it the only live destination-side recall available today
- The authors of matching posts are people who mentioned the place: been there, want to go, or live nearby — all count
- Keep only posts **created within 30 days**
- What it proves is "this person has a connection to my destination" — **not** "this person also wants to go". Keep the wording separate; see the table

### Tiers (each end judged on distance, neither privileged)

| Tier | Condition | Source | Wording |
|---|---|---|---|
| **R1 both near** | origin ≤3 km **and** destination ≤3 km | A | "**Right by you**, and also heading to **Wukang Road**, leaving Nov 1. Ride along together?" |
| **R2 destination near** | destination ≤3 km, origin far | A | "They start from **Chaoyang**, but their destination is basically yours. Ride along together?" |
| **R3 origin near** | origin ≤3 km, destination unknown or different | B | "**Around your Shichahai**, someone posted here last week. Route's negotiable — ride along together?" |
| **R4 mentioned it** | body mentions your destination | C | "They wrote about **Wukang Road**. Not necessarily going now, but they probably know the area. Ride along together?" |

**Take them in order R1 → R2 → R3 → R4, one at a time.**

Why this order: R2 outranks R3 because the whole point is "going to the same place"; R4 comes last because "mentioned it" only proves a connection, **not that they want to go now** — so R4 wording must never become "they want to go too".

**Quota**: `geocode_place` is rate-limited. Coarse-filter on the place-name string first (shared characters or same district), and only geocode what survives — no more than 10 geocodes per run.

The same person wearing two costumes (`糖果故宫` and `糖渍故宫_user`) counts as one person; someone hit by several routes is still offered only once.

## 4. Asking (this is the product's key moment)

Every offer carries three things: **a place, one verbatim line from their post, and a concrete date**. Never just a name.

> "**@grain.bei** posted from Shichahai last month:
> "The October night wind is turning cold. Passing the convenience store I heard someone humming an old song…"
> They're probably in that area. **Want to ride along?** I'll give you their post and profile — whether to make contact is your call."

Three possible answers:

- **Yes** → go to section 5
- **Let me think** → keep it, re-offer at most once the next day
- **No** → write it into `rejected`, never mention them again

**One person per turn.** Never dump five candidates and make the user choose.

## 5. After a yes (what I can and cannot do)

**Can do** (all of it inside the user's own account):

- Hand over their `post_url` and profile link (`get_user_profile`) so the user can reach out themselves
- `nearby_attractions(destination)` to pick a nearby landmark as the meeting point, then draft the plan: what time / which gate / which route
- With the user's explicit consent, post a short status update **on the user's own account** marking the original as "companion found"

**Cannot do — say so plainly**:

- ❌ **I cannot notify them** — the platform has no push
- ❌ **I cannot DM them or comment** — the MCP has no such tools
- ❌ **I will not follow, friend, or subscribe to anyone for you** — building any relationship with a person is something you do yourself, in the app
- ❌ **I cannot edit anyone else's post**

So reaching out always ends with the user. This skill finds the person and puts the material in the user's hands; **it never forms a relationship with anyone on the user's behalf**.

## 6. Night watch (when nobody shows up)

**Whenever a round turns up nobody, you must proactively offer the scheduled task** — don't wait to be asked, and don't quietly create it.

Fixed wording:

> "Nobody yet this time. Want me to set a night watch that re-checks for you **every night at 20:00**? If something turns up I'll bring it to you the next morning. Or skip it — you can always just ask me."

- User says yes → **actually create a recurring task**. **Describing it is not enough, claiming it's set is not enough, writing the JSON and stopping is not enough.**
- User says no → don't nag. Leave the order at `status: open`.

**Task parameters (fix them explicitly; don't rely on memory or defaults)**:

| Item | Value |
|---|---|
| Frequency | Daily at 20:00 (user may pick another hour) |
| Timezone | The user's local timezone |
| Prompt must contain | origin, destination, date window, their own `post_id`, the `orders.json` path, and "call `whoami` first" |

**Prompt template** (substitute the bracketed values and paste the whole thing into the task):

```
Call whoami first; if it fails, stop. Do not continue, do not simulate.
Read [orders.json path] and take the entry with status=open and post_id=[POST_ID].
Scan all three routes:
  A: search_posts("Solo out") and search_posts("一个人出发"); parse each post's origin and destination and compare both ends.
  B: find_nearby(place=[origin], radius_meters=3000, types=['posts']); take people who set off near [origin].
  C: search_posts("[destination]"); take people whose text mentions [destination].
Both ends use <=3 km for near and <=1 km for the same patch; place names do not need to match.
Keep only candidates within 30 days, with dates not yet passed, not in rejected. Invent nothing.
If there are candidates: describe place / one verbatim line / date, one at a time, and ask "ride along together?".
If there are none: reply only "Nobody tonight." Do not re-explain at length, do not repeat how the flow works.
After 5 consecutive empty days: suggest changing the date or destination, or widening 3 km to 10 km.
If [date window] has passed with no companion: remind "Nobody came this time — want to post a new one?" and set status to expired.
```

After creating it, write the task id into `orders.json` as `watch_task_id`, so it can be found later for cancellation.

## 7. State file

Prefer `<SKILL_ROOT>/state/orders.json`; if that directory isn't writable (read-only install), fall back to `~/.workbuddy/state/powpop-depart/orders.json` and tell the user where it lives on the first write. Shape:

```json
{
  "orders": [
    {
      "post_id": "...",
      "origin": "Shichahai",
      "origin_lat": 39.9405,
      "origin_lng": 116.386,
      "destination": "Wukang Road",
      "dest_lat": 31.208,
      "dest_lng": 121.44,
      "date_window": "2026-11-01~2026-11-02",
      "party_size": 2,
      "status": "open",
      "matched": [],
      "rejected": [],
      "watch_task_id": null,
      "created_at": "2026-10-27T02:40:00+08:00"
    }
  ]
}
```

- `status`: `open` / `matched` / `expired`. The night watch only processes `open`.
- `watch_task_id`: id of the night-watch task, `null` if none; use it to cancel or rebuild.

## 8. Hard rules (violating any of these is an implementation bug)

1. **MCP must be connected first**; if it isn't, say so plainly. Never simulate.
2. **Posting is always two steps**: show the draft → user approves → only then `publish_post`.
3. **R3 may only say "posted here", never "is here now"** — the platform has no live location.
4. **Never invent a name, a post, or a date.** Every offer must come from a real response.
5. **One candidate per turn**; anyone rejected is never mentioned again.
6. **A place confidence below 0.8 is a hard failure** — hand the match back verbatim and let the user correct it; never swap words yourself.
7. **Never claim you notified them**, and never claim they "agreed".
8. **At most 3 `find_nearby` calls per run** (quota), and `types` must be passed explicitly as `['posts']`.
9. **The body must start with `【Solo out. Together in.】`** — rewrite if it doesn't; don't call `prepare_post`.
10. **When nobody is found you must proactively offer the night watch**; create it only after consent, and report back "what time daily + task id" — never just "it's set".
11. **R4 may only say "they mentioned this place", never "they want to go too"** — that would be inventing intent.
12. **Both ends are judged near by distance, not by name equality**; origin and destination use the same threshold (≤3 km). Never tighten one end and loosen the other.
13. **Never form a relationship on the user's behalf**: no `follow_user`, no DMs, no comments, no friend requests. Hand over the post and profile links; contact is always the user's own move.
14. **Only ever change the user's own content**: posts and status updates go under the user's own account, each with a draft shown and an explicit yes first.

## 9. The honest part about a cold start (say it on the first use)

There are currently 0 invitations on PowPop, and the whole site adds only a few dozen posts in 30 days. So:

- On your first post, **chances are nobody answers** — it goes straight to the night watch
- What can be offered immediately is only **R3 (people who set off near you)** and **R4 (people who mentioned your destination)**, roughly 1–10 each; R1 and R2 only become possible once real invitations exist
- This whole thing needs **everyone to post one first** before there's a pool — the first person waits a long time, the tenth person starts to have a chance of bumping into someone

Don't retain users with "you'll find someone right away". Being straight is what makes someone willing to be first.