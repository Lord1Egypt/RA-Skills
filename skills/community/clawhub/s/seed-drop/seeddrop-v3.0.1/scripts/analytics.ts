// SECURITY MANIFEST:
//   Environment variables accessed: none
//   External endpoints called: none
//   Local files read: memory/interaction-log.jsonl, memory/performance-stats.json
//   Local files written: memory/performance-stats.json, stdout (report)

import { readFileSync, writeFileSync, existsSync, mkdirSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import type { InteractionLogEntry, PerformanceStats } from './types.js';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
const BASE_DIR = join(__dirname, '..');

const LOG_PATH = join(BASE_DIR, 'memory', 'interaction-log.jsonl');
const STATS_PATH = join(BASE_DIR, 'memory', 'performance-stats.json');

// ─── Data Loading ───────────────────────────────────────────

function loadLog(): InteractionLogEntry[] {
  if (!existsSync(LOG_PATH)) return [];
  try {
    return readFileSync(LOG_PATH, 'utf-8')
      .split('\n')
      .filter((l: string) => l.trim())
      .map((l: string) => JSON.parse(l) as InteractionLogEntry);
  } catch (err) {
    console.error(`[analytics] Failed to load log: ${(err as Error).message}`);
    return [];
  }
}

function loadStats(): PerformanceStats {
  if (!existsSync(STATS_PATH)) {
    return { total_replies: 0, by_platform: {}, by_date: {} };
  }
  try {
    return JSON.parse(readFileSync(STATS_PATH, 'utf-8')) as PerformanceStats;
  } catch {
    return { total_replies: 0, by_platform: {}, by_date: {} };
  }
}

function saveStats(stats: PerformanceStats): void {
  const dir = dirname(STATS_PATH);
  if (!existsSync(dir)) mkdirSync(dir, { recursive: true });
  writeFileSync(STATS_PATH, JSON.stringify(stats, null, 2), 'utf-8');
}

// ─── Report Generation ─────────────────────────────────────

function filterByDateRange(entries: InteractionLogEntry[], daysBack: number): InteractionLogEntry[] {
  const cutoff = Date.now() - daysBack * 24 * 60 * 60 * 1000;
  return entries.filter(e => new Date(e.timestamp).getTime() >= cutoff);
}

function generateReport(entries: InteractionLogEntry[], label: string): object {
  const total = entries.length;
  const successful = entries.filter(e => e.success).length;
  const failed = total - successful;

  const byPlatform: Record<string, { total: number; success: number }> = {};
  const byDate: Record<string, number> = {};
  const byMode: Record<string, number> = { approve: 0, auto: 0 };
  const avgScore = total > 0
    ? entries.reduce((sum, e) => sum + e.score, 0) / total
    : 0;

  for (const entry of entries) {
    const plat = entry.platform;
    if (!byPlatform[plat]) byPlatform[plat] = { total: 0, success: 0 };
    byPlatform[plat].total++;
    if (entry.success) byPlatform[plat].success++;

    const dateKey = entry.timestamp.substring(0, 10);
    byDate[dateKey] = (byDate[dateKey] ?? 0) + 1;

    byMode[entry.mode] = (byMode[entry.mode] ?? 0) + 1;
  }

  return {
    report: label,
    period: {
      from: entries.length > 0 ? entries[0].timestamp : null,
      to: entries.length > 0 ? entries[entries.length - 1].timestamp : null,
    },
    summary: {
      total,
      successful,
      failed,
      successRate: total > 0 ? Math.round((successful / total) * 100) : 0,
      averageScore: Math.round(avgScore * 1000) / 1000,
    },
    byPlatform,
    byDate,
    byMode,
  };
}

function generateTuningAdvice(entries: InteractionLogEntry[]): object {
  const suggestions: string[] = [];

  if (entries.length === 0) {
    return { suggestions: ['No data yet. Run some monitoring cycles first.'] };
  }

  const avgScore = entries.reduce((s, e) => s + e.score, 0) / entries.length;
  if (avgScore < 0.6) {
    suggestions.push('Average score is low. Consider refining keywords in brand-profile.md to target more relevant discussions.');
  }
  if (avgScore > 0.85) {
    suggestions.push('Average score is very high. You might lower the threshold slightly to capture more opportunities.');
  }

  const successRate = entries.filter(e => e.success).length / entries.length;
  if (successRate < 0.7) {
    suggestions.push('Success rate is below 70%. Check credential validity and platform rate limits.');
  }

  const platformCounts: Record<string, number> = {};
  for (const e of entries) {
    platformCounts[e.platform] = (platformCounts[e.platform] ?? 0) + 1;
  }
  const platforms = Object.keys(platformCounts);
  if (platforms.length === 1) {
    suggestions.push(`All activity is on ${platforms[0]}. Consider expanding to other platforms for broader reach.`);
  }

  const hourBuckets = new Array<number>(24).fill(0);
  for (const e of entries) {
    const hour = new Date(e.timestamp).getHours();
    hourBuckets[hour]++;
  }
  const peakHour = hourBuckets.indexOf(Math.max(...hourBuckets));
  suggestions.push(`Peak activity hour: ${peakHour}:00. Consider scheduling monitoring around this time.`);

  if (suggestions.length === 0) {
    suggestions.push('Everything looks good! Keep the current configuration.');
  }

  return {
    tuning: 'advice',
    averageScore: Math.round(avgScore * 1000) / 1000,
    successRate: Math.round(successRate * 100),
    platformDistribution: platformCounts,
    peakHour,
    suggestions,
  };
}

// ─── Stats Update ───────────────────────────────────────────

function updateStats(entries: InteractionLogEntry[]): void {
  const stats = loadStats();

  stats.total_replies = entries.filter(e => e.success).length;
  stats.by_platform = {};
  stats.by_date = {};

  for (const entry of entries) {
    if (!entry.success) continue;
    stats.by_platform[entry.platform] = (stats.by_platform[entry.platform] ?? 0) + 1;
    const dateKey = entry.timestamp.substring(0, 10);
    stats.by_date[dateKey] = (stats.by_date[dateKey] ?? 0) + 1;
  }

  saveStats(stats);
  console.error('[analytics] performance-stats.json updated');
}

// ─── CLI Entry Point ────────────────────────────────────────

function main(): void {
  const args = process.argv.slice(2);
  const command = args[0] ?? 'daily';

  if (command === 'test') {
    const log = loadLog();
    const stats = loadStats();
    console.log(JSON.stringify({
      script: 'analytics',
      status: 'ok',
      logEntries: log.length,
      currentStats: stats,
    }));
    return;
  }

  const log = loadLog();

  switch (command) {
    case 'daily': {
      const today = filterByDateRange(log, 1);
      const report = generateReport(today, 'daily');
      updateStats(log);
      console.log(JSON.stringify(report, null, 2));
      break;
    }

    case 'weekly': {
      const week = filterByDateRange(log, 7);
      const report = generateReport(week, 'weekly');
      updateStats(log);
      console.log(JSON.stringify(report, null, 2));
      break;
    }

    case 'tune': {
      const recent = filterByDateRange(log, 14);
      const advice = generateTuningAdvice(recent);
      console.log(JSON.stringify(advice, null, 2));
      break;
    }

    default:
      console.error('Usage: analytics.ts <daily|weekly|tune|test>');
      process.exit(1);
  }
}

main();
