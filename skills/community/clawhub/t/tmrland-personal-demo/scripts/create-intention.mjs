#!/usr/bin/env node
import { tmrFetch, parseArgs } from "./_lib.mjs";

const { help, named } = parseArgs(process.argv);
if (help || !named.content) {
  console.error('Usage: create-intention.mjs --content "..." [--locale zh]');
  process.exit(2);
}

const body = {
  content: named.content,
};
if (named.locale) body.locale = named.locale;

const data = await tmrFetch("POST", "/intentions/", body);
console.log(`Intention created: ${data.id}`);
console.log(JSON.stringify(data, null, 2));
