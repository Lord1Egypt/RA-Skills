#!/usr/bin/env node
const fs = require('fs');
const path = require('path');

function readSkillMeta(skillDir) {
  const skillPath = path.join(skillDir, 'SKILL.md');
  if (!fs.existsSync(skillPath)) return null;
  const text = fs.readFileSync(skillPath, 'utf-8');
  const name = (text.match(/^name:\s*(.+)$/m) || [])[1] || path.basename(skillDir);
  const description = (text.match(/^description:\s*(.+)$/m) || [])[1] || '';
  return {
    folder: path.basename(skillDir),
    name: name.trim().replace(/^"|"$/g, ''),
    description: description.trim().replace(/^"|"$/g, ''),
    path: skillDir
  };
}

function listSkills(skillsDir) {
  if (!fs.existsSync(skillsDir)) return [];
  return fs.readdirSync(skillsDir)
    .map(name => path.join(skillsDir, name))
    .filter(p => fs.existsSync(path.join(p, 'SKILL.md')))
    .map(readSkillMeta)
    .filter(Boolean);
}

function tokenize(text) {
  return String(text || '')
    .toLowerCase()
    .replace(/[^a-z0-9\u4e00-\u9fa5\-\s]/g, ' ')
    .split(/\s+/)
    .filter(Boolean);
}

function inferMatchType(score) {
  if (score >= 80) return 'direct-match';
  if (score >= 60) return 'strong-adjacent';
  if (score >= 40) return 'overlap';
  return 'weak-adjacent';
}

function scoreSkill(query, skill) {
  const qTokens = tokenize(query);
  const nameTokens = tokenize(skill.name + ' ' + skill.folder);
  const descTokens = tokenize(skill.description);
  let score = 0;
  const matched = [];

  for (const token of qTokens) {
    if (nameTokens.includes(token)) {
      score += 30;
      matched.push(token);
      continue;
    }
    if (descTokens.includes(token)) {
      score += 18;
      matched.push(token);
      continue;
    }
    if (skill.description.toLowerCase().includes(token)) {
      score += 10;
      matched.push(token);
    }
  }

  const full = `${skill.name} ${skill.folder} ${skill.description}`.toLowerCase();
  const heuristics = [
    ['购物', ['shopping', 'shop', '电商', 'commerce']],
    ['采购', ['procurement', 'shopping', 'purchase']],
    ['库存', ['inventory', 'stock']],
    ['提醒', ['reminder', 'cron', 'alert']],
    ['知识库', ['knowledge', 'second-brain', 'obsidian']],
    ['外卖', ['delivery', 'eleme', 'meituan']],
    ['技能', ['skill', 'skills']],
  ];
  for (const [queryHint, words] of heuristics) {
    if (query.includes(queryHint) && words.some(w => full.includes(w))) score += 12;
  }

  return {
    score,
    matched: [...new Set(matched)]
  };
}

function recommendSkills(input) {
  const skillsDir = input.skills_dir || path.resolve(process.cwd(), 'skills');
  const query = input.query || input.intent || input.topic;
  const limit = Number(input.limit || 8);
  if (!query) return { error: 'Missing required field: query' };

  const skills = listSkills(skillsDir);
  const ranked = skills
    .map(skill => {
      const scored = scoreSkill(query, skill);
      return {
        skill: skill.folder,
        name: skill.name,
        description: skill.description,
        score: scored.score,
        match_type: inferMatchType(scored.score),
        matched_terms: scored.matched,
        why: scored.matched.length > 0
          ? `Matched on: ${scored.matched.join(', ')}`
          : 'Related by domain heuristics.',
        boundary: `Current scope is defined by: ${skill.description || skill.name}`
      };
    })
    .filter(x => x.score > 0)
    .sort((a, b) => b.score - a.score);

  return {
    query,
    scanned: skills.length,
    recommended: ranked.slice(0, limit),
    secondary: ranked.slice(limit, limit + 5)
  };
}

if (require.main === module) {
  const arg = process.argv[2];
  if (!arg) {
    console.log(JSON.stringify({ error: 'Usage: recommend_skills.js \'{...}\'' }, null, 2));
    process.exit(1);
  }
  try {
    const input = JSON.parse(arg);
    console.log(JSON.stringify(recommendSkills(input), null, 2));
  } catch (e) {
    console.log(JSON.stringify({ error: e.message }, null, 2));
    process.exit(1);
  }
}

module.exports = { recommendSkills, listSkills, readSkillMeta };
