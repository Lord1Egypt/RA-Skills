/**
 * Proactive Tools v1.0
 * MCP tools for managing proactive schedules and digests
 */

import { getProactiveScheduler } from '../proactive_scheduler.js';
import { getRecallTrigger } from '../recall_trigger.js';
import { generateDailyDigest, generateWeeklyDigest, formatDigestText } from '../digest_generator.js';
import { z } from 'zod';
import { randomUUID } from 'crypto';

// ─── Schedule Schemas ──────────────────────────────────────────────────────────

const PeriodicSchema = z.object({
  intervalMinutes: z.number().min(1).max(10080).describe('Interval in minutes (1-10080)'),
  query: z.string().optional().describe('Optional recall query context'),
});

const TimeBasedSchema = z.object({
  times: z.array(z.string()).describe('List of HH:MM times'),
  query: z.string().optional().describe('Optional recall query context'),
});

const EventBasedSchema = z.object({
  keywords: z.array(z.string()).optional().describe('Keywords to match against context'),
  categories: z.array(z.string()).optional().describe('Categories to match'),
  query: z.string().optional().describe('Optional recall query context'),
});

const AddScheduleSchema = z.object({
  name: z.string().describe('Schedule name'),
  type: z.enum(['periodic', 'time_based', 'event_based']).describe('Schedule type'),
  config: z.union([PeriodicSchema, TimeBasedSchema, EventBasedSchema]).describe('Schedule config'),
  enabled: z.boolean().optional().default(true),
});

// ─── Tool Implementations ──────────────────────────────────────────────────────

export function memoryProactiveList() {
  const scheduler = getProactiveScheduler();
  const schedules = scheduler.list();
  return {
    content: [{
      type: 'text',
      text: JSON.stringify({
        count: schedules.length,
        schedules: schedules.map(s => ({
          id: s.id,
          name: s.name,
          type: s.type,
          config: s.config,
          enabled: s.enabled,
          createdAt: s.createdAt,
          lastFired: s.lastFired,
        })),
      }, null, 2),
    }],
  };
}

export function memoryProactiveAdd({ name, type, config, enabled = true }) {
  const scheduler = getProactiveScheduler();

  // Validate config
  const validators = {
    periodic: PeriodicSchema,
    time_based: TimeBasedSchema,
    event_based: EventBasedSchema,
  };
  const validator = validators[type];
  if (!validator) {
    return { content: [{ type: 'text', text: `Unknown schedule type: ${type}` }], isError: true };
  }

  const parsed = validator.safeParse(config);
  if (!parsed.success) {
    return { content: [{ type: 'text', text: `Invalid config: ${parsed.error.message}` }], isError: true };
  }

  const schedule = {
    id: randomUUID(),
    name,
    type,
    config: parsed.data,
    enabled,
    createdAt: new Date().toISOString(),
    lastFired: null,
  };

  scheduler.add(schedule);

  return {
    content: [{
      type: 'text',
      text: JSON.stringify({ success: true, schedule: { id: schedule.id, name, type, enabled } }),
    }],
  };
}

export function memoryProactiveRemove({ id }) {
  const scheduler = getProactiveScheduler();
  scheduler.remove(id);
  return {
    content: [{ type: 'text', text: JSON.stringify({ success: true, removed: id }) }],
  };
}

export function memoryDigest({ period = 'daily', topK = 10 } = {}) {
  const digest = period === 'weekly'
    ? generateWeeklyDigest({ topK })
    : generateDailyDigest({ topK });

  const text = formatDigestText(digest);

  return {
    content: [{ type: 'text', text }],
    _digest: digest, // attach for internal use
  };
}

// ─── Tool Registrations (called by index.js) ──────────────────────────────────

export function registerProactiveTools(server) {

  server.registerTool('memory_proactive_list', {
    description: 'List all active proactive recall schedules.',
    inputSchema: z.object({}),
  }, () => memoryProactiveList());

  server.registerTool('memory_proactive_add', {
    description: 'Add a proactive recall schedule. Types: periodic (every N minutes), time_based (specific HH:MM times), event_based (keyword patterns in context).',
    inputSchema: AddScheduleSchema,
  }, (args) => memoryProactiveAdd(args));

  server.registerTool('memory_proactive_remove', {
    description: 'Remove a proactive recall schedule by ID.',
    inputSchema: z.object({
      id: z.string().describe('Schedule ID to remove'),
    }),
  }, (args) => memoryProactiveRemove(args));

  server.registerTool('memory_digest', {
    description: 'Generate a memory digest: daily (past 24h) or weekly (past 7 days). Returns top memories by importance+recency score, grouped by category, with daily activity distribution.',
    inputSchema: z.object({
      period: z.enum(['daily', 'weekly']).optional().default('daily').describe('Digest period'),
      topK: z.number().optional().default(10).describe('Number of top memories to include'),
    }),
  }, (args) => memoryDigest(args));
}
