#!/usr/bin/env node

import fs from 'fs';
import path from 'path';
import crypto from 'crypto';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Configuration
const WORKSPACE_ROOT = path.resolve(__dirname, '../..');
const BACKUP_DIR = path.join(__dirname, '../backups');
const SOUL_FILES = [
  'SOUL.md',
  'USER.md',
  'AGENTS.md',
  'IDENTITY.md',
  'TOOLS.md',
  'HEARTBEAT.md',
  'BOOTSTRAP.md'
];

// Sensitive field patterns to sanitize
const SENSITIVE_PATTERNS = [
  /token/i,
  /key/i,
  /secret/i,
  /password/i,
  /apikey/i,
  /api_key/i,
  /auth/i,
  /credential/i,
  /bearer/i
];

// Parse CLI arguments
const args = process.argv.slice(2);
const options = {
  name: null,
  description: null
};

for (let i = 0; i < args.length; i++) {
  if (args[i] === '--name' && args[i + 1]) {
    options.name = args[i + 1];
    i++;
  } else if (args[i] === '--desc' && args[i + 1]) {
    options.description = args[i + 1];
    i++;
  }
}

// Utility: Calculate SHA-256 hash
function calculateHash(filePath) {
  const content = fs.readFileSync(filePath);
  return crypto.createHash('sha256').update(content).digest('hex');
}

// Utility: Get timestamp string
function getTimestamp() {
  return new Date().toISOString().replace(/:/g, '-').split('.')[0];
}

// Utility: Sanitize openclaw.json
function sanitizeOpenClawConfig(configPath) {
  try {
    const content = fs.readFileSync(configPath, 'utf8');
    const config = JSON.parse(content);
    
    // Recursively sanitize sensitive fields
    function sanitizeObject(obj) {
      if (typeof obj !== 'object' || obj === null) return obj;
      
      const sanitized = Array.isArray(obj) ? [] : {};
      
      for (const [key, value] of Object.entries(obj)) {
        const isSensitive = SENSITIVE_PATTERNS.some(pattern => pattern.test(key));
        
        if (isSensitive && typeof value === 'string' && value.length > 0) {
          // Replace with placeholder
          sanitized[key] = '[REDACTED]';
        } else if (typeof value === 'object' && value !== null) {
          sanitized[key] = sanitizeObject(value);
        } else {
          sanitized[key] = value;
        }
      }
      
      return sanitized;
    }
    
    return JSON.stringify(sanitizeObject(config), null, 2);
  } catch (err) {
    return null;
  }
}

// Main backup function
async function backup() {
  console.log('🔍 Starting SOUL backup...\n');

  // Create backup directory structure
  const timestamp = getTimestamp();
  const backupPath = options.name
    ? path.join(BACKUP_DIR, 'named', options.name)
    : path.join(BACKUP_DIR, timestamp);

  if (fs.existsSync(backupPath)) {
    console.error(`❌ Backup already exists: ${backupPath}`);
    process.exit(1);
  }

  fs.mkdirSync(backupPath, { recursive: true });

  // Collect file metadata
  const manifest = {
    timestamp: new Date().toISOString(),
    name: options.name || null,
    description: options.description || null,
    workspace: WORKSPACE_ROOT,
    files: {},
    created_by: path.basename(WORKSPACE_ROOT),
    openclaw_version: '1.0.0'
  };

  let backedUpCount = 0;
  let skippedCount = 0;

  // Backup each SOUL file
  for (const filename of SOUL_FILES) {
    const sourcePath = path.join(WORKSPACE_ROOT, filename);
    const destPath = path.join(backupPath, filename);

    if (fs.existsSync(sourcePath)) {
      // Copy file
      fs.copyFileSync(sourcePath, destPath);

      // Calculate metadata
      const stats = fs.statSync(sourcePath);
      const hash = calculateHash(sourcePath);

      manifest.files[filename] = {
        size: stats.size,
        hash: `sha256:${hash}`,
        exists: true
      };

      console.log(`✅ Backed up: ${filename} (${stats.size} bytes)`);
      backedUpCount++;
    } else {
      manifest.files[filename] = {
        size: 0,
        hash: null,
        exists: false
      };

      console.log(`⚠️  Skipped: ${filename} (not found)`);
      skippedCount++;
    }
  }

  // Backup openclaw.json (sanitized)
  const openclawJsonPath = path.join(WORKSPACE_ROOT, 'openclaw.json');
  if (fs.existsSync(openclawJsonPath)) {
    const sanitizedContent = sanitizeOpenClawConfig(openclawJsonPath);
    
    if (sanitizedContent) {
      const destPath = path.join(backupPath, 'openclaw.sanitized.json');
      fs.writeFileSync(destPath, sanitizedContent);
      
      const stats = fs.statSync(destPath);
      const hash = crypto.createHash('sha256').update(sanitizedContent).digest('hex');
      
      manifest.files['openclaw.sanitized.json'] = {
        size: stats.size,
        hash: `sha256:${hash}`,
        exists: true,
        sanitized: true,
        original: 'openclaw.json'
      };
      
      console.log(`✅ Backed up: openclaw.json → openclaw.sanitized.json (${stats.size} bytes, sensitive fields redacted)`);
      backedUpCount++;
    } else {
      console.log(`⚠️  Skipped: openclaw.json (parse error or not found)`);
      skippedCount++;
    }
  } else {
    console.log(`⚠️  Skipped: openclaw.json (not found)`);
    skippedCount++;
  }

  // Write manifest
  const manifestPath = path.join(backupPath, 'manifest.json');
  fs.writeFileSync(manifestPath, JSON.stringify(manifest, null, 2));

  console.log(`\n📦 Backup complete!`);
  console.log(`   Location: ${backupPath}`);
  console.log(`   Files backed up: ${backedUpCount}`);
  console.log(`   Files skipped: ${skippedCount}`);
  
  if (options.name) {
    console.log(`   Name: ${options.name}`);
  }
  if (options.description) {
    console.log(`   Description: ${options.description}`);
  }
}

// Run backup
backup().catch(err => {
  console.error('❌ Backup failed:', err.message);
  process.exit(1);
});
