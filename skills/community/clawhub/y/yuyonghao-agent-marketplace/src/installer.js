/**
 * Installer - Skill installation, dependency resolution, and rollback
 */

const fs = require('fs');
const path = require('path');
const https = require('https');
const http = require('http');

class Installer {
  constructor(options = {}) {
    this.registry = options.registry;
    this.catalog = options.catalog;
    this.installDir = options.installDir || './skills';
    this.backupDir = options.backupDir || './.marketplace-cache/backups';
    this.dataDir = options.dataDir || './.marketplace-cache';
    this.installedPath = path.join(this.dataDir, 'installed.json');
    this.historyPath = path.join(this.dataDir, 'install-history.json');
    
    this._ensureDirs();
    this._loadInstalled();
    this._loadHistory();
  }

  _ensureDirs() {
    [this.installDir, this.backupDir, this.dataDir].forEach(dir => {
      if (!fs.existsSync(dir)) {
        fs.mkdirSync(dir, { recursive: true });
      }
    });
  }

  _loadInstalled() {
    if (fs.existsSync(this.installedPath)) {
      try {
        const data = fs.readFileSync(this.installedPath, 'utf8');
        this.installed = JSON.parse(data);
      } catch (err) {
        this.installed = {};
      }
    } else {
      this.installed = {};
    }
  }

  _saveInstalled() {
    fs.writeFileSync(this.installedPath, JSON.stringify(this.installed, null, 2));
  }

  _loadHistory() {
    if (fs.existsSync(this.historyPath)) {
      try {
        const data = fs.readFileSync(this.historyPath, 'utf8');
        this.history = JSON.parse(data);
      } catch (err) {
        this.history = [];
      }
    } else {
      this.history = [];
    }
  }

  _saveHistory() {
    fs.writeFileSync(this.historyPath, JSON.stringify(this.history, null, 2));
  }

  _addToHistory(action, skillName, version, details = {}) {
    this.history.push({
      action,
      skillName,
      version,
      timestamp: Date.now(),
      ...details
    });
    // Keep last 1000 entries
    this.history = this.history.slice(-1000);
    this._saveHistory();
  }

  // Resolve dependencies
  async resolveDependencies(skillName, version, resolved = new Map(), installing = new Set()) {
    const key = `${skillName}@${version}`;
    
    if (resolved.has(key)) {
      return resolved;
    }

    if (installing.has(key)) {
      throw new Error(`Circular dependency detected: ${key}`);
    }

    installing.add(key);

    try {
      const skill = await this.registry.getSkill(skillName, version);
      
      if (skill.dependencies) {
        for (const [depName, depRange] of Object.entries(skill.dependencies)) {
          // Check if already installed
          const installed = this.installed[depName];
          if (installed) {
            if (this.catalog.satisfiesVersion(installed.version, depRange)) {
              continue; // Already satisfied
            }
          }

          // Find matching version
          const depSkill = await this.registry.getSkill(depName);
          const matchingVersion = this.catalog.resolveVersion(
            depSkill.versions,
            depRange
          );

          await this.resolveDependencies(depName, matchingVersion, resolved, installing);
        }
      }

      resolved.set(key, { name: skillName, version, skill });
      installing.delete(key);
      
      return resolved;
    } catch (err) {
      installing.delete(key);
      throw err;
    }
  }

  // Check for conflicts
  async checkConflicts(skillName, version) {
    const conflicts = [];

    try {
      const skill = await this.registry.getSkill(skillName, version);

      // Check for version conflicts with installed skills
      if (this.installed[skillName]) {
        const installed = this.installed[skillName];
        if (installed.version !== version) {
          conflicts.push({
            type: 'version-conflict',
            skill: skillName,
            installed: installed.version,
            requested: version,
            message: `${skillName}@${installed.version} is already installed, but ${version} was requested`
          });
        }
      }

      // Check dependency conflicts
      if (skill.dependencies) {
        for (const [depName, depRange] of Object.entries(skill.dependencies)) {
          const installed = this.installed[depName];
          if (installed && !this.catalog.satisfiesVersion(installed.version, depRange)) {
            conflicts.push({
              type: 'dependency-conflict',
              skill: depName,
              installed: installed.version,
              required: depRange,
              message: `${skillName}@${version} requires ${depName}@${depRange}, but ${depName}@${installed.version} is installed`
            });
          }
        }
      }

      return { hasConflicts: conflicts.length > 0, conflicts };
    } catch (err) {
      return { hasConflicts: true, conflicts: [{ type: 'error', message: err.message }] };
    }
  }

  // Download skill package
  async _downloadPackage(skill, targetDir) {
    // If skill has a download URL
    if (skill.downloadUrl) {
      return new Promise((resolve, reject) => {
        const url = skill.downloadUrl;
        const client = url.startsWith('https:') ? https : http;
        
        const req = client.get(url, { timeout: 60000 }, (res) => {
          if (res.statusCode !== 200) {
            reject(new Error(`Download failed with status ${res.statusCode}`));
            return;
          }

          const chunks = [];
          res.on('data', chunk => chunks.push(chunk));
          res.on('end', () => {
            const data = Buffer.concat(chunks);
            fs.writeFileSync(targetDir, data);
            resolve(targetDir);
          });
        });

        req.on('error', reject);
        req.on('timeout', () => {
          req.destroy();
          reject(new Error('Download timeout'));
        });
      });
    }

    // Otherwise, create a minimal package from registry data
    const packageData = {
      name: skill.name,
      version: skill.version,
      description: skill.description,
      dependencies: skill.dependencies || {},
      installDate: new Date().toISOString()
    };

    fs.writeFileSync(
      path.join(targetDir, 'package.json'),
      JSON.stringify(packageData, null, 2)
    );

    if (skill.code) {
      fs.writeFileSync(
        path.join(targetDir, 'index.js'),
        skill.code
      );
    }

    return targetDir;
  }

  // Install a skill
  async install(skillName, options = {}) {
    const { 
      version = 'latest',
      force = false,
      dryRun = false 
    } = options;

    // Get skill info
    const skill = await this.registry.getSkill(skillName);
    const targetVersion = version === 'latest' 
      ? skill.latestVersion 
      : this.catalog.resolveVersion(skill.versions, version);

    // Check if already installed
    if (this.installed[skillName] && !force) {
      const installed = this.installed[skillName];
      if (installed.version === targetVersion) {
        return { 
          success: true, 
          alreadyInstalled: true,
          skill: skillName,
          version: targetVersion
        };
      }
    }

    // Check conflicts
    const conflictCheck = await this.checkConflicts(skillName, targetVersion);
    if (conflictCheck.hasConflicts && !force) {
      throw new Error(
        `Installation conflicts detected: ${conflictCheck.conflicts.map(c => c.message).join(', ')}`
      );
    }

    // Resolve dependencies
    const dependencies = await this.resolveDependencies(skillName, targetVersion);
    
    // Remove the main skill from dependencies (we'll install it separately)
    const depList = Array.from(dependencies.entries())
      .filter(([key]) => !key.startsWith(`${skillName}@`))
      .map(([, value]) => value);

    if (dryRun) {
