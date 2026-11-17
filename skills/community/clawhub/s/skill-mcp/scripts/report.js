#!/usr/bin/env node
// Prints what the execution fence handed this script. Deliberately reports the
// NAMES of the environment variables and never their values: this output goes
// straight into a tool result, and nothing downstream redacts a script's stdout.
const report = {
  argv: process.argv.slice(2),
  cwd: process.cwd(),
  envNames: Object.keys(process.env).sort(),
  node: process.version,
};
process.stdout.write(`${JSON.stringify(report, null, 2)}\n`);
process.stderr.write('skill-mcp-demo: logs go to stderr; stdout is the result\n');
