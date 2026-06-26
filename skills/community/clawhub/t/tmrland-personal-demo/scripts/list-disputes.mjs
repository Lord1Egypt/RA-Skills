#!/usr/bin/env node
import { tmrFetch, parseArgs } from "./_lib.mjs";

const { help, named } = parseArgs(process.argv);
if (help) {
  console.error("Usage: list-disputes.mjs [--limit N]");
  process.exit(2);
}

const limit = Number.parseInt(named.limit ?? "20", 10);
const data = await tmrFetch("GET", `/disputes/?limit=${limit}`);

console.log(`## Disputes (${data.items?.length ?? 0})\n`);
for (const d of data.items ?? []) {
  console.log(`- ${d.id} | ${d.status ?? "—"} | ${d.created_at ?? "—"}`);
}
console.log(JSON.stringify(data, null, 2));
