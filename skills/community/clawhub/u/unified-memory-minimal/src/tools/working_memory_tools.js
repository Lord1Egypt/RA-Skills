/**
 * tools/working_memory_tools.js - MCP Tools for Working Memory
 * 
 * Registers the following tools:
 * - memory_working_start   Create a new working memory
 * - memory_working_list    List active working memories
 * - memory_working_get     Get a specific working memory
 * - memory_working_hold    Hold (pause) a working memory
 * - memory_working_resume  Resume a held working memory
 * - memory_working_clear   Explicitly clear a working memory
 * - memory_working_extend  Extend TTL
 * - memory_working_context Update context window
 * - memory_working_tree    Get task hierarchy tree
 */

import { z } from 'zod';
import {
  create,
  hold,
  resume,
  clear,
  extend,
  getActive,
  get,
  updateContext,
} from '../working_memory_manager.js';
import {
  buildTaskTree,
  getSubtasks,
  getAncestry,
  getDescendants,
  linkToEpisode,
  getWorkingMemoriesByEpisode,
  visualizeTaskTree,
} from '../task_hierarchy.js';

/**
 * Register working memory tools with MCP server
 * @param {import('@modelcontextprotocol/sdk').McpServer} server
 */
export function registerWorkingMemoryTools(server) {

  // ─── memory_working_start ───────────────────────────────────────────────
  server.registerTool('memory_working_start', {
    description: 'Start a new working memory for a task you are currently working on. Working memory is short-term, task-focused context that auto-expires after 2 hours. Use this when actively working on something specific.',
    inputSchema: z.object({
      task: z.string().describe('Description of the current task'),
      context: z.string().optional().describe('Additional context/details about the task'),
      ttl_ms: z.number().optional().describe('Custom TTL in milliseconds (default: 2 hours)'),
      task_id: z.string().optional().describe('Custom task ID'),
      episode_id: z.string().optional().describe('Episode/session ID to link with episodic memory'),
      parent_task_id: z.string().optional().describe('Parent task ID for subtask hierarchy'),
    }),
  }, async ({ task, context = '', ttl_ms = null, task_id = null, episode_id = null, parent_task_id = null }) => {
    try {
      const result = create({
        taskDescription: task,
        taskId: task_id,
        contextWindow: context,
        ttlMs: ttl_ms,
        episodeId: episode_id,
        parentTaskId: parent_task_id,
      });

      if (!result.success) {
        return { content: [{ type: 'text', text: `Failed: ${result.error}` }], isError: true };
      }

      const wm = result.workingMemory;
      let msg = `✅ Working memory created\n`;
      msg += `   ID: ${wm.id}\n`;
      msg += `   Task: ${wm.description}\n`;
      msg += `   Status: ${wm.status}\n`;
      msg += `   Expires: ${wm.expiresAt}\n`;
      if (result.archived) {
        msg += `   ⚠️ Oldest working memory auto-archived (max limit 5)`;
      }

      return { content: [{ type: 'text', text: msg }] };
    } catch (err) {
      return { content: [{ type: 'text', text: `Error: ${err.message}` }], isError: true };
    }
  });

  // ─── memory_working_list ─────────────────────────────────────────────────
  server.registerTool('memory_working_list', {
    description: 'List all active (and held) working memories. Shows tasks you are currently working on or have paused.',
    inputSchema: z.object({}),
  }, async () => {
    try {
      const { active, held, counts } = getActive();

      let msg = `🧠 Working Memories\n`;
      msg += `   Active: ${counts.active}/${counts.maxActive} | Held: ${counts.held}\n\n`;

      if (active.length === 0 && held.length === 0) {
        msg += `   No active working memories.\n`;
        return { content: [{ type: 'text', text: msg }] };
      }

      for (const wm of active) {
        const remainingMin = Math.round(wm.remainingMs / 60000);
        msg += `● [ACTIVE] ${wm.description}\n`;
        msg += `  ID: ${wm.id} | Expires: in ${remainingMin}min\n`;
        if (wm.contextWindow) {
          msg += `  Context: ${wm.contextWindow.slice(0, 80)}...\n`;
        }
        msg += `\n`;
      }

      for (const wm of held) {
        msg += `○ [HELD] ${wm.description}\n`;
        msg += `  ID: ${wm.id}\n`;
        msg += `\n`;
      }

      return { content: [{ type: 'text', text: msg }] };
    } catch (err) {
      return { content: [{ type: 'text', text: `Error: ${err.message}` }], isError: true };
    }
  });

  // ─── memory_working_get ──────────────────────────────────────────────────
  server.registerTool('memory_working_get', {
    description: 'Get a specific working memory by ID.',
    inputSchema: z.object({
      id: z.string().describe('Working memory ID'),
    }),
  }, async ({ id }) => {
    try {
      const wm = get(id);
      if (!wm) {
        return { content: [{ type: 'text', text: `Working memory not found: ${id}` }], isError: true };
      }

      const remainingMin = Math.round(wm.remainingMs / 60000);
      let msg = `🧠 Working Memory\n`;
      msg += `   ID: ${wm.id}\n`;
      msg += `   Task: ${wm.description}\n`;
      msg += `   Status: ${wm.status}\n`;
      msg += `   Created: ${wm.createdAt}\n`;
      msg += `   Expires: in ${remainingMin}min\n`;
      if (wm.contextWindow) {
        msg += `   Context: ${wm.contextWindow}\n`;
      }
      if (wm.episodeId) {
        msg += `   Episode: ${wm.episodeId}\n`;
      }
      if (wm.parentTaskId) {
        msg += `   Parent: ${wm.parentTaskId}\n`;
      }
      if (wm.subtaskCount > 0) {
        msg += `   Subtasks: ${wm.subtaskCount}\n`;
      }

      return { content: [{ type: 'text', text: msg }] };
    } catch (err) {
      return { content: [{ type: 'text', text: `Error: ${err.message}` }], isError: true };
    }
  });

  // ─── memory_working_hold ─────────────────────────────────────────────────
  server.registerTool('memory_working_hold', {
    description: 'Hold (pause) a working memory without clearing it. Use when switching tasks temporarily.',
    inputSchema: z.object({
      id: z.string().describe('Working memory ID to hold'),
    }),
  }, async ({ id }) => {
    try {
      const result = hold(id);
      if (!result.success) {
        return { content: [{ type: 'text', text: `Failed: ${result.error}` }], isError: true };
      }

      return {
        content: [{
          type: 'text',
          text: `⏸️ Working memory held: ${result.workingMemory.description}\n   ID: ${result.workingMemory.id}`,
        }],
      };
    } catch (err) {
      return { content: [{ type: 'text', text: `Error: ${err.message}` }], isError: true };
    }
  });

  // ─── memory_working_resume ────────────────────────────────────────────────
  server.registerTool('memory_working_resume', {
    description: 'Resume a held working memory back to active status.',
    inputSchema: z.object({
      id: z.string().describe('Working memory ID to resume'),
      extend_ms: z.number().optional().describe('Extend TTL by this many milliseconds'),
    }),
  }, async ({ id, extend_ms = null }) => {
    try {
      const result = resume(id, extend_ms);
      if (!result.success) {
        return { content: [{ type: 'text', text: `Failed: ${result.error}` }], isError: true };
      }

      return {
        content: [{
          type: 'text',
          text: `▶️ Working memory resumed: ${result.workingMemory.description}\n   ID: ${result.workingMemory.id}`,
        }],
      };
    } catch (err) {
      return { content: [{ type: 'text', text: `Error: ${err.message}` }], isError: true };
    }
  });

  // ─── memory_working_clear ────────────────────────────────────────────────
  server.registerTool('memory_working_clear', {
    description: 'Explicitly clear a working memory. Its subtasks will be auto-held.',
    inputSchema: z.object({
      id: z.string().describe('Working memory ID to clear'),
      reason: z.string().optional().describe('Reason for clearing'),
    }),
  }, async ({ id, reason = 'explicit_clear' }) => {
    try {
      const result = clear(id, reason);
      if (!result.success) {
        return { content: [{ type: 'text', text: `Failed: ${result.error}` }], isError: true };
      }

      return {
        content: [{
          type: 'text',
          text: `✅ Working memory cleared: ${result.workingMemory.description}\n   ID: ${result.workingMemory.id}`,
        }],
      };
    } catch (err) {
      return { content: [{ type: 'text', text: `Error: ${err.message}` }], isError: true };
    }
  });

  // ─── memory_working_extend ───────────────────────────────────────────────
  server.registerTool('memory_working_extend', {
    description: 'Extend the TTL (time-to-live) of a working memory.',
    inputSchema: z.object({
      id: z.string().describe('Working memory ID'),
      duration_ms: z.number().describe('Duration to extend in milliseconds (e.g., 3600000 for +1 hour)'),
    }),
  }, async ({ id, duration_ms }) => {
    try {
      const result = extend(id, duration_ms);
      if (!result.success) {
        return { content: [{ type: 'text', text: `Failed: ${result.error}` }], isError: true };
      }

      const extendedMin = Math.round(duration_ms / 60000);
      return {
        content: [{
          type: 'text',
          text: `⏰ Working memory extended by ${extendedMin}min: ${result.workingMemory.description}\n   New expiry: ${result.workingMemory.expiresAt}`,
        }],
      };
    } catch (err) {
      return { content: [{ type: 'text', text: `Error: ${err.message}` }], isError: true };
    }
  });

  // ─── memory_working_context ──────────────────────────────────────────────
  server.registerTool('memory_working_context', {
    description: 'Update the context window of a working memory.',
    inputSchema: z.object({
      id: z.string().describe('Working memory ID'),
      context: z.string().describe('New context content'),
    }),
  }, async ({ id, context }) => {
    try {
      const result = updateContext(id, context);
      if (!result.success) {
        return { content: [{ type: 'text', text: `Failed: ${result.error}` }], isError: true };
      }

      return {
        content: [{
          type: 'text',
          text: `✅ Context updated for: ${result.workingMemory.description}`,
        }],
      };
    } catch (err) {
      return { content: [{ type: 'text', text: `Error: ${err.message}` }], isError: true };
    }
  });

  // ─── memory_working_tree ─────────────────────────────────────────────────
  server.registerTool('memory_working_tree', {
    description: 'Get the task hierarchy tree showing parent/child relationships between working memories.',
    inputSchema: z.object({
      id: z.string().optional().describe('Optional working memory ID to get subtree for'),
    }),
  }, async ({ id = null }) => {
    try {
      if (id) {
        const descendants = getDescendants(id);
        const ancestry = getAncestry(id);
        
        let msg = `📋 Task Tree for ${id}\n\n`;
        msg += `Ancestry (${ancestry.length} levels):\n`;
        for (const wm of ancestry) {
          msg += `  › ${wm.taskId}: ${wm.description}\n`;
        }
        msg += `\nSubtasks (${descendants.length}):\n`;
        for (const wm of descendants) {
          msg += `  › ${wm.taskId}: ${wm.description}\n`;
        }
        return { content: [{ type: 'text', text: msg }] };
      }

      const tree = visualizeTaskTree();
      return { content: [{ type: 'text', text: tree }] };
    } catch (err) {
      return { content: [{ type: 'text', text: `Error: ${err.message}` }], isError: true };
    }
  });

  // ─── memory_working_episode ──────────────────────────────────────────────
  server.registerTool('memory_working_episode', {
    description: 'Get all working memories linked to a specific episode/session, or link a working memory to an episode.',
    inputSchema: z.object({
      action: z.enum(['get', 'link']).describe('Action: get memories for an episode, or link a working memory to an episode'),
      episode_id: z.string().describe('Episode/session ID'),
      working_memory_id: z.string().optional().describe('Working memory ID (for link action)'),
    }),
  }, async ({ action, episode_id, working_memory_id = null }) => {
    try {
      if (action === 'get') {
        const wms = getWorkingMemoriesByEpisode(episode_id);
        let msg = `📎 Working memories for episode: ${episode_id}\n`;
        msg += `   Count: ${wms.length}\n\n`;
        for (const wm of wms) {
          msg += `  ● [${wm.status}] ${wm.description}\n`;
        }
        return { content: [{ type: 'text', text: msg }] };
      }

      if (action === 'link') {
        if (!working_memory_id) {
          return { content: [{ type: 'text', text: 'working_memory_id required for link action' }], isError: true };
        }
        const result = linkToEpisode(working_memory_id, episode_id);
        return {
          content: [{
            type: 'text',
            text: result.success
              ? `🔗 Linked ${working_memory_id} to episode ${episode_id}`
              : `Failed to link`,
          }],
        };
      }
    } catch (err) {
      return { content: [{ type: 'text', text: `Error: ${err.message}` }], isError: true };
    }
  });
}
