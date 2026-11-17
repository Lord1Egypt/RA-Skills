/**
 * Pure Node: parse Oracle TABLES.sql DDL export and write:
 *   - references/table-index.md (grouped names)
 *   - references/table-reference.md (per-table columns)
 * Usage (from skill dir): node scripts/gen-table-index.mjs
 *   --tables-sql <path>   input DDL file (default: resolveTablesSqlPath())
 *   --out <path>          override output (default: references/table-index.md next to this skill)
 *   --detail-out <path>   override output (default: references/table-reference.md)
 */
import fs from 'fs';
import path from 'path';
import { SKILL_ROOT, LOCAL_TABLES_SQL, resolveTablesSqlPath } from './lib/paths.mjs';

const DEFAULT_OUT = path.join(SKILL_ROOT, 'references', 'table-index.md');
const DEFAULT_DETAIL_OUT = path.join(SKILL_ROOT, 'references', 'table-reference.md');
const DEFAULT_REL_OUT = path.join(SKILL_ROOT, 'references', 'table-relationships.md');

const REGEN_HINT = [
  '> ```bash',
  '> npm run setup',
  '> # or: npm run table-index',
  '> ```',
].join('\n');

const DDL_LINE = /^\s*--\s+DDL for Table (\S+)\s*$/;
const DDL_LINE_GLOBAL = /^\s*--\s+DDL for Table (\S+)\s*$/gm;

/** Longer / more specific rules first. */
const GROUP_RULES = [
  { group: 'Security & access keys', test: (n) => /^(USER_|PERMISSION|FUNCTION_|USER_API_KEY|ACCESS_INFO)/.test(n) },
  { group: 'General ledger & statements', test: (n) => /^(ACCOUNT_STMT|ACCOUNT_MGR|GL_|JOURNAL_|BALANCE_SHEET|BALANCE_CURR|BALANCE_TRANSFER|CASH_FLOW_STMT|ACCOUNT_TYPE)/.test(n) },
  { group: 'Banking & payments', test: (n) => /^(BANK_|PAYMENT|CUST_PAYMENT|SUPP_PAYMENT|CUST_PDC|DEBIT_PAYMENT)/.test(n) },
  { group: 'Sales, AR, deliveries (customer)', test: (n) => /^(CUST_|CUSTOMER|SALE_|CREDIT_MEMO|DEBIT_NOTE|COUNTER_RECEIPT|DELIVERY|DELIVERER|APPROVED_CUST)/.test(n) },
  { group: 'Purchasing, AP, supplier', test: (n) => /^(SUPP_|SUPPLIER|PURCHASE_|PURCH_|VENDOR_)/.test(n) },
  { group: 'Inventory, warehouse, manufacturing', test: (n) => /^(INV_|INVENTORY|WAREHOUSE|TRANSFER|ASSEMBLY|BILL_OF_MATERIAL|STOCK_|PICK_|PACK_|PRODUCTION)/.test(n) },
  { group: 'Products, pricing, catalog', test: (n) => /^(PRODUCT|PRICE_LIST|BRAND|CATEGORY|UOM|BARCODE|ADVERTISEMENT|SKU|PROD_)/.test(n) },
  { group: 'Partners, tax, currency, terms', test: (n) => /^(PARTNER|CREDIT_TERM|CURRENCY|TAX|EXCHANGE_RATE|AREA|MEMBERSHIP)/.test(n) },
  { group: 'Orders & documents (shared)', test: (n) => /^(ORDER_|DOC_|INVOICE|SALE_INVOICE|PURCHASE_INVOICE|PO_|SO_)/.test(n) },
  { group: 'System & misc', test: (n) => /^(SYS_PAR|DEBUG|SEQUENCE|TMP_|TEMP_|BLOB_|NOTIF|EMAIL_|QUEUE|JOB)/.test(n) },
];

const ID_COLUMN_EXCLUDE = new Set([
  'JNL_ID',
  'CREATED_BY',
  'UPDATED_BY',
  'ACTION_BY',
  'WH_ADDED_BY',
  'SID',
]);

