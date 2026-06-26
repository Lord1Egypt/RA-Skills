/**
 * Memory Tiering System v2.0
 * 
 * Three-tier memory architecture:
 * 1. persistent - Long-term retention (important decisions, user preferences)
 * 2. normal - Medium-term retention (current projects, recent context)
 * 3. ephemeral - Short-term auto-cleanup (temp data, session notes)
 * 
 * Each memory file has a type field identifying its tier.
 */

const fs = require("fs");
const path = require("path");
const os = require("os");

// Paths
const MEMORY_DIR = "E:\\zhuazhua\\.openclaw\\.openclaw\\workspace\\memory";
const SHARED_MEMORY_DIR = "E:\\zhuazhua\\.openclaw-shared\\memory";
const MEMORY_DB_DIR = "E:\\zhuazhua\\.openclaw\\.openclaw\\workspace\\.memory_db";

// Memory tier configurations
const MEMORY_TIERS = {
  persistent: {
    name: "persistent",
    description: "Long-term important memories",
    retentionDays: 365,  // Keep for 1 year
    autoCleanup: false,  // Never auto-delete
    priority: 1,
    patterns: ["*.md"],
    frontmatterField: "memory_type"
  },
  normal: {
    name: "normal",
    description: "Medium-term normal memories",
    retentionDays: 30,   // Keep for 30 days
    autoCleanup: true,
    priority: 2,
    patterns: ["*.md"],
    frontmatterField: "memory_type"
  },
  ephemeral: {
    name: "ephemeral",
    description: "Short-term temporary memories",
    retentionDays: 7,   // Keep for 7 days
    autoCleanup: true,
    priority: 3,
    patterns: ["*.md"],
    frontmatterField: "memory_type"
  }
};

// Default tier for new memories
const DEFAULT_TIER = "normal";

// Files that should never be cleaned up
const PROTECTED_FILES = [
  "MEMORY.md",
  "shared_state.md",
  "heartbeat-state.json",
  "decisions.jsonl"
];

/**
 * Get memory type from file frontmatter
 */
function getMemoryType(filePath) {
  try {
    const content = fs.readFileSync(filePath, "utf-8");
    
    // Check for frontmatter
    const fmMatch = content.match(/^---\n([\s\S]*?)\n---/);
    if (fmMatch) {
      const fmContent = fmMatch[1];
      const typeMatch = fmContent.match(/memory_type:\s*(\w+)/);
      if (typeMatch) {
        return typeMatch[1];
      }
      
      // Also check type field
      const typeMatch2 = fmContent.match(/^type:\s*(\w+)/m);
      if (typeMatch2) {
        return typeMatch2[1];
      }
    }
    
    // Check for legacy patterns
    const basename = path.basename(filePath);
    if (basename.startsWith("2026-") || basename.match(/^\d{4}-\d{2}-\d{2}/)) {
      // Daily notes are normal by default
      return "normal";
    }
    
    return null;
  } catch (e) {
    return null;
  }
}

/**
 * Set memory type in file frontmatter
 */
function setMemoryType(filePath, tier) {
  if (!MEMORY_TIERS[tier]) {
    return { ok: false, error: `Invalid tier: ${tier}` };
  }
  
  try {
    const content = fs.readFileSync(filePath, "utf-8");
    let newContent;
    
    // Check if frontmatter exists
    if (content.startsWith("---")) {
      const fmEnd = content.indexOf("\n---\n");
      if (fmEnd !== -1) {
        const fm = content.slice(0, fmEnd + 5);
        const body = content.slice(fmEnd + 5);
        
        // Update or add memory_type field
        let fmContent = content.slice(4, fmEnd);
        
        // Check if memory_type already exists
        if (fmContent.includes("memory_type:")) {
          fmContent = fmContent.replace(/memory_type:\s*\w+/, `memory_type: ${tier}`);
        } else {
          // Add memory_type after date field or at beginning
          if (fmContent.includes("date:")) {
            fmContent = fmContent.replace(/date:/, `memory_type: ${tier}\ndate:`);
          } else {
            fmContent = `memory_type: ${tier}\n` + fmContent;
          }
        }
        
        newContent = `---\n${fmContent}\n---${body}`;
      } else {
        // Malformed frontmatter, add new one
        newContent = `---\nmemory_type: ${tier}\n---\n${content}`;
      }
    } else {
      // No frontmatter, add one
      newContent = `---\nmemory_type: ${tier}\n---\n${content}`;
    }
    
    fs.writeFileSync(filePath, newContent, "utf-8");
    return { ok: true, tier };
  } catch (e) {
    return { ok: false, error: e.message };
  }
}

