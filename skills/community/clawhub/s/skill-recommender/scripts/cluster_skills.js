#!/usr/bin/env node
const { listSkills } = require('./recommend_skills');

function classify(skill) {
  const text = `${skill.name} ${skill.folder} ${skill.description}`.toLowerCase();
  if (/shopping|电商|shop|taobao|jd|pdd|meituan|eleme|vip|shein/.test(text)) return 'commerce';
  if (/skill|skills|clawhub/.test(text)) return 'skilling';
  if (/food|营养|采购|inventory|meal|grocery/.test(text)) return 'household-food';
  if (/second-brain|obsidian|knowledge|阅读|读书/.test(text)) return 'knowledge';
  if (/travel|trip|qunar|flight|hotel/.test(text)) return 'travel';
  return 'general';
}

function clusterSkills(input) {
  const skillsDir = input.skills_dir || require('path').resolve(process.cwd(), 'skills');
  const skills = listSkills(skillsDir);
  const groups = {};
  for (const skill of skills) {
    const key = classify(skill);
    if (!groups[key]) groups[key] = [];
    groups[key].push({ skill: skill.folder, name: skill.name, description: skill.description });
  }
  return {
    scanned: skills.length,
    groups: Object.entries(groups).map(([group, items]) => ({ group, count: items.length, items }))
  };
}

if (require.main === module) {
  const arg = process.argv[2] || '{}';
  try {
    const input = JSON.parse(arg);
    console.log(JSON.stringify(clusterSkills(input), null, 2));
  } catch (e) {
    console.log(JSON.stringify({ error: e.message }, null, 2));
    process.exit(1);
  }
}

module.exports = { clusterSkills };
