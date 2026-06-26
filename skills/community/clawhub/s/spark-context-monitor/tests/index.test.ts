/**
 * Context Usage Checker 单元测试
 */

import { estimateTokens, getModelContextWindow, generateProgressBar, formatNumber, generateContextReport, matchesTrigger } from '../src/index';

describe('Context Usage Checker', () => {
  describe('estimateTokens', () => {
    it('should estimate Chinese characters correctly', () => {
      const text = '你好世界'; // 4 个中文字符
      const tokens = estimateTokens(text);
      // 4 / 1.5 ≈ 2.67 → 3 tokens
      expect(tokens).toBeGreaterThan(1);
      expect(tokens).toBeLessThan(5);
    });

    it('should estimate English characters correctly', () => {
      const text = 'Hello World'; // 11 个英文字符（含空格）
      const tokens = estimateTokens(text);
      // 11 / 4 ≈ 2.75 → 3 tokens
      expect(tokens).toBeGreaterThan(1);
      expect(tokens).toBeLessThan(5);
    });

    it('should handle mixed text', () => {
      const text = '你好 Hello 世界 World';
      const tokens = estimateTokens(text);
      expect(tokens).toBeGreaterThan(0);
    });

    it('should return 0 for empty string', () => {
      expect(estimateTokens('')).toBe(0);
      expect(estimateTokens(null as any)).toBe(0);
    });
  });

  describe('getModelContextWindow', () => {
    it('should return correct window for qwen3.5-plus', () => {
      expect(getModelContextWindow('qwen3.5-plus')).toBe(256000);
    });

    it('should return correct window for qwen3.5', () => {
      expect(getModelContextWindow('qwen3.5')).toBe(256000);
    });

    it('should return correct window for qwen-max', () => {
      expect(getModelContextWindow('qwen-max')).toBe(32000);
    });

    it('should return correct window for claude', () => {
      expect(getModelContextWindow('claude')).toBe(200000);
    });

    it('should return correct window for gpt-4', () => {
      expect(getModelContextWindow('gpt-4')).toBe(128000);
    });

    it('should return default for unknown model', () => {
      expect(getModelContextWindow('unknown-model')).toBe(128000);
    });

    it('should handle case insensitivity', () => {
      expect(getModelContextWindow('QWEN3.5-PLUS')).toBe(256000);
      expect(getModelContextWindow('Claude')).toBe(200000);
    });
  });

  describe('generateProgressBar', () => {
    it('should generate correct progress bar for 0%', () => {
      const bar = generateProgressBar(0);
      expect(bar).toBe('░'.repeat(20));
    });

    it('should generate correct progress bar for 100%', () => {
      const bar = generateProgressBar(100);
      expect(bar).toBe('▓'.repeat(20));
    });

    it('should generate correct progress bar for 50%', () => {
      const bar = generateProgressBar(50);
      expect(bar).toBe('▓'.repeat(10) + '░'.repeat(10));
    });

    it('should always return 20 characters', () => {
      for (const percentage of [0, 25, 50, 75, 100]) {
        const bar = generateProgressBar(percentage);
        expect(bar.length).toBe(20);
      }
    });
  });

  describe('formatNumber', () => {
    it('should format small numbers', () => {
      expect(formatNumber(123)).toBe('123');
    });

    it('should format thousands', () => {
      expect(formatNumber(1234)).toBe('1,234');
    });

    it('should format millions', () => {
      expect(formatNumber(1234567)).toBe('1,234,567');
    });

    it('should format large token counts', () => {
      expect(formatNumber(256000)).toBe('256,000');
      expect(formatNumber(128000)).toBe('128,000');
    });
  });

  describe('generateContextReport', () => {
    it('should generate normal status report', () => {
      const report = generateContextReport(35000, 256000, 'qwen3.5-plus');
      expect(report).toContain('📊');
      expect(report).toContain('正常');
      expect(report).toContain('✅');
    });

    it('should generate warning status report', () => {
      const report = generateContextReport(180000, 256000, 'qwen3.5-plus');
      expect(report).toContain('⚠️');
      expect(report).toContain('警告');
      expect(report).toContain('/new');
    });

    it('should generate critical status report', () => {
      const report = generateContextReport(240000, 256000, 'qwen3.5-plus');
      expect(report).toContain('🚨');
      expect(report).toContain('严重');
      expect(report).toContain('立即');
    });

    it('should include progress bar', () => {
      const report = generateContextReport(50000, 256000, 'qwen3.5-plus');
      expect(report).toContain('▓');
      expect(report).toContain('░');
    });

    it('should format numbers with commas', () => {
      const report = generateContextReport(256000, 256000, 'qwen3.5-plus');
      expect(report).toContain('256,000');
    });
  });

  describe('matchesTrigger', () => {
    it('should match /token command', () => {
      expect(matchesTrigger('/token')).toBe(true);
    });

    it('should match Chinese triggers', () => {
      expect(matchesTrigger('查上下文')).toBe(true);
      expect(matchesTrigger('查 token')).toBe(true);
      expect(matchesTrigger('上下文使用率')).toBe(true);
    });

    it('should match English triggers', () => {
      expect(matchesTrigger('token usage')).toBe(true);
      expect(matchesTrigger('context usage')).toBe(true);
    });

    it('should be case insensitive', () => {
      expect(matchesTrigger('/TOKEN')).toBe(true);
      expect(matchesTrigger('TOKEN USAGE')).toBe(true);
    });

    it('should not match unrelated messages', () => {
      expect(matchesTrigger('你好')).toBe(false);
      expect(matchesTrigger('今天天气不错')).toBe(false);
      expect(matchesTrigger('random message')).toBe(false);
    });
  });
});
