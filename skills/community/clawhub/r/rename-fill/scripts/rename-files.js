#!/usr/bin/env node

/**
 * File rename script for rename-file skill
 * Usage: node rename-files.js <prefix> <directory>
 */

const fs = require('fs');
const path = require('path');

function main() {
  // Parse command line arguments
  const args = process.argv.slice(2);
  if (args.length < 2) {
    console.error('Usage: node rename-files.js <prefix> <directory>');
    process.exit(1);
  }

  const prefix = args[0];
  const dirPath = args[1];

  // Validate directory
  if (!fs.existsSync(dirPath)) {
    console.error(`Error: Directory "${dirPath}" does not exist`);
    process.exit(1);
  }

  const stats = fs.statSync(dirPath);
  if (!stats.isDirectory()) {
    console.error(`Error: "${dirPath}" is not a directory`);
    process.exit(1);
  }

  // Read directory contents
  let entries;
  try {
    entries = fs.readdirSync(dirPath, { withFileTypes: true });
  } catch (err) {
    console.error(`Error reading directory "${dirPath}": ${err.message}`);
    process.exit(1);
  }

  // Filter for files only (skip directories)
  const files = entries.filter(entry => entry.isFile());

  if (files.length === 0) {
    console.log(`No files found in directory "${dirPath}"`);
    process.exit(0);
  }

  console.log(`Found ${files.length} file(s) in "${dirPath}"`);
  console.log(`Adding prefix: "${prefix}"`);

  // Prepare rename operations
  const operations = [];
  for (const file of files) {
    const oldName = file.name;
    const extension = path.extname(oldName);
    const baseName = path.basename(oldName, extension);
    const newName = prefix + baseName + extension;

    // Skip if new name would be same as old name (prefix might be empty)
    if (oldName === newName) {
      console.log(`Skipping "${oldName}" -> name unchanged`);
      continue;
    }

    const oldPath = path.join(dirPath, oldName);
    const newPath = path.join(dirPath, newName);

    // Check if target already exists
    if (fs.existsSync(newPath)) {
      console.error(`Error: Cannot rename "${oldName}" -> "${newName}" (file already exists)`);
      continue;
    }

    operations.push({ oldPath, newPath, oldName, newName });
  }

  if (operations.length === 0) {
    console.log('No files to rename (all skipped)');
    process.exit(0);
  }

  console.log(`\nWill rename ${operations.length} file(s):`);
  operations.forEach(op => {
    console.log(`  ${op.oldName} -> ${op.newName}`);
  });

  // Perform rename operations
  console.log('\nRenaming files...');
  const results = {
    success: 0,
    failed: 0,
    errors: []
  };

  for (const op of operations) {
    try {
      fs.renameSync(op.oldPath, op.newPath);
      console.log(`✓ ${op.oldName} -> ${op.newName}`);
      results.success++;
    } catch (err) {
      console.error(`✗ ${op.oldName} -> ${op.newName}: ${err.message}`);
      results.failed++;
      results.errors.push({
        file: op.oldName,
        error: err.message
      });
    }
  }

  // Summary
  console.log('\n' + '='.repeat(50));
  console.log('RENAME SUMMARY');
  console.log('='.repeat(50));
  console.log(`Directory: ${dirPath}`);
  console.log(`Prefix: "${prefix}"`);
  console.log(`Total files processed: ${files.length}`);
  console.log(`Successfully renamed: ${results.success}`);
  console.log(`Failed: ${results.failed}`);

  if (results.errors.length > 0) {
    console.log('\nErrors:');
    results.errors.forEach(err => {
      console.log(`  - ${err.file}: ${err.error}`);
    });
  }

  if (results.failed > 0) {
    process.exit(1);
  }
}

// Run main function
if (require.main === module) {
  try {
    main();
  } catch (err) {
    console.error('Unexpected error:', err.message);
    process.exit(1);
  }
}

module.exports = { main };