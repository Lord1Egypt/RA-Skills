/**
 * Relationship OS — Bootstrap Hook
 *
 * Injects a relationship context summary at the start of each agent session.
 * Reads state files under .relationship/, generates a ~150 token context injection.
 *
 * Debug log output: .relationship/debug.log
 */

import type { HookHandler } from 'openclaw/hooks';
import { readFileSync, readdirSync, existsSync, appendFileSync, mkdirSync } from 'fs';
import { join } from 'path';

// ====== Debug Logging ======

function debugLog(relDir: string, level: 'INFO' | 'WARN' | 'ERROR', module: string, msg: string): void {
  try {
    const now = new Date().toISOString();
    const line = `[${now}] [${level}] [${module}] ${msg}\n`;
    appendFileSync(join(relDir, 'debug.log'), line);
  } catch {
    // Logging failure should not affect main flow
  }
}

// ====== Type Definitions ======

interface RelationshipState {
  stage: string;
  stageStarted: string;
  interactionCount: number;
  emotionBaseline: { valence: number; arousal: number };
  userPatterns: {
    activeHours: number[];
    avgMessagesPerDay: number;
    lastSeen: string;
  };
  milestones: Array<{ type: string; date: string; note: string }>;
}

interface Thread {
  id: string;
  type: string;
  status: string;
  followUpAt: string;
  context: string;
  priority: string;
}

interface Secrets {
  nicknames: { user_calls_agent: string[]; agent_calls_user: string[] };
  inside_jokes: Array<{ context: string; reference: string }>;
  shared_goals: Array<{ goal: string; status: string }>;
  agreements: Array<{ rule: string }>;
}

interface Stance {
  values: Array<{ topic: string; position: string; strength: number }>;
}

// ====== Utility Functions ======

function readJsonSafe<T>(path: string, fallback: T, relDir?: string): T {
  try {
    if (!existsSync(path)) {
      if (relDir) debugLog(relDir, 'WARN', 'io', `File not found: ${path}`);
      return fallback;
    }
    const data = JSON.parse(readFileSync(path, 'utf-8')) as T;
    if (relDir) debugLog(relDir, 'INFO', 'io', `Read OK: ${path}`);
    return data;
  } catch (err) {
    if (relDir) debugLog(relDir, 'ERROR', 'io', `JSON parse failed: ${path} — ${err}`);
    return fallback;
  }
}

function getMoodLabel(valence: number): string {
  if (valence > 0.3) return 'positive';
  if (valence < -0.3) return 'negative';
  if (valence > 0.1) return 'slightly positive';
  if (valence < -0.1) return 'slightly negative';
  return 'neutral';
}

function countSecrets(secrets: Secrets): number {
  return (
    secrets.nicknames.user_calls_agent.length +
    secrets.nicknames.agent_calls_user.length +
    secrets.inside_jokes.length +
    secrets.shared_goals.length +
    secrets.agreements.length
  );
}

// ====== Core Builder ======

