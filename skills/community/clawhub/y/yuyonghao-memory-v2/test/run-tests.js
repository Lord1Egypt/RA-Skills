#!/usr/bin/env node

/**
 * Memory V2 测试运行器
 */

import { run } from 'node:test';
import { spec } from 'node:test/reporters';
import path from 'path';
import { fileURLToPath } from 'url';
import fs from 'fs/promises';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

async function runTests() {
  console.log('🧪 Running Memory V2 tests...\n');

  const testFiles = [
    'vector-store.test.js',
    'graph-store.test.js',
    'ner-extractor.test.js',
    'memory-manager.test.js'
  ];

  let passed = 0;
  let failed = 0;

  for (const testFile of testFiles) {
    const testPath = path.join(__dirname, testFile);
    
    try {
      await fs.access(testPath);
    } catch (e) {
      console.log(`⊘ Skipping ${testFile} (not found)`);
      continue;
    }

    console.log(`📄 Testing ${testFile}...`);
    
    try {
      const test = await import(testPath);
      passed++;
      console.log(`✅ ${testFile} passed\n`);
    } catch (e) {
      failed++;
      console.error(`❌ ${testFile} failed:`, e.message);
      console.error(e.stack);
      console.log();
    }
  }

  console.log('='.repeat(50));
  console.log(`Tests: ${passed + failed} total, ${passed} passed, ${failed} failed`);
  
  if (failed > 0) {
    process.exit(1);
  }
}

runTests().catch(e => {
  console.error('Test runner failed:', e);
  process.exit(1);
});
