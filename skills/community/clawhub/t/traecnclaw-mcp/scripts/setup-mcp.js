#!/usr/bin/env node
'use strict';

const fs = require('fs');
const path = require('path');
const { resolveServerPath } = require('./start-mcp');

const DEFAULT_SKILL_DIR = path.resolve(__dirname, '..');

function buildClientConfig({ skillDir = DEFAULT_SKILL_DIR } = {}) {
  const resolvedSkillDir = path.resolve(skillDir);
  const templatePath = path.join(resolvedSkillDir, 'assets', 'mcp-client-config.json');
  const template = JSON.parse(fs.readFileSync(templatePath, 'utf8'));
  template.mcpServers.traecn.args = [
    path.join(resolvedSkillDir, 'scripts', 'start-mcp.js')
  ];
  return template;
}

function parseArgs(argv = []) {
  const options = { output: null, help: false };
  for (let index = 0; index < argv.length; index += 1) {
    const arg = argv[index];
    if (arg === '--help' || arg === '-h') {
      options.help = true;
      continue;
    }
    if (arg === '--output' || arg === '-o') {
      const value = argv[index + 1];
      if (!value || value.startsWith('-')) throw new Error(`${arg} requires a file path`);
      options.output = path.resolve(value);
      index += 1;
      continue;
    }
    throw new Error(`Unknown option: ${arg}`);
  }
  return options;
}

function writeClientConfig(outputPath, config) {
  const resolvedOutput = path.resolve(outputPath);
  const outputDir = path.dirname(resolvedOutput);
  const tempPath = `${resolvedOutput}.tmp-${process.pid}-${Date.now()}`;
  if (fs.existsSync(resolvedOutput)) {
    throw new Error(`Output already exists: ${resolvedOutput}`);
  }
  fs.mkdirSync(outputDir, { recursive: true });
  let fd;
  try {
    fd = fs.openSync(tempPath, 'wx', 0o600);
    fs.writeFileSync(fd, `${JSON.stringify(config, null, 2)}\n`, 'utf8');
    fs.fsyncSync(fd);
    fs.closeSync(fd);
    fd = undefined;
    fs.linkSync(tempPath, resolvedOutput);
    fs.unlinkSync(tempPath);
    const dirFd = fs.openSync(outputDir, 'r');
    try {
      fs.fsyncSync(dirFd);
    } finally {
      fs.closeSync(dirFd);
    }
    return resolvedOutput;
  } catch (error) {
    if (fd !== undefined) fs.closeSync(fd);
    try {
      fs.unlinkSync(tempPath);
    } catch {}
    if (error.code === 'EEXIST') {
      throw new Error(`Output already exists: ${resolvedOutput}`);
    }
    throw error;
  }
}

function main(argv = process.argv.slice(2)) {
  const options = parseArgs(argv);
  if (options.help) {
    process.stdout.write([
      'Usage: setup-mcp.js [--output FILE]',
      '',
      'Validate the matching TRAECNclaw server and render an MCP client config.',
      'Without --output, the JSON config is printed to stdout.',
      'With --output, a new file is written atomically and existing files are never overwritten.',
      ''
    ].join('\n'));
    return;
  }
  const config = buildClientConfig();
  const launcherPath = config.mcpServers.traecn.args[0];
  if (!fs.existsSync(launcherPath) || !fs.statSync(launcherPath).isFile()) {
    throw new Error(`MCP launcher is missing: ${launcherPath}`);
  }
  const serverPath = resolveServerPath();
  if (!serverPath) {
    throw new Error(
      'TRAECNclaw server is not installed. Install the matching server package or run setup from a source checkout.'
    );
  }
  process.stderr.write(`[setup-mcp] server ready: ${serverPath}\n`);
  if (options.output) {
    const writtenPath = writeClientConfig(options.output, config);
    process.stdout.write(`[setup-mcp] wrote ${writtenPath}\n`);
    return;
  }
  process.stdout.write(`${JSON.stringify(config, null, 2)}\n`);
}

if (require.main === module) {
  try {
    main();
  } catch (error) {
    process.stderr.write(`[setup-mcp] ERROR ${error.message}\n`);
    process.exitCode = 1;
  }
}

module.exports = { buildClientConfig, main, parseArgs, writeClientConfig };
