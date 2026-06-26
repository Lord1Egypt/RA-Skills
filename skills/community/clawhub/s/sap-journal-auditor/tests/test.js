/**
 * SAP Journal Auditor - Test Suite
 * Automated tests for all audit check implementations.
 *
 * @author Daryoosh Dehestani (https://github.com/dda-oo)
 * @organization RadarRoster (https://radarroster.com)
 * @license CC-BY-4.0
 *
 * Run with: node tests/test.js
 * Expected: 34 tests passing
 */

"use strict";

const path = require("path");
const fs = require("fs");
const { parseJournalFile } = require("../lib/parser");
const { runAllChecks } = require("../lib/auditor");
const { generateMemo } = require("../lib/reporter");
const { exportFlaggedCSV } = require("../lib/exporter");

// ── Simple test runner ───────────────────────────────────────────────────────
let passed = 0;
let failed = 0;

function assert(condition, message) {
  if (condition) {
    console.log(`  ✅ ${message}`);
    passed++;
  } else {
    console.error(`  ❌ FAIL: ${message}`);
    failed++;
  }
}

function assertEqual(actual, expected, message) {
  if (actual === expected) {
    console.log(`  ✅ ${message} (got: ${actual})`);
    passed++;
  } else {
    console.error(`  ❌ FAIL: ${message} — expected ${expected}, got ${actual}`);
    failed++;
  }
}

// ── Tests ─────────────────────────────────────────────────────────────────────

