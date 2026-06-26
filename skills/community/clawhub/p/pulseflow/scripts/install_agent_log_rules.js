#!/usr/bin/env node
const { deriveRuntimePaths, loadJson } = require('./_common');
const { installAgentLogRules } = require('./_agent_log_rules');

function main() {
  const paths = deriveRuntimePaths();
  const config = loadJson(paths.configPath, null);
  if (!config) {
    throw new Error('Missing config.json: run init_system.js first');
  }

  const results = installAgentLogRules({ config, paths });
  process.stdout.write(`${JSON.stringify({ ok: true, results }, null, 2)}\n`);
}

main();
