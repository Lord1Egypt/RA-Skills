/**
 * Conversation Self-Improvement Hook for OpenClaw
 * 
 * Injects a reminder to evaluate dialogue learnings during agent bootstrap.
 * Fires on agent:bootstrap event before workspace files are injected.
 */

import type { HookHandler } from 'openclaw/hooks';

const REMINDER_CONTENT = `## Conversation Self-Improvement Reminder

After completing dialogue tasks, evaluate if any conversational learnings should be captured:

**Log when:**
- User expresses frustration or confusion → \`.learnings/DIALOGUE_ISSUES.md\`
- Tone mismatch detected (formal vs casual) → \`.learnings/LEARNINGS.md\` with \`tone_mismatch\`
- Context lost mid-conversation → \`.learnings/LEARNINGS.md\` with \`context_loss\`
- Hallucinated information (wrong facts, policies, hours) → \`.learnings/LEARNINGS.md\` with \`hallucination\`
- User requests escalation to human → \`.learnings/DIALOGUE_ISSUES.md\`
- Missing conversational capability identified → \`.learnings/FEATURE_REQUESTS.md\`

**Promote when pattern is proven:**
- Conversation tone patterns → \`SOUL.md\`
- Dialogue workflows and escalation protocols → \`AGENTS.md\`
- Channel integration gotchas → \`TOOLS.md\`

Keep entries focused: date, dialogue excerpt, what went wrong, how to handle it next time.`;

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

  // Skip sub-agent sessions to avoid bootstrap noise
  const sessionKey = event.sessionKey || '';
  if (sessionKey.includes(':subagent:')) {
    return;
  }

  if (Array.isArray(event.context.bootstrapFiles)) {
    event.context.bootstrapFiles.push({
      path: 'CONVERSATION_SELF_IMPROVEMENT_REMINDER.md',
      content: REMINDER_CONTENT,
      virtual: true,
    });
  }
};

export default handler;
