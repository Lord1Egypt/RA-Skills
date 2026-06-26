# Linter Rules (.rsc)

`lint_rsc.py` performs heuristic, line-oriented static analysis of RouterOS
`.rsc` scripts. It tracks scope (guards, error handlers, loops) so that safe
patterns recommended by this skill are **not** flagged.

## Severities

| Level   | Meaning                                 | Exit code |
|---------|-----------------------------------------|-----------|
| error   | Always dangerous                        | 1         |
| warning | Should review; exit 1 only with `--strict` | 0 (1 with `--strict`) |
| info    | Nit / suggestion                        | 0         |

## Rules

### Destructive commands (error)

| Rule ID | Trigger |
|---------|---------|
| `destructive/reset-configuration` | `/system reset-configuration` |
| `destructive/routerboard-reset`   | `/system routerboard settings reset-configuration` |
| `destructive/disk-format`         | `/disk format-drive` |
| `destructive/package-downgrade`   | `/system package downgrade` |
| `destructive/wireless-reset`      | `/interface wireless reset-configuration` |

### Dangerous bulk operations (error)

| Rule ID | Trigger |
|---------|---------|
| `dangerous/unconditional-firewall-remove` | `remove [find]` without `where` on firewall menus |
| `dangerous/unconditional-user-remove`     | `/user remove [find]` without `where` |
| `dangerous/unconditional-file-remove`     | `/file remove [find]` without `where` |

Adding a `where` filter (e.g. `[find where comment="old"]`) suppresses the finding.

### Idempotency (warning)

| Rule ID | Trigger |
|---------|---------|
| `idempotency/unguarded-add` | `add` in a sensitive menu without a `:if ([:len [/... find where ...]] = 0) do={...}` guard |
| `idempotency/fixed-id` | `set <N>` or `remove <N>` using a numeric ID instead of `[find where ...]` |

Sensitive menus: `ip firewall filter/nat/mangle/raw`, `ip address`, `ip route`,
`ip pool`, `ip dhcp-server lease`, `interface list member`,
`interface bridge port`, `interface vlan`.

The `unguarded-add` warning is **suppressed** when the `add` appears inside a
matching guard scope (i.e. the `:if` block tests the same menu).

### Security (error / warning)

| Rule ID | Severity | Trigger |
|---------|----------|---------|
| `security/dont-require-permissions` | error | `dont-require-permissions=yes` on a script |
| `security/log-secret` | error | `:log` message referencing password/secret/token/apikey |
| `security/excessive-policy` | warning | `/system script add` with policies beyond `read,write,test` |

### Robustness (warning / info)

| Rule ID | Severity | Trigger |
|---------|----------|---------|
| `robustness/delay-in-loop` | warning | `:delay` inside `:while`/`:for`/`:foreach` |
| `robustness/bare-import` | info | `import` not wrapped in `:onerror` or `:do {} on-error={}` |

The `bare-import` finding is **suppressed** when the `import` is inside:
- A single-line `:do { import ... } on-error={...}`
- A multi-line `:do { ... } on-error={...}` block
- A `:onerror <var> in={...} do={...}` block

## Scope tracking

The linter maintains a scope stack with the following kinds:

- **root** — top-level code
- **guard** — inside `:if ([:len [/... find where ...]] = 0) do={...}` (tracks which menu)
- **onerror** — inside `:onerror ... in={...}` or a `:do {} on-error={}` wrapper
- **loop** — inside `:while`, `:for`, `:foreach`
- **plain** — any other `{...}` block

Braces inside double-quoted strings are excluded from scope counting.

## CLI usage

```
python scripts/lint_rsc.py [OPTIONS] FILE [FILE ...]
```

| Flag | Effect |
|------|--------|
| `--json` | Emit findings as JSON array |
| `--quiet` | Show only errors (suppress warnings and info) |
| `--strict` | Exit 1 if any warning is found |

## Exit codes

| Code | Meaning |
|------|---------|
| 0 | Clean, or only info-level findings |
| 1 | Errors found (or warnings with `--strict`) |
| 2 | Usage error or file not found |

## Limitations

- Analysis is line-oriented with lightweight scope tracking; it does not
  comprehend full control flow or router state.
- Rules are heuristics and require human review of flagged lines.
- Nested guards are tracked but only the innermost guard menu is considered
  for suppression.
