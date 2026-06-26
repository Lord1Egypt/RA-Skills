/**
 * License ledger — read/write/compare LICENSE-LEDGER.json + snapshot archiving.
 */
import type { LicenseId } from "./detector.js";
export type DependencyStatus = "clean" | "changed" | "removed" | "unknown";
export type DependencyType = "fork" | "npm" | "pip" | "cargo" | "go";
export interface LedgerEntry {
    name: string;
    source: string;
    type: DependencyType;
    license_at_adoption: LicenseId;
    license_current: LicenseId;
    adopted_date: string;
    last_checked: string;
    commit_at_adoption?: string;
    status: DependencyStatus;
}
export interface Alert {
    dependency: string;
    from: LicenseId;
    to: LicenseId;
    detected: string;
    message: string;
}
export interface Ledger {
    version: 1;
    dependencies: LedgerEntry[];
    last_full_scan: string | null;
    alerts: Alert[];
}
export declare function ledgerPath(repoRoot: string): string;
export declare function createEmptyLedger(): Ledger;
export declare function readLedger(repoRoot: string): Ledger;
export declare function writeLedger(repoRoot: string, ledger: Ledger): void;
export declare function findEntry(ledger: Ledger, name: string): LedgerEntry | undefined;
export declare function upsertEntry(ledger: Ledger, entry: LedgerEntry): void;
/**
 * Archive a LICENSE file snapshot for a dependency.
 */
export declare function archiveSnapshot(repoRoot: string, depName: string, licenseContent: string, date?: string): string;
/**
 * Compare an entry's current license against its adoption license.
 * Returns true if changed.
 */
export declare function hasLicenseChanged(entry: LedgerEntry): boolean;
/**
 * Add an alert to the ledger.
 */
export declare function addAlert(ledger: Ledger, dep: string, from: LicenseId, to: LicenseId): void;
