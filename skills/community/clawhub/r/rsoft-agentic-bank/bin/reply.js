"use strict";
// Answer your human sponsor in their RSoft Zero app. The signature covers
// keccak256 of the text, so send EXACTLY what you signed (this script does).
//
// Usage:  node reply.js "Requested $5 (req_…) — above my ceiling, please approve in the app."
// Output: the stored message { id, direction: "to_sponsor", created_at }
const { signInbox, MCP } = require("./inbox-sign");

(async () => {
  const text = (process.argv.slice(2).join(" ") || "").trim();
  if (!text) throw new Error('Usage: node reply.js "<text>" (1-2000 characters)');
  if (text.length > 2000) throw new Error("Reply is over 2000 characters.");
  const signed = await signInbox("reply", text);
  const res = await fetch(`${MCP}/api/sponsor/inbox/reply`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ ...signed, text }),
  });
  const out = await res.text();
  console.log(out);
  if (!res.ok || /"error"\s*:\s*true/.test(out)) process.exit(2);
})().catch((e) => {
  console.error("ERROR:", e.message);
  process.exit(1);
});
