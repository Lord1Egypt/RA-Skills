import {
  estimateTokenCount,
  mergeCompactedSummaries,
  getContinuationPrompt,
  shouldCompact,
  extractSummaryHighlights,
  extractTimeline
} from '../engine.js';

describe('Token Estimation', () => {
  describe('estimateTokenCount', () => {
    it('should estimate tokens for empty messages', () => {
      const count = estimateTokenCount([]);
      expect(count).toBe(0);
    });

    it('should estimate tokens for single message', () => {
      const messages = [{ content: 'hello world' }];
      const count = estimateTokenCount(messages);
      // 'hello world' = 11 chars, 11/4 = 2.75, ceil = 3
      expect(count).toBe(3);
    });

    it('should estimate tokens for multiple messages', () => {
      const messages = [
        { content: 'hello' },
        { content: 'world test' }
      ];
      const count = estimateTokenCount(messages);
      // 'hello' = 5/4 = 1.25 -> 2, 'world test' = 10/4 = 2.5 -> 3
      expect(count).toBe(5);
    });

    it('should handle messages without content', () => {
      const messages = [
        { content: 'test' },
        {},
        { content: '' }
      ];
      const count = estimateTokenCount(messages);
      expect(count).toBe(1); // only 'test' contributes
    });

    it('should handle long text', () => {
      const longText = 'a'.repeat(1000);
      const messages = [{ content: longText }];
      const count = estimateTokenCount(messages);
      expect(count).toBe(250); // 1000/4 = 250
    });
  });
});

describe('Summary Merging', () => {
  describe('mergeCompactedSummaries', () => {
    it('should return new summary when no existing summary', () => {
      const newSummary = '<summary>New content</summary>';
      const result = mergeCompactedSummaries(undefined, newSummary);
      expect(result).toBe(newSummary);
    });

    it('should merge highlights from both summaries', () => {
      const existing = '<summary>- Old point 1\n- Old point 2</summary>';
      const newSum = '<summary>- New point 1</summary>';
      const result = mergeCompactedSummaries(existing, newSum);
      
      expect(result).toContain('Previously compacted context:');
      expect(result).toContain('Newly compacted context:');
      expect(result).toContain('Old point 1');
      expect(result).toContain('New point 1');
    });

    it('should merge timelines from both summaries', () => {
      const existing = '<summary>- Key timeline:\n - user: action 1</summary>';
      const newSum = '<summary>- Key timeline:\n - assistant: response</summary>';
      const result = mergeCompactedSummaries(existing, newSum);
      
      expect(result).toContain('- user: action 1');
      expect(result).toContain('- assistant: response');
    });

    it('should limit merged timeline to 10 items', () => {
      const existingLines = Array(6).fill(' - user: old').join('\n');
      const newLines = Array(6).fill(' - assistant: new').join('\n');
      const existing = `<summary>- Key timeline:${existingLines}</summary>`;
      const newSum = `<summary>- Key timeline:${newLines}</summary>`;
      
      const result = mergeCompactedSummaries(existing, newSum);
      const timelineMatch = result.match(/- Key timeline:([\s\S]*?)(?:<\/summary>)/);
      expect(timelineMatch).toBeTruthy();
      const timelineLines = timelineMatch![1].split('\n').filter(l => l.trim());
      expect(timelineLines.length).toBeLessThanOrEqual(10);
    });

    it('should handle empty highlights', () => {
      const existing = '<summary>- Scope: 5 messages</summary>';
      const newSum = '<summary>- Scope: 3 messages</summary>';
      const result = mergeCompactedSummaries(existing, newSum);
      
      expect(result).toContain('Previously compacted context:');
      expect(result).toContain('Newly compacted context:');
    });
  });
});

describe('Continuation Prompt', () => {
  describe('getContinuationPrompt', () => {
    it('should include preamble and summary', () => {
      const summary = 'Test summary content';
      const prompt = getContinuationPrompt(summary, false);
      
      expect(prompt).toContain('This session is being continued');
      expect(prompt).toContain('Summary:');
      expect(prompt).toContain('Test summary content');
    });

    it('should include recent messages note when preserveRecent is true', () => {
      const prompt = getContinuationPrompt('summary', true);
      expect(prompt).toContain('Recent messages are preserved verbatim.');
    });

    it('should not include recent messages note when preserveRecent is false', () => {
      const prompt = getContinuationPrompt('summary', false);
      expect(prompt).not.toContain('Recent messages are preserved verbatim.');
    });

    it('should include resume instructions', () => {
      const prompt = getContinuationPrompt('summary', false);
      expect(prompt).toContain('Continue the conversation from where it left off');
      expect(prompt).toContain('without asking further questions');
      expect(prompt).toContain('do not acknowledge the summary');
    });

    it('should format prompt correctly with all parts', () => {
      const summary = 'Key findings';
      const prompt = getContinuationPrompt(summary, true);
      
      expect(prompt).toMatch(/This session is being continued/);
      expect(prompt).toMatch(/Summary:\nKey findings/);
      expect(prompt).toMatch(/Recent messages are preserved verbatim/);
      expect(prompt).toMatch(/Continue the conversation/);
    });
  });
});

