/**
 * Search & Recommendation Engine
 */

const fs = require('fs');
const path = require('path');

class SearchEngine {
  constructor(options = {}) {
    this.registry = options.registry;
    this.dataDir = options.dataDir || './.marketplace-cache';
    this.indexPath = path.join(this.dataDir, 'search-index.json');
    this.userPrefsPath = path.join(this.dataDir, 'user-preferences.json');
    
    this._ensureDataDir();
    this._loadIndex();
    this._loadUserPreferences();
  }

  _ensureDataDir() {
    if (!fs.existsSync(this.dataDir)) {
      fs.mkdirSync(this.dataDir, { recursive: true });
    }
  }

  _loadIndex() {
    if (fs.existsSync(this.indexPath)) {
      try {
        const data = fs.readFileSync(this.indexPath, 'utf8');
        this.index = JSON.parse(data);
      } catch (err) {
        this._initIndex();
      }
    } else {
      this._initIndex();
    }
  }

  _initIndex() {
    this.index = {
      keywords: {},
      categories: {},
      tags: {},
      authors: {},
      lastUpdated: Date.now()
    };
  }

  _saveIndex() {
    this.index.lastUpdated = Date.now();
    fs.writeFileSync(this.indexPath, JSON.stringify(this.index, null, 2));
  }

  _loadUserPreferences() {
    if (fs.existsSync(this.userPrefsPath)) {
      try {
        const data = fs.readFileSync(this.userPrefsPath, 'utf8');
        this.userPreferences = JSON.parse(data);
      } catch (err) {
        this.userPreferences = {};
      }
    } else {
      this.userPreferences = {};
    }
  }

  _saveUserPreferences() {
    fs.writeFileSync(this.userPrefsPath, JSON.stringify(this.userPreferences, null, 2));
  }

  // Build search index from skills
  async buildIndex(skills) {
    this._initIndex();

    for (const skill of skills) {
      this._indexSkill(skill);
    }

    this._saveIndex();
    return { indexed: skills.length };
  }

  _indexSkill(skill) {
    const name = skill.name;

    // Index by keywords
    const keywords = this._extractKeywords(skill);
    for (const keyword of keywords) {
      if (!this.index.keywords[keyword]) {
        this.index.keywords[keyword] = [];
      }
      if (!this.index.keywords[keyword].includes(name)) {
        this.index.keywords[keyword].push(name);
      }
    }

    // Index by category
    if (skill.categories) {
      for (const cat of skill.categories) {
        if (!this.index.categories[cat]) {
          this.index.categories[cat] = [];
        }
        if (!this.index.categories[cat].includes(name)) {
          this.index.categories[cat].push(name);
        }
      }
    }

    // Index by tags
    if (skill.tags) {
      for (const tag of skill.tags) {
        if (!this.index.tags[tag]) {
          this.index.tags[tag] = [];
        }
        if (!this.index.tags[tag].includes(name)) {
          this.index.tags[tag].push(name);
        }
      }
    }

    // Index by author
    if (skill.author) {
      if (!this.index.authors[skill.author]) {
        this.index.authors[skill.author] = [];
      }
      if (!this.index.authors[skill.author].includes(name)) {
        this.index.authors[skill.author].push(name);
      }
    }
  }

  _extractKeywords(skill) {
    const keywords = new Set();
    
    // From name
    if (skill.name) {
      skill.name.toLowerCase().split(/[-_\s]+/).forEach(w => keywords.add(w));
    }
    
    // From description
    if (skill.description) {
      skill.description.toLowerCase().split(/\W+/).forEach(w => {
        if (w.length > 2) keywords.add(w);
      });
    }
    
    // From tags
    if (skill.tags) {
      skill.tags.forEach(t => keywords.add(t.toLowerCase()));
    }

    return Array.from(keywords);
  }

