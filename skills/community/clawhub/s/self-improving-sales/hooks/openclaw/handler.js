/**
 * Self-Improving Sales Hook for OpenClaw
 *
 * Injects a sales-specific reminder to evaluate learnings during agent bootstrap.
 * Fires on agent:bootstrap event before workspace files are injected.
 */

const REMINDER_CONTENT = `
## Sales Self-Improvement Reminder

After completing sales tasks, evaluate if any learnings should be captured:

**Log deal issues when:**
- Deal stuck in same stage >30 days → \`.learnings/DEAL_ISSUES.md\` (pipeline_leak)
- Pricing mistake or unapproved discount → \`.learnings/DEAL_ISSUES.md\` (pricing_error)
- Forecast miss >20% on committed deal → \`.learnings/DEAL_ISSUES.md\` (forecast_miss)
- Deal lost post-mortem reveals process gap → \`.learnings/DEAL_ISSUES.md\`

**Log learnings when:**
- Objection you couldn't handle → \`.learnings/LEARNINGS.md\` (objection_pattern)
- Lost deal to competitor → \`.learnings/LEARNINGS.md\` (competitor_shift)
- Deal velocity dropping in a segment → \`.learnings/LEARNINGS.md\` (deal_velocity_drop)
- Pipeline leak pattern at specific stage → \`.learnings/LEARNINGS.md\` (pipeline_leak)

**Log feature requests when:**
- Sales tool or CRM automation needed → \`.learnings/FEATURE_REQUESTS.md\`

**Promote when pattern is proven (3+ deals):**
- Objection patterns → battle cards or objection handling scripts
- Competitor intelligence → competitive battle cards
- Pricing insights → pricing playbooks
- Qualification gaps → MEDDIC/BANT framework updates

Include deal context (anonymized), exact objection wording, and area tag.
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
      path: 'SALES_SELF_IMPROVEMENT_REMINDER.md',
      content: REMINDER_CONTENT,
      virtual: true,
    });
  }
};

module.exports = handler;
module.exports.default = handler;
