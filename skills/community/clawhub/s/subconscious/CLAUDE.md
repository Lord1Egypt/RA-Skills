# Subconscious System — Claude Code Guide

## System Purpose

This is a self-improving agent skill for OpenClaw. It provides a persistent, bounded bias layer that shapes agent behavior over time without modifying core identity.

## Key Constraints

- **Never touch `core/` items** — they are immutable by design
- **All mutations must be typed** — use `MutationType` enum, never raw field edits
- **Check governance before mutations** — `check_mutation_allowed()` exists for a reason
- **Deduplicate before queuing** — `is_duplicate()` checks ID + text similarity before `queue_pending()`
- **Reinforce once per tick** — track state to prevent double-reinforcing the same item in one tick
- **Promotion needs `--enable-promotion`** — rotate does NOT promote by default

## Working with the Metabolism

```bash
# Verify system health first
python3 subconscious_metabolism.py status

# Never run rotate without --enable-promotion unless you explicitly want NO promotion
python3 subconscious_metabolism.py rotate

# Force promotion cycle
python3 subconscious_metabolism.py rotate --enable-promotion

# Manual tick
python3 subconscious_metabolism.py tick
```

## Testing Changes

After any code change:
```bash
python3 subconscious_metabolism.py verify   # integration checks
python3 subconscious_metabolism.py status    # should show healthy
python3 subconscious_cli.py bias            # should show biases
```

## Common Issues

- **Pending queue grows unbounded**: Check if `scan_and_promote_eligible` is running with `--enable-promotion`
- **Item stuck in pending**: Check `confidence`, `reinforcement.count`, `freshness` vs thresholds
- **Duplicates in live**: Check `promote_pending_to_live` has ID dedup before append
- **Bias empty**: Check `fetch_relevant()` returns items and `build_bias()` formats correctly

## Path Configuration

Memory store is at: `~/.openclaw/workspace-alfred/memory/subconscious/`

Override with: `export SUBCONSCIOUS_WORKSPACE=/path/to/workspace`
