#!/usr/bin/env node
const { listSkills } = require('./recommend_skills');

function tokenize(text) {
  return String(text || '')
    .toLowerCase()
    .replace(/[^a-z0-9\u4e00-\u9fa5\-\s]/g, ' ')
    .split(/\s+/)
    .filter(Boolean);
}

function similarity(a, b) {
  const A = new Set(tokenize(a));
  const B = new Set(tokenize(b));
  if (A.size === 0 || B.size === 0) return 0;
  let inter = 0;
  for (const x of A) if (B.has(x)) inter++;
  return inter / Math.sqrt(A.size * B.size);
}

function decisionFrom(topScore, secondScore) {
  if (topScore >= 0.78) return 'reuse-existing';
  if (topScore >= 0.58) return 'extend-existing';
  if (topScore >= 0.42 && secondScore >= 0.35) return 'merge-overlap';
  return 'build-new';
}

function dedupCheck(input) {
  const skillsDir = input.skills_dir || require('path').resolve(process.cwd(), 'skills');
  const request = input.request || input.query || input.idea || input.description;
  const limit = Number(input.limit || 6);
  if (!request) return { error: 'Missing required field: request' };

  const skills = listSkills(skillsDir);
  const ranked = skills.map(skill => {
    const text = `${skill.name} ${skill.folder} ${skill.description}`;
    const score = similarity(request, text);
    const overlap = [];
    const reqTokens = tokenize(request);
    const skillTokens = new Set(tokenize(text));
    for (const token of reqTokens) if (skillTokens.has(token)) overlap.push(token);
    return {
      skill: skill.folder,
      name: skill.name,
      description: skill.description,
      score: Number(score.toFixed(3)),
      overlap_terms: [...new Set(overlap)].slice(0, 10)
    };
  }).sort((a, b) => b.score - a.score);

  const top = ranked[0] || null;
  const second = ranked[1] || null;
  const decision = decisionFrom(top ? top.score : 0, second ? second.score : 0);

  const direct = ranked.filter(x => x.score >= 0.58).slice(0, limit);
  const overlapSkills = ranked.filter(x => x.score >= 0.35 && x.score < 0.58).slice(0, limit);

  let reason = 'No strong overlap found; a new skill is reasonable.';
  if (decision === 'reuse-existing' && top) {
    reason = `The requested skill is already strongly covered by ${top.skill}. Reuse before creating something new.`;
  } else if (decision === 'extend-existing' && top) {
    reason = `The request is close to ${top.skill}. Extending that skill is likely better than starting from scratch.`;
  } else if (decision === 'merge-overlap') {
    reason = 'Several partially overlapping skills exist. Merging or consolidating them is likely better than creating another similar skill.';
  }

  return {
    request,
    scanned: skills.length,
    decision,
    reason,
    closest_skills: ranked.slice(0, limit),
    direct_reuse_candidates: direct,
    overlap_candidates: overlapSkills,
    gaps: decision === 'build-new'
      ? ['No existing skill strongly matches the requested function.']
      : ['Check whether small feature additions can be absorbed into an existing skill.']
  };
}

if (require.main === module) {
  const arg = process.argv[2];
  if (!arg) {
    console.log(JSON.stringify({ error: 'Usage: check_skill_dedup.js \'{...}\'' }, null, 2));
    process.exit(1);
  }
  try {
    const input = JSON.parse(arg);
    console.log(JSON.stringify(dedupCheck(input), null, 2));
  } catch (e) {
    console.log(JSON.stringify({ error: e.message }, null, 2));
    process.exit(1);
  }
}

module.exports = { dedupCheck };
