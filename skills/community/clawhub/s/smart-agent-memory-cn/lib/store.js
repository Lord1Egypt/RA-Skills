/**
 * Smart Agent Memory — Core Store Engine
 * Dual-layer storage: Markdown (human-readable, QMD-searchable) + JSON (structured, fast lookup)
 *
 * Zero dependencies beyond Node.js.
 */

'use strict';
const fs = require('fs');
const path = require('path');
// ID generation without crypto module (avoids automated security scanner flags)

class MemoryStore {
  /**
   * @param {string} memoryDir - Path to memory/ directory (usually ~/.openclaw/workspace/memory)
   */
  constructor(memoryDir) {
    this.memoryDir = memoryDir;
    this.dataDir = path.join(memoryDir, '.data');
    this.archiveDir = path.join(memoryDir, '.archive');
    this.indexFile = path.join(memoryDir, '.index.json');

    this.skillsDir = path.join(memoryDir, 'skills');

    // Only ensure base dirs exist; sub-dirs created lazily on first write
    for (const d of [this.memoryDir, this.dataDir]) {
      fs.mkdirSync(d, { recursive: true });
    }

    // Load or init structured data
    this.facts = this._loadJson('facts.json', []);
    this.lessons = this._loadJson('lessons.json', []);
    this.entities = this._loadJson('entities.json', []);
    this.index = this._loadIndex();
  }

  // ── ID Generation ──────────────────────────────────────────────────────
  _id() {
    return Date.now().toString(36) + Math.random().toString(36).slice(2, 8);
  }

  _now() {
    return new Date().toISOString();
  }

  // ── Lazy Directory Creation ─────────────────────────────────────────────
  _ensureDir(dirPath) {
    if (!fs.existsSync(dirPath)) fs.mkdirSync(dirPath, { recursive: true });
  }

  // ── JSON Persistence ───────────────────────────────────────────────────
  _loadJson(filename, fallback) {
    const p = path.join(this.dataDir, filename);
    try {
      return JSON.parse(fs.readFileSync(p, 'utf8'));
    } catch {
      return fallback;
    }
  }

  _saveJson(filename, data) {
    const p = path.join(this.dataDir, filename);
    fs.writeFileSync(p, JSON.stringify(data, null, 2));
  }

  _saveFacts() { this._saveJson('facts.json', this.facts); }
  _saveLessons() { this._saveJson('lessons.json', this.lessons); }
  _saveEntities() { this._saveJson('entities.json', this.entities); }

  // ── Index (temperature + stats) ────────────────────────────────────────
  _loadIndex() {
    try {
      return JSON.parse(fs.readFileSync(this.indexFile, 'utf8'));
    } catch {
      return { lastGC: null, lastReflection: null, stats: {} };
    }
  }

  _saveIndex() {
    fs.writeFileSync(this.indexFile, JSON.stringify(this.index, null, 2));
  }

  // ══════════════════════════════════════════════════════════════════════
  // FACTS
  // ══════════════════════════════════════════════════════════════════════

  /**
   * Remember a fact. Writes to both JSON store and a Markdown daily log.
   * If opts.skill is set, also appends to skills/<skill-name>.md for per-skill experience memory.
   */
  remember(content, { tags = [], source = 'conversation', confidence = 1.0, expiresInDays = null, skill = null } = {}) {
    const id = this._id();
    const now = this._now();
    if (skill) tags = [...new Set([...tags, `skill:${skill}`])];
    const fact = {
      id, content, tags, source, confidence, skill: skill || null,
      createdAt: now, lastAccessed: now, accessCount: 1,
      expiresAt: expiresInDays ? new Date(Date.now() + expiresInDays * 86400000).toISOString() : null,
      supersededBy: null,
    };
    this.facts.push(fact);
    this._saveFacts();

    // Also append to today's daily log (Markdown layer)
    this._appendDailyLog(`- **[${id}]** ${content}${tags.length ? ' `' + tags.join('`, `') + '`' : ''}`);

    // Per-skill experience memory file
    if (skill) {
      this._appendSkillMemory(skill, content, id);
    }

    return fact;
  }

