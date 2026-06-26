/**
 * organize.js - Automatic Memory Organization
 * 
 * Implements automatic memory tiering and compression.
 * Moves memories between HOT/WARM/COLD tiers based on activity.
 * 
 * Inspired by Memory Tiering's automatic organization
 */

import { writeFileSync, readFileSync, existsSync, mkdirSync, readdirSync, statSync } from 'fs';
import { join } from 'path';

const HOME = process.env.HOME || '/root';
const MEMORY_DIR = join(HOME, '.openclaw', 'workspace', 'memory');
const HOT_DIR = join(MEMORY_DIR, 'hot');
const WARM_DIR = join(MEMORY_DIR, 'warm');
const COLD_DIR = join(MEMORY_DIR, 'cold');

// Ensure directories exist
[HOT_DIR, WARM_DIR, COLD_DIR].forEach(dir => {
  if (!existsSync(dir)) {
    mkdirSync(dir, { recursive: true });
  }
});

// Tier configuration
const TIER_CONFIG = {
  hot: {
    maxAge: 7 * 24 * 60 * 60 * 1000, // 7 days
    maxSize: 10, // max memories
    compressionRatio: 0.5 // compress to 50%
  },
  warm: {
    maxAge: 30 * 24 * 60 * 60 * 1000, // 30 days
    maxSize: 50,
    compressionRatio: 0.3
  },
  cold: {
    maxAge: 365 * 24 * 60 * 60 * 1000, // 365 days
    maxSize: 1000,
    compressionRatio: 0.1
  }
};

/**
 * Memory tier structure:
 * {
 *   id: string,
 *   text: string,
 *   category: string,
 *   importance: number,
 *   scope: string,
 *   tags: string[],
 *   tier: 'hot' | 'warm' | 'cold',
 *   createdAt: number,
 *   lastAccessed: number,
 *   accessCount: number,
 *   compressed: boolean
 * }
 */

/**
 * Determine target tier based on memory age and importance
 */
function determineTargetTier(memory) {
  const now = Date.now();
  const age = now - memory.createdAt;
  const lastAccessAge = now - memory.lastAccessed;

  // Hot: recently created and recently accessed, high importance
  if (age < TIER_CONFIG.hot.maxAge && 
      lastAccessAge < TIER_CONFIG.hot.maxAge && 
      memory.importance >= 0.7) {
    return 'hot';
  }

  // Warm: moderate age or moderate importance
  if (age < TIER_CONFIG.warm.maxAge && memory.importance >= 0.4) {
    return 'warm';
  }

  // Cold: old or low importance
  return 'cold';
}

/**
 * Compress memory content
 */
function compressMemory(memory, ratio) {
  if (memory.compressed) {
    return memory;
  }

  // Simple compression: summarize if too long
  const maxChars = Math.floor(memory.text.length * ratio);
  
  if (memory.text.length > maxChars) {
    return {
      ...memory,
      text: memory.text.substring(0, maxChars) + '...',
      compressed: true,
      originalLength: memory.text.length
    };
  }

  return memory;
}

/**
 * Move memory to target tier
 */
function moveMemory(memory, targetTier) {
  const sourceDir = join(MEMORY_DIR, memory.tier || 'hot');
  const targetDir = join(MEMORY_DIR, targetTier);
  
  const sourceFile = join(sourceDir, `${memory.id}.json`);
  const targetFile = join(targetDir, `${memory.id}.json`);

  // Compress if needed
  const config = TIER_CONFIG[targetTier];
  const compressedMemory = compressMemory(memory, config.compressionRatio);
  compressedMemory.tier = targetTier;
  compressedMemory.lastMoved = Date.now();

  // Write to new location
  writeFileSync(targetFile, JSON.stringify(compressedMemory, null, 2));

  // Remove from old location
  if (existsSync(sourceFile)) {
    // Don't delete, just mark as moved
    const movedFile = sourceFile + '.moved';
    writeFileSync(movedFile, JSON.stringify({
      movedFrom: sourceFile,
      movedTo: targetFile,
      movedAt: Date.now()
    }));
  }

  return compressedMemory;
}

/**
 * Organize all memories based on tier rules
 */
