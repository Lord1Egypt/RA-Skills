/**
 * Self-Improving Negotiation Hook for OpenClaw
 *
 * Injects a negotiation-specific reminder during agent bootstrap.
 * Reminder-only: does not approve or execute agreement actions.
 */

import type { HookHandler } from 'openclaw/hooks';

const REMINDER_CONTENT = `## Negotiation Self-Improvement Reminder

After completing negotiation tasks, evaluate if learnings should be captured:

**Log negotiation issues when:**
- Deadlock persists across rounds -> \`.learnings/NEGOTIATION_ISSUES.md\` (escalation_misalignment/framing_miss)
- Concession made without reciprocity -> \`.learnings/NEGOTIATION_ISSUES.md\` (concession_leak)
- BATNA not defined or not actionable -> \`.learnings/NEGOTIATION_ISSUES.md\` (batna_weakness)
- Approval missing for high-impact concession -> \`.learnings/NEGOTIATION_ISSUES.md\` (escalation_misalignment)
- Term ambiguity or unresolved redline remains -> \`.learnings/NEGOTIATION_ISSUES.md\` (agreement_risk)

**Log learnings when:**
- Anchor strategy failed or drifted -> \`.learnings/LEARNINGS.md\` (anchor_error)
- Value framing improved acceptance -> \`.learnings/LEARNINGS.md\` (value_articulation_gap/framing_miss)
- Objection handling pattern recurs -> \`.learnings/LEARNINGS.md\` (objection_handling_gap)

**Log feature requests when:**
- Negotiation workflow/tooling support is needed -> \`.learnings/FEATURE_REQUESTS.md\`

If pattern repeats 3+ times, promote to playbook, objection library, guardrail, BATNA checklist, or review template.

Safety: reminder-only. Never auto-accept terms, commit pricing, execute approvals, or finalize agreements.
`;

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

  // Skip subagents to reduce duplicated reminder noise.
  const sessionKey = event.sessionKey || '';
  if (sessionKey.includes(':subagent:')) {
    return;
  }

  if (Array.isArray(event.context.bootstrapFiles)) {
    event.context.bootstrapFiles.push({
      path: 'NEGOTIATION_SELF_IMPROVEMENT_REMINDER.md',
      content: REMINDER_CONTENT,
      virtual: true,
    });
  }
};

export default handler;