const STEM_ALIAS_MAP = {
  CUST: ['CUSTOMER'],
  SUPP: ['SUPPLIER'],
  PROD: ['PRODUCT'],
  WH: ['WAREHOUSE'],
  INV: ['INVENTORY'],
  PURCH: ['PURCHASE'],
  PO: ['PURCHASE_ORDER'],
  SO: ['SALE_ORDER'],
  UOM: ['UOM'],
};

const STEM_PREFIXES_TO_STRIP = [
  'REF_',
  'SRC_',
  'DEST_',
  'FROM_',
  'TO_',
  'OLD_',
  'NEW_',
];

const CURATED_RELATIONSHIPS = [
  {
    table: 'CUSTOMER',
    column: 'PARTNER_ID',
    target: 'PARTNER',
    reason: 'Customer master profile is rooted in partner.',
  },
  {
    table: 'SUPPLIER',
    column: 'PARTNER_ID',
    target: 'PARTNER',
    reason: 'Supplier master profile is rooted in partner.',
  },
  {
    table: 'SALE_ORDER',
    column: 'CUSTOMER_ID',
    target: 'CUSTOMER',
    reason: 'Sales orders belong to a customer.',
  },
  {
    table: 'SALE_INVOICE',
    column: 'CUSTOMER_ID',
    target: 'CUSTOMER',
    reason: 'Sales invoices belong to a customer.',
  },
  {
    table: 'SUPPLIER_PROD',
    column: 'SUPPLIER_ID',
    target: 'SUPPLIER',
    reason: 'Supplier product mappings belong to a supplier.',
  },
];

function parseArgs(argv) {
  let tablesSql = resolveTablesSqlPath() || LOCAL_TABLES_SQL;
  let out = DEFAULT_OUT;
  let detailOut = DEFAULT_DETAIL_OUT;
  let relOut = DEFAULT_REL_OUT;
  for (let i = 2; i < argv.length; i++) {
    if (argv[i] === '--tables-sql' && argv[i + 1]) {
      tablesSql = path.resolve(argv[++i]);
    } else if (argv[i] === '--out' && argv[i + 1]) {
      out = path.resolve(argv[++i]);
    } else if (argv[i] === '--detail-out' && argv[i + 1]) {
      detailOut = path.resolve(argv[++i]);
    } else if (argv[i] === '--rel-out' && argv[i + 1]) {
      relOut = path.resolve(argv[++i]);
    }
  }
  return { tablesSql, out, detailOut, relOut };
}

function extractTableNames(content) {
  const names = [];
  for (const line of content.split(/\r?\n/)) {
    const m = line.match(DDL_LINE);
    if (m) names.push(m[1]);
  }
  return names;
}

function parseTableColumns(content) {
  const byTable = new Map();
  const ddls = [...content.matchAll(DDL_LINE_GLOBAL)];
  for (let idx = 0; idx < ddls.length; idx++) {
    const tableName = ddls[idx][1];
    const sectionStart = ddls[idx].index ?? 0;
    const sectionEnd = idx + 1 < ddls.length ? (ddls[idx + 1].index ?? content.length) : content.length;
    const section = content.slice(sectionStart, sectionEnd);
    const createPos = section.search(/CREATE TABLE\b/i);
    if (createPos < 0) {
      byTable.set(tableName, []);
      continue;
    }
    const createSection = section.slice(createPos);
    const openIdx = createSection.indexOf('(');
    if (openIdx < 0) {
      byTable.set(tableName, []);
      continue;
    }

    let depth = 0;
    let closeIdx = -1;
    for (let i = openIdx; i < createSection.length; i++) {
      const ch = createSection[i];
      if (ch === '(') depth++;
      else if (ch === ')') {
        depth--;
        if (depth === 0) {
          closeIdx = i;
          break;
        }
      }
    }
    if (closeIdx < 0) {
      byTable.set(tableName, []);
      continue;
    }

    const columnsBlock = createSection.slice(openIdx + 1, closeIdx);
    const lines = columnsBlock.split(/\r?\n/);
    const columns = [];
    for (const rawLine of lines) {
      const line = rawLine.trim();
      if (!line) continue;
      if (!line.startsWith('"')) continue;
      const colMatch = line.match(/^"([^"]+)"\s+(.+?)\s*(?:,)?$/);
      if (!colMatch) continue;
      const colName = colMatch[1].trim();
      let colType = colMatch[2].trim();
      colType = colType.replace(/\s+NOT NULL$/i, '').trim();
      columns.push({ name: colName, type: colType });
    }
    byTable.set(tableName, columns);
  }
  return byTable;
}

