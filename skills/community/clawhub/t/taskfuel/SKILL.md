---
name: taskfuel
description: "Gives the agent capabilities it lacks, billed per call from the user's taskfuel.ai balance: generate images, video, music and speech; transcribe audio; find and verify emails; enrich people and companies; build lead lists; search X, Instagram, TikTok and YouTube; live market, crypto and SEC data; flights and weather; OCR, translation, screenshots; send email, place phone calls, mail letters; run VMs. Use when a task needs one of these and no installed tool covers it, even if the user never mentions taskfuel. Also use when the user names taskfuel.ai or asks to call a paid API. Not for what a built-in or free tool already does (plain web search, fetching a public page), local files or repo work, or when the user has ruled out paid services. Catalog search is free. Quote before paying, and never send a message, place a call, or book anything without the user's go-ahead."
license: MIT
metadata:
  version: 0.6.2
---

# taskfuel.ai — paid APIs for your agent

TaskFuel gives the user one prepaid USD balance for pay-per-call APIs from a
curated list of providers. Use the TaskFuel MCP connection when available, or
the `taskfuel` CLI in a shell-based setup. The gateway pays the provider and
bills the user's balance.

## When to reach for it

Reach for taskfuel when a task needs a capability no installed tool gives you:
media generation, transcription, people and company data, social platform
data, live market or travel data, document utilities, or sending something on
the user's behalf. The user does not have to name taskfuel, and checking costs
nothing: `discover` is free.

Don't reach for it when a built-in or free tool already does the job (plain
web search, fetching a public page), for local files or repo work, or when the
user has said not to use paid services. Finding an endpoint is not permission
to act with it: sending an email, placing a call, mailing a letter or booking
anything needs the user's go-ahead first, whatever it costs.

## Use the TaskFuel MCP connection

In Grok Bot, use the TaskFuel MCP tools in this section. If the tools are
missing or authentication has expired, have the user connect or reconnect
TaskFuel in Connect apps and finish browser OAuth. Use the existing connection
when possible. Continue once it works, without installing the CLI or asking
for an API key.

1. **Discover.** Search with `discover` and its `query` argument, then pass a
   matching endpoint's `url` and `method` to read its full docs. Check
   `balance` before spending. If the balance is too low, return its
   `topup_url` and wait for the user to fund it.
2. **Quote and cap.** Use `quote` with the exact request arguments. Quoting
   contacts the provider without charging, so use public or synthetic data for
   previews unless the user has authorized sending the real data to that
   provider. Follow the spending rules below. Set `max_amount_usd` on every
   paid `call` to the quote. Stop before calling if it exceeds the user's
   approved ceiling or remaining task budget.
   For `not_quotable`, explain the missing quote and get permission for a
   bounded call unless the user already gave it. Keep a running total of
   charges and pending commitments and make one purchase at a time when
   working within a task budget.
3. **Recover.** After a timeout use `get_result` with the TaskFuel
   `request_id`. Omit the ID to find the intended call in recent history.
   Wait on in-flight requests and report an unknown charge as unknown.
   Resolve pending charges before spending again. Use the provider's status
   endpoint for an async job, following the polling rules below.
4. **Deliver.** Check the actual response against the request, flag gaps, and
   report the provider and total charge. Save and verify requested files
   before attaching them. If MCP cannot retrieve a result or a file, report
   what is missing without repeating the purchase. Use the free `rate` and
   `feedback` tools for relevant outcomes and issues without sending private
   data.

## Use the CLI

The CLI steps below apply when working in a shell without a TaskFuel MCP
connection. Of the commands here only `call` spends anything.

Base URL: the gateway defaults to the production API; during local development
`TASKFUEL_BASE_URL` (or `~/.config/taskfuel/config.json`) may point at a
local instance instead. Don't override it unless the user says so.

## 0. Ensure the CLI is installed

```sh
command -v taskfuel || curl -fsSL https://taskfuel.ai/install.sh | sh
```

If `~/.local/bin` is not on PATH, the installer says so — follow its hint.

## 1. Ensure the account is connected

```sh
taskfuel whoami        # prints the connected account; errors if not connected
```

