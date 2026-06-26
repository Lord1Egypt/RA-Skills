/**
 * Reporter — generate reports, alerts, and static dashboard HTML.
 */
import { type Ledger } from "./ledger.js";
import type { ScanResult } from "./scanner.js";
export declare function formatScanReport(results: ScanResult[]): string;
export declare function formatGateOutput(safe: boolean, alerts: string[]): string;
export declare function formatLedgerReport(ledger: Ledger): string;
export declare function generateDashboardHtml(ledger: Ledger): string;
export declare function generateBadgeUrl(ledger: Ledger): string;
/**
 * Write the dashboard HTML to disk.
 */
export declare function writeDashboard(repoRoot: string, ledger?: Ledger): string;
