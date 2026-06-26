#!/usr/bin/env node
import { tmrFetch, parseArgs } from "./_lib.mjs";

const { help, positional } = parseArgs(process.argv);
if (help || !positional[0]) {
  console.error("Usage: mark-negotiation-read.mjs <session-id>");
  process.exit(2);
}

await tmrFetch("POST", `/negotiations/${positional[0]}/messages/read`);
console.log(`Negotiation ${positional[0]} messages marked as read.`);
