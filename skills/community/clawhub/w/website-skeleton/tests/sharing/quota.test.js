import { describe, it, expect, beforeEach, vi } from 'vitest';
import {
  HARD_LIMITS,
  SOFT_LIMITS,
  checkQuota,
  incrementQuota,
  resetQuota,
  getSlidingWindowCount,
  recordBillingEvent,
  checkBillingQuota,
} from '../../sharing/quota.js';

describe('quota.js — constants', () => {
  it('HARD_LIMITS has expected values', () => {
    expect(HARD_LIMITS).toEqual({
      kv_ops: 10000,
      storage: 10485760,
      api_calls: 1000,
    });
  });

  it('SOFT_LIMITS is 90% of hard limits', () => {
    expect(SOFT_LIMITS.kv_ops).toBe(9000);
    expect(SOFT_LIMITS.storage).toBe(9437184); // floor(10485760 * 0.9)
    expect(SOFT_LIMITS.api_calls).toBe(900);
  });
});

describe('quota.js — checkQuota', () => {
  let mockKV;
  let env;

  beforeEach(() => {
    mockKV = {
      _store: {},
      get: vi.fn(async (key) => mockKV._store[key] || null),
      put: vi.fn(async (key, val, opts) => {
        mockKV._store[key] = val;
      }),
      delete: vi.fn(async (key) => {
        delete mockKV._store[key];
      }),
    };
    env = { KV: mockKV };
  });

  it('returns allowed when below soft limit', async () => {
    mockKV._store['quota:tenant1:kv_ops'] = '100';
    const result = await checkQuota(env, 'tenant1', 'kv_ops');
    expect(result.allowed).toBe(true);
    expect(result.remaining).toBe(9900);
    expect(result.current).toBe(100);
    expect(result.limit).toBe(10000);
  });

  it('returns warning when above soft limit but below hard limit', async () => {
    mockKV._store['quota:tenant1:kv_ops'] = '9500';
    const result = await checkQuota(env, 'tenant1', 'kv_ops');
    expect(result.allowed).toBe(true);
    expect(result.warning).toBe('NEAR_QUOTA_LIMIT');
    expect(result.remaining).toBe(500);
  });

  it('returns blocked when above hard limit', async () => {
    mockKV._store['quota:tenant1:kv_ops'] = '10000';
    const result = await checkQuota(env, 'tenant1', 'kv_ops');
    expect(result.allowed).toBe(false);
    expect(result.reason).toBe('QUOTA_EXCEEDED');
    expect(result.hard).toBe(true);
  });

  it('returns allowed but degradedMode when KV is not available', async () => {
    const result = await checkQuota({}, 'tenant1', 'kv_ops');
    expect(result.allowed).toBe(true);
    expect(result.degradedMode).toBe(true);
  });

  it('returns allowed but degradedMode when KV throws', async () => {
    env.KV.get = vi.fn().mockRejectedValue(new Error('KV down'));
    const result = await checkQuota(env, 'tenant1', 'kv_ops');
    expect(result.allowed).toBe(true);
    expect(result.degradedMode).toBe(true);
  });

  it('defaults type to kv_ops', async () => {
    mockKV._store['quota:tenant1:kv_ops'] = '50';
    const result = await checkQuota(env, 'tenant1');
    expect(result.allowed).toBe(true);
    expect(result.current).toBe(50);
  });

  it('handles unknown type by using default limits', async () => {
    const result = await checkQuota(env, 't1', 'unknown_type');
    expect(result.limit).toBe(10000);
  });

  it('handles non-existent KV key as zero', async () => {
    const result = await checkQuota(env, 't1', 'kv_ops');
    expect(result.allowed).toBe(true);
    expect(result.current).toBe(0);
    expect(result.remaining).toBe(10000);
  });
});

describe('quota.js — incrementQuota', () => {
  let mockKV;
  let env;

  beforeEach(() => {
    mockKV = {
      _store: {},
      get: vi.fn(async (key) => mockKV._store[key] || null),
      put: vi.fn(async (key, val, opts) => {
        mockKV._store[key] = val;
      }),
    };
    env = { KV: mockKV };
  });

  it('increments quota by default amount of 1', async () => {
    await incrementQuota(env, 't1', 'kv_ops');
    expect(mockKV.put).toHaveBeenCalledWith(
      'quota:t1:kv_ops',
      '1',
      expect.objectContaining({ expirationTtl: 86400 })
    );
  });

  it('increments existing quota', async () => {
    mockKV._store['quota:t1:kv_ops'] = '5';
    await incrementQuota(env, 't1', 'kv_ops', 3);
    expect(mockKV._store['quota:t1:kv_ops']).toBe('8');
  });

  it('does nothing when KV is unavailable', async () => {
    await incrementQuota({}, 't1', 'kv_ops');
    // no error thrown
  });

  it('does not throw on KV error', async () => {
    env.KV.get = vi.fn().mockRejectedValue(new Error('KV down'));
    await expect(incrementQuota(env, 't1', 'kv_ops')).resolves.not.toThrow();
  });
});

