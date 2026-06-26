/**
 * 基础使用示例
 * 
 * 本示例展示如何使用 Unified Memory Architect 的基础查询功能
 */

const { queryByTag, queryByDate, getStats } = require('../memory/scripts/query.cjs');

console.log('=== Unified Memory Architect - 基础使用示例 ===\n');

// 1. 获取系统统计
console.log('1. 获取系统统计');
const stats = getStats();
console.log(`   总记忆数: ${stats.totalMemories}`);
console.log(`   唯一标签: ${stats.uniqueTags}`);
console.log(`   唯一实体: ${stats.uniqueEntities}`);
console.log('');

// 2. 按标签查询
console.log('2. 按标签查询 (reflection)');
const reflections = queryByTag('reflection', 3);
console.log(`   找到 ${reflections.length} 条相关记忆:`);
reflections.forEach((m, i) => {
  console.log(`   [${i+1}] ${m.content.assistant.substring(0, 80)}...`);
});
console.log('');

// 3. 按日期查询
console.log('3. 按日期查询 (2026-04-12)');
const todayMemories = queryByDate('2026-04-12', 3);
console.log(`   找到 ${todayMemories.length} 条记忆`);
console.log('');

// 4. 情感分析
console.log('4. 情感分布');
console.log(`   中性: ${stats.bySentiment?.neutral || 0}`);
console.log(`   积极: ${stats.bySentiment?.positive || 0}`);
console.log(`   消极: ${stats.bySentiment?.negative || 0}`);
console.log('');

// 5. 语言分布
console.log('5. 语言分布');
console.log(`   中文: ${stats.byLanguage?.zh || 0}`);
console.log(`   英文: ${stats.byLanguage?.en || 0}`);

console.log('\n=== 示例完成 ===');
