/**
 * WALVIS msg — wraps a message with the correct inline buttons
 * Usage: node msg.mjs <type> <message_text>
 *
 * Types:
 *   cron-digest   — "✅ Sync Now" + "💤 Skip Tonight" buttons
 *   reminder      — "👍 Got it" + "🔕 Stop reminding" buttons
 *
 * Output: JSON message payload to pass directly to the `message` tool.
 * AI should call: message(action, channel, message, buttons) with the output fields.
 * Do NOT include `to` or `target`.
 */

const BUTTONS = {
  'cron-digest': [[
    { text: '✅ Sync Now',      callback_data: 'w:cron:sync' },
    { text: '💤 Skip Tonight',  callback_data: 'w:cron:snooze' },
  ]],
  'reminder': [[
    { text: '👍 Got it',              callback_data: 'w:remind:ack' },
    { text: '🔕 Stop reminding me',   callback_data: 'w:remind:stop' },
  ]],
};

const args = process.argv.slice(2);
const type = args[0];
const text = args[1];

if (!type || !text) {
  console.error('Usage: node msg.mjs <cron-digest|reminder> "<message text>"');
  process.exit(1);
}

if (!BUTTONS[type]) {
  console.error(`Unknown type: ${type}. Valid: ${Object.keys(BUTTONS).join(', ')}`);
  process.exit(1);
}

console.log(JSON.stringify({
  action: 'send',
  channel: 'telegram',
  message: text,
  buttons: BUTTONS[type],
}));
