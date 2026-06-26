#!/usr/bin/env node
const fs = require('fs');
const path = require('path');
const { handleWineChat, classifyWineIntent } = require('../lib/wine-chat');

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

function print(obj) {
  process.stdout.write(`${JSON.stringify(obj, null, 2)}\n`);
}

function shellQuote(value) {
  return `'${String(value).replace(/'/g, `'"'"'`)}'`;
}

function main() {
  const args = parseArgs(process.argv.slice(2));
  const text = args.text || args._.join(' ');
  let labelText = args['label-text'] || '';
  if (!labelText && args.file) {
    labelText = fs.readFileSync(path.resolve(args.file), 'utf8');
  }

  const payload = {
    text,
    labelText,
    imagePath: args.image || null,
  };
  const result = handleWineChat(payload);
  const output = {
    status: result.ok ? 'ok' : 'error',
    intent: classifyWineIntent(text || labelText),
    ...result,
  };

  if (args['telegram-send'] && result.action === 'show-label' && result.mediaPath) {
    const target = args.target;
    const threadId = args['thread-id'];
    const replyTo = args['reply-to'];
    if (!target) {
      output.status = 'error';
      output.reply = 'telegram-send requires --target';
    } else {
      const parts = [
        'openclaw message send',
        '--channel telegram',
        `--target ${shellQuote(target)}`,
        threadId ? `--thread-id ${shellQuote(threadId)}` : null,
        replyTo ? `--reply-to ${shellQuote(replyTo)}` : null,
        `--media ${shellQuote(result.mediaPath)}`,
        `--message ${shellQuote(result.caption || 'Wine label')}`,
        '--json',
      ].filter(Boolean);
      output.telegramSendCommand = parts.join(' ');
    }
  }

  print(output);
}

main();