function buildRelationshipContext(workspaceDir: string): string {
  const relDir = join(workspaceDir, '.relationship');

  if (!existsSync(relDir)) {
    return '';
  }

  debugLog(relDir, 'INFO', 'bootstrap', '========== Relationship OS Bootstrap ==========');
  debugLog(relDir, 'INFO', 'bootstrap', `workspace: ${workspaceDir}`);

  // 1. Read state
  const state = readJsonSafe<RelationshipState>(join(relDir, 'state.json'), {
    stage: 'initial',
    stageStarted: '',
    interactionCount: 0,
    emotionBaseline: { valence: 0, arousal: 0 },
    userPatterns: { activeHours: [], avgMessagesPerDay: 0, lastSeen: '' },
    milestones: [],
  }, relDir);

  debugLog(relDir, 'INFO', 'state', `stage=${state.stage} interactions=${state.interactionCount} milestones=${state.milestones.length}`);

  // 2. Read pending threads
  const threadsDir = join(relDir, 'threads');
  let pendingThreads: Thread[] = [];
  let totalThreads = 0;
  if (existsSync(threadsDir)) {
    const threadFiles = readdirSync(threadsDir).filter((f) => f.endsWith('.json'));
    totalThreads = threadFiles.length;
    for (const file of threadFiles) {
      const thread = readJsonSafe<Thread>(join(threadsDir, file), null as unknown as Thread, relDir);
      if (thread && thread.status === 'pending') {
        pendingThreads.push(thread);
      }
    }
  }
  debugLog(relDir, 'INFO', 'threads', `total=${totalThreads} pending=${pendingThreads.length}`);

  // 3. Read exclusive memories
  const secrets = readJsonSafe<Secrets>(join(relDir, 'secrets.json'), {
    nicknames: { user_calls_agent: [], agent_calls_user: [] },
    inside_jokes: [],
    shared_goals: [],
    agreements: [],
  }, relDir);

  const secretsCount = countSecrets(secrets);
  debugLog(relDir, 'INFO', 'secrets', `total_entries=${secretsCount} jokes=${secrets.inside_jokes.length} goals=${secrets.shared_goals.length}`);

  // 4. Read stances
  const stance = readJsonSafe<Stance>(join(relDir, 'stance.json'), {
    values: [],
  }, relDir);
  debugLog(relDir, 'INFO', 'stance', `values=${stance.values.length}`);

  // 5. Recent events
  const timelineDir = join(relDir, 'timeline');
  let recentEvents: string[] = [];
  let totalEvents = 0;
  if (existsSync(timelineDir)) {
    const eventFiles = readdirSync(timelineDir)
      .filter((f) => f.endsWith('.md'))
      .sort();
    totalEvents = eventFiles.length;
    recentEvents = eventFiles
      .reverse()
      .slice(0, 3)
      .map((f) => f.replace('.md', '').replace(/^\d{4}-\d{2}-\d{2}-/, ''));
  }
  debugLog(relDir, 'INFO', 'timeline', `total_events=${totalEvents} recent=[${recentEvents.join(', ')}]`);

  // 6. Build context
  const lines: string[] = ['<relationship-context>'];

  // Stage info
  lines.push(
    `Stage: ${state.stage} (since ${state.stageStarted || 'unknown'}, ${state.interactionCount} interactions)`,
  );

  // Emotion baseline
  lines.push(`Mood baseline: ${getMoodLabel(state.emotionBaseline.valence)}`);

  // Pending threads
  if (pendingThreads.length > 0) {
    const threadSummaries = pendingThreads
      .slice(0, 3)
      .map((t) => `${t.context} (due ${t.followUpAt.split('T')[0]}, ${t.priority})`)
      .join('; ');
    lines.push(`Pending threads: ${pendingThreads.length} — ${threadSummaries}`);
  } else {
    lines.push('Pending threads: none');
  }

  // Active shared goals
  const activeGoals = secrets.shared_goals.filter((g) => g.status === 'active');
  if (activeGoals.length > 0) {
    lines.push(`Active shared goals: ${activeGoals.map((g) => g.goal).join(', ')}`);
  }

  // Stance reminders (only the strongest)
  const topStance = stance.values.sort((a, b) => b.strength - a.strength).slice(0, 2);
  if (topStance.length > 0) {
    lines.push(`Stance reminders: ${topStance.map((s) => s.position).join('; ')}`);
  }

  // Recent events
  if (recentEvents.length > 0) {
    lines.push(`Recent events: ${recentEvents.join(', ')}`);
  }

  // Recent milestone
  const recentMilestone = state.milestones[state.milestones.length - 1];
  if (recentMilestone) {
    lines.push(`Latest milestone: ${recentMilestone.note} (${recentMilestone.date})`);
  }

  lines.push('');
  lines.push('Follow relationship-os skill workflow for event capture and tone modulation.');
  lines.push('</relationship-context>');

  const contextStr = lines.join('\n');
  const tokenEstimate = Math.ceil(contextStr.length / 4);
  debugLog(relDir, 'INFO', 'bootstrap', `Injected context: ${contextStr.length} chars (~${tokenEstimate} tokens)`);
  debugLog(relDir, 'INFO', 'bootstrap', `Context content:\n${contextStr}`);
  debugLog(relDir, 'INFO', 'bootstrap', '========== Bootstrap Complete ==========');

  return contextStr;
}

// ====== Hook Entry Point ======

const handler: HookHandler = async (event) => {
  // Safety checks
  if (!event || typeof event !== 'object') return;
  if (event.type !== 'agent' || event.action !== 'bootstrap') return;
  if (!event.context || typeof event.context !== 'object') return;

  // Skip sub-agent sessions
  const sessionKey = event.sessionKey || '';
  if (sessionKey.includes(':subagent:')) return;

  // Get workspace dir from context
  const workspaceDir = event.context.workspaceDir as string;
  if (!workspaceDir) return;

  const relDir = join(workspaceDir, '.relationship');
  debugLog(relDir, 'INFO', 'hook', `Triggered agent:bootstrap — session=${sessionKey}`);

  // Build relationship context
  const context = buildRelationshipContext(workspaceDir);
  if (!context) {
    debugLog(relDir, 'WARN', 'hook', 'Context empty, skipping injection');
    return;
  }

  // Inject as virtual bootstrap file
  if (Array.isArray(event.context.bootstrapFiles)) {
    event.context.bootstrapFiles.push({
      path: 'RELATIONSHIP_CONTEXT.md',
      content: context,
      virtual: true,
    });
    debugLog(relDir, 'INFO', 'hook', 'Injected RELATIONSHIP_CONTEXT.md into bootstrapFiles');
  } else {
    debugLog(relDir, 'WARN', 'hook', 'bootstrapFiles is not an array, cannot inject');
  }
};

export default handler;
