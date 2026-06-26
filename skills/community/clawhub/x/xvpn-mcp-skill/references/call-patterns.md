# Call patterns

How to sequence the X-VPN MCP tools. Pick the pattern that matches
your situation and run it top-to-bottom. For deciding whether a
pattern applies in the first place — recognizing a geo-block, picking
a region, distinguishing geo from auth or rate-limit failures — see
`references/task-integration.md`.

## Pattern A — Reactive: your task hit a geo-block

The most common pattern. You tried to do the user's task, hit a
403/451 or geo-restricted body, and concluded geography is the cause.
(For how to make that call confidently, see `task-integration.md`.)

```
You're in the middle of: fetching https://news.example.us/article
You got: 403 with body "not available in your region"

1. xvpn_get_overview
   → vpn_status: {connected: false}        ← note this for cleanup
2. xvpn_list_locations(search="united-states")
   → nodes include `united-states`
3. xvpn_connect(location="united-states")
   → accepted: true
4. xvpn_get_status
   → connected: true, location: "united-states"
5. (retry the original fetch — succeeds, you have the article body)
6. xvpn_disconnect
7. (continue with the user's task using the data you fetched)
```

The disconnect at step 6 is intentional. From this point on, the
user's real task no longer needs the US egress. Leaving the tunnel up
routes the rest of your work through it for no reason — slower, and
on the free tier, eats into the connection's limited budget.

## Pattern B — Anticipatory: the task is intrinsically geographic

The user's request has geography baked in (`"what's trending on US
Reddit"`, `"audit our JP site"`). You haven't seen a failure yet, but
you can tell up front you'll need that egress.

```
1. xvpn_get_overview
2. xvpn_list_locations(search="japan")    # if needed for picking the slug
3. xvpn_connect(location="japan")
4. xvpn_get_status                        # wait for connected: true
5. (do the user's geographic task)
6. xvpn_disconnect
```

If the request mentions a city or state, prefer that specificity but
be ready to fall back up the hierarchy on failure. See
`references/locations.md`.

## Pattern C — User-explicit: "connect through <geo_name>"

Less common as a top-level intent. The user directly asked to connect
through a region — usually as a setup step before another instruction.

```
User: "Connect through Germany, then fetch our pricing page."

1. xvpn_get_overview
2. xvpn_list_locations(search="germany")
3. xvpn_connect(location="germany")
4. xvpn_get_status
5. (the actual task — fetch the pricing page)
6. xvpn_disconnect
```

Treat the connect as a means to the follow-up task. If the user only
said "connect through X" with no further task, you can stop after
step 4 and ask what they want to do next.

## Pattern D — "Fastest" or unspecified

If you've decided you need *some* egress switch but the region
doesn't matter (the user wants their IP changed; you want to retry
through any different exit; the request just says "use a VPN"):

```
1. xvpn_get_overview
2. xvpn_connect(location="the-fastest-server")   # premium default
   # for free users use location="free"
3. xvpn_get_status
```

`the-fastest-server` is the documented default value. Don't invent
your own (`"auto"`, `"best"`, etc. will fail).

## Pattern E — Free-tier user

`xvpn_get_overview` will tell you. On the free tier:

- Stay inside the `free/` subtree. Discover with
  `xvpn_list_locations(search="free")`. A bare `list_locations()` on
  a free account returns non-free nodes too, and connecting to those
  returns an upgrade prompt.
- Each free connection has a limited budget for data transfer and 
  drops when it's reached. The drop is reactive — there's no 
  advance warning, and no quota field you can poll. 
  See `references/free-tier.md`.

## Pattern F — Already connected to where you need

If `xvpn_get_overview.vpn_status.location` already matches what your
task needs, do not reconnect. Just do the task. Reconnecting tears
the existing tunnel down, adds latency, and risks failing the second
handshake.

This is also the case where the user was already connected somewhere
unrelated to your task. Note that prior location, do whatever
connecting your task needs, and restore the prior connection in
cleanup. See `task-integration.md` → "Restoring the prior egress".

## End-to-end example

User: "Pull the top 5 trending topics on Twitter as Tokyo would see
them, and tell me how they differ from what I'd see normally."

Pattern B (anticipatory): "as Tokyo would see them" is geography
baked into the request.

```
1. xvpn_get_overview
   → { account_info: {plan: "premium"}, vpn_status: {connected: false} }
2. xvpn_list_locations(search="japan")
   → nodes: [japan, japan/tokyo, ...]
3. xvpn_connect(location="japan/tokyo")
   → { accepted: true, status: "connecting" }
4. xvpn_get_status
   → { vpn_status: {connected: true, location: "japan/tokyo"} }
5. (fetch x.com/explore — request egresses through Tokyo, returns JP trends)
6. xvpn_disconnect
   → { accepted: true }
7. (now back on the user's normal egress — fetch x.com/explore again
   to get *their* baseline trends)
8. (compare and reply)
```

Step 7 is the key part. The comparison half of the user's task
explicitly needs *their* normal view, so you have to disconnect
first. Leaving the tunnel up here would have given you Tokyo trends
twice.
