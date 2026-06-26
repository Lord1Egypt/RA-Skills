/**
 * License ledger — read/write/compare LICENSE-LEDGER.json + snapshot archiving.
 */

import { readFileSync, writeFileSync, mkdirSync, existsSync, copyFileSync } from "node:fs";
import { join, dirname } from "node:path";
import type { LicenseId } from "./detector.js";

export type DependencyStatus = "clean" | "changed" | "removed" | "unknown";
export type DependencyType = "fork" | "npm" | "pip" | "cargo" | "go";

export interface LedgerEntry {
  name: string;
  source: string;
  type: DependencyType;
  license_at_adoption: LicenseId;
  license_current: LicenseId;
  adopted_date: string;       // ISO date
  last_checked: string;       // ISO date
  commit_at_adoption?: string;
  status: DependencyStatus;
}

export interface Alert {
  dependency: string;
  from: LicenseId;
  to: LicenseId;
  detected: string;  // ISO datetime
  message: string;
}

export interface Ledger {
  version: 1;
  dependencies: LedgerEntry[];
  last_full_scan: string | null;
  alerts: Alert[];
}

const LEDGER_FILE = "LICENSE-LEDGER.json";
const SNAPSHOT_DIR = "ledger/snapshots";

export function ledgerPath(repoRoot: string): string {
  return join(repoRoot, LEDGER_FILE);
}

export function createEmptyLedger(): Ledger {
  return {
    version: 1,
    dependencies: [],
    last_full_scan: null,
    alerts: [],
  };
}

export function readLedger(repoRoot: string): Ledger {
  const p = ledgerPath(repoRoot);
  if (!existsSync(p)) return createEmptyLedger();
  return JSON.parse(readFileSync(p, "utf-8"));
}

export function writeLedger(repoRoot: string, ledger: Ledger): void {
  const p = ledgerPath(repoRoot);
  writeFileSync(p, JSON.stringify(ledger, null, 2) + "\n", "utf-8");
}

export function findEntry(ledger: Ledger, name: string): LedgerEntry | undefined {
  return ledger.dependencies.find((d) => d.name === name);
}

export function upsertEntry(ledger: Ledger, entry: LedgerEntry): void {
  const idx = ledger.dependencies.findIndex((d) => d.name === entry.name);
  if (idx >= 0) {
    ledger.dependencies[idx] = entry;
  } else {
    ledger.dependencies.push(entry);
  }
}

/**
 * Archive a LICENSE file snapshot for a dependency.
 */
export function archiveSnapshot(
  repoRoot: string,
  depName: string,
  licenseContent: string,
  date?: string
): string {
  const d = date ?? new Date().toISOString().slice(0, 10);
  const dir = join(repoRoot, SNAPSHOT_DIR, depName);
  mkdirSync(dir, { recursive: true });
  const filename = `LICENSE-${d}.txt`;
  const p = join(dir, filename);
  writeFileSync(p, licenseContent, "utf-8");
  return p;
}

/**
 * Compare an entry's current license against its adoption license.
 * Returns true if changed.
 */
export function hasLicenseChanged(entry: LedgerEntry): boolean {
  return entry.license_at_adoption !== entry.license_current;
}

/**
 * Add an alert to the ledger.
 */
export function addAlert(ledger: Ledger, dep: string, from: LicenseId, to: LicenseId): void {
  ledger.alerts.push({
    dependency: dep,
    from,
    to,
    detected: new Date().toISOString(),
    message: `⚠️  License changed: ${dep} went from ${from} → ${to}`,
  });
}
