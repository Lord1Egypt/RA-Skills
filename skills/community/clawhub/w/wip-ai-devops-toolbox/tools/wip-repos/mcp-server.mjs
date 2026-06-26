#!/usr/bin/env node
// wip-repos/mcp-server.mjs
// MCP server exposing repo manifest reconciler as tools.
// Wraps core.mjs. Registered via .mcp.json.

import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import { CallToolRequestSchema, ListToolsRequestSchema } from '@modelcontextprotocol/sdk/types.js';
import {
  check, planSync, addRepo, moveRepo, generateReadmeTree,
} from './core.mjs';

const server = new Server(
  { name: 'wip-repos', version: '0.1.0' },
  { capabilities: { tools: {} } }
);

// ── Tool Definitions ──

server.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools: [
    {
      name: 'repos_check',
      description: 'Diff the filesystem against the manifest. Shows repos in manifest but not on disk, on disk but not in manifest, and matched.',
      inputSchema: {
        type: 'object',
        properties: {
          manifestPath: { type: 'string', description: 'Path to repos-manifest.json' },
          reposRoot: { type: 'string', description: 'Root directory containing repos' },
        },
        required: ['manifestPath', 'reposRoot'],
      },
    },
    {
      name: 'repos_sync_plan',
      description: 'Plan moves to reconcile filesystem with manifest. Matches repos by git remote URL. Returns planned moves without executing.',
      inputSchema: {
        type: 'object',
        properties: {
          manifestPath: { type: 'string', description: 'Path to repos-manifest.json' },
          reposRoot: { type: 'string', description: 'Root directory containing repos' },
        },
        required: ['manifestPath', 'reposRoot'],
      },
    },
    {
      name: 'repos_add',
      description: 'Add a repo to the manifest.',
      inputSchema: {
        type: 'object',
        properties: {
          manifestPath: { type: 'string', description: 'Path to repos-manifest.json' },
          repoPath: { type: 'string', description: 'Relative path in the manifest (e.g. ldm-os/utilities/my-tool)' },
          remote: { type: 'string', description: 'GitHub remote (e.g. wipcomputer/my-tool)' },
          description: { type: 'string', description: 'Short description' },
        },
        required: ['manifestPath', 'repoPath', 'remote'],
      },
    },
    {
      name: 'repos_move',
      description: 'Move a repo in the manifest from one path to another.',
      inputSchema: {
        type: 'object',
        properties: {
          manifestPath: { type: 'string', description: 'Path to repos-manifest.json' },
          fromPath: { type: 'string', description: 'Current manifest path' },
          toPath: { type: 'string', description: 'New manifest path' },
        },
        required: ['manifestPath', 'fromPath', 'toPath'],
      },
    },
    {
      name: 'repos_tree',
      description: 'Generate a markdown directory tree from the manifest.',
      inputSchema: {
        type: 'object',
        properties: {
          manifestPath: { type: 'string', description: 'Path to repos-manifest.json' },
        },
        required: ['manifestPath'],
      },
    },
  ],
}));

// ── Tool Handlers ──

server.setRequestHandler(CallToolRequestSchema, async (req) => {
  const { name, arguments: args } = req.params;

  try {
    if (name === 'repos_check') {
      const result = check(args.manifestPath, args.reposRoot);
      return {
        content: [{
          type: 'text',
          text: JSON.stringify(result, null, 2),
        }],
      };
    }

    if (name === 'repos_sync_plan') {
      const moves = planSync(args.manifestPath, args.reposRoot);
      return {
        content: [{
          type: 'text',
          text: moves.length === 0
            ? 'No moves needed. Filesystem matches manifest.'
            : JSON.stringify(moves.map(m => ({ from: m.from, to: m.to, remote: m.remote })), null, 2),
        }],
      };
    }

    if (name === 'repos_add') {
      const entry = addRepo(args.manifestPath, args.repoPath, args.remote, {
        description: args.description,
      });
      return {
        content: [{
          type: 'text',
          text: `Added ${args.repoPath} -> ${args.remote}`,
        }],
      };
    }

    if (name === 'repos_move') {
      moveRepo(args.manifestPath, args.fromPath, args.toPath);
      return {
        content: [{
          type: 'text',
          text: `Moved ${args.fromPath} -> ${args.toPath}`,
        }],
      };
    }

    if (name === 'repos_tree') {
      const tree = generateReadmeTree(args.manifestPath);
      return {
        content: [{ type: 'text', text: tree }],
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
