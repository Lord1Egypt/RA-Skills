---
name: splitwise
description: Manage shared expenses via the Splitwise CLI. Use when asked to log, split, or track expenses with other people, check balances, see who owes whom, settle debts, or list recent charges. Triggers on mentions of Splitwise, shared expenses, splitting costs, "log this expense," "who owes what," roommate/partner bills, or any expense-tracking request. Even casual mentions like "split this with a roommate" or "add the internet bill" should trigger this skill.
version: 1.0.1
metadata:
  openclaw:
    requires:
      bins:
        - splitwise
      config:
        - ~/.config/splitwise-cli/auth.json
        - ~/.config/splitwise-cli/config.json
    homepage: https://github.com/example/splitwise-cli
---

# Splitwise CLI Skill

Manage shared expenses, balances, and settlements through the `splitwise` CLI.

## Setup

This skill requires the `splitwise` CLI to be installed and available on `PATH`. It uses OAuth 2.0 credentials stored at `~/.config/splitwise-cli/auth.json`. If auth expires, the CLI will tell you — run `splitwise auth` to re-authenticate (requires browser OAuth flow).

If a default group is already configured locally, you can omit `--group`. Otherwise, pass `--group` explicitly.

## Quick Reference

### Check balances
```bash
# Default group balances
splitwise balances

# Specific group
splitwise balances --group "Trip"
```

### List expenses
```bash
# Recent expenses in default group
splitwise expenses list --limit 10

# Date-filtered
splitwise expenses list --after 2026-03-01 --before 2026-03-31

# Different group
splitwise expenses list --group "Trip" --limit 5
```

### Create an expense
```bash
# Even split, you paid
splitwise expenses create "Internet - March" 51.30

# Custom exact split (60/40, 70/30, any ratio)
splitwise expenses create "Utilities - March 2026" 254.80 --split "exact:MemberA:152.88,MemberB:101.92"
splitwise expenses create "Rent - April" 9300 --split "exact:MemberA:7300,MemberB:2000"

# Another member paid
splitwise expenses create "Groceries" 87.50 --paid-by "MemberB"

# Another member paid with custom split
splitwise expenses create "Dinner" 120.00 --paid-by "MemberB" --split "exact:MemberA:80,MemberB:40"

# Different group
splitwise expenses create "Dinner" 120.00 --group "Trip"

# Different currency
splitwise expenses create "Dinner on Trip" 45.00 --group "Trip" --currency EUR
```

### Other commands
```bash
splitwise me                          # Current user info
splitwise groups                      # List all groups
splitwise group "Household"           # Group details + member balances
splitwise friends                     # List friends
splitwise settle "MemberB"            # Record a settlement
splitwise expenses delete 12345       # Delete an expense by ID
```

## Output Modes

Every command supports:
- `--json` — raw JSON (for scripting or piping)
- `--quiet` — minimal output, just IDs/amounts
- `--no-color` — disable color (also respects `NO_COLOR` env var)

## Patterns for Common Tasks

### Log a recurring shared bill
Include the month in the description to avoid confusion:
```bash
splitwise expenses create "Internet - March 2026" 51.30
```

### Check before logging (avoid duplicates)
```bash
splitwise expenses list --after 2026-03-01 --limit 50 --json
```
Search the output for matching descriptions before creating.

### Batch-log multiple expenses
Run multiple `splitwise expenses create` commands in sequence. No special syntax.

## Error Handling

- **"not logged in"** → Run `splitwise auth` (needs browser for OAuth)
- **"group not found"** → Verify name with `splitwise groups`
- **"friend not found"** → Verify name with `splitwise friends`
- **Network errors** → Retry once, then report to user

## Key Details

- Group/friend names use case-insensitive partial matching
- A configured default group means `--group` is optional
- Amounts are USD by default (configurable via `splitwise config set default_currency`)
- `--split even` is the default — expense split equally among all group members
- `--split "exact:Name:Amount,Name:Amount"` — custom per-person split (amounts must sum to total)
- The `--paid-by` flag defaults to the authenticated user
