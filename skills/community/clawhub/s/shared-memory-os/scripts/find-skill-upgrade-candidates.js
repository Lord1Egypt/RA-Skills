#!/usr/bin/env node
const fs = require('fs');
const path = require('path');
const ROOT = '/home/zqh2333/.openclaw/workspace';
const LEARN = path.join(ROOT, '.learnings');
const skillsDir = path.join(ROOT, 'skills');
const learnings = fs.readdirSync(LEARN).filter(f => f.endsWith('.md') && f !== 'INDEX.md').map(f => fs.readFileSync(path.join(LEARN, f), 'utf8')).join('\n');
const keywords = ['learnings', 'governance', 'fallback', 'trigger', 'review', 'retry', 'browser', 'memory'];
const suggestions = [];
for (const skill of fs.readdirSync(skillsDir)) {
  const p = path.join(skillsDir, skill, 'SKILL.md');
  if (!fs.existsSync(p)) continue;
  const text = fs.readFileSync(p, 'utf8').toLowerCase();
  const hits = keywords.filter(k => learnings.toLowerCase().includes(k) && !text.includes(k));
  if (!hits.length) continue;
  suggestions.push({
    skill,
    reason: 'Workspace learnings suggest reusable guidance that this skill does not explicitly mention yet.',
    evidence: hits,
    confidence: hits.length >= 3 ? 'medium' : 'low',
    suggestedAction: 'Review whether these repeated patterns should be added to the skill guidance or references.',
    collaborationType: 'memory-to-skill-upgrade'
  });
}
console.log(JSON.stringify({ candidates: suggestions.length, suggestions }, null, 2));
