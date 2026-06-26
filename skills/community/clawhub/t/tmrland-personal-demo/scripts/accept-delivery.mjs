#!/usr/bin/env node
import { tmrFetch, parseArgs } from "./_lib.mjs";

const { help, positional } = parseArgs(process.argv);
if (help || !positional[0]) {
  console.error("Usage: accept-delivery.mjs <order-id>");
  process.exit(2);
}

const data = await tmrFetch("POST", `/orders/${positional[0]}/accept-delivery`);
console.log(`Delivery accepted for order ${positional[0]} — status: ${data.status}`);
console.log(JSON.stringify(data, null, 2));
