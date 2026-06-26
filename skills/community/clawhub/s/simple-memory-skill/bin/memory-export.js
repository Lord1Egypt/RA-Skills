#!/usr/bin/env node

const fs = require('fs');
const MemoryCore = require('../lib/memory-core');

function parseArgs() {
  const args = process.argv.slice(2);
  const options = { format: 'json', output: null };

  for (let i = 0; i < args.length; i++) {
    const arg = args[i];
    const nextArg = args[i + 1];

    if (arg === '--format' && nextArg) {
      options.format = nextArg.toLowerCase();
      i++;
    } else if (arg === '--output' && nextArg) {
      options.output = nextArg;
      i++;
    }
  }

  return options;
}

function main() {
  const options = parseArgs();

  try {
    const memory = new MemoryCore();
    const exported = memory.exportMemories(options.format);

    if (options.output) {
      fs.writeFileSync(options.output, exported);
      console.log(`✓ Memories exported to ${options.output}`);
    } else {
      console.log(exported);
    }
  } catch (error) {
    console.error('Error exporting memories:', error.message);
    process.exit(1);
  }
}

main();
