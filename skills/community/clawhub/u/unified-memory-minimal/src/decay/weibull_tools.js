/**
 * src/decay/weibull_tools.js
 * Weibull 衰减统计工具
 */

import { z } from 'zod';
import { getWeibullDecayModel } from './weibull_decay.js';
import { getAllMemories } from '../storage.js';

export function registerDecayStatsTool(server) {

  server.registerTool('memory_decay_stats', {
    description: 'Show Weibull decay statistics: memory strength distribution across strong/moderate/weak/prune buckets. Helps understand memory health.',
    inputSchema: z.object({
      threshold: z.number().optional().default(0.1).describe('Prune threshold (default 0.1)'),
      maxAgeDays: z.number().optional().default(365).describe('Max age in days (default 365)'),
      shape: z.number().optional().describe('Weibull shape parameter (default from config 1.5)'),
      scale: z.number().optional().describe('Weibull scale parameter in days (default from config 30)'),
    }),
  }, async ({ threshold, maxAgeDays, shape, scale } = {}) => {
    try {
      const decayModel = getWeibullDecayModel({ shape, scale });
      const memories = await getAllMemories();
      
      const stats = decayModel.getStats(memories);
      const candidates = decayModel.getPruneCandidates(memories, { threshold, max_age_days: maxAgeDays });

      return {
        content: [{
          type: 'text',
          text: JSON.stringify({
            model: 'Weibull',
            shape: decayModel.shape,
            scale: decayModel.scale,
            threshold,
            maxAgeDays,
            totalMemories: memories.length,
            strengthDistribution: stats.buckets,
            avgStrength: Math.round(stats.avgStrength * 1000) / 1000,
            pruneCandidates: candidates.length,
            candidatesPreview: candidates.slice(0, 5).map(m => ({
              id: m.id || m._id,
              content: (m.content || '').slice(0, 80),
              strength: Math.round(decayModel.getStrength(m) * 1000) / 1000,
            })),
          }, null, 2)
        }]
      };
    } catch (err) {
      return { content: [{ type: 'text', text: `Decay stats error: ${err.message}` }], isError: true };
    }
  });

  server.registerTool('memory_decay_strength', {
    description: 'Get the Weibull strength score for a specific memory.',
    inputSchema: z.object({
      memory_id: z.string().describe('Memory ID to check strength for'),
    }),
  }, async ({ memory_id }) => {
    try {
      const { getMemory } = await import('../storage.js');
      const memory = await getMemory(memory_id);
      if (!memory) {
        return { content: [{ type: 'text', text: `Memory not found: ${memory_id}` }], isError: true };
      }
      const decayModel = getWeibullDecayModel();
      const strength = decayModel.getStrength(memory);
      const pruneCandidates = decayModel.getPruneCandidates([memory]);
      
      return {
        content: [{
          type: 'text',
          text: JSON.stringify({
            memory_id,
            strength: Math.round(strength * 1000) / 1000,
            shouldPrune: pruneCandidates.length > 0,
            model: 'Weibull',
            shape: decayModel.shape,
            scale: decayModel.scale,
          }, null, 2)
        }]
      };
    } catch (err) {
      return { content: [{ type: 'text', text: `Error: ${err.message}` }], isError: true };
    }
  });
}
