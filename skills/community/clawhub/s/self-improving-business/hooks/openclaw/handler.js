/**
 * Business Self-Improvement Hook for OpenClaw
 *
 * Injects a reminder to evaluate business administration findings.
 * Fires on agent:bootstrap event.
 */

const REMINDER_CONTENT = `
## Business Self-Improvement Reminder

After completing tasks, evaluate if business administration findings should be captured:

**Log when:**
- missed SLA or delivery commitment appears -> \`.learnings/BUSINESS_ISSUES.md\` (decision_latency/process_breakdown)
- overdue approval delays execution -> \`.learnings/BUSINESS_ISSUES.md\` (decision_latency)
- RACI ownership conflict appears -> \`.learnings/BUSINESS_ISSUES.md\` (stakeholder_misalignment)
- KPI definition mismatch or unexplained variance -> \`.learnings/LEARNINGS.md\` (kpi_misalignment)
- vendor handoff failure or dependency block -> \`.learnings/BUSINESS_ISSUES.md\` (handoff_failure)
- policy missing or documentation drift is detected -> \`.learnings/LEARNINGS.md\` (policy_gap/documentation_drift)
- audit issue indicates control weakness -> \`.learnings/BUSINESS_ISSUES.md\` (compliance_oversight)

**Reminder-only safety:**
- this workflow does NOT execute approvals, spending, vendor commitments, payroll, or legal actions
- recommend explicit human approval for high-impact business decisions

**Promote proven patterns to:**
- process playbooks
- governance checklists
- KPI definition registry
- RACI matrix updates
- operating cadences
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
      path: 'BUSINESS_SELF_IMPROVEMENT_REMINDER.md',
      content: REMINDER_CONTENT,
      virtual: true,
    });
  }
};

module.exports = handler;
module.exports.default = handler;
