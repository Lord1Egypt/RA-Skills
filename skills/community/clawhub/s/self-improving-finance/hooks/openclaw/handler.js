/**
 * Self-Improving Finance Hook for OpenClaw
 *
 * Injects a finance-specific reminder to evaluate learnings during agent bootstrap.
 * Fires on agent:bootstrap event before workspace files are injected.
 *
 * IMPORTANT: This hook emphasizes data anonymization. Never log real account numbers,
 * bank details, specific financial figures for real entities, or audit findings
 * with client names.
 */

const REMINDER_CONTENT = `
## Finance Self-Improvement Reminder

After completing finance tasks, evaluate if any learnings should be captured:

**CRITICAL: Always anonymize financial data. Never log real account numbers, bank details,
specific figures for real entities, or audit findings with client names.**

**Log finance issues when:**
- Reconciliation break identified → \`.learnings/FINANCE_ISSUES.md\` [FIN-YYYYMMDD-XXX]
- SOX control test failure → \`.learnings/FINANCE_ISSUES.md\` (control_test trigger)
- Budget vs. actual variance >10% → \`.learnings/FINANCE_ISSUES.md\` (variance_analysis)
- Close task past deadline → \`.learnings/FINANCE_ISSUES.md\` (close_review trigger)
- Intercompany imbalance → \`.learnings/FINANCE_ISSUES.md\` (reconciliation trigger)
- Unusual journal entry flagged → \`.learnings/FINANCE_ISSUES.md\` (audit trigger)
- AR aging past 90 days → \`.learnings/FINANCE_ISSUES.md\` (aging_review trigger)

**Log learnings when:**
- Control weakness discovered → \`.learnings/LEARNINGS.md\` (control_weakness)
- Regulatory gap found → \`.learnings/LEARNINGS.md\` (regulatory_gap)
- Reconciliation error pattern → \`.learnings/LEARNINGS.md\` (reconciliation_error)
- Forecast methodology improvement → \`.learnings/LEARNINGS.md\` (forecast_variance)
- Valuation model error → \`.learnings/LEARNINGS.md\` (valuation_error)
- Cash flow anomaly detected → \`.learnings/LEARNINGS.md\` (cash_flow_anomaly)

**Log feature requests when:**
- Finance tool or automation needed → \`.learnings/FEATURE_REQUESTS.md\`

**Promote when pattern is proven (3+ occurrences across periods/entities):**
- Close procedures → close checklists
- Reconciliation patterns → reconciliation procedures
- Control gaps → control matrices
- Tax compliance → tax calendars
- Forecast improvements → forecast models
- Audit findings → audit response templates
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
      path: 'FINANCE_SELF_IMPROVEMENT_REMINDER.md',
      content: REMINDER_CONTENT,
      virtual: true,
    });
  }
};

module.exports = handler;
module.exports.default = handler;
