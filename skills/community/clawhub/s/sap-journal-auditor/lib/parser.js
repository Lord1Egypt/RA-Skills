/**
 * SAP Journal Parser
 * Parses SAP FI/CO journal exports (CSV or Excel) into a normalized entry array.
 *
 * @author Daryoosh Dehestani (https://github.com/dda-oo)
 * @organization RadarRoster (https://radarroster.com)
 * @license CC-BY-4.0
 *
 * Supports common SAP export formats:
 *   - FB03 (Document Display)
 *   - FAGLL03 (G/L Account Line Items)
 *   - KSB1 (Cost Center Line Items)
 *   - ACDOCA extract (S/4HANA Universal Journal)
 *
 * Features:
 *   - German and English column header mapping
 *   - European (1.234,56) and US (1,234.56) number formats
 *   - SAP date formats (YYYYMMDD, DD.MM.YYYY)
 *   - Zero-dependency fallback parsers
 */

"use strict";

const fs = require("fs");
const path = require("path");
// Zero-dependency fallbacks (used when npm packages are not installed)
// To use the full npm packages instead, run: npm install csv-parse xlsx
let csvParse, xlsxReadFile;
try {
  csvParse = require("csv-parse/sync").parse;
} catch {
  csvParse = require("./csv-parse-lite").parse;
}
try {
  const XLSX = require("xlsx");
  xlsxReadFile = (p) => {
    const wb = XLSX.readFile(p);
    const sheet = wb.Sheets[wb.SheetNames[0]];
    return XLSX.utils.sheet_to_json(sheet, { defval: "" });
  };
} catch {
  xlsxReadFile = require("./xlsx-lite").readExcel;
}

/**
 * SAP column name mappings → normalized field names.
 * SAP exports vary by transaction and locale (EN/DE).
 */
const COLUMN_MAP = {
  // Document Number
  "Document Number": "docNumber",
  "Belegnummer": "docNumber",
  "BELNR": "docNumber",
  "Doc. No.": "docNumber",
  "Beleg-Nr.": "docNumber",

  // Posting Date
  "Posting Date": "postingDate",
  "Buchungsdatum": "postingDate",
  "BUDAT": "postingDate",
  "Pstg Date": "postingDate",

  // Entry Date
  "Entry Date": "entryDate",
  "Erfassungsdatum": "entryDate",
  "BLDAT": "entryDate",

  // Fiscal Period
  "Fiscal Period": "fiscalPeriod",
  "Buchungsperiode": "fiscalPeriod",
  "MONAT": "fiscalPeriod",
  "Period": "fiscalPeriod",

  // Amount
  "Amount": "amount",
  "Betrag": "amount",
  "DMBTR": "amount",
  "Amount in LC": "amount",
  "Betrag in HW": "amount",
  "HSL": "amount",

  // Currency
  "Currency": "currency",
  "Währung": "currency",
  "WAERS": "currency",
  "Curr.": "currency",

  // GL Account
  "G/L Account": "account",
  "Sachkonto": "account",
  "HKONT": "account",
  "Account": "account",
  "Konto": "account",

  // Cost Center
  "Cost Center": "costCenter",
  "Kostenstelle": "costCenter",
  "KOSTL": "costCenter",
  "Cost Ctr": "costCenter",

  // Profit Center
  "Profit Center": "profitCenter",
  "Profitcenter": "profitCenter",
  "PRCTR": "profitCenter",

  // Reference
  "Reference": "reference",
  "Referenz": "reference",
  "XBLNR": "reference",
  "Ref.Doc.No": "reference",

  // Document Text
  "Document Text": "docText",
  "Belegtext": "docText",
  "BKTXT": "docText",
  "Text": "docText",

  // User / Created By
  "User Name": "user",
  "Benutzername": "user",
  "USNAM": "user",
  "User": "user",
  "Created by": "user",
  "Erfasst von": "user",

  // Vendor
  "Vendor": "vendor",
  "Kreditor": "vendor",
  "LIFNR": "vendor",

  // Customer
  "Customer": "customer",
  "Debitor": "customer",
  "KUNNR": "customer",

  // Debit/Credit Indicator
  "D/C": "debitCredit",
  "S/H": "debitCredit",
  "SHKZG": "debitCredit",

  // Company Code
  "Company Code": "companyCode",
  "Buchungskreis": "companyCode",
  "BUKRS": "companyCode",
};

/**
 * Normalize raw column headers to internal field names.
 */
function normalizeHeaders(headers) {
  return headers.map((h) => {
    const trimmed = (h || "").trim();
    return COLUMN_MAP[trimmed] || trimmed.toLowerCase().replace(/[\s/().-]+/g, "_");
  });
}

/**
 * Parse amount string to float, handling European and US formats.
 * e.g. "1.234,56" → 1234.56 | "1,234.56" → 1234.56 | "-500" → -500
 */
