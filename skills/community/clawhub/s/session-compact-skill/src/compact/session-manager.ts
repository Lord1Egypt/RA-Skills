/**
 * Session Manager - High-level session lifecycle management
 * Provides automatic compaction, session tracking, and state management
 */

import {
  Session,
  ConversationMessage,
  SessionMetadata,
  TokenUsage,
  calculateTotalTokens,
  createUserMessage,
  createSystemMessage
} from './types.js';
import { SessionStore, createSessionStore } from './session-store.js';
import {
  compactSession,
  estimateTokenCount,
  shouldCompact,
  calculateActualTokenUsage,
  getContinuationPrompt
} from './engine.js';
import { loadConfig, type CompactConfig } from './config.js';

/**
 * Session state
 */
export enum SessionState {
  ACTIVE = 'active',
  COMPACTING = 'compacting',
  COMPACTED = 'compacted',
  ERROR = 'error'
}

/**
 * Session event for tracking changes
 */
export interface SessionEvent {
  type: 'message_added' | 'compacted' | 'error' | 'state_changed';
  timestamp: string;
  data: any;
}

/**
 * Session Manager - Manages session lifecycle with automatic compaction
 */
export class SessionManager {
  private session: Session;
  private sessionId: string;
  private store: SessionStore;
  private config: CompactConfig;
  private state: SessionState;
  private events: SessionEvent[];
  private autoCompactEnabled: boolean;

  constructor(
    sessionId: string,
    config: CompactConfig,
    store?: SessionStore
  ) {
    this.sessionId = sessionId;
    this.config = config;
    this.store = store || createSessionStore();
    this.session = { version: 1, messages: [] };
    this.state = SessionState.ACTIVE;
    this.events = [];
    this.autoCompactEnabled = config.auto_compact !== false;
  }

  /**
   * Load existing session or create new one
   */
  static async create(
    sessionId: string,
    config?: Partial<CompactConfig>,
    store?: SessionStore
  ): Promise<SessionManager> {
    const manager = new SessionManager(
      sessionId,
      loadConfig(config),
      store
    );

    // Try to load existing session
    if (manager.store.sessionExists(sessionId)) {
      try {
        manager.session = manager.store.loadSession(sessionId);
        manager.state = SessionState.ACTIVE;
        manager.trackEvent('state_changed', { state: SessionState.ACTIVE });
      } catch (error) {
        console.warn(`[SessionManager] Failed to load session ${sessionId}, creating new:`, error);
      }
    }

    return manager;
  }

  /**
   * Add a user message to the session
   */
  addUserMessage(text: string, usage?: TokenUsage): void {
    if (this.state === SessionState.ERROR) {
      throw new Error('Cannot add message to session in error state');
    }

    const message = createUserMessage(text);
    if (usage) {
      message.usage = usage;
    }

    this.session.messages.push(message);
    this.trackEvent('message_added', { role: 'user', messageIndex: this.session.messages.length - 1 });

    // Auto-compact if enabled
    if (this.autoCompactEnabled) {
      this.checkAndAutoCompact();
    }
  }

  /**
   * Add an assistant message to the session
   */
  addAssistantMessage(message: ConversationMessage): void {
    if (this.state === SessionState.ERROR) {
      throw new Error('Cannot add message to session in error state');
    }

    this.session.messages.push(message);
    this.trackEvent('message_added', { role: 'assistant', messageIndex: this.session.messages.length - 1 });

    // Auto-compact if enabled
    if (this.autoCompactEnabled) {
      this.checkAndAutoCompact();
    }
  }

  /**
   * Add a tool result to the session
   */
  addToolResult(
    toolUseId: string,
    toolName: string,
    output: string,
    isError: boolean
  ): void {
    if (this.state === SessionState.ERROR) {
      throw new Error('Cannot add message to session in error state');
    }

    const message = {
      role: 'tool' as const,
      blocks: [{
        type: 'tool_result' as const,
        tool_use_id: toolUseId,
        tool_name: toolName,
        output,
        is_error: isError
      }],
      usage: undefined
    };

    this.session.messages.push(message);
    this.trackEvent('message_added', { role: 'tool', messageIndex: this.session.messages.length - 1 });
  }

  /**
   * Add a system message (typically from compaction)
   */
  addSystemMessage(text: string): void {
    if (this.state === SessionState.ERROR) {
      throw new Error('Cannot add message to session in error state');
    }

    const message = createSystemMessage(text);
    this.session.messages.push(message);
    this.trackEvent('message_added', { role: 'system', messageIndex: this.session.messages.length - 1 });
  }

  /**
   * Check if compaction is needed and perform it automatically
   */
  private async checkAndAutoCompact(): Promise<void> {
    if (!this.autoCompactEnabled || this.state === SessionState.COMPACTING) {
      return;
    }

    if (shouldCompact(this.session.messages as any[], this.config)) {
      await this.compact();
    }
  }

