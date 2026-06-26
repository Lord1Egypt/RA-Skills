const { spawnSync } = require('child_process');
const path = require('path');

const {
  REPO_SLUG,
  packageRoot,
  claudeConfigDir,
  codexConfigDir,
} = require('./common');
const { installClaudeCode, installCodex } = require('./install-hooks');
const { installAsClaudePlugin } = require('./install-plugin');
const { installCursorSkill, installWindsurfRule } = require('./install-rule-file');

const AGENT_ALIASES = {
  'claude-code': 'claude',
};

function normalizeAgentIds(ids) {
  return ids.map((id) => AGENT_ALIASES[id] || id);
}

const CHOICES = [
  { value: 'opencode', label: 'OpenCode (npx skills)' },
  { value: 'openclaw', label: 'OpenClaw (npx skills)' },
  { value: 'cursor', label: 'Cursor (global skill ~/.cursor/skills/)' },
  { value: 'antigravity', label: 'Antigravity (npx skills)' },
  { value: 'claude', label: 'Claude Code (native plugin + marketplace)' },
  { value: 'codex', label: 'Codex (hooks in ~/.codex)' },
  { value: 'windsurf', label: 'Windsurf (npx skills)' },
  { value: 'cline', label: 'Cline (npx skills)' },
  { value: 'copilot', label: 'GitHub Copilot (npx skills)' },
];

function parseAgentsFlag(argv) {
  const i = argv.indexOf('--agents');
  if (i === -1 || !argv[i + 1]) return null;
  return normalizeAgentIds(
    argv[i + 1]
      .split(',')
      .map((s) => s.trim().toLowerCase())
      .filter(Boolean)
  );
}

function npxSkillsAdd(npxFlag) {
  const r = spawnSync(
    process.platform === 'win32' ? 'npx.cmd' : 'npx',
    ['skills', 'add', REPO_SLUG, '-a', npxFlag],
    { stdio: 'inherit', shell: process.platform === 'win32' }
  );
  return r.status === 0;
}

function printInstallReport(report) {
  if (!report) return;
  console.log(`${report.label}:`);
  for (const line of report.lines) {
    console.log(`  ${line}`);
  }
}

const INSTALLERS = {
  opencode: () => {
    npxSkillsAdd('opencode');
    return null;
  },
  openclaw: () => {
    npxSkillsAdd('openclaw');
    return null;
  },
  cursor: (pkg) => {
    const skillPath = installCursorSkill(pkg);
    return {
      label: 'Cursor',
      lines: [
        `global skill at ${skillPath}`,
        'Invoke in Agent: @fasterizy or / menu → fasterizy (see SKILL.md section Cursor).',
      ],
    };
  },
  antigravity: () => {
    npxSkillsAdd('antigravity');
    return null;
  },
  claude: (pkg) => {
    const cd = claudeConfigDir();
    try {
      const r = installAsClaudePlugin();
      const lines = [
        `marketplace: ${r.marketplacePath}${r.local ? ' (local repo)' : ''}`,
        `plugin cache: ${r.installPath}`,
        `version: ${r.shortSha}`,
        'enabledPlugins[fasterizy@fasterizy] = true in settings.json',
      ];
      if (r.strippedHooksFromSettings) {
        lines.push('Stripped old fasterizy hook entries from settings.json.');
      }
      if (r.removedHookFiles && r.removedHookFiles.length) {
        lines.push(`Removed ${r.removedHookFiles.length} legacy hook file(s) from ${path.join(cd, 'hooks')}.`);
      }
      lines.push('Restart Claude Code; fasterizy will load via the plugin.');
      return { label: 'Claude Code', lines };
    } catch (e) {
      console.warn(
        'fasterizy: native plugin install failed, falling back to hooks mode:',
        e.message || e
      );
      const r = installClaudeCode(pkg, { repoSlug: REPO_SLUG });
      return {
        label: 'Claude Code (fallback: hooks)',
        lines: [
          `hooks installed at ${path.join(cd, 'hooks')}`,
          ...(r.backup ? [`backup: ${r.backup}`] : []),
          'Marketplace registered (settings.json extraKnownMarketplaces.fasterizy).',
          'fasterizy is active via hooks — restart Claude Code to load.',
          'Retry as native plugin later: npx fasterizy promote-to-plugin',
        ],
      };
    }
  },
  codex: (pkg) => {
    const r = installCodex(pkg);
    const cx = codexConfigDir();
    return {
      label: 'Codex',
      lines: [
        `hooks installed at ${path.join(cx, 'hooks')}, hooks.json patched`,
        ...(r.backup ? [`backup: ${r.backup}`] : []),
      ],
    };
  },
  windsurf: (pkg) => {
    const target = installWindsurfRule(pkg);
    return {
      label: 'Windsurf',
      lines: [
        `rule installed at ${target}`,
        'fasterizy is always-on in this project (trimmed stub, ~500 tokens/turn).',
        'Full skill available on-demand via the native `fasterizy` skill or repo SKILL.md.',
      ],
    };
  },
  cline: () => {
    npxSkillsAdd('cline');
    return null;
  },
  copilot: () => {
    npxSkillsAdd('github-copilot');
    return null;
  },
};

module.exports = async function install(argv) {
  const pkg = packageRoot();
  let selected = parseAgentsFlag(argv);

  if (!selected || selected.length === 0) {
    const { checkbox } = await import('@inquirer/prompts');
    selected = normalizeAgentIds(
      await checkbox({
        message: 'Select where to install fasterizy',
        choices: CHOICES.map((c) => ({ name: c.label, value: c.value })),
        required: true,
      })
    );
  }

  console.log('');

  for (const id of selected) {
    try {
      const handler = INSTALLERS[id];
      if (!handler) {
        console.warn('Unknown agent:', id);
        continue;
      }
      printInstallReport(handler(pkg));
    } catch (e) {
      console.error('Error installing', id + ':', e.message || e);
    }
  }

  console.log('');
  console.log('Restart Claude Code / Codex after hook changes.');
};
