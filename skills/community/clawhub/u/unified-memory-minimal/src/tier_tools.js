/**
 * tier_tools.js - Tier Management MCP Tools
 * memory_tier_status, memory_tier_migrate, memory_tier_compress
 */
import { getAllMemories, saveMemories, deleteMemory } from './storage.js';
import {
  TIER_CONFIG,
  assignTiers,
  partitionByTier,
  redistributeTiers,
  compressColdTier,
  getTierStats,
  autoMigrateTiers,
} from './tier.js';
import { log } from './config.js';

const DAY_MS = 86400000;

/**
 * memory_tier_status - View tier statistics
 */
export async function memoryTierStatusTool() {
  try {
    const memories = await getAllMemories();
    console.error(`[DEBUG] memories=${memories?.length}, type=${typeof memories}`);
    const stats = getTierStats(memories);
    const tiers = partitionByTier(memories);

    // Calculate size by tier (tier already assigned via partitionByTier)
    const sizeByTier = { HOT: 0, WARM: 0, COLD: 0 };
    for (const tierKey of ['HOT', 'WARM', 'COLD']) {
      for (const m of (tiers[tierKey] || [])) {
        const size = Buffer.byteLength(JSON.stringify(m), 'utf8');
        sizeByTier[tierKey] += size;
      }
    }

    // Access stats per tier
    const accessStats = {};
    for (const [tier, configs] of Object.entries(TIER_CONFIG)) {
      const tierMems = tiers[tier] || [];
      const recentAccess = tierMems.filter(m => {
        const lastAcc = m.last_access || m.lastAccess || m.timestamp || m.created_at || m.createdAt || 0;
        const ts = typeof lastAcc === 'string' ? new Date(lastAcc).getTime() : lastAcc;
        return (Date.now() - ts) < 7 * DAY_MS;
      }).length;
      const avgImportance = tierMems.length > 0
        ? tierMems.reduce((s, m) => s + (m.importance || 0.5), 0) / tierMems.length
        : 0;
      accessStats[tier] = {
        count: tierMems.length,
        recent_access_7d: recentAccess,
        avg_importance: Math.round(avgImportance * 1000) / 1000,
        size_bytes: sizeByTier[tier],
      };
    }

    return {
      content: [{
        type: 'text',
        text: JSON.stringify({
          total_memories: memories.length,
          tier_config: {
            HOT: { maxAgeDays: TIER_CONFIG.HOT.maxAgeDays, compress: TIER_CONFIG.HOT.compress },
            WARM: { maxAgeDays: TIER_CONFIG.WARM.maxAgeDays, compress: TIER_CONFIG.WARM.compress },
            COLD: { maxAgeDays: 'unlimited', compress: TIER_CONFIG.COLD.compress },
          },
          distribution: {
            HOT: stats.HOT,
            WARM: stats.WARM,
            COLD: stats.COLD,
          },
          tier_details: accessStats,
        }, null, 2),
      }],
    };
  } catch (err) {
    log('ERROR', `[memory_tier_status] ${err.message}`);
    return { content: [{ type: 'text', text: `Error: ${err.message}` }], isError: true };
  }
}

/**
 * memory_tier_migrate - Manually trigger tier migration
 */
export async function memoryTierMigrateTool({ apply = false } = {}) {
  try {
    const memories = await getAllMemories();
    const beforeStats = getTierStats(memories);

    // Get migration recommendations
    const migration = autoMigrateTiers(memories, { dryRun: !apply });
    const afterStats = getTierStats(migration.memories);

    const changes = [];
    for (const m of migration.changes) {
      changes.push({
        id: m.id,
        from: m.fromTier,
        to: m.toTier,
        reason: m.reason,
        importance: m.memory.importance,
      });
    }

    if (apply) {
      saveMemories(migration.memories);
      log('INFO', `[memory_tier_migrate] Applied ${changes.length} tier changes`);
    } else {
      log('INFO', `[memory_tier_migrate] Dry-run: ${changes.length} tier changes would be made`);
    }

    return {
      content: [{
        type: 'text',
        text: JSON.stringify({
          dry_run: !apply,
          before: beforeStats,
          after: afterStats,
          migrations: changes.length,
          applied: apply,
          details: changes.slice(0, 50), // cap output
        }, null, 2),
      }],
    };
  } catch (err) {
    log('ERROR', `[memory_tier_migrate] ${err.message}`);
    return { content: [{ type: 'text', text: `Error: ${err.message}` }], isError: true };
  }
}

/**
 * memory_tier_compress - Compress COLD tier storage
 */
export async function memoryTierCompressTool({ apply = false } = {}) {
  try {
    const memories = await getAllMemories();
    const tiers = partitionByTier(memories);
    const coldMemories = tiers.COLD || [];

    if (coldMemories.length === 0) {
      return {
        content: [{
          type: 'text',
          text: JSON.stringify({
            message: 'No COLD tier memories to compress',
            cold_count: 0,
          }, null, 2),
        }],
      };
    }

    // Compress cold memories
    const compressed = compressColdTier(coldMemories);
    const originalSize = coldMemories.reduce((s, m) => s + Buffer.byteLength(JSON.stringify(m), 'utf8'), 0);
    const compressedSize = compressed.reduce((s, m) => s + Buffer.byteLength(JSON.stringify(m), 'utf8'), 0);

    const result = {
      content: [{
        type: 'text',
        text: JSON.stringify({
          dry_run: !apply,
          cold_count: coldMemories.length,
          compressed_count: compressed.length,
          original_size_bytes: originalSize,
          compressed_size_bytes: compressedSize,
          space_saved_bytes: originalSize - compressedSize,
          savings_percent: Math.round(((originalSize - compressedSize) / originalSize) * 1000) / 10,
          applied: apply,
        }, null, 2),
      }],
    };

    if (apply) {
      // Build a map of compressed memories by id
      const compressedMap = new Map(compressed.map(c => [c.id, c]));
      // Replace cold memories with their compressed versions in the full array
      const updatedMemories = memories.map(m =>
        compressedMap.has(m.id) ? compressedMap.get(m.id) : m
      );
      saveMemories(updatedMemories);
      log('INFO', `[memory_tier_compress] Compressed ${compressed.length} COLD memories`);
    }

    return result;
  } catch (err) {
    log('ERROR', `[memory_tier_compress] ${err.message}`);
    return { content: [{ type: 'text', text: `Error: ${err.message}` }], isError: true };
  }
}

export default {
  memoryTierStatusTool,
  memoryTierMigrateTool,
  memoryTierCompressTool,
};
