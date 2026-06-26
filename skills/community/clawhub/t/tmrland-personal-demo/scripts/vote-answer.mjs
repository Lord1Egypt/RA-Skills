#!/usr/bin/env node
import { tmrFetch, parseArgs } from "./_lib.mjs";

const { help, named, positional } = parseArgs(process.argv);
if (help || !positional[0] || !named.direction) {
  console.error("Usage: vote-answer.mjs <answer-id> --direction like|dislike");
  process.exit(2);
}

const data = await tmrFetch("POST", `/apparatus/answers/${positional[0]}/${named.direction}`);
console.log(JSON.stringify(data, null, 2));
