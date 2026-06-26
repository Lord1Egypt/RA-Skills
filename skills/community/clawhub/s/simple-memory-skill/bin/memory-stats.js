#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const MemoryCore = require('../lib/memory-core');

function formatBytes(bytes) {
  if (bytes === 0) return '0 B';
  const k = 1024;
  const sizes = ['B', 'KB', 'MB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

function main() {
  console.log('🧠 Simple Local Memory Status\n');

  const memory = new MemoryCore();

  // Check SESSION-STATE.json
  if (fs.existsSync('SESSION-STATE.json')) {
    try {
      const state = JSON.parse(fs.readFileSync('SESSION-STATE.json', 'utf8'));
      const size = fs.statSync('SESSION-STATE.json').size;
      console.log(`✓ SESSION-STATE.json (${formatBytes(size)}, updated ${new Date(state.last_updated).toLocaleString()})`);

      if (state.current_task) {
        console.log(`  Current task: ${state.current_task}`);
      }
      if (state.key_context && state.key_context.length > 0) {
        console.log(`  Context items: ${state.key_context.length}`);
      }
      if (state.pending_actions && state.pending_actions.length > 0) {
        console.log(`  Pending actions: ${state.pending_actions.length}`);
      }
    } catch (e) {
      console.log('✗ SESSION-STATE.json exists but is invalid');
    }
  } else {
    console.log('✗ SESSION-STATE.json missing (run memory-init)');
  }

  console.log('');

  // Check MEMORY.md
  if (fs.existsSync('MEMORY.md')) {
    const stat = fs.statSync('MEMORY.md');
    const content = fs.readFileSync('MEMORY.md', 'utf8');
    const lines = content.split('\n').length;
    console.log(`✓ MEMORY.md (${lines} lines, ${formatBytes(stat.size)})`);
  } else {
    console.log('✗ MEMORY.md missing (run memory-init)');
  }

  console.log('');

  // Check memories directory
  if (fs.existsSync('memories')) {
    const files = fs.readdirSync('memories').filter(f => f.endsWith('.json'));
    console.log(`✓ memories/ directory (${files.length} files)`);

    // Show detailed stats
    const stats = memory.getStats();
    console.log(`  Total memories: ${stats.totalMemories}`);
    console.log(`  Storage used: ${formatBytes(stats.storageSize)}`);

    if (Object.keys(stats.byType).length > 0) {
      console.log('  By type:');
      for (const [type, count] of Object.entries(stats.byType)) {
        console.log(`    - ${type}: ${count}`);
      }
    }

    console.log('  By importance:');
    console.log(`    - High (≥0.8): ${stats.byImportance.high}`);
    console.log(`    - Medium (≥0.5): ${stats.byImportance.medium}`);
    console.log(`    - Low (<0.5): ${stats.byImportance.low}`);

    if (stats.oldestMemory) {
      console.log(`  Oldest: ${new Date(stats.oldestMemory).toLocaleString()}`);
    }
    if (stats.newestMemory) {
      console.log(`  Newest: ${new Date(stats.newestMemory).toLocaleString()}`);
    }
  } else {
    console.log('✗ memories/ directory missing (run memory-init)');
  }

  console.log('\n💡 Tips:');
  console.log('  - Run memory-init if any files are missing');
  console.log('  - Use memory-store to save new memories');
  console.log('  - Use memory-search to find memories');
  console.log('  - Review MEMORY.md weekly and archive important insights');
}

main();
