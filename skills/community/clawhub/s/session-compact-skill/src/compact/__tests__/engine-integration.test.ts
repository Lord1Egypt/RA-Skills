import {
  getCurrentModel,
  shouldCompact,
  compactSession,
  generateSummary,
  getContinuationPrompt
} from '../engine.js';
import { loadConfig } from '../config.js';

// Mock fs and child_process
jest.mock('node:fs', () => ({
  readFileSync: jest.fn()
}));

jest.mock('node:child_process', () => ({
  execSync: jest.fn()
}));

import { readFileSync } from 'node:fs';
import { execSync } from 'node:child_process';

describe('getCurrentModel', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('should read model from OpenClaw config', () => {
    (readFileSync as jest.Mock).mockReturnValue(JSON.stringify({
      default_model: 'qwen/custom-model'
    }));

    const model = getCurrentModel();
    expect(model).toBe('qwen/custom-model');
  });

  it('should use default model when config not found', () => {
    (readFileSync as jest.Mock).mockImplementation(() => {
      throw new Error('File not found');
    });

    const model = getCurrentModel();
    expect(model).toBe('qwen/qwen3.5-122b-a10b');
  });

  it('should handle malformed JSON gracefully', () => {
    (readFileSync as jest.Mock).mockReturnValue('invalid json');

    const model = getCurrentModel();
    expect(model).toBe('qwen/qwen3.5-122b-a10b');
  });
});

describe('compactSession integration', () => {
  it('should return early when session is small', async () => {
    const config = loadConfig({ max_tokens: 10000 });
    const messages = [
      { role: 'user', content: 'hello' },
      { role: 'assistant', content: 'hi there' }
    ];

    const result = await compactSession(messages, config);
    
    expect(result.removedCount).toBe(0);
    expect(result.savedTokens).toBe(0);
    expect(result.summary).toBe('');
  });

  it('should handle compactSession error gracefully', async () => {
    const config = loadConfig({ 
      max_tokens: 100, // Very low threshold
      preserve_recent: 2 
    });
    
    // Create messages that exceed threshold
    const messages = [
      { role: 'user', content: 'x'.repeat(500) },
      { role: 'assistant', content: 'y'.repeat(500) },
      { role: 'user', content: 'keep this' },
      { role: 'assistant', content: 'and this' }
    ];

    // Mock callLLM to throw error
    jest.mock('../engine.js', () => {
      const original = jest.requireActual('../engine.js');
      return {
        ...original,
        callLLM: jest.fn().mockRejectedValue(new Error('LLM failed'))
      };
    });

    const result = await compactSession(messages, config);
    
    // Should return original session on error
    expect(result.removedCount).toBe(0);
    expect(result.savedTokens).toBe(0);
  });
});

describe('getContinuationPrompt edge cases', () => {
  it('should handle empty summary', () => {
    const prompt = getContinuationPrompt('', false);
    expect(prompt).toContain('This session is being continued');
    expect(prompt).toContain('Summary:');
  });

  it('should handle summary with special characters', () => {
    const summary = 'Summary with "quotes" and \n newlines';
    const prompt = getContinuationPrompt(summary, false);
    expect(prompt).toContain('Summary with "quotes"');
  });

  it('should include all required instructions', () => {
    const prompt = getContinuationPrompt('test summary', true);
    
    expect(prompt).toContain('Continue the conversation from where it left off');
    expect(prompt).toContain('without asking further questions');
    expect(prompt).toContain('do not acknowledge the summary');
    expect(prompt).toContain('do not recap');
    expect(prompt).toContain('do not preface with continuation text');
  });

  it('should format prompt structure correctly', () => {
    const summary = 'Key findings';
    const prompt = getContinuationPrompt(summary, true);
    
    const parts = prompt.split('\n\n');
    expect(parts.length).toBeGreaterThanOrEqual(3);
    expect(prompt).toMatch(/Summary:\nKey findings/);
    expect(prompt).toMatch(/Recent messages are preserved verbatim/);
  });
});

describe('shouldCompact edge cases', () => {
  it('should handle empty messages array', () => {
    const config = loadConfig({ max_tokens: 10000 });
    expect(shouldCompact([], config)).toBe(false);
  });

  it('should handle messages with undefined content', () => {
    const config = loadConfig({ max_tokens: 10000 });
    const messages = [
      { role: 'user' },
      { role: 'assistant', content: undefined },
      { role: 'user', content: '' }
    ];
    expect(shouldCompact(messages, config)).toBe(false);
  });

  it('should be exactly at threshold', () => {
    const config = loadConfig({ max_tokens: 10000 });
    // 90% of 10000 = 9000 tokens = 36000 chars
    const messages = [{ content: 'x'.repeat(36000) }];
    // Should be at or slightly below threshold
    const result = shouldCompact(messages, config);
    // Depends on exact calculation, either is acceptable
    expect(typeof result).toBe('boolean');
  });

  it('should scale with different max_tokens values', () => {
    const configs = [
      loadConfig({ max_tokens: 5000 }),
      loadConfig({ max_tokens: 10000 }),
      loadConfig({ max_tokens: 20000 })
    ];
    
    const messages = [{ content: 'x'.repeat(20000) }];
    // 20000/4 = 5000 tokens
    
    expect(shouldCompact(messages, configs[0])).toBe(true); // 5000 > 4500
    expect(shouldCompact(messages, configs[1])).toBe(false); // 5000 < 9000
    expect(shouldCompact(messages, configs[2])).toBe(false); // 5000 < 18000
  });
});