export function organizeMemories() {
  const organized = {
    hot: { moved: 0, compressed: 0 },
    warm: { moved: 0, compressed: 0 },
    cold: { moved: 0, compressed: 0 }
  };

  // Process each tier
  ['hot', 'warm', 'cold'].forEach(sourceTier => {
    const tierDir = join(MEMORY_DIR, sourceTier);
    
    if (!existsSync(tierDir)) return;

    const files = readdirSync(tierDir).filter(f => f.endsWith('.json'));

    for (const file of files) {
      try {
        const content = readFileSync(join(tierDir, file), 'utf-8');
        const memory = JSON.parse(content);

        const targetTier = determineTargetTier(memory);

        if (targetTier !== sourceTier) {
          moveMemory(memory, targetTier);
          organized[sourceTier].moved++;
          organized[targetTier].moved++;

          if (memory.text.length > TIER_CONFIG[targetTier].maxSize * 100) {
            organized[targetTier].compressed++;
          }
        }
      } catch (err) {
        console.error(`[Organize] Error processing ${file}: ${err.message}`);
      }
    }
  });

  return organized;
}

/**
 * Compress old memories in a specific tier
 */
export function compressTier(tier) {
  const tierDir = join(MEMORY_DIR, tier);
  
  if (!existsSync(tierDir)) {
    return { compressed: 0, errors: 0 };
  }

  const files = readdirSync(tierDir).filter(f => f.endsWith('.json'));
  const config = TIER_CONFIG[tier];
  let compressed = 0;
  let errors = 0;

  for (const file of files) {
    try {
      const content = readFileSync(join(tierDir, file), 'utf-8');
      const memory = JSON.parse(content);

      // Compress old memories
      const age = Date.now() - memory.createdAt;
      if (age > config.maxAge / 2 && !memory.compressed) {
        const compressedMemory = compressMemory(memory, config.compressionRatio);
        writeFileSync(join(tierDir, file), JSON.stringify(compressedMemory, null, 2));
        compressed++;
      }
    } catch (err) {
      console.error(`[Organize] Error compressing ${file}: ${err.message}`);
      errors++;
    }
  }

  return { compressed, errors };
}

/**
 * Archive memories older than threshold
 */
export function archiveOldMemories(thresholdDays = 365) {
  const threshold = Date.now() - thresholdDays * 24 * 60 * 60 * 1000;
  const archived = [];

  ['hot', 'warm', 'cold'].forEach(tier => {
    const tierDir = join(MEMORY_DIR, tier);
    
    if (!existsSync(tierDir)) return;

    const files = readdirSync(tierDir).filter(f => f.endsWith('.json'));

    for (const file of files) {
      try {
        const content = readFileSync(join(tierDir, file), 'utf-8');
        const memory = JSON.parse(content);

        if (memory.createdAt < threshold) {
          const archiveDir = join(MEMORY_DIR, 'archive', new Date(memory.createdAt).toISOString().split('T')[0]);
          mkdirSync(archiveDir, { recursive: true });
          
          const archiveFile = join(archiveDir, file);
          writeFileSync(archiveFile, JSON.stringify(memory, null, 2));
          archived.push(memory.id);
        }
      } catch (err) {
        console.error(`[Organize] Error archiving ${file}: ${err.message}`);
      }
    }
  });

  return { archived: archived.length, ids: archived };
}

/**
 * Get tier statistics
 */
export function getTierStats() {
  const stats = {};

  ['hot', 'warm', 'cold'].forEach(tier => {
    const tierDir = join(MEMORY_DIR, tier);
    
    if (!existsSync(tierDir)) {
      stats[tier] = { count: 0, totalSize: 0 };
      return;
    }

    const files = readdirSync(tierDir).filter(f => f.endsWith('.json'));
    let totalSize = 0;

    for (const file of files) {
      try {
        const content = readFileSync(join(tierDir, file), 'utf-8');
        totalSize += Buffer.byteLength(content, 'utf-8');
      } catch (err) {
        // Skip invalid files
      }
    }

    stats[tier] = {
      count: files.length,
      totalSize
    };
  });

  return stats;
}

/**
 * Full organization run
 */
export function fullOrganize() {
  const organizeResult = organizeMemories();
  const compressResult = {
    hot: compressTier('hot'),
    warm: compressTier('warm'),
    cold: compressTier('cold')
  };
  const archiveResult = archiveOldMemories(365);
  const stats = getTierStats();

  return {
    organize: organizeResult,
    compress: compressResult,
    archive: archiveResult,
    stats
  };
}
