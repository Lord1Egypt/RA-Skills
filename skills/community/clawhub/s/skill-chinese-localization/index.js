const skillGlossary = require('./glossary.json');
// 自然语言匹配技能
function matchSkill(userQuery) {
  const matches = [];
  for (const [techName, info] of Object.entries(skillGlossary)) {
    if (userQuery.includes(info.keyword) || info.cnName.includes(userQuery) || info.description.includes(userQuery)) {
      matches.push({
        techName,
        cnName: info.cnName,
        description: info.description,
        value: info.value
      });
    }
  }
  return matches.length > 0 ? matches : null;
}
module.exports = { matchSkill };
