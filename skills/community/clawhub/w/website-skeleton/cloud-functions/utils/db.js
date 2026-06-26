/**
 * 数据库工具 — 多租户隔离 + 事务支持
 *
 * Phase 4 P0-3 + W1 实现：
 * - 强制 {tenant} 占位符（IMA C1）
 * - 不导出 db 对象（IMA C2：防止绕过）
 * - 支持事务 withTransaction()（平台专家 B-3）
 *
 * 使用方式：
 *   import { query, execute, withTransaction } from '../utils/db.js';
 *
 *   // 单语句查询
 *   query(env, 'SELECT * FROM orders WHERE tenant_id = {tenant} AND id = ?', [id], tenant);
 *
 *   // 事务
 *   withTransaction(env, tenant, (ctx) => {
 *     const order = ctx.queryOne('SELECT * FROM orders WHERE id = {tenant} AND id = ? FOR UPDATE', [id]);
 *     ctx.execute('UPDATE orders SET status = ? WHERE id = {tenant} AND id = ?', ['paid', id]);
 *   });
 */

// ===================== 单语句接口 =====================

/**
 * 执行带 {tenant} 占位符的 SQL 查询（返回多行）
 * @param {Object} env - 环境变量（含 env.DB D1 绑定）
 * @param {string} sql - SQL 语句，必须包含 {tenant} 占位符
 * @param {Array} [params] - 查询参数
 * @param {string} tenant - 租户 ID
 * @returns {Array} 结果数组
 */
export function query(env, sql, params, tenant) {
  if (!sql.includes('{tenant}')) {
    throw new Error(`SQL missing {tenant} placeholder: ${sql.substring(0, 80)}`);
  }
  if (!env?.DB) throw new Error('Database not configured: env.DB is required');
  const tenantSql = sql.replace(/\{tenant\}/g, '?');
  const stmt = env.DB.prepare(tenantSql);
  return stmt.bind(tenant, ...(params || [])).all();
}

/**
 * 执行带 {tenant} 占位符的 SQL 查询（返回单行）
 * @param {Object} env - 环境变量
 * @param {string} sql - SQL 语句，必须包含 {tenant} 占位符
 * @param {Array} [params] - 查询参数
 * @param {string} tenant - 租户 ID
 * @returns {Object|null} 单行结果
 */
export function queryOne(env, sql, params, tenant) {
  const results = query(env, sql, params, tenant);
  return results[0] || null;
}

/**
 * 执行带 {tenant} 占位符的 SQL 写操作
 * @param {Object} env - 环境变量
 * @param {string} sql - SQL 语句，必须包含 {tenant} 占位符
 * @param {Array} [params] - 参数
 * @param {string} tenant - 租户 ID
 * @returns {Object} 执行结果
 */
export function execute(env, sql, params, tenant) {
  if (!sql.includes('{tenant}')) {
    throw new Error(`SQL missing {tenant} placeholder: ${sql.substring(0, 80)}`);
  }
  if (!env?.DB) throw new Error('Database not configured: env.DB is required');
  const tenantSql = sql.replace(/\{tenant\}/g, '?');
  const stmt = env.DB.prepare(tenantSql);
  return stmt.bind(tenant, ...(params || [])).run();
}

// ⚠️ 故意不 export env.DB 实例本身，防止绕过

// ===================== 事务接口 =====================

/**
 * 执行带 tenant 上下文的事务
 *
 * 使用示例：
 *   withTransaction(env, tenant, (ctx) => {
 *     const product = ctx.queryOne(
 *       'SELECT * FROM products WHERE id = {tenant} AND id = ? FOR UPDATE', [id]
 *     );
 *     ctx.execute(
 *       'UPDATE products SET stock = stock - 1 WHERE id = {tenant} AND id = ?', [id]
 *     );
 *   });
 *
 * @param {Object} env - 环境变量（含 env.DB D1 绑定）
 * @param {string} tenant - 租户 ID
 * @param {Function} callback - 事务回调，接收 ctx 对象
 * @returns {*} 回调返回值
 */
export function withTransaction(env, tenant, callback) {
  if (!env?.DB) throw new Error('Database not configured: env.DB is required');

  const ctx = {
    query: (sql, params) => {
      if (!sql.includes('{tenant}')) {
        throw new Error(`SQL missing {tenant} placeholder: ${sql.substring(0, 80)}`);
      }
      const tenantSql = sql.replace(/\{tenant\}/g, '?');
      return env.DB.prepare(tenantSql).bind(tenant, ...(params || [])).all();
    },
    queryOne: (sql, params) => {
      const results = ctx.query(sql, params);
      return results[0] || null;
    },
    execute: (sql, params) => {
      if (!sql.includes('{tenant}')) {
        throw new Error(`SQL missing {tenant} placeholder: ${sql.substring(0, 80)}`);
      }
      const tenantSql = sql.replace(/\{tenant\}/g, '?');
      return env.DB.prepare(tenantSql).bind(tenant, ...(params || [])).run();
    },
    tenant,
  };

  // D1 事务：使用 env.DB.transaction()
  const tx = env.DB.transaction(() => {
    return callback(ctx);
  });

  return tx();
}
