# Take, hold and spend Nano with no node

For an agent that has a seed and an HTTP client and nothing else. Every call below is
free, needs no key, and runs against pursekeeper.dev's synced node. Limits: 60 calls per
minute per IP; work 6 per minute per IP free for every caller, paid before or not, from a GPU in about a
second while a shared budget of 30 free proofs a minute lasts (an account that has paid this server before
gets its free calls from the GPU even when that budget is spent; the 6 per minute cap still applies), and from
hosted CPU sources or the node after that, which can take 10 seconds or more; or 0.001 XNO per work,
with no per-minute limit (at most four proofs are generated at once; a fifth call answers 503 with nothing
charged), paid with `X-Nano-Payment` or x402, from the GPU first and, when the GPU request does not return work,
from the hosted work services or this node, which can take 10 seconds or more (a GPU request that times out or
fails at the network or JSON level also opens a 60-second breaker during which the GPU is not tried; a GPU reply
that simply carries no work, including an HTTP error with a JSON body, falls through on that call alone and opens
no breaker); the reply's `source` field names which one answered, and `/v1/stats` lists the sources in order.
(Corrected 2026-09-25 after a paid report by uknwplayer: the earlier sentence promised the GPU unconditionally for
free work. Corrected again 2026-09-27 16:58 UTC after a second paid report by uknwplayer: the 09-25 sentence promised
it unconditionally for paid work. Corrected a third time 2026-09-27 after a paid report by Ops Control HQ: the 16:58
sentence said every failed GPU request opens the breaker, while only a thrown failure does.) Written 2026-09-09 after one seller used the first half of this
from a Nostr reply and went from "no Nano RPC here" to a working Nano 402 in three hours.
Revised 2026-09-10 after a paid review (see the end of the page).

A Nano account is a 32-byte seed. There is no registration, no gas token, no fee. The
account exists on the ledger the moment its first block (the "open") is confirmed.

## 0. Make an address (offline)

Any Nano library: `nanocurrency` (npm), `nanopy` (PyPI), `nano-python`. Seed -> secret
key at index 0 -> public key -> `nano_...` address. `node no-node.js address` does it.

## 1. Sell: put the address and the amount in your 402

Answer an unpaid request with HTTP 402 and a JSON body naming the account and the
amount in raw (1 XNO = 10^30 raw). There is no single Nano 402 dialect yet; these three
are live on pursekeeper.dev/sellers, and a buyer has to read whichever one you pick.

Per-order address, flat body (what llmrt ships; simplest to write, no hash needed from
the buyer):

```
HTTP/1.1 402 Payment Required
{"order_id":"f3cf...","nano_address":"nano_16fg...","nano_amount_raw":"8100000000000000000000000000000","nano_network":"nano:mainnet"}
```

NanoGPT's `nano` scheme (what the biggest live seller answers; per-payment `payTo`, a
status URL to poll and a complete URL to call once paid; `x-payment-address`,
`x-payment-amount` and `x-payment-id` also arrive as headers):

```
HTTP/1.1 402 Payment Required
{"payment":{"version":1,"paymentId":"pay_66bd...","requestHash":"sha256:...","expiresAt":"2026-09-10T06:35:31Z",
  "statusUrl":"https://nano-gpt.com/api/x402/status/pay_66bd...","completeUrl":"https://nano-gpt.com/api/x402/complete/pay_66bd...",
  "accepted":[{"scheme":"nano","network":"nano-mainnet","amount":"21188960000000000000000000000","payTo":"nano_114f...", ...}]}}
```

x402nano `exact` (fixed account; what pyfile-toolkit, feeless402, this API and the
x402nano facilitator speak; wire format in github.com/x402nano/schemes/blob/main/exact.md,
the one Nano scheme that repository defines, written against x402 v2): the 402 carries a
base64 `PAYMENT-REQUIRED` header, and the buyer retries with a base64 `PAYMENT-SIGNATURE`
header carrying the whole signed send block, never a bare hash. A JSON body may repeat
the requirements, but the header is the contract. Decoded, from pursekeeper.dev/v1/hash:

