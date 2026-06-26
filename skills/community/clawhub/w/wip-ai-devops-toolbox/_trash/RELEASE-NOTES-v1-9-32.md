# Release Notes: wip-ai-devops-toolbox v1.9.32

Remove wip-install binary from toolbox. It lives in LDM OS now.

## What changed

The `wip-install` CLI binary has been removed from `@wipcomputer/universal-installer`. It now ships with `@wipcomputer/wip-ldm-os` (v0.4.1+). This prevents the EEXIST collision that blocked `npm install -g @wipcomputer/wip-ldm-os` when both packages tried to own the same binary.

## Issues closed

- Closes wipcomputer/wip-ldm-os#46

## How to verify

```bash
npm install -g @wipcomputer/wip-ldm-os@0.4.1  # no EEXIST error
which wip-install  # points to LDM OS, not toolbox
```
