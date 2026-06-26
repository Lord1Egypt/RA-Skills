#!/usr/bin/env node
import { tmrFetch, parseArgs } from "./_lib.mjs";

const { help, positional } = parseArgs(process.argv);
if (help || !positional[0]) {
  console.error("Usage: match-status.mjs <intention-id>");
  process.exit(2);
}

const data = await tmrFetch("GET", `/intentions/${positional[0]}/match/status`);
console.log(`## Match Status for ${positional[0]}\n`);
console.log(`Status: ${data.status}`);
if (data.started_at) console.log(`Started: ${data.started_at}`);
if (data.completed_at) console.log(`Completed: ${data.completed_at}`);
