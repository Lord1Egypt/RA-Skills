// SECURITY MANIFEST:
//   Environment variables accessed: none
//   External endpoints called: none (delegated to adapters)
//   Local files read: memory/brand-profile.md, memory/interaction-log.jsonl, memory/blacklist.md
//   Local files written: stdout (JSONL)

import { readFileSync, existsSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { getAdapter, listPlatforms } from './adapters/base.js';
import { getCredential } from './auth-bridge.js';
import type { Post, InteractionLogEntry } from './types.js';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
const BASE_DIR = join(__dirname, '..');

// ─── Brand Profile ──────────────────────────────────────────

interface MonitorConfig {
  keywords: string[];
  platforms: string[];
  timeRange: string;
}

function loadConfig(): MonitorConfig {
  const profilePath = join(BASE_DIR, 'memory', 'brand-profile.md');
  const defaults: MonitorConfig = {
    keywords: [],
    platforms: [],
    timeRange: 'day',
  };

  if (!existsSync(profilePath)) {
    console.error('[monitor] brand-profile.md not found');
    return defaults;
  }

  try {
    const raw = readFileSync(profilePath, 'utf-8');

    const kwMatch = raw.match(/##\s*关键词.*?\n([\s\S]*?)(?=\n##|\n$|$)/i)
      ?? raw.match(/##\s*Keywords.*?\n([\s\S]*?)(?=\n##|\n$|$)/i);
    if (kwMatch) {
      defaults.keywords = kwMatch[1]
        .split('\n')
        .map((l: string) => l.replace(/^[-*]\s*/, '').trim())
        .filter((l: string) => l.length > 0);
    }

    const platMatch = raw.match(/##\s*平台.*?\n([\s\S]*?)(?=\n##|\n$|$)/i)
      ?? raw.match(/##\s*Platforms.*?\n([\s\S]*?)(?=\n##|\n$|$)/i);
    if (platMatch) {
      defaults.platforms = platMatch[1]
        .split('\n')
        .map((l: string) => l.replace(/^[-*]\s*/, '').trim())
        .filter((l: string) => l.length > 0);
    }

    return defaults;
  } catch (err) {
    console.error(`[monitor] Failed to load config: ${(err as Error).message}`);
    return defaults;
  }
}

// ─── Deduplication ──────────────────────────────────────────

function loadRepliedPostIds(): Set<string> {
  const logPath = join(BASE_DIR, 'memory', 'interaction-log.jsonl');
  if (!existsSync(logPath)) return new Set();

  try {
    const raw = readFileSync(logPath, 'utf-8');
    const ids = new Set<string>();
    for (const line of raw.split('\n')) {
      if (!line.trim()) continue;
      try {
        const entry = JSON.parse(line) as InteractionLogEntry;
        ids.add(entry.postId);
      } catch { /* skip malformed lines */ }
    }
    return ids;
  } catch {
    return new Set();
  }
}

// ─── Blacklist ──────────────────────────────────────────────

interface Blacklist {
  users: string[];
  communities: string[];
  keywords: string[];
}

function loadBlacklist(): Blacklist {
  const path = join(BASE_DIR, 'memory', 'blacklist.md');
  const defaults: Blacklist = { users: [], communities: [], keywords: [] };

  if (!existsSync(path)) return defaults;

  try {
    const raw = readFileSync(path, 'utf-8');
    let currentSection = '';

    for (const line of raw.split('\n')) {
      const sectionMatch = line.match(/^##\s*(.+)/);
      if (sectionMatch) {
        currentSection = sectionMatch[1].toLowerCase();
        continue;
      }
      const item = line.replace(/^[-*]\s*/, '').trim();
      if (!item || item.startsWith('#')) continue;

      if (currentSection.includes('用户') || currentSection.includes('user')) {
        defaults.users.push(item.toLowerCase());
      } else if (currentSection.includes('社区') || currentSection.includes('communit') || currentSection.includes('subreddit')) {
        defaults.communities.push(item.toLowerCase());
      } else if (currentSection.includes('关键词') || currentSection.includes('keyword')) {
        defaults.keywords.push(item.toLowerCase());
      }
    }

    return defaults;
  } catch {
    return defaults;
  }
}

function isBlacklisted(post: Post, blacklist: Blacklist): boolean {
  if (blacklist.users.includes(post.author.toLowerCase())) return true;
  if (post.community && blacklist.communities.includes(post.community.toLowerCase())) return true;

  const text = `${post.title} ${post.body}`.toLowerCase();
  for (const kw of blacklist.keywords) {
    if (text.includes(kw)) return true;
  }

  return false;
}

// ─── Main Monitor Logic ─────────────────────────────────────

async function monitorPlatform(
  platformId: string,
  keywords: string[],
  timeRange: string,
  target?: string,
): Promise<Post[]> {
  const adapter = await getAdapter(platformId);
  const cred = getCredential(platformId);

  if (!cred) {
    console.error(`[monitor] No credentials for ${platformId}, skipping`);
    return [];
  }

  if (cred.value.startsWith('__socialvault_pending__:')) {
    console.error(`[monitor] SocialVault credential pending for ${platformId}`);
    console.error(`[monitor] Agent should run: ${cred.value.replace('__socialvault_pending__:', '')}`);
    console.error(`[monitor] Then re-run monitor with valid credentials`);
    return [];
  }

  const allPosts: Post[] = [];
  for (const keyword of keywords) {
    console.error(`[monitor] Searching ${platformId} for "${keyword}" (range: ${timeRange})${target ? ` in ${target}` : ''}`);
    const posts = await adapter.search(keyword, timeRange, cred, target);
    allPosts.push(...posts);
  }

  const uniquePosts = new Map<string, Post>();
  for (const post of allPosts) {
    if (!uniquePosts.has(post.id)) {
      uniquePosts.set(post.id, post);
    }
  }

  return Array.from(uniquePosts.values());
}

// ─── CLI Entry Point ────────────────────────────────────────

async function main(): Promise<void> {
  const args = process.argv.slice(2);

  if (args[0] === 'test') {
    const config = loadConfig();
    const blacklist = loadBlacklist();
    const repliedIds = loadRepliedPostIds();
    console.log(JSON.stringify({
      script: 'monitor',
      status: 'ok',
      config,
      blacklistCounts: {
        users: blacklist.users.length,
        communities: blacklist.communities.length,
        keywords: blacklist.keywords.length,
      },
      repliedPostCount: repliedIds.size,
      availablePlatforms: listPlatforms(),
    }));
    return;
  }

  const platformArg = args[0];
  const targetArg = args[1]; // e.g. specific community (吧名, 分区等)

  if (!platformArg) {
    console.error('Usage: monitor.ts <platform|all> [target]');
    console.error(`Available platforms: ${listPlatforms().join(', ')}`);
    process.exit(1);
  }

  const config = loadConfig();
  if (config.keywords.length === 0) {
    console.error('[monitor] No keywords configured in brand-profile.md');
    console.error('[monitor] Run "seeddrop setup" to configure keywords');
    process.exit(1);
  }

  const blacklist = loadBlacklist();
  const repliedIds = loadRepliedPostIds();

  const platforms = platformArg === 'all'
    ? (config.platforms.length > 0 ? config.platforms : listPlatforms())
    : [platformArg];

  let totalOutput = 0;

  for (const plat of platforms) {
    try {
      const posts = await monitorPlatform(plat, config.keywords, config.timeRange, targetArg);
      console.error(`[monitor] ${plat}: found ${posts.length} raw posts`);

      for (const post of posts) {
        if (repliedIds.has(post.id)) {
          console.error(`[monitor] SKIP ${post.id}: already replied`);
          continue;
        }
        if (isBlacklisted(post, blacklist)) {
          console.error(`[monitor] SKIP ${post.id}: blacklisted`);
          continue;
        }
        console.log(JSON.stringify(post));
        totalOutput++;
      }
    } catch (err) {
      console.error(`[monitor] Error monitoring ${plat}: ${(err as Error).message}`);
    }
  }

  console.error(`[monitor] Total output: ${totalOutput} posts`);
}

main().catch(err => {
  console.error(`[monitor] Fatal error: ${(err as Error).message}`);
  process.exit(1);
});
