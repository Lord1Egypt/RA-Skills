---
name: tock-sniper
description: Use when the user wants to run the Tock reservation sniper for a timed release or cancellation watch, locally on their Mac or on a remote node.
---

# Tock Sniper

## Quick Start

Generate one concrete `t0cksn1per` command and run it. Do not reimplement reservation logic in the skill.

Prefer:

- local plus headed when the user wants a visible browser or checkout handoff
- node plus headless when the user wants unattended polling
- CDP only when the user explicitly wants to use an existing local Chrome

## Command Source

Run with:

```bash
uvx t0cksn1per --help
```

## What To Gather

- restaurant slug
- party size
- launch time or restock mode
- exact dates or no preference
- exact times or any time
- local or node execution target
- whether CDP is requested

Then produce one command and run it.

## References

- For example commands, read `references/commands.md`
- For CDP setup, read `references/cdp.md`
