# Release Notes: wip-ldm-os v0.4.55

Fix duplicate export that broke v0.4.54 install.

## What changed

- Removed duplicate export of detectHarnesses (was exported both inline and in the export block)
- v0.4.54 install failed with "Duplicate export of 'detectHarnesses'" for every user

## Why

v0.4.54 added detectHarnesses() with `export function` at line 90 AND listed it again in the `export {}` block at the bottom. Node.js rejects duplicate exports.

## Issues closed

- #212

## How to verify

```bash
npm install -g @wipcomputer/wip-ldm-os@latest
ldm install    # should not error
```
