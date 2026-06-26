# Release Notes: wip-ldm-os v0.4.13

**Add `ldm catalog show` command for full component install details**

## What changed

- New `ldm catalog show <name>` command that displays full install details for any component in the catalog: npm package, repo, CLI commands, MCP servers, post-install steps.
- Also updated Memory Crystal npm references from unscoped `memory-crystal` to `@wipcomputer/memory-crystal` in spec docs.

## Why

Users running `ldm install` could see the component list but had no way to inspect a specific component's details before installing. `ldm catalog show memory-crystal` now gives the full picture.

## Issues closed

- Closes #72

## How to verify

```bash
ldm catalog show memory-crystal
ldm catalog show wip-ai-devops-toolbox
```
