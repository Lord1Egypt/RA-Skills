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

let flags;
try {
  ({ values: flags } = parseArgs({
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
    allowPositionals: false,
    strict: true,
  }));
} catch (error) {
  console.error(`Error: ${error.message}`);
  process.exit(1);
}

if (flags.help) {
  console.log(`Usage:
  node table.mjs --headers '["A","B"]' --rows '[["1","2"]]'
  echo '{"headers":["A","B"],"rows":[["1","2"]]}' | node table.mjs --stdin
  node table.mjs --json '{"headers":["A","B"],"rows":[["1","2"]]}'

Options:
  --headers JSON          Header row, bold by default
  --rows JSON             Data rows
  --json JSON             Single JSON input with headers and rows
  --stdin                 Read JSON input from stdin
  --align COL:ALIGN,...   Column alignments: left, center, right
  --wrap COL,...          Columns to wrap
  --bold-headers          Bold headers (default)
  --no-bold-headers       Plain headers
  --compact               Output minified JSON
  --blocks-only           Output just the blocks array`);
  process.exit(0);
}

// --- Parse input ---
let headers, rows;

function parseJsonArg(label, value) {
  try {
    return JSON.parse(value);
  } catch (error) {
    console.error(`Error: invalid JSON for ${label}: ${error.message}`);
    process.exit(1);
  }
}

if (flags.stdin) {
  const chunks = [];
  for await (const chunk of process.stdin) chunks.push(chunk);
  const input = parseJsonArg("--stdin", Buffer.concat(chunks).toString());
  headers = input.headers;
  rows = input.rows;
} else if (flags.json) {
  const input = parseJsonArg("--json", flags.json);
  headers = input.headers;
  rows = input.rows;
} else {
  headers = flags.headers ? parseJsonArg("--headers", flags.headers) : null;
  rows = flags.rows ? parseJsonArg("--rows", flags.rows) : [];
}

if (headers && !Array.isArray(headers)) {
  console.error("Error: headers must be a JSON array");
  process.exit(1);
}

if (!Array.isArray(rows) || rows.length === 0) {
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
  // Slack requires non-empty text in cells - use a zero-width space for empty
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
  if (!Array.isArray(row) && (!row || typeof row !== "object")) {
    console.error("Error: each row must be an array or object");
    process.exit(1);
  }
  tableRows.push(
    (Array.isArray(row) ? row : Object.values(row)).map(cell => rawCell(cell))
  );
}

// --- Column settings ---
let columnSettings;
const alignMap = {};
const wrapSet = new Set();

function parseColumnIndex(raw, flagName) {
  if (!/^\d+$/.test(String(raw))) {
    console.error(`Error: ${flagName} column must be a non-negative integer, got "${raw}"`);
    process.exit(1);
  }
  return Number(raw);
}

if (flags.align) {
  for (const part of flags.align.split(",")) {
    const [col, align] = part.split(":");
    const index = parseColumnIndex(col, "--align");
    if (!["left", "center", "right"].includes(align)) {
      console.error(`Error: invalid alignment "${align}" for column ${col}`);
      process.exit(1);
    }
    alignMap[index] = align;
  }
}
if (flags.wrap) {
  for (const col of flags.wrap.split(",")) {
    wrapSet.add(parseColumnIndex(col, "--wrap"));
  }
}

const numCols = tableRows[0]?.length ?? 0;
if (numCols === 0) {
  console.error("Error: table must have at least one column");
  process.exit(1);
}
if (numCols > 20) {
  console.error("Error: Slack table blocks support at most 20 columns");
  process.exit(1);
}
if (tableRows.length > 100) {
  console.error("Error: Slack table blocks support at most 100 rows");
  process.exit(1);
}
for (const [index, row] of tableRows.entries()) {
  if (row.length !== numCols) {
    console.error(`Error: row ${index} has ${row.length} columns; expected ${numCols}`);
    process.exit(1);
  }
}

for (const col of [...Object.keys(alignMap).map(Number), ...wrapSet]) {
  if (col >= numCols) {
    console.error(`Error: column ${col} is out of range for ${numCols} columns`);
    process.exit(1);
  }
}

if (Object.keys(alignMap).length > 0 || wrapSet.size > 0) {
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