describe('quota.js — resetQuota', () => {
  let mockKV;
  let env;

  beforeEach(() => {
    mockKV = {
      _store: {
        'quota:t1:kv_ops': '500',
        'quota:t1:api_calls': '100',
        'quota:t1:storage': '1000',
      },
      delete: vi.fn(async (key) => {
        delete mockKV._store[key];
      }),
    };
    env = { KV: mockKV };
  });

  it('resets all quota types when no type is specified', async () => {
    await resetQuota(env, 't1');
    expect(mockKV.delete).toHaveBeenCalledWith('quota:t1:kv_ops');
    expect(mockKV.delete).toHaveBeenCalledWith('quota:t1:storage');
    expect(mockKV.delete).toHaveBeenCalledWith('quota:t1:api_calls');
  });

  it('resets specific quota type', async () => {
    await resetQuota(env, 't1', 'kv_ops');
    expect(mockKV.delete).toHaveBeenCalledWith('quota:t1:kv_ops');
    expect(mockKV.delete).not.toHaveBeenCalledWith('quota:t1:api_calls');
  });

  it('does not throw when KV is missing', async () => {
    await expect(resetQuota({}, 't1', 'kv_ops')).resolves.not.toThrow();
  });

  it('does not throw on KV error', async () => {
    env.KV.delete = vi.fn().mockRejectedValue(new Error('KV down'));
    await expect(resetQuota(env, 't1', 'kv_ops')).resolves.not.toThrow();
  });
});

describe('quota.js — sliding window billing', () => {
  let mockKV;
  let env;

  beforeEach(() => {
    let store = {};
    mockKV = {
      _store: store,
      get: vi.fn(async (key) => store[key] || null),
      put: vi.fn(async (key, val, opts) => {
        store[key] = val;
      }),
      list: vi.fn(async ({ prefix }) => {
        const keys = Object.keys(store).filter(k => k.startsWith(prefix));
        return { keys: keys.map(k => ({ name: k })) };
      }),
    };
    env = { KV: mockKV };
  });

  it('getSlidingWindowCount returns 0 when no KV', async () => {
    const count = await getSlidingWindowCount({}, 't1', 'api_calls');
    expect(count).toBe(0);
  });

  it('getSlidingWindowCount returns 0 for empty data', async () => {
    const count = await getSlidingWindowCount(env, 't1', 'api_calls');
    expect(count).toBe(0);
  });

  it('getSlidingWindowCount aggregates matching slots', async () => {
    const now = Date.now();
    const slot1 = Math.floor(now / 60000) * 60000;
    const slot2 = slot1 - 60000;
    mockKV._store[`billing:sw:t1:api_calls:${slot1}`] = '10';
    mockKV._store[`billing:sw:t1:api_calls:${slot2}`] = '5';
    const count = await getSlidingWindowCount(env, 't1', 'api_calls');
    expect(count).toBe(15);
  });

  it('getSlidingWindowCount ignores slots outside window', async () => {
    const oldSlot = Date.now() - 2 * 60 * 60 * 1000; // 2 hours ago
    mockKV._store[`billing:sw:t1:api_calls:${oldSlot}`] = '100';
    const count = await getSlidingWindowCount(env, 't1', 'api_calls', 60);
    expect(count).toBe(0);
  });

  it('recordBillingEvent stores a slot entry', async () => {
    await recordBillingEvent(env, 't1', 'api_calls', 1);
    const keys = Object.keys(mockKV._store);
    expect(keys.length).toBe(1);
    expect(keys[0]).toMatch(/^billing:sw:t1:api_calls:\d+$/);
    expect(mockKV._store[keys[0]]).toBe('1');
  });

  it('recordBillingEvent does nothing when no KV', async () => {
    await expect(recordBillingEvent({}, 't1', 'api_calls')).resolves.not.toThrow();
  });

  it('checkBillingQuota returns allowed when under limit', async () => {
    const result = await checkBillingQuota(env, 't1', 'api_calls', 100);
    expect(result.allowed).toBe(true);
    expect(result.count).toBe(0);
    expect(result.remaining).toBe(100);
  });

  it('checkBillingQuota returns upgrade when over limit', async () => {
    mockKV._store[`billing:sw:t1:api_calls:${Math.floor(Date.now() / 60000) * 60000}`] = '150';
    const result = await checkBillingQuota(env, 't1', 'api_calls', 100);
    expect(result.allowed).toBe(false);
    expect(result.upgrade).toBe(true);
    expect(result.count).toBe(150);
    expect(result.message).toContain('超出免费额度');
  });
});
