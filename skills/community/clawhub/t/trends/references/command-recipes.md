# Command Recipes

Use these recipes to keep user guidance safe, minimal, and aligned with the current CLI behavior.

## 1) Read-only account checks

Balance (uses current keypair when address omitted):

```bash
trends-skill-tool balance
```

Balance for explicit address:

```bash
trends-skill-tool balance 11111111111111111111111111111111
```

Holdings:

```bash
trends-skill-tool holdings 11111111111111111111111111111111 --count 20
```

Created tokens:

```bash
trends-skill-tool created 11111111111111111111111111111111 --count 20
```

Transactions:

```bash
trends-skill-tool transactions 11111111111111111111111111111111 --count 20
```

Count rules:

- `holdings --count`: integer `>= 1`
- `created --count`: integer `1..25`
- `transactions --count`: integer `1..25`

Read response completeness contract (for beginner-friendly answers):

- Always show queried wallet `address`.
- For each holdings/created row, always show token mint address (prefer `mintAddress`, then `mint_addr`, then `mint`).
- For transactions, always show transaction id/signature/hash when available.
- Do not summarize by token name/symbol only. If same symbol appears multiple times, disambiguate with mint address.
- If a field is unavailable, print `N/A` instead of omitting silently.
- Include `next_cursor` explicitly for `created` and `transactions` when present.
- Numeric scaling rule (mandatory for `holdings`, `created`, `transactions`):
  - For `holdings`/`created`, `owner_context.balance` is `decimals=6`; normalize by `/1_000_000`.
  - For `transactions`, `sol_amount` is lamports `decimals=9`; normalize by `/1_000_000_000`.
  - For `transactions`, `token_amount` is token base units `decimals=6`; normalize by `/1_000_000`.
  - Explicitly warn the user that raw API numbers are scaled.
  - Do not output raw values as final amounts without normalized value.

Suggested disclosure line:

- `Note: holdings/created owner_context.balance uses decimals=6 (/1,000,000); transactions sol_amount uses decimals=9 (/1,000,000,000); transactions token_amount uses decimals=6 (/1,000,000).`

## 2) Write confirmation gate for trades

The following operations are gated writes:

- `trends-skill-tool create`
- `trends-skill-tool buy`
- `trends-skill-tool sell`
- `trends-skill-tool reward claim`

Default behavior:

- For `create`, complete missing parameters first.
- Do preflight after parameters are fully resolved.
- Ask for explicit confirmation only after parameters are fully resolved.
- Only then provide/write execution command steps.

Bypass behavior:

- If user explicitly requests direct write (`direct write`, `不要确认`, `skip confirmation`, `直接执行`), bypass confirmation for current request unless user says session-level.
- Even under bypass, still provide preflight disclosure before write execution.
- Bypass does not skip parameter completion for missing create fields.

## 3) Quote-first trade flow (required for buy/sell)

Before any `buy` or `sell`, always quote first and explain quote summary.

Quote buy first:

```bash
trends-skill-tool quote buy <mint> --in-sol 0.1
```

Quote sell first:

```bash
trends-skill-tool quote sell <mint> --in-token 1
```

Preflight fields to echo for buy/sell:

- side (`buy` or `sell`)
- route (`--in-sol` / `--out-token` / `--in-token` / `--out-sol`)
- requested amount
- `slippage-bps` (explicit or default)
- key quote fields from `result`

Confirmation prompt example:

- `Please confirm execution. Reply with confirm / yes proceed / 确认执行 / 直接执行.`

After confirmation, execute:

```bash
trends-skill-tool buy <mint> --in-sol 0.1
```

or

```bash
trends-skill-tool sell <mint> --in-token 1
```

Mutual-exclusion rules:

- `buy`: exactly one of `--in-sol` or `--out-token`
- `sell`: exactly one of `--in-token` or `--out-sol`
- `quote buy`: exactly one of `--in-sol` or `--out-token`
- `quote sell`: exactly one of `--in-token` or `--out-sol`

## 4) Create flow with parameter completion + preflight checklist

Before `trends-skill-tool create`, complete missing parameters first. Do not jump directly to execution confirmation.

Create parameter definitions (plain language):

- `name`: token name.
- `symbol`: token symbol/ticker.
- `desc`: why this token is launched (short description).
- `image`: token icon source (`--image-path` or auto-generated from symbol).
- `url`: related X profile or X tweet link (`x.com`/`twitter.com`).
- `first-buy`: first buy amount in SOL after create.
- `dev-bps`: token deployer share / 代币部署者分成 (user share). X creator share is `10000-dev-bps` when `url` exists.

Step 1: Parameter completion (mandatory)

- Resolve every field before asking create confirmation.
- A field is resolved only when user gives a value or explicitly accepts default/empty behavior.
- Resolve checklist:
  - `name` (required)
  - `symbol` (required)
  - `desc` (value or explicit empty)
  - `image source` (`--image-path` or explicit auto-generate)
  - `url` (valid X URL or explicit none)
  - `first-buy` (value or explicit `0`)
  - `dev-bps` (if `url` exists: value or explicit default `9600`; if no `url`: explicitly mark ignored)

