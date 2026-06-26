const fs = require('fs');
const os = require('os');
const path = require('path');

const STUB_HTML_COMMENT =
  '<!-- fasterizy stub for always-on rule context. Full skill: https://github.com/felipeinf/fasterizy/blob/main/SKILL.md -->\n\n';

function readSkillBody(packageRoot) {
  const skillPath = path.join(packageRoot, 'SKILL.md');
  const raw = fs.readFileSync(skillPath, 'utf8');
  return raw.replace(/^---[\s\S]*?---\s*/, '').trim();
}

function buildStubBody(fullBody) {
  try {
    const re = /^## (.+)$/gm;
    const matches = [...fullBody.matchAll(re)];
    if (matches.length === 0) {
      console.warn('fasterizy: buildStubBody: no ## sections, using full body');
      return fullBody;
    }

    const parts = [];
    for (let i = 0; i < matches.length; i++) {
      const m = matches[i];
      const title = m[1].trim();
      const start = m.index;
      const nextStart = i + 1 < matches.length ? matches[i + 1].index : fullBody.length;
      let block = fullBody.slice(start, nextStart);

      if (title === 'Cursor' || title.startsWith('Documentation scope') || title === 'Explicit pass') {
        continue;
      }
      if (title === 'Rules') {
        const ex = block.indexOf('\n### Examples');
        if (ex !== -1) {
          block = `${block.slice(0, ex).replace(/\s+$/, '')}\n`;
        }
        parts.push(block);
        continue;
      }
      parts.push(block);
    }

    const result = `${parts.join('\n').trim()}\n`;
    if (result.length < 80) {
      console.warn('fasterizy: buildStubBody: result too short, using full body');
      return fullBody;
    }
    return result;
  } catch (e) {
    console.warn('fasterizy: buildStubBody error:', e.message);
    return fullBody;
  }
}

/**
 * Copies root SKILL.md (including frontmatter) to the user-scoped Cursor skills dir (~/.cursor/skills/fasterizy/).
 * Visible in all Cursor projects, loaded on-demand.
 * @param {string} packageRoot
 * @param {{ root?: string }} [opts] - override base dir (e.g. home) for tests
 * @returns {string} Absolute path to the installed SKILL.md
 */
function installCursorSkill(packageRoot, opts) {
  const root = (opts && opts.root) || os.homedir();
  const src = path.join(packageRoot, 'SKILL.md');
  const targetDir = path.join(root, '.cursor', 'skills', 'fasterizy');
  fs.mkdirSync(targetDir, { recursive: true });
  const target = path.join(targetDir, 'SKILL.md');
  fs.copyFileSync(src, target);
  return target;
}

function writeRule({ cwd, segments, filename, frontmatter, body }) {
  const targetDir = path.join(cwd, ...segments);
  fs.mkdirSync(targetDir, { recursive: true });
  const target = path.join(targetDir, filename);
  const content = `---\n${frontmatter}\n---\n\n${body}\n`;
  fs.writeFileSync(target, content);
  return target;
}

/**
 * @param {string} packageRoot
 * @param {{ cwd?: string }} [opts]
 * @returns {string} Path to fasterizy.md
 */
function installWindsurfRule(packageRoot, opts) {
  const cwd = (opts && opts.cwd) || process.cwd();
  const body = STUB_HTML_COMMENT + buildStubBody(readSkillBody(packageRoot));
  return writeRule({
    cwd,
    segments: ['.windsurf', 'rules'],
    filename: 'fasterizy.md',
    frontmatter:
      'trigger: always_on\ndescription: Fasterizy — direct prose for agent planning and docs',
    body,
  });
}

module.exports = {
  installCursorSkill,
  installWindsurfRule,
  buildStubBody,
  readSkillBody,
};
