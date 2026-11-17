# SimplePractice Client Portal — request reference

Base: `https://<practice>.clientsecure.me/client-portal-api`

Every shape below was taken from the portal app's own published sourcemaps
(`widget-cdn.simplepractice.com/assets/*.map`, which ship full
`sourcesContent`) and then confirmed against a live signed-in portal. Nothing
here is guessed. Where a field could not be exercised on the account used for
verification, it says so.

Assumes the `sp()` helper and `$SP_API` from `SKILL.md`.

---

## 0. Two naming systems — the trap

URLs are **dashed and plural**. JSON:API `type` values are **camelCase and
plural**. They are not the same string, and one endpoint uses both:

| URL path | `.data[].type` |
|---|---|
| `/sign-in-tokens` | `signInTokens` |
| `/document-requests` | `documentRequestQuestionnaires`, `documentRequestConsentDocuments`, … |
| `/billing-items` | `invoices`, `statements`, `superbills`, `receipts`, `payments` |
| `/client-billing-overviews` | `clientBillingOverviews` |
| `/environment` (singular!) | `environments` |

So never build a `jq` filter by pluralising the path. Match on the `type`
string the response actually carries, or select positionally.

`/environment` is the one singular path in the API.

---

## 1. Auth

### 1.1 Request a magic link — `POST /sign-in-tokens`

```sh
sp -X POST "$SP_API/sign-in-tokens" \
  -H 'Content-Type: application/vnd.api+json' \
  --data '{"data":{"type":"sign-in-tokens","attributes":{"email":"you@example.com","expiresIn":"15 minutes"}}}'
```

`202 Accepted`:

```json
{"data":{"id":"…","type":"signInTokens","attributes":{"email":"you@example.com","expiresIn":"24 hours"}}}
```

- `expiresIn` in the **response** is the real lifetime (24 hours) whatever you
  request. The portal app deliberately shows the same "24 hours" wording for an
  address with no account, so that the response cannot be used to test whether
  an email is registered. A `202` is therefore not proof the address exists.
- Optional `redirect` attribute: a portal-relative path to land on after
  verifying (the app uses it for `payment-link/<id>`).
- **Errors.** `429` with title `Email request limit reached` or
  `IP request limit reached`; `422` for a malformed address. Do not retry
  either — this is the only auth path the portal has.

### 1.2 Exchange the token — `POST /sessions/token`

The emailed link is
**`https://<practice>.clientsecure.me/sign-in/token#<TOKEN>`** — `/sign-in/token`,
*not* the `sign-in/token/verify` the app's route tree implies. A second variant,
sent for the mobile app, points at the bare apex under the API namespace:
`https://clientsecure.me/client-portal-api/sign-in/token#<TOKEN>`. Either works —
take the fragment, ignore the path.

The token is the **fragment** (303–317 characters observed). A browser never
sends a fragment to the server; the app reads `location.hash` and posts it.
Fetching the link with `curl` accomplishes nothing — copy the part after `#`.

Both emails are quoted-printable, so the URL is **wrapped across lines with
trailing `=`**. Pulling it out of a raw message with a naive regex silently
truncates the token — decode the quoted-printable first.

```sh
sp -X POST "$SP_API/sessions/token" \
  -H 'Content-Type: application/vnd.api+json' \
  --data '{"data":{"type":"sessions","attributes":{"type":"token","token":"'"$TOKEN"'"}}}'
```

Success sets the `simplepractice-session` cookie (Rails/Devise) and returns
`.data.meta.status`:

| `meta.status` | meaning |
|---|---|
| `verified` | signed in; the cookie jar is now good |
| `expired` | older than 24h — request a new link |
| `merged` | the account was merged into another; sign in from the new portal |

Tokens are single-use — confirmed by replay, which answers
`401 {"title":"Authorization has already been used or expired"}`. That is a 401
on a sign-in endpoint, where you have no session yet; it means *get a new
link*, not *your session expired*.

### 1.3 PIN variant — `POST /sessions/pin`

```sh
sp -X POST "$SP_API/sessions/pin" \
  -H 'Content-Type: application/vnd.api+json' \
  --data '{"data":{"type":"sessions","attributes":{"type":"pin","email":"you@example.com","pin":"123456"}}}'
```