async function runTests() {
  console.log("\n=== SAP Journal Auditor — Test Suite ===\n");

  const sampleFile = path.join(__dirname, "../sample-data/journal_march_2025.csv");

  // ── Test 1: Parser ─────────────────────────────────────────────────────────
  console.log("📋 Test 1: File Parsing\n");

  let entries;
  try {
    entries = await parseJournalFile(sampleFile, {});
    assert(entries.length > 0, `Parsed ${entries.length} entries from sample CSV`);
    assert(entries[0].docNumber !== undefined, "First entry has docNumber");
    assert(entries[0].amount !== undefined, "First entry has amount");
    assert(entries[0].postingDate instanceof Date, "First entry has Date object for postingDate");
    assert(entries[0].account !== undefined, "First entry has account");
  } catch (err) {
    console.error("  ❌ Parser threw error:", err.message);
    failed++;
    return;
  }

  // ── Test 2: Amount parsing ─────────────────────────────────────────────────
  console.log("\n💶 Test 2: Amount & Date Parsing\n");

  const { parseAmount, parseDate } = require("../lib/parser");
  assertEqual(parseAmount("1.234,56"), 1234.56, "European format 1.234,56");
  assertEqual(parseAmount("1,234.56"), 1234.56, "US format 1,234.56");
  assertEqual(parseAmount("-500"), -500, "Negative plain -500");
  assertEqual(parseAmount(12345.67), 12345.67, "Already a number");

  const d1 = parseDate("15.03.2025");
  assert(d1 instanceof Date && d1.getDate() === 15, "German date 15.03.2025 → day 15");

  const d2 = parseDate("20250315");
  assert(d2 instanceof Date && d2.getMonth() === 2, "SAP raw 20250315 → March (month index 2)");

  // ── Test 3: Duplicate detection ────────────────────────────────────────────
  console.log("\n🔍 Test 3: Duplicate Detection\n");

  const auditResults = runAllChecks(entries, { duplicateThreshold: 1000 });
  const duplicates = auditResults.findings.filter((f) => f.checkType.startsWith("Duplicate"));
  assert(duplicates.length > 0, `Detected ${duplicates.length} duplicate finding(s) in sample data`);

  // Docs 1800000001 and 1800000002 are identical — should be flagged
  const doc1dup = duplicates.find(
    (f) => f.docNumbers.includes("1800000001") && f.docNumbers.includes("1800000002")
  );
  assert(doc1dup !== undefined, "Correctly flagged docs 1800000001 and 1800000002 as duplicates");
  assertEqual(doc1dup?.risk, "HIGH", "Duplicate has HIGH risk");

  // ── Test 4: Round amount + period-end ─────────────────────────────────────
  console.log("\n🔵 Test 4: Round Amount / Period-End Accruals\n");

  const roundFindings = auditResults.findings.filter((f) => f.checkType.startsWith("Round Amount"));
  assert(roundFindings.length > 0, `Detected ${roundFindings.length} round-amount finding(s)`);

  // Doc 1800000011 is 50000 EUR on accrual account 480000 on 28.03 → should be HIGH
  const doc11 = roundFindings.find((f) => f.docNumbers.includes("1800000011"));
  assert(doc11 !== undefined, "Detected round accrual posting doc 1800000011 (50000 EUR, account 480000)");

  // ── Test 5: Backdated posting ─────────────────────────────────────────────
  console.log("\n📅 Test 5: Backdated Posting Detection\n");

  const backdated = auditResults.findings.filter((f) => f.checkType === "Backdated Posting");
  assert(backdated.length > 0, `Detected ${backdated.length} backdated posting(s)`);

  // Doc 1800000032: posting date 15.01.2025, entry date 30.03.2025 → should flag
  const doc32 = backdated.find((f) => f.docNumbers.includes("1800000032"));
  assert(doc32 !== undefined, "Correctly flagged doc 1800000032 as backdated (Jan posting date, Mar entry)");

  // ── Test 6: Intercompany / missing reference ───────────────────────────────
  console.log("\n🏢 Test 6: Intercompany Anomalies\n");

  const icFindings = auditResults.findings.filter((f) => f.checkType.startsWith("Intercompany"));
  assert(icFindings.length > 0, `Detected ${icFindings.length} intercompany anomaly/anomalies`);

  // Doc 1800000016: IC account 182000, no reference
  const doc16 = icFindings.find((f) => f.docNumbers.includes("1800000016"));
  assert(doc16 !== undefined, "Flagged doc 1800000016 as intercompany posting without reference");

  // ── Test 7: Missing documentation ─────────────────────────────────────────
  console.log("\n📄 Test 7: Missing Documentation\n");

  const missingDoc = auditResults.findings.filter((f) => f.checkType === "Missing Documentation");
  assert(missingDoc.length > 0, `Detected ${missingDoc.length} undocumented posting(s)`);

  // ── Test 8: Overall risk calculation ──────────────────────────────────────
  console.log("\n⚠️  Test 8: Overall Risk\n");

  assert(["HIGH", "CRITICAL"].includes(auditResults.overallRisk), `Overall risk is correctly HIGH or CRITICAL (got: ${auditResults.overallRisk})`);

  // ── Test 9: Memo generation ────────────────────────────────────────────────
  console.log("\n📝 Test 9: Memo Generation\n");

  const memoEN = generateMemo(auditResults, entries, { language: "en", period: "2025-03" });
  assert(memoEN.includes("SAP FI/CO Journal Entry Audit Report"), "English memo has correct title");
  assert(memoEN.includes("RadarRoster"), "English memo contains RadarRoster branding");
  assert(memoEN.includes("## Executive Summary"), "English memo has Executive Summary section");
  assert(memoEN.includes("## Audit Findings"), "English memo has Findings section");

  const memoDE = generateMemo(auditResults, entries, { language: "de", period: "2025-03" });
  assert(memoDE.includes("Buchungsbeleg-Prüfbericht"), "German memo has correct title");
  assert(memoDE.includes("Zusammenfassung"), "German memo has Zusammenfassung section");

  // ── Test 10: CSV export ────────────────────────────────────────────────────
  console.log("\n📊 Test 10: CSV Export\n");

  const tmpCSV = path.join(__dirname, "../sample-data/test_output_flagged.csv");
  exportFlaggedCSV(auditResults.findings, tmpCSV);
  assert(fs.existsSync(tmpCSV), "CSV export file created");

  const csvContent = fs.readFileSync(tmpCSV, "utf8");
  const csvLines = csvContent.trim().split("\n");
  assert(csvLines.length > 1, `CSV has header + ${csvLines.length - 1} finding row(s)`);
  assert(csvLines[0].includes("FindingID"), "CSV header contains FindingID");
  assert(csvLines[0].includes("RiskLevel"), "CSV header contains RiskLevel");

  // ── Test 11: Period filtering ──────────────────────────────────────────────
  console.log("\n🗓️  Test 11: Period Filtering\n");

  const filteredEntries = await parseJournalFile(sampleFile, { period: "2025-03" });
  assert(filteredEntries.length > 0, `Period filter 2025-03 returns ${filteredEntries.length} entries`);
  const wrongPeriod = filteredEntries.filter(
    (e) => e.postingDate && e.postingDate.getMonth() !== 2 // March = index 2
  );
  // Note: some entries may have null dates — filter only valid ones
  const validWrong = wrongPeriod.filter((e) => e.postingDate !== null);
  assertEqual(validWrong.length, 0, "No entries outside March 2025 after period filter");

  // ── Summary ───────────────────────────────────────────────────────────────
  console.log("\n=== Test Results ===");
  console.log(`✅ Passed: ${passed}`);
  if (failed > 0) {
    console.error(`❌ Failed: ${failed}`);
    process.exit(1);
  } else {
    console.log("🎉 All tests passed!\n");
  }

  // Save a full audit memo for review
  const outputMemo = path.join(__dirname, "../sample-data/sample_audit_memo.md");
  const outputCSV = path.join(__dirname, "../sample-data/sample_flagged.csv");
  fs.writeFileSync(outputMemo, memoEN, "utf8");
  exportFlaggedCSV(auditResults.findings, outputCSV);

  console.log(`📄 Sample audit memo saved → ${outputMemo}`);
  console.log(`📊 Sample flagged CSV saved → ${outputCSV}\n`);
}

runTests().catch((err) => {
  console.error("Test runner error:", err);
  process.exit(1);
});
