# Free tier

How free-tier accounts behave, and what to do at the two boundaries
the daemon enforces.

## Detection

Inspect `account_info` from `xvpn_get_overview`. Free accounts have a
plan field indicating free tier; premium / VIP accounts have unlimited
quota and broader location access.

The status response (`xvpn_get_status`) does **not** include a quota
field you can poll. Free-tier quota is per-connection, not per-day,
and the daemon communicates it reactively (see "Quota model" below).

## Quota model

Each free connection has a limited data transfer per connection. 
When you reach it, the daemon drops the connection. This shapes 
how to plan free-tier work:

- For short tasks (single fetch, single page audit), 
  just do the task; quota is unlikely to matter.
- For long-running or data-heavy work, expect the tunnel to drop
  partway through. If a drop happens before you finish, surface the
  upgrade notice and ask the user whether to continue on free
  (open a new free connection and resume from the next chunk) or
  upgrade.

## Connecting

Free users can only connect to slugs under the `free/` prefix.
Connecting elsewhere fails with:

```
Upgrade to X-VPN Premium to access 250+ locations including <location>.
```

Recovery:

1. Stop. Don't retry the same call.
2. Surface the message verbatim — it contains the location name and
   the upgrade hook the user needs.
3. Optionally, run `xvpn_list_locations(search="free")` to find a
   nearby free alternative: *"Free-tier doesn't include Germany, but
   the Netherlands is available — want to use that?"*

Note the symmetric restriction: premium / VIP accounts trying to
connect to a `free/...` slug get `location not found: <slug>`, not an
upgrade message, because free nodes aren't part of the premium pool.
If you see `location not found` on a `free/...` slug, the account
isn't free — pick a non-free slug instead.

## Picking free destinations

When `xvpn_list_locations` is called for a free user with no `search`
argument, the response includes both free and non-free top-level
countries. Only `free/...` slugs are actually connectable. Two ways
to handle this safely:

- Pass `search="free"` to scope the list to the free subtree.
- Filter the response yourself for slugs starting with `free/` before
  picking one to connect to.

The free node list mirrors X-VPN's mobile free product — a small set
of countries plus a few US cities. **Don't hardcode** the list; it
changes over time. Always discover it via
`xvpn_list_locations(search="free")` and treat that as the source of
truth for the current session.

## Upgrading mid-session

If the user wants to upgrade right now and has a login token from
`https://xvpn.io/account/settings`:

```
xvpn_login_with_token(login_token="<token>")
```

This is the only situation where calling `xvpn_login_with_token` is
appropriate. Don't call it speculatively. After a successful login,
the account becomes premium for the rest of the session and free-tier
restrictions no longer apply.
