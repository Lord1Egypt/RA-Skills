# Release Notes: wip-ldm-os v0.4.60

**Fix tavily catalog npm name collision. Guard bug doc.**

## The story

The catalog had `"npm": "tavily"` for the openclaw-tavily plugin, but `tavily` on npm is a third-party package (Tavily SDK by transitive-bullshit). Every `ldm install` saw a version mismatch (local v1.0.0 vs npm v1.0.2), cloned the repo, rebuilt the plugin, and deployed the same v1.0.0 that was already there. This added minutes to every install.

Fixed the catalog to `"npm": "@wipcomputer/openclaw-tavily"`. Also added the guard bugfix doc to `ai/product/bugs/`.

## Issues closed

- #232 (tavily catalog fix, guard bug doc)

## How to verify

```bash
ldm install --dry-run
# tavily should NOT show as needing an update
```
