const { spawnSync } = require('child_process');
const fs = require('fs');
const path = require('path');

const skillDir = '/home/irtual/.openclaw/workspace/skills/qwen-orchestrator';
const ask = path.join(skillDir, 'ask-qwen.sh');
const session = `ci-followup-${Date.now()}`;
const rounds = Number(process.env.QWEN_CONTINUITY_ROUNDS || '3');

function run(args, input = null, timeout = 240000) {
  const res = spawnSync('bash', [ask, ...args], {
    cwd: skillDir,
    input,
    encoding: 'utf8',
    timeout,
    maxBuffer: 8 * 1024 * 1024,
  });
  return res;
}

function assert(cond, msg) {
  if (!cond) throw new Error(msg);
}

function loadSession() {
  const file = path.join(skillDir, '.sessions', `${session}.json`);
  return JSON.parse(fs.readFileSync(file, 'utf8'));
}

try {
  let r1 = run(['--daemon', '--session', session, 'Reply with exactly: FIRST_OK']);
  console.log('--- round1 code', r1.status);
  console.log(r1.stdout.split('\n').slice(-20).join('\n'));
  assert(r1.status === 0, `round1 failed: ${r1.stderr || r1.stdout}`);
  let s1 = loadSession();
  assert(/\/c\//.test(s1.chatUrl), 'round1 did not persist chatUrl');
  const chat1 = s1.chatUrl;

  const labels = ['SECOND_OK', 'FOLLOWUP_3_OK', 'FOLLOWUP_4_OK', 'FOLLOWUP_5_OK', 'FOLLOWUP_6_OK'];
  for (let i = 0; i < rounds - 1; i++) {
    const label = labels[i] || `FOLLOWUP_${i + 2}_OK`;
    const rx = new RegExp(label, 'i');
    const rr = run(['--daemon', '--session', session, `Reply with exactly: ${label}`]);
    console.log(`--- follow-up ${i + 2} code`, rr.status);
    console.log(rr.stdout.split('\n').slice(-40).join('\n'));
    assert(rr.status === 0, `follow-up ${i + 2} failed: ${rr.stderr || rr.stdout}`);
    const sx = loadSession();
    assert(sx.chatUrl === chat1, `follow-up ${i + 2} changed chatUrl: ${chat1} -> ${sx.chatUrl}`);
    assert(rx.test(rr.stdout), `follow-up ${i + 2} output missing ${label}`);
    assert(!/Chat continuity broken/i.test(rr.stdout + '\n' + rr.stderr), `follow-up ${i + 2} reported continuity break`);
  }

  let rNew = run(['--daemon', '--session', session, '--new-chat', 'Reply with exactly: THIRD_OK']);
  console.log('--- round new-chat code', rNew.status);
  console.log(rNew.stdout.split('\n').slice(-30).join('\n'));
  assert(rNew.status === 0, `new-chat failed: ${rNew.stderr || rNew.stdout}`);
  let sNew = loadSession();
  assert(/\/c\//.test(sNew.chatUrl), 'new-chat did not persist chatUrl');
  assert(sNew.chatUrl !== chat1, 'new-chat did not rotate chatUrl');

  let end = run(['--session', session, '--end-session']);
  assert(end.status === 0, `end-session failed: ${end.stderr || end.stdout}`);

  console.log(`[OK] follow-up continuity smoke passed (${rounds} rounds before new-chat)`);
} catch (err) {
  console.error('[FAIL]', err.message);
  process.exit(1);
}
