#!/usr/bin/env node
import { setApiBaseUrl } from "./config.js";
import { runCli } from "./cli.js";

setApiBaseUrl("https://api.useselva.com");

runCli(process.argv).catch((error) => {
  console.error(error instanceof Error ? error.message : String(error));
  process.exit(1);
});
