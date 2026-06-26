/**
 * 测试 cloud-functions/utils/db.js
 *
 * 注意：db.query 返回的是 D1 all() 的结果（Promise），但 queryOne 未 await query()，
 * 因此 mock 中 all() 使用同步 mockReturnValue 以测试预期业务逻辑。
 */
import { describe, it, expect, vi } from 'vitest';
import { query, queryOne, execute, withTransaction } from '../../cloud-functions/utils/db.js';

function createMockDB() {
  const mockDB = {
    prepare: vi.fn().mockReturnThis(),
    bind: vi.fn().mockReturnThis(),
    // 使用同步返回值：queryOne 没有 await query，需要 all() 直接返回数组
    all: vi.fn().mockReturnValue([{ id: 1, name: 'test' }]),
    run: vi.fn().mockReturnValue({ success: true, meta: { changes: 1 } }),
    transaction: vi.fn(fn => vi.fn(() => fn())),
  };
  return mockDB;
}

function makeEnv(db) {
  return { DB: db ?? createMockDB() };
}

// ===================== db.query =====================

describe('db.query', () => {
  it('替换 {tenant} 占位符并绑定参数', () => {
    const db = createMockDB();
    const env = makeEnv(db);

    query(env, 'SELECT * FROM orders WHERE tenant_id = {tenant} AND id = ?', [42], 'tenant-abc');

    expect(db.prepare).toHaveBeenCalledWith('SELECT * FROM orders WHERE tenant_id = ? AND id = ?');
    expect(db.bind).toHaveBeenCalledWith('tenant-abc', 42);
    expect(db.all).toHaveBeenCalledOnce();
  });

  it('不带 params 时只绑定 tenant', () => {
    const db = createMockDB();
    const env = makeEnv(db);

    query(env, 'SELECT * FROM orders WHERE tenant_id = {tenant}', undefined, 'tenant-xyz');

    expect(db.bind).toHaveBeenCalledWith('tenant-xyz');
  });

  it('包含多个 {tenant} 占位符时全部替换', () => {
    const db = createMockDB();
    const env = makeEnv(db);

    query(
      env,
      'SELECT * FROM orders WHERE tenant_id = {tenant} AND org_id = {tenant}',
      [],
      't1',
    );

    expect(db.prepare).toHaveBeenCalledWith(
      'SELECT * FROM orders WHERE tenant_id = ? AND org_id = ?',
    );
    expect(db.bind).toHaveBeenCalledWith('t1');
  });

  it('SQL 缺少 {tenant} 时同步抛出 Error', () => {
    const env = makeEnv();
    expect(() => query(env, 'SELECT * FROM orders', [], 't1')).toThrow(
      'SQL missing {tenant} placeholder',
    );
  });

  it('env.DB 未配置时同步抛出 Error', () => {
    expect(() => query({}, 'SELECT * FROM {tenant}', [], 't1')).toThrow(
      'Database not configured',
    );
  });

  it('env 为 null/undefined 时同步抛出 Error', () => {
    expect(() => query(null, 'SELECT * FROM {tenant}', [], 't1')).toThrow(
      'Database not configured',
    );
    expect(() => query(undefined, 'SELECT * FROM {tenant}', [], 't1')).toThrow(
      'Database not configured',
    );
  });

  it('返回 all() 的结果', () => {
    const db = createMockDB();
    const env = makeEnv(db);

    const result = query(env, 'SELECT * FROM {tenant}', [], 't1');

    expect(result).toEqual([{ id: 1, name: 'test' }]);
  });
});

// ===================== db.queryOne =====================

describe('db.queryOne', () => {
  it('返回第一行结果', () => {
    const db = createMockDB();
    const env = makeEnv(db);

    const result = queryOne(env, 'SELECT * FROM {tenant} WHERE id = ?', [1], 't1');

    expect(result).toEqual({ id: 1, name: 'test' });
  });

  it('结果为空时返回 null', () => {
    const db = createMockDB();
    db.all.mockReturnValue([]);
    const env = makeEnv(db);

    const result = queryOne(env, 'SELECT * FROM {tenant} WHERE id = ?', [999], 't1');

    expect(result).toBeNull();
  });

  it('内部调用 query 并透传参数', () => {
    const db = createMockDB();
    db.all.mockReturnValue([{ id: 42 }]);
    const env = makeEnv(db);

    const result = queryOne(env, 'SELECT * FROM {tenant} WHERE id = ?', [1], 't1');

    expect(db.prepare).toHaveBeenCalledWith('SELECT * FROM ? WHERE id = ?');
    expect(db.bind).toHaveBeenCalledWith('t1', 1);
    expect(result).toEqual({ id: 42 });
  });

  it('SQL 缺少 {tenant} 时同步抛出 Error（透传 query 的校验）', () => {
    const env = makeEnv();
    expect(() => queryOne(env, 'SELECT * FROM orders', [], 't1')).toThrow(
      'SQL missing {tenant} placeholder',
    );
  });
});

