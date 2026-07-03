import { test, beforeEach } from 'node:test';
import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import {
  existsSync,
  mkdirSync,
  mkdtempSync,
  readFileSync,
  writeFileSync,
} from 'node:fs';
import { tmpdir } from 'node:os';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const SCRIPT = resolve(
  dirname(fileURLToPath(import.meta.url)),
  '..',
  'credential-store.mjs',
);

const VALID_CANDIDATE_KEY = 'wai_candidate_test_token_xyz';
const VALID_EMPLOYER_KEY = 'wai_employer_test_token_xyz';

let sandbox;

beforeEach(() => {
  sandbox = mkdtempSync(join(tmpdir(), 'workorai-cred-'));
});

// Always returns { stdout, stderr, status }; tests inspect whatever
// they need without caring whether the CLI exited 0 or non-zero.
const runCli = (args, { input, env = {} } = {}) => {
  const result = spawnSync(process.execPath, [SCRIPT, ...args], {
    input,
    env: {
      ...process.env,
      XDG_CONFIG_HOME: sandbox,
      WORKORAI_DISABLE_OS_KEYSTORE: '1',
      WORKORAI_MCP_API_KEY: '',
      WORKORAI_EMPLOYER_MCP_API_KEY: '',
      ...env,
    },
    encoding: 'utf8',
  });
  return {
    stdout: result.stdout ?? '',
    stderr: result.stderr ?? '',
    status: result.status,
  };
};

const writeFile0600 = (filePath, content) => {
  mkdirSync(dirname(filePath), { recursive: true });
  writeFileSync(filePath, content, { mode: 0o600 });
};

test('save --role=employer --shared-file writes to mcp-token-employer', () => {
  runCli(['save', '--role=employer', '--shared-file'], { input: `${VALID_EMPLOYER_KEY}\n` });
  const employerPath = join(sandbox, 'workorai', 'mcp-token-employer');
  const candidatePath = join(sandbox, 'workorai', 'mcp-token');
  assert.ok(existsSync(employerPath), 'employer token file should exist');
  assert.equal(readFileSync(employerPath, 'utf8').trim(), VALID_EMPLOYER_KEY);
  assert.ok(!existsSync(candidatePath), 'candidate token file should NOT be created');
});

test('save without --role (default candidate) writes to mcp-token', () => {
  runCli(['save', '--shared-file'], { input: `${VALID_CANDIDATE_KEY}\n` });
  const tokenPath = join(sandbox, 'workorai', 'mcp-token');
  assert.ok(existsSync(tokenPath));
  assert.equal(readFileSync(tokenPath, 'utf8').trim(), VALID_CANDIDATE_KEY);
});

test('save --role=candidate writes to mcp-token (explicit form)', () => {
  runCli(['save', '--role=candidate', '--shared-file'], { input: `${VALID_CANDIDATE_KEY}\n` });
  const tokenPath = join(sandbox, 'workorai', 'mcp-token');
  assert.ok(existsSync(tokenPath));
});

test('get --role=employer reads from employer slot', () => {
  writeFile0600(join(sandbox, 'workorai', 'mcp-token-employer'), VALID_EMPLOYER_KEY);
  const result = runCli(['get', '--role=employer']);
  assert.equal(result.stdout.trim(), VALID_EMPLOYER_KEY);
});

test('get (default candidate) does NOT see employer slot', () => {
  writeFile0600(join(sandbox, 'workorai', 'mcp-token-employer'), VALID_EMPLOYER_KEY);
  const result = runCli(['get']);
  assert.equal(result.status, 1, 'should exit 1 when candidate slot is empty');
});

test('get --role=employer reads WORKORAI_EMPLOYER_MCP_API_KEY env first', () => {
  const result = runCli(['get', '--role=employer'], {
    env: { WORKORAI_EMPLOYER_MCP_API_KEY: VALID_EMPLOYER_KEY },
  });
  assert.equal(result.stdout.trim(), VALID_EMPLOYER_KEY);
});

test('get (default candidate) reads WORKORAI_MCP_API_KEY env first', () => {
  const result = runCli(['get'], {
    env: { WORKORAI_MCP_API_KEY: VALID_CANDIDATE_KEY },
  });
  assert.equal(result.stdout.trim(), VALID_CANDIDATE_KEY);
});