/**
 * Get all memories grouped by tier
 */
function getMemoriesByTier() {
  const result = {
    persistent: [],
    normal: [],
    ephemeral: [],
    unknown: []
  };
  
  // Scan memory directory
  if (fs.existsSync(MEMORY_DIR)) {
    scanMemoryDirectory(MEMORY_DIR, result);
  }
  
  return result;
}

/**
 * Recursively scan memory directory
 */
function scanMemoryDirectory(dir, result) {
  try {
    const entries = fs.readdirSync(dir, { withFileTypes: true });
    
    for (const entry of entries) {
      const fullPath = path.join(dir, entry.name);
      
      if (entry.isDirectory()) {
        // Skip inbox subdirectory
        if (entry.name !== "inbox") {
          scanMemoryDirectory(fullPath, result);
        }
      } else if (entry.isFile() && entry.name.endsWith(".md")) {
        // Skip protected files
        if (PROTECTED_FILES.includes(entry.name)) {
          continue;
        }
        
        const tier = getMemoryType(fullPath);
        
        if (tier && result[tier]) {
          result[tier].push(fullPath);
        } else {
          result.unknown.push(fullPath);
        }
      }
    }
  } catch (e) {
    // Skip inaccessible directories
  }
}

/**
 * Check if memory should be cleaned up based on tier retention
 */
function shouldCleanup(filePath, tier) {
  if (!MEMORY_TIERS[tier]) return false;
  if (!MEMORY_TIERS[tier].autoCleanup) return false;
  if (PROTECTED_FILES.includes(path.basename(filePath))) return false;
  
  try {
    const stat = fs.statSync(filePath);
    const ageDays = (Date.now() - stat.mtime.getTime()) / (1000 * 60 * 60 * 24);
    return ageDays > MEMORY_TIERS[tier].retentionDays;
  } catch (e) {
    return false;
  }
}

/**
 * Clean up ephemeral memories that have expired
 */
function cleanupExpiredMemories(dryRun = true) {
  const memoriesByTier = getMemoriesByTier();
  const cleanupPlan = {
    ephemeral: [],
    normal: [],
    protected: [],
    errors: []
  };
  
  // Check ephemeral memories
  for (const filePath of memoriesByTier.ephemeral) {
    if (shouldCleanup(filePath, "ephemeral")) {
      cleanupPlan.ephemeral.push(filePath);
    }
  }
  
  // Check normal memories
  for (const filePath of memoriesByTier.normal) {
    if (shouldCleanup(filePath, "normal")) {
      cleanupPlan.normal.push(filePath);
    }
  }
  
  // Apply cleanup if not dry run
  if (!dryRun) {
    for (const filePath of cleanupPlan.ephemeral) {
      try {
        fs.unlinkSync(filePath);
      } catch (e) {
        cleanupPlan.errors.push({ file: filePath, error: e.message });
      }
    }
    
    for (const filePath of cleanupPlan.normal) {
      try {
        // Move to archive instead of delete for normal tier
        const archiveDir = path.join(MEMORY_DIR, "_archive");
        if (!fs.existsSync(archiveDir)) {
          fs.mkdirSync(archiveDir, { recursive: true });
        }
        fs.renameSync(filePath, path.join(archiveDir, path.basename(filePath)));
      } catch (e) {
        cleanupPlan.errors.push({ file: filePath, error: e.message });
      }
    }
  }
  
  return cleanupPlan;
}

