/**
 * Unit tests for import adapters.
 *
 * Run with: npx tsx import-adapters/import-adapters.test.ts
 *
 * Uses TAP-style output (no test framework dependency).
 *
 * ChatGPT and Claude adapters return conversation CHUNKS (not facts).
 * Fact extraction is delegated to the LLM via extractFacts().
 * Mem0 and MCP Memory adapters return pre-structured facts.
 */

import { Mem0Adapter } from './mem0-adapter.js';
import { MCPMemoryAdapter } from './mcp-memory-adapter.js';
import { ChatGPTAdapter } from './chatgpt-adapter.js';
import { ClaudeAdapter } from './claude-adapter.js';
import { GeminiAdapter } from './gemini-adapter.js';
import { BaseImportAdapter } from './base-adapter.js';
import { getAdapter } from './index.js';
import type {
  NormalizedFact,
  AdapterParseResult,
  ImportSource,
  ProgressCallback,
} from './types.js';
import fs from 'node:fs';
import os from 'node:os';

// ---------------------------------------------------------------------------
// TAP Helpers
// ---------------------------------------------------------------------------

let passed = 0;
let failed = 0;
let testNum = 0;

function assert(condition: boolean, message: string): void {
  testNum++;
  if (condition) {
    passed++;
    console.log(`ok ${testNum} - ${message}`);
  } else {
    failed++;
    console.log(`not ok ${testNum} - ${message}`);
  }
}

function assertThrows(fn: () => void, message: string): void {
  try {
    fn();
    failed++;
    testNum++;
    console.log(`not ok ${testNum} - ${message} (did not throw)`);
  } catch {
    passed++;
    testNum++;
    console.log(`ok ${testNum} - ${message}`);
  }
}

// ---------------------------------------------------------------------------
// Concrete subclass to test protected BaseImportAdapter.validateFact()
// ---------------------------------------------------------------------------

class TestAdapter extends BaseImportAdapter {
  readonly source: ImportSource = 'mem0';
  readonly displayName = 'Test Adapter';

  async parse(): Promise<AdapterParseResult> {
    return { facts: [], chunks: [], totalMessages: 0, warnings: [], errors: [] };
  }

  // Expose protected methods for testing
  public testValidateFact(fact: Partial<NormalizedFact>): NormalizedFact | null {
    return this.validateFact(fact);
  }

  public testValidateFacts(
    rawFacts: Partial<NormalizedFact>[],
  ): { facts: NormalizedFact[]; invalidCount: number } {
    return this.validateFacts(rawFacts);
  }
}

// ---------------------------------------------------------------------------
// Tests
// ---------------------------------------------------------------------------

