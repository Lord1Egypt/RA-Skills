#!/usr/bin/env node
import { spawnSync } from 'node:child_process';
import assert from 'node:assert/strict';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { readFileSync } from 'node:fs';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const script = path.resolve(__dirname, '..', 'scripts', 'send.mjs');

function run(args, env = {}, options = {}) {
  return spawnSync(process.execPath, [script, ...args], {
    encoding: 'utf8',
    input: options.input,
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
function syntheticResendKey() { return ['re', 'SECRET', 'SENTINEL'].join('_'); }

{
  const source = readFileSync(script, 'utf8');
  assert.match(source, /redirect:\s*["']error["']/);
}

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
  const subject = 'Weekly reviewed report digest';
  const r = run(['--json', '--to', 'you@example.com', '--subject', subject, '--body', 'Hi'], { RESEND_ALLOWED_TO: 'you@example.com', RESEND_API_KEY: syntheticResendKey() });
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
  assert.doesNotMatch(combined(r), new RegExp(syntheticResendKey()));
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
  const r = run(['--json', '--dry-run', '--send', '--to', 'you@example.com', '--subject', 'Dry run wins', '--body', 'Hi'], {
    RESEND_ALLOWED_TO: 'you@example.com',
    RESEND_API_KEY: syntheticResendKey(),
  });
  assert.equal(r.status, 0);
  const receipt = JSON.parse(r.stdout);
  assert.equal(receipt.mode, 'dry-run');
  assert.equal(receipt.sent, false);
  assert.equal(receipt.subject, 'Dry run wins');
  assert.deepEqual(receipt.allowlist.blocked, []);
  assert.equal(receipt.payload.text, 'Hi');
  assert.doesNotMatch(combined(r), /resend-id:/i);
  assert.doesNotMatch(combined(r), new RegExp(syntheticResendKey()));
}

{
  const hostileSubject = 'Reviewed subject " ; ` $() | & < >\nnext line';
  const hostileBody = 'Approved body with quotes " and semicolon ; and backtick ` and $(calc) and newline\nsecond line';
  const r = run(['--json', '--dry-run', '--input-json-stdin'], {
    RESEND_ALLOWED_TO: 'you@example.com,copy@example.com,blind@example.com',
    RESEND_API_KEY: syntheticResendKey(),
  }, {
    input: JSON.stringify({
      to: ['you@example.com'],
      cc: ['copy@example.com'],
      bcc: ['blind@example.com'],
      from: 'Reports <onboarding@resend.dev>',
      replyTo: 'reply@example.com',
      subject: hostileSubject,
      body: hostileBody,
      html: false,
    }),
  });
  assert.equal(r.status, 0);
  const receipt = JSON.parse(r.stdout);
  assert.equal(receipt.mode, 'dry-run');
  assert.equal(receipt.sent, false);
  assert.equal(receipt.subject, hostileSubject);
  assert.equal(receipt.payload.text, hostileBody);
  assert.deepEqual(receipt.cc, ['copy@example.com']);
  assert.deepEqual(receipt.bcc, ['blind@example.com']);
  assert.equal(receipt.from, 'Reports <onboarding@resend.dev>');
  assert.equal(receipt.replyTo, 'reply@example.com');
  assert.deepEqual(receipt.allowlist.blocked, []);
  assert.doesNotMatch(combined(r), new RegExp(syntheticResendKey()));
}

{
  const r = run(['--json', '--dry-run', '--input-json-stdin', '--body', 'inline'], {}, {
    input: JSON.stringify({ to: 'you@example.com', subject: 'Hello', body: 'Hi' }),
  });
  assert.equal(r.status, 1);
  assert.match(r.stderr, /cannot be combined with inline message flags/);
}

{
  const r = run(['--json', '--dry-run', '--input-json-stdin'], {}, {
    input: JSON.stringify({ to: 'you@example.com', subject: 'Hello', body: 'Hi', send: true }),
  });
  assert.equal(r.status, 1);
  assert.match(r.stderr, /unsupported field\(s\): send/);
}

{
  const r = run(['--send', '--to', 'allowed@example.com', '--cc', 'blocked-cc@example.com', '--subject', 'CC blocked', '--body', 'Hi'], {
    RESEND_ALLOWED_TO: 'allowed@example.com',
    RESEND_API_KEY: syntheticResendKey(),
  });
  assert.equal(r.status, 1);
  assert.match(r.stderr, /recipient not in RESEND_ALLOWED_TO allowlist: blocked-cc@example.com/);
  assert.doesNotMatch(combined(r), /POST https:\/\/api\.resend\.com\/emails/);
  assert.doesNotMatch(combined(r), new RegExp(syntheticResendKey()));
}

{
  const r = run(['--send', '--to', 'allowed@example.com', '--bcc', 'blocked-bcc@example.com', '--subject', 'BCC blocked', '--body', 'Hi'], {
    RESEND_ALLOWED_TO: 'allowed@example.com',
    RESEND_API_KEY: syntheticResendKey(),
  });
  assert.equal(r.status, 1);
  assert.match(r.stderr, /recipient not in RESEND_ALLOWED_TO allowlist: blocked-bcc@example.com/);
  assert.doesNotMatch(combined(r), /POST https:\/\/api\.resend\.com\/emails/);
  assert.doesNotMatch(combined(r), new RegExp(syntheticResendKey()));
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
  assert.match(r.stdout, /Required message fields \(inline flags or --input-json-stdin\)/);
  assert.match(r.stdout, /RESEND_ALLOWED_TO/);
}

console.log('resend-send-native-node tests PASS');