Follow-up question style for missing fields:

- Ask only unresolved fields.
- Keep each question explicit and choice-like, e.g.:
  - `desc is missing. Provide a short description now, or reply "empty" to leave it blank.`
  - `image is missing. Provide --image-path, or reply "auto image" to auto-generate from symbol.`
  - `url is missing. Provide an X profile/tweet URL, or reply "no url".`
  - `first-buy is missing. Provide SOL amount, or reply "0" for no initial buy.`
  - `dev-bps is missing (url present). Provide 0-10000, or reply "default" to use 9600.`

Chinese wording contract (when the assistant answers in Chinese):

- URL question must use:
  - `请输入你想指向的费用受益人X profile 或推文链接（可留空）`
- `dev-bps` label must use:
  - `代币部署者分成(dev-bps)`

Step 2: Create preflight checklist (only after Step 1 is complete)

Create Preflight Checklist (always echo):

- `name`
- `symbol`
- `url`
- `desc`
- image source (local `--image-path` or auto-generated)
- `first-buy` amount (initial buy amount at create time)
- `dev-bps` (token deployer share / 代币部署者分成)
- creator split (token deployer vs X creator)

Minimal create:

```bash
trends-skill-tool create --name "My Coin" --symbol "MYC"
```

Create with URL, description, and first buy:

```bash
trends-skill-tool create \
  --name "My Coin" \
  --symbol "MYC" \
  --url "https://x.com/example/status/1234567890" \
  --desc "my coin description" \
  --first-buy 0.01
```

Create with local image:

```bash
trends-skill-tool create --name "My Coin" --symbol "MYC" --image-path ./logo.png
```

Behavior notes:

- `--image-path` is optional. If omitted, image is generated from symbol.
- `--dev-bps` is ignored when `--url` is not provided.
- `--url` (when provided) only supports `x.com`/`twitter.com` profile or tweet (`/status/...`) links.
- Invalid/unsupported `--url` values return validation errors such as:
  - `Invalid URL format`
  - `URL only supports x.com/twitter.com tweet or profile links`
  - `URL only supports X profile or X tweet (status) links`
- `--slippage-bps` is not supported on `trends-skill-tool create`.
- `--first-buy` means initial buy amount at create time:
  - omitted or `0`: create/pool initialization runs, but no immediate buy is executed
  - greater than `0`: create and first buy are submitted atomically
- In non-JSON mode, missing `--url` with `--dev-bps` prints warning:
  - `Warning: --dev-bps is ignored when --url is not provided.`
- Creator split rules:
  - with `url`: token deployer share is `dev-bps` (default `9600` if omitted), X creator share is `10000-dev-bps`
  - without `url`: `--dev-bps` is ignored; effective split is token deployer `100%`, X creator `0%`

Step 3: Confirmation prompt:

- `Please confirm create execution. Reply with confirm / yes proceed / 确认执行 / 直接执行.`

Step 4: Execution:

- After confirmation, execute selected create command.

## 5) Reward status + claim flow (claim is gated write)

Check reward status first (uses current keypair as claimer):

```bash
trends-skill-tool reward status
```

Expected status fields:

- `claimType=coin-creator`
- `claimer`
- `rewardAccount`
- `accountExists`
- `rewardLamports`
- `rewardSol`

Claim only when `accountExists=true` and `rewardLamports>0`:

```bash
trends-skill-tool reward claim
```

Claim behavior:

- Success: includes `claimType=coin-creator`, `claimer`, and transaction info.
- Blocked: if reward account is missing or reward is `0`, command returns validation error and does not submit transaction.
- Preflight requirement before claim:
  - echo `accountExists`
  - echo `rewardLamports`
  - echo `rewardSol` (expected SOL claim amount)
  - request explicit confirmation before claim execution
- If not claimable (`accountExists=false` or `rewardLamports=0`), stop and provide retry condition.

## 6) Pagination with cursor

First page:

```bash
trends-skill-tool created <address> --count 20
```

Next page with cursor from previous response:

```bash
trends-skill-tool created <address> --count 20 --cursor <next_cursor>
```

Same for transactions:

```bash
trends-skill-tool transactions <address> --count 20 --cursor <next_cursor>
```

## 7) JSON automation mode

Use global `--json` when user needs structured parsing:

```bash
trends-skill-tool --json quote buy <mint> --in-sol 0.1
```

Success payload shape:

- `ok: true`
- `command`
- `input`
- `result`
- optional `tx`

Error payload shape:

- `ok: false`
- `command`
- `error.code`
- `error.message`
- `error.details`

## 8) Private-key safety

Never ask for, print, or echo:

- private keys
- mnemonic/seed phrases
- `secretKey` arrays
- raw keypair file contents

Never suggest commands that read key material files, including:

- `cat ~/.config/solana/id.json`

Allowed wallet verification:

- `trends-skill-tool wallet address`
