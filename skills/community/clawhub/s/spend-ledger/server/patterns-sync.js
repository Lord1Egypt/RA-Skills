/**
 * Community pattern sync.
 *
 * Fetches the curated patterns.json from api.spend-ledger.com and caches it
 * to disk so detectors.js can merge it with local tracked-tools at runtime.
 *
 * Also provides a stable submitter_hash (SHA-256 of a per-install UUID) used
 * when the user opts to share a pattern with maintainers.
 */

import { createHash, randomUUID } from "node:crypto";
import {
  readFileSync,
  writeFileSync,
  existsSync,
  mkdirSync,
} from "node:fs";
import { resolve, dirname } from "node:path";

// ── Config ────────────────────────────────────────────────────────────────────

const DEFAULT_CONFIG_PATH = resolve(
  process.env.SPEND_LEDGER_CONFIG ||
    new URL("../data/config.json", import.meta.url).pathname
);

const DEFAULT_CONFIG = {
  sync_community_patterns: true, // set false to disable automatic pattern download
};

/**
 * Load spend-ledger configuration, merging stored values with defaults.
 */
export function loadConfig(configPath = DEFAULT_CONFIG_PATH) {
  if (!existsSync(configPath)) return { ...DEFAULT_CONFIG };
  try {
    const stored = JSON.parse(readFileSync(configPath, "utf-8"));
    return { ...DEFAULT_CONFIG, ...stored };
  } catch {
    return { ...DEFAULT_CONFIG };
  }
}

const API_BASE =
  process.env.SPEND_LEDGER_API_URL || "https://api.spend-ledger.com";

const PATTERNS_URL =
  process.env.SPEND_LEDGER_PATTERNS_URL || `${API_BASE}/patterns.json`;

const CACHE_PATH = resolve(
  process.env.SPEND_LEDGER_COMMUNITY_PATTERNS ||
    new URL("../data/community-patterns.json", import.meta.url).pathname
);

const INSTALL_ID_PATH = resolve(
  new URL("../data/install-id.json", import.meta.url).pathname
);

// ── Install ID ────────────────────────────────────────────────────────────────

/**
 * Return a stable per-install UUID, creating one on first call.
 */
export function getInstallId() {
  if (existsSync(INSTALL_ID_PATH)) {
    try {
      return JSON.parse(readFileSync(INSTALL_ID_PATH, "utf-8")).install_id;
    } catch {
      // fall through and regenerate
    }
  }
  const id = randomUUID();
  const dir = dirname(INSTALL_ID_PATH);
  if (!existsSync(dir)) mkdirSync(dir, { recursive: true });
  writeFileSync(INSTALL_ID_PATH, JSON.stringify({ install_id: id }), { mode: 0o600 });
  return id;
}

/**
 * Return a SHA-256 hex hash of the install ID — used as submitter_hash.
 * Stable across calls but not reversible back to the raw UUID.
 */
export function getSubmitterHash() {
  return createHash("sha256").update(getInstallId()).digest("hex");
}

// ── Cache ─────────────────────────────────────────────────────────────────────

/**
 * Load community patterns from the local cache file.
 * Returns an array in the same shape as tracked-tools.json entries so
 * detectUserTracked() can merge them directly.
 */
export function loadCachedPatterns() {
  if (!existsSync(CACHE_PATH)) return [];
  try {
    const data = JSON.parse(readFileSync(CACHE_PATH, "utf-8"));
    return (data.patterns || []).map((p) => ({
      tool_name_pattern: p.tool_name_pattern,
      description: p.description || "",
      category: p.category || null,
      _source: "community",
    }));
  } catch {
    return [];
  }
}

// ── Fetch ─────────────────────────────────────────────────────────────────────

/**
 * Fetch patterns.json from the remote API and save to cache.
 * Safe to call in the background — never throws.
 */
export async function syncPatterns() {
  try {
    const res = await fetch(PATTERNS_URL, {
      headers: { "User-Agent": "spend-ledger-skill/1.0" },
      signal: AbortSignal.timeout(10_000),
    });
    if (!res.ok) {
      console.error(`[patterns-sync] HTTP ${res.status} from ${PATTERNS_URL}`);
      return;
    }
    const data = await res.json();
    const dir = dirname(CACHE_PATH);
    if (!existsSync(dir)) mkdirSync(dir, { recursive: true });
    writeFileSync(CACHE_PATH, JSON.stringify(data), { mode: 0o600 });
    console.log(
      `[patterns-sync] cached ${data.pattern_count ?? "?"} community patterns`
    );
  } catch (err) {
    // Network errors are expected in offline environments — log and move on
    console.error(`[patterns-sync] fetch failed: ${err.message}`);
  }
}

/**
 * POST a single pattern submission to api.spend-ledger.com/patterns.
 * Returns true on success, false on failure. Never throws.
 */
export async function submitPattern({ tool_name_pattern, description, category }) {
  try {
    const res = await fetch(
      `${API_BASE}/patterns`,
      {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          submitter_hash: getSubmitterHash(),
          tool_name_pattern,
          description: description || "",
          category: category || undefined,
        }),
        signal: AbortSignal.timeout(10_000),
      }
    );
    if (!res.ok) {
      const body = await res.text().catch(() => "");
      console.error(`[patterns-sync] submit failed HTTP ${res.status}: ${body}`);
      return false;
    }
    return true;
  } catch (err) {
    console.error(`[patterns-sync] submit error: ${err.message}`);
    return false;
  }
}
