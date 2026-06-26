#!/usr/bin/env node
import { tmrFetch, parseArgs } from "./_lib.mjs";

const { help, positional, named } = parseArgs(process.argv);
if (help || !positional[0]) {
  console.error("Usage: pay-order.mjs <order-id> [--currency USD|USDC]");
  process.exit(2);
}

const currency = named.currency ?? "USD";
const data = await tmrFetch("POST", `/orders/${positional[0]}/pay`, { currency });
console.log(`Order ${data.id} paid (${currency}) — status: ${data.status}`);
console.log(JSON.stringify(data, null, 2));
