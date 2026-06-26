---
name: solidity-audit-precheck
version: 1.0.0
description: >
  Automated pre-audit checklist for Solidity smart contracts. Runs SWC registry
  scan, OpenZeppelin pattern validation, gas optimization suggestions, and common
  vulnerability detection before sending contracts to a paid manual audit. Reduces
  audit cost and scope by catching low-hanging fruit automatically.
tags:
  - solidity
  - smart-contracts
  - security
  - ethereum
  - audit
  - defi
author: PrecisionLedger / Sam Ledger
---

# Solidity Audit Pre-Check Skill

Automated security pre-flight for Solidity contracts. Catches common vulnerabilities, validates OpenZeppelin usage, and surfaces gas inefficiencies — before you pay $20k+ for a manual audit.

## When to Use

- Before submitting contracts to a paid auditor (Trail of Bits, Certik, Spearbit, etc.)
- After writing a new contract feature or major refactor
- During internal review of a PR that touches contract code
- When onboarding a new contract codebase to understand risk surface
- Pre-deployment to mainnet or any public testnet

## When NOT to Use

- **As a replacement for a manual audit.** This is a pre-filter, not a security guarantee.
- For non-Solidity contracts (Rust/Anchor, Cairo, Stylus — use language-specific tools)
- For already-deployed and immutable contracts (nothing actionable)
- For frontend/UI code or off-chain scripts
- As a compliance certification — automated tools have known false negative rates

---

## Toolchain Setup

Install required CLI tools:

```bash
# Slither — most complete static analyzer
pip install slither-analyzer

# Mythril — symbolic execution / SMT-based analysis
pip install mythril

# Foundry (forge, cast, anvil) — for testing and gas snapshots
curl -L https://foundry.paradigm.xyz | bash && foundryup

# Solhint — linter for style and security rules
npm install -g solhint

# Aderyn — Rust-based Solidity AST analyzer (fast)
cargo install aderyn
```

Verify:
```bash
slither --version
myth version
forge --version
solhint --version
aderyn --version
```

---

## Pre-Check Workflow

### Step 1 — Inventory the Codebase

```bash
# Count contracts, identify external deps
find . -name "*.sol" | head -50
cat foundry.toml   # or hardhat.config.ts
cat remappings.txt

# Identify entry points (deployed contracts vs libraries/interfaces)
grep -r "contract " src/ --include="*.sol" | grep -v "interface\|abstract\|library"
```

Key questions:
- How many contracts? How many are deployed vs inherited?
- What OpenZeppelin version? (`lib/openzeppelin-contracts/package.json`)
- External protocols used? (Uniswap, Aave, Chainlink, etc.)
- Upgradeability pattern? (UUPS, Transparent Proxy, Beacon, none)

---

### Step 2 — Slither Static Analysis

```bash
# Full scan with all detectors
slither . --checklist --markdown-root .

# JSON output for structured review
slither . --json slither-output.json

# Print human-readable summary
slither . --print human-summary

# Filter by severity
slither . --filter-paths "lib/,node_modules/" --exclude-low
```

**Severity levels:**
| Level | Action |
|-------|--------|
| High | Block deployment — fix before audit |
| Medium | Must address — provide justification if not fixed |
| Low | Fix or document rationale |
| Informational | Style/gas — address in optimization pass |

Common high-severity detectors to watch:
- `reentrancy-eth` — reentrant Ether transfers
- `unchecked-transfer` — ERC20 transfer without return value check
- `arbitrary-send-eth` — unrestricted ETH send
- `controlled-delegatecall` — attacker-controlled delegatecall
- `suicidal` — selfdestruct reachable by anyone
- `tx-origin` — tx.origin used for auth

---

### Step 3 — Mythril Symbolic Execution

```bash
# Analyze single contract (slower, deeper)
myth analyze contracts/MyContract.sol --solc-json mythril-config.json

# With timeout for large contracts
myth analyze contracts/MyContract.sol --execution-timeout 120 --max-depth 12

# Output as JSON
myth analyze contracts/MyContract.sol -o json
```

Mythril catches:
- Integer overflow/underflow (pre-0.8.x contracts)
- Reentrancy via symbolic paths
- Delegatecall to user-supplied addresses
- Unprotected selfdestruct
- Dependence on predictable values (block.timestamp, blockhash)

---

### Step 4 — Aderyn AST Analysis

```bash
# Run from project root
aderyn .

# Output markdown report
aderyn . --output report.md

# Target specific directory
aderyn src/ --output aderyn-report.md
```

