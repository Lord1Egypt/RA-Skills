---
name: signupgenius-api
description: "Access SignUpGenius (sign-ups, groups, RSVPs) from a shell with curl instead of running the signupgenius-mcp server — server-side email/password login to a JWT + cfid/cftoken cookies, then curl the v3 API and legacy /SUGboxAPI.cfm dispatcher directly. Use when you want SignUpGenius data without the MCP, in a script, or on a machine where the MCP isn't installed."
---

# SignUpGenius via curl (no MCP)

SignUpGenius's session mode is a classic ColdFusion login: POST email+password
to the login form, get back a `accessToken` JWT cookie plus `cfid`/`cftoken`
session cookies. No browser or extension needed — everything here is a plain
`curl` call. This is the same auth path `signupgenius-mcp` uses in session
mode (`src/auth-session-login.ts`); its fetchproxy path (lifting the same
cookies out of a signed-in browser tab) is only a **fallback** for when you
don't want to put a password in `.env` — this skill always logs in directly.

## One-time setup

```sh
export SIGNUPGENIUS_EMAIL="you@example.com"
export SIGNUPGENIUS_PASSWORD="..."
# or: export SIGNUPGENIUS_PASSWORD="$(op read 'op://Private/SignUpGenius/password')"
```

SSO accounts (Google/Apple/Facebook/Microsoft) and 2FA-enabled accounts can't
use this flow — same limitation as the MCP's session mode.

## Log in: get the JWT + cookies

```sh
COOKIEJAR=$(mktemp)

CSRF=$(curl -s -c "$COOKIEJAR" https://www.signupgenius.com/login \
  | grep -oE 'name="csrfToken"[[:space:]]+value="[^"]+"' \
  | sed -E 's/.*value="([^"]+)".*/\1/')

curl -s -D /tmp/sug-login-headers.txt -o /dev/null \
  -b "$COOKIEJAR" -c "$COOKIEJAR" \
  -A 'Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36' \
  -X POST 'https://www.signupgenius.com/index.cfm?go=c.Login' \
  --data-urlencode "csrfToken=$CSRF" \
  --data-urlencode "loginemail=$SIGNUPGENIUS_EMAIL" \
  --data-urlencode "pword=$SIGNUPGENIUS_PASSWORD" \
  --data-urlencode "successpage=c.jump&jump=/index.cfm?go=c.MyAccount" \
  --data-urlencode "failpage=c.Register" \
  --data-urlencode "ScreenWidth=2000" \
  --data-urlencode "ScreenHeight=1200" \
  --data-urlencode "formaction=1" \
  --data-urlencode "formName=loginform" \
  --data-urlencode "refererUrl="

# Bad credentials 302 to c.Register instead of setting accessToken — check both:
grep -q 'c.Register' /tmp/sug-login-headers.txt && echo "LOGIN FAILED (bad credentials)" >&2

ACCESS_TOKEN=$(awk -F'\t' '$6=="accessToken"{print $7}' "$COOKIEJAR")
CFID=$(awk -F'\t' '$6=="cfid"{print $7}' "$COOKIEJAR")
CFTOKEN=$(awk -F'\t' '$6=="cftoken"{print $7}' "$COOKIEJAR")
[ -z "$ACCESS_TOKEN" ] && echo "LOGIN FAILED (no accessToken cookie set)" >&2
COOKIE_HEADER="accessToken=${ACCESS_TOKEN}; cfid=${CFID}; cftoken=${CFTOKEN}"
```

This mirrors `sessionLoginFlow` exactly: GET `/login` for the CSRF token +
`cfid`/`cftoken`, POST the credentials with the exact same static form fields
the wizard sends, and read the `accessToken` cookie back out of the jar as
the success marker.

## Core call pattern

Every authenticated call carries **both** headers — a Bearer JWT for the v3
API and the raw cookie header for the legacy dispatcher (the client sends
both on every request regardless of which surface it's hitting):

```sh
curl -s 'https://api.signupgenius.com/v3/member/profile/' \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Cookie: $COOKIE_HEADER" | jq .
```

```sh
curl -s -X POST 'https://www.signupgenius.com/SUGboxAPI.cfm?go=t.getMySignups' \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Cookie: $COOKIE_HEADER" \
  -H 'Content-Type: application/json' \
  -d '{}' | jq .
```

Ready-to-run request bodies for every tool endpoint (groups, sign-up
listings, public sign-up lookup, and the 3-step RSVP flow) are in
`references/sug-endpoints.md`. RSVPs and slot claims send a name and email,
but the entry is tied to the signed-in account whatever you send, so default
them to the `/v3/member/profile` values unless you mean to sign up someone else.

## The two envelope shapes

- v3 API (`api.signupgenius.com/v3/...`) returns **lower-case**
  `{data, message, success}`.
- The legacy dispatcher (`/SUGboxAPI.cfm?go=...`) returns **upper-case**
  `{DATA, MESSAGE, SUCCESS}` — `MESSAGE` may be a bare string instead of an
  array.

`jq` recipes in the reference file account for the case difference per
endpoint.

## Session expiry

Two signals mean the session lapsed — re-run the login step and retry:

- an HTTP `401` from either surface, or
- an HTTP `200` whose body is HTML containing `loginform`/`loginemail`/
  `go=c.Login` (the server quietly bounced you to the login page instead of
  returning JSON).

A `403` is a Pro-permission failure, not expiry — don't retry the login for
that one.

## Out of scope for this skill

- **Pro API key mode** (`SIGNUPGENIUS_USER_KEY`, `Authorization: <key>` against
  `api.signupgenius.com/v2/k`) is a different auth entirely — it's the only
  mode that can call the slot-report endpoints
  (`/signups/report/{all,filled,available}/{signupId}`), which are not
  reachable in session mode at all (no v3 equivalent exists). Not covered
  here since this skill is the email/password session path.
- **fetchproxy** (lifting these same cookies out of a signed-in browser tab)
  is the MCP's fallback for when no env credentials are set. This skill
  always logs in directly, so fetchproxy/the ContextMint Bridge extension is never
  needed.
