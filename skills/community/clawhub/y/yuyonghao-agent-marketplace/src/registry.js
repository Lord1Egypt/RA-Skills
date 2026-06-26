/**
 * Registry Manager - Handles local and remote registry operations
 */

const fs = require('fs');
const path = require('path');
const https = require('https');
const http = require('http');

class RegistryManager {
  constructor(options = {}) {
    this.registryUrl = options.registry || 'https://clawhub.com/registry';
    this.cacheDir = options.cacheDir || './.marketplace-cache';
    this.cacheTTL = options.cacheTTL || 3600000; // 1 hour default
    this.localRegistryPath = options.localRegistry || path.join(this.cacheDir, 'local-registry.json');
    
    this._ensureCacheDir();
    this._loadLocalRegistry();
  }

  _ensureCacheDir() {
    if (!fs.existsSync(this.cacheDir)) {
      fs.mkdirSync(this.cacheDir, { recursive: true });
    }
  }

  _loadLocalRegistry() {
    if (fs.existsSync(this.localRegistryPath)) {
      try {
        const data = fs.readFileSync(this.localRegistryPath, 'utf8');
        this.localRegistry = JSON.parse(data);
      } catch (err) {
        this.localRegistry = { skills: {}, metadata: { version: '1.0', lastUpdated: Date.now() } };
      }
    } else {
      this.localRegistry = { skills: {}, metadata: { version: '1.0', lastUpdated: Date.now() } };
    }
  }

  _saveLocalRegistry() {
    this.localRegistry.metadata.lastUpdated = Date.now();
    fs.writeFileSync(this.localRegistryPath, JSON.stringify(this.localRegistry, null, 2));
  }

  _getCachePath(key) {
    return path.join(this.cacheDir, `${key.replace(/[^a-zA-Z0-9_-]/g, '_')}.json`);
  }

  _isCacheValid(cachePath) {
    if (!fs.existsSync(cachePath)) return false;
    const stats = fs.statSync(cachePath);
    return (Date.now() - stats.mtime.getTime()) < this.cacheTTL;
  }

