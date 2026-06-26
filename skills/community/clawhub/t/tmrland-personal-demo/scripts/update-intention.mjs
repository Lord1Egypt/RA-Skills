#!/usr/bin/env node
import { tmrFetch, parseArgs } from "./_lib.mjs";

const { help, named, positional } = parseArgs(process.argv);
if (help || !positional[0]) {
  console.error("Usage: update-intention.mjs <intention-id> [--title '...'] [--description '...']");
  process.exit(2);
}

const body = {};
if (named.title) body.title = named.title;
if (named.description) body.description = named.description;

const data = await tmrFetch("PATCH", `/intentions/${positional[0]}`, body);
console.log(JSON.stringify(data, null, 2));
