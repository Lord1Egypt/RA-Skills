/**
 * Security Self-Improvement Hook for OpenClaw
 *
 * Injects a reminder to evaluate security findings during agent bootstrap.
 * Fires on agent:bootstrap event before workspace files are injected.
 */

import type { HookHandler } from 'openclaw/hooks';

const REMINDER_CONTENT = `## Security Self-Improvement Reminder

After completing tasks, evaluate if any security findings should be captured:

**Log when:**
- Vulnerability discovered (CVE, dependency, code) → \`.learnings/SECURITY_INCIDENTS.md\`
- Misconfiguration found (permissions, policies, configs) → \`.learnings/LEARNINGS.md\` (misconfiguration)
- Access control issue (unauthorized access, broken auth) → \`.learnings/SECURITY_INCIDENTS.md\`
- Compliance gap identified (audit finding, missing control) → \`.learnings/LEARNINGS.md\` (compliance_gap)
- Secrets in output or logs → \`.learnings/SECURITY_INCIDENTS.md\` — **REDACT IMMEDIATELY**
- Threat intelligence gathered → \`.learnings/LEARNINGS.md\` (threat_intelligence)

**CRITICAL: NEVER log actual secrets, credentials, tokens, private keys, or PII.**
Always use REDACTED_* placeholders. Describe the type and location, not the content.

**Promote when pattern is proven:**
- Security principles → \`SOUL.md\`
- Incident response workflows → \`AGENTS.md\`
- Security tool hardening → \`TOOLS.md\`
- Hardening checklist items → \`HARDENING.md\`
- Incident response playbooks → \`PLAYBOOKS.md\`

Keep entries actionable: what was found, impact, remediation, and verification.`;

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
      path: 'SECURITY_SELF_IMPROVEMENT_REMINDER.md',
      content: REMINDER_CONTENT,
      virtual: true,
    });
  }
};

export default handler;
