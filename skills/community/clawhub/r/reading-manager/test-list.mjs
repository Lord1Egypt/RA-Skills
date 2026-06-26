import { listTextFiles } from '/Users/jianghaidong/.npm-global/lib/node_modules/clawhub/dist/skills.js';

const files = await listTextFiles('.');
console.log('Found files:', files.length);
files.forEach(f => console.log(' -', f.relPath));

// Check for SKILL.md
const hasSkillMd = files.some(f => f.relPath.toLowerCase() === 'skill.md');
console.log('Has SKILL.md:', hasSkillMd);
