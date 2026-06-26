/**
 * SAP Journal Auditor
 * Enterprise-grade SAP FI/CO journal audit automation
 *
 * @author Daryoosh Dehestani (https://github.com/dda-oo)
 * @organization RadarRoster (https://radarroster.com)
 * @license CC-BY-4.0
 *
 * Detects anomalies in SAP FI/CO journal entry exports:
 *   - Duplicate postings
 *   - Round-amount / period-end irregularities
 *   - Unusual cost center assignments
 *   - Approval bypass indicators
 *   - Intercompany / clearing anomalies
 *   - User pattern anomalies
 */

"use strict";

const fs = require("fs");
const path = require("path");
const { parseJournalFile } = require("./lib/parser");
const { runAllChecks } = require("./lib/auditor");
const { generateMemo } = require("./lib/reporter");
const { exportFlaggedCSV } = require("./lib/exporter");

/**
 * Main OpenClaw skill handler.
 * OpenClaw calls this with a context object containing:
 *   - context.inputs       : user-supplied inputs
 *   - context.message      : raw user message
 *   - context.reply(text)  : send text back to user
 *   - context.replyFile(p) : send file back to user
 *   - context.memory       : persistent key-value store
 */
async function handler(context) {
  const { inputs, reply, replyFile } = context;

  // ── 1. Validate input file ──────────────────────────────────────────────
  const filePath = inputs?.file;
  if (!filePath || !fs.existsSync(filePath)) {
    await reply(
      "❌ No file found. Please upload a SAP journal export (CSV or Excel) and try again.\n\n" +
        "Supported exports:\n" +
        "• FB03 / FAGLL03 (General Ledger)\n" +
        "• KSB1 (Cost Center Line Items)\n" +
        "• ACDOCA extract (Universal Journal)\n" +
        "• Any CSV/XLSX with columns: DocNumber, PostingDate, Amount, Account, CostCenter, User"
    );
    return;
  }

  const language = (inputs?.language || "en").toLowerCase();
  const period = inputs?.period || null;
  const duplicateThreshold = parseFloat(inputs?.threshold_duplicate_amount) || 1000;

  await reply(
    language === "de"
      ? "⏳ Analyse läuft... Bitte warten."
      : "⏳ Running audit checks... please wait."
  );

  // ── 2. Parse file ───────────────────────────────────────────────────────
  let entries;
  try {
    entries = await parseJournalFile(filePath, { period });
  } catch (err) {
    await reply(`❌ Failed to parse file: ${err.message}\n\nPlease ensure the file is a valid SAP export.`);
    return;
  }

  if (!entries || entries.length === 0) {
    await reply(
      language === "de"
        ? "⚠️ Keine Buchungszeilen gefunden. Bitte Dateiformat prüfen."
        : "⚠️ No journal entries found. Please check the file format."
    );
    return;
  }

  // ── 3. Run audit checks ─────────────────────────────────────────────────
  const auditResults = runAllChecks(entries, { duplicateThreshold, language });

  // ── 4. Generate memo ────────────────────────────────────────────────────
  const memoPath = path.join(path.dirname(filePath), "audit_memo.md");
  const memoContent = generateMemo(auditResults, entries, { language, period });
  fs.writeFileSync(memoPath, memoContent, "utf8");

  // ── 5. Export flagged CSV ───────────────────────────────────────────────
  const csvPath = path.join(path.dirname(filePath), "flagged_entries.csv");
  exportFlaggedCSV(auditResults.findings, csvPath);

  // ── 6. Summary reply ────────────────────────────────────────────────────
  const totalFlags = auditResults.findings.length;
  const critical = auditResults.findings.filter((f) => f.risk === "CRITICAL").length;
  const high = auditResults.findings.filter((f) => f.risk === "HIGH").length;

  const summaryEn =
    `✅ **Audit Complete**\n\n` +
    `📊 Entries analyzed: **${entries.length}**\n` +
    `🚩 Total findings: **${totalFlags}**\n` +
    `🔴 Critical: **${critical}** | 🟠 High: **${high}**\n` +
    `📋 Overall risk: **${auditResults.overallRisk}**\n\n` +
    `Two files have been generated:\n` +
    `• \`audit_memo.md\` — Full audit memo with recommendations\n` +
    `• \`flagged_entries.csv\` — Machine-readable findings`;

  const summaryDe =
    `✅ **Analyse abgeschlossen**\n\n` +
    `📊 Analysierte Buchungen: **${entries.length}**\n` +
    `🚩 Gesamtbefunde: **${totalFlags}**\n` +
    `🔴 Kritisch: **${critical}** | 🟠 Hoch: **${high}**\n` +
    `📋 Gesamtrisiko: **${auditResults.overallRisk}**\n\n` +
    `Zwei Dateien wurden erstellt:\n` +
    `• \`audit_memo.md\` — Vollständiges Prüfungsprotokoll\n` +
    `• \`flagged_entries.csv\` — Maschinell lesbare Befunde`;

  await reply(language === "de" ? summaryDe : summaryEn);
  await replyFile(memoPath);
  await replyFile(csvPath);

  // ── 7. Persist run metadata to memory ──────────────────────────────────
  if (context.memory) {
    const runs = (await context.memory.get("audit_runs")) || [];
    runs.push({
      timestamp: new Date().toISOString(),
      entriesCount: entries.length,
      findings: totalFlags,
      overallRisk: auditResults.overallRisk,
      period: period || "all",
    });
    await context.memory.set("audit_runs", runs.slice(-20)); // keep last 20 runs
  }
}

module.exports = { handler };
