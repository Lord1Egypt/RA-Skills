---
name: web-fetch-fakeip
description: Legacy workaround for web_fetch fake-ip failures on older npm-global OpenClaw installs. Use when web_fetch is blocked under Clash, Mihomo, or Surge fake-ip mode and the OpenClaw version does not yet support the openclaw.json ssrfPolicy fix. For OpenClaw v2026.4.10 and later, prefer configuration instead of patching.
---

# web_fetch Fake-IP Workaround

Apply a small, reversible patch so `web_fetch` works under TUN + fake-ip environments that resolve through `198.18.0.0/15`.

## Best fit

Use this skill when:

- OpenClaw was installed with `npm install -g openclaw`
- You use Clash, Mihomo, or Surge with fake-ip enabled
- `web_fetch` fails with private/internal/special-use IP blocking
- Your OpenClaw version is older than `v2026.4.10`
- You need a legacy workaround because the config-based fix is unavailable

## Not for

- OpenClaw `v2026.4.10` or later, use `openclaw.json` instead
- Source-built OpenClaw
- Certificate problems
- Proxy rule or port mistakes
- Missing proxy environment variables

## What changes

The script finds the bundled `web_fetch` call to `fetchWithWebToolsNetworkGuard({...})` and inserts:

```js
policy: { allowRfc2544BenchmarkRange: true }, // openclaw-fakeip-patch
```

This only opens the RFC2544 benchmark range used by common fake-ip setups.

## Workflow

```bash
bash patch-openclaw-global-fakeip.sh status
bash patch-openclaw-global-fakeip.sh inspect
bash patch-openclaw-global-fakeip.sh apply
openclaw gateway restart
```

Then retry the failing `web_fetch` request.

## Revert

```bash
bash patch-openclaw-global-fakeip.sh revert
openclaw gateway restart
```

## Notes

- Safe to run repeatedly
- Creates backup files on apply/revert
- After OpenClaw upgrades, rerun if needed
- On `v2026.4.10+`, prefer the built-in config fix instead of this patch

## Resources

- `scripts/patch-openclaw-global-fakeip.sh`
- `references/README.md`
