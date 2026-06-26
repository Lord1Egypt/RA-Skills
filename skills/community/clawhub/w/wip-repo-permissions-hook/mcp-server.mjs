#!/usr/bin/env node
// wip-repo-permissions-hook/mcp-server.mjs
// MCP server exposing repo visibility guard as tools.
// Wraps core.mjs. Registered via .mcp.json.

import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import { CallToolRequestSchema, ListToolsRequestSchema } from '@modelcontextprotocol/sdk/types.js';
import {
  checkPrivateCounterpart, auditOrg,
} from './core.mjs';

const server = new Server(
  { name: 'wip-repo-permissions', version: '1.0.0' },
  { capabilities: { tools: {} } }
);

// ── Tool Definitions ──

server.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools: [
    {
      name: 'repo_permissions_check',
      description: 'Check if a repo has a -private counterpart on GitHub. Required before making any repo public.',
      inputSchema: {
        type: 'object',
        properties: {
          org: { type: 'string', description: 'GitHub org (e.g. wipcomputer)' },
          repo: { type: 'string', description: 'Repo name (e.g. memory-crystal)' },
        },
        required: ['org', 'repo'],
      },
    },
    {
      name: 'repo_permissions_audit',
      description: 'Audit all public repos in a GitHub org for missing -private counterparts. Returns violations and passing repos.',
      inputSchema: {
        type: 'object',
        properties: {
          org: { type: 'string', description: 'GitHub org (e.g. wipcomputer)' },
        },
        required: ['org'],
      },
    },
  ],
}));

// ── Tool Handlers ──

server.setRequestHandler(CallToolRequestSchema, async (req) => {
  const { name, arguments: args } = req.params;

  try {
    if (name === 'repo_permissions_check') {
      const result = checkPrivateCounterpart(args.org, args.repo);
      return {
        content: [{
          type: 'text',
          text: `${result.allowed ? 'ALLOWED' : 'BLOCKED'}: ${result.reason}`,
        }],
      };
    }

    if (name === 'repo_permissions_audit') {
      const result = auditOrg(args.org);
      const lines = [];
      if (result.violations.length > 0) {
        lines.push(`${result.violations.length} violation(s):`);
        for (const v of result.violations) {
          lines.push(`  BLOCKED: ${v.name} - ${v.reason}`);
        }
      }
      lines.push(`${result.ok.length} repo(s) OK.`);
      return {
        content: [{ type: 'text', text: lines.join('\n') }],
      };
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
