# pursekeeper skill

An OpenClaw / ClawHub skill: earn and spend Nano (XNO) with other agents. The skill text
is `SKILL.md`; `scripts/` holds a no-node Nano wallet and an x402 `exact` client for
`nano:mainnet`; `references/` holds the seller directory snapshot and the recipes.

Install from ClawHub once published: `clawhub install pursekeeper`. Until then:

```
git clone https://github.com/pursekeeper/skill ~/.openclaw/skills/pursekeeper   # or your skills dir
cd ~/.openclaw/skills/pursekeeper/scripts && npm install
```

Everything here is MIT-0, like every ClawHub skill. Source of the recipes and the
endpoints: https://github.com/pursekeeper/api. Site: https://pursekeeper.dev.

## Tests

With Node.js 18 or newer, install the root development dependency once, then run:

```sh
npm install --include=dev --ignore-scripts
npm test
```

(`--include=dev`: on a box with `NODE_ENV=production` npm omits development dependencies
and the tests then stop at "Cannot find module 'nanocurrency'".)

`npm test` uses `node --test test/` (`test/index.js` is the directory entry point).
It needs no Internet access, API key, wallet, or funds after dependency installation.
Each test starts an ephemeral `127.0.0.1` HTTP server and runs the real
`scripts/no-node.js` CLI in a child process with a new throwaway seed. The child
gets only explicit test environment variables, and its fetch is restricted to the
mock's exact origin with redirects disabled. No real proof of work is generated.

The mock implements `account_info`, `receivable`, `work`, `process`, and `verify`.
It accepts and hashes the first block, updates the actual frontier and balance,
then returns a 502/Fork error instead of the success reply (the node-like stand
from [issue #3](https://github.com/pursekeeper/skill/issues/3)). A valid second send
is accepted too, so the mock exposes a double payment rather than hiding it.
Both tests require one process call, one accepted block, one balance change,
and a CLI receipt containing the original block hash. The receive case also
removes the pending source when pocketed, rather than leaving a stale receivable.

To reproduce the regression against the historical scripts without modifying
production code or fetching anything during the tests:

```sh
snapshots=$(mktemp -d)
git show fe43bbd:scripts/no-node.js > "$snapshots/0.1.3.cjs"
git show 8fe3ac7:scripts/no-node.js > "$snapshots/0.1.4.cjs"
NO_NODE_SCRIPT="$snapshots/0.1.3.cjs" npm test # expected failure
NO_NODE_SCRIPT="$snapshots/0.1.4.cjs" npm test # expected success
npm test                                    # current scripts
rm -r "$snapshots"
```

On 0.1.3 the send test reports **two** process calls and accepted blocks instead
of one; the receive test also fails because the CLI skips the pocketed source
without returning its accepted hash. Both pass on 0.1.4 and current main.
These tests model that specific Fork-shaped lost reply; they do not claim to
exercise all later timeout/indeterminate-verification fixes or mainnet consensus.

## Unsigned quote redirects

The unpaid x402 quote request follows redirects only while the target stays on the original URL's origin. Same-origin redirects are followed for up to 20 hops with the original method, body and headers (including POST on 301/302/303); a cross-origin redirect exits with code 6 before any request reaches the target, whether or not `HEADERS` is set. No payment is signed on this path. To use a canonical URL on another origin, pass that final URL directly and provide only the headers intended for it. The later signed request remains manual and never forwards its payment block to a redirect target.

## Traps seen in the field

Both reported by an OpenClaw agent on its first paid call (expeditious, 2026-09-29):

- `nanocurrency.deriveAddress(publicKey)` without `{ useNanoPrefix: true }` returns an
  `xrb_` address. Sellers and this API accept `xrb_` and `nano_` alike for the block's
  `account`, but a payTo or a payout address written as `xrb_` reads as wrong to most
  wallets and directories; `scripts/no-node.js` and `scripts/client-x402.js` pass the
  option and rewrite `xrb_` to `nano_` on the block. Copy that, not the bare call.
- `scripts/client-x402.js` asks the seller's own `POST /v1/work` for work when `WORK_URL`
  is unset. A seller that answers that route with an HTML page (a hosting front page, a
  tunnel error) makes the client fail on the JSON parse after the 402, before anything is
  signed or paid. Set `WORK_URL` to a work_generate endpoint you trust (pursekeeper.dev's
  `/v1/work`, your own node) and the seller's route is not used.
