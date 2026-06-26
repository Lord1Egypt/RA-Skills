/**
 * Tests for qa-bug-report.ts (3.3.1-rc.3).
 *
 * Covers:
 *   - isRcBuild accepts SemVer -rc. + PEP-440 rc, rejects stable + beta.
 *   - redactSecrets hits BIP-39, OpenAI keys, Google keys, Telegram bot
 *     tokens, bearer tokens, hex blobs, private keys.
 *   - validateQaBugArgs rejects missing/invalid fields.
 *   - buildIssueBody applies redaction to every user field.
 *   - postQaBugIssue calls the right URL with the right headers + body,
 *     returns issue URL + number. On non-2xx, throws with status.
 *
 * Run with: npx tsx qa-bug-report.test.ts
 */

import {
  DEFAULT_QA_REPO,
  PUBLIC_REPOS_DENYLIST,
  isRcBuild,
  redactSecrets,
  resolveQaRepo,
  validateQaBugArgs,
  buildIssueBody,
  postQaBugIssue,
  type QaBugArgs,
} from './qa-bug-report.js';

let passed = 0;
let failed = 0;

function assert(cond: boolean, name: string): void {
  const n = passed + failed + 1;
  if (cond) {
    console.log(`ok ${n} - ${name}`);
    passed++;
  } else {
    console.log(`not ok ${n} - ${name}`);
    failed++;
  }
}

// ---------------------------------------------------------------------------
// isRcBuild
// ---------------------------------------------------------------------------

assert(isRcBuild('3.3.1-rc.3'), 'isRcBuild: SemVer -rc.N → true');
assert(isRcBuild('3.3.1-rc.0'), 'isRcBuild: -rc.0 accepted');
assert(isRcBuild('2.3.1rc3'), 'isRcBuild: PEP-440 rcN → true');
assert(isRcBuild('1.0.0-rc.1'), 'isRcBuild: SemVer with pre-release suffix');

assert(!isRcBuild('3.3.1'), 'isRcBuild: stable SemVer → false');
assert(!isRcBuild('3.3.1-beta.1'), 'isRcBuild: non-RC pre-release → false');
assert(!isRcBuild(''), 'isRcBuild: empty string → false');
assert(!isRcBuild(null), 'isRcBuild: null → false');
assert(!isRcBuild(undefined), 'isRcBuild: undefined → false');

// ---------------------------------------------------------------------------
// redactSecrets
// ---------------------------------------------------------------------------

{
  // 12-word BIP-39 phrase
  const in1 = 'my phrase is abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about please help';
  const out1 = redactSecrets(in1);
  assert(!out1.includes('abandon abandon'), 'redact: BIP-39 12-word phrase stripped');
  assert(out1.includes('<REDACTED>'), 'redact: inserts <REDACTED>');
}

{
  // 24-word BIP-39 phrase
  const phrase24 = 'legal winner thank year wave sausage worth useful legal winner thank year wave sausage worth useful legal winner thank year wave sausage worth title';
  const out = redactSecrets(`recovery: ${phrase24} end`);
  assert(!out.includes('legal winner thank'), 'redact: 24-word phrase stripped');
}

{
  // OpenAI-style sk- key
  const in2 = 'set OPENAI_API_KEY=sk-abc123XYZ456DEF789012ABC';
  const out2 = redactSecrets(in2);
  assert(!/sk-[A-Za-z0-9]{20,}/.test(out2), 'redact: sk- key stripped');
  assert(out2.includes('<REDACTED>'), 'redact: sk- replacement');
}

{
  // Google API key (AIzaSy...)
  const in3 = 'GOOGLE_API_KEY=AIzaSyAbCdEfGhIjKlMnOpQrStUvWxYz012345678';
  const out3 = redactSecrets(in3);
  assert(!/AIza[A-Za-z0-9_-]{35}/.test(out3), 'redact: Google API key stripped');
}

{
  // Telegram bot token
  const in4 = 'TELEGRAM_BOT_TOKEN=1234567890:AAHdqTcvGhLxjkM12345_hjklzxcv67890abcd';
  const out4 = redactSecrets(in4);
  assert(!/\d{6,}:[A-Za-z0-9_-]{35,}/.test(out4), 'redact: Telegram bot token stripped');
}

