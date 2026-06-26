#!/usr/bin/env node

/**
 * Sync Project Skills
 * 
 * Detects .openclaw-skills.json in current project,
 * checks installed skills, and installs missing ones.
 * 
 * Usage:
 *   node sync-project-skills.js [--force] [--verbose]
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const CONFIG_FILE = '.openclaw-skills.json';
const CACHE_DIR = path.join(process.env.APPDATA || process.env.HOME, '.openclaw', 'cache');
const POSSIBLE_SKILLS_DIRS = [
  path.join(process.env.APPDATA || process.env.HOME, '.openclaw', 'skills'),
  path.join(process.env.USERPROFILE, '.openclaw', 'skills'),
  path.join(process.env.USERPROFILE, '.openclaw', 'workspace', 'skills')
];
const CACHE_FILE = path.join(CACHE_DIR, 'skills.json');
const LOG_FILE = path.join(path.dirname(CACHE_DIR), 'logs', 'skills.log');

// Ensure directories exist
function ensureDir(dir) {
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }
}

// Log message
function log(message, level = 'info') {
  const timestamp = new Date().toISOString();
  const logLine = `[${timestamp}] [${level.toUpperCase()}] ${message}\n`;
  
  // Console output
  if (level === 'error') {
    console.error(message);
  } else {
    console.log(message);
  }
  
  // File log
  try {
    ensureDir(path.dirname(LOG_FILE));
    fs.appendFileSync(LOG_FILE, logLine);
  } catch (err) {
    // Ignore log write errors
  }
}

// Find config file by walking up directories
function findConfigFile(startDir) {
  let current = startDir;
  const maxDepth = 10;
  let depth = 0;
  
  while (current !== path.dirname(current) && depth < maxDepth) {
    const configPath = path.join(current, CONFIG_FILE);
    if (fs.existsSync(configPath)) {
      return { path: configPath, projectRoot: current };
    }
    current = path.dirname(current);
    depth++;
  }
  return null;
}

// Load and validate config
function loadConfig(configPath) {
  try {
    const content = fs.readFileSync(configPath, 'utf8');
    const config = JSON.parse(content);
    
    if (!config.skills || !Array.isArray(config.skills)) {
      throw new Error('Missing or invalid "skills" array');
    }
    
    return config;
  } catch (err) {
    log(`Config error: ${err.message}`, 'error');
    log('   Please check the config file format.', 'error');
    return null;
  }
}

// Load cache
function loadCache() {
  try {
    if (fs.existsSync(CACHE_FILE)) {
      return JSON.parse(fs.readFileSync(CACHE_FILE, 'utf8'));
    }
  } catch (err) {
    // Cache corrupted, ignore
  }
  return { skills: {}, sources: {}, lastSync: 0 };
}

// Save cache
function saveCache(cache) {
  try {
    ensureDir(CACHE_DIR);
    fs.writeFileSync(CACHE_FILE, JSON.stringify(cache, null, 2));
  } catch (err) {
    log(`Failed to save cache: ${err.message}`, 'warn');
  }
}

// Check if skill is installed
function isSkillInstalled(skillName, expectedVersion) {
  for (const skillsDir of POSSIBLE_SKILLS_DIRS) {
    const skillPath = path.join(skillsDir, skillName);
    if (!fs.existsSync(skillPath)) continue;
    
    const skillMdPath = path.join(skillPath, 'SKILL.md');
    if (fs.existsSync(skillMdPath)) {
      return true;
    }
  }
  return false;
}

// Install skill from clawhub
function installFromClawhub(skillName, version, force = false) {
  try {
    log(`📦 Installing ${skillName} from clawhub...`);
    
    const versionSpec = version && version !== 'latest' ? `@${version}` : '';
    const forceFlag = force ? ' --force' : '';
    const cmd = `clawhub install ${skillName}${versionSpec}${forceFlag}`;
    
    execSync(cmd, { 
      stdio: 'inherit', 
      cwd: process.cwd(),
      env: { ...process.env, FORCE_COLOR: '1' }
    });
    
    log(`✅ Installed ${skillName}`);
    return true;
  } catch (err) {
    log(`❌ Failed to install ${skillName}: ${err.message}`, 'error');
    return false;
  }
}

// Check if skill exists in local source
function checkLocalSource(skillName, sourcePaths) {
  for (const sourcePath of sourcePaths) {
    const expandedPath = sourcePath.replace('~', process.env.HOME || process.env.USERPROFILE);
    const skillPath = path.join(expandedPath, skillName);
    
    if (fs.existsSync(skillPath)) {
      const skillMdPath = path.join(skillPath, 'SKILL.md');
      if (fs.existsSync(skillMdPath)) {
        log(`✅ Found ${skillName} in ${sourcePath}`);
        return true;
      }
    }
  }
  return false;
}

// Main sync function
async function sync(force = false, verbose = false) {
  const startDir = process.cwd();
  
  log('🔍 Searching for project configuration...');
  
  // Find config
  const configInfo = findConfigFile(startDir);
  if (!configInfo) {
    log('ℹ️  No .openclaw-skills.json found in project.');
    log('   Using global skills configuration.');
    return true;
  }
  
  log(`📁 Project root: ${configInfo.projectRoot}`);
  log(`📄 Config: ${configInfo.path}`);
  
  // Load config
  const config = loadConfig(configInfo.path);
  if (!config) {
    return false;
  }
  
  const projectName = config.name || path.basename(configInfo.projectRoot);
  log(`\n🔧 Project: ${projectName}`);
  log(`📦 Skills: ${config.skills.length} configured`);
  log(`🌐 Exclude Global: ${config.excludeGlobal ? 'Yes' : 'No'}`);
  
  // Load cache
  const cache = loadCache();
  const now = Date.now();
  const cacheTtl = (config.cache?.ttlHours || 24) * 60 * 60 * 1000;
  const cacheValid = !force && cache.lastSync && (now - cache.lastSync) < cacheTtl && config.cache?.enabled !== false;
  
  if (cacheValid) {
    log('\n✅ Cache valid, skipping sync.');
    log(`   Run with --force to refresh.`);
    return true;
  }
  
  log('\n🔄 Syncing skills...');
  
  // Check and install skills
  const sources = config.sources || [];
  const installed = [];
  const failed = [];
  const skipped = [];
  
  for (const skillSpec of config.skills) {
    const skillName = typeof skillSpec === 'string' ? skillSpec : skillSpec.name;
    const version = typeof skillSpec === 'object' ? skillSpec.version : 'latest';
    
    if (verbose) {
      log(`   Checking ${skillName}...`);
    }
    
    // Check if already installed
    if (isSkillInstalled(skillName, version)) {
      log(`✅ ${skillName} (already installed)`);
      installed.push(skillName);
      continue;
    }
    
    // Try to install from sources
    let success = false;
    
    for (const source of sources) {
      if (!source.enabled && source.enabled !== undefined) {
        if (verbose) {
          log(`   ⏭️  Skipping disabled source: ${source.name}`);
        }
        continue;
      }
      
      if (verbose) {
        log(`   Trying source: ${source.name} (${source.type})`);
      }
      
      switch (source.type) {
        case 'registry':
          if (source.name === 'clawhub') {
            success = installFromClawhub(skillName, version, force);
          } else {
            log(`⚠️  Unknown registry: ${source.name}`, 'warn');
          }
          break;
        case 'filesystem':
          success = checkLocalSource(skillName, source.paths || []);
          break;
        case 'git':
          log(`⚠️  Git source not yet implemented: ${source.name}`, 'warn');
          break;
        case 'url':
          log(`⚠️  URL source not yet implemented: ${source.name}`, 'warn');
          break;
        default:
          log(`⚠️  Unknown source type: ${source.type}`, 'warn');
      }
      
      if (success) break;
    }
    
    if (success) {
      installed.push(skillName);
    } else {
      failed.push(skillName);
      log(`❌ Failed to install ${skillName}`, 'error');
    }
  }
  
  // Update cache
  cache.lastSync = now;
  cache.skills = {};
  for (const name of installed) {
    cache.skills[name] = { installed: true, timestamp: now };
  }
  for (const name of failed) {
    cache.skills[name] = { installed: false, timestamp: now, error: true };
  }
  saveCache(cache);
  
  // Summary
  log('\n' + '='.repeat(60));
  log(`✅ Installed: ${installed.length}`);
  
  if (skipped.length > 0) {
    log(`⏭️  Skipped: ${skipped.length}`);
  }
  
  if (failed.length > 0) {
    log(`❌ Failed: ${failed.length} - ${failed.join(', ')}`, 'error');
  }
  
  if (failed.length > 0 && config.autoSync?.onSkillMissing) {
    log('\n💡 Tip: Run with --force to retry failed installations.');
  }
  
  return failed.length === 0;
}

// CLI
const args = process.argv.slice(2);
const force = args.includes('--force') || args.includes('-f');
const verbose = args.includes('--verbose') || args.includes('-v');
const help = args.includes('--help') || args.includes('-h');

if (help) {
  console.log(`
Project Skills Sync

Usage: node sync-project-skills.js [options]

Options:
  --force, -f      Force re-sync, ignore cache
  --verbose, -v    Show detailed output
  --help, -h       Show this help message

Examples:
  node sync-project-skills.js              # Normal sync
  node sync-project-skills.js --force      # Force refresh
  node sync-project-skills.js -f -v        # Force with verbose output
`);
  process.exit(0);
}

sync(force, verbose)
  .then(success => {
    process.exit(success ? 0 : 1);
  })
  .catch(err => {
    log(`❌ Sync failed: ${err.message}`, 'error');
    process.exit(1);
  });
