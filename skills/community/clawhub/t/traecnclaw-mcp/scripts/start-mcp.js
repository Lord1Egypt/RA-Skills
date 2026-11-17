#!/usr/bin/env node
'use strict';

/**
 * MCP server launcher for the traecnclaw-mcp skill.
 *
 * Locates and starts the TRAECNclaw stdio MCP server, inheriting stdio
 * so JSON-RPC messages flow directly between the MCP client and server.
 *
 * Resolution order:
 *   1. In-repo relative path (skill/scripts/ → repo root)
 *   2. Installed `@luckycat133/traecnclaw` package export
 *   3. Legacy installed `traecnclaw` package export
 *   4. `traecnclaw-mcp` executable on PATH
 *
 * Usage from an MCP client config:
 *   "command": "node",
 *   "args": ["/path/to/skills/traecnclaw-mcp/scripts/start-mcp.js"]
 */

const path = require('path');
const fs = require('fs');
const { createRequire } = require('module');

const SCRIPT_DIR = __dirname;

/**
 * Resolve the path to mcp-server.js.
 *
 * Checks the in-repo location, installed package export, and PATH launcher.
 * Each candidate is validated as an existing regular file so directories or
 * broken symlinks are rejected silently. An environment-selected JavaScript
 * path is deliberately unsupported because the launcher executes the result.
 *
 * @param {object} [env=process.env] - environment variables (injectable for tests)
 * @param {string} [scriptDir=__dirname] - scripts dir (injectable for tests)
 * @param {object} [options] - process values (injectable for tests)
 * @returns {string|null} absolute path to mcp-server.js, or null if not found
 */
function resolveServerPath(env = process.env, scriptDir = SCRIPT_DIR, options = {}) {
  const repoRoot = path.resolve(scriptDir, '../../..');
  const cwd = options.cwd || process.cwd();
  const platform = options.platform || process.platform;
  const candidates = [path.join(repoRoot, 'mcp-server.js')];

  try {
    const searchPaths = [cwd, scriptDir];
    if (env.NODE_PATH) searchPaths.push(...env.NODE_PATH.split(path.delimiter).filter(Boolean));
    for (const packageExport of ['@luckycat133/traecnclaw/mcp', 'traecnclaw/mcp']) {
      for (const searchPath of searchPaths) {
        try {
          const resolveFrom = createRequire(path.join(path.resolve(searchPath), 'package.json'));
          candidates.push(resolveFrom.resolve(packageExport));
          break;
        } catch {
          // Try the next package search root.
        }
      }
    }
  } catch {
    // The package channel is optional; continue to PATH resolution.
  }

  const pathEntries = String(env.PATH || '').split(path.delimiter).filter(Boolean);
  const executableNames = platform === 'win32'
    ? String(env.PATHEXT || '.EXE;.CMD;.BAT').split(';').map(ext => `traecnclaw-mcp${ext.toLowerCase()}`)
    : ['traecnclaw-mcp'];
  for (const entry of pathEntries) {
    for (const executableName of executableNames) {
      candidates.push(path.join(entry, executableName));
    }
  }

  for (const candidate of candidates) {
    try {
      if (fs.existsSync(candidate) && fs.statSync(candidate).isFile()) {
        return path.resolve(candidate);
      }
    } catch {
      // Ignore unreadable paths and try the next candidate.
    }
  }
  return null;
}

/**
 * Locate and start the stdio MCP server.
 *
 * Exits with a diagnostic message on any startup failure so MCP clients
 * see a clear error instead of a raw stack trace.
 *
 * @returns {void}
 */
function main() {
  const serverPath = resolveServerPath();

  if (!serverPath) {
    const repoRoot = path.resolve(SCRIPT_DIR, '../../..');
    const tried = [path.join(repoRoot, 'mcp-server.js')];
    console.error('[traecnclaw-mcp] mcp-server.js not found.');
    console.error('Tried: ' + tried.join(', '));
    console.error('Install the matching @luckycat133/traecnclaw package, add traecnclaw-mcp to PATH,');
    console.error('or install this skill inside the repository.');
    process.exit(1);
  }

  // Chdir to repo root so .env and relative file reads resolve correctly.
  try {
    process.chdir(path.dirname(serverPath));
  } catch (cause) {
    console.error(`[traecnclaw-mcp] Failed to set working directory: ${cause.message}`);
    process.exit(1);
  }

  let serverModule;
  try {
    serverModule = require(serverPath);
  } catch (cause) {
    console.error(`[traecnclaw-mcp] Failed to load mcp-server.js: ${cause.message}`);
    process.exit(1);
  }

  if (typeof serverModule.startStdioServer !== 'function') {
    console.error('[traecnclaw-mcp] mcp-server.js does not export startStdioServer().');
    process.exit(1);
  }

  serverModule.startStdioServer();
}

// Graceful shutdown: MCP clients (Cursor, Claude Desktop, etc.) send SIGTERM
// or SIGINT when closing the connection. Exit cleanly so no zombie processes
// or broken stdio pipes are left behind.
process.once('SIGINT', () => process.exit(0));
process.once('SIGTERM', () => process.exit(0));

// Only run main when invoked directly, not when required for testing.
if (require.main === module) {
  main();
}

module.exports = { resolveServerPath, main };
