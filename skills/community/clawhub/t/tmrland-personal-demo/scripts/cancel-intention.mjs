#!/usr/bin/env node
import { tmrFetch, parseArgs } from "./_lib.mjs";

const { help, positional } = parseArgs(process.argv);
if (help || !positional[0]) {
  console.error("Usage: cancel-intention.mjs <intention-id>");
  process.exit(2);
}

const data = await tmrFetch("POST", `/intentions/${positional[0]}/cancel`);
console.log(`Intention ${positional[0]} cancelled — status: ${data.status}`);
console.log(JSON.stringify(data, null, 2));
