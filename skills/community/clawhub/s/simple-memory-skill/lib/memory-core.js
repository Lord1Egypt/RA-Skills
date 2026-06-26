/**
 * Simple Local Memory - Core Library
 * Zero-dependency memory system with local storage and search
 */

const fs = require('fs');
const path = require('path');

class MemoryCore {
  constructor(baseDir = process.cwd()) {
    this.baseDir = baseDir;
    this.memoriesDir = path.join(baseDir, 'memories');
    this.sessionStatePath = path.join(baseDir, 'SESSION-STATE.json');
    this.ensureDirectories();
  }

  ensureDirectories() {
    if (!fs.existsSync(this.memoriesDir)) {
      fs.mkdirSync(this.memoriesDir, { recursive: true });
    }
  }

  generateId() {
    return `${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
  }

  getTodayFilePath() {
    const today = new Date().toISOString().split('T')[0];
    return path.join(this.memoriesDir, `${today}.json`);
  }

  getCategoryFilePath(category) {
    return path.join(this.memoriesDir, `${category}.json`);
  }

  /**
   * Store a memory
   */
  storeMemory(content, options = {}) {
    const {
      type = 'fact',
      importance = 0.5,
      tags = [],
      context = ''
    } = options;

    const memory = {
      id: this.generateId(),
      type,
      content,
      importance: parseFloat(importance),
      tags: Array.isArray(tags) ? tags : [tags],
      context,
      timestamp: new Date().toISOString()
    };

    // Add to daily file
    this.addToDailyFile(memory);

    // Add to category file if applicable
    if (['preference', 'decision', 'lesson'].includes(type)) {
      this.addToCategoryFile(memory);
    }

    return memory;
  }

  addToDailyFile(memory) {
    const dailyPath = this.getTodayFilePath();
    let dailyData = { date: new Date().toISOString().split('T')[0], memories: [] };

    if (fs.existsSync(dailyPath)) {
      try {
        dailyData = JSON.parse(fs.readFileSync(dailyPath, 'utf8'));
      } catch (e) {
        console.error('Error reading daily file:', e.message);
      }
    }

    dailyData.memories.push(memory);
    fs.writeFileSync(dailyPath, JSON.stringify(dailyData, null, 2));
  }

  addToCategoryFile(memory) {
    const categoryPath = this.getCategoryFilePath(memory.type + 's');
    let categoryData = {};

    if (fs.existsSync(categoryPath)) {
      try {
        categoryData = JSON.parse(fs.readFileSync(categoryPath, 'utf8'));
      } catch (e) {
        console.error('Error reading category file:', e.message);
      }
    }

    const key = memory.type + 's';
    if (!categoryData[key]) {
      categoryData[key] = [];
    }

    const entry = {
      id: memory.id,
      content: memory.content,
      set_at: memory.timestamp,
      importance: memory.importance,
      tags: memory.tags,
      context: memory.context
    };

    categoryData[key].push(entry);
    fs.writeFileSync(categoryPath, JSON.stringify(categoryData, null, 2));
  }

  /**
   * Search memories using TF-IDF like scoring
   */
  searchMemories(query, options = {}) {
    const {
      limit = 10,
      type = null,
      minImportance = 0,
      days = 30
    } = options;

    const queryTokens = this.tokenize(query.toLowerCase());
    const allMemories = this.loadRecentMemories(days);

    let scoredMemories = allMemories.map(memory => {
      const content = memory.content.toLowerCase();
      const relevanceScore = this.calculateRelevance(queryTokens, content);
      const recencyBoost = this.calculateRecencyBoost(memory.timestamp);
      const importanceBoost = memory.importance || 0.5;

      return {
        ...memory,
        score: relevanceScore + recencyBoost + importanceBoost
      };
    });

    // Filter by type if specified
    if (type) {
      scoredMemories = scoredMemories.filter(m => m.type === type);
    }

    // Filter by importance
    scoredMemories = scoredMemories.filter(m => m.importance >= minImportance);

    // Sort by score and limit
    return scoredMemories
      .sort((a, b) => b.score - a.score)
      .slice(0, limit);
  }

  loadRecentMemories(days = 30) {
    const memories = [];
    const cutoffDate = new Date();
    cutoffDate.setDate(cutoffDate.getDate() - days);

    // Load daily files
    const files = fs.readdirSync(this.memoriesDir)
      .filter(f => f.endsWith('.json') && f.match(/^\d{4}-\d{2}-\d{2}\.json$/));

    for (const file of files) {
      const filePath = path.join(this.memoriesDir, file);
      try {
        const data = JSON.parse(fs.readFileSync(filePath, 'utf8'));
        if (data.memories) {
          memories.push(...data.memories);
        }
      } catch (e) {
        console.error(`Error reading ${file}:`, e.message);
      }
    }

    return memories.filter(m => new Date(m.timestamp) >= cutoffDate);
  }

  tokenize(text) {
    return text.split(/\s+/).filter(token => token.length > 2);
  }

  calculateRelevance(queryTokens, content) {
    let score = 0;
    const contentTokens = this.tokenize(content);
    const contentTokenSet = new Set(contentTokens);

    for (const token of queryTokens) {
      // Exact match bonus
      if (content.includes(token)) {
        score += 0.5;
      }

      // Token match bonus
      if (contentTokenSet.has(token)) {
        score += 0.3;
      }

      // Partial match bonus
      for (const contentToken of contentTokens) {
        if (contentToken.includes(token) || token.includes(contentToken)) {
          score += 0.1;
        }
      }
    }

    return score;
  }

  calculateRecencyBoost(timestamp) {
    const age = Date.now() - new Date(timestamp).getTime();
    const daysOld = age / (1000 * 60 * 60 * 24);

    // Decay formula: 0.2 * e^(-days/7)
    // Gives higher boost to recent memories
    return 0.2 * Math.exp(-daysOld / 7);
  }

  /**
   * List memories
   */
  listMemories(options = {}) {
    const { limit = 20, type = null, date = null } = options;

    let memories;

    if (date) {
      const datePath = path.join(this.memoriesDir, `${date}.json`);
      if (fs.existsSync(datePath)) {
        const data = JSON.parse(fs.readFileSync(datePath, 'utf8'));
        memories = data.memories || [];
      } else {
        memories = [];
      }
    } else {
      memories = this.loadRecentMemories(30);
    }

    if (type) {
      memories = memories.filter(m => m.type === type);
    }

    return memories.slice(0, limit);
  }

  /**
   * Get memory statistics
   */
  getStats() {
    const stats = {
      totalMemories: 0,
      byType: {},
      byImportance: { high: 0, medium: 0, low: 0 },
      oldestMemory: null,
      newestMemory: null,
      storageSize: 0
    };

    const files = fs.readdirSync(this.memoriesDir)
      .filter(f => f.endsWith('.json'));

    for (const file of files) {
      const filePath = path.join(this.memoriesDir, file);
      const stat = fs.statSync(filePath);
      stats.storageSize += stat.size;

      try {
        const data = JSON.parse(fs.readFileSync(filePath, 'utf8'));

        if (data.memories) {
          for (const memory of data.memories) {
            stats.totalMemories++;

            // Count by type
            stats.byType[memory.type] = (stats.byType[memory.type] || 0) + 1;

            // Count by importance
            if (memory.importance >= 0.8) {
              stats.byImportance.high++;
            } else if (memory.importance >= 0.5) {
              stats.byImportance.medium++;
            } else {
              stats.byImportance.low++;
            }

            // Track oldest/newest
            const memoryDate = new Date(memory.timestamp);
            if (!stats.oldestMemory || memoryDate < new Date(stats.oldestMemory)) {
              stats.oldestMemory = memory.timestamp;
            }
            if (!stats.newestMemory || memoryDate > new Date(stats.newestMemory)) {
              stats.newestMemory = memory.timestamp;
            }
          }
        }
      } catch (e) {
        // Skip invalid files
      }
    }

    return stats;
  }

  /**
   * Export memories
   */
  exportMemories(format = 'json') {
    const allMemories = this.loadRecentMemories(365); // Load all

    if (format === 'json') {
      return JSON.stringify({
        exported_at: new Date().toISOString(),
        total: allMemories.length,
        memories: allMemories
      }, null, 2);
    } else if (format === 'markdown') {
      let markdown = '# Memory Export\n\n';
      markdown += `Exported: ${new Date().toISOString()}\n`;
      markdown += `Total memories: ${allMemories.length}\n\n`;

      for (const memory of allMemories) {
        markdown += `## ${memory.type}: ${memory.content}\n`;
        markdown += `- Importance: ${memory.importance}\n`;
        markdown += `- Date: ${memory.timestamp}\n`;
        if (memory.tags && memory.tags.length > 0) {
          markdown += `- Tags: ${memory.tags.join(', ')}\n`;
        }
        if (memory.context) {
          markdown += `- Context: ${memory.context}\n`;
        }
        markdown += '\n';
      }

