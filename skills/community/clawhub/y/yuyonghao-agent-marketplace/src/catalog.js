/**
 * Catalog Manager - Skill catalog, categories, and version management
 */

const fs = require('fs');
const path = require('path');

class CatalogManager {
  constructor(options = {}) {
    this.registry = options.registry;
    this.dataDir = options.dataDir || './.marketplace-cache';
    this.catalogPath = path.join(this.dataDir, 'catalog.json');
    
    this._ensureDataDir();
    this._loadCatalog();
  }

  _ensureDataDir() {
    if (!fs.existsSync(this.dataDir)) {
      fs.mkdirSync(this.dataDir, { recursive: true });
    }
  }

  _loadCatalog() {
    if (fs.existsSync(this.catalogPath)) {
      try {
        const data = fs.readFileSync(this.catalogPath, 'utf8');
        this.catalog = JSON.parse(data);
      } catch (err) {
        this._initDefaultCatalog();
      }
    } else {
      this._initDefaultCatalog();
    }
  }

  _initDefaultCatalog() {
    this.catalog = {
      categories: [
        { id: 'data-processing', name: 'Data Processing', description: 'Tools for data transformation and analysis' },
        { id: 'web-scraping', name: 'Web Scraping', description: 'Extract data from websites' },
        { id: 'ai-ml', name: 'AI & ML', description: 'Artificial Intelligence and Machine Learning tools' },
        { id: 'automation', name: 'Automation', description: 'Workflow and task automation' },
        { id: 'communication', name: 'Communication', description: 'Messaging and communication tools' },
        { id: 'storage', name: 'Storage', description: 'File and data storage solutions' },
        { id: 'security', name: 'Security', description: 'Security and authentication tools' },
        { id: 'integration', name: 'Integration', description: 'Third-party service integrations' },
        { id: 'developer-tools', name: 'Developer Tools', description: 'Tools for developers' },
        { id: 'productivity', name: 'Productivity', description: 'Productivity and utility tools' }
      ],
      tags: [],
      featured: [],
      newArrivals: [],
      lastUpdated: Date.now()
    };
    this._saveCatalog();
  }

  _saveCatalog() {
    this.catalog.lastUpdated = Date.now();
    fs.writeFileSync(this.catalogPath, JSON.stringify(this.catalog, null, 2));
  }

  getCategories() {
    return this.catalog.categories;
  }

  getCategory(id) {
    return this.catalog.categories.find(c => c.id === id);
  }

  addCategory(category) {
    if (!category.id || !category.name) {
      throw new Error('Category ID and name are required');
    }
    
    if (this.catalog.categories.find(c => c.id === category.id)) {
      throw new Error(`Category ${category.id} already exists`);
    }

    this.catalog.categories.push(category);
    this._saveCatalog();
    return category;
  }

  async getSkillsByCategory(categoryId, options = {}) {
    const { limit = 50, offset = 0 } = options;
    
    try {
      const result = await this.registry.listSkills({ 
        category: categoryId, 
        limit, 
        offset 
      });
      return result;
    } catch (err) {
      return { skills: [], total: 0, offset, limit };
    }
  }

  async getFeaturedSkills(limit = 10) {
    const featured = [];
    for (const skillName of this.catalog.featured.slice(0, limit)) {
      try {
        const skill = await this.registry.getSkill(skillName);
        featured.push(skill);
      } catch (err) {
        // Skip unavailable skills
      }
    }
    return featured;
  }

  async getNewArrivals(limit = 10) {
    const arrivals = [];
    for (const skillName of this.catalog.newArrivals.slice(0, limit)) {
      try {
        const skill = await this.registry.getSkill(skillName);
        arrivals.push(skill);
      } catch (err) {
        // Skip unavailable skills
      }
    }
    return arrivals;
  }

  setFeatured(skillNames) {
    this.catalog.featured = skillNames;
    this._saveCatalog();
    return { featured: skillNames };
  }

  addNewArrival(skillName) {
    // Remove if already exists
    this.catalog.newArrivals = this.catalog.newArrivals.filter(s => s !== skillName);
    // Add to front
    this.catalog.newArrivals.unshift(skillName);
    // Keep only last 50
    this.catalog.newArrivals = this.catalog.newArrivals.slice(0, 50);
    this._saveCatalog();
    return { newArrivals: this.catalog.newArrivals };
  }

