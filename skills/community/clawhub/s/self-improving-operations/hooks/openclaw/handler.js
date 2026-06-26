/**
 * Self-Improving Operations Hook for OpenClaw
 *
 * Injects an operations-specific reminder to evaluate learnings during agent bootstrap.
 * Fires on agent:bootstrap event before workspace files are injected.
 */

const REMINDER_CONTENT = `
## Operations Self-Improvement Reminder

After completing operations tasks, evaluate if any learnings should be captured:

**Log operations issues when:**
- Incident repeats within 30 days → \`.learnings/OPERATIONS_ISSUES.md\` (incident_pattern)
- MTTR exceeds target (>4h P1, >8h P2) → \`.learnings/OPERATIONS_ISSUES.md\`
- SLO/SLA breach detected → \`.learnings/OPERATIONS_ISSUES.md\` (sla_breach)
- Capacity threshold exceeded (>85% CPU/disk) → \`.learnings/OPERATIONS_ISSUES.md\` (capacity_issue)
- Deployment rollback required → \`.learnings/OPERATIONS_ISSUES.md\`

**Log learnings when:**
- Process bottleneck slowing delivery → \`.learnings/LEARNINGS.md\` (process_bottleneck)
- Manual step in automated pipeline → \`.learnings/LEARNINGS.md\` (automation_gap)
- Alert fatigue (>50 alerts/day same monitor) → \`.learnings/LEARNINGS.md\` (monitoring)
- Change failure rate >15% → \`.learnings/LEARNINGS.md\` (change_management)
- Toil exceeding 50% of on-call time → \`.learnings/LEARNINGS.md\` (toil_accumulation)

**Log feature requests when:**
- Operations tool or automation needed → \`.learnings/FEATURE_REQUESTS.md\`

**Promote when pattern is proven (3+ occurrences):**
- Incident response steps → runbooks
- Root cause findings → incident postmortems
- Automation candidates → automation backlog
- Resource projections → capacity models
- Reliability targets → SLO definitions

Include timeline, impact metrics, and DORA metrics context. Never log secrets or PII.
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
      path: 'OPERATIONS_SELF_IMPROVEMENT_REMINDER.md',
      content: REMINDER_CONTENT,
      virtual: true,
    });
  }
};

module.exports = handler;
module.exports.default = handler;
