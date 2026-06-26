/**
 * Self-Improving Meta Hook for OpenClaw
 *
 * Injects a meta-specific reminder to evaluate infrastructure learnings during agent bootstrap.
 * Fires on agent:bootstrap event before workspace files are injected.
 */

const REMINDER_CONTENT = `
## Meta Self-Improvement Reminder

After completing tasks, evaluate if any agent infrastructure learnings should be captured:

**Log learnings when:**
- Agent misinterprets a prompt file instruction → \`.learnings/LEARNINGS.md\` (instruction_ambiguity)
- Two rules contradict each other across files → \`.learnings/LEARNINGS.md\` (rule_conflict)
- Context window feels cramped or truncated → \`.learnings/LEARNINGS.md\` (context_bloat)
- Memory entry is stale or causing wrong behavior → \`.learnings/LEARNINGS.md\` (prompt_drift)
- Skill template is missing a section → \`.learnings/LEARNINGS.md\` (skill_gap)

**Log meta issues when:**
- Hook fails or produces no output → \`.learnings/META_ISSUES.md\`
- Skill doesn't activate when expected → \`.learnings/META_ISSUES.md\`
- Prompt file has malformed frontmatter → \`.learnings/META_ISSUES.md\`
- Extension API breaks or behaves unexpectedly → \`.learnings/META_ISSUES.md\`

**Log feature requests when:**
- New infrastructure capability needed → \`.learnings/FEATURE_REQUESTS.md\`
- Skill authoring workflow improvement → \`.learnings/FEATURE_REQUESTS.md\`
- Hook development tooling gap → \`.learnings/FEATURE_REQUESTS.md\`

**Promote when pattern is proven:**
- Instruction fixes → rewrite directly in AGENTS.md / SOUL.md / TOOLS.md
- Behavior patterns → SOUL.md
- Workflow improvements → AGENTS.md
- Tool integration fixes → TOOLS.md
- Memory management patterns → MEMORY.md
- Skill improvements → update the affected SKILL.md

Meta-learnings modify the infrastructure all other skills depend on. Apply fixes directly.
`.trim();

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
