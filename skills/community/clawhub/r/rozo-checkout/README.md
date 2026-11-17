# rozo-checkout

**English** | [简体中文](docs/README.zh.md) | [日本語](docs/README.ja.md) | [Español](docs/README.es.md)

### When your agent needs to pay OpenRouter (or any Coinbase invoice) with the crypto you already hold

OpenRouter crypto top-ups and other Coinbase-hosted invoices settle in USDC on
Base. This skill pays them from whatever you hold instead, and it does three
things the official path cannot:

- **Pay from the chain you are already on.** USDT or USDC on Solana, BNB Chain,
  Ethereum, Polygon or Arbitrum, USDC on Base or Stellar, BTC over Lightning, or
  a native coin: ETH on Ethereum, Base or Arbitrum, BNB, SOL or POL. Coinbase's
  own direct pay takes USDC on Base.
- **No Coinbase account.** Pay the deposit address from any wallet or straight
  from an exchange withdrawal. No sign-up, no API key, no browser.
- **Scriptable.** OpenRouter's crypto credits API (`POST /api/v1/credits/coinbase`)
  now returns `410 Gone`, so top-ups can no longer be automated there. Once you
  have the payment link, paying it is one command an agent or a cron job can
  run: without a terminal it stops for confirmation, so an unattended caller
  reviews the quote and then passes `--yes`.

Merchants we have been paid through so far: **OpenRouter, Venice.ai, Porkbun
and Alchemy**. Any `payments.coinbase.com` link is quoted the same way.

Before you pay, know two things:

- **The fee is in the live quote.** You pay the full invoice, no discount, plus
  a Rozo service fee shown as its own line (1% today, never more than 1% in this
  CLI); the bridge and network fee is added to the deposit amount, which is
  shown in the order summary before the deposit address is released. Send
  exactly that amount, nothing more is charged.
- **Crypto payments to OpenRouter are never refundable.** That is OpenRouter's
  policy, not ours; check the credit amount before you send.

```bash
npx @rozoai/checkout pay <coinbase-link>
```

It asks which coin you want to pay with — paste your wallet address at the
prompt and it will mark which coins you can actually afford — then prints a
deposit address for you to pay from any wallet — **no private key, no environment variable, no
configuration** — and waits until the invoice is settled.

Paying a **Bitrefill** invoice instead? Create it on Bitrefill with "USDC on
Base", then pass its id, address and amount (Coinbase payment links and
Bitrefill invoices are the two supported targets; Stripe is not):

```bash
npx @rozoai/checkout pay --bitrefill-invoice <id> --to <0x…> --amount 7.90 --expires-at <ISO> --with usdc-stellar
```

Know your coin already? Skip the question:

```bash
npx @rozoai/checkout pay <coinbase-link> --with usdt-solana
```

## Coins you can pay with

| Chain | `--with` | Chain id | Notes |
|---|---|---|---|
| Ethereum | `usdt-ethereum` `usdc-ethereum` | `1` | 6 decimals |
| BNB Chain | `usdt-bnb` `usdc-bnb` | `56` | 18 decimals |
| Polygon | `usdt-polygon` `usdc-polygon` | `137` | 6 decimals |
| Arbitrum | `usdt-arbitrum` `usdc-arbitrum` | `42161` | 6 decimals |
| Base | `usdc-base` | `8453` | 6 decimals |
| Solana | `usdt-solana` `usdc-solana` | `900` | SPL |
| Stellar | `usdc-stellar` | `1500` | `MEMO_TEXT` memo required — shown in the deposit block |
| Bitcoin Lightning | `btc-lightning` | `lightning` | BOLT11; amounts in satoshis. Any wallet that can pay an invoice works, including Cashu/ecash wallets — the mint melts your ecash into the Lightning payment. |

**Native coins**, each on its own chain:

| Coin | `--with` | Chain id | Notes |
|---|---|---|---|
| ETH on Ethereum | `eth-ethereum` | `1` | 18 decimals (wei); $1 minimum |
| ETH on Base | `eth-base` | `8453` | 18 decimals (wei) |
| ETH on Arbitrum | `eth-arbitrum` | `42161` | 18 decimals (wei) |
| BNB | `bnb-bnb` or `bnb` | `56` | 18 decimals |
| SOL | `sol-solana` or `sol` | `900` | 9 decimals (lamports) |
| POL | `pol-polygon` or `pol` | `137` | 18 decimals |

