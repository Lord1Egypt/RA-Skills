#!/usr/bin/env node
/**
 * 获取面经完整详情
 * 用法: node interviews_get.js <面经ID>
 *
 * 示例:
 *   node interviews_get.js 69d76d511489a0e96aa770a4
 */
const { mcpCall } = require('./mcp_client');

async function main() {
  const id = process.argv[2];
  if (!id) {
    console.error('请提供面经ID，例如: node interviews_get.js 69d76d511489a0e96aa770a4');
    process.exit(1);
  }

  const result = await mcpCall('interviews.get', { id });
  const det = result?.data || result;
  const c = det?.content || {};

  console.log('========== 面经详情 ==========');
  console.log('标题:   ' + (det.title || '-'));
  console.log('公司:   ' + (det.company || '-'));
  console.log('岗位:   ' + (det.position || '-'));
  console.log('城市:   ' + (det.city || '-'));
  console.log('结果:   ' + (c.outcome || '-'));
  console.log('');
  console.log('--- 面试者背景 ---');
  console.log(c.background || '（无）');
  console.log('');

  const rounds = c.rounds || [];
  rounds.forEach((round, ri) => {
    console.log('===== ' + round.title + ' (' + (round.duration || '') + ') =====');
    console.log('考察重点: ' + (round.tags || []).join(' / '));
    if (round.characteristics) {
      console.log('面试风格: ' + round.characteristics);
    }
    console.log('');
    const qas = round.questionAnswers || [];
    qas.forEach((qa, qi) => {
      console.log('Q' + (qi + 1) + ': ' + qa.question);
      console.log('A' + (qi + 1) + ': ' + (qa.answer || '（无作答）'));
      console.log('');
    });
  });

  if (c.takeaways && c.takeaways.length > 0) {
    console.log('--- 关键要点 ---');
    c.takeaways.forEach((t, i) => console.log((i + 1) + '. ' + t));
  }
}

main().catch(e => { console.error('错误:', e.message); process.exit(1); });
