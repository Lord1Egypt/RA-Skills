/**
 * Self-Improving Coding Hook for OpenClaw
 *
 * Injects a coding-specific reminder to evaluate learnings during agent bootstrap.
 * Fires on agent:bootstrap event before workspace files are injected.
 */

import type { HookHandler } from 'openclaw/hooks';

const REMINDER_CONTENT = `## Coding Self-Improvement Reminder

After completing coding tasks, evaluate if any learnings should be captured:

**Log bug patterns when:**
- Lint error encountered (ESLint, Ruff, Clippy) → \`.learnings/BUG_PATTERNS.md\`
- Type error from checker (tsc, mypy, pyright) → \`.learnings/BUG_PATTERNS.md\`
- Runtime exception thrown (TypeError, NullPointer, panic) → \`.learnings/BUG_PATTERNS.md\`
- Test assertion failure → \`.learnings/BUG_PATTERNS.md\`

**Log learnings when:**
- Anti-pattern discovered in code → \`.learnings/LEARNINGS.md\` (anti_pattern)
- Better language idiom found → \`.learnings/LEARNINGS.md\` (idiom_gap)
- Debugging breakthrough reveals root cause → \`.learnings/LEARNINGS.md\` (debugging_insight)
- Tooling issue blocks development → \`.learnings/LEARNINGS.md\` (tooling_issue)
- Refactoring opportunity identified → \`.learnings/LEARNINGS.md\` (refactor_opportunity)

**Log feature requests when:**
- Coding tool or automation needed → \`.learnings/FEATURE_REQUESTS.md\`

**Promote when pattern is proven (3+ occurrences):**
- Code style patterns → style guide
- Recurring lint violations → lint rules (\`.eslintrc\`, \`ruff.toml\`)
- Reusable solutions → code snippets library
- Debugging workflows → debug playbooks

Include minimal before/after code snippets. Specify language and area tag.`;

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
      path: 'CODING_SELF_IMPROVEMENT_REMINDER.md',
      content: REMINDER_CONTENT,
      virtual: true,
    });
  }
};

export default handler;
