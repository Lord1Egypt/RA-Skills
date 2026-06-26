/**
 * License ledger — read/write/compare LICENSE-LEDGER.json + snapshot archiving.
 */
import { readFileSync, writeFileSync, mkdirSync, existsSync } from "node:fs";
import { join } from "node:path";
const LEDGER_FILE = "LICENSE-LEDGER.json";
const SNAPSHOT_DIR = "ledger/snapshots";
export function ledgerPath(repoRoot) {
    return join(repoRoot, LEDGER_FILE);
}
export function createEmptyLedger() {
    return {
        version: 1,
        dependencies: [],
        last_full_scan: null,
        alerts: [],
    };
}
export function readLedger(repoRoot) {
    const p = ledgerPath(repoRoot);
    if (!existsSync(p))
        return createEmptyLedger();
    return JSON.parse(readFileSync(p, "utf-8"));
}
export function writeLedger(repoRoot, ledger) {
    const p = ledgerPath(repoRoot);
    writeFileSync(p, JSON.stringify(ledger, null, 2) + "\n", "utf-8");
}
export function findEntry(ledger, name) {
    return ledger.dependencies.find((d) => d.name === name);
}
export function upsertEntry(ledger, entry) {
    const idx = ledger.dependencies.findIndex((d) => d.name === entry.name);
    if (idx >= 0) {
        ledger.dependencies[idx] = entry;
    }
    else {
        ledger.dependencies.push(entry);
    }
}
/**
 * Archive a LICENSE file snapshot for a dependency.
 */
export function archiveSnapshot(repoRoot, depName, licenseContent, date) {
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
export function hasLicenseChanged(entry) {
    return entry.license_at_adoption !== entry.license_current;
}
/**
 * Add an alert to the ledger.
 */
export function addAlert(ledger, dep, from, to) {
    ledger.alerts.push({
        dependency: dep,
        from,
        to,
        detected: new Date().toISOString(),
        message: `⚠️  License changed: ${dep} went from ${from} → ${to}`,
    });
}
//# sourceMappingURL=ledger.js.map