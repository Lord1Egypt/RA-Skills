/**
 * Self-Improving Meta Hook for OpenClaw
 *
 * Optional session-start reminder. Log-only. Does not edit files or call the network.
 * Enable only if you want this reminder in main sessions. Not matcher-gated.
 */

const REMINDER_CONTENT = `## Meta Self-Improvement Reminder (log-only)

This reminder does not authorize edits. Do not change AGENTS.md, SOUL.md, TOOLS.md, MEMORY.md, hooks, rules, or skills unless the user explicitly asked in this session.

After tasks, if infrastructure issues appeared, log a short redacted note:

**Learnings** (\`.learnings/LEARNINGS.md\`):
- Misread prompt-file instruction → \`instruction_ambiguity\`
- Contradictory rules across files → \`rule_conflict\`
- Truncated or bloated context → \`context_bloat\`
- Stale memory causing wrong behavior → \`prompt_drift\`

**Meta issues** (\`.learnings/META_ISSUES.md\`):
- Hook produced no output or failed
- Skill did not activate when expected
- Malformed skill frontmatter

**Feature requests** (\`.learnings/FEATURE_REQUESTS.md\`):
- Missing infrastructure capability

Do not apply patches, extract skills, or send cross-session messages from this reminder.`.trim();

const handler = async (event) => {
  if (!event || typeof event !== 'object') {
    return;
  }

  if (event.type !== 'agent' || event.action !== 'bootstrap') {
    return;
  }

  if (!event.context || typeof event.context !== 'object') {
    return;
  }

  const sessionKey = event.sessionKey || '';
  if (sessionKey.includes(':subagent:')) {
    return;
  }

  if (Array.isArray(event.context.bootstrapFiles)) {
    event.context.bootstrapFiles.push({
      path: 'META_SELF_IMPROVEMENT_REMINDER.md',
      content: REMINDER_CONTENT,
      virtual: true,
    });
  }
};

module.exports = handler;
module.exports.default = handler;