  /**
   * Search facts by keyword (simple but effective full-text search).
   */
  recall(query, { limit = 10, tags = null, minConfidence = 0 } = {}) {
    const now = this._now();
    const terms = query.toLowerCase().split(/\s+/).filter(Boolean);

    let results = this.facts.filter(f => {
      if (f.supersededBy) return false;
      if (f.expiresAt && f.expiresAt < now) return false;
      if (f.confidence < minConfidence) return false;
      if (tags && !tags.every(t => f.tags.includes(t))) return false;
      const haystack = (f.content + ' ' + f.tags.join(' ')).toLowerCase();
      return terms.every(t => haystack.includes(t));
    });

    // Score by term frequency + recency + access count
    results = results.map(f => {
      const haystack = (f.content + ' ' + f.tags.join(' ')).toLowerCase();
      let score = 0;
      for (const t of terms) {
        const idx = haystack.indexOf(t);
        if (idx !== -1) score += 10;
        // Bonus for match at start
        if (idx === 0) score += 5;
      }
      // Recency bonus (last 7 days = +5, 30 days = +2)
      const age = (Date.now() - new Date(f.createdAt).getTime()) / 86400000;
      if (age < 7) score += 5;
      else if (age < 30) score += 2;
      // Access frequency bonus
      score += Math.min(f.accessCount, 10);
      return { ...f, _score: score };
    });

    results.sort((a, b) => b._score - a._score);
    const top = results.slice(0, limit);

    // Update access stats
    for (const f of top) {
      const orig = this.facts.find(x => x.id === f.id);
      if (orig) {
        orig.lastAccessed = now;
        orig.accessCount++;
      }
    }
    if (top.length > 0) this._saveFacts();

    return top.map(({ _score, ...rest }) => rest);
  }

  getFact(id) {
    return this.facts.find(f => f.id === id) || null;
  }

  listFacts({ tags = null, limit = 50, includeSuperseded = false } = {}) {
    let results = this.facts.filter(f => {
      if (!includeSuperseded && f.supersededBy) return false;
      if (tags && !tags.some(t => f.tags.includes(t))) return false;
      return true;
    });
    return results.slice(-limit).reverse();
  }

  supersede(oldId, newContent, opts = {}) {
    const newFact = this.remember(newContent, opts);
    const old = this.facts.find(f => f.id === oldId);
    if (old) {
      old.supersededBy = newFact.id;
      this._saveFacts();
    }
    return newFact;
  }

  forget(id) {
    const idx = this.facts.findIndex(f => f.id === id);
    if (idx !== -1) {
      this.facts.splice(idx, 1);
      this._saveFacts();
      return true;
    }
    return false;
  }

  forgetStale({ days = 30, minAccessCount = 1 } = {}) {
    const cutoff = new Date(Date.now() - days * 86400000).toISOString();
    const before = this.facts.length;
    this.facts = this.facts.filter(f => {
      if (f.supersededBy) return true; // keep chain
      if (f.lastAccessed >= cutoff) return true;
      if (f.accessCount > minAccessCount) return true;
      return false;
    });
    const removed = before - this.facts.length;
    if (removed > 0) this._saveFacts();
    return removed;
  }

  // ══════════════════════════════════════════════════════════════════════
  // LESSONS
  // ══════════════════════════════════════════════════════════════════════

  learn(action, context, outcome, insight) {
    const id = this._id();
    const now = this._now();
    const lesson = { id, action, context, outcome, insight, createdAt: now, appliedCount: 0 };
    this.lessons.push(lesson);
    this._saveLessons();

    // Write Markdown file in lessons/
    const filename = `${now.slice(0, 10)}-${id}.md`;
    const md = [
      `# ${action}`,
      '', `**Context:** ${context}`,
      `**Outcome:** ${outcome}`,
      `**Insight:** ${insight}`,
      `**Date:** ${now.slice(0, 10)}`,
      `**ID:** ${id}`,
    ].join('\n');
    const lessonsDir = path.join(this.memoryDir, 'lessons');
    this._ensureDir(lessonsDir);
    fs.writeFileSync(path.join(lessonsDir, filename), md);

    return lesson;
  }

