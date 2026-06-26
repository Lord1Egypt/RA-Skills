const path = require('path');
const { ensureDir, exists, readText, writeText } = require('./_common');

const START = '<!-- AI_WORKLOG_RULE_START -->';
const END = '<!-- AI_WORKLOG_RULE_END -->';

function buildManagedBlock({ skillDir, agentName, reportsDir }) {
  const appendScript = path.join(skillDir, 'scripts', 'append_ai_log.js');
  return [
    '## AI Work Log Integration',
    '',
    START,
    `每完成一个独立工作单元，立刻追加今日 AI work log：`,
    '',
    '```bash',
    `node ${appendScript} \\`,
    `  --agent ${agentName} \\`,
    `  --reports-dir "${reportsDir}" \\`,
    '  --task "一句话描述本次完成的工作" \\',
    '  --tokens 0',
    '```',
    '',
    '规则：',
    '- append-only',
    '- 每完成一个明确工作单元就写一行',
    '- `task` 必须是一句话',
    '- `tokens` 写总 token；拿不到就写 `0`',
    '- 不要直接改 `todo/NOW.md`',
    END,
    '',
  ].join('\n');
}

function upsertManagedBlock(original, block) {
  if (original.includes(START) && original.includes(END)) {
    const pattern = new RegExp(`## AI Work Log Integration\\n\\n${START}[\\s\\S]*?${END}`, 'm');
    if (pattern.test(original)) {
      return original.replace(pattern, block.trimEnd());
    }

    const markerPattern = new RegExp(`${START}[\\s\\S]*?${END}`, 'm');
    return original.replace(markerPattern, block.trimEnd());
  }

  const trimmed = original.replace(/\s*$/, '');
  return `${trimmed}\n\n${block.trimEnd()}\n`;
}

function installAgentLogRules({ config, paths }) {
  const results = [];
  const skillDir = paths.skillDir;

  for (const agent of config.agents || []) {
    if (!agent || agent.enabled === false || !agent.name || !agent.reportsDir) {
      continue;
    }

    const agentsFilePath = agent.agentsFilePath;
    if (!agentsFilePath) {
      results.push({ agent: agent.name, status: 'skipped', reason: 'missing agentsFilePath' });
      continue;
    }

    if (!exists(agentsFilePath)) {
      results.push({ agent: agent.name, status: 'skipped', reason: 'AGENTS.md not found', path: agentsFilePath });
      continue;
    }

    const current = readText(agentsFilePath);
    const block = buildManagedBlock({
      skillDir,
      agentName: agent.name,
      reportsDir: agent.reportsDir,
    });
    const next = upsertManagedBlock(current, block);
    if (next !== current) {
      ensureDir(path.dirname(agentsFilePath));
      writeText(agentsFilePath, next);
      results.push({ agent: agent.name, status: 'updated', path: agentsFilePath });
    } else {
      results.push({ agent: agent.name, status: 'unchanged', path: agentsFilePath });
    }
  }

  return results;
}

module.exports = {
  installAgentLogRules,
};
