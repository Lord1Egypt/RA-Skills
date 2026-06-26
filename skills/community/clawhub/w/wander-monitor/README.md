# Wander Monitor (ClawHub)

## The problem

Coding agents and humans both waste cycles **re-checking GitHub Actions**. The fix is not “more dashboard tabs”—it is a **small, repeatable watch command** tied to `gh`, plus optional macOS notifications.

## What this folder is

This directory is the **publishable skill package** for [Wander](https://github.com/ERerGB/wander): `SKILL.md` is what ClawHub ships; the shell scripts and deep docs live one level up.

| Path | Role |
|------|------|
| `SKILL.md` | Agent instructions (published by CI) |
| [`.github/workflows/publish-clawhub.yml`](../.github/workflows/publish-clawhub.yml) | Versioned publish to ClawHub |
| Parent repo | `watch-*.sh`, `smart-push.sh`, [README](../README.md), [EDGE_CASES.md](../EDGE_CASES.md) |

## Install

**Agents (ClawHub):**

```bash
clawhub install wander-monitor
```

**Humans (tooling):** clone the main repository and follow the single quickstart in the [main README](../README.md).

## License

MIT (same as the parent repository).