A native coin is offered only when the invoice's quote lists it (`quote` shows
which), and only for invoices up to $3,500. The order is **exact-out**, like
Lightning: send exactly the coin amount in the deposit block. Its price is
locked only until the time shown (about an hour, while the OpenRouter link
itself stays payable about 24 hours); after that, do not send it,
let the order expire and start a new one. The coin amount includes an FX spread
on top of the service fee, and your wallet needs a little more of the same coin
for the network fee. If you pay from an exchange, the amount that arrives must
be the full amount: check that the withdrawal fee is not taken out of it.
`--send` pays native coins too, as a plain transfer of the exact amount.

On-chain BTC and Tron are not supported.

ZEC from a shielded balance (Beta): `pay <link> --with zec --shielded` prints the
Unified Address, the exact amount and a ZIP-321 payment URI to scan with a shielded
wallet such as Zashi. The CLI never sends ZEC. Pay the exact amount in one
transaction; underpayments are not refunded automatically. Beta limit $1,200 per
payment, minimum $5. Transparent ZEC: use https://checkout.rozo.ai/zec.

## Which wallet do I need?

**One wallet, on one chain — not one per chain.** Pick whichever coin above you
already hold and pay from wherever it already lives.

- **Any wallet works, and so does an exchange withdrawal.** The default path
  just prints a deposit block: send exactly that `amount` of that
  `tokenSymbol`, on that `chain`, to that `receiverAddress`. Nothing connects to
  a site and nothing is approved in a browser. In practice people use MetaMask
  or Rabby on the EVM chains, Phantom or Solflare on Solana, and a Lightning
  wallet such as Phoenix or Wallet of Satoshi for BTC.
- **Stellar is the one to be careful with.** Its deposits route through a shared
  address plus `receiverMemo`, so whatever you send from — exchange or wallet —
  must let you set a memo. Omit it and the payment is lost.
- **Lightning pays an invoice, not an address.** Scan or paste
  `deposit.lnInvoice`; there is no address to send to. A Cashu/ecash wallet
  works here too — paying the invoice melts the ecash on your behalf, and this
  route settles against ROZO's own Lightning node rather than a third-party
  swap, so no special handling is needed on our side.
- **Only `--send` needs a private key**, read from `ROZO_CHECKOUT_EVM_KEY` or
  `ROZO_CHECKOUT_SOL_KEY`, and it covers EVM chains and Solana only (their
  native coins included). Everything else is keyless.

## Use it from your agent

Install it as a skill, or just run the CLI:

```text
# Claude Code
/plugin marketplace add RozoAI/rozo-checkout-skill
/plugin install rozo-checkout@rozo

# OpenClaw / ClawHub
clawhub install rozo-checkout

# Any agent that can run a shell: review the quote, then pay unattended
npx @rozoai/checkout quote <coinbase-link>
npx @rozoai/checkout pay <coinbase-link> --with usdt-solana --yes
```

The payload is the same everywhere: the one-liner above, or point the agent at
[llms.txt](llms.txt). Agents and scripts should always pass `--with` — the
picker only appears on a terminal, and there is deliberately no default coin. **Paying from your own wallet never needs a key.** Only
the optional `--send` flag signs locally: on Solana it uses the
`~/.config/solana/id.json` that `solana-keygen` already created, and on EVM an
encrypted JSON keystore whose passphrase is prompted. A raw key in the
environment (or a gitignored `.env`) still works for unattended automation.

Distributing this CLI? `--utm-source <label>` (or `ROZO_CHECKOUT_UTM_SOURCE`) is an optional channel label for reporting; no identity, no privilege.

Want ROZO to be able to reach you if a payment needs attention? Add the optional `--email you@example.com` to `pay`.

### Privacy: anonymous install id

Every order this CLI creates carries two optional reporting fields in
`attribution`, so repeat orders from one install can be counted as one payer:

- `install_id`: a random UUID v4 made on first run and stored in
  `~/.rozo-checkout/prefs.json` (mode 0600). It is not derived from your
  machine, wallet or anything else about you.
