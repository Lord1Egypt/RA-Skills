#!/usr/bin/env node
import { tmrFetch, parseArgs } from "./_lib.mjs";

const { help, positional } = parseArgs(process.argv);
if (help || !positional[0]) {
  console.error("Usage: delete-intention.mjs <intention-id>");
  process.exit(2);
}

await tmrFetch("DELETE", `/intentions/${positional[0]}`);
console.log(`Intention ${positional[0]} deleted.`);
