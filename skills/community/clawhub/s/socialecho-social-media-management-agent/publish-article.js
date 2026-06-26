#!/usr/bin/env node
import fs from "node:fs";

import { buildRequestOptions, callJsonPost, getOption, parseArgs, printAndExit } from "./client.js";

const args = parseArgs(process.argv);
const options = buildRequestOptions(args);
const payloadPath = getOption(args, "payload");

let body;
try {
  const raw = fs.readFileSync(payloadPath, "utf8");
  body = JSON.parse(raw);
} catch (e) {
  console.error(`Failed to read/parse --payload JSON file: ${payloadPath}`);
  console.error(e?.message || e);
  process.exit(2);
}

const result = await callJsonPost("/v1/publish/article", body, options);
printAndExit(result);
