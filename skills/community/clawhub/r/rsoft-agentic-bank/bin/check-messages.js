"use strict";
// Read the messages your human sponsor left you in the bank's mailbox
// (RSoft Zero app → bank → you). Signed pull; each message is delivered once.
//
// Usage:  node check-messages.js
// Output: { messages: [{id, body, created_at}], sponsor_bound, next_action }
const { signInbox, MCP } = require("./inbox-sign");

(async () => {
  const signed = await signInbox("pull");
  const res = await fetch(`${MCP}/api/sponsor/inbox/pull`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ ...signed, limit: 50 }),
  });
  const text = await res.text();
  console.log(text);
  if (!res.ok || /"error"\s*:\s*true/.test(text)) process.exit(2);
})().catch((e) => {
  console.error("ERROR:", e.message);
  process.exit(1);
});
