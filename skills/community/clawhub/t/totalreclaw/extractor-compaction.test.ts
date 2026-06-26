/**
 * Tests for compaction-aware extraction (Phase 2.3).
 *
 * Validates that parseFactsResponseForCompaction uses importance >= 5
 * threshold and that the COMPACTION_SYSTEM_PROMPT is distinct from
 * EXTRACTION_SYSTEM_PROMPT.
 *
 * Run with: npx tsx extractor-compaction.test.ts
 */

import {
  parseFactsResponse,
  parseFactsResponseForCompaction,
  EXTRACTION_SYSTEM_PROMPT,
  COMPACTION_SYSTEM_PROMPT,
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
// Prompt constants are distinct
// ---------------------------------------------------------------------------

assert(
  COMPACTION_SYSTEM_PROMPT !== EXTRACTION_SYSTEM_PROMPT,
  'prompts: COMPACTION_SYSTEM_PROMPT is distinct from EXTRACTION_SYSTEM_PROMPT',
);

assert(
  COMPACTION_SYSTEM_PROMPT.includes('5+ = worth storing'),
  'prompts: compaction prompt mentions importance 5+ threshold',
);

assert(
  COMPACTION_SYSTEM_PROMPT.includes('LAST CHANCE'),
  'prompts: compaction prompt emphasizes urgency',
);

assert(
  COMPACTION_SYSTEM_PROMPT.toLowerCase().includes('format-agnostic'),
  'prompts: compaction prompt includes format-agnostic guidance',
);

assert(
  COMPACTION_SYSTEM_PROMPT.includes('bullet lists'),
  'prompts: compaction prompt mentions bullet format handling',
);

assert(
  COMPACTION_SYSTEM_PROMPT.includes('plain prose'),
  'prompts: compaction prompt mentions prose format handling',
);

assert(
  COMPACTION_SYSTEM_PROMPT.includes("Do NOT skip content just because it's in a summary"),
  'prompts: compaction prompt includes anti-pattern guidance',
);

// ---------------------------------------------------------------------------
// Importance threshold: compaction accepts >= 5, regular rejects < 6
// ---------------------------------------------------------------------------

{
  const factsWithImportance5 = JSON.stringify([
    {
      text: 'Working on the Fly.io migration project',
      type: 'context',
      importance: 5,
      confidence: 0.85,
      action: 'ADD',
    },
    {
      text: 'User prefers dark mode in all editors',
      type: 'preference',
      importance: 6,
      confidence: 0.9,
      action: 'ADD',
    },
    {
      text: 'Chose PostgreSQL because data is relational',
      type: 'decision',
      importance: 8,
      confidence: 0.95,
      action: 'ADD',
    },
    {
      text: 'Ephemeral greeting text not worth storing',
      type: 'fact',
      importance: 4,
      confidence: 0.5,
      action: 'ADD',
    },
  ]);

  // Compaction parser: should keep importance >= 5 (3 facts, drop the 4)
  const compactionFacts = parseFactsResponseForCompaction(factsWithImportance5);
  assert(compactionFacts.length === 3, 'compaction threshold: keeps 3 facts (importance >= 5)');
  assert(
    compactionFacts.some((f) => f.importance === 5),
    'compaction threshold: importance-5 fact is kept',
  );
  assert(
    !compactionFacts.some((f) => f.importance === 4),
    'compaction threshold: importance-4 fact is dropped',
  );

  // Regular parser: should only keep importance >= 6 (2 facts)
  const regularFacts = parseFactsResponse(factsWithImportance5);
  assert(regularFacts.length === 2, 'regular threshold: keeps 2 facts (importance >= 6)');
  assert(
    !regularFacts.some((f) => f.importance === 5),
    'regular threshold: importance-5 fact is dropped by regular parser',
  );
}

// ---------------------------------------------------------------------------
// Bullet-list format extracts correctly through compaction parser
// ---------------------------------------------------------------------------

{
  const bulletListResponse = JSON.stringify([
    {
      text: 'Migrating from Heroku to Fly.io, Django monolith',
      type: 'context',
      importance: 7,
      confidence: 0.9,
      action: 'ADD',
      entities: [
        { name: 'Heroku', type: 'tool' },
        { name: 'Fly.io', type: 'tool' },
        { name: 'Django', type: 'tool' },
      ],
    },
    {
      text: 'Will run a 2-week spike on Fly.io with one Celery worker first',
      type: 'decision',
      importance: 8,
      confidence: 0.95,
      action: 'ADD',
      entities: [
        { name: 'Fly.io', type: 'tool' },
        { name: 'Celery', type: 'tool' },
      ],
    },
    {
      text: "Fly.io internal DNS doesn't resolve the same as Heroku — service discovery needs explicit config",
      type: 'rule',
      importance: 8,
      confidence: 1.0,
      action: 'ADD',
      entities: [{ name: 'Fly.io', type: 'tool' }],
    },
  ]);

  const facts = parseFactsResponseForCompaction(bulletListResponse);
  assert(facts.length === 3, 'bullet-list: all 3 facts extracted');

  // v1 coercion: context → claim, decision → claim, rule → directive
  const types = facts.map((f) => f.type).sort();
  assert(types.includes('claim'), 'bullet-list: claim type present (v0 context/decision → v1 claim)');
  assert(types.includes('directive'), 'bullet-list: directive type present (v0 rule → v1 directive)');

  // Entities preserved — look for a claim fact with 3 entities (the v0 context).
  const entityRich = facts.find((f) => f.entities && f.entities.length === 3);
  assert(
    entityRich !== undefined,
    'bullet-list: the entity-rich fact has 3 entities',
  );
}

// ---------------------------------------------------------------------------
// Prose format extracts correctly through compaction parser
// ---------------------------------------------------------------------------

{
  const proseResponse = JSON.stringify([
    {
      text: 'JWT tokens were producing 401 errors due to an off-by-one error in the refresh handler',
      type: 'episodic',
      importance: 7,
      confidence: 0.95,
      action: 'ADD',
      entities: [{ name: 'JWT', type: 'tool' }],
    },
    {
      text: 'Fixed the JWT refresh off-by-one bug and added a 30-second buffer to the expiry check',
      type: 'decision',
      importance: 8,
      confidence: 0.95,
      action: 'ADD',
    },
    {
      text: 'User wants to move to refresh tokens with sliding expiry rather than fixed expiry',
      type: 'preference',
      importance: 7,
      confidence: 0.9,
      action: 'ADD',
    },
    {
      text: 'Flask-JWT-Extended defaults to fixed expiry; sliding expiry requires JWT_REFRESH_TOKEN_EXPIRES_DELTA',
      type: 'rule',
      importance: 8,
      confidence: 1.0,
      action: 'ADD',
      entities: [{ name: 'Flask-JWT-Extended', type: 'tool' }],
    },
    {
      text: 'Revisit the JWT fixed-vs-sliding expiry decision after the Q2 security review',
      type: 'goal',
      importance: 7,
      confidence: 0.9,
      action: 'ADD',
    },
  ]);

  const facts = parseFactsResponseForCompaction(proseResponse);
  assert(facts.length === 5, 'prose: all 5 facts extracted from prose-style response');

  // v1 coercion: episodic → episode, decision → claim, rule → directive, goal → commitment
  const typeSet = new Set(facts.map((f) => f.type));
  assert(typeSet.has('episode'), 'prose: episode type present (v0 episodic → v1 episode)');
  assert(typeSet.has('claim'), 'prose: claim type present (v0 decision → v1 claim)');
  assert(typeSet.has('preference'), 'prose: preference type preserved');
  assert(typeSet.has('directive'), 'prose: directive type present (v0 rule → v1 directive)');
  assert(typeSet.has('commitment'), 'prose: commitment type present (v0 goal → v1 commitment)');
}

// ---------------------------------------------------------------------------
// Mixed format (bullets + prose) — both types extract
// ---------------------------------------------------------------------------

{
  const mixedResponse = JSON.stringify([
    {
      text: 'Running Django on Fly.io with 2 worker instances',
      type: 'context',
      importance: 5,
      confidence: 0.8,
      action: 'ADD',
    },
    {
      text: 'Auth system uses JWT with 30-second refresh buffer',
      type: 'fact',
      importance: 7,
      confidence: 0.9,
      action: 'ADD',
    },
    {
      text: 'Celery task routing needs explicit Fly Redis connection pool config',
      type: 'rule',
      importance: 8,
      confidence: 1.0,
      action: 'ADD',
    },
  ]);

  const facts = parseFactsResponseForCompaction(mixedResponse);
  assert(facts.length === 3, 'mixed: all 3 facts from mixed format extracted');
  assert(
    facts.some((f) => f.importance === 5),
    'mixed: importance-5 fact kept in compaction mode',
  );
}

// ---------------------------------------------------------------------------
// DELETE actions pass regardless of importance (same as regular)
// ---------------------------------------------------------------------------

{
  const deleteResponse = JSON.stringify([
    {
      text: 'User no longer uses Heroku — migrated to Fly.io',
      type: 'context',
      importance: 3,
      action: 'DELETE',
      existingFactId: 'abc-123',
    },
  ]);

  const compactionFacts = parseFactsResponseForCompaction(deleteResponse);
  assert(
    compactionFacts.length === 1,
    'delete: DELETE action passes even with importance 3 in compaction',
  );
  assertEq(compactionFacts[0]?.action, 'DELETE', 'delete: action is DELETE');
  assertEq(
    compactionFacts[0]?.existingFactId,
    'abc-123',
    'delete: existingFactId preserved',
  );
}

// ---------------------------------------------------------------------------
// Think-tag stripping works in compaction parser too
// ---------------------------------------------------------------------------

{
  const thinkTagResponse = `<think>
Let me analyze this conversation for extractable memories...
The user mentioned they prefer Vim over VS Code.
</think>
[{"text": "User prefers Vim over VS Code for coding", "type": "preference", "importance": 5, "confidence": 0.9, "action": "ADD", "entities": [{"name": "Vim", "type": "tool"}]}]`;

  const facts = parseFactsResponseForCompaction(thinkTagResponse);
  assert(facts.length === 1, 'think-tag: compaction parser strips think tags');
  assert(facts[0]?.importance === 5, 'think-tag: importance-5 fact kept in compaction');
  assert(facts[0]?.type === 'preference', 'think-tag: type preserved');
}

// ---------------------------------------------------------------------------
// Prose-wrapped JSON recovery works in compaction parser
// ---------------------------------------------------------------------------

{
  const proseWrapped = `Here are the memories I extracted from the conversation:

[{"text": "Using Redis for session caching on production", "type": "context", "importance": 6, "confidence": 0.85, "action": "ADD"}]

I hope this captures the key points.`;

  const logs: string[] = [];
  const mockLogger = {
    info: (msg: string) => logs.push(msg),
    warn: (msg: string) => logs.push(`WARN: ${msg}`),
  };

  const facts = parseFactsResponseForCompaction(proseWrapped, mockLogger);
  assert(facts.length === 1, 'prose-wrapped: bracket-scan recovery works in compaction parser');
  assert(
    logs.some((l) => l.includes('bracket-scan')),
    'prose-wrapped: recovery logged',
  );
}

// ---------------------------------------------------------------------------
// Confidence preserved and clamped in compaction parser
// ---------------------------------------------------------------------------

{
  const confidenceResponse = JSON.stringify([
    {
      text: 'User is working on Django auth system',
      type: 'context',
      importance: 5,
      confidence: 0.72,
      action: 'ADD',
    },
    {
      text: 'Sarah manages the infrastructure team',
      type: 'fact',
      importance: 6,
      action: 'ADD',
      // confidence omitted — should default to 0.85
    },
  ]);

  const facts = parseFactsResponseForCompaction(confidenceResponse);
  assert(facts.length === 2, 'confidence: both facts parsed');
  assert(facts[0]?.confidence === 0.72, 'confidence: explicit value preserved');
  assert(facts[1]?.confidence === 0.85, 'confidence: missing defaults to 0.85');
}

// ---------------------------------------------------------------------------
// Summary
// ---------------------------------------------------------------------------

console.log('');
console.log(`# ${passed}/${passed + failed} passed`);
if (failed > 0) {
  console.log('');
  console.log(`FAILED: ${failed} test(s)`);
  process.exit(1);
} else {
  console.log('');
  console.log('ALL TESTS PASSED');
}
