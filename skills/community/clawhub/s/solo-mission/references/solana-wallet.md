# SoloMission Platform — Solana Wallet (Paid Missions)

Paid missions escrow into the `solo_escrow` Anchor program on Solana. The Sponsor is a Solana
keypair that signs `create_task` (funding), and later `cancel_task` / `emergency_refund` /
`claim_refund`. All of them must be signed by the **same address**.

The backend builds every one of these transactions; the sponsor verifies and signs it. Three things
follow from that, and each one has tripped someone up:

1. **You need SOL as well as USDC.** SOL pays transaction fees and *rent*, a deposit for the
   accounts your mission creates.
2. **You do not build the transaction, you sign it.** So you must **verify what you are signing**,
   because a headless agent has no wallet UI to decode it for you.
3. **There is no CLI command that signs a transaction someone else built.** Signing happens in the
   solo-mission-mcp server (in-process), or in your own code with a Solana SDK.

---

## What you need, by path

| | MCP path (recommended) | Raw REST path |
|---|---|---|
| Keypair file | yes, created by the operator | yes, created by the operator |
| Signing | `fund_solana_mission` / `refund_solana_mission`, in-process | your own code, using a Solana SDK (for example `@solana/web3.js`) |
| Verification before signing | done by the tool, cannot be skipped | **your responsibility**, see *Why verification is not optional* |
| Program id and RPC to check against | pinned in the server for devnet; `SOLO_SOLANA_PROGRAM_ID` + `SOLO_SOLANA_RPC_URL` for any other cluster (see *Pinned program and RPC*) | yours to pin, the same way |
| Solana CLI | **not needed** | optional: address, token-account and balance lookups, decoding a transaction for inspection, independent escrow checks |

The Solana CLI (`solana`, `solana-keygen`, `spl-token`) is needed in exactly two places:

- the **operator**, once, to create the keypair file (`solana-keygen`), unless they already have
  a tool that writes the same 64-byte JSON format;
- the **raw REST path**, for the read-only lookups listed below.

The agent never installs it. Before using it, check:

```bash
for BIN in solana solana-keygen spl-token; do
  command -v "$BIN" > /dev/null 2>&1 || { echo "MISSING: $BIN"; MISSING=1; }
done
[ -z "${MISSING:-}" ] && solana --version && spl-token --version
```

If anything is missing, tell the operator: *"The Solana CLI isn't installed. Please install it
yourself following Anza's official instructions at https://docs.anza.xyz/cli/install, then
restart this session."* Then stop. Do not download or run an installer yourself.

---

## What the money is actually for

Read this before deciding an amount. The rent line is the one that surprises people.

| Item | SOL | ≈USD | Comes back? |
|---|---|---|---|
| Task account rent | 0.00374 | $0.374 | partly — $0.139 on `close_task` |
| TaskVault token account | 0.00204 | $0.204 | **in full** on `close_task` |
| `create_task` + confirm fees | 0.00004 | $0.004 | no |
| **Locked during the mission** | 0.00582 | **$0.58** | |
| **Permanent cost per mission** | 0.00239 | **$0.24** | no — kept on purpose |

**Rent is a refundable deposit, not a fee.** The lamports sit in accounts you control and come back
when they close. The ~$0.24 that does not return buys the on-chain record that makes your escrow and
your frozen participant list checkable by anyone, forever. On a $10 mission that is 2.4%; on a
$1,000 mission, 0.024%.

Budget **0.02 SOL per concurrent mission** and you will not think about it again.

---

## Creating the keypair (operator action — not the agent)

> Do this on a machine the operator trusts, in the operator's own terminal. The agent never
> generates, reads, prints or holds the key.

```bash
# Writes the keypair as a JSON byte array. It prompts for an optional BIP39 passphrase.
solana-keygen new --outfile ~/.config/solana/solo-sponsor.json
chmod 600 ~/.config/solana/solo-sponsor.json

# The public address to fund (prints the public key only)
solana address -k ~/.config/solana/solo-sponsor.json
```

Fund that address with SOL and with the payout token. On devnet:

```bash
solana airdrop 1 <ADDRESS> --url devnet
```

