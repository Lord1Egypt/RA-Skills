#!/usr/bin/env node
/**
 * migrate.js — 数据库迁移执行脚本
 *
 * 按文件名顺序执行 db/migrations/ 下的 SQL 文件 (001_ -> 002_ -> 003_)
 * 支持 D1 (默认) 和 MySQL 两种模式。
 *
 * 用法:
 *   node scripts/migrate.js                  # 默认 D1 模式，输出 SQL 到 stdout
 *   node scripts/migrate.js --db mysql       # MySQL 兼容模式
 *   node scripts/migrate.js --dry-run        # 只打印不执行
 *   node scripts/migrate.js --execute        # 实际执行（通过 D1 API）
 *   node scripts/migrate.js --db mysql --execute  # 通过 mysql CLI 执行
 *
 * 管道到 D1:
 *   node scripts/migrate.js | npx wrangler d1 execute <DB_NAME> --remote
 */

import { readFileSync, readdirSync, existsSync } from 'node:fs';
import { resolve, dirname, basename } from 'node:path';
import { fileURLToPath } from 'node:url';
import { execSync } from 'node:child_process';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
const ROOT = resolve(__dirname, '..');
const MIGRATIONS_DIR = resolve(ROOT, 'db', 'migrations');

// ──────────────────────────────────────────────
// 解析 CLI 参数
// ──────────────────────────────────────────────

function parseArgs() {
  const args = process.argv.slice(2);
  const flags = {
    db: 'd1',        // 'd1' | 'mysql'
    mode: 'stdout',  // 'stdout' | 'dry-run' | 'execute'
  };

  for (let i = 0; i < args.length; i++) {
    switch (args[i]) {
      case '--db':
        flags.db = args[++i] || 'd1';
        break;
      case '--dry-run':
        flags.mode = 'dry-run';
        break;
      case '--execute':
        flags.mode = 'execute';
        break;
      case '--help':
      case '-h':
        printHelp();
        process.exit(0);
    }
  }

  return flags;
}

function printHelp() {
  console.log(`
migrate.js — 数据库迁移执行脚本

用法:
  node scripts/migrate.js [选项]

选项:
  --db <type>    数据库类型: d1 (默认) 或 mysql
  --dry-run      仅打印迁移计划，不执行
  --execute      实际执行迁移（D1 API 或 mysql CLI）
  --help, -h     显示帮助

示例:
  node scripts/migrate.js                          # D1 模式，输出 SQL
  node scripts/migrate.js --db mysql               # MySQL 模式
  node scripts/migrate.js --dry-run                # 查看迁移计划
  node scripts/migrate.js | npx wrangler d1 execute my-db --remote
  node scripts/migrate.js --execute                # 直接执行（需配置 .env）
`);
}

// ──────────────────────────────────────────────
// 扫描迁移文件
// ──────────────────────────────────────────────

function scanMigrations() {
  if (!existsSync(MIGRATIONS_DIR)) {
    console.error('错误: 迁移目录不存在: ' + MIGRATIONS_DIR);
    process.exit(1);
  }

  const files = readdirSync(MIGRATIONS_DIR)
    .filter((f) => f.endsWith('.sql'))
    .sort(); // 按文件名排序: 001_xxx < 002_xxx < 003_xxx

  if (files.length === 0) {
    console.error('错误: 未找到任何 SQL 迁移文件在: ' + MIGRATIONS_DIR);
    process.exit(1);
  }

  return files.map((f) => ({
    filename: f,
    path: resolve(MIGRATIONS_DIR, f),
    content: readFileSync(resolve(MIGRATIONS_DIR, f), 'utf-8'),
  }));
}

// ──────────────────────────────────────────────
// 改写 SQL (D1 vs MySQL 兼容)
// ──────────────────────────────────────────────

function adaptSQL(sql, dbType) {
  if (dbType === 'd1') {
    // D1 (SQLite) 兼容性调整
    return sql
      // 移除 MySQL-only 引擎/字符集子句
      .replace(/ENGINE\s*=\s*\w+\s*/gi, '')
      .replace(/DEFAULT\s+CHARSET\s*=\s*\w+/gi, '')
      .replace(/COLLATE\s*=\s*\w+/gi, '')
      .replace(/COLLATE\s+\w+/gi, '')
      // 移除 ALGORITHM / LOCK 子句
      .replace(/ALGORITHM\s*=\s*\w+/gi, '')
      .replace(/LOCK\s*=\s*\w+/gi, '')
      // AUTO_INCREMENT -> AUTOINCREMENT (SQLite)
      .replace(/AUTO_INCREMENT/gi, 'AUTOINCREMENT')
      // 移除 IF NOT EXISTS on ADD COLUMN (SQLite 不支持)
      .replace(/ADD\s+COLUMN\s+IF\s+NOT\s+EXISTS/gi, 'ADD COLUMN')
      // BIGINT UNSIGNED -> INTEGER (SQLite 没有 unsigned bigint)
      .replace(/BIGINT\s+UNSIGNED/gi, 'INTEGER')
      // INT UNSIGNED -> INTEGER
      .replace(/INT\s+UNSIGNED/gi, 'INTEGER')
      // DECIMAL(10,2) -> REAL
      .replace(/DECIMAL\s*\([^)]+\)/gi, 'REAL')
      // ENUM -> TEXT CHECK
      .replace(/ENUM\s*\([^)]+\)/gi, 'TEXT')
      // JSON -> TEXT
      .replace(/\bJSON\b/gi, 'TEXT')
      // 移除外键约束 (D1 支持有限)
      .replace(/,\s*FOREIGN\s+KEY\s*\([^)]+\)\s*REFERENCES\s*\w+\s*\([^)]+\)\s*(ON\s+DELETE\s+\w+)?/gi, '')
      // 清理多余空格
      .replace(/\n{3,}/g, '\n\n')
      .trim();
  }

  // MySQL 模式 — 保持原样
  return sql;
}

