# Release Notes: wip-ldm-os v0.4.56

Remove ghost directory names. Fix tavily catalog. Stop creating ldm-install- prefixed directories.

## What changed

- Tmp clone directories no longer use `ldm-install-` prefix (was `~/.ldm/tmp/ldm-install-<name>`, now `~/.ldm/tmp/<name>`)
- This was the root cause of ghost directories leaking into `~/.ldm/extensions/`
- Tavily added to catalog with repo `wipcomputer/openclaw-tavily` so it can update automatically
- Ghost migration code remains to clean up existing installs

## Why

Extensions installed via `ldm install` got directory names like `ldm-install-wip-xai-grok` because the tmp clone path leaked into the extension path. This caused a permanent "update available" loop: the registry had the clean name but pointed to the ghost directory, so the update checker always saw a version mismatch.

## Issues closed

- #212

## How to verify

```bash
npm install -g @wipcomputer/wip-ldm-os@latest
ldm install
ls ~/.ldm/extensions/ | grep ldm-install   # should be empty
ldm status                                  # grok and tavily should not show as needing update
```
