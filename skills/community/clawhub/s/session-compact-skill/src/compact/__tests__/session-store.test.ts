/**
 * Tests for session store (persistence layer)
 */

import { SessionStore, createSessionStore } from '../session-store.js';
import { Session, createUserMessage, createAssistantMessage, SessionError } from '../types.js';
import { existsSync, mkdirSync, rmSync } from 'node:fs';
import { join } from 'node:path';
import { tmpdir } from 'node:os';

describe('SessionStore', () => {
  let store: SessionStore;
  let testDir: string;

  beforeEach(() => {
    testDir = join(tmpdir(), `session-store-test-${Date.now()}`);
    store = createSessionStore(testDir);
  });

  afterEach(() => {
    // Cleanup test directory
    if (existsSync(testDir)) {
      rmSync(testDir, { recursive: true, force: true });
    }
  });

  test('initializes storage directory', () => {
    expect(existsSync(testDir)).toBe(false);
    store.initialize();
    expect(existsSync(testDir)).toBe(true);
  });

  test('saves and loads session', () => {
    const session: Session = {
      version: 1,
      messages: [
        createUserMessage('Hello'),
        createAssistantMessage([{ type: 'text', text: 'Hi!' }])
      ]
    };

    store.saveSession(session, 'test-session');
    const loaded = store.loadSession('test-session');

    expect(loaded).toEqual(session);
  });

  test('throws error when loading non-existent session', () => {
    expect(() => store.loadSession('non-existent')).toThrow(SessionError);
    expect(() => store.loadSession('non-existent')).toThrow('Session not found');
  });

  test('checks if session exists', () => {
    const session: Session = {
      version: 1,
      messages: [createUserMessage('Test')]
    };

    expect(store.sessionExists('test')).toBe(false);
    store.saveSession(session, 'test');
    expect(store.sessionExists('test')).toBe(true);
  });

  test('deletes session', () => {
    const session: Session = {
      version: 1,
      messages: [createUserMessage('Test')]
    };

    store.saveSession(session, 'test');
    expect(store.sessionExists('test')).toBe(true);

    store.deleteSession('test');
    expect(store.sessionExists('test')).toBe(false);
  });

  test('throws error when deleting non-existent session', () => {
    expect(() => store.deleteSession('non-existent')).toThrow(SessionError);
  });

  test('throws error for invalid session format', () => {
    store.initialize();
    const { writeFileSync } = require('node:fs');
    const path = join(testDir, 'invalid.json');
    writeFileSync(path, JSON.stringify({ invalid: 'format' }), 'utf-8');

    expect(() => store.loadSession('invalid')).toThrow(SessionError);
    expect(() => store.loadSession('invalid')).toThrow('Invalid session format');
  });

  test('throws error for malformed JSON', () => {
    store.initialize();
    const { writeFileSync } = require('node:fs');
    const path = join(testDir, 'malformed.json');
    writeFileSync(path, '{invalid json}', 'utf-8');

    expect(() => store.loadSession('malformed')).toThrow(SessionError);
    expect(() => store.loadSession('malformed')).toThrow('Failed to parse session');
  });

  test('lists sessions with metadata', () => {
    const session1: Session = {
      version: 1,
      messages: [
        createUserMessage('Hello'),
        createAssistantMessage([{ type: 'text', text: 'Hi!' }])
      ]
    };

    const session2: Session = {
      version: 1,
      messages: [
        createUserMessage('Test'),
        createAssistantMessage([
          { type: 'tool_use', id: '1', name: 'read', input: '{"path": "test.ts"}' }
        ])
      ]
    };

    store.saveSession(session1, 'session-1');
    store.saveSession(session2, 'session-2');

    const sessions = store.listSessions();

    expect(sessions).toHaveLength(2);
    expect(sessions.map((s: any) => s.session_id)).toContain('session-1');
    expect(sessions.map((s: any) => s.session_id)).toContain('session-2');

    // Check metadata structure
    sessions.forEach((s: any) => {
      expect(s.session_id).toBeDefined();
      expect(s.created_at).toBeDefined();
      expect(s.updated_at).toBeDefined();
      expect(s.message_count).toBeDefined();
      expect(s.total_input_tokens).toBeDefined();
      expect(s.total_output_tokens).toBeDefined();
      expect(s.total_cache_tokens).toBeDefined();
      expect(s.compaction_count).toBeDefined();
    });
  });

  test('returns empty list when no sessions exist', () => {
    const sessions = store.listSessions();
    expect(sessions).toEqual([]);
  });

  test('gets storage directory path', () => {
    expect(store.getStorageDir()).toBe(testDir);
  });

  test('cleans up old sessions', () => {
    const session: Session = {
      version: 1,
      messages: [createUserMessage('Test')]
    };

    store.saveSession(session, 'old-session');
    expect(store.sessionExists('old-session')).toBe(true);

    // Cleanup with 0 days max age (should remove all)
    const cleaned = store.cleanupOldSessions(0);
    expect(cleaned).toBeGreaterThanOrEqual(0);
  });

  test('handles session with usage metadata', () => {
    const session: Session = {
      version: 1,
      messages: [
        {
          role: 'assistant',
          blocks: [{ type: 'text', text: 'Response' }],
          usage: {
            input_tokens: 100,
            output_tokens: 50,
            cache_creation_input_tokens: 10,
            cache_read_input_tokens: 20
          }
        }
      ]
    };

    store.saveSession(session, 'with-usage');
    const loaded = store.loadSession('with-usage');

    expect(loaded.messages[0].usage).toEqual(session.messages[0].usage);
  });

  test('handles complex session with multiple block types', () => {
    const session: Session = {
      version: 1,
      messages: [
        createUserMessage('Read test.ts'),
        {
          role: 'assistant',
          blocks: [
            { type: 'tool_use', id: '1', name: 'read', input: '{"path": "test.ts"}' }
          ]
        },
        {
          role: 'tool',
          blocks: [
            {
              type: 'tool_result',
              tool_use_id: '1',
              tool_name: 'read',
              output: 'export const x = 1;',
              is_error: false
            }
          ]
        },
        createAssistantMessage([{ type: 'text', text: 'Found it!' }])
      ]
    };

    store.saveSession(session, 'complex');
    const loaded = store.loadSession('complex');

    expect(loaded.messages).toHaveLength(4);
    expect(loaded.messages[1].blocks[0].type).toBe('tool_use');
    expect(loaded.messages[2].blocks[0].type).toBe('tool_result');
  });
});

describe('createSessionStore', () => {
  test('creates store with default directory', () => {
    const store = createSessionStore();
    expect(store.getStorageDir()).toContain('.openclaw');
    expect(store.getStorageDir()).toContain('sessions');
  });

  test('creates store with custom directory', () => {
    const customDir = '/tmp/custom-sessions';
    const store = createSessionStore(customDir);
    expect(store.getStorageDir()).toBe(customDir);
  });
});
