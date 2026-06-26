#!/usr/bin/env node
import { buildRequestOptions, callJsonGet, parseArgs, parseCsvIdsToArray, printAndExit } from "./client.js";

const args = parseArgs(process.argv);
const options = buildRequestOptions(args);

if (!args["start-date"] || !args["end-date"]) {
  console.error(
    "Usage: ./report.js --api-key <key> --start-date YYYY-MM-DD --end-date YYYY-MM-DD [--base-url https://api.socialecho.net] [--team-id 123] [--lang zh_CN] [--time-type 1] [--group day] [--account-ids 1,2]"
  );
  process.exit(2);
}

const accountIds = parseCsvIdsToArray(args["account-ids"]);
const body = {
  start_date: args["start-date"],
  end_date: args["end-date"],
  time_type: Number(args["time-type"] ?? 1),
  group: args.group ?? ""
};
if (accountIds) body.account_ids = accountIds;

const result = await callJsonGet("/v1/report", body, options);

printAndExit(result);
