/**
 * Organize Tools Registration
 * Inline tool registration for memory organization across tiers
 */
import { organizeMemories, compressTier, archiveOldMemories, getTierStats, fullOrganize } from '../organize.js';

export function registerOrganizeTools(server, { z }) {
  server.registerTool('memory_organize', {
    description: 'Organize memories across tiers (HOT/WARM/COLD)',
    inputSchema: z.object({})
  }, async () => {
    const result = organizeMemories();
    return { content: [{ type: 'text', text: JSON.stringify(result, null, 2) }] };
  });

  server.registerTool('memory_compress_tier', {
    description: 'Compress memories in a specific tier',
    inputSchema: z.object({ tier: z.enum(['hot', 'warm', 'cold']).describe('Tier to compress') })
  }, async ({ tier }) => {
    const result = compressTier(tier);
    return { content: [{ type: 'text', text: JSON.stringify(result, null, 2) }] };
  });

  server.registerTool('memory_archive_old', {
    description: 'Archive memories older than threshold',
    inputSchema: z.object({ thresholdDays: z.number().default(365).describe('Threshold in days') })
  }, async ({ thresholdDays }) => {
    const result = archiveOldMemories(thresholdDays);
    return { content: [{ type: 'text', text: JSON.stringify(result, null, 2) }] };
  });

  server.registerTool('memory_tier_stats', {
    description: 'Get tier statistics',
    inputSchema: z.object({})
  }, async () => {
    const stats = getTierStats();
    return { content: [{ type: 'text', text: JSON.stringify(stats, null, 2) }] };
  });

  server.registerTool('memory_full_organize', {
    description: 'Run full organization (organize + compress + archive)',
    inputSchema: z.object({})
  }, async () => {
    const result = fullOrganize();
    return { content: [{ type: 'text', text: JSON.stringify(result, null, 2) }] };
  });
}
