#!/usr/bin/env node
import { tmrFetch, parseArgs } from "./_lib.mjs";

const { help } = parseArgs(process.argv);
if (help) {
  console.error("Usage: get-wallet.mjs");
  process.exit(2);
}

const data = await tmrFetch("GET", "/wallet");
console.log(`## Wallet\n`);
console.log(`USD: ${data.usd_balance ?? "0.00"}`);
console.log(`USDC: ${data.usdc_balance ?? "0.00"}`);
console.log(`\n${JSON.stringify(data, null, 2)}`);
