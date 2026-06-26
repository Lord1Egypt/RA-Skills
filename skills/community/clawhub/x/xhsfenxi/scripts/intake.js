#!/usr/bin/env node
/**
 * xhsfenxi — intake.js
 * Purpose: Print a structured intake template for a Xiaohongshu creator-analysis task.
 * Usage:
 *   node scripts/intake.js
 *   node scripts/intake.js --json
 */

const args = process.argv.slice(2);
const asJson = args.includes('--json');

const template = {
  task: 'xiaohongshu-creator-analysis',
  creatorNames: ['<creator-name>'],
  links: ['<homepage-or-search-url>'],
  screenshots: ['<optional-local-path-or-url>'],
  deliverables: ['structured-report'],
  outputDir: '<optional-output-dir>',
  needWord: false,
  needBusinessVersion: false,
  needComparison: false,
  notes: 'What exactly should be learned from this creator?'
};

if (asJson) {
  console.log(JSON.stringify(template, null, 2));
  process.exit(0);
}

console.log(`
=== xhsfenxi intake template ===

Provide or confirm the following before deep research:

- creator name(s)
- homepage/search URL(s)
- screenshots or links for representative posts (optional but helpful)
- requested deliverable(s): structured-report / topic-formula / comparison / business-word
- output directory
- any specific question to answer

JSON template:
${JSON.stringify(template, null, 2)}
`);
