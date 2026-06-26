// SECURITY MANIFEST:
//   Environment variables accessed: none
//   External endpoints called: none (reply sending delegated to adapters via Agent)
//   Local files read: stdin (JSONL), memory/interaction-log.jsonl, memory/brand-profile.md
//   Local files written: stdout (drafts/results), memory/interaction-log.jsonl

import { readFileSync, appendFileSync, existsSync, mkdirSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { createInterface } from 'node:readline';
import type {
  ScoredPost,
  InteractionLogEntry,
  ReplyDraft,
  ReplyMode,
} from './types.js';
import { PLATFORM_DAILY_LIMITS } from './types.js';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
const BASE_DIR = join(__dirname, '..');

const LOG_PATH = join(BASE_DIR, 'memory', 'interaction-log.jsonl');

// ─── Interaction Log ────────────────────────────────────────

function loadInteractionLog(): InteractionLogEntry[] {
  if (!existsSync(LOG_PATH)) return [];
  try {
    const raw = readFileSync(LOG_PATH, 'utf-8');
    return raw
      .split('\n')
      .filter((l: string) => l.trim())
      .map((l: string) => JSON.parse(l) as InteractionLogEntry);
  } catch (err) {
    console.error(`[responder] Failed to load interaction log: ${(err as Error).message}`);
    return [];
  }
}

export function appendToLog(entry: InteractionLogEntry): void {
  const dir = dirname(LOG_PATH);
  if (!existsSync(dir)) mkdirSync(dir, { recursive: true });
  appendFileSync(LOG_PATH, JSON.stringify(entry) + '\n', 'utf-8');
}

// ─── Deduplication & Safety Checks ──────────────────────────

function isAlreadyReplied(postId: string, log: InteractionLogEntry[]): boolean {
  return log.some(entry => entry.postId === postId);
}

function isAuthorCoolingDown(author: string, platform: string, log: InteractionLogEntry[]): boolean {
  const cutoff = Date.now() - 24 * 60 * 60 * 1000;
  return log.some(
    entry =>
      entry.author === author &&
      entry.platform === platform &&
      new Date(entry.timestamp).getTime() > cutoff,
  );
}

function getTodayReplyCount(platform: string, log: InteractionLogEntry[]): number {
  const todayStart = new Date();
  todayStart.setHours(0, 0, 0, 0);
  const cutoff = todayStart.getTime();

  return log.filter(
    entry =>
      entry.platform === platform &&
      entry.success &&
      new Date(entry.timestamp).getTime() >= cutoff,
  ).length;
}

function getDailyLimit(platform: string, mode: ReplyMode): number {
  const limits = PLATFORM_DAILY_LIMITS[platform] ?? PLATFORM_DAILY_LIMITS['_default']!;
  return mode === 'auto' ? limits.auto : limits.approve;
}

// ─── Reply Draft Generation ─────────────────────────────────

function generateDraft(post: ScoredPost): ReplyDraft {
  return {
    postId: post.id,
    postUrl: post.url,
    postTitle: post.title,
    platform: post.platform,
    content: `__DRAFT_PLACEHOLDER__`,
    score: post.finalScore,
  };
}

// ─── CLI Entry Point ────────────────────────────────────────

async function main(): Promise<void> {
  const args = process.argv.slice(2);

  if (args[0] === 'test') {
    const log = loadInteractionLog();
    console.log(JSON.stringify({
      script: 'responder',
      status: 'ok',
      logEntries: log.length,
      logPath: LOG_PATH,
    }));
    return;
  }

  // SECURITY: Only approve mode is supported - no auto-reply to prevent abuse
  const mode: ReplyMode = 'approve';
  if (args[0] === 'auto') {
    console.error('[responder] SECURITY: Auto mode is disabled. All replies require manual approval.');
    process.exit(1);
  }

  console.error(`[responder] Mode: ${mode} (manual approval required)`);

  const log = loadInteractionLog();
  const rl = createInterface({ input: process.stdin, terminal: false });
  let inputCount = 0;
  let draftCount = 0;
  let skipDup = 0;
  let skipAuthor = 0;
  let skipLimit = 0;

  for await (const line of rl) {
    if (!line.trim()) continue;
    try {
      const post = JSON.parse(line) as ScoredPost;
      inputCount++;

      if (isAlreadyReplied(post.id, log)) {
        console.error(`[responder] SKIP ${post.id}: already replied`);
        skipDup++;
        continue;
      }

      if (isAuthorCoolingDown(post.author, post.platform, log)) {
        console.error(`[responder] SKIP ${post.id}: author "${post.author}" cooldown (24h)`);
        skipAuthor++;
        continue;
      }

      const dailyLimit = getDailyLimit(post.platform, mode);
      const todayCount = getTodayReplyCount(post.platform, log);
      if (todayCount >= dailyLimit) {
        console.error(`[responder] SKIP ${post.id}: daily limit reached (${todayCount}/${dailyLimit})`);
        skipLimit++;
        continue;
      }

      const draft = generateDraft(post);

      if (mode === 'approve') {
        console.log(JSON.stringify({
          action: 'review_draft',
          draft,
          post: {
            id: post.id,
            url: post.url,
            title: post.title,
            body: post.body.substring(0, 300),
            author: post.author,
            platform: post.platform,
            community: post.community,
            scores: post.scores,
            finalScore: post.finalScore,
          },
          instructions: `Generate a value-first reply for this ${post.platform} post. Follow the template at templates/reply-${post.platform}.md. Brand mention ≤20%. Then present the draft to the user for approval.`,
        }));
      } else {
        console.log(JSON.stringify({
          action: 'auto_reply',
          draft,
          post: {
            id: post.id,
            url: post.url,
            title: post.title,
            body: post.body.substring(0, 300),
            author: post.author,
            platform: post.platform,
            community: post.community,
            scores: post.scores,
            finalScore: post.finalScore,
          },
          instructions: `Generate and send a value-first reply for this ${post.platform} post. Follow the template at templates/reply-${post.platform}.md. Brand mention ≤20%. Log the result to interaction-log.jsonl.`,
        }));
      }

      draftCount++;
    } catch {
      console.error(`[responder] Failed to parse line: ${line.substring(0, 80)}`);
    }
  }

  console.error(`[responder] Done: ${draftCount} drafts from ${inputCount} posts (skipped: ${skipDup} dup, ${skipAuthor} author, ${skipLimit} limit)`);
}

main().catch(err => {
  console.error(`[responder] Fatal error: ${(err as Error).message}`);
  process.exit(1);
});
