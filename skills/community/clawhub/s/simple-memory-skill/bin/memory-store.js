#!/usr/bin/env node

const MemoryCore = require('../lib/memory-core');

function parseArgs() {
  const args = process.argv.slice(2);
  const options = {};

  for (let i = 0; i < args.length; i++) {
    const arg = args[i];
    const nextArg = args[i + 1];

    if (arg === '--type' && nextArg) {
      options.type = nextArg;
      i++;
    } else if (arg === '--content' && nextArg) {
      options.content = nextArg;
      i++;
    } else if (arg === '--importance' && nextArg) {
      options.importance = parseFloat(nextArg);
      i++;
    } else if (arg === '--tags' && nextArg) {
      options.tags = nextArg.split(',').map(t => t.trim());
      i++;
    } else if (arg === '--context' && nextArg) {
      options.context = nextArg;
      i++;
    } else if (!options.content && !arg.startsWith('--')) {
      options.content = arg;
    }
  }

  return options;
}

function main() {
  const options = parseArgs();

  if (!options.content) {
    console.error('Error: --content is required');
    console.log('\nUsage: memory-store --content "your content" [--type fact] [--importance 0.5] [--tags tag1,tag2]');
    console.log('\nExamples:');
    console.log('  memory-store --content "User prefers dark mode" --type preference --importance 0.9');
    console.log('  memory-store "Use React for frontend" --type decision --tags frontend,framework');
    console.log('  memory-store "API endpoint: /api/users" --type fact');
    process.exit(1);
  }

  try {
    const memory = new MemoryCore();
    const stored = memory.storeMemory(options.content, options);

    console.log('✓ Memory stored successfully!');
    console.log(`  ID: ${stored.id}`);
    console.log(`  Type: ${stored.type}`);
    console.log(`  Importance: ${stored.importance}`);
    if (stored.tags && stored.tags.length > 0) {
      console.log(`  Tags: ${stored.tags.join(', ')}`);
    }
    console.log(`  Timestamp: ${stored.timestamp}`);
  } catch (error) {
    console.error('Error storing memory:', error.message);
    process.exit(1);
  }
}

main();