async function runTests(): Promise<void> {
  // =========================================================================
  // Mem0Adapter
  // =========================================================================

  console.log('# Mem0Adapter');

  // --- parses API response format ---
  {
    const content = JSON.stringify({
      results: [
        { id: 'mem-1', memory: 'User prefers dark mode', categories: ['preference'] },
        { id: 'mem-2', memory: 'User works at Acme Corp', categories: ['fact'] },
      ],
    });

    const adapter = new Mem0Adapter();
    const result = await adapter.parse({ content });

    assert(result.facts.length === 2, 'Mem0: API response format yields 2 facts');
    assert(result.facts[0].text === 'User prefers dark mode', 'Mem0: first fact text correct');
    assert(result.facts[0].type === 'preference', 'Mem0: preference category mapped');
    assert(result.facts[0].source === 'mem0', 'Mem0: source is mem0');
    assert(result.facts[1].type === 'fact', 'Mem0: fact category mapped');
    assert(result.facts[1].sourceId === 'mem-2', 'Mem0: sourceId preserved');
    assert(result.chunks.length === 0, 'Mem0: no chunks (pre-structured source)');
  }

  // --- parses export file format ---
  {
    const content = JSON.stringify({
      export_date: '2026-03-10',
      memories: [
        { id: 'mem-1', memory: 'User likes TypeScript' },
      ],
    });

    const adapter = new Mem0Adapter();
    const result = await adapter.parse({ content });

    assert(result.facts.length === 1, 'Mem0: export file format yields 1 fact');
    assert(result.facts[0].text === 'User likes TypeScript', 'Mem0: export fact text correct');
  }

  // --- parses bare array format ---
  {
    const content = JSON.stringify([
      { id: 'mem-1', memory: 'User prefers Python' },
      { id: 'mem-2', memory: 'User dislikes Java' },
    ]);

    const adapter = new Mem0Adapter();
    const result = await adapter.parse({ content });

    assert(result.facts.length === 2, 'Mem0: bare array yields 2 facts');
    assert(result.facts[0].text === 'User prefers Python', 'Mem0: bare array first fact correct');
  }

  // --- skips empty/short memories ---
  {
    const content = JSON.stringify({
      results: [
        { id: 'mem-1', memory: '' },
        { id: 'mem-2', memory: 'Valid fact here' },
        { id: 'mem-3', memory: 'ab' }, // too short (< 3 chars)
      ],
    });

    const adapter = new Mem0Adapter();
    const result = await adapter.parse({ content });

    assert(result.facts.length === 1, 'Mem0: skips empty/short memories, keeps 1 valid');
    assert(result.facts[0].text === 'Valid fact here', 'Mem0: only valid fact kept');
    const hasWarning = result.warnings.some((w) => w.includes('2 memories had invalid'));
    assert(hasWarning, 'Mem0: warning about 2 invalid memories');
  }

  // --- returns errors on invalid JSON ---
  {
    const adapter = new Mem0Adapter();
    const result = await adapter.parse({ content: 'not json {{{' });

    assert(result.facts.length === 0, 'Mem0: invalid JSON yields 0 facts');
    assert(result.errors.length > 0, 'Mem0: invalid JSON produces error');
    assert(
      result.errors[0].includes('Failed to parse Mem0 JSON'),
      'Mem0: error message mentions JSON parse failure',
    );
  }

  // --- returns error when no content or api_key ---
  {
    const adapter = new Mem0Adapter();
    const result = await adapter.parse({});

    assert(result.facts.length === 0, 'Mem0: no input yields 0 facts');
    assert(result.errors.length > 0, 'Mem0: no input produces error');
    assert(
      result.errors[0].includes('requires either content'),
      'Mem0: error message mentions required input',
    );
  }

  // --- category mapping ---
  {
    const content = JSON.stringify({
      results: [
        { id: '1', memory: 'User likes hiking', categories: ['like'] },
        { id: '2', memory: 'User dislikes rain', categories: ['dislike'] },
        { id: '3', memory: 'Graduated in 2020', categories: ['biographical'] },
        { id: '4', memory: 'Wants to learn Rust', categories: ['objective'] },
        { id: '5', memory: 'Visited Paris in 2023', categories: ['event'] },
        { id: '6', memory: 'Chose React over Vue', categories: ['decision'] },
        { id: '7', memory: 'Some unknown category', categories: ['zzz_unknown'] },
      ],
    });

    const adapter = new Mem0Adapter();
    const result = await adapter.parse({ content });

    assert(result.facts[0].type === 'preference', 'Mem0: "like" -> preference');
    assert(result.facts[1].type === 'preference', 'Mem0: "dislike" -> preference');
    assert(result.facts[2].type === 'fact', 'Mem0: "biographical" -> fact');
    assert(result.facts[3].type === 'goal', 'Mem0: "objective" -> goal');
    assert(result.facts[4].type === 'episodic', 'Mem0: "event" -> episodic');
    assert(result.facts[5].type === 'decision', 'Mem0: "decision" -> decision');
    assert(result.facts[6].type === 'fact', 'Mem0: unknown category defaults to fact');
  }

  // --- importance defaults to 6 ---
  {
    const content = JSON.stringify({
      results: [
        { id: 'mem-1', memory: 'User prefers dark mode' },
      ],
    });

    const adapter = new Mem0Adapter();
    const result = await adapter.parse({ content });

    assert(result.facts[0].importance === 6, 'Mem0: default importance is 6');
  }

  // --- handles unrecognized format ---
  {
    const content = JSON.stringify({ some_key: 'some_value' });

    const adapter = new Mem0Adapter();
    const result = await adapter.parse({ content });

    assert(result.facts.length === 0, 'Mem0: unrecognized format yields 0 facts');
    assert(
      result.errors.some((e) => e.includes('Unrecognized Mem0 format')),
      'Mem0: unrecognized format error message',
    );
  }

  // =========================================================================
  // MCPMemoryAdapter
  // =========================================================================

  console.log('# MCPMemoryAdapter');

  // --- parses entities with observations ---
  {
    const content = [
      JSON.stringify({ type: 'entity', name: 'John', entityType: 'person', observations: ['Works at Acme Corp', 'Prefers TypeScript'] }),
      JSON.stringify({ type: 'entity', name: 'Project Alpha', entityType: 'project', observations: ['Uses React'] }),
    ].join('\n');

    const adapter = new MCPMemoryAdapter();
    const result = await adapter.parse({ content });

    assert(result.facts.length === 3, 'MCP: 2 entities with 3 total observations -> 3 facts');
    assert(result.facts[0].text.includes('John'), 'MCP: first fact includes entity name');
    assert(result.facts[0].text.includes('Acme Corp'), 'MCP: first fact includes observation');
    assert(result.facts[1].text.includes('TypeScript'), 'MCP: second fact includes TypeScript');
    assert(result.facts[0].source === 'mcp-memory', 'MCP: source is mcp-memory');
    assert(result.chunks.length === 0, 'MCP: no chunks (pre-structured source)');
  }

  // --- contextualizes observations correctly ---
  {
    const content = [
      JSON.stringify({
        type: 'entity', name: 'John', entityType: 'person',
        observations: [
          'works at Acme Corp',       // lowercase verb -> "John works at Acme Corp"
          'John likes TypeScript',     // already starts with name -> unchanged
          'He prefers React',          // pronoun -> replaced: "John prefers React"
          'An avid hiker',             // uppercase start -> "John: An avid hiker"
        ],
      }),
    ].join('\n');

    const adapter = new MCPMemoryAdapter();
    const result = await adapter.parse({ content });

    assert(result.facts.length === 4, 'MCP: 4 observations -> 4 facts');
    assert(result.facts[0].text === 'John works at Acme Corp', 'MCP: lowercase verb prefixed with entity name');
    assert(result.facts[1].text === 'John likes TypeScript', 'MCP: already has entity name, unchanged');
    assert(result.facts[2].text === 'John prefers React', 'MCP: pronoun "He" replaced with entity name');
    assert(result.facts[3].text === 'John: An avid hiker', 'MCP: uppercase standalone sentence prefixed with colon');
  }

  // --- parses relations ---
  {
    const content = [
      JSON.stringify({ type: 'entity', name: 'John', entityType: 'person', observations: ['Developer'] }),
      JSON.stringify({ type: 'entity', name: 'Project Alpha', entityType: 'project', observations: ['Deadline March'] }),
      JSON.stringify({ type: 'relation', from: 'John', to: 'Project Alpha', relationType: 'works_on' }),
    ].join('\n');

    const adapter = new MCPMemoryAdapter();
    const result = await adapter.parse({ content });

    // 2 observations + 1 relation = 3 facts
    assert(result.facts.length === 3, 'MCP: 2 observations + 1 relation = 3 facts');
    assert(
      result.facts[2].text === 'John works on Project Alpha',
      'MCP: relation converted to human-readable text',
    );
    assert(result.facts[2].type === 'fact', 'MCP: relation type defaults to fact');
  }

  // --- later entity overrides earlier (append-only semantics) ---
  {
    const content = [
      JSON.stringify({ type: 'entity', name: 'John', entityType: 'person', observations: ['Old observation'] }),
      JSON.stringify({ type: 'entity', name: 'John', entityType: 'person', observations: ['New observation'] }),
    ].join('\n');

    const adapter = new MCPMemoryAdapter();
    const result = await adapter.parse({ content });

    // Only the later entity should be used (Map overwrites)
    assert(result.facts.length === 1, 'MCP: duplicate entity keeps only latest');
    assert(
      result.facts[0].text.includes('New observation'),
      'MCP: latest entity observations used',
    );
  }

  // --- warns on orphaned relations ---
  {
    const content = [
      JSON.stringify({ type: 'relation', from: 'Unknown', to: 'Also Unknown', relationType: 'knows' }),
    ].join('\n');

    const adapter = new MCPMemoryAdapter();
    const result = await adapter.parse({ content });

    const hasWarning = result.warnings.some((w) => w.includes('unknown entity'));
    assert(hasWarning, 'MCP: warns on orphaned relation with unknown entities');
    // Orphaned relation should not produce a fact
    assert(result.facts.length === 0, 'MCP: orphaned relation produces no facts');
  }

  // --- handles empty/blank lines in JSONL ---
  {
    const content = [
      '',
      JSON.stringify({ type: 'entity', name: 'Alice', entityType: 'person', observations: ['Likes coffee'] }),
      '   ',
      JSON.stringify({ type: 'entity', name: 'Bob', entityType: 'person', observations: ['Likes tea'] }),
      '',
    ].join('\n');

    const adapter = new MCPMemoryAdapter();
    const result = await adapter.parse({ content });

    assert(result.facts.length === 2, 'MCP: blank lines in JSONL are skipped');
    assert(result.errors.length === 0, 'MCP: blank lines do not produce errors');
  }

  // --- invalid JSON lines produce errors ---
  {
    const content = [
      JSON.stringify({ type: 'entity', name: 'Alice', entityType: 'person', observations: ['Valid'] }),
      'this is not json',
      JSON.stringify({ type: 'entity', name: 'Bob', entityType: 'person', observations: ['Also valid'] }),
    ].join('\n');

    const adapter = new MCPMemoryAdapter();
    const result = await adapter.parse({ content });

    assert(result.facts.length === 2, 'MCP: valid facts parsed despite invalid line');
    assert(result.errors.length === 1, 'MCP: one error for the invalid JSON line');
    assert(result.errors[0].includes('Line 2'), 'MCP: error references correct line number');
  }

  // --- entity type mapping ---
  {
    const content = [
      JSON.stringify({ type: 'entity', name: 'React', entityType: 'tool', observations: ['Frontend framework'] }),
      JSON.stringify({ type: 'entity', name: 'Launch', entityType: 'goal', observations: ['Ship by March'] }),
      JSON.stringify({ type: 'entity', name: 'Meeting', entityType: 'event', observations: ['Quarterly review'] }),
      JSON.stringify({ type: 'entity', name: 'PickedAWS', entityType: 'decision', observations: ['Over GCP'] }),
    ].join('\n');

    const adapter = new MCPMemoryAdapter();
    const result = await adapter.parse({ content });

    assert(result.facts[0].type === 'preference', 'MCP: "tool" entityType -> preference');
    assert(result.facts[1].type === 'goal', 'MCP: "goal" entityType -> goal');
    assert(result.facts[2].type === 'episodic', 'MCP: "event" entityType -> episodic');
    assert(result.facts[3].type === 'decision', 'MCP: "decision" entityType -> decision');
  }

  // --- no content and no file_path (and no default file) ---
  {
    const adapter = new MCPMemoryAdapter();
    // Pass a non-existent file_path to trigger the file read error path
    const result = await adapter.parse({ file_path: '/tmp/definitely-does-not-exist-totalreclaw-test.jsonl' });

    assert(result.facts.length === 0, 'MCP: missing file yields 0 facts');
    assert(result.errors.length > 0, 'MCP: missing file produces error');
  }

  // --- relation type humanization ---
  {
    const content = [
      JSON.stringify({ type: 'entity', name: 'A', entityType: 'person', observations: ['exists'] }),
      JSON.stringify({ type: 'entity', name: 'B', entityType: 'project', observations: ['exists'] }),
      JSON.stringify({ type: 'relation', from: 'A', to: 'B', relationType: 'MEMBER_OF' }),
    ].join('\n');

    const adapter = new MCPMemoryAdapter();
    const result = await adapter.parse({ content });

    const relFact = result.facts.find((f) => f.tags?.includes('relation'));
    assert(
      relFact?.text === 'A is a member of B',
      `MCP: MEMBER_OF humanized to "is a member of" (got: ${relFact?.text})`,
    );
  }

  // =========================================================================
  // BaseImportAdapter (via TestAdapter)
  // =========================================================================

  console.log('# BaseImportAdapter');

  const testAdapter = new TestAdapter();

  // --- text validation: minimum 3 chars ---
  {
    assert(testAdapter.testValidateFact({ text: '' }) === null, 'Base: empty text returns null');
    assert(testAdapter.testValidateFact({ text: 'ab' }) === null, 'Base: 2-char text returns null');
    assert(testAdapter.testValidateFact({ text: '   ' }) === null, 'Base: whitespace-only text returns null');
    assert(testAdapter.testValidateFact({ text: 'a  ' }) === null, 'Base: 1-char trimmed text returns null');

    const result = testAdapter.testValidateFact({ text: 'abc' });
    assert(result !== null, 'Base: 3-char text is valid');
    assert(result?.text === 'abc', 'Base: 3-char text preserved');
  }

  // --- text truncation at 512 chars ---
  {
    const longText = 'x'.repeat(600);
    const result = testAdapter.testValidateFact({ text: longText });

    assert(result !== null, 'Base: long text is valid');
    assert(result!.text.length === 512, `Base: text truncated to 512 chars (got ${result!.text.length})`);
  }

  // --- text is trimmed ---
  {
    const result = testAdapter.testValidateFact({ text: '  hello world  ' });
    assert(result !== null, 'Base: padded text is valid');
    assert(result!.text === 'hello world', 'Base: text is trimmed');
  }

  // --- type normalization ---
  {
    const validTypes = ['fact', 'preference', 'decision', 'episodic', 'goal', 'context', 'summary'] as const;

    for (const t of validTypes) {
      const result = testAdapter.testValidateFact({ text: 'test fact', type: t });
      assert(result?.type === t, `Base: type "${t}" preserved`);
    }

    const invalidResult = testAdapter.testValidateFact({ text: 'test fact', type: 'bogus' as any });
    assert(invalidResult?.type === 'fact', 'Base: invalid type defaults to "fact"');

    const missingResult = testAdapter.testValidateFact({ text: 'test fact' });
    assert(missingResult?.type === 'fact', 'Base: missing type defaults to "fact"');
  }

  // --- importance scale conversion (0-1 -> 1-10) ---
  {
    // 0-1 scale conversion
    const r0 = testAdapter.testValidateFact({ text: 'test fact', importance: 0.0 });
    assert(r0?.importance === 1, `Base: importance 0.0 -> 1 (got ${r0?.importance})`);

    const r05 = testAdapter.testValidateFact({ text: 'test fact', importance: 0.5 });
    assert(r05?.importance === 5, `Base: importance 0.5 -> 5 (got ${r05?.importance})`);

    const r1 = testAdapter.testValidateFact({ text: 'test fact', importance: 1.0 });
    assert(r1?.importance === 10, `Base: importance 1.0 -> 10 (got ${r1?.importance})`);

    const r03 = testAdapter.testValidateFact({ text: 'test fact', importance: 0.3 });
    assert(r03?.importance === 3, `Base: importance 0.3 -> 3 (got ${r03?.importance})`);

    const r08 = testAdapter.testValidateFact({ text: 'test fact', importance: 0.8 });
    assert(r08?.importance === 8, `Base: importance 0.8 -> 8 (got ${r08?.importance})`);
  }

  // --- importance already on 1-10 scale ---
  {
    const r5 = testAdapter.testValidateFact({ text: 'test fact', importance: 5 });
    assert(r5?.importance === 5, `Base: importance 5 stays 5 (got ${r5?.importance})`);

    const r10 = testAdapter.testValidateFact({ text: 'test fact', importance: 10 });
    assert(r10?.importance === 10, `Base: importance 10 stays 10 (got ${r10?.importance})`);

    const r7 = testAdapter.testValidateFact({ text: 'test fact', importance: 7 });
    assert(r7?.importance === 7, `Base: importance 7 stays 7 (got ${r7?.importance})`);
  }

  // --- importance clamping ---
  {
    const rNeg = testAdapter.testValidateFact({ text: 'test fact', importance: -5 });
    assert(rNeg?.importance === 1, `Base: importance -5 clamped to 1 (got ${rNeg?.importance})`);

    const rHuge = testAdapter.testValidateFact({ text: 'test fact', importance: 100 });
    assert(rHuge?.importance === 10, `Base: importance 100 clamped to 10 (got ${rHuge?.importance})`);
  }

  // --- importance default ---
  {
    const rDefault = testAdapter.testValidateFact({ text: 'test fact' });
    assert(rDefault?.importance === 5, `Base: missing importance defaults to 5 (got ${rDefault?.importance})`);
  }

  // --- source defaults to adapter's source ---
  {
    const result = testAdapter.testValidateFact({ text: 'test fact' });
    assert(result?.source === 'mem0', 'Base: source defaults to adapter source');

    const withSource = testAdapter.testValidateFact({ text: 'test fact', source: 'mcp-memory' });
    assert(withSource?.source === 'mcp-memory', 'Base: explicit source preserved');
  }

  // --- validateFacts batch ---
  {
    const rawFacts: Partial<NormalizedFact>[] = [
      { text: 'Valid fact one' },
      { text: '' },               // invalid
      { text: 'Valid fact two' },
      { text: 'xy' },             // too short
      { text: 'Valid fact three' },
    ];

    const { facts, invalidCount } = testAdapter.testValidateFacts(rawFacts);
    assert(facts.length === 3, `Base: validateFacts keeps 3 valid out of 5 (got ${facts.length})`);
    assert(invalidCount === 2, `Base: validateFacts counts 2 invalid (got ${invalidCount})`);
  }

  // =========================================================================
  // ChatGPTAdapter — conversations.json (returns chunks, not facts)
  // =========================================================================

  console.log('# ChatGPTAdapter — conversations.json (chunks)');

  // --- returns conversation chunks with user + assistant messages ---
  {
    const conversations = [
      {
        id: 'conv-1',
        title: 'Test Conversation',
        create_time: 1700000000,
        mapping: {
          root: { id: 'root', message: null, parent: null, children: ['msg1'] },
          msg1: {
            id: 'msg1',
            message: {
              id: 'msg1',
              author: { role: 'user' },
              content: { content_type: 'text', parts: ['I work at Google as a software engineer'] },
              create_time: 1700000001,
            },
            parent: 'root',
            children: ['msg2'],
          },
          msg2: {
            id: 'msg2',
            message: {
              id: 'msg2',
              author: { role: 'assistant' },
              content: { content_type: 'text', parts: ['That sounds great! Tell me more about your work.'] },
              create_time: 1700000002,
            },
            parent: 'msg1',
            children: ['msg3'],
          },
          msg3: {
            id: 'msg3',
            message: {
              id: 'msg3',
              author: { role: 'user' },
              content: { content_type: 'text', parts: ['I prefer TypeScript over JavaScript for new projects'] },
              create_time: 1700000003,
            },
            parent: 'msg2',
            children: [],
          },
        },
      },
    ];

    const adapter = new ChatGPTAdapter();
    const result = await adapter.parse({ content: JSON.stringify(conversations) });

    assert(result.facts.length === 0, 'ChatGPT conv: no pre-extracted facts (uses chunks)');
    assert(result.chunks.length === 1, `ChatGPT conv: 1 conversation chunk (got ${result.chunks.length})`);
    assert(result.chunks[0].title === 'Test Conversation', 'ChatGPT conv: chunk title matches conversation title');
    assert(result.chunks[0].messages.length === 3, `ChatGPT conv: 3 messages (user + assistant) (got ${result.chunks[0].messages.length})`);
    assert(result.chunks[0].messages[0].role === 'user', 'ChatGPT conv: first message is user');
    assert(result.chunks[0].messages[0].text.includes('Google'), 'ChatGPT conv: first message text correct');
    assert(result.chunks[0].messages[1].role === 'assistant', 'ChatGPT conv: second message is assistant');
    assert(result.chunks[0].messages[2].role === 'user', 'ChatGPT conv: third message is user');
    assert(result.chunks[0].messages[2].text.includes('TypeScript'), 'ChatGPT conv: third message text correct');
    assert(result.chunks[0].timestamp !== undefined, 'ChatGPT conv: chunk has timestamp');
    assert(result.totalMessages === 3, `ChatGPT conv: totalMessages is 3 (got ${result.totalMessages})`);
    assert(result.errors.length === 0, 'ChatGPT conv: no errors');
  }

  // --- includes both user and assistant messages ---
  {
    const conversations = [
      {
        title: 'Context Test',
        mapping: {
          root: { id: 'root', message: null, parent: null, children: ['msg1'] },
          msg1: {
            id: 'msg1',
            message: {
              id: 'msg1',
              author: { role: 'user' },
              content: { content_type: 'text', parts: ['I want to migrate to TypeScript'] },
            },
            parent: 'root',
            children: ['msg2'],
          },
          msg2: {
            id: 'msg2',
            message: {
              id: 'msg2',
              author: { role: 'assistant' },
              content: { content_type: 'text', parts: ['TypeScript migration involves setting up tsconfig and converting files'] },
            },
            parent: 'msg1',
            children: [],
          },
        },
      },
    ];

    const adapter = new ChatGPTAdapter();
    const result = await adapter.parse({ content: JSON.stringify(conversations) });

    assert(result.chunks.length === 1, 'ChatGPT: includes assistant messages for context');
    assert(result.chunks[0].messages.length === 2, 'ChatGPT: both user and assistant in chunk');
    assert(result.chunks[0].messages[1].role === 'assistant', 'ChatGPT: assistant message preserved');
  }

  // --- skips system and tool messages ---
  {
    const conversations = [
      {
        title: 'Test',
        mapping: {
          root: { id: 'root', message: null, parent: null, children: ['msg1'] },
          msg1: {
            id: 'msg1',
            message: {
              id: 'msg1',
              author: { role: 'system' },
              content: { content_type: 'text', parts: ['You are a helpful assistant'] },
            },
            parent: 'root',
            children: ['msg2'],
          },
          msg2: {
            id: 'msg2',
            message: {
              id: 'msg2',
              author: { role: 'tool' },
              content: { content_type: 'text', parts: ['Tool output: search results...'] },
            },
            parent: 'msg1',
            children: ['msg3'],
          },
          msg3: {
            id: 'msg3',
            message: {
              id: 'msg3',
              author: { role: 'user' },
              content: { content_type: 'text', parts: ['I work at Google as a senior engineer'] },
            },
            parent: 'msg2',
            children: [],
          },
        },
      },
    ];

    const adapter = new ChatGPTAdapter();
    const result = await adapter.parse({ content: JSON.stringify(conversations) });

    assert(result.chunks.length === 1, 'ChatGPT: has 1 chunk');
    assert(result.chunks[0].messages.length === 1, 'ChatGPT: only user message (skips system + tool)');
    assert(result.chunks[0].messages[0].role === 'user', 'ChatGPT: the surviving message is user');
  }

  // --- chunks large conversations into batches of 20 ---
  {
    // Build a conversation with 45 messages
    const mapping: Record<string, any> = {
      root: { id: 'root', message: null, parent: null, children: ['msg-0'] },
    };

    for (let i = 0; i < 45; i++) {
      const role = i % 2 === 0 ? 'user' : 'assistant';
      mapping[`msg-${i}`] = {
        id: `msg-${i}`,
        message: {
          id: `msg-${i}`,
          author: { role },
          content: { content_type: 'text', parts: [`Message number ${i} from ${role} about various topics`] },
        },
        parent: i === 0 ? 'root' : `msg-${i - 1}`,
        children: i < 44 ? [`msg-${i + 1}`] : [],
      };
    }

    const conversations = [{ title: 'Long Conversation', mapping }];

    const adapter = new ChatGPTAdapter();
    const result = await adapter.parse({ content: JSON.stringify(conversations) });

    assert(result.chunks.length === 3, `ChatGPT: 45 messages -> 3 chunks (got ${result.chunks.length})`);
    assert(result.chunks[0].messages.length === 20, `ChatGPT: first chunk has 20 messages (got ${result.chunks[0].messages.length})`);
    assert(result.chunks[1].messages.length === 20, `ChatGPT: second chunk has 20 messages (got ${result.chunks[1].messages.length})`);
    assert(result.chunks[2].messages.length === 5, `ChatGPT: third chunk has 5 messages (got ${result.chunks[2].messages.length})`);
    assert(result.chunks[0].title.includes('part 1/3'), `ChatGPT: first chunk title has part indicator (got: ${result.chunks[0].title})`);
    assert(result.chunks[2].title.includes('part 3/3'), `ChatGPT: last chunk title has part indicator (got: ${result.chunks[2].title})`);
    assert(result.totalMessages === 45, `ChatGPT: totalMessages is 45 (got ${result.totalMessages})`);
  }

  // --- handles single conversation object (not array) ---
  {
    const conv = {
      title: 'Single',
      mapping: {
        root: { id: 'root', message: null, parent: null, children: ['msg1'] },
        msg1: {
          id: 'msg1',
          message: { id: 'msg1', author: { role: 'user' }, content: { content_type: 'text', parts: ['I live in San Francisco near the park'] } },
          parent: 'root', children: [],
        },
      },
    };

    const adapter = new ChatGPTAdapter();
    const result = await adapter.parse({ content: JSON.stringify(conv) });

    assert(result.chunks.length === 1, 'ChatGPT: single conversation object parses into 1 chunk');
    assert(result.chunks[0].messages[0].text.includes('San Francisco'), 'ChatGPT: single conv message correct');
  }

  // --- handles null/non-string parts ---
  {
    const conversations = [
      {
        title: 'Null Parts',
        mapping: {
          root: { id: 'root', message: null, parent: null, children: ['msg1'] },
          msg1: {
            id: 'msg1',
            message: {
              id: 'msg1',
              author: { role: 'user' },
              content: { content_type: 'text', parts: [null, { type: 'image' }, 'I prefer dark mode in all my applications'] },
            },
            parent: 'root', children: [],
          },
        },
      },
    ];

    const adapter = new ChatGPTAdapter();
    const result = await adapter.parse({ content: JSON.stringify(conversations) });

    assert(result.chunks.length === 1, 'ChatGPT: handles null/non-string parts');
    assert(result.chunks[0].messages[0].text.includes('dark mode'), 'ChatGPT: extracted text from valid part');
  }

  // --- invalid JSON returns error ---
  {
    const adapter = new ChatGPTAdapter();
    const result2 = await adapter.parse({ content: '[invalid json array' });
    assert(result2.chunks.length === 0, 'ChatGPT: invalid JSON array yields 0 chunks');
    assert(result2.errors.length > 0, 'ChatGPT: invalid JSON produces error');
  }

  // --- empty input returns error ---
  {
    const adapter = new ChatGPTAdapter();
    const result = await adapter.parse({});

    assert(result.chunks.length === 0, 'ChatGPT: no input yields 0 chunks');
    assert(result.errors.length > 0, 'ChatGPT: no input produces error');
  }

  // --- conversation with no text messages produces no chunks ---
  {
    const conversations = [
      {
        title: 'Empty',
        mapping: {
          root: { id: 'root', message: null, parent: null, children: ['msg1'] },
          msg1: {
            id: 'msg1',
            message: {
              id: 'msg1',
              author: { role: 'user' },
              content: { content_type: 'text', parts: [null] },
            },
            parent: 'root', children: [],
          },
        },
      },
    ];

    const adapter = new ChatGPTAdapter();
    const result = await adapter.parse({ content: JSON.stringify(conversations) });

    assert(result.chunks.length === 0, 'ChatGPT: conversation with no text -> no chunks');
  }

  // --- multiple conversations produce multiple chunks ---
  {
    const conversations = [
      {
        title: 'Conv 1',
        create_time: 1700000000,
        mapping: {
          root: { id: 'root', message: null, parent: null, children: ['msg1'] },
          msg1: {
            id: 'msg1',
            message: { id: 'msg1', author: { role: 'user' }, content: { content_type: 'text', parts: ['First conversation message'] } },
            parent: 'root', children: [],
          },
        },
      },
      {
        title: 'Conv 2',
        create_time: 1700100000,
        mapping: {
          root: { id: 'root', message: null, parent: null, children: ['msg1'] },
          msg1: {
            id: 'msg1',
            message: { id: 'msg1', author: { role: 'user' }, content: { content_type: 'text', parts: ['Second conversation message'] } },
            parent: 'root', children: [],
          },
        },
      },
    ];

    const adapter = new ChatGPTAdapter();
    const result = await adapter.parse({ content: JSON.stringify(conversations) });

    assert(result.chunks.length === 2, `ChatGPT: 2 conversations -> 2 chunks (got ${result.chunks.length})`);
    assert(result.chunks[0].title === 'Conv 1', 'ChatGPT: first chunk title correct');
    assert(result.chunks[1].title === 'Conv 2', 'ChatGPT: second chunk title correct');
  }

  // =========================================================================
  // ChatGPTAdapter — memories text (returns chunks, not facts)
  // =========================================================================

  console.log('# ChatGPTAdapter — memories text (chunks)');

  // --- parses plain text memories into chunks ---
  {
    const memoriesText = `User prefers dark mode
User works at Google as a software engineer
User lives in San Francisco
User likes hiking on weekends`;

    const adapter = new ChatGPTAdapter();
    const result = await adapter.parse({ content: memoriesText });

    assert(result.facts.length === 0, 'ChatGPT memories: no pre-extracted facts');
    assert(result.chunks.length === 1, `ChatGPT memories: 4 lines -> 1 chunk (got ${result.chunks.length})`);
    assert(result.chunks[0].messages.length === 4, `ChatGPT memories: 4 messages in chunk (got ${result.chunks[0].messages.length})`);
    assert(result.chunks[0].messages[0].text === 'User prefers dark mode', 'ChatGPT memories: first message text correct');
    assert(result.chunks[0].messages[0].role === 'user', 'ChatGPT memories: all messages are user role');
    assert(result.totalMessages === 4, `ChatGPT memories: totalMessages is 4 (got ${result.totalMessages})`);
  }

  // --- handles bullet points and numbered lists ---
  {
    const memoriesText = `- User prefers TypeScript
* User works remotely
1. User lives in Berlin
2) User likes coffee in the morning`;

    const adapter = new ChatGPTAdapter();
    const result = await adapter.parse({ content: memoriesText });

    assert(result.chunks.length === 1, 'ChatGPT memories: 4 lines -> 1 chunk');
    assert(result.chunks[0].messages.length === 4, `ChatGPT memories: handles bullets/numbers (got ${result.chunks[0].messages.length})`);
    assert(!result.chunks[0].messages[0].text.startsWith('-'), 'ChatGPT memories: bullet stripped');
    assert(!result.chunks[0].messages[2].text.startsWith('1'), 'ChatGPT memories: number stripped');
  }

  // --- skips empty lines and header lines ---
  {
    const memoriesText = `Memories:

User prefers dark mode

User lives in London`;

    const adapter = new ChatGPTAdapter();
    const result = await adapter.parse({ content: memoriesText });

    assert(result.chunks.length === 1, 'ChatGPT memories: skips header/blank');
    assert(result.chunks[0].messages.length === 2, `ChatGPT memories: only 2 valid lines (got ${result.chunks[0].messages.length})`);
  }

  // --- empty text input ---
  {
    const adapter = new ChatGPTAdapter();
    const result = await adapter.parse({ content: '' });

    assert(result.chunks.length === 0, 'ChatGPT memories: empty text yields 0 chunks');
  }

  // --- large memory list chunks into multiple batches ---
  {
    const lines = Array.from({ length: 50 }, (_, i) => `User memory item number ${i + 1} about their preferences`);
    const memoriesText = lines.join('\n');

    const adapter = new ChatGPTAdapter();
    const result = await adapter.parse({ content: memoriesText });

    assert(result.chunks.length === 3, `ChatGPT memories: 50 lines -> 3 chunks (got ${result.chunks.length})`);
    assert(result.chunks[0].messages.length === 20, `ChatGPT memories: first chunk has 20 (got ${result.chunks[0].messages.length})`);
    assert(result.chunks[1].messages.length === 20, `ChatGPT memories: second chunk has 20 (got ${result.chunks[1].messages.length})`);
    assert(result.chunks[2].messages.length === 10, `ChatGPT memories: third chunk has 10 (got ${result.chunks[2].messages.length})`);
    assert(result.totalMessages === 50, `ChatGPT memories: totalMessages is 50 (got ${result.totalMessages})`);
  }

  // =========================================================================
  // ClaudeAdapter (returns chunks, not facts)
  // =========================================================================

  console.log('# ClaudeAdapter (chunks)');

  // --- parses plain text memories into chunks ---
  {
    const memoriesText = `User prefers functional programming
User works at a startup in Berlin
User decided to use Rust for the backend
User wants to learn machine learning`;

    const adapter = new ClaudeAdapter();
    const result = await adapter.parse({ content: memoriesText });

    assert(result.facts.length === 0, 'Claude: no pre-extracted facts (uses chunks)');
    assert(result.chunks.length === 1, `Claude: 4 memories -> 1 chunk (got ${result.chunks.length})`);
    assert(result.chunks[0].messages.length === 4, `Claude: 4 messages in chunk (got ${result.chunks[0].messages.length})`);
    assert(result.chunks[0].messages[0].role === 'user', 'Claude: all messages are user role');
    assert(result.chunks[0].messages[0].text === 'User prefers functional programming', 'Claude: first message text correct');
    assert(result.totalMessages === 4, `Claude: totalMessages is 4 (got ${result.totalMessages})`);
  }

  // --- handles date prefixes (strips them from text) ---
  {
    const memoriesText = `[2026-03-15] - User prefers dark mode
[2026-03-10] - User works at Google
No date prefix here but still a memory`;

    const adapter = new ClaudeAdapter();
    const result = await adapter.parse({ content: memoriesText });

    assert(result.chunks.length === 1, 'Claude: parsed into 1 chunk');
    assert(result.chunks[0].messages.length === 3, `Claude: 3 messages (got ${result.chunks[0].messages.length})`);
    assert(!result.chunks[0].messages[0].text.includes('[2026'), 'Claude: date prefix stripped from text');
    assert(result.chunks[0].messages[0].text === 'User prefers dark mode', 'Claude: cleaned text correct');
    assert(result.chunks[0].timestamp === '2026-03-15', 'Claude: chunk timestamp from first dated entry');
  }

  // --- handles bullet points and numbered lists ---
  {
    const memoriesText = `- User prefers TypeScript
* User works remotely from home
1. User lives in Lisbon, Portugal
2) User likes exploring new restaurants`;

    const adapter = new ClaudeAdapter();
    const result = await adapter.parse({ content: memoriesText });

    assert(result.chunks.length === 1, 'Claude: 4 lines -> 1 chunk');
    assert(result.chunks[0].messages.length === 4, `Claude: handles bullets/numbers (got ${result.chunks[0].messages.length})`);
    assert(!result.chunks[0].messages[0].text.startsWith('-'), 'Claude: bullet stripped');
    assert(!result.chunks[0].messages[2].text.startsWith('1'), 'Claude: number stripped');
  }

  // --- skips empty lines and header lines ---
  {
    const memoriesText = `Claude Memories:

User prefers dark mode in editors

User lives in Tokyo`;

    const adapter = new ClaudeAdapter();
    const result = await adapter.parse({ content: memoriesText });

    assert(result.chunks.length === 1, 'Claude: skips header/blank');
    assert(result.chunks[0].messages.length === 2, `Claude: only 2 valid lines (got ${result.chunks[0].messages.length})`);
  }

  // --- empty input returns error ---
  {
    const adapter = new ClaudeAdapter();
    const result = await adapter.parse({});

    assert(result.chunks.length === 0, 'Claude: no input yields 0 chunks');
    assert(result.errors.length > 0, 'Claude: no input produces error');
  }

  // --- empty text yields 0 chunks ---
  {
    const adapter = new ClaudeAdapter();
    const result = await adapter.parse({ content: '' });

    assert(result.chunks.length === 0, 'Claude: empty text yields 0 chunks');
  }

  // --- skips very short memories ---
  {
    const memoriesText = `ok
ab
User prefers TypeScript over JavaScript`;

    const adapter = new ClaudeAdapter();
    const result = await adapter.parse({ content: memoriesText });

    // "ok" and "ab" are < 3 chars after validation
    assert(result.chunks.length === 1, 'Claude: has 1 chunk');
    assert(result.chunks[0].messages.length === 1, `Claude: skips short memories (got ${result.chunks[0].messages.length})`);
    assert(result.chunks[0].messages[0].text.includes('TypeScript'), 'Claude: valid memory kept');
  }

  // --- large memory list chunks correctly ---
  {
    const lines = Array.from({ length: 25 }, (_, i) => `Claude memory item number ${i + 1} about their workflow`);
    const memoriesText = lines.join('\n');

    const adapter = new ClaudeAdapter();
    const result = await adapter.parse({ content: memoriesText });

    assert(result.chunks.length === 2, `Claude: 25 lines -> 2 chunks (got ${result.chunks.length})`);
    assert(result.chunks[0].messages.length === 20, `Claude: first chunk has 20 (got ${result.chunks[0].messages.length})`);
    assert(result.chunks[1].messages.length === 5, `Claude: second chunk has 5 (got ${result.chunks[1].messages.length})`);
    assert(result.totalMessages === 25, `Claude: totalMessages is 25 (got ${result.totalMessages})`);
  }

  // =========================================================================
  // getAdapter factory
  // =========================================================================

  console.log('# getAdapter factory');

  // --- valid sources ---
  {
    const mem0 = getAdapter('mem0');
    assert(mem0 instanceof Mem0Adapter, 'getAdapter("mem0") returns Mem0Adapter');

    const mcp = getAdapter('mcp-memory');
    assert(mcp instanceof MCPMemoryAdapter, 'getAdapter("mcp-memory") returns MCPMemoryAdapter');

    const chatgpt = getAdapter('chatgpt');
    assert(chatgpt instanceof ChatGPTAdapter, 'getAdapter("chatgpt") returns ChatGPTAdapter');

    const claude = getAdapter('claude');
    assert(claude instanceof ClaudeAdapter, 'getAdapter("claude") returns ClaudeAdapter');
  }

  // --- unknown source throws ---
  {
    assertThrows(
      () => getAdapter('nonexistent' as ImportSource),
      'getAdapter throws on unknown source',
    );
  }

  // --- error message lists valid sources ---
  {
    try {
      getAdapter('bogus' as ImportSource);
      assert(false, 'getAdapter should throw for bogus source');
    } catch (e: unknown) {
      const msg = (e as Error).message;
      assert(msg.includes('mem0'), 'getAdapter error lists "mem0" as valid source');
      assert(msg.includes('mcp-memory'), 'getAdapter error lists "mcp-memory" as valid source');
      assert(msg.includes('chatgpt'), 'getAdapter error lists "chatgpt" as valid source');
      assert(msg.includes('claude'), 'getAdapter error lists "claude" as valid source');
    }
  }

  // =========================================================================
  // File preflight — 500MB cap + RAM check
  // =========================================================================

  console.log('# File preflight checks');

  // Monkey-patch helpers for statSync / freemem without a mocking framework.
  async function withFakeStat(fakeSize: number, fn: () => Promise<void>): Promise<void> {
    const orig = fs.statSync;
    (fs as any).statSync = (_p: string) => ({ size: fakeSize } as fs.Stats);
    await fn().finally(() => { (fs as any).statSync = orig; });
  }
  async function withFakeFreemem(fakeBytes: number, fn: () => Promise<void>): Promise<void> {
    const orig = os.freemem;
    os.freemem = () => fakeBytes;
    await fn().finally(() => { os.freemem = orig; });
  }

  // --- 500MB hard cap returns an error with size info (Claude) ---
  {
    await withFakeStat(501 * 1024 * 1024, async () => {
      const result = await new ClaudeAdapter().parse({ file_path: '/tmp/fake-large.txt' });
      assert(result.errors.length > 0, 'Preflight: Claude oversized file returns error');
      assert(
        result.errors[0].includes('501') || result.errors[0].includes('500MB'),
        `Preflight: Claude error mentions size/cap (got: ${result.errors[0]})`,
      );
      assert(result.chunks.length === 0, 'Preflight: no chunks on oversized file');
    });
  }

  // --- 500MB hard cap (ChatGPT) ---
  {
    await withFakeStat(600 * 1024 * 1024, async () => {
      const result = await new ChatGPTAdapter().parse({ file_path: '/tmp/fake-large.json' });
      assert(result.errors.length > 0, 'Preflight: ChatGPT oversized file returns error');
      assert(result.errors[0].includes('500MB'), 'Preflight: ChatGPT error mentions 500MB cap');
    });
  }

  // --- 500MB hard cap (Gemini) ---
  {
    await withFakeStat(510 * 1024 * 1024, async () => {
      const result = await new GeminiAdapter().parse({ file_path: '/tmp/fake-large.html' });
      assert(result.errors.length > 0, 'Preflight: Gemini oversized file returns error');
      assert(result.errors[0].includes('500MB'), 'Preflight: Gemini error mentions 500MB cap');
    });
  }

  // --- RAM preflight triggers when freemem < 2x file size (Claude) ---
  {
    await withFakeFreemem(1 * 1024 * 1024, async () => {  // 1MB free
      await withFakeStat(10 * 1024 * 1024, async () => {  // 10MB file (passes 500MB check)
        const result = await new ClaudeAdapter().parse({ file_path: '/tmp/fake-low-mem.txt' });
        assert(result.errors.length > 0, 'Preflight: low RAM returns error');
        assert(
          result.errors[0].toLowerCase().includes('memory'),
          `Preflight: RAM error mentions memory (got: ${result.errors[0]})`,
        );
      });
    });
  }

  // --- normal-sized file passes preflight (real temp file) ---
  {
    const tmpFile = os.tmpdir() + '/totalreclaw-preflight-test.txt';
    fs.writeFileSync(tmpFile, 'User prefers dark mode\nUser works remotely\n', 'utf-8');
    try {
      const result = await new ClaudeAdapter().parse({ file_path: tmpFile });
      assert(result.errors.length === 0, 'Preflight: normal file has no errors');
      assert(result.chunks.length > 0, 'Preflight: normal file produces chunks');
    } finally {
      fs.unlinkSync(tmpFile);
    }
  }

  // =========================================================================
  // Summary
  // =========================================================================

  console.log(`\n1..${testNum}`);
  console.log(`# pass: ${passed}`);
  console.log(`# fail: ${failed}`);

  if (failed > 0) {
    console.log('\nFAILED');
    process.exit(1);
  } else {
    console.log('\nALL TESTS PASSED');
    process.exit(0);
  }
}

runTests().catch((err) => {
  console.error('Test runner failed:', err);
  process.exit(1);
});
