#!/usr/bin/env node
import { tmrFetch, parseArgs } from "./_lib.mjs";

const { help, named } = parseArgs(process.argv);
if (help) {
  console.error("Usage: list-intentions.mjs [--limit N]");
  process.exit(2);
}

const limit = Number.parseInt(named.limit ?? "20", 10);
const data = await tmrFetch("GET", `/intentions/?limit=${limit}`);

console.log(`## Intentions (${data.items?.length ?? 0})\n`);
for (const i of data.items ?? []) {
  console.log(`- ${i.id} | ${i.status} | ${i.content?.slice(0, 80) ?? "—"}`);
}