Aderyn is fast (sub-second on most codebases) and catches:
- Centralization risk (single owner controls)
- Missing events on state changes
- Unsafe ERC20 operations
- Weak access control patterns
- Incorrect inheritance order

---

### Step 5 — Solhint Linting

```bash
# Init config
solhint --init

# Lint all contracts
solhint 'contracts/**/*.sol'

# Use security ruleset
solhint --config .solhint.json 'contracts/**/*.sol'
```

Recommended `.solhint.json`:
```json
{
  "extends": "solhint:recommended",
  "rules": {
    "avoid-call-value": "error",
    "avoid-low-level-calls": "warn",
    "avoid-tx-origin": "error",
    "check-send-result": "error",
    "compiler-version": ["error", "^0.8.20"],
    "func-visibility": ["warn", {"ignoreConstructors": true}],
    "mark-callable-contracts": "error",
    "multiple-sends": "error",
    "no-complex-fallback": "error",
    "no-inline-assembly": "warn",
    "not-rely-on-block-hash": "error",
    "not-rely-on-time": "warn",
    "reentrancy": "error",
    "state-visibility": "error"
  }
}
```

---

### Step 6 — OpenZeppelin Pattern Validation

Manual checklist — verify each applies:

```bash
# Check OZ version
cat lib/openzeppelin-contracts/package.json | grep '"version"'

# Find all inherited OZ contracts
grep -r "import.*openzeppelin" contracts/ --include="*.sol"
```

**Access Control:**
- [ ] `Ownable2Step` used instead of `Ownable` (prevents accidental ownership transfer)
- [ ] `AccessControl` roles defined with `keccak256` constants, not inline strings
- [ ] `DEFAULT_ADMIN_ROLE` not held by an EOA in production (use multisig)
- [ ] `renounceRole` and `revokeRole` tested for edge cases

**Tokens (ERC20/ERC721):**
- [ ] `SafeERC20.safeTransfer` used for all external token transfers
- [ ] `_safeMint` used in ERC721 (not `_mint`)
- [ ] Callback hooks (`onERC721Received`) handled
- [ ] Reentrancy guard on any function that calls external contracts after state change

**Upgradeability:**
- [ ] Initializers called correctly (no constructor logic in upgradeable contracts)
- [ ] `_disableInitializers()` called in implementation constructor
- [ ] Storage gaps defined in all base contracts
- [ ] ERC-7201 namespaced storage used (OZ v5+)
- [ ] No storage collisions between proxy and implementation

**Pausability:**
- [ ] `Pausable` integrated with `whenNotPaused` on critical functions
- [ ] `pause()` protected by role (not public)
- [ ] Emergency unpause path defined and tested

---

### Step 7 — Gas Optimization Audit

```bash
# Forge gas snapshot baseline
forge snapshot

# Gas report per function
forge test --gas-report

# Compare before/after optimization
forge snapshot --diff .gas-snapshot
```

Common gas optimizations to flag:

| Pattern | Issue | Fix |
|---------|-------|-----|
| `uint256 i = 0` in loop | Wastes gas | `uint256 i` (zero default) |
| `storage` variable read in loop | SLOAD per iteration | Cache in `memory` first |
| `require(condition, "long string")` | String costs gas | Use custom errors |
| Multiple mappings vs struct | Extra SLOADs | Pack into struct |
| `public` on internal functions | Extra ABI overhead | `internal` or `private` |
| Unbounded loops | DoS risk + gas | Add `maxIterations` param |
| `transfer()` / `send()` | 2300 gas limit | Use `call{value: x}("")` |

Custom error pattern (saves ~50 gas per revert):
```solidity
// Bad
require(balance >= amount, "Insufficient balance");

// Good
error InsufficientBalance(uint256 balance, uint256 required);
if (balance < amount) revert InsufficientBalance(balance, amount);
```

---

### Step 8 — SWC Registry Cross-Reference

