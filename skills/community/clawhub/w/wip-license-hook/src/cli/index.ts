#!/usr/bin/env node
/**
 * wip-license-hook CLI
 *
 * Commands:
 *   init        Initialize ledger for current project
 *   scan        Scan all deps, update ledger
 *   check <dep> Check specific dependency
 *   gate        Pre-merge license gate (for hooks)
 *   report      Print ledger report
 *   dashboard   Generate static dashboard HTML
 *   alert       Print current alerts
 *   install     Install git hooks in current repo
 */

import { resolve } from "node:path";
import { existsSync, writeFileSync, mkdirSync, copyFileSync } from "node:fs";
import {
  readLedger, writeLedger, createEmptyLedger, findEntry,
  scanAndUpdate, gateCheck,
  formatScanReport, formatGateOutput, formatLedgerReport,
  writeDashboard, generateBadgeUrl,
} from "../core/index.js";

const args = process.argv.slice(2);
const command = args[0];
const flags = new Set(args.filter((a) => a.startsWith("--")));
const positional = args.filter((a) => !a.startsWith("--")).slice(1);

const repoRoot = resolve(process.cwd());
const offline = flags.has("--offline");
const verbose = flags.has("--verbose");

function help(): void {
  console.log(`
wip-license-hook — License rug-pull detection

Usage: wip-license-hook <command> [options]

Commands:
  init              Initialize LICENSE-LEDGER.json
  scan              Scan all dependencies, update ledger
  check <name>      Check a specific dependency
  gate              Pre-merge license gate (exit 1 if changed)
  report            Print ledger status
  dashboard         Generate static HTML dashboard
  alert             Show current alerts
  install           Install git hooks in .git/hooks/
  badge             Print shields.io badge URL

Options:
  --offline         Skip network calls (use cached data only)
  --verbose         Verbose output
  --help            Show this help
`);
}

async function main(): Promise<void> {
  if (!command || command === "--help" || flags.has("--help")) {
    help();
    return;
  }

  switch (command) {
    case "init": {
      const ledgerPath = resolve(repoRoot, "LICENSE-LEDGER.json");
      if (existsSync(ledgerPath)) {
        console.log("⚠️  LICENSE-LEDGER.json already exists. Use 'scan' to update.");
        return;
      }
      writeLedger(repoRoot, createEmptyLedger());
      mkdirSync(resolve(repoRoot, "ledger/snapshots"), { recursive: true });
      console.log("✅ Initialized LICENSE-LEDGER.json and ledger/snapshots/");
      console.log("   Run 'wip-license-hook scan' to populate.");
      break;
    }

    case "scan": {
      console.log(offline ? "📡 Scanning (offline mode)..." : "📡 Scanning dependencies...");
      const results = scanAndUpdate({ repoRoot, offline, verbose });
      console.log(formatScanReport(results));
      break;
    }

    case "check": {
      const name = positional[0];
      if (!name) {
        console.error("Usage: wip-license-hook check <dependency-name>");
        process.exit(1);
      }
      const ledger = readLedger(repoRoot);
      const entry = findEntry(ledger, name);
      if (!entry) {
        console.log(`❓ ${name} not found in ledger. Run 'scan' first.`);
        process.exit(1);
      }
      console.log(`\n  ${entry.status === "clean" ? "✅" : "🚫"} ${entry.name}`);
      console.log(`     Type:    ${entry.type}`);
      console.log(`     Source:  ${entry.source}`);
      console.log(`     Adopted: ${entry.license_at_adoption} on ${entry.adopted_date}`);
      console.log(`     Current: ${entry.license_current} (checked ${entry.last_checked})`);
      console.log(`     Status:  ${entry.status}\n`);
      break;
    }

    case "gate": {
      if (offline) {
        console.log("⚠️  Offline mode — skipping license gate (cannot verify upstream).");
        console.log("    Your push will proceed, but licenses were NOT checked.");
        process.exit(0);
      }
      const { safe, alerts } = gateCheck(repoRoot, offline);
      console.log(formatGateOutput(safe, alerts));
      if (!safe) process.exit(1);
      break;
    }

    case "report": {
      const ledger = readLedger(repoRoot);
      console.log(formatLedgerReport(ledger));
      break;
    }

    case "dashboard": {
      const outPath = writeDashboard(repoRoot);
      console.log(`✅ Dashboard written to ${outPath}`);
      break;
    }

    case "alert": {
      const ledger = readLedger(repoRoot);
      if (ledger.alerts.length === 0) {
        console.log("✅ No active alerts.");
      } else {
        console.log(`\n⚠️  ${ledger.alerts.length} alert(s):\n`);
        for (const a of ledger.alerts) {
          console.log(`  ${a.message}`);
          console.log(`  Detected: ${a.detected}\n`);
        }
      }
      break;
    }

    case "install": {
      const hooksDir = resolve(repoRoot, ".git/hooks");
      if (!existsSync(resolve(repoRoot, ".git"))) {
        console.error("❌ Not a git repository. Run from a git repo root.");
        process.exit(1);
      }
      mkdirSync(hooksDir, { recursive: true });

      // Find hooks relative to the package
      const pkgRoot = resolve(new URL(".", import.meta.url).pathname, "../../..");
      const prePullSrc = resolve(pkgRoot, "hooks/pre-pull.sh");
      const preCommitSrc = resolve(pkgRoot, "hooks/pre-push.sh");

      for (const [src, dest] of [
        [prePullSrc, resolve(hooksDir, "pre-merge-commit")],
        [preCommitSrc, resolve(hooksDir, "pre-push")],
      ]) {
        if (existsSync(src)) {
          copyFileSync(src, dest);
          const { chmodSync } = await import("node:fs");
          chmodSync(dest, 0o755);
          console.log(`✅ Installed ${dest}`);
        } else {
          console.log(`⚠️  Hook source not found: ${src}`);
        }
      }
      break;
    }

    case "badge": {
      const ledger = readLedger(repoRoot);
      console.log(generateBadgeUrl(ledger));
      break;
    }

    default:
      console.error(`Unknown command: ${command}`);
      help();
      process.exit(1);
  }
}

main().catch((err) => {
  console.error("Fatal error:", err.message);
  process.exit(1);
});
