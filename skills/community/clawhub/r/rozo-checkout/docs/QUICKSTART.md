# Quick start

**English** | [简体中文](QUICKSTART.zh.md) | [日本語](QUICKSTART.ja.md) | [Español](QUICKSTART.es.md)

Pay an OpenRouter Coinbase Payment Link with USDT/USDC on Solana, BNB Chain,
Ethereum, Polygon, Arbitrum, Base or Stellar, with BTC over Lightning, or with a
native coin (ETH on Ethereum, Base or Arbitrum, BNB, SOL, POL). Five minutes.
For how it works and why, see [README.md](../README.md).

## The one-liner

```bash
npx @rozoai/checkout pay https://payments.coinbase.com/payment-links/pl_01YOURLINKID
```

That runs every step below for you: pick a coin, quote, create, review,
confirm, deposit instructions, then polling until settlement. At the coin
prompt you can paste your wallet address and the picker will check your
balances and mark which coins you can afford — optional, and it never changes
what gets signed.

If you already know your coin, name it and skip the question:

```bash
npx @rozoai/checkout pay https://payments.coinbase.com/payment-links/pl_01YOURLINKID --with usdt-solana
```

Coins for `--with`: `usdt-solana`, `usdc-solana`, `usdt-bnb`, `usdc-bnb`,
`usdt-ethereum`, `usdc-ethereum`, `usdt-polygon`, `usdc-polygon`,
`usdt-arbitrum`, `usdc-arbitrum`, `usdc-base`, `usdc-stellar`, `btc-lightning`,
and the native coins `eth-ethereum`, `eth-base`, `eth-arbitrum`, `bnb-bnb`,
`sol-solana`, `pol-polygon`. Scripts and agents must pass `--with`: the picker
only appears on a terminal, and there is no default coin.

A native coin is offered only when the invoice's quote lists it, for invoices up
to $3,500 (native ETH on Ethereum: $1 minimum). It is exact-out: send exactly
the coin amount shown, before its price lock ends (about an hour; the OpenRouter
link itself stays payable about 24 hours), and keep a
little of the same coin for gas. On-chain BTC and Tron are not supported.
ZEC on Zcash (Beta): use https://checkout.rozo.ai/zec, this CLI does not create ZEC orders.

By default it just prints an address for you to pay from any wallet — no key
and no configuration needed. Add `--send` only if you want the CLI to sign
from a hot wallet instead, and `--json` for machine-readable output.

The rest of this page is the same flow run one step at a time, which is what
you want if something goes wrong or you are scripting it yourself.

## Before you start

- **Node 18 or newer** (`node -v`). Nothing else to install — `npx` fetches the
  CLI, and the cloned `scripts/dist/*.js` are self-contained bundles.
- **A wallet** holding the coin you want to pay with, on the chain you pick.
- **The Coinbase link**, e.g.
  `https://payments.coinbase.com/payment-links/pl_01YOURLINKID`.
- No account and no API key. Every endpoint here is public.

Set it once:

```bash
LINK="https://payments.coinbase.com/payment-links/pl_01YOURLINKID"
```

Chain ids: `1` Ethereum · `56` BNB Chain · `137` Polygon · `8453` Base ·
`42161` Arbitrum · `900` Solana · `1500` Stellar · `lightning` Bitcoin Lightning.

## Which wallet do I need?

**One wallet, on one chain — not one per chain.** Pick whichever coin you
already hold and pay from wherever it already lives.

Any wallet works, and so does an exchange withdrawal: Mode A below just prints
a deposit block, and you send exactly that `amount` of that `tokenSymbol`, on
that `chain`, to that `receiverAddress`. Nothing connects to a site and nothing
is approved in a browser. In practice people use MetaMask or Rabby on the EVM
chains, Phantom or Solflare on Solana, and a Lightning wallet such as Phoenix
or Wallet of Satoshi for BTC.

