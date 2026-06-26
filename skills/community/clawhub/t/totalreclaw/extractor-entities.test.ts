/**
 * Tests for entity + confidence extraction in parseFactsResponse.
 *
 * Run with: npx tsx extractor-entities.test.ts
 */

import {
  parseFactsResponse,
  normalizeConfidence,
  DEFAULT_EXTRACTION_CONFIDENCE,
  type ExtractedFact,
} from './extractor.js';

let passed = 0;
let failed = 0;

function assert(condition: boolean, name: string): void {
  const n = passed + failed + 1;
  if (condition) {
    console.log(`ok ${n} - ${name}`);
    passed++;
  } else {
    console.log(`not ok ${n} - ${name}`);
    failed++;
  }
}

function assertEq<T>(actual: T, expected: T, name: string): void {
  const ok = JSON.stringify(actual) === JSON.stringify(expected);
  if (!ok) {
    console.log(`  actual:   ${JSON.stringify(actual)}`);
    console.log(`  expected: ${JSON.stringify(expected)}`);
  }
  assert(ok, name);
}

// ---------------------------------------------------------------------------
// Entity parsing
// ---------------------------------------------------------------------------

{
  const raw = JSON.stringify([
    {
      text: 'Pedro chose PostgreSQL because it is relational.',
      type: 'decision',
      importance: 8,
      confidence: 0.92,
      action: 'ADD',
      entities: [
        { name: 'Pedro', type: 'person', role: 'chooser' },
        { name: 'PostgreSQL', type: 'tool' },
      ],
    },
  ]);
  const facts = parseFactsResponse(raw);
  assert(facts.length === 1, 'entities: one fact parsed');
  const f = facts[0]!;
  assert(f.entities !== undefined && f.entities.length === 2, 'entities: two entities');
  assertEq(f.entities?.[0], { name: 'Pedro', type: 'person', role: 'chooser' }, 'entities: first entity has role');
  assertEq(f.entities?.[1], { name: 'PostgreSQL', type: 'tool' }, 'entities: second entity has no role');
  assert(f.confidence === 0.92, 'entities: confidence preserved');
}

// Backward compat: no entities field at all.
{
  const raw = JSON.stringify([
    { text: 'User lives in Lisbon.', type: 'fact', importance: 7, action: 'ADD' },
  ]);
  const facts = parseFactsResponse(raw);
  assert(facts.length === 1, 'backcompat: fact without entities parsed');
  assert(facts[0]!.entities === undefined, 'backcompat: entities undefined when absent');
  assert(facts[0]!.confidence === DEFAULT_EXTRACTION_CONFIDENCE, 'backcompat: default confidence 0.85');
}

// Empty entities array → undefined (dropped).
{
  const raw = JSON.stringify([
    { text: 'User likes tea.', type: 'preference', importance: 6, action: 'ADD', entities: [] },
  ]);
  const facts = parseFactsResponse(raw);
  assert(facts.length === 1, 'empty entities: parsed');
  assert(facts[0]!.entities === undefined, 'empty entities: dropped to undefined');
}

// Invalid entities are silently dropped without killing the fact.
{
  const raw = JSON.stringify([
    {
      text: 'Test mixed-validity entities.',
      type: 'fact',
      importance: 7,
      action: 'ADD',
      entities: [
        { name: 'Valid', type: 'concept' },
        { name: '', type: 'person' }, // empty name - invalid
        { name: 'NoType' }, // missing type - invalid
        { name: 'BadType', type: 'alien' }, // unknown type - invalid
        'not-an-object', // wrong shape - invalid
        { name: 'Another', type: 'tool', role: 'driver' },
      ],
    },
  ]);
  const facts = parseFactsResponse(raw);
  assert(facts.length === 1, 'mixed entities: fact survives');
  assertEq(
    facts[0]!.entities,
    [
      { name: 'Valid', type: 'concept' },
      { name: 'Another', type: 'tool', role: 'driver' },
    ],
    'mixed entities: invalid dropped, valid kept',
  );
}

// Entity type case normalization: we accept only lowercase canonical values.
{
  const raw = JSON.stringify([
    {
      text: 'Case test.',
      type: 'fact',
      importance: 7,
      action: 'ADD',
      entities: [
        { name: 'Acme', type: 'Company' }, // uppercase - we normalize to lowercase
        { name: 'Nope', type: 'PERSON' },
      ],
    },
  ]);
  const facts = parseFactsResponse(raw);
  assert(facts.length === 1, 'case test: parsed');
  assert(facts[0]!.entities?.length === 2, 'case test: both entities accepted after lowercase');
  assert(facts[0]!.entities?.[0].type === 'company', 'case test: Company → company');
  assert(facts[0]!.entities?.[1].type === 'person', 'case test: PERSON → person');
}

