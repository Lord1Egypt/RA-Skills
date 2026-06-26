/**
 * 高级查询示例
 * 
 * 本示例展示高级查询功能，包括全文搜索、情感查询等
 */

const { 
  queryByTag, 
  queryByDate, 
  queryBySentiment, 
  searchMemories, 
  getStats 
} = require('../memory/scripts/query.cjs');

console.log('=== Unified Memory Architect - 高级查询示例 ===\n');

// 1. 全文搜索
console.log('1. 全文搜索: "memory system"');
const searchResults = searchMemories('memory system', 5);
console.log(`   找到 ${searchResults.length} 条相关记忆:`);
searchResults.forEach((result, i) => {
  const preview = result.memory.content.assistant.substring(0, 100);
  console.log(`   [${i+1}] 分数: ${result.score.toFixed(2)}`);
  console.log(`       内容: ${preview}...`);
});
console.log('');

// 2. 按情感查询 - 积极
console.log('2. 积极情感记忆');
const positiveMemories = queryBySentiment('positive', 3);
console.log(`   找到 ${positiveMemories.length} 条积极记忆:`);
positiveMemories.forEach((m, i) => {
  console.log(`   [${i+1}] ${m.content.assistant.substring(0, 60)}...`);
});
console.log('');

// 3. 按情感查询 - 中性
console.log('3. 中性情感记忆');
const neutralMemories = queryBySentiment('neutral', 3);
console.log(`   找到 ${neutralMemories.length} 条中性记忆:`);
neutralMemories.forEach((m, i) => {
  console.log(`   [${i+1}] ${m.content.assistant.substring(0, 60)}...`);
});
console.log('');

// 4. 多标签组合
console.log('4. 标签分析');
const stats = getStats();
console.log('   热门标签 TOP 10:');
const topTags = Object.entries(stats.byTag || {})
  .sort((a, b) => b[1] - a[1])
  .slice(0, 10);
topTags.forEach(([tag, count], i) => {
  console.log(`   [${i+1}] ${tag}: ${count}`);
});
console.log('');

// 5. 日期范围查询
console.log('5. 日期分布');
const dates = Object.entries(stats.byDate || {})
  .sort((a, b) => b[0].localeCompare(a[0]))
  .slice(0, 5);
console.log('   最近日期:');
dates.forEach(([date, count]) => {
  console.log(`   ${date}: ${count} 条记忆`);
});

console.log('\n=== 示例完成 ===');