/**
 * Migrate existing memories to tiered system
 */
function migrateMemoriesToTiered(dryRun = true) {
  const memoriesByTier = getMemoriesByTier();
  const migrations = [];
  
  // Categorize unknown memories
  for (const filePath of memoriesByTier.unknown) {
    const basename = path.basename(filePath);
    
    // Determine appropriate tier based on filename/content
    let suggestedTier = "normal";
    
    // Check file content for hints
    try {
      const content = fs.readFileSync(filePath, "utf-8");
      
      if (content.includes("[P0]") || content.includes("important") || 
          content.includes("critical") || content.includes("决策")) {
        suggestedTier = "persistent";
      } else if (content.includes("[ephemeral]") || content.includes("temp") ||
                 content.includes("临时")) {
        suggestedTier = "ephemeral";
      }
    } catch (e) {}
    
    migrations.push({
      file: filePath,
      currentType: "unknown",
      suggestedTier,
      basename
    });
  }
  
  // Apply migrations if not dry run
  if (!dryRun) {
    for (const m of migrations) {
      const result = setMemoryType(m.file, m.suggestedTier);
      m.applied = result.ok;
      m.error = result.error;
    }
  }
  
  return migrations;
}

/**
 * Get memory tier statistics
 */
function getMemoryStats() {
  const memoriesByTier = getMemoriesByTier();
  const stats = {
    persistent: {
      count: memoriesByTier.persistent.length,
      files: memoriesByTier.persistent.map(f => path.basename(f))
    },
    normal: {
      count: memoriesByTier.normal.length,
      files: memoriesByTier.normal.map(f => path.basename(f))
    },
    ephemeral: {
      count: memoriesByTier.ephemeral.length,
      files: memoriesByTier.ephemeral.map(f => path.basename(f))
    },
    unknown: {
      count: memoriesByTier.unknown.length,
      files: memoriesByTier.unknown.map(f => path.basename(f))
    }
  };
  
  return stats;
}

/**
 * Create a new memory with specified tier
 */
function createMemory(filePath, content, tier = DEFAULT_TIER) {
  if (!MEMORY_TIERS[tier]) {
    return { ok: false, error: `Invalid tier: ${tier}` };
  }
  
  try {
    // Ensure directory exists
    const dir = path.dirname(filePath);
    if (!fs.existsSync(dir)) {
      fs.mkdirSync(dir, { recursive: true });
    }
    
    // Add frontmatter with tier
    const timestamp = new Date().toISOString();
    const frontmatter = `---
memory_type: ${tier}
created: ${timestamp}
---

`;
    
    const fullContent = frontmatter + content;
    fs.writeFileSync(filePath, fullContent, "utf-8");
    
    return { ok: true, tier, file: filePath };
  } catch (e) {
    return { ok: false, error: e.message };
  }
}

/**
 * List memories eligible for cleanup
 */
function listCleanupCandidates() {
  const memoriesByTier = getMemoriesByTier();
  const candidates = [];
  
  for (const tier of ["ephemeral", "normal"]) {
    for (const filePath of memoriesByTier[tier]) {
      if (shouldCleanup(filePath, tier)) {
        try {
          const stat = fs.statSync(filePath);
          const ageDays = (Date.now() - stat.mtime.getTime()) / (1000 * 60 * 60 * 24);
          candidates.push({
            file: filePath,
            tier,
            ageDays: ageDays.toFixed(1),
            retentionDays: MEMORY_TIERS[tier].retentionDays,
            basename: path.basename(filePath)
          });
        } catch (e) {}
      }
    }
  }
  
  return candidates;
}

module.exports = {
  MEMORY_TIERS,
  DEFAULT_TIER,
  PROTECTED_FILES,
  getMemoryType,
  setMemoryType,
  getMemoriesByTier,
  shouldCleanup,
  cleanupExpiredMemories,
  migrateMemoriesToTiered,
  getMemoryStats,
  createMemory,
  listCleanupCandidates
};
