const path = require('path');
const { loadSleepState } = require('../../lib/sleep-check');

const QUEUE_SCRIPT = path.join(
  process.env.HOME,
  '.openclaw', 'skills', 'sleep-snooze', 'scripts', 'queue-message.js'
);

const handler = async (event) => {
  if (event.type !== 'agent' || event.action !== 'bootstrap') return;

  let isSleeping, state;
  try {
    ({ isSleeping, state } = loadSleepState());
  } catch {
    // sleep-snooze not configured yet — skip silently
    return;
  }

  if (!isSleeping) return;

  if (event.context && Array.isArray(event.context.bootstrapFiles)) {
    event.context.bootstrapFiles.push({
      basename: 'SLEEP_MODE_ACTIVE.md',
      content:  buildSleepNotice(state, QUEUE_SCRIPT),
    });
  }
};

function buildSleepNotice(state, queueScript) {
  return `# 🌙 SLEEP MODE IS ACTIVE — READ THIS BEFORE TAKING ANY ACTION

The user is currently sleeping. Sleep window: **${state.sleepStart} → ${state.wakeTime} (${state.timezone})**.

## RULE: Do NOT send any message to the user

This includes: summaries, alerts, status updates, heartbeats, digests, reports, or any other notification.

## Instead: use gate.js before every send

Replace any direct message send with a gate check:

\`\`\`bash
node ${path.join(path.dirname(queueScript), 'gate.js')} \\
  --provider <provider-name> \\
  --sender-id <your-agent-id> \\
  --sender-name "<Your Agent Name>" \\
  --message "<the full message text>"
\`\`\`

Exit codes:
- **0** — queued, do NOT send
- **2** — urgent, send immediately with 🚨 prefix
- **3** — awake, send normally

## Urgency bypass

Only urgent if message contains: \`urgent\`, \`emergency\`, \`critical\`, \`911\`, \`help me\`, or sender is a VIP contact.

Heartbeats, weekly recaps, stock summaries, backup confirmations → **NOT urgent → queue them**.
`;
}

module.exports = handler;