describe('Compaction Decision', () => {
  describe('shouldCompact', () => {
    const mockConfig = {
      max_tokens: 10000,
      preserve_recent: 4,
      auto_compact: true,
      model: ''
    };

    it('should return false for small sessions', () => {
      const messages = [{ content: 'short message' }];
      expect(shouldCompact(messages, mockConfig)).toBe(false);
    });

    it('should return false when tokens below threshold (90%)', () => {
      // 90% of 10000 = 9000 tokens
      // Need ~36000 characters to reach 9000 tokens
      const messages = [{ content: 'x'.repeat(35000) }];
      expect(shouldCompact(messages, mockConfig)).toBe(false);
    });

    it('should return true when tokens exceed threshold (90%)', () => {
      // 90% of 10000 = 9000 tokens
      // Need ~36000+ characters to exceed 9000 tokens
      const messages = [{ content: 'x'.repeat(37000) }];
      expect(shouldCompact(messages, mockConfig)).toBe(true);
    });

    it('should handle multiple messages', () => {
      const messages = [
        { content: 'a'.repeat(10000) },
        { content: 'b'.repeat(10000) },
        { content: 'c'.repeat(10000) }
      ];
      // Total: 30000 chars = 7500 tokens < 9000
      expect(shouldCompact(messages, mockConfig)).toBe(false);
    });

    it('should respect custom max_tokens config', () => {
      const customConfig = { ...mockConfig, max_tokens: 5000 };
      const messages = [{ content: 'x'.repeat(25000) }];
      // 25000/4 = 6250 tokens > 4500 (90% of 5000)
      expect(shouldCompact(messages, customConfig)).toBe(true);
    });
  });
});

describe('Summary Extraction', () => {
  describe('extractSummaryHighlights', () => {
    it('should extract highlights from summary tags', () => {
      const summary = '<summary>- Point 1\n- Point 2\n- Point 3</summary>';
      const highlights = extractSummaryHighlights(summary);
      expect(highlights).toEqual(['- Point 1', '- Point 2', '- Point 3']);
    });

    it('should filter out scope and timeline lines', () => {
      const summary = `<summary>
- Scope: 10 messages
- Point 1
- Key timeline:
 - user: action
- Point 2
</summary>`;
      const highlights = extractSummaryHighlights(summary);
      expect(highlights.some(h => h.includes('Scope:'))).toBe(false);
      expect(highlights.some(h => h.includes('Key timeline:'))).toBe(false);
    });

    it('should limit to 5 highlights', () => {
      const lines = Array(10).fill('').map((_, i) => `- Point ${i}`).join('\n');
      const summary = `<summary>${lines}</summary>`;
      const highlights = extractSummaryHighlights(summary);
      expect(highlights.length).toBe(5);
    });

    it('should handle summary without tags', () => {
      const summary = 'Plain text summary';
      const highlights = extractSummaryHighlights(summary);
      expect(highlights).toEqual(['Plain text summary']);
    });
  });

  describe('extractTimeline', () => {
    it('should extract timeline from summary', () => {
      const summary = `Summary
- Key timeline:
 - user: action 1
 - assistant: response
 - user: action 2

More content`;
      const timeline = extractTimeline(summary);
      expect(timeline).toEqual([
        '- user: action 1',
        '- assistant: response',
        '- user: action 2'
      ]);
    });

    it('should return empty array when no timeline', () => {
      const summary = 'No timeline here';
      const timeline = extractTimeline(summary);
      expect(timeline).toEqual([]);
    });

    it('should limit to 5 timeline items', () => {
      const lines = Array(10).fill('').map((_, i) => ` - user: action ${i}`).join('\n');
      const summary = `- Key timeline:\n${lines}`;
      const timeline = extractTimeline(summary);
      expect(timeline.length).toBe(5);
    });

    it('should filter only lines starting with -', () => {
      const summary = `- Key timeline:
 - user: valid
  invalid line
 - assistant: also valid
`;
      const timeline = extractTimeline(summary);
      expect(timeline).toEqual(['- user: valid', '- assistant: also valid']);
    });
  });
});
