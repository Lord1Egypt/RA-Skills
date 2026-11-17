#!/usr/bin/env node
import { buildRequestOptions, callJsonPost, getOption, parseArgs, printAndExit } from "./client.js";

const args = parseArgs(process.argv);
const accountId = Number(getOption(args, "account-id"));
if (!Number.isInteger(accountId) || accountId < 1) {
  throw new Error("--account-id must be a positive integer");
}
if (args.execute !== true) {
  console.log(JSON.stringify({
    ok: true,
    dry_run: true,
    action: "sync_tiktokshop_products",
    preview: { account_id: accountId },
    next: `After explicit user authorization for this account, rerun with --execute --confirm-account-id ${accountId}`
  }, null, 2));
  process.exit(0);
}
const confirmedAccountId = Number(getOption(args, "confirm-account-id"));
if (confirmedAccountId !== accountId) {
  throw new Error(`--confirm-account-id must match --account-id (${accountId})`);
}
printAndExit(await callJsonPost(
  "/v1/tiktokshop/products/sync",
  { account_id: accountId },
  buildRequestOptions(args)
));
