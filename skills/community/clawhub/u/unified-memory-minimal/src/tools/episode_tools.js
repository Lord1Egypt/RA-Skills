/**
 * Episode Tools - MCP tool definitions for episode management
 *
 * Provides tools:
 * - memory_episode_start: Start a new episode
 * - memory_episode_add: Add message to episode
 * - memory_episode_complete: Complete and summarize episode
 * - memory_episode_search: Search within episodes
 * - memory_episode_list: List episodes
 */

import { z } from 'zod';
import {
  startEpisode,
  addMessage,
  completeEpisode,
  archiveOldEpisodes,
  searchEpisodes,
  getEpisodeContext,
  episodeList,
  getEpisodeWithMessages,
  getEpisodeStats,
} from '../episode_manager.js';

import { getActiveEpisode, EPISODE_STATUS } from '../episode_store.js';

/**
 * Register episode tools with the MCP server
 * @param {object} server - MCP server instance
 */
export function registerEpisodeTools(server) {
  // ─── memory_episode_start ──────────────────────────────────────────────────

  server.registerTool('memory_episode_start', {
    description: 'Start a new conversation episode. An episode represents a complete conversation session that can be searched later.',
    inputSchema: z.object({
      sessionId: z.string().describe('Unique session identifier (e.g., user ID, conversation ID)'),
      participants: z.array(z.string()).optional().default([]).describe('List of participant names/IDs'),
      title: z.string().optional().describe('Optional title for the episode'),
      tags: z.array(z.string()).optional().default([]).describe('Optional tags'),
    }),
  }, async ({ sessionId, participants = [], title, tags = [] }) => {
    try {
      const episode = startEpisode(sessionId, participants, { title, tags });
      return {
        content: [{
          type: 'text',
          text: JSON.stringify({
            success: true,
            episode: {
              id: episode.id,
              sessionId: episode.sessionId,
              state: episode.state,
              startTime: new Date(episode.startTime).toISOString(),
              participants: episode.participants,
              title: episode.title,
            },
          }, null, 2),
        }],
      };
    } catch (err) {
      return { content: [{ type: 'text', text: `Error: ${err.message}` }], isError: true };
    }
  });

  // ─── memory_episode_add ─────────────────────────────────────────────────────

  server.registerTool('memory_episode_add', {
    description: 'Add a message to an active episode.',
    inputSchema: z.object({
      sessionId: z.string().describe('Session ID (to find active episode or create new)'),
      role: z.enum(['user', 'assistant', 'system']).describe('Message role'),
      content: z.string().describe('Message content'),
      messageId: z.string().optional().describe('Optional external message ID'),
      participant: z.string().optional().default('default').describe('Participant identifier'),
    }),
  }, async ({ sessionId, role, content, messageId, participant = 'default' }) => {
    try {
      const result = await addMessage(sessionId, role, content, messageId, {
        participant,
      });

      return {
        content: [{
          type: 'text',
          text: JSON.stringify({
            success: result.added,
            episodeId: result.episodeId,
            messageCount: result.messageCount,
          }, null, 2),
        }],
      };
    } catch (err) {
      return { content: [{ type: 'text', text: `Error: ${err.message}` }], isError: true };
    }
  });

  // ─── memory_episode_complete ────────────────────────────────────────────────

  server.registerTool('memory_episode_complete', {
    description: 'Complete an active episode and generate a summary. Also extracts decision memories.',
    inputSchema: z.object({
      episodeId: z.string().describe('Episode ID to complete'),
      summary: z.object({
        title: z.string().optional(),
        keyTopics: z.array(z.string()).optional(),
        decisions: z.array(z.string()).optional(),
        nextSteps: z.array(z.string()).optional(),
      }).optional().describe('Optional override summary data'),
    }),
  }, async ({ episodeId, summary }) => {
    try {
      const result = await completeEpisode(episodeId, summary || null);

      return {
        content: [{
          type: 'text',
          text: JSON.stringify({
            success: true,
            episode: {
              id: result.episode.id,
              state: result.episode.state,
              endTime: result.episode.endTime ? new Date(result.episode.endTime).toISOString() : null,
            },
            summary: result.summary,
            decisionsExtracted: result.decisionMemories.length,
          }, null, 2),
        }],
      };
    } catch (err) {
      return { content: [{ type: 'text', text: `Error: ${err.message}` }], isError: true };
    }
  });

  // ─── memory_episode_search ─────────────────────────────────────────────────

  server.registerTool('memory_episode_search', {
    description: 'Search within episode messages. Finds episodes containing specific content.',
    inputSchema: z.object({
      query: z.string().describe('Search query text'),
      limit: z.number().optional().default(10).describe('Maximum results'),
      state: z.enum(['ACTIVE', 'COMPLETED', 'ARCHIVED']).optional().describe('Filter by episode state'),
      includeArchived: z.boolean().optional().default(false).describe('Include archived episodes in search'),
    }),
  }, async ({ query, limit = 10, state, includeArchived = false }) => {
    try {
      const results = searchEpisodes(query, { limit, state, includeArchived });

      return {
        content: [{
          type: 'text',
          text: JSON.stringify({
            query,
            count: results.length,
            results: results.map(r => ({
              episode: {
                id: r.episode.id,
                sessionId: r.episode.sessionId,
                state: r.episode.state,
                title: r.episode.title,
                keyTopics: r.episode.keyTopics,
                messageCount: r.episode.messageCount,
              },
              relevance: r.relevance,
              matchCount: r.matchCount,
              matchedMessages: r.matchedMessages.slice(0, 3).map(m => ({
                role: m.role,
                content: m.content?.slice(0, 100),
                timestamp: new Date(m.timestamp).toISOString(),
              })),
            })),
          }, null, 2),
        }],
      };
    } catch (err) {
      return { content: [{ type: 'text', text: `Error: ${err.message}` }], isError: true };
    }
  });

  // ─── memory_episode_list ───────────────────────────────────────────────────

  server.registerTool('memory_episode_list', {
    description: 'List all episodes with optional filtering.',
    inputSchema: z.object({
      state: z.enum(['ACTIVE', 'COMPLETED', 'ARCHIVED']).optional().describe('Filter by episode state'),
      limit: z.number().optional().default(20).describe('Number of episodes to return'),
      offset: z.number().optional().default(0).describe('Offset for pagination'),
      includeArchived: z.boolean().optional().default(false).describe('Include archived episodes'),
    }),
  }, async ({ state, limit = 20, offset = 0, includeArchived = false }) => {
    try {
      const result = episodeList({ state, limit, offset, includeArchived });

      return {
        content: [{
          type: 'text',
          text: JSON.stringify(result, null, 2),
        }],
      };
    } catch (err) {
      return { content: [{ type: 'text', text: `Error: ${err.message}` }], isError: true };
    }
  });

  // ─── memory_episode_get ────────────────────────────────────────────────────

  server.registerTool('memory_episode_get', {
    description: 'Get full details of a specific episode including all messages.',
    inputSchema: z.object({
      episodeId: z.string().describe('Episode ID to retrieve'),
    }),
  }, async ({ episodeId }) => {
    try {
      const episode = getEpisodeWithMessages(episodeId);

      if (!episode) {
        return { content: [{ type: 'text', text: JSON.stringify({ error: 'Episode not found' }) }], isError: true };
      }

      return {
        content: [{
          type: 'text',
          text: JSON.stringify({
            id: episode.id,
            sessionId: episode.sessionId,
            state: episode.state,
            startTime: episode.startTime ? new Date(episode.startTime).toISOString() : null,
            endTime: episode.endTime ? new Date(episode.endTime).toISOString() : null,
            lastActivity: episode.lastActivity ? new Date(episode.lastActivity).toISOString() : null,
            messageCount: episode.messageCount,
            participants: episode.participants,
            title: episode.title,
            summary: episode.summary,
            keyTopics: episode.keyTopics,
            decisions: episode.decisions,
            nextSteps: episode.nextSteps,
            tags: episode.tags,
            memoryIds: episode.memoryIds,
            messages: episode.messages?.map(m => ({
              role: m.role,
              content: m.content,
              timestamp: new Date(m.timestamp).toISOString(),
            })),
          }, null, 2),
        }],
      };
    } catch (err) {
      return { content: [{ type: 'text', text: `Error: ${err.message}` }], isError: true };
    }
  });

  // ─── memory_episode_archive ────────────────────────────────────────────────

  server.registerTool('memory_episode_archive', {
    description: 'Archive old completed episodes (move to cold storage).',
    inputSchema: z.object({
      daysOld: z.number().optional().default(30).describe('Archive episodes older than this many days'),
    }),
  }, async ({ daysOld = 30 }) => {
    try {
      const count = archiveOldEpisodes(daysOld);

      return {
        content: [{
          type: 'text',
          text: JSON.stringify({
            success: true,
            archived: count,
            message: `Archived ${count} episodes older than ${daysOld} days`,
          }, null, 2),
        }],
      };
    } catch (err) {
      return { content: [{ type: 'text', text: `Error: ${err.message}` }], isError: true };
    }
  });

  // ─── memory_episode_stats ─────────────────────────────────────────────────

  server.registerTool('memory_episode_stats', {
    description: 'Get episode statistics.',
    inputSchema: z.object({}),
  }, async () => {
    try {
      const stats = getEpisodeStats();
      return {
        content: [{
          type: 'text',
          text: JSON.stringify(stats, null, 2),
        }],
      };
    } catch (err) {
      return { content: [{ type: 'text', text: `Error: ${err.message}` }], isError: true };
    }
  });

  // ─── memory_episode_context ────────────────────────────────────────────────

  server.registerTool('memory_episode_context', {
    description: 'Get episode messages as context for a search query. Useful for "what did we discuss about X".',
    inputSchema: z.object({
      query: z.string().describe('Search query'),
      maxMessages: z.number().optional().default(10).describe('Max messages per episode'),
    }),
  }, async ({ query, maxMessages = 10 }) => {
    try {
      const context = await getEpisodeContext(query, maxMessages);

      return {
        content: [{
          type: 'text',
          text: JSON.stringify({
            query,
            episodes: context.map(c => ({
              episodeId: c.episodeId,
              sessionId: c.sessionId,
              title: c.title,
              relevance: c.relevance,
              keyTopics: c.keyTopics,
              decisions: c.decisions,
              messages: c.messages.map(m => ({
                role: m.role,
                content: m.content?.slice(0, 150),
                relevance: m.relevance,
              })),
            })),
          }, null, 2),
        }],
      };
    } catch (err) {
      return { content: [{ type: 'text', text: `Error: ${err.message}` }], isError: true };
    }
  });
}

export default { registerEpisodeTools };
