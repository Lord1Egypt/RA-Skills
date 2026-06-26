#!/usr/bin/env node
/**
 * memo.cjs — 宙一记忆 CLI 工具
 * 
 * 用法:
 *   node memo.cjs add <内容> [重要性=1.0] [标签1,标签2,...]
 *   node memo.cjs query <关键词> [k=5] [min_imp=0]
 *   node memo.cjs recent [n=10] [min_imp=0]
 *   node memo.cjs status
 *   node memo.cjs compact [group_size=5] [min_imp=0.5]
 *   node memo.cjs cleanup <max_age_hours> [min_imp=0] [max_items]
 *   node memo.cjs clear                      ← 谨慎使用
 *   node memo.cjs migrate <file>             ← 从文件批量导入记忆
 */

(async () => {
  const { MemorySystem } = await import('./memory.js');
  const mem = new MemorySystem();

  const [cmd, ...args] = process.argv.slice(2);

  if (!cmd) {
    console.log(`
Usage:
  memo add <content> [importance=1.0] [tags]
  memo query <query> [k=5] [min_imp=0]
  memo recent [n=10] [min_imp=0]
  memo status
  memo compact [group_size=5] [min_imp=0.5]
  memo cleanup <max_age_hours> [min_imp=0] [max_items]
  memo clear
  memo migrate <file>
`);
    process.exit(1);
  }

  switch (cmd) {
    case 'add':
    case 'a': {
      const text = args[0];
      if (!text) { console.error('Usage: memo add "content" [importance] [tags]'); process.exit(1); }
      const imp = parseFloat(args[1]) || 1.0;
      const tags = args[2] ? args[2].split(',').map(t => t.trim()) : [];
      const meta = tags.length > 0 ? { tags } : {};
      const item = mem.add(text, imp, meta);
      console.log(`Added: [${item.importance}] ${item.content.slice(0, 60)}`);
      console.log(`  id=${item.id.slice(0, 8)}... at=${new Date(item.timestamp).toISOString()}`);
      if (tags.length > 0) console.log(`  tags=${tags.join(', ')}`);
      break;
    }

    case 'query':
    case 'q': {
      const query = args[0];
      if (!query) { console.error('Usage: memo query "query" [k=5] [min_imp=0]'); process.exit(1); }
      const k = parseInt(args[1]) || 5;
      const minImp = parseFloat(args[2]) || 0;
      const results = mem.retrieve(query, k, minImp);
      if (results.length === 0) {
        console.log('No results found.');
        break;
      }
      console.log(`Found ${results.length} results for "${query}":\n`);
      for (const r of results) {
        const date = new Date(r.timestamp).toLocaleDateString('zh-CN');
        console.log(`  [${r.importance.toFixed(1)}] [${date}] ${r.content}`);
        if (r.metadata?.tags) console.log(`       tags: ${r.metadata.tags.join(', ')}`);
        if (r._score) console.log(`       score: ${r._score}`);
        console.log('');
      }
      break;
    }

    case 'recent':
    case 'r': {
      const n = parseInt(args[0]) || 10;
      const minImp = parseFloat(args[1]) || 0;
      const items = mem.getRecent(n, minImp);
      if (items.length === 0) { console.log('No memories.'); break; }
      console.log(`Recent ${items.length} memories:\n`);
      for (const r of items) {
        const date = new Date(r.timestamp).toLocaleDateString('zh-CN');
        console.log(`  [${r.importance.toFixed(1)}] [${date}] ${r.content.slice(0, 80)}`);
      }
      break;
    }

    case 'status':
    case 's': {
      const c = mem.config;
      console.log(`
=== Memory Status ===
  Count:      ${mem.count}
  Max:        ${c.maxMemories}
  DecayRate:  ${c.decayRate}s (${(c.decayRate / 3600).toFixed(1)}h)
  SimWeight:  ${c.simWeight}
  RecencyWgt: ${c.recencyWeight}
  DefaultImp: ${c.defaultImportance}
`);
      break;
    }

    case 'compact':
    case 'c': {
      const gs = parseInt(args[0]) || 5;
      const minImp = parseFloat(args[1]) || 0.5;
      const removed = mem.compact(gs, minImp);
      console.log(`Compacted: removed ${removed}, remaining ${mem.count}`);
      break;
    }

    case 'cleanup': {
      const hours = parseFloat(args[0]);
      if (!hours || hours <= 0) { console.error('Usage: memo cleanup <max_age_hours> [min_imp=0] [max_items]'); process.exit(1); }
      const minImp = parseFloat(args[1]) || 0;
      const maxItems = args[2] ? parseInt(args[2]) : undefined;
      const removed = mem.cleanup(hours * 3600, minImp, maxItems);
      console.log(`Cleaned up: removed ${removed}, remaining ${mem.count}`);
      break;
    }

    case 'clear': {
      console.warn('WARNING: This will delete ALL memories!');
      console.warn('Type CLEAR to confirm:');
      process.stdin.once('data', (d) => {
        if (d.toString().trim() === 'CLEAR') {
          mem.clear();
          console.log('Cleared all memories.');
        } else {
          console.log('Cancelled.');
        }
      });
      break;
    }

    case 'migrate':
    case 'm': {
      const filePath = args[0];
      if (!filePath) { console.error('Usage: memo migrate <json_file>'); process.exit(1); }
      try {
        const { readFileSync, existsSync } = await import('node:fs');
        if (!existsSync(filePath)) { console.error(`File not found: ${filePath}`); process.exit(1); }
        const raw = readFileSync(filePath, 'utf-8');
        const data = JSON.parse(raw);
        let items = [];
        if (Array.isArray(data)) items = data;
        else if (data.memories) items = data.memories;
        else { console.error('Unrecognized format. Expected array or {memories: [...]}'); process.exit(1); }
        let imported = 0;
        for (const item of items) {
          mem.add(item.content, item.importance, item.metadata || {});
          imported++;
        }
        console.log(`Imported ${imported} memories from ${filePath}`);
      } catch (err) {
        console.error(`Migration error: ${err.message}`);
      }
      break;
    }

    default:
      console.error(`Unknown command: ${cmd}`);
      process.exit(1);
  }
})().catch(err => {
  console.error('Error:', err.message);
  process.exit(1);
});
