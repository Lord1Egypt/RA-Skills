#!/usr/bin/env node
// Explicit local operation only: no subprocesses, network calls, or schedules.
const { run } = require("../lib/flavors/runtime");
try {
  console.log(JSON.stringify(run(process.argv.slice(2)), null, 2));
} catch (error) {
  console.error(
    error.code?.startsWith("FLAVOR_") ? error.code : "FLAVOR_OPERATION_FAILED",
  );
  process.exitCode = 1;
}
