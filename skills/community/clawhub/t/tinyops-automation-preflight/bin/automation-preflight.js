#!/usr/bin/env node
'use strict';

const fs = require('node:fs');
const path = require('node:path');
const { requestPreflight, redact } = require('../index.js');

function usage() {
  return `Usage: automation-preflight --url <public-url> [options]

Options:
  --mode <analyze|acceptance-pack>  Check mode (default: analyze)
  --objective <text>                Optional acceptance objective
  --output <path>                   Write JSON to a file instead of stdout
  --help                            Show this help

Set RAPIDAPI_KEY in the environment. The key is sent only to the RapidAPI gateway.`;
}

function parseArgs(argv) {
  const options = { mode: 'analyze', objective: '', output: '' };
  for (let index = 0; index < argv.length; index += 1) {
    const argument = argv[index];
    if (argument === '--help' || argument === '-h') options.help = true;
    else if (argument === '--url') options.url = argv[++index];
    else if (argument === '--mode') options.mode = argv[++index];
    else if (argument === '--objective') options.objective = argv[++index];
    else if (argument === '--output') options.output = argv[++index];
    else throw new Error(`unknown argument: ${argument}`);
  }
  return options;
}

function resolveOutput(raw) {
  const root = process.cwd();
  const output = path.resolve(root, raw);
  if (output !== root && !output.startsWith(`${root}${path.sep}`)) {
    throw new Error('output must stay inside the current working directory');
  }
  return output;
}

async function main() {
  const options = parseArgs(process.argv.slice(2));
  if (options.help) {
    process.stdout.write(`${usage()}\n`);
    return;
  }
  if (!options.url) throw new Error('--url is required');
  const rapidApiKey = process.env.RAPIDAPI_KEY || '';
  const result = await requestPreflight({
    rapidApiKey,
    url: options.url,
    mode: options.mode,
    objective: options.objective,
    apiBase: process.env.AUTOMATION_PREFLIGHT_API_BASE_URL,
  });
  const report = `${JSON.stringify(result.payload, null, 2)}\n`;
  if (options.output) {
    const outputPath = resolveOutput(options.output);
    fs.mkdirSync(path.dirname(outputPath), { recursive: true });
    fs.writeFileSync(outputPath, report, 'utf8');
    process.stderr.write(`Automation preflight complete: ${path.relative(process.cwd(), outputPath)}\n`);
  } else {
    process.stdout.write(report);
  }
}

main().catch((error) => {
  const safeMessage = redact(error?.message || error, [process.env.RAPIDAPI_KEY || '']).slice(0, 1000);
  process.stderr.write(`Automation preflight failed: ${safeMessage}\n`);
  process.exitCode = 1;
});