// ===================== db.execute =====================

describe('db.execute', () => {
  it('替换 {tenant} 并调用 run()', () => {
    const db = createMockDB();
    const env = makeEnv(db);

    const result = execute(
      env,
      'UPDATE orders SET status = ? WHERE tenant_id = {tenant}',
      ['paid'],
      't1',
    );

    expect(db.prepare).toHaveBeenCalledWith(
      'UPDATE orders SET status = ? WHERE tenant_id = ?',
    );
    expect(db.bind).toHaveBeenCalledWith('t1', 'paid');
    expect(db.run).toHaveBeenCalledOnce();
    expect(result).toEqual({ success: true, meta: { changes: 1 } });
  });

  it('SQL 缺少 {tenant} 时同步抛出 Error', () => {
    const env = makeEnv();
    expect(() => execute(env, 'UPDATE orders SET status = ?', ['paid'], 't1')).toThrow(
      'SQL missing {tenant} placeholder',
    );
  });

  it('env.DB 未配置时同步抛出 Error', () => {
    expect(() => execute({}, 'UPDATE {tenant} SET status = ?', ['paid'], 't1')).toThrow(
      'Database not configured',
    );
  });
});

// ===================== withTransaction =====================

describe('db.withTransaction', () => {
  it('在事务中执行 query/execute', () => {
    const db = createMockDB();
    const env = makeEnv(db);
    const callback = vi.fn();

    withTransaction(env, 't1', (ctx) => {
      callback(ctx);
      ctx.query('SELECT * FROM orders WHERE tenant_id = {tenant}', []);
      ctx.execute('UPDATE orders SET status = ? WHERE tenant_id = {tenant}', ['shipped']);
    });

    // 验证事务被调用
    expect(db.transaction).toHaveBeenCalledOnce();
    expect(callback).toHaveBeenCalledOnce();

    // 验证 ctx.query 使用了正确的 tenant
    expect(db.bind).toHaveBeenNthCalledWith(1, 't1');
    expect(db.bind).toHaveBeenNthCalledWith(2, 't1', 'shipped');
  });

  it('ctx.queryOne 返回第一行', () => {
    const db = createMockDB();
    db.all.mockReturnValue([{ id: 1, status: 'PENDING' }]);
    const env = makeEnv(db);

    let order;
    withTransaction(env, 't1', (ctx) => {
      order = ctx.queryOne('SELECT * FROM orders WHERE id = {tenant} AND id = ? FOR UPDATE', [1]);
    });

    expect(order).toEqual({ id: 1, status: 'PENDING' });
  });

  it('ctx.queryOne 结果为空返回 null', () => {
    const db = createMockDB();
    db.all.mockReturnValue([]);
    const env = makeEnv(db);

    let result;
    withTransaction(env, 't1', (ctx) => {
      result = ctx.queryOne('SELECT * FROM orders WHERE id = {tenant} AND id = ?', [999]);
    });

    expect(result).toBeNull();
  });

  it('ctx.query 缺少 {tenant} 时同步抛出 Error', () => {
    const env = makeEnv();

    expect(() =>
      withTransaction(env, 't1', (ctx) => {
        ctx.query('SELECT * FROM orders WHERE id = ?', [1]);
      }),
    ).toThrow('SQL missing {tenant} placeholder');
  });

  it('ctx.execute 缺少 {tenant} 时同步抛出 Error', () => {
    const env = makeEnv();

    expect(() =>
      withTransaction(env, 't1', (ctx) => {
        ctx.execute('UPDATE orders SET status = ?', ['paid']);
      }),
    ).toThrow('SQL missing {tenant} placeholder');
  });

  it('env.DB 未配置时同步抛出 Error', () => {
    expect(() => withTransaction({}, 't1', () => {})).toThrow(
      'Database not configured',
    );
  });

  it('回调返回值透传', () => {
    const db = createMockDB();
    const env = makeEnv(db);

    const result = withTransaction(env, 't1', (ctx) => {
      ctx.query('SELECT * FROM {tenant}', []);
      return 'transaction-result';
    });

    expect(result).toBe('transaction-result');
  });

  it('ctx 对象包含 tenant 字段', () => {
    const env = makeEnv();

    let ctxRef;
    withTransaction(env, 'my-tenant', (ctx) => {
      ctxRef = ctx;
    });

    expect(ctxRef).toBeDefined();
    expect(ctxRef.tenant).toBe('my-tenant');
  });
});
