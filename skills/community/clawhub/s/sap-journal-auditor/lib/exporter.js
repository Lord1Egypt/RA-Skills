/**
 * SAP Journal Auditor - CSV Exporter
 * Exports flagged journal findings to CSV for downstream processing.
 *
 * @author Daryoosh Dehestani (https://github.com/dda-oo)
 * @organization RadarRoster (https://radarroster.com)
 * @license CC-BY-4.0
 */

"use strict";

const fs = require("fs");

function escapeCSV(val) {
  if (val === null || val === undefined) return "";
  const str = String(val);
  if (str.includes(",") || str.includes('"') || str.includes("\n")) {
    return `"${str.replace(/"/g, '""')}"`;
  }
  return str;
}

function fmtDate(d) {
  if (!d) return "";
  if (typeof d === "string") return d;
  return d.toISOString().slice(0, 10);
}

/**
 * Write findings to a CSV file.
 * @param {Array} findings - array of finding objects from auditor.js
 * @param {string} outputPath - destination file path
 */
function exportFlaggedCSV(findings, outputPath) {
  const headers = [
    "FindingID",
    "RiskLevel",
    "CheckType",
    "DocumentNumbers",
    "Amount",
    "Currency",
    "Account",
    "CostCenter",
    "PostingDate",
    "User",
    "Description",
    "Recommendation",
  ];

  const rows = findings.map((f) => [
    f.id,
    f.risk,
    f.checkType,
    (f.docNumbers || []).join("; "),
    f.amount !== undefined ? String(f.amount) : "",
    f.currency || "",
    f.account || "",
    f.costCenter || "",
    fmtDate(f.postingDate),
    f.user || "",
    f.description || "",
    f.recommendation || "",
  ]);

  const lines = [headers.map(escapeCSV).join(","), ...rows.map((r) => r.map(escapeCSV).join(","))];

  fs.writeFileSync(outputPath, lines.join("\n"), "utf8");
}

module.exports = { exportFlaggedCSV };
