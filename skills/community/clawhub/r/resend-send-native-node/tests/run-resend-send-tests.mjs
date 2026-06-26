#!/usr/bin/env node
import { spawnSync } from 'node:child_process';
import assert from 'node:assert/strict';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const script = path.resolve(__dirname, '..', 'scripts', 'send.mjs');

function run(args, env = {}) {
  return spawnSync(process.execPath, [script, ...args], {
    encoding: 'utf8',
    env: {
      PATH: process.env.PATH || '',
      SystemRoot: process.env.SystemRoot || '',
      WINDIR: process.env.WINDIR || '',
      RESEND_API_KEY: '',
      RESEND_ALLOWED_TO: '',
      ...env,
    },
  });
}

function combined(r) { return `${r.stdout || ''}\n${r.stderr || ''}`; }

{
  const r = run(['--to', 'you@example.com', '--subject', 'Hello', '--body', 'Hi']);
  assert.equal(r.status, 0);
  assert.match(r.stdout, /--- DRY RUN/);
  assert.match(r.stdout, /note: add --send/);
  assert.match(r.stdout, /Authorization: Bearer \[redacted\]/);
  assert.match(r.stdout, /WARNING: RESEND_ALLOWED_TO is not configured/);
  assert.match(r.stdout, /"text": "Hi"/);
  assert.doesNotMatch(combined(r), /re_[A-Za-z0-9]/);
}

{
  const r = run(['--html', '--to', 'you@example.com', '--subject', 'Styled', '--body', '<p>Hi</p>'], { RESEND_ALLOWED_TO: 'you@example.com' });
  assert.equal(r.status, 0);
  assert.match(r.stdout, /allowlist: all recipients are allowed/);
  assert.match(r.stdout, /"html": "<p>Hi<\/p>"/);
  assert.doesNotMatch(r.stdout, /"text"/);
}

{
  const subject = 'Tavily Basic — AI agent governance radar';
  const r = run(['--json', '--to', 'you@example.com', '--subject', subject, '--body', 'Hi'], { RESEND_ALLOWED_TO: 'you@example.com', RESEND_API_KEY: 're_SECRET_SENTINEL' });
  assert.equal(r.status, 0);
  const receipt = JSON.parse(r.stdout);
  assert.equal(receipt.mode, 'dry-run');
  assert.equal(receipt.sent, false);
  assert.deepEqual(receipt.to, ['you@example.com']);
  assert.equal(receipt.subject, subject);
  assert.equal(receipt.bodyBytes, 2);
  assert.equal(receipt.bodySha256Prefix.length, 12);
  assert.equal(receipt.bodySha256.length, 64);
  assert.equal(receipt.allowlist.configured, true);
  assert.deepEqual(receipt.allowlist.blocked, []);
  assert.equal(receipt.payload.text, 'Hi');
  assert.doesNotMatch(combined(r), /re_SECRET_SENTINEL/);
}

{
  const r = run(['--json', '--dry-run', '--to', 'you@example.com', '--subject', 'No allowlist', '--body', 'Hi']);
  assert.equal(r.status, 0);
  const receipt = JSON.parse(r.stdout);
  assert.equal(receipt.mode, 'dry-run');
  assert.equal(receipt.allowlist.configured, false);
  assert.deepEqual(receipt.allowlist.blocked, ['you@example.com']);
}

{
  const r = run(['--send', '--to', 'you@example.com', '--subject', 'Hello', '--body', 'Hi']);
  assert.equal(r.status, 1);
  assert.match(r.stderr, /RESEND_ALLOWED_TO must be set/);
  assert.doesNotMatch(combined(r), /POST https:\/\/api\.resend\.com\/emails/);
}

{
  const r = run(['--send', '--to', 'blocked@example.com', '--subject', 'Hello', '--body', 'Hi'], { RESEND_ALLOWED_TO: 'allowed@example.com' });
  assert.equal(r.status, 1);
  assert.match(r.stderr, /recipient not in RESEND_ALLOWED_TO allowlist: blocked@example\.com/);
  assert.doesNotMatch(combined(r), /POST https:\/\/api\.resend\.com\/emails/);
}

{
  const r = run(['--send', '--to', 'you@example.com', '--subject', 'Hello', '--body', 'Hi'], { RESEND_ALLOWED_TO: 'you@example.com' });
  assert.equal(r.status, 1);
  assert.match(r.stderr, /RESEND_API_KEY not set/);
  assert.doesNotMatch(combined(r), /POST https:\/\/api\.resend\.com\/emails/);
}

{
  const r = run(['--to', 'you@example.com', '--subject', 'Hello', '--body-file', 'reviewed-body.txt']);
  assert.equal(r.status, 1);
  assert.match(r.stderr, /--body-file is not supported/);
}

{
  const r = run(['--to', 'not-an-email', '--subject', 'Hello', '--body', 'Hi']);
  assert.equal(r.status, 1);
  assert.match(r.stderr, /invalid email address/);
}

{
  const r = run(['--reply-to', 'reply@example.com', '--to', 'you@example.com', '--subject', 'Hello', '--body', 'Hi']);
  assert.equal(r.status, 0);
  assert.match(r.stdout, /"reply_to": "reply@example\.com"/);
}

{
  const r = run(['--help']);
  assert.equal(r.status, 0);
  assert.match(r.stdout, /Usage: send\.mjs/);
  assert.match(r.stdout, /RESEND_ALLOWED_TO/);
}

console.log('resend-send-native-node tests PASS');
