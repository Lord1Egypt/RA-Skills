/**
 * Reporter — generate reports, alerts, and static dashboard HTML.
 */
import { writeFileSync, mkdirSync } from "node:fs";
import { join } from "node:path";
import { readLedger } from "./ledger.js";
// ─── Console reports ───
export function formatScanReport(results) {
    const lines = [
        "",
        "╔══════════════════════════════════════════════════╗",
        "║         wip-license-hook — Scan Report           ║",
        "╚══════════════════════════════════════════════════╝",
        "",
    ];
    const changed = results.filter((r) => r.wasChanged);
    const newDeps = results.filter((r) => r.isNew);
    const clean = results.filter((r) => !r.wasChanged && !r.isNew);
    if (changed.length > 0) {
        lines.push("🚨 LICENSE CHANGES DETECTED:");
        lines.push("─".repeat(50));
        for (const r of changed) {
            lines.push(`  🚫 ${r.name} (${r.type})`);
            lines.push(`     License changed → now: ${r.detectedLicense}`);
            lines.push(`     Source: ${r.source}`);
        }
        lines.push("");
    }
    if (newDeps.length > 0) {
        lines.push(`📦 New dependencies found: ${newDeps.length}`);
        for (const r of newDeps) {
            lines.push(`  ➕ ${r.name} (${r.type}) — ${r.detectedLicense}`);
        }
        lines.push("");
    }
    if (clean.length > 0) {
        lines.push(`✅ Clean dependencies: ${clean.length}`);
        for (const r of clean) {
            lines.push(`  ✓ ${r.name} — ${r.detectedLicense}`);
        }
        lines.push("");
    }
    lines.push(`Total scanned: ${results.length}`);
    lines.push("");
    return lines.join("\n");
}
export function formatGateOutput(safe, alerts) {
    const lines = [];
    if (safe) {
        lines.push("");
        lines.push("╔══════════════════════════════════════════════════╗");
        lines.push("║  ✅  LICENSE CHECK PASSED — All licenses clean   ║");
        lines.push("╚══════════════════════════════════════════════════╝");
        lines.push("");
    }
    else {
        lines.push("");
        lines.push("╔══════════════════════════════════════════════════╗");
        lines.push("║  🚫  LICENSE CHECK FAILED — Changes detected!    ║");
        lines.push("╚══════════════════════════════════════════════════╝");
        lines.push("");
        for (const alert of alerts) {
            lines.push(`  ${alert}`);
        }
        lines.push("");
        lines.push("  Action required: Review license changes before proceeding.");
        lines.push("  Run: wip-license-hook scan --verbose for details.");
        lines.push("");
    }
    return lines.join("\n");
}
export function formatLedgerReport(ledger) {
    const lines = [
        "",
        "╔══════════════════════════════════════════════════╗",
        "║         wip-license-hook — Ledger Status         ║",
        "╚══════════════════════════════════════════════════╝",
        "",
        `Last full scan: ${ledger.last_full_scan ?? "never"}`,
        `Total dependencies: ${ledger.dependencies.length}`,
        `Active alerts: ${ledger.alerts.length}`,
        "",
    ];
    const statusIcon = {
        clean: "✅",
        changed: "🚫",
        removed: "❓",
        unknown: "❔",
    };
    for (const dep of ledger.dependencies) {
        const icon = statusIcon[dep.status] ?? "❔";
        lines.push(`  ${icon} ${dep.name} (${dep.type})`);
        lines.push(`     Adopted: ${dep.license_at_adoption} on ${dep.adopted_date}`);
        lines.push(`     Current: ${dep.license_current} (checked ${dep.last_checked})`);
        lines.push(`     Source:  ${dep.source}`);
    }
    if (ledger.alerts.length > 0) {
        lines.push("");
        lines.push("⚠️  ALERTS:");
        lines.push("─".repeat(50));
        for (const a of ledger.alerts) {
            lines.push(`  ${a.message}`);
            lines.push(`  Detected: ${a.detected}`);
        }
    }
    lines.push("");
    return lines.join("\n");
}
// ─── Dashboard HTML generation ───
export function generateDashboardHtml(ledger) {
    const rows = ledger.dependencies
        .map((d) => {
        const statusClass = d.status === "clean" ? "clean" : d.status === "changed" ? "changed" : "unknown";
        const statusEmoji = d.status === "clean" ? "✅" : d.status === "changed" ? "🚫" : "❔";
        return `<tr class="${statusClass}">
        <td>${statusEmoji} ${escHtml(d.name)}</td>
        <td>${escHtml(d.type)}</td>
        <td>${escHtml(d.license_at_adoption)}</td>
        <td>${escHtml(d.license_current)}</td>
        <td>${escHtml(d.adopted_date)}</td>
        <td>${escHtml(d.last_checked)}</td>
        <td>${escHtml(d.status)}</td>
      </tr>`;
    })
        .join("\n");
    const alertRows = ledger.alerts
        .map((a) => `<tr>
        <td>⚠️ ${escHtml(a.dependency)}</td>
        <td>${escHtml(a.from)} → ${escHtml(a.to)}</td>
        <td>${escHtml(a.detected)}</td>
        <td>${escHtml(a.message)}</td>
      </tr>`)
        .join("\n");
    return `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>License Compliance Dashboard — wip-license-hook</title>
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #0d1117; color: #c9d1d9; padding: 2rem; }
    h1 { color: #58a6ff; margin-bottom: 0.5rem; }
    .subtitle { color: #8b949e; margin-bottom: 2rem; }
    .stats { display: flex; gap: 2rem; margin-bottom: 2rem; }
    .stat { background: #161b22; border: 1px solid #30363d; border-radius: 8px; padding: 1rem 1.5rem; }
    .stat-value { font-size: 2rem; font-weight: bold; }
    .stat-label { color: #8b949e; font-size: 0.875rem; }
    .stat-clean .stat-value { color: #3fb950; }
    .stat-changed .stat-value { color: #f85149; }
    .stat-total .stat-value { color: #58a6ff; }
    table { width: 100%; border-collapse: collapse; background: #161b22; border: 1px solid #30363d; border-radius: 8px; overflow: hidden; margin-bottom: 2rem; }
    th { background: #21262d; text-align: left; padding: 0.75rem 1rem; color: #8b949e; font-weight: 600; border-bottom: 1px solid #30363d; }
    td { padding: 0.75rem 1rem; border-bottom: 1px solid #30363d; }
    tr.changed td { background: #f8514922; }
    tr.clean td { }
    .footer { color: #8b949e; font-size: 0.8rem; margin-top: 2rem; }
    h2 { color: #58a6ff; margin: 1.5rem 0 1rem; }
  </style>
</head>
<body>
  <h1>🔒 License Compliance Dashboard</h1>
  <p class="subtitle">Generated by wip-license-hook — ${new Date().toISOString()}</p>

  <div class="stats">
    <div class="stat stat-total">
      <div class="stat-value">${ledger.dependencies.length}</div>
      <div class="stat-label">Total Dependencies</div>
    </div>
    <div class="stat stat-clean">
      <div class="stat-value">${ledger.dependencies.filter((d) => d.status === "clean").length}</div>
      <div class="stat-label">Clean</div>
    </div>
    <div class="stat stat-changed">
      <div class="stat-value">${ledger.dependencies.filter((d) => d.status === "changed").length}</div>
      <div class="stat-label">Changed</div>
    </div>
  </div>

  <h2>Dependencies</h2>
  <table>
    <thead>
      <tr><th>Name</th><th>Type</th><th>License (Adopted)</th><th>License (Current)</th><th>Adopted</th><th>Last Checked</th><th>Status</th></tr>
    </thead>
    <tbody>${rows}</tbody>
  </table>

  ${ledger.alerts.length > 0
        ? `<h2>⚠️ Alerts</h2>
  <table>
    <thead><tr><th>Dependency</th><th>Change</th><th>Detected</th><th>Message</th></tr></thead>
    <tbody>${alertRows}</tbody>
  </table>`
        : ""}

  <div class="footer">
    <p>Last full scan: ${ledger.last_full_scan ?? "never"}</p>
    <p>Powered by <a href="https://github.com/wipcomputer/wip-license-hook" style="color: #58a6ff;">wip-license-hook</a></p>
  </div>
</body>
</html>`;
}
function escHtml(s) {
    return s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
}
// ─── Badge generation (shields.io style) ───
export function generateBadgeUrl(ledger) {
    const changed = ledger.dependencies.filter((d) => d.status === "changed").length;
    const total = ledger.dependencies.length;
    const color = changed === 0 ? "brightgreen" : "red";
    const label = "license%20compliance";
    const message = changed === 0 ? `${total}%20clean` : `${changed}%20changed`;
    return `https://img.shields.io/badge/${label}-${message}-${color}`;
}
/**
 * Write the dashboard HTML to disk.
 */
export function writeDashboard(repoRoot, ledger) {
    const l = ledger ?? readLedger(repoRoot);
    const html = generateDashboardHtml(l);
    const dir = join(repoRoot, "dashboard");
    mkdirSync(dir, { recursive: true });
    const outPath = join(dir, "index.html");
    writeFileSync(outPath, html, "utf-8");
    return outPath;
}
//# sourceMappingURL=reporter.js.map