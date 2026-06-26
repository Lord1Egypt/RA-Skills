# Terms of service and etiquette

This skill calls **public, unauthenticated** JSON endpoints from Target's
public-facing web API — the
same URLs that `target.com` itself loads in your browser. There is no
private API key, no signed request, and no login flow involved for any
read operation. That said:

## Be a polite client

1. **Throttle.** The shared client enforces a minimum gap between requests
   via `TARGET_MIN_INTERVAL` (default `1.0` second). Do not lower this
   below `0.5`. For batch jobs, raise it to `2`+.
2. **Use a real User-Agent.** Default identifies the skill. Override with
   `TARGET_USER_AGENT` if you fork.
3. **No scraping at scale.** This skill is for assistant-driven, one-shot
   product lookups — not for mirroring the catalog, price monitoring, or
   building a competing product feed.
4. **Cache locally** if you call the same TCIN repeatedly in a session.
   The trim layer is cheap to re-run on cached raw JSON.
5. **Stop on 403/429.** These signal upstream/CDN protection. Back off for
   minutes, not seconds. Do not retry in a tight loop.

## What this skill does NOT do

- **No login, no auth, no checkout.** The skill never handles credentials,
  payment info, addresses, or session cookies.
- **No mutating endpoints.** Every API call is a `GET`. `cart_link.py`
  builds a URL string locally — no network.
- **No bulk catalog dumps.** The `count` cap on search is 24 (Target's
  own limit) and the skill defaults to 10.

## Target.com terms

Target's site terms apply to any automated use. If Target asks you to
stop, stop. If your IP gets blocked, that is the answer. Do not route
this skill through proxy rotation, residential IPs, or any other
evasion mechanism.
