/**
 * Bun:sqlite compatibility wrapper around better-sqlite3.
 * Exposes the same API surface that Zouroboros memory code uses.
 */
import Sqlite3 from 'better-sqlite3';

interface RunResult {
  changes: number;
  lastInsertRowid: number | bigint;
}

class QueryStatement<T = Record<string, unknown>> {
  private stmt: Sqlite3.Statement;
  constructor(stmt: Sqlite3.Statement) { this.stmt = stmt; }
  all(...params: unknown[]): T[] { return this.stmt.all(...params) as T[]; }
  get(...params: unknown[]): T | null { return (this.stmt.get(...params) ?? null) as T | null; }
  run(...params: unknown[]): RunResult { return this.stmt.run(...params) as RunResult; }
}

export class Database {
  private _db: Sqlite3.Database;

  constructor(path: string, options?: { readonly?: boolean }) {
    this._db = new Sqlite3(path, options);
  }

  exec(sql: string): void { this._db.exec(sql); }

  query<T = Record<string, unknown>>(sql: string): QueryStatement<T> {
    return new QueryStatement<T>(this._db.prepare(sql));
  }

  prepare(sql: string): QueryStatement {
    return new QueryStatement(this._db.prepare(sql));
  }

  run(sql: string, params: unknown[] = []): RunResult {
    return this._db.prepare(sql).run(...params) as RunResult;
  }

  close(): void { this._db.close(); }
}
