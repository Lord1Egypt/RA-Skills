#!/usr/bin/env node
import { buildRequestOptions, callJsonGet, getOption, parseArgs, printAndExit } from "./client.js";

const args = parseArgs(process.argv);
const params = {
  account_id: Number(getOption(args, "account-id")),
  country_code: args["country-code"],
  genre: args.genre,
  date_range: args["date-range"]
};
printAndExit(await callJsonGet("/v1/tiktokshop/music/trending", params, buildRequestOptions(args)));
