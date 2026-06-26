#!/usr/bin/env node
// wip-release/mcp-server.mjs
// MCP server exposing release pipeline as tools.
// Wraps core.mjs. Registered via .mcp.json.

import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import { CallToolRequestSchema, ListToolsRequestSchema } from '@modelcontextprotocol/sdk/types.js';
import {
  release, detectCurrentVersion, bumpSemver, buildReleaseNotes,
} from './core.mjs';

const server = new Server(
  { name: 'wip-release', version: '1.3.0' },
  { capabilities: { tools: {} } }
);

// ── Tool Definitions ──

server.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools: [
    {
      name: 'release',
      description: 'Run the full release pipeline. Bumps version, updates changelog + SKILL.md, commits, tags, publishes to npm + GitHub. Must be run from repo root or provide repoPath.',
      inputSchema: {
        type: 'object',
        properties: {
          repoPath: { type: 'string', description: 'Absolute path to the repo. Defaults to cwd.' },
          level: { type: 'string', enum: ['patch', 'minor', 'major'], description: 'Semver bump level' },
          notes: { type: 'string', description: 'Changelog entry and release notes summary' },
          dryRun: { type: 'boolean', description: 'Preview only, no changes', default: false },
          noPublish: { type: 'boolean', description: 'Bump + tag only, skip npm/GitHub publish', default: false },
          skipProductCheck: { type: 'boolean', description: 'Skip product doc freshness check', default: false },
          skipTechDocsCheck: { type: 'boolean', description: 'Skip technical docs freshness check', default: false },
          skipCoverageCheck: { type: 'boolean', description: 'Skip interface coverage table check', default: false },
        },
        required: ['level', 'notes'],
      },
    },
    {
      name: 'release_status',
      description: 'Check current version and what the next version would be for a given bump level.',
      inputSchema: {
        type: 'object',
        properties: {
          repoPath: { type: 'string', description: 'Absolute path to the repo. Defaults to cwd.' },
          level: { type: 'string', enum: ['patch', 'minor', 'major'], description: 'Semver bump level to preview' },
        },
        required: ['level'],
      },
    },
  ],
}));

// ── Tool Handlers ──

server.setRequestHandler(CallToolRequestSchema, async (req) => {
  const { name, arguments: args } = req.params;

  if (name === 'release') {
    try {
      const result = await release({
        repoPath: args.repoPath || process.cwd(),
        level: args.level,
        notes: args.notes,
        dryRun: args.dryRun || false,
        notesSource: 'flag', // MCP always passes notes directly
        noPublish: args.noPublish || false,
        skipProductCheck: args.skipProductCheck || false,
        skipTechDocsCheck: args.skipTechDocsCheck || false,
        skipCoverageCheck: args.skipCoverageCheck || false,
      });
      return {
        content: [{
          type: 'text',
          text: `Release complete: ${result.currentVersion} -> ${result.newVersion}${result.dryRun ? ' (dry run)' : ''}`,
        }],
      };
    } catch (err) {
      return {
        content: [{ type: 'text', text: `Release failed: ${err.message}` }],
        isError: true,
      };
    }
  }

  if (name === 'release_status') {
    try {
      const repoPath = args.repoPath || process.cwd();
      const current = detectCurrentVersion(repoPath);
      const next = bumpSemver(current, args.level);
      return {
        content: [{
          type: 'text',
          text: `Current: ${current}\nNext (${args.level}): ${next}`,
        }],
      };
    } catch (err) {
      return {
        content: [{ type: 'text', text: `Status check failed: ${err.message}` }],
        isError: true,
      };
    }
  }

  return {
    content: [{ type: 'text', text: `Unknown tool: ${name}` }],
    isError: true,
  };
});

const transport = new StdioServerTransport();
await server.connect(transport);
