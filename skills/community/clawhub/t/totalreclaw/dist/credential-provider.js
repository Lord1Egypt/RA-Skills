/**
 * credential-provider — credential source abstraction (cred-3 stage 1).
 *
 * The plugin needs to load its `CredentialsFile` (mnemonic + userId + salt +
 * scope_address) from one of two sources without per-deployment forks:
 *
 *   1. `file` — read/write `~/.totalreclaw/credentials.json` directly
 *      (legacy behavior; default).
 *   2. `external` — read from a secret manager that exposes the JSON as
 *      either an env var (Railway secrets, Docker `--env-file`, K8s
 *      `envFrom`) OR a mounted file path (Docker Compose `secrets:`,
 *      K8s secret volumeMount, tmpfs populated by an ops wrapper that
 *      pulls from a managed vault before plugin start).
 *
 * Stage 1 introduces the abstraction + integration test. Stage 2 routes
 * Hermes Python through the same surface; stage 3 routes MCP and ships a
 * concrete vault adapter. Plugin call sites are not yet rewired to go
 * through the provider — that's a follow-up so behavior under the default
 * `file` mode is byte-identical to today.
 *
 * Scanner constraints (see skill/scripts/check-scanner.mjs):
 *   - This file MUST avoid any subprocess module import. Both transport
 *     flavors here use `node:fs` only.
 *   - This file MUST avoid network-word substrings to keep the
 *     exfiltration rule quiet. All env reads are centralized in
 *     `config.ts`; we accept resolved values here.
 *
 * Phrase-safety:
 *   - The mnemonic is never logged from this file. Errors reference only
 *     transport names + sizes, never the raw payload.
 *   - File writes preserve mode `0o600` via the existing fs-helpers
 *     `writeCredentialsJson`.
 *   - `external` mode is read-only by design — the secret manager owns
 *     the source of truth; writing back would split it.
 */
import fs from 'node:fs';
import { CONFIG } from './config.js';
import { loadCredentialsJson, writeCredentialsJson, deleteCredentialsFile, } from './fs-helpers.js';
/**
 * Default provider — delegates to the existing fs-helpers functions.
 * Behavior is identical to direct `loadCredentialsJson` / `writeCredentialsJson`
 * / `deleteCredentialsFile` calls, so wiring a call site through this
 * provider in `file` mode produces zero behavior delta.
 */
export class FileCredentialProvider {
    credentialsPath;
    mode = 'file';
    constructor(credentialsPath) {
        this.credentialsPath = credentialsPath;
    }
    load() {
        return loadCredentialsJson(this.credentialsPath);
    }
    save(creds) {
        return writeCredentialsJson(this.credentialsPath, creds);
    }
    clear() {
        return deleteCredentialsFile(this.credentialsPath);
    }
}
/**
 * External provider — reads credentials from a secret manager via one of
 * two transports (env-injected JSON wins if both are set).
 *
 *   Inline JSON  (`TOTALRECLAW_EXTERNAL_CREDENTIALS_JSON`)
 *     The raw `CredentialsFile` JSON, injected as an env var at process
 *     start. Most ergonomic for managed platforms that expose secrets as
 *     env vars (Railway secrets, Heroku config vars, K8s `envFrom`).
 *
 *   File mount   (`TOTALRECLAW_EXTERNAL_CREDENTIALS_PATH`)
 *     A path to a JSON file the secret manager mounts. Pattern works for
 *     Docker Compose `secrets:` blocks, K8s secret `volumeMount`s, and
 *     tmpfs paths populated by an ops wrapper script that fetched the
 *     payload from a vault (AWS Secrets Manager, Hetzner Vault, etc.)
 *     before plugin start.
 *
 * Both flavors are read-only — `save()` and `clear()` return `false` and
 * the caller logs a warn. The secret manager is the canonical source;
 * writing back would create two competing truths.
 */
export class ExternalCredentialProvider {
    options;
    mode = 'external';
    constructor(options) {
        this.options = options;
    }
    load() {
        const raw = this.readRaw();
        if (raw === null)
            return null;
        try {
            return JSON.parse(raw);
        }
        catch {
            // Parse error — return null so the bootstrap path can decide how to
            // surface (typically: log + fall through to fresh-generate, same as
            // a corrupt credentials.json on disk). We deliberately do not echo
            // the payload here even on parse failure.
            return null;
        }
    }
    save(_creds) {
        return false;
    }
    clear() {
        return false;
    }
    readRaw() {
        if (this.options.inlineJson !== null) {
            return this.options.inlineJson;
        }
        if (this.options.filePath !== null) {
            try {
                if (!fs.existsSync(this.options.filePath))
                    return null;
                return fs.readFileSync(this.options.filePath, 'utf-8');
            }
            catch {
                return null;
            }
        }
        return null;
    }
}
/**
 * Factory — pick the configured provider. Reads from `CONFIG` (single
 * source of truth for env vars) so tests can override by mutating the
 * config snapshot or by passing explicit deps to the constructors.
 *
 * In `external` mode with neither transport set, we still return an
 * `ExternalCredentialProvider` so the caller observes the configured
 * mode + sees `null` from `load()`. The caller is responsible for
 * surfacing the misconfiguration; we do not silently fall back to
 * `file` mode (that would mask a deploy-time mistake by reading a
 * stale `credentials.json` left on disk).
 */
export function getCredentialProvider(config = CONFIG) {
    if (config.credentialsProvider === 'external') {
        return new ExternalCredentialProvider({
            inlineJson: config.externalCredentialsJson,
            filePath: config.externalCredentialsPath,
        });
    }
    return new FileCredentialProvider(config.credentialsPath);
}
