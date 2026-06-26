#!/usr/bin/env node

import { readFileSync } from "node:fs";

function main() {
  const input = readFileSync(0, "utf8");
  const payload = JSON.parse(input);
  console.log("[owner-dispatch-adapter-demo]");
  console.log(payload.summary || "");
}

main();