{
  // Bearer token in Authorization header
  const in5 = 'Authorization: Bearer a1b2c3d4e5f67890abcdef12345678901234567890abcdef';
  const out5 = redactSecrets(in5);
  // The header name survives; the token is replaced.
  assert(/authorization/i.test(out5), 'redact: Authorization header name preserved');
  assert(out5.includes('<REDACTED>'), 'redact: bearer token replaced');
}

{
  // 64-char hex auth key
  const in6 = 'authKey=0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef';
  const out6 = redactSecrets(in6);
  assert(!/[a-f0-9]{64}/.test(out6), 'redact: 64-char hex blob stripped');
}

{
  // 0x-prefixed private key
  const in7 = 'privkey=0x0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef';
  const out7 = redactSecrets(in7);
  assert(!/0x[a-f0-9]{64}/.test(out7), 'redact: 0x private key stripped');
}

{
  // Things we DO NOT redact — fact UUIDs, commit SHAs (40-char hex), normal addresses
  const in8 = 'fact_id=abc12345-def6-7890-abcd-ef0123456789 commit=1234567890abcdef1234567890abcdef12345678 address=0xabc123def456';
  const out8 = redactSecrets(in8);
  assert(out8.includes('abc12345-def6-7890-abcd-ef0123456789'), 'redact: preserves naked UUIDs (fact ids)');
  assert(out8.includes('1234567890abcdef1234567890abcdef12345678'), 'redact: preserves 40-char commit SHA');
  assert(out8.includes('0xabc123def456'), 'redact: preserves short EVM addresses');
}

{
  // Empty / null input
  assert(redactSecrets('') === '', 'redact: empty string → empty');
  assert(redactSecrets(null as unknown as string) === '', 'redact: null → empty');
}

// ---------------------------------------------------------------------------
// validateQaBugArgs
// ---------------------------------------------------------------------------

const validArgs: QaBugArgs = {
  integration: 'plugin',
  rc_version: '3.3.1-rc.3',
  severity: 'high',
  title: 'AA25 on rapid stores',
  symptom: 'Storing 5 facts in a row triggers AA25',
  expected: 'All 5 should store cleanly',
  repro: '1. ...\n2. ...',
  logs: 'error: AA25 invalid account nonce',
  environment: 'VPS, OpenClaw 2026.4.15, zai',
};

assert(validateQaBugArgs(validArgs).ok === true, 'validate: valid args → ok');

{
  const bad = { ...validArgs, integration: 'unknown' };
  const res = validateQaBugArgs(bad);
  assert(res.ok === false, 'validate: unknown integration rejected');
  if (!res.ok) assert(res.error.includes('integration'), 'validate: error mentions integration');
}

{
  const bad = { ...validArgs, severity: 'critical' };
  const res = validateQaBugArgs(bad);
  assert(res.ok === false, 'validate: unknown severity rejected');
}

{
  const bad = { ...validArgs, title: 'x'.repeat(70) };
  const res = validateQaBugArgs(bad);
  assert(res.ok === false, 'validate: title > 60 chars rejected');
}

{
  const bad = { ...validArgs, symptom: '' };
  const res = validateQaBugArgs(bad);
  assert(res.ok === false, 'validate: empty symptom rejected');
}

// ---------------------------------------------------------------------------
// buildIssueBody
// ---------------------------------------------------------------------------

{
  const body = buildIssueBody(validArgs);
  assert(body.includes('### What happened'), 'body: contains "What happened" header');
  assert(body.includes('### Environment'), 'body: contains "Environment" header');
  assert(body.includes('OpenClaw plugin'), 'body: integration display name expanded');
  assert(body.includes('3.3.1-rc.3'), 'body: rc_version embedded');
  assert(body.includes('AA25'), 'body: symptom embedded');
}

{
  const withSecret: QaBugArgs = {
    ...validArgs,
    logs: 'error: sk-abc123XYZ456DEF789012ABC leaked',
  };
  const body = buildIssueBody(withSecret);
  assert(!body.includes('sk-abc123'), 'body: applies redaction to logs');
  assert(body.includes('<REDACTED>'), 'body: shows <REDACTED> marker');
}

// ---------------------------------------------------------------------------
// resolveQaRepo — rc.14 target-repo guard
// ---------------------------------------------------------------------------