Two cases differ. **Stellar** routes through a shared address plus
`receiverMemo`, so whatever you send from must let you set a memo — omit it and
the payment is lost. **Lightning** pays the BOLT11 invoice in
`deposit.lnInvoice`; there is no address to send to.

Only `--send` (Mode B) needs a private key, from `ROZO_CHECKOUT_EVM_KEY` or
`ROZO_CHECKOUT_SOL_KEY`, and it covers EVM chains and Solana only.

## 1. Quote it (read-only, free)

```bash
node scripts/dist/quote.js --url "$LINK"
```

```json
{
  "success": true,
  "merchant": "OpenRouter, Inc.",
  "invoice": { "amount": "1050.00", "fiat": { "amount": "1050.00", "currency": "USD" } },
  "serviceFee": "10.5",
  "feeBps": 100,
  "callerPays": "1060.5",
  "coinbaseExpiryIso": "2026-08-09T10:00:00.000Z"
}
```

`"success": false` with `LINK_NO_LONGER_PAYABLE` means the link is used or
expired — ask for a fresh one and stop.

## 2. Create the order

```bash
node scripts/dist/create-order.js --url "$LINK" --chain 900 --token USDT
```

No money moves, and an unfunded order simply expires. The order lasts about an
hour, while the OpenRouter link stays payable about 24 hours after it was
created (`coinbaseExpiryIso`), so an expired order can be replaced on the same
link. The full deposit address
is **withheld** at this stage — you get a masked summary to check first.

```json
{
  "success": true,
  "rozoPaymentId": "11111111-2222-4333-8444-555555555555",
  "invoice": { "amount": "1050.000000", "currency": "USD" },
  "serviceFee": "10.5",
  "feeBps": 100,
  "callerPays": "1060.5",
  "deposit": null,
  "depositWithheld": true,
  "display": {
    "chain": "Solana",
    "amount": "1064.910000 USDT",
    "payToMasked": "9WzDXw...AWWM"
  },
  "expiry": { "effectiveDeadlineIso": "2026-08-08T11:00:00.000Z", "minutesOfSlack": 55 }
}
```

This example is the flagship case: a **$1,050.00** invoice for $1,000 of
OpenRouter credits. Any invoice up to **$1,100** can be paid this way.

**Check `display.amount` before going on.** It is normally larger than the
invoice — it includes the bridge and network fees. Note the `rozoPaymentId`;
every later command uses it.

## 3. Confirm

Only once you have decided to pay, re-run the same command with `--confirm`:

```bash
node scripts/dist/create-order.js --url "$LINK" --chain 900 --token USDT --confirm
```

This releases the full deposit details and records the confirmation the send
scripts require.

```json
{
  "success": true,
  "confirmed": true,
  "deposit": {
    "chain": "Solana",
    "tokenSymbol": "USDT",
    "receiverAddress": "9WzDXwBbmkg8ZTbNMqUxvQRAyrZzDsGYdLVL9zYtAWWM",
    "receiverMemo": "rozo-901",
    "amount": "1054.410000",
    "payTo": "9WzDXwBbmkg8ZTbNMqUxvQRAyrZzDsGYdLVL9zYtAWWM"
  }
}
```

Send exactly the fields this block gives you. On Stellar the memo is
**`MEMO_TEXT`** even when it looks numeric — sending it as `MEMO_ID` will not
match. `deposit.expiresIn` tells you how long the order stays valid. For
Lightning,
`deposit.lnInvoice` holds the BOLT11 string to scan, and `deposit.amount` is
in satoshis.

## 4. Pay

### The simple way: from your own wallet

**No key, no environment variable, no configuration.** Open any wallet, and
send exactly what the `deposit` block above says:

- the `amount` of the `tokenSymbol`,
- on the `chain`,
- to the `receiverAddress` — copied from the JSON, never retyped.