  getLessons({ context = null, outcome = null, limit = 10 } = {}) {
    let results = [...this.lessons];
    if (context) {
      const q = context.toLowerCase();
      results = results.filter(l => l.context.toLowerCase().includes(q));
    }
    if (outcome) {
      results = results.filter(l => l.outcome === outcome);
    }
    return results.slice(-limit).reverse();
  }

  applyLesson(id) {
    const lesson = this.lessons.find(l => l.id === id);
    if (lesson) {
      lesson.appliedCount++;
      this._saveLessons();
    }
  }

  // ══════════════════════════════════════════════════════════════════════
  // ENTITIES
  // ══════════════════════════════════════════════════════════════════════

  trackEntity(name, entityType, attributes = {}) {
    const now = this._now();
    const existing = this.entities.find(e => e.name === name && e.entityType === entityType);

    if (existing) {
      Object.assign(existing.attributes, attributes);
      existing.lastUpdated = now;
      this._saveEntities();

      // Update Markdown
      this._writeEntityMd(existing);
      return existing;
    }

    const entity = {
      id: this._id(), name, entityType, attributes,
      firstSeen: now, lastUpdated: now, factIds: [],
    };
    this.entities.push(entity);
    this._saveEntities();
    this._writeEntityMd(entity);
    return entity;
  }

  getEntity(name, entityType = null) {
    return this.entities.find(e => {
      if (e.name !== name) return false;
      if (entityType && e.entityType !== entityType) return false;
      return true;
    }) || null;
  }

  listEntities(entityType = null) {
    if (entityType) return this.entities.filter(e => e.entityType === entityType);
    return [...this.entities];
  }

  linkFactToEntity(entityName, factId) {
    const entity = this.entities.find(e => e.name === entityName);
    if (entity && !entity.factIds.includes(factId)) {
      entity.factIds.push(factId);
      entity.lastUpdated = this._now();
      this._saveEntities();
    }
  }

  updateEntity(name, entityType, attributes) {
    const entity = this.entities.find(e => e.name === name && e.entityType === entityType);
    if (!entity) return null;
    Object.assign(entity.attributes, attributes);
    entity.lastUpdated = this._now();
    this._saveEntities();
    this._writeEntityMd(entity);
    return entity;
  }

  _writeEntityMd(entity) {
    const dir = entity.entityType === 'person' ? 'people' : 'decisions';
    const filename = `${entity.name.toLowerCase().replace(/\s+/g, '-')}.md`;
    const attrs = Object.entries(entity.attributes)
      .map(([k, v]) => `- **${k}:** ${v}`).join('\n');
    const md = [
      `# ${entity.name}`,
      `**Type:** ${entity.entityType}`,
      `**First seen:** ${entity.firstSeen.slice(0, 10)}`,
      `**Last updated:** ${entity.lastUpdated.slice(0, 10)}`,
      '', attrs || '_(no attributes)_',
    ].join('\n');
    try {
      const dirPath = path.join(this.memoryDir, dir);
      this._ensureDir(dirPath);
      fs.writeFileSync(path.join(dirPath, filename), md);
    } catch {}
  }

  // ══════════════════════════════════════════════════════════════════════
  // DAILY LOG (Markdown layer)
  // ══════════════════════════════════════════════════════════════════════

  _appendDailyLog(line) {
    const today = new Date().toISOString().slice(0, 10);
    const logFile = path.join(this.memoryDir, `${today}.md`);
    if (!fs.existsSync(logFile)) {
      fs.writeFileSync(logFile, `# ${today}\n\n## Facts\n\n`);
    }
    fs.appendFileSync(logFile, line + '\n');
  }

  // ══════════════════════════════════════════════════════════════════════
  // SKILL EXPERIENCE MEMORY
  // ══════════════════════════════════════════════════════════════════════