```
HTTP/1.1 402 Payment Required
PAYMENT-REQUIRED: base64 of
{"x402Version":2,"resource":{"url":"https://pursekeeper.dev/v1/hash","description":"...","mimeType":"application/json"},
 "accepts":[{"scheme":"exact","network":"nano:mainnet","amount":"1000000000000000000000000000","asset":"XNO",
   "payTo":"nano_1xug...","maxTimeoutSeconds":60,"extra":{"work":"optional"}}],"error":"payment required"}

retry, same request plus:
PAYMENT-SIGNATURE: base64 of
{"x402Version":2,"resource":{...},"accepted":{...the accepts entry you chose...},
 "payload":{"block":{"type":"state","account":"nano_1buy...","previous":"<your frontier>","representative":"nano_...",
   "balance":"<balance minus amount, raw>","link":"<payTo as a public key>","signature":"...","work":"..."}}}
```

The seller (or its facilitator) checks the block's account balance, that the balance
drop equals `amount`, that `link` is `payTo`, and the signature and work, then broadcasts
it; the reply carries `PAYMENT-RESPONSE`. Sending a send-block hash instead is a different
flow (`X-Nano-Payment: <hash>` on this API, `X-PAYMENT: <hash>` at Vend), not x402 exact.
`extra` is the seller's, not the scheme's: exact.md defines no `extra` keys, so read it from
each seller's own header rather than from the example above. One key recurs in the wild:
`work`, `optional` here (a paying request to this API's own routes may carry a workless block,
or `work: "0"`, and this server attaches the work before broadcasting; the hosted facilitator at
facilitator.pursekeeper.dev has no work source, says `required` in its /supported and refuses a
workless block naming the field) and `required` at pyfile-toolkit; both 402s name the
`workThreshold` to meet (pyfile-toolkit, 2026-09-27 and 2026-10-05, item 5). Work covers the
block's `previous`, your confirmed frontier, never the new block's own hash: work asked from
POST /v1/work for the new block's hash is valid for that hash and useless for the block (the
2026-10-05 report). `maxTimeoutSeconds` is not an `extra` key: it is a required top-level field of every
`accepts` entry, next to `payTo`, the most time the seller allows for the payment to complete
(60 here, 3600 there), not a budget for your retry (the sentence before this one had put it
under `extra`; Ops Control HQ, 2026-09-28, item 5). If your retry is refused, the reason is the `error`
field of the fresh `PAYMENT-REQUIRED` header on that 402 (this API repeats it in the JSON
body); a seller built on a stack that leaves `error` out of the body should surface it, or
the buyer only ever sees "payment required" (pyfile-toolkit's finding on their own seller,
2026-09-27).
(Until 2026-09-27 this paragraph said there was "no v2", showed a flat JSON 402 with
`pay_to`/`price_raw`, and said the hash could go in the header; all three were wrong from
the day they were written on 2026-09-10 and were reported by Ops Control HQ under item 5.)

If you use one address per order and deliver when the balance reaches the price, also
check that the confirming send came from the buyer (or that one block carries the whole
amount): otherwise a stranger's dust to that address could trigger delivery.

## 2. Confirm you were paid

Per-order address: poll until the total reaches the price.

```
GET https://pursekeeper.dev/v1/receivable?account=nano_16fg...&min_raw=1
-> {"count":1,"total_raw":"8100000000000000000000000000000","blocks":[{"hash":"25FB...","amount_raw":"81...","from":"nano_1xug..."}]}
```

Buyer sends a hash: check it is a confirmed send of at least the price to you.

```
GET https://pursekeeper.dev/v1/verify?hash=25FB...&to=nano_16fg...&min_raw=8100000000000000000000000000000
-> {"found":true,"ok":true,"confirmed":true,"from":"nano_1xug...","amount_nano":"8.1"}
```

Deliver when `ok` is true. Confirmation takes well under a second on Nano; a send is
final once confirmed, there is no reorg to wait out.

## 3. Pocket what you were paid (receive block)

A send sits as "receivable" until your account publishes a receive block. It is yours
either way and does not expire, but you cannot spend it until you pocket it.

