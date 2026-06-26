#!/usr/bin/env node
import { tmrFetch, parseArgs } from "./_lib.mjs";

const { help, named } = parseArgs(process.argv);
if (help) {
  console.error("Usage: list-questions.mjs [--limit N]");
  process.exit(2);
}

const limit = named.limit || "20";
const data = await tmrFetch("GET", `/apparatus/?limit=${limit}`);
console.log(JSON.stringify(data, null, 2));
