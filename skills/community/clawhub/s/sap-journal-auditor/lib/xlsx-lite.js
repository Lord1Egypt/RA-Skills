/**
 * Zero-Dependency XLSX Reader
 * Minimal XLSX reader using only Node.js built-ins.
 *
 * @author Daryoosh Dehestani (https://github.com/dda-oo)
 * @organization RadarRoster (https://radarroster.com)
 * @license CC-BY-4.0
 *
 * Reads the first sheet of an .xlsx file (ZIP-based Open XML format).
 * Falls back gracefully with clear error messages if structure is unexpected.
 *
 * For production use, install the 'xlsx' npm package for full format support.
 * This file is the zero-dependency fallback for air-gapped environments.
 */

"use strict";

const fs = require("fs");
const zlib = require("zlib");

/**
 * Very lightweight ZIP reader — finds a named entry and returns its raw buffer.
 */
function readZipEntry(buffer, targetName) {
  let offset = 0;
  while (offset < buffer.length - 30) {
    const sig = buffer.readUInt32LE(offset);
    if (sig !== 0x04034b50) break; // Not a local file header

    const flags = buffer.readUInt16LE(offset + 6);
    const compression = buffer.readUInt16LE(offset + 8);
    const compressedSize = buffer.readUInt32LE(offset + 18);
    const fileNameLength = buffer.readUInt16LE(offset + 26);
    const extraLength = buffer.readUInt16LE(offset + 28);
    const fileName = buffer.slice(offset + 30, offset + 30 + fileNameLength).toString("utf8");
    const dataOffset = offset + 30 + fileNameLength + extraLength;

    if (fileName === targetName) {
      const compressedData = buffer.slice(dataOffset, dataOffset + compressedSize);
      if (compression === 0) return compressedData; // Stored
      if (compression === 8) return zlib.inflateRawSync(compressedData); // Deflate
    }

    offset = dataOffset + compressedSize;
    if (flags & 0x8) offset += 16; // Skip data descriptor
  }
  return null;
}

/**
 * Parse shared strings XML into an array.
 */
function parseSharedStrings(xml) {
  const strings = [];
  const re = /<si>[\s\S]*?<\/si>/g;
  let match;
  while ((match = re.exec(xml)) !== null) {
    const tMatch = match[0].match(/<t[^>]*>([\s\S]*?)<\/t>/g);
    if (tMatch) {
      strings.push(tMatch.map((t) => t.replace(/<[^>]+>/g, "")).join(""));
    } else {
      strings.push("");
    }
  }
  return strings;
}

/**
 * Decode a cell reference like "A1" → { col: 0, row: 1 }
 */
function decodeRef(ref) {
  const m = ref.match(/^([A-Z]+)(\d+)$/);
  if (!m) return { col: 0, row: 0 };
  let col = 0;
  for (const ch of m[1]) col = col * 26 + ch.charCodeAt(0) - 64;
  return { col: col - 1, row: parseInt(m[2], 10) };
}

/**
 * Parse a worksheet XML into a 2D array of raw cell values.
 */
function parseSheet(xml, sharedStrings) {
  const rows = {};

  const rowRe = /<row[^>]*r="(\d+)"[^>]*>([\s\S]*?)<\/row>/g;
  let rowMatch;
  while ((rowMatch = rowRe.exec(xml)) !== null) {
    const rowNum = parseInt(rowMatch[1], 10);
    const rowContent = rowMatch[2];
    const cells = {};

    const cellRe = /<c[^>]*r="([A-Z]+\d+)"[^>]*(?:t="([^"]*)")?[^>]*>[\s\S]*?<v>([\s\S]*?)<\/v>/g;
    let cellMatch;
    while ((cellMatch = cellRe.exec(rowContent)) !== null) {
      const ref = cellMatch[1];
      const type = cellMatch[2] || "";
      const rawVal = cellMatch[3];
      const { col } = decodeRef(ref);

      let value;
      if (type === "s") {
        value = sharedStrings[parseInt(rawVal, 10)] || "";
      } else if (type === "b") {
        value = rawVal === "1" ? "TRUE" : "FALSE";
      } else {
        value = rawVal;
      }
      cells[col] = value;
    }
    rows[rowNum] = cells;
  }

  return rows;
}

/**
 * Read first sheet of an XLSX file and return array of row objects.
 * @param {string} filePath
 * @returns {Array<Object>}
 */
function readExcel(filePath) {
  const buffer = fs.readFileSync(filePath);

  // Read shared strings
  const ssRaw = readZipEntry(buffer, "xl/sharedStrings.xml");
  const sharedStrings = ssRaw ? parseSharedStrings(ssRaw.toString("utf8")) : [];

  // Read workbook to find first sheet name/id
  const wbRaw = readZipEntry(buffer, "xl/workbook.xml");
  if (!wbRaw) throw new Error("Invalid XLSX: workbook.xml not found");
  const wbXml = wbRaw.toString("utf8");
  const sheetMatch = wbXml.match(/<sheet[^>]*name="([^"]*)"[^>]*r:id="([^"]*)"/);
  if (!sheetMatch) throw new Error("No sheets found in workbook");

  // Read relationships to find sheet file path
  const relsRaw = readZipEntry(buffer, "xl/_rels/workbook.xml.rels");
  let sheetPath = "xl/worksheets/sheet1.xml"; // default
  if (relsRaw) {
    const relsXml = relsRaw.toString("utf8");
    const relId = sheetMatch[2];
    const relMatch = relsXml.match(new RegExp(`Id="${relId}"[^>]*Target="([^"]+)"`));
    if (relMatch) sheetPath = `xl/${relMatch[1].replace(/^\.\.\//, "")}`;
  }

  const sheetRaw = readZipEntry(buffer, sheetPath);
  if (!sheetRaw) throw new Error(`Sheet file not found: ${sheetPath}`);
  const sheetXml = sheetRaw.toString("utf8");

  const rowData = parseSheet(sheetXml, sharedStrings);
  const rowNums = Object.keys(rowData).map(Number).sort((a, b) => a - b);
  if (rowNums.length === 0) return [];

  // First row = headers
  const headerRow = rowData[rowNums[0]];
  const maxCol = Math.max(...Object.keys(headerRow).map(Number));
  const headers = [];
  for (let i = 0; i <= maxCol; i++) headers.push(headerRow[i] || `col_${i}`);

  const result = [];
  for (const rn of rowNums.slice(1)) {
    const cells = rowData[rn];
    const obj = {};
    for (let i = 0; i <= maxCol; i++) {
      obj[headers[i]] = cells[i] !== undefined ? cells[i] : "";
    }
    result.push(obj);
  }

  return result;
}

module.exports = { readExcel };