- `account_hash`: sent only if `OPENROUTER_API_KEY` is set in your
  environment. It is the lowercase hex sha256 of `"rozo-acct-v1:" + key`. The
  key itself is never sent, logged or written to disk. An OpenRouter account id
  is never used for this, because a hash of a short id could be guessed back.

Delete `~/.rozo-checkout/prefs.json` to get a new id (it also forgets your last
wallet and coin). Set `ROZO_CHECKOUT_ANON_ID=off` to send neither field.

Need help? Email hi@rozo.ai, or reach us on [X](https://x.com/ROZOai) or [Discord](https://discord.gg/EfWejgTbuU).

<details>
<summary><b>Set up a local wallet for <code>--send</code></b> — .env template and per-wallet export steps</summary>

You very likely do not need any of this: the default path needs no key, and for Stellar the `stellar-agent-wallet` skill sends with its own key handling — this `.env` setup is only for unattended EVM/Solana automation with a dedicated low-balance hot wallet.

**None of this is needed for the default path.** Paying from your own wallet
needs no key and no configuration, and works with wallets that can never be
used here — including hardware wallets and exchange accounts.

A `.env` in the directory you run from, with every variable this tool reads:

```bash
# None of this is needed to pay from your own wallet. These are read only
# when you use --send.

# Solana secret key: a base58 string, or a JSON byte array. Only needed if you
# do NOT have ~/.config/solana/id.json, which is picked up automatically.
ROZO_CHECKOUT_SOL_KEY=REPLACE_ME_base58_secret_key

# EVM raw private key: 64 hex characters, 0x prefix optional. The least safe
# option — prefer the keystore below.
ROZO_CHECKOUT_EVM_KEY=0x0000000000000000000000000000000000000000000000000000000000000000

# EVM encrypted V3 keystore: path to the file. Preferred over the raw key.
ROZO_CHECKOUT_EVM_KEYSTORE=/replace/me/keystores/my-hot-wallet

# Passphrase for that keystore. Only for unattended runs; on a terminal you
# are prompted instead, and nothing is stored.
ROZO_CHECKOUT_KEYSTORE_PASSPHRASE=REPLACE_ME_not_a_real_passphrase

# Optional RPC overrides, one per chain id. 8453 = Base, 42161 = Arbitrum,
# 900 = Solana.
ROZO_CHECKOUT_RPC_8453=https://mainnet.base.org
ROZO_CHECKOUT_RPC_900=https://api.mainnet-beta.solana.com
```

Then lock it down and keep it out of git:

```bash
chmod 600 .env
echo '.env' >> .gitignore
```

**Solana**

- `solana-keygen new` writes `~/.config/solana/id.json`. Nothing to configure —
  it is found automatically. This is the path we recommend.
- **Phantom** → Settings → Export Private Key gives a **base58** string. Put it
  in `ROZO_CHECKOUT_SOL_KEY`.
- **Solflare** exports a base58 string in current versions and a JSON byte
  array in older ones. Both are accepted as-is.

**EVM**

- **MetaMask** and **Rabby** → Export private key gives 64 hex characters.
  Paste it into `ROZO_CHECKOUT_EVM_KEY` as-is; the `0x` prefix is optional.
- **Encrypted keystore (safer).** Browser wallets export raw keys, not
  keystores. To turn one into an encrypted keystore, use Foundry:
  `cast wallet import my-hot-wallet --interactive` prompts for the key and
  writes an encrypted V3 keystore to `~/.foundry/keystores/my-hot-wallet`
  (`--keystore-dir` changes where). Point `ROZO_CHECKOUT_EVM_KEYSTORE` at that
  file. `geth account import` also produces a V3 keystore.

**Wallets that cannot be used with `--send`:** hardware wallets (Ledger,
Trezor), WalletConnect-only mobile wallets, and exchange accounts. None of them
hand over a signing key, by design. Use the default keyless path instead — it
works with all of them.

</details>


<details>
<summary><b>Claude Code</b> — install the skill, or paste the one-liner</summary>

This repo is a Claude Code skill: it ships `SKILL.md` plus the executables in
`scripts/dist/`. Clone it into your skills directory and Claude Code picks it
up automatically.

```bash
git clone https://github.com/RozoAI/rozo-checkout-skill ~/.claude/skills/rozo-checkout
```

Or skip the install and just ask it to run:

```
Pay this OpenRouter link with USDT on Solana:
npx @rozoai/checkout pay <coinbase-link> --with usdt-solana
```

Wallet: any wallet, no key. Add `--send` only if you want Claude to sign from a
hot wallet, which needs the env key.
</details>

<details>
<summary><b>Codex CLI</b> — AGENTS.md, or run it directly</summary>

Codex reads `AGENTS.md` from the project root. Add a standing instruction so it
knows how to pay without being told each time:

```
To pay an OpenRouter / Coinbase payment link, run:
npx @rozoai/checkout pay <coinbase-link> --with usdt-solana
```

Wallet: any wallet, no key. `--send` signs locally using your Solana CLI
keypair or an encrypted keystore, and supports EVM chains and Solana only —
Stellar and Lightning are Mode A only.
</details>

<details>
<summary><b>OpenCode</b> — AGENTS.md, or run it directly</summary>

OpenCode also reads `AGENTS.md` from the project root, so the Codex snippet
above works unchanged. The shortest path is still the command itself:

```bash
npx @rozoai/checkout pay <coinbase-link> --with usdt-solana
```

Wallet: any wallet, no key. `--send` signs locally using your Solana CLI
keypair or an encrypted keystore, and supports EVM chains and Solana only —
Stellar and Lightning are Mode A only.
</details>

<details>
<summary><b>Cline</b> — .clinerules, or run it directly</summary>

Cline reads standing instructions from `.clinerules` in the project root:

```
To pay an OpenRouter / Coinbase payment link, run:
npx @rozoai/checkout pay <coinbase-link> --with usdt-solana
```

Wallet: any wallet, no key. `--send` signs locally using your Solana CLI
keypair or an encrypted keystore, and supports EVM chains and Solana only —
Stellar and Lightning are Mode A only.
</details>

<details>
<summary><b>Cursor</b> — .cursor/rules, or run it directly</summary>

Add a project rule at `.cursor/rules/rozo-checkout.mdc`:

```
To pay an OpenRouter / Coinbase payment link, run:
npx @rozoai/checkout pay <coinbase-link> --with usdt-solana
```

Wallet: any wallet, no key. `--send` signs locally using your Solana CLI
keypair or an encrypted keystore, and supports EVM chains and Solana only —
Stellar and Lightning are Mode A only.
</details>

<details>
<summary><b>Hermes Agent</b> — run the one-liner in a session</summary>

Hermes Agent (Nous Research) has shell access and its own skill system. Start it
with `hermes` and ask:

```
Fetch https://checkout.rozo.ai/llms.txt, then pay this OpenRouter link:
npx @rozoai/checkout pay <coinbase-link> --with usdt-solana
```

Wallet: any wallet, no key. `--send` signs locally using your Solana CLI
keypair or an encrypted keystore, and supports EVM chains and Solana only —
Stellar and Lightning are Mode A only.
</details>

<details>
<summary><b>OpenClaw</b> — openclaw agent exec</summary>

OpenClaw's headless entry point runs a one-off task, which suits a payment you
trigger from a script or a chat channel:

```bash
openclaw agent exec "Pay this OpenRouter link with USDT on Solana by running: npx @rozoai/checkout pay <coinbase-link> --with usdt-solana"
```

Wallet: any wallet, no key. `--send` signs locally using your Solana CLI
keypair or an encrypted keystore, and supports EVM chains and Solana only —
Stellar and Lightning are Mode A only.
</details>

<details>
<summary><b>Pi</b> — run the one-liner in a session</summary>

Pi is a BYOK terminal agent whose built-in tools include `bash`, so it can run
the command directly. Start it with `pi` and ask:

```
Pay this OpenRouter link with USDT on Solana by running:
npx @rozoai/checkout pay <coinbase-link> --with usdt-solana
```

Wallet: any wallet, no key. `--send` signs locally using your Solana CLI
keypair or an encrypted keystore, and supports EVM chains and Solana only —
Stellar and Lightning are Mode A only.
</details>

<details>
<summary><b>Terminal — no agent at all</b> — run the scripts step by step</summary>

Drive each step yourself. The bundles are self-contained; nothing to install
beyond Node 20.18+.

```bash
git clone https://github.com/RozoAI/rozo-checkout-skill && cd rozo-checkout-skill
LINK="https://payments.coinbase.com/payment-links/pl_01YOURLINKID"

# Read-only quote, costs nothing
node scripts/dist/quote.js --url "$LINK"

# Create the order. The full deposit address is WITHHELD here; you get a
# masked summary to review first.
node scripts/dist/create-order.js --url "$LINK" --chain 900 --token USDT

# Once you have decided to pay, re-run with --confirm to release it
node scripts/dist/create-order.js --url "$LINK" --chain 900 --token USDT --confirm

# Pay the deposit block from any wallet, then watch it settle
node scripts/dist/status.js --rozo-payment-id <uuid> --watch
```

Each script prints exactly one JSON object on stdout. Exit `0` success, `1`
refused/failed (read `error.code`), `2` usage, `3` submitted but unconfirmed.
Full walkthrough: [QUICKSTART](docs/QUICKSTART.md).

Wallet: any wallet, no key. For hot-wallet sending see `send-evm.js` /
`send-sol.js`, which use your Solana CLI keypair or an encrypted keystore.
</details>

<details>
<summary><b>Any other agent</b> — point it at llms.txt</summary>

Any agent that can fetch a URL and run a command can do this:

```
Fetch https://checkout.rozo.ai/llms.txt into your context, then use it
to pay this OpenRouter link: <coinbase-link>
```

If the agent has no shell but can make HTTP requests, it can drive the four
public endpoints directly — see [how it works](docs/how-it-works.md).

Wallet: any wallet, no key. `--send` signs locally using your Solana CLI
keypair or an encrypted keystore, and supports EVM chains and Solana only —
Stellar and Lightning are Mode A only.
</details>

## Bulk and automated use

Buying credits regularly, reselling them, or building an agent that tops up
OpenRouter for its users? The [Bulk Purchases and Agents](https://docs.rozo.ai/products/checkout/bulk-and-agents)
guide covers the CLI, the MCP server and the raw HTTP flow side by side, plus
fees, rate limits, idempotency, error codes and what each final status means.
The batch script below is the CLI half of it.

## Paying many invoices (batch / resellers)

Each OpenRouter top-up is its own Coinbase link, so paying many is a loop: one
`pay` per link, one logged result per link. Install once
(`npm i -g @rozoai/checkout`) so each run skips the npx download, run the links
one at a time, and pay each deposit right after it is created.

```bash
#!/usr/bin/env bash
# links.txt: one Coinbase link per line (payment-links/pl_* or payment-sessions/paymentSession_*)
mkdir -p runs
while IFS= read -r link; do
  link="${link%$'\r'}"; link="${link%%\?*}"
  [ -n "$link" ] || continue
  id="${link##*/}"
  rozo-checkout pay "$link" --with btc-lightning --yes --json --no-watch \
    --email you@example.com </dev/null > "runs/$id.json"
  code=$?
  row=$(jq -r --arg id "$id" --arg code "$code" '[$id, $code,
      (.order.rozoPaymentId // .error.details.body.rozoPaymentId // "-"),
      (if .success then "pending: pay before " + (.order.expiry.effectiveDeadlineIso // "?")
       else (.error.code // .send.error.code // "FAILED") end)] | @tsv' \
    "runs/$id.json" 2>/dev/null) || row="$id	$code	-	NO_OUTPUT"
  printf '%s\n' "$row" >> runs/batch.tsv
done < links.txt
```

- `--yes` is required when stdin is not a terminal, `--json` prints exactly one
  JSON object, and `--no-watch` returns as soon as the deposit details exist.
  Without `--no-watch`, `pay --json` first waits for settlement (up to
  `--timeout`, default 900 s; for Lightning, the invoice's remaining validity,
  at most 60 minutes) and prints nothing until then, invoice included.
- Without `--send` (the loop above), a successful `pay --no-watch` means the
  order and its deposit details exist. **No money has moved yet**, which is
  why the log says `pending`. With `--send`, the CLI may already have
  broadcast your payment, so never pay that deposit by hand as well. A link is
  paid only when `status` later reports `settled`.
- `order.rozoPaymentId` names the order and `order.deposit` says what to pay.
  Lightning: `deposit.lnInvoice` (the BOLT11) for `deposit.amount` sats. Other
  coins: `deposit.receiverAddress` and `deposit.amount`, plus
  `deposit.receiverMemo` on Stellar. `--send` cannot pay Lightning or Stellar.
  A native coin order has `deposit.native: true` and `deposit.exactOut: true`.
- The deadline to watch is `order.expiry.effectiveDeadlineIso`, not
  `deposit.expiresAt`: it is the earlier of our order expiry and the Coinbase
  link expiry, and for a native coin also its price lock
  (`deposit.quoteExpiresAt`). The two differ a lot: an OpenRouter link stays
  payable about 24 hours after it is created, while a Rozo order lasts about
  an hour, so an order that expires unfunded can be replaced on the same link. Stop paying at least `order.expiry.marginMinutes`
  before it, since settlement needs that much time.
- If time has passed since you created the order, do not pay saved deposit
  details blindly. Re-run the same `pay` command (same `--with`): while the
  order is still payable it re-checks the link and the deadline and hands back
  the same order. Pay only if that succeeds.

Check settlement by `rozoPaymentId` (a link alone is only resolved from this
machine's own records in `~/.rozo-checkout/state`):

```bash
rozo-checkout status <rozoPaymentId> --json | jq -r '.state, .escalate'
rozo-checkout status <rozoPaymentId> --watch --timeout 900 --json   # poll every 10 s
```

Exit 0 means the check itself ran cleanly, not that the invoice settled:
`expired_unfunded` also exits 0. Always read `state`, or the simpler
`paymentOutcome` and `nextAction` fields.

For a yes/no answer, use `receipt`. It exits 0 only when Coinbase itself
reports the invoice paid (v3 `CAPTURE_SUCCEEDED`), 3 while the payment is in
flight or unknown, and 1 if the order expired unpaid or needs a human:

```bash
rozo-checkout receipt <rozoPaymentId> --json | jq '.receipt | .paymentOutcome, .merchantSettlement.status'
```

Closed the terminal before paying? `resume` picks the order back up without
creating a new one:

```bash
rozo-checkout resume <rozoPaymentId>          # asks before showing the address
rozo-checkout resume <rozoPaymentId> --yes    # non-interactive
```

If the order is still unpaid and has enough time left, it prints the hosted pay
page and (after you confirm) the exact deposit instructions again. A paid order
is reported as paid (exit 0); an expired one exits 1 and says how to start
over; it refuses if this machine already recorded a send. Nothing is created or
sent.

It reports your payment, the merchant invoice and service delivery as separate
layers. Delivery is always `unknown`: Rozo cannot see your OpenRouter credits.

With `--send`, the wallet must also hold the chain's fee coin (ETH, BNB, POL or
SOL). If it does not, the CLI stops with `INSUFFICIENT_GAS` before signing and
tells you how much is missing; the order is left untouched. Paying with a native
coin spends that same coin, so the wallet needs the order amount plus the fee.
A native order is never sent after its price lock (`QUOTE_EXPIRED`).

**Retrying without paying twice.** Running `pay` again on the same link does
not create a second order while its order is open: you get the same order
back, and once money has arrived `pay` refuses with `ORDER_ALREADY_ACTIVE` or
`ORDER_ALREADY_FUNDED`. Only after an order expired with nothing received does
`pay` on the same link create a new order. The risk is paying a deposit twice, so before acting on
a link again, run `status` on its `rozoPaymentId`:

| `status` result | What to do |
| --- | --- |
| `escalate: true` (includes `underpaid`, `stuck_after_payment`; exit 1) | Do not pay again. Contact support with the link, `rozoPaymentId` and any tx hash or payment preimage. |
| `state: settled` | Done. Skip this link. |
| `state: awaiting_deposit` | Still open, but a payment you just sent may not be detected yet. First check your wallet: if a send or Lightning payment to this deposit exists or is pending, wait and poll. Only if nothing was sent, re-run the same `pay` to re-check it, then pay the deposit once. |
| `state: payin_detected`, `payin_confirmed`, `bridging`, `paying_coinbase` | Money is in flight. Wait and poll; do not pay again. |
| `state: expired_unfunded` | Nothing has arrived and this order is dead. **First check your own wallet**: if you sent anything to the old deposit, or a Lightning payment is still pending, do not pay again; contact support with the link and `rozoPaymentId` (we cannot see a pending Lightning payment). If nothing was sent, re-run the same `pay` on the same link with the same `--with`: it creates a new order. If that answers `PAYMENT_EXPIRED`, see below. |
| `state: unknown` (exit 1) | The backend could not be read. Not proof that nothing was paid: retry `status`, not `pay`. |

- Exit codes: `0` ok, `1` refused or failed (read `error.code`), `2` usage
  error (nothing was created), `3` the watch window ended before a final
  state. Exit 3 means money may still be in flight: keep polling, do not pay
  again.
- Use the same `--with` coin on every run for a link. A different coin can be
  refused with `REUSED_SOURCE_MISMATCH` or change the open order's deposit.
- `LINK_USED_OR_EXPIRED` or `LINK_NO_LONGER_PAYABLE`: the Coinbase link itself
  is already paid or expired. Check your OpenRouter balance and get a new link
  if it was not credited.
- `PAYMENT_EXPIRED`: an earlier order for this link expired. Read
  `error.details.body`: with `retryable: true` (`confirmed: false`) the old
  order cannot be proved unfunded yet, so wait a few minutes and retry the same
  `pay`; with `confirmed: true` the link has used all its re-orders, so get a
  new link from OpenRouter.
- `RATE_LIMITED`: order creation is capped per IP per hour (currently 30
  requests, and each `pay` makes two), so plan on about 15 links per hour from
  one IP. Wait for the next hour and resume with the links not yet `settled`.
  Need more? Email us. The CLI retries a 429 by itself, up to 3 times, when
  the server's `Retry-After` (or `retryAfterSeconds`) fits in 2 minutes of
  total waiting. A longer wait fails at once: read
  `error.details.retryAfterSeconds`, and `error.details.rateLimit` (limit,
  remaining, tier, scope) when the server sends it.

Questions about a batch? Email hi@rozo.ai, or reach us on
[X](https://x.com/ROZOai) or [Discord](https://discord.gg/EfWejgTbuU).

## Three rules worth knowing

- **The deposit address is one-time.** Never reuse one from an older order, a
  cached response or a screenshot.
- **Send the exact amount shown.** It is normally larger than the invoice — it
  includes the bridge and network fees.
- **Stellar deposits carry a memo, and it is `MEMO_TEXT`** — even when it looks
  like a number (`65371582` is text, not an id). Sending it as `MEMO_ID`
  produces a different memo and the payment will not be matched. The deposit
  block states the type as `receiverMemoType`.
- **Never pay a funded order twice.** If a payment has already been detected,
  stop and get a human to reconcile it; a second payment to a one-time address
  is not guaranteed to be credited.

The full list of what this refuses to do, and why, is in
[docs/safety.md](docs/safety.md).

## Links

- [Quick start](docs/QUICKSTART.md) — the five commands, with expected output
- [How it works](docs/how-it-works.md) — the flow, the endpoints, the identifiers
- [Safety design](docs/safety.md) — every rail, in detail
- [SKILL.md](SKILL.md) — agent-facing instructions · [llms.txt](llms.txt) — one-file summary
- [checkout.rozo.ai/agent](https://checkout.rozo.ai/agent.html) — the same thing on the web
- [Issues](https://github.com/RozoAI/rozo-checkout-skill/issues) — bugs and requests

## Changelog

- **0.1.17**: new `resume <rozoPaymentId>` command: re-shows the pay page and
  deposit instructions for an unpaid order (read-only, same expiry, payability
  and blacklist gates as `pay`), and answers clearly when it is already paid or
  expired. Orders now carry an anonymous `attribution.install_id` and, when
  `OPENROUTER_API_KEY` is set, a salted `attribution.account_hash`; see
  Privacy. `ROZO_CHECKOUT_ANON_ID=off` sends neither.
- **0.1.16**: new `receipt` command: one read, exit 0 only when the merchant
  side itself reports the invoice paid (Coinbase v3 `CAPTURE_SUCCEEDED`, v1 usage
  count, or the Bitrefill payout), reported as three layers
  (your payment, merchant invoice, service delivery). `status` adds
  `paymentOutcome`, `nextAction` and `sendWindow`; `nextAction.canSend` is the
  only field that permits paying. With `--send`, the wallet's fee coin (ETH,
  BNB, POL, SOL; on Base including the L1 data fee) is checked before signing:
  `INSUFFICIENT_GAS` says how much is missing and leaves the order untouched.
  Transaction hashes this tool reports are no longer masked; anything inside
  error text still is.
- **0.1.15**: corrected guidance after an order expires unpaid. First check
  your own wallet that nothing was sent to the old deposit and no Lightning
  payment is pending; if nothing was sent, re-run the same `pay` on the same
  link (the router opens a new order once it has verified the old one is
  unfunded). `PAYMENT_EXPIRED` with `retryable: true` means try again in a few
  minutes; `LINK_USED_OR_EXPIRED` or `PAYMENT_EXPIRED` with `confirmed: true`
  means get a new link from the merchant. New README section on paying many
  invoices (batch / resellers).
- **0.1.14**: optional `--email <addr>` on `pay` (and on the create-order
  scripts) stores a contact email with the order so ROZO can reach you if the
  payment needs attention. Never required; an invalid address is rejected
  before any order is created. Support channels (hi@rozo.ai, X, Discord) are
  shown at order creation and whenever an order is not clean.
- **0.1.13**: optional `--utm-source <label>` / `ROZO_CHECKOUT_UTM_SOURCE`
  adds `attribution.utm_source` to created orders so distribution channels can
  be measured. Invalid values are dropped, never failing an order.
- **0.1.12**: pay Bitrefill invoices. `pay --bitrefill-invoice <id> --to <0x…>
  --amount <USDC> --expires-at <ISO>` creates a Rozo exactOut order through
  mpprouter that delivers the exact USDC on Base straight to the Bitrefill
  invoice address, payable from Stellar USDC or any supported coin.
- **0.1.11**: each order now carries `attribution.client`
  (`rozo-checkout-skill/<version>`) so skill-created orders can be told apart
  from the web checkout. Installable as a Claude Code plugin
  (`/plugin marketplace add RozoAI/rozo-checkout-skill`). README and skill
  description rewritten around paying Coinbase invoices from the crypto you
  already hold.
- **0.1.3** — fixes found by the first real payment. The built bundles no
  longer crash with `__filename is not defined` on Node 22+ (the esbuild banner
  now shims `__filename`/`__dirname` as well as `require`, and every bundle is
  now executed by the test suite). Stellar deposits state their memo type
  (`MEMO_TEXT`, even when the memo looks numeric). Orders show remaining
  validity as a duration ("expires in 47m") in the deposit block and in
  `status`, with the exact command to make a fresh one. Reusing an existing
  unpaid order, and asking for a coin that differs from it, are both explained
  instead of reading as errors.
- **0.1.2** — Mode B no longer needs a raw private key in an environment
  variable. On Solana it uses the `~/.config/solana/id.json` that
  `solana-keygen` already wrote; on EVM an encrypted V3 keystore whose
  passphrase is prompted. `--keyfile` names either explicitly, and settings can
  come from a gitignored `.env`. Raw env keys still work for unattended
  automation. Key files and `.env` must be `chmod 600` and untracked by git.
- **0.1.1** — one spend limit instead of two: a single payment may not exceed
  $1,100 (sized for a $1,000 credit purchase plus its 5% fee), the cumulative
  session cap and the `--yes-large` override are removed. Docs make it explicit
  that paying from your own wallet needs no key or configuration.
- **0.1.0** — first release: `npx @rozoai/checkout`.

## License

MIT.

## Secret scanning

Enable the local gitleaks pre-commit hook once per clone: `brew install gitleaks pre-commit && pre-commit install` (config in `.pre-commit-config.yaml`). CI also runs a report-only scan in `.github/workflows/secret-scan.yml`.
