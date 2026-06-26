#!/usr/bin/env node

import fs from 'fs';
import path from 'path';
import crypto from 'crypto';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Configuration
const BACKUP_DIR = path.join(__dirname, '../backups');

// Parse CLI arguments
const args = process.argv.slice(2);
const options = {
  timestamp: null
};

for (let i = 0; i < args.length; i++) {
  if (args[i] === '--timestamp' && args[i + 1]) {
    options.timestamp = args[i + 1];
    i++;
  }
}

// Utility: Calculate SHA-256 hash
function calculateHash(filePath) {
  const content = fs.readFileSync(filePath);
  return crypto.createHash('sha256').update(content).digest('hex');
}

// Validate single backup
function validateBackup(backupPath) {
  const manifestPath = path.join(backupPath, 'manifest.json');
  const dirname = path.basename(backupPath);
  
  console.log(`\n🔍 Validating: ${dirname}`);

  let errors = 0;
  let warnings = 0;

  // Check manifest exists
  if (!fs.existsSync(manifestPath)) {
    console.log(`   ❌ manifest.json not found`);
    return { errors: 1, warnings: 0 };
  }

  // Parse manifest
  let manifest;
  try {
    manifest = JSON.parse(fs.readFileSync(manifestPath, 'utf8'));
  } catch (err) {
    console.log(`   ❌ Invalid JSON in manifest: ${err.message}`);
    return { errors: 1, warnings: 0 };
  }

  // Validate manifest structure
  const requiredFields = ['timestamp', 'workspace', 'files', 'created_by'];
  for (const field of requiredFields) {
    if (!manifest[field]) {
      console.log(`   ❌ Missing required field: ${field}`);
      errors++;
    }
  }

  // Validate timestamp format
  if (manifest.timestamp) {
    const date = new Date(manifest.timestamp);
    if (isNaN(date.getTime())) {
      console.log(`   ❌ Invalid timestamp format: ${manifest.timestamp}`);
      errors++;
    }
  }

  // Validate files
  if (manifest.files && typeof manifest.files === 'object') {
    for (const [filename, info] of Object.entries(manifest.files)) {
      if (!info.exists) {
        console.log(`   ⚠️  ${filename}: marked as not existing (expected)`);
        warnings++;
        continue;
      }

      const filePath = path.join(backupPath, filename);

      // Check file exists
      if (!fs.existsSync(filePath)) {
        console.log(`   ❌ ${filename}: file missing from backup`);
        errors++;
        continue;
      }

      // Verify size
      const stats = fs.statSync(filePath);
      if (stats.size !== info.size) {
        console.log(`   ❌ ${filename}: size mismatch (expected ${info.size}, got ${stats.size})`);
        errors++;
      }

      // Verify hash
      if (info.hash && info.hash.startsWith('sha256:')) {
        const expectedHash = info.hash.replace('sha256:', '');
        const actualHash = calculateHash(filePath);
        if (expectedHash !== actualHash) {
          console.log(`   ❌ ${filename}: hash mismatch (file corrupted)`);
          errors++;
        }
      }
    }
  } else {
    console.log(`   ❌ Invalid files structure in manifest`);
    errors++;
  }

  // Summary
  if (errors === 0 && warnings === 0) {
    console.log(`   ✅ Valid backup (no issues)`);
  } else if (errors === 0) {
    console.log(`   ✅ Valid backup (${warnings} warning(s))`);
  } else {
    console.log(`   ❌ Invalid backup (${errors} error(s), ${warnings} warning(s))`);
  }

  return { errors, warnings };
}

// Main validate function
function validate() {
  if (!fs.existsSync(BACKUP_DIR)) {
    console.log('❌ No backups found (backup directory does not exist)');
    process.exit(1);
  }

  const backupsToValidate = [];

  if (options.timestamp) {
    // Validate specific backup
    const backupPath = path.join(BACKUP_DIR, options.timestamp);
    if (!fs.existsSync(backupPath)) {
      console.error(`❌ Backup not found: ${options.timestamp}`);
      process.exit(1);
    }
    backupsToValidate.push(backupPath);
  } else {
    // Validate all backups
    const entries = fs.readdirSync(BACKUP_DIR);
    for (const entry of entries) {
      if (entry === 'named') {
        // Validate named backups
        const namedDir = path.join(BACKUP_DIR, 'named');
        const namedEntries = fs.readdirSync(namedDir);
        for (const namedEntry of namedEntries) {
          const fullPath = path.join(namedDir, namedEntry);
          if (fs.statSync(fullPath).isDirectory()) {
            backupsToValidate.push(fullPath);
          }
        }
      } else {
        const fullPath = path.join(BACKUP_DIR, entry);
        if (fs.statSync(fullPath).isDirectory()) {
          backupsToValidate.push(fullPath);
        }
      }
    }
  }

  if (backupsToValidate.length === 0) {
    console.log('📦 No backups found to validate');
    return;
  }

  console.log(`📦 Validating ${backupsToValidate.length} backup(s)...`);

  let totalErrors = 0;
  let totalWarnings = 0;

  for (const backupPath of backupsToValidate) {
    const result = validateBackup(backupPath);
    totalErrors += result.errors;
    totalWarnings += result.warnings;
  }

  console.log(`\n📊 Validation Summary`);
  console.log(`   Total backups: ${backupsToValidate.length}`);
  console.log(`   Total errors: ${totalErrors}`);
  console.log(`   Total warnings: ${totalWarnings}`);

  if (totalErrors > 0) {
    console.log(`\n❌ Validation failed with ${totalErrors} error(s)`);
    process.exit(1);
  } else {
    console.log(`\n✅ All backups valid`);
  }
}

// Run validate
validate();