test('delete --role=employer --shared-file removes only the employer slot', () => {
  writeFile0600(join(sandbox, 'workorai', 'mcp-token'), VALID_CANDIDATE_KEY);
  writeFile0600(join(sandbox, 'workorai', 'mcp-token-employer'), VALID_EMPLOYER_KEY);
  runCli(['delete', '--role=employer', '--shared-file']);
  assert.ok(!existsSync(join(sandbox, 'workorai', 'mcp-token-employer')));
  assert.ok(existsSync(join(sandbox, 'workorai', 'mcp-token')), 'candidate slot preserved');
});

test('--role rejects invalid value', () => {
  const result = runCli(['get', '--role=admin']);
  assert.equal(result.status, 1);
  assert.match(result.stderr, /--role/);
});

test('--role specified twice is rejected (no silent last-write-wins)', () => {
  const result = runCli(['get', '--role=candidate', '--role=employer']);
  assert.equal(result.status, 1);
  assert.match(result.stderr, /more than once/);
});

test('save --best-effort falls back to shared file when OS keystore is bypassed', () => {
  // Proves the catch path in handleSave actually writes the shared
  // file on OS keystore failure. The thrown error in this test does
  // NOT carry a token, so this case alone does not validate the
  // redaction contract; the next test does.
  runCli(['save', '--role=employer', '--best-effort'], {
    input: `${VALID_EMPLOYER_KEY}\n`,
  });
  const employerPath = join(sandbox, 'workorai', 'mcp-token-employer');
  assert.ok(existsSync(employerPath), 'fallback shared file should be written');
  assert.equal(readFileSync(employerPath, 'utf8').trim(), VALID_EMPLOYER_KEY);
});

test('save --best-effort redacts the token from any keystore error message that contains it', () => {
  // Real keystore errors on macOS / Windows can echo the offending
  // value back in stderr (e.g. `security add-generic-password` quoted
  // the -w argument in older releases; PowerShell error messages can
  // include $env values verbatim). Inject a token-bearing fake error
  // via the test hook in saveToOsStore so handleSave's catch block
  // has something real to redact. Without this guard, a refactor
  // that drops redactSecrets from the catch block would silently
  // leak the user's MCP key to their terminal log.
  const fakeError = `macOS Keychain failed: SecKeychainItemCreate token=${VALID_EMPLOYER_KEY} status=-25299`;
  const result = runCli(['save', '--role=employer', '--best-effort'], {
    input: `${VALID_EMPLOYER_KEY}\n`,
    env: { WORKORAI_TEST_FAKE_KEYSTORE_ERROR: fakeError },
  });
  assert.match(result.stderr, /wai_\[REDACTED\]/, 'stderr should contain the redaction marker');
  assert.ok(
    !result.stderr.includes(VALID_EMPLOYER_KEY),
    `stderr must not contain the raw token. stderr was: ${result.stderr}`,
  );
  const employerPath = join(sandbox, 'workorai', 'mcp-token-employer');
  assert.ok(existsSync(employerPath), 'shared file should still be written');
  assert.equal(readFileSync(employerPath, 'utf8').trim(), VALID_EMPLOYER_KEY);
});

test('warnIfKeystoreDisabled fires on get when env is set', () => {
  // The disable env var is on by default in this test harness.
  const result = runCli(['get']);
  assert.match(result.stderr, /WORKORAI_DISABLE_OS_KEYSTORE/);
});

test('warnIfKeystoreDisabled does NOT fire on save --shared-file (avoids stderr noise when shared-file is the chosen mode)', () => {
  const result = runCli(['save', '--shared-file', '--role=candidate'], {
    input: `${VALID_CANDIDATE_KEY}\n`,
  });
  assert.ok(
    !result.stderr.includes('WORKORAI_DISABLE_OS_KEYSTORE'),
    `--shared-file save should not emit the disable-warning. stderr was: ${result.stderr}`,
  );
});

test('handleDelete exits 1 when OS keystore delete fails (C1 contract)', () => {
  // Without this contract, the previous shape returned exit 0 even on
  // real backend failures (Keychain locked, secret-tool D-Bus dead,
  // PowerShell vault inaccessible). Scripts piping
  // `credential-store delete && next-cmd` saw `next-cmd` run despite
  // the rotation having silently failed.
  const result = runCli(['delete', '--role=candidate'], {
    env: { WORKORAI_TEST_FAKE_DELETE_FAILURE: '1' },
  });
  assert.equal(result.status, 1, 'should exit 1 on real keystore delete failure');
  assert.match(result.stderr, /delete reported failures/);
});
