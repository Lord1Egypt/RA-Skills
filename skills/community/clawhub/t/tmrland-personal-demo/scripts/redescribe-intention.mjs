#!/usr/bin/env node
import { tmrFetch, parseArgs } from "./_lib.mjs";

const { help, named, positional } = parseArgs(process.argv);
if (help || !positional[0] || !named.content) {
  console.error("Usage: redescribe-intention.mjs <intention-id> --content '...' [--locale zh]");
  process.exit(2);
}

const body = { content: named.content };
if (named.locale) body.locale = named.locale;

const data = await tmrFetch("POST", `/intentions/${positional[0]}/redescribe`, body);
console.log(JSON.stringify(data, null, 2));
