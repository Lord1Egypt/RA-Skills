import Database from "better-sqlite3";
import { join } from "node:path";
import { homedir } from "node:os";

export interface ArchiveMessage {
  id?: number;
  sessionKey: string;
  sessionId: string;
  role: "user" | "assistant" | "system" | "tool";
  content: string;
  model?: string;
  tokens?: number;
  createdAt: number;
  // 新增元数据字段
  channel?: string;      // 消息来源渠道 (wecom/tui/openclaw-weixin等)
  accountId?: string;    // 账号标识
  messageId?: string;    // 消息唯一ID
  messageType?: string;  // 消息类型 (text/voice/image/file)
  toolName?: string;     // 工具名称 (如果是tool call)
  mediaPath?: string;    // 媒体文件路径 (如果有附件)
  parentSessionKey?: string; // 父会话key (子会话用)
  tokensInput?: number;  // 输入token数
  tokensOutput?: number; // 输出token数
  costUsd?: number;      // 预估费用
}

// 操作记录接口
export interface Operation {
  id?: number;
  sessionKey?: string;
  operationType: string;  // file_write/file_edit/file_delete/exec/config_change/gateway_restart/login/logout/plugin_install/etc
  target: string;         // 操作目标（文件路径/命令/配置项等）
  details?: string;       // 详情（JSON格式）
  result?: string;       // 结果（success/failed/error）
  operator?: string;     // 操作者（user/agent/system）
  createdAt: number;
}

// Token使用记录接口
export interface TokenUsage {
  id?: number;
  sessionKey?: string;
  sessionId?: string;
  model: string;
  promptTokens?: number;
  completionTokens?: number;
  totalTokens?: number;
  costUsd?: number;
  source?: string;      // 'api' | 'estimated' | 'fallback'
  isEstimated?: number;  // 1=估算, 0=真实
  timestamp?: string;    // ISO格式时间
  createdAt: number;
}

export interface SessionArchiveDb {
  insertMessage(msg: ArchiveMessage): void;
  insertOperation(op: Operation): void;
  insertTokenUsage(tu: TokenUsage): void;
  getMessages(sessionKey: string, limit?: number): ArchiveMessage[];
  getMessagesBySessionId(sessionId: string, limit?: number): ArchiveMessage[];
  getOperations(sessionKey?: string, operationType?: string, limit?: number): Operation[];
  getTokenUsage(sessionKey?: string, model?: string, limit?: number): TokenUsage[];
  close(): void;
  db: Database.Database;
}

