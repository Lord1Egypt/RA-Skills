/**
 * CLI - 统一命令行入口
 * 
 * Usage:
 *   node cli/index.js search "query"
 *   node cli/index.js store "text" --category preference --importance 0.8
 *   node cli/index.js stats
 *   node cli/index.js health
 *   node cli/index.js insights
 *   node cli/index.js graph build
 *   node cli/index.js qa "question"
 *   node cli/index.js dedup --dry-run
 *   node cli/index.js decay --apply
 *   node cli/index.js forget --dry-run
 *   node cli/index.js archive --days 90
 *   node cli/index.js compress
 *   node cli/index.js server
 *   node cli/index.js sync status
 *   node cli/index.js sync add-node --node-id agent-2
 */

import { parseArgs } from 'util';
import { hybridSearch } from '../fusion.js';
import { getAllMemories, addMemory, deleteMemory } from '../storage.js';
import { analyzeInsights } from '../tools/insights.js';
import { exportMemories } from '../tools/export.js';
import { dedupMemories } from '../tools/dedup.js';
import { cmdDedup } from './dedup_commands.js';
import { decayMemories } from '../tools/decay.js';
import { askQuestion } from '../tools/qa.js';
import { forget, archive, compressCold, forgetterStats } from '../quality/smart_forgetter.js';
import { buildGraph, getGraphStats } from '../graph/graph.js';
import { getSyncStatus, registerNode, sync, resolveConflicts } from '../backup/sync.js';
import { startServer } from '../api/server.js';

const COMMANDS = {
  search: { description: '搜索记忆', handler: cmdSearch },
  store: { description: '存储记忆', handler: cmdStore },
  stats: { description: '统计信息', handler: cmdStats },
  health: { description: '健康检查', handler: cmdHealth },
  insights: { description: '用户洞察', handler: cmdInsights },
  export: { description: '导出记忆', handler: cmdExport },
  graph: { description: '知识图谱', handler: cmdGraph },
  qa: { description: '智能问答', handler: cmdQA },
  dedup: { description: '去重检测', handler: cmdDedup },
  decay: { description: '应用衰减', handler: cmdDecay },
  forget: { description: '智能遗忘', handler: cmdForget },
  archive: { description: '归档记忆', handler: cmdArchive },
  compress: { description: '压缩冷记忆', handler: cmdCompress },
  server: { description: '启动API服务器', handler: cmdServer },
  sync: { description: '多Agent同步', handler: cmdSync },
  resolve: { description: '解决冲突', handler: cmdResolve },
  list: { description: '列出所有记忆', handler: cmdList },
  delete: { description: '删除记忆', handler: cmdDelete },
  help: { description: '显示帮助', handler: cmdHelp }
};

async function cmdSearch(args) {
  const query = args.query || (args._ ? args._[0] : undefined);
  const topK = args.topK || args.k || 5;
  
  if (!query) {
    console.log('Usage: memory search "query" [--top-k 5]');
    return;
  }
  
  console.log(`🔍 搜索: "${query}"\n`);
  
  const results = await hybridSearch(query, topK, 'hybrid');
  
  if (results.length === 0) {
    console.log('   未找到相关记忆\n');
    return;
  }
  
  console.log(`📊 找到 ${results.length} 条记忆:\n`);
  
  for (let i = 0; i < results.length; i++) {
    const r = results[i];
    const pct = Math.round(r.fusionScore * 100);
    console.log(`[${i + 1}] [${r.memory.category || 'general'}] ${r.memory.text.slice(0, 70)}...`);
    console.log(`    匹配度: ${pct}% | 重要性: ${r.memory.importance || 0.5}`);
    if (r.highlight) console.log(`    高亮: ${r.highlight.slice(0, 50)}...`);
    console.log();
  }
}

async function cmdStore(args) {
  const text = args.text || args._[0];
  const category = args.category || 'general';
  const importance = parseFloat(args.importance || 0.5);
  
  if (!text) {
    console.log('Usage: memory store "text" [--category preference] [--importance 0.8]');
    return;
  }
  
  const mem = addMemory({ text, category, importance });
  console.log(`✅ 已存储: ${text.slice(0, 50)}...`);
  console.log(`   ID: ${mem.id}`);
  console.log(`   Category: ${category} | Importance: ${importance}`);
}

