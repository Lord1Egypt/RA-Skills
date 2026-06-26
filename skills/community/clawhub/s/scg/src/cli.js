#!/usr/bin/env node

import { Command } from 'commander';
import { parseGoal } from './sources/goalParser.js';
import { searchLocal, indexProject } from './sources/localSearch.js';
import { searchKnowledgeBase } from './sources/knowledgeBase.js';
import { searchWeb } from './sources/webSearch.js';
import { composeContext } from './sources/contextComposer.js';
import { tokenCount } from './utils/tokenCounter.js';

const program = new Command();

program
  .name('scg')
  .description('The Synthetic Context Generator - Feed it a goal, get the perfect context')
  .version('1.0.0');

program
  .argument('[goal]', 'The goal or task you want context for')
  .option('-c, --context <path>', 'Path to project/context files')
  .option('-m, --max-tokens <number>', 'Max tokens in output', '4000')
  .option('--no-web', 'Skip web searches')
  .option('--verbose', 'Show verbose output')
  .action(async (goal, options) => {
    if (!goal) {
      console.log('Usage: scg "write secure SQL query"');
      console.log('       scg --goal "fix auth bug" --context ./myproject');
      process.exit(0);
    }

    console.log(`🎯 Goal: ${goal}\n`);
    
    // Parse goal
    const parsed = parseGoal(goal);
    if (options.verbose) console.log('📊 Parsed:', parsed);

    // Search local files if context path provided
    let localResults = [];
    if (options.context) {
      localResults = await searchLocal(parsed, options.context);
    }

    // Search knowledge base
    const kbResults = await searchKnowledgeBase(parsed);

    // Search web if enabled
    let webResults = [];
    if (options.web && options.web !== false) {
      webResults = await searchWeb(parsed);
    }

    // Compose final context
    const maxTokens = parseInt(options.maxTokens || '4000');
    const context = composeContext({
      goal,
      parsed,
      local: localResults,
      kb: kbResults,
      web: webResults,
      maxTokens
    });

    console.log(context);
    
    const tokens = await tokenCount(context);
    console.log(`\n📏 Context size: ${tokens} tokens`);
  });

// Index command
program
  .command('index <path>')
  .description('Index a project for local search')
  .action(async (path) => {
    console.log(`📂 Indexing ${path}...`);
    await indexProject(path);
    console.log('✅ Indexed successfully!');
  });

// Learn command
program
  .command('learn <path>')
  .description('Add files to knowledge base')
  .action(async (path) => {
    console.log(`📚 Learning from ${path}...`);
    // TODO: Implement learning
    console.log('✅ Learned!');
  });

program.parse();