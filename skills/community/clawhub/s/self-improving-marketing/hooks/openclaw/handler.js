/**
 * Self-Improving Marketing Hook for OpenClaw
 *
 * Injects a marketing-specific reminder to evaluate learnings during agent bootstrap.
 * Fires on agent:bootstrap event before workspace files are injected.
 */

const REMINDER_CONTENT = `
## Marketing Self-Improvement Reminder

After completing marketing tasks, evaluate if any learnings should be captured:

**Log campaign issues when:**
- CTR dropped >20% from baseline → \`.learnings/CAMPAIGN_ISSUES.md\`
- Conversion rate declined >15% → \`.learnings/CAMPAIGN_ISSUES.md\`
- Email bounce rate exceeded 5% → \`.learnings/CAMPAIGN_ISSUES.md\`
- Campaign CPL exceeded benchmark by >50% → \`.learnings/CAMPAIGN_ISSUES.md\`

**Log learnings when:**
- Messaging missed the target segment → \`.learnings/LEARNINGS.md\` (messaging_miss)
- Channel underperformed benchmarks → \`.learnings/LEARNINGS.md\` (channel_underperformance)
- Audience behavior or demographics shifted → \`.learnings/LEARNINGS.md\` (audience_drift)
- Brand guideline violation discovered → \`.learnings/LEARNINGS.md\` (brand_inconsistency)
- UTM parameters or attribution broken → \`.learnings/LEARNINGS.md\` (attribution_gap)
- Content lost traffic or ranking → \`.learnings/LEARNINGS.md\` (content_decay)

**Log feature requests when:**
- Marketing tool or automation needed → \`.learnings/FEATURE_REQUESTS.md\`

**Promote when pattern is proven (3+ occurrences):**
- Messaging patterns → brand guidelines
- Channel insights → channel playbooks
- Audience shifts → updated personas
- Attribution fixes → attribution model standards

Include before/after metrics. Specify channel and area tag.
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
      path: 'MARKETING_SELF_IMPROVEMENT_REMINDER.md',
      content: REMINDER_CONTENT,
      virtual: true,
    });
  }
};

module.exports = handler;
module.exports.default = handler;
