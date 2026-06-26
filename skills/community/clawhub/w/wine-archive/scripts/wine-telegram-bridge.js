#!/usr/bin/env node
/**
 * wine-telegram-bridge.js — Resolve a wine chat request and output a structured
 * result for the calling agent to act on.
 *
 * This script does NOT execute external commands. It outputs JSON describing
 * the resolved action (including mediaPath and caption for label sends).
 * The calling agent (Claude / OpenClaw) is responsible for sending the
 * Telegram message using the openclaw CLI or SDK.
 *
 * Usage:
 *   node scripts/wine-telegram-bridge.js --text "Show me the Vinho Verde label"
 *
 * Output (JSON):
 *   {
 *     status: "ok" | "error",
 *     intent: string,
 *     action: "send-media" | "reply-text",
 *     reply: string,
 *     mediaPath: string,   // present when action === "send-media"
 *     caption: string,     // media caption
 *     result: { ... }      // full wine-chat result
 *   }
 *
 * When action === "send-media", the agent should send the file at mediaPath
 * with the given caption. Example openclaw CLI invocation (run by the agent):
 *   openclaw message send --channel telegram --target <chat-id> \
 *     --thread-id <thread-id> --reply-to <reply-to> \
 *     --media <mediaPath> --message <caption>
 */

'use strict';

const { classifyWineIntent, handleWineChat } = require('../lib/wine-chat');

function parseArgs(argv) {
  const args = { _: [] };
  for (let i = 0; i < argv.length; i += 1) {
    const token = argv[i];
    if (token.startsWith('--')) {
      const key = token.slice(2);
      const next = argv[i + 1];
      if (!next || next.startsWith('--')) {
        args[key] = true;
      } else {
        args[key] = next;
        i += 1;
      }
    } else {
      args._.push(token);
    }
  }
  return args;
}

function main() {
  const args = parseArgs(process.argv.slice(2));
  const text = args.text || args._.join(' ');
  const imagePath = args.image || null;
  const labelText = args['label-text'] || '';
  const intent = classifyWineIntent(text || labelText, { hasImage: Boolean(imagePath) });
  const result = handleWineChat({ text, labelText, imagePath, intent });

  const hasMedia = result.ok && result.mediaPath &&
    (intent === 'show-label' || result.action === 'show-label' ||
     result.action === 'recall-catalog' || result.action === 'show-wine');

  const output = {
    status: result.ok ? 'ok' : 'error',
    intent,
    action: hasMedia ? 'send-media' : 'reply-text',
    reply: result.reply,
    ...(hasMedia ? { mediaPath: result.mediaPath, caption: result.caption || 'Wine label' } : {}),
    result,
  };

  process.stdout.write(`${JSON.stringify(output, null, 2)}\n`);
}

main();
