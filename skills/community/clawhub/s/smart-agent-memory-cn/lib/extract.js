/**
 * Skill Extraction — turn lessons into reusable SKILL.md templates.
 */

'use strict';
const fs = require('fs');
const path = require('path');

/**
 * Extract a lesson into a skill template.
 * @param {object} lesson - Lesson object from store
 * @param {string} outputDir - Where to write the skill (e.g., ~/.openclaw/skills/<name>)
 * @param {string} skillName - Skill name (slug)
 */
function extractSkill(lesson, outputDir, skillName) {
  fs.mkdirSync(outputDir, { recursive: true });

  const skillMd = `---
name: ${skillName}
description: "Auto-extracted from lesson: ${lesson.action}"
metadata:
  openclaw:
    trust: low
---

# ${skillName}

> Auto-generated from lesson **${lesson.id}** on ${lesson.createdAt.slice(0, 10)}

## Context

${lesson.context}

## What Happened

${lesson.action}

## Outcome

**${lesson.outcome}**

## Insight / Best Practice

${lesson.insight}

## When to Use

Apply this skill when you encounter a similar situation:
- Context matches: ${lesson.context}
- To avoid repeating: ${lesson.outcome === 'negative' ? 'the same mistake' : 'missing the opportunity'}

---

*Extracted by smart-agent-memory skill extraction.*
`;

  fs.writeFileSync(path.join(outputDir, 'SKILL.md'), skillMd);
  return path.join(outputDir, 'SKILL.md');
}

module.exports = { extractSkill };
