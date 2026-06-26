#!/usr/bin/env node

const fs = require('fs');
const MemoryCore = require('../lib/memory-core');

function parseArgs() {
  const args = process.argv.slice(2);
  const options = { file: null };

  for (let i = 0; i < args.length; i++) {
    const arg = args[i];
    const nextArg = args[i + 1];

    if (arg === '--file' && nextArg) {
      options.file = nextArg;
      i++;
    }
  }

  return options;
}

function main() {
  const options = parseArgs();

  if (!options.file) {
    console.error('Error: --file is required');
    console.log('\nUsage: memory-import --file backup.json');
    process.exit(1);
  }

  try {
    const memory = new MemoryCore();
    const data = fs.readFileSync(options.file, 'utf8');
    const imported = memory.importMemories(data);

    console.log(`✓ Imported ${imported} memories from ${options.file}`);
  } catch (error) {
    console.error('Error importing memories:', error.message);
    process.exit(1);
  }
}

main();
