# QR Code Pairing for Relay Key Sharing

**Date:** 2026-02-27
**Author:** cc-mini
**Status:** Spec (ready for review)
**Priority:** High (Grok flagged key sharing UX as top critique)

## Problem

Right now, sharing the Relay encryption key between devices requires:
1. Run `openssl rand -base64 32 > ~/.openclaw/secrets/crystal-relay-key`
2. Manually copy the file to every other device (AirDrop, 1Password, USB, etc.)

This works for Parker. It does not work for anyone else. Grok called it out: "For normies or big teams it'll feel clunky until you add something like QR codes or secure enclave flow."

## Solution

`crystal pair` ... a QR code pairing flow that transfers the encryption key between devices without touching a server.

## User Experience

### Device A (has the key, or generates one)

```bash
$ crystal pair

  No relay key found. Generating one...
  Key saved to ~/.openclaw/secrets/crystal-relay-key

  Scan this QR code from your other device:

  ██████████████████████████████
  ██████████████████████████████
  ██  ██  ████  ██    ██  ██  █
  ██████████████████████████████
  ...

  Waiting for scan... (expires in 5 minutes)
  Press Ctrl+C to cancel.
```

If a key already exists:
```bash
$ crystal pair

  Relay key found.
  Scan this QR code from your other device:

  [QR code]

  Waiting for scan... (expires in 5 minutes)
```

### Device B (receiving the key)

```bash
$ crystal pair --scan

  Point your camera at the QR code...
  (or paste the pairing code manually)

  > mc1:AaBbCc...XxYyZz

  Key received and saved to ~/.openclaw/secrets/crystal-relay-key
  Relay encryption is now active on this device.
```

### Alternative: no camera (SSH, headless, remote)

The QR code encodes a pairing string. The user can also just copy-paste it:

```bash
$ crystal pair
  ...
  Or copy this pairing code:
  mc1:T2hJbGxPZkRhcmtuZXNzTXlPbGRGcmllbmQ=

$ crystal pair --code mc1:T2hJbGxPZkRhcmtuZXNzTXlPbGRGcmllbmQ=
  Key received and saved.
```

## Technical Design

### What the QR code contains

A pairing string with this format:

```
mc1:<base64-encoded-key>
```

- `mc1` ... protocol version prefix (Memory Crystal v1)
- The rest is the raw 32-byte encryption key, base64 encoded

That's it. No server. No handshake. No session tokens. The QR code IS the key. Scan it, save it, done.

### Why this is safe

1. **QR codes are physical proximity only.** You have to be in the same room to scan it. That's the security model. Same as AirDrop.
2. **The key never touches a network.** No HTTP call, no relay, no cloud. Camera to screen. Local.
3. **Terminal QR codes are ephemeral.** They exist on screen for a few minutes, then the terminal scrolls past them. No persistence.
4. **The pairing string is copy-pasteable** for headless/SSH scenarios. The user is responsible for secure transfer in that case (same as today).

### What we are NOT building

- **No TOTP/rotating codes.** The key is static. If you pair once, you're paired forever (until you rotate the key).
- **No relay-assisted pairing.** The whole point is the key never touches a server.
- **No Bluetooth/NFC.** Terminal-first. QR code covers 90% of cases. The manual code covers the rest.
- **No key rotation in this spec.** That's a separate feature (`crystal rotate`). This spec is about initial pairing only.

## Implementation

### New CLI commands

Add to `cli.ts`:

```
crystal pair              Show QR code with current key (generate if none exists)
crystal pair --scan       Open camera to scan QR code (macOS only, uses AVFoundation)
crystal pair --code <str> Accept a pairing code directly (no camera needed)
```

### Dependencies

- **QR generation:** `qrcode-terminal` (npm, MIT, zero deps, renders QR in terminal using Unicode block chars). Already well-established, 2M+ weekly downloads.
- **QR scanning (macOS):** Two options:
  - **Option A:** `imagesnap` + `zbar` (brew install, captures frame from camera, decodes QR). Heavy.
  - **Option B:** AppleScript/Swift bridge to AVFoundation camera. Native, no deps, macOS only.
  - **Option C (recommended):** Skip camera scanning entirely for v1. Just support `--code` for manual paste. The showing side (QR display) is the important UX win. Scanning can come later or be done via phone camera (most people will photograph the terminal QR with their phone, then type the code on the other machine).

### Recommended v1 scope

1. `crystal pair` ... generate key if missing, display QR code + pairing string in terminal
2. `crystal pair --code <string>` ... accept pairing string, save key
3. Skip `--scan` for v1 (camera scanning is complex, cross-platform headache, and the manual code covers it)

### Files to change

| File | Change |
|------|--------|
| `src/cli.ts` | Add `pair` subcommand with QR display and `--code` flag |
| `src/crypto.ts` | Add `generateRelayKey()` function (wraps `randomBytes(32)`) |
| `src/pair.ts` (new) | Pairing logic: encode/decode pairing string, QR generation, key save |
| `package.json` | Add `qrcode-terminal` dependency |
| `RELAY.md` | Update key sharing section with `crystal pair` instructions |
| `SKILL.md` | Add pairing instructions to the relay setup flow |

### Pairing string format

```
mc1:<base64(32-byte-key)>
```

Validation:
- Must start with `mc1:`
- Base64 portion must decode to exactly 32 bytes
- Reject anything else with a clear error

Future versions could use `mc2:` for a different key format or include metadata (device name, timestamp). But v1 is just the key.

### Key generation function

```typescript
// src/crypto.ts
export function generateRelayKey(): Buffer {
  return randomBytes(32);
}

export function encodeRelayPairingString(key: Buffer): string {
  if (key.length !== 32) throw new Error('Key must be 32 bytes');
  return `mc1:${key.toString('base64')}`;
}

export function decodeRelayPairingString(str: string): Buffer {
  if (!str.startsWith('mc1:')) throw new Error('Invalid pairing string (expected mc1: prefix)');
  const key = Buffer.from(str.slice(4), 'base64');
  if (key.length !== 32) throw new Error('Invalid key length (expected 32 bytes)');
  return key;
}
```

## Open Questions

1. **Should `crystal pair` also configure the relay URL and auth token?** Right now those are separate env vars (`CRYSTAL_RELAY_URL`, `CRYSTAL_RELAY_TOKEN`). The pairing flow could prompt for these too, making `crystal pair` a full "connect to relay" wizard. Or keep it key-only and add `crystal relay setup` separately.

2. **Key rotation.** If you pair a third device later, it gets the current key. But what if you want to rotate the key and re-pair everything? That's `crystal rotate` territory. Not in this spec, but worth noting.

3. **Enterprise key provisioning.** For teams, QR pairing is per-device. Enterprise might want a different flow (admin provisions keys via 1Password, vault, or MDM). That's the enterprise spec, not this one.

## Timeline

This is small. Estimated scope:
- `pair.ts` + CLI wiring: ~100 lines
- `crypto.ts` additions: ~20 lines
- Docs updates: ~30 lines
- Testing: manual (pair between Mac Mini and MacBook Air)

## References

- Grok feedback: `ai/notes/2026-02-27--cc-mini--grok-feedback.md`
- Lēsa feedback: `ai/notes/2026-02-27--cc-mini--lesa-feedback.md`
- Current crypto: `src/crypto.ts`
- Current relay docs: `RELAY.md`, `TECHNICAL.md`