      return markdown;
    }

    throw new Error(`Unsupported format: ${format}`);
  }

  /**
   * Import memories
   */
  importMemories(data) {
    let imported = 0;

    try {
      const importedData = JSON.parse(data);

      if (!importedData.memories || !Array.isArray(importedData.memories)) {
        throw new Error('Invalid import format');
      }

      for (const memory of importedData.memories) {
        // Create a new entry with new ID
        const newMemory = {
          id: this.generateId(),
          type: memory.type || 'fact',
          content: memory.content,
          importance: memory.importance || 0.5,
          tags: memory.tags || [],
          context: memory.context || '',
          timestamp: memory.timestamp || new Date().toISOString()
        };

        this.addToDailyFile(newMemory);
        imported++;
      }
    } catch (e) {
      throw new Error(`Import failed: ${e.message}`);
    }

    return imported;
  }

  /**
   * Update session state
   */
  updateSessionState(updates) {
    let sessionState = {
      current_task: '',
      key_context: [],
      pending_actions: [],
      recent_decisions: [],
      last_updated: new Date().toISOString()
    };

    // Load existing if available
    if (fs.existsSync(this.sessionStatePath)) {
      try {
        sessionState = {
          ...sessionState,
          ...JSON.parse(fs.readFileSync(this.sessionStatePath, 'utf8'))
        };
      } catch (e) {
        // Use defaults
      }
    }

    // Apply updates
    const updated = { ...sessionState, ...updates, last_updated: new Date().toISOString() };
    fs.writeFileSync(this.sessionStatePath, JSON.stringify(updated, null, 2));

    return updated;
  }

  getSessionState() {
    if (fs.existsSync(this.sessionStatePath)) {
      try {
        return JSON.parse(fs.readFileSync(this.sessionStatePath, 'utf8'));
      } catch (e) {
        return null;
      }
    }
    return null;
  }
}

module.exports = MemoryCore;