  // Version management
  parseVersion(version) {
    const match = version.match(/^(\d+)\.(\d+)\.(\d+)(?:-([a-zA-Z0-9.-]+))?(?:\+([a-zA-Z0-9.-]+))?$/);
    if (!match) {
      throw new Error(`Invalid version format: ${version}`);
    }
    
    return {
      major: parseInt(match[1], 10),
      minor: parseInt(match[2], 10),
      patch: parseInt(match[3], 10),
      prerelease: match[4] || null,
      build: match[5] || null,
      raw: version
    };
  }

  compareVersions(v1, v2) {
    const a = typeof v1 === 'string' ? this.parseVersion(v1) : v1;
    const b = typeof v2 === 'string' ? this.parseVersion(v2) : v2;

    if (a.major !== b.major) return a.major - b.major;
    if (a.minor !== b.minor) return a.minor - b.minor;
    if (a.patch !== b.patch) return a.patch - b.patch;

    // Prerelease comparison (no prerelease > has prerelease)
    if (!a.prerelease && b.prerelease) return 1;
    if (a.prerelease && !b.prerelease) return -1;
    if (a.prerelease && b.prerelease) {
      return a.prerelease.localeCompare(b.prerelease);
    }

    return 0;
  }

  satisfiesVersion(version, range) {
    // Simple semver range parsing
    // Supports: ^1.0.0, ~1.0.0, >=1.0.0, 1.0.0, 1.x, etc.
    
    const v = this.parseVersion(version);
    
    // Exact version
    if (!range.match(/^[\^~>=<]/)) {
      return this.compareVersions(v, range) === 0;
    }

    // Caret (^) - compatible with version
    if (range.startsWith('^')) {
      const min = this.parseVersion(range.slice(1));
      if (this.compareVersions(v, min) < 0) return false;
      if (v.major !== min.major) return false;
      return true;
    }

    // Tilde (~) - approximately equivalent
    if (range.startsWith('~')) {
      const min = this.parseVersion(range.slice(1));
      if (this.compareVersions(v, min) < 0) return false;
      if (v.major !== min.major || v.minor !== min.minor) return false;
      return true;
    }

    // Comparison operators
    if (range.startsWith('>=')) {
      return this.compareVersions(v, range.slice(2)) >= 0;
    }
    if (range.startsWith('>')) {
      return this.compareVersions(v, range.slice(1)) > 0;
    }
    if (range.startsWith('<=')) {
      return this.compareVersions(v, range.slice(2)) <= 0;
    }
    if (range.startsWith('<')) {
      return this.compareVersions(v, range.slice(1)) < 0;
    }

    return false;
  }

  getLatestVersion(versions) {
    if (!versions || versions.length === 0) return null;
    
    return versions.reduce((latest, current) => {
      if (!latest) return current;
      return this.compareVersions(current, latest) > 0 ? current : latest;
    }, null);
  }

  resolveVersion(availableVersions, requestedVersion = null) {
    if (!requestedVersion || requestedVersion === 'latest') {
      return this.getLatestVersion(availableVersions);
    }

    // Check for exact match first
    if (availableVersions.includes(requestedVersion)) {
      return requestedVersion;
    }

    // Try to satisfy range
    const satisfying = availableVersions.filter(v => 
      this.satisfiesVersion(v, requestedVersion)
    );

    if (satisfying.length === 0) {
      throw new Error(`No version satisfies ${requestedVersion}`);
    }

    return this.getLatestVersion(satisfying);
  }

  async checkCompatibility(skillName, version, installedSkills = {}) {
    try {
      const skill = await this.registry.getSkill(skillName, version);
      const issues = [];

      if (skill.dependencies) {
        for (const [depName, depRange] of Object.entries(skill.dependencies)) {
          const installed = installedSkills[depName];
          if (!installed) {
            issues.push({
              type: 'missing',
              skill: depName,
              required: depRange,
              message: `Missing dependency: ${depName}@${depRange}`
            });
          } else if (!this.satisfiesVersion(installed.version, depRange)) {
            issues.push({
              type: 'version-mismatch',
              skill: depName,
              required: depRange,
              installed: installed.version,
              message: `Version mismatch: ${depName} requires ${depRange}, but ${installed.version} is installed`
            });
          }
        }
      }

      return {
        compatible: issues.length === 0,
        issues
      };
    } catch (err) {
      return {
        compatible: false,
        issues: [{ type: 'error', message: err.message }]
      };
    }
  }
}

module.exports = { CatalogManager };