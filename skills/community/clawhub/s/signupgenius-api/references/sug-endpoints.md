# SignUpGenius session-mode endpoints for curl

All calls assume `$ACCESS_TOKEN` and `$COOKIE_HEADER` from the login step in
`../SKILL.md`. Every call sends both:

```
-H "Authorization: Bearer $ACCESS_TOKEN" -H "Cookie: $COOKIE_HEADER"
```

Paths under `api.signupgenius.com/v3` are the exact paths `signupgenius-mcp`'s
`client.ts` builds in session mode (it appends a trailing `/` to every v3
path — included below). Legacy calls POST JSON to
`https://www.signupgenius.com/SUGboxAPI.cfm?go=<action>` with
`Content-Type: application/json`.

---

## 1. Profile

```sh
curl -s 'https://api.signupgenius.com/v3/member/profile/' \
  -H "Authorization: Bearer $ACCESS_TOKEN" -H "Cookie: $COOKIE_HEADER" | jq '.data'
```

## 2. Groups

List groups (`sort` is optional, `asc`/`desc`):

```sh
curl -s 'https://api.signupgenius.com/v3/groups/all/?sort=asc' \
  -H "Authorization: Bearer $ACCESS_TOKEN" -H "Cookie: $COOKIE_HEADER" \
  | jq -r '.data[] | "\(.groupid)\t\(.title)"'
```

List a group's members (`GROUP_ID` from above):

```sh
curl -s "https://api.signupgenius.com/v3/groups/${GROUP_ID}/members/" \
  -H "Authorization: Bearer $ACCESS_TOKEN" -H "Cookie: $COOKIE_HEADER" \
  | jq -r '.data[] | "\(.communitymemberid)\t\(.emailaddress)"'
```

Get one member's detail (address/phone — only present if they supplied it on
a sign-up):

```sh
curl -s "https://api.signupgenius.com/v3/groups/${GROUP_ID}/members/${MEMBER_ID}/details/" \
  -H "Authorization: Bearer $ACCESS_TOKEN" -H "Cookie: $COOKIE_HEADER" | jq '.data'
```

Add a member (**write** — confirm with the user first; `firstname`/`lastname`
are optional):

```sh
curl -s -X POST "https://api.signupgenius.com/v3/groups/${GROUP_ID}/members/create/" \
  -H "Authorization: Bearer $ACCESS_TOKEN" -H "Cookie: $COOKIE_HEADER" \
  -H 'Content-Type: application/json' \
  -d '{"emailaddress":"new-member@example.com","firstname":"Jane","lastname":"Doe"}' \
  | jq '.success, .message'
```

## 3. Sign-up listings

