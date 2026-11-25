#!/usr/bin/env node
// Lists slow (per-row) policies and the Supabase performance advisor's findings for one project.
// Usage: SUPABASE_ACCESS_TOKEN=sbp_... node rls-speed.mjs <project-ref>
// Exit code 1 when anything is found, so the app flow and reviews can gate on it.
import { readFileSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const ref = process.argv[2];
const token = process.env.SUPABASE_ACCESS_TOKEN;
if (!ref || !token) {
  console.error('usage: SUPABASE_ACCESS_TOKEN=sbp_... node rls-speed.mjs <project-ref>');
  process.exit(2);
}
const api = `https://api.supabase.com/v1/projects/${ref}`;
const headers = { Authorization: `Bearer ${token}`, 'Content-Type': 'application/json' };
const sql = readFileSync(path.join(path.dirname(fileURLToPath(import.meta.url)), 'rls-speed.sql'), 'utf8');

const rows = await (await fetch(`${api}/database/query`, { method: 'POST', headers, body: JSON.stringify({ query: sql }) })).json();
if (!Array.isArray(rows)) throw new Error(JSON.stringify(rows));
const adv = await (await fetch(`${api}/advisors/performance`, { headers })).json().catch(() => ({}));
const lints = (adv.lints ?? []).filter((l) => ['auth_rls_initplan', 'unindexed_foreign_keys', 'multiple_permissive_policies'].includes(l.name));

for (const r of rows) console.log(`per-row policy  ${r.schemaname}.${r.tablename}  "${r.policyname}" (${r.cmd}): ${r.condition.trim()}`);
for (const l of lints) console.log(`advisor ${l.name}  ${l.detail ?? l.title}`);
if (rows.length + lints.length === 0) console.log('no per-row policies found');
process.exit(rows.length + lints.filter((l) => l.name === 'auth_rls_initplan').length > 0 ? 1 : 0);