Cross-check findings against [SWC Registry](https://swcregistry.io/):

| SWC | Name | Slither Detector | Severity |
|-----|------|-----------------|----------|
| SWC-100 | Function Default Visibility | `suicidal`, `controlled-selfdestruct` | High |
| SWC-101 | Integer Overflow/Underflow | `integer-overflow` | High (pre-0.8.x) |
| SWC-104 | Unchecked Call Return Value | `unchecked-transfer` | High |
| SWC-105 | Unprotected Ether Withdrawal | `arbitrary-send-eth` | High |
| SWC-106 | Unprotected SELFDESTRUCT | `suicidal` | High |
| SWC-107 | Reentrancy | `reentrancy-eth`, `reentrancy-no-eth` | High/Med |
| SWC-111 | Use of Deprecated Functions | `deprecated-standards` | Med |
| SWC-112 | Delegate Call to Untrusted Callee | `controlled-delegatecall` | High |
| SWC-115 | Authorization via tx.origin | `tx-origin` | High |
| SWC-116 | Block values as time proxy | `weak-prng`, `block-timestamp` | Low/Med |
| SWC-120 | Weak Sources of Randomness | `weak-prng` | High |
| SWC-128 | DoS With Block Gas Limit | `costly-loop` | Med |

---

### Step 9 — Manual Review Checklist

Items automated tools miss — must be done by human:

**Business Logic:**
- [ ] Economic invariants hold (balances sum to total supply, etc.)
- [ ] State machine transitions are complete and non-overlapping
- [ ] Off-by-one errors in fee/slippage calculations
- [ ] Rounding direction favors protocol, not attacker (round down for user, up for protocol)
- [ ] Flash loan attack surface: any function callable within a single tx that can drain funds?

**Access Control Logic:**
- [ ] Every privileged function has a role check
- [ ] Role assignments tested for separation of duties
- [ ] Time locks on critical parameter changes (fee changes, oracle updates)

**Oracle / Price Feed:**
- [ ] Chainlink feeds: stale data check (`updatedAt` + heartbeat)
- [ ] Chainlink feeds: min/max circuit breakers handled
- [ ] TWAP used instead of spot price for large positions
- [ ] No single-source price oracle

**Proxy Patterns:**
- [ ] Proxy admin is a multisig, not an EOA
- [ ] Implementation cannot be initialized by attacker
- [ ] `selfdestruct` in implementation would brick proxy — is it present?

---

### Step 10 — Pre-Audit Report Template

Generate a structured handoff document for the audit team:

```markdown
# Pre-Audit Report: [Contract Name]
Date: YYYY-MM-DD
Audited by: [Team]
Commit: [git hash]

## Scope
- Contracts: [list]
- Out of scope: [list]
- Solidity version: [version]
- OZ version: [version]

## Automated Scan Results
### Slither
- High: [N] findings
- Medium: [N] findings
- [Link to slither-output.json]

### Mythril
- [N] issues found
- [Summary]

### Aderyn
- [N] issues found

## Known Issues (Won't Fix)
- [Issue]: [Rationale]

## Fixed Issues (Pre-Audit)
- [Issue]: [Fix applied, commit hash]

## Gas Baseline
- forge snapshot attached
- Estimated deployment cost: [N] ETH at [gwei] gwei

## Areas of Concern for Auditors
- [Specific complex logic to focus on]
- [External protocol integrations]
- [Novel patterns used]

## Test Coverage
forge coverage output:
[paste output]
```

---

## Example: Full Pre-Check Run

```bash
#!/bin/bash
# precheck.sh — run from project root

echo "=== Solidity Audit Pre-Check ==="
echo "Date: $(date)"
echo "Commit: $(git rev-parse --short HEAD)"

mkdir -p audit-precheck

echo "\n[1/5] Slither..."
slither . --filter-paths "lib/,node_modules/" \
  --json audit-precheck/slither.json \
  --markdown-root . 2>&1 | tee audit-precheck/slither.log

echo "\n[2/5] Aderyn..."
aderyn . --output audit-precheck/aderyn.md

echo "\n[3/5] Solhint..."
solhint 'contracts/**/*.sol' > audit-precheck/solhint.log 2>&1

echo "\n[4/5] Forge gas snapshot..."
forge snapshot --snap audit-precheck/.gas-snapshot

echo "\n[5/5] Forge coverage..."
forge coverage --report lcov > audit-precheck/coverage.log 2>&1

echo "\nPre-check complete. Results in ./audit-precheck/"
echo "Run: cat audit-precheck/slither.log | grep 'Impact\|Result'"
```

---

## Integration with Other Skills

- **develop-secure-contracts** — Use to integrate OpenZeppelin patterns that this skill validates
- **upgrade-solidity-contracts** — Pre-check upgradeable proxies before upgrade
- **ethskills** — General Ethereum dev context and deployment patterns
- **erc20-tokenomics-builder** — Pre-check token contracts built with this skill

---

## Severity Thresholds for Deployment Go/No-Go

| Severity | Count | Decision |
|----------|-------|----------|
| Critical/High | Any | **Block** — do not deploy |
| Medium | > 3 | **Block** — audit required |
| Medium | 1-3 | Mitigate or justify in writing |
| Low | Any | Document and accept or fix |
| Informational | Any | Fix in optimization pass |

A clean pre-check (zero High/Critical, documented Mediums) typically reduces manual audit time by 30-50% and audit cost by 20-40%.