In session mode `created`/`invited`/`signedupfor` each have **one** v3 path
each (unlike key mode's separate `/active`/`/expired`/`/all` paths) — filter
on `enddate` client-side if you only want active ones:

```sh
# everything the account created (active + expired together)
curl -s 'https://api.signupgenius.com/v3/signups/created/' \
  -H "Authorization: Bearer $ACCESS_TOKEN" -H "Cookie: $COOKIE_HEADER" \
  | jq -r '.data[] | "\(.signupid)\t\(.enddate)\t\(.title)"'

# sign-ups invited to
curl -s 'https://api.signupgenius.com/v3/signups/invited/' \
  -H "Authorization: Bearer $ACCESS_TOKEN" -H "Cookie: $COOKIE_HEADER" | jq '.data'

# sign-ups personally signed up for
curl -s 'https://api.signupgenius.com/v3/signups/signedupfor/' \
  -H "Authorization: Bearer $ACCESS_TOKEN" -H "Cookie: $COOKIE_HEADER" | jq '.data'
```

Legacy dispatcher equivalent — sometimes returns fuller data than v3
(note the **upper-case** envelope):

```sh
curl -s -X POST 'https://www.signupgenius.com/SUGboxAPI.cfm?go=t.getMySignups' \
  -H "Authorization: Bearer $ACCESS_TOKEN" -H "Cookie: $COOKIE_HEADER" \
  -H 'Content-Type: application/json' -d '{}' \
  | jq -r '.DATA[] | "\(.signupid)\t\(.title)"'
```

## 4. Public sign-up lookup (no auth)

Any sign-up's public page is at
`https://www.signupgenius.com/go/<urlid>-<signupid>[-<vanity>]` — no login
needed, works even without the login step above.

**The modern page is an Angular shell, not server-rendered.** Verified
2026-08-02: it contains no `h1.SUGHeaderText`, no slot markup, and a generic
`<title>Sign Me Up</title>` under any User-Agent.

**Do not scrape it. Use `s.getSignupInfo`.** An earlier revision of this file
claimed there was "no JSON surface that returns the same data" and told you to
fall back to the Open Graph block. **That was wrong**, and it made
`get_public_signup` return a useless stub (`"title": "Sign Me Up"`, empty
description). The SPA's own metadata call is public:

```sh
curl -s -X POST -H 'Content-Type: application/json' \
  --data '{"urlid":"10C0849AAAA2EA4FD0-62393618-20262027"}' \
  'https://www.signupgenius.com/SUGboxAPI.cfm?go=s.getSignupInfo'
```

Verified live 2026-08-10 against sign-up 62393618:

- **No auth of any kind.** A cold `curl` with an empty cookie jar returns the
  same ~10 KB envelope the signed-in browser gets (10048 vs 10075 bytes — the
  delta is theme/ad noise, not sheet data).
- **No priming step.** `s.PreProcessSignup` and a prior `GET /go/<slug>` are
  both unnecessary; all three orderings (cold / after-GET / after-preprocess)
  return byte-identical `DATA`. This is ONE request, not a 3-step dance. (The
  preprocess step is still required before a *write* — see §5.)

Returns the upper-case `{MESSAGE, DATA, SUCCESS, CODE}` envelope. Useful
`DATA` keys:

| Key | Meaning |
| --- | --- |
| `title` | the real sheet name |
| `description` | rich-text HTML — strip tags before showing |
| `id`, `urlid`, `fullurl` | identity |
| `community`, `communityid` | owning group |
| `listType`, `listformat` | e.g. `Volunteering` / `Standard` |
| `contactname`, `ownerfirst`, `ownerlast`, `owneremail`, `owner` | creator |
| `datecreated`, `datemodified`, `tzshort` | timestamps + timezone |
| `useRSVP`, `showRSVP` | `1` = Yes/No/Maybe sheet, `0` = slot-based |
| `accountRequired`, `emailrequired`, `commentRequired` | participation gates |
| `hascustomfields`, `customfields[]` | questions a claim MUST answer |

**`DATA` carries no slots** — in either anonymous or authenticated mode. Slots
live on the endpoints in "Reading slots" below.

**Two `customfields` traps.** Its `fieldvalues` is an array for Select-style
fields but an empty **string** for free-text ones, and inside that array the
key casing is inconsistent — the placeholder row uses `optionname`/`optionval`
while every real choice uses `OPTIONNAME`/`OPTIONVAL`. Read both casings and
guard the non-array, or you will silently drop every option.

## 5. RSVP (write, 3-step flow)

RSVP-only (Yes/No/Maybe headcount) sheets. **Confirm with the user before
running step 3** — it's the real submit. Get `URLID` (the full slug) by
parsing the public URL as in §4.

**Step 1 — PreProcessSignup** (sets a server-side session pointer; without
this every SUGboxAPI call below 404s with "none to be processed"). Expect
**301/302**, not 200:

```sh
curl -s -o /dev/null -w '%{http_code}\n' -D - \
  -H "Authorization: Bearer $ACCESS_TOKEN" -H "Cookie: $COOKIE_HEADER" \
  -H 'Content-Type: application/x-www-form-urlencoded' -H 'Accept: text/html' \
  -X POST "https://www.signupgenius.com/index.cfm?go=s.PreProcessSignup&URLID=${URLID}" \
  --data 'ScreenWidth=2000&ScreenHeight=1200'
```

**Step 2 — getSignupInfo** (fetch `useRSVP` + `rsvpdetails.slotid`; reject if
`useRSVP != 1` or `rsvpdetails.rsvpitems` is non-empty — that's an item-based
sheet, unsupported by this flow):

```sh
curl -s -X POST 'https://www.signupgenius.com/SUGboxAPI.cfm?go=s.getSignupInfo' \
  -H "Authorization: Bearer $ACCESS_TOKEN" -H "Cookie: $COOKIE_HEADER" \
  -H 'Content-Type: application/json' \
  -d "{\"urlid\":\"${URLID}\"}" | tee /tmp/sug-signupinfo.json | jq '.DATA | {useRSVP, owner, id, title, slotid: .rsvpdetails.slotid}'
```

**Step 3 — processSignUpFormHandler** (the actual RSVP submit). `RSVPITEMS`
must always be present as `[]` — the CFML validator throws
`key [RSVPITEMS] doesn't exist` if it's omitted. `changemembermame` is
SignUpGenius's own typo — preserve it verbatim. `rsvpresponse` is a single
letter: `y`/`n`/`m`. A `n` response forces both guest counts to `0`
regardless of what you pass.

`firstname`/`lastname`/`email` are whatever name the organizer will see, but
the entry is tied to the signed-in account either way. Take them from
`/v3/member/profile` (`.data.firstname`, `.data.lastname`, `.data.email`)
unless you mean to sign up someone else, as the MCP's `signupgenius_rsvp` and
`signupgenius_claim_slot` do by default:

```sh
OWNER=$(jq -r '.DATA.owner' /tmp/sug-signupinfo.json)
LISTID=$(jq -r '.DATA.id' /tmp/sug-signupinfo.json)
TITLE=$(jq -r '.DATA.title' /tmp/sug-signupinfo.json)
SLOTID=$(jq -r '.DATA.rsvpdetails.slotid' /tmp/sug-signupinfo.json)

curl -s -X POST 'https://www.signupgenius.com/SUGboxAPI.cfm?go=s.processSignUpFormHandler' \
  -H "Authorization: Bearer $ACCESS_TOKEN" -H "Cookie: $COOKIE_HEADER" \
  -H 'Content-Type: application/json' \
  -d @- <<JSON | jq '.SUCCESS, .MESSAGE'
{
  "listid": ${LISTID},
  "owner": ${OWNER},
  "urlid": "${URLID}",
  "title": "${TITLE}",
  "siid": "",
  "rsvpid": 0,
  "imid": 0,
  "usealternatename": false,
  "changemembermame": false,
  "displayfirstname": "Jane",
  "displaylastname": "Doe",
  "firstname": "Jane",
  "lastname": "Doe",
  "email": "jane@example.com",
  "optInStatus": false,
  "savecontactinfo": false,
  "rsvpresponse": "y",
  "rsvpadult": 1,
  "rsvpchildren": 0,
  "rsvpitems": [],
  "rsvpcomments": "",
  "type": "rsvp",
  "source": "main",
  "slotid": ${SLOTID},
  "isLoggedin": true,
  "payLater": false,
  "customFields": []
}
JSON
```

## Renewing an expired session token

`POST https://api.signupgenius.com/v3/auth/refresh` trades a `refreshToken`
cookie for a fresh 30-minute access token. The JWT's TTL is exactly 30
minutes (`exp - iat == 1800`).

```sh
curl -s 'https://api.signupgenius.com/v3/auth/refresh' \
  -H 'Content-Type: application/json' \
  -d "{\"refreshToken\":\"${REFRESH_TOKEN}\",\"token\":\"${ACCESS_TOKEN}\"}" \
  | jq -r '.data.response.token'
```

Verified 2026-08-02. Notes:

- **Both fields are required.** Sending only `refreshToken` returns 400 with
  `{"details":"token should not be null or undefined"}`. `token` is the
  current access token — it may already be expired.
- The response nests under `data.response`, with **lower-case** keys:
  `{token, refreshtoken, expiresin, expires}`. `expiresin` is `1800`. The
  refresh token is rotated, so store the new one.
- The exchange does **not** invalidate the session you already hold — a
  controlled test confirmed the legacy dispatcher still accepted both the old
  and the new token afterwards.

### The two lifetimes (important)

The JWT and the ColdFusion session expire on **separate clocks**:

| | Cookie | Lifetime | Renewable by |
| --- | --- | --- | --- |
| v3 JSON API | `accessToken` | 30 min | `POST /v3/auth/refresh` |
| legacy `/SUGboxAPI.cfm` | `cfid` + `cftoken` | idle timeout | a real login, or loading a legacy page |

Renewing the JWT does **not** revive a lapsed ColdFusion session. So `/v3/*`
calls can succeed while every legacy `go=` action returns 200
`{"SUCCESS":false,"MESSAGE":["…You are no longer logged in…"]}` — with the
browser still visibly signed in. Treat that message as an expiry signal, not
an application error.

## Reading slots on ANY sign-up — no auth required

`GET https://api.signupgenius.com/v3/signups/{signupId}/slots` returns the
full slot grid for a public sign-up **with no Authorization header, no
cookies, and no Pro key**. This is the display feed the `/go/<slug>` page
renders from, and it is the correct way to read slot data — not the Pro
report endpoints below.

```sh
curl -s "https://api.signupgenius.com/v3/signups/${SIGNUP_ID}/slots" \
  | jq -r '.data.slots[] | .title as $t | .slotitems[]
           | "\($t)\t\(.date.starttime)\t\(.date.location.displaytext // "-")\ttaken=\(.quantity.taken)/\(.quantity.limit)\tleft=\(.quantity.remaining)"'
```

A sibling endpoint, `/v3/signups/{signupId}/dates`, returns the same
slotitems pivoted by date instead of by slot (each entry nests its parent
`slot` object). Both are unauthenticated.

Verified 2026-08-02 against sign-up `62393618`. Notes:

- **Sending a bogus `Authorization` header returns 500** — call it clean, the
  way `tools/public-signup.ts` calls `/go/`. Sending the *real* session token
  is accepted but changes nothing: the payload is byte-identical to the
  anonymous one.
- `participants.itemmembers` is `[]` and `viewer.signedupqty` is `0` even for
  a signed-in participant. On the verified sheet the slot carries
  `hidenames: true`, an owner display setting — so absent names are a sheet
  configuration, not a permission boundary. Whether a `hidenames: false` sheet
  populates `itemmembers` anonymously is **untested**.
- An unknown `signupId` returns 404 with `{"success":false,"message":[]}`.
- `signupid` comes from the `/go/` slug's middle segment, or from
  `s.getSignupInfo`'s `DATA.id`.

### Participant names + quantities — also no auth

`/v3/.../slots` gives you counts but not people. The names come from the
legacy dispatcher, and it too needs **no** credentials (verified 2026-08-10
from a cold `curl`):

```sh
curl -s -X POST -H 'Content-Type: application/json' \
  --data '{"listid":62393618,"slotitemid":1762735194,"offset":1,"limitTo":100,
           "search":"","orderBy":"","orderDesc":false,"memberidViewing":0}' \
  'https://www.signupgenius.com/SUGboxAPI.cfm?go=s.getSignUpParticipantsBySlotItem'
```

Each row carries `firstname`, `lastname`, `nonmembername`, `mycomment`,
`memberid`, **`myqty`** and **`itemmemberid`**.

Two things make this endpoint essential:

1. **`myqty` is how the counts reconcile.** A single entry can consume more
   than one spot (a couple signing up together renders as one name with
   `myqty: 2`). On 10/24/2026 the sheet
   reads "4 of 6 filled" across only THREE name entries. **Never compute
   filled-count from `participants.length`** — use `quantity.taken` from the
   v3 slots feed, which is already quantity-weighted. (`quantity
   .participantcount` is the distinct-people count, and is legitimately
   lower.)
2. **`itemmemberid` is the `imid`** that a release/withdraw needs (§6).

Note this returns names even though the same slot reports `hidenames: true`
on the v3 feed, so `hidenames` is a display preference on that feed, not an
access control across the API as a whole.

### `s.getSignUpFormItems` — a param problem, not an auth problem

Earlier recon recorded this action as unusable ("Invalid Request" for
`{listid}`, `{listid, siid:""}`, `{listid, siid:[]}`; an empty `DATA` for
`siid: 0`) and left open whether a session cookie would fix it. **It would
not.** Those inputs all describe an *empty selection*. Pass a real slot-item
id and it answers immediately, unauthenticated:

```sh
curl -s -X POST -H 'Content-Type: application/json' \
  --data '{"listid":62393618,"siid":["1762735186"],"hasProductImages":false}' \
  'https://www.signupgenius.com/SUGboxAPI.cfm?go=s.getSignUpFormItems'
```

`siid` accepts an array of ids, a bare number, or a numeric string. The reply
is upper-cased (`ITEM`, `SLOTITEMID`, `AVAILABLEQTY`, `STARTTIME`, `LOCATION`,
…); the wizard lower-cases these client-side before echoing them back in a
claim. This is **not** a slot-enumeration API — it describes ids you already
have. Enumerate with `/v3/signups/{id}/slots`.

Its sibling `s.getSignUpFormAttrs` is **wizard session state**, not a query:
with nothing selected it returns "Oops! Looks like there's none to be
processed or you're already done processing this sign up."

## 6. Slot claim + release (write)

Applies to slot-based sheets (`useRSVP: 0`). **Confirm with the user before
either call.**

**Claim** — `POST /SUGboxAPI.cfm?go=s.processSignUpFormHandler`, preceded by
the §5 step-1 `PreProcessSignup`. Payload shape read directly out of the live
Angular `objForm` plus `d.ProcessSignUp` in `/dist/js/signups/signup.min.js`:

```js
i = d.objForm;                            // listid, owner, urlid, title, siid[],
                                          // rsvpid, imid, usealternatename,
                                          // changemembermame, displayfirst/lastname,
                                          // firstname, lastname, email,
                                          // optInStatus, savecontactinfo
i.type   = d.isrsvp ? "rsvp" : "standard";  // slot claims are "standard"
i.source = "main";
if (!d.isrsvp) i.items = d.items;         // rows from s.getSignUpFormItems,
                                          // lower-cased, + myqty + mycomment
i.member = d.user;
i.isLoggedin = true;                      // when signed in
i.customFields = [...custom, ...cq_address, ...cq_phone];  // cq_phone rows get
                                                           // fieldtype = fieldname
i.payLater = false;
```

Differences from the RSVP payload (§5): `siid` is an **array** of slot-item
ids (RSVP sends `""`), `items` replaces `slotid`/`rsvp*`, and `type` is
`"standard"`. The `changemembermame` misspelling is load-bearing in both.
Omitting a required custom field (this sheet mandates `PhoneType` + `Phone`)
gets the submission rejected by the CFML validator.

**Release** — NOT a SUGboxAPI action. In the wizard (`d.deleteSignUp`) it is a
plain browser navigation that answers HTML:

```
GET /index.cfm?go=s.DeletePerson&id=<signupid>&imid=<itemmemberid>&mid=<memberid>
```

(anonymous sign-ups send `&token=<attrs.token>` instead of `imid`/`mid`).
Get `imid` from `itemmemberid` in `s.getSignUpParticipantsBySlotItem`.
`s.deleteItemMember` looks like the obvious candidate but is the **owner's**
path — the admin modal that removes somebody else from a slot.

Two traps on this call. It answers HTML, and a **lapsed ColdFusion session
redirects (3xx) to `go=c.Login`** rather than returning an error status — so a
"did it work?" check on the status code alone reports a failed withdrawal as a
success. Check the redirect destination, and re-read the slot to confirm the
entry is gone. And because the participants endpoint publishes every
`itemmemberid` **and** `memberid` publicly, confirm the entry belongs to the
signed-in member before sending anything; the session profile reports that id
as `id`, not `memberid`.

> **Verification status.** Every READ above was exercised live. The two writes
> in this section were reverse-engineered but deliberately **not** executed,
> to avoid claiming and withdrawing a slot on a real sheet. Treat the claim
> payload as high-confidence-but-unverified.

## Omitted — not reachable in session mode

Slot-report endpoints (`/signups/report/all|filled|available/{signupId}`)
require `SIGNUPGENIUS_USER_KEY` (Pro API key mode, `Authorization: <key>`
against `api.signupgenius.com/v2/k`, `user_key` in the query string) — a
different auth entirely from the session login this skill uses. No v3
equivalent was found during the MCP's recon (`src/tools/reports.ts`), so
there's nothing to transcribe for session mode.

These reports are also **owner-scoped**: they answer for sign-ups the key
holder created. For a sheet someone else owns, a Pro key is not a workaround —
so reports cannot serve the common participant case at all. Use the
unauthenticated pair above instead: `/v3/signups/{id}/slots` for titles,
dates, locations and taken/remaining counts, and
`s.getSignUpParticipantsBySlotItem` for who is in each slot and how many
spots each entry consumes. Between them they cover everything the reports
were being reached for except custom-question answers, which remain
owner-only.

`s.getSignUpFormItems` is a **form** call, not a display call — its `siid` is
a list of slot-item IDs, so it cannot enumerate a sheet. But it is NOT
unusable and NOT auth-gated; see the section above for the working call.
Unlike a write, it needs no `PreProcessSignup` priming.
