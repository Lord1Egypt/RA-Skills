import { describe, it, expect } from 'vitest';
import {
  makeKey,
  getTenant,
  DEFAULT_TENANT,
  sessionKey,
  rtMetaKey,
  cartKey,
  aiSessionKey,
  idempotencyKey,
  rateLimitKey,
  productCacheKey,
  KEY_PREFIXES,
  KEY_TTL,
  getShardSessionKey,
  key,
} from '../../sharing/kv-keys.js';

describe('kv-keys.js — makeKey', () => {
  it('joins tenant and parts with colon separator', () => {
    expect(makeKey('tenant1', 'session', 'abc123')).toBe('tenant1:session:abc123');
  });

  it('works with single part', () => {
    expect(makeKey('t', 'session')).toBe('t:session');
  });

  it('works with multiple parts', () => {
    expect(makeKey('t', 'a', 'b', 'c')).toBe('t:a:b:c');
  });

  it('throws Error when tenant is empty string', () => {
    expect(() => makeKey('', 'session', 'x')).toThrow('tenant is required');
  });

  it('throws Error when tenant is undefined', () => {
    expect(() => makeKey(undefined, 'session', 'x')).toThrow('tenant is required');
  });

  it('throws Error when tenant is null', () => {
    expect(() => makeKey(null, 'session', 'x')).toThrow('tenant is required');
  });

  it('throws Error when tenant is the string "undefined"', () => {
    expect(() => makeKey('undefined', 'session', 'x')).toThrow('tenant is required');
  });

  it('throws Error when tenant is the string "null"', () => {
    expect(() => makeKey('null', 'session', 'x')).toThrow('tenant is required');
  });
});

describe('kv-keys.js — key (default export alias)', () => {
  it('key is an alias for makeKey', () => {
    expect(key).toBe(makeKey);
    expect(key('t', 'a')).toBe('t:a');
  });
});

describe('kv-keys.js — getTenant', () => {
  it('returns tenant from payload', () => {
    expect(getTenant({ tenant: 'acme' })).toBe('acme');
  });

  it('returns DEFAULT_TENANT when payload has no tenant', () => {
    expect(getTenant({ sub: '123' })).toBe(DEFAULT_TENANT);
  });

  it('returns DEFAULT_TENANT when payload is empty object', () => {
    expect(getTenant({})).toBe(DEFAULT_TENANT);
  });

  it('returns DEFAULT_TENANT when payload is null', () => {
    expect(getTenant(null)).toBe(DEFAULT_TENANT);
  });

  it('returns DEFAULT_TENANT when payload is undefined', () => {
    expect(getTenant(undefined)).toBe(DEFAULT_TENANT);
  });

  it('DEFAULT_TENANT is "default"', () => {
    expect(DEFAULT_TENANT).toBe('default');
  });
});

describe('kv-keys.js — KEY_PREFIXES', () => {
  it('has all expected prefixes', () => {
    expect(KEY_PREFIXES).toEqual({
      SESSION: 'session',
      REFRESH_TOKEN: 'rt',
      CART: 'cart',
      AI_SESSION: 'ai',
      IDEMPOTENCY: 'pay:idempotency',
      RATE_LIMIT: 'rl',
      ANALYTICS: 'analytics',
      PRODUCT_CACHE: 'product',
    });
  });
});

describe('kv-keys.js — KEY_TTL', () => {
  it('has all expected TTL values', () => {
    expect(KEY_TTL.SESSION).toBe(86400);
    expect(KEY_TTL.REFRESH_TOKEN).toBe(604800);
    expect(KEY_TTL.CART).toBe(2592000);
    expect(KEY_TTL.AI_SESSION).toBe(86400);
    expect(KEY_TTL.IDEMPOTENCY).toBe(86400);
    expect(KEY_TTL.RATE_LIMIT).toBe(120);
    expect(KEY_TTL.PRODUCT_CACHE).toBe(300);
    expect(KEY_TTL.ANALYTICS).toBe(7776000);
  });
});

describe('kv-keys.js — convenience functions', () => {
  it('sessionKey builds correct key', () => {
    expect(sessionKey('t1', 'sess1')).toBe('t1:session:sess1');
  });

  it('rtMetaKey builds correct key', () => {
    expect(rtMetaKey('t1', 42)).toBe('t1:rt:42:meta');
  });

  it('rtMetaKey converts userId to string', () => {
    expect(rtMetaKey('t1', 'user-abc')).toBe('t1:rt:user-abc:meta');
  });

  it('cartKey builds correct key', () => {
    expect(cartKey('t1', 99)).toBe('t1:cart:99');
  });

  it('cartKey converts userId to string', () => {
    expect(cartKey('t1', 'u1')).toBe('t1:cart:u1');
  });

  it('aiSessionKey builds correct key', () => {
    expect(aiSessionKey('t1', 5, 'sess-x')).toBe('t1:ai:5:sess-x');
  });

  it('idempotencyKey builds correct key', () => {
    expect(idempotencyKey('t1', 'trade123')).toBe('t1:pay:idempotency:trade123');
  });

  it('rateLimitKey builds correct key', () => {
    expect(rateLimitKey('t1', 'ip-1.2.3.4', 'w1')).toBe('t1:rl:ip-1.2.3.4:w1');
  });

  it('productCacheKey builds correct key', () => {
    expect(productCacheKey('t1', 100)).toBe('t1:product:100');
  });

  it('productCacheKey converts productId to string', () => {
    expect(productCacheKey('t1', 'prod-1')).toBe('t1:product:prod-1');
  });
});

describe('kv-keys.js — fnv1a (internal, tested via getShardSessionKey)', () => {
  it('getShardSessionKey produces deterministic shard values', () => {
    expect(getShardSessionKey('t1', 'sess-abc')).toBe(getShardSessionKey('t1', 'sess-abc'));
  });

  it('different session IDs produce different shards', () => {
    const shard1 = getShardSessionKey('t1', 'sess-1');
    const shard2 = getShardSessionKey('t1', 'sess-2');
    expect(shard1).not.toEqual(shard2);
  });

  it('shard number is a valid partition index', () => {
    const shard = getShardSessionKey('t1', 'sess-test');
    const shardNum = parseInt(shard.split(':')[1], 10);
    expect(Number.isInteger(shardNum)).toBe(true);
    expect(shardNum).toBeGreaterThanOrEqual(0);
    expect(shardNum).toBeLessThan(64);
  });
});

describe('kv-keys.js — getShardSessionKey', () => {
  it('returns sharded session key with default 64 partitions', () => {
    const result = getShardSessionKey('t1', 'sess-abc');
    expect(result).toMatch(/^session_shard:\d+:/);
    // deterministic
    expect(getShardSessionKey('t1', 'sess-abc')).toBe(getShardSessionKey('t1', 'sess-abc'));
  });

  it('uses specified partitions count', () => {
    const result = getShardSessionKey('t1', 'sess-x', 16);
    const shardNum = parseInt(result.split(':')[1], 10);
    expect(shardNum).toBeGreaterThanOrEqual(0);
    expect(shardNum).toBeLessThan(16);
  });

  it('throws when tenant is empty', () => {
    expect(() => getShardSessionKey('', 'sess-x')).toThrow('tenant is required');
    expect(() => getShardSessionKey(null, 'sess-x')).toThrow('tenant is required');
    expect(() => getShardSessionKey(undefined, 'sess-x')).toThrow('tenant is required');
  });
});
