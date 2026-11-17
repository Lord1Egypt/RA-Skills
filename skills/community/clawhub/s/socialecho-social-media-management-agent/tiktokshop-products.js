#!/usr/bin/env node
import { buildRequestOptions, callJsonGet, getOption, parseArgs, printAndExit } from "./client.js";

const args = parseArgs(process.argv);
const params = {
  account_id: Number(getOption(args, "account-id")),
  page: Number(args.page ?? 1),
  per_page: Number(args["per-page"] ?? 20),
  keyword: args.keyword
};
printAndExit(await callJsonGet("/v1/tiktokshop/products", params, buildRequestOptions(args)));