export function createSessionArchiveDb(dbPath?: string): SessionArchiveDb {
  const resolvedPath = resolveDbPath(dbPath);
  const db = new Database(resolvedPath);
  db.pragma("journal_mode = WAL");
  db.pragma("foreign_keys = ON");

  db.exec(`
    CREATE TABLE IF NOT EXISTS messages (
      id           INTEGER PRIMARY KEY AUTOINCREMENT,
      session_key  TEXT NOT NULL,
      session_id   TEXT NOT NULL,
      role         TEXT NOT NULL CHECK(role IN ('user','assistant','system','tool')),
      content      TEXT NOT NULL DEFAULT '',
      model        TEXT,
      tokens       INTEGER,
      created_at   INTEGER NOT NULL,
      -- 新增元数据字段
      channel      TEXT,
      account_id   TEXT,
      message_id   TEXT,
      message_type TEXT,
      tool_name    TEXT,
      media_path   TEXT,
      parent_session_key TEXT,
      tokens_input INTEGER,
      tokens_output INTEGER,
      cost_usd     REAL
    );

    CREATE INDEX IF NOT EXISTS idx_messages_session_key ON messages(session_key, created_at);
    CREATE INDEX IF NOT EXISTS idx_messages_session_id   ON messages(session_id, created_at);
    CREATE INDEX IF NOT EXISTS idx_messages_created_at   ON messages(created_at);
    CREATE INDEX IF NOT EXISTS idx_messages_channel      ON messages(channel, created_at);
    CREATE INDEX IF NOT EXISTS idx_messages_message_type ON messages(message_type, created_at);
  `);

  // 创建 operations 表（记录操作历史）
  db.exec(`
    CREATE TABLE IF NOT EXISTS operations (
      id           INTEGER PRIMARY KEY AUTOINCREMENT,
      session_key  TEXT,
      operation_type TEXT NOT NULL,  -- file_write/file_edit/file_delete/exec/config_change/gateway_restart/login/logout/plugin_install
      target       TEXT NOT NULL,    -- 操作目标（文件路径/命令/配置项等）
      details      TEXT,             -- 详情（JSON格式）
      result       TEXT,             -- 结果（success/failed/error）
      operator     TEXT,             -- 操作者（user/agent/system）
      created_at   INTEGER NOT NULL
    );

    CREATE INDEX IF NOT EXISTS idx_ops_type ON operations(operation_type, created_at);
    CREATE INDEX IF NOT EXISTS idx_ops_session ON operations(session_key, created_at);
    CREATE INDEX IF NOT EXISTS idx_ops_target ON operations(target, created_at);
    CREATE INDEX IF NOT EXISTS idx_ops_created_at ON operations(created_at);
  `);

  // 创建 token_usage 表（记录 Token 消耗）
  db.exec(`
    CREATE TABLE IF NOT EXISTS token_usage (
      id               INTEGER PRIMARY KEY AUTOINCREMENT,
      session_key      TEXT,
      session_id       TEXT,
      model            TEXT NOT NULL,
      prompt_tokens    INTEGER,
      completion_tokens INTEGER,
      total_tokens     INTEGER,
      cost_usd         REAL,
      source           TEXT DEFAULT 'unknown',  -- 'api' | 'estimated' | 'fallback'
      is_estimated     INTEGER DEFAULT 0,        -- 1=估算, 0=真实
      timestamp        TEXT,                    -- ISO格式时间
      created_at       INTEGER NOT NULL
    );

    CREATE INDEX IF NOT EXISTS idx_token_session ON token_usage(session_key, created_at);
    CREATE INDEX IF NOT EXISTS idx_token_model ON token_usage(model, created_at);
    CREATE INDEX IF NOT EXISTS idx_token_created_at ON token_usage(created_at);
    CREATE INDEX IF NOT EXISTS idx_token_source ON token_usage(source, created_at);
  `);

  return {
    insertMessage(msg: ArchiveMessage): void {
      const stmt = db.prepare(`
        INSERT INTO messages (session_key, session_id, role, content, model, tokens, created_at, 
          channel, account_id, message_id, message_type, tool_name, media_path, parent_session_key,
          tokens_input, tokens_output, cost_usd)
        VALUES (@sessionKey, @sessionId, @role, @content, @model, @tokens, @createdAt,
          @channel, @accountId, @messageId, @messageType, @toolName, @mediaPath, @parentSessionKey,
          @tokensInput, @tokensOutput, @costUsd)
      `);
      stmt.run({
        sessionKey: msg.sessionKey,
        sessionId: msg.sessionId,
        role: msg.role,
        content: msg.content,
        model: msg.model ?? null,
        tokens: msg.tokens ?? null,
        createdAt: msg.createdAt,
        channel: msg.channel ?? null,
        accountId: msg.accountId ?? null,
        messageId: msg.messageId ?? null,
        messageType: msg.messageType ?? null,
        toolName: msg.toolName ?? null,
        mediaPath: msg.mediaPath ?? null,
        parentSessionKey: msg.parentSessionKey ?? null,
        tokensInput: msg.tokensInput ?? null,
        tokensOutput: msg.tokensOutput ?? null,
        costUsd: msg.costUsd ?? null,
      });
    },

    insertOperation(op: Operation): void {
      const stmt = db.prepare(`
        INSERT INTO operations (session_key, operation_type, target, details, result, operator, created_at)
        VALUES (@sessionKey, @operationType, @target, @details, @result, @operator, @createdAt)
      `);
      stmt.run({
        sessionKey: op.sessionKey ?? null,
        operationType: op.operationType,
        target: op.target,
        details: op.details ?? null,
        result: op.result ?? null,
        operator: op.operator ?? null,
        createdAt: op.createdAt,
      });
    },

    insertTokenUsage(tu: TokenUsage): void {
      const stmt = db.prepare(`
        INSERT INTO token_usage (session_key, session_id, model, prompt_tokens, completion_tokens, 
          total_tokens, cost_usd, source, is_estimated, timestamp, created_at)
        VALUES (@sessionKey, @sessionId, @model, @promptTokens, @completionTokens, 
          @totalTokens, @costUsd, @source, @isEstimated, @timestamp, @createdAt)
      `);
      stmt.run({
        sessionKey: tu.sessionKey ?? null,
        sessionId: tu.sessionId ?? null,
        model: tu.model,
        promptTokens: tu.promptTokens ?? null,
        completionTokens: tu.completionTokens ?? null,
        totalTokens: tu.totalTokens ?? null,
        costUsd: tu.costUsd ?? null,
        source: tu.source ?? 'unknown',
        isEstimated: tu.isEstimated ?? 0,
        timestamp: tu.timestamp ?? null,
        createdAt: tu.createdAt,
      });
    },

    getMessages(sessionKey, limit = 100): ArchiveMessage[] {
      return db
        .prepare(
          `SELECT id, session_key AS sessionKey, session_id AS sessionId,
                  role, content, model, tokens, created_at AS createdAt
           FROM messages
           WHERE session_key = ?
           ORDER BY created_at ASC, id ASC
           LIMIT ?`,
        )
        .all(sessionKey, limit) as ArchiveMessage[];
    },

    getMessagesBySessionId(sessionId, limit = 100): ArchiveMessage[] {
      return db
        .prepare(
          `SELECT id, session_key AS sessionKey, session_id AS sessionId,
                  role, content, model, tokens, created_at AS createdAt
           FROM messages
           WHERE session_id = ?
           ORDER BY created_at ASC, id ASC
           LIMIT ?`,
        )
        .all(sessionId, limit) as ArchiveMessage[];
    },

    getOperations(sessionKey?: string, operationType?: string, limit = 100): Operation[] {
      let sql = `SELECT id, session_key AS sessionKey, operation_type AS operationType,
                 target, details, result, operator, created_at AS createdAt
           FROM operations WHERE 1=1`;
      const params: unknown[] = [];
      
      if (sessionKey) {
        sql += ` AND session_key = ?`;
        params.push(sessionKey);
      }
      if (operationType) {
        sql += ` AND operation_type = ?`;
        params.push(operationType);
      }
      
      sql += ` ORDER BY created_at DESC, id DESC LIMIT ?`;
      params.push(limit);
      
      return db.prepare(sql).all(...params) as Operation[];
    },

    getTokenUsage(sessionKey?: string, model?: string, limit = 100): TokenUsage[] {
      let sql = `SELECT id, session_key AS sessionKey, session_id AS sessionId, model,
                 prompt_tokens AS promptTokens, completion_tokens AS completionTokens,
                 total_tokens AS totalTokens, cost_usd AS costUsd, created_at AS createdAt
           FROM token_usage WHERE 1=1`;
      const params: unknown[] = [];
      
      if (sessionKey) {
        sql += ` AND session_key = ?`;
        params.push(sessionKey);
      }
      if (model) {
        sql += ` AND model = ?`;
        params.push(model);
      }
      
      sql += ` ORDER BY created_at DESC, id DESC LIMIT ?`;
      params.push(limit);
      
      return db.prepare(sql).all(...params) as TokenUsage[];
    },

    close: () => db.close(),
    db,
  };
}

function resolveDbPath(dbPath?: string): string {
  if (dbPath && dbPath.trim()) return dbPath.trim();
  return join(homedir(), ".openclaw", "session-archive.db");
}