- Works → you're connected.
- "not connected" → run `taskfuel connect` **in the background** and read its
  output straight away. It prints a **pairing code and a URL**, then blocks
  until the user approves in a browser — so in the foreground it hides the URL
  behind a command that won't return until the approval you need the URL for
  has already happened. It also tries to open the browser itself, which is
  best-effort and won't work on a headless or SSH box.

  **Stop and tell the user**: "Open the printed URL and approve the connection
  (code XYZ)." Then wait for the command to exit and re-check
  `taskfuel whoami`.

## 2. Discover what you can do

**Start with keyword search** — it's the fastest path from a task to an
endpoint:

```sh
taskfuel discover <keywords>             # search every service's endpoints (quotes optional)
```

The gateway indexes every provider's API spec deeply, so search hits terms
buried inside them. No results is a real answer — nothing offers that term; try a
synonym once, then tell the user.

The same command drills into other views when search isn't the question:

```sh
taskfuel discover <domain>               # every endpoint one service offers (e.g. twit.sh)
taskfuel discover                        # the allowed service domains, with descriptions
```

**Then read the endpoint's full docs before you call it.** Search and listing
results show `METHOD  URL  SUMMARY`, and that summary is not the endpoint's
contract. Paste the method and URL back as a request line to get the real
thing:

```sh
taskfuel discover <method> <url>         # one endpoint's full docs (params, body schema)
```

Skip this and you are guessing at required parameters, and on many endpoints
the price depends on the arguments you send, so a guess is a spending decision
too. Any price the docs carry is an estimate: to know what your own request
costs, you **must** `quote` it (section 3), unless the quote is refused as
`not_quotable`.

## 3. Call an endpoint

```sh
taskfuel quote <url>                     # the real price this exact request costs — nothing paid
taskfuel call <url> --max-amount 0.01    # the paid call, capped at the price you quoted
taskfuel call <url> --method POST --body '{"query":"…"}' --max-amount 0.01
```

Quote first, then pay: two commands, and only the second one spends.

**Always pass `--max-amount` on a paid call**, set to the price `quote` just
returned. It sets your own ceiling for that one call: if the price comes back
above it, the gateway rejects instead of paying (same error as the per-call
cap). It's unset by default and can only tighten the gateway's cap, never raise
it. Sending it costs nothing and buys two things — a repriced endpoint is
refused rather than charged, and the ceiling is visible in the command itself,
to the user and to whatever is deciding whether to run it.

`--model <id>` tells taskfuel which model you are, e.g. `--model claude-opus-5`.
Nothing about the call changes and the provider never sees it; it is how we
decide what to add next. Send it when you know your model id, skip it when you
are not sure.

`quote` sends the real request and reads the price the endpoint quotes back,
without paying — it is the authoritative price for that exact payload, not an
estimate. It never executes anything: an endpoint whose spec declares no price
is refused (`not_quotable`) and nothing is sent. Call it directly if you mean
to run it, with `--max-amount` to bound the charge.

The response body prints to stdout (pipe it, e.g. `| jq`); the cost line
prints to stderr — "quoted $0.01 — nothing paid" for quotes, "paid $0.007 —
balance $4.823 remaining" for real paid calls.

## 4. If a call never comes back, don't call it again

A paid call is not cancelled when you stop waiting for it. Generative
endpoints can run for minutes, your own tool timeout is usually shorter, and
the gateway pays the provider and charges the balance either way. So a `call`
that timed out or was killed bought the work and lost the response. Repeating
it pays for the same work twice.

Recover it instead, free:

```sh
taskfuel result                                # what you lost, and what is still running
taskfuel result <request_id>                   # print that call's response body
taskfuel result <request_id> --output out.png  # ...or write it to a file
```

Run it bare first: a call that died on your side never printed its request id,
so the listing is where you find one. Each row says what state it is in and
what to do about it.

## 5. Rate the endpoints you call, and report upstream issues

The provider, not taskfuel, maintains each endpoint and its docs,
response quality, price, and payment terms. taskfuel pays the provider on the
user's behalf and curates which APIs appear in discovery. Feedback from real
calls helps taskfuel surface reliable APIs and deprioritize providers with
recurring problems.

After calling an endpoint, rate it with the same method and URL you called:

```sh
taskfuel rate https://api.example.com/search --vote up
taskfuel rate https://api.example.com/generate --method POST --vote down
```

- Vote `up` if you got the expected/useful result; vote `down` if the
  endpoint didn't work or wasn't worth the price. Vote and report must agree:
  no `up` with a complaint attached.