  /**
   * Manually compact the session
   */
  async compact(): Promise<void> {
    if (this.state === SessionState.COMPACTING) {
      console.warn('[SessionManager] Compaction already in progress');
      return;
    }

    this.state = SessionState.COMPACTING;
    this.trackEvent('state_changed', { state: SessionState.COMPACTING });

    try {
      const result = await compactSession(this.session.messages, this.config);

      if (result.removedCount === 0) {
        console.log('[SessionManager] No compaction needed');
        this.state = SessionState.ACTIVE;
        this.trackEvent('state_changed', { state: SessionState.ACTIVE });
        return;
      }

      // Create continuation message
      const continuationMessage = createSystemMessage(
        getContinuationPrompt(result.summary, this.config.preserve_recent > 0)
      );

      // Keep only recent messages and add continuation
      const recentMessages = this.session.messages.slice(-this.config.preserve_recent);
      this.session.messages = [continuationMessage, ...recentMessages];

      this.state = SessionState.COMPACTED;
      this.trackEvent('compacted', {
        removedCount: result.removedCount,
        savedTokens: result.savedTokens,
        originalTokens: result.originalTokens,
        compactedTokens: result.compactedTokens
      });
      this.trackEvent('state_changed', { state: SessionState.COMPACTED });

      console.log(
        `[SessionManager] Compacted: removed ${result.removedCount} messages, ` +
        `saved ${result.savedTokens} tokens (${((result.savedTokens / result.originalTokens) * 100).toFixed(1)}%)`
      );

      // Save session
      this.save();
    } catch (error) {
      this.state = SessionState.ERROR;
      this.trackEvent('error', { error: error instanceof Error ? error.message : String(error) });
      this.trackEvent('state_changed', { state: SessionState.ERROR });
      console.error('[SessionManager] Compaction failed:', error);
      throw error;
    }
  }

  /**
   * Save session to persistent storage
   */
  save(): void {
    try {
      this.store.saveSession(this.session, this.sessionId);
    } catch (error) {
      console.error('[SessionManager] Failed to save session:', error);
      throw error;
    }
  }

  /**
   * Get current session
   */
  getSession(): Session {
    return { ...this.session };
  }

  /**
   * Get session messages (read-only)
   */
  getMessages(): ReadonlyArray<ConversationMessage> {
    return this.session.messages;
  }

  /**
   * Get estimated token count
   */
  getEstimatedTokens(): number {
    return estimateTokenCount(this.session.messages);
  }

  /**
   * Get actual token usage from metadata
   */
  getActualTokenUsage(): TokenUsage {
    return calculateActualTokenUsage(this.session.messages);
  }

  /**
   * Get session metadata
   */
  getMetadata(): SessionMetadata {
    const usage = this.getActualTokenUsage();
    const compactionCount = this.session.messages.filter(msg =>
      msg.role === 'system' &&
      msg.blocks.some(b =>
        b.type === 'text' &&
        b.text.includes('This session is being continued from a previous conversation')
      )
    ).length;

    return {
      session_id: this.sessionId,
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
      message_count: this.session.messages.length,
      total_input_tokens: usage.input_tokens,
      total_output_tokens: usage.output_tokens,
      total_cache_tokens: usage.cache_creation_input_tokens + usage.cache_read_input_tokens,
      compaction_count: compactionCount
    };
  }

  /**
   * Get session state
   */
  getState(): SessionState {
    return this.state;
  }

  /**
   * Get session events
   */
  getEvents(): ReadonlyArray<SessionEvent> {
    return this.events;
  }

  /**
   * Check if session should be compacted
   */
  shouldCompact(): boolean {
    return shouldCompact(this.session.messages as any[], this.config);
  }

  /**
   * Clear session
   */
  clear(): void {
    this.session = { version: 1, messages: [] };
    this.state = SessionState.ACTIVE;
    this.events = [];
    this.trackEvent('state_changed', { state: SessionState.ACTIVE });
  }

  /**
   * Delete session from storage
   */
  delete(): void {
    if (this.store.sessionExists(this.sessionId)) {
      this.store.deleteSession(this.sessionId);
    }
    this.clear();
  }

  /**
   * Track session event
   */
  private trackEvent(type: SessionEvent['type'], data: any): void {
    this.events.push({
      type,
      timestamp: new Date().toISOString(),
      data
    });

    // Keep only last 100 events
    if (this.events.length > 100) {
      this.events = this.events.slice(-100);
    }
  }

  /**
   * Get session ID
   */
  getSessionId(): string {
    return this.sessionId;
  }

  /**
   * Get config
   */
  getConfig(): CompactConfig {
    return { ...this.config };
  }

  /**
   * Update config
   */
  updateConfig(newConfig: Partial<CompactConfig>): void {
    this.config = { ...this.config, ...newConfig };
    this.autoCompactEnabled = this.config.auto_compact !== false;
  }
}

/**
 * Create a new session manager
 */
export async function createSessionManager(
  sessionId: string,
  config?: Partial<CompactConfig>
): Promise<SessionManager> {
  return SessionManager.create(sessionId, config);
}