function categorizeBase(name) {
  for (const { group, test } of GROUP_RULES) {
    if (test(name)) return group;
  }
  return 'Other / uncategorized';
}

function normalizeStem(stem) {
  let s = stem.toUpperCase().trim();
  for (const prefix of STEM_PREFIXES_TO_STRIP) {
    if (s.startsWith(prefix) && s.length > prefix.length) {
      s = s.slice(prefix.length);
    }
  }
  return s;
}

function buildCandidatesFromStem(rawStem) {
  const stem = normalizeStem(rawStem);
  const out = new Set([stem]);
  if (STEM_ALIAS_MAP[stem]) {
    for (const alt of STEM_ALIAS_MAP[stem]) out.add(alt);
  }
  if (stem.endsWith('IES') && stem.length > 3) out.add(`${stem.slice(0, -3)}Y`);
  if (stem.endsWith('S') && stem.length > 1) out.add(stem.slice(0, -1));
  if (!stem.endsWith('S')) out.add(`${stem}S`);
  return [...out];
}

function inferRelationships(baseTables, columnsByTable) {
  const baseSet = new Set(baseTables);
  const relByTable = new Map();
  const unresolved = [];

  for (const table of baseTables) {
    const cols = columnsByTable.get(table) || [];
    const parentRefs = [];
    const seenPairs = new Set();

    for (const col of cols) {
      const colName = col.name.toUpperCase();
      if (!colName.endsWith('_ID')) continue;
      if (ID_COLUMN_EXCLUDE.has(colName)) continue;
      if (colName === `${table}_ID`) continue;

      const stem = colName.slice(0, -3);
      const candidates = buildCandidatesFromStem(stem)
        .filter((c) => baseSet.has(c) && c !== table)
        .sort();

      if (candidates.length === 0) {
        unresolved.push({ table, column: col.name, stem });
        continue;
      }

      const target = candidates[0];
      const key = `${col.name}->${target}`;
      if (seenPairs.has(key)) continue;
      seenPairs.add(key);
      parentRefs.push({
        column: col.name,
        target,
        candidates,
        inferred: true,
      });
    }

    relByTable.set(table, {
      parentRefs,
      childRefs: [],
      noDetectedRelations: false,
    });
  }

  for (const rel of CURATED_RELATIONSHIPS) {
    if (!baseSet.has(rel.table) || !baseSet.has(rel.target)) continue;
    const info = relByTable.get(rel.table);
    const existing = info.parentRefs.find((r) => r.column === rel.column && r.target === rel.target);
    if (existing) {
      existing.inferred = false;
      existing.reason = rel.reason;
    } else {
      info.parentRefs.push({
        column: rel.column,
        target: rel.target,
        candidates: [rel.target],
        inferred: false,
        reason: rel.reason,
      });
    }
  }

  for (const table of baseTables) {
    const info = relByTable.get(table);
    for (const r of info.parentRefs) {
      const parentInfo = relByTable.get(r.target);
      parentInfo.childRefs.push({
        fromTable: table,
        viaColumn: r.column,
        inferred: r.inferred,
      });
    }
  }

  for (const table of baseTables) {
    const info = relByTable.get(table);
    info.parentRefs.sort((a, b) => a.column.localeCompare(b.column) || a.target.localeCompare(b.target));
    info.childRefs.sort((a, b) => a.fromTable.localeCompare(b.fromTable) || a.viaColumn.localeCompare(b.viaColumn));
    info.noDetectedRelations = info.parentRefs.length === 0 && info.childRefs.length === 0;
  }

  unresolved.sort((a, b) => a.table.localeCompare(b.table) || a.column.localeCompare(b.column));
  return { relByTable, unresolved };
}

