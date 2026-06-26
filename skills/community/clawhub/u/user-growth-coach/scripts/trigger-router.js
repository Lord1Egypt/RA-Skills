#!/usr/bin/env node

const input = process.argv.slice(2).join(' ').trim();
if (!input) {
  console.log(JSON.stringify({ error: 'empty_input' }, null, 2));
  process.exit(1);
}

const mode = /(快速|标准|深度)/.exec(input)?.[1] || '标准';
const trigger = ['复盘','周盘','月盘','决策','情绪','目标','习惯','结束','汇总','总结'].find(t => input.includes(t));

const map = {
  '复盘': { type: 'daily_review', dimension: 'work' },
  '周盘': { type: 'weekly_review', dimension: 'all' },
  '月盘': { type: 'monthly_review', dimension: 'all' },
  '决策': { type: 'decision_review', dimension: 'wealth' },
  '情绪': { type: 'emotion_check', dimension: 'relationship_emotion' },
  '目标': { type: 'goal_alignment', dimension: 'all' },
  '习惯': { type: 'habit_tracking', dimension: 'health' },
  '结束': { type: 'insight_summary', dimension: 'all' },
  '汇总': { type: 'insight_summary', dimension: 'all' },
  '总结': { type: 'insight_summary', dimension: 'all' },
};

if (!trigger) {
  console.log(JSON.stringify({
    route: 'fallback',
    message: '未匹配触发词，请使用：复盘/周盘/月盘/决策/情绪/目标/习惯',
  }, null, 2));
  process.exit(0);
}

console.log(JSON.stringify({
  route: map[trigger].type,
  trigger,
  mode,
  dimension: map[trigger].dimension,
  next: 'load_template',
  templateRef: 'references/templates.md'
}, null, 2));
