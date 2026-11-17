#!/usr/bin/env node
// Imports reviewed local exports only; never reads credentials or starts a sync job.
const { run } = require("../lib/projects/runtime");
run(process.argv.slice(2))
  .then((result) => console.log(JSON.stringify(result, null, 2)))
  .catch((error) => {
    console.error(
      error.code?.startsWith("PROJECT_")
        ? error.code
        : "PROJECT_OPERATION_FAILED",
    );
    process.exitCode = 1;
  });
