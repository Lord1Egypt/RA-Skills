/**
 * Memory OpenClaw Integration - OpenClaw系统集成
 * 
 * Ported from memory_openclaw_integration.py
 */

import { existsSync, readFileSync, writeFileSync, mkdirSync } from 'fs';
import { join } from 'path';

const HOME = process.env.HOME || '/root';
const WORKSPACE = join(HOME, '.openclaw', 'workspace');
const MEMORY_DIR = join(WORKSPACE, 'memory');
const OPENCLAW_DIR = join(MEMORY_DIR, 'openclaw');

// ============================================================
// OpenClawIntegration
// ============================================================

export class OpenClawIntegration {
  constructor() {
    mkdirSync(OPENCLAW_DIR, { recursive: true });
    this.stateFile = join(OPENCLAW_DIR, 'state.json');
    this.state = this._loadState();
  }

  _loadState() {
    if (existsSync(this.stateFile)) {
      try { return JSON.parse(readFileSync(this.stateFile, 'utf-8')); } catch { /* ignore */ }
    }
    return {
      session_count: 0,
      last_session: null,
      agents: {},
      preferences: {}
    };
  }

  _saveState() {
    writeFileSync(this.stateFile, JSON.stringify(this.state, null, 2), 'utf-8');
  }

  /**
   * Record a session
   * @param {string} sessionId
   * @param {object} metadata
   */
  recordSession(sessionId, metadata = {}) {
    this.state.session_count++;
    this.state.last_session = sessionId;
    if (!this.state.sessions) this.state.sessions = {};
    this.state.sessions[sessionId] = {
      id: sessionId,
      metadata,
      started_at: new Date().toISOString(),
      memories_linked: 0
    };
    this._saveState();
    return sessionId;
  }

  /**
   * Link a memory to a session
   * @param {string} sessionId
   * @param {string} memoryId
   */
  linkMemory(sessionId, memoryId) {
    if (this.state.sessions && this.state.sessions[sessionId]) {
      if (!this.state.sessions[sessionId].memory_ids) {
        this.state.sessions[sessionId].memory_ids = [];
      }
      this.state.sessions[sessionId].memory_ids.push(memoryId);
      this.state.sessions[sessionId].memories_linked++;
      this._saveState();
    }
  }

  /**
   * Get session info
   * @param {string} sessionId
   */
  getSession(sessionId) {
    if (this.state.sessions && this.state.sessions[sessionId]) {
      return this.state.sessions[sessionId];
    }
    return null;
  }

  /**
   * Get all sessions
   * @param {number} limit
   */
  getSessions(limit = 20) {
    const sessions = Object.values(this.state.sessions || {});
    return sessions.sort((a, b) => (b.started_at || '').localeCompare(a.started_at || '')).slice(0, limit);
  }

  /**
   * Set agent preference
   * @param {string} agentId
   * @param {string} key
   * @param {any} value
   */
  setPreference(agentId, key, value) {
    if (!this.state.preferences) this.state.preferences = {};
    if (!this.state.preferences[agentId]) this.state.preferences[agentId] = {};
    this.state.preferences[agentId][key] = value;
    this._saveState();
  }

  /**
   * Get agent preferences
   * @param {string} agentId
   */
  getPreferences(agentId) {
    return this.state.preferences && this.state.preferences[agentId] || {};
  }

  getStatus() {
    return {
      total_sessions: this.state.session_count,
      last_session: this.state.last_session,
      agents: Object.keys(this.state.agents || {}).length,
      preferences: Object.keys(this.state.preferences || {}).length
    };
  }
}

export default { OpenClawIntegration };
