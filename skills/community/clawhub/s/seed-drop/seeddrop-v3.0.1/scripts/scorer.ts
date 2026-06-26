// SECURITY MANIFEST:
//   Environment variables accessed: none
//   External endpoints called: none
//   Local files read: stdin (JSONL), memory/brand-profile.md
//   Local files written: stdout (JSONL)

import { readFileSync, existsSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { createInterface } from 'node:readline';
import type { Post, ScoredPost, ScoreBreakdown } from './types.js';
import {
  SCORE_WEIGHTS,
  DEFAULT_THRESHOLD,
  AUTO_MODE_MIN_THRESHOLD,
  AUTO_MODE_MIN_RISK,
} from './types.js';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
const BASE_DIR = join(__dirname, '..');

// ─── Brand Profile Loading ──────────────────────────────────

interface ParsedBrandProfile {
  keywords: string[];
  mode: 'approve' | 'auto';
  threshold: number;
}

function loadBrandProfile(): ParsedBrandProfile {
  const profilePath = join(BASE_DIR, 'memory', 'brand-profile.md');
  const defaults: ParsedBrandProfile = {
    keywords: [],
    mode: 'approve',
    threshold: DEFAULT_THRESHOLD,
  };

  if (!existsSync(profilePath)) {
    console.error('[scorer] brand-profile.md not found, using defaults');
    return defaults;
  }

  try {
    const raw = readFileSync(profilePath, 'utf-8');

    const keywordsMatch = raw.match(/##\s*关键词.*?\n([\s\S]*?)(?=\n##|\n$|$)/i)
      ?? raw.match(/##\s*Keywords.*?\n([\s\S]*?)(?=\n##|\n$|$)/i);
    if (keywordsMatch) {
      defaults.keywords = keywordsMatch[1]
        .split('\n')
        .map((l: string) => l.replace(/^[-*]\s*/, '').trim())
        .filter((l: string) => l.length > 0);
    }

    const modeMatch = raw.match(/模式[：:]\s*(approve|auto)/i)
      ?? raw.match(/mode[：:]\s*(approve|auto)/i);
    if (modeMatch) {
      defaults.mode = modeMatch[1].toLowerCase() as 'approve' | 'auto';
    }

    const thresholdMatch = raw.match(/阈值[：:]\s*([\d.]+)/i)
      ?? raw.match(/threshold[：:]\s*([\d.]+)/i);
    if (thresholdMatch) {
      defaults.threshold = parseFloat(thresholdMatch[1]);
    }

    return defaults;
  } catch (err) {
    console.error(`[scorer] Failed to load brand profile: ${(err as Error).message}`);
    return defaults;
  }
}

// ─── Scoring Functions ──────────────────────────────────────

const INTENT_KEYWORDS = {
  high: ['求推荐', '怎么', '有什么好的', '推荐一下', '求助', '请问', '有没有推荐', '怎么选', '怎么办', 'how to', 'recommend', 'help', 'looking for'],
  medium: ['讨论', '大家觉得', '有没有人用过', '有经验', '分享一下', '什么体验', '值不值', 'what do you think', 'experience'],
  low: ['坑', '吐槽', '垃圾', '难用', '太差了', '后悔', '避雷', 'frustrated', 'terrible'],
};

function scoreRelevance(post: Post, keywords: string[]): number {
  if (keywords.length === 0) return 0.5;

  const text = `${post.title} ${post.body}`.toLowerCase();
  let hits = 0;
  for (const kw of keywords) {
    if (text.includes(kw.toLowerCase())) hits++;
  }

  const ratio = hits / keywords.length;
  if (ratio > 0.5) return 1.0;
  if (ratio > 0.2) return 0.7;
  if (ratio > 0) return 0.5;
  return 0.2;
}

function scoreIntent(post: Post): number {
  const text = `${post.title} ${post.body}`.toLowerCase();

  for (const kw of INTENT_KEYWORDS.high) {
    if (text.includes(kw)) return 0.9;
  }
  for (const kw of INTENT_KEYWORDS.medium) {
    if (text.includes(kw)) return 0.7;
  }
  for (const kw of INTENT_KEYWORDS.low) {
    if (text.includes(kw)) return 0.5;
  }
  return 0.3;
}

function scoreFreshness(post: Post): number {
  const ageMs = Date.now() - new Date(post.createdAt).getTime();
  const ageHours = ageMs / (1000 * 60 * 60);

  if (ageHours <= 2) return 1.0;
  if (ageHours <= 6) return 0.9;
  if (ageHours <= 12) return 0.8;
  if (ageHours <= 24) return 0.6;
  if (ageHours <= 48) return 0.4;
  return 0.2;
}

function scoreRisk(post: Post): number {
  const text = `${post.title} ${post.body}`.toLowerCase();

  const officialMarkers = ['[meta]', '[announcement]', '[mod]', '[official]', '置顶', 'pinned'];
  for (const marker of officialMarkers) {
    if (text.includes(marker)) return 0.3;
  }

  const controversialMarkers = ['politic', 'religion', 'controversial', '政治', '宗教', '敏感'];
  for (const marker of controversialMarkers) {
    if (text.includes(marker)) return 0.2;
  }

  return 0.9;
}

export function scorePost(post: Post, keywords: string[]): ScoredPost {
  const scores: ScoreBreakdown = {
    relevance: scoreRelevance(post, keywords),
    intent: scoreIntent(post),
    freshness: scoreFreshness(post),
    risk: scoreRisk(post),
  };

  const finalScore =
    scores.relevance * SCORE_WEIGHTS.relevance +
    scores.intent * SCORE_WEIGHTS.intent +
    scores.freshness * SCORE_WEIGHTS.freshness +
    scores.risk * SCORE_WEIGHTS.risk;

  return { ...post, scores, finalScore: Math.round(finalScore * 1000) / 1000 };
}

// ─── CLI Entry Point ────────────────────────────────────────

async function main(): Promise<void> {
  const args = process.argv.slice(2);

  if (args[0] === 'test') {
    const testPost: Post = {
      id: 'test1',
      url: 'https://reddit.com/r/test/test1',
      title: 'How to build a landing page?',
      body: 'Looking for recommendations on tools to build a quick landing page.',
      author: 'testuser',
      createdAt: new Date().toISOString(),
      platform: 'reddit',
    };
    const result = scorePost(testPost, ['landing page', 'build', 'tool']);
    console.log(JSON.stringify({
      script: 'scorer',
      status: 'ok',
      testResult: result,
    }));
    return;
  }

  const thresholdArg = parseFloat(args[0] || '');
  const profile = loadBrandProfile();
  const threshold = !isNaN(thresholdArg) ? thresholdArg : profile.threshold;

  const effectiveThreshold = profile.mode === 'auto'
    ? Math.max(threshold, AUTO_MODE_MIN_THRESHOLD)
    : threshold;

  console.error(`[scorer] Mode: ${profile.mode}, Threshold: ${effectiveThreshold}, Keywords: ${profile.keywords.length}`);

  const rl = createInterface({ input: process.stdin, terminal: false });
  let inputCount = 0;
  let passedCount = 0;

  for await (const line of rl) {
    if (!line.trim()) continue;
    try {
      const post = JSON.parse(line) as Post;
      inputCount++;

      const scored = scorePost(post, profile.keywords);

      if (scored.finalScore < effectiveThreshold) {
        console.error(`[scorer] SKIP ${scored.id} (score=${scored.finalScore} < ${effectiveThreshold})`);
        continue;
      }

      if (profile.mode === 'auto' && scored.scores.risk < AUTO_MODE_MIN_RISK) {
        console.error(`[scorer] SKIP ${scored.id} (risk=${scored.scores.risk} < ${AUTO_MODE_MIN_RISK}, auto mode)`);
        continue;
      }

      passedCount++;
      console.log(JSON.stringify(scored));
    } catch {
      console.error(`[scorer] Failed to parse line: ${line.substring(0, 80)}`);
    }
  }

  console.error(`[scorer] Done: ${passedCount}/${inputCount} posts passed threshold`);
}

main().catch(err => {
  console.error(`[scorer] Fatal error: ${(err as Error).message}`);
  process.exit(1);
});
