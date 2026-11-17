# Safety design

[← back to the README](../README.md) · [Quick start](QUICKSTART.md) · [How it works](how-it-works.md)

The interesting part of this project is what it refuses to do. The README keeps
the three rules a payer needs; everything below is the full list, for anyone
reviewing or extending the code.

- **Two-phase confirmation, enforced.** `create-order.js` withholds the full
  deposit address, memo and BOLT11 until it is re-run with `--confirm`, which
  records a confirmation bound to a sha256 of those exact instructions. The
  send scripts refuse without both `--send` and a confirmation whose digest
  still matches the live data, so neither an accidental invocation nor a
  swapped deposit address can move funds.
- **Full invoice plus a stated fee, nothing else.** `discount` must be `"0"`
  (else `NO_DISCOUNT_VIOLATION`), and `callerPays` must equal the invoice amount
  plus the service fee the router states in `serviceFee` and `feeBps`. The fee
  must come with its rate, be at most 100 bps, equal the fee that rate produces
  (rounded up to a whole cent) and be the same in the quote and the created
  order; anything else aborts with `PRICING_VIOLATION` or `CREATE_DRIFT`.
  Security-critical fields (`linkId`, `merchant`, `original`, `callerPays`, the
  echoed source) must be present as well as equal — a missing field is drift.
- **Reuse guard.** Creating an order for a link that already has an unexpired
  order returns that existing order — even if it has already been funded. So on
  every run the live order is required to be unpaid (`payment_unpaid`, no tx
  hash, no amount received, no confirmation) and to match the chain and token
  the caller chose. Otherwise: `ORDER_ALREADY_FUNDED` or
  `REUSED_SOURCE_MISMATCH`.
- **Money-detected rule, fail closed.** Once any pay-in exists, the tooling
  never reports a plain failure, never advises paying again, and never retries
  into a new order. An `amountReceived` that is non-null but unreadable counts
  as money, not as absence of money. An unreadable backend reports `unknown`,
  never `awaiting_deposit`.
- **Complete deposit instructions.** A zero, negative or unparsable amount
  aborts. Lightning requires the BOLT11 (which arrives in `source.lnInvoice`
  with an empty address). A Stellar deposit is a shared hub address plus a
  per-order memo, so the memo is part of the destination: an order that
  arrives without one is a hard abort, never rendered as "no memo required".
- **Expiry margins.** Payment is refused unless the earlier of the order expiry
  and the Coinbase expiry is more than a per-chain margin away (10 min EVM and
  Stellar, 5 min Solana). Lightning additionally requires at least 10 minutes
  of BOLT11 validity. A missing or unparsable deadline aborts.
- **Payability revalidation.** A quote receipt makes order creation skip the
  live Coinbase check, and the link can be consumed by someone else at any
  moment — so payability is re-checked immediately before the deposit address
  is shown, and again as the very last step before broadcast, after all the RPC
  preparation. Incomplete Coinbase state is treated as "cannot prove payable",
  not as payable.
- **Compromised-address list, fail closed.** `scripts/src/lib/blacklist.json`
  carries a vendored list with a provenance header and a sha256 over the
  addresses. The digest proves only that this vendored copy has not been edited
  since its sync date; it is not a signature by the upstream source. Both the
  deposit address and the sending wallet are checked. If the file is missing,
  malformed, empty, or its digest does not match, every send is refused rather
  than proceeding unchecked.
- **Send-once, across processes.** Order state lives in
  `$HOME/.rozo-checkout/state/<uuid>.json`, written atomically (temp file,
  fsync, rename). Every read-modify-write of a state file — the claim, the
  spend caps, the order record and the confirmation — runs inside one exclusive
  lockfile, so two concurrent invocations can neither both decide they are
  first, nor overwrite each other's send record. A send is claimed *before* broadcasting, so an ambiguous RPC error can
  never become a second transfer. Transactions are signed before broadcast so
  the hash is known in advance; on an ambiguous result the scripts look that
  exact transaction up instead of rebroadcasting.
- **Hot-wallet controls.** A signing key is read from a local key file (a
  solana-keygen keypair, or an encrypted V3 keystore whose passphrase is
  prompted) or from the environment for unattended runs. A key file that is
  readable by other users, or tracked by git, is refused — as is a `.env`
  carrying the same settings, which is parsed as plain text and never
  evaluated by a shell. Keys and passphrases
  are never accepted on the command line, and are never printed; library and RPC errors are redacted
  before display, including credential-bearing provider URLs, bearer tokens and
  key-shaped strings. The scripts refuse to run when any `.env`/`.env.*` in the
  working directory is git-tracked, and refuse just as hard when git cannot
  prove it is untracked. The RPC's chain id (or Solana genesis hash) and the token's
  on-chain decimals are verified before signing. One limit applies: a single
  payment may not exceed $1,100. There is no override flag and no cumulative
  session cap — a larger invoice is paid from your own wallet, which needs no
  key and has no limit.
- **Address masking.** Prose shows `first6...last4`. The full deposit address,
  memo and BOLT11 string appear only inside the machine-readable `deposit`
  object, so they stay copy-pastable without being scattered through logs.
