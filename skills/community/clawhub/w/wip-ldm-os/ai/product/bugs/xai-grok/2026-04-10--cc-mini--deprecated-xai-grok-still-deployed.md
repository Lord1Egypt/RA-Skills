# Bug: Deprecated `wip-xai-grok` still deployed instead of `wip-x-xai-grok`

**Date:** 2026-04-10
**Filed by:** cc-mini + Parker
**Component:** wip-xai-grok deployment, extensions migration
**Severity:** High (triggers 1Password GUI prompt, breaks headless flows)

## Summary

The deprecated version of wip-xai-grok is still what's installed at `~/.openclaw/extensions/wip-xai-grok/` and `/opt/homebrew/bin/wip-xai-grok`. The new version (`@wipcomputer/wip-x-xai-grok` in `ldm-os/apis/wip-x-xai-grok-private`) has a correct SDK-based auth layer but was never deployed to replace the old one.

## Repo state

- **Deprecated (deployed):** `ldm-os/apis/wip-xai-grok-private-deprecated/core.mjs`
- **Correct (not deployed):** `ldm-os/apis/wip-x-xai-grok-private/core/{grok,auth,x-platform}.mjs`
- **Installed at runtime:** `~/.openclaw/extensions/wip-xai-grok/` (old code) and `/opt/homebrew/bin/wip-xai-grok` (old binary)

## The broken auth path

`wip-xai-grok-private-deprecated/core.mjs` line ~28:

```javascript
const key = execSync('op read "op://Agent Secrets/X API/api key"', {
  stdio: ['pipe', 'pipe', 'pipe'],
  timeout: 10000,
}).toString().trim();
```

Bare `op` shells out to the 1Password CLI without setting `OP_SERVICE_ACCOUNT_TOKEN`. Default CLI auth uses the 1Password desktop app, which triggers a biometric prompt ("Allow openclaw-gateway to get CLI access"). It worked for months because the desktop app had cached authorization for `openclaw-gateway` after the first prompt. Today (likely after the OpenClaw 2026.4.8 upgrade) the cached authorization was invalidated, and the prompt started firing again. This breaks headless automation the moment Parker is not physically at the keyboard.

## The correct auth path (already built, not deployed)

`wip-x-xai-grok-private/core/auth.mjs` imports from `@wipcomputer/wip-1password/helper` and uses the JS SDK directly:

```javascript
import { opRead, opReadMultiple } from '@wipcomputer/wip-1password/helper';

_xaiKey = await opRead('x.ai - API KEY - wipcomputer-dev', 'credential');
```

The helper (`wip-1password-private/src/helper.ts`) uses `createClient` from `@1password/sdk`, reads the SA token from `~/.openclaw/secrets/op-sa-token`, and does everything in-process. No shell. No CLI. No biometric prompt. This is the canonical headless pattern.

## Repro (today)

1. Parker asked Lēsa to generate an image via `wip-xai-grok imagine ...`
2. Command ran inside the gateway exec subprocess
3. Deprecated `core.mjs` was invoked, which called bare `op read`
4. 1Password desktop app showed "Allow openclaw-gateway to get CLI access" dialog
5. Parker was working remotely, had to interact with the dialog
6. Even after approval, the downstream curl didn't save a file (verification failed)
7. Lēsa reported "mixed results" ... which was honest, and the Write Verification Rule caught it

## Fix

**Deploy `@wipcomputer/wip-x-xai-grok` to replace `wip-xai-grok`.**

Steps:
1. Build + publish `@wipcomputer/wip-x-xai-grok` (the new package) from `ldm-os/apis/wip-x-xai-grok-private`
2. Add it to the LDM OS installer's deploy manifest
3. On next `ldm install`:
   a. Remove the old `~/.openclaw/extensions/wip-xai-grok/` directory
   b. Install the new `wip-x-xai-grok` package (or rename-back to `wip-xai-grok` for binary compatibility; see Ticket 2 for the naming question)
   c. Update any scripts/skills that reference the old binary path
4. Verify that `op` no longer shows up in the process tree when `wip-xai-grok` runs (everything should use the SDK)
5. Verify Lēsa can call `wip-xai-grok imagine ...` from exec without any desktop app prompts

## Related tickets

- **Ticket 2:** `wip-xai-grok-private-deprecated` repo needs to actually get deprecated (archived, binary removed)
- **Ticket 3:** LDM OS installer needs to know about `wip-x-xai-grok`
- **Ticket 4:** Audit all tools that shell out to `op` and migrate them to the helper

## Files involved

- **Deprecated source:** `ldm-os/apis/wip-xai-grok-private-deprecated/core.mjs`
- **Correct source:** `ldm-os/apis/wip-x-xai-grok-private/core/auth.mjs`, `core/grok.mjs`, `core/x-platform.mjs`
- **Helper:** `ldm-os/utilities/wip-1password-private/src/helper.ts`
- **Deployed (broken):** `~/.openclaw/extensions/wip-xai-grok/core.mjs`, `/opt/homebrew/bin/wip-xai-grok`
- **Installer:** `wip-ldm-os-private/src/boot/installer.mjs` (or wherever the deploy manifest lives)
