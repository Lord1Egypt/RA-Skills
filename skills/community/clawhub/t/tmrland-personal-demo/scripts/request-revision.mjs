#!/usr/bin/env node
import { tmrFetch, parseArgs } from "./_lib.mjs";

const { help, named, positional } = parseArgs(process.argv);
if (help || !positional[0] || !named.feedback) {
  console.error("Usage: request-revision.mjs <order-id> --feedback '...'");
  process.exit(2);
}

const data = await tmrFetch("POST", `/orders/${positional[0]}/request-revision`, { feedback: named.feedback });
console.log(JSON.stringify(data, null, 2));
