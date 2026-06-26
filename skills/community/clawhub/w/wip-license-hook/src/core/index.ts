export { detectLicenseFromText, normalizeSpdx, type LicenseId } from "./detector.js";
export { readLedger, writeLedger, createEmptyLedger, findEntry, upsertEntry, archiveSnapshot, hasLicenseChanged, addAlert, type Ledger, type LedgerEntry, type Alert, type DependencyType, type DependencyStatus } from "./ledger.js";
export { scanAll, scanAndUpdate, gateCheck, findLicenseFile, readLicenseFromDir, type ScanResult } from "./scanner.js";
export { formatScanReport, formatGateOutput, formatLedgerReport, generateDashboardHtml, generateBadgeUrl, writeDashboard } from "./reporter.js";
