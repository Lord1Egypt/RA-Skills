/**
 * Tests for session types and helper functions
 */

import {
  TokenUsage,
  calculateTotalTokens,
  TextBlock,
  ToolUseBlock,
  ToolResultBlock,
  ContentBlock,
  ConversationMessage,
  MessageRole,
  createUserMessage,
  createAssistantMessage,
  createToolResultMessage,
  createSystemMessage,
  extractMessageText,
  convertLegacyMessage,
  convertToLegacyMessage,
  Session,
  SessionError
} from '../types.js';

describe('TokenUsage', () => {
  test('calculates total tokens correctly', () => {
    const usage: TokenUsage = {
      input_tokens: 100,
      output_tokens: 50,
      cache_creation_input_tokens: 10,
      cache_read_input_tokens: 20
    };

    expect(calculateTotalTokens(usage)).toBe(180);
  });

  test('handles zero values', () => {
    const usage: TokenUsage = {
      input_tokens: 0,
      output_tokens: 0,
      cache_creation_input_tokens: 0,
      cache_read_input_tokens: 0
    };

    expect(calculateTotalTokens(usage)).toBe(0);
  });
});

describe('Message Helpers', () => {
  test('creates user message', () => {
    const message = createUserMessage('Hello world');

    expect(message.role).toBe('user');
    expect(message.blocks).toHaveLength(1);
    expect(message.blocks[0]).toEqual({
      type: 'text',
      text: 'Hello world'
    });
    expect(message.usage).toBeUndefined();
  });

  test('creates assistant message with blocks', () => {
    const blocks: ContentBlock[] = [
      { type: 'text', text: 'Let me help you' },
      { type: 'tool_use', id: '1', name: 'read', input: '{"path": "test.ts"}' }
    ];
    const usage: TokenUsage = {
      input_tokens: 10,
      output_tokens: 5,
      cache_creation_input_tokens: 1,
      cache_read_input_tokens: 2
    };

    const message = createAssistantMessage(blocks, usage);

    expect(message.role).toBe('assistant');
    expect(message.blocks).toEqual(blocks);
    expect(message.usage).toEqual(usage);
  });

  test('creates tool result message', () => {
    const message = createToolResultMessage(
      '1',
      'read',
      'file content',
      false
    );

    expect(message.role).toBe('tool');
    expect(message.blocks).toHaveLength(1);
    expect(message.blocks[0]).toEqual({
      type: 'tool_result',
      tool_use_id: '1',
      tool_name: 'read',
      output: 'file content',
      is_error: false
    });
  });

  test('creates system message', () => {
    const message = createSystemMessage('System instruction');

    expect(message.role).toBe('system');
    expect(message.blocks).toHaveLength(1);
    expect(message.blocks[0]).toEqual({
      type: 'text',
      text: 'System instruction'
    });
  });
});

describe('extractMessageText', () => {
  test('extracts text from text blocks', () => {
    const message: ConversationMessage = {
      role: 'user',
      blocks: [
        { type: 'text', text: 'Hello' },
        { type: 'text', text: 'World' }
      ]
    };

    expect(extractMessageText(message)).toBe('Hello\nWorld');
  });

  test('ignores non-text blocks', () => {
    const message: ConversationMessage = {
      role: 'assistant',
      blocks: [
        { type: 'text', text: 'Using tool' },
        { type: 'tool_use', id: '1', name: 'read', input: '{}' }
      ]
    };

    expect(extractMessageText(message)).toBe('Using tool');
  });

  test('returns empty string for no text blocks', () => {
    const message: ConversationMessage = {
      role: 'tool',
      blocks: [
        { type: 'tool_result', tool_use_id: '1', tool_name: 'read', output: 'ok', is_error: false }
      ]
    };

    expect(extractMessageText(message)).toBe('');
  });
});

describe('Message Format Conversion', () => {
  test('converts legacy message to new format', () => {
    const legacy = { role: 'user', content: 'Hello world' };
    const converted = convertLegacyMessage(legacy);

    expect(converted.role).toBe('user');
    expect(converted.blocks).toHaveLength(1);
    expect(converted.blocks[0]).toEqual({
      type: 'text',
      text: 'Hello world'
    });
  });

  test('converts legacy message with undefined content', () => {
    const legacy = { role: 'assistant' };
    const converted = convertLegacyMessage(legacy);

    expect(converted.role).toBe('assistant');
    expect(converted.blocks[0]).toEqual({
      type: 'text',
      text: ''
    });
  });

  test('converts new message to legacy format', () => {
    const message: ConversationMessage = {
      role: 'user',
      blocks: [
        { type: 'text', text: 'Hello' },
        { type: 'text', text: 'World' }
      ]
    };

    const legacy = convertToLegacyMessage(message);

    expect(legacy.role).toBe('user');
    expect(legacy.content).toBe('Hello\nWorld');
  });

  test('conversion is reversible', () => {
    const legacy = { role: 'user', content: 'Test message' };
    const converted = convertLegacyMessage(legacy);
    const backToLegacy = convertToLegacyMessage(converted);

    expect(backToLegacy.role).toBe(legacy.role);
    expect(backToLegacy.content).toBe(legacy.content);
  });
});

describe('Session', () => {
  test('creates valid session', () => {
    const session: Session = {
      version: 1,
      messages: [
        createUserMessage('Hello'),
        createAssistantMessage([{ type: 'text', text: 'Hi!' }])
      ]
    };

    expect(session.version).toBe(1);
    expect(session.messages).toHaveLength(2);
  });
});

describe('SessionError', () => {
  test('creates error with code', () => {
    const error = new SessionError('Test error', 'IO_ERROR');

    expect(error.message).toBe('Test error');
    expect(error.code).toBe('IO_ERROR');
    expect(error.name).toBe('SessionError');
    expect(error).toBeInstanceOf(Error);
  });

  test('supports all error codes', () => {
    const codes: Array<SessionError['code']> = [
      'IO_ERROR',
      'PARSE_ERROR',
      'NOT_FOUND',
      'INVALID_FORMAT'
    ];

    codes.forEach(code => {
      const error = new SessionError('Error', code);
      expect(error.code).toBe(code);
    });
  });
});
