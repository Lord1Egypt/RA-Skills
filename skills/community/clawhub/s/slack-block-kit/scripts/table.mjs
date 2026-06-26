#!/usr/bin/env node
/**
 * Generate Slack Block Kit table JSON from simple input.
 *
 * Usage:
 *   node table.mjs --headers '["Source","Gross In","Net"]' --rows '[["Mochary","$11K","$8.5K"],["MHC","$13.4K","$6.7K"]]'
 *   echo '{"headers":["A","B"],"rows":[["1","2"]]}' | node table.mjs --stdin
 *   node table.mjs --json '{"headers":["A","B"],"rows":[["1","2"]]}'
 *
 * Options:
 *   --bold-headers     Bold the first row (default: true)
 *   --no-bold-headers  Don't bold the first row
 *   --align <col:align,...>  Column alignments (e.g. "1:right,2:center")
 *   --wrap <col,...>   Columns to wrap (e.g. "0,2")
 *   --compact          Output minified JSON
 *   --blocks-only      Output just the blocks array (default: full payload with blocks key)
 */

import { parseArgs } from "node:util";

const { values: flags, positionals } = parseArgs({
  options: {
    headers:        { type: "string" },
    rows:           { type: "string" },
    json:           { type: "string" },
    stdin:          { type: "boolean", default: false },
    "bold-headers": { type: "boolean", default: true },
    "no-bold-headers": { type: "boolean", default: false },
    align:          { type: "string" },
    wrap:           { type: "string" },
    compact:        { type: "boolean", default: false },
    "blocks-only":  { type: "boolean", default: false },
    help:           { type: "boolean", short: "h", default: false },
  },
  allowPositionals: true,
  strict: false,
});

if (flags.help) {
  console.log(`Usage: node table.mjs --headers '[...]' --rows '[[...],...]'
       echo '{"headers":[...],"rows":[[...],...]}' | node table.mjs --stdin
       node table.mjs --json '{"headers":[...],"rows":[[...],...]}'`);
  process.exit(0);
}

// --- Parse input ---
let headers, rows;

if (flags.stdin) {
  const chunks = [];
  for await (const chunk of process.stdin) chunks.push(chunk);
  const input = JSON.parse(Buffer.concat(chunks).toString());
  headers = input.headers;
  rows = input.rows;
} else if (flags.json) {
  const input = JSON.parse(flags.json);
  headers = input.headers;
  rows = input.rows;
} else {
  headers = flags.headers ? JSON.parse(flags.headers) : null;
  rows = flags.rows ? JSON.parse(flags.rows) : [];
}

if (!rows || rows.length === 0) {
  console.error("Error: no rows provided");
  process.exit(1);
}

// --- Build cells ---
const boldHeaders = flags["bold-headers"] && !flags["no-bold-headers"];

function textCell(text, bold = false) {
  const elements = [{
    type: "rich_text_section",
    elements: [{
      type: "text",
      text: String(text ?? ""),
      ...(bold ? { style: { bold: true } } : {}),
    }],
  }];
  return { type: "rich_text", elements };
}

function rawCell(text) {
  const str = String(text ?? "");
  // Slack requires non-empty text in cells — use a zero-width space for empty
  return { type: "raw_text", text: str || "\u200B" };
}

// --- Build rows ---
const tableRows = [];

if (headers) {
  tableRows.push(
    headers.map(h => boldHeaders ? textCell(h, true) : rawCell(h))
  );
}

for (const row of rows) {
  tableRows.push(
    (Array.isArray(row) ? row : Object.values(row)).map(cell => rawCell(cell))
  );
}

// --- Column settings ---
let columnSettings;
const alignMap = {};
const wrapSet = new Set();

if (flags.align) {
  for (const part of flags.align.split(",")) {
    const [col, align] = part.split(":");
    alignMap[Number(col)] = align;
  }
}
if (flags.wrap) {
  for (const col of flags.wrap.split(",")) {
    wrapSet.add(Number(col));
  }
}

if (Object.keys(alignMap).length > 0 || wrapSet.size > 0) {
  const numCols = tableRows[0]?.length ?? 0;
  columnSettings = [];
  for (let i = 0; i < numCols; i++) {
    const setting = {};
    if (alignMap[i]) setting.align = alignMap[i];
    if (wrapSet.has(i)) setting.is_wrapped = true;
    columnSettings.push(setting);
  }
}

// --- Output ---
const tableBlock = {
  type: "table",
  rows: tableRows,
  ...(columnSettings ? { column_settings: columnSettings } : {}),
};

const output = flags["blocks-only"]
  ? [tableBlock]
  : { blocks: [tableBlock] };

console.log(JSON.stringify(output, null, flags.compact ? 0 : 2));
