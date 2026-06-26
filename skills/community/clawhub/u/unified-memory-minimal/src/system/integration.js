/**
 * Memory Integration - 系统集成
 * 
 * Ported from memory_integration.py
 */

import { existsSync, readFileSync, writeFileSync, mkdirSync } from 'fs';
import { join } from 'path';

const HOME = process.env.HOME || '/root';
const WORKSPACE = join(HOME, '.openclaw', 'workspace');
const MEMORY_DIR = join(WORKSPACE, 'memory');
const INTEGRATION_DIR = join(MEMORY_DIR, 'integration');

// ============================================================
// Integrations
// ============================================================

const INTEGRATIONS = {
  feishu: {
    name: '飞书',
    description: '飞书消息、文档、日程集成',
    events: ['message', 'doc_created', 'calendar_event']
  },
  qq: {
    name: 'QQ',
    description: 'QQ消息集成',
    events: ['message']
  },
  wechat: {
    name: '微信',
    description: '微信消息集成',
    events: ['message']
  },
  github: {
    name: 'GitHub',
    description: 'GitHub PR/Issue 集成',
    events: ['pr_opened', 'pr_merged', 'issue_created']
  },
  notion: {
    name: 'Notion',
    description: 'Notion 页面同步',
    events: ['page_created', 'page_updated']
  }
};

// ============================================================
// IntegrationManager
// ============================================================

export class IntegrationManager {
  constructor() {
    mkdirSync(INTEGRATION_DIR, { recursive: true });
    this.configFile = join(INTEGRATION_DIR, 'config.json');
    this.logFile = join(INTEGRATION_DIR, 'events.jsonl');
    this.config = this._loadConfig();
  }

  _loadConfig() {
    if (existsSync(this.configFile)) {
      try { return JSON.parse(readFileSync(this.configFile, 'utf-8')); } catch { /* ignore */ }
    }
    return { enabled: {}, handlers: {} };
  }

  _saveConfig() {
    writeFileSync(this.configFile, JSON.stringify(this.config, null, 2), 'utf-8');
  }

  listIntegrations() {
    return Object.entries(INTEGRATIONS).map(([id, info]) => ({
      id,
      ...info,
      enabled: !!(this.config.enabled && this.config.enabled[id])
    }));
  }

  enable(integrationId) {
    if (!INTEGRATIONS[integrationId]) {
      return { success: false, error: '未知集成' };
    }
    if (!this.config.enabled) this.config.enabled = {};
    this.config.enabled[integrationId] = true;
    this._saveConfig();
    return { success: true };
  }

  disable(integrationId) {
    if (this.config.enabled) {
      delete this.config.enabled[integrationId];
    }
    this._saveConfig();
    return { success: true };
  }

  /**
   * Log an event from an integration
   * @param {string} integrationId
   * @param {string} eventType
   * @param {object} data
   */
  logEvent(integrationId, eventType, data) {
    const entry = {
      integration: integrationId,
      event_type: eventType,
      data,
      timestamp: new Date().toISOString()
    };
    const fs = require('fs');
    fs.appendFileSync(this.logFile, JSON.stringify(entry) + '\n', 'utf-8');
    return entry;
  }

  /**
   * Get recent events
   * @param {string} integrationId
   * @param {number} limit
   */
  getEvents(integrationId, limit = 50) {
    if (!existsSync(this.logFile)) return [];
    const lines = readFileSync(this.logFile, 'utf-8').split('\n').filter(Boolean);
    const events = [];
    for (const line of lines.slice(-limit)) {
      try {
        const entry = JSON.parse(line);
        if (!integrationId || entry.integration === integrationId) {
          events.push(entry);
        }
      } catch { /* skip */ }
    }
    return events.reverse();
  }

  getStatus() {
    const enabled = Object.keys(this.config.enabled || {}).filter(k => this.config.enabled[k]);
    return {
      total_integrations: Object.keys(INTEGRATIONS).length,
      enabled_count: enabled.length,
      enabled,
      integrations: this.listIntegrations()
    };
  }
}

export default { IntegrationManager, INTEGRATIONS };
