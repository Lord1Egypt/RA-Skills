#!/usr/bin/env node
import { buildRequestOptions, callJsonGet, parseArgs, printAndExit } from "./client.js";

const args = parseArgs(process.argv);
const options = buildRequestOptions(args);

const page = Number(args.page ?? 1);
const type = Number(args.type ?? 1);

const result = await callJsonGet("/v1/account", { page, type }, options);
printAndExit(result);
