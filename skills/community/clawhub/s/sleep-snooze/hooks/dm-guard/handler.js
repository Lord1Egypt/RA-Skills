const { spawnSync } = require('child_process');
const path = require('path');
const { loadSleepState } = require('../../lib/sleep-check');

const QUEUE_SCRIPT = path.join(
  process.env.HOME,
  '.openclaw', 'skills', 'sleep-snooze', 'scripts', 'queue-message.js'
);

const handler = async (event) => {
  if (event.type !== 'message' || event.action !== 'received') return;

  let isSleeping, state;
  try {
    ({ isSleeping, state } = loadSleepState());
  } catch {
    return; // not configured
  }

  if (!isSleeping) return;

  const ctx        = event.context || {};
  const provider   = ctx.channel   || 'unknown';
  const senderId   = ctx.senderId  || ctx.from || 'unknown';
  const senderName = ctx.senderName || ctx.username || senderId;
  const message    = ctx.content   || ctx.text || '';

  if (!message) return;

  // Queue the incoming DM
  const result = spawnSync('node', [
    QUEUE_SCRIPT,
    '--provider',    provider,
    '--sender-id',   senderId,
    '--sender-name', senderName,
    '--message',     message,
  ], { encoding: 'utf8' });

  const exitCode = result.status ?? 1;

  if (exitCode === 2) {
    // Urgent — let it through, don't push an auto-reply
    return;
  }

  if (exitCode === 0) {
    // Queued — send auto-reply to the sender via event.messages
    event.messages.push(
      `💤 ${senderName}, the user is currently sleeping (${state.sleepStart}–${state.wakeTime} ${state.timezone}). ` +
      `Your message has been saved and they'll see it in their morning digest at ${state.wakeTime}.`
    );
  }
};

module.exports = handler;