function main() {
  const { tablesSql, out, detailOut, relOut } = parseArgs(process.argv);
  if (!fs.existsSync(tablesSql)) {
    console.error(`TABLES.sql not found: ${tablesSql}`);
    console.error('');
    console.error('  Pass the file explicitly:');
    console.error('    node scripts/gen-table-index.mjs --tables-sql /path/to/TABLES.sql');
    console.error('');
    console.error('  Or set SIMPLEERP_TABLES_SQL, or place DDL at schema/TABLES.sql.');
    console.error('');
    process.exit(1);
  }
  const content = fs.readFileSync(tablesSql, 'utf8');
  const all = extractTableNames(content);
  const columnsByTable = parseTableColumns(content);
  const journals = all.filter((n) => n.endsWith('_JNL'));
  const base = all.filter((n) => !n.endsWith('_JNL'));
  const { relByTable, unresolved } = inferRelationships(base, columnsByTable);

  const byGroup = new Map();
  for (const name of base) {
    const g = categorizeBase(name);
    if (!byGroup.has(g)) byGroup.set(g, []);
    byGroup.get(g).push(name);
  }
  for (const arr of byGroup.values()) arr.sort();

  const journalSet = new Set(journals);
  const pairedBase = base.filter((b) => journalSet.has(`${b}_JNL`));
  const unpairedJournals = journals.filter((j) => {
    const baseName = j.slice(0, -4);
    return !base.includes(baseName);
  });

  const lines = [];
  lines.push('# SimpleERP table index');
  lines.push('');
  lines.push('> **Generated file.** Regenerate after schema changes:');
  lines.push('>');
  lines.push(REGEN_HINT);
  lines.push('');
  lines.push('Schema in DDL export: **`SIMPLEERP`**. Object names are uppercase in Oracle.');
  lines.push('');
  lines.push('Full column definitions: search your `TABLES.sql` export for `--  DDL for Table YOUR_TABLE`.');
  lines.push('');
  lines.push('## Base tables by domain (heuristic groups)');
  lines.push('');
  lines.push('Groups are assigned by table-name rules in `scripts/gen-table-index.mjs`; use this file to discover names, not business boundaries.');
  lines.push('');

  const groupOrder = [...GROUP_RULES.map((r) => r.group), 'Other / uncategorized'];
  const seen = new Set();
  for (const g of groupOrder) {
    const list = byGroup.get(g);
    if (!list || list.length === 0) continue;
    seen.add(g);
    lines.push(`### ${g}`);
    lines.push('');
    for (const t of list) lines.push(`- ${t}`);
    lines.push('');
  }
  for (const [g, list] of byGroup) {
    if (seen.has(g)) continue;
    lines.push(`### ${g}`);
    lines.push('');
    for (const t of list) lines.push(`- ${t}`);
    lines.push('');
  }

  lines.push('## Journal (`*_JNL`) tables');
  lines.push('');
  lines.push('Change-history / audit snapshots. See [journal-pattern.md](journal-pattern.md).');
  lines.push('');
  lines.push(`- **Count:** ${journals.length} journal tables in this export.`);
  lines.push(`- **Base tables with a matching \`*_JNL\`:** ${pairedBase.length} (name pattern: \`TABLE\` → \`TABLE_JNL\`; some journals may not follow this if compound names).`);
  if (unpairedJournals.length) {
    lines.push(`- **Journal tables without same-stem base in export:** ${unpairedJournals.length} (inspect DDL).`);
  }
  lines.push('');
  lines.push('### All `*_JNL` names (sorted)');
  lines.push('');
  for (const t of [...journals].sort()) lines.push(`- ${t}`);
  lines.push('');

  fs.mkdirSync(path.dirname(out), { recursive: true });
  fs.writeFileSync(out, lines.join('\n'), 'utf8');

  const detailLines = [];
  detailLines.push('# SimpleERP table reference (columns)');
  detailLines.push('');
  detailLines.push('> **Generated file.** Regenerate after schema changes:');
  detailLines.push('>');
  detailLines.push(REGEN_HINT);
  detailLines.push('');
  detailLines.push('Schema in DDL export: **`SIMPLEERP`**. Object names are uppercase in Oracle.');
  detailLines.push('');
  detailLines.push(`Total tables in export: **${all.length}** (${base.length} base, ${journals.length} journal).`);
  detailLines.push('');
  detailLines.push('## Tables');
  detailLines.push('');

  for (const tableName of [...all].sort()) {
    detailLines.push(`### ${tableName}`);
    detailLines.push('');
    const cols = columnsByTable.get(tableName) || [];
    if (!cols.length) {
      detailLines.push('- _No columns parsed; check source DDL formatting._');
      detailLines.push('');
      continue;
    }
    for (const c of cols) {
      detailLines.push(`- \`${c.name}\` \`${c.type}\``);
    }
    detailLines.push('');
  }

  fs.mkdirSync(path.dirname(detailOut), { recursive: true });
  fs.writeFileSync(detailOut, detailLines.join('\n'), 'utf8');

  const relLines = [];
  relLines.push('# SimpleERP table relationships');
  relLines.push('');
  relLines.push('> **Generated file.** Regenerate after schema changes:');
  relLines.push('>');
  relLines.push(REGEN_HINT);
  relLines.push('');
  relLines.push('This file is heuristic. It infers likely links from `*_ID` columns, then applies curated business mappings for key entities.');
  relLines.push('');
  relLines.push(`Base tables processed: **${base.length}**.`);
  relLines.push(`Tables with no detected links: **${base.filter((t) => relByTable.get(t).noDetectedRelations).length}**.`);
  relLines.push(`Unresolved ID-like columns: **${unresolved.length}**.`);
  relLines.push('');
  relLines.push('## Curated business-critical links');
  relLines.push('');
  for (const c of CURATED_RELATIONSHIPS) {
    if (!relByTable.has(c.table)) continue;
    relLines.push(`- \`${c.table}.${c.column}\` -> \`${c.target}\` (${c.reason})`);
  }
  relLines.push('');
  relLines.push('## Relationships by table');
  relLines.push('');

  for (const tableName of [...base].sort()) {
    const info = relByTable.get(tableName);
    relLines.push(`### ${tableName}`);
    relLines.push('');
    relLines.push('- Parent references:');
    if (info.parentRefs.length === 0) {
      relLines.push('  - _none_');
    } else {
      for (const ref of info.parentRefs) {
        const sourceTag = ref.inferred ? 'inferred' : 'curated';
        relLines.push(`  - \`${ref.column}\` -> \`${ref.target}\` (${sourceTag})`);
      }
    }
    relLines.push('- Child references:');
    if (info.childRefs.length === 0) {
      relLines.push('  - _none_');
    } else {
      for (const ref of info.childRefs) {
        const sourceTag = ref.inferred ? 'inferred' : 'curated';
        relLines.push(`  - \`${ref.fromTable}.${ref.viaColumn}\` -> \`${tableName}\` (${sourceTag})`);
      }
    }
    if (info.noDetectedRelations) {
      relLines.push('- `no_detected_relations`: `true`');
    }
    relLines.push('');
  }

  relLines.push('## Unresolved ID-like columns');
  relLines.push('');
  if (unresolved.length === 0) {
    relLines.push('- _none_');
  } else {
    for (const item of unresolved) {
      relLines.push(`- \`${item.table}.${item.column}\` (stem: \`${item.stem}\`)`);
    }
  }
  relLines.push('');

  fs.mkdirSync(path.dirname(relOut), { recursive: true });
  fs.writeFileSync(relOut, relLines.join('\n'), 'utf8');
  console.error(`Wrote ${out} (${base.length} base, ${journals.length} journal tables)`);
  console.error(`Wrote ${detailOut} (${all.length} tables with column metadata)`);
  console.error(`Wrote ${relOut} (${base.length} base tables with inferred/curated links)`);
}

main();