async function cmdStats(args) {
  const memories = getAllMemories();
  const categories = {};
  const tagCounts = {};
  
  for (const m of memories) {
    const cat = m.category || 'other';
    categories[cat] = (categories[cat] || 0) + 1;
    for (const tag of m.tags || []) {
      tagCounts[tag] = (tagCounts[tag] || 0) + 1;
    }
  }
  
  console.log(`\n📊 记忆统计\n`);
  console.log(`   总数: ${memories.length}`);
  console.log(`   类别:`);
  for (const [cat, count] of Object.entries(categories)) {
    console.log(`     - ${cat}: ${count}`);
  }
  
  const topTags = Object.entries(tagCounts).sort((a, b) => b[1] - a[1]).slice(0, 5);
  if (topTags.length > 0) {
    console.log(`   热门标签:`);
    for (const [tag, count] of topTags) {
      console.log(`     - ${tag}: ${count}`);
    }
  }
  console.log();
}

async function cmdHealth(args) {
  console.log('🏥 健康检查\n');
  
  let ollamaOk = false;
  try {
    const res = await fetch('http://localhost:11434/api/tags');
    ollamaOk = res.ok;
  } catch { }
  
  const memories = getAllMemories();
  
  console.log(`   记忆数: ${memories.length}`);
  console.log(`   Ollama: ${ollamaOk ? '✅ 连接正常' : '⚠️ 未连接'}`);
  console.log(`   嵌入模型: nomic-embed-text`);
  console.log();
}

async function cmdInsights(args) {
  const result = await analyzeInsights();
  console.log(JSON.parse(result.content[0].text));
}

async function cmdExport(args) {
  const format = args.format || 'json';
  const output = args.output || null;
  const category = args.category || null;
  const minImportance = args.minImportance ? parseFloat(args.minImportance) : undefined;
  
  const result = await exportMemories({ format, output, category, minImportance });
  const data = JSON.parse(result.content[0].text);
  
  if (data.success) {
    console.log(`✅ 导出成功: ${data.count} 条记忆`);
    console.log(`   格式: ${data.format}`);
    console.log(`   路径: ${data.path}`);
  } else {
    console.log(`❌ 导出失败: ${result.content[0].text}`);
  }
}

async function cmdGraph(args) {
  const subcmd = args._[0] || 'build';
  
  if (subcmd === 'build') {
    console.log('🔨 构建知识图谱...\n');
    const result = await buildGraph();
    console.log(`   节点: ${result.nodes?.length || 0}`);
    console.log(`   边: ${result.edges?.length || 0}`);
  } else if (subcmd === 'stats') {
    const stats = await getGraphStats();
    console.log(stats);
  }
}

async function cmdQA(args) {
  const question = args.question || args._[0];
  
  if (!question) {
    console.log('Usage: memory qa "问题"');
    return;
  }
  
  console.log(`❓ 问题: ${question}\n`);
  
  const result = await askQuestion({ question });
  const data = JSON.parse(result.content[0].text);
  
  console.log(`💡 回答: ${data.answer}\n`);
  if (data.sources?.length > 0) {
    console.log(`📚 参考记忆 (${data.sources.length} 条):`);
    for (const s of data.sources) {
      console.log(`   - [${s.id.slice(0, 8)}] ${s.text.slice(0, 50)}... (相关度: ${s.relevance})`);
    }
  }
}

async function cmdDecay(args) {
  const apply = args.apply !== undefined;
  
  const result = await decayMemories({ apply });
  const data = JSON.parse(result.content[0].text);
  
  console.log(`\n📉 衰减分析\n`);
  console.log(`   总记忆: ${data.stats.total}`);
  console.log(`   显著衰减: ${data.stats.significantly_decayed}`);
  console.log(`   轻微衰减: ${data.stats.slightly_decayed}`);
  console.log(`   无变化: ${data.stats.unchanged}`);
  console.log(`   模式: ${apply ? '已应用' : '预览'}`);
  console.log();
}

async function cmdForget(args) {
  const dryRun = args.dryRun !== undefined ? args.dryRun : true;
  
  const result = await forget({ dryRun });
  const data = JSON.parse(result.content[0].text);
  
  console.log(`\n🧹 智能遗忘 (${data.mode})\n`);
  console.log(`   可遗忘: ${data.forgettable_count || data.forgotten_count || 0}`);
  if (data.forgettable) {
    for (const f of data.forgettable.slice(0, 5)) {
      console.log(`   - [${f.reason}] ${f.text?.slice(0, 40)}...`);
    }
  }
  console.log();
}

async function cmdArchive(args) {
  const days = parseInt(args.days || 90);
  const dryRun = args.dryRun !== undefined ? args.dryRun : true;
  
  const result = await archive({ days, dryRun });
  const data = JSON.parse(result.content[0].text);
  
  console.log(`\n📦 归档 (${data.mode}, ${days}天)\n`);
  console.log(`   将归档: ${data.archived_count}`);
  console.log();
}

