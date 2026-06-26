#!/usr/bin/env node
import { buildRequestOptions, callJsonGet, parseArgs, parseCsvIdsToArray, printAndExit } from "./client.js";

const args = parseArgs(process.argv);
const options = buildRequestOptions(args);
const page = Number(args.page ?? 1);
const accountIds = parseCsvIdsToArray(args["account-ids"]);

const body = { page };
if (accountIds) body.account_ids = accountIds;

const result = await callJsonGet("/v1/article", body, options);

printAndExit(result);