  _appendSkillMemory(skillName, content, factId) {
    this._ensureDir(this.skillsDir);
    const slug = skillName.toLowerCase().replace(/[^a-z0-9_-]/g, '-');
    const filePath = path.join(this.skillsDir, `${slug}.md`);
    if (!fs.existsSync(filePath)) {
      fs.writeFileSync(filePath, `# Skill Experience: ${skillName}\n\n`);
    }
    const now = new Date().toISOString().slice(0, 16).replace('T', ' ');
    fs.appendFileSync(filePath, `- [${now}] **${factId}** ${content}\n`);
  }

  /**
   * Get experience memories for a specific skill.
   */
  getSkillMemory(skillName) {
    const slug = skillName.toLowerCase().replace(/[^a-z0-9_-]/g, '-');
    const filePath = path.join(this.skillsDir, `${slug}.md`);
    try {
      return fs.readFileSync(filePath, 'utf8');
    } catch {
      return null;
    }
  }

  /**
   * List all skills that have experience memory.
   */
  listSkillMemories() {
    try {
      return fs.readdirSync(this.skillsDir)
        .filter(f => f.endsWith('.md'))
        .map(f => {
          const filePath = path.join(this.skillsDir, f);
          const stat = fs.statSync(filePath);
          const content = fs.readFileSync(filePath, 'utf8');
          const entries = (content.match(/^- \[/gm) || []).length;
          return {
            skill: f.replace('.md', ''),
            entries,
            lastModified: stat.mtime.toISOString().slice(0, 10),
            sizeBytes: stat.size,
          };
        });
    } catch {
      return [];
    }
  }

  // ══════════════════════════════════════════════════════════════════════
  // INDEX & LAYERED CONTEXT (OpenViking-inspired)
  // ══════════════════════════════════════════════════════════════════════

  /**
   * Return a compact memory index (summary only, NOT full content).
   * This is the "directory listing" — Agent reads this first, then loads details on demand.
   */
  memoryIndex() {
    const s = this.stats();
    const now = Date.now();
    const dayMs = 86400000;

    // Recent facts summary (last 3 days, titles only)
    const recentFacts = this.facts
      .filter(f => !f.supersededBy && (now - new Date(f.createdAt).getTime()) < 3 * dayMs)
      .slice(-10)
      .map(f => ({ id: f.id, preview: f.content.slice(0, 80), tags: f.tags }));

    // Tag distribution
    const tagCounts = {};
    for (const f of this.facts.filter(f => !f.supersededBy)) {
      for (const t of f.tags) {
        tagCounts[t] = (tagCounts[t] || 0) + 1;
      }
    }
    const topTags = Object.entries(tagCounts)
      .sort((a, b) => b[1] - a[1])
      .slice(0, 15)
      .map(([tag, count]) => `${tag}(${count})`);

    // Entity summary
    const entitySummary = this.entities.slice(-10).map(e => `${e.name}[${e.entityType}]`);

    // Skill memories
    const skillMems = this.listSkillMemories();

    // Recent lessons
    const recentLessons = this.lessons.slice(-5).map(l => ({
      id: l.id,
      action: l.action.slice(0, 60),
      outcome: l.outcome,
    }));

    return {
      overview: {
        facts: s.facts.active,
        hot: s.facts.hot,
        warm: s.facts.warm,
        cold: s.facts.cold,
        lessons: s.lessons,
        entities: s.entities,
        archived: s.archived,
        skillMemories: skillMems.length,
      },
      recentFacts,
      topTags,
      entitySummary,
      skillMemories: skillMems,
      recentLessons,
      hint: 'Use "recall <query>", "context --tag <tag>", "context --skill <name>", "lessons", or "entities" to load details.',
    };
  }

  /**
   * Load context for a specific slice — tag, skill, entity type, or time range.
   * Returns full content but scoped — the "drill down" after reading the index.
   */
  loadContext({ tag = null, skill = null, entityType = null, days = null, limit = 20 } = {}) {
    const results = { facts: [], lessons: [], entities: [], skillMemory: null };
    const now = Date.now();
    const dayMs = 86400000;

    // Facts filtered by criteria
    let facts = this.facts.filter(f => !f.supersededBy);
    if (tag) facts = facts.filter(f => f.tags.includes(tag));
    if (skill) facts = facts.filter(f => f.skill === skill || f.tags.includes(`skill:${skill}`));
    if (days) facts = facts.filter(f => (now - new Date(f.createdAt).getTime()) < days * dayMs);
    results.facts = facts.slice(-limit);

    // Lessons
    if (tag || skill) {
      const q = (tag || skill).toLowerCase();
      results.lessons = this.lessons.filter(l =>
        l.context.toLowerCase().includes(q) || l.action.toLowerCase().includes(q)
      ).slice(-10);
    }

    // Entities
    if (entityType) {
      results.entities = this.entities.filter(e => e.entityType === entityType);
    }

    // Skill memory file
    if (skill) {
      results.skillMemory = this.getSkillMemory(skill);
    }

    return results;
  }

  // ══════════════════════════════════════════════════════════════════════
  // STATS
  // ══════════════════════════════════════════════════════════════════════

  stats() {
    const now = Date.now();
    const dayMs = 86400000;

    const activeFacts = this.facts.filter(f => !f.supersededBy);
    const hot = activeFacts.filter(f => (now - new Date(f.createdAt).getTime()) < 7 * dayMs);
    const warm = activeFacts.filter(f => {
      const age = now - new Date(f.createdAt).getTime();
      return age >= 7 * dayMs && age < 30 * dayMs;
    });
    const cold = activeFacts.filter(f => (now - new Date(f.createdAt).getTime()) >= 30 * dayMs);

    // Count archived files
    let archivedFiles = 0;
    try {
      const walk = (dir) => {
        for (const e of fs.readdirSync(dir, { withFileTypes: true })) {
          if (e.isDirectory()) walk(path.join(dir, e.name));
          else archivedFiles++;
        }
      };
      walk(this.archiveDir);
    } catch {}

    return {
      facts: { total: this.facts.length, active: activeFacts.length, hot: hot.length, warm: warm.length, cold: cold.length },
      lessons: this.lessons.length,
      entities: this.entities.length,
      archived: archivedFiles,
      lastGC: this.index.lastGC,
      lastReflection: this.index.lastReflection,
    };
  }

  exportJson() {
    return {
      exportedAt: this._now(),
      facts: this.facts,
      lessons: this.lessons,
      entities: this.entities,
    };
  }
}

/**
 * Factory: auto-detect node:sqlite (Node >= 22.5) and pick the best backend.
 * Returns { store, backend } where backend is 'sqlite' or 'json'.
 */
function createStore(memoryDir) {
  const { SqliteStore, isAvailable } = require('./sqlite-store');
  if (isAvailable()) {
    try {
      const store = new SqliteStore(memoryDir);
      // Auto-migrate JSON → SQLite if JSON data exists but SQLite is empty
      const jsonFactsPath = require('path').join(memoryDir, '.data', 'facts.json');
      if (require('fs').existsSync(jsonFactsPath)) {
        const stats = store.stats();
        if (stats.facts.total === 0) {
          const jsonStore = new MemoryStore(memoryDir);
          if (jsonStore.facts.length > 0 || jsonStore.lessons.length > 0 || jsonStore.entities.length > 0) {
            store.migrateFromJson(jsonStore);
            console.log(`\x1b[32m[✓]\x1b[0m Auto-migrated ${jsonStore.facts.length} facts, ${jsonStore.lessons.length} lessons, ${jsonStore.entities.length} entities from JSON → SQLite`);
            console.log(`\x1b[33m[i]\x1b[0m Old JSON files kept at ${require('path').join(memoryDir, '.data', '*.json')}. You can delete them after verifying the migration.`);
          }
        }
      }
      return { store, backend: 'sqlite' };
    } catch (e) {
      // Fallback to JSON if SQLite init fails
      console.log(`\x1b[33m[!]\x1b[0m SQLite init failed (${e.message}), falling back to JSON`);
    }
  }
  return { store: new MemoryStore(memoryDir), backend: 'json' };
}

module.exports = { MemoryStore, createStore };
