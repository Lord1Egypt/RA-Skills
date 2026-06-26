import { describe, test, expect, beforeAll, afterAll } from '@jest/globals';
import {
  ping,
  preflight_check,
  contact_search,
  contact_get_userlist
} from '../src/index';

describe('wecom-deep-op Skill Tests', () => {
  beforeAll(() => {
    // 确保环境变量已设置（测试环境）
    if (!process.env.WECOM_CONTACT_BASE_URL) {
      console.warn('WECOM_CONTACT_BASE_URL not set, some tests will be skipped');
    }
  });

  test('ping returns healthy status', async () => {
    const result = await ping();
    expect(result.errcode).toBe(0);
    expect(result.data.status).toBe('healthy');
    expect(result.data.service).toBe('wecom-deep-op');
  });

  test('preflight_check detects missing config', async () => {
    const result = await preflight_check();
    // 在没有配置时，应该有 missing_services
    expect(result.errcode).toBeGreaterThanOrEqual(0);
    if (result.data.status === 'incomplete') {
      expect(result.data.missing_services).toBeDefined();
      expect(Array.isArray(result.data.missing_services)).toBe(true);
    }
  });

  test('contact_search filters results', async () => {
    // 需要配置 WECOM_CONTACT_BASE_URL
    if (!process.env.WECOM_CONTACT_BASE_URL) {
      console.log('Skipping contact_search test - no config');
      return;
    }

    const result = await contact_search('不存在的用户xyz');
    expect(result.errcode).toBe(0);
    expect(result.userlist).toBeDefined();
    expect(result.matched_count).toBe(0);
  });

  test('contact_get_userlist returns array', async () => {
    if (!process.env.WECOM_CONTACT_BASE_URL) {
      console.log('Skipping contact_get_userlist test - no config');
      return;
    }

    const result = await contact_get_userlist();
    expect(result.errcode).toBe(0);
    expect(result.userlist).toBeDefined();
    expect(Array.isArray(result.userlist)).toBe(true);
  });
});
