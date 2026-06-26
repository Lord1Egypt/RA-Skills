#!/usr/bin/env node
/**
 * Batch answer script - read content from files and post
 */
import { readFileSync } from 'fs';

async function main() {
  const args = process.argv.slice(2);
  let questionId = '', contentFile = '';
  
  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--question-id') questionId = args[++i];
    if (args[i] === '--content-file') contentFile = args[++i];
  }

  if (!questionId || !contentFile) {
    console.error('用法: node zhihu-batch-answer.js --question-id ID --content-file FILE');
    process.exit(1);
  }

  const content = readFileSync(contentFile, 'utf-8');
  
  // Import and use the answer function
  const { default: answerModule } = await import('./scripts/zhihu-answer.js');
  // The module exports a main function that parses argv, let's call it directly
  
  // Instead, let's use the internal function
  // Re-import with the right args
  process.argv = [
    process.argv[0],
    process.argv[1],
    '--question-id', questionId,
    '--content', content,
  ];
  
  await import('./scripts/zhihu-answer.js');
}

main();