If the block contains any other field, such as `receiverMemo`, include it
exactly as given; it is part of the address for that chain. For Lightning,
scan or paste `deposit.lnInvoice` instead.

That is the whole of Mode A. Skip to step 5.

### The optional way: let the script pay (Mode B)

Only if you want this machine to sign for you, and only on **EVM chains and
Solana** — there is no `--send` for Stellar or Lightning, which are paid from
your own wallet. This is the only part that needs a key.

**Solana — use the keypair you already have.** If you have ever run
`solana-keygen`, `~/.config/solana/id.json` already exists and is used
automatically:

```bash
node scripts/dist/send-sol.js --rozo-payment-id <rozoPaymentId> --send
```

**EVM — use an encrypted keystore.** Export a V3 JSON keystore from your
wallet and point at it. The passphrase is prompted; it is never a flag:

```bash
ROZO_CHECKOUT_EVM_KEYSTORE=~/wallets/hot.json \
  node scripts/dist/send-evm.js --rozo-payment-id <rozoPaymentId> --send
```

Either file can also be given explicitly with `--keyfile <path>`, and
`--dry-run` works with every source: it derives the address and runs all the
checks without signing anything.

**For unattended automation**, where nobody can type a passphrase, a raw key in
the environment still works exactly as before — `ROZO_CHECKOUT_SOL_KEY` or
`ROZO_CHECKOUT_EVM_KEY`, or `ROZO_CHECKOUT_KEYSTORE_PASSPHRASE` alongside a
keystore. On a machine a person uses, prefer a key file.

These settings can also live in a `.env` in the directory you run from (or
`--env-file <path>`). Only `ROZO_CHECKOUT_*` keys are read from it, it is
parsed as plain text and never run through a shell, and anything already in
your real environment wins. **Add `.env` to your `.gitignore`.**

A key file or `.env` must not be readable by other users (`chmod 600`) and must
not be tracked by git. Both are refused rather than warned about.

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

# Optional RPC overrides, one per chain id. 8453 = Base, 900 = Solana.
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


A single payment may not exceed **$1,100**; above that, pay from your own
wallet as above.

```json
{
  "success": true,
  "submitted": true,
  "confirmed": true,
  "txHash": "3Bxs4h24hBjHziQ8UJqSjqjbjWQq2sQ3yV9Fq4HrVh5c"
}
```

## 5. Watch it settle

```bash
node scripts/dist/status.js --rozo-payment-id <rozoPaymentId> --watch --timeout 600
```

```json
{
  "success": true,
  "state": "settled",
  "terminal": true,
  "payin": { "txHash": "3Bxs4h24...", "confirmedAt": "2026-08-08T10:05:00.000Z" }
}
```

States run `awaiting_deposit` → `payin_detected` → `payin_confirmed` →
`bridging` → `paying_coinbase` → `settled`. Your on-chain transaction
confirming is not the end: keep polling until `settled`.

## If something goes wrong

Read `error.code`. The three you are most likely to hit:

| `error.code` | What happened | What to do |
|---|---|---|
| `LINK_NO_LONGER_PAYABLE` | someone already paid the link, or it expired | ask the merchant for a fresh link; do not pay anything |
| `EXPIRY_MARGIN` | too little time left to fund, bridge and settle safely | do not fund this order; let it expire, then re-run from step 1 on the same link (a new order is created once the old one is proved unfunded). If that answers `LINK_USED_OR_EXPIRED` or `PAYMENT_EXPIRED` with `confirmed: true`, ask the merchant for a fresh link |
| `ALREADY_SENT` | a send is already recorded for this order | do **not** send again; run `status.js` and check the chain first |

**If any money has already left your wallet, never pay again.** Keep the
`linkId`, the `rozoPaymentId` and every transaction hash, and get a human to
reconcile it. A second payment to a one-time deposit address is not guaranteed
to be credited.

The full error table is in [README.md](../README.md), and the agent-facing
instructions are in [SKILL.md](../SKILL.md).