- Judge the endpoint against its own docs, from a call you made. A missing
  catalog entry, your own bad arguments, or an endpoint that worked but wasn't
  what the task needed are not down-votes: a catalog gap goes to `taskfuel
  feedback` (section 6) and to the user.
- One vote per endpoint, changeable at any time — voting again replaces the
  previous vote. `discover` shows each endpoint's rating, so a low score is a
  reason to prefer an alternative before spending.
- Add `--report '…'` when something concrete disrupted usage: an unexpected
  response code, arguments silently ignored, an empty or low-quality response,
  behavior contradicting the docs. Lead with the finding, briefly; no secrets
  or unrelated response data, up to 2000 characters. A report is a curation
  signal, not a rating — your vote is the rating.

## 6. Send feedback about taskfuel itself

Ratings are about one endpoint. For everything else there is one free-text
channel to taskfuel:

```sh
taskfuel feedback "discover finds nothing for weather data; three searches, zero usable hits"
```

Send it for a problem with taskfuel rather than with one endpoint's behavior:
install, `connect` or auth trouble; CLI or gateway errors; `discover` that
found nothing or the wrong things; a capability missing from the catalog (tell
the user too); billing, balance or spending-cap confusion; docs that turned out
to be wrong; or the same failure pattern across several providers — describe
that once here, and still rate each endpoint you called.

Send it when you actually hit something, once per problem — don't restate an
endpoint report you already filed, and don't include secrets or response
data. Lead with what happened and what you expected; up to 2000 characters.

## What you get charged for

- **Success or nothing.** A call rejected before it goes out (empty balance,
  a domain that is not allowed, a price above the cap, a rate limit, a
  malformed request) and a call the provider fails (4xx, 5xx, or a payment
  that does not settle) both cost nothing. taskfuel absorbs the provider's cost
  rather than passing it on.
- **A successful call is charged even when its answer is useless to you.**
  Success means the endpoint answered, not that it answered well. An empty
  search result, a thin response, or a bad match for your query is a real
  charge and not a billing error, so don't tell the user to expect a refund.
  Downvote the endpoint instead (section 5), and use `taskfuel feedback`
  (section 6) when the problem is taskfuel's rather than one endpoint's.

## Spending rules (non-negotiable)

- **Preview before paying**: Quote the first call to any endpoint in a session.
  Set your per-call cap with `--max-amount` in the CLI or `max_amount_usd`
  in MCP. A quote refused as `not_quotable` means the endpoint declares no
  price. In the CLI, use a `--max-amount` within the applicable budget and
  approval limits. In MCP, follow the bounded-call permission rule above.
  A `spec_unavailable` refusal is transient: retry the quote shortly.
- **Ask before big spends, and ask once**: a single call over $1, or a task
  whose paid calls will add up to more than $5, needs the user's explicit OK
  first. Below those lines, call without asking: the quote and the gateway's
  hard cap already bound what a call can cost, and asking for every $0.10
  call is what users complain about. An approval sticks for the session:
  once the user has OK'd an endpoint at a quoted price, do not ask again for
  that endpoint at the same or a lower price. Ask again only when a quote
  comes back higher, an endpoint is new, or the running total crosses the
  budget again (each further $5, or whatever budget the user named up front,
  which replaces the default).
- **Approved price is the ceiling.** Keep your per-call cap at or below the
  approved price. If a call is rejected for exceeding a cap, raising it needs the
  user's OK, and the gateway's hard cap is not yours to raise.
- **Rate limit**: 60 calls/min per key.
- **Report spend once per task.** Give the user the total when the result
  is in, not a line per paid call. An async job is one purchase: polling its
  task id to a terminal status belongs to the submit, approved or not, and
  the polls count toward the task budget. Poll through taskfuel too: the
  job belongs to the wallet that paid for it, so its status URL refuses a
  direct request. Polls can be charged: poll at the documented cadence, or
  every 20 seconds past the typical completion time. After 30 polls, stop and
  tell the user the job is still running. Resubmitting buys it twice.
- **Never retry a paid call blindly.** A "paid" line means the call was
  charged, however bad the response: tell the user and let them decide, and
  rate the endpoint down. Recover a lost response with `taskfuel result` in
  the CLI or `get_result` in MCP.
- **Stop at low balance**: if balance < the next call's price, stop and tell
  the user to top up at their dashboard. Don't hunt for workarounds. If you
  could pay for credit yourself, tell us with `taskfuel feedback` which
  payment method you would use.
