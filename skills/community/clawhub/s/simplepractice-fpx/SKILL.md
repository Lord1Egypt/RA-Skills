---
name: simplepractice-fpx
description: >-
  Read a SimplePractice Client Portal (`<practice>.clientsecure.me`) from a
  shell — appointments, invoices/statements/superbills/receipts, documents to
  sign, announcements, practice and clinician info — with plain `curl` against
  its JSON:API, instead of running the simplepractice-mcp server. Sign in
  headlessly with an emailed magic link, or capture the session cookie from an
  already-signed-in browser tab with `fpx`. Use when you want Client Portal
  data without the MCP, in a script, or on a machine where the MCP isn't
  installed.
---

# SimplePractice Client Portal via curl (+ optional fpx)

The Client Portal is an Ember app whose backend is a plain **JSON:API** at
`https://<practice>.clientsecure.me/client-portal-api`. It has **no bot wall**
— every endpoint below answers ordinary server-side `curl` once you hold a
session cookie. So this skill is curl-first; `fpx` appears only as an optional
one-time way to lift the cookie out of a browser you're already signed into.

There is **no password**. Sign-in is passwordless: SimplePractice emails you
either a magic link or a 6-digit PIN, and you trade that for a session cookie.
That flow carries **no captcha** (reCAPTCHA guards only the new-client request,
waitlist and contact forms), so §1 below works headlessly with nothing but
`curl` and access to your inbox.

> This is protected health information — your own therapy/medical record.
> Treat the cookie jar as a credential: it is a full-access bearer token for
> the portal. Keep it `chmod 600`, out of git, and off shared machines.

## Your practice subdomain

Every URL is scoped to one practice. Take the host from the portal link your
provider sent you and export it once:

```sh
export SP_HOST='achievebalancetherapy.clientsecure.me'   # <-- yours
export SP_API="https://$SP_HOST/client-portal-api"
export SP_JAR="$HOME/.simplepractice-cookies"

# curl creates a cookie jar world-readable (644). This one holds a live
# session for a medical record, so create it 0600 BEFORE curl ever writes it.
[ -e "$SP_JAR" ] || ( umask 077; : > "$SP_JAR" )
chmod 600 "$SP_JAR"
```

## The four headers — all of them, on every call

```sh
sp() { curl -s -b "$SP_JAR" -c "$SP_JAR" \
  -H 'Api-Version: 2026-05-25' \
  -H 'Application-Build-Version: 0.0.0' \
  -H 'Application-Platform: web' \
  -H 'Accept: application/vnd.api+json' "$@"; }
```

Omit `Application-Build-Version` and the API rejects the call with
`400 {"errors":[{"title":"Application build version is missing"}]}` — verified.
`Api-Version` is the API's own dated contract version, unrelated to any package
version; send it as-is.

## 1. Sign in with a magic link (no browser)

**a. Request the link.** One call, to your own portal address:

```sh
sp -X POST "$SP_API/sign-in-tokens" \
  -H 'Content-Type: application/vnd.api+json' \
  --data '{"data":{"type":"sign-in-tokens","attributes":{"email":"you@example.com","expiresIn":"15 minutes"}}}'
```

`202 Accepted` means it was sent. The response echoes `expiresIn: "24 hours"`
regardless of what you asked for — that is the real token lifetime, and it is
also what the API returns for an *unknown* email, deliberately, so that a 202
never reveals whether an address has an account.

**Do not retry a failed sign-in.** `429` is a real limit with two distinct
titles — `Email request limit reached` and `IP request limit reached` — and
hammering it locks you out of the only auth path there is. Wait it out.

**b. Take the token out of the emailed link.** The link looks like

```
https://<practice>.clientsecure.me/sign-in/token#<TOKEN>
```

SimplePractice also mails a mobile-app variant on the bare apex,
`https://clientsecure.me/client-portal-api/sign-in/token#<TOKEN>`. Either
works — the path is irrelevant, only the fragment matters.

The token is the **URL fragment**, after the `#` (about 300 characters).
Because it is a fragment it is never sent to the server by a browser
navigation — the app reads it in JS and posts it. So you must copy it
yourself; following the link with `curl` does nothing.