  // Search skills
  async search(query, options = {}) {
    const { 
      category = null, 
      sort = 'relevance',
      limit = 20, 
      offset = 0 
    } = options;

    if (!query || query.trim() === '') {
      // Return all skills if no query
      const result = await this.registry.listSkills({ category, limit, offset });
      return { ...result, query: '' };
    }

    const normalizedQuery = query.toLowerCase().trim();
    const searchTerms = normalizedQuery.split(/\s+/);

    // Collect matching skills
    const matches = new Map();

    for (const term of searchTerms) {
      // Search in index
      for (const [keyword, skills] of Object.entries(this.index.keywords)) {
        if (keyword.includes(term) || term.includes(keyword)) {
          for (const skillName of skills) {
            matches.set(skillName, (matches.get(skillName) || 0) + 1);
          }
        }
      }

      // Search in tags
      for (const [tag, skills] of Object.entries(this.index.tags)) {
        if (tag.includes(term) || term.includes(tag)) {
          for (const skillName of skills) {
            matches.set(skillName, (matches.get(skillName) || 0) + 2);
          }
        }
      }

      // Search in categories
      if (category) {
        const catSkills = this.index.categories[category] || [];
        for (const skillName of catSkills) {
          if (matches.has(skillName)) {
            matches.set(skillName, matches.get(skillName) + 1);
          }
        }
      }
    }

    // Fetch full skill data and apply filters
    const results = [];
    for (const [skillName, score] of matches.entries()) {
      try {
        const skill = await this.registry.getSkill(skillName);
        
        if (category && !skill.categories?.includes(category)) {
          continue;
        }

        results.push({ ...skill, searchScore: score });
      } catch (err) {
        // Skip unavailable skills
      }
    }

    // Sort results
    if (sort === 'relevance') {
      results.sort((a, b) => b.searchScore - a.searchScore);
    } else if (sort === 'rating') {
      results.sort((a, b) => (b.rating || 0) - (a.rating || 0));
    } else if (sort === 'downloads') {
      results.sort((a, b) => (b.downloads || 0) - (a.downloads || 0));
    } else if (sort === 'newest') {
      results.sort((a, b) => (b.createdAt || 0) - (a.createdAt || 0));
    }

    const total = results.length;
    const paginated = results.slice(offset, offset + limit);

    return {
      skills: paginated,
      total,
      offset,
      limit,
      query: normalizedQuery
    };
  }

  // Get related skills
  async getRelatedSkills(skillName, limit = 5) {
    try {
      const skill = await this.registry.getSkill(skillName);
      const related = new Map();

      // By category
      if (skill.categories) {
        for (const cat of skill.categories) {
          const catSkills = this.index.categories[cat] || [];
          for (const name of catSkills) {
            if (name !== skillName) {
              related.set(name, (related.get(name) || 0) + 3);
            }
          }
        }
      }

      // By tags
      if (skill.tags) {
        for (const tag of skill.tags) {
          const tagSkills = this.index.tags[tag] || [];
          for (const name of tagSkills) {
            if (name !== skillName) {
              related.set(name, (related.get(name) || 0) + 2);
            }
          }
        }
      }

      // By author
      if (skill.author) {
        const authorSkills = this.index.authors[skill.author] || [];
        for (const name of authorSkills) {
          if (name !== skillName) {
            related.set(name, (related.get(name) || 0) + 1);
          }
        }
      }

      // Sort and fetch full data
      const sorted = Array.from(related.entries())
        .sort((a, b) => b[1] - a[1])
        .slice(0, limit);

      const results = [];
      for (const [name, score] of sorted) {
        try {
          const relatedSkill = await this.registry.getSkill(name);
          results.push({ ...relatedSkill, relationScore: score });
        } catch (err) {
          // Skip unavailable skills
        }
      }

      return results;
    } catch (err) {
      return [];
    }
  }

  // Record user interaction for personalization
  recordInteraction(userId, skillName, interactionType) {
    if (!this.userPreferences[userId]) {
      this.userPreferences[userId] = {
        installed: [],
        searched: [],
        viewed: [],
        rated: [],
        categoryPreferences: {}
      };
    }

    const prefs = this.userPreferences[userId];
    const timestamp = Date.now();

    switch (interactionType) {
      case 'install':
        if (!prefs.installed.includes(skillName)) {
          prefs.installed.push(skillName);
        }
        break;
      case 'search':
        prefs.searched.push({ query: skillName, timestamp });
        break;
      case 'view':
        prefs.viewed.push({ skill: skillName, timestamp });
        break;
      case 'rate':
        if (!prefs.rated.includes(skillName)) {
          prefs.rated.push(skillName);
        }
        break;
    }

    this._saveUserPreferences();
  }