{
  // Default (no override, no env) → internal.
  assert(resolveQaRepo(null, {}) === 'p-diogo/totalreclaw-internal', 'resolve: default → internal');
  assert(resolveQaRepo(null, {}) === DEFAULT_QA_REPO, 'resolve: DEFAULT_QA_REPO exported constant');
}

{
  // Env override accepted when slug ends in -internal.
  const env = { TOTALRECLAW_QA_REPO: 'acme/totalreclaw-qa-internal' };
  assert(
    resolveQaRepo(null, env) === 'acme/totalreclaw-qa-internal',
    'resolve: env override accepted for -internal fork',
  );
}

{
  // Explicit override beats env override.
  const env = { TOTALRECLAW_QA_REPO: 'other/totalreclaw-internal' };
  assert(
    resolveQaRepo('acme/totalreclaw-internal', env) === 'acme/totalreclaw-internal',
    'resolve: explicit override beats env',
  );
}

{
  // Public repo denylist hit — throws.
  let threw = false;
  try {
    resolveQaRepo(null, { TOTALRECLAW_QA_REPO: 'p-diogo/totalreclaw' });
  } catch (err) {
    threw = true;
    assert(
      err instanceof Error && err.message.includes('PUBLIC'),
      'resolve: public-repo error mentions "PUBLIC"',
    );
  }
  assert(threw, 'resolve: env pointing at public repo throws');
}

{
  // Public repo via explicit override — throws.
  let threw = false;
  try {
    resolveQaRepo('p-diogo/totalreclaw', {});
  } catch {
    threw = true;
  }
  assert(threw, 'resolve: explicit public-repo override throws');
}

{
  // Non -internal slug — throws.
  let threw = false;
  try {
    resolveQaRepo('someone/random-repo', {});
  } catch (err) {
    threw = true;
    assert(
      err instanceof Error && err.message.includes('-internal'),
      'resolve: structural-rule error mentions "-internal"',
    );
  }
  assert(threw, 'resolve: non "-internal" slug throws');
}

{
  // Malformed slug — throws.
  let threw = false;
  try {
    resolveQaRepo('no-slash', {});
  } catch (err) {
    threw = true;
    assert(
      err instanceof Error && err.message.includes('owner/name'),
      'resolve: malformed slug error mentions format hint',
    );
  }
  assert(threw, 'resolve: malformed slug throws');
}

{
  // Denylist sanity — historical leak target captured.
  assert(
    PUBLIC_REPOS_DENYLIST.has('p-diogo/totalreclaw'),
    'resolve: denylist contains public repo',
  );
}

// ---------------------------------------------------------------------------
// postQaBugIssue — mocked fetch
// ---------------------------------------------------------------------------