The PIN is exactly 6 digits (client-side regex `^\d{6}$`) and is likewise
single-use — a wrong or reused code comes back as a validation error on `pin`,
and `429` is the rate limit.

### 1.4 Session expiry

Any endpoint answers `401 {"errors":[{"title":"You have no access to this client","status":"401"}]}`
once the cookie lapses. There is no refresh token: re-run §1.1.

---

## 2. Identity — `GET /environment`

```sh
sp "$SP_API/environment?include=currentPractice,currentClient,currentClientOptions"
```

`.data` is the singleton `environments` record; the interesting part is
`.data.relationships` + `.included[]`:

| relationship | shape |
|---|---|
| `currentPractice` | one `practices` |
| `currentClient` | one `clients` — whose data every other endpoint returns |
| `currentClientOptions` | **array** of `clients` this login may switch between |
| `currentClientAccess` | one `clientAccesses` — the login itself |

```sh
sp "$SP_API/environment?include=currentPractice,currentClientOptions" | jq '{
  practice: (.included[] | select(.type=="practices") | .attributes.fullName),
  timeZone: (.included[] | select(.type=="practices") | .attributes.timeZone),
  clients: [.included[] | select(.type=="clients")
            | {id, name: ((.attributes.preferredName // .attributes.firstName) + " " + .attributes.lastName)}]
}'
```

Useful `practices` attributes (67 in all): `fullName`, `timeZone`, `currency`,
`practiceUrl`, `phoneNumber`, `isGroupPractice`, `telehealthEnabled`,
`selfSchedulingEnabled`, `isClientAllowedToCancelAppt`,
`isClientAllowedToConfirmAppt`, `clientCancellableHrs`,
`announcementsAvailable`, `featureSecureMessagingEmber`.

`isClientAllowedToCancelAppt` and `clientCancellableHrs` are the practice's
actual cancellation policy — worth reading before assuming an appointment can
be cancelled.

`clients` attributes include `firstName`, `lastName`, `preferredName`,
`nickname`, `birthDate`, `hashedId`, `status`, `billingType`,
`hasIncompleteDocument`, `hasNewAnnouncements`, `hasInvoicedAppointments`,
`permissions`, and `relationshipToCurrentClientAccess`.

**`clients[].email` is `null` on a login that acts for someone else** (a parent
portal, say). The sign-in address belongs to the *access*, not the client.

---

## 3. Appointments — `GET /appointments`

```sh
# upcoming / confirmed
sp "$SP_API/appointments?include=clinician,office,client&filter[hasPendingConfirmation]=false&page[size]=50&page[number]=1"
# requested, awaiting the practice's confirmation
sp "$SP_API/appointments?include=clinician,office,client&filter[hasPendingConfirmation]=true&page[size]=50&page[number]=1"
```

`.data[].type` is `appointments`; `.included[]` carries `clinicians`,
`offices`, `clients`.

Attributes (21 live; from `models/unauthenticated-appointment.js` +
`models/appointment.js`):

| field | notes |
|---|---|
| `startTime`, `endTime` | ISO-8601 with offset |
| `serviceDescription` | e.g. the CPT service name |
| `confirmationStatus`, `clientConfirmationStatus` | practice-side vs client-side |
| `isCancellable` | boolean — respects the practice's own policy |
| `cancelReason`, `visitReason`, `visitTherapyReasons` | |
| `videoRoomUrl` | telehealth link, when the appointment is video |
| `icalUrl`, `gcalendarUrl` | ready-made calendar links |
| `fee`, `uninvoicedFee`, `billableDescription`, `cptCodes`, `units` | |
| `channel`, `schedulingSource`, `source` | how it was booked |
| `files` | attachments |

Relationships: `clinician`, `office`, `client`, `card`, `superbill`,
`invoiceItems`, `appointmentClient`.

`offices` carry `name`, `street`, `city`, `state`, `zip`, `phone`, `isVideo`,
`geolocation` — `isVideo: true` is a telehealth "room", not an address.

Joined one-liner:

```sh
sp "$SP_API/appointments?include=clinician,office&filter[hasPendingConfirmation]=false&page[size]=50&page[number]=1" \
| jq -r '
  (.included // []) as $inc
  | .data[]
  | . as $a
  | ($inc[]? | select(.type=="clinicians" and .id==$a.relationships.clinician.data.id)) as $c
  | ($inc[]? | select(.type=="offices"    and .id==$a.relationships.office.data.id))    as $o
  | [$a.attributes.startTime,
     ($a.attributes.serviceDescription // "—"),
     "\($c.attributes.firstName) \($c.attributes.lastName)",
     (if $o.attributes.isVideo then "telehealth" else ($o.attributes.name // "—") end)
    ] | @tsv'
```

