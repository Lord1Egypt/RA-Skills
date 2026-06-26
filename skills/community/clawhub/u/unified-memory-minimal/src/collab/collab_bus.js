/**
 * Collaboration Bus - Real-time agent collaboration communication
 * Ported from Python collab_bus.py
 * 
 * Features:
 * - Event publish/subscribe
 * - Offline queue support
 * - Event persistence
 * - Broadcast and targeted messaging
 */

import { existsSync, mkdirSync, readFileSync, writeFileSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';
import { EventEmitter } from 'events';

const __dirname = dirname(fileURLToPath(import.meta.url));
const HOME = process.env.HOME || '/root';
const WORKSPACE = join(HOME, '.openclaw', 'workspace');
const COLLAB_DIR = join(WORKSPACE, 'memory', 'collab');
const EVENTS_FILE = join(COLLAB_DIR, 'events.jsonl');
const STATUS_FILE = join(COLLAB_DIR, 'status.json');

/**
 * Event types for collaboration communication
 */
export const EventType = {
  MEMORY_CREATED: 'memory_created',
  MEMORY_UPDATED: 'memory_updated',
  MEMORY_DELETED: 'memory_deleted',
  CONFLICT_DETECTED: 'conflict_detected',
  CONFLICT_RESOLVED: 'conflict_resolved',
  TASK_ASSIGNED: 'task_assigned',
  TASK_COMPLETED: 'task_completed',
  TASK_HANDOFF: 'task_handoff',
  AGENT_ONLINE: 'agent_online',
  AGENT_OFFLINE: 'agent_offline',
  SYNC_REQUEST: 'sync_request',
};

/**
 * CollaborationEvent - 事件结构
 */
export class CollaborationEvent {
  /**
   * @param {object} opts
   */
  constructor({
    eventId = `evt_${Date.now()}_${Math.random().toString(36).slice(2, 8)}`,
    eventType,
    sourceAgent,
    targetAgents = [],
    timestamp = new Date().toISOString(),
    payload = {},
    priority = 'normal',
    acknowledgedBy = []
  }) {
    this.event_id = eventId;
    this.event_type = eventType;
    this.source_agent = sourceAgent;
    this.target_agents = targetAgents;
    this.timestamp = timestamp;
    this.payload = payload;
    this.priority = priority;
    this.acknowledged_by = acknowledgedBy;
  }

  toDict() {
    return {
      event_id: this.event_id,
      event_type: this.event_type,
      source_agent: this.source_agent,
      target_agents: this.target_agents,
      timestamp: this.timestamp,
      payload: this.payload,
      priority: this.priority,
      acknowledged_by: this.acknowledged_by
    };
  }

  static fromDict(data) {
    return new CollaborationEvent({
      eventId: data.event_id,
      eventType: data.event_type,
      sourceAgent: data.source_agent,
      targetAgents: data.target_agents || [],
      timestamp: data.timestamp,
      payload: data.payload || {},
      priority: data.priority || 'normal',
      acknowledgedBy: data.acknowledged_by || []
    });
  }

  static create(eventType, sourceAgent, payload = {}, targetAgents = [], priority = 'normal') {
    return new CollaborationEvent({
      eventType,
      sourceAgent,
      payload,
      targetAgents,
      priority
    });
  }
}

/**
 * Subscription - Agent订阅
 */
export class Subscription {
  /**
   * @param {object} opts
   */
  constructor({
    agentId,
    topics = [],
    callback = null,
    createdAt = new Date().toISOString()
  }) {
    this.agent_id = agentId;
    this.topics = topics; // array of event type strings
    this.callback = callback;
    this.created_at = createdAt;
  }

  toDict() {
    return {
      agent_id: this.agent_id,
      topics: this.topics,
      created_at: this.created_at
    };
  }

  static fromDict(data) {
    return new Subscription({
      agentId: data.agent_id,
      topics: data.topics || [],
      createdAt: data.created_at || ''
    });
  }

  /**
   * Check if this subscription matches an event type
   * @param {string} eventType
   * @returns {boolean}
   */
  matches(eventType) {
    return this.topics.includes(eventType) || 
           this.topics.includes('*') || 
           this.topics.includes('all');
  }
}

/**
 * CollaborationBus - 实时协作总线
 */
export class CollaborationBus extends EventEmitter {
  constructor(storagePath = null) {
    super();
    this.storagePath = storagePath || COLLAB_DIR;
    /** @type {Map<string, Subscription[]>} */
    this.subscriptions = new Map();
    /** @type {CollaborationEvent[]} */
    this.eventHistory = [];
    this.running = false;

    // Ensure storage directory exists
    if (!existsSync(this.storagePath)) {
      mkdirSync(this.storagePath, { recursive: true });
    }

    // Load existing state
    this._loadState();
    this._loadEventHistory();
  }

  _loadState() {
    if (!existsSync(STATUS_FILE)) return;
    try {
      const data = JSON.parse(readFileSync(STATUS_FILE, 'utf8'));
      for (const [agentId, subs] of Object.entries(data.subscriptions || {})) {
        this.subscriptions.set(agentId, subs.map(s => Subscription.fromDict(s)));
      }
    } catch (e) {
      console.warn(`Warning: Failed to load state: ${e.message}`);
    }
  }

  _saveState() {
    try {
      const subscriptions = {};
      for (const [agentId, subs] of this.subscriptions) {
        subscriptions[agentId] = subs.map(s => s.toDict());
      }
      const data = {
        subscriptions,
        last_updated: new Date().toISOString()
      };
      writeFileSync(STATUS_FILE, JSON.stringify(data, null, 2), 'utf8');
    } catch (e) {
      console.warn(`Warning: Failed to save state: ${e.message}`);
    }
  }

  _loadEventHistory() {
    if (!existsSync(EVENTS_FILE)) return;
    try {
      const lines = readFileSync(EVENTS_FILE, 'utf8').split('\n');
      for (const line of lines) {
        const trimmed = line.trim();
        if (!trimmed) continue;
        try {
          const event = CollaborationEvent.fromDict(JSON.parse(trimmed));
          this.eventHistory.push(event);
        } catch {
          /* ignore malformed lines */
        }
      }
    } catch (e) {
      console.warn(`Warning: Failed to load event history: ${e.message}`);
    }
  }

  _appendEvent(event) {
    try {
      const line = JSON.stringify(event.toDict(), null, 0);
      writeFileSync(EVENTS_FILE, line + '\n', { flag: 'a', encoding: 'utf8' });
    } catch (e) {
      console.warn(`Warning: Failed to append event: ${e.message}`);
    }
  }

  /**
   * Start the collaboration bus
   */
  start() {
    if (this.running) {
      console.log('Bus already running');
      return;
    }
    this.running = true;
    console.log('Collaboration bus started');
  }

  /**
   * Stop the collaboration bus
   */
  stop() {
    this.running = false;
    this._saveState();
    console.log('Collaboration bus stopped');
  }

  /**
   * Dispatch event to subscribers
   * @param {CollaborationEvent} event
   */
  _dispatchEvent(event) {
    // Emit for Node EventEmitter compatibility
    this.emit(event.event_type, event);

    for (const [agentId, subs] of this.subscriptions) {
      // Skip if source is same as target
      if (agentId === event.source_agent) continue;

      // Check if targeted or broadcast
      const isTargeted = event.target_agents.length === 0 || event.target_agents.includes(agentId);
      if (!isTargeted) continue;

      // Check subscription topics
      for (const sub of subs) {
        if (sub.matches(event.event_type)) {
          // Invoke callback if available
          if (sub.callback && typeof sub.callback === 'function') {
            try {
              sub.callback(event);
            } catch (e) {
              console.error(`Callback error for ${agentId}: ${e.message}`);
            }
          }
        }
      }
    }

    // Store in history
    this.eventHistory.push(event);
    this._appendEvent(event);
  }

  /**
   * Publish an event to the bus
   * @param {CollaborationEvent} event
   * @param {boolean} [immediate=false]
   * @returns {string} event_id
   */
  publish(event, immediate = false) {
    if (immediate || !this.running) {
      this._dispatchEvent(event);
    } else {
      // Queue for async processing
      setImmediate(() => this._dispatchEvent(event));
    }
    return event.event_id;
  }

  /**
   * Subscribe an agent to event topics
   * @param {string} agentId
   * @param {string[]} topics
   * @param {Function} [callback]
   * @returns {Subscription}
   */
  subscribe(agentId, topics, callback = null) {
    const subscription = new Subscription({ agentId, topics, callback });

    if (!this.subscriptions.has(agentId)) {
      this.subscriptions.set(agentId, []);
    }

    // Remove existing subscription for same topics
    const existing = this.subscriptions.get(agentId).filter(
      s => !topics.every(t => s.topics.includes(t))
    );
    existing.push(subscription);
    this.subscriptions.set(agentId, existing);
    this._saveState();

    return subscription;
  }

  /**
   * Unsubscribe an agent from all topics
   * @param {string} agentId
   */
  unsubscribe(agentId) {
    if (this.subscriptions.has(agentId)) {
      this.subscriptions.delete(agentId);
      this._saveState();
    }
  }

  /**
   * Broadcast a memory change event
   * @param {string} memoryId
   * @param {string} changeType - 'created' | 'updated' | 'deleted'
   * @param {string} sourceAgent
   * @param {object} [payload]
   * @returns {string}
   */
  broadcastChange(memoryId, changeType, sourceAgent, payload = null) {
    const eventTypeMap = {
      'created': EventType.MEMORY_CREATED,
      'updated': EventType.MEMORY_UPDATED,
      'deleted': EventType.MEMORY_DELETED
    };

    const eventType = eventTypeMap[changeType] || EventType.MEMORY_UPDATED;
    const event = CollaborationEvent.create(
      eventType,
      sourceAgent,
      { memory_id: memoryId, ...(payload || {}) }
    );

    return this.publish(event);
  }

  /**
   * Get unacknowledged events for an agent
   * @param {string} agentId
   * @returns {CollaborationEvent[]}
   */
  getPendingEvents(agentId) {
    /** @type {CollaborationEvent[]} */
    const pending = [];

    // Get agent's subscribed topics
    const subscribedTopics = new Set();
    if (this.subscriptions.has(agentId)) {
      for (const sub of this.subscriptions.get(agentId)) {
        for (const t of sub.topics) {
          subscribedTopics.add(t);
        }
      }
    }

    // Find unacknowledged events matching subscriptions
    const recentEvents = this.eventHistory.slice(-100);
    for (const event of recentEvents) {
      // Skip if already acknowledged
      if (event.acknowledged_by.includes(agentId)) continue;

      // Skip if source is same agent
      if (event.source_agent === agentId) continue;

      // Check if targeted or broadcast
      const isTargeted = event.target_agents.length === 0 || event.target_agents.includes(agentId);
      if (!isTargeted) continue;

      // Check if event type is subscribed
      if (subscribedTopics.has(event.event_type) || subscribedTopics.has('*') || subscribedTopics.has('all')) {
        pending.push(event);
      }
    }

    return pending;
  }

  /**
   * Acknowledge an event has been processed
   * @param {string} eventId
   * @param {string} agentId
   */
  acknowledge(eventId, agentId) {
    for (const event of this.eventHistory) {
      if (event.event_id === eventId) {
        if (!event.acknowledged_by.includes(agentId)) {
          event.acknowledged_by.push(agentId);
        }
        break;
      }
    }
    this._rewriteEventsFile();
  }

  _rewriteEventsFile() {
    try {
      const lines = this.eventHistory.map(e => JSON.stringify(e.toDict(), null, 0));
      writeFileSync(EVENTS_FILE, lines.join('\n') + '\n', 'utf8');
    } catch (e) {
      console.warn(`Warning: Failed to rewrite events file: ${e.message}`);
    }
  }

  /**
   * Get overall sync state
   * @returns {object}
   */
  getSyncState() {
    const agents = Array.from(this.subscriptions.keys());
    /** @type {object} */
    const pendingCounts = {};
    for (const agentId of agents) {
      pendingCounts[agentId] = this.getPendingEvents(agentId).length;
    }

    return {
      running: this.running,
      total_subscriptions: Array.from(this.subscriptions.values()).reduce((sum, subs) => sum + subs.length, 0),
      agents,
      event_history_size: this.eventHistory.length,
      pending_events: pendingCounts,
      storage_path: this.storagePath
    };
  }

  /**
   * Request sync from one agent to another
   * @param {string} fromAgent
   * @param {string} toAgent
   * @returns {string}
   */
  requestSync(fromAgent, toAgent) {
    const event = CollaborationEvent.create(
      EventType.SYNC_REQUEST,
      fromAgent,
      { request_time: new Date().toISOString() },
      [toAgent]
    );
    return this.publish(event);
  }
}

/**
 * SyncManager - 同步管理器
 * Handles conflict detection and resolution
 */
export class SyncManager {
  /**
   * @param {CollaborationBus} bus
   */
  constructor(bus) {
    this.bus = bus;
    /** @type {Map<string, object>} */
    this.syncStates = new Map();
  }

  /**
   * Check sync status for an agent
   * @param {string} agentId
   * @returns {object}
   */
  checkSyncStatus(agentId) {
    const pending = this.bus.getPendingEvents(agentId);
    const state = this.syncStates.get(agentId) || {};

    return {
      agent_id: agentId,
      pending_events: pending.length,
      last_sync: state.last_sync || null,
      sync_required: pending.length > 0,
      pending_types: [...new Set(pending.map(e => e.event_type))]
    };
  }

  /**
   * Resolve a sync conflict
   * @param {object} conflictData
   * @returns {object}
   */
  resolveConflict(conflictData) {
    const strategy = conflictData.strategy || 'latest_wins';
    const memories = conflictData.memories || [];

    if (memories.length === 0) {
      return { resolved: false, reason: 'No memories to resolve' };
    }

    if (strategy === 'latest_wins') {
      const sorted = [...memories].sort((a, b) => {
        const tsA = a.timestamp || '';
        const tsB = b.timestamp || '';
        return tsB.localeCompare(tsA);
      });
      const winner = sorted[0] || null;

      return {
        resolved: true,
        strategy,
        winner,
        conflict_id: `conf_${Date.now()}_${Math.random().toString(36).slice(2, 6)}`
      };
    } else if (strategy === 'merge') {
      const mergedContent = memories
        .filter(m => m.content || m.text)
        .map(m => m.content || m.text)
        .join('\n');

      return {
        resolved: true,
        strategy,
        merged_content: mergedContent,
        conflict_id: `conf_${Date.now()}_${Math.random().toString(36).slice(2, 6)}`
      };
    }

    return { resolved: false, reason: `Unknown strategy: ${strategy}` };
  }

  /**
   * Perform full sync for an agent
   * @param {string} agentId
   * @returns {object}
   */
  performSync(agentId) {
    const pending = this.bus.getPendingEvents(agentId);
    /** @type {object[]} */
    const results = [];

    for (const event of pending) {
      results.push({
        event_id: event.event_id,
        event_type: event.event_type,
        processed: true
      });

      // Acknowledge the event
      this.bus.acknowledge(event.event_id, agentId);
    }

    // Update sync state
    this.syncStates.set(agentId, {
      last_sync: new Date().toISOString(),
      events_processed: results.length
    });

    return {
      agent_id: agentId,
      synced: true,
      events_processed: results.length,
      results
    };
  }
}

// CLI Interface
const args = process.argv.slice(2);
if (args.length > 0) {
  runCLI(args);
}

export async function runCLI(argv) {
  const [command, ...rest] = argv;
  const bus = new CollaborationBus();

  const parsers = {
    async start() {
      bus.start();
      console.log('Bus started. Press Ctrl+C to stop.');
      // Keep alive
      await new Promise(() => {});
    },

    async stop() {
      bus.stop();
    },

    async status() {
      const status = bus.getSyncState();
      console.log(JSON.stringify(status, null, 2));
    },

    async subscribe() {
      // parse: subscribe <agent_id> --topics <topics>
      const agentId = rest[0];
      const topicsStr = rest.find(a => a.startsWith('--topics='))?.split('=')[1] || 
                        rest.find(a => a === '--topics') ? rest[rest.indexOf('--topics') + 1] : '';
      const topics = topicsStr ? topicsStr.split(',') : [];
      if (!agentId || topics.length === 0) {
        console.log('Usage: subscribe <agent_id> --topics=topic1,topic2');
        return;
      }
      bus.subscribe(agentId, topics);
      console.log(`Subscribed ${agentId} to: ${topics.join(', ')}`);
    },

    async unsubscribe() {
      const agentId = rest[0];
      if (!agentId) {
        console.log('Usage: unsubscribe <agent_id>');
        return;
      }
      bus.unsubscribe(agentId);
      console.log(`Unsubscribed ${agentId}`);
    },

    async pending() {
      const agentId = rest[0];
      if (!agentId) {
        console.log('Usage: pending <agent_id>');
        return;
      }
      const events = bus.getPendingEvents(agentId);
      const result = {
        agent_id: agentId,
        count: events.length,
        events: events.map(e => e.toDict())
      };
      console.log(JSON.stringify(result, null, 2));
    },

    async broadcast() {
      // parse broadcast --type <type> --source <agent> [--payload <json>] [--targets <agents>] [--priority <p>]
      const eventType = rest.find(a => a.startsWith('--type='))?.split('=')[1];
      const source = rest.find(a => a.startsWith('--source='))?.split('=')[1];
      const payloadStr = rest.find(a => a.startsWith('--payload='))?.split('=')[1] || '{}';
      const targetsStr = rest.find(a => a.startsWith('--targets='))?.split('=')[1] || '';
      const priority = rest.find(a => a.startsWith('--priority='))?.split('=')[1] || 'normal';

      if (!eventType || !source) {
        console.log('Usage: broadcast --type=<type> --source=<agent> [--payload=<json>] [--targets=<agents>]');
        return;
      }

      let payload;
      try {
        payload = JSON.parse(payloadStr);
      } catch {
        console.log('Error: Invalid JSON payload');
        return;
      }

      const targets = targetsStr ? targetsStr.split(',') : [];
      const event = CollaborationEvent.create(eventType, source, payload, targets, priority);
      const eventId = bus.publish(event, true);
      console.log(`Event published: ${eventId}`);
    },

    async ack() {
      const [eventId, agentId] = rest;
      if (!eventId || !agentId) {
        console.log('Usage: ack <event_id> <agent_id>');
        return;
      }
      bus.acknowledge(eventId, agentId);
      console.log(`Event ${eventId} acknowledged by ${agentId}`);
    },

    async sync() {
      const agentId = rest[0];
      if (!agentId) {
        console.log('Usage: sync <agent_id>');
        return;
      }
      const syncManager = new SyncManager(bus);
      const result = syncManager.performSync(agentId);
      console.log(JSON.stringify(result, null, 2));
    }
  };

  if (parsers[command]) {
    await parsers[command]();
  } else {
    console.log(`Unknown command: ${command}`);
    console.log('Available: start, stop, status, subscribe, unsubscribe, pending, broadcast, ack, sync');
  }
}