async function runPostTests(): Promise<void> {
  // Success path
  {
    let capturedUrl = '';
    let capturedInit: RequestInit | null = null;
    const mockFetch = (async (url: string | URL | Request, init?: RequestInit): Promise<Response> => {
      capturedUrl = String(url);
      capturedInit = init ?? null;
      return new Response(
        JSON.stringify({ number: 42, html_url: 'https://github.com/p-diogo/totalreclaw-internal/issues/42' }),
        { status: 201, headers: { 'Content-Type': 'application/json' } },
      );
    }) as typeof fetch;

    const result = await postQaBugIssue(validArgs, {
      githubToken: 'gh-test-token',
      fetchImpl: mockFetch,
    });
    assert(result.issue_number === 42, 'post: returns issue number');
    assert(result.issue_url.includes('/issues/42'), 'post: returns issue URL');
    assert(capturedUrl.endsWith('/repos/p-diogo/totalreclaw-internal/issues'), 'post: default repo is internal');
    assert((capturedInit?.method ?? '') === 'POST', 'post: uses POST');
    const headers = (capturedInit?.headers ?? {}) as Record<string, string>;
    assert(headers.Authorization === 'Bearer gh-test-token', 'post: auth header set');
    assert(headers.Accept === 'application/vnd.github+json', 'post: accept header set');
    const body = JSON.parse(String(capturedInit?.body ?? '{}'));
    assert(body.title.startsWith('[qa-bug]'), 'post: title prefixed');
    assert(Array.isArray(body.labels) && body.labels.includes('qa-bug'), 'post: labels include qa-bug');
    assert(body.labels.includes('severity:high'), 'post: severity label');
    assert(body.labels.includes('component:plugin'), 'post: component label');
    assert(body.labels.some((l: string) => l.startsWith('rc:')), 'post: rc label included');
  }

  // Secrets in fields are redacted before POST
  {
    let capturedBody = '';
    const mockFetch = (async (url: string | URL | Request, init?: RequestInit): Promise<Response> => {
      capturedBody = String(init?.body ?? '');
      return new Response(
        JSON.stringify({ number: 1, html_url: 'https://example/1' }),
        { status: 201, headers: { 'Content-Type': 'application/json' } },
      );
    }) as typeof fetch;

    const withSecret: QaBugArgs = {
      ...validArgs,
      logs: 'TELEGRAM_BOT_TOKEN=1234567890:AAHdqTcvGhLxjkM12345_hjklzxcv67890abcd leaked',
      environment: 'with mnemonic abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about',
    };
    await postQaBugIssue(withSecret, { githubToken: 'gh-test-token', fetchImpl: mockFetch });
    assert(!capturedBody.includes('abandon abandon'), 'post: BIP-39 in body is redacted');
    assert(!capturedBody.includes('AAHdqTcvGhLxjkM12345'), 'post: Telegram token in body is redacted');
  }

  // Non-2xx throws
  {
    const mockFetch = (async (): Promise<Response> => {
      return new Response('{"message":"Bad credentials"}', {
        status: 401,
        headers: { 'Content-Type': 'application/json' },
      });
    }) as typeof fetch;
    let threw = false;
    try {
      await postQaBugIssue(validArgs, { githubToken: 'bad-token', fetchImpl: mockFetch });
    } catch (err) {
      threw = true;
      assert(
        err instanceof Error && err.message.includes('401'),
        'post: 401 error mentions status code',
      );
    }
    assert(threw, 'post: non-2xx throws');
  }

  // Missing token throws
  {
    let threw = false;
    try {
      await postQaBugIssue(validArgs, { githubToken: '' });
    } catch (err) {
      threw = true;
      assert(err instanceof Error && err.message.includes('githubToken'), 'post: empty token error');
    }
    assert(threw, 'post: empty token throws');
  }

  // Invalid args throws
  {
    let threw = false;
    try {
      await postQaBugIssue(
        { ...validArgs, integration: 'bogus' },
        { githubToken: 'test', fetchImpl: (async () => new Response('', { status: 200 })) as typeof fetch },
      );
    } catch (err) {
      threw = true;
      assert(err instanceof Error && err.message.includes('integration'), 'post: invalid integration error');
    }
    assert(threw, 'post: invalid args throws');
  }

  // rc.14 regression: post rejects explicit public-repo override, never calls fetch.
  {
    let fetchCalled = false;
    const mockFetch = (async (): Promise<Response> => {
      fetchCalled = true;
      return new Response('{}', { status: 200 });
    }) as typeof fetch;
    let threw = false;
    try {
      await postQaBugIssue(validArgs, {
        githubToken: 'gh-token',
        repo: 'p-diogo/totalreclaw',
        fetchImpl: mockFetch,
      });
    } catch (err) {
      threw = true;
      assert(
        err instanceof Error && err.message.includes('PUBLIC'),
        'post: public-repo error mentions "PUBLIC"',
      );
    }
    assert(threw, 'post: rejects public-repo override');
    assert(!fetchCalled, 'post: fetch never called for public repo');
  }

  // rc.14 regression: post uses explicit internal override when provided.
  {
    let capturedUrl = '';
    const mockFetch = (async (url: string | URL | Request): Promise<Response> => {
      capturedUrl = String(url);
      return new Response(
        JSON.stringify({ number: 1, html_url: 'https://example/1' }),
        { status: 201, headers: { 'Content-Type': 'application/json' } },
      );
    }) as typeof fetch;
    await postQaBugIssue(validArgs, {
      githubToken: 'gh-token',
      repo: 'acme/totalreclaw-internal',
      fetchImpl: mockFetch,
    });
    assert(
      capturedUrl.endsWith('/repos/acme/totalreclaw-internal/issues'),
      'post: honors -internal override slug',
    );
  }
}

await runPostTests();

// ---------------------------------------------------------------------------
// Summary
// ---------------------------------------------------------------------------

console.log(`# fail: ${failed}`);
console.log(`# ${passed}/${passed + failed} passed`);
if (failed > 0) {
  console.log('SOME TESTS FAILED');
  process.exit(1);
}
console.log('ALL TESTS PASSED');
