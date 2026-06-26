# web_fetch Fake-IP Workaround

Legacy workaround reference for older npm-global OpenClaw installs.

## Important

For **OpenClaw v2026.4.10 and later**, this workaround is no longer the recommended fix.
Use `openclaw.json` instead:

```json
{
  "tools": {
    "web": {
      "fetch": {
        "ssrfPolicy": {
          "allowRfc2544BenchmarkRange": true
        }
      }
    }
  }
}
```

## Use this skill only when

- You are on an older OpenClaw version that does not support the config fix
- OpenClaw was installed with `npm install -g openclaw`
- Clash, Mihomo, or Surge fake-ip is enabled
- `web_fetch` is blocked as a private/internal/special-use IP

## What it does

It inserts:

```js
policy: { allowRfc2544BenchmarkRange: true }, // openclaw-fakeip-patch
```

into the bundled `web_fetch` runtime.

## Limits

- npm global installs only
- legacy workaround for older versions
- not for source builds
- does not fix cert, proxy, or env issues
- not needed on OpenClaw v2026.4.10+

## Quick flow

```bash
bash patch-openclaw-global-fakeip.sh status
bash patch-openclaw-global-fakeip.sh inspect
bash patch-openclaw-global-fakeip.sh apply
openclaw gateway restart
```

## Undo

```bash
bash patch-openclaw-global-fakeip.sh revert
openclaw gateway restart
```

## Script source

The bundled shell script is adapted from the original repository here:

- <https://github.com/xing-xing-coder/OpenClaw-web_fetch-Fake-IP-Workaround>
