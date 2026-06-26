#!/usr/bin/env node
/**
 * xhsfenxi — report-plan.js
 * Purpose: Print recommended deliverables and filenames for a Xiaohongshu analysis request.
 * Usage:
 *   node scripts/report-plan.js <creator-name>
 *   node scripts/report-plan.js <creator-a> <creator-b> --mode compare
 */

const args = process.argv.slice(2);
const modeIdx = args.indexOf('--mode');
const mode = modeIdx !== -1 ? args[modeIdx + 1] : 'single';
const names = args.filter((a, i) => {
  if (a === '--mode') return false;
  if (modeIdx !== -1 && i === modeIdx + 1) return false;
  return true;
});

if (!names.length) {
  console.error('Usage: node scripts/report-plan.js <creator-name>');
  console.error('       node scripts/report-plan.js <creator-a> <creator-b> --mode compare');
  process.exit(1);
}

if (mode === 'compare') {
  if (names.length < 2) {
    console.error('Compare mode requires two creator names.');
    process.exit(1);
  }
  const [a, b] = names;
  const files = [
    `选题公式学习-综合版.docx`
  ];
  console.log(`
=== xhsfenxi report plan ===

Mode: comparison
Creators: ${a} / ${b}

Recommended deliverables:
- comparison report
- hybrid topic-formula study
- optional business Word version

Recommended filenames:
${files.map(f => `- ${f}`).join('\n')}
`);
  process.exit(0);
}

const name = names[0];
const files = [
  `${name}-结构化总结报告.docx`,
  `${name}-爆款选题公式.docx`
];

console.log(`
=== xhsfenxi report plan ===

Mode: single creator
Creator: ${name}

Recommended deliverables:
- structured report
- viral topic formula
- optional business Word version

Recommended filenames:
${files.map(f => `- ${f}`).join('\n')}
`);
