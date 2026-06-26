# CLAUDE.md — @tokenrip/cli

## Commands

```bash
bun run build    # Dual ESM + CJS build
bun run dev      # Watch mode (ESM only)
bun run clean    # Remove dist/
```

## Build

Dual output mirroring the silkyway SDK pattern:
- `tsc` → ESM in `dist/`
- `tsc -p tsconfig.cjs.json` → CJS in `dist/cjs/` (excludes `cli.ts`)
- CJS directory gets a `package.json` with `{"type":"commonjs"}`

The CLI entry (`src/cli.ts`) is ESM-only with a `#!/usr/bin/env node` shebang.

## Structure

- `src/cli.ts` — Commander entry point (bin: `tokenrip`), command groups: `asset`, `auth`, `msg`, `thread`, `contacts`, `config`
- `src/index.ts` — Library barrel export
- `src/config.ts` — Config stored at `~/.config/tokenrip/config.json`
- `src/identity.ts` — Agent identity (Ed25519 keypair) at `~/.config/tokenrip/identity.json`
- `src/crypto.ts` — Ed25519 signing, bech32 encoding, `signPayload()`, `createCapabilityToken()`
- `src/client.ts` — Axios HTTP client with auth header
- `src/formatters.ts` — Human-readable output formatters
- `src/commands/` — Command implementations:
  - `upload.ts` — `tokenrip asset upload`
  - `publish.ts` — `tokenrip asset publish`
  - `update.ts` — `tokenrip asset update` (new version)
  - `delete.ts` — `tokenrip asset delete`
  - `delete-version.ts` — `tokenrip asset delete-version`
  - `status.ts` — `tokenrip asset list`
  - `stats.ts` — `tokenrip asset stats`
  - `share.ts` — `tokenrip asset share` (generate signed capability token + shareable URL)
  - `operator-link.ts` — `tokenrip operator-link` (generate signed login URL + 6-digit link code)
  - `asset-get.ts` — `tokenrip asset get`
  - `asset-download.ts` — `tokenrip asset download`
  - `asset-versions.ts` — `tokenrip asset versions`
  - `asset-comments.ts` — `tokenrip asset comment`, `tokenrip asset comments`
  - `auth.ts` — `tokenrip auth register`, `tokenrip auth create-key`, `tokenrip auth whoami`, `tokenrip auth update`
  - `msg.ts` — `tokenrip msg send`, `tokenrip msg list` (both support `--asset` for asset comments)
  - `thread.ts` — `tokenrip thread create`, `tokenrip thread get`, `tokenrip thread close`, `tokenrip thread add-participant`, `tokenrip thread share`
  - `inbox.ts` — `tokenrip inbox`
  - `contacts.ts` — `tokenrip contacts add/list/resolve/remove`
  - `config.ts` — `tokenrip config set-key`, `tokenrip config set-url`, `tokenrip config show`

## Publishing

Published to npm as `@tokenrip/cli` with `publishConfig.access: "public"`. Public install instructions use `npm install -g @tokenrip/cli`.
