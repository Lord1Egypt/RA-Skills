/**
 * Self-Improving Analytics Hook for OpenClaw
 *
 * Injects an analytics-specific reminder to evaluate learnings during agent bootstrap.
 * Fires on agent:bootstrap event before workspace files are injected.
 */

const REMINDER_CONTENT = `
## Analytics Self-Improvement Reminder

After completing analytics tasks, evaluate if any learnings should be captured:

**Log data issues when:**
- ETL/ELT pipeline failed or produced errors → \`.learnings/DATA_ISSUES.md\`
- Data freshness SLA breached (>24h stale) → \`.learnings/DATA_ISSUES.md\`
- Metric value anomaly (>3σ from norm) → \`.learnings/DATA_ISSUES.md\`
- NULL rate spike in key column → \`.learnings/DATA_ISSUES.md\`
- Schema change broke downstream → \`.learnings/DATA_ISSUES.md\`
- Dashboard rendering timeout or error → \`.learnings/DATA_ISSUES.md\`

**Log learnings when:**
- Conflicting metric definitions across teams → \`.learnings/LEARNINGS.md\` (definition_mismatch)
- Visualization misleads due to axis, scale, or aggregation → \`.learnings/LEARNINGS.md\` (visualization_mislead)
- Metric drift discovered (silent change in calculation) → \`.learnings/LEARNINGS.md\` (metric_drift)
- Data quality pattern found → \`.learnings/LEARNINGS.md\` (data_quality)
- Freshness monitoring insight → \`.learnings/LEARNINGS.md\` (freshness_issue)

**Log feature requests when:**
- Analytics tool or automation needed → \`.learnings/FEATURE_REQUESTS.md\`

**Promote when pattern is proven (3+ occurrences):**
- Metric definitions → data dictionary
- Pipeline failure patterns → pipeline runbooks
- Visualization standards → dashboard style guide
- Data quality rules → data quality SLAs

Include SQL snippets, affected tables/columns, and area tag.
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
      path: 'ANALYTICS_SELF_IMPROVEMENT_REMINDER.md',
      content: REMINDER_CONTENT,
      virtual: true,
    });
  }
};

module.exports = handler;
module.exports.default = handler;
