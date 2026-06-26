#!/usr/bin/env node

const MemoryCore = require('../lib/memory-core');

function parseArgs() {
  const args = process.argv.slice(2);
  const options = {};

  for (let i = 0; i < args.length; i++) {
    const arg = args[i];
    const nextArg = args[i + 1];

    if (arg === '--limit' && nextArg) {
      options.limit = parseInt(nextArg);
      i++;
    } else if (arg === '--type' && nextArg) {
      options.type = nextArg;
      i++;
    } else if (arg === '--date' && nextArg) {
      options.date = nextArg;
      i++;
    }
  }

  return options;
}

function main() {
  const options = parseArgs();

  try {
    const memory = new MemoryCore();
    const memories = memory.listMemories(options);

    if (memories.length === 0) {
      console.log('No memories found.');
    } else {
      console.log(`\nShowing ${memories.length} memories:\n`);

      memories.forEach((mem, index) => {
        console.log(`${index + 1}. [${mem.type}] ${mem.content}`);
        console.log(`   Importance: ${mem.importance} | ${new Date(mem.timestamp).toLocaleString()}`);

        if (mem.tags && mem.tags.length > 0) {
          console.log(`   Tags: ${mem.tags.join(', ')}`);
        }

        console.log('');
      });
    }
  } catch (error) {
    console.error('Error listing memories:', error.message);
    process.exit(1);
  }
}

main();
