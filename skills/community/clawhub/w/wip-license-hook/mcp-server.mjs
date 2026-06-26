#!/usr/bin/env node
// wip-license-hook/mcp-server.mjs
// MCP server exposing license compliance scanning as tools.
// Wraps the compiled dist/ output. Registered via .mcp.json.

import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import { CallToolRequestSchema, ListToolsRequestSchema } from '@modelcontextprotocol/sdk/types.js';
import {
  scanAll, scanAndUpdate, gateCheck,
  readLedger, formatScanReport, formatLedgerReport,
} from './dist/core/index.js';

const server = new Server(
  { name: 'wip-license-hook', version: '1.0.0' },
  { capabilities: { tools: {} } }
);

// ── Tool Definitions ──

server.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools: [
    {
      name: 'license_scan',
      description: 'Scan a project for all dependency licenses. Returns a report of every dependency, its license, and any changes detected.',
      inputSchema: {
        type: 'object',
        properties: {
          repoPath: { type: 'string', description: 'Absolute path to the repo to scan' },
        },
        required: ['repoPath'],
      },
    },
    {
      name: 'license_audit',
      description: 'Scan and update the license ledger for a project. Detects license changes (rug-pulls) by comparing against the stored ledger.',
      inputSchema: {
        type: 'object',
        properties: {
          repoPath: { type: 'string', description: 'Absolute path to the repo to audit' },
        },
        required: ['repoPath'],
      },
    },
    {
      name: 'license_gate',
      description: 'Gate check: returns pass/fail for license compliance. Use before merging PRs or publishing.',
      inputSchema: {
        type: 'object',
        properties: {
          repoPath: { type: 'string', description: 'Absolute path to the repo to check' },
        },
        required: ['repoPath'],
      },
    },
    {
      name: 'license_ledger',
      description: 'Read the current license ledger for a project. Shows all tracked dependencies and their license status.',
      inputSchema: {
        type: 'object',
        properties: {
          repoPath: { type: 'string', description: 'Absolute path to the repo' },
        },
        required: ['repoPath'],
      },
    },
  ],
}));

// ── Tool Handlers ──

server.setRequestHandler(CallToolRequestSchema, async (req) => {
  const { name, arguments: args } = req.params;

  try {
    if (name === 'license_scan') {
      const results = await scanAll(args.repoPath);
      const report = formatScanReport(results);
      return { content: [{ type: 'text', text: report }] };
    }

    if (name === 'license_audit') {
      const results = await scanAndUpdate(args.repoPath);
      const report = formatScanReport(results);
      return { content: [{ type: 'text', text: report }] };
    }

    if (name === 'license_gate') {
      const result = await gateCheck(args.repoPath);
      return {
        content: [{
          type: 'text',
          text: result.pass
            ? `PASS: All licenses compliant.`
            : `FAIL: ${result.reason}`,
        }],
      };
    }

    if (name === 'license_ledger') {
      const ledger = readLedger(args.repoPath);
      const report = formatLedgerReport(ledger);
      return { content: [{ type: 'text', text: report }] };
    }

    return {
      content: [{ type: 'text', text: `Unknown tool: ${name}` }],
      isError: true,
    };
  } catch (err) {
    return {
      content: [{ type: 'text', text: `Error: ${err.message}` }],
      isError: true,
    };
  }
});

const transport = new StdioServerTransport();
await server.connect(transport);
