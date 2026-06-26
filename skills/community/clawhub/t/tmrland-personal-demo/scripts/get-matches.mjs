#!/usr/bin/env node
import { tmrFetch, parseArgs } from "./_lib.mjs";

const { help, positional } = parseArgs(process.argv);
if (help || !positional[0]) {
  console.error("Usage: get-matches.mjs <intention-id>");
  process.exit(2);
}

const data = await tmrFetch("GET", `/intentions/${positional[0]}/matches`);
const candidates = data.candidates ?? data.items ?? [];
console.log(`## Match Candidates (${candidates.length})\n`);
for (const c of candidates) {
  console.log(`- **${c.business_name_en ?? c.business_id}** — score: ${c.score ?? "N/A"}`);
  if (c.recall_sources) console.log(`  Sources: ${c.recall_sources.join(", ")}`);
  if (c.explanation) console.log(`  ${c.explanation.slice(0, 150)}`);
  console.log();
}
