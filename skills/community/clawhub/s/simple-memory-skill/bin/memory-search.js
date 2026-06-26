#!/usr/bin/env node

const MemoryCore = require('../lib/memory-core');

function parseArgs() {
  const args = process.argv.slice(2);
  const options = { query: '' };

  for (let i = 0; i < args.length; i++) {
    const arg = args[i];
    const nextArg = args[i + 1];

    if (arg === '--limit' && nextArg) {
      options.limit = parseInt(nextArg);
      i++;
    } else if (arg === '--type' && nextArg) {
      options.type = nextArg;
      i++;
    } else if (arg === '--days' && nextArg) {
      options.days = parseInt(nextArg);
      i++;
    } else if (!arg.startsWith('--')) {
      options.query = arg;
    }
  }

  return options;
}

function main() {
  const options = parseArgs();

  if (!options.query) {
    console.error('Error: search query is required');
    console.log('\nUsage: memory-search "your query" [--limit 10] [--type preference] [--days 30]');
    console.log('\nExamples:');
    console.log('  memory-search "CSS preferences"');
    console.log('  memory-search "frontend" --type decision --limit 5');
    console.log('  memory-search "API" --days 7');
    process.exit(1);
  }

  try {
    const memory = new MemoryCore();
    const results = memory.searchMemories(options.query, options);

    if (results.length === 0) {
      console.log('No memories found matching your query.');
    } else {
      console.log(`\nFound ${results.length} memories:\n`);

      results.forEach((mem, index) => {
        console.log(`${index + 1}. [${mem.type}] ${mem.content}`);
        console.log(`   Score: ${mem.score.toFixed(2)} | Importance: ${mem.importance} | ${new Date(mem.timestamp).toLocaleString()}`);

        if (mem.tags && mem.tags.length > 0) {
          console.log(`   Tags: ${mem.tags.join(', ')}`);
        }

        if (mem.context) {
          console.log(`   Context: ${mem.context}`);
        }

        console.log(`   ID: ${mem.id}\n`);
      });
    }
  } catch (error) {
    console.error('Error searching memories:', error.message);
    process.exit(1);
  }
}

main();
