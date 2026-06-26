/**
 * Episode Tools v2 — MCP tool definitions for Episode management
 *
 * 5 tools matching the v2 spec:
 * - memory_episode_start: Start a new episode
 * - memory_episode_end: End current active episode, generate summary
 * - memory_episode_list: List all episodes (paginated)
 * - memory_episode_recall: Recall full context of a specific episode
 * - memory_episode_merge: Merge two episodes into one
 *
 * Based on the Episode schema:
 * {
 *   id, topic, started_at, ended_at,
 *   turns, message_count,
 *   memory_ids, entities,
 *   last_refresh, status
 * }
 */

import { z } from 'zod';
import {
  createEpisode,
  endEpisode,
  updateEpisode,
  getActiveEpisode,
  getEpisode,
  autoSplitEpisode,
  listEpisodes,
  mergeEpisodes,
  recallEpisodeAsync,
  EPISODE_STATUS,
} from './episode_store.js';

/**
 * Register all episode tools with the MCP server
 * @param {object} server - MCP server instance (from @modelcontextprotocol/sdk)
 */
export function registerEpisodeTools(server) {

  // ─── memory_episode_start ──────────────────────────────────────────────────
  server.registerTool('memory_episode_start', {
    description: 'Start a new conversation episode. An episode represents a focused conversation session around a single topic. Automatically ends any existing active episode first.',
    inputSchema: z.object({
      topic: z.string().describe('Topic/title of the episode (e.g. "刘总问unified-memory功能")'),
    }),
  }, async ({ topic }) => {
    try {
      const episode = createEpisode(topic);
      return {
        content: [{
          type: 'text',
          text: JSON.stringify({
            success: true,
            episode: {
              id: episode.id,
              topic: episode.topic,
              started_at: episode.started_at,
              turns: episode.turns,
              message_count: episode.message_count,
              status: episode.status,
            },
          }, null, 2),
        }],
      };
    } catch (err) {
      return { content: [{ type: 'text', text: `Error: ${err.message}` }], isError: true };
    }
  });

  // ─── memory_episode_end ────────────────────────────────────────────────────
  server.registerTool('memory_episode_end', {
    description: 'End the current active episode and generate a summary. Extracts key topics, decisions, and entities from the conversation.',
    inputSchema: z.object({
      episodeId: z.string().optional().describe('Episode ID to end. If omitted, ends the current active episode.'),
    }),
  }, async ({ episodeId }) => {
    try {
      let targetId = episodeId;

      // If no ID provided, find active episode
      if (!targetId) {
        const active = getActiveEpisode();
        if (!active) {
          return {
            content: [{
              type: 'text',
              text: JSON.stringify({ success: false, error: 'No active episode to end' }),
            }],
            isError: false,
          };
        }
        targetId = active.id;
      }

      const updated = endEpisode(targetId);
      if (!updated) {
        return { content: [{ type: 'text', text: JSON.stringify({ success: false, error: 'Episode not found or already ended' }) }], isError: true };
      }

      // Extract summary data from topic and entities
      const summary = generateEpisodeSummary(updated);

      return {
        content: [{
          type: 'text',
          text: JSON.stringify({
            success: true,
            episode: {
              id: updated.id,
              topic: updated.topic,
              started_at: updated.started_at,
              ended_at: updated.ended_at,
              turns: updated.turns,
              message_count: updated.message_count,
              status: updated.status,
              entities: updated.entities,
            },
            summary,
          }, null, 2),
        }],
      };
    } catch (err) {
      return { content: [{ type: 'text', text: `Error: ${err.message}` }], isError: true };
    }
  });

  // ─── memory_episode_list ───────────────────────────────────────────────────
  server.registerTool('memory_episode_list', {
    description: 'List all episodes with optional pagination and status filter.',
    inputSchema: z.object({
      status: z.enum(['active', 'completed']).optional().describe("Filter by status: 'active' or 'completed'"),
      limit: z.number().optional().default(20).describe('Number of episodes to return (default 20)'),
      offset: z.number().optional().default(0).describe('Offset for pagination (default 0)'),
    }),
  }, async ({ status, limit = 20, offset = 0 }) => {
    try {
      const result = listEpisodes({ status, limit, offset });

      return {
        content: [{
          type: 'text',
          text: JSON.stringify({
            total: result.total,
            offset,
            limit,
            episodes: result.episodes.map(ep => ({
              id: ep.id,
              topic: ep.topic,
              started_at: ep.started_at,
              ended_at: ep.ended_at,
              turns: ep.turns,
              message_count: ep.message_count,
              entities: ep.entities,
              status: ep.status,
              last_refresh: ep.last_refresh,
            })),
          }, null, 2),
        }],
      };
    } catch (err) {
      return { content: [{ type: 'text', text: `Error: ${err.message}` }], isError: true };
    }
  });

  // ─── memory_episode_recall ─────────────────────────────────────────────────
  server.registerTool('memory_episode_recall', {
    description: 'Recall the full context of a specific episode including associated memories.',
    inputSchema: z.object({
      episodeId: z.string().describe('Episode ID to recall'),
    }),
  }, async ({ episodeId }) => {
    try {
      const result = await recallEpisodeAsync(episodeId);

      if (!result) {
        return { content: [{ type: 'text', text: JSON.stringify({ success: false, error: 'Episode not found' }) }], isError: true };
      }

      const { episode, memories } = result;

      return {
        content: [{
          type: 'text',
          text: JSON.stringify({
            success: true,
            episode: {
              id: episode.id,
              topic: episode.topic,
              started_at: episode.started_at,
              ended_at: episode.ended_at,
              turns: episode.turns,
              message_count: episode.message_count,
              memory_ids: episode.memory_ids,
              entities: episode.entities,
              last_refresh: episode.last_refresh,
              status: episode.status,
            },
            memories: memories.map(m => ({
              id: m.id,
              text: m.text,
              category: m.category,
              importance: m.importance,
              created_at: m.created_at,
            })),
            memory_count: memories.length,
          }, null, 2),
        }],
      };
    } catch (err) {
      return { content: [{ type: 'text', text: `Error: ${err.message}` }], isError: true };
    }
  });

  // ─── memory_episode_merge ──────────────────────────────────────────────────
  server.registerTool('memory_episode_merge', {
    description: 'Merge two episodes into one. The first episode survives; the second is deleted. All memory IDs and entities from both are combined.',
    inputSchema: z.object({
      episodeId1: z.string().describe('First episode ID (will be the surviving episode)'),
      episodeId2: z.string().describe('Second episode ID (will be deleted after merge)'),
    }),
  }, async ({ episodeId1, episodeId2 }) => {
    try {
      if (episodeId1 === episodeId2) {
        return { content: [{ type: 'text', text: JSON.stringify({ success: false, error: 'Cannot merge an episode with itself' }) }], isError: true };
      }

      const merged = mergeEpisodes(episodeId1, episodeId2);

      if (!merged) {
        return { content: [{ type: 'text', text: JSON.stringify({ success: false, error: 'One or both episodes not found' }) }], isError: true };
      }

      return {
        content: [{
          type: 'text',
          text: JSON.stringify({
            success: true,
            merged: {
              id: merged.id,
              topic: merged.topic,
              started_at: merged.started_at,
              ended_at: merged.ended_at,
              turns: merged.turns,
              message_count: merged.message_count,
              memory_ids: merged.memory_ids,
              entities: merged.entities,
              status: merged.status,
            },
          }, null, 2),
        }],
      };
    } catch (err) {
      return { content: [{ type: 'text', text: `Error: ${err.message}` }], isError: true };
    }
  });
}

// ─── Helpers ────────────────────────────────────────────────────────────────

/**
 * Generate a human-readable summary from episode metadata
 * @param {object} episode
 * @returns {object}
 */
function generateEpisodeSummary(episode) {
  const lines = [];
  if (episode.entities && episode.entities.length) {
    lines.push(`涉及实体: ${episode.entities.join(', ')}`);
  }
  lines.push(`总轮次: ${episode.turns} turns, ${episode.message_count} 条消息`);

  return {
    topic: episode.topic,
    entities: episode.entities || [],
    turns: episode.turns,
    message_count: episode.message_count,
    description: lines.join(' | '),
  };
}

// Aliases for consistent naming (episodes can be "started" or "created", "ended" or "completed")
export { createEpisode as startEpisode };
export { endEpisode as completeEpisode };

export default { registerEpisodeTools };
