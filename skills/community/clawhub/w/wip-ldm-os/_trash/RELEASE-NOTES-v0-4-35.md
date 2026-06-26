# Release Notes: wip-ldm-os v0.4.35

**Repo review quick fixes: hardcoded path, engines field, safer fs ops, debug logger, CI pipeline.**

## What changed

1. **Fix hardcoded /Users/lesa path (#144).** `src/bridge/core.ts` now uses `os.homedir()` instead of a hardcoded fallback. Breaks for any non-lesa user were possible.

2. **Add engines field (#151).** `package.json` now declares `node >= 18`. Users get a clear error on older Node instead of cryptic ESM failures.

3. **Replace shell rm -rf with fs.rmSync (#150).** Two locations in `lib/deploy.mjs` used `execSync('rm -rf ...')`. Now uses Node's built-in `rmSync` (no shell injection surface, cross-platform).

4. **Add debug logger (#148).** New `lib/log.mjs` with `LDM_DEBUG=1` opt-in. Foundation for replacing 29 silent `catch {}` blocks across the codebase.

5. **Add GitHub Actions CI (#146).** `.github/workflows/ci.yml` runs build + test on push and PR. Expands as test coverage grows.

## Issues closed

- #144
- #146
- #148
- #150
- #151

## How to verify

```bash
# Debug mode:
LDM_DEBUG=1 ldm install --dry-run

# Engines check:
node -e "console.log(JSON.parse(require('fs').readFileSync('package.json','utf8')).engines)"
```