  async _fetchFromRemote(endpoint, useCache = true) {
    const cacheKey = endpoint.replace(/\//g, '_');
    const cachePath = this._getCachePath(cacheKey);

    if (useCache && this._isCacheValid(cachePath)) {
      try {
        const data = fs.readFileSync(cachePath, 'utf8');
        return JSON.parse(data);
      } catch (err) {
        // Cache corrupted, fetch from remote
      }
    }

    const url = `${this.registryUrl}${endpoint}`;
    
    return new Promise((resolve, reject) => {
      const client = url.startsWith('https:') ? https : http;
      
      const req = client.get(url, { timeout: 30000 }, (res) => {
        let data = '';
        res.on('data', chunk => data += chunk);
        res.on('end', () => {
          try {
            const parsed = JSON.parse(data);
            // Cache successful responses
            if (useCache) {
              fs.writeFileSync(cachePath, JSON.stringify(parsed, null, 2));
            }
            resolve(parsed);
          } catch (err) {
            reject(new Error(`Failed to parse response: ${err.message}`));
          }
        });
      });

      req.on('error', (err) => {
        reject(new Error(`Network error: ${err.message}`));
      });

      req.on('timeout', () => {
        req.destroy();
        reject(new Error('Request timeout'));
      });
    });
  }

  async getSkill(name, version = null) {
    // Try local first
    if (this.localRegistry.skills[name]) {
      const skill = this.localRegistry.skills[name];
      if (!version || skill.versions.includes(version)) {
        return { ...skill, source: 'local' };
      }
    }

    // Try remote
    try {
      const endpoint = version 
        ? `/skills/${name}/versions/${version}`
        : `/skills/${name}`;
      const skill = await this._fetchFromRemote(endpoint);
      return { ...skill, source: 'remote' };
    } catch (err) {
      throw new Error(`Skill not found: ${name}${version ? `@${version}` : ''}`);
    }
  }

  async listSkills(options = {}) {
    const { category, limit = 100, offset = 0 } = options;
    
    try {
      const query = new URLSearchParams();
      if (category) query.append('category', category);
      if (limit) query.append('limit', limit.toString());
      if (offset) query.append('offset', offset.toString());
      
      const endpoint = `/skills?${query.toString()}`;
      return await this._fetchFromRemote(endpoint);
    } catch (err) {
      // Fallback to local registry
      const skills = Object.values(this.localRegistry.skills);
      let result = skills;
      if (category) {
        result = skills.filter(s => s.categories?.includes(category));
      }
      return {
        skills: result.slice(offset, offset + limit),
        total: result.length,
        offset,
        limit
      };
    }
  }

  async searchSkills(query, options = {}) {
    try {
      const params = new URLSearchParams({ q: query });
      if (options.category) params.append('category', options.category);
      if (options.sort) params.append('sort', options.sort);
      
      const endpoint = `/search?${params.toString()}`;
      return await this._fetchFromRemote(endpoint);
    } catch (err) {
      // Local search fallback
      const skills = Object.values(this.localRegistry.skills);
      const results = skills.filter(skill => {
        const matchName = skill.name?.toLowerCase().includes(query.toLowerCase());
        const matchDesc = skill.description?.toLowerCase().includes(query.toLowerCase());
        const matchTags = skill.tags?.some(tag => tag.toLowerCase().includes(query.toLowerCase()));
        const matchCategory = !options.category || skill.categories?.includes(options.category);
        return (matchName || matchDesc || matchTags) && matchCategory;
      });

      if (options.sort === 'rating') {
        results.sort((a, b) => (b.rating || 0) - (a.rating || 0));
      } else if (options.sort === 'downloads') {
        results.sort((a, b) => (b.downloads || 0) - (a.downloads || 0));
      }

      return { skills: results, total: results.length };
    }
  }

  registerSkill(skillData) {
    if (!skillData.name) {
      throw new Error('Skill name is required');
    }

    const existing = this.localRegistry.skills[skillData.name];
    
    if (existing) {
      // Update existing
      existing.versions = [...new Set([...existing.versions, skillData.version])].sort();
      existing.latestVersion = skillData.version;
      existing.updatedAt = Date.now();
      Object.assign(existing, skillData);
    } else {
      // New skill
      this.localRegistry.skills[skillData.name] = {
        ...skillData,
        versions: [skillData.version],
        latestVersion: skillData.version,
        createdAt: Date.now(),
        updatedAt: Date.now()
      };
    }

    this._saveLocalRegistry();
    return this.localRegistry.skills[skillData.name];
  }

  unregisterSkill(name, version = null) {
    if (!this.localRegistry.skills[name]) {
      throw new Error(`Skill not found: ${name}`);
    }

    if (version) {
      const skill = this.localRegistry.skills[name];
      skill.versions = skill.versions.filter(v => v !== version);
      if (skill.versions.length === 0) {
        delete this.localRegistry.skills[name];
      } else if (skill.latestVersion === version) {
        skill.latestVersion = skill.versions[skill.versions.length - 1];
      }
    } else {
      delete this.localRegistry.skills[name];
    }

    this._saveLocalRegistry();
    return { success: true };
  }

  clearCache() {
    const files = fs.readdirSync(this.cacheDir);
    for (const file of files) {
      if (file.endsWith('.json') && file !== 'local-registry.json') {
        fs.unlinkSync(path.join(this.cacheDir, file));
      }
    }
    return { cleared: true };
  }

  getStats() {
    const localCount = Object.keys(this.localRegistry.skills).length;
    const cacheFiles = fs.readdirSync(this.cacheDir).filter(f => f.endsWith('.json')).length;
    
    return {
      localSkills: localCount,
      cachedFiles: cacheFiles,
      registryUrl: this.registryUrl,
      lastUpdated: this.localRegistry.metadata.lastUpdated
    };
  }
}

module.exports = { RegistryManager };