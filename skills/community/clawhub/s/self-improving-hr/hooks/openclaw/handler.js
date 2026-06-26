/**
 * Self-Improving HR Hook for OpenClaw
 *
 * Injects an HR-specific reminder to evaluate learnings during agent bootstrap.
 * Fires on agent:bootstrap event before workspace files are injected.
 * Emphasizes PII anonymization for all HR-related logging.
 */

const REMINDER_CONTENT = `
## HR Self-Improvement Reminder

After completing HR tasks, evaluate if any learnings should be captured:

**CRITICAL: NEVER log PII (names, SSNs, salaries, medical info). Always anonymize.**

**Log HR process issues when:**
- Compliance audit finding discovered → \`.learnings/HR_PROCESS_ISSUES.md\` (compliance_risk)
- Benefits enrollment error occurred → \`.learnings/HR_PROCESS_ISSUES.md\` (process_inefficiency)
- I-9 verification issue found → \`.learnings/HR_PROCESS_ISSUES.md\` (compliance_risk)
- Policy violation or regulatory exposure identified → \`.learnings/HR_PROCESS_ISSUES.md\`

**Log learnings when:**
- Policy gap discovered (missing or outdated) → \`.learnings/LEARNINGS.md\` (policy_gap)
- Candidate drops off at pipeline stage → \`.learnings/LEARNINGS.md\` (candidate_experience)
- New hire leaves within 90 days → \`.learnings/LEARNINGS.md\` (retention_signal)
- Exit interview reveals recurring theme → \`.learnings/LEARNINGS.md\` (retention_signal)
- Onboarding step causing delays → \`.learnings/LEARNINGS.md\` (onboarding_friction)
- Process taking too long or failing → \`.learnings/LEARNINGS.md\` (process_inefficiency)

**Log feature requests when:**
- HR automation or tooling needed → \`.learnings/FEATURE_REQUESTS.md\`

**Promote when pattern is proven (3+ occurrences):**
- Onboarding patterns → onboarding checklists
- Compliance findings → compliance calendars
- Interview insights → interview scorecards
- Policy gaps → policy documents

Specify area tag and jurisdiction. Anonymize all examples.
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
      path: 'HR_SELF_IMPROVEMENT_REMINDER.md',
      content: REMINDER_CONTENT,
      virtual: true,
    });
  }
};

module.exports = handler;
module.exports.default = handler;
