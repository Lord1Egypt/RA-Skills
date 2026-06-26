#!/usr/bin/env node
import { buildRequestOptions, callJsonGet, getOption, parseArgs, printAndExit } from "./client.js";

const args = parseArgs(process.argv);
const options = buildRequestOptions(args);
const accountId = Number(getOption(args, "account-id"));
if (Number.isNaN(accountId)) {
  console.error("Usage: ./reddit-communities.js --api-key <key> --account-id <int> [--base-url ...] [--team-id ...] [--lang ...]");
  process.exit(2);
}

const result = await callJsonGet("/v1/reddit/communities", { account_id: accountId }, options);
printAndExit(result);
