# CLI workflows

Use command help for shorthand. Do not mix shorthand with `--arguments`. For an offline plan, use supplied terms and IDs with `--dry-run`; defer live account/merchant preflight and sign-in until execution is authorized. Local validation does not establish merchant availability, card eligibility, or payment acceptance.

## Image search

Use `shop search --like-image photo.jpg`, optionally with a text query. Files and inline MIME/base64 accept JPEG, PNG, WebP, AVIF, or HEIC, not GIF or SVG. This is format-declaration checking, not image decoding.

The complete request must fit 4 MiB after base64 and JSON framing; a usable file is therefore smaller than 3 MiB, depending on other arguments and metadata. If a local `invalid_input` names the framing limit, resize the image or reduce other arguments before submitting again. No request was sent for that refusal.

## Find stores

Search a business's physical stores by place words, or by a radius around coordinates the user gave; narrow to stores that can currently provide a variant with `--item`:

```sh
shop location search 'New York' --shop '<seller.domain>'
shop location search --shop '<seller.domain>' --center-latitude 40.7227 --center-longitude -73.9946 --distance-max 5000 --item '<variant-id>'
shop location lookup '<location-id>' --shop '<seller.domain>' --item '<variant-id>'
```

The three distance flags travel together. `--item` repeats or takes a comma-separated list; `--country` helps resolve the variants. Read `messages[]` and `next[]` in the result.

## Ask the business

Ask a shop a free-form question; optionally ground it in one or more of the shop's resources with `--id` — a variant from a catalog result, a collection, a cart `id` as the cart returned it — and add the buyer's country, currency and language when the answer depends on them:

```sh
shop ask 'What is your return window, and who pays return shipping?' --shop '<seller.domain>'
shop ask 'What is this made of, and where is it made?' --shop '<seller.domain>' --id '<variant-id>' --country CA --currency CAD --language en
shop ask 'Which of these come in a size 10?' --shop '<seller.domain>' --id '<collection-id>,<variant-id>'
```

`--id` repeats or takes a comma-separated list; a cart grounds the products in it. The answer is the business's own statement; `messages[]` name IDs the shop did not use, `next[]` what to do with the document. `--format md` prints the answer as prose.

## Cart to checkout

Create checkout from a returned cart:

```sh
shop checkout create --shop '<seller.domain>' --cart '<cart-id>'
```

The cart id stays exact; do not combine this form with item or buyer-country shorthand.

## Guarded edits

`cart update` and `checkout update` with `--patch` read, apply guarded RFC 6902, then send a full update. Each positional line edit needs a preceding `test` on the returned `/line_items/N/id`, not its variant `item.id`.

```sh
shop checkout update '<checkout-id>' --shop '<seller.domain>' --patch '[{"op":"test","path":"/line_items/0/id","value":"<line-id>"},{"op":"replace","path":"/line_items/0/quantity","value":2}]'
```

Replace placeholders with returned values. The guard checks local assumptions, not concurrent merchant edits.

## Complete a Shop checkout

Inspect the latest checkout returned by `checkout create`, `checkout update`, or `checkout get`, including its status, items, totals, messages, and `payment.instruments`. If it may be stale, call `checkout get` first. `ready_for_complete` is the authoritative signal that the current checkout may be completed through the API; `requires_escalation` means give the user its `continue_url`. Present the offered instruments to the user, confirm one exact instrument with the current purchase terms, then pass that complete instrument object exactly as returned:

```sh
shop checkout complete '<checkout-id>' --shop '<seller.domain>' --instrument @instrument.json
# Or pipe the exact JSON object on stdin and pass: --instrument -
```

Use `@FILE` or stdin for an object that contains a credential or other secret so it does not enter argv or shell history. Use inline JSON only when the complete instrument is demonstrably non-secret. The CLI preserves every instrument field and extension, sets only root `selected:true`, and sends exactly one `complete_checkout`; it does not fetch, preflight readiness, look up an id/handler/display value, choose a default, or accept multiple instruments. The merchant remains authoritative for freshness, readiness, and whether the instrument is still offered. Do not independently infer completion authority from the account's spend permissions. Only a returned `completed` checkout with an order confirms the purchase. No separate spend request is needed for this checkout, even when buyer review opens in a browser. Never switch to a spend request after an API failure, timeout, decline, or escalation.

## Pay through a website's card form

Follow the purchase flow in [transactions.md](transactions.md). Use command help or `--schema` for the purchase terms and approval text.

Wait for the buyer to approve the request and retrieve the issued card in one call:

```sh
shop spend-request get '<spend-request-id>' --include card --wait 90
```

Omit `--include card` to read status and terms only. For private file handoff, add `--output-file payment.json` to the same command. It requires explicit card selection and writes a new `{spend_request_id,card}` file; stdout contains `credential_output_file` instead of the card. Give the file directly to the consuming program without printing its contents.

Existing files are refused; the caller owns cleanup. POSIX files are mode `0600`; on Windows, use a directory with private ACLs. Browser-hosted Shop cannot export files. `--dry-run` creates nothing.
