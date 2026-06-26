# Changelog Analysis Patterns for Silent Breaking Changes

This document contains patterns and keywords to aid in the semantic analysis of application release notes. The goal is to identify changes that, while not explicitly labeled "breaking," have a high potential to alter default behavior, invalidate existing configurations, or disrupt runtime workflows.

## Analysis Goals

Identify two categories of risks:
1. **Configuration-level**: Changes affecting `openclaw.json` or static config
2. **Runtime-level**: Changes affecting behavior without config modifications

---

## High-Risk Keywords (Architecture)

These words often signal deep architectural changes where unintended side effects are common.

- `refactor`
- `rework`
- `unify`
- `centralize`
- `modernize`
- `improve handling of`
- `streamline`
- `overhaul`

**Impact**: Can affect both config and runtime behavior. Analyze feature area carefully.

---

## Config-Level Keywords

### Schema & Validation
- `schema updated`
- `validation logic`
- `require explicit`
- `fail closed`
- `enforce strict`

**What to check**: Does our config rely on permissive validation or implicit defaults?

### Defaults & Behavior
- `new default`
- `behavior changed`
- `now falls back to`
- `default to`
- `previously` (e.g., "previously allowed")

**What to check**: Do we rely on the old default behavior?

### Deprecation & Migration
- `deprecate`
- `legacy`
- `migrated to`
- `no longer supports`
- `will be removed in`
- `renamed to`

**What to check**: Do we use deprecated fields or features?

### Security Policy
- `policy` (e.g., "add new ... policy")
- `hardening`
- `restrict`
- `block`
- `sanitize`

**What to check**: Will our current setup be blocked or require new permissions?

---

## Runtime-Level Keywords

### Behavioral Logic
- `fix` (especially "fix duplicate", "fix race", "fix timing")
- `prevent`
- `avoid`
- `no longer`
- `instead of`

**What to check**: Does this fix change behavior we rely on (even if buggy)?

### Routing & Delivery
- `route`
- `deliver`
- `suppress`
- `dedupe`
- `inherit`
- `fallback`

**What to check**: Will messages/routes go to unexpected destinations?

### Session & State
- `session`
- `reset`
- `clear`
- `preserve`
- `archive`
- `cleanup`

**What to check**: Will session state be lost or handled differently?

### Streaming & Protocol
- `streaming`
- `compat`
- `force`
- `normalize`
- `parse`

**What to check**: Will streaming responses or API calls break?

### Performance & Caching
- `lazy`
- `cache`
- `optimize`
- `reduce`
- `batch`

**What to check**: Will caching/lazy loading cause staleness or delays?

### CLI/UX
- `/new`, `/reset`, `/status` (command names)
- `TUI`
- `interactive`
- `prompt`
- `output format`

**What to check**: Will user workflows or muscle memory break?

---

## Pattern Combinations

Some keyword combinations indicate higher risk:

### High-Risk Combinations
- `refactor` + `routing` → Session routing may break
- `fix` + `duplicate` → Reply suppression may affect legitimate messages
- `unify` + `auth` → Authentication logic may change
- `streamline` + `validation` → Stricter config validation

### Medium-Risk Combinations
- `improve` + `performance` → Caching may cause staleness
- `add` + `policy` → New restrictions may apply
- `prevent` + `race` → Timing-dependent workflows may break

---

## Analysis Process

### Step 1: Scan for Keywords
Scan changelog for keywords listed above. Don't limit to "BREAKING" labels.

### Step 2: Categorize by Type
For each match, determine if it's:
- **Config-level**: Affects `openclaw.json` or config loading
- **Runtime-level**: Affects behavior without config changes

### Step 3: Identify Feature Area
Map each change to a feature area:
- `gateway`, `auth`, `config`
- `channels`, `telegram`, `discord`
- `agents`, `sessions`, `memory`
- `models`, `providers`
- `tools`, `browser`, `media`
- `cron`, `hooks`, `plugins`
- `cli`, `tui`, `ui`

### Step 4: Cross-Reference with Environment

**For config-level risks**:
- Load `openclaw.json`
- Ask: "Does our config rely on an implicit behavior in this area?"
- Identify specific config paths (jq notation) affected

**For runtime-level risks**:
- Identify active workflows:
  - Do we use TUI regularly?
  - Do we rely on cron jobs?
  - Do we use custom model providers?
  - Do we have complex session routing?
- Ask: "Does our workflow rely on the old behavior?"

### Step 5: Formulate Scenarios
For each high/medium-risk change, formulate a "what-if" scenario:

**Config scenario template**:
> "What if `{CHANGE}` means our config at `{PATH}` with value `{VALUE}` is now invalid/rejected/ignored? → `{CONSEQUENCE}`"

**Runtime scenario template**:
> "What if `{CHANGE}` means our workflow `{WORKFLOW}` now behaves differently (`OLD` → `NEW`)? → `{CONSEQUENCE}`"

---

## Examples

### Example 1: Config-Level Risk
**Changelog**: "Gateway auth now requires explicit `gateway.auth.mode`"

**Analysis**:
- Keywords: `requires explicit` (config-level)
- Feature area: `gateway`, `auth`
- Our config: `gateway.auth.token` set, but no `gateway.auth.mode`
- Scenario: "What if 'requires explicit mode' means our config with both token and password but no mode is rejected?" → Gateway fails to start
- Risk: High (P0)

### Example 2: Runtime-Level Risk
**Changelog**: "fix: suppress duplicate replies in DM scope=main"

**Analysis**:
- Keywords: `fix`, `suppress`, `duplicate` (runtime-level)
- Feature area: `routing`, `delivery`
- Our workflow: DMs go to main session, expect replies
- Scenario: "What if 'suppress duplicate' means legitimate follow-up messages are dropped?" → Bot stops replying in DM
- Risk: Medium (P2)

### Example 3: CLI/UX Risk
**Changelog**: "TUI: `/new` creates independent session instead of resetting shared session"

**Analysis**:
- Keywords: `/new` (runtime-level, CLI/UX)
- Feature area: `tui`, `session`
- Our workflow: Use `/new` to clear conversation
- Scenario: "What if '/new creates independent session' means our muscle memory of '/new = clear' now creates new sessions instead?" → Workflow disrupted
- Risk: Medium (P2)

---

## Quick Reference: Risk Indicators

| Keyword Pattern | Config Risk | Runtime Risk | Feature Areas |
|----------------|-------------|--------------|---------------|
| `refactor` | ⚠️ | ⚠️ | Any |
| `unify` + `auth` | 🔴 | 🟡 | gateway, auth |
| `fix` + `duplicate` | 🟢 | 🟡 | routing, delivery |
| `/command` | 🟢 | 🔴 | cli, tui |
| `streaming` + `compat` | 🟢 | 🟡 | models, providers |
| `require explicit` | 🔴 | 🟢 | config, validation |
| `deprecate` | 🔴 | 🟡 | Any |
| `policy` + `add` | 🟡 | 🟡 | security |

Legend: 🔴 High risk, 🟡 Medium risk, 🟢 Low risk (context-dependent)

---

## Notes

- **Context matters**: A keyword like `fix` can be low-risk if it's for an obscure feature, but high-risk if it affects core functionality (routing, auth).
- **Cumulative effects**: Multiple small changes in the same area can combine to create significant behavioral shifts.
- **Documentation gaps**: Changelogs often under-document behavioral changes. Look at commit messages or PRs if available.
- **Test with real workflows**: The best way to catch runtime risks is to test actual user workflows post-upgrade.
