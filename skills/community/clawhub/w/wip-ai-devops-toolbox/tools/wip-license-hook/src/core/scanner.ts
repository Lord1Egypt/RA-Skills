/**
 * Scanner — detects dependencies and their licenses across package managers.
 * Supports: npm, pip, cargo, go modules. Works offline.
 */

import { readFileSync, existsSync, readdirSync } from "node:fs";
import { join } from "node:path";
import { execSync } from "node:child_process";
import { detectLicenseFromText, normalizeSpdx, type LicenseId } from "./detector.js";
import {
  readLedger, writeLedger, upsertEntry, findEntry, addAlert,
  archiveSnapshot, hasLicenseChanged,
  type Ledger, type LedgerEntry, type DependencyType,
} from "./ledger.js";

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

// ─── License file discovery ───

const LICENSE_NAMES = ["LICENSE", "LICENSE.md", "LICENSE.txt", "LICENCE", "COPYING", "COPYING.md"];

export function findLicenseFile(dir: string): string | null {
  for (const name of LICENSE_NAMES) {
    const p = join(dir, name);
    if (existsSync(p)) return p;
  }
  return null;
}

export function readLicenseFromDir(dir: string): { license: LicenseId; text: string } | null {
  const p = findLicenseFile(dir);
  if (!p) return null;
  const text = readFileSync(p, "utf-8");
  return { license: detectLicenseFromText(text), text };
}

// ─── Package manager detection ───

function detectPackageManagers(repoRoot: string): DependencyType[] {
  const types: DependencyType[] = [];
  if (existsSync(join(repoRoot, "package.json"))) types.push("npm");
  if (existsSync(join(repoRoot, "requirements.txt")) || existsSync(join(repoRoot, "Pipfile")) || existsSync(join(repoRoot, "pyproject.toml"))) types.push("pip");
  if (existsSync(join(repoRoot, "Cargo.toml"))) types.push("cargo");
  if (existsSync(join(repoRoot, "go.mod"))) types.push("go");
  return types;
}

// ─── npm scanning ───

function scanNpmDeps(repoRoot: string, offline: boolean): ScanResult[] {
  const results: ScanResult[] = [];
  const pkgPath = join(repoRoot, "package.json");
  if (!existsSync(pkgPath)) return results;

  const pkg = JSON.parse(readFileSync(pkgPath, "utf-8"));
  const allDeps = { ...pkg.dependencies, ...pkg.devDependencies };

  for (const [name, _version] of Object.entries(allDeps)) {
    let detectedLicense: LicenseId = "UNKNOWN";
    let licenseText: string | undefined;

    // Check node_modules first (works offline)
    const modDir = join(repoRoot, "node_modules", name);
    if (existsSync(modDir)) {
      const fromFile = readLicenseFromDir(modDir);
      if (fromFile) {
        detectedLicense = fromFile.license;
        licenseText = fromFile.text;
      }
      // Also check package.json license field
      const modPkg = join(modDir, "package.json");
      if (existsSync(modPkg) && detectedLicense === "UNKNOWN") {
        try {
          const modMeta = JSON.parse(readFileSync(modPkg, "utf-8"));
          if (modMeta.license) detectedLicense = normalizeSpdx(modMeta.license);
        } catch { /* skip */ }
      }
    }

    // Try npm view if online and still unknown
    if (detectedLicense === "UNKNOWN" && !offline) {
      try {
        const out = execSync(`npm view ${name} license 2>/dev/null`, { encoding: "utf-8", timeout: 10000 }).trim();
        if (out) detectedLicense = normalizeSpdx(out);
      } catch { /* offline or not found */ }
    }

    results.push({
      name,
      source: `npm:${name}`,
      type: "npm",
      detectedLicense,
      licenseText,
      wasChanged: false,
      isNew: true,
    });
  }

  return results;
}

// ─── pip scanning ───

