// SECURITY MANIFEST:
//   Environment variables accessed: none
//   External endpoints called: none
//   Local files read: none
//   Local files written: none

// ─── Credential ─────────────────────────────────────────────

export interface Credential {
  authType: 'api_token' | 'cookie' | 'oauth';
  value: string;
  profile?: string;
  source: 'socialvault' | 'local';
}

// ─── Post & Scoring ─────────────────────────────────────────

export interface Post {
  id: string;
  url: string;
  title: string;
  body: string;
  author: string;
  createdAt: string; // ISO 8601
  platform: string;
  community?: string; // 吧名、知乎话题、B站分区等
  metadata?: Record<string, unknown>;
}

export interface ScoreBreakdown {
  relevance: number;
  intent: number;
  freshness: number;
  risk: number;
}

export interface ScoredPost extends Post {
  scores: ScoreBreakdown;
  finalScore: number;
}

// ─── Reply ──────────────────────────────────────────────────

export interface ReplyResult {
  success: boolean;
  replyId?: string;
  error?: string;
  mode?: 'api' | 'browser';
}

export interface ReplyDraft {
  postId: string;
  postUrl: string;
  postTitle: string;
  platform: string;
  content: string;
  score: number;
}

// ─── Auth / Check ───────────────────────────────────────────

export interface CheckResult {
  valid: boolean;
  username?: string;
  error?: string;
}

export type AuthMode = 'socialvault' | 'none';

// ─── Rate Limiting ──────────────────────────────────────────

export interface RateLimitInfo {
  requestsPerMinute: number;
  repliesPerDay: number;
  minReplyIntervalSeconds: number;
  notes: string;
}

export interface DailyLimits {
  approve: number;
  auto: number;
}

export const PLATFORM_DAILY_LIMITS: Record<string, DailyLimits> = {
  'bilibili':           { approve: 30, auto: 15 },
  'tieba':              { approve: 20, auto: 10 },
  'zhihu':              { approve: 10, auto: 5  },
  'xiaohongshu':        { approve: 10, auto: 5  },
  '_default':           { approve: 10, auto: 5  },
};

// ─── Platform Adapter ───────────────────────────────────────

export interface PlatformAdapter {
  readonly platformId: string;
  readonly platformName: string;

  search(
    keyword: string,
    timeRange: string,
    credential: Credential,
    target?: string,
  ): Promise<Post[]>;

  reply(
    postId: string,
    content: string,
    credential: Credential,
  ): Promise<ReplyResult>;

  check(credential: Credential): Promise<CheckResult>;

  rateLimitInfo(): RateLimitInfo;

  /**
   * Returns BrowserInstruction for Agent to execute search via browser tool.
   * Used as fallback when API search is blocked (403).
   */
  browserSearch?(
    keyword: string,
    target?: string,
  ): BrowserInstruction;
}

// ─── Interaction Log ────────────────────────────────────────

export interface InteractionLogEntry {
  timestamp: string; // ISO 8601
  platform: string;
  postId: string;
  postUrl: string;
  postTitle: string;
  author: string;
  replyContent: string;
  replyId?: string;
  score: number;
  mode: 'approve' | 'auto';
  success: boolean;
}

// ─── Brand Profile ──────────────────────────────────────────

export interface BrandProfile {
  businessName: string;
  description: string;
  keywords: string[];
  platforms: string[];
  mode: 'approve' | 'auto';
  threshold: number;
  language: string;
}

// ─── Scoring Config ─────────────────────────────────────────

export const SCORE_WEIGHTS = {
  relevance: 0.35,
  intent: 0.30,
  freshness: 0.20,
  risk: 0.15,
} as const;

export const DEFAULT_THRESHOLD = 0.6;
export const AUTO_MODE_MIN_THRESHOLD = 0.7;
export const AUTO_MODE_MIN_RISK = 0.5;

// ─── Browser Instruction (for adapter browser mode) ─────────

export const BROWSER_INSTRUCTION_ID = '__browser_instruction__';

export interface BrowserStep {
  action: 'navigate' | 'wait' | 'extract' | 'click' | 'type';
  url?: string;
  selector?: string;
  fields?: string[];
  text?: string;
}

export interface BrowserInstruction {
  mode: 'browser';
  action: 'search' | 'reply' | 'check';
  steps: BrowserStep[];
  cookies?: string;
}

// ─── Anti-Detection Helpers ──────────────────────────────────

const CHROME_VERSION = '131';

export function buildBrowserHeaders(cookie: string, extra?: Record<string, string>): Record<string, string> {
  return {
    'Cookie': cookie,
    'User-Agent': `Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/${CHROME_VERSION}.0.0.0 Safari/537.36`,
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Cache-Control': 'max-age=0',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'Sec-Ch-Ua': `"Chromium";v="${CHROME_VERSION}", "Not_A Brand";v="24"`,
    'Sec-Ch-Ua-Mobile': '?0',
    'Sec-Ch-Ua-Platform': '"Windows"',
    'Upgrade-Insecure-Requests': '1',
    ...extra,
  };
}

export function buildApiHeaders(cookie: string, extra?: Record<string, string>): Record<string, string> {
  return {
    'Cookie': cookie,
    'User-Agent': `Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/${CHROME_VERSION}.0.0.0 Safari/537.36`,
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Ch-Ua': `"Chromium";v="${CHROME_VERSION}", "Not_A Brand";v="24"`,
    'Sec-Ch-Ua-Mobile': '?0',
    'Sec-Ch-Ua-Platform': '"Windows"',
    ...extra,
  };
}

export async function fetchWithRetry(
  url: string,
  options: RequestInit,
  maxRetries = 3,
): Promise<Response> {
  let lastError: Error | null = null;
  for (let attempt = 0; attempt < maxRetries; attempt++) {
    if (attempt > 0) {
      const delay = Math.min(1000 * Math.pow(2, attempt) + Math.random() * 500, 8000);
      await new Promise(r => setTimeout(r, delay));
    }
    try {
      const response = await fetch(url, options);
      if (response.status === 403 && attempt < maxRetries - 1) {
        console.error(`[fetchWithRetry] 403 on attempt ${attempt + 1}, retrying...`);
        continue;
      }
      return response;
    } catch (err) {
      lastError = err as Error;
      console.error(`[fetchWithRetry] Attempt ${attempt + 1} failed: ${lastError.message}`);
    }
  }
  throw lastError ?? new Error('All retry attempts failed');
}

// ─── Cookie Parsing ─────────────────────────────────────────

export function parseCookieValue(raw: string, name: string): string | undefined {
  const match = raw.match(new RegExp(`(?:^|;\\s*)${name}=([^;]*)`));
  return match?.[1];
}

// ─── Utility types ──────────────────────────────────────────

export type ReplyMode = 'approve' | 'auto';

export interface PerformanceStats {
  total_replies: number;
  by_platform: Record<string, number>;
  by_date: Record<string, number>;
}
