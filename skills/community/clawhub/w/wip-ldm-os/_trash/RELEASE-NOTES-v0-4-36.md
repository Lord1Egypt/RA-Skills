# Release Notes: wip-ldm-os v0.4.36

**Prettier config, .gitignore cleanup, prepublishOnly hook.**

## What changed

- Prettier config added (.prettierrc + fmt/fmt:check scripts) (#149)
- .gitignore updated: dist/, node_modules/, .claude/worktrees/, _worktrees/ (#152)
- prepublishOnly hook ensures bridge is built before npm publish

## Issues closed

- #149
- #152

## How to verify

```bash
npm run fmt:check    # verify formatting
cat .gitignore       # should include dist/
```