> The devnet faucet is aggressively IP-rate-limited and will often refuse outright. If it does, use
> https://faucet.solana.com (GitHub login) rather than retrying in a loop.

The payout token is decided by the platform, not by you: call `get_solana_config` (or
`GET /agent/solana/config`) to see which mints are whitelisted on the current cluster. On devnet the
platform funds new missions in **`USDC`** (Circle's devnet USDC), not the `TEST_USDC` mint also
listed there, which exists for the platform's own automated funding. Get devnet USDC from
https://faucet.circle.com (select **Solana Devnet**); `solana airdrop` only dispenses SOL.

The server needs Node.js 22.23.4+, 24.22.1+ or 26.12.1+. It exits with an upgrade message on older
Node, which trusts certificate authorities that were compromised in October 2026.

Then point the solo-mission-mcp server at the file by path, in the environment the server runs in:

```bash
export SOLO_SOLANA_KEYPAIR_PATH=~/.config/solana/solo-sponsor.json
```

Only the path goes into the environment, never the key material: the server does not accept the
key itself in an environment variable. The file is still plaintext:
`chmod 600` keeps other users on the machine out, but whoever gets that one file (a compromised
account, a stray backup, a copied disk image) gets the key. Fine for a devnet test; for a wallet
holding anything real, encrypt it.

### Encrypting the keypair at rest (recommended)

Split the secret across two files that are each useless alone: a ciphertext and a passphrase file.
Generate the passphrase straight into its file so it never appears on screen, in a command line
or in shell history:

```bash
( umask 077; openssl rand -base64 32 > "$HOME/.config/solana/solo-sponsor.pass" )

openssl enc -aes-256-cbc -pbkdf2 -iter 10000 -md sha256 -salt \
  -in  "$HOME/.config/solana/solo-sponsor.json" \
  -out "$HOME/.config/solana/solo-sponsor.json.enc" \
  -pass "file:$HOME/.config/solana/solo-sponsor.pass"
chmod 600 "$HOME/.config/solana/solo-sponsor.json.enc"

# Delete the plaintext: the encrypted file + passphrase file are the only copies from here on
shred -u "$HOME/.config/solana/solo-sponsor.json"    # or `rm` if shred isn't available
```

Point the MCP server at the encrypted pair instead:

```bash
export SOLO_SOLANA_KEYPAIR_ENCRYPTED_PATH=~/.config/solana/solo-sponsor.json.enc
export SOLO_SOLANA_KEYPAIR_PASSWORD_FILE=~/.config/solana/solo-sponsor.pass
```

`-iter 10000 -md sha256` is not optional decoration: the MCP server decrypts this itself (it does
not shell out to `openssl`) and derives the key using exactly those parameters.

**Never store the passphrase file on the same backup or snapshot as the `.enc` file it unlocks.**
An attacker needs both; keeping them apart is what makes that true in practice.

### Keeping the key in a secret manager

Better still, keep the keyfile (or the passphrase) in the secret manager the operator already
uses, and have that tool write the file when the MCP server starts, so it isn't left on disk
between runs. Examples: 1Password (`op inject`, `op read --out-file`), a HashiCorp Vault Agent
template, GCP Secret Manager (`gcloud secrets versions access`), or the macOS Keychain
(`security find-generic-password -w`). The server reads the key only from a file, through a path
(`SOLO_SOLANA_KEYPAIR_PATH`, or the encrypted pair). Whatever the tool, the key and the
passphrase never go into chat, a command-line argument or shell history.

**The key stays on your machine.** It is never sent to the Solo API. The backend builds
transactions and submits them, but only the sponsor can authorise one, which is why a compromised
backend cannot move your funds.

### Pinned program and RPC

The same backend that builds the transaction also answers `GET /agent/solana/config`, so the
server doesn't take the escrow program, or the RPC endpoint it checks against, from there:

- **The escrow program id is pinned in the server**, per cluster. Today that is devnet only:
  `2CPC5V63FDs7SdWu89iSYYsTEpqBwuQeYuA9ASzuSo8a`. If the API reports a different `program_id`,
  funding and refunds are refused before anything is signed.
- **Reads that decide what to sign** (the mint's decimals, the escrow Config account) go to
  `SOLO_SOLANA_RPC_URL`, or the pinned cluster's public endpoint (`https://api.devnet.solana.com`),
  never the API's `rpc_url`.
- **A cluster the server doesn't pin** (a future mainnet, a localnet) is refused until the
  operator sets both, in the environment the server runs in:

  ```bash
  export SOLO_SOLANA_PROGRAM_ID=<the escrow program id you trust>
  export SOLO_SOLANA_RPC_URL=<an RPC endpoint you trust for that cluster>
  ```

On devnet neither is needed. `SOLO_SOLANA_RPC_URL` alone is useful if the public devnet endpoint
rate-limits you. Neither is a secret. `SOLO_SOLANA_PROGRAM_ID` replaces the built-in pin on every
cluster, so set it only to a program id the operator has verified independently, never to a value
taken from the API.

---

## Check you can actually pay before you create anything

```
get_solana_wallet
```

```json
{
  "configured": true,
  "address": "SNWf…7X1Z",
  "sol": 1.5,
  "token_account": "…",
  "token_account_exists": true,
  "token_balance": "5000",
  "can_pay_fees": true
}
```

Two fields worth understanding:

- **`token_account_exists: false`** means you hold no balance of that mint yet. An SPL token account
  is created when tokens first arrive, and `create_task` reads yours, so funding fails without one.
  The on-chain error names the *account*, not the missing balance.
- **`sol: 0`** produces `Attempt to debit an account but found no record of a prior credit`. That
  message never mentions SOL. If you see it, this is why.

---

## Deadlines the escrow accepts

`create_mission` turns your two durations into the escrow's two deadlines:

```
qualify_deadline    = creation time    + hiring_duration_hours   (hiring closes)
settlement_deadline = qualify_deadline + work_duration_hours     (last moment to settle)
```

The escrow program checks both when the funding transaction lands, and refuses to create the
task unless:

| Rule | In durations |
|---|---|
| `settlement_deadline ≥ qualify_deadline + min_review_window + finalize grace` | `work_duration_hours` at least `min_review_window` + finalize grace |
| `qualify_deadline` at most 180 days ahead | `hiring_duration_hours ≤ 4320` |
| `settlement_deadline` at most 90 days after `qualify_deadline` | `work_duration_hours ≤ 2160` |
| `qualify_deadline` still in the future | fund while hiring is open |

`min_review_window` is the program's setting (the mission records it as
`solana_min_review_window`), and the finalize grace is fixed per build. On the current devnet
build both are 10 s, so `create_mission`'s own floor of 60 s per duration is what binds there. On
a production build both are at least 1 hour, so the work window must be at least 2 hours.
`create_mission` applies the same rules and returns 400 naming `hiring_duration_hours` or
`work_duration_hours`, so a mission it accepts can be funded while hiring is open.

The grace exists because finalizing must happen at least `min_review_window` before
`settlement_deadline`: it is the room to finalize after hiring closes. Practical consequences:

- **Size the work window for the work, not for the minimum.** Submissions close
  `max(60 s, min_review_window)` + 20 minutes before `settlement_deadline`, but never before
  hiring closes: about 21 minutes before on devnet today, about 80 on a production build. On a
  production build a 2-hour work window leaves participants 40 minutes.
- **Keep `settlement_deadline` no later than you would wait for your money.** The fallback when
  anything goes wrong is `emergency_refund`, and that opens only after `settlement_deadline`.

---

## Funding a mission

```
create_mission        { chain: "solana", budget: 10, max_humans: 2, base_reward: 5, … }
fund_solana_mission   { mission_id: "…", expected_budget: 10 }
```

`fund_solana_mission` does four things in one call: asks the backend to build the transaction,
**decodes and verifies it**, signs it locally, and submits it through `confirm-funding`.

What the transaction carries since the escrow upgrade of 2026-09-30 (`GET /agent/solana/config`
reports `escrow_interface: "v2"`):

- **A fee cap.** Besides the mission's parameters, `create_task` carries `max_fee_bps`, the fee
  rate you were quoted at `create_mission` (the mission's `solana_quoted_fee_bps`). If the
  program's fee has risen above it by the time the transaction lands, it fails with
  `FeeAboveSponsorMax` and nothing moves, instead of charging you more.
- **For a lottery, the platform Operator's signature.** The program creates a lottery task only
  if the Operator co-signs, because the platform holds the seed it must reveal to draw. So a
  lottery's transaction arrives already signed by the Operator, and you add only your own
  signature. **Do not change it**: rebuilding it, swapping the blockhash or touching any byte
  invalidates the Operator's signature, and `confirm-funding` accepts only the exact message the
  backend co-signed (anything else is 409). A non-lottery transaction has you as its only signer.

Over REST, a paid `create_mission` with no `chain` defaults to `"solana"`; sending it explicitly
is still clearer.

Changed your mind before funding? `cancel_mission` cancels a `pending_funding` mission with
nothing escrowed, and an unfunded mission is cancelled automatically 24 hours after creation
(`funding_params.expires_at`). A `media_review` mission can't be funded until a track is ready:
funding returns 409 before anything is signed.

### Why verification is not optional

The backend builds the transaction and hands you base64. That keeps the instruction layout out of
your integration, but it hands you bytes you cannot read by eye. A human signing in a wallet app
gets that decoded for them. **You have no wallet UI.**

So `fund_solana_mission` decodes the transaction and checks it. It checks against values it
gets from somewhere other than the funding response, because comparing the API's answer to itself
proves nothing:

| Expected value | Where the tool gets it |
|---|---|
| Budget | `expected_budget`, which you pass as **what you intended**, scaled by the mint's decimals as read from the mint account on chain. The API's `decimals` is ignored |
| Mint | `expected_mint` if you pass it, otherwise what `create_mission` recorded for the mission (`token_address`, returned as `funding_params.mint`) |
| Lottery or not, prize, both deadlines, `seed_commit` | The mission record (`GET /agent/missions/:id`), i.e. what `create_mission` recorded |
| Base pool | Not checked against an expectation: only the response's `declared` value against the bytes (the backend derives it from `base_reward × max_humans`) |
| Fee ceiling (`max_fee_bps`) | In order: the `expected_max_fee_bps` argument; else the mission's `solana_quoted_fee_bps`; else, only for a mission with no recorded quote, the program's on-chain `Config.fee_bps` |
| Program id | The server's pin, or `SOLO_SOLANA_PROGRAM_ID` (see *Pinned program and RPC*) |
| Operator | `operator` in the program's Config account (PDA `["config"]`, bytes 40–72), read from chain over the trusted RPC, with its owner and discriminator checked |
| Sponsor, token account | Your wallet, and its associated token account for the mint |

It refuses **before anything is built** if the deployment doesn't report
`escrow_interface: "v2"` (there is no v1 path), if the API's `program_id` isn't the pinned one,
if the cluster has no pin and no `SOLO_SOLANA_PROGRAM_ID` / `SOLO_SOLANA_RPC_URL`, or if the
mint's decimals can't be read from chain.

It then **refuses to sign**, and returns the discrepancies, if:

- the transaction is not a legacy transaction with **exactly one instruction** (an appended
  transfer would be authorised by your signature too)
- that instruction isn't `create_task` on the pinned program with the v2 layout: 86 bytes of data,
  ending in `max_fee_bps` (the 84-byte v1 layout is refused)
- any of its 12 accounts is not the one expected in its position. The tool derives the Config,
  whitelist, task, vault and event-authority addresses itself from the pinned program id,
  `task_id` and mint, so a vault that isn't the task's program-derived address (one **someone
  holds the private key to**) is refused. The response's own `accounts` block must agree
- the vault equals your own token account, i.e. the budget never actually leaves your control
- you are not the fee payer, or not a writable signer
- any field differs from the expected value above, or `max_fee_bps` isn't exactly the quote (or
  there is no quote to check it against)
- **non-lottery:** anyone else signs, or the Operator slot holds anything but the program id
  (Anchor's "none")
- **lottery:** the Config account can't be read; the co-signer isn't its `operator`, or is you;
  the signers aren't exactly you (first, as fee payer) and the Operator; the Operator's signature
  is missing or doesn't verify over the exact message bytes you received; or the response's
  `message_sha256` isn't that message's hash
- the parameters the backend *described* (`declared`) disagree with the bytes it *built*

That last one is the strongest check. Everything else compares the backend's description against
your expectations, and a dishonest backend controls that description. Comparing the description
against the instruction data catches a backend that quotes correct numbers and encodes different
ones.

When it signs, it writes only your 64-byte signature into your slot of the bytes it received, and
checks that the message and every other signature (the Operator's included) are unchanged.

It also warns, without refusing, when the transaction would fail on chain anyway: the program is
paused, or its fee has already risen above `max_fee_bps`. In the second case, cancel the mission
with `cancel_mission` and create a new one to get a fresh quote.

Use `dry_run: true` to see exactly what would be signed without signing or paying anything.

If verification fails: **do not retry blindly.** Nothing was escrowed and no fee was paid. The
discrepancy is either a bug worth reporting or an attempt to have you authorise something else.

If it verified and signed but `confirm-funding` then failed, the result has `funded: false`,
`signed: true`, the backend's `message` and, when the escrow program rejected the transaction,
`program_error` naming it with what to do (e.g. `FeeAboveSponsorMax`, `LotteryRequiresOperator`,
`SettlementWindowTooShort`).

### Lottery and non-lottery both work

```
create_mission { chain: "solana", budget: 20, max_humans: 10,
                 base_reward: 1, lottery_winner_count: 2, lottery_prize_per_winner: 5 }
```

`budget` must cover `base_reward × max_humans + lottery_prize_per_winner × lottery_winner_count`
plus `floor(budget × fee_bps / 10000)`, where `fee_bps` is the escrow program's fee rate (currently
`0` on devnet). Headroom beyond that is optional; unused budget comes back through `claim_refund`.

### Where a lottery's randomness comes from

If you are asked to justify a draw, this is the whole mechanism. A draw happens only when more
participants qualify than there are prizes. Otherwise every qualified participant wins, and the
program consumes no randomness at all: nothing to verify, nothing to wait for.

1. **Finalize commits a slot.** `finalize_qualification` stores `entropy_round`, the slot after
   the one it lands in. The qualified set is frozen before that slot exists.
2. **That slot's bank hash is the entropy.** The draw uses the SlotHashes sysvar entry for the
   smallest *produced* slot ≥ `entropy_round` (if the leader skips the slot, the next produced one
   counts). That entry is a **bank hash**. It is **not** the blockhash `getBlock` returns, which is
   a different value: a draw recomputed from `getBlock` gets the wrong answer.
3. **Someone records it within about 512 slots.** SlotHashes keeps only the last 512 slots, about
   3.4 minutes. `record_entropy` copies the entry onto the Task as `entropy_slot` and
   `entropy_hash`. Anyone may call it: it moves no value and works even while the program is
   paused. The platform calls it right after finalizing, and a keeper retries every minute;
   `settle_task` also records it if nobody has yet. **If nobody records it in time, the draw can
   never happen.** Settle fails with `EntropyExpired`, and the mission can only end with
   `emergency_refund` after `settlement_deadline`: you get the whole budget back, and participants
   are not paid. There is deliberately no way to commit a new slot, because a re-roll would let
   the Operator, who knows the seed, discard outcomes it dislikes.
4. **Settle mixes in the seed.** `final_entropy = keccak256(seed_reveal ‖ entropy_hash)`, where
   `seed_reveal` is the secret whose hash (`seed_commit`) was fixed when you funded. The program
   checks the seed against that commitment, stores `final_entropy` on the Task and emits it in
   `TaskSettled`.

**What that does and does not guarantee.** The platform cannot supply or pick the entropy, and
cannot change a draw once finalize has committed the slot, since the seed was fixed before. But
this is **not a VRF**, and the draw is not unbiased randomness. The leader of the entropy slot
sees its bank hash first, shapes it through the block it produces, and can skip the slot to move
the draw to the next one. The leader schedule is public, so an Operator colluding with a
validator can time finalize so that the entropy slot is that validator's, and together they can
bias the draw. The Operator alone can refuse to settle a draw it dislikes (you then get the budget
back through `emergency_refund`), but cannot change the outcome.

#### Recomputing a draw from public data

| Input | Where to read it |
|---|---|
| `seed_reveal` | The settle transaction: bytes 8–40 of the `settle_task` instruction data (its first argument). `keccak256(seed_reveal)` must equal the mission's `seed_commit` |
| `entropy_slot`, `entropy_hash`, `final_entropy` | The Task account, PDA `["task", task_id as u64 little-endian]` under `program_id`. Offsets include the 8-byte discriminator: `final_entropy` 275–307, `entropy_slot` 377–385, `entropy_hash` 385–417. The same values are in the settle transaction's `TaskSettled` event |
| `actual_winner_count` | `TaskSettled`, or `min(qualified_count, lottery_winner_count)` |

Once a finished task is archived (`close_task` shrinks the account to 278 bytes), only
`final_entropy` stays on it, at bytes 149–181. Take `entropy_slot` and `entropy_hash` from
`TaskSettled` (or from the `EntropyRecorded` event of the `record_entropy` transaction). Both are
Anchor CPI events: an inner instruction to the escrow program whose data is the 8-byte tag
`e445a52e51cb9a1d`, an 8-byte event discriminator, then the fields, little-endian.
`TaskSettled`'s fields are `task_id`, `payout`, `refundable`, `fee` (u64 each),
`actual_winner_count` (u32), `final_entropy` (32 bytes), `entropy_slot` (u64), `entropy_hash`
(32 bytes) and `settled_at` (i64).

Then:

1. **`final_entropy = keccak256(seed_reveal ‖ entropy_hash)`.** This is Keccak-256, the Ethereum
   variant (not NIST SHA3-256), over the 64 concatenated bytes. It must equal the stored
   `final_entropy`.
2. **Winners.** Take the qualified participants' payout addresses as raw 32-byte keys, drop
   duplicates, and sort them by those bytes. Score each as `keccak256(final_entropy ‖ address)`.
   The `actual_winner_count` lowest scores win; a tie goes to the address that sorts first.

The Task records the qualified set only as a hash (`qualified_root`), not the addresses, so step
2 needs the list itself. Step 1 needs nothing but the chain.

Worked example, devnet task 1037 (settled 2026-09-30, 3 qualified, 1 prize):
`entropy_round` = `entropy_slot` = 505769953, recorded 4 slots later;
`seed_reveal` = `000c31a533b8b26f4c60d65cdf4581a556417b4a37dc3915e5b3a2e7e7f3f6bb`;
`entropy_hash` = `7709ccdcf50197c48917adb38656e4e59322f212a6a03c3147a00b2213fcabad`;
`final_entropy` = `febd4776afe8c9d06605e5cb1dbf4ca3b7df5f5d831ce4838daa5f616582ef5c`.
`getBlock` for that slot returns blockhash `eb548734…`, which is not `entropy_hash` and does not
reproduce the draw.

Draws settled before the 2026-09-30 upgrade read `entropy_slot = 0`: the old program accepted the
randomness as an argument from the Operator, which is what the upgrade removed, so this recipe
does not apply to them.

### The task id race

The funding response includes a `task_id`. It is valid only while the program's internal counter has
not moved: if another mission is funded in between, your transaction fails on a seeds constraint.
That is the safe direction, since a stale id cannot fund the wrong task. Request a fresh transaction
and sign again. For a lottery the backend co-signs each fresh transaction, and if a co-signed one
for this mission already landed, `funding-transaction` returns 409 with that `task_id`: confirm
it through `confirm-funding` instead of funding again.

Blockhashes also expire in **60–90 seconds**. If signing takes longer, request a fresh transaction
rather than submitting a stale one.

---

## Raw REST path

Use this only if you cannot run the solo-mission-mcp server. The routes:

```
GET  /agent/solana/config                          program_id, cluster, rpc_url, mints, decimals, escrow_interface
POST /agent/solana/missions/:id/funding-transaction { sponsor_wallet, sponsor_token_account }
POST /agent/solana/missions/:id/confirm-funding     { signed_transaction, task_id }
POST /agent/solana/missions/:id/refund-transaction  { action, sponsor_wallet, sponsor_token_account }
POST /agent/solana/missions/:id/confirm-refund      { signed_transaction, action }
```

Read-only lookups with the Solana CLI (check it is installed first, see *What you need, by path*).
None of these read or print key material:

```bash
CFG=$(curl -s https://api.mission.projectsolo.ai/agent/solana/config)
MINT=$(echo "$CFG" | jq -r '.mints.USDC')

# Don't take the program or the RPC endpoint from the API you are checking: pin them, as the
# MCP server does (devnet values; see "Pinned program and RPC").
PROGRAM_ID="${SOLO_SOLANA_PROGRAM_ID:-2CPC5V63FDs7SdWu89iSYYsTEpqBwuQeYuA9ASzuSo8a}"
RPC="${SOLO_SOLANA_RPC_URL:-https://api.devnet.solana.com}"
[ "$(echo "$CFG" | jq -r '.program_id')" = "$PROGRAM_ID" ] || echo "STOP: the API reports another escrow program"
[ "$(echo "$CFG" | jq -r '.escrow_interface')" = "v2" ] || echo "STOP: not the v2 escrow interface"

# The mint's decimals, from the mint account rather than the API
spl-token display "$MINT" --url "$RPC"

# Sponsor address (public key only) from the operator's keypair file path
SPONSOR=$(solana address -k "$SOLO_SOLANA_KEYPAIR_PATH")

# The sponsor's associated token account for the payout mint
TOKEN_ACCOUNT=$(spl-token address --token "$MINT" --owner "$SPONSOR" --verbose --output json \
  | jq -r '.associatedTokenAddress')

# Balances
solana balance "$SPONSOR" --url "$RPC"
spl-token balance --address "$TOKEN_ACCOUNT" --url "$RPC"

# Human-readable decode of a transaction the backend built, for inspection before signing
solana decode-transaction "$TX_BASE64" base64
```

For a refund, use the mission's own mint (`token_address` from `GET /agent/missions/:id`), not a
default: a mission is funded in exactly one mint, and the wrong token account makes the transaction
fail on chain.

**Signing** a backend-built transaction needs a Solana SDK in your own code; the CLI cannot do it.
Before signing, apply every check from *Why verification is not optional* to the decoded
transaction. For refunds, also check that the one instruction's data is exactly the 8-byte
discriminator (none of the three refund instructions takes arguments) and that your token account
is the destination. Load the keypair from its file inside that code; never pass key bytes through
the environment, argv or a shell variable.

Add your signature without rebuilding the transaction. That matters for a lottery, whose
transaction already carries the Operator's signature: in `@solana/web3.js`, deserialize it with
`Transaction.from` and call `partialSign`, not `sign`, which discards existing signatures. Then
check that the serialized message is byte-identical to the one you received and verified, and that
the Operator's signature is unchanged. The MCP server goes one step further and writes only your
64-byte signature slot into the bytes it received.

---

## Verifying escrow independently

You should not have to trust the Solo API that your money is locked. The funding response's
`accounts` object names the Task account (`task`) and the vault (`vault`), and you can read both
from any RPC node:

```bash
# Raw Task account
solana account <TASK_PDA> --url "$RPC"

# The vault's actual token balance — this is the escrow
spl-token balance --address <VAULT_PDA> --url "$RPC"
```

The vault is a program-derived address whose authority is the task itself, so **no key can move
it**, not yours and not the platform's. That is the guarantee, and it is checkable rather than
promised.

---

## Getting the money back

Three routes, and which one is legal depends on the mission's state. **`refund_solana_mission` with
no `action` tells you which** rather than making you guess:

```
refund_solana_mission { mission_id: "…" }
→ { available_actions: ["emergency_refund"], why_not_claim_refund: "…" }
```

| Action | Legal when | Returns | Mission becomes |
|---|---|---|---|
| `cancel` | funded, not finalized, and strictly before `qualify_deadline` (hiring close). The program itself enforces the cut-off | the whole budget | `cancelled` |
| `emergency_refund` | funded or qualified, and `settlement_deadline` has passed. Works even while the program is paused | the whole budget | `cancelled` |
| `claim_refund` | the mission settled `refundable` | the unspent remainder | `refunded` |

These all need an escrow. A mission still `pending_funding` with nothing escrowed is cancelled with
`cancel_mission` instead; if that returns 409 with a `task_id`, an escrow exists and `cancel` here
applies.

Then run it for real:

```
refund_solana_mission { mission_id: "…", action: "emergency_refund" }
```

Same shape as funding: the backend builds, the tool **verifies and signs locally**, the backend
submits and then reads the vault balance. Success returns `onchain_status: "cancelled"` or
`"refunded"` and `vault_remaining_raw: "0"`. Use `dry_run: true` to see what would be signed
without moving anything.

A refund moves the *entire* escrow. The tool uses the mission's own mint (`token_address`), and
refuses to sign unless the transaction targets the pinned escrow program (see *Pinned program and
RPC*), contains exactly one instruction, has you as the only signer, includes your token account
for that mint as the destination, and carries exactly the 8-byte discriminator (none of the three
refund instructions takes arguments, in v1 or v2).

When a refund doesn't happen, the result says who refused it in `rejected_by`, and carries
`qualify_deadline`, `settlement_deadline`, `cancel_cutoff` and a `what_to_do`:

| `rejected_by` | Meaning |
|---|---|
| `"client"` | The tool itself, before building anything: a `cancel` once `qualify_deadline` has passed by this machine's clock |
| `"backend"` | The platform refused: `refund-transaction` answered 409 with `available_actions`, or `confirm-refund` failed without an on-chain program error |
| `"chain"` | The escrow program rejected the signed transaction. `program_error` names it, with its code and what to do: e.g. `TooLateToCancel` (6125) for a cancel that landed after `qualify_deadline`, `TooEarlyForEmergencyRefund` (6016) |

A verification failure is different: `refused_to_sign: true` with `problems`, and nothing was
signed.

Over REST, `refund-transaction` with an action that isn't legal right now returns 409 with
`available_actions`, which is how you ask the same question without the MCP.

> **If nothing is available yet, that is the program's rule, not a bug.** Once `qualify_deadline`
> passes, `cancel` is gone: participants may already have done the work, and since the 2026-09-30
> upgrade the program itself refuses a later cancel (`TooLateToCancel`), so a cancel built just
> before the deadline that lands after it fails, and `confirm-refund` returns 409.
> `emergency_refund` only opens once `settlement_deadline` passes. A mission mid-flight has no
> refund route by design.

### Two missions that end in a refund, not a payout

- **Nobody was hired.** `cancel` is gone once hiring closes, even with no participants. Either
  finalize with an empty qualified list and settle now (zero payout; the mission becomes
  `refundable`, and `claim_refund` returns the budget less the platform fee, which is `0` on devnet
  today), or wait for `settlement_deadline` and `emergency_refund` the whole budget. The platform
  does neither for you: its reconciler auto-finalizes only when someone is hired (it hires any
  applicant still waiting first) and, for `media_review`, only when someone finished. Finalize
  must still run at least `max(60 s, min_review_window)` before `settlement_deadline`.
- **A lottery's entropy expired.** `settle_mission` returns 409 `entropy_expired`: nobody recorded
  the slot's entry in time (see *Where a lottery's randomness comes from*), and the draw can never
  happen. Stop retrying settle. After `settlement_deadline`, `emergency_refund` returns the whole
  budget; the participants are not paid.

### Rent is separate from the budget

A refund returns the USDC. The ~$0.24 of permanent per-mission rent is not part of it, and the
recoverable ~$0.20 comes back through `close_task`, which is permissionless and batched by the
backend. You do not need to call it.

## After funding

`hire_participant`, `finalize_qualification` and `settle_mission` need nothing from your wallet:
the platform signs those, not you. The same goes for `record_entropy`, which the platform submits
right after finalizing a lottery that needs a draw.

The one participant-facing detail worth knowing: a participant funds their own token account
(~$0.21, refundable) at their **first** collection, and needs no SOL before that. So a participant
can bind a wallet, apply, be hired, do the work and see their rewards with an empty wallet. What
they cannot do with zero SOL is take delivery.
