#!/usr/bin/env node
/**
 * Optimization Applier - Automatically apply optimizations
 */

const fs = require('fs');
const path = require('path');

class OptimizationApplier {
  constructor(options = {}) {
    this.backupDir = options.backupDir || path.join(process.env.HOME || process.env.USERPROFILE, '.openclaw', 'backups');
    this.ensureDirectory();
  }

  ensureDirectory() {
    if (!fs.existsSync(this.backupDir)) {
      fs.mkdirSync(this.backupDir, { recursive: true });
    }
  }

  /**
   * Apply optimization to a skill
   */
  apply(skillPath, recommendation) {
    if (!recommendation.autoApplicable) {
      return {
        success: false,
        error: 'Recommendation requires manual application',
      };
    }

    try {
      // Create backup
      this.createBackup(skillPath);

      // Apply based on type
      switch (recommendation.type) {
        case 'performance':
          return this.applyPerformanceOptimization(skillPath, recommendation);
        case 'reliability':
          return this.applyReliabilityOptimization(skillPath, recommendation);
        case 'resource':
          return this.applyResourceOptimization(skillPath, recommendation);
        default:
          return {
            success: false,
            error: `Unknown optimization type: ${recommendation.type}`,
          };
      }
    } catch (error) {
      return {
        success: false,
        error: error.message,
      };
    }
  }

  /**
   * Create backup of skill
   */
  createBackup(skillPath) {
    const skillName = path.basename(skillPath);
    const backupPath = path.join(this.backupDir, `${skillName}-${Date.now()}.zip`);
    
    // Simple backup: copy directory
    const backupDir = path.join(this.backupDir, `${skillName}-${Date.now()}`);
    this.copyDirectory(skillPath, backupDir);

    return backupPath;
  }

  /**
   * Copy directory recursively
   */
  copyDirectory(src, dest) {
    if (!fs.existsSync(dest)) {
      fs.mkdirSync(dest, { recursive: true });
    }

    const entries = fs.readdirSync(src, { withFileTypes: true });

    for (const entry of entries) {
      const srcPath = path.join(src, entry.name);
      const destPath = path.join(dest, entry.name);

      if (entry.isDirectory()) {
        this.copyDirectory(srcPath, destPath);
      } else {
        fs.copyFileSync(srcPath, destPath);
      }
    }
  }

  /**
   * Apply performance optimization
   */
  applyPerformanceOptimization(skillPath, recommendation) {
    // Add caching wrapper
    const indexPath = path.join(skillPath, 'src', 'index.js');
    if (fs.existsSync(indexPath)) {
      let content = fs.readFileSync(indexPath, 'utf-8');
      
      // Add cache if not present
      if (!content.includes('cache')) {
        const cacheCode = `
// Auto-added cache
const cache = new Map();
const CACHE_TTL = 5 * 60 * 1000; // 5 minutes

function getCached(key) {
  const entry = cache.get(key);
  if (entry && Date.now() - entry.time < CACHE_TTL) {
    return entry.value;
  }
  cache.delete(key);
  return null;
}

function setCached(key, value) {
  cache.set(key, { value, time: Date.now() });
}
`;
        content = cacheCode + '\n' + content;
        fs.writeFileSync(indexPath, content);
      }
    }

    return {
      success: true,
      message: 'Performance optimization applied: Added caching',
      filesModified: [