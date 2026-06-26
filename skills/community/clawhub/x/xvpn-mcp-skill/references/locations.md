# Locations — naming and discovery

How to name a place and how to search for one. Read this when you're
about to call `xvpn_list_locations` or pass a `location` slug to
`xvpn_connect`.

## Slug form

Locations are slugs: lowercase, hyphen-separated, slash-nested.

```
united-states
united-states/california
united-states/california/los-angeles
japan
japan/tokyo
singapore
```

These slugs are stable. Pass them directly as the `location` argument
to `xvpn_connect`. Individual servers below the city level are not
exposed; the daemon picks one for you when you connect to a city,
state, or country node.

## Free subtree

Free-tier locations live under a `free/` prefix:

```
free                              # generic "any free server"
free/united-states                # free US root
free/united-states/california     # free US, CA
```

What's connectable depends on the account tier — both directions are
restricted:

| Account tier | `free/...` slugs | non-free slugs |
|---|---|---|
| Free | yes | no, returns upgrade prompt (see `references/free-tier.md`) |
| Premium / VIP | no, returns `location not found` | yes |

Premium users connecting to `free/...` get `location not found` rather
than an upgrade message, because they already have unrestricted access
— a free node simply isn't the right slug for them.

## What `xvpn_list_locations` returns

The response shape is minimal:

```json
{
  "nodes": [ {"location": "<slug>"}, ... ],
  "count": <int>,
  "hint": "<optional fallback message>"
}
```

Each node has only one field — `location`. Every returned node is
connectable in principle (subject to the tier rules above); you don't
need to inspect `has_children` or `depth` flags. There aren't any.

## Search vs browse

Two modes:

- **Search** (recommended): pass `search="..."`. The daemon normalizes
  input to slug form (lowercase, spaces → hyphens) and does substring
  matching on path segments. This is what you want 95% of the time.
- **Browse**: omit `search`. Returns the top-level regions only.

Search expands matches down to the city level. So `search="united-
states"` returns the country slug plus every state and city under it,
plus the free counterparts where applicable. Server-level nodes are
never returned.

## Tier-dependent visibility

Browse and search results vary by account tier — this is the
single biggest gotcha in this tool:

- **Premium / VIP** users do not see `free` nodes in any results.
- **Free** users see the full list, including non-free countries and
  cities. **Those non-free nodes are not connectable** — picking one
  returns an upgrade prompt.

When you're operating on a free account, scope the result to the free
subtree to avoid picking an unconnectable slug. Either:

- Pass `search="free"` (or `search="free/..."`) to scope from the
  start, or
- Filter the response yourself for slugs starting with `free/` before
  picking one.

A bare `xvpn_list_locations()` on a free account looks like a complete
country menu, but most of those countries will reject the connect.

## When `list_locations` returns no match

The response includes a `hint` like:

```
"No match for 'First Avenue'. Make sure you search with English names
like 'United States', 'California'. Suggest nearby city, state, or
country to the user."
```

Surface that hint verbatim to the user. It nudges them toward valid
input far better than a paraphrase will.

## Ambiguous names

When the user gives an ambiguous name (`"California"`, `"New York"`,
`"Tokyo"`), search for it directly. The daemon disambiguates
correctly, and the returned slug encodes the hierarchy
(`country/state/city` or `country/city`). You don't need to guess the
structure — let the response tell you.