// ---------------------------------------------------------------------------
// Confidence handling
// ---------------------------------------------------------------------------

{
  assert(normalizeConfidence(0.5) === 0.5, 'confidence: in-range kept');
  assert(normalizeConfidence(1.0) === 1.0, 'confidence: 1.0 kept');
  assert(normalizeConfidence(0.0) === 0.0, 'confidence: 0.0 kept');
  assert(normalizeConfidence(1.7) === 1, 'confidence: > 1 clamped to 1');
  assert(normalizeConfidence(-0.3) === 0, 'confidence: < 0 clamped to 0');
  assert(normalizeConfidence(undefined) === DEFAULT_EXTRACTION_CONFIDENCE, 'confidence: undefined → 0.85');
  assert(normalizeConfidence('0.9') === DEFAULT_EXTRACTION_CONFIDENCE, 'confidence: string → default');
  assert(normalizeConfidence(NaN) === DEFAULT_EXTRACTION_CONFIDENCE, 'confidence: NaN → default');
}

{
  const raw = JSON.stringify([
    { text: 'Confidence high.', type: 'fact', importance: 7, confidence: 5, action: 'ADD' },
  ]);
  const facts = parseFactsResponse(raw);
  assert(facts[0]!.confidence === 1, 'confidence: out-of-range > 1 clamped at parse');
}

{
  const raw = JSON.stringify([
    { text: 'Confidence low.', type: 'fact', importance: 7, confidence: -2, action: 'ADD' },
  ]);
  const facts = parseFactsResponse(raw);
  assert(facts[0]!.confidence === 0, 'confidence: out-of-range < 0 clamped at parse');
}

// ---------------------------------------------------------------------------
// Importance filter still applies; entities don't bypass the 6-floor.
// ---------------------------------------------------------------------------
{
  const raw = JSON.stringify([
    {
      text: 'Low importance chatter.',
      type: 'fact',
      importance: 3,
      action: 'ADD',
      entities: [{ name: 'Thing', type: 'concept' }],
    },
  ]);
  const facts = parseFactsResponse(raw);
  assert(facts.length === 0, 'importance filter: low importance still dropped even with entities');
}

// ---------------------------------------------------------------------------
// v1 taxonomy: legacy v0 tokens are coerced to v1 on parse
// ---------------------------------------------------------------------------

// parseFactsResponse accepts legacy v0 'rule' and coerces to v1 'directive'.
{
  const raw = JSON.stringify([
    {
      text: 'Stop the OpenClaw gateway before rm -rf ~/.totalreclaw/ — async flush can recreate stale files',
      type: 'rule',
      importance: 8,
      confidence: 1.0,
      action: 'ADD',
      entities: [{ name: 'OpenClaw gateway', type: 'tool' }],
    },
  ]);
  const facts = parseFactsResponse(raw);
  assert(facts.length === 1, 'v0 rule: parsed 1 fact');
  assert(facts[0].type === 'directive', 'v0 rule → v1 directive');
  assert(facts[0].importance === 8, 'v0 rule: importance preserved');
  assert(facts[0].entities?.length === 1, 'v0 rule: entities preserved');
  assert(facts[0].entities?.[0].name === 'OpenClaw gateway', 'v0 rule: entity name preserved');
}

// v0 → v1 coercion for the full 8-type legacy set.
{
  const legacyToV1: Record<string, string> = {
    fact: 'claim',
    preference: 'preference',
    decision: 'claim',
    episodic: 'episode',
    goal: 'commitment',
    context: 'claim',
    summary: 'summary',
    rule: 'directive',
  };
  const types = Object.keys(legacyToV1);
  const raw = JSON.stringify(
    types.map((t) => ({
      text: `Test ${t} memory value`,
      type: t,
      importance: 8,
      action: 'ADD',
    })),
  );
  const facts = parseFactsResponse(raw);
  assert(facts.length === 8, 'v0 coercion: all 8 tokens parse');
  for (let i = 0; i < types.length; i++) {
    const v0 = types[i];
    const expected = legacyToV1[v0];
    assert(facts[i].type === expected, `v0 "${v0}" → v1 "${expected}"`);
  }
}

