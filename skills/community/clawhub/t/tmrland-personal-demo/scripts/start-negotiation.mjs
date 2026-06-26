#!/usr/bin/env node
import { tmrFetch, parseArgs } from "./_lib.mjs";

const { help, named } = parseArgs(process.argv);
if (help || !named.intention || !named.businesses) {
  console.error("Usage: start-negotiation.mjs --intention <id> --businesses <id1,id2,...>");
  process.exit(2);
}

const body = {
  intention_id: named.intention,
  business_ids: named.businesses.split(",").map((s) => s.trim()),
};

const data = await tmrFetch("POST", "/negotiations/", body);
console.log(`Negotiation sessions created:`);
for (const s of data.sessions ?? [data]) {
  console.log(`  - ${s.id} (business: ${s.business_id})`);
}
console.log(JSON.stringify(data, null, 2));
