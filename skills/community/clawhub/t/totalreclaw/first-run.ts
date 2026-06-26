/**
 * first-run — detect a fresh machine and return the welcome/branch-question
 * copy that the `before_agent_start` hook prepends to the first agent prompt
 * after install.
 *
 * Shipped 2026-04-20 as part of the 3.3.0-rc.2 UX polish. Paired with the
 * scanner false-positive fix that unblocked rc.1 install.
 *
 * Scope and scanner surface
 * -------------------------
 *   - This module reads credentials.json via `loadCredentialsJson` from
 *     `fs-helpers.ts` (the one file in the plugin that is allowed to touch
 *     disk) — we do NOT import `node:fs` directly. That preserves the
 *     file-level isolation pattern introduced in 3.0.8 (see `fs-helpers.ts`
 *     header) and ensures the expanded `check-scanner.mjs` rules cannot
 *     flag this file even incidentally.
 *   - No network. No env-var reads. No dynamic code execution.
 *   - All user-facing copy is exported as `COPY` so tests can assert on
 *     exact strings and a future localisation pass has a single seam.
 *
 * Design notes
 * ------------
 *   - `detectFirstRun` is deliberately lax: missing file, empty file,
 *     JSON-parse-error, or a file that parses but carries no usable
 *     mnemonic (neither `mnemonic` nor the `recovery_phrase` alias) all
 *     count as first-run. Anything looser would risk double-welcoming a
 *     returning user whose credentials.json has been hand-edited.
 *   - `buildWelcomePrepend` branches on `'local'` vs `'remote'` gateway
 *     mode. The caller in `index.ts` resolves the mode from
 *     `api.config.gateway.remote.url` the same way `buildPairingUrl`
 *     already does.
 *   - Terminology: "recovery phrase" everywhere in user-facing copy. The
 *     prior mix of "account key", "mnemonic", "seed phrase", and "recovery
 *     phrase" across the plugin was confusing users; 3.3.0-rc.2
 *     standardises on "recovery phrase". Internal variable names
 *     (`mnemonic`, etc.) are intentionally kept so we do not churn the
 *     crypto code for a copy change.
 */

import { loadCredentialsJson, extractBootstrapMnemonic } from './fs-helpers.js';

// ---------------------------------------------------------------------------
// Canonical copy — single source of truth for the welcome-on-first-run UX.
// Tests import these constants and assert on exact-match substrings; the
// `index.ts` before_agent_start hook consumes them via `buildWelcomePrepend`.
// ---------------------------------------------------------------------------

export const WELCOME =
  'Welcome to TotalReclaw — encrypted, agent-portable memory.\n\n' +
  'Your memories are stored end-to-end encrypted and on-chain. You can restore them on any agent — OpenClaw, Hermes, or NanoClaw — with a single recovery phrase.';

export const BRANCH_QUESTION =
  "Let's set up your account. Do you already have a recovery phrase, or should we generate a new one?";

export const LOCAL_MODE_INSTRUCTIONS =
  'If you have one, run: openclaw plugin totalreclaw onboard restore\n' +
  'If you need a new one, run: openclaw plugin totalreclaw onboard generate';

export const REMOTE_MODE_INSTRUCTIONS =
  'Run: openclaw plugin totalreclaw pair start\n' +
  'This opens a browser page with a QR code. Scan it (or open the URL) to complete setup securely — your recovery phrase never passes through the chat.';

export const STORAGE_GUIDANCE =
  'Your recovery phrase is 12 words. Store it somewhere safe — a password manager works well. Use it only for TotalReclaw. Don\'t reuse it anywhere else. Don\'t put funds on it.';

export const RESTORE_PROMPT =
  'Enter your 12-word recovery phrase to restore your account.';

export const GENERATED_CONFIRMATION =
  'A new recovery phrase has been generated. Write it down now, somewhere safe. This is the only way to restore your account later.';

export const COPY = {
  WELCOME,
  BRANCH_QUESTION,
  LOCAL_MODE_INSTRUCTIONS,
  REMOTE_MODE_INSTRUCTIONS,
  STORAGE_GUIDANCE,
  RESTORE_PROMPT,
  GENERATED_CONFIRMATION,
} as const;

// ---------------------------------------------------------------------------
// Public API
// ---------------------------------------------------------------------------

export type GatewayMode = 'local' | 'remote';

/**
 * Returns `true` when the machine at `credentialsPath` has never been
 * onboarded. Specifically: the file is missing, unreadable, invalid JSON,
 * or parses but carries neither `mnemonic` nor `recovery_phrase`.
 *
 * All failure modes collapse to "first run" so the welcome can always
 * recover from a broken install. The caller is responsible for deciding
 * whether to ALSO preserve the broken file for recovery (the onboarding
 * wizard already handles that via `autoBootstrapCredentials`).
 */
export async function detectFirstRun(credentialsPath: string): Promise<boolean> {
  const creds = loadCredentialsJson(credentialsPath);
  if (!creds) return true;
  const mnemonic = extractBootstrapMnemonic(creds);
  return mnemonic === null || mnemonic.length === 0;
}

/**
 * Build the exact text to feed `prependContext` on first run. The text is
 * structured as a markdown block with a visible heading so the agent and
 * user can both tell at a glance that this is the one-shot first-run
 * banner, not arbitrary injected context.
 *
 * The mode-specific instructions branch on whether the gateway is running
 * locally (user has shell access → CLI onboard wizard) or remotely (user
 * needs QR-pairing). The caller resolves the mode from
 * `api.config.gateway.remote.url` — same resolution `buildPairingUrl`
 * uses.
 */
export function buildWelcomePrepend(mode: GatewayMode): string {
  const instructions =
    mode === 'local' ? LOCAL_MODE_INSTRUCTIONS : REMOTE_MODE_INSTRUCTIONS;

  return (
    '## Welcome to TotalReclaw\n\n' +
    WELCOME +
    '\n\n' +
    BRANCH_QUESTION +
    '\n\n' +
    instructions +
    '\n\n' +
    STORAGE_GUIDANCE
  );
}
