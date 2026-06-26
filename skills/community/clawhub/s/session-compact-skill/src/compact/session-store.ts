/**
 * Session persistence and storage management
 * Provides JSON file-based session storage with version tracking
 */

import { Session, SessionMetadata, SessionError } from './types.js';
import { readFileSync, writeFileSync, existsSync, mkdirSync, readdirSync, statSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { homedir } from 'node:os';

/**
 * Default session storage directory
 */
export const DEFAULT_SESSION_DIR = join(homedir(), '.openclaw', 'sessions');

/**
 * Session storage manager
 */
export class SessionStore {
  private storageDir: string;

  constructor(storageDir: string = DEFAULT_SESSION_DIR) {
    this.storageDir = storageDir;
  }

  /**
   * Initialize storage directory
   */
  initialize(): void {
    if (!existsSync(this.storageDir)) {
      mkdirSync(this.storageDir, { recursive: true });
    }
  }

  /**
   * Get session file path
   */
  private getSessionPath(sessionId: string): string {
    return join(this.storageDir, `${sessionId}.json`);
  }

  /**
   * Save session to file
   */
  saveSession(session: Session, sessionId: string): void {
    this.initialize();
    const path = this.getSessionPath(sessionId);

    try {
      const data = JSON.stringify(session, null, 2);
      writeFileSync(path, data, 'utf-8');
    } catch (error) {
      throw new SessionError(
        `Failed to save session: ${error instanceof Error ? error.message : 'Unknown error'}`,
        'IO_ERROR'
      );
    }
  }

  /**
   * Load session from file
   */
  loadSession(sessionId: string): Session {
    const path = this.getSessionPath(sessionId);

    if (!existsSync(path)) {
      throw new SessionError(`Session not found: ${sessionId}`, 'NOT_FOUND');
    }

    try {
      const data = readFileSync(path, 'utf-8');
      const parsed = JSON.parse(data);

      // Validate session structure
      if (!parsed.version || !Array.isArray(parsed.messages)) {
        throw new SessionError('Invalid session format', 'INVALID_FORMAT');
      }

      return parsed as Session;
    } catch (error) {
      if (error instanceof SessionError) {
        throw error;
      }
      if (error instanceof SyntaxError) {
        throw new SessionError(
          `Failed to parse session: ${error.message}`,
          'PARSE_ERROR'
        );
      }
      throw new SessionError(
        `Failed to load session: ${error instanceof Error ? error.message : 'Unknown error'}`,
        'IO_ERROR'
      );
    }
  }

  /**
   * Check if session exists
   */
  sessionExists(sessionId: string): boolean {
    return existsSync(this.getSessionPath(sessionId));
  }

  /**
   * Delete session
   */
  deleteSession(sessionId: string): void {
    const path = this.getSessionPath(sessionId);

    if (!existsSync(path)) {
      throw new SessionError(`Session not found: ${sessionId}`, 'NOT_FOUND');
    }

    try {
      const { unlinkSync } = require('node:fs');
      unlinkSync(path);
    } catch (error) {
      throw new SessionError(
        `Failed to delete session: ${error instanceof Error ? error.message : 'Unknown error'}`,
        'IO_ERROR'
      );
    }
  }

  /**
   * List all sessions with metadata
   */
  listSessions(): SessionMetadata[] {
    this.initialize();

    try {
      const files = readdirSync(this.storageDir).filter(f => f.endsWith('.json'));

      return files.map(file => {
        const path = join(this.storageDir, file);
        const stats = statSync(path);
        const sessionId = file.replace('.json', '');

        // Try to load session to get metadata
        try {
          const session = this.loadSession(sessionId);
          const totalInputTokens = session.messages.reduce((sum, msg) => {
            return sum + (msg.usage?.input_tokens || 0);
          }, 0);
          const totalOutputTokens = session.messages.reduce((sum, msg) => {
            return sum + (msg.usage?.output_tokens || 0);
          }, 0);
          const totalCacheTokens = session.messages.reduce((sum, msg) => {
            return sum + (msg.usage?.cache_creation_input_tokens || 0) +
                   (msg.usage?.cache_read_input_tokens || 0);
          }, 0);

          // Count compaction markers
          const compactionCount = session.messages.filter(msg =>
            msg.role === 'system' &&
            msg.blocks.some(b =>
              b.type === 'text' &&
              b.text.includes('This session is being continued from a previous conversation')
            )
          ).length;

          return {
            session_id: sessionId,
            created_at: stats.birthtime.toISOString(),
            updated_at: stats.mtime.toISOString(),
            message_count: session.messages.length,
            total_input_tokens: totalInputTokens,
            total_output_tokens: totalOutputTokens,
            total_cache_tokens: totalCacheTokens,
            compaction_count: compactionCount
          };
        } catch {
          // Return minimal metadata if session can't be loaded
          return {
            session_id: sessionId,
            created_at: stats.birthtime.toISOString(),
            updated_at: stats.mtime.toISOString(),
            message_count: 0,
            total_input_tokens: 0,
            total_output_tokens: 0,
            total_cache_tokens: 0,
            compaction_count: 0
          };
        }
      });
    } catch (error) {
      throw new SessionError(
        `Failed to list sessions: ${error instanceof Error ? error.message : 'Unknown error'}`,
        'IO_ERROR'
      );
    }
  }

  /**
   * Get storage directory path
   */
  getStorageDir(): string {
    return this.storageDir;
  }

  /**
   * Clean up old sessions (optional cleanup utility)
   */
  cleanupOldSessions(maxAgeDays: number = 30): number {
    this.initialize();

    try {
      const files = readdirSync(this.storageDir).filter(f => f.endsWith('.json'));
      const cutoffDate = new Date();
      cutoffDate.setDate(cutoffDate.getDate() - maxAgeDays);

      let cleanedCount = 0;

      for (const file of files) {
        const path = join(this.storageDir, file);
        const stats = statSync(path);

        if (stats.mtime < cutoffDate) {
          const { unlinkSync } = require('node:fs');
          unlinkSync(path);
          cleanedCount++;
        }
      }

      return cleanedCount;
    } catch (error) {
      console.error('[SessionStore] Failed to cleanup old sessions:', error);
      return 0;
    }
  }
}

/**
 * Create default session store
 */
export function createSessionStore(storageDir?: string): SessionStore {
  return new SessionStore(storageDir);
}