If you are pulling the link out of a raw message rather than clicking it, note
the mail is **quoted-printable**: the URL is wrapped across lines with trailing
`=`, and a naive regex will hand you a silently truncated token. Decode first.

**c. Trade it for a session cookie.**

```sh
sp -X POST "$SP_API/sessions/token" \
  -H 'Content-Type: application/vnd.api+json' \
  --data '{"data":{"type":"sessions","attributes":{"type":"token","token":"'"$TOKEN"'"}}}' \
  | jq '.data.meta.status'
```

`"verified"` means the cookie jar is now authenticated. The other statuses are
`"expired"` and `"merged"`; a `401`/`422` means the token was already used —
they are single-use.

**PIN variant.** If your portal mails a 6-digit code instead of a link, post it
to `sessions/pin` with the address it was sent to:

```sh
sp -X POST "$SP_API/sessions/pin" \
  -H 'Content-Type: application/vnd.api+json' \
  --data '{"data":{"type":"sessions","attributes":{"type":"pin","email":"you@example.com","pin":"123456"}}}'
```

## 2. Or lift the cookie from a signed-in browser tab (fpx)

Only worth it if you're already signed in and would rather not wait on an
email. Requires the **Transporter** extension and `npm i -g @fetchproxy/cli`.

```sh
fpx profile add simplepractice --domain clientsecure.me
fpx profile declare simplepractice \
  --cookie simplepractice-session --cookie client-portal-session \
  --local-storage client-portal-session --local-storage stored-email \
  --capture-header cookie@$SP_HOST
fpx get "https://$SP_HOST/" -p simplepractice >/dev/null   # prints a pair code → approve in Transporter
```

Declare **every** scope before that first pairing. Widening it afterwards
leaves fetches working on the old grant while the new capability errors
`capability "read_cookies" not granted`, and the fix is to remove the profile
and re-pair from scratch.

Then seed the jar from the browser's cookie:

```sh
SESSION=$(fpx cookies simplepractice-session -p simplepractice \
            --storage-subdomain "${SP_HOST%%.*}" | jq -r '.["simplepractice-session"]')
printf '#HttpOnly_%s\tFALSE\t/\tTRUE\t0\tsimplepractice-session\t%s\n' "$SP_HOST" "$SESSION" > "$SP_JAR"
chmod 600 "$SP_JAR"
```

`fpx` exit codes: `2` bridge unavailable, `3` bot wall, `4` upstream non-2xx.

## 3. Who am I, and which client am I looking at

```sh
sp "$SP_API/environment?include=currentPractice,currentClient,currentClientOptions" | jq '{
  practice: (.included[] | select(.type=="practices") | .attributes.fullName),
  timeZone: (.included[] | select(.type=="practices") | .attributes.timeZone),
  clients:  [.included[] | select(.type=="clients") | {id, name: (.attributes.firstName+" "+.attributes.lastName)}]
}'
```