**Pagination: by number.** `page[number]` / `page[size]`, max size 50. A short
page is the last page.

---

## 4. Billing — `GET /billing-items`

One polymorphic collection, switched by `filter[thisType]`:

| `filter[thisType]` | `.data[].type` | key attributes |
|---|---|---|
| `invoice` | `invoices` | `displayName`, `displayStatus`, `invoiceDate`, `totalAmount`, `remainingAmount`, `isNewForClient` |
| `statement` | `statements` | `displayName`, `createdAt`, `isNewForClient` |
| `superbill` | `superbills` | `displayName`, `createdAt`, `totalAmount`, `isNewForClient` |
| `receipt` | `receipts` | `displayName`, `createdAt`, `isNewForClient` |
| `billable-item,payment` (+ `filter[thisTypeCondition]=unallocated`) | mixed | account history |

```sh
sp "$SP_API/billing-items?filter[thisType]=invoice&page[size]=50" \
| jq '{balance: .meta.endBalance,
       rows: [.data[] | {type, id, name: .attributes.displayName,
                         status: .attributes.displayStatus,
                         total: .attributes.totalAmount,
                         due: .attributes.remainingAmount}]}'
```

Every billing query returns `.meta.endBalance`.

Optional `filter[timeRange]` narrows by date; the portal sends it as a
`{start,end}` object, which `curl` writes as
`filter[timeRange][start]=…&filter[timeRange][end]=…`. Omit it for everything.

**Pagination: by cursor, backwards.** `page[size]=50`, then
`page[before]=<the last row's cursorId>`. The cursor is the row's `cursorId`
attribute, **not** its `id`. A short page is the last page.

```sh
sp "$SP_API/billing-items?filter[thisType]=invoice&page[size]=50" | jq -r '.data[-1].attributes.cursorId'
```

An empty `.data[]` here is a normal, correct answer — many practices invoice
entirely outside the portal. All five filters were confirmed to return `200`
with `meta.endBalance` on the account used for verification, which had no
portal billing rows.

### 4.1 Balance summary and saved cards live ON the client record

There is **no** `/client-billing-overviews` collection and **no** `/cards`
collection. Both are `include`-able relationships of `/clients/<id>`:

```sh
CLIENT_ID=$(sp "$SP_API/environment?include=currentClient" \
            | jq -r '.data.relationships.currentClient.data.id')
sp "$SP_API/clients/$CLIENT_ID?include=clientBillingOverview,cards"
```

- `clientBillingOverviews` — `balanceDue`, `unallocatedPaymentAmount`, and the
  counts `invoicesCount` / `statementsCount` / `superbillsCount` /
  `receiptsCount` / `insuranceInfoCount`. Cheaper than paging the collections
  just to see whether anything is there.
- `cards` — `brand`, `last4`, `expiry` (e.g. `"07 / 30"`), `expMonth`,
  `expYear`, `isDefault` (a **string** `"true"`/`"false"`), plus the Stripe
  identifiers `paymentMethodId` / `customStripeCardId` /
  `customStripeCustomerId`. No full card number.

> Guessing `/cards` and `/client-billing-overviews` is the natural first move,
> and both return **HTTP 200** — with `text/html` and the app shell, because
> the SPA catch-all swallows every undefined path. They read as working,
> empty endpoints. This cost a full debugging round during this build; check
> `content-type`, never status, when an endpoint returns suspiciously nothing.

---

## 5. Documents — `GET /document-requests`

Paperwork the practice has sent you to read, complete or sign.

```sh
sp "$SP_API/document-requests?page[size]=50" \
| jq -r '.data[] | [.attributes.status, .type, .attributes.documentTitle] | @tsv'
```

`.data[].type` is the *subtype*, and the attribute set varies with it:

| `type` | what it is |
|---|---|
| `documentRequestConsentDocuments` | a consent form to sign |
| `documentRequestQuestionnaires` | a questionnaire — `templateQuestions`, `userAnswers` |
| `documentRequestContactInfos` | demographics/contact form |
| `documentRequestInsuranceInfos` | insurance details |
| `documentRequestCreditCardInfos` | card on file — `cardAttributes` |
| `documentRequestStoredDocuments` | a file shared with you |
| `documentRequestNotes` | a note |
| `documentRequestGoodFaithEstimates` | a Good Faith Estimate |
| `documentRequestPostSessionSummaries` | post-session summary |

`status` ∈ `sent` · `viewed` · `reviewing` · `completed` · `locked`
(`completed`, `sent` and `viewed` seen live). Anything not `completed`/`locked`
is outstanding:

```sh
sp "$SP_API/document-requests?page[size]=50" \
| jq -r '[.data[] | select(.attributes.status | IN("completed","locked") | not)
          | .attributes.documentTitle] | "outstanding: \(length)\n" + join("\n")'
```

Common attributes: `documentTitle`, `status`, `createdAt`, `updatedAt`,
`hasDocumentPdf`.

> **`hasDocumentPdf` is a JSON string**, `"true"` or `"false"` — not a boolean,
> despite `models/document-request.js` declaring `@attr('boolean')` (Ember casts
> it client-side; the wire value is a string). Both values were seen live. So
> `select(.attributes.hasDocumentPdf)` matches every row, including the ones
> with no PDF. Always compare to the string:
>
> ```sh
> jq -r '.data[] | select(.attributes.hasDocumentPdf == "true") | .attributes.documentTitle'
> ```
>
> It is not the only one: a saved card's `isDefault` arrives as `"true"` /
> `"false"` too. The declared type in the model is not evidence of the wire
> type — check any boolean you come to depend on, with a real response. Subtype-specific: `documentType`, `documentExt`,
`documentMimeType`, `documentBody`, `templateQuestions`, `userAnswers`,
`cardAttributes`, `mixpanelType`.

Collection `.meta` carries `hasDocumentsIntro` and `welcomeText`.

Single request: `GET /document-requests/<id>`.

`hasDocumentPdf: true` means a rendered PDF exists. The portal fetches it
through the same authenticated origin; treat the URL as session-scoped.

`GET /documents` is the separate "files shared with you" list —
`documentName`, `documentExt`, `thisType`, `createdAt`.

---

## 6. Announcements — `GET /announcements`

```sh
sp "$SP_API/announcements?page[size]=50" \
| jq -r '.data[] | [(.attributes.readAt // "UNREAD"), .attributes.title] | @tsv'
```

Attributes: `title`, `message`, `fromLabel`, `createdAt`, `readAt`,
`isDeleted`. `clients[].hasNewAnnouncements` (§2) is the cheap "is there
anything new" flag.

There is a `POST /announcements/read-announcements` that marks them all read —
a write, so out of scope here; it is listed only so you recognise it.

---

## 7. Secure messaging

Messaging is **not** on this API. It lives at
`https://messaging-api.simplepractice.com` (`messagingApiUrl` in the portal's
config) with models `messagingConversation` / `messagingMessage` /
`messagingContact` / `messagingProfile` / `messagingUser`, and is gated by the
practice's `featureSecureMessagingEmber` flag.

Its request shapes were **not** captured for this skill. If you need messages,
read them in the portal, or capture the host's calls first — don't guess them.

---

## 8. Errors

| status | meaning |
|---|---|
| `400` `Application build version is missing` | you dropped `Application-Build-Version` |
| `401` `You have no access to this client` | cookie stale/absent → re-auth (§1) |
| `422` | validation — the body names the offending field |
| `429` | rate limit; on auth calls the title says email- or IP-scoped. Do not retry |

Errors are JSON:API: `.errors[] | {title, code, status}`.

---

## Appendix — where these shapes came from

The portal serves public sourcemaps with full original sources:

```sh
curl -s https://widget-cdn.simplepractice.com/assets/<chunk>.js.map | gunzip > map.json
node -e 'const m=require("./map.json");m.sources.forEach((s,i)=>{/* write m.sourcesContent[i] */})'
```

The chunk filenames are hashed per deploy — read them out of the portal HTML's
`<script src>` tags. `adapters/application.js` defines the namespace and the
required headers; `models/*.js` define every attribute; `routes/site/**` show
which filters each screen sends. When SimplePractice ships a new build, that is
the authoritative place to re-check a shape.
