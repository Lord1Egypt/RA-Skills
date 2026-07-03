#!/usr/bin/env node
// Public agent lookup via /explorer/agents (no auth). Pass a name fragment or
// id-like string; for the full private DTO use:
//   node scripts/aacp-api.mjs GET /api/v1/agents/<id> --auth session
import { getJson, main, printJson, usage } from "./aacp-http.mjs";

if (process.argv.length !== 3) {
  usage("Usage: node scripts/aacp-agent.mjs <name-or-query>");
}

await main(async () => {
  printJson(await getJson(`/explorer/agents?query=${encodeURIComponent(process.argv[2])}&pageSize=5`));
});
