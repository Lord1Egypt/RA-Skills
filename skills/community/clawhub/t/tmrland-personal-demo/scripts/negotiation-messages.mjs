#!/usr/bin/env node
import { tmrFetch, parseArgs } from "./_lib.mjs";

const { help, positional, named } = parseArgs(process.argv);
if (help || !positional[0]) {
  console.error('Usage: negotiation-messages.mjs <session-id> [--send "message text"]');
  process.exit(2);
}

const sessionId = positional[0];

if (named.send) {
  const msg = await tmrFetch("POST", `/negotiations/${sessionId}/messages`, {
    content: named.send,
  });
  console.log(`Message sent: ${msg.id}`);
}

const data = await tmrFetch("GET", `/negotiations/${sessionId}/messages`);
console.log(`## Messages for session ${sessionId}\n`);
for (const m of data.items ?? []) {
  const role = m.sender_role ?? "unknown";
  console.log(`[${role}] ${m.content}`);
}
