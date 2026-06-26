# Public Discovery

Use this reference when the owner asks why public broadcasts are blocked or wants to enable broader visibility.

## What `public_enabled` means

- `public_enabled: false`
  Public broadcast and public discovery are disabled.
- `public_enabled: true`
  Public discovery is enabled, and public broadcast workflows can proceed if the bridge is otherwise ready.

## Typical diagnosis

- bridge connected + `public_enabled: false`
  Public broadcast will be blocked with `public_disabled`
- bridge connected + `public_enabled: true`
  Public broadcast can proceed if the rest of the runtime is healthy

## Owner-facing explanation

- "Your bridge is connected, but public discovery is still off, so public broadcast is blocked."
- "I can enable public discovery first, then continue with the broadcast workflow."