One portal login is a **client access**, and it can cover more than one client
— a parent seeing two children, say. `currentClientOptions` is always an array;
`currentClient` is the one whose data the other endpoints return. Don't assume
there is exactly one. (On a login that acts for someone else, the client
record's own `email` is `null` — the sign-in address lives on the access, not
the client, so don't reach for `clients[].email` to find out who you are.)

`401 {"title":"You have no access to this client"}` on any endpoint below means
the cookie is stale or absent — go back to §1.

## 4. Reads

All of these are verified live. Collections are JSON:API, so records live under
`.data[]` with fields under `.attributes`; `include=` pulls related records into
a sibling `.included[]` array that you join on
`.relationships.<name>.data.id`.

```sh
# Upcoming appointments (and the requested-but-unconfirmed ones)
sp "$SP_API/appointments?include=clinician,office,client&filter[hasPendingConfirmation]=false&page[size]=50&page[number]=1"
sp "$SP_API/appointments?include=clinician,office,client&filter[hasPendingConfirmation]=true&page[size]=50&page[number]=1"

# Billing — one endpoint, switched by filter[thisType]
sp "$SP_API/billing-items?filter[thisType]=invoice&page[size]=50"
sp "$SP_API/billing-items?filter[thisType]=statement&page[size]=50"
sp "$SP_API/billing-items?filter[thisType]=superbill&page[size]=50"
sp "$SP_API/billing-items?filter[thisType]=receipt&page[size]=50"
sp "$SP_API/billing-items?filter[thisType]=billable-item,payment&filter[thisTypeCondition]=unallocated&page[size]=50"

# Documents to review or sign, and files shared with you
sp "$SP_API/document-requests?page[size]=50"
sp "$SP_API/documents?page[size]=50"

# Practice announcements
sp "$SP_API/announcements?page[size]=50"

# Balance summary and saved cards hang off the CLIENT record, not collections
# of their own — see the warning below.
CLIENT_ID=$(sp "$SP_API/environment?include=currentClient" \
            | jq -r '.data.relationships.currentClient.data.id')
sp "$SP_API/clients/$CLIENT_ID?include=clientBillingOverview,cards" \
| jq '{balance: (.included[] | select(.type=="clientBillingOverviews") | .attributes),
       cards:  [.included[] | select(.type=="cards")
                | {brand: .attributes.brand, last4: .attributes.last4,
                   expiry: .attributes.expiry, isDefault: .attributes.isDefault}]}'
```

> **A 200 is not proof an endpoint exists.** The portal is a single-page app,
> so *any* path it does not define comes back as `200 text/html` with the app
> shell (a constant ~7.5 KB) rather than a 404. `/cards` and
> `/client-billing-overviews` are the obvious guesses for the two above, and
> both answer 200 that way — they are not API paths at all. Check the
> `content-type`, not the status:
>
> ```sh
> sp -o /dev/null -w '%{http_code} %{content_type}\n' "$SP_API/whatever"
> ```
>
> Anything other than `application/vnd.api+json` means the path is wrong.

A readable next-appointment line:

```sh
sp "$SP_API/appointments?include=clinician,office&filter[hasPendingConfirmation]=false&page[size]=1&page[number]=1" \
| jq -r '.data[0] as $a
  | (.included[]? | select(.type=="clinicians")) as $c
  | "\($a.attributes.startTime)  \($a.attributes.serviceDescription // "—")  with \($c.attributes.firstName) \($c.attributes.lastName)"'
```

## Pagination — two schemes, don't mix them

- **Appointments** page by number: `page[number]=1&page[size]=50`. You're on
  the last page when a page comes back shorter than `page[size]`.
- **Billing items** page by *cursor*, backwards: `page[size]=50` and then
  `page[before]=<cursorId of the last row you saw>`. The row's `cursorId` is
  the cursor, not its `id`.

`50` is the server's max page size; asking for more does not get you more.

## Notes

- Times come back ISO-8601 with an offset. The practice's own `timeZone`
  (§3) is what its staff schedule in — use it when a date matters.
- **`permissions` on the client is a JSON string, not an object.** It parses
  to the portal features this client actually has —
  `{"messaging":…,"selfScheduling":…,"billingDocuments":…,"payments":…,"appointments":…}`.
  Read it with `.attributes.permissions | fromjson`; used raw it is a string of
  characters. `billingDocuments` is what gates the whole billing tab.
- **`hasDocumentPdf` is a string, not a boolean.** It arrives as `"true"` or
  `"false"` — both seen live — so `if (hasDocumentPdf)` and
  `jq 'select(.attributes.hasDocumentPdf)'` are BOTH true for `"false"`.
  Compare against the string: `select(.attributes.hasDocumentPdf == "true")`.
  A card's `isDefault` is the same — so do not assume a JSON boolean anywhere
  in this API without checking the value you actually get back.
- `billing-items` is polymorphic: `.data[].type` tells you which of
  invoice / statement / superbill / receipt / payment a row actually is, and
  the attribute set differs per type. `.meta.endBalance` accompanies every
  billing query.
- An empty `.data[]` is a real answer, not a failure — plenty of practices
  bill outside the portal entirely and every billing endpoint returns `200`
  with nothing in it.
- Everything here is a **read**. Cancelling an appointment, submitting a
  signed document, or paying an invoice are writes this skill deliberately
  does not cover — do those in the portal, where you can see what you're
  agreeing to.
- This project is developed and maintained by AI (Claude).
