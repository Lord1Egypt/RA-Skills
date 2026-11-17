#!/usr/bin/env node
// Bounded offline compiler: explicit JSON stdin -> display graph stdout. No writes or credentials.
const { compile } = require("../lib/work-graph");
const chunks = [];
let bytes = 0;
process.stdin.on("data", (chunk) => {
  bytes += chunk.length;
  if (bytes > 4 * 1024 * 1024) {
    console.error("WORK_GRAPH_INPUT_TOO_LARGE");
    process.exit(1);
  }
  chunks.push(chunk);
});
process.stdin.on("end", () => {
  try {
    console.log(
      JSON.stringify(
        compile(JSON.parse(Buffer.concat(chunks).toString("utf8"))),
        null,
        2,
      ),
    );
  } catch {
    console.error("WORK_GRAPH_INVALID_INPUT");
    process.exitCode = 1;
  }
});
