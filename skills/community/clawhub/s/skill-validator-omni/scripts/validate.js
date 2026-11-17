// skill-validator-omni — validate agent skills against multiple standards.
// Standards: agentskills.io spec, Anthropic best practices, Hermes in-repo
// standard, OpenAgent skills.sh ecosystem discoverability, Claude Code
// marketplace installability, OpenAI Codex (CLI + ChatGPT) skill format.
//
// Canonical source: https://github.com/adelpro/skill-validator-omni
// (the Hermes skill keeps a synced copy under scripts/validate.js)
import { access, readFile, readdir } from 'node:fs/promises';
import { join, relative } from 'node:path';

// Prefer the `yaml` package when resolvable; fall back to a built-in parser
// for the SKILL.md frontmatter subset so the script runs with zero setup.
let parseYaml;
try {
  const yamlMod = await import('yaml');
  parseYaml = (s) => yamlMod.parse(s);
} catch {
  parseYaml = parseSimpleYaml;
}

// Minimal YAML parser for SKILL.md frontmatter: scalar keys, inline lists,
// nested maps via indentation, `key:` + `- item` block lists, quoted,
// boolean, and number values. Fallback when the `yaml` package is absent.
export function parseSimpleYaml(text) {
  const lines = text.split('\n');
  const root = {};
  const stack = [{ indent: -1, obj: root }];
  const unquote = (v) => {
    v = v.trim();
    if ((v.startsWith('"') && v.endsWith('"')) || (v.startsWith("'") && v.endsWith("'"))) {
      return v.slice(1, -1);
    }
    if (v === 'true') return true;
    if (v === 'false') return false;
    if (/^-?\d+$/.test(v)) return Number(v);
    return v;
  };
  const clean = (raw) => {
    const line = raw.replace(/#.*$/, '').trimEnd();
    return line.trim() && !line.trim().startsWith('#') ? line : null;
  };
  let i = 0;
  while (i < lines.length) {
    const line = clean(lines[i]);
    i += 1;
    if (line === null) continue;
    const indent = line.match(/^ */)[0].length;
    const content = line.trim();
    while (stack.length > 1 && indent <= stack[stack.length - 1].indent) stack.pop();
    const { obj } = stack[stack.length - 1];
    const m = content.match(/^([A-Za-z0-9_.-]+):\s*(.*)$/);
    if (!m) continue;
    const key = m[1];
    const val = m[2].trim();
    if (val === '') {
      // Lookahead: block list (`- item`) or nested map?
      const next = clean(lines[i]);
      const nextIndent = next ? next.match(/^ */)[0].length : -1;
      if (next && next.trim().startsWith('- ') && nextIndent > indent) {
        const list = [];
        while (i < lines.length) {
          const item = clean(lines[i]);
          if (!item || item.match(/^ */)[0].length !== nextIndent) break;
          if (!item.trim().startsWith('- ')) break;
          list.push(unquote(item.trim().slice(2)));
          i += 1;
        }
        obj[key] = list;
      } else {
        const nextObj = {};
        obj[key] = nextObj;
        stack.push({ indent, obj: nextObj });
      }
      continue;
    }
    if (val.startsWith('[') && val.endsWith(']')) {
      obj[key] = val.slice(1, -1).split(',').map((s) => unquote(s)).filter((s) => s !== '');
      continue;
    }
    obj[key] = unquote(val);
  }
  return root;
}

export const SCHEMA_URL = 'https://schemas.agentskills.io/discovery/0.2.0/schema.json';
export const AGENT_PLUGINS_SCHEMA = 'https://agent-plugins.org/schemas/1.0.0/plugin.schema.json';
export const AGENT_PLUGINS_MCP_SCHEMA = 'https://agent-plugins.org/schemas/1.0.0/mcp.schema.json';
const AGENT_PLUGINS_ALLOWED_FIELDS = new Set([
  '$schema', 'name', 'version', 'description', 'author', 'homepage',
  'repository', 'license', 'keywords', 'extensions',
]);

// OpenAI Codex skill frontmatter: only these keys are allowed. Mirrors the
// official quick_validate.py from openai/skills ("Do not include any other
// fields in YAML frontmatter" — skill-creator).
const CODEX_ALLOWED_FIELDS = new Set([
  'name', 'description', 'license', 'allowed-tools', 'metadata',
]);

const AGENT_SKILL_DIRS = [
  '.claude/skills',
  '.agents/skills',
  '.cursor/skills',
  '.codex/skills',
  '.gemini/skills',
  '.config/opencode/skills',
];

export function parseFrontmatter(content) {
  if (!content.startsWith('---')) {
    return { error: 'frontmatter must start at byte 0 with ---' };
  }
  const rest = content.slice(3);
  const m = rest.match(/\n---\s*\n/);
  if (!m) {
    return { error: 'frontmatter not closed with ---' };
  }
  const fmText = content.slice(3, m.index + 3);
  try {
    const fm = parseYaml(fmText);
    return { fm, body: content.slice(m.index + 3) };
  } catch (e) {
    return { error: `invalid YAML: ${e.message}` };
  }
}

async function isFile(p) {
  try {
    await access(p);
    return true;
  } catch {
    return false;
  }
}

async function hasSkillMd(dir) {
  return isFile(join(dir, 'SKILL.md'));
}

async function walkForSkillMds(root, maxDepth, skip = new Set()) {
  const found = [];
  let dirs;
  try {
    dirs = await readdir(root, { withFileTypes: true });
  } catch {
    return found;
  }
  for (const entry of dirs) {
    if (!entry.isDirectory() || skip.has(entry.name)) continue;
    const child = join(root, entry.name);
    if (await hasSkillMd(child)) {
      found.push(child);
    } else if (maxDepth > 1) {
      found.push(...(await walkForSkillMds(child, maxDepth - 1, skip)));
    }
  }
  return found;
}

export function validateSingleSkill(skillDir, prefix = '') {
  const checks = [];

  async function run() {
    const skillMd = join(skillDir, 'SKILL.md');
    let content;
    try {
      content = await readFile(skillMd, 'utf8');
    } catch {
      return [{ name: `${prefix}SKILL.md present`, ok: false, detail: `missing ${skillMd}` }];
    }
    const { fm, body, error } = parseFrontmatter(content);
    if (error) {
      return [{ name: `${prefix}frontmatter`, ok: false, detail: error }];
    }
    const name = String(fm.name ?? '');
    const desc = String(fm.description ?? '');

    // Agent Skills spec (agentskills.io/specification.md)
    checks.push({ name: `${prefix}spec: name == directory`, ok: name === skillDir.split(/[\\/]/).pop(), detail: `${name} vs dir ${skillDir}` });
    checks.push({
      name: `${prefix}spec: name format`,
      ok: /^[a-z0-9]+(-[a-z0-9]+)*$/.test(name),
      detail: "lowercase alnum + hyphens; no leading/trailing/consecutive '-'",
    });
    checks.push({ name: `${prefix}spec: name <= 64 chars`, ok: name.length >= 1 && name.length <= 64, detail: `${name.length} chars` });
    checks.push({ name: `${prefix}spec: description 1-1024`, ok: desc.length >= 1 && desc.length <= 1024, detail: `${desc.length} chars` });
    checks.push({ name: `${prefix}spec: body non-empty`, ok: body.trim().length > 0 });
    if ('compatibility' in fm) {
      checks.push({
        name: `${prefix}spec: compatibility <= 500`,
        ok: String(fm.compatibility).length <= 500,
        detail: `${String(fm.compatibility).length} chars`,
      });
    }
    if ('allowed-tools' in fm) {
      checks.push({
        name: `${prefix}spec: allowed-tools is a string`,
        ok: typeof fm['allowed-tools'] === 'string',
        detail: 'space-separated tool allowlist (experimental)',
      });
    }

    // Anthropic best practices
    checks.push({
      name: `${prefix}anthropic: third person`,
      ok: !/^(I |You |We |This skill helps me )/.test(desc),
      detail: desc.slice(0, 50),
    });
    const lineCount = content.split('\n').length - 1;
    checks.push({ name: `${prefix}anthropic: body < 500 lines`, ok: lineCount < 500, detail: `${lineCount} lines` });
    let hasSubdirs = false;
    try {
      const entries = await readdir(skillDir, { withFileTypes: true });
      hasSubdirs = entries.some((e) => e.isDirectory());
    } catch { /* ignore */ }
    checks.push({
      name: `${prefix}anthropic: progressive disclosure`,
      ok: hasSubdirs || lineCount < 200,
      detail: hasSubdirs
        ? 'supporting dirs present'
        : `${lineCount} lines, no supporting dirs (fine below 200 lines)`,
    });

    // Hermes in-repo standard
    checks.push({ name: `${prefix}hermes: description <= 60`, ok: desc.length <= 60, detail: `${desc.length} chars` });
    checks.push({ name: `${prefix}hermes: description ends with .`, ok: desc.endsWith('.') });
    for (const field of ['version', 'author', 'license', 'platforms']) {
      checks.push({ name: `${prefix}hermes: has ${field}`, ok: field in fm });
    }
    const meta = fm.metadata ?? {};
    const hermes = meta.hermes ?? {};
    checks.push({ name: `${prefix}hermes: metadata.hermes.tags`, ok: Boolean(hermes.tags) });
    checks.push({ name: `${prefix}hermes: metadata.hermes.related_skills`, ok: Boolean(hermes.related_skills) });
    for (const section of ['When to Use', 'Procedure', 'Pitfalls', 'Verification']) {
      checks.push({ name: `${prefix}hermes: ## ${section}`, ok: body.includes(`## ${section}`) });
    }

    // Codex / OpenAI (developers.openai.com/codex/skills + openai/skills
    // quick_validate.py). Codex reads ONLY name + description to decide when a
    // skill triggers; everything else must live in the body or supporting
    // files. The directory must be named exactly after the skill.
    const codexName = name === skillDir.split(/[\\/]/).pop();
    const codexNameFormat = /^[a-z0-9-]+$/.test(name) &&
      !name.startsWith('-') && !name.endsWith('-') && !name.includes('--');
    const unexpected = Object.keys(fm).filter((k) => !CODEX_ALLOWED_FIELDS.has(k));
    checks.push({ name: `${prefix}codex: name == directory`, ok: codexName, detail: `${name} vs dir ${skillDir}` });
    checks.push({
      name: `${prefix}codex: name format`,
      ok: codexNameFormat,
      detail: 'hyphen-case: lowercase letters/digits/hyphens, no leading/trailing/consecutive hyphens (openai/skills quick_validate.py)',
    });
    checks.push({
      name: `${prefix}codex: name <= 64 chars`,
      ok: name.length >= 1 && name.length <= 64,
      detail: `${name.length} chars`,
    });
    checks.push({
      name: `${prefix}codex: frontmatter fields allowed`,
      ok: unexpected.length === 0,
      detail: unexpected.length
        ? `unexpected field(s): ${unexpected.slice(0, 4).join(', ')} (allowed: name, description, license, allowed-tools, metadata)`
        : 'only name/description/license/allowed-tools/metadata',
    });
    checks.push({
      name: `${prefix}codex: description present`,
      ok: 'description' in fm && String(fm.description ?? '').length > 0,
    });
    checks.push({
      name: `${prefix}codex: description no angle brackets`,
      ok: !/[<>]/.test(desc),
      detail: 'quick_validate.py rejects < and > in descriptions',
    });
    checks.push({
      name: `${prefix}codex: description <= 1024`,
      ok: desc.length <= 1024,
      detail: `${desc.length} chars`,
    });
    checks.push({
      name: `${prefix}codex: description is the trigger`,
      ok: /\b(when|use|used|for|triggers?|handles?|helps?|if)\b/i.test(desc),
      detail: 'Codex matches a skill by description alone — include what it does AND when to use it (front-load trigger words)',
    });
    checks.push({
      name: `${prefix}codex: body < 500 lines`,
      ok: lineCount < 500,
      detail: `${lineCount} lines`,
    });
    // no ancillary docs: skill-creator says a skill must NOT contain
    // README.md / INSTALLATION_GUIDE.md / QUICK_REFERENCE.md / CHANGELOG.md
    const ancillaryDocs = ['README.md', 'INSTALLATION_GUIDE.md', 'QUICK_REFERENCE.md', 'CHANGELOG.md'];
    const ancillaryFound = [];
    try {
      const entries = await readdir(skillDir, { withFileTypes: true });
      for (const e of entries) {
        if (e.isFile() && ancillaryDocs.includes(e.name)) ancillaryFound.push(e.name);
      }
    } catch { /* ignore */ }
    checks.push({
      name: `${prefix}codex: no ancillary docs`,
      ok: ancillaryFound.length === 0,
      detail: ancillaryFound.length ? `remove ${ancillaryFound.join(', ')}` : 'only SKILL.md + resources allowed',
    });
    // agents/openai.yaml — optional Codex/ChatGPT UI metadata (interface,
    // policy, dependencies). Must parse as YAML with known top-level keys.
    const oaiPath = join(skillDir, 'agents', 'openai.yaml');
    const oaiContent = await readFile(oaiPath, 'utf8').catch(() => null);
    if (oaiContent !== null) {
      const OAI_ALLOWED_KEYS = new Set(['interface', 'policy', 'dependencies']);
      try {
        const oai = parseYaml(oaiContent);
        const oaiKeys = Object.keys(oai ?? {});
        const oaiUnknown = oaiKeys.filter((k) => !OAI_ALLOWED_KEYS.has(k));
        checks.push({
          name: `${prefix}codex: agents/openai.yaml keys`,
          ok: oaiUnknown.length === 0,
          detail: oaiUnknown.length ? `unknown key(s): ${oaiUnknown.join(', ')} (allowed: interface, policy, dependencies)` : oaiKeys.join(', '),
        });
      } catch (e) {
        checks.push({ name: `${prefix}codex: agents/openai.yaml keys`, ok: false, detail: `invalid YAML: ${e.message}` });
      }
    }
    return checks;
  }
  return run();
}

// Human-readable description for each check. Matched by substring against
// the full check name, most specific first, so prefixed checks
// ("skills/x: spec: name format", "agentplugins: ./my-plugin: name format")
// resolve to the right entry.
const DESCRIPTIONS = [
  ['spec: name == directory', 'Frontmatter name must equal the skill directory name. Installers (npx skills, agents) resolve a skill by directory, so a mismatch breaks discovery.'],
  ['spec: name format', 'Skill name: lowercase alphanumerics and hyphens only, no leading, trailing, or consecutive hyphens.'],
  ['spec: name <= 64 chars', 'Skill name must be at most 64 characters.'],
  ['spec: description 1-1024', 'Frontmatter must declare a description of 1 to 1024 characters.'],
  ['spec: body non-empty', 'The SKILL.md body after the frontmatter must not be empty.'],
  ['spec: compatibility <= 500', 'The optional compatibility field must stay within 500 characters.'],
  ['anthropic: third person', 'Description should describe what the skill does (third person), not instruct the agent.'],
  ['anthropic: body < 500 lines', 'Anthropic recommends keeping SKILL.md under 500 lines; move detail into references/ files.'],
  ['anthropic: progressive disclosure', 'Long content belongs in supporting files (references/, scripts/, templates/) so the main SKILL.md stays scannable.'],
  ['hermes: description <= 60', 'Hermes truncates descriptions in its skill index, so keep the description under 60 characters.'],
  ['hermes: description ends with .', 'Hermes convention: the description ends with a full stop.'],
  ['hermes: has version', 'Frontmatter must declare a version.'],
  ['hermes: has author', 'Frontmatter must declare an author.'],
  ['hermes: has license', 'Frontmatter must declare a license.'],
  ['hermes: has platforms', 'Frontmatter must declare platforms (e.g. linux, macos, windows).'],
  ['hermes: metadata.hermes.tags', 'metadata.hermes.tags with category keywords improves discovery.'],
  ['hermes: metadata.hermes.related_skills', 'metadata.hermes.related_skills links to sibling skills in the same category.'],
  ['hermes: ## When to Use', 'The body must include the "When to Use" section.'],
  ['hermes: ## Procedure', 'The body must include the "Procedure" section.'],
  ['hermes: ## Pitfalls', 'The body must include the "Pitfalls" section.'],
  ['hermes: ## Verification', 'The body must include the "Verification" section.'],
  ['skills found', 'A SKILL.md must exist at the repo root, under skills/ (max 3 levels), or in an agent skills directory.'],
  ['openagent: npx skills discoverable layout', 'npx skills and agent tooling discover skills via this layout: root SKILL.md, skills/ (max 3 levels), or agent dirs.'],
  ['openagent: every skill dir name == frontmatter name', 'Each discovered skill directory name must match its frontmatter name.'],
  ['openagent: well-known index $schema', 'A well-known discovery index (.well-known/agent-skills/) must declare the official agentskills.io schema URL.'],
  ['claude: marketplace.json valid JSON', '.claude-plugin/marketplace.json must parse as JSON.'],
  ['claude: marketplace has name', 'A Claude Code marketplace must declare a name.'],
  ['claude: marketplace lists plugins', 'A marketplace must list at least one plugin.'],
  ['claude: plugin ', 'A Claude Code plugin manifest (.claude-plugin/plugin.json) must be valid JSON and declare a name and skills/.'],
  ['claude: installable layout', 'The repo is directly installable in Claude Code via a marketplace or .claude/skills.'],
  ['codex: repo-scoped .agents/skills layout', 'Codex CLI auto-scans .agents/skills upward from the working directory to the repo root (legacy: .codex/skills). Without one of these, Codex will not auto-load the skills — install them with `npx skills add -a codex` or as an Agent Plugins package instead.'],
  ['codex: name == directory', 'Codex resolves a skill by its directory; the directory must be named exactly after the frontmatter name.'],
  ['codex: name format', 'Codex names are hyphen-case: lowercase letters, digits, hyphens, no leading/trailing/consecutive hyphens (openai/skills quick_validate.py).'],
  ['codex: name <= 64 chars', 'Codex caps skill names at 64 characters.'],
  ['codex: frontmatter fields allowed', 'Codex (openai/skills quick_validate.py) allows only name, description, license, allowed-tools, and metadata in the frontmatter. Hermes-style fields (version, author, platforms) are rejected — keep those in skills targeted at other hosts, or accept a Codex failure here.'],
  ['codex: description present', 'Codex requires a description in the frontmatter.'],
  ['codex: description no angle brackets', 'Codex quick_validate.py rejects angle brackets (< >) in descriptions.'],
  ['codex: description <= 1024', 'Codex caps descriptions at 1024 characters.'],
  ['codex: description is the trigger', 'Codex matches skills by description only (the body loads after triggering) — the description must state what the skill does AND when to use it, with trigger words front-loaded.'],
  ['codex: body < 500 lines', 'Codex progressive disclosure: keep SKILL.md under 500 lines; move detail into references/ and scripts/.'],
  ['codex: no ancillary docs', 'A Codex skill contains only SKILL.md plus supporting dirs — README.md, INSTALLATION_GUIDE.md, QUICK_REFERENCE.md, and CHANGELOG.md are explicitly discouraged (skill-creator).'],
  ['codex: agents/openai.yaml keys', 'Optional Codex/ChatGPT UI metadata (agents/openai.yaml) with only interface, policy, and dependencies keys.'],
  ['agentplugins: no plugin.json manifest', 'No Agent Plugin manifest found; the repo makes no Agent Plugins compliance claims (fine for plain skill repos).'],
  ['agentplugins: manifest readable', 'The plugin.json manifest must be readable.'],
  ['agentplugins: manifest valid JSON', 'The plugin.json manifest must parse as JSON.'],
  ['agentplugins: $schema declares Agent Plugins', 'The manifest must reference the official Agent Plugins schema URL (https://agent-plugins.org/schemas/1.0.0/plugin.schema.json).'],
  ['agentplugins: name format', 'Plugin name: 1-64 chars, lowercase alphanumerics, hyphens, dots; no "--" or ".."; must start and end alphanumeric.'],
  ['agentplugins: no unknown top-level fields', 'Agent Plugins uses a closed schema; unknown top-level fields are rejected.'],
  ['agentplugins: keywords is array', 'keywords must be an array of strings.'],
  ['agentplugins: author is object', 'author must be an object (or null).'],
  ['agentplugins: skills/ layout', 'Plugin skills are immediate children of skills/ (skills/<name>/SKILL.md). A skills/ file is invalid; a missing skills/ is fine for MCP-only plugins.'],
  ['agentplugins: mcp.json valid JSON', 'mcp.json (when present) must parse as a JSON object.'],
  ['name format', 'The name must follow the standard\'s format rules: lowercase alphanumerics and hyphens, no leading, trailing, or consecutive hyphens.'],
  ['manifest valid JSON', 'The manifest must parse as JSON.'],
];

export function describeCheck(name) {
  for (const [sub, desc] of DESCRIPTIONS) {
    if (name.includes(sub)) return desc;
  }
  return 'Validation check from the skill standards (agentskills.io, agent-plugins.org, skills.sh, Codex).';
}

// Attach a description to every check before returning.
function annotateChecks(checks) {
  for (const c of checks) {
    if (!c.description) c.description = describeCheck(c.name);
  }
  return checks;
}

export async function validate(root) {
  const checks = [];
  const rootSkill = join(root, 'SKILL.md');

  // Discover skills: root, skills/ (3 levels), agent dirs
  const discovered = [];
  if (await hasSkillMd(root)) discovered.push(root);
  discovered.push(...(await walkForSkillMds(join(root, 'skills'), 3)));
  for (const agentDir of AGENT_SKILL_DIRS) {
    discovered.push(...(await walkForSkillMds(join(root, agentDir), 2)));
  }

  // Validate every discovered skill (root first, no prefix)
  const validated = new Set();
  if (await hasSkillMd(root)) {
    checks.push(...(await validateSingleSkill(root)));
    validated.add(root);
  }
  for (const d of discovered) {
    if (validated.has(d)) continue;
    const rel = relative(root, d);
    checks.push(...(await validateSingleSkill(d, `${rel}: `)));
  }
  if (discovered.length === 0) {
    checks.push({ name: 'skills found', ok: false, detail: `no SKILL.md at ${root} or under skills/, agent dirs` });
  }

  // --- OpenAgent skills.sh ecosystem (`npx skills add <owner/repo>`) ---
  checks.push({
    name: 'openagent: npx skills discoverable layout',
    ok: discovered.length > 0,
    detail: 'SKILL.md at root, or under skills/ (<=3 levels), or agent dirs',
  });
  const badNames = [];
  for (const d of discovered) {
    const content = await readFile(join(d, 'SKILL.md'), 'utf8').catch(() => '');
    const { fm } = parseFrontmatter(content);
    if (fm && String(fm.name ?? '') !== d.split(/[\\/]/).pop()) {
      badNames.push(`${d.split(/[\\/]/).pop()} (frontmatter ${fm.name})`);
    }
  }
  checks.push({
    name: 'openagent: every skill dir name == frontmatter name',
    ok: badNames.length === 0,
    detail: badNames.slice(0, 3).join('; '),
  });

  // Well-known discovery index schema (HTTP-published skills)
  for (const wk of [join(root, '.well-known/agent-skills/index.json'), join(root, '.well-known/skills/index.json')]) {
    const content = await readFile(wk, 'utf8').catch(() => null);
    if (content !== null) {
      try {
        const idx = JSON.parse(content);
        checks.push({
          name: 'openagent: well-known index $schema',
          ok: idx.$schema === SCHEMA_URL,
          detail: idx.$schema ?? '(missing)',
        });
      } catch (e) {
        checks.push({ name: 'openagent: well-known index $schema', ok: false, detail: `invalid JSON: ${e.message}` });
      }
    }
  }

  // --- Claude Code installability ---
  const mp = join(root, '.claude-plugin/marketplace.json');
  const mpContent = await readFile(mp, 'utf8').catch(() => null);
  if (mpContent !== null) {
    try {
      const mdata = JSON.parse(mpContent);
      checks.push({ name: 'claude: marketplace.json valid JSON', ok: true });
      checks.push({ name: 'claude: marketplace has name', ok: Boolean(mdata.name) });
      checks.push({
        name: 'claude: marketplace lists plugins',
        ok: Array.isArray(mdata.plugins) && mdata.plugins.length > 0,
        detail: `${(mdata.plugins ?? []).length} plugins`,
      });
    } catch (e) {
      checks.push({ name: 'claude: marketplace.json valid JSON', ok: false, detail: e.message });
    }
  }

  // Plugin dirs = subdirectories (up to 2 levels deep, marketplace layouts
  // like ./plugins/<name>/) that contain .claude-plugin/plugin.json
  const pluginDirs = [];
  try {
    const entries = await readdir(root, { withFileTypes: true });
    for (const entry of entries) {
      if (!entry.isDirectory()) continue;
      const oneLevel = join(root, entry.name);
      if (await isFile(join(oneLevel, '.claude-plugin/plugin.json'))) {
        pluginDirs.push({ name: entry.name, dir: oneLevel });
        continue;
      }
      let subEntries = [];
      try {
        subEntries = await readdir(oneLevel, { withFileTypes: true });
      } catch { /* skip */ }
      for (const sub of subEntries) {
        if (!sub.isDirectory()) continue;
        const twoLevel = join(oneLevel, sub.name);
        if (await isFile(join(twoLevel, '.claude-plugin/plugin.json'))) {
          pluginDirs.push({ name: sub.name, dir: twoLevel });
        }
      }
    }
  } catch { /* root unreadable */ }

  for (const pd of pluginDirs) {
    const pjContent = await readFile(join(pd.dir, '.claude-plugin/plugin.json'), 'utf8').catch(() => null);
    if (pjContent === null) continue;
    try {
      const pdata = JSON.parse(pjContent);
      checks.push({ name: `claude: plugin ${pd.name} has name`, ok: Boolean(pdata.name) });
      const skillsDir = join(pd.dir, 'skills');
      const skillsFound = await walkForSkillMds(skillsDir, 1);
      checks.push({
        name: `claude: plugin ${pd.name} has skills/`,
        ok: skillsFound.length > 0,
        detail: `${skillsFound.length} skills`,
      });
    } catch (e) {
      checks.push({ name: `claude: plugin ${pd.name} plugin.json valid`, ok: false, detail: e.message });
    }
  }

  const claudeProjectSkills = await walkForSkillMds(join(root, '.claude/skills'), 2);
  const claudeLayoutPresent = mpContent !== null || pluginDirs.length > 0 || claudeProjectSkills.length > 0;
  if (claudeLayoutPresent) {
    checks.push({ name: 'claude: installable layout (marketplace or .claude/skills)', ok: true, detail: 'present; validated above' });
  } else {
    checks.push({
      name: 'claude: no broken .claude layout',
      ok: true,
      detail: 'no .claude-plugin/.claude dirs — Claude layout not claimed (ok for local/Hermes skills)',
    });
  }

  // --- Codex / OpenAI repo discovery ---
  // Codex CLI auto-scans .agents/skills upward from $CWD to the repo root
  // ("Where Codex loads local skills" — developers.openai.com/codex/skills);
  // .codex/skills is the legacy repo-scoped location. A repo with a valid
  // Agent Plugins manifest (plugin.json) is also Codex-installable — Codex
  // distributes skills via plugins. A bare skills/ repo without any of these
  // still works via `npx skills add -a codex` (skills.sh layout, above).
  const codexScoped = [];
  for (const cd of ['.agents/skills', '.codex/skills']) {
    codexScoped.push(...(await walkForSkillMds(join(root, cd), 2)));
  }
  const rootIsSkill = await hasSkillMd(root);
  const rootPlugin = await readFile(join(root, 'plugin.json'), 'utf8').catch(() => null);
  let pluginIsAgentPlugins = false;
  if (rootPlugin) {
    try {
      pluginIsAgentPlugins = JSON.parse(rootPlugin).$schema === AGENT_PLUGINS_SCHEMA;
    } catch { /* invalid JSON — the agentplugins section reports it */ }
  }
  const codexLayoutOk = rootIsSkill || codexScoped.length > 0 || pluginIsAgentPlugins;
  checks.push({
    name: 'codex: repo-scoped .agents/skills layout',
    ok: codexLayoutOk,
    detail: codexScoped.length
      ? `${codexScoped.length} skill(s) under .agents/skills / .codex/skills — Codex auto-loads these`
      : pluginIsAgentPlugins
        ? 'Agent Plugins manifest at root — Codex installs skills from plugins'
        : rootIsSkill
          ? 'single-skill dir: Codex loads a SKILL.md at the root it is run from'
          : 'no .agents/skills, .codex/skills, or plugin.json — Codex will not auto-load these skills (use npx skills add -a codex or package a plugin)',
  });

  // --- Agent Plugins 1.0.0 (agent-plugins.org, vendor-neutral spec) ---
  // A plugin dir contains plugin.json at its root. Check the repo root and
  // nested plugin dirs (up to 2 levels), like the Claude plugin scan above.
  const apPluginDirs = [];
  const SKIP_AP_DIRS = new Set(['.claude-plugin', '.git', 'node_modules', '.github', 'test', 'bin', 'src']);
  if (await isFile(join(root, 'plugin.json'))) apPluginDirs.push(root);
  for (const entry of await readdir(root, { withFileTypes: true }).catch(() => [])) {
    if (!entry.isDirectory() || SKIP_AP_DIRS.has(entry.name)) continue;
    if (await isFile(join(root, entry.name, 'plugin.json'))) {
      apPluginDirs.push(join(root, entry.name));
    } else {
      for (const sub of await readdir(join(root, entry.name), { withFileTypes: true }).catch(() => [])) {
        if (sub.isDirectory() && await isFile(join(root, entry.name, sub.name, 'plugin.json'))) {
          apPluginDirs.push(join(root, entry.name, sub.name));
        }
      }
    }
  }

  if (apPluginDirs.length === 0) {
    checks.push({
      name: 'agentplugins: no plugin.json manifest',
      ok: true,
      detail: 'not packaged as an Agent Plugin — spec claims not made (ok for plain skill repos)',
    });
  }

  for (const pd of apPluginDirs) {
    const label = pd === root ? 'agentplugins' : `agentplugins: ${relative(root, pd)}`;
    const pjPath = join(pd, 'plugin.json');
    let pjContent;
    try {
      pjContent = await readFile(pjPath, 'utf8');
    } catch {
      checks.push({ name: `${label}: manifest readable`, ok: false, detail: pjPath });
      continue;
    }
    let manifest;
    try {
      manifest = JSON.parse(pjContent);
      checks.push({ name: `${label}: manifest valid JSON`, ok: true });
    } catch (e) {
      checks.push({ name: `${label}: manifest valid JSON`, ok: false, detail: e.message });
      continue;
    }
    checks.push({
      name: `${label}: $schema declares Agent Plugins`,
      ok: manifest.$schema === AGENT_PLUGINS_SCHEMA,
      detail: manifest.$schema ?? '(missing)',
    });
    const pname = String(manifest.name ?? '');
    const nameOk = pname.length >= 1 && pname.length <= 64 &&
      /^(?!.*--)(?!.*\.\.)[a-z0-9][a-z0-9.-]*[a-z0-9]$/.test(pname);
    checks.push({
      name: `${label}: name format`,
      ok: nameOk,
      detail: "1-64 chars, lowercase alnum/hyphen/dot, no '--', no '..', alnum ends",
    });
    const unknown = Object.keys(manifest).filter((k) => !AGENT_PLUGINS_ALLOWED_FIELDS.has(k));
    checks.push({
      name: `${label}: no unknown top-level fields (closed schema)`,
      ok: unknown.length === 0,
      detail: unknown.slice(0, 3).join(', ') || 'all fields allowed',
    });
    if ('keywords' in manifest) {
      checks.push({ name: `${label}: keywords is array`, ok: Array.isArray(manifest.keywords) });
    }
    if ('author' in manifest && manifest.author !== null) {
      checks.push({ name: `${label}: author is object`, ok: typeof manifest.author === 'object' && !Array.isArray(manifest.author) });
    }
    // skills/ dir: immediate children with SKILL.md (Agent Plugins layout).
    // Missing skills/ is valid (MCP-only plugin); existing-as-file is not.
    const pluginSkills = await walkForSkillMds(join(pd, 'skills'), 1);
    const skillsDirPath = join(pd, 'skills');
    const skillsIsDir = await readdir(skillsDirPath, { withFileTypes: true }).then(() => true).catch(() => false);
    const skillsIsFile = skillsIsDir ? false : await isFile(skillsDirPath);
    checks.push({
      name: `${label}: skills/ layout`,
      ok: !skillsIsFile,
      detail: skillsIsDir
        ? `${pluginSkills.length} skill(s) in skills/ (immediate children)`
        : skillsIsFile
          ? 'skills/ exists but is not a directory (skills component invalid)'
          : 'no skills/ dir (valid — MCP-only plugin)',
    });
    // mcp.json: optional, must parse as JSON object
    const mcpPath = join(pd, 'mcp.json');
    const mcpContent = await readFile(mcpPath, 'utf8').catch(() => null);
    if (mcpContent !== null) {
      try {
        const mcp = JSON.parse(mcpContent);
        checks.push({ name: `${label}: mcp.json valid JSON`, ok: typeof mcp === 'object' && !Array.isArray(mcp) });
      } catch (e) {
        checks.push({ name: `${label}: mcp.json valid JSON`, ok: false, detail: e.message });
      }
    }
  }

  // --- Multi-tool compatibility (report-only) ---
  // Aggregates the repo-level install surfaces detected above into one view so a
  // skill author can see how many ecosystems a skill installs into at once. This
  // group is purely informational: it never fails a skill for having only one
  // route, because a single-route skill is a valid choice, not an error.
  const pkgContent = await readFile(join(root, 'package.json'), 'utf8').catch(() => null);
  let hasNpmCli = false;
  if (pkgContent) {
    try {
      const pkg = JSON.parse(pkgContent);
      hasNpmCli = Boolean(pkg && typeof pkg === 'object' && pkg.bin);
    } catch { /* invalid package.json — npm route not claimed */ }
  }
  const routes = [
    { route: 'skills.sh (npx skills add)', present: discovered.length > 0 },
    { route: 'Agent Plugins 1.0.0 (plugin.json)', present: apPluginDirs.length > 0 },
    { route: 'Claude marketplace (.claude-plugin)', present: mpContent !== null },
    { route: 'Claude .claude/skills', present: claudeProjectSkills.length > 0 },
    { route: 'Codex (.agents/.codex/skills or plugin)', present: codexLayoutOk },
    { route: 'npm CLI (package.json bin)', present: hasNpmCli },
  ];
  for (const { route, present } of routes) {
    checks.push({
      name: `multi-tool: ${route}`,
      ok: true,
      detail: present ? 'present' : 'not present',
    });
  }
  const surfaces = routes.filter((r) => r.present);
  checks.push({
    name: 'multi-tool: install surfaces',
    ok: true,
    detail: surfaces.length
      ? `${surfaces.length} install route(s): ${surfaces.map((s) => s.route.split(' ')[0]).join(', ')}`
      : 'none detected',
  });

  return annotateChecks(checks);
}

// Group checks by standard. Check names carry a standard keyword, so the
// mapping is structural, not guessed: agentplugins, openagent, claude,
// hermes, anthropic, spec. Anything else lands in General.
export function groupChecksByStandard(checks) {
  const KEYWORDS = [
    ['agentplugins', 'Agent Plugins 1.0.0'],
    ['openagent', 'OpenAgent skills.sh'],
    ['claude', 'Claude Code'],
    ['codex', 'Codex (OpenAI)'],
    ['multi-tool', 'Multi-tool compatibility'],
    ['hermes', 'Hermes in-repo'],
    ['anthropic', 'Anthropic best practices'],
    ['spec:', 'agentskills.io'],
  ];
  const groups = new Map();
  const labelFor = (name) => {
    for (const [kw, label] of KEYWORDS) {
      if (name.includes(kw)) return label;
    }
    return 'General';
  };
  for (const c of checks) {
    const label = labelFor(c.name);
    if (!groups.has(label)) {
      groups.set(label, { name: label, passed: 0, failed: 0, total: 0, ok: true, checks: [] });
    }
    const g = groups.get(label);
    g.total += 1;
    if (c.ok) g.passed += 1;
    else { g.failed += 1; g.ok = false; }
    g.checks.push(c);
  }
  return [...groups.values()];
}

// Canonical standard identifiers accepted by --standard / -s.
export const STANDARD_IDS = ['agentplugins', 'agentskills', 'anthropic', 'hermes', 'multi-tool', 'openagent', 'claude', 'codex'];

export const STANDARD_ALIASES = new Map([
  ['agentplugins', 'Agent Plugins 1.0.0'],
  ['agent-plugin', 'Agent Plugins 1.0.0'],
  ['agentplugin', 'Agent Plugins 1.0.0'],
  ['plugins', 'Agent Plugins 1.0.0'],
  ['agentskills', 'agentskills.io'],
  ['agentskills.io', 'agentskills.io'],
  ['spec', 'agentskills.io'],
  ['anthropic', 'Anthropic best practices'],
  ['anthropic best practices', 'Anthropic best practices'],
  ['hermes', 'Hermes in-repo'],
  ['hermes in-repo', 'Hermes in-repo'],
  ['openagent', 'OpenAgent skills.sh'],
  ['skills.sh', 'OpenAgent skills.sh'],
  ['claude', 'Claude Code'],
  ['claude-code', 'Claude Code'],
  ['claude code', 'Claude Code'],
  ['codex', 'Codex (OpenAI)'],
  ['codex-cli', 'Codex (OpenAI)'],
  ['openai', 'Codex (OpenAI)'],
  ['openai-codex', 'Codex (OpenAI)'],
  ['multi-tool', 'Multi-tool compatibility'],
  ['multitool', 'Multi-tool compatibility'],
  ['polyglot', 'Multi-tool compatibility'],
  ['tools', 'Multi-tool compatibility'],
]);

// Resolve a requested standard id/alias to its group label, or null if unknown.
export function resolveStandardLabel(id) {
  const label = STANDARD_ALIASES.get(String(id).toLowerCase());
  return label ?? null;
}

// Filter checks to the requested standards. General checks (skills found,
// structural) always run, so a filtered run is never meaningless. Returns
// { ok: false, unknown: [...] } when a requested standard is not recognised.
export function filterChecksByStandard(checks, requested) {
  const labels = new Set();
  const unknown = [];
  for (const id of requested) {
    const label = resolveStandardLabel(id);
    if (label === null) unknown.push(id);
    else labels.add(label);
  }
  if (unknown.length > 0) return { ok: false, unknown, checks: [] };
  if (labels.size === 0) return { ok: true, checks };
  const groups = groupChecksByStandard(checks);
  const kept = [];
  for (const g of groups) {
    if (g.name === 'General' || labels.has(g.name)) kept.push(...g.checks);
  }
  return { ok: true, checks: kept };
}

// CLI entry when run directly: `node validate.js <dir>` (library otherwise)
const isMain = process.argv[1] && import.meta.url === new URL(`file://${process.argv[1]}`).href;
if (isMain) {
  const dir = process.argv[2];
  if (!dir) {
    console.error('usage: node validate.js <dir>');
    process.exit(2);
  }
  const checks = await validate(dir);
  const failed = checks.filter((c) => !c.ok);
  console.log(`Validating: ${dir}`);
  for (const c of checks) {
    const mark = c.ok ? 'PASS' : 'FAIL';
    console.log(`  [${mark}] ${c.name}${c.detail ? `  (${c.detail})` : ''}`);
  }
  console.log(`\n${checks.length - failed.length}/${checks.length} checks passed`);
  process.exit(failed.length === 0 ? 0 : 1);
}