// v1 tokens pass through unchanged. Note: summary+source=user is an
// illegal combination in v1 and is rejected by the parser, so we use
// source='derived' for the summary case.
{
  const v1Types = ['claim', 'preference', 'directive', 'commitment', 'episode', 'summary'];
  const raw = JSON.stringify(
    v1Types.map((t) => ({
      text: `Test ${t} memory value`,
      type: t,
      source: t === 'summary' ? 'derived' : 'user',
      importance: 8,
      action: 'ADD',
    })),
  );
  const facts = parseFactsResponse(raw);
  assert(facts.length === 6, 'v1 native: all 6 tokens parse');
  for (let i = 0; i < v1Types.length; i++) {
    assert(facts[i].type === v1Types[i], `v1 "${v1Types[i]}" preserved`);
  }
}

// Unknown type falls back to v1 'claim'.
{
  const raw = JSON.stringify([
    {
      text: 'Some test memory with an unknown type',
      type: 'invented_category',
      importance: 8,
      action: 'ADD',
    },
  ]);
  const facts = parseFactsResponse(raw);
  assert(facts.length === 1, 'unknown type: still produces 1 fact');
  assert(facts[0].type === 'claim', 'unknown type: falls back to v1 "claim"');
}

// ---------------------------------------------------------------------------
// Phase 2.2.5: thinking-tag stripping, prose-wrapper recovery, observability
// ---------------------------------------------------------------------------

function makeCaptureLogger() {
  const infos: string[] = [];
  const warns: string[] = [];
  return {
    logger: {
      info: (m: string) => infos.push(m),
      warn: (m: string) => warns.push(m),
    },
    infos,
    warns,
  };
}

// 2.2.5: strip <think>...</think> prefix produced by thinking models.
{
  const raw =
    '<think>The user mentioned preferring dark mode. I should extract that as a preference with high confidence.</think>\n' +
    JSON.stringify([
      { text: 'User prefers dark mode', type: 'preference', importance: 7, action: 'ADD' },
    ]);
  const cap = makeCaptureLogger();
  const facts = parseFactsResponse(raw, cap.logger);
  assert(facts.length === 1, 'think-tag: still parses 1 fact');
  assert(facts[0].type === 'preference', 'think-tag: type round-trips');
  assert(facts[0].text === 'User prefers dark mode', 'think-tag: text round-trips');
  assert(cap.warns.length === 0, 'think-tag: no parse-error warning');
}

// 2.2.5: strip <thinking>...</thinking> (longer variant) case-insensitively.
{
  const raw =
    '<THINKING>\nLet me think step by step.\nThe gateway shutdown rule is a classic operational gotcha.\n</THINKING>' +
    JSON.stringify([
      {
        text: 'Stop the gateway before rm -rf to avoid async-flush race',
        type: 'rule',
        importance: 8,
        action: 'ADD',
      },
    ]);
  const cap = makeCaptureLogger();
  const facts = parseFactsResponse(raw, cap.logger);
  assert(facts.length === 1, 'thinking-tag uppercase: parses 1 fact');
  assert(facts[0].type === 'directive', 'thinking-tag uppercase: v0 rule → v1 directive');
  assert(cap.warns.length === 0, 'thinking-tag uppercase: no parse-error warning');
}

// 2.2.5: multi-tag + markdown-fence combo.
{
  const raw =
    '<think>first thought</think>\n' +
    '<think>second thought</think>\n' +
    '```json\n' +
    JSON.stringify([
      { text: 'The sky is blue on this planet', type: 'fact', importance: 7, action: 'ADD' },
    ]) +
    '\n```';
  const cap = makeCaptureLogger();
  const facts = parseFactsResponse(raw, cap.logger);
  assert(facts.length === 1, 'multi-tag + fence: parses');
  assert(cap.warns.length === 0, 'multi-tag + fence: no parse-error warning');
}

// 2.2.5: bracket-scan recovery — prose wraps a valid JSON array.
{
  const raw =
    'Here are the extracted facts I found in this conversation:\n\n' +
    JSON.stringify([
      { text: 'Always check d.get(errors) on subgraph queries', type: 'rule', importance: 8, action: 'ADD' },
    ]) +
    '\n\nLet me know if you want me to add more.';
  const cap = makeCaptureLogger();
  const facts = parseFactsResponse(raw, cap.logger);
  assert(facts.length === 1, 'prose-wrapper: recovered 1 fact via bracket-scan');
  assert(facts[0].type === 'directive', 'prose-wrapper: v0 rule → v1 directive');
  assert(
    cap.infos.some((m) => m.includes('bracket-scan fallback')),
    'prose-wrapper: info log announces recovery path',
  );
  assert(cap.warns.length === 0, 'prose-wrapper: no parse-error warning on successful recovery');
}

