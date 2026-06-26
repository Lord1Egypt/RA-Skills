/**
 * Self-Improving Engineering Hook for OpenClaw
 * 
 * Injects an engineering-focused reminder to evaluate learnings during agent bootstrap.
 * Fires on agent:bootstrap event before workspace files are injected.
 */

const REMINDER_CONTENT = `
## Engineering Self-Improvement Reminder

After completing tasks, evaluate if engineering knowledge should be captured:

**Log when:**
- Build or deploy failure encountered → \`.learnings/ENGINEERING_ISSUES.md\`
- Architecture violation discovered → \`.learnings/LEARNINGS.md\` (category: architecture_debt)
- Test gap or flaky test identified → \`.learnings/LEARNINGS.md\` (category: testing_gap)
- Performance regression detected → \`.learnings/ENGINEERING_ISSUES.md\`
- Dependency vulnerability found → \`.learnings/ENGINEERING_ISSUES.md\`
- Design flaw surfaces during review → \`.learnings/LEARNINGS.md\` (category: design_flaw)

**Promote when pattern is proven:**
- Design patterns & principles → \`SOUL.md\`
- CI/CD workflows & deploy patterns → \`AGENTS.md\`
- Build tool & infra gotchas → \`TOOLS.md\`

Keep entries specific: date, component, what broke, root cause, fix applied.
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
      path: 'ENGINEERING_IMPROVEMENT_REMINDER.md',
      content: REMINDER_CONTENT,
      virtual: true,
    });
  }
};

module.exports = handler;
module.exports.default = handler;
