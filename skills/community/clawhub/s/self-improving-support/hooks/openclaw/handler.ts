/**
 * Self-Improving Support Hook for OpenClaw
 *
 * Injects a support-specific reminder to evaluate learnings during agent bootstrap.
 * Fires on agent:bootstrap event before workspace files are injected.
 */

import type { HookHandler } from 'openclaw/hooks';

const REMINDER_CONTENT = `## Support Self-Improvement Reminder

After completing support tasks, evaluate if any learnings should be captured:

**Log ticket issues when:**
- Resolution took longer than SLA target → \`.learnings/TICKET_ISSUES.md\` (sla_breach)
- Initial diagnosis was incorrect → \`.learnings/TICKET_ISSUES.md\` (misdiagnosis)
- Customer reopened a previously closed ticket → \`.learnings/TICKET_ISSUES.md\` (ticket_reopen)
- Same issue reported by multiple customers → \`.learnings/TICKET_ISSUES.md\` (repeat_ticket)

**Log learnings when:**
- Knowledge base search returned no results → \`.learnings/LEARNINGS.md\` (knowledge_gap)
- Escalation went to wrong team or was delayed → \`.learnings/LEARNINGS.md\` (escalation_gap)
- Customer expressed frustration or cancellation intent → \`.learnings/LEARNINGS.md\` (customer_churn_signal)
- Resolution was delayed by process or tooling → \`.learnings/LEARNINGS.md\` (resolution_delay)

**Log feature requests when:**
- Support tool or automation needed → \`.learnings/FEATURE_REQUESTS.md\`

**Promote when pattern is proven (3+ occurrences):**
- Diagnostic patterns → KB articles
- Triage workflows → troubleshooting trees
- Escalation insights → escalation matrices
- Common resolutions → canned response templates

Anonymise customer data. Use ticket IDs, not names.`;

const handler: HookHandler = async (event) => {
  if (!event || typeof event !== 'object') {
    return;
  }

  if (event.type !== 'agent' || event.action !== 'bootstrap') {
    return;
  }

  if (!event.context || typeof event.context !== 'object') {
    return;
  }

  const sessionKey = event.sessionKey || '';
  if (sessionKey.includes(':subagent:')) {
    return;
  }

  if (Array.isArray(event.context.bootstrapFiles)) {
    event.context.bootstrapFiles.push({
      path: 'SUPPORT_SELF_IMPROVEMENT_REMINDER.md',
      content: REMINDER_CONTENT,
      virtual: true,
    });
  }
};

export default handler;