function parseAmount(raw) {
  if (raw === null || raw === undefined || raw === "") return 0;
  if (typeof raw === "number") return raw;
  const str = String(raw).trim();
  // Detect European format: has comma as decimal separator
  if (/^\-?\d{1,3}(\.\d{3})*(,\d+)?$/.test(str)) {
    return parseFloat(str.replace(/\./g, "").replace(",", "."));
  }
  // US format or plain number
  return parseFloat(str.replace(/,/g, "")) || 0;
}

/**
 * Parse a date string into a JS Date object.
 * Handles: DD.MM.YYYY (German), MM/DD/YYYY, YYYY-MM-DD, YYYYMMDD (SAP raw).
 */
function parseDate(raw) {
  if (!raw) return null;
  if (raw instanceof Date) return raw;
  const s = String(raw).trim();
  // YYYYMMDD
  if (/^\d{8}$/.test(s)) {
    return new Date(`${s.slice(0, 4)}-${s.slice(4, 6)}-${s.slice(6, 8)}`);
  }
  // DD.MM.YYYY
  const de = s.match(/^(\d{2})\.(\d{2})\.(\d{4})$/);
  if (de) return new Date(`${de[3]}-${de[2]}-${de[1]}`);
  // MM/DD/YYYY
  const us = s.match(/^(\d{2})\/(\d{2})\/(\d{4})$/);
  if (us) return new Date(`${us[3]}-${us[1]}-${us[2]}`);
  // ISO
  return new Date(s);
}

/**
 * Read rows from a CSV file.
 */
function readCSV(filePath) {
  const content = fs.readFileSync(filePath, "utf8");
  const delimiter = content.includes("\t") ? "\t" : ",";
  return csvParse(content, {
    columns: true,
    skip_empty_lines: true,
    trim: true,
    delimiter,
    bom: true,
  });
}

function readExcel(filePath) {
  return xlsxReadFile(filePath);
}

/**
 * Normalize a raw row object into a clean entry.
 */
function normalizeRow(rawRow, index) {
  const row = {};
  for (const [key, val] of Object.entries(rawRow)) {
    const mapped = COLUMN_MAP[key.trim()] || key.trim().toLowerCase().replace(/[\s/().-]+/g, "_");
    row[mapped] = val;
  }

  return {
    _rowIndex: index + 2, // 1-based, +1 for header
    docNumber: String(row.docNumber || row.belnr || "").trim() || `ROW-${index + 2}`,
    postingDate: parseDate(row.postingDate || row.budat),
    entryDate: parseDate(row.entryDate || row.bldat),
    fiscalPeriod: String(row.fiscalPeriod || row.monat || "").trim(),
    amount: parseAmount(row.amount || row.dmbtr || row.hsl),
    currency: String(row.currency || row.waers || "EUR").trim(),
    account: String(row.account || row.hkont || row.sachkonto || "").trim(),
    costCenter: String(row.costCenter || row.kostl || "").trim(),
    profitCenter: String(row.profitCenter || row.prctr || "").trim(),
    reference: String(row.reference || row.xblnr || "").trim(),
    docText: String(row.docText || row.bktxt || row.text || "").trim(),
    user: String(row.user || row.usnam || "").trim(),
    vendor: String(row.vendor || row.lifnr || "").trim(),
    customer: String(row.customer || row.kunnr || "").trim(),
    debitCredit: String(row.debitCredit || row.shkzg || "").trim().toUpperCase(),
    companyCode: String(row.companyCode || row.bukrs || "").trim(),
  };
}

/**
 * Main export: parse a journal file and return normalized entries.
 * @param {string} filePath - path to CSV or Excel file
 * @param {object} options  - { period: 'YYYY-MM' } to filter by period
 * @returns {Array} normalized entry objects
 */
async function parseJournalFile(filePath, options = {}) {
  const ext = path.extname(filePath).toLowerCase();
  let rawRows;

  if (ext === ".csv" || ext === ".txt") {
    rawRows = readCSV(filePath);
  } else if (ext === ".xlsx" || ext === ".xls") {
    rawRows = readExcel(filePath);
  } else {
    throw new Error(`Unsupported file type: ${ext}. Please provide a CSV or Excel file.`);
  }

  if (!rawRows || rawRows.length === 0) {
    throw new Error("File appears empty or could not be parsed.");
  }

  let entries = rawRows.map((row, i) => normalizeRow(row, i));

  // Filter by period if specified
  if (options.period) {
    const [year, month] = options.period.split("-");
    entries = entries.filter((e) => {
      if (!e.postingDate) return true;
      const y = e.postingDate.getFullYear();
      const m = e.postingDate.getMonth() + 1;
      return String(y) === String(year) && String(m).padStart(2, "0") === String(month).padStart(2, "0");
    });
  }

  return entries;
}

module.exports = { parseJournalFile, parseAmount, parseDate };
