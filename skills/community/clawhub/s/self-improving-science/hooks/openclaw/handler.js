/**
 * Self-Improving Science Hook for OpenClaw
 *
 * Injects a reminder to evaluate experiment and methodology learnings
 * during agent bootstrap. Fires on agent:bootstrap event before
 * workspace files are injected.
 */

const REMINDER_CONTENT = `
## Self-Improving Science Reminder

After completing tasks, evaluate if any research learnings should be captured:

**Log when:**
- Data quality issue found → \`.learnings/EXPERIMENT_ISSUES.md\`
- Methodology flaw discovered → \`.learnings/LEARNINGS.md\` with \`methodology_flaw\`
- Statistical error detected → \`.learnings/LEARNINGS.md\` with \`statistical_error\`
- Model fails to reproduce → \`.learnings/EXPERIMENT_ISSUES.md\` with \`reproducibility_issue\`
- Hypothesis needs revision → \`.learnings/LEARNINGS.md\` with \`hypothesis_revision\`
- User wants missing ML tool → \`.learnings/FEATURE_REQUESTS.md\`

**Promote when pattern is proven:**
- Experiment design patterns → Experiment Checklist
- Data handling rules → Data Governance Docs
- Model limitations → Model Card
- Pipeline best practices → \`AGENTS.md\`
- ML framework gotchas → \`TOOLS.md\`

Keep entries specific: include metrics, sample sizes, seeds, and library versions.
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
      path: 'SELF_IMPROVING_SCIENCE_REMINDER.md',
      content: REMINDER_CONTENT,
      virtual: true,
    });
  }
};

module.exports = handler;
module.exports.default = handler;
