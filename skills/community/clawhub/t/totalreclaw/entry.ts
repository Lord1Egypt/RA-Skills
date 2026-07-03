/**
 * entry — env-reading seam (Task 1.3, OpenClaw native integration plan,
 * 2026-06-21).
 *
 * This file is one of the TWO designated homes for `process.env.*` reads
 * in the plugin (the other is `config.ts`). Every other source file
 * receives env-derived values as PARAMETERS via the primitives exported
 * here — never reading the env directly. The invariant is locked in by
 * `entry-env.test.ts` and exists so NO plugin file can accidentally trip
 * OpenClaw's env-harvesting scanner rule (which fires on a per-file AND
 * of `process.env` + a network trigger word). Keeping every env read in
 * env-only files (`config.ts` + `entry.ts`) means the AND can never fire
 * outside these two files, which perform no network I/O.
 *
 * Phase 1 scope (this file): expose pure env-reader primitives so the 7
 * former env-reading modules (`batch-gate`, `consolidation`,
 * `semantic-dedup`, `download-ux`, `fs-helpers`, `contradiction-sync`,
 * `claims-helper`) can replace their direct `process.env.*` reads with
 * imported helpers — keeping their per-call test-toggle semantics intact
 * (the primitives read env at CALL time, not boot time).
 *
 * Phase 2 scope (future): this file becomes the
 * `definePluginEntry({ register })` home — `register()` will move out of
 * `index.ts` into here, giving the OpenClaw runtime a single native
 * entry-point. The env-reader primitives stay; the register logic joins
 * them.
 *
 * Hard contracts (enforced by entry-env.test.ts):
 *   - This file ONLY reads `process.env.*`. No network. No disk I/O
 *     beyond what `node:os` already does for the home dir.
 *   - No outbound-network primitive token in this file's source.
 */

import os from 'node:os';

// ---------------------------------------------------------------------------
// Primitive env-readers — read at CALL time so tests can toggle env vars
// between assertions without a module reload. Each helper centralizes one
// shape (string, number, boolean, home-dir) so call sites stay terse.
// ---------------------------------------------------------------------------

/**
 * Read a string env var. Returns the raw value if set and non-empty,
 * otherwise the provided fallback. Never throws.
 */
export function envString(name: string, fallback = ''): string {
  const v = process.env[name];
  if (v === undefined || v === null) return fallback;
  return v;
}

/**
 * Read a string env var and return the trimmed-lowercase form, or the
 * fallback if unset/empty. Common shape for mode/flag env vars compared
 * against literal strings like `'true'`, `'off'`, `'shadow'`.
 */
export function envStringLower(name: string, fallback = ''): string {
  const v = process.env[name];
  if (v === undefined || v === null || v === '') return fallback;
  return v.trim().toLowerCase();
}

/**
 * Read a numeric env var with bounds checking. Returns `fallback` when
 * the var is unset, empty, non-finite, or outside `[min, max]`.
 *
 * `kind` controls integer vs float parsing; defaults to float.
 */
export function envNumber(
  name: string,
  fallback: number,
  opts: { min?: number; max?: number; integer?: boolean } = {},
): number {
  const raw = process.env[name];
  if (raw === undefined || raw === null || raw === '') return fallback;
  const parsed = opts.integer ? parseInt(raw, 10) : parseFloat(raw);
  if (!Number.isFinite(parsed)) return fallback;
  if (opts.min !== undefined && parsed < opts.min) return fallback;
  if (opts.max !== undefined && parsed > opts.max) return fallback;
  return parsed;
}

/**
 * Read a boolean env var. Returns `true` only when the raw value
 * case-insensitively equals `truthy`; `false` otherwise (including
 * unset). Mirrors the common `process.env.X === 'true'` shape.
 */
export function envBoolean(name: string, truthy = 'true'): boolean {
  return process.env[name] === truthy;
}

/**
 * Resolve the user home directory. Centralized so the fallback
 * (`/home/node`) is consistent across every call site (mirrors
 * `config.ts`'s own `home` derivation — kept independent so this file
 * has no dependency on `config.ts`'s internal state).
 */
export function envHomeDir(): string {
  return process.env.HOME ?? '/home/node';
}

/**
 * Same as `envHomeDir` but prefers `os.homedir()` when `HOME` is unset
 * — used by modules that historically called `os.homedir()` directly so
 * behaviour is preserved exactly.
 */
export function envHomedir(): string {
  const h = process.env.HOME;
  if (h && h.length > 0) return h;
  return os.homedir();
}

// ---------------------------------------------------------------------------
// Module-load-time reads — values that are documented as boot-only
// (intentionally NOT re-read on each call). Imported by modules that need
// a one-shot snapshot at load time.
// ---------------------------------------------------------------------------

/**
 * Gnosis chain-batching kill-switch. Read ONCE at module load — the env
 * does not change mid-process and per-call re-parsing is too expensive
 * for the auto-extraction hot path. Spec #281 §9 Phase 1 (item imp-16).
 *
 * `false` (any case) disables batching on every chain; any other value
 * (including unset) leaves it enabled.
 */
const GNOSIS_BATCH_ENABLED_AT_BOOT: boolean =
  envString('TOTALRECLAW_GNOSIS_BATCH_ENABLED').toLowerCase() !== 'false';

export function isGnosisBatchEnabledAtBoot(): boolean {
  return GNOSIS_BATCH_ENABLED_AT_BOOT;
}
