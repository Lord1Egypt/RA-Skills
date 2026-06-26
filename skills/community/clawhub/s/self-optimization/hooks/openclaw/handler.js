/**
 * Self-Optimization Hook for OpenClaw
 *
 * Injects a compact reminder during bootstrap so the agent can turn
 * corrections, failures, and repeated work into durable improvements.
 */
const REMINDER_CONTENT = `## Self-Optimization Reminder

Before wrapping up work, check whether today's effort uncovered durable signal:

- correction or missing fact -> \`.learnings/LEARNINGS.md\`
- non-obvious command/tool failure -> \`.learnings/ERRORS.md\`
- missing capability the user wanted -> \`.learnings/FEATURE_REQUESTS.md\`
- repeated pattern -> link entries, raise priority, consider promotion

Promote stable patterns into \`AGENTS.md\`, \`CLAUDE.md\`, \`TOOLS.md\`, or \`SOUL.md\`.
Extract a reusable skill when the solution is broad, verified, and repeatable.`;
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
  const sessionKey = event.sessionKey || '';
  if (sessionKey.includes(':subagent:')) {
    return;
  }
  if (Array.isArray(event.context.bootstrapFiles)) {
    event.context.bootstrapFiles.push({
      path: 'SELF_OPTIMIZATION_REMINDER.md',
      content: REMINDER_CONTENT,
      virtual: true
    });
  }
};
export default handler;
