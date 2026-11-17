'use strict';

// Discovery supplies the analyzer with SKILL.md metadata from explicit host
// roots. It does not select, execute, install, or suppress a skill itself.
const fs = require('fs');
const { platformRoots } = require('./platforms');
const path = require('path');
const { directSkillFiles, locateSkillRoots, readSkill } = require('./skill');

function discoverSkills(options = {}) {
  const roots = options.roots || platformRoots(options);
  const found = [];
  const seen = new Map();

  for (const origin of roots) {
    if (!fs.existsSync(origin.root)) continue;
    const rootsToRead = origin.direct || path.basename(origin.root).toLowerCase() === 'skills'
      ? [origin.root]
      : locateSkillRoots(origin.root, origin.depth);
    for (const file of rootsToRead.flatMap(directSkillFiles)) {
      let real;
      try {
        real = fs.realpathSync(file);
      } catch (_) {
        continue;
      }
      if (seen.has(real)) {
        const existing = seen.get(real);
        if (!existing.origins.some((item) => item.agent === origin.agent && item.scope === origin.scope)) {
          existing.origins.push({ agent: origin.agent, scope: origin.scope, root: origin.root });
        }
        continue;
      }
      try {
        const skill = readSkill(file, origin);
        skill.origins = [{ agent: origin.agent, scope: origin.scope, root: origin.root }];
        found.push(skill);
        seen.set(real, skill);
      } catch (_) {
        // An unreadable skill should not break every prompt hook.
      }
    }
  }
  return found.sort((left, right) => left.name.localeCompare(right.name) || left.path.localeCompare(right.path));
}

module.exports = { discoverSkills };