// ──────────────────────────────────────────────
// 执行迁移 (通过 child_process)
// ──────────────────────────────────────────────

function executeMigration(sql, dbType) {
  if (dbType === 'mysql') {
    // 尝试通过 mysql CLI 执行
    try {
      // 从 .env 或环境变量读取配置
      const host = process.env.DB_HOST || 'localhost';
      const port = process.env.DB_PORT || '3306';
      const user = process.env.DB_USER || 'root';
      const pass = process.env.DB_PASSWORD || '';
      const dbName = process.env.DB_NAME || 'website_skeleton';

      const cmd = 'mysql -h ' + host + ' -P ' + port + ' -u ' + user +
        (pass ? ' -p' + pass : '') + ' ' + dbName;

      execSync(cmd, { input: sql, stdio: ['pipe', 'inherit', 'inherit'] });
      return true;
    } catch (err) {
      console.error('MySQL 执行失败:', err.message);
      return false;
    }
  } else {
    // D1 模式 — 直接输出 SQL 到 stdout (用户可管道到 wrangler)
    // 如果设置了 D1_API_TOKEN, 尝试通过 REST API 执行
    const apiToken = process.env.D1_API_TOKEN;
    const dbId = process.env.D1_DATABASE_ID;
    const accountId = process.env.CF_ACCOUNT_ID;

    if (apiToken && dbId && accountId) {
      // 通过 Cloudflare API 执行
      try {
        const body = JSON.stringify({ sql });
        const curlCmd = [
          'curl -s -X POST',
          "'https://api.cloudflare.com/client/v4/accounts/" + accountId + "/d1/database/" + dbId + "/query'",
          '-H "Authorization: Bearer ' + apiToken + '"',
          '-H "Content-Type: application/json"',
          '--data \'' + body.replace(/'/g, "'\\''") + '\'',
        ].join(' ');
        const result = execSync(curlCmd, { encoding: 'utf-8' });
        const parsed = JSON.parse(result);
        if (parsed.success) {
          console.log('D1 迁移成功: ' + parsed.result?.length + ' 条语句执行');
          return true;
        } else {
          console.error('D1 迁移失败:', JSON.stringify(parsed.errors));
          return false;
        }
      } catch (err) {
        console.error('D1 API 调用失败:', err.message);
        return false;
      }
    }

    // 没有 API 凭证 — 直接输出 SQL
    console.log(sql);
    return true;
  }
}

// ──────────────────────────────────────────────
// 打印迁移摘要
// ──────────────────────────────────────────────

function printSummary(migrations, dbType, mode) {
  console.error('\n' + '='.repeat(60));
  console.error('  迁移摘要');
  console.error('='.repeat(60));
  console.error('  数据库类型: ' + dbType.toUpperCase());
  console.error('  执行模式: ' + mode);
  console.error('  迁移文件数: ' + migrations.length);
  console.error('  ' + '-'.repeat(40));

  let totalStatements = 0;
  for (const m of migrations) {
    const stmts = m.content.split(';').filter((s) => s.trim().length > 0 && !s.trim().startsWith('--')).length;
    totalStatements += stmts;
    console.error('  ' + m.filename + ' (' + stmts + ' 条语句)');
  }

  console.error('  ' + '-'.repeat(40));
  console.error('  总计: ' + totalStatements + ' 条 SQL 语句');
  console.error('='.repeat(60));

  if (mode === 'dry-run') {
    console.error('\n  ⚠️  dry-run 模式 — 未实际执行任何语句');
  } else if (mode === 'stdout') {
    console.error('\n  ℹ️  输出模式 — SQL 已写入 stdout，可管道到 D1 执行');
    console.error('  示例: node scripts/migrate.js | npx wrangler d1 execute my-db --remote');
  } else {
    console.error('\n  ✅  迁移执行完成');
  }
}

// ──────────────────────────────────────────────
// 主入口
// ──────────────────────────────────────────────

function main() {
  const flags = parseArgs();
  const migrations = scanMigrations();

  console.error('发现 ' + migrations.length + ' 个迁移文件');
  console.error('按顺序执行: ' + migrations.map((m) => m.filename).join(' -> '));
  console.error('');

  const allSQL = [];

  for (const m of migrations) {
    const adapted = adaptSQL(m.content, flags.db);
    allSQL.push('-- ============================================================');
    allSQL.push('-- 迁移: ' + m.filename);
    allSQL.push('-- ============================================================');
    allSQL.push('');
    allSQL.push(adapted);
    allSQL.push('');
  }

  const fullSQL = allSQL.join('\n');

  if (flags.mode === 'dry-run') {
    // dry-run: 只打印摘要，不输出 SQL
    console.error('  [dry-run] 已处理的迁移文件:');
    for (const m of migrations) {
      const lineCount = m.content.split('\n').length;
      console.error('    ' + m.filename + ' (' + lineCount + ' 行)');
    }
    printSummary(migrations, flags.db, flags.mode);
    return;
  }

  if (flags.mode === 'execute') {
    console.error('正在执行迁移...');
    const success = executeMigration(fullSQL, flags.db);
    if (!success) {
      console.error('迁移执行失败');
      process.exit(1);
    }
    printSummary(migrations, flags.db, flags.mode);
    return;
  }

  // stdout 模式 — 输出 SQL 到 stdout
  process.stdout.write(fullSQL + '\n');
  printSummary(migrations, flags.db, flags.mode);
}

main();
