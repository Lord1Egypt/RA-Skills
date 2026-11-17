#!/usr/bin/env node
import { buildRequestOptions, callJsonGet, parseArgs, printAndExit } from "./client.js";

const args = parseArgs(process.argv);
printAndExit(await callJsonGet("/v1/tiktokshop/music/genres", {}, buildRequestOptions(args)));
