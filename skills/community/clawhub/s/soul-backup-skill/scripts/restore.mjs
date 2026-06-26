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

// Parse CLI arguments
const args = process.argv.slice(2);
const options = {
  timestamp: null,
  name: null,
  dryRun: false,
  file: null
};

for (let i = 0; i < args.length; i++) {
  if (args[i] === '--timestamp' && args[i + 1]) {
    options.timestamp = args[i + 1];
    i++;
  } else if (args[i] === '--name' && args[i + 1]) {
    options.name = args[i + 1];
    i++;
  } else if (args[i] === '--dry-run') {
    options.dryRun = true;
  } else if (args[i] === '--file' && args[i + 1]) {
    options.file = args[i + 1];
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

// Find backup directory
function findBackupDir() {
  if (options.name) {
    const namedPath = path.join(BACKUP_DIR, 'named', options.name);
    if (!fs.existsSync(namedPath)) {
      console.error(`❌ Named backup not found: ${options.name}`);
      process.exit(1);
    }
    return namedPath;
  }

  if (options.timestamp) {
    const timestampPath = path.join(BACKUP_DIR, options.timestamp);
    if (!fs.existsSync(timestampPath)) {
      console.error(`❌ Backup not found: ${options.timestamp}`);
      process.exit(1);
    }
    return timestampPath;
  }

  // Find latest backup
  const backups = [];
  
  if (fs.existsSync(BACKUP_DIR)) {
    const entries = fs.readdirSync(BACKUP_DIR);
    for (const entry of entries) {
      if (entry === 'named') continue;
      const fullPath = path.join(BACKUP_DIR, entry);
      if (fs.statSync(fullPath).isDirectory()) {
        const manifestPath = path.join(fullPath, 'manifest.json');
        if (fs.existsSync(manifestPath)) {
          const manifest = JSON.parse(fs.readFileSync(manifestPath, 'utf8'));
          backups.push({ path: fullPath, timestamp: manifest.timestamp });
        }
      }
    }
  }

  if (backups.length === 0) {
    console.error('❌ No backups found');
    process.exit(1);
  }

  backups.sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp));
  return backups[0].path;
}

// Create pre-restore backup
async function createPreRestoreBackup() {
  console.log('📦 Creating pre-restore backup...');
  
  const timestamp = getTimestamp();
  const backupPath = path.join(BACKUP_DIR, `pre-restore-${timestamp}`);
  
  fs.mkdirSync(backupPath, { recursive: true });

  const manifest = {
    timestamp: new Date().toISOString(),
    name: `pre-restore-${timestamp}`,
    description: 'Automatic backup before restore operation',
    workspace: WORKSPACE_ROOT,
    files: {},
    created_by: path.basename(WORKSPACE_ROOT),
    openclaw_version: '1.0.0'
  };

  for (const filename of SOUL_FILES) {
    const sourcePath = path.join(WORKSPACE_ROOT, filename);
    const destPath = path.join(backupPath, filename);

    if (fs.existsSync(sourcePath)) {
      fs.copyFileSync(sourcePath, destPath);
      const stats = fs.statSync(sourcePath);
      const hash = calculateHash(sourcePath);
      manifest.files[filename] = {
        size: stats.size,
        hash: `sha256:${hash}`,
        exists: true
      };
    } else {
      manifest.files[filename] = {
        size: 0,
        hash: null,
        exists: false
      };
    }
  }

  const manifestPath = path.join(backupPath, 'manifest.json');
  fs.writeFileSync(manifestPath, JSON.stringify(manifest, null, 2));

  console.log(`✅ Pre-restore backup created: ${backupPath}\n`);
  return backupPath;
}

// Main restore function
async function restore() {
  const backupPath = findBackupDir();
  const manifestPath = path.join(backupPath, 'manifest.json');

  if (!fs.existsSync(manifestPath)) {
    console.error(`❌ Invalid backup: manifest.json not found in ${backupPath}`);
    process.exit(1);
  }

  const manifest = JSON.parse(fs.readFileSync(manifestPath, 'utf8'));

  console.log('🔍 Restore Preview\n');
  console.log(`   Backup: ${path.basename(backupPath)}`);
  console.log(`   Created: ${manifest.timestamp}`);
  if (manifest.name) console.log(`   Name: ${manifest.name}`);
  if (manifest.description) console.log(`   Description: ${manifest.description}`);
  console.log();

  // Filter files if --file specified
  const filesToRestore = options.file
    ? [options.file]
    : SOUL_FILES;

  let restoredCount = 0;
  let skippedCount = 0;
  let sanitizedConfigFound = false;

  console.log('Files to restore:');
  for (const filename of filesToRestore) {
    const sourcePath = path.join(backupPath, filename);
    const destPath = path.join(WORKSPACE_ROOT, filename);
    const fileInfo = manifest.files[filename];

    if (!fileInfo || !fileInfo.exists) {
      console.log(`⚠️  Skip: ${filename} (not in backup)`);
      skippedCount++;
      continue;
    }

    if (!fs.existsSync(sourcePath)) {
      console.log(`❌ Error: ${filename} (missing from backup directory)`);
      skippedCount++;
      continue;
    }

    const currentExists = fs.existsSync(destPath);
    const status = currentExists ? 'overwrite' : 'create';
    console.log(`✅ ${status}: ${filename} (${fileInfo.size} bytes)`);
    restoredCount++;
  }

  // Check for sanitized openclaw.json
  const sanitizedConfigPath = path.join(backupPath, 'openclaw.sanitized.json');
  if (fs.existsSync(sanitizedConfigPath)) {
    sanitizedConfigFound = true;
    console.log(`⚠️  Found: openclaw.sanitized.json (sensitive fields redacted)`);
    console.log(`   → Manual action required: restore openclaw.json and fill in API keys/tokens`);
  }

  console.log();

  if (options.dryRun) {
    console.log('🔍 Dry run complete. No files were modified.');
    console.log(`   Would restore: ${restoredCount} files`);
    console.log(`   Would skip: ${skippedCount} files`);
    if (sanitizedConfigFound) {
      console.log(`   ⚠️  openclaw.json requires manual restoration (see backup for structure)`);
    }
    return;
  }

  // Create pre-restore backup
  await createPreRestoreBackup();

  // Perform restore
  console.log('🔄 Restoring files...\n');

  for (const filename of filesToRestore) {
    const sourcePath = path.join(backupPath, filename);
    const destPath = path.join(WORKSPACE_ROOT, filename);
    const fileInfo = manifest.files[filename];

    if (!fileInfo || !fileInfo.exists || !fs.existsSync(sourcePath)) {
      continue;
    }

    fs.copyFileSync(sourcePath, destPath);
    console.log(`✅ Restored: ${filename}`);
  }

  console.log(`\n✨ Restore complete!`);
  console.log(`   Files restored: ${restoredCount}`);
  console.log(`   Files skipped: ${skippedCount}`);
  
  if (sanitizedConfigFound) {
    console.log(`\n⚠️  IMPORTANT: openclaw.json was not restored automatically.`);
    console.log(`   Sensitive fields (API keys, tokens) were redacted in backup.`);
    console.log(`   To restore openclaw.json:`);
    console.log(`   1. Copy openclaw.sanitized.json from backup to workspace as openclaw.json`);
    console.log(`   2. Manually fill in [REDACTED] fields with your actual API keys/tokens`);
    console.log(`   Backup location: ${sanitizedConfigPath}`);
  }
}

// Run restore
restore().catch(err => {
  console.error('❌ Restore failed:', err.message);
  process.exit(1);
});
