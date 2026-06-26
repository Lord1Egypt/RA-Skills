/**
 * Zero-Dependency CSV Parser
 * Minimal CSV/TSV parser for air-gapped environments.
 *
 * @author Daryoosh Dehestani (https://github.com/dda-oo)
 * @organization RadarRoster (https://radarroster.com)
 * @license CC-BY-4.0
 *
 * Features:
 *   - No external dependencies
 *   - Handles quoted fields and escaped quotes
 *   - UTF-8 BOM support
 *   - Tab-separated and comma-separated formats
 */

"use strict";

/**
 * Parse a CSV/TSV string into an array of objects (keyed by header row).
 * @param {string} content - raw file content
 * @param {object} opts    - { delimiter: ',' | '\t', trim: true }
 * @returns {Array<Object>}
 */
function parse(content, opts = {}) {
  // Strip UTF-8 BOM if present
  if (content.charCodeAt(0) === 0xfeff) content = content.slice(1);

  const delimiter = opts.delimiter || (content.includes("\t") ? "\t" : ",");
  const shouldTrim = opts.trim !== false;

  const lines = content.split(/\r?\n/);
  const result = [];

  // Parse a single line into fields, respecting quoted strings
  function parseLine(line) {
    const fields = [];
    let field = "";
    let inQuotes = false;

    for (let i = 0; i < line.length; i++) {
      const ch = line[i];

      if (inQuotes) {
        if (ch === '"') {
          if (line[i + 1] === '"') {
            field += '"';
            i++;
          } else {
            inQuotes = false;
          }
        } else {
          field += ch;
        }
      } else {
        if (ch === '"') {
          inQuotes = true;
        } else if (ch === delimiter) {
          fields.push(shouldTrim ? field.trim() : field);
          field = "";
        } else {
          field += ch;
        }
      }
    }
    fields.push(shouldTrim ? field.trim() : field);
    return fields;
  }

  let headers = null;
  for (const line of lines) {
    if (!line.trim()) continue;
    const fields = parseLine(line);
    if (!headers) {
      headers = fields;
      continue;
    }
    const row = {};
    for (let i = 0; i < headers.length; i++) {
      row[headers[i]] = fields[i] !== undefined ? fields[i] : "";
    }
    result.push(row);
  }

  return result;
}

module.exports = { parse };
