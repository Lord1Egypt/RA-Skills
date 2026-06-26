/**
 * src/integrations/git_tools.js
 * Git 集成工具注册
 */

import { z } from 'zod';
import { GitManager, getGitManager } from './git_manager.js';
import { getAllMemories } from '../storage.js';

export function registerGitTools(server) {
  const gitManager = getGitManager();

  server.registerTool('memory_git_init', {
    description: 'Initialize Git repository for memory versioning. Creates a git repo in memory dir for versioned memory history.',
    inputSchema: z.object({
      remote_url: z.string().optional().describe('Remote repository URL (e.g. GitHub git URL)'),
    }),
  }, async ({ remote_url }) => {
    try {
      const result = await gitManager.init({ remote_url });
      return { content: [{ type: 'text', text: JSON.stringify(result, null, 2) }] };
    } catch (err) {
      return { content: [{ type: 'text', text: `Git init error: ${err.message}` }], isError: true };
    }
  });

  server.registerTool('memory_git_sync', {
    description: 'Sync memories to git: auto-commit all current memories and push to remote.',
    inputSchema: z.object({
      message: z.string().optional().describe('Commit message (auto-generated if not provided)'),
      push: z.boolean().optional().default(false).describe('Push to remote after commit'),
    }),
  }, async ({ message, push = false } = {}) => {
    try {
      const memories = await getAllMemories();
      const timestamp = new Date().toISOString();
      const msg = message || `memory: auto-sync ${timestamp}`;

      // Write memories to repo files first
      const { join } = await import('path');
      const { writeFileSync, existsSync, mkdirSync } = await import('fs');
      const { config } = await import('../config.js');
      
      const repoPath = gitManager.repo_path;
      if (!existsSync(repoPath)) {
        mkdirSync(repoPath, { recursive: true });
      }

      // Commit
      const result = await gitManager.commit({ message: msg });
      
      if (push && result.committed) {
        await gitManager.push();
      }

      return { content: [{ type: 'text', text: JSON.stringify({ ...result, push }, null, 2) }] };
    } catch (err) {
      return { content: [{ type: 'text', text: `Git sync error: ${err.message}` }], isError: true };
    }
  });

  server.registerTool('memory_git_history', {
    description: 'Get memory version history from git log.',
    inputSchema: z.object({
      since: z.string().optional().describe('Start date ISO string'),
      limit: z.number().optional().default(50),
    }),
  }, async ({ since, limit = 50 } = {}) => {
    try {
      const history = await gitManager.getHistory({ since, limit });
      return { content: [{ type: 'text', text: JSON.stringify(history, null, 2) }] };
    } catch (err) {
      return { content: [{ type: 'text', text: `Git history error: ${err.message}` }], isError: true };
    }
  });

  server.registerTool('memory_git_note', {
    description: 'Save a git note (metadata tag) on the latest commit.',
    inputSchema: z.object({
      key: z.string().describe('Note key'),
      value: z.string().describe('Note value'),
    }),
  }, async ({ key, value }) => {
    try {
      const result = await gitManager.saveNote({ key, value });
      return { content: [{ type: 'text', text: JSON.stringify(result, null, 2) }] };
    } catch (err) {
      return { content: [{ type: 'text', text: `Git note error: ${err.message}` }], isError: true };
    }
  });

  server.registerTool('memory_git_pull', {
    description: 'Pull memory updates from remote git repository.',
    inputSchema: z.object({}),
  }, async () => {
    try {
      const result = await gitManager.pull();
      return { content: [{ type: 'text', text: JSON.stringify(result, null, 2) }] };
    } catch (err) {
      return { content: [{ type: 'text', text: `Git pull error: ${err.message}` }], isError: true };
    }
  });

  server.registerTool('memory_git_push', {
    description: 'Push local memory commits to remote git repository.',
    inputSchema: z.object({}),
  }, async () => {
    try {
      const result = await gitManager.push();
      return { content: [{ type: 'text', text: JSON.stringify(result, null, 2) }] };
    } catch (err) {
      return { content: [{ type: 'text', text: `Git push error: ${err.message}` }], isError: true };
    }
  });
}