  // Get personalized recommendations
  async getRecommendations(userId, limit = 10) {
    if (!this.userPreferences[userId]) {
      // Return popular skills for new users
      return this.getPopularSkills(limit);
    }

    const prefs = this.userPreferences[userId];
    const scores = new Map();

    // Score based on installed skills
    for (const skillName of prefs.installed) {
      try {
        const skill = await this.registry.getSkill(skillName);
        
        // Related skills get high score
        const related = await this.getRelatedSkills(skillName, 10);
        for (const r of related) {
          if (!prefs.installed.includes(r.name)) {
            scores.set(r.name, (scores.get(r.name) || 0) + r.relationScore * 2);
          }
        }

        // Same category skills
        if (skill.categories) {
          for (const cat of skill.categories) {
            const catSkills = this.index.categories[cat] || [];
            for (const name of catSkills) {
              if (!prefs.installed.includes(name)) {
                scores.set(name, (scores.get(name) || 0) + 1);
              }
            }
          }
        }
      } catch (err) {
        // Skip
      }
    }

    // Score based on search history
    const recentSearches = prefs.searched.slice(-10);
    for (const search of recentSearches) {
      const results = await this.search(search.query, { limit: 5 });
      for (const skill of results.skills) {
        if (!prefs.installed.includes(skill.name)) {
          scores.set(skill.name, (scores.get(skill.name) || 0) + 1);
        }
      }
    }

    // Sort and return
    const sorted = Array.from(scores.entries())
      .sort((a, b) => b[1] - a[1])
      .slice(0, limit);

    const results = [];
    for (const [name, score] of sorted) {
      try {
        const skill = await this.registry.getSkill(name);
        results.push({ ...skill, recommendationScore: score });
      } catch (err) {
        // Skip
      }
    }

    return results;
  }

  // Get popular skills
  async getPopularSkills(limit = 10) {
    try {
      const all = await this.registry.listSkills({ limit: 100 });
      const sorted = all.skills
        .sort((a, b) => (b.downloads || 0) - (a.downloads || 0))
        .slice(0, limit);
      return sorted;
    } catch (err) {
      return [];
    }
  }

  // Get new skills
  async getNewSkills(limit = 10, days = 30) {
    const cutoff = Date.now() - (days * 24 * 60 * 60 * 1000);
    
    try {
      const all = await this.registry.listSkills({ limit: 100 });
      const sorted = all.skills
        .filter(s => (s.createdAt || 0) > cutoff)
        .sort((a, b) => (b.createdAt || 0) - (a.createdAt || 0))
        .slice(0, limit);
      return sorted;
    } catch (err) {
      return [];
    }
  }

  // Get skills by tag
  async getSkillsByTag(tag, limit = 20) {
    const skillNames = this.index.tags[tag.toLowerCase()] || [];
    const results = [];
    
    for (const name of skillNames.slice(0, limit)) {
      try {
        const skill = await this.registry.getSkill(name);
        results.push(skill);
      } catch (err) {
        // Skip
      }
    }

    return results;
  }

  // Get skills by author
  async getSkillsByAuthor(author, limit = 20) {
    const skillNames = this.index.authors[author] || [];
    const results = [];
    
    for (const name of skillNames.slice(0, limit)) {
      try {
        const skill = await this.registry.getSkill(name);
        results.push(skill);
      } catch (err) {
        // Skip
      }
    }

    return results;
  }

  // Get search suggestions
  getSuggestions(partial, limit = 5) {
    const normalized = partial.toLowerCase();
    const suggestions = [];

    // From keywords
    for (const keyword of Object.keys(this.index.keywords)) {
      if (keyword.startsWith(normalized)) {
        suggestions.push({ type: 'keyword', value: keyword });
      }
    }

    // From tags
    for (const tag of Object.keys(this.index.tags)) {
      if (tag.startsWith(normalized) && !suggestions.find(s => s.value === tag)) {
        suggestions.push({ type: 'tag', value: tag });
      }
    }

    return suggestions.slice(0, limit);
  }
}

module.exports = { SearchEngine };