function parsePipDeps(repoRoot: string): string[] {
  const names: string[] = [];
  const reqPath = join(repoRoot, "requirements.txt");
  if (existsSync(reqPath)) {
    const lines = readFileSync(reqPath, "utf-8").split("\n");
    for (const line of lines) {
      const trimmed = line.trim();
      if (!trimmed || trimmed.startsWith("#") || trimmed.startsWith("-")) continue;
      const name = trimmed.split(/[=<>!~\[]/)[0].trim();
      if (name) names.push(name);
    }
  }
  return names;
}

function scanPipDeps(repoRoot: string, offline: boolean): ScanResult[] {
  const deps = parsePipDeps(repoRoot);
  const results: ScanResult[] = [];

  for (const name of deps) {
    let detectedLicense: LicenseId = "UNKNOWN";

    if (!offline) {
      try {
        const out = execSync(`pip show ${name} 2>/dev/null`, { encoding: "utf-8", timeout: 10000 });
        const match = out.match(/^License:\s*(.+)$/m);
        if (match) detectedLicense = normalizeSpdx(match[1]);
      } catch { /* skip */ }
    }

    results.push({
      name,
      source: `pip:${name}`,
      type: "pip",
      detectedLicense,
      wasChanged: false,
      isNew: true,
    });
  }

  return results;
}

// ─── cargo scanning ───

function scanCargoDeps(repoRoot: string, offline: boolean): ScanResult[] {
  const results: ScanResult[] = [];
  const cargoPath = join(repoRoot, "Cargo.toml");
  if (!existsSync(cargoPath)) return results;

  const content = readFileSync(cargoPath, "utf-8");
  const depSection = content.match(/\[dependencies\]([\s\S]*?)(\[|$)/);
  if (!depSection) return results;

  const lines = depSection[1].split("\n");
  for (const line of lines) {
    const match = line.match(/^(\S+)\s*=/);
    if (!match) continue;
    const name = match[1];

    let detectedLicense: LicenseId = "UNKNOWN";
    if (!offline) {
      try {
        const out = execSync(`cargo info ${name} 2>/dev/null`, { encoding: "utf-8", timeout: 10000 });
        const lMatch = out.match(/license:\s*(.+)/i);
        if (lMatch) detectedLicense = normalizeSpdx(lMatch[1]);
      } catch { /* skip */ }
    }

    results.push({
      name,
      source: `cargo:${name}`,
      type: "cargo",
      detectedLicense,
      wasChanged: false,
      isNew: true,
    });
  }

  return results;
}

// ─── go scanning ───

function scanGoDeps(repoRoot: string, _offline: boolean): ScanResult[] {
  const results: ScanResult[] = [];
  const goModPath = join(repoRoot, "go.mod");
  if (!existsSync(goModPath)) return results;

  const content = readFileSync(goModPath, "utf-8");
  const requireBlock = content.match(/require\s*\(([\s\S]*?)\)/);
  const lines = requireBlock ? requireBlock[1].split("\n") : [];

  // Also handle single-line requires
  const singleRequires = content.match(/^require\s+(\S+)\s+/gm) ?? [];
  for (const sr of singleRequires) {
    const m = sr.match(/^require\s+(\S+)/);
    if (m) lines.push(m[1]);
  }

  for (const line of lines) {
    const trimmed = line.trim();
    if (!trimmed || trimmed.startsWith("//")) continue;
    const parts = trimmed.split(/\s+/);
    const name = parts[0];
    if (!name || name.startsWith(")")) continue;

    results.push({
      name,
      source: `go:${name}`,
      type: "go",
      detectedLicense: "UNKNOWN",  // Go modules need network for license check
      wasChanged: false,
      isNew: true,
    });
  }

  return results;
}

// ─── Fork/upstream scanning ───

function scanUpstreamLicense(repoRoot: string, offline: boolean): ScanResult | null {
  // Check if there's an upstream remote
  try {
    const remote = execSync("git remote get-url upstream 2>/dev/null", {
      cwd: repoRoot, encoding: "utf-8", timeout: 5000
    }).trim();
    if (!remote) return null;

    // Fetch upstream (if online)
    if (!offline) {
      try {
        execSync("git fetch upstream --quiet 2>/dev/null", { cwd: repoRoot, timeout: 30000 });
      } catch { /* offline, use cached */ }
    }

    // Try to read LICENSE from upstream/main or upstream/master
    for (const branch of ["upstream/main", "upstream/master"]) {
      try {
        const text = execSync(`git show ${branch}:LICENSE 2>/dev/null`, {
          cwd: repoRoot, encoding: "utf-8", timeout: 5000
        });
        if (text) {
          const license = detectLicenseFromText(text);
          return {
            name: "upstream",
            source: remote,
            type: "fork",
            detectedLicense: license,
            licenseText: text,
            wasChanged: false,
            isNew: true,
          };
        }
      } catch { /* try next branch */ }
    }
  } catch { /* no upstream remote */ }

  return null;
}

// ─── Main scan ───

export function scanAll(opts: ScanOptions): ScanResult[] {
  const { repoRoot, offline = false } = opts;
  const managers = detectPackageManagers(repoRoot);
  const results: ScanResult[] = [];

  // Always check upstream fork
  const upstream = scanUpstreamLicense(repoRoot, offline);
  if (upstream) results.push(upstream);

  if (managers.includes("npm")) results.push(...scanNpmDeps(repoRoot, offline));
  if (managers.includes("pip")) results.push(...scanPipDeps(repoRoot, offline));
  if (managers.includes("cargo")) results.push(...scanCargoDeps(repoRoot, offline));
  if (managers.includes("go")) results.push(...scanGoDeps(repoRoot, offline));

  return results;
}

/**
 * Run a full scan and update the ledger. Returns results with change detection.
 */
export function scanAndUpdate(opts: ScanOptions): ScanResult[] {
  const { repoRoot } = opts;
  const ledger = readLedger(repoRoot);
  const results = scanAll(opts);
  const today = new Date().toISOString().slice(0, 10);

  for (const result of results) {
    const existing = findEntry(ledger, result.name);

    if (existing) {
      result.isNew = false;
      existing.license_current = result.detectedLicense;
      existing.last_checked = today;

      if (hasLicenseChanged(existing)) {
        existing.status = "changed";
        result.wasChanged = true;
        addAlert(ledger, result.name, existing.license_at_adoption, result.detectedLicense);
      } else {
        existing.status = "clean";
      }

      upsertEntry(ledger, existing);
    } else {
      // New dependency
      const entry: LedgerEntry = {
        name: result.name,
        source: result.source,
        type: result.type,
        license_at_adoption: result.detectedLicense,
        license_current: result.detectedLicense,
        adopted_date: today,
        last_checked: today,
        status: "clean",
      };
      upsertEntry(ledger, entry);
    }

    // Archive license text if available
    if (result.licenseText) {
      archiveSnapshot(repoRoot, result.name, result.licenseText, today);
    }
  }

  ledger.last_full_scan = new Date().toISOString();
  writeLedger(repoRoot, ledger);

  return results;
}

/**
 * Gate check — returns true if safe to proceed, false if blocked.
 */
export function gateCheck(repoRoot: string, offline: boolean): { safe: boolean; results: ScanResult[]; alerts: string[] } {
  const results = scanAndUpdate({ repoRoot, offline });
  const changed = results.filter((r) => r.wasChanged);
  const alerts = changed.map(
    (r) => `🚫 LICENSE CHANGED: ${r.name} — was adopted under different terms, now detected as ${r.detectedLicense}`
  );

  return {
    safe: changed.length === 0,
    results,
    alerts,
  };
}