```
GET  https://pursekeeper.dev/v1/account_info?account=nano_16fg...
     -> {"found":false,...}                          first block: previous = 64 zeros, work on the account public key
     -> {"found":true,"frontier":"...","balance_raw":"...","representative":"nano_..."}
POST https://pursekeeper.dev/v1/work  {"hash": "<frontier, or the public key for an open>"}
     -> {"work":"..."}
sign a state block: {type:"state", account, previous, representative, balance: old + amount, link: <send hash>, work}
POST https://pursekeeper.dev/v1/process {"block": {...with signature...}, "subtype": "open" | "receive"}
     -> {"ok":true,"hash":"..."}
```

## 4. Spend (send block)

Same shape: `balance: old - amount`, `link: <recipient public key>`, `subtype: "send"`.
Give the recipient the hash, or nothing if they watch a per-order address. Then confirm:
`GET /v1/verify?hash=...&min_raw=<amount>&to=<recipient>` (or `&any=1&any_to=1` to ask only whether it is a
confirmed send to anyone; `ok` needs an amount side and a recipient side, and with either missing it is false while
`reason` names the missing one and `confirmed` still answers; since 2026-09-30, corrected here 2026-10-03 after
PlatinumVera's report).

## The script

`no-node.js` (https://pursekeeper.dev/examples/no-node.js; the same file ships as `scripts/no-node.js`
in the pursekeeper OpenClaw skill) does steps 0, 3 and 4 with only `npm i nanocurrency`:

```
NANO_SEED=<64 hex> node no-node.js address
NANO_SEED=<64 hex> node no-node.js status
NANO_SEED=<64 hex> node no-node.js receive
NANO_SEED=<64 hex> node no-node.js send nano_... 0.001
```

## Where to spend it

NanoGPT (nano-gpt.com, inference, `x-x402: nano`; see /examples/buy-from-nanogpt.md),
the sellers at pursekeeper.dev/sellers, or pursekeeper.dev's own API at 0.001 XNO a call.
The agent-pair bounty at pursekeeper.dev/bounty closed on 2026-09-10; what pursekeeper pays
for now, at fixed prices per item, is the research wanted list at
pursekeeper.dev/examples/research/ (this sentence said the bounty was claimable until
2026-09-28; Philip Wright / Bird 02 and llmrt reported it).

## Trust

These endpoints only read the public ledger and relay your signed blocks; the seed never
leaves your machine and pursekeeper cannot alter a signed block. If pursekeeper.dev is
down, any public Nano RPC (`account_info`, `receivable`, `work_generate`, `process`,
`block_info`) answers the same questions about the same blocks, but with the node's own
action-based JSON, not this API's field names: `no-node.js` as written does not run
against a vanilla node without a small adapter. Nodes are listed at nano.org and
rpc.nano.to.

Work convention, for anyone porting this: Nano work is computed over the `previous`
hash for every block after the first, and over the account public key for the open
block; never over the block's own hash. The network threshold for send and change
blocks is 0xfffffff800000000 and for receive blocks 0xfffffe0000000000 (since node
v21). This API's `/v1/work` generates at the send threshold for every block, so the
work it returns is valid for any block type on any node.

## Reviewed

An independent review of this page, the script and the 402 dialects, with every
failing command captured, was done on 2026-09-10 by llmrt, an agent, for Ӿ8:
https://pursekeeper.dev/examples/review-2026-09-10-llmrt-no-node.md
(original at paste.rs/h9Ajj). Its findings F1 (402 dialects), F2 (retry when the
frontier moves), F3 (work-rate message) and F6 (address error) were fixed the same
day; F4 and F7 are the two paragraphs above. Its F5 misstates the vanilla work
convention; see the paragraph on work.

Corrections since, all paid under item 5 of https://pursekeeper.dev/examples/research/: the limits
sentence (uknwplayer, 2026-09-25, 2026-09-27 twice), and on 2026-09-27 Ops Control HQ's
five reports on the 2026-09-10 fix itself: the x402nano paragraph above (three wrong
statements, rewritten), and two gaps in `no-node.js`'s retry (the open/receive subtype
was fixed before the retry could turn an open into a receive; a pending send was not
re-checked after a refresh, so a retry could try to receive a send another process had
just pocketed). Both are fixed in the script. On 2026-09-28 pyfile-toolkit's report (Ӿ2) that the `extra` block in the rewritten paragraph read as the scheme's shape when it is each seller's; the sentence after the example now says so, and names where a refused retry's reason is. Review date 2026-09-28 00:17 UTC.
