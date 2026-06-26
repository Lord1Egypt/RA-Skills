#!/usr/bin/env node
import { tmrFetch, parseArgs } from "./_lib.mjs";

const { help, named } = parseArgs(process.argv);
if (help || !named.content) {
  console.error('Usage: quick-search.mjs --content "Need an NLP model for sentiment analysis"');
  process.exit(2);
}

const data = await tmrFetch("POST", "/intentions/search", { content: named.content });
console.log(JSON.stringify(data, null, 2));