// 2.2.5: genuine parse failure — logs WARN with preview, returns empty.
{
  const raw = 'The model just rambled and never emitted any JSON at all. Nothing to parse here.';
  const cap = makeCaptureLogger();
  const facts = parseFactsResponse(raw, cap.logger);
  assert(facts.length === 0, 'parse-failure: returns empty array');
  assert(
    cap.warns.some((m) => m.startsWith('parseFactsResponse: could not parse')),
    'parse-failure: warn-level log surfaces the failure',
  );
  assert(
    cap.warns.some((m) => m.includes('rambled')),
    'parse-failure: preview includes actual response content',
  );
}

// 2.2.5: legacy silent behavior preserved when no logger is passed.
{
  const raw = 'nothing parseable here';
  const facts = parseFactsResponse(raw); // no logger
  assert(facts.length === 0, 'no-logger: returns empty array (legacy silent path)');
}

// Single-object payload (not an array) — v1 parser auto-wraps it into a
// 1-element fact list so marginal LLM outputs still recover gracefully.
{
  const raw = JSON.stringify({ text: 'A single object, not an array', type: 'fact', importance: 7 });
  const cap = makeCaptureLogger();
  const facts = parseFactsResponse(raw, cap.logger);
  assert(facts.length === 1, 'single-object: auto-wrapped into 1 fact');
  assert(facts[0].type === 'claim', 'single-object: v0 "fact" coerced to v1 "claim"');
  assert(cap.warns.length === 0, 'single-object: no warn (graceful recovery)');
}

// 2.2.5: thinking tag that wraps WITHOUT closing — should not break the parser.
// (Some models emit malformed tags when they hit a token limit.)
{
  const raw =
    '<think>unterminated reasoning that goes on forever but eventually' +
    JSON.stringify([
      { text: 'Fallback content that should still extract', type: 'fact', importance: 7, action: 'ADD' },
    ]);
  const cap = makeCaptureLogger();
  const facts = parseFactsResponse(raw, cap.logger);
  // Unclosed think tag won't match the strip regex; we rely on bracket-scan fallback.
  assert(facts.length === 1, 'unclosed-think: bracket-scan fallback recovers the JSON');
  assert(
    cap.infos.some((m) => m.includes('bracket-scan')),
    'unclosed-think: info log announces recovery',
  );
}

// ---------------------------------------------------------------------------
// Phase 2.2.6: lexical importance bump
// ---------------------------------------------------------------------------

import { computeLexicalImportanceBump } from './extractor.ts';

{
  const conv = '[user]: I prefer Vim. Note to self: this is a rule of thumb for the team.';
  const bump = computeLexicalImportanceBump('User prefers Vim', conv);
  assert(bump >= 1, 'bump: strong-intent ("rule of thumb", "note to self") gives +1');
}

{
  const conv = '[user]: I really love dark mode!! Use dark mode in IDEs.';
  const bump = computeLexicalImportanceBump('User loves dark mode', conv);
  assert(bump >= 1, 'bump: !! emphasis gives +1');
}

{
  const conv = '[user]: NEVER FORGET DARK MODE. Always use it.';
  const bump = computeLexicalImportanceBump('User always uses dark mode', conv);
  assert(bump >= 2, 'bump: ALL CAPS phrase + intent ("never forget") give +2');
}

{
  const conv = '[user]: I prefer PostgreSQL. ... [user]: yeah PostgreSQL is right for OLTP. ... [user]: PostgreSQL all the way.';
  const bump = computeLexicalImportanceBump('User prefers PostgreSQL', conv);
  assert(bump >= 1, 'bump: repetition (3+ mentions) gives +1');
}

{
  const conv = '[user]: I think I might use VS Code. Not sure yet.';
  const bump = computeLexicalImportanceBump('User uses VS Code', conv);
  assert(bump === 0, 'bump: tentative conversation gives 0');
}

{
  const conv = '[user]: REMEMBER THIS!! Critical rule of thumb: never ever use sudo rm -rf. NEVER FORGET that.';
  const bump = computeLexicalImportanceBump('Never use sudo rm -rf', conv);
  assert(bump === 2, `bump: capped at +2 even with multiple signals (got ${bump})`);
}

{
  const conv = '[user]: a b c d. a b c d. a b c d.';
  const bump = computeLexicalImportanceBump('hi', conv); // fact text too short for fingerprint
  assert(bump === 0, 'bump: short fact fingerprint (< 5 chars) skips repetition check');
}

// ---------------------------------------------------------------------------
// Summary
// ---------------------------------------------------------------------------

console.log(`\n# ${passed}/${passed + failed} passed`);
if (failed > 0) {
  console.log('\nSOME TESTS FAILED');
  process.exit(1);
} else {
  console.log('\nALL TESTS PASSED');
}

export {};
