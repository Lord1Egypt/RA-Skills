#!/usr/bin/env node
import { buildRequestOptions, callJsonGet, parseArgs, printAndExit } from "./client.js";

const args = parseArgs(process.argv);
const options = buildRequestOptions(args);
const result = await callJsonGet("/v1/team", {}, options);
printAndExit(result);
