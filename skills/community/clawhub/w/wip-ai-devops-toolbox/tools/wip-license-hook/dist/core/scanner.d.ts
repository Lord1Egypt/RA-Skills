/**
 * Scanner — detects dependencies and their licenses across package managers.
 * Supports: npm, pip, cargo, go modules. Works offline.
 */
import { type LicenseId } from "./detector.js";
import { type DependencyType } from "./ledger.js";
export interface ScanResult {
    name: string;
    source: string;
    type: DependencyType;
    detectedLicense: LicenseId;
    licenseText?: string;
    wasChanged: boolean;
    isNew: boolean;
}
interface ScanOptions {
    repoRoot: string;
    offline?: boolean;
    verbose?: boolean;
}
export declare function findLicenseFile(dir: string): string | null;
export declare function readLicenseFromDir(dir: string): {
    license: LicenseId;
    text: string;
} | null;
export declare function scanAll(opts: ScanOptions): ScanResult[];
/**
 * Run a full scan and update the ledger. Returns results with change detection.
 */
export declare function scanAndUpdate(opts: ScanOptions): ScanResult[];
/**
 * Gate check — returns true if safe to proceed, false if blocked.
 */
export declare function gateCheck(repoRoot: string, offline: boolean): {
    safe: boolean;
    results: ScanResult[];
    alerts: string[];
};
export {};