async function cmdCompress(args) {
  const result = await compressCold();
  const data = JSON.parse(result.content[0].text);
  
  console.log(`\n🗜️ 冷记忆压缩\n`);
  console.log(`   压缩: ${data.compressed_count} 条`);
  console.log(`   压缩率: ${Math.round(data.compression_ratio * 100)}%`);
  console.log();
}

async function cmdServer(args) {
  const port = parseInt(args.port || 38421);
  console.log(`🚀 启动 API 服务器 on port ${port}...\n`);
  startServer(port);
}

async function cmdSync(args) {
  const subcmd = args._[0] || 'status';
  
  if (subcmd === 'status') {
    const status = getSyncStatus();
    console.log(`\n🔄 同步状态\n`);
    console.log(`   节点: ${status.nodes}`);
    console.log(`   活跃: ${status.active_nodes?.length || 0}`);
    console.log(`   最后同步: ${status.last_sync || '从未'}`);
    console.log(`   待处理冲突: ${status.pending_conflicts}`);
    console.log();
  } else if (subcmd === 'add-node') {
    const nodeId = args.nodeId || args.n;
    if (!nodeId) {
      console.log('Usage: memory sync add-node --node-id <id>');
      return;
    }
    const result = registerNode(nodeId);
    console.log(`✅ 节点注册: ${nodeId} (${result.registered ? '成功' : result.reason})`);
  } else if (subcmd === 'sync') {
    const result = sync();
    console.log(`✅ 同步完成: ${result.nodes} 节点`);
  }
}

async function cmdResolve(args) {
  const strategy = args.strategy || 'last_write_wins';
  const result = resolveConflicts(strategy);
  console.log(`\n✅ 冲突解决 (${strategy})\n`);
  console.log(`   已解决: ${result.resolved} 个`);
  console.log();
}

async function cmdList(args) {
  const memories = getAllMemories();
  console.log(`\n📋 所有记忆 (${memories.length})\n`);
  
  for (let i = 0; i < memories.length; i++) {
    const m = memories[i];
    console.log(`[${i + 1}] [${m.category || 'general'}] ${m.text.slice(0, 60)}...`);
    console.log(`    ID: ${m.id.slice(0, 8)} | 重要性: ${m.importance || 0.5}`);
  }
  console.log();
}

async function cmdDelete(args) {
  const id = args.id || args._[0];
  
  if (!id) {
    console.log('Usage: memory delete <id>');
    return;
  }
  
  const success = deleteMemory(id);
  console.log(success ? `✅ 已删除: ${id}` : `❌ 删除失败: ${id}`);
}

function cmdHelp(args) {
  console.log(`\n🧠 Unified Memory CLI\n`);
  console.log(`Usage: memory <command> [options]\n`);
  console.log(`Commands:`);
  
  const maxLen = Math.max(...Object.keys(COMMANDS).map(k => k.length));
  for (const [cmd, info] of Object.entries(COMMANDS)) {
    const padding = ' '.repeat(maxLen - cmd.length);
    console.log(`  ${cmd}${padding}  ${info.description}`);
  }
  
  console.log(`\nExamples:\n`);
  console.log(`  memory search "刘总偏好"`);
  console.log(`  memory store "学会了React" --category learning --importance 0.7`);
  console.log(`  memory dedup --threshold 0.9`);
  console.log(`  memory graph build`);
  console.log(`  memory server --port 38421`);
  console.log();
}

// Main entry
const CMD = process.argv[2] || 'help';
const handler = COMMANDS[CMD];

if (!handler) {
  console.log(`Unknown command: ${CMD}`);
  console.log(`Run 'memory help' for usage.\n`);
  process.exit(1);
}

// Parse remaining args
const { values, positionals } = parseArgs({
  args: process.argv.slice(3),
  options: {
    query: { type: 'string' },
    text: { type: 'string' },
    category: { type: 'string' },
    importance: { type: 'string' },
    'top-k': { type: 'string' },
    k: { type: 'string' },
    format: { type: 'string' },
    output: { type: 'string' },
    threshold: { type: 'string' },
    'dry-run': { type: 'boolean' },
    apply: { type: 'boolean' },
    days: { type: 'string' },
    port: { type: 'string' },
    'node-id': { type: 'string' },
    n: { type: 'string' },
    strategy: { type: 'string' },
    id: { type: 'string' },
    minImportance: { type: 'string' }
  },
  allowPositionals: true
});


values._ = positionals;
Promise.resolve(handler.handler(values)).catch(err => {
  console.error(`❌ Error: ${err.message}`);
  process.exit(1);
});
