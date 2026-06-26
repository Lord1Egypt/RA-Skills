/**
 * Relationship OS — Bootstrap Hook (ESM)
 *
 * Injects relationship context summary on each agent session bootstrap.
 * Reads .relationship/ state files, generates ~150 token context injection.
 *
 * Debug log: .relationship/debug.log
 */

import { readFileSync, readdirSync, existsSync, appendFileSync } from 'fs';
import { join } from 'path';

// ====== Debug Logging ======

function debugLog(relDir, level, mod, msg) {
  try {
    const now = new Date().toISOString();
    const line = `[${now}] [${level}] [${mod}] ${msg}\n`;
    appendFileSync(join(relDir, 'debug.log'), line);
  } catch {
    // logging failure should not affect main flow
  }
}

// ====== Helpers ======

function readJsonSafe(filePath, fallback, relDir) {
  try {
    if (!existsSync(filePath)) {
      if (relDir) debugLog(relDir, 'WARN', 'io', `File not found: ${filePath}`);
      return fallback;
    }
    const data = JSON.parse(readFileSync(filePath, 'utf-8'));
    if (relDir) debugLog(relDir, 'INFO', 'io', `Read OK: ${filePath}`);
    return data;
  } catch (err) {
    if (relDir) debugLog(relDir, 'ERROR', 'io', `JSON parse failed: ${filePath} — ${err}`);
    return fallback;
  }
}

function getMoodLabel(valence) {
  if (valence > 0.3) return 'positive';
  if (valence < -0.3) return 'negative';
  if (valence > 0.1) return 'slightly positive';
  if (valence < -0.1) return 'slightly negative';
  return 'neutral';
}

// ====== Core Builder ======

function buildRelationshipContext(workspaceDir) {
  const relDir = join(workspaceDir, '.relationship');

  if (!existsSync(relDir)) {
    return '';
  }

  debugLog(relDir, 'INFO', 'bootstrap', '========== Relationship OS Bootstrap ==========');
  debugLog(relDir, 'INFO', 'bootstrap', `workspace: ${workspaceDir}`);

  // 1. Read state
  const state = readJsonSafe(join(relDir, 'state.json'), {
    stage: 'initial',
    stageStarted: '',
    interactionCount: 0,
    emotionBaseline: { valence: 0, arousal: 0 },
    userPatterns: { activeHours: [], avgMessagesPerDay: 0, lastSeen: '' },
    milestones: [],
  }, relDir);

  debugLog(relDir, 'INFO', 'state', `stage=${state.stage} interactions=${state.interactionCount} milestones=${(state.milestones || []).length}`);

  // 2. Read pending threads
  const threadsDir = join(relDir, 'threads');
  let pendingThreads = [];
  let totalThreads = 0;
  if (existsSync(threadsDir)) {
    const threadFiles = readdirSync(threadsDir).filter((f) => f.endsWith('.json'));
    totalThreads = threadFiles.length;
    for (const file of threadFiles) {
      const thread = readJsonSafe(join(threadsDir, file), null, relDir);
      if (thread && thread.status === 'pending') {
        pendingThreads.push(thread);
      }
    }
  }
  debugLog(relDir, 'INFO', 'threads', `total=${totalThreads} pending=${pendingThreads.length}`);

  // 3. Read shared secrets
  const secrets = readJsonSafe(join(relDir, 'secrets.json'), {
    nicknames: { user_calls_agent: [], agent_calls_user: [] },
    inside_jokes: [],
    shared_goals: [],
    agreements: [],
  }, relDir);

  const uNames = (secrets.nicknames && secrets.nicknames.user_calls_agent) || [];
  const aNames = (secrets.nicknames && secrets.nicknames.agent_calls_user) || [];
  const jokes = secrets.inside_jokes || [];
  const goals = secrets.shared_goals || [];
  const agreements = secrets.agreements || [];
  const secretsCount = uNames.length + aNames.length + jokes.length + goals.length + agreements.length;
  debugLog(relDir, 'INFO', 'secrets', `total_entries=${secretsCount} jokes=${jokes.length} goals=${goals.length}`);

  // 4. Read stance
  const stance = readJsonSafe(join(relDir, 'stance.json'), { values: [] }, relDir);
  const stanceValues = stance.values || [];
  debugLog(relDir, 'INFO', 'stance', `values=${stanceValues.length}`);

  // 5. Recent events
  const timelineDir = join(relDir, 'timeline');
  let recentEvents = [];
  let totalEvents = 0;
  if (existsSync(timelineDir)) {
    const eventFiles = readdirSync(timelineDir).filter((f) => f.endsWith('.md')).sort();
    totalEvents = eventFiles.length;
    recentEvents = eventFiles
      .reverse()
      .slice(0, 3)
      .map((f) => f.replace('.md', '').replace(/^\d{4}-\d{2}-\d{2}-/, ''));
  }
  debugLog(relDir, 'INFO', 'timeline', `total_events=${totalEvents} recent=[${recentEvents.join(', ')}]`);

  // 6. Build context
  const lines = ['<relationship-context>'];

  lines.push(`Stage: ${state.stage} (since ${state.stageStarted || 'unknown'}, ${state.interactionCount} interactions)`);
  lines.push(`Mood baseline: ${getMoodLabel((state.emotionBaseline || {}).valence || 0)}`);

  if (pendingThreads.length > 0) {
    const threadSummaries = pendingThreads
      .slice(0, 3)
      .map((t) => `${t.context} (due ${(t.followUpAt || '').split('T')[0]}, ${t.priority})`)
      .join('; ');
    lines.push(`Pending threads: ${pendingThreads.length} — ${threadSummaries}`);
  } else {
    lines.push('Pending threads: none');
  }

  const activeGoals = goals.filter((g) => g.status === 'active');
  if (activeGoals.length > 0) {
    lines.push(`Active shared goals: ${activeGoals.map((g) => g.goal).join(', ')}`);
  }

  const topStance = stanceValues.sort((a, b) => (b.strength || 0) - (a.strength || 0)).slice(0, 2);
  if (topStance.length > 0) {
    lines.push(`Stance reminders: ${topStance.map((s) => s.position).join('; ')}`);
  }

  if (recentEvents.length > 0) {
    lines.push(`Recent events: ${recentEvents.join(', ')}`);
  }

  const milestones = state.milestones || [];
  const recentMilestone = milestones[milestones.length - 1];
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

// ====== Hook Handler ======

const handler = async (event) => {
  // Safety checks
  if (!event || typeof event !== 'object') return;
  if (event.type !== 'agent' || event.action !== 'bootstrap') return;
  if (!event.context || typeof event.context !== 'object') return;

  // Skip sub-agent sessions
  const sessionKey = event.sessionKey || '';
  if (sessionKey.includes(':subagent:')) return;

  // Get workspace dir from context
  const workspaceDir = event.context.workspaceDir;
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
