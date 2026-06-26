# Syntax Capabilities (Authoritative Authoring Reference)

Use this file before creating or modifying any `.spell` file.

## Top-Level Shape

Required form:

```spell
spell MySpell {
  on manual: {
    emit started()
  }
}
```

Supported top-level sections:

- `version`
- `description`
- `assets`
- `params`
- `limits`
- `venues`
- `state`
- `skills`
- `advisors`
- `guards`
- `import`
- `block`
- one or more `on ...: { ... }` handlers

## Section Capabilities

### `assets`

Array form:

```spell
assets: [USDC, WETH,]
```

Object form:

```spell
assets: {
  USDC: {
    chain: 8453
    address: "0x..."
    decimals: 6
  }
}
```

### `params`

Simple values:

```spell
params: {
  amount: 1000000
  enabled: true
}
```

**Amounts must be in raw token units (smallest denomination).** This applies to all venue actions — swaps, lending, bridging, etc.

| Token | Decimals | 1000 tokens as raw | Example |
|-------|----------|-------------------|---------|
| USDC | 6 | `1000000000` | `amount: 1000000000` |
| USDT | 6 | `1000000000` | `amount: 1000000000` |
| ETH/WETH | 18 | `1000000000000000000000` | `amount: 1000000000000000000000` |
| WBTC | 8 | `100000000000` | `amount: 100000000000` |
| DAI | 18 | `1000000000000000000000` | `amount: 1000000000000000000000` |

Formula: `raw_amount = human_amount × 10^decimals`

Common mistake: writing `amount: 1000` for "1000 USDC" — this is actually 0.001 USDC (1000 / 10^6). Use `amount: 1000000000` instead.

Typed/extended values:

```spell
params: {
  amount: {
    type: amount
    asset: USDC
    default: 1.5 USDC
    min: 0
    max: 1000000
  }
}
```

### `limits`

```spell
limits: {
  max_single_move: 500000
  approval_required_above: 100000
}
```

### `venues`

```spell
venues: {
  uniswap_v3: @uniswap_v3
  lending: [@aave_v3, @morpho_blue,]
}
```

### `state`

```spell
state: {
  persistent: {
    counter: 0
  }
  ephemeral: {
    temp: 0
  }
}
```

### `skills`

```spell
skills: {
  dex: {
    type: swap
    adapters: [uniswap_v3]
    default_constraints: {
      max_slippage: 50
    }
  }
}
```

### `advisors`

```spell
advisors: {
  risk: {
    model: anthropic:sonnet
    system_prompt: "Return strict JSON"
    skills: [grimoire]
    allowed_tools: [read_file]
    mcp: [docs]
    timeout: 30
    fallback: true
    rate_limit: {
      max_per_run: 10
      max_per_hour: 100
    }
  }
}
```

### `guards`

```spell
guards: {
  enough_balance: balance(USDC) > 1000 with (
    severity="halt",
    message="Insufficient balance",
  )
}
```

Guard metadata keys accepted in `with (...)`:

- `severity` (`warn | revert | halt`)
- `message`
- `fallback`

## Trigger Capabilities

Trigger form:

```spell
on <trigger>: {
  ...
}
```

Supported trigger kinds:

- `manual`
- `hourly`
- `daily`
- schedule string: `on "0 * * * *": { ... }`
- condition: `on condition <expr> every <seconds>: { ... }`
- event: `on event "EventName" where <expr>: { ... }`

## Statement Capabilities

Supported statement forms inside blocks:

- assignment: `x = expr`
- action/method call: `venue.swap(...)`
- `if / elif / else`
- `for x in expr { ... }`
- `repeat N { ... }`
- `loop until cond max N { ... }`
- `try { ... } catch ... { ... } finally { ... }`
- `parallel ... { branch: { ... } }`
- pipeline: `source | map: { ... } | ...`
- `do blockName(args)`
- `atomic { ... }`
- `atomic skip|halt|revert { ... }`
- `emit event(k=v, ...)`
- `halt "reason"`
- `wait 60`
- `pass`
- advisory assignment: `x = advise advisor: "prompt" { ... }`

## Action Routing Capabilities

Method calls on venue-like identifiers compile into action steps.

All amounts are in **raw token units** (see params section above).

Examples:

```spell
# Swap 1000 USDC (6 decimals) to WETH
uniswap_v3.swap(USDC, WETH, params.amount)

# Lend 1000 USDC to Aave
aave_v3.lend(USDC, params.amount)

# Borrow 1000 USDC with ETH collateral
aave_v3.borrow(USDC, params.amount, WETH)

# Bridge 1000 USDC to Arbitrum
across.bridge(USDC, params.amount, 42161)
```

Optional action clauses:

- `using <skill>`
- `with key=value, ...`
- multiline `with (...)`

Constraint alias normalization:

- `slippage` -> `max_slippage`
- `min_out` -> `min_output`
- `max_in` -> `max_input`

## Advisory Capabilities

Inline advisory markers (`**...**`) are unsupported for authoring.

Supported advisory form:

```spell
decision = advise risk: "Should we rebalance?" {
  context: {
    current_rate: rate
    gas: gas_cost
  }
  within: "execution"
  output: {
    type: object
    fields: {
      allow: boolean
      reason: string
    }
  }
  on_violation: reject
  clamp_constraints: [max_slippage]
  timeout: 20
  fallback: { allow: false, reason: "timeout" }
}
```

Required fields inside advise block:

- `output`
- `timeout`
- `fallback`

Advisory field semantics:

- `context`: optional object of named expressions to pass into advisory input
- `within`: optional policy scope label
- `output`: required output schema contract
- `on_violation`: optional, `reject` or `clamp` (default behavior is `reject`)
- `clamp_constraints`: required when `on_violation: clamp`
- `timeout`: required positive number
- `fallback`: required expression used if advisory resolution fails

Output schema types:

- `boolean`
- `number` (`min`, `max`)
- `enum` (`values`)
- `string` (`min_length`, `max_length`, `pattern`)
- `object` (`fields`)
- `array` (`items`)

## Expression Capabilities

Operator precedence (high to low):

1. postfix (`.`, `[]`, call)
2. unary (`not`, unary `-`)
3. multiplicative (`* / %`)
4. additive (`+ -`)
5. comparison (`< > <= >=`)
6. equality (`== !=`)
7. logical `and`
8. logical `or`
9. ternary `? :`

Expression forms:

- literals: numbers, booleans, strings, addresses
- percentages: `50%`
- unit literals: `1.5 USDC`, `25 bps`, `5m`, `1h`, `1d`
- arrays: `[a, b,]`
- objects: `{ key: value, ... }`
- identifiers
- property access and indexing
- function calls (`min`, `max`, `sum`, `avg`, `to_number`, `to_bigint`, etc.)
- query functions: `price(base, quote, source?)`, `balance(asset, address?)`, `apy(venue, asset, selector?)`, `metric(surface, venue, asset?, selector?)`

### Query Functions vs Advisory

**Always prefer query functions over advisory calls for structured data fetching.**

- `price(WBTC, USDC)` — returns a live price from the query provider (Alchemy API). Deterministic, fast, no LLM cost.
- `balance(USDC)` — returns on-chain token balance via RPC. No LLM needed.
- `balance(USDC, 0xaddr)` — balance of a specific address.
- `price(ETH, USDC, "chainlink")` — with explicit source hint.
- `apy(aave, USDC)` — venue-backed APY query for lending comparison.
- `apy(morpho, USDC, "wbtc-usdc-86")` — APY query with explicit market selector.
- `metric("quote_out", uni_v3, USDC, "asset_out=WETH,amount=1000000,fee_tier=3000")` — DEX quote comparison.
- `metric("mid_price", polymarket, USDC, "token_id=<clobTokenId>")` — offchain midpoint comparison.

Use advisory (`advise`) **only** when the task requires LLM judgment, reasoning, or interpretation — not for fetching prices, balances, APYs, or other structured metrics that query functions handle natively.

**Anti-pattern (do NOT do this):**

```spell
# BAD: Using an LLM call just to fetch a price
price_data = advise oracle: "Fetch BTC/USD price from API" { ... }
```

**Correct pattern:**

```spell
# GOOD: Direct query function
btc_price = price(WBTC, USDC)
```

Requires `--rpc-url` with an Alchemy URL for `price()`; any RPC works for `balance()`.
`apy()` and `metric()` are adapter-backed and do not require Alchemy.

## Constraint Clause Capabilities

Inline:

```spell
... with max_slippage=50, deadline=300
```

Multiline:

```spell
... with (
  max_slippage=50,
  deadline=300,
  min_output=1000,
)
```

Trailing commas are accepted.

**Commas are required** inside `with (...)` — parentheses suppress newlines, so newlines alone do not separate entries. This applies to all parenthesized contexts: `with (...)`, `emit foo(k=v, ...)`, function calls, and array literals `[...]`.

## Grammar/Formatting Behaviors

- `#` begins a comment.
- **Delimiter rule:** `{}` blocks use newlines as separators. `()` and `[]` suppress newlines, so commas are required.
- Braces `{}` are required for block structure.
- Trailing commas are accepted in list-like contexts.
- Multiline objects are supported.

## Authoring Guardrails

Before finalizing any authored spell:

1. Run `validate`.
2. Run `simulate`.
3. Confirm no unsupported syntax is used.
4. Confirm advisory blocks include required fields.
5. Confirm value-moving spells include appropriate constraints (`max_slippage` and `min_output` for swaps).